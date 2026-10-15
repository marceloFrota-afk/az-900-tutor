# MVP completion matrix — 2026-10-15

Initial inspection: PR #1 head `519dfa8`; existing CI green in four OS/Python combinations. Official guide retrieved again on 2026-10-15: effective 2026-07-20, 57 objectives. Final execution dispositions follow; behavioral and human limitations are explicit.

| Priority | Previous gap | Closure evidence required | Result |
| --- | --- | --- | --- |
| P1 | 27 competencies without questions | Automatic exact coverage; reviewed keys, rubrics and sources | Implemented and tested — 65 items, 57/57; `scripts/coverage.py`, `tests/test_question_coverage.py`, dated independent AI editorial record |
| P1 | No essential lessons | Usable units mapped to all objectives, references and activities; contract tests | Implemented and tested — 57 units, exact coverage/depth/source regressions in `tests/test_lessons.py` |
| P1 | Concurrent writes, duplicate/order sensitivity | Real concurrent processes and fault injection regressions | Implemented and tested — 8 concurrent real CLI writers, lock retries, duplicates, same-day order and fault injection |
| P1 | No curriculum migration | Explicit reviewed mapping, original backup, re-evaluation and synthetic fixtures | Implemented and tested — `scripts/migrate.py`, synthetic preserved/changed/split/removed fixtures, backup and archive |
| P1 | Unobserved full session | Real CLI artifacts, portable handoff import, coherent resume | Implemented and tested — five observed scripted events; `evals/runs/2026-10-15/session-cli.json`, three directories including raw chatbot handoff |
| P2 | Behavioral smoke lacks matched baseline | Preserved actual responses/settings and separate criterion judgments; honest isolation limits | Partial — 20 actual fresh-context responses; 9 passed/1 failed per condition; unblinded same-family review; exact deployment/settings unavailable; repair not re-evaluated |
| P2 | Monitor publication only mocked | Collector regressions, workflow attempt, clearly marked test issue create/update/close | Implemented and tested — live workflow 38749582792, issue #2 create/repeat/update/close; changed-path Actions-token write remains unobserved |
| P2 | Human review difficult | Sensitive item/source/decision checklist | Implemented — `docs/human-review-pack.md`; human review itself pending |
| P3 | Human expertise and learner outcomes unverified | Human SME review, learner study, real delayed retrieval | Pending — requires people and elapsed time |
