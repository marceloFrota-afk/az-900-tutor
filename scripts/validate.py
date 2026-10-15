"""Validate cross-file contracts without third-party dependencies."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(rows, label):
    ids = [r["id"] for r in rows]
    require(len(ids) == len(set(ids)), f"Duplicate {label} ID")
    return set(ids)


def validate_graph(rows):
    graph = {r["id"]: r["prerequisites"] for r in rows}
    seen, active = set(), set()

    def visit(node):
        require(node in graph, f"Unknown prerequisite: {node}")
        require(node not in active, f"Prerequisite cycle at {node}")
        if node in seen:
            return
        active.add(node)
        for parent in graph[node]:
            visit(parent)
        active.remove(node)
        seen.add(node)

    for node in graph:
        visit(node)


def validate():
    c = load("exam/curriculum.json")
    rows = c["competencies"]
    ids = unique(rows, "competency")
    domains = unique(c["domains"], "domain")
    catalog = load("resources/catalog.json")
    resources = catalog if isinstance(catalog, list) else catalog["resources"]
    resource_ids = unique(resources, "resource")
    for d in c["domains"]:
        require(0 < d["weight_min"] <= d["weight_max"] < 100, "Invalid domain weights")
    validate_graph(rows)
    for row in rows:
        for field in ("name", "description", "subdomain_id", "learning_objectives", "concepts",
                      "evaluation_criteria", "mastery_criteria", "provenance", "misconceptions"):
            require(bool(row.get(field)), f"{row['id']}: missing {field}")
        require(row["domain_id"] in domains, f"Unknown domain: {row['id']}")
        require(row["exam_version"] == c["version"], f"Stale objective: {row['id']}")
        refs = row.get("sources", row.get("official_references", []))
        require(bool(refs), f"Unsourced objective: {row['id']}")
        require(set(refs) <= resource_ids, f"Unknown source: {row['id']}")
        require(set(row.get("complementary_resources", [])) <= resource_ids, f"Unknown complement: {row['id']}")
    for resource in resources:
        require(resource["url"].startswith("https://"), f"Non-HTTPS URL: {resource['id']}")
        require(set(resource.get("competencies", resource.get("competency_ids", []))) <= ids,
                f"Unknown catalog competency: {resource['id']}")
        require(set(resource.get("domains", resource.get("domain_ids", []))) <= domains,
                f"Unknown catalog domain: {resource['id']}")
    # Independent, editor-approved source outline: catches dropped/added/mis-mapped bullets.
    coverage = load("exam/coverage.json")
    mapped = coverage["objectives"]
    require(len(mapped) == len(ids), "Coverage count differs")
    require({x["competency_id"] for x in mapped} == ids, "Coverage IDs differ")
    require(len({x["source_anchor"] for x in mapped}) == len(mapped), "Duplicate source objective mapping")
    for x in mapped:
        row = next(r for r in rows if r["id"] == x["competency_id"])
        require(row["domain_id"] == x["domain_id"], "Coverage domain differs")
    questions = load("assessments/questions.json")
    questions = questions if isinstance(questions, list) else questions["questions"]
    unique(questions, "question")
    qdomains = set()
    for q in questions:
        require(q["competency_id"] in ids, f"Unknown question competency: {q['id']}")
        row = next(r for r in rows if r["id"] == q["competency_id"])
        require(q["domain_id"] == row["domain_id"], f"Question domain mismatch: {q['id']}")
        for field in ("prompt", "answer", "rubric", "rationale", "source_urls", "difficulty", "skill_type"):
            require(bool(q.get(field)), f"Question {q['id']}: missing {field}")
        if q.get("options"):
            require(bool(q.get("distractor_rationales")), f"Question {q['id']}: missing distractor feedback")
        qdomains.add(q["domain_id"])
    require(qdomains == domains, "Question bank misses a domain")
    skill = (ROOT / ".agents/skills/az-900-tutor/SKILL.md").read_text(encoding="utf-8")
    require(skill.startswith("---\n"), "Skill requires YAML frontmatter")
    front = skill.split("---", 2)[1]
    require(re.search(r"^name: az-900-tutor$", front, re.M), "Skill name differs")
    require(re.search(r"^description: .+", front, re.M), "Skill description missing")
    print(f"Validated {len(rows)} objectives, {len(resources)} resources, {len(questions)} questions and skill contracts")


if __name__ == "__main__":
    try:
        validate()
    except (KeyError, TypeError, ValueError, OSError) as exc:
        raise SystemExit(f"Validation failed: {exc}") from exc
