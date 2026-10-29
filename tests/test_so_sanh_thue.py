"""Regression tests for arithmetic, legal gates and CLI safety (stdlib only)."""
import importlib.util
import json
import math
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'scripts' / 'so_sanh_thue.py'
spec = importlib.util.spec_from_file_location('so_sanh_thue', SCRIPT)
tax = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = tax
spec.loader.exec_module(tax)


class ArithmeticTests(unittest.TestCase):
    def test_17_percent_example_is_simulation_before_incentives(self):
        result = tax.tinh(8e9, 1.2e9, .015, .17)
        self.assertAlmostEqual(result.thue_theo_loi_nhuan, 204e6)
        self.assertAlmostEqual(result.bien_hoa_von, .015 / .17)
        self.assertEqual(result.che_do, 'mo-phong')
        self.assertIn('GTGT', result.gia_dinh)
        self.assertNotIn('mất khấu trừ', result.khuyen_nghi)

    def test_above_breakeven_profit_tax_is_higher(self):
        result = tax.tinh(2e9, 300e6, .015, .15)
        self.assertGreater(result.chenh_lech, 0)
        self.assertIn('lớn hơn', result.khuyen_nghi)

    def test_below_breakeven_profit_tax_is_lower(self):
        self.assertLess(tax.tinh(2e9, 100e6, .015, .15).chenh_lech, 0)

    def test_equal_breakeven(self):
        self.assertAlmostEqual(tax.tinh(2e9, 200e6, .015, .15).chenh_lech, 0)

    def test_income_above_revenue_can_include_adjustments(self):
        self.assertEqual(tax.tinh(100, 200, .015, .17).thue_theo_loi_nhuan, 34)

    def test_one_percent_is_explicit_decimal(self):
        self.assertEqual(tax.chuan_hoa_ty_le(.01), .01)
        for value in [1, 1.5, 15, 0, -1]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                tax.chuan_hoa_ty_le(value)

    def test_non_finite_values_rejected_in_every_position(self):
        for value in [math.nan, math.inf, -math.inf]:
            for index in range(4):
                values = [2e9, 300e6, .015, .15]
                values[index] = value
                with self.subTest(value=value, index=index), self.assertRaises(ValueError):
                    tax.tinh(*values)

    def test_overflow_rejected(self):
        with self.assertRaises(ValueError):
            tax.tinh(1e308, 1e308, .9, 1e-320)

    def test_invalid_revenue_and_negative_income(self):
        for revenue, income in [(0, 0), (-1, 1), (100, -1)]:
            with self.subTest(revenue=revenue, income=income), self.assertRaises(ValueError):
                tax.tinh(revenue, income, .015, .15)

    def test_statutory_rate_boundaries_are_not_payable_tax(self):
        for revenue, expected in [(1e9, .15), (3e9, .15), (3e9 + 1, .17),
                                  (50e9, .17), (50e9 + 1, .20)]:
            with self.subTest(revenue=revenue):
                self.assertEqual(tax.thue_suat_theo_doanh_thu(revenue), expected)


class CliTests(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args],
                              text=True, capture_output=True, timeout=10)

    def assessment(self, *extra):
        proc = self.run_cli('--doanh-thu', '2e9', '--doanh-thu-can-cu', '2e9',
                            '--nganh', 'dich-vu', '--xac-dinh-chi-phi', 'khong',
                            '--ngoai-le', 'khong', *extra, '--json')
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return json.loads(proc.stdout)

    def test_default_does_not_silently_assume_rates(self):
        proc = self.run_cli('--doanh-thu', '8e9', '--loi-nhuan', '1.2e9', '--json')
        self.assertEqual(proc.returncode, 0, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertEqual(result['trang_thai'], 'thieu_du_kien')
        self.assertIsNone(result['so_sanh'])
        self.assertIsNone(result['thue_suat'])

    def test_8_billion_basis_not_eligible_for_percent_method(self):
        result = self.assessment('--doanh-thu-can-cu', '8e9')
        self.assertEqual(result['trang_thai'], 'khong_du_dieu_kien')
        self.assertIsNone(result['so_sanh'])
        self.assertEqual(result['thue_suat'], .17)

    def test_current_revenue_is_not_rate_basis(self):
        result = self.assessment('--doanh-thu', '8e9', '--doanh-thu-can-cu', '60e9')
        self.assertEqual(result['thue_suat'], .20)
        self.assertIsNone(result['so_sanh'])

    def test_exemption_boundary_and_plus_one(self):
        result = self.assessment('--doanh-thu-can-cu', '1e9')
        self.assertEqual(result['trang_thai'], 'can_kiem_tra_mien_thue')
        self.assertIsNone(result['so_sanh'])
        result = self.assessment('--doanh-thu-can-cu', '1000000001')
        self.assertEqual(result['trang_thai'], 'du_dieu_kien_so_bo')

    def test_exemption_review_precedes_method_gate_without_comparison(self):
        result = self.assessment('--doanh-thu-can-cu', '0', '--xac-dinh-chi-phi', 'co')
        self.assertEqual(result['trang_thai'], 'can_kiem_tra_mien_thue')
        self.assertIsNone(result['so_sanh'])

    def test_simulation_warns_about_conditional_reduction(self):
        result = tax.tinh(8e9, 1.2e9, .015, .17)
        self.assertIn('43/2026', result.gia_dinh)
        self.assertIn('chưa áp giảm', result.gia_dinh)

    def test_known_costs_not_eligible(self):
        result = self.assessment('--xac-dinh-chi-phi', 'co', '--loi-nhuan', '3e8')
        self.assertEqual(result['trang_thai'], 'khong_du_dieu_kien')
        self.assertIsNone(result['so_sanh'])

    def test_special_cases_fail_closed_without_assigning_rate(self):
        result = self.assessment('--ngoai-le', 'co', '--loi-nhuan', '3e8')
        self.assertEqual(result['trang_thai'], 'can_chuyen_chuyen_gia')
        self.assertIsNone(result['thue_suat'])
        self.assertIsNone(result['so_sanh'])

    def test_eligible_comparison_is_only_hypothetical_before_incentives(self):
        result = self.assessment('--thu-nhap-tinh-thue', '3e8')
        self.assertEqual(result['trang_thai'], 'du_dieu_kien_so_bo')
        self.assertEqual(result['so_sanh']['thue_theo_loi_nhuan'], 45e6)
        self.assertEqual(result['so_sanh']['thue_theo_doanh_thu'], 30e6)
        self.assertTrue(any('43/2026' in text for text in result['canh_bao']))
        self.assertTrue(any('GTGT' in text for text in result['canh_bao']))

    def test_each_sector_has_own_rate(self):
        for sector, expected in [('hang-hoa', .003), ('san-xuat', .012),
                                 ('dich-vu', .015), ('cho-thue-dai-ly', .04),
                                 ('noi-dung-so', .04), ('khac', .005)]:
            with self.subTest(sector=sector):
                self.assertEqual(self.assessment('--nganh', sector)['ty_le_doanh_thu'], expected)

    def test_simulation_requires_rates(self):
        proc = self.run_cli('--che-do', 'mo-phong', '--doanh-thu', '8e9',
                            '--loi-nhuan', '1.2e9', '--json')
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, '')

    def test_simulation_output_and_rate_format(self):
        args = ['--che-do', 'mo-phong', '--doanh-thu', '8e9', '--loi-nhuan', '1.2e9',
                '--ty-le', '.015', '--thue-suat', '.17', '--json']
        proc = self.run_cli(*args)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)['thue_theo_loi_nhuan'], 204e6)
        proc = self.run_cli(*args, '--ty-le', '1.5')
        self.assertEqual(proc.returncode, 2)

    def test_assessment_cannot_override_rates_or_silently_ignore_context(self):
        proc = self.run_cli('--doanh-thu', '8e9', '--thue-suat', '.17', '--json')
        self.assertEqual(proc.returncode, 2)
        proc = self.run_cli('--che-do', 'mo-phong', '--doanh-thu', '8e9',
                            '--loi-nhuan', '1.2e9', '--ty-le', '.015', '--thue-suat', '.17',
                            '--doanh-thu-can-cu', '2e9', '--json')
        self.assertEqual(proc.returncode, 2)

    def test_non_finite_input_never_emits_json_nan(self):
        for option in ['--doanh-thu', '--doanh-thu-can-cu', '--loi-nhuan']:
            for value in ['nan', 'inf', '-inf']:
                with self.subTest(option=option, value=value):
                    proc = self.run_cli('--doanh-thu', '2e9', f'{option}={value}', '--json')
                    self.assertEqual(proc.returncode, 2)
                    self.assertEqual(proc.stdout, '')

    def test_self_test(self):
        proc = self.run_cli('--self-test')
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn('Self-test OK', proc.stdout)


if __name__ == '__main__':
    unittest.main()
