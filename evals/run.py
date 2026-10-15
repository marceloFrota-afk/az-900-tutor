"""Prepare a model-neutral qualitative run and summarize explicit reviewer judgments.

This utility never infers tutor quality from keywords or fabricates model responses.
"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def prepare(args):
    if args.output.exists():
        raise ValueError("Output already exists; select a new private file")
    cases = load(ROOT / "evals/scenarios.json")["cases"]
    result = {"schema_version": 1, "condition": args.condition, "model": args.model,
              "model_settings": "FILL: version, sampling, tool access, context and configuration",
              "evaluator": "", "executed_at": "", "cases": []}
    for case in cases:
        result["cases"].append({"id": case["id"], "learner_prompt": case["learner_prompt"],
            "transcript": "", "judgments": [{"id": criterion["id"], "pass": None,
                "evidence": "", "criterion": criterion["criterion"]} for criterion in case["criteria"]]})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"prepared": str(args.output), "status": "not_executed", "cases": len(cases)}


def summarize(args):
    run = load(args.input)
    fixtures = load(ROOT / "evals/scenarios.json")["cases"]
    expected = {c["id"]: {x["id"] for x in c["criteria"]} for c in fixtures}
    if run.get("condition") not in {"with-repository", "baseline"}:
        raise ValueError("Unknown evaluation condition")
    rows = run.get("cases", [])
    if len(rows) != len(expected) or {r["id"] for r in rows} != set(expected):
        raise ValueError("Run must contain each scenario exactly once")
    outcomes = []
    for row in rows:
        judgments = row.get("judgments", [])
        if len(judgments) != len(expected[row["id"]]) or {j["id"] for j in judgments} != expected[row["id"]]:
            raise ValueError("Criteria differ from fixtures")
        complete = bool(run.get("evaluator") and run.get("executed_at") and row.get("transcript", "").strip())
        complete = complete and all(type(j.get("pass")) is bool and j.get("evidence", "").strip() for j in judgments)
        outcome = "not_evaluated" if not complete else ("passed" if all(j["pass"] for j in judgments) else "failed")
        outcomes.append({"id": row["id"], "outcome": outcome})
    return {"condition": run["condition"], "model": run.get("model"),
            "results": outcomes, "passed": sum(r["outcome"] == "passed" for r in outcomes),
            "failed": sum(r["outcome"] == "failed" for r in outcomes),
            "not_evaluated": sum(r["outcome"] == "not_evaluated" for r in outcomes),
            "limitation": "Explicit reviewer judgments only; no automatic model grading or causal claim."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare")
    prep.add_argument("--condition", choices=["with-repository", "baseline"], required=True)
    prep.add_argument("--model", required=True)
    prep.add_argument("--output", type=Path, required=True)
    summary = commands.add_parser("summarize")
    summary.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(prepare(args) if args.command == "prepare" else summarize(args), ensure_ascii=False, indent=2))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
