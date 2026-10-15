# AZ-900 Tutor

[Português brasileiro](README.pt-BR.md) · [Start studying](docs/usage.md) · [Resources](resources/README.md) · [Contribute](CONTRIBUTING.md)

A portable tutoring kit for Microsoft Azure Fundamentals. Give an agent the
curriculum, teaching contract and original questions; it can diagnose gaps,
teach with traceable sources, assess explanations and plan reviews. No hosted app,
model subscription, Azure account or cloud deployment is required by this toolkit.
Your chosen agent may have its own requirements.

## Start in five minutes

**ChatGPT or another chatbot:** download this repository as a ZIP, extract it,
and attach `TUTOR.md`, `.agents/skills/az-900-tutor/SKILL.md`, `pedagogy/protocol.md`, `pedagogy/evidence.md`,
`exam/curriculum.json`, `resources/catalog.json`, `lessons/units.pt-BR.json` and `assessments/questions.json`.
If uploads are limited, provide the contract and relevant domain first, and ask
the agent to report which files it can actually read. A repository URL alone does
not guarantee access. Send:

> Use TUTOR.md as the tutoring protocol. I am a software developer with little
> Azure experience. I have ten days and 45 minutes daily. Teach me in Brazilian
> Portuguese. Start with a short diagnostic, one question at a time. Explain why
> before marking knowledge demonstrated. Cite sources and finish with a portable
> progress summary. Do not claim to save files unless you can.

**Coding agent:** clone the repo and open it as the workspace. Read `AGENTS.md`
and activate `.agents/skills/az-900-tutor/SKILL.md` using the agent's supported
skill mechanism, or ask it to read that file directly. Keep the whole repository
available; the skill references its data here. Say “Use az-900-tutor; diagnose my
Azure gaps and start my first session.” See [installation and alternatives](docs/usage.md).

**Custom integration:** consume the JSON files directly and use the protocols as
your agent policy. Python is optional for tutoring; Python 3.11+ runs the utilities
with no packages to install. [Contracts](docs/data-contracts.md) explain the formats.

## What is included

| Layer | Purpose |
| --- | --- |
| [Curriculum](exam/curriculum.json) | Every bullet objective mapped to a stable ID, sources, prerequisites, misconceptions and assessment criteria |
| [Catalog](resources/catalog.json) | Official-first resources with language, authority and limitations |
| [Tutor contract](TUTOR.md) and [skill](.agents/skills/az-900-tutor/SKILL.md) | Diagnostic, teaching, Socratic, practice, review, simulation and readiness modes |
| [Original questions](assessments/questions.json) | Scenarios, explanation, comparisons and selected-response practice with rubrics |
| [Progress utility](scripts/tutor.py) | Local evidence ledger, pending objectives, review dates and portable export/import |
| [Source monitor](docs/maintenance.md) | Weekly/manual detection with review issues; never auto-approves curriculum changes |
| [Evaluation scenarios](evals/) | Behavioral cases separate from deterministic data/tool tests |

Baseline: the [official study guide](https://learn.microsoft.com/credentials/certifications/resources/study-guides/az-900?wt.mc_id=studentamb_475517)
effective **July 20, 2026**, checked **October 15, 2026**. Domain ranges are
25–30% cloud concepts, 35–40% architecture/services, and 30–35% management/governance.
The source guide and [coverage map](exam/coverage.json) are the scope authority;
57 essential lessons and 65 original questions cover all 57 objectives. A changing
exam requires reviewed updates, even when the monitor has not reported a change.

## Keep your progress

Run from the repository root; replace the deadline with your own date:

```sh
python scripts/tutor.py init --deadline 2026-12-20 --minutes 45 --language pt-BR --experience "Software developer; little Azure"
python scripts/tutor.py next
python scripts/tutor.py record AZ900-1.1.1 --question custom-cloud-1 --score 0.5 --kind explanation --evidence "Recognized on-demand resources; confused cloud with virtualization"
python scripts/tutor.py pending
python scripts/tutor.py reviews
python scripts/tutor.py export .learner/portable.json
python scripts/tutor.py --state .learner/restored.json import .learner/portable.json
```

The agent uses each question's rubric; the CLI stores that judgment, it does not
automatically grade your answer. One correct choice is insufficient for demonstrated
competence. Evidence must include independent explanation and application on
different prompts and days; expired evidence prompts review. These are conservative
project heuristics, not a validated model of learning or an exam pass prediction.

`.learner/` is ignored by Git. Optional [private-fork progress sync](docs/fork-progress.md) requires explicit opt-in and keeps learner history on a separate branch in a verified personal private fork. Keep exports private, including when switching
agents. With a chatbot that cannot write files, request the JSON state at the end
of the session and save it yourself. Do not assume chat memory carries over.

## Validation and maintenance

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
```

CI checks the files, relationships, question metadata and progress/monitor behavior.
Scheduled monitoring becomes active only after the workflow is merged onto the
default branch. Fetch failures are errors, never “no changes”. Review issues use
a stable marker to avoid duplicates; semantic changes need human review.
[Maintenance](docs/maintenance.md) documents baseline approval and monitoring limits.

Official Microsoft Learn links may include the maintainer's Student Ambassadors contributor ID for attribution, without guaranteeing qualified visits or Microsoft endorsement. [Details](resources/README.md#microsoft-student-ambassadors-attribution).

## Limits and contribution

This MVP supplies full structural scope, 57 concise teaching units and at least one original question for every objective. It is not a comprehensive course. Questions are original and have not been statistically calibrated or
reviewed by Microsoft. Agent quality, hallucinations, browsing availability and
context limits remain relevant. Behavioral fixtures do not prove that all models
follow the contract. No exam dumps, confidential questions or pass guarantees.
Labs may incur Azure charges: read the lab prerequisites and clean up resources.

[Architecture](docs/architecture.md), [research](docs/research.md),
[evaluation report](docs/validation.md) and [contribution policy](CONTRIBUTING.md)
describe decisions, evidence and remaining work. MIT licenses original project
code/content; third-party linked material retains its own rights. This is an
independent project, not affiliated with or endorsed by Microsoft.

See / Veja [completion evidence](docs/completion-report.md), [teaching units](lessons/README.md) and [state migration](docs/state-migration.md).
