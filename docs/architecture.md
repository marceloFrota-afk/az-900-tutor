# ADR 001 — Files as the tutor's public contract

Accepted 2026-10-15. Target: beginners and experienced developers preparing for
AZ-900 with an agent, including Portuguese speakers and students moving between agents.

The hard problem is selecting and assessing learning against current objectives,
not generating another explanation of cloud computing.

Use versioned JSON curriculum, curated resources and original assessment items;
Markdown pedagogy and an Agent Skill; Python 3.11+ standard-library tools for
validation, local progress and conservative source monitoring. JSON avoids a YAML
runtime dependency and has unambiguous interoperable types. Data is authoritative;
human indexes are generated or concise curated entry points. No model provider API
is needed. The tutor reads only relevant objectives and questions after onboarding.

Rejected for MVP: hosted LMS (operational/privacy cost), vector database/RAG service
(unnecessary for this corpus), prompts alone (no auditable coverage/state), and a
calibrated psychometric score (no learner population data). Original assessment
items sample the curriculum; structural objective coverage is complete, lesson and
item coverage can grow. Relationships are editorial learning suggestions, not
official exam prerequisites.

Local `.learner/` JSON stores explicit evidence, question exposure and review dates.
The CLI suggests next work but does not grade natural language: the tutor/student
records rubric judgments with rationale. Heuristics are visible and testable,
not pass probabilities. Export/import preserves state without a server. Never put
real learner examples in the public repository.

Monitoring proposes review issues and candidate snapshots; it cannot approve or
rewrite curriculum. Public HTML detection is deliberately guarded and can fail
closed when structure changes. Semantic interpretation remains editorial work.

Out of scope: web/mobile UI, accounts, cloud hosting, payments, proprietary runtime,
full lessons for every objective, real exam reproduction, guaranteed readiness,
or evidence that this toolkit improves actual exam outcomes. Qualitative agent
evaluations and calibrated learning studies are separate from deterministic tests.
