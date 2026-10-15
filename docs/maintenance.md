# Source maintenance

The MVP checks the public [official AZ-900 study guide](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-900). It detects changes and requests review; it never edits the approved curriculum. Run from the repository root with Python 3.11+:

```sh
python scripts/monitor.py
python scripts/monitor.py --check-links
python -m unittest discover -s tests -p 'test_monitor.py'
```

`work/monitor/report.json` records the UTC check time and one of `unchanged`, `changed`, or `failure`. The deterministic `candidate.json` contains the effective exam date, domain/group labels, and one SHA-256 digest per normalized objective. It deliberately avoids storing the full guide text. These working outputs are ignored by Git. Never share a student's local state in maintenance reports.

The approved snapshot is `exam/versions/monitor-baseline.json`. Whitespace-only changes are ignored. Reports distinguish exam date, objective digests added/removed, source URL, nomenclature/placement, and editorial section changes. A changed bullet may be a rename, factual correction, or semantic replacement: hashes cannot decide which. A human must follow the source and classify its meaning. Narrative outside the skills section is intentionally excluded. Link redirects to another host are reported for manual URL review, rather than automatically adopting a new authority.

Malformed HTML, missing boundaries, empty groups, implausible counts, a changed number of domains, an objective reduction exceeding 25%, or an increase exceeding 50% are collection/structure failures. They never count as an empty curriculum. The parser assumes English Microsoft heading conventions; an intentional redesign can require a parser update. This conservative HTML detector is not a supported machine-readable contract from Microsoft. Failed checks exit 2; valid changes exit 0 pending editorial review. Read `status` before using any candidate left by an earlier run.

## Scheduled reports

`.github/workflows/monitor.yml` runs Mondays at 08:23 UTC and supports manual dispatch. GitHub scheduled workflows run from the default branch after merge; repository settings can disable them. No deployed service or Azure account is needed. The job reads repository contents and can write issues; checkout credentials are not persisted. It cannot write repository files. Concurrent runs are serialized.

`--issue` requires the GitHub CLI and a repository-scoped token (Actions supplies its standard token). One open issue is identified by the `az900-source-monitor:v1` HTML marker. Identical results ignore the check timestamp and leave the issue alone. Meaningful changes update the existing issue body; a closed issue permits a fresh alert. Do not remove the marker. If publication fails, the workflow fails visibly and preserves diagnostic artifacts. Collection failures also publish an alert before returning a failing exit code. Artifacts remain available for 14 days. A valid unchanged check does not create an issue or close an unresolved one.

Optional `--check-links` checks up to 30 catalog entries sequentially with a 20-second request timeout and two-megabyte response limit. Public HTTPS is required; private network targets and cross-host redirects are refused. An error is a request for review, not proof a resource was deleted. Downloads, videos, blocked bots, and rate limits can all require manual verification. Link results are advisory; the weekly job excludes them to keep its scope and duration bounded. Reachability cannot establish factual accuracy or alignment with the exam.

## Approving a new version

1. Inspect the issue, official guide, and change log. Confirm the effective version and review additions, removals, terminology, weights, and resource applicability.
2. Update curriculum, provenance, coverage mappings, questions, and documentation together in a branch. Preserve stable competency IDs when meaning is unchanged; document migrations for changed meaning.
3. Download the official HTML locally, then explicitly generate a proposed snapshot:

   ```sh
   python scripts/monitor.py --html work/az900-guide.html --write-baseline work/proposed-baseline.json
   ```

4. Review that snapshot against the curriculum and copy it into `exam/versions/monitor-baseline.json` only in the reviewed PR. The manual flag has no workflow usage. Keep historical version metadata as appropriate.
5. Run validation and tests, review the diff, and require human review before merging semantic changes. A detector report is evidence for investigation, never authorization to remove objectives.

The tool treats fetched content as untrusted data: it extracts text, never executes scripts or follows instructions from pages, and does not send page content to an agent. Fixtures in tests are original synthetic examples; live HTML stays in ignored working files.

## API investigation (verified 2026-10-15)

The [current Platform API reference](https://learn.microsoft.com/en-us/training/support/integrations-learn-platform-api-catalog-endpoints-developer-reference) describes authenticated catalog endpoints under `/api/v1` and says the older unauthenticated Catalog API began deprecation in June 2026. Therefore the MVP does not rely on that legacy endpoint or assume it remains supported.

The [getting-started guide](https://learn.microsoft.com/en-us/training/support/integrations-learn-platform-api-get-started) requires Microsoft Entra authentication: app access uses an app registration or managed identity and a token for `https://learn.microsoft.com/.default`; delegated access requires app registration and user consent, including `PublicContent.Read.All`. Requests require an `api-version`; the documented version is `2023-11-01-preview`. The documented default quota is 100 calls per minute over five minutes, with pagination. These account and credential prerequisites exceed the credential-free MVP. API integration and end-to-end authentication were not tested; consult current documentation and support before onboarding. No API secret is required to study or to run the public-page monitor.
