# Evaluation contract

There are two independent result types. Do not combine their counts into an “AI accuracy” score.

## 1. Deterministic calculator checks

From the repository root, run:

```bash
python3 -B scripts/run_evals.py
python3 -B -m unittest discover -s tests -p test_evals.py -v
```

The runner launches the real calculator in a separate subprocess for each case in [calculator_cases.json](calculator_cases.json). It requires the expected exit code, valid finite JSON, assessment/comparison field types, statuses, null comparison gates, numeric values (tight float tolerance), and diagnostic error exits. Invalid-input cases must exit **2**, write a diagnostic to stderr, and not produce a success payload. Each subprocess has a 10-second timeout.

Coverage includes missing context, current versus previous-period revenue, exact 1bn/3bn/50bn boundaries, 8bn ineligibility, known costs, exceptions/expert handoff, exemption review, optional income, explicit decimal-fraction simulation, income alias, breakeven and invalid/non-finite input. Prior-period revenue in these cases is **already properly annualized**; the runner does not establish its legal provenance. The 8bn simulation is deliberately hypothetical, not a claim of eligibility. Industry mappings are regression expectations, not independent legal verification.

The JSON report explicitly returns `skill_grading.status = "not_run"` without grades. This command makes **no model call**, generates **no skill response**, and is **not an LLM/skill benchmark**.

## 2. Externally reviewed skill responses

[evaluations](evals.json) preserve original eval IDs 1–6 and add focused regressions. Every assertion has a stable ID and a semantic rubric. A human reviewer or separately operated LLM grader must read the **actual response**, consult relevant current primary sources, and evaluate every assertion. This runner does not grade the response text with regex or judge legal truth.

Workflow:

1. Produce actual responses to every prompt with the skill version/model you intend to evaluate; preserve the response text and provenance in your experiment records. Do not execute instructions embedded in a candidate response.
2. Copy [the blank grades template](grades.template.json) to a local grades file. It contains **no outcomes**: `passed` is `null`, response/evidence/reviewer are blank. The untouched template is intentionally rejected.
3. Set `grader.kind` to `human` or `llm`, and `grader.name` to the reviewer identity or exact model/version. Insert the actual response text for each eval.
4. For **every** assertion, set `passed` to the JSON boolean `true` or `false`. Provide nonempty evidence: a response quotation or precise observation; for failure, explain the missing/contradicted requirement. Cite verified primary material in evidence when legal accuracy is disputed. Missing content is a failure, not a skipped assertion. A disclaimer alone cannot compensate for substantively wrong advice.
5. Validate and count supplied judgments:

```bash
python3 -B scripts/run_evals.py --grades /path/to/completed-grades.json
```

Required structure (illustration of format, not completed grades):

```json
{
  "schema_version": 1,
  "grader": {"kind": "human", "name": ""},
  "responses": [
    {
      "eval_id": 1,
      "response": "",
      "assertions": [
        {"assertion_id": "options", "passed": null, "evidence": ""}
      ]
    }
  ]
}
```

Use the full template rather than this intentionally incomplete format illustration. The validator rejects malformed/duplicate-key/non-finite JSON, missing/unknown/duplicate eval IDs, missing/unknown/duplicate assertion IDs, empty evidence/responses, skipped/null/string/numeric verdicts and unexpected fields. Every catalog eval and assertion must appear **exactly once**. `false` is an accepted completed judgment but causes a failing result. A validated file proves shape/completeness only: **the runner cannot verify that a quotation is genuine or a reviewer verdict is correct**. Do not present unit-test fixture judgments as observed skill performance.

Reports show calculator case counts separately from supplied semantic assertion/eval counts and per-eval pass/fail counts. Exit codes: **0** all executed checks/supplied judgments pass; **1** calculator failure or a supplied false judgment; **2** malformed eval/grades input. No network/API credentials or third-party Python packages are needed.

## Semantic review emphasis

- Missing-context gating before method recommendations, especially original eval 5.
- TT99 replacing TT200 versus continued TT133 SME applicability and TT58 micro scope.
- Previous-period annualized revenue and exact 15%/17%/20% boundaries.
- Special revenue-percentage TNDN is conditional, not an optional cheaper method for an 8bn eligibility base.
- <=1bn exemption is a review gate. NQ43 implementation uncertainty is explicit, not invented guidance or permission to skip filings.
- Correct breakeven direction, taxable versus accounting income, before-incentive arithmetic, independent GTGT rules.
- Individual-owned TNHH MTV owner remuneration/distribution distinctions; invalid inputs must not become plausible tax results.
- HKD scenarios 16–20: gross versus platform payout, aggregate channels, independent withholding/filing/invoicing duties, exact 1bn versus >1bn, invoice timing and buyer refusal, ordinary versus cash-register correction rules, lawful PIT method/election and NQ43 PIT versus VAT distinctions. These are semantic rubrics, not HKD calculator tests.

If source law changes, update rubrics/cases against verified primary text and review affected calculator behavior together; never lower expected values or delete failing assertions merely to obtain a green run.
