import content from './content.json';

export type Event = {competency:string;question:string;score:number;kind:'recall'|'explanation'|'application';evidence:string;misconception:string;assisted:boolean;date:string;requires_reassessment?:boolean};
export type State = {schema_version:1;curriculum_version:string;profile:Record<string,unknown>;events:Event[];migration?:unknown};
const curriculum=(content as any).curriculum;
export const objectives: any[] = curriculum.competencies ?? curriculum.objectives;
export const version = objectives[0].exam_version as string;
export const questions: any[] = (content as any).questions.questions;
export const lessons: any[] = (content as any).lessons.units;
const known = new Set(objectives.map(o=>o.id));
const enc = new TextEncoder();
function jsonCanonical(value:any,key=''):string {
  if (Array.isArray(value)) return `[${value.map(v=>jsonCanonical(v)).join(',')}]`;
  if (value && typeof value==='object') return `{${Object.keys(value).sort().map(k=>`${JSON.stringify(k)}:${jsonCanonical(value[k],k)}`).join(',')}}`;
  if (typeof value==='string') return JSON.stringify(value);
  if (typeof value==='number') return key==='score'&&Number.isInteger(value)?`${value}.0`:String(value);
  return JSON.stringify(value);
}
export function canonicalJson(value:any):string { return jsonCanonical(value); }
export async function sha256(value:any):Promise<string> {
  const bytes=await crypto.subtle.digest('SHA-256',enc.encode(canonicalJson(value)));
  return [...new Uint8Array(bytes)].map(b=>b.toString(16).padStart(2,'0')).join('');
}
export async function validateState(s:any,expected=version,ids:Set<string>|string[]=known):Promise<State> {
  if (!s || s.schema_version!==1) throw new Error('Unsupported learner schema; expected schema_version 1');
  if (s.curriculum_version!==expected) throw new Error('Curriculum version differs; review objectives before migration');
  if (!s.profile || typeof s.profile!=='object' || Array.isArray(s.profile) || !Array.isArray(s.events)) throw new Error('Profile must be an object and events must be an array');
  if (!Number.isInteger(s.profile.minutes_per_day) || s.profile.minutes_per_day<=0) throw new Error('minutes_per_day must be a positive integer');
  isoDate(s.profile.deadline);
  const accepted=ids instanceof Set?ids:new Set(ids);
  const seen=new Set<string>();
  for (const e of s.events) {
    if (!e || !accepted.has(e.competency)) throw new Error('Unknown competency in event');
    if (typeof e.score!=='number' || !Number.isFinite(e.score) || e.score<0 || e.score>1) throw new Error('Score must be finite and between 0 and 1');
    if (!['recall','explanation','application'].includes(e.kind)) throw new Error('Unknown evidence kind');
    for(const k of ['question','evidence','misconception']) if(typeof e[k]!=='string') throw new Error(`Event ${k} must be text`);
    if(!e.question.trim()||!e.evidence.trim()) throw new Error('Question and evidence cannot be empty');
    const d=isoDate(e.date); if(d>new Date().toISOString().slice(0,10)) throw new Error('Future assessment evidence is invalid');
    if(typeof e.assisted!=='boolean') throw new Error('assisted must be boolean');
    if(e.requires_reassessment!==undefined && typeof e.requires_reassessment!=='boolean') throw new Error('requires_reassessment must be boolean');
    const fp=await sha256(e); if(seen.has(fp)) throw new Error('Duplicate evidence event; retrying the same record does not add evidence'); seen.add(fp);
  }
  return s as State;
}
export function isoDate(value:any):string {
  if(typeof value!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(value)||new Date(`${value}T00:00:00.000Z`).toISOString().slice(0,10)!==value) throw new Error('Date must use canonical YYYY-MM-DD format');
  return value;
}
export async function exportState(state:State):Promise<any> { return {...state,_integrity:{algorithm:'sha256',digest:await sha256(state)}}; }
export async function importState(payload:any,expected=version,ids:Set<string>|string[]=known):Promise<State> {
  if(!payload||typeof payload!=='object'||Array.isArray(payload)) throw new Error('Import must be a JSON object');
  const {_integrity,...state}=payload;
  if(_integrity) {
    const integerScoreDigest=await sha256WithIntegerScores(state);
    if(_integrity.algorithm!=='sha256'||(_integrity.digest!==await sha256(state)&&_integrity.digest!==integerScoreDigest)) throw new Error('Export integrity check failed; original file remains unchanged');
  }
  return validateState(state,expected,ids);
}
async function sha256WithIntegerScores(value:any):Promise<string>{
 const normalize=(v:any):any=>Array.isArray(v)?v.map(normalize):v&&typeof v==='object'?Object.fromEntries(Object.entries(v).map(([k,x])=>[k,k==='score'&&typeof x==='number'&&Number.isInteger(x)?{__integer_score__:x}:normalize(x)])):v;
 const walk=(v:any):string=>Array.isArray(v)?`[${v.map(walk).join(',')}]`:v&&typeof v==='object'?(Object.keys(v).length===1&&'__integer_score__' in v?String(v.__integer_score__):`{${Object.keys(v).sort().map(k=>`${JSON.stringify(k)}:${walk(v[k])}`).join(',')}}`):JSON.stringify(v);
 const marked=normalize(value);
 const d=await crypto.subtle.digest('SHA-256',enc.encode(walk(marked)));return [...new Uint8Array(d)].map(b=>b.toString(16).padStart(2,'0')).join('');
}
export function exportText(payload:any){return JSON.stringify(payload,null,2).replace(/(\"score\"\s*:\s*)(-?\d+)(?=,|\n)/g,'$1$2.0')+'\n';}
export async function eventHash(event:Event){return sha256(event);}
export function activeEvents(s:State){return s.events.filter(e=>!e.requires_reassessment);}
export function competencyStatus(events:Event[],today=new Date().toISOString().slice(0,10)) {
  if(!events.length)return {status:'not_assessed',next_review:null,evidence_count:0};
  const ordered=[...events].sort((a,b)=>a.date.localeCompare(b.date));
  const good=events.filter(e=>e.score>=.8&&!e.assisted&&!e.misconception.trim());
  const failures=events.filter(e=>e.score<.8||e.assisted||e.misconception.trim()).map(e=>e.date);
  const lastFailure=failures.sort().at(-1);
  const qualified=good.filter(e=>!lastFailure||e.date>lastFailure);
  const demonstrated=new Set(qualified.map(e=>e.date)).size>=2&&new Set(qualified.map(e=>e.question)).size>=2&&['explanation','application'].every(k=>qualified.some(e=>e.kind===k));
  const interval=Math.min(14,3*Math.max(1,new Set(qualified.map(e=>e.date)).size-1));
  const due=new Date(`${ordered.at(-1)!.date}T00:00:00.000Z`); due.setUTCDate(due.getUTCDate()+(demonstrated?interval:1)); const next_review=due.toISOString().slice(0,10);
  let status=demonstrated?'demonstrated':'learning';
  if(events.length===1&&(ordered[0].kind==='recall'||ordered[0].assisted))status='inconclusive';
  if(next_review<=today)status='needs_review';
  return {status,next_review,evidence_count:events.length};
}
export function report(s:State,today?:string){return Object.fromEntries(objectives.map(o=>[o.id,competencyStatus(activeEvents(s).filter(e=>e.competency===o.id),today)]));}
export function recommend(s:State,today=new Date().toISOString().slice(0,10)) {
 const statuses=report(s,today), weights:any={D1:.275,D2:.375,D3:.325};
 const counts=Object.fromEntries(Object.keys(weights).map(d=>[d,objectives.filter(o=>o.domain_id===d).length])) as Record<string,number>;
 const used=new Set(s.events.map(e=>e.question));
 const ranked=objectives.flatMap(o=>{
  const stat:any=statuses[o.id]; if(stat.status==='demonstrated')return [];
  const missing=o.prerequisites.filter((p:string)=>(statuses as any)[p]?.status!=='demonstrated');
  const events=activeEvents(s).filter(e=>e.competency===o.id), urgency=stat.status==='needs_review'?4:2, uncertainty=1/(1+events.length);
  const latest=events.map(e=>e.date).sort().at(-1), error=events.some(e=>e.date===latest&&(e.score<.8||e.misconception.trim()))?1:0;
  const daysLeft=Math.max(1,(Date.parse(`${s.profile.deadline}T00:00:00Z`)-Date.parse(`${today}T00:00:00Z`))/86400000);
  const priority=(urgency+uncertainty+error+weights[o.domain_id]*10/(counts[o.domain_id]||1))/(1+missing.length);
  return [{competency:o.id,name:o.name,priority:Number(priority.toFixed(4)),reason:stat.status,prerequisites_to_check:missing,session_minutes:Math.min(Number(s.profile.minutes_per_day),daysLeft<=3?15:25),avoid_questions:[...new Set(events.map(e=>e.question))].sort(),question_candidates:questions.filter(q=>q.competency_id===o.id&&!used.has(q.id)).map(q=>q.id),fallback:'If no unseen bank item exists, author a changed scenario from the objective rubric; identify it as unreviewed.'}];
 });
 return ranked.sort((a,b)=>b.priority-a.priority||a.competency.localeCompare(b.competency)).slice(0,5);
}

export async function migrateState(source:State,plan:any):Promise<State>{
 if(!plan||typeof plan!=='object'||typeof plan.from_version!=='string'||!plan.from_version||plan.to_version!==version||plan.from_version===version)throw new Error('Plan must migrate a different source curriculum version to the approved curriculum');
 if(typeof plan.reviewer!=='string'||!plan.reviewer.trim())throw new Error('A named mapping reviewer is required; AI review must be labeled AI');isoDate(plan.reviewed_at);
 const oldIds=plan.source_competencies;if(!Array.isArray(oldIds)||!oldIds.length||oldIds.some((x:any)=>typeof x!=='string'||!x)||new Set(oldIds).size!==oldIds.length)throw new Error('Plan must list all distinct source competency IDs');
 await validateState(source,plan.from_version,new Set(oldIds));const rows=plan.mappings;if(!Array.isArray(rows)||rows.length!==oldIds.length||new Set(rows.map((r:any)=>r.source)).size!==oldIds.length||!oldIds.every((id:string)=>rows.some((r:any)=>r.source===id)))throw new Error('Plan must map every source competency exactly once');
 const current=new Set(objectives.map(o=>o.id)),byId=new Map<string,any>();
 for(const row of rows){const {change,targets}=row;if(!['preserved','changed','split','removed'].includes(change)||!Array.isArray(targets)||new Set(targets).size!==targets.length||targets.some((t:string)=>!current.has(t))||typeof row.reason!=='string'||!row.reason.trim())throw new Error('Invalid reviewed mapping');if(change==='preserved'&&(targets.length!==1||targets[0]!==row.source)||change==='changed'&&targets.length!==1||change==='split'&&targets.length<2||change==='removed'&&targets.length!==0)throw new Error('Mapping shape does not match change type');byId.set(row.source,row);}
 const result:any={schema_version:1,curriculum_version:version,profile:structuredClone(source.profile),events:[],migration:{source_sha256:await sha256(source),plan_sha256:await sha256(plan),plan:structuredClone(plan),original_state:structuredClone(source)}};
 for(const event of source.events){const row=byId.get(event.competency);for(const target of row.targets){const translated={...structuredClone(event),competency:target,...(row.change!=='preserved'?{requires_reassessment:true}:{})};if(!result.events.some((e:any)=>JSON.stringify(e)===JSON.stringify(translated)))result.events.push(translated);}}
 result.events.sort((a:Event,b:Event)=>a.date.localeCompare(b.date));return validateState(result);
}
