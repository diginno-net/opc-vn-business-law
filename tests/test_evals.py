"""Automatic tests for calculator eval execution and external semantic grades."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("run_evals", ROOT / "scripts/run_evals.py")
runner = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runner)


def clone_json(value):
    """Isolate mutable JSON-only fixtures between validation cases."""
    return json.loads(json.dumps(value))


def eval_fixture():
    return {"evals": [{"id": 1, "assertions": [
        {"id": "context", "rubric": "Ask for missing context."},
        {"id": "safety", "rubric": "Do not invent eligibility."},
    ]}]}


def grade_fixture():
    return {"schema_version": 1, "grader": {"kind": "human", "name": "Test reviewer"},
            "responses": [{"eval_id": 1, "response": "Please provide prior-year revenue.",
                           "assertions": [
                               {"assertion_id": "context", "passed": True,
                                "evidence": "Response asks for prior-year revenue."},
                               {"assertion_id": "safety", "passed": False,
                                "evidence": "Response omits an explicit eligibility warning."},
                           ]}]}


class GradeValidationTests(unittest.TestCase):
    def test_counts_real_supplied_boolean_judgments(self):
        result = runner.validate_grades(grade_fixture(), eval_fixture())
        self.assertEqual(result["evals"], 1)
        self.assertEqual(result["assertions"], 2)
        self.assertEqual(result["passed"], 1)
        self.assertEqual(result["failed"], 1)

    def test_rejects_malformed_missing_unknown_duplicate_and_skipped_judgments(self):
        mutations = {
            "wrong root": lambda g: [],
            "missing grader": lambda g: g.pop("grader"),
            "malformed grader": lambda g: g.update(grader=[]),
            "malformed responses": lambda g: g.update(responses={}),
            "malformed response item": lambda g: g.update(responses=[[]]),
            "malformed assertion list": lambda g: g["responses"][0].update(assertions={}),
            "malformed assertion item": lambda g: g["responses"][0].update(assertions=[None]),
            "unknown grader kind": lambda g: g["grader"].update(kind="regex"),
            "empty reviewer": lambda g: g["grader"].update(name=" "),
            "wrong version": lambda g: g.update(schema_version=True),
            "missing eval": lambda g: g.update(responses=[]),
            "unknown eval": lambda g: g["responses"][0].update(eval_id=999),
            "boolean eval id": lambda g: g["responses"][0].update(eval_id=True),
            "duplicate eval": lambda g: g["responses"].append(clone_json(g["responses"][0])),
            "missing assertions": lambda g: g["responses"][0].pop("assertions"),
            "missing assertion": lambda g: g["responses"][0]["assertions"].pop(),
            "unknown assertion": lambda g: g["responses"][0]["assertions"][0].update(assertion_id="bogus"),
            "duplicate assertion": lambda g: g["responses"][0]["assertions"].append(clone_json(g["responses"][0]["assertions"][0])),
            "skipped assertion": lambda g: g["responses"][0]["assertions"][0].update(passed="skipped"),
            "numeric verdict": lambda g: g["responses"][0]["assertions"][0].update(passed=1),
            "null verdict": lambda g: g["responses"][0]["assertions"][0].update(passed=None),
            "missing verdict": lambda g: g["responses"][0]["assertions"][0].pop("passed"),
            "missing evidence": lambda g: g["responses"][0]["assertions"][0].pop("evidence"),
            "empty evidence": lambda g: g["responses"][0]["assertions"][0].update(evidence=" \n"),
            "missing response": lambda g: g["responses"][0].pop("response"),
            "empty response": lambda g: g["responses"][0].update(response=""),
            "skip flag": lambda g: g["responses"][0]["assertions"][0].update(skipped=True),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                grades = grade_fixture()
                replacement = mutate(grades)
                if name == "wrong root":
                    grades = replacement
                with self.assertRaises(ValueError):
                    runner.validate_grades(grades, eval_fixture())

    def test_accepts_complete_llm_grades_without_generating_them(self):
        grades = grade_fixture()
        grades["grader"] = {"kind": "llm", "name": "external-model-version"}
        for judgment in grades["responses"][0]["assertions"]:
            judgment["passed"] = True
        result = runner.validate_grades(grades, eval_fixture())
        self.assertEqual(result["failed"], 0)
        self.assertEqual(result["passed"], 2)
        self.assertEqual(result["status"], "supplied_grades_validated")

    def test_rejects_invalid_eval_catalog_instead_of_silently_skipping(self):
        for catalog in [{"evals": []}, {"evals": [{"id": 1, "assertions": []}]},
                        {"evals": [eval_fixture()["evals"][0]] * 2}]:
            with self.subTest(catalog=catalog), self.assertRaises(ValueError):
                runner.validate_grades(grade_fixture(), catalog)

    def test_strict_json_rejects_duplicate_keys_nonfinite_and_malformed(self):
        for text in ['{"passed":true,"passed":false}', '{"x":NaN}',
                     '{"x":Infinity}', '{"x":1e999}', '{broken']:
            with self.subTest(text=text), self.assertRaises(ValueError):
                runner.parse_json(text)

    def test_template_contains_no_claimed_outcomes_and_is_not_accepted_as_grades(self):
        catalog = runner.load_json(ROOT / "evals/evals.json")
        template = runner.load_json(ROOT / "evals/grades.template.json")
        self.assertEqual({r["eval_id"] for r in template["responses"]},
                         {e["id"] for e in catalog["evals"]})
        for response in template["responses"]:
            self.assertEqual(response["response"], "")
            for assertion in response["assertions"]:
                self.assertIsNone(assertion["passed"])
                self.assertEqual(assertion["evidence"], "")
        with self.assertRaises(ValueError):
            runner.validate_grades(template, catalog)


class CalculatorRunnerTests(unittest.TestCase):
    def simulation(self):
        return {"che_do": "mo-phong", "doanh_thu": 8e9, "loi_nhuan": 1.2e9,
                "ty_le_doanh_thu": .015, "thue_suat": .17,
                "thue_theo_doanh_thu": 120e6, "thue_theo_loi_nhuan": 204e6,
                "bien_loi_nhuan": .15, "bien_hoa_von": .015 / .17,
                "chenh_lech": 84e6, "khuyen_nghi": "Illustration only",
                "gia_dinh": "Before incentives", "disclaimer": "Not tax advice"}

    def case(self):
        return {"id": "arithmetic", "args": ["--che-do", "mo-phong"],
                "exit_code": 0, "kind": "simulation",
                "expected": {"thue_theo_loi_nhuan": 204e6, "bien_hoa_von": .015 / .17}}

    def run_stub(self, case, stdout, returncode=0, stderr=""):
        with patch.object(runner.subprocess, "run", return_value=subprocess.CompletedProcess(
                [], returncode, stdout, stderr)):
            return runner.run_calculator_case(case, ROOT / "scripts/so_sanh_thue.py")

    def test_validates_json_values_with_float_tolerance(self):
        self.assertTrue(self.run_stub(self.case(), json.dumps(self.simulation()))["passed"])
        bad = self.simulation()
        bad["thue_theo_loi_nhuan"] = 240e6
        self.assertFalse(self.run_stub(self.case(), json.dumps(bad))["passed"])

    def test_rejects_wrong_exit_bad_json_nonfinite_bool_and_missing_fields(self):
        for output, code in [(json.dumps(self.simulation()), 2), ("not json", 0),
                             ('{"x":NaN}', 0), ("[]", 0), ("{}", 0)]:
            with self.subTest(output=output, code=code):
                self.assertFalse(self.run_stub(self.case(), output, code)["passed"])
        for field, value in [("thue_theo_loi_nhuan", True), ("bien_hoa_von", None),
                             ("thue_suat", float("inf"))]:
            bad = self.simulation()
            bad[field] = value
            self.assertFalse(self.run_stub(self.case(), json.dumps(bad))["passed"])

    def test_error_cases_require_exact_exit_diagnostic_and_no_success_json(self):
        case = {"id": "bad", "args": [], "exit_code": 2, "kind": "error", "expected": {}}
        self.assertTrue(self.run_stub(case, "", 2, "Invalid argument")["passed"])
        for stdout, code, stderr in [("", 0, ""), ("", 1, "error"),
                                     ("{}", 2, "error"), ("", 2, "")]:
            self.assertFalse(self.run_stub(case, stdout, code, stderr)["passed"])

    def test_assessment_validates_status_shape_and_missing_context_no_comparison(self):
        case = {"id": "gate", "args": [], "exit_code": 0, "kind": "assessment",
                "expected": {"trang_thai": "thieu_du_kien", "so_sanh": None},
                "nonempty": ["du_kien_thieu", "canh_bao"]}
        good = {"trang_thai": "thieu_du_kien", "thue_suat": None,
                "ty_le_doanh_thu": None, "so_sanh": None,
                "canh_bao": ["Need context"], "du_kien_thieu": ["nganh"]}
        self.assertTrue(self.run_stub(case, json.dumps(good))["passed"])
        for field, value in [("so_sanh", self.simulation()), ("du_kien_thieu", []),
                             ("canh_bao", "warning"), ("trang_thai", "eligible")]:
            bad = dict(good, **{field: value})
            self.assertFalse(self.run_stub(case, json.dumps(bad))["passed"])

    def test_reports_subprocess_timeout_as_failed_case(self):
        with patch.object(runner.subprocess, "run", side_effect=subprocess.TimeoutExpired([], 10)):
            self.assertFalse(runner.run_calculator_case(
                self.case(), ROOT / "scripts/so_sanh_thue.py")["passed"])

    def test_suite_rejects_missing_duplicate_and_vacuous_cases(self):
        for suite in [{"schema_version": 1, "cases": []},
                      {"schema_version": True, "cases": [self.case()]},
                      {"schema_version": 1, "cases": [self.case(), self.case()]},
                      {"schema_version": 1, "cases": [dict(self.case(), expected={})]},
                      {"schema_version": 1, "cases": [dict(self.case(), args="--json")]},
                      {"schema_version": 1, "cases": [dict(self.case(), exit_code=1)]}]:
            with self.subTest(suite=suite), self.assertRaises(ValueError):
                runner.run_calculator_suite(suite, ROOT / "scripts/so_sanh_thue.py")

    def test_deterministic_subprocess_suite_against_real_calculator(self):
        suite = runner.load_json(ROOT / "evals/calculator_cases.json")
        results = runner.run_calculator_suite(suite, ROOT / "scripts/so_sanh_thue.py")
        failures = [r for r in results if not r["passed"]]
        self.assertGreaterEqual(len(results), 25)
        self.assertEqual(failures, [], json.dumps(failures, ensure_ascii=False, indent=2))


class RunnerCliTests(unittest.TestCase):
    def test_no_grades_only_claims_calculator_checks(self):
        output = io.StringIO()
        with patch.object(runner, "run_calculator_suite", return_value=[{"id": "ok", "passed": True}]), \
                patch.object(runner, "load_json", return_value={}), contextlib.redirect_stdout(output):
            code = runner.main([])
        self.assertEqual(code, 0)
        report = json.loads(output.getvalue())
        self.assertEqual(report["calculator"]["passed"], 1)
        self.assertEqual(report["skill_grading"]["status"], "not_run")
        self.assertNotIn("passed", report["skill_grading"])

    def test_invalid_grades_exit_two_and_failed_judgments_exit_one(self):
        for grades, expected_code in [({}, 2), (grade_fixture(), 1)]:
            def load(path):
                if str(path).endswith("evals.json"):
                    return eval_fixture()
                if str(path).endswith("grades.json"):
                    return grades
                return {}
            with self.subTest(code=expected_code), \
                    patch.object(runner, "run_calculator_suite", return_value=[]), \
                    patch.object(runner, "load_json", side_effect=load), \
                    contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(runner.main(["--grades", "grades.json"]), expected_code)


if __name__ == "__main__":
    unittest.main()
