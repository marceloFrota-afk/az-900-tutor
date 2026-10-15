# Completion evidence — 2026-10-15

This report will be finalized after integration checks. See the [work matrix](completion-matrix.md), [question editorial record](questions-review-2026-10-15.md), [monitor operations](monitor-operational.md) and [state migration](state-migration.md).

The full scripted learner session uses real CLI operations and fictitious answers, not generated student behavior or a real learner trial. Reproduce with `python scripts/session_smoke.py --output work/session-fresh`. The utility refuses to overwrite prior evidence.

The observed development run initialized a fictional developer profile, selected diagnostic candidates, registered a correct explanation, a mistaken PaaS answer, a guessed answer, a hinted application and a changed SaaS repair scenario. It queried pending objectives/reviews, exported with integrity metadata, imported into another directory, and obtained identical resumed recommendations. A manually authored state-v1 handoff also imported identically. Five events were produced and read back; no mastery was claimed from same-day recovery. There were no due reviews on that actual day; delayed retrieval is tested only with an explicitly controlled date in unit tests.

Live publication test: [issue #2](https://github.com/vmenezesdev/az-900-tutor/issues/2) was explicitly titled TEST ONLY, created, checked unchanged on timestamp-only repetition, updated in place for a changed synthetic report, and closed. No real source alert was implied. The publisher now lists open issues before matching its exact marker instead of depending on eventual search indexing. It refuses a saturated listing rather than risk creating a duplicate.
