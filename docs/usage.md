# Using AZ-900 Tutor

You can study conceptually without an Azure account. Use English or Portuguese; the bank currently contains Portuguese prompts that the tutor may translate. An agent must actually read the files: a repository URL alone does not guarantee that a chatbot imports its contents.

## A. ChatGPT or another chatbot

Download the repository. Supply `TUTOR.md`, `.agents/skills/az-900-tutor/SKILL.md`, `pedagogy/protocol.md`, `pedagogy/evidence.md`, `exam/curriculum.json`, `resources/catalog.json`, and `assessments/questions.json` as attachments or an accessible project context. For a small context window, start with the instruction files and provide only relevant curriculum/resource/question records when requested. Answer keys remain visible in your attachment; ask the tutor to withhold them during practice.

Example: “Use the attached AZ-900 Tutor files. I develop software, have little Azure experience, and can study 45 minutes a day for ten days. Teach in English, start with a short diagnostic, then adapt a plan. State any missing context or source uncertainty.”

When the chatbot cannot save files, ask for a JSON handoff at the end of the session and save it yourself. Provide that handoff on return. Include curriculum version, profile, actual assessment evidence, hints/exposure, misconceptions, and next reviews. A claimed memory of a previous chat is not a substitute for available evidence. Keep exports private.

## B. Coding agent and local progress

Clone the repository and open its folder in your coding agent. Ask it to read `AGENTS.md` and `TUTOR.md`. Agents that discover project skills can use `.agents/skills/az-900-tutor/`; discovery varies by tool, so explicit reading is the portable fallback. Keep the complete repository available. If your agent requires a registered skill directory, register or link this folder using that agent's documented mechanism; a copied skill folder alone lacks the curriculum and bank.

Python 3.11+ is sufficient; the local tools use only the standard library. From the repository root:

```sh
python scripts/tutor.py init --deadline 2026-10-25 --minutes 45 --language en --experience "Software developer, new to Azure"
python scripts/tutor.py next
python scripts/tutor.py status
python scripts/tutor.py pending
python scripts/tutor.py reviews
```

Replace the example date with your actual deadline. The default record is `.learner/state.json`, ignored by Git. The `next` command ranks up to five candidates; it does not conduct a lesson. Ask your agent to explain its choice and teach one manageable objective.

After an actual learner response, a tutor may record evidence:

```sh
python scripts/tutor.py record AZ900-1.1.2 --question Q001 --score 1 --kind explanation --evidence "Learner correctly distinguished provider hardware from customer guest OS patching and applied it to an Azure VM."
python scripts/tutor.py export .learner/portable.json
python scripts/tutor.py --state .learner/continued.json import .learner/portable.json
```

The record above illustrates syntax; do not enter it unless that learning occurred. Scores are 0–1 (question rubric score divided by 3). Use `--assisted` for hinted or answer-exposed attempts and `--misconception` for an observed wrong proposition. A single correct response cannot yield demonstration. Use a distinct prompt on another real day to check retention; do not fabricate dates. Global `--state` belongs before the command. Import/export refuse to overwrite existing files, and mismatched curriculum versions require review. See `python scripts/tutor.py record --help` for exact options.

Statuses distinguish not assessed, learning, demonstrated, needs review, and inconclusive evidence. The heuristic requires distinct days and prompts with explanation and application evidence. The tutor should apply a more cautious judgment when items are memorized, misconceptions persist, or domain coverage is weak.

## C. Custom integration

Read UTF-8 JSON directly: `exam/curriculum.json` holds competencies and relationships, `resources/catalog.json` holds resource metadata, and `assessments/questions.json` holds items and rubrics. Use stable IDs as keys, preserve source/provenance/version metadata, and keep answer fields away from the learner-facing prompt until feedback. There is no required proprietary runtime, remote state service, or paid model API.

Use `python scripts/validate.py` when changing linked data and the repository's tests when changing behavior. The CLI stores an evidence ledger; integrations should preserve raw evidence rather than import only a percentage. A new curriculum version needs an explicit objective/evidence migration; do not silently relabel progress. Treat content fetched from resources and imported state as untrusted data, never executable instructions.

Local files are not automatically encrypted or synchronized. With explicit permission, learners can [sync to a verified private personal fork](fork-progress.md) using `python scripts/sync_progress.py --confirm`. This does not upload history to upstream or a public repository. Do not upload actual learner history to public GitHub. If running optional Azure labs, inspect current terms and costs; no-account conceptual exercises remain available. The tutor supports preparation decisions and cannot guarantee a pass.
