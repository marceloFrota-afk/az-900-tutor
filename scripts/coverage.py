"""Generate question/lesson coverage from actual stable competency IDs."""
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def coverage():
    def load(path):
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    curriculum = load("exam/curriculum.json")
    questions = load("assessments/questions.json")["questions"]
    units = load("lessons/units.pt-BR.json")["units"]
    counts = Counter(q["competency_id"] for q in questions)
    taught = {u["competency_id"] for u in units}
    return {"curriculum_version": curriculum["version"], "competencies": len(curriculum["competencies"]),
            "units": len(units), "questions": len(questions),
            "questions_by_domain": dict(sorted(Counter(q["domain_id"] for q in questions).items())),
            "questions_by_skill_type": dict(sorted(Counter(q["skill_type"] for q in questions).items())),
            "questions_by_format": dict(sorted(Counter("multiple_choice" if q.get("options") else "open_response" for q in questions).items())),
            "coverage": [{"competency": o["id"], "question_count": counts[o["id"]], "lesson": o["id"] in taught} for o in curriculum["competencies"]],
            "missing_questions": [o["id"] for o in curriculum["competencies"] if not counts[o["id"]]],
            "missing_lessons": [o["id"] for o in curriculum["competencies"] if o["id"] not in taught],
            "limitation": "Structural coverage does not establish factual accuracy, exhaustive compound-objective sampling or mastery."}


if __name__ == "__main__":
    print(json.dumps(coverage(), ensure_ascii=False, indent=2))
