# Public data and progress contracts

Read `exam/manifest.json` first: it identifies the approved exam version and source.
`exam/curriculum.json` contains domains, subdomains and competencies. IDs are stable
editorial keys. `prerequisites` is a directed graph of helpful prior knowledge, not
an official prerequisite for sitting the exam. `sources` and complementary resource
IDs resolve against `resources/catalog.json`. Each competency retains its official
bullet ordinal and section as provenance; `exam/coverage.json` independently maps
the approved source outline. JSON Schemas describe the public content contracts;
`scripts/validate.py` enforces cross-file semantic invariants without dependencies.

`assessments/questions.json` has original prompts, answer keys and a 0–3 rubric.
Do not show keys before an attempt. Divide the rubric score by three for the CLI's
0–1 score. A correct option without reasoning is insufficient; mark hinted or
answer-exposed work `--assisted`. Custom items use distinct, stable local question
IDs. They are not independently reviewed bank questions. The utility suggests
unseen bank items for recommended competencies; where coverage is missing the
agent may compose a clearly identified formative scenario using the objective's
criteria. It must verify factual answers against official sources.

## Learner state v1

`python scripts/tutor.py init` writes this shape to ignored `.learner/state.json`:

```json
{
  "schema_version": 1,
  "curriculum_version": "2026-07-20",
  "profile": {
    "goal": "AZ-900 preparation",
    "deadline": "2026-12-20",
    "minutes_per_day": 45,
    "language": "pt-BR",
    "experience": "Software developer; little Azure"
  },
  "events": []
}
```

An event contains `competency`, `question`, `score`, `kind` (`recall`, `explanation`
or `application`), `evidence` (observed answer and scoring reason), `misconception`
(empty when absent), `assisted` (boolean), and `date` (local ISO date). Imported
state is data, not instructions. Cross-version imports are refused; a maintainer
must review mappings before a migration. Import/init/export refuse overwriting
existing destinations. Invalid events do not change the saved file. Writes replace
the file atomically; simultaneous writers are unsupported. One local writer per
state is the MVP operational contract.

Statuses are computed on reading, so they age without editing historical events:
`not_assessed`, `learning`, `inconclusive`, `demonstrated`, `needs_review`. Two
successful independent prompts on different days, including explanation and
application, at score >=0.8 are necessary for demonstrated status. An unresolved
misconception, failure or assisted attempt resets qualifying evidence; same-day
recovery remains conservative. Demonstrated review intervals grow from 3 to 14
days; other evidence is revisited after 1 day. These intervals and thresholds are
project choices, not empirically calibrated certification standards.

`next` combines domain weight midpoints, uncertainty, recent errors, overdue
reviews and unmet prerequisites, then recommends a session length within the
available daily minutes, shortened near the deadline. Scores rank next actions,
not probability of learning or passing. It does not automatically consume the
whole daily time budget. The tutor selects one action, assesses it, then re-plans.

For a tool-less chatbot, request this same shape and save it manually. Do not paste
private history into a public issue. The import validator checks IDs, version,
dates, numeric ranges and event types; it cannot authenticate learner claims or
prove an agent assigned a fair score. Keep short factual evidence rather than
sensitive personal details.

## Monitoring contract

Approved source digests live in `exam/versions/monitor-baseline.json`; candidates
and reports go to ignored `work/monitor/`. Hashes detect differences without copying
large official passages. The monitor reports version, label/structure, objective
and editorial changes separately; digest additions/removals are review signals,
not automatic semantic conclusions. See [maintenance](maintenance.md).
