"""Package only public allowlisted sources, never move the live checkout."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def test_archives_include_runtime_and_zip_eval_dependencies_only(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/build_packages.py'),
                                     '--output', directory], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((ROOT / '.git').exists())
            with zipfile.ZipFile(Path(directory) / 'opc-vn-business-law.skill') as archive:
                names = archive.namelist()
                self.assertIn('opc-vn-business-law/SKILL.md', names)
                self.assertIn('opc-vn-business-law/scripts/so_sanh_thue.py', names)
                self.assertFalse(any('/evals/' in name or '/tests/' in name for name in names))
                self.assertNotIn('opc-vn-business-law/scripts/run_evals.py', names)
            with zipfile.ZipFile(Path(directory) / 'opc-vn-business-law-v1.1.0.zip') as archive:
                names += archive.namelist()
                self.assertIn('evals/calculator_cases.json', archive.namelist())
                self.assertIn('tests/test_so_sanh_thue.py', archive.namelist())
                self.assertIn('scripts/run_evals.py', archive.namelist())
            for name in names:
                self.assertFalse(any(part in {'.git', 'dist', 'launch', '__pycache__'}
                                     for part in Path(name).parts), name)
                self.assertNotIn('.audit-internal-terms', name)


if __name__ == '__main__':
    unittest.main()
