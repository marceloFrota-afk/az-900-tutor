import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

spec = importlib.util.spec_from_file_location('monitor', Path(__file__).parents[1] / 'scripts/monitor.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def fixture(date='July 20, 2026', count=5):
    domains = ''.join('<h3>Domain %d (25–30%%)</h3>' % d + ''.join(
        '<h4>Group %d.%d</h4><ul>' % (d, g) + ''.join(
            '<li><p>Original test concept %d.%d.%d</p></li>' % (d, g, i)
            for i in range(count)) + '</ul>' for g in range(3)) for d in range(2))
    return '<h2>Skills measured as of %s</h2><h3>Audience profile</h3>%s<h2>Study resources</h2>' % (date, domains)


class MonitorTests(unittest.TestCase):
    def setUp(self):
        self.html = fixture()
        self.baseline = m.snapshot(self.html)

    def test_deterministic_and_formatting_ignored(self):
        self.assertEqual(self.baseline, m.snapshot(self.html.replace('Original test', 'Original  \n test')))
        self.assertEqual([], m.compare(self.baseline, m.snapshot(self.html))['classifications'])
        self.assertNotIn('Original test concept', json.dumps(self.baseline))

    def test_objective_change_and_removal(self):
        result = m.compare(self.baseline, m.snapshot(self.html.replace('Original test concept 0.0.0', 'Changed test concept')))
        self.assertIn('objectives_changed', result['classifications'])
        self.assertEqual(1, len(result['added_objective_digests']))
        self.assertEqual(1, len(result['removed_objective_digests']))
        result = m.compare(self.baseline, m.snapshot(self.html.replace('<li><p>Original test concept 0.0.0</p></li>', '')))
        self.assertEqual(1, len(result['removed_objective_digests']))

    def test_version_editorial_and_labels(self):
        self.assertIn('exam_version_changed', m.compare(self.baseline, m.snapshot(fixture('August 20, 2026')))['classifications'])
        self.assertEqual(['editorial_changed'], m.compare(self.baseline, m.snapshot(self.html.replace('Audience profile', 'Candidate profile')))['classifications'])
        self.assertEqual(['nomenclature_or_structure_changed'], m.compare(self.baseline, m.snapshot(self.html.replace('Group 0.0', 'New group name')))['classifications'])

    def test_malformed_or_empty_is_failure(self):
        for html in ('<html>Blocked</html>', self.html.replace('<h2>Study resources</h2>', ''), fixture(count=0), self.html.replace('July 20, 2026', 'unknown'), self.html + self.html):
            with self.subTest(html=html[:50]), self.assertRaises(m.SourceError):
                m.snapshot(html)

    def test_abrupt_deletion_is_failure(self):
        with self.assertRaises(m.SourceError):
            m.compare(m.snapshot(fixture(count=10)), self.baseline)

    def test_cli_network_failure_preserves_baseline(self):
        with tempfile.TemporaryDirectory() as td:
            baseline = Path(td) / 'baseline.json'
            baseline.write_text(json.dumps(self.baseline))
            before = baseline.read_bytes()
            with patch.object(m, 'fetch', side_effect=urllib.error.URLError('unavailable')):
                self.assertEqual(2, m.main(['--baseline', str(baseline), '--output', td]))
            self.assertEqual(before, baseline.read_bytes())
            self.assertEqual('failure', json.loads((Path(td) / 'report.json').read_text())['status'])

    def test_cli_changed_does_not_write_approved_file(self):
        with tempfile.TemporaryDirectory() as td:
            baseline = Path(td) / 'baseline.json'
            baseline.write_text(json.dumps(self.baseline))
            before = baseline.read_bytes()
            with patch.object(m, 'fetch', return_value=self.html.replace('concept 0.0.0', 'updated concept')):
                self.assertEqual(0, m.main(['--baseline', str(baseline), '--output', td]))
            self.assertEqual(before, baseline.read_bytes())
            self.assertEqual('changed', json.loads((Path(td) / 'report.json').read_text())['status'])

    def test_issue_dedup_ignores_timestamp_and_updates_meaningful_change(self):
        report = {'checked_at': 'today', 'status': 'failure', 'error': 'unavailable'}
        sig = m.digest({k: v for k, v in report.items() if k != 'checked_at'})
        body = m.MARKER + '\n<!-- report:%s -->' % sig
        with tempfile.TemporaryDirectory() as td:
            with patch.object(m, 'gh', return_value=json.dumps([{'number': 12, 'body': body}])) as gh:
                m.publish_issue(dict(report, checked_at='tomorrow'), Path(td))
                self.assertEqual(1, gh.call_count)
            with patch.object(m, 'gh', side_effect=[json.dumps([{'number': 12, 'body': body}]), '']) as gh:
                m.publish_issue(dict(report, error='malformed'), Path(td))
                self.assertEqual('edit', gh.call_args.args[1])
            with patch.object(m, 'gh', side_effect=['[]', '']) as gh:
                m.publish_issue(report, Path(td))
                self.assertEqual('create', gh.call_args.args[1])

    def test_redirect_policy(self):
        import urllib.request
        request = urllib.request.Request(m.GUIDE)
        for target in ('http://learn.microsoft.com/foo', 'https://evil.example/foo'):
            with self.assertRaises(m.SourceError):
                m.SafeRedirect().redirect_request(request, None, 302, '', {}, target)


if __name__ == '__main__':
    unittest.main()
