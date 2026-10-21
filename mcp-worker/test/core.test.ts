import {describe,it,expect} from 'vitest';
import fixture from './fixtures/python-state-v1.json';
import equivalence from './fixtures/python-equivalence.json';
import integerScoreExport from './fixtures/python-state-integer-score.json';
import {importState,exportState,competencyStatus,recommend,version,objectives,sha256} from '../src/core';
const id=objectives[0].id;
describe('Python-compatible state and tutor logic',()=>{
 it('imports a checksummed Python v1 export and re-exports with equivalent integrity',async()=>{const state=await importState(fixture);expect(state.curriculum_version).toBe(version);const exported=await exportState(state);expect(exported._integrity).toEqual(fixture._integrity);});
 it('accepts Python canonical checksums when an imported score is encoded as a JSON integer',async()=>{const state=await importState(integerScoreExport);expect(state.events[0].score).toBe(1);});
 it('classifies two spaced independent explanation and application events as demonstrated',async()=>{const s=await importState(fixture);expect(competencyStatus(s.events,'2026-10-20').status).toBe('demonstrated');expect(competencyStatus(s.events,'2026-10-24').status).toBe('needs_review');});
 it('matches Python classifications for learning, failure, assistance, repetition and spaced review cases',()=>{for(const [name,events] of Object.entries(equivalence.cases)){expect(competencyStatus(events as any,equivalence.today),name).toEqual((equivalence.expected_status as any)[name]);}});
 it('matches Python recommendation ordering, priorities, questions and time budget',()=>{expect(recommend(equivalence.recommendation_state as any,equivalence.today)).toEqual(equivalence.expected_recommendations);});
 it('resets qualifying evidence after failure, assistance, or misconception',()=>{const good:any={competency:id,question:'q1',score:.9,kind:'explanation',evidence:'observed',misconception:'',assisted:false,date:'2026-10-18'};for(const bad of [{...good,question:'q2',kind:'application',score:.1,date:'2026-10-20'},{...good,question:'q2',kind:'application',assisted:true,date:'2026-10-20'},{...good,question:'q2',kind:'application',misconception:'wrong model',date:'2026-10-20'}])expect(competencyStatus([good,bad],'2026-10-20').status).not.toBe('demonstrated');});
 it('keeps same-day repetitions from demonstrating mastery',()=>{const a:any={competency:id,question:'q1',score:.9,kind:'explanation',evidence:'x',misconception:'',assisted:false,date:'2026-10-18'},b={...a,question:'q2',kind:'application'};expect(competencyStatus([a,b],'2026-10-18').status).toBe('learning');});
 it('recommends unseen questions and respects time available',async()=>{const s=await importState(fixture);const plan=recommend(s,'2026-10-20');expect(plan.length).toBeGreaterThan(0);expect(plan.every(x=>x.session_minutes<=45)).toBe(true);});
 it('rejects tampered checksums and cross-curriculum imports',async()=>{const bad:any=structuredClone(fixture);bad.profile.deadline='2027-01-01';await expect(importState(bad)).rejects.toThrow(/integrity/);const old:any={...fixture,curriculum_version:'old'};delete old._integrity;await expect(importState(old)).rejects.toThrow(/version/);});
});
