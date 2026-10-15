import unittest
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
