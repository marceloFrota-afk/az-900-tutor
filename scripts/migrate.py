"""Explicit, non-destructive curriculum migration. Plans require editorial review."""
import argparse
import copy
import json
from pathlib import Path

try:
    from . import tutor
except ImportError:
    import tutor


def migrate(source, plan):
    if not isinstance(plan, dict):
        raise ValueError("Migration plan must be a JSON object")
    if not isinstance(plan.get("from_version"), str) or not plan["from_version"].strip():
        raise ValueError("Plan must name the source curriculum version")
    if plan.get("to_version") != tutor.version() or plan.get("from_version") == plan.get("to_version"):
        raise ValueError("Plan must migrate a different source version to the approved curriculum")
    if not isinstance(plan.get("reviewer"), str) or not plan["reviewer"].strip():
        raise ValueError("A named mapping reviewer is required; AI review must be labeled AI")
    tutor.iso_date(plan["reviewed_at"])
    old_ids = plan.get("source_competencies")
    if not isinstance(old_ids, list) or not old_ids or not all(isinstance(x, str) and x for x in old_ids) or len(set(old_ids)) != len(old_ids):
        raise ValueError("Plan must list all distinct source competency IDs")
    tutor.validate_state(source, expected_version=plan["from_version"], known_ids=set(old_ids))
    rows = plan.get("mappings", [])
    if not isinstance(rows, list) or not all(isinstance(row, dict) for row in rows):
        raise ValueError("Plan mappings must be an array of objects")
    if len(rows) != len(old_ids) or {r["source"] for r in rows} != set(old_ids):
        raise ValueError("Plan must map every source competency exactly once")
    current = {o["id"] for o in tutor.objectives()}
    by_id = {}
    for row in rows:
        kind, targets = row.get("change"), row.get("targets")
        if kind not in {"preserved", "changed", "split", "removed"}:
            raise ValueError("Unknown mapping change")
        if not isinstance(targets, list) or len(set(targets)) != len(targets) or not set(targets) <= current:
            raise ValueError("Mapping targets must be distinct current competencies")
        if not isinstance(row.get("reason"), str) or not row["reason"].strip():
            raise ValueError("Each mapping requires an editorial reason")
        if (kind == "preserved" and targets != [row["source"]] or
                kind == "changed" and len(targets) != 1 or
                kind == "split" and len(targets) < 2 or
                kind == "removed" and targets):
            raise ValueError("Mapping shape does not match change type")
        by_id[row["source"]] = row
    result = {"schema_version": 1, "curriculum_version": tutor.version(),
              "profile": copy.deepcopy(source["profile"]), "events": [],
              "migration": {"source_sha256": tutor.digest(source), "plan_sha256": tutor.digest(plan),
                            "plan": copy.deepcopy(plan), "original_state": copy.deepcopy(source)}}
    for event in source["events"]:
        row = by_id[event["competency"]]
        for target in row["targets"]:
            translated = copy.deepcopy(event)
            translated["competency"] = target
            if row["change"] != "preserved":
                translated["requires_reassessment"] = True
            # Distinct source events can map to the same evidence. Keep one active copy;
            # the complete original ledger is always retained in migration.original_state.
            if translated not in result["events"]:
                result["events"].append(translated)
    result["events"].sort(key=tutor.event_key)
    return tutor.validate_state(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("plan", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    try:
        if args.source.resolve() == args.destination.resolve():
            raise ValueError("Migration needs a new destination; source is never overwritten")
        with tutor.state_lock(args.source), tutor.state_lock(args.destination):
            backup = args.destination.with_name(args.destination.name + ".original.json")
            with tutor.state_lock(backup):
                if args.destination.exists() or backup.exists():
                    raise ValueError("Destination or original backup exists; choose new paths")
                source = tutor.read(args.source)
                if "_integrity" in source:
                    integrity = source.pop("_integrity")
                    if integrity != {"algorithm": "sha256", "digest": tutor.digest(source)}:
                        raise ValueError("Source export integrity check failed")
                result = migrate(source, tutor.read(args.plan))
                tutor.atomic_write(backup, source)
                tutor.atomic_write(args.destination, result)
        print(json.dumps({"migrated": str(args.destination), "backup": str(backup),
                          "requires_reassessment": sum(e.get("requires_reassessment", False) for e in result["events"])}))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
