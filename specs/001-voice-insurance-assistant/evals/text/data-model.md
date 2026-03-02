# Data Model: Text-Based Evaluation Specification

## 1. TextEvaluationScenario

### Fields
- `scenario_id` (string, required): Stable unique ID (e.g., `TXT-001`).
- `title` (string, required): Human-readable scenario name.
- `preconditions` (list[string], required): Required setup state before execution.
- `turn_inputs` (list[string], required): Ordered user input steps.
- `expected_outcomes` (list[string], required): Expected branch/output checkpoints.
- `assertions` (list[string], required): Objective pass/fail checks.
- `requirement_refs` (list[string], required): Linked requirement IDs.
- `execution_order` (integer, required): Sequence order within a run.

### Validation Rules
- `scenario_id` must be unique within the scenario set.
- `turn_inputs`, `expected_outcomes`, and `assertions` must be non-empty.
- Every scenario must include at least one requirement reference.

### Relationships
- One scenario can produce many execution results over time.

## 2. TextEvaluationResult

### Fields
- `run_id` (string, required): Parent run identifier.
- `scenario_id` (string, required): References `TextEvaluationScenario.scenario_id`.
- `status` (enum, required): `PASS`, `FAIL`, `BLOCKED`.
- `expected_summary` (string, required): Condensed expected behavior.
- `actual_summary` (string, required): Observed behavior.
- `evidence_notes` (string, required): Verification evidence and deviations.
- `requirement_refs` (list[string], required): Requirement IDs evaluated by this result.
- `assertion_trace` (list[string], required): Assertion-level outcomes with mismatch notes.
- `reviewer_id` (string, optional): Reviewer identity marker.
- `executed_at` (string timestamp, required): Execution timestamp.

### Validation Rules
- `status` must be one of `PASS`, `FAIL`, `BLOCKED`.
- `BLOCKED` requires explicit unmet-precondition notes.
- `FAIL` requires at least one assertion mismatch note.

### Relationships
- Each result belongs to one scenario and one evaluation run.

## 3. EvaluationRunSummary

### Fields
- `run_id` (string, required)
- `total_scenarios` (integer, required)
- `passed_count` (integer, required)
- `failed_count` (integer, required)
- `blocked_count` (integer, required)
- `scenario_pass_rate` (decimal, required)
- `requirement_coverage_rate` (decimal, required)
- `reviewer_agreement_rate` (decimal, required)
- `unmapped_requirements` (list[string], optional)
- `notes` (string, optional)

### Validation Rules
- `total_scenarios = passed_count + failed_count + blocked_count`.
- Rates must be between 0 and 1 inclusive.
- Coverage rate must be based on in-scope requirement set.
- Rates are rounded to 4 decimal places after calculation.

### Relationships
- One run summary aggregates many text evaluation results.
