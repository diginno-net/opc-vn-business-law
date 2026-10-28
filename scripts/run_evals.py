#!/usr/bin/env python3
"""Run deterministic calculator checks; validate externally supplied semantic grades.

This program does not call a model, generate responses, or decide legal truth.
Only a human/LLM reviewer can supply semantic verdicts and supporting evidence.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"thieu_du_kien", "khong_du_dieu_kien", "can_kiem_tra_mien_thue",
            "can_chuyen_chuyen_gia", "du_dieu_kien_so_bo"}
NUMERIC_FIELDS = {"doanh_thu", "loi_nhuan", "ty_le_doanh_thu", "thue_suat",
                  "thue_theo_doanh_thu", "thue_theo_loi_nhuan", "bien_loi_nhuan",
                  "bien_hoa_von", "chenh_lech"}
TEXT_FIELDS = {"khuyen_nghi", "gia_dinh", "disclaimer"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def nonblank(value):
    return isinstance(value, str) and bool(value.strip())


def finite_number(value):
    if type(value) not in (int, float):
        return False
    try:
        return math.isfinite(value)
    except OverflowError:
        return False


def parse_json(text):
    """Reject ambiguous duplicate keys and non-JSON NaN/Infinity, including overflow."""
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, f"Duplicate JSON key: {key}")
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError(f"Non-finite JSON number: {value}")

    def check(value):
        if isinstance(value, float):
            require(math.isfinite(value), "Non-finite JSON number")
        elif isinstance(value, dict):
            for child in value.values():
                check(child)
        elif isinstance(value, list):
            for child in value:
                check(child)

    result = json.loads(text, object_pairs_hook=pairs, parse_constant=reject_constant)
    check(result)
    return result


def load_json(path):
    return parse_json(Path(path).read_text(encoding="utf-8"))


def exact_keys(value, keys, location):
    require(isinstance(value, dict), f"{location} must be an object")
    require(set(value) == set(keys), f"{location} requires exactly {sorted(keys)}")


def assertion_catalog(catalog):
    require(isinstance(catalog, dict), "Eval catalog must be an object")
    evals = catalog.get("evals")
    require(isinstance(evals, list) and bool(evals), "Eval catalog must contain evals")
    result = {}
    for evaluation in evals:
        require(isinstance(evaluation, dict), "Eval must be an object")
        eval_id = evaluation.get("id")
        require(type(eval_id) is int and eval_id > 0, "Eval id must be a positive integer")
        require(eval_id not in result, f"Duplicate eval id: {eval_id}")
        assertions = evaluation.get("assertions")
        require(isinstance(assertions, list) and bool(assertions), f"Eval {eval_id} has no assertions")
        ids = set()
        for assertion in assertions:
            require(isinstance(assertion, dict), "Assertion must be an object")
            assertion_id = assertion.get("id")
            require(nonblank(assertion_id), "Assertion id must be a nonempty string")
            require(assertion_id not in ids, f"Duplicate assertion: {eval_id}/{assertion_id}")
            require(nonblank(assertion.get("rubric")), f"Missing rubric: {eval_id}/{assertion_id}")
            ids.add(assertion_id)
        result[eval_id] = ids
    return result


def validate_grades(grades, catalog):
    """Check completeness/shape only, never infer a verdict from response text."""
    expected = assertion_catalog(catalog)
    exact_keys(grades, {"schema_version", "grader", "responses"}, "Grades")
    require(type(grades["schema_version"]) is int and grades["schema_version"] == 1,
            "Grades schema_version must be 1")
    exact_keys(grades["grader"], {"kind", "name"}, "Grader")
    require(grades["grader"]["kind"] in ("human", "llm"), "Grader kind must be human or llm")
    require(nonblank(grades["grader"]["name"]), "Grader name must be nonempty")
    require(isinstance(grades["responses"], list), "responses must be an array")
    seen = set()
    passed = failed = 0
    per_eval = []
    for response in grades["responses"]:
        exact_keys(response, {"eval_id", "response", "assertions"}, "Response")
        eval_id = response["eval_id"]
        require(type(eval_id) is int and eval_id in expected, f"Unknown eval id: {eval_id}")
        require(eval_id not in seen, f"Duplicate eval id: {eval_id}")
        require(nonblank(response["response"]), f"Eval {eval_id} needs the actual response text")
        require(isinstance(response["assertions"], list), "assertions must be an array")
        seen.add(eval_id)
        seen_assertions = set()
        eval_passed = eval_failed = 0
        for judgment in response["assertions"]:
            exact_keys(judgment, {"assertion_id", "passed", "evidence"}, "Judgment")
            assertion_id = judgment["assertion_id"]
            require(isinstance(assertion_id, str) and assertion_id in expected[eval_id],
                    f"Unknown assertion: {eval_id}/{assertion_id}")
            require(assertion_id not in seen_assertions,
                    f"Duplicate assertion: {eval_id}/{assertion_id}")
            require(type(judgment["passed"]) is bool,
                    f"Verdict must be boolean, not skipped: {eval_id}/{assertion_id}")
            require(nonblank(judgment["evidence"]), f"Evidence required: {eval_id}/{assertion_id}")
            seen_assertions.add(assertion_id)
            if judgment["passed"]:
                eval_passed += 1
            else:
                eval_failed += 1
        require(seen_assertions == expected[eval_id],
                f"Missing assertions for eval {eval_id}: {sorted(expected[eval_id] - seen_assertions)}")
        passed += eval_passed
        failed += eval_failed
        per_eval.append({"eval_id": eval_id, "passed": eval_passed, "failed": eval_failed})
    require(seen == set(expected), f"Missing evals: {sorted(set(expected) - seen)}")
    return {"status": "supplied_grades_validated", "grader": grades["grader"],
            "evals": len(seen), "assertions": passed + failed, "passed": passed,
            "failed": failed, "per_eval": per_eval,
            "note": "Externally supplied judgments only; evidence/legal correctness not verified by runner."}


def validate_comparison(data, simulation=False):
    require(isinstance(data, dict), "Comparison must be a JSON object")
    for field in NUMERIC_FIELDS:
        require(field in data and finite_number(data[field]), f"{field} must be finite numeric")
    for field in TEXT_FIELDS:
        require(nonblank(data.get(field)), f"{field} must be nonempty text")
    if simulation:
        require(data.get("che_do") == "mo-phong", "Simulation must identify che_do=mo-phong")


def validate_assessment(data):
    require(isinstance(data, dict), "Assessment must be a JSON object")
    require(isinstance(data.get("trang_thai"), str) and data["trang_thai"] in STATUSES,
            "Unknown/missing assessment status")
    for field in ("thue_suat", "ty_le_doanh_thu"):
        require(field in data and (data[field] is None or finite_number(data[field])),
                f"{field} must be finite numeric or null")
    for field in ("canh_bao", "du_kien_thieu"):
        require(isinstance(data.get(field), list) and all(nonblank(v) for v in data[field]),
                f"{field} must be an array of nonempty strings")
    require("so_sanh" in data, "Missing so_sanh")
    if data["so_sanh"] is not None:
        require(data["trang_thai"] == "du_dieu_kien_so_bo", "Gated assessment cannot compare")
        validate_comparison(data["so_sanh"])
    if data["trang_thai"] == "thieu_du_kien":
        require(bool(data["du_kien_thieu"]), "Missing-context status needs du_kien_thieu")


def at_path(data, path):
    for key in path.split("."):
        require(isinstance(data, dict) and key in data, f"Missing expected field: {path}")
        data = data[key]
    return data


def matches(actual, expected):
    if finite_number(expected):
        return finite_number(actual) and math.isclose(actual, expected, rel_tol=1e-10, abs_tol=1e-7)
    return type(actual) is type(expected) and actual == expected


def run_calculator_case(case, calculator):
    result = {"id": case["id"], "passed": False}
    try:
        command = [sys.executable, "-B", str(calculator), *case["args"], "--json"]
        completed = subprocess.run(command, capture_output=True, text=True, timeout=10, check=False)
        require(completed.returncode == case["exit_code"],
                f"Expected exit {case['exit_code']}, got {completed.returncode}: {completed.stderr.strip()}")
        if case["kind"] == "error":
            require(not completed.stdout.strip(), "Invalid input must not produce a success payload")
            require(nonblank(completed.stderr), "Invalid input needs a stderr diagnostic")
        else:
            data = parse_json(completed.stdout)
            if case["kind"] == "simulation":
                validate_comparison(data, simulation=True)
            else:
                validate_assessment(data)
            for path, expected in case["expected"].items():
                actual = at_path(data, path)
                require(matches(actual, expected), f"{path}: expected {expected!r}, got {actual!r}")
            for path in case.get("nonempty", []):
                value = at_path(data, path)
                require(isinstance(value, (list, str)) and bool(value), f"{path} must not be empty")
        result["passed"] = True
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        result["error"] = str(exc)
    return result


def run_calculator_suite(suite, calculator):
    require(isinstance(suite, dict) and type(suite.get("schema_version")) is int
            and suite["schema_version"] == 1, "Calculator suite schema_version must be 1")
    cases = suite.get("cases")
    require(isinstance(cases, list) and bool(cases), "Calculator suite must contain cases")
    seen = set()
    for case in cases:
        require(isinstance(case, dict), "Case must be an object")
        case_id = case.get("id")
        require(nonblank(case_id) and case_id not in seen, "Missing/duplicate calculator case id")
        seen.add(case_id)
        require(case.get("kind") in ("simulation", "assessment", "error"), "Invalid case kind")
        require(isinstance(case.get("args"), list) and all(isinstance(a, str) for a in case["args"]),
                "Case args must be strings")
        require(type(case.get("exit_code")) is int and
                case["exit_code"] == (2 if case["kind"] == "error" else 0), "Invalid expected exit")
        require(isinstance(case.get("expected"), dict), "Case needs expected object")
        require(case["kind"] == "error" or bool(case["expected"]), "Success case needs expectations")
        require(isinstance(case.get("nonempty", []), list) and
                all(nonblank(p) for p in case.get("nonempty", [])), "Invalid nonempty paths")
    return [run_calculator_case(case, calculator) for case in cases]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grades", type=Path, help="Complete human/LLM semantic judgments; never generated here")
    args = parser.parse_args(argv)
    try:
        suite = load_json(ROOT / "evals/calculator_cases.json")
        results = run_calculator_suite(suite, ROOT / "scripts/so_sanh_thue.py")
        grading = {"status": "not_run", "note": "No grades supplied; calculator checks only, not an LLM benchmark."}
        if args.grades is not None:
            grading = validate_grades(load_json(args.grades), load_json(ROOT / "evals/evals.json"))
        passed = sum(result["passed"] for result in results)
        report = {"calculator": {"total": len(results), "passed": passed,
                                 "failed": len(results) - passed, "cases": results},
                  "skill_grading": grading}
        print(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False))
        return 1 if passed != len(results) or grading.get("failed", 0) else 0
    except (ValueError, OSError) as exc:
        print(f"Invalid eval input: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
