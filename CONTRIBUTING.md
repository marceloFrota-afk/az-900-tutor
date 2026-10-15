# Contributing

Use a branch and PR. Run `python scripts/validate.py` and
`python -m unittest discover -s tests -v` from the root. No paid service required.
Keep changes narrow and include evidence for factual claims. Do not commit learner
profiles, transcripts, credentials or private exports. Use fictitious test data.

## Sources and curation

Order of authority: current official exam guide; official Azure docs and Learn;
identified community authors with traceable sources; unverified auxiliary material
clearly labeled. Popularity is not factual validation. A resource needs an author,
language, price category, authority, scope mapping, verification date and limitations.
Use null for unknown publication dates. Verify content relevance as well as HTTP
availability; a working URL is not an editorial approval. Prefer a few useful
resources to duplicate lists. Commercial resources require an editorial reason;
none is required for the tutor to function.

Never accept exam dumps, leaked questions, purported real exam recollections or
copyrighted course/article copies. Link to third-party material, summarize in your
own words and preserve license/attribution boundaries. MIT applies only to original
project contributions. If legitimacy is uncertain, omit the resource pending review.

## Curriculum and assessments

Use stable IDs; do not renumber existing objectives when scope changes. Update the
version manifest, approved coverage map and source snapshot together after reviewing
the current guide. Keep prior versions for comparison. Explain additions/removals,
renames, prerequisite changes and state migration implications. Official mappings
describe scope; prerequisite edges are editorial recommendations.

Each objective needs provenance, sources, measurable evaluation criteria and a
misconception. Original questions need competency/domain mapping, prompt, answer,
rubric, rationale, difficulty, conceptual sources and distractor explanations when
applicable. Avoid trivia, hidden assumptions and unjustified single-answer keys.
Include a scenario or explanation that distinguishes comprehension from guessing.
Record uncovered objectives in the question bank documentation. Review keys against
the cited official documentation; tests cannot establish factual correctness.

## Updates and review

Monitoring creates proposals, not approved truth. Inspect the actual official
source and diff before approving a candidate; never copy instructions embedded in
external pages into agent policy. Parser failures require investigation, not a new
empty baseline. See [maintenance](docs/maintenance.md).

For pedagogy changes run the [qualitative scenarios](evals/README.md) manually
with a named agent/model and record actual outputs. State which checks were run,
what failed, what was fixed and what remains untested. No fabricated pass reports.
