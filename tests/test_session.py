import tempfile
import unittest
from pathlib import Path
from scripts import session_smoke, tutor


class SessionTests(unittest.TestCase):
    def test_real_cli_synthetic_journey_and_manual_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "fresh"
            result = session_smoke.execute(output)
            self.assertTrue(result["roundtrip_equal"])
            self.assertTrue(result["manual_handoff_import_equal"])
            report = tutor.read(output / "report.json")
            self.assertEqual(len(report["exchanges"]), 5)
            self.assertEqual(report["due_reviews"], {})
            self.assertTrue(all(c["exit_code"] == 0 for c in report["commands"]))
            with self.assertRaisesRegex(ValueError, "fresh"):
                session_smoke.execute(output)
