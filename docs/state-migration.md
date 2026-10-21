# Persistence and reviewed migration

Run Python 3.11+ from the repository root. Ordinary sessions continue to use `scripts/tutor.py`; existing valid state-v1 files remain supported. Whole CLI operations lock the state using an exclusive adjacent `.lock` file. A contending writer receives an explicit retry message; successful writes are never silently dropped. Writers outside this utility must honor the same protocol. After a crash, confirm no writer remains before removing a stale lock. Temporary files are flushed and replaced atomically; replacement failure preserves the original. This is not encryption or a guarantee against hardware failure.

Exports contain a SHA-256 canonical JSON checksum. Import checks it when present; modifying an exported response, profile or version invalidates the checksum. It is accidental-corruption detection, not authentication. Raw state-v1 JSON produced by a tool-less chatbot remains importable. Dates, competencies, score types and duplicates are checked in both paths. Exact duplicate evidence objects are rejected rather than inflating evidence counts. An observation with a different ID may still be repeated exposure; the tutor must judge that context.

For curriculum changes, write a plan containing `from_version`, `to_version`, `reviewer`, `reviewed_at`, all `source_competencies`, and exactly one mapping per source ID. Every mapping needs a `reason`, `source`, `change` and `targets`:

| Change | Targets | Treatment |
| --- | --- | --- |
| `preserved` | Same stable ID only | Retain evidence and existing reassessment flag |
| `changed` | One current ID | Preserve observation, require reassessment |
| `split` | Two or more current IDs | Copy historical observation to targets, require reassessment for each |
| `removed` | Empty | Keep original observation in archive, no active evidence |

The mapping is an editorial judgment, not an automatic comparison of labels. A preserved ID must mean genuinely preserved scope; the utility cannot prove that assertion. New objectives without old mappings start unassessed. Review merged evidence particularly carefully. Changed/split history has `requires_reassessment: true`; it cannot establish mastery. Reassessment means a new actually observed event, not silently clearing historical flags.

Execute the included **synthetic fixture, not an official historical version**:

```sh
python scripts/migrate.py tests/fixtures/migration.synthetic-source.json tests/fixtures/migration.synthetic-plan.json .learner/migration-demo.json
python scripts/tutor.py --state .learner/migration-demo.json status
```

Use a new destination for another run. Migration refuses existing destination or backup and never overwrites the source. The new destination embeds the original state and reviewed plan with digests; `migration-demo.json.original.json` also preserves the original ledger. If destination writing fails after backup creation, the source and backup remain; inspect before choosing a new destination. Plan validation failures create neither file. Original exports retain their checksum verification on input; the backup preserves their complete state payload, not its redundant checksum field.

Tests exercise preserved/changed/split/removed mappings, incomplete and malformed plans, retained history, reassessment exclusion, backup/no-overwrite, atomic replacement failure, duplicate events, export tampering and eight concurrent real CLI writers. Synthetic fixtures do not reconstruct any past Microsoft curriculum.


The hosted MCP `import_progress` accepts a state-v1 export. A current-version export merges idempotently. For a different curriculum version, include a reviewed `migration_plan` with the same fields and mapping rules required by `scripts/migrate.py`; changed and split evidence is retained with `requires_reassessment: true`. The original source and plan remain in the migration archive. Do not map objectives based on ID or label similarity alone.
