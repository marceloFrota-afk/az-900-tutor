import copy
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

from scripts import tutor


def event(day="2026-10-10", question="a", kind="explanation", score=1, assisted=False):
    return {"competency": tutor.objectives()[0]["id"], "date": day, "question": question,
            "kind": kind, "score": score, "assisted": assisted,
            "evidence": "Explained responsibility boundaries with an example", "misconception": ""}


class ProgressTests(unittest.TestCase):
    def test_lucky_answer_never_demonstrates(self):
        result = tutor.competency_status([event(kind="recall")], date(2026, 10, 10))
        self.assertEqual(result["status"], "inconclusive")

    def test_same_day_repeats_never_demonstrate(self):
        events = [event(), event(question="b", kind="application")]
        self.assertEqual(tutor.competency_status(events, date(2026, 10, 10))["status"], "learning")

    def test_transfer_and_spacing_then_expiry(self):
        events = [event(), event(day="2026-10-11", question="b", kind="application")]
        self.assertEqual(tutor.competency_status(events, date(2026, 10, 11))["status"], "demonstrated")
        self.assertEqual(tutor.competency_status(events, date(2026, 10, 15))["status"], "needs_review")

    def test_failure_resets_demonstration(self):
        events = [event(), event(day="2026-10-11", question="b", kind="application"),
                  event(day="2026-10-12", question="c", score=.2)]
        self.assertEqual(tutor.competency_status(events, date(2026, 10, 12))["status"], "learning")

    def test_assisted_answer_is_not_independent_evidence(self):
        events = [event(), event(day="2026-10-11", question="b", kind="application", assisted=True)]
        self.assertNotEqual(tutor.competency_status(events, date(2026, 10, 11))["status"], "demonstrated")

    def test_misconception_blocks_demonstration(self):
        events = [event(), event(day="2026-10-11", question="b", kind="application")]
        events[-1]["misconception"] = "Still confuses service and deployment models"
        self.assertNotEqual(tutor.competency_status(events, date(2026, 10, 11))["status"], "demonstrated")

    def test_cli_roundtrip_invalid_import_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as folder:
            folder = Path(folder)
            script = tutor.ROOT / "scripts/tutor.py"
            state = folder / "state.json"
            def run(*args, state_path=state):
                return subprocess.run([sys.executable, str(script), "--state", str(state_path), *args],
                                      capture_output=True, text=True)
            self.assertEqual(run("init", "--deadline", "2026-12-20").returncode, 0)
            original = state.read_bytes()
            self.assertNotEqual(run("init", "--deadline", "2026-12-20").returncode, 0)
            self.assertEqual(run("record", tutor.objectives()[0]["id"], "--question", "q1", "--score", "1",
                                 "--kind", "recall", "--evidence", "Correct choice, could not justify").returncode, 0)
            saved = state.read_bytes()
            self.assertNotEqual(run("record", "bogus", "--question", "q2", "--score", "nan",
                                    "--kind", "recall", "--evidence", "x").returncode, 0)
            self.assertEqual(state.read_bytes(), saved)
            export = folder / "export.json"
            self.assertEqual(run("export", str(export)).returncode, 0)
            restored = folder / "restored.json"
            self.assertEqual(run("import", str(export), state_path=restored).returncode, 0)
            self.assertEqual(json.loads(restored.read_text()), json.loads(state.read_text()))
            self.assertTrue(json.loads(run("pending").stdout))
            self.assertTrue(json.loads(run("next").stdout))
            bad = json.loads(export.read_text())
            bad["curriculum_version"] = "old"
            export.write_text(json.dumps(bad))
            self.assertNotEqual(run("import", str(export), state_path=folder / "bad.json").returncode, 0)
            self.assertFalse((folder / "bad.json").exists())

    def test_invalid_events_rejected(self):
        for score in (float("nan"), float("inf"), -1, 1.1, True):
            state = {"schema_version": 1, "curriculum_version": tutor.version(),
                     "profile": {"deadline": "2026-12-20", "minutes_per_day": 30}, "events": [event(score=score)]}
            with self.assertRaises(ValueError):
                tutor.validate_state(state)

    def test_noncanonical_dates_rejected(self):
        state = {"schema_version": 1, "curriculum_version": tutor.version(),
                 "profile": {"deadline": "2026-12-20", "minutes_per_day": 30},
                 "events": [event(day="20261010")]}
        with self.assertRaises(ValueError):
            tutor.validate_state(state)

    def test_import_order_does_not_change_priority(self):
        state = {"events": [event(score=.1), event(day="2026-10-11", question="b", kind="application")],
                 "profile": {"deadline": "2026-12-20", "minutes_per_day": 30}}
        expected = tutor.recommend(state, date(2026, 10, 11))
        state["events"].reverse()
        self.assertEqual(tutor.recommend(state, date(2026, 10, 11)), expected)

    def test_recommendation_deterministic_and_respects_time(self):
        state = {"events": [], "profile": {"deadline": "2026-10-17", "minutes_per_day": 10}}
        first = tutor.recommend(state, date(2026, 10, 15))
        self.assertEqual(first, tutor.recommend(state, date(2026, 10, 15)))
        self.assertTrue(all(x["session_minutes"] == 10 for x in first))


if __name__ == "__main__":
    unittest.main()
