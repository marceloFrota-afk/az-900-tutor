"""Explicit live test: create/update/deduplicate/close one clearly synthetic issue."""
import json
from pathlib import Path

try:
    from . import monitor
except ImportError:
    import monitor


def main():
    output = monitor.ROOT / 'work/monitor-publication-test'
    output.mkdir(parents=True, exist_ok=True)
    marker = '<!-- az900-source-monitor-test:2026-10-15 -->'
    title = '[TEST ONLY] AZ-900 monitor publication — no exam change'
    report = {'status': 'failure', 'test_only': True,
              'error': 'SYNTHETIC publication exercise; no actual exam/source incident', 'test_phase': 1}
    evidence = {'test_only': True, 'repository': 'vmenezesdev/az-900-tutor', 'steps': []}
    number = None

    def issues():
        # List, then filter exact marker: do not depend on delayed GitHub search indexing.
        return [i for i in json.loads(monitor.gh('issue', 'list', '--state', 'open', '--limit', '100',
                                               '--json', 'number,body,url,updatedAt')) if marker in (i.get('body') or '')]

    try:
        if issues():
            raise ValueError('An open publication test already exists; inspect it before retrying')
        monitor.publish_issue(report, output, marker=marker, title=title)
        first = issues()
        assert len(first) == 1
        number = first[0]['number']
        evidence['issue_url'] = first[0]['url']
        evidence['steps'].append('created one clearly labeled synthetic issue')
        monitor.publish_issue(dict(report, checked_at='timestamp-only-repeat'), output, marker=marker, title=title)
        repeated = issues()
        assert len(repeated) == 1 and repeated[0]['body'] == first[0]['body']
        evidence['steps'].append('same report with changed timestamp left body unchanged')
        report['test_phase'] = 2
        monitor.publish_issue(report, output, marker=marker, title=title)
        updated = issues()
        assert len(updated) == 1 and updated[0]['number'] == number and updated[0]['body'] != first[0]['body']
        evidence['steps'].append('changed report updated the same issue')
    finally:
        if number is not None:
            monitor.gh('issue', 'close', str(number))
            evidence['steps'].append('closed test issue')
        (output / 'evidence.json').write_text(json.dumps(evidence, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(evidence))


if __name__ == '__main__':
    main()
