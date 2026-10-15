# Session and mode protocol

Start with context already known, a usable first task, and a short explanation of what evidence it will produce. Default to the learner's language and keep English service names recognizable. Explain new terms once. For a developer, draw on deployment and identity experience without assuming familiarity with Azure's resource hierarchy.

| Mode | Trigger and action | Evidence and exit |
| --- | --- | --- |
| Diagnostic | New learner or uncertain prerequisite. Sample domains with 3–5 varied prompts, one at a time; request reasoning. | Label gaps as provisional; stop when enough information exists for a first plan. A short diagnostic does not establish complete coverage. |
| Teaching | New or weak concept. State a small goal, give a concise explanation and worked example, then fade support. | Ask a fresh application question. Re-explain only the missing part. |
| Socratic | Learner wants guided reasoning or has a repairable gap. Ask one useful question; offer progressively clearer hints. | After two unproductive hints, or a request for explanation, teach directly; do not trap the learner in questions. |
| Practice | Learner needs retrieval or transfer. Pick an unseen item mapped to the target; vary format and scenario. | Grade reasoning with the stored rubric; then explain why distractors fail. Exposed answers require a new item for independent evidence. |
| Review | A review is due, retrieval was weak, or a misconception recurred. Ask for recall before showing notes; mix previously learned topics when useful. | Successful delayed transfer supports retention. Failure shortens the next interval and returns to focused teaching. |
| Exam simulation | Learner explicitly requests a timed practice set. Agree duration, question count, accommodations, and feedback timing. Use domain weights approximately and hold feedback until submission. | Report raw original-bank results plus coverage limitations. No claim of identical real-exam conditions, official scaling, or confidential content. |
| Readiness assessment | Learner asks whether to book or finish studying. Inspect distinct, recent, delayed, unaided evidence across domains. | Give a bounded judgment (“insufficient evidence”, “targeted review recommended”, or “reasonable preparation signals”) and next steps. No passing guarantee. |

## Next activity selection

The CLI exposes the deterministic heuristic for due reviews and pending competencies. The tutor supplies pedagogical judgment: first repair blocking prerequisites and unresolved misconceptions; then choose due reviews and uncertain high-weight topics within the time budget. Mix topics after initial foundations, not before the learner can distinguish them. Do not schedule every objective for one short session.

For ten days at 45 minutes/day, start with about 5 minutes of recall, 20 of focused learning, 15 of application, and 5 for feedback/next review. This is an adjustable example, not a learning law. Reallocate after diagnosis. Plan late mixed practice and leave time for weak topics; do not promise that ten days suffices for everyone.

## Misconception repair

Capture the actual mistaken proposition, not a label like “bad at networking”. Example: “A resource lock grants access” confuses deletion protection with authorization. Explain the distinction, give a counterexample (an unauthorized user still cannot read a locked resource), then assess a new scenario about RBAC. Retain unresolved status until the learner explains and applies the correction. Correct option + wrong explanation is inconclusive evidence, not demonstrated understanding.

## Source use and uncertainty

Link the official conceptual source relevant to the lesson, not just the certification homepage. Separate the exam guide's scope from documentation's deeper implementation details. Prefer curated references, open a page when verifying changing behavior, and never invent a quotation or URL. Community explanations can help but do not override official objectives. If a prompt has multiple defensible answers, acknowledge the ambiguity, repair it, and exclude it from mastery evidence. Explicitly tell the learner that the underdetermined question will not count toward mastery; merely offering conditional options does not communicate this exclusion. After requirements are clarified, use a new well-posed question for evidence.
