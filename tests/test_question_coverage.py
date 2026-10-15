"""Editorial coverage contracts, not measurements of learner understanding."""
import copy
from collections import Counter
import unittest
from unittest.mock import patch

from scripts import validate as checker


class QuestionCoverageTests(unittest.TestCase):
    def test_every_competency_has_an_original_scenario(self):
        curriculum = checker.load("exam/curriculum.json")
        bank = checker.load("assessments/questions.json")
        rows = bank["questions"]
        expected = {c["id"]: c["domain_id"] for c in curriculum["competencies"]}
        self.assertEqual(set(expected), {q["competency_id"] for q in rows})
        for q in rows:
            with self.subTest(question=q["id"]):
                self.assertTrue(q["original"])
                self.assertEqual(expected[q["competency_id"]], q["domain_id"])
                self.assertTrue(q["source_urls"])
                self.assertTrue(all(u.startswith("https://learn.microsoft.com/") for u in q["source_urls"]))
                self.assertEqual("0..3", q["rubric"]["scale"])
                self.assertTrue(q["rubric"]["criterion"])
                self.assertTrue(q["rubric"]["no_credit"])
        self.assertEqual(len(rows), bank["provenance"]["coverage"]["question_count"])
        self.assertEqual(len(expected), bank["provenance"]["coverage"]["competency_count"])
        self.assertEqual(curriculum["version"], bank["provenance"]["coverage"]["curriculum_version"])

    def test_original_ids_keep_primary_meaning(self):
        primary = ["1.1.2", "1.1.3", "1.1.5", "1.1.7", "1.2.1", "1.2.2", "1.3.1", "1.3.2", "1.3.3",
                   "2.1.2", "2.1.7", "2.2.1", "2.2.4", "2.2.5", "2.2.6", "2.3.1", "2.3.2", "2.3.3",
                   "2.3.6", "2.4.2", "2.4.5", "3.1.2", "3.1.3", "3.1.4", "3.2.2", "3.2.3", "3.3.3",
                   "3.3.5", "3.4.2", "3.4.3"]
        rows = {q["id"]: q for q in checker.load("assessments/questions.json")["questions"]}
        for n, competency in enumerate(primary, 1):
            self.assertEqual("AZ900-" + competency, rows[f"Q{n:03d}"]["competency_id"])

    def test_transfer_variants_have_distinct_scenarios(self):
        bank = checker.load("assessments/questions.json")
        rows = bank["questions"]
        variants = [q for q in rows if q.get("transfer_variant")]
        self.assertGreaterEqual(len(variants), 8)
        self.assertEqual({q["id"] for q in variants}, set(bank["provenance"]["coverage"]["transfer_question_ids"]))
        self.assertEqual(len(rows), len({q["prompt"] for q in rows}))
        coverage = Counter(q["competency_id"] for q in rows)
        for q in variants:
            with self.subTest(question=q["id"]):
                self.assertEqual("transfer", q["skill_type"])
                self.assertGreaterEqual(coverage[q["competency_id"]], 2)
                self.assertNotEqual("multiple_choice", q["type"])

    def test_validator_rejects_missing_competency_despite_all_domains(self):
        original = checker.load

        def missing(path):
            data = copy.deepcopy(original(path))
            if path == "assessments/questions.json":
                data["questions"] = [q for q in data["questions"] if q["competency_id"] != "AZ900-2.4.8"]
            return data

        with patch.object(checker, "load", side_effect=missing):
            with self.assertRaises(ValueError):
                checker.validate()


if __name__ == "__main__":
    unittest.main()
