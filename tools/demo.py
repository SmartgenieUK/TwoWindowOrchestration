#!/usr/bin/env python3
"""Deterministic teaching replay. Every step is scripted; no AI is called."""
import argparse
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

SOURCE = Path(__file__).resolve().parents[1]

def invoke(root, *args, expected=0):
    # Pin the pipe encoding: otherwise Windows decodes the child's output with the locale codepage.
    result = subprocess.run([sys.executable, 'tools/workflow.py', *args], cwd=root,
                            capture_output=True, encoding='utf-8',
                            env={**os.environ, 'PYTHONIOENCODING': 'utf-8'})
    print(result.stdout + result.stderr, end='')
    if result.returncode != expected:
        raise RuntimeError(f'{args}: expected exit {expected}, got {result.returncode}')

def copy_lab(dest):
    dest = dest.resolve()
    if dest.exists():
        raise ValueError('Destination exists. Choose a new empty path; the demo never resets a working copy.')
    # Copy only explicit lab content, never another generated rehearsal directory.
    # Prepared briefs stay out so a live executor cannot read the expected answer.
    dest.mkdir(parents=True)
    for name in ['src', 'tests', 'tools', 'fixtures', 'docs', '.claude']:
        shutil.copytree(SOURCE / name, dest / name, ignore=shutil.ignore_patterns(
            '__pycache__', '*.pyc', '.lock', 'evidence', 'BRIEF-*.md', 'briefs', 'logs'))
    for name in ['AGENTS.md', 'CLAUDE.md', 'README.md']:
        shutil.copy2(SOURCE / name, dest / name)
    (dest / '.smartretry-rehearsal').write_text('Created by tools/demo.py\n')
    shutil.copy2(dest / 'fixtures/flawed.py.txt', dest / 'src/retry_policy.py')
    return dest

def deviation(dest):
    dest = copy_lab(dest)
    print('SCRIPTED SETUP: an authored brief with deliberate gaps, issued for a live executor.\n')
    invoke(dest, 'new')
    prepared = (SOURCE / 'fixtures/briefs/DEVIATION_BRIEF.md').read_text(encoding='utf-8')
    context = prepared.split('## 1 Context and decision\n', 1)[1].split('## 2 Brief\n', 1)
    brief = dest / 'docs/co-arch/BRIEF-001-retry-budget.md'
    text = brief.read_text(encoding='utf-8')
    for number, body in [(1, context[0]), (2, context[1])]:
        text = re.sub(rf'(<!-- section:{number} -->\n).*?(\n<!-- /section:{number} -->)',
                      lambda m: m.group(1) + body.strip() + m.group(2), text, flags=re.S)
    brief.write_text(text, encoding='utf-8', newline='\n')
    invoke(dest, 'issue')
    print(f'\nPrepared: {dest}\nNext: start the executor in that folder; it should return returned-deviation.\n'
          f'Fallback: python tools/workflow.py return --summary {SOURCE / "fixtures/briefs/DEVIATION_HANDBACK.txt"}')

def start(dest):
    dest = copy_lab(dest)
    print('SCRIPTED REPLAY: a seeded defect and deliberately incomplete historical handback.\n')
    invoke(dest, 'new'); invoke(dest, 'issue')
    invoke(dest, 'check', '--suite', 'basic')
    (dest / 'docs/co-arch/executor-summary.txt').write_text(
        'done\nChanged: src/retry_policy.py\nChecks: tests.test_basic, 6 passed.\n'
        'Not run: full acceptance suite. This is the intentional teaching trap.\n'
        'Evidence: docs/co-arch/evidence/\nQuestion: none\n')
    invoke(dest, 'return', '--summary', 'docs/co-arch/executor-summary.txt')
    print(f'\nPrepared: {dest}\nNext: reviewer checks the contract and boundary, then rejects.')

def reject(root):
    check_root(root)
    (root / 'docs/co-arch/review-notes.txt').write_text(
        'Scope: inspected src/retry_policy.py.\n'
        'Intent: final permitted attempt incorrectly schedules another attempt.\n'
        'Risk: retry budget is exceeded.\n'
        'Understanding: a budget of 3 permits only 2 additional retries.\n')
    invoke(root, 'review', '--verdict', 'rejected', '--notes', 'docs/co-arch/review-notes.txt')

def repair(root):
    check_root(root)
    invoke(root, 'issue')
    shutil.copy2(root / 'fixtures/fixed.py.txt', root / 'src/retry_policy.py')
    invoke(root, 'check', '--suite', 'acceptance')
    (root / 'docs/co-arch/executor-summary.txt').write_text(
        'done\nChanged: src/retry_policy.py, <= changed to <.\n'
        'Checks: tests.test_acceptance, 18 passed.\n'
        'Evidence: docs/co-arch/evidence/\nLimit: policy function only; no HTTP calls.\nQuestion: none\n')
    invoke(root, 'return', '--summary', 'docs/co-arch/executor-summary.txt')
    (root / 'docs/co-arch/review-notes.txt').write_text(
        'Scope: compared corrected fixture; product change is confined to retry policy.\n'
        'Intent: contract permits another attempt only below the total-attempt limit.\n'
        'Risk: this is a teaching policy, without production retry scheduling.\n'
        'Understanding: attempt 3 of 3 returns False; a fourth attempt is forbidden.\n')
    invoke(root, 'review', '--verdict', 'accepted', '--notes', 'docs/co-arch/review-notes.txt')
    print('\nOWNER RECEIPT\ndone\nBudget 3 now stops after attempt 3.\n'
          'Reviewer reran 18 acceptance tests and inspected the boundary.\n'
          'Evidence: docs/co-arch/BRIEF-001-retry-budget.md\n'
          'Limit: teaching policy only.\nNo decision needed.\n')

def check_root(root):
    if not (root / '.smartretry-rehearsal').is_file():
        raise ValueError('Use a rehearsal directory created by demo.py start.')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    for name in ['start', 'deviation']:
        s = sub.add_parser(name); s.add_argument('--dest', type=Path, required=True)
    for name in ['reject', 'repair']:
        s = sub.add_parser(name); s.add_argument('--root', type=Path, required=True)
    sub.add_parser('run')
    args = p.parse_args()
    try:
        if args.command == 'start': start(args.dest)
        elif args.command == 'deviation': deviation(args.dest)
        elif args.command == 'reject': reject(args.root.resolve())
        elif args.command == 'repair': repair(args.root.resolve())
        else:
            with tempfile.TemporaryDirectory(prefix='smartretry-demo-') as temp:
                root = Path(temp) / 'rehearsal'
                start(root); reject(root); repair(root)
            print('Replay complete. Temporary copy removed; original lab unchanged.')
    except (ValueError, RuntimeError) as error:
        print(error, file=sys.stderr); return 1
    return 0

if __name__ == '__main__': raise SystemExit(main())
