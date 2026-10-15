import unittest
import copy
from unittest.mock import patch
from scripts import validate as checker
from scripts.validate import validate, validate_graph, unique


class IntegrityTests(unittest.TestCase):
    def test_repository(self):
        validate()

    def test_cycles_and_dangling_edges_fail(self):
        for rows in ([{"id": "a", "prerequisites": ["b"]}],
                     [{"id": "a", "prerequisites": ["b"]}, {"id": "b", "prerequisites": ["a"]}]):
            with self.assertRaises(ValueError):
                validate_graph(rows)

    def test_duplicate_ids_fail(self):
        with self.assertRaises(ValueError):
            unique([{"id": "a"}, {"id": "a"}], "test")

    def test_cross_file_corruption_rejected(self):
        original = checker.load
        for mutation in ("subdomain", "source", "answer", "coverage"):
            def changed(path):
                data = copy.deepcopy(original(path))
                if path == "exam/curriculum.json":
                    if mutation == "subdomain":
                        data["competencies"][0]["subdomain_id"] = "missing"
                    if mutation == "source":
                        data["competencies"][0]["sources"] = ["savill-course"]
                if path == "assessments/questions.json" and mutation == "answer":
                    next(q for q in data["questions"] if q.get("options"))["answer"] = "not an option"
                if path == "exam/coverage.json" and mutation == "coverage":
                    data["objectives"][0]["normalized_source_hash"] = "wrong"
                return data
            with self.subTest(mutation=mutation), patch.object(checker, "load", side_effect=changed):
                with self.assertRaises(ValueError):
                    checker.validate()
