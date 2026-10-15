# Monitor operational audit

Audit date: **2026-10-15**. The monitor detects review needs; it never approves or edits curriculum, assessment keys, or the approved baseline.

## Verified locally

`python -m unittest discover -s tests -p test_monitor.py -v` passes 16 synthetic regression cases. They cover ordinary changes and a single removal; abrupt deletion; version, label, and editorial changes; malformed, empty, truncated and duplicate sections; corrupted baseline fingerprints/counts; network failure; redirect host/scheme/credentials/port/public-address checks; UTF-8, media type and size failures; issue create/update/deduplication; multiple existing markers; publication failure diagnostics; separate publication without fetching; and catalog-error alert eligibility. These are deterministic tests, not proof that every future Microsoft HTML redesign will parse correctly.

A credential-free live fetch on 2026-10-15 at **14:05:45 UTC** succeeded after allowing public network access in the execution environment:

```sh
python scripts/monitor.py --output work/monitor-live
```

Result: `unchanged`, 57 objectives, baseline and candidate fingerprint `a5bfd686d941f9f095483c45ef3d8f045c7b6305d6aeea6b50ee34c65b5bdbaa`. The first sandbox-restricted attempt returned a socket-permission failure; that was recorded as `failure`, never interpreted as an empty or unchanged source. Working artifacts stay ignored by Git.

## Collection and publication

The weekly/manual workflow has two jobs. `collect` has `contents: read`, fetches without an issue token, and uploads `official-source-review` even if collection exits with an error. `publish` runs after successful or failed collection, downloads that run's artifact, and receives `contents: read`, `actions: read`, and `issues: write`. Checkout credentials are not persisted. Only the publication step receives `GH_TOKEN`. It runs:

```sh
python scripts/monitor.py --publish-report
```

That command reads `work/monitor/report.json` and performs no source fetch. It preserves `official-source-publication`, including issue-body and publication diagnostics, even if publication fails. Both artifacts expire after 14 days. A missing report or upload/download failure makes the workflow visibly fail. A collection failure remains a failed workflow even if its issue publishes successfully. The workflow has no repository-content write permission, no PR trigger, and no automatic baseline update.

Local combined operation remains available with `python scripts/monitor.py --issue`; it requires the GitHub CLI, authenticated repository access and an unambiguous repository context (`GH_REPO` in Actions). Reports distinguish collection `status` from `publication.status`. Exit 0 means a valid collection (including reviewable changes) or successful standalone publication; exit 2 means collection failure; exit 3 means issue-publication failure, taking precedence if collection also failed. The report remains available when issue access fails. CLI diagnostic output is deliberately omitted from the report to avoid copying authentication details.

## Alert lifecycle and failure handling

- One open issue is identified by the exact `<!-- az900-source-monitor:v1 -->` marker. A deterministic report signature ignores collection time and prior publication metadata. Identical repeated alerts do not edit or create issues. Meaningful changes update the same issue. Closing it permits a fresh issue for the next alert.
- Multiple open marked issues are an operational error requiring a maintainer to reconcile markers. The monitor refuses to pick one silently. Issue search checks up to 100 matching open issues; maintainers should preserve the one-open-issue convention.
- A valid unchanged collection does not close an unresolved review. Optional catalog failures, including an unreadable catalog, are alertable review needs. Reachability never establishes content relevance.
- Every collection removes its previous candidate first. A failed run therefore cannot publish a stale candidate as evidence. The approved baseline is never overwritten during normal operation. Only an explicit maintainer `--write-baseline` operation generates a proposed snapshot.
- TLS/public HTTPS, standard port, public DNS results, same-host redirects, a 20-second request timeout, and a two-megabyte body bound constrain fetching. Redirect destinations are checked again. These checks are defense in depth: standard-library DNS validation does not pin the subsequent connection's address, and environment proxies can mediate requests. This is not a general hostile-network isolation service. Keep catalog URLs curated and run maintenance in an appropriately restricted environment.

## GitHub acceptance checks

After pushing the review branch, maintainers can run the workflow without merging it:

```sh
gh workflow run monitor.yml --ref BRANCH
gh run list --workflow monitor.yml --branch BRANCH --limit 5
gh run view RUN_ID --json status,conclusion,jobs
gh run download RUN_ID --dir work/monitor-actions
```

Inspect both artifacts, collection status, source counts/fingerprints, issue behavior and actual job permissions. A default-branch schedule activates only after merge. For an isolated operational issue test, use a disposable repository or a uniquely identified test marker; never overwrite a real unresolved source-review issue with synthetic evidence. Close any test alert after documenting create, identical-repeat deduplication, and meaningful-update results. Local mocked issue tests do not establish live GitHub token permissions or prove a dispatched workflow succeeded; record live run/issue URLs separately when those checks occur.
