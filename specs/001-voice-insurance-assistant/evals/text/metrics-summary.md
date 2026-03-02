# Metrics Summary: Text Evaluation Runs

## Run Summary Template

- `run_id`: RUN-20260302-001
- `total_scenarios`: 4
- `passed_count`: 3
- `failed_count`: 0
- `blocked_count`: 1
- `scenario_pass_rate`: 0.7500
- `requirement_coverage_rate`: 1.0000
- `reviewer_agreement_rate`: 1.0000
- `unmapped_requirements`: none
- `notes`: TXT-003 intentionally blocked by skipped-reset precondition; formulas validated from ledger records.

## Metric Calculation Steps

1. `total_executed_scenarios = passed_count + failed_count + blocked_count`
2. `scenario_pass_rate = passed_count / total_executed_scenarios`
3. `requirement_coverage_rate = covered_requirements / total_in_scope_requirements`
4. `reviewer_agreement_rate = agreed_status_count / jointly_executed_non_blocked_count`
5. Round all rates to 4 decimal places after calculation.

## Reviewer Agreement Method

- Compare reviewer A and reviewer B status for scenarios executed by both reviewers.
- Exclude any scenario where either reviewer marked `BLOCKED`.
- Agreement counts only exact status matches (`PASS` with `PASS`, `FAIL` with `FAIL`).

## Formula Validation Checklist

- [X] Formula inputs match ledger totals
- [X] Denominator is non-zero where required
- [X] Rounded values are consistent across recalculation
- [X] Coverage and pass rates are reproducible by independent reviewer
