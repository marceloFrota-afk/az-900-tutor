"""Conservative, credential-free official guide change detection (Python stdlib)."""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
GUIDE = 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-900'
MARKER = '<!-- az900-source-monitor:v1 -->'
MAX_BYTES = 2_000_000


class SourceError(ValueError):
    """Unexpected source structure; never interpret as removed objectives."""


def normalized(text):
    return ' '.join(text.split())


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


class Blocks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.blocks, self.tag, self.parts, self.skip = [], None, [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.skip += 1
        if not self.skip and (tag in ('h2', 'h3', 'h4', 'li') or (tag == 'p' and self.tag is None)):
            if self.tag:
                raise SourceError('Nested or unclosed structural element')
            self.tag, self.parts = tag, []

    def handle_data(self, data):
        if self.tag and not self.skip:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.skip = max(0, self.skip - 1)
        if tag == self.tag:
            self.blocks.append((tag, normalized(''.join(self.parts))))
            self.tag, self.parts = None, []


def snapshot(html, source_url=GUIDE):
    parser = Blocks()
    parser.feed(html)
    # Work strictly within the one versioned skills section, not navigation/changelog.
    starts = [i for i, (tag, text) in enumerate(parser.blocks)
              if tag == 'h2' and text.startswith('Skills measured as of ')]
    if len(starts) != 1:
        raise SourceError('Expected exactly one versioned skills section')
    start = starts[0]
    date_text = parser.blocks[start][1].removeprefix('Skills measured as of ')
    try:
        effective_date = datetime.strptime(date_text, '%B %d, %Y').date().isoformat()
    except ValueError as exc:
        raise SourceError('Unrecognized effective date') from exc
    end = next((i for i in range(start + 1, len(parser.blocks))
                if parser.blocks[i][0] == 'h2'), None)
    if end is None or parser.blocks[end][1] != 'Study resources':
        raise SourceError('Missing expected section boundary')
    section = parser.blocks[start + 1:end]
    domains, editorial, group, domain = [], [], None, None
    for tag, text in section:
        if tag == 'h3':
            group = None
            if re.search(r'\(\d+\s*[–-]\s*\d+%\)$', text):
                domain = {'label': text, 'groups': []}
                domains.append(domain)
            elif domain is None:
                editorial.append((tag, text))
            else:
                raise SourceError('Unknown heading inside objective domains')
        elif tag == 'h4':
            if domain is None:
                raise SourceError('Objective group before domain')
            group = {'label': text, 'objectives': []}
            domain['groups'].append(group)
        elif tag == 'p':
            editorial.append((tag, text))
        elif tag == 'li':
            if group is None:
                if domain is not None:
                    raise SourceError('Objective without group')
                editorial.append((tag, text))
            else:
                if not text:
                    raise SourceError('Empty objective')
                group['objectives'].append(digest(normalized(text)))
    if len(domains) < 2 or len(domains) > 10:
        raise SourceError('Implausible domain count')
    groups = [g for d in domains for g in d['groups']]
    count = sum(len(g['objectives']) for g in groups)
    if len(groups) < 5 or count < 20 or count > 300 or any(not g['objectives'] for g in groups):
        raise SourceError('Incomplete or implausible objective structure')
    result = {'schema_version': 1, 'source_url': source_url,
              'effective_date': effective_date, 'domains': domains,
              'editorial_digest': digest(editorial), 'objective_count': count}
    result['fingerprint'] = digest(result)
    return result


class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urllib.parse.urlparse(newurl)
        original = urllib.parse.urlparse(req.full_url)
        if target.scheme != 'https' or target.hostname != original.hostname:
            raise SourceError('Cross-host or non-HTTPS redirect requires manual review')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        raise SourceError('Only public HTTPS URLs are supported')
    # Optional link checking must not access local/private network endpoints.
    import ipaddress
    import socket
    for address in socket.getaddrinfo(parsed.hostname, 443, type=socket.SOCK_STREAM):
        if not ipaddress.ip_address(address[4][0]).is_global:
            raise SourceError('Non-public address refused')
    request = urllib.request.Request(url, headers={'User-Agent': 'az-900-tutor-monitor/1.0',
                                                  'Accept': 'text/html'})
    with urllib.request.build_opener(SafeRedirect()).open(request, timeout=20) as response:
        if 'text/html' not in response.headers.get('Content-Type', '').lower():
            raise SourceError('Expected HTML response')
        data = response.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise SourceError('Response exceeds size limit')
        return data.decode('utf-8')


def compare(baseline, candidate):
    old, new = baseline['domains'], candidate['domains']
    old_count, new_count = baseline['objective_count'], candidate['objective_count']
    if len(old) != len(new) or new_count < old_count * .75 or new_count > old_count * 1.5:
        raise SourceError('Abrupt structure/count change; investigate before updating')
    changes = []
    if baseline['source_url'] != candidate['source_url']:
        changes.append('source_url_changed')
    if baseline['effective_date'] != candidate['effective_date']:
        changes.append('exam_version_changed')
    before = Counter(h for d in old for g in d['groups'] for h in g['objectives'])
    after = Counter(h for d in new for g in d['groups'] for h in g['objectives'])
    if before != after:
        changes.append('objectives_changed')
    # Labels and placement are reviewed independently; cannot infer semantic equivalence.
    structure = lambda ds: [(d['label'], [(g['label'], g['objectives']) for g in d['groups']]) for d in ds]
    labels = lambda ds: [(d['label'], [g['label'] for g in d['groups']]) for d in ds]
    if labels(old) != labels(new) or (before == after and structure(old) != structure(new)):
        changes.append('nomenclature_or_structure_changed')
    if baseline.get('editorial_digest') != candidate.get('editorial_digest'):
        changes.append('editorial_changed')
    return {'classifications': changes, 'added_objective_digests': sorted((after - before).elements()),
            'removed_objective_digests': sorted((before - after).elements()),
            'old_count': old_count, 'new_count': new_count}


def gh(*args):
    return subprocess.run(['gh', *args], check=True, capture_output=True, text=True).stdout


def publish_issue(report, output):
    """One open monitoring issue; timestamp alone never triggers an update."""
    signature = digest({k: v for k, v in report.items() if k != 'checked_at'})
    signature_marker = f'<!-- report:{signature} -->'
    issues = json.loads(gh('issue', 'list', '--state', 'open', '--search',
                           'in:body "az900-source-monitor:v1"', '--limit', '100',
                           '--json', 'number,body'))
    matches = [i for i in issues if MARKER in i['body']]
    if any(signature_marker in issue['body'] for issue in matches):
        return
    body = output / 'issue.md'
    # No untrusted page text is executed or inserted into shell commands.
    body.write_text(MARKER + '\n' + signature_marker + '\n\n'
                    'Official guide monitoring requires maintainer review. Approved files are unchanged.\n\n'
                    '```json\n' + json.dumps(report, indent=2) + '\n```\n', encoding='utf-8')
    if matches:
        gh('issue', 'edit', str(matches[0]['number']), '--body-file', str(body))
    else:
        gh('issue', 'create', '--title', 'Review AZ-900 official source monitoring', '--body-file', str(body))


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('--baseline', type=Path, default=ROOT / 'exam/versions/monitor-baseline.json')
    cli.add_argument('--html', type=Path, help='Offline HTML input; never executes page content')
    cli.add_argument('--output', type=Path, default=ROOT / 'work/monitor')
    cli.add_argument('--write-baseline', type=Path, help='Explicit manual snapshot generation only')
    cli.add_argument('--issue', action='store_true')
    cli.add_argument('--check-links', action='store_true', help='Optional bounded catalog check')
    args = cli.parse_args(argv)
    args.output.mkdir(parents=True, exist_ok=True)
    report = {'checked_at': datetime.now(timezone.utc).isoformat(timespec='seconds')}
    exit_code = 0
    try:
        candidate = snapshot(args.html.read_text(encoding='utf-8') if args.html else fetch(GUIDE))
        if args.write_baseline:
            args.write_baseline.parent.mkdir(parents=True, exist_ok=True)
            args.write_baseline.write_text(json.dumps(candidate, indent=2) + '\n', encoding='utf-8')
            return 0
        baseline = json.loads(args.baseline.read_text(encoding='utf-8'))
        differences = compare(baseline, candidate)
        report.update(status='changed' if differences['classifications'] else 'unchanged',
                      source_url=GUIDE, baseline_fingerprint=baseline['fingerprint'],
                      candidate_fingerprint=candidate['fingerprint'], differences=differences)
        (args.output / 'candidate.json').write_text(json.dumps(candidate, indent=2) + '\n', encoding='utf-8')
    except (OSError, ValueError, KeyError, urllib.error.URLError) as exc:
        report.update(status='failure', error_type=type(exc).__name__, error=str(exc))
        exit_code = 2
    if args.check_links:
        links = []
        try:
            catalog = json.loads((ROOT / 'resources/catalog.json').read_text(encoding='utf-8'))
            resources = catalog if isinstance(catalog, list) else catalog['resources']
            for resource in resources[:30]:
                try:
                    fetch(resource['url'])
                    links.append({'id': resource['id'], 'status': 'reachable_html'})
                except (OSError, ValueError, urllib.error.URLError) as exc:
                    links.append({'id': resource['id'], 'status': 'review', 'error': str(exc)})
            report['links'] = links
        except (OSError, ValueError, KeyError) as exc:
            report['links_error'] = str(exc)
    (args.output / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))
    if args.issue and (report['status'] != 'unchanged' or any(x['status'] == 'review' for x in report.get('links', []))):
        publish_issue(report, args.output)
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
