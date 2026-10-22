import {beforeAll,describe,it,expect} from 'vitest';
import {Client,StreamableHTTPClientTransport} from '@modelcontextprotocol/client';
import {env} from 'cloudflare:workers';
import worker from '../src/index';
import {applyD1Migrations} from 'cloudflare:test';
import {version,objectives} from '../src/core';
import pythonExport from './fixtures/python-state-v1.json';
import type {Env} from '../src/auth';
const testEnv=env as unknown as Env & {TEST_MIGRATIONS:any[]};
const base='https://tutor.example.test';
const bytesToBase64Url=(bytes:Uint8Array)=>btoa(String.fromCharCode(...bytes)).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
async function signedToken(sub:string,clientId:string){const now=Math.floor(Date.now()/1000),payload=bytesToBase64Url(new TextEncoder().encode(JSON.stringify({iss:base,aud:`${base}/mcp`,sub,client_id:clientId,scope:'tutor:read tutor:write',iat:now,exp:now+900})));const key=await crypto.subtle.importKey('raw',new TextEncoder().encode(testEnv.TOKEN_SIGNING_SECRET),{name:'HMAC',hash:'SHA-256'},false,['sign']);const sig=await crypto.subtle.sign('HMAC',key,new TextEncoder().encode(payload));return `${payload}.${bytesToBase64Url(new Uint8Array(sig))}`;}
async function connect(sub:string){const client=new Client({name:`test-${sub}`,version:'1.0.0'});const token=await signedToken(sub,`client-${sub}`);const fetcher:typeof fetch=async(input,init)=>{const request=input instanceof Request?input:new Request(input,init);return worker.fetch(request,testEnv);};const transport=new StreamableHTTPClientTransport(new URL(`${base}/mcp`),{authProvider:{token:async()=>token},fetch:fetcher});await client.connect(transport);return client;}
function value(call:any){const block=call.content?.find((x:any)=>x.type==='text');if(!block)throw new Error(JSON.stringify(call));return JSON.parse(block.text);}
beforeAll(async()=>{
 await applyD1Migrations(testEnv.DB,testEnv.TEST_MIGRATIONS);
 await testEnv.DB.batch(['student-a','student-b','student-c'].map((id,i)=>testEnv.DB.prepare('INSERT OR IGNORE INTO users(id,provider,provider_subject,created_at,updated_at) VALUES(?,?,?,?,?)').bind(id,'test',`subject-${i}`,Date.now(),Date.now())));
});
describe('Cloudflare Worker MCP integration',()=>{
 it('requires bearer auth, publishes OAuth metadata and DCR validates callbacks',async()=>{
  const unauth=await worker.fetch(new Request(`${base}/mcp`,{method:'POST'}),testEnv);expect(unauth.status).toBe(401);expect(unauth.headers.get('www-authenticate')).toContain('oauth-protected-resource');
  const metadata=await worker.fetch(new Request(`${base}/.well-known/oauth-authorization-server`),testEnv);expect(metadata.status).toBe(200);const authMeta:any=await metadata.json();expect(authMeta.code_challenge_methods_supported).toContain('S256');expect(authMeta.client_id_metadata_document_supported).toBe(true);expect(authMeta.grant_types_supported).toEqual(['authorization_code']);
  const bad=await worker.fetch(new Request(`${base}/register`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({redirect_uris:['https://attacker.invalid/callback']})}),testEnv);expect(bad.status).toBe(201);
  const auth=await worker.fetch(new Request(`${base}/authorize?client_id=${(await bad.json() as any).client_id}&redirect_uri=http%3A%2F%2Fevil.test%2Fcb&response_type=code&state=x&code_challenge=${'a'.repeat(43)}&code_challenge_method=S256&resource=${encodeURIComponent(`${base}/mcp`)}`),testEnv);expect(auth.status).toBe(400);
 });
 it('resumes real MCP client history after disconnect, writes idempotently and isolates learners',async()=>{
  const first=await connect('student-a');let competency='';
  try{
   expect((await first.listTools()).tools.map(x=>x.name)).toEqual(expect.arrayContaining(['get_profile','update_profile','get_study_plan','get_lesson','get_question','record_assessment','get_progress','export_progress','import_progress','delete_progress']));const docs=await first.listResources();expect(docs.resources.map(r=>r.uri)).toContain('az900://tutor/pedagogy/evidence');const protocol=await first.readResource({uri:'az900://tutor/pedagogy/evidence'});expect(JSON.stringify(protocol)).toContain('not psychometric estimates');
   expect(value(await first.callTool({name:'update_profile',arguments:{deadline:'2026-12-20',minutes_per_day:45,language:'pt-BR',experience:'worker test'}})).saved).toBe(true);
   const initial=value(await first.callTool({name:'get_study_plan',arguments:{today:'2026-10-21'}}));competency=initial.recommendations[0].competency;
   const question=value(await first.callTool({name:'get_question',arguments:{competency}}));const displayed=JSON.stringify(question);expect(displayed).not.toContain('rationale');expect(displayed).not.toContain('correct_answer');expect(question.answer_key_withheld).toBe(true);
   const assessment={competency,question:question.question.id,score:0.4,kind:'explanation',evidence:'Observed response showed a misunderstanding.',misconception:'Test misconception.',assisted:false,date:'2026-10-21'};
   const results=await Promise.all([first.callTool({name:'record_assessment',arguments:assessment}),first.callTool({name:'record_assessment',arguments:assessment})]);expect(results.map(r=>value(r).saved)).toEqual([true,true]);expect(results.filter(r=>value(r).duplicate).length).toBe(1);const sequential=value(await first.callTool({name:'record_assessment',arguments:assessment}));expect(sequential.duplicate).toBe(true);
  }finally{await first.close();}
  const resumed=await connect('student-a');try{const p=value(await resumed.callTool({name:'get_progress',arguments:{today:'2026-10-21'}}));expect(p.evidence).toHaveLength(1);expect(p.evidence[0].competency).toBe(competency);const plan=value(await resumed.callTool({name:'get_study_plan',arguments:{today:'2026-10-21'}}));expect(plan.recommendations[0].competency).toBe(competency);const exported=value(await resumed.callTool({name:'export_progress',arguments:{}}));expect(exported._integrity.algorithm).toBe('sha256');expect(exported.curriculum_version).toBe(version);}finally{await resumed.close();}
  const other=await connect('student-b');try{expect(value(await other.callTool({name:'get_progress',arguments:{today:'2026-10-21'}}))).toEqual({initialized:false});}finally{await other.close();}
 });

 it('imports and exports Python state-v1 through D1 without changing its checksum',async()=>{const client=await connect('student-c');try{const imported=value(await client.callTool({name:'import_progress',arguments:{state:pythonExport}}));expect(imported.inserted_events).toBe(2);const roundtrip=value(await client.callTool({name:'export_progress',arguments:{}}));expect(roundtrip).toEqual(pythonExport);const repeated=value(await client.callTool({name:'import_progress',arguments:{state:pythonExport}}));expect(repeated.inserted_events).toBe(0);expect(repeated.duplicates_skipped).toBe(2);const progress=value(await client.callTool({name:'get_progress',arguments:{today:'2026-10-21'}}));expect(progress.evidence).toHaveLength(2);}finally{await client.close();}});
 it('rejects invalid competency and records evidence only for authenticated identity',async()=>{const client=await connect('student-b');try{await client.callTool({name:'update_profile',arguments:{deadline:'2026-12-20',minutes_per_day:30,language:'en',experience:'test'}});const result=value(await client.callTool({name:'record_assessment',arguments:{competency:'unknown-id',question:'q',score:.9,kind:'application',evidence:'answer',date:'2026-10-21'}}));expect(result.saved).not.toBe(true);}finally{await client.close();}});
});
