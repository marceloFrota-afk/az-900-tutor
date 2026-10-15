import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import subprocess
import socket
import urllib.request

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

    def test_corrupt_baseline_is_failure_not_change(self):
        corrupt = dict(self.baseline, objective_count=1)
        with self.assertRaises(m.SourceError):
            m.compare(corrupt, self.baseline)
        corrupt['fingerprint'] = m.digest({k: v for k, v in corrupt.items() if k != 'fingerprint'})
        with self.assertRaises(m.SourceError):
            m.compare(corrupt, self.baseline)
        with self.assertRaises(m.SourceError):
            m.compare([], self.baseline)

    def test_unclosed_html_is_failure(self):
        for suffix in ('<li>truncated', '<script>truncated'):
            with self.subTest(suffix=suffix), self.assertRaises(m.SourceError):
                m.snapshot(self.html + suffix)

    def test_redirect_rechecks_public_dns_and_rejects_credentials_and_ports(self):
        request = urllib.request.Request(m.GUIDE)
        for target in ('https://user@learn.microsoft.com/foo', 'https://learn.microsoft.com:444/foo'):
            with self.subTest(target=target), self.assertRaises(m.SourceError):
                m.SafeRedirect().redirect_request(request, None, 302, '', {}, target)
        with patch.object(socket, 'getaddrinfo', return_value=[(2, 1, 6, '', ('127.0.0.1', 443))]):
            with self.assertRaises(m.SourceError):
                m.SafeRedirect().redirect_request(request, None, 302, '', {}, m.GUIDE + '?redirect')
        with patch.object(socket, 'getaddrinfo', return_value=[(2, 1, 6, '', ('13.107.42.16', 443))]):
            redirected = m.SafeRedirect().redirect_request(request, None, 302, '', {}, m.GUIDE + '?redirect')
            self.assertEqual(m.GUIDE + '?redirect', redirected.full_url)

    def test_fetch_rejects_nonpublic_missing_dns_and_invalid_utf8(self):
        for addresses in ([], [(2, 1, 6, '', ('10.0.0.1', 443))], [(10, 1, 6, '', ('::1', 443))]):
            with patch.object(socket, 'getaddrinfo', return_value=addresses), self.assertRaises(m.SourceError):
                m.fetch(m.GUIDE)
        from unittest.mock import MagicMock
        response = MagicMock()
        response.__enter__.return_value = response
        response.headers = {'Content-Type': 'text/html; charset=utf-8'}
        response.read.return_value = b'\xff'
        with patch.object(m, 'validate_public_url'), patch.object(urllib.request, 'build_opener') as opener:
            opener.return_value.open.return_value = response
            with self.assertRaises(UnicodeDecodeError):
                m.fetch(m.GUIDE)
            response.read.return_value = b'x' * (m.MAX_BYTES + 1)
            with self.assertRaises(m.SourceError):
                m.fetch(m.GUIDE)
            response.headers = {'Content-Type': 'application/json'}
            with self.assertRaises(m.SourceError):
                m.fetch(m.GUIDE)

    def test_publication_failure_preserves_report_and_clears_stale_candidate(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td)
            (output / 'candidate.json').write_text('stale')
            with patch.object(m, 'fetch', side_effect=urllib.error.URLError('offline')), patch.object(
                    m, 'gh', side_effect=subprocess.CalledProcessError(1, ['gh'], stderr='secret')):
                self.assertEqual(3, m.main(['--output', td, '--issue']))
            report = json.loads((output / 'report.json').read_text())
            self.assertEqual('failure', report['status'])
            self.assertEqual('failure', report['publication']['status'])
            self.assertNotIn('secret', json.dumps(report))
            self.assertFalse((output / 'candidate.json').exists())

    def test_separate_publication_alerts_link_catalog_error_without_fetch(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td)
            (output / 'report.json').write_text(json.dumps({'status': 'unchanged', 'links_error': 'invalid catalog'}))
            with patch.object(m, 'fetch') as fetch, patch.object(m, 'publish_issue') as publish:
                self.assertEqual(0, m.main(['--output', td, '--publish-report']))
                fetch.assert_not_called()
                publish.assert_called_once()

    def test_duplicate_open_markers_require_manual_reconciliation(self):
        issues = [{'number': i, 'body': m.MARKER} for i in (12, 13)]
        with tempfile.TemporaryDirectory() as td, patch.object(m, 'gh', return_value=json.dumps(issues)) as gh:
            with self.assertRaises(m.SourceError):
                m.publish_issue({'status': 'failure'}, Path(td))
            self.assertEqual(1, gh.call_count)

    def test_redirect_policy(self):
        import urllib.request
        request = urllib.request.Request(m.GUIDE)
        for target in ('http://learn.microsoft.com/foo', 'https://evil.example/foo'):
            with self.assertRaises(m.SourceError):
                m.SafeRedirect().redirect_request(request, None, 302, '', {}, target)


if __name__ == '__main__':
    unittest.main()
