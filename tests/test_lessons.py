"""Structural content checks; these do not grade factual or teaching quality."""
import json
from datetime import date
from pathlib import Path
import unittest
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]


class LessonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.curriculum = json.loads((ROOT / 'exam/curriculum.json').read_text(encoding='utf-8'))
        cls.lessons = json.loads((ROOT / 'lessons/units.pt-BR.json').read_text(encoding='utf-8'))
        cls.units = cls.lessons['units']

    def test_exact_coverage_of_approved_objectives(self):
        expected = {c['id'] for c in self.curriculum['competencies']}
        actual = [u['competency_id'] for u in self.units]
        self.assertEqual(set(actual), expected)
        self.assertEqual(len(actual), len(set(actual)), 'Duplicate competency coverage')
        ids = [u['id'] for u in self.units]
        self.assertEqual(len(ids), len(set(ids)), 'Duplicate lesson IDs')
        for unit in self.units:
            self.assertEqual(unit['id'], 'L-' + unit['competency_id'].removeprefix('AZ900-'))

    def test_curriculum_version_and_language_are_explicit(self):
        self.assertEqual(self.lessons['schema_version'], '1.0')
        self.assertEqual(self.lessons['curriculum_version'], self.curriculum['version'])
        self.assertEqual(self.lessons['language'], 'pt-BR')
        self.assertEqual(self.lessons['edition'], 'essential-original')

    def test_each_unit_teaches_and_checks_transfer(self):
        for unit in self.units:
            with self.subTest(unit=unit['id']):
                for field in ('title', 'explanation', 'worked_example', 'contrast',
                              'retrieval_prompt', 'transfer_prompt'):
                    self.assertIsInstance(unit[field], str)
                    self.assertGreater(len(unit[field].strip()), 1 if field == 'title' else 15, field)
                self.assertNotEqual(unit['retrieval_prompt'], unit['transfer_prompt'])
                self.assertNotEqual(unit['explanation'], unit['worked_example'])
                self.assertIsInstance(unit['estimated_minutes'], int)
                self.assertGreaterEqual(unit['estimated_minutes'], 3)
                self.assertLessEqual(unit['estimated_minutes'], 20)

    def test_prompts_are_not_repeated_across_objectives(self):
        for field in ('retrieval_prompt', 'transfer_prompt'):
            values = [u[field] for u in self.units]
            self.assertEqual(len(values), len(set(values)), field)

    def test_official_sources_and_review_dates_exist(self):
        for unit in self.units:
            with self.subTest(unit=unit['id']):
                self.assertTrue(unit['source_urls'])
                self.assertEqual(len(unit['source_urls']), len(set(unit['source_urls'])))
                for url in unit['source_urls']:
                    parsed = urlparse(url)
                    self.assertEqual(parsed.scheme, 'https')
                    self.assertEqual(parsed.netloc, 'learn.microsoft.com')
                    self.assertTrue(parsed.path.startswith('/en-us/training/modules/'))
                self.assertEqual(date.fromisoformat(unit['reviewed_on']).isoformat(),
                                 unit['reviewed_on'])


if __name__ == '__main__':
    unittest.main()
