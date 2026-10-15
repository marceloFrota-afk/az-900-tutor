# Curriculum contract

The English AZ-900 study guide checked on **2026-10-15** still identifies **2026-07-20** as its effective skills version. [manifest.json](manifest.json) records that source and expected coverage; [curriculum.json](curriculum.json) maps its **57 bullets** across **11 subdomains**, with domain counts **15 / 27 / 15**. Every named example inside a bullet is retained among the competency concepts or description. The scope weights are ranges: **25–30%, 35–40%, 30–35%**. Their midpoints can be normalized for scheduling; they are not per-objective exam probabilities.

Each competency is an editorial paraphrase with a stable ID, learning goals, prerequisites, common misconception, assessment criteria, mastery evidence and provenance. `source_bullet` is the ordinal within `source_section`, not a question count. Product names remain searchable; no official question wording or answer bank is reproduced. The curriculum claims complete structural coverage of the guide's bullets, not full authored lessons or full question-bank coverage. Microsoft can assess related topics beyond illustrative bullets.

IDs initially use `AZ900-domain.subdomain.bullet` for navigation. They must remain stable after publication: preserve an existing ID when wording or position changes; use a new ID for a genuinely new competency and retain a reviewed migration record for removals. Do not renumber by sorting a future guide.

`sources` resolves resource IDs in `resources/catalog.json`; the first source is the scope authority and the second is an official teaching path. The prerequisite graph is an **editorial learning heuristic**, not an official certification requirement. An experienced student can demonstrate a prerequisite through diagnosis and move ahead. Dependencies intentionally run from foundations toward product use, not every conceivable related concept.

Mastery requires multiple reasoned demonstrations, transfer and later retrieval. The textual criteria here specify evidence to collect; the CLI implements the transparent approximation documented in the progress and readiness instructions. Neither is a calibrated probability of passing.

The JSON format was chosen for standard-library parsing, deterministic diffs and consumption across agent runtimes. JSON Schemas describe shapes; repository validation additionally checks references, cycles and scope coverage. Future semantic changes require human review.
