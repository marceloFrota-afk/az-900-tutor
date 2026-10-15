# Focused human review packet

Status: **Pending human Azure SME and education review**. AI authorship plus a separate AI editorial pass is implemented; it does not constitute human approval, Microsoft endorsement or empirical item validation. Public source checks were made on 2026-10-15; current product exceptions should still be verified.

Open `assessments/questions.json` by stable item ID, compare `prompt`, `answer`, `rubric`, `rationale`, `distractor_rationales` and `source_urls`, then read the corresponding `competency_id` and lesson. Do not infer quality from structural validation.

| Items / area | Decision already made | Human check |
| --- | --- | --- |
| Q013, Q041 — hosting | Managed container hosting can also satisfy a managed API requirement; App Service is an example | Confirm all defensible options receive credit under stated runtime/OS constraints |
| Q016 — storage protocols | Require SMB to distinguish Files; Blob can support NFS | Check prompt constraints and distractors against current service documentation |
| Q021, Q059 — Reader/RBAC | Configuration visibility does not imply blob data access | Separate control-plane actions from DataActions and alternate data authorization |
| Q026, Q060 — locks/Policy/RBAC | Locks protect control-plane operations | Confirm no implication that resource locks prevent data-plane deletion or grant access |
| Q032 — private cloud | Exclusively used whole cloud environment, not merely dedicated hardware | Distinguish Azure Dedicated Host within public Azure |
| Q037, Q065 — regions/zones | Region pairs are not universal; application recovery needs design | Verify regional/service conditions and sovereignty wording |
| Q023, Q061 — budgets | Alerting does not itself impose a spending cap | Check distinction from separately configured automation |
| Q050 — defense in depth | One additional layer requested and required | Check example actually covers a distinct layer and matches rubric |
| Q063 — recovery | Replication is not historical retention/backup | Verify accidental deletion scenario and chosen recovery mechanism |
| Q001, Q064 — responsibility | Provider manages managed platform OS; customer retains identity/data decisions | Check SaaS/PaaS language avoids transferring all security duties |
| All 57 lessons | Concise starting explanations, not exhaustive coverage of compound objectives | Check beginner comprehension, Azure/general distinction, experienced transfer depth |

Use the exact official links in each item and [independent editorial record](questions-review-2026-10-15.md). The previous SMB/Reader fixes are in [the first editorial review](editorial-review.md). Runtime/price/region assertions must be checked against live service-specific docs rather than the exam outline alone.

Reviewer checklist:

- [ ] Record name/role, date, item IDs and source versions actually inspected.
- [ ] Answer the prompt without seeing its key; identify alternate defensible answers and hidden assumptions.
- [ ] Match every full-credit requirement to something the prompt requests.
- [ ] Inspect distractors for technical correctness and useful feedback.
- [ ] Run one novice think-aloud and one experienced-developer session with consent, preserving actual errors.
- [ ] Check that corrected guesses/hinted answers are retained as exposed learning evidence.
- [ ] Review changed/split migration decisions individually; source and backup must remain intact.
- [ ] Re-run affected tests after edits and preserve prior evaluation failures.
- [ ] Keep human editorial signoff separate from psychometric calibration, retention data and exam-success claims.

Suggested review outcomes are `accept`, `revise` or `needs source confirmation`, with a specific reason per item. No prefilled approval is supplied.
