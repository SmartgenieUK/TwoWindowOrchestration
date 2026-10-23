#!/usr/bin/env python3
"""Small, cooperative two-window workflow. Standard library only; no model APIs.

The Markdown brief is authoritative. INDEX.md is a generated view. A short-lived
exclusive lock serialises CLI transitions. This is NOT an adversarial security boundary.
"""
import argparse
import difflib
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / 'docs/co-arch'
BRIEF = STATE / 'BRIEF-001-retry-budget.md'
SECTIONS = ['Context and decision', 'Brief', 'Executor summary', 'Acceptance', 'History']
ACTIVE = {'issued', 'returned'}

def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')

def digest(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def atomic_write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.write-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='\n') as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)

@contextmanager
def locked():
    STATE.mkdir(parents=True, exist_ok=True)
    path = STATE / '.lock'
    try:
        fd = os.open(str(path), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise ValueError('Workflow busy. If a prior process crashed, verify it has stopped before removing docs/co-arch/.lock.')
    try:
        with os.fdopen(fd, 'w') as handle:
            handle.write(f'pid={os.getpid()} time={now()}\n')
        yield
    finally:
        path.unlink(missing_ok=True)

def read_brief(path=BRIEF):
    text = path.read_text(encoding='utf-8')
    match = re.search(r'<!-- workflow\n(.*?)\n-->', text, re.S)
    if not match:
        raise ValueError(f'Missing workflow metadata: {path.name}')
    meta = json.loads(match.group(1))
    sections = {}
    for i, title in enumerate(SECTIONS, 1):
        section = re.search(rf'<!-- section:{i} -->\n(.*?)\n<!-- /section:{i} -->', text, re.S)
        if not section:
            raise ValueError(f'Missing section {i}: {path.name}')
        sections[title] = section.group(1)
    return meta, sections

def save_brief(meta, sections):
    text = '# BRIEF-001 Retry budget\n\n'
    text += '<!-- workflow\n' + json.dumps(meta, indent=2, sort_keys=True) + '\n-->\n\n'
    text += f"Status: {meta['status']}\nRevision: {meta['revision']}\n\n"
    for i, title in enumerate(SECTIONS, 1):
        text += f'## {i} {title}\n\n<!-- section:{i} -->\n{sections[title]}\n<!-- /section:{i} -->\n\n'
    atomic_write(BRIEF, text)
    rebuild_index()

def rebuild_index():
    lines = ['# Brief index', '', 'Generated from brief metadata. Rebuild with `python tools/workflow.py status`.', '']
    for path in sorted(STATE.glob('BRIEF-*.md')):
        meta, _ = read_brief(path)
        lines.append(f"- {meta['id']} retry-budget — {meta['status']} — revision {meta['revision']}")
    atomic_write(STATE / 'INDEX.md', '\n'.join(lines) + '\n')

def active_briefs():
    return [(p, read_brief(p)[0]) for p in STATE.glob('BRIEF-*.md')
            if read_brief(p)[0]['status'] in ACTIVE]

def snapshot():
    paths = []
    for directory in ['src', 'tests', 'tools']:
        paths.extend(p for p in (ROOT / directory).rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    paths.append(ROOT / 'docs/CONTRACT.md')
    return {str(p.relative_to(ROOT)).replace(os.sep, '/'): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths)}

def record_digest(sections):
    return digest('\n'.join(sections[title] for title in SECTIONS[:3]))

def check(suite):
    module = 'tests.test_basic' if suite == 'basic' else 'tests.test_acceptance'
    result = subprocess.run([sys.executable, '-m', 'unittest', module, '-v'],
                            cwd=ROOT, capture_output=True, text=True, timeout=30)
    path = STATE / 'evidence' / f'{suite}-{uuid.uuid4().hex[:12]}.txt'
    command = f'{sys.executable} -m unittest {module} -v'
    atomic_write(path, f'Time: {now()}\nCommand: {command}\nExit: {result.returncode}\n\n'
                 + result.stdout + result.stderr)
    return result.returncode, path, result.stdout + result.stderr

def new():
    if BRIEF.exists():
        raise ValueError('Brief already exists. Use a fresh lab copy to start again.')
    meta = {'id': 'BRIEF-001', 'status': 'drafting', 'revision': 1, 'created': now()}
    sections = {title: 'Not yet recorded.' for title in SECTIONS}
    sections['Context and decision'] = (
        'D001: max_attempts includes the first request. Budget 3 means 3 total attempts.\n'
        'Reason: bounded downstream load. Rejected: 3 retries after the initial request.\n'
        'Reopen if the owner changes the budget or requirement. The lab pre-agrees this decision.')
    sections['Brief'] = (
        'Objective: implement the bounded retry policy in docs/CONTRACT.md.\n'
        'Owned product path: src/retry_policy.py.\n'
        'Out of scope: network I/O, delays, write-method retries, dependencies, test or tool edits.\n'
        'Executor: run basic and acceptance checks; report actual results.\n'
        'Reviewer: inspect the diff and contract; independently run tests.test_acceptance.\n'
        'Boundary: attempt == max_attempts must return False.\n'
        'Understanding: explain total attempts versus additional retries.\n'
        'Kill criterion: stop if the fix needs any file outside the owned path.\n'
        'Attempt budget: 2 unsuccessful delivery attempts, then the brief pauses for the owner.')
    save_brief(meta, sections)
    print('BRIEF-001 — drafting')

def issue():
    meta, sections = read_brief()
    if meta['status'] not in {'drafting', 'rejected'}:
        raise ValueError('Only drafting or rejected briefs may be issued.')
    if active_briefs():
        raise ValueError('WIP limit: resolve the issued or returned brief first.')
    if meta['status'] == 'rejected':
        old = f"### Revision {meta['revision']}\n\n"
        old += 'Executor summary:\n' + sections['Executor summary'] + '\n\nAcceptance:\n' + sections['Acceptance']
        old += '\n\nPrior round metadata:\n```json\n' + json.dumps(meta, indent=2, sort_keys=True) + '\n```'
        prior = '' if sections['History'] == 'Not yet recorded.' else sections['History'] + '\n\n'
        sections['History'] = prior + old
        meta['revision'] += 1
    sections['Executor summary'] = 'Awaiting executor.'
    sections['Acceptance'] = 'Awaiting reviewer.'
    for field in ['returned_snapshot', 'record_digest', 'executor_verdict', 'reviewed_snapshot']:
        meta.pop(field, None)
    meta.update(status='issued', issued=now())
    save_brief(meta, sections)
    print(f"BRIEF-001 — issued — revision {meta['revision']}")

def handback(path):
    meta, sections = read_brief()
    if meta['status'] != 'issued' or len(active_briefs()) != 1:
        raise ValueError('Return requires exactly one active, issued brief.')
    summary = path.read_text(encoding='utf-8').strip()
    lines = summary.splitlines()
    if not lines or lines[0].strip() not in {'done', 'partial', 'blocked', 'returned-deviation'}:
        raise ValueError('First summary line must be done, partial, blocked or returned-deviation.')
    if len(lines) > 30:
        raise ValueError('Executor summary exceeds 30 lines. Link to evidence instead.')
    if sum(line.startswith('Question:') for line in lines) > 1:
        raise ValueError('At most one Question: line is permitted.')
    sections['Executor summary'] = summary
    meta.update(status='returned', returned=now(), returned_snapshot=snapshot(),
                record_digest=record_digest(sections), executor_verdict=lines[0].strip())
    save_brief(meta, sections)
    print(f'BRIEF-001 — returned\nSummary written to {BRIEF.relative_to(ROOT)}\nReview required.')

def review(verdict, notes_path):
    meta, sections = read_brief()
    if meta['status'] != 'returned' or len(active_briefs()) != 1:
        raise ValueError('Review requires exactly one active, returned brief.')
    if record_digest(sections) != meta['record_digest']:
        raise ValueError('Brief or handback changed after return. Restore or investigate before review.')
    if snapshot() != meta['returned_snapshot']:
        raise ValueError('Source, tests, tools or contract changed after return. Stop and investigate.')
    notes = notes_path.read_text(encoding='utf-8').strip()
    for prefix in ['Scope:', 'Intent:', 'Risk:', 'Understanding:']:
        if not any(line.startswith(prefix) and line[len(prefix):].strip() for line in notes.splitlines()):
            raise ValueError(f'Review notes need a nonempty {prefix} line.')
    code, evidence, output = check('acceptance')
    print(output, end='')
    if snapshot() != meta['returned_snapshot']:
        raise ValueError('Files changed during review. Acceptance refused.')
    if verdict == 'accepted' and (code != 0 or meta['executor_verdict'] != 'done'):
        print(f'Acceptance refused. Evidence: {evidence.relative_to(ROOT)}')
        return 1
    meta.update(status=verdict, reviewed=now(), reviewed_snapshot=snapshot())
    sections['Acceptance'] = (
        f"{verdict}\nRevision: {meta['revision']}\nReviewer check exit: {code}\n"
        f'Evidence: {evidence.relative_to(ROOT)}\n{notes}\n'
        'Snapshot hashes recorded in metadata. These are local consistency checks, not signatures.')
    save_brief(meta, sections)
    print(f"BRIEF-001 — {verdict}\nEvidence: {evidence.relative_to(ROOT)}")
    return 0

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ['new', 'issue', 'status', 'diff']: sub.add_parser(name)
    p = sub.add_parser('return'); p.add_argument('--summary', type=Path, required=True)
    p = sub.add_parser('check'); p.add_argument('--suite', choices=['basic', 'acceptance'], default='acceptance')
    p = sub.add_parser('review'); p.add_argument('--verdict', choices=['accepted', 'rejected'], required=True)
    p.add_argument('--notes', type=Path, required=True)
    args = parser.parse_args()
    try:
        with locked():
            if args.command == 'new': new()
            elif args.command == 'issue': issue()
            elif args.command == 'return': handback(args.summary.resolve())
            elif args.command == 'review': return review(args.verdict, args.notes.resolve())
            elif args.command == 'status':
                rebuild_index()
                print((STATE / 'INDEX.md').read_text(encoding='utf-8'), end='')
            elif args.command == 'diff':
                original=(ROOT / 'fixtures/flawed.py.txt').read_text().splitlines(keepends=True)
                current=(ROOT / 'src/retry_policy.py').read_text().splitlines(keepends=True)
                print(''.join(difflib.unified_diff(original, current, fromfile='starter/retry_policy.py',
                                                 tofile='src/retry_policy.py')), end='')
            else:
                code, path, output = check(args.suite)
                print(output, end=''); print(f'Evidence: {path.relative_to(ROOT)}')
                return code
    except (ValueError, FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired) as error:
        print(f'Blocked: {error}', file=sys.stderr)
        return 2
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
