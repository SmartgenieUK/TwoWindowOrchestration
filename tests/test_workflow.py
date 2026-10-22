"""Meaningful lifecycle tests, each isolated in a temporary lab copy."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SOURCE = Path(__file__).resolve().parents[1]

class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='smartretry-test-')
        self.root = Path(self.tmp.name)
        for name in ['src', 'tests', 'tools', 'fixtures', 'docs']:
            shutil.copytree(SOURCE / name, self.root / name,
                ignore=shutil.ignore_patterns('__pycache__', '*.pyc', 'BRIEF-*.md', '.lock', 'evidence'))
        self.notes = self.root / 'notes.txt'
        self.notes.write_text('Scope: reviewed.\nIntent: checked.\nRisk: teaching only.\nUnderstanding: total attempts.\n')
        self.summary = self.root / 'summary.txt'
        self.summary.write_text('done\nActual checks recorded here for test fixture.\n')
        self.cli('new'); self.cli('issue')
    def tearDown(self): self.tmp.cleanup()
    def cli(self, *args, expected=0):
        result = subprocess.run([sys.executable, 'tools/workflow.py', *args], cwd=self.root,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return result
    def returned(self): self.cli('return', '--summary', str(self.summary))
    def fixed(self): shutil.copy2(self.root/'fixtures/fixed.py.txt', self.root/'src/retry_policy.py')
    def test_bad_code_cannot_be_accepted(self):
        self.returned(); self.cli('review', '--verdict', 'accepted', '--notes', str(self.notes), expected=1)
        self.assertIn('returned', self.cli('status').stdout)
    def test_corrected_code_can_be_accepted(self):
        self.fixed(); self.returned(); self.cli('review', '--verdict', 'accepted', '--notes', str(self.notes))
        self.assertIn('accepted', self.cli('status').stdout)
    def test_drift_after_return_is_blocked(self):
        self.returned(); self.fixed()
        self.cli('review', '--verdict', 'rejected', '--notes', str(self.notes), expected=2)
    def test_issued_cannot_be_issued_again(self): self.cli('issue', expected=2)
    def test_returned_blocks_reissue(self): self.returned(); self.cli('issue', expected=2)
    def test_rejection_preserves_history(self):
        self.returned(); self.cli('review', '--verdict', 'rejected', '--notes', str(self.notes))
        self.cli('issue')
        text = (self.root/'docs/co-arch/BRIEF-001-retry-budget.md').read_text()
        self.assertIn('### Revision 1', text); self.assertIn('Revision: 2', text)
    def test_summary_limit(self):
        self.summary.write_text('done\n' + 'line\n' * 30)
        self.cli('return', '--summary', str(self.summary), expected=2)
    def test_partial_cannot_be_accepted(self):
        self.fixed(); self.summary.write_text('partial\nWork remains.\n'); self.returned()
        self.cli('review', '--verdict', 'accepted', '--notes', str(self.notes), expected=1)
    def test_returned_deviation_is_returned_not_accepted(self):
        self.fixed(); self.summary.write_text('returned-deviation\nBrief contradicts contract.\n'); self.returned()
        self.assertIn('returned', self.cli('status').stdout)
        self.cli('review', '--verdict', 'accepted', '--notes', str(self.notes), expected=1)
    def test_lock_blocks_concurrent_transition(self):
        (self.root/'docs/co-arch/.lock').write_text('another process')
        self.cli('status', expected=2)
        self.assertTrue((self.root/'docs/co-arch/.lock').exists())
    def test_index_can_be_rebuilt(self):
        (self.root/'docs/co-arch/INDEX.md').write_text('stale')
        self.assertIn('issued', self.cli('status').stdout)
    def test_brief_tamper_is_blocked(self):
        self.returned(); p = self.root/'docs/co-arch/BRIEF-001-retry-budget.md'
        p.write_text(p.read_text().replace('bounded downstream load', 'unbounded downstream load'))
        self.cli('review', '--verdict', 'rejected', '--notes', str(self.notes), expected=2)
    def test_review_requires_semantic_notes(self):
        self.fixed(); self.returned(); self.notes.write_text('Looks good.\n')
        self.cli('review', '--verdict', 'accepted', '--notes', str(self.notes), expected=2)

if __name__ == '__main__': unittest.main()
