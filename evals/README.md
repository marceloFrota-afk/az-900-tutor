# Qualitative behavior evaluations

`scenarios.json` defines ten minimum cases: beginner, experienced developer, service-model misconception, lucky correct answer, short deadline, return after a pause, stale source, ambiguous question, external prompt injection, and exam dumps. These are executable evaluation prompts and review criteria, not evidence that a model passed them.

Run each scenario in a fresh agent session. For the repository condition, load `AGENTS.md`, `TUTOR.md`, the skill and its relevant references/data; require the model to read them. For the baseline, give the same learner prompt to the same model/configuration without those repository instructions or data. Match tool access and record any unavailable files or sources. Keep actual responses and any follow-up learner turns verbatim. Do not coach only one condition or give a baseline less useful factual context if testing the behavioral instructions alone.

Prepare separate local records (Python standard library only):

```sh
python evals/run.py prepare --condition with-repository --model actual-model-version --output .learner/eval-with.json
python evals/run.py prepare --condition baseline --model actual-model-version --output .learner/eval-baseline.json
```

Fill evaluator identity, execution date, exact model settings, each transcript, and each criterion's `pass` boolean plus a short quotation or observed action supporting that judgment. Empty/null fields mean unexecuted, not passed. An evaluator can be a human or a separately configured model; disclose which and preserve disagreements. All three criteria per scenario are required. Any critical failure fails that scenario. A model-generated judgment is not a substitute for checking the transcript against its rubric.

```sh
python evals/run.py summarize .learner/eval-with.json
python evals/run.py summarize .learner/eval-baseline.json
```

The utility reports only explicit reviewer judgments; it does not call a model or classify prose using keywords. It refuses missing/duplicate cases or altered criterion IDs. Keep real learner transcripts private. Publish only synthetic, reviewed transcripts with model/configuration, date, criterion evidence, failures, and limitations; do not publish account identifiers or hidden reasoning.

For a paired comparison, use identical prompts, fresh contexts, equivalent tools, and preferably randomize condition order and blind the reviewer to the condition. Report per-case results before aggregates. A single sample per condition is noisy, the cases were written by this project, and contamination from development context is possible. This suite can identify contract violations; it does not establish better exam outcomes, statistical significance, learner mastery, or a passing probability.

Structural tests check data links, state transitions and this runner. They do not execute or grade a tutor model. Consult committed run reports, if any, for actually executed qualitative results. Independent subject-matter review and learner trials remain needed.

## Continuation actually executed

See [completion report](../docs/completion-report.md) and [preserved paired development probes](runs/2026-10-15/). Twenty real responses, ten per condition, were judged criterion by criterion; both arms have 9 passes and 1 failure. Shared factual packet and known context/configuration limits are preserved. A behavior repair has no post-fix evaluation claim. These observations do not establish controlled instructional efficacy.
