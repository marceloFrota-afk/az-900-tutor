# Validation and adversarial review

Verification date: 2026-10-15. This report separates implemented tools from evidence
about an actual tutoring model. No real learner history is included.

## Implementation evidence

- Repository audit: `trunk` and existing `feat/agent-native-tutor-mvp` both started
  at `28a9c9e`, containing only README.md; no PRs or workflows existed. Reused the
  feature branch, preserving history.
- Full current official scope read and mapped: 57 bullet objectives, 11 subdomains,
  3 domains, effective 2026-07-20. Independent ordered source digests are tied to
  every coverage mapping. Domain weights and manifest counts are checked.
- Curriculum and catalog JSON Schemas were checked with a locally available
  JSON Schema validator, including formats; the runtime remains dependency-free.
- `python scripts/validate.py` checks coverage against approved source digests,
  unique IDs, prerequisite cycles, sources, domain/subdomain relationships,
  catalog references, question keys/distractors, skill metadata and local links.
- `python -m unittest discover -s tests -v` covers state transitions, CLI
  init/record/export/import, invalid evidence and overwrite guards, monitor parsing,
  differences, malformed input, network failure and issue deduplication with mocks.
  Final local run: **25 tests passed** on Windows / Python 3.13.5. Consult CI for
  the matrix results on Windows/Linux and Python 3.11/3.13.
- The bundled skill-creator validator was executed: `Skill is valid!`. This checks
  metadata/structure, not pedagogical quality or compatibility with every agent.
- Live official HTML retrieval, parsing and comparison succeeded: 57 objectives,
  `unchanged`, fingerprint
  `a5bfd686d941f9f095483c45ef3d8f045c7b6305d6aeea6b50ee34c65b5bdbaa`.
- Final live optional link check: all **15 catalog URLs** returned reachable HTML.
  This is availability evidence, not full semantic or interactive-content review.

## Qualitative evidence

Ten synthetic cases and an evaluation-record runner are implemented in `evals/`.
Preparing an empty run and summarizing it correctly reports ten unexecuted cases,
zero passes. The runner never generates transcripts or guesses reviewer scores.
The [observed smoke responses](../evals/observed-smoke.md) record actual delegated
agent responses under the contract and their limitations. They are development
smoke evidence, not a controlled experiment or a claim that all agents pass.

No matched no-repository baseline, randomized/blinded evaluation, calibrated judge,
real learner trial or statistical learning benefit has been established. The
evaluation README supplies a paired protocol for future work. Model configuration
is inherited from the development session; an exact public deployment/version
identifier is unavailable, so reproduction across hosted products is limited.

## Adversarial review and fixes

| Perspective | Finding and disposition |
| --- | --- |
| Beginner | Chatbots need actual files, including the skill, rather than only a URL. Both READMEs list them and give a ready-to-use Portuguese prompt. Context/upload limits remain. |
| Experienced engineer | Short diagnostics focus Azure differences; prior experience is reused but never treated as proof of all Azure skills. Synthetic smoke response exercises this path. |
| Maintainer | JSON and Python stdlib avoid service setup. Coverage digests, editorial provenance and source checks make changes reviewable. Baseline approval still needs human reading. |
| Azure reviewer | Region pairs are not universal; tags do not inherit automatically; locks protect control-plane operations. Targeted official references added. Original questions received a second editorial pass; certified SME review remains open. |
| Education reviewer | One correct answer cannot demonstrate competence. Explanations, application, distinct days/prompts and delayed review are required. Unresolved misconceptions now block demonstration. Thresholds remain uncalibrated. |
| Agent developer | Corrected skill data paths and documented repository context; copying the skill alone is insufficient. Imported state and retrieved material are treated as data, not instructions. |
| Security engineer | Local state ignored; atomic writes; invalid imports refuse overwrite. Workflows use minimal permissions; external source data is never executed. Concurrent learner-state writers remain unsupported. |
| Product evaluator | Concrete added value is explicit coverage, source provenance, evidence and review continuity; superior outcomes over a generic chatbot are still unproven. |

An independent code review reproduced noncanonical ISO dates causing false
demonstration and imported event order affecting priorities. Canonical dates are
now required and latest evidence is selected by date; regression tests cover both.
The same review found missing official-source, subdomain and MC key checks; these
are enforced with corruption tests. Observed misconceptions cannot count toward
qualifying success evidence. Earlier integration checks failed while files were
being assembled; they are not described as successful runs.

The [second editorial review](editorial-review.md) inspected all 30 question keys
and mappings. It corrected Q016's ambiguous file-protocol scenario to SMB and
Q021's Reader permissions to control-plane configuration access. It is an AI
editorial review with cited documentation, not human certification expertise.

## Operational boundaries and next work

Implemented and locally exercised: content checks, learner CLI and live guide
detector. Issue creation/update has mock coverage; a real change alert has not been
posted because the current source is unchanged. Scheduled Actions only become
active after a human-approved merge onto `trunk`. No merge was performed.

Partial: question coverage (30 primary objectives of 57), complete lessons, and
semantic change classification. Digests identify additions/removals; a reviewer
determines meaning. Unknown historical changes before the initial baseline are
explicitly not reconstructed. Optional link checks report reachability, not truth.

Priorities: (1) certified Azure/editorial review and additional items for uncovered
objectives; (2) matched qualitative runs across agents plus real learner feedback;
(3) trial the scheduled alert after merge and review source changes; (4) add an
explicit curriculum-state migration when the next exam version requires it.
