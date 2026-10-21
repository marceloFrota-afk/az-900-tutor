"""Bundle the current tutor source contracts and data for the optional MCP Worker."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "mcp-worker/src/content.json"
SOURCES = {
    "curriculum": ROOT / "exam/curriculum.json",
    "questions": ROOT / "assessments/questions.json",
    "lessons": ROOT / "lessons/units.pt-BR.json",
    "tutor": ROOT / "TUTOR.md",
    "skill": ROOT / ".agents/skills/az-900-tutor/SKILL.md",
    "protocol": ROOT / "pedagogy/protocol.md",
    "evidence": ROOT / "pedagogy/evidence.md",
}


def bundle():
    result = {}
    for key, path in SOURCES.items():
        text = path.read_text(encoding="utf-8")
        result[key] = json.loads(text) if path.suffix == ".json" else text
    return json.dumps(result, ensure_ascii=False, indent=2) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the checked-in Worker content is stale")
    args = parser.parse_args()
    expected = bundle()
    if args.check:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != expected:
            parser.error("mcp-worker/src/content.json is stale; run python scripts/sync_mcp_content.py")
        print("MCP bundle matches the source curriculum, questions, lessons and pedagogy")
    else:
        TARGET.write_text(expected, encoding="utf-8")
        print(f"Wrote {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
