"""Portable evidence ledger. Run from any directory; state defaults to repository .learner/."""
import argparse
import json
import math
import os
import tempfile
import hashlib
from contextlib import contextmanager
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def curriculum():
    return read(ROOT / "exam/curriculum.json")


def objectives():
    data = curriculum()
    return data.get("competencies", data.get("objectives", []))


def version():
    return objectives()[0]["exam_version"]


def iso_date(value):
    if not isinstance(value, str):
        raise ValueError("Date must be YYYY-MM-DD text")
    parsed = date.fromisoformat(value)
    if parsed.isoformat() != value:
        raise ValueError("Date must use canonical YYYY-MM-DD format")
    return parsed


def atomic_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(dir=path.parent, prefix=".state-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


@contextmanager
def state_lock(path):
    """Cooperating processes lock the whole read/modify/write transaction."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lock = path.with_name(path.name + ".lock")
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError(f"State is locked: {lock}. Retry; after a crash verify no writer remains before removing this lock.") from None
    try:
        os.write(fd, str(os.getpid()).encode("ascii"))
        os.close(fd)
        fd = None
        yield
    finally:
        if fd is not None:
            os.close(fd)
        lock.unlink()


def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":"), allow_nan=False).encode("utf-8")).hexdigest()


def export_state(state):
    payload = dict(state)
    payload["_integrity"] = {"algorithm": "sha256", "digest": digest(state)}
    return payload


def import_state(payload):
    if not isinstance(payload, dict):
        raise ValueError("Import must be a JSON object")
    state = {k: v for k, v in payload.items() if k != "_integrity"}
    check = payload.get("_integrity")
    if check is not None and check != {"algorithm": "sha256", "digest": digest(state)}:
        raise ValueError("Export integrity check failed; original file remains unchanged")
    return validate_state(state)


def event_key(event):
    return (event["date"], digest(event))


def active_events(state):
    return [e for e in state["events"] if not e.get("requires_reassessment", False)]


def validate_state(state, *, expected_version=None, known_ids=None):
    if not isinstance(state, dict) or state.get("schema_version") != 1:
        raise ValueError("Unsupported learner schema; expected schema_version 1")
    if state.get("curriculum_version") != (expected_version or version()):
        raise ValueError("Curriculum version differs; review objectives before migration")
    if not isinstance(state.get("profile"), dict) or not isinstance(state.get("events"), list):
        raise ValueError("Profile must be an object and events must be an array")
    profile = state["profile"]
    if not isinstance(profile.get("minutes_per_day"), int) or isinstance(profile["minutes_per_day"], bool) or profile["minutes_per_day"] <= 0:
        raise ValueError("minutes_per_day must be a positive integer")
    iso_date(profile["deadline"])
    known = known_ids if known_ids is not None else {o["id"] for o in objectives()}
    seen = set()
    for event in state["events"]:
        if not isinstance(event, dict) or event.get("competency") not in known:
            raise ValueError("Unknown competency in event")
        score = event.get("score")
        if isinstance(score, bool) or not isinstance(score, (int, float)) or not math.isfinite(score) or not 0 <= score <= 1:
            raise ValueError("Score must be finite and between 0 and 1")
        if event.get("kind") not in {"recall", "explanation", "application"}:
            raise ValueError("Unknown evidence kind")
        for key in ("question", "evidence", "misconception"):
            if not isinstance(event.get(key), str):
                raise ValueError(f"Event {key} must be text")
        if not event["question"].strip() or not event["evidence"].strip():
            raise ValueError("Question and evidence cannot be empty")
        when = iso_date(event["date"])
        if when > date.today():
            raise ValueError("Future assessment evidence is invalid")
        if type(event.get("assisted")) is not bool:
            raise ValueError("assisted must be boolean")
        if "requires_reassessment" in event and type(event["requires_reassessment"]) is not bool:
            raise ValueError("requires_reassessment must be boolean")
        fingerprint = digest(event)
        if fingerprint in seen:
            raise ValueError("Duplicate evidence event; retrying the same record does not add evidence")
        seen.add(fingerprint)
    return state


def competency_status(events, today=None):
    today = today or date.today()
    if not events:
        return {"status": "not_assessed", "next_review": None, "evidence_count": 0}
    events = sorted(events, key=event_key)
    last = events[-1]
    good = [e for e in events if e["score"] >= .8 and not e["assisted"] and not e["misconception"].strip()]
    # Distinct days + distinct prompts + explanation/application, after most recent failure.
    failures = [e["date"] for e in events if e["score"] < .8 or e["assisted"] or e["misconception"].strip()]
    good = [e for e in good if not failures or e["date"] > max(failures)]
    demonstrated = (len({e["date"] for e in good}) >= 2 and
                    len({e["question"] for e in good}) >= 2 and
                    {"explanation", "application"}.issubset({e["kind"] for e in good}))
    interval = min(14, 3 * max(1, len({e["date"] for e in good}) - 1)) if demonstrated else 1
    due = date.fromisoformat(last["date"]) + timedelta(days=interval)
    status = "demonstrated" if demonstrated else "learning"
    if len(events) == 1 and (last["kind"] == "recall" or last["assisted"]):
        status = "inconclusive"
    if due <= today:
        status = "needs_review"
    return {"status": status, "next_review": due.isoformat(), "evidence_count": len(events)}


def report(state, today=None):
    return {o["id"]: competency_status([e for e in active_events(state) if e["competency"] == o["id"]], today)
            for o in objectives()}


def recommend(state, today=None):
    """Transparent heuristic, no calibrated probability or official per-objective weights."""
    today = today or date.today()
    statuses = report(state, today)
    weights = {"D1": .275, "D2": .375, "D3": .325}
    counts = {d: sum(o["domain_id"] == d for o in objectives()) for d in weights}
    bank = read(ROOT / "assessments/questions.json")["questions"]
    used = {e["question"] for e in state["events"]}
    ranked = []
    for o in objectives():
        s = statuses[o["id"]]
        if s["status"] == "demonstrated":
            continue
        missing = [p for p in o["prerequisites"] if statuses[p]["status"] != "demonstrated"]
        events = [e for e in active_events(state) if e["competency"] == o["id"]]
        urgency = 4 if s["status"] == "needs_review" else 2
        uncertainty = 1 / (1 + len(events))
        latest_day = max((e["date"] for e in events), default=None)
        error = int(any(e["date"] == latest_day and (e["score"] < .8 or e["misconception"].strip()) for e in events))
        days_left = max(1, (date.fromisoformat(state["profile"]["deadline"]) - today).days)
        priority = (urgency + uncertainty + error + weights[o["domain_id"]] * 10 / counts[o["domain_id"]]) / (1 + len(missing))
        ranked.append({"competency": o["id"], "name": o["name"], "priority": round(priority, 4),
                       "reason": s["status"], "prerequisites_to_check": missing,
                       "session_minutes": min(state["profile"]["minutes_per_day"], 15 if days_left <= 3 else 25),
                       "avoid_questions": sorted({e["question"] for e in events}),
                       "question_candidates": [q["id"] for q in bank if q["competency_id"] == o["id"] and q["id"] not in used],
                       "fallback": "If no unseen bank item exists, author a changed scenario from the objective rubric; identify it as unreviewed."})
    return sorted(ranked, key=lambda r: (-r["priority"], r["competency"]))[:5]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state", type=Path, default=ROOT / ".learner/state.json")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init")
    init.add_argument("--deadline", required=True)
    init.add_argument("--minutes", type=int, default=45)
    init.add_argument("--language", default="pt-BR")
    init.add_argument("--experience", default="not provided")
    init.add_argument("--goal", default="AZ-900 preparation")
    sub.add_parser("status")
    sub.add_parser("pending")
    sub.add_parser("next")
    sub.add_parser("reviews")
    rec = sub.add_parser("record")
    rec.add_argument("competency")
    rec.add_argument("--question", required=True)
    rec.add_argument("--score", type=float, required=True)
    rec.add_argument("--kind", choices=["recall", "explanation", "application"], required=True)
    rec.add_argument("--evidence", required=True)
    rec.add_argument("--misconception", default="")
    rec.add_argument("--assisted", action="store_true")
    rec.add_argument("--date", default=date.today().isoformat())
    for command in ("export", "import"):
        sub.add_parser(command).add_argument("path", type=Path)
    args = parser.parse_args(argv)
    try:
        with state_lock(args.state):
            if args.command == "init":
                if args.state.exists():
                    raise ValueError("State already exists; select another --state path")
                state = {"schema_version": 1, "curriculum_version": version(), "profile": {
                    "goal": args.goal, "deadline": args.deadline, "minutes_per_day": args.minutes,
                    "language": args.language, "experience": args.experience}, "events": []}
                validate_state(state)
                atomic_write(args.state, state)
                output = {"initialized": str(args.state)}
            elif args.command == "import":
                if args.state.exists():
                    raise ValueError("Import refuses to overwrite state; choose a new --state path")
                state = import_state(read(args.path))
                atomic_write(args.state, state)
                output = {"imported": str(args.state)}
            else:
                state = validate_state(read(args.state))
                if args.command == "record":
                    state["events"].append({"competency": args.competency, "question": args.question,
                        "score": args.score, "kind": args.kind, "evidence": args.evidence,
                        "misconception": args.misconception, "assisted": args.assisted, "date": args.date})
                    validate_state(state)
                    atomic_write(args.state, state)
                    output = report(state)[args.competency]
                elif args.command == "export":
                    if args.path.resolve() == args.state.resolve():
                        raise ValueError("Export destination must differ from state")
                    with state_lock(args.path):
                        if args.path.exists():
                            raise ValueError("Export destination already exists")
                        atomic_write(args.path, export_state(state))
                    output = {"exported": str(args.path), "privacy": "Contains personal evidence; keep private"}
                elif args.command == "next":
                    output = recommend(state)
                else:
                    output = report(state)
                    if args.command in {"pending", "reviews"}:
                        output = {k: v for k, v in output.items() if
                                  (v["status"] == "needs_review" if args.command == "reviews" else v["status"] != "demonstrated")}
        print(json.dumps(output, indent=2, ensure_ascii=False))
    except (ValueError, KeyError, TypeError, OSError) as error:
        parser.exit(2, f"Error: {error}\n")


if __name__ == "__main__":
    main()
