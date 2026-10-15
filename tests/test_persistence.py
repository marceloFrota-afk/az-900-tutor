import copy
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

from scripts import migrate, tutor


def event(question="a", competency=None):
    return {"competency": competency or tutor.objectives()[0]["id"], "date": date.today().isoformat(),
            "question": question, "kind": "explanation", "score": 1, "assisted": False,
            "evidence": "SYNTHETIC: explained ownership", "misconception": ""}


def state():
    return {"schema_version": 1, "curriculum_version": tutor.version(),
            "profile": {"deadline": "2026-12-20", "minutes_per_day": 30}, "events": [event()]}


class PersistenceTests(unittest.TestCase):
    def test_lock_excludes_other_writer_and_releases_after_exception(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "state.json"
            with self.assertRaisesRegex(RuntimeError, "synthetic"):
                with tutor.state_lock(p):
                    with self.assertRaisesRegex(ValueError, "locked"):
                        with tutor.state_lock(p):
                            self.fail("second writer admitted")
                    raise RuntimeError("synthetic")
            with tutor.state_lock(p):
                pass

    def test_concurrent_real_cli_writers_never_lose_successful_records(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "state.json"
            s = state()
            s["events"] = []
            tutor.atomic_write(p, s)
            prefix = [sys.executable, str(tutor.ROOT / "scripts/tutor.py"), "--state", str(p), "record", event()["competency"]]
            commands = [prefix + ["--question", f"concurrent-{i}", "--score", "1", "--kind", "explanation", "--evidence", "SYNTHETIC"] for i in range(8)]
            processes = [subprocess.Popen(c, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for c in commands]
            retries = []
            for cmd, process in zip(commands, processes):
                out, err = process.communicate(timeout=30)
                if process.returncode:
                    self.assertIn("locked", err)
                    retries.append(cmd)
            # Wait for every original writer before retrying lock conflicts.
            for cmd in retries:
                retry = subprocess.run(cmd, capture_output=True, text=True)
                self.assertEqual(retry.returncode, 0, retry.stderr)
            self.assertEqual(len(tutor.read(p)["events"]), 8)

    def test_atomic_failure_keeps_original_and_removes_temp(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "state.json"
            tutor.atomic_write(p, state())
            original = p.read_bytes()
            with patch.object(tutor.os, "replace", side_effect=OSError("synthetic disk fault")):
                with self.assertRaises(OSError):
                    tutor.atomic_write(p, {"replacement": True})
            self.assertEqual(p.read_bytes(), original)
            self.assertEqual(list(Path(d).glob("*.tmp")), [])

    def test_duplicate_evidence_and_tampered_export_fail(self):
        s = state()
        s["events"].append(copy.deepcopy(s["events"][0]))
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            tutor.validate_state(s)
        payload = tutor.export_state(state())
        self.assertEqual(tutor.import_state(payload), state())
        payload["events"][0]["score"] = .2
        with self.assertRaisesRegex(ValueError, "integrity"):
            tutor.import_state(payload)
        self.assertEqual(tutor.import_state(state()), state())  # manual tool-less handoff

    def test_same_day_import_order_and_failure_priority(self):
        s = state()
        failed = event("b")
        failed["score"] = 0
        s["events"].append(failed)
        expected = tutor.recommend(s)
        s["events"].reverse()
        self.assertEqual(tutor.recommend(s), expected)
        self.assertEqual(tutor.report(s)[event()["competency"]]["status"], "learning")

    def plan_and_source(self):
        ids = [o["id"] for o in tutor.objectives()[:4]]
        source = state()
        source["curriculum_version"] = "SYNTHETIC-OLD-NOT-OFFICIAL"
        source["events"] = [event(str(i), x) for i, x in enumerate([ids[0], "old-changed", "old-split", "old-removed"])]
        plan = {"from_version": source["curriculum_version"], "to_version": tutor.version(),
                "reviewer": "AI synthetic fixture; not official history", "reviewed_at": date.today().isoformat(),
                "source_competencies": [e["competency"] for e in source["events"]],
                "mappings": [{"source": ids[0], "change": "preserved", "targets": [ids[0]], "reason": "Synthetic identical scope"},
                             {"source": "old-changed", "change": "changed", "targets": [ids[1]], "reason": "Synthetic changed scope"},
                             {"source": "old-split", "change": "split", "targets": ids[2:4], "reason": "Synthetic split"},
                             {"source": "old-removed", "change": "removed", "targets": [], "reason": "Synthetic removal"}]}
        return plan, source

    def test_migration_preserves_history_and_excludes_changed_evidence(self):
        plan, source = self.plan_and_source()
        result = migrate.migrate(source, plan)
        self.assertEqual(result["migration"]["original_state"], source)
        self.assertEqual(result["migration"]["source_sha256"], tutor.digest(source))
        self.assertEqual(len(result["events"]), 4)
        self.assertEqual(len(tutor.active_events(result)), 1)
        self.assertEqual(tutor.report(result)[plan["mappings"][1]["targets"][0]]["status"], "not_assessed")

    def test_malformed_migration_plans_are_rejected_without_partial_files(self):
        plan, source = self.plan_and_source()
        for malformed in (None, [], dict(plan, mappings=[None]), dict(plan, from_version=None)):
            with self.subTest(plan=malformed), self.assertRaises(ValueError):
                migrate.migrate(source, malformed)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            a, b, c = root / "source.json", root / "plan.json", root / "destination.json"
            tutor.atomic_write(a, source)
            tutor.atomic_write(b, None)
            before = a.read_bytes()
            result = subprocess.run([sys.executable, str(tutor.ROOT / "scripts/migrate.py"),
                                     str(a), str(b), str(c)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertIn("plan must be a JSON object", result.stderr)
            self.assertNotIn("Traceback", result.stderr)
            self.assertEqual(a.read_bytes(), before)
            self.assertFalse(c.exists())
            self.assertFalse(c.with_name(c.name + ".original.json").exists())
            self.assertEqual(list(root.glob("*.lock")), [])

    def test_migration_cli_backup_no_overwrite_and_incomplete_plan(self):
        plan, source = self.plan_and_source()
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            a, b, c = d / "source.json", d / "plan.json", d / "destination.json"
            tutor.atomic_write(a, source)
            tutor.atomic_write(b, plan)
            cmd = [sys.executable, str(tutor.ROOT / "scripts/migrate.py"), str(a), str(b), str(c)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(tutor.read(c.with_name(c.name + ".original.json")), source)
            self.assertEqual(tutor.read(a), source)
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
        plan["mappings"].pop()
        with self.assertRaisesRegex(ValueError, "every source"):
            migrate.migrate(source, plan)


if __name__ == "__main__":
    unittest.main()
