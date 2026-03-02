# Quickstart: Text Evaluation Specification Validation

## Purpose
Validate that the specification package supports reproducible text-only evaluation execution.

## Prerequisites

- Read `spec.md`, `plan.md`, `research.md`, `data-model.md`, and all files in `contracts/`.
- Use the same seeded baseline state before each run.
- Reset the baseline before starting a new run profile.

## Canonical Scenario Execution Order

Scenarios MUST run in this order for comparable results:
1. `TXT-001`
2. `TXT-002`
3. `TXT-003`
4. `TXT-004`

## Scenario Catalog

### TXT-001 - Deterministic Clarification Path
- Preconditions:
  - Baseline state reset complete.
  - Requirement mapping table loaded.
- Turn Inputs:
  1. "I need help but not sure what exactly"
  2. "I need appointment help"
- Expected Outcomes:
  - System asks one clear clarification question.
  - Scenario routes to a specific requirement-linked branch after clarification.
- Assertions:
  - `A1`: Clarification prompt is present and objective.
  - `A2`: Post-clarification outcome maps to the declared requirement refs.
- Requirement Refs: `FR-001`, `FR-002`, `NFR-001`

### TXT-002 - Requirement Mapping Integrity
- Preconditions:
  - Scenario inventory table populated.
- Turn Inputs:
  1. "Show mapping for FR-001"
  2. "Show mapping for FR-004"
- Expected Outcomes:
  - Mapping matrix returns linked scenarios for each requested requirement.
  - No orphan scenario appears in mapping output.
- Assertions:
  - `A1`: Each queried requirement has at least one linked scenario.
  - `A2`: No scenario is missing requirement refs.
- Requirement Refs: `FR-004`, `NFR-004`, `SC-001`

### TXT-003 - Blocked Status Handling
- Preconditions:
  - Baseline reset intentionally skipped.
- Turn Inputs:
  1. "Execute TXT-001 without reset"
- Expected Outcomes:
  - Result marked `BLOCKED`.
  - Unmet precondition is explicitly captured.
- Assertions:
  - `A1`: Status is `BLOCKED` (not `FAIL`).
  - `A2`: Evidence includes missing-precondition detail.
- Requirement Refs: `FR-006`, `FR-005`, `SC-002`

### TXT-004 - Run Summary Determinism
- Preconditions:
  - At least three scenario result entries exist.
- Turn Inputs:
  1. "Generate run summary"
  2. "Recalculate coverage"
- Expected Outcomes:
  - Summary includes pass rate, coverage rate, reviewer agreement.
  - Recalculated values match original summary.
- Assertions:
  - `A1`: Metrics are present with deterministic values.
  - `A2`: Recalculation yields identical percentages.
- Requirement Refs: `FR-007`, `NFR-004`, `SC-004`

## Requirement Inventory (In-Scope IDs)

| Requirement ID | Description | In Scope |
|---|---|---|
| FR-001 | Text scenarios with explicit preconditions/inputs/expected outcomes | Yes |
| FR-002 | Objective pass/fail assertions | Yes |
| FR-003 | Standard result format | Yes |
| FR-004 | Requirement-to-scenario mapping | Yes |
| FR-005 | Execution order and reset consistency | Yes |
| FR-006 | BLOCKED status semantics | Yes |
| FR-007 | Summary metrics | Yes |
| FR-008 | Text-only scope with voice compatibility boundaries | Yes |
| NFR-001 | Rerun outcome determinism threshold | Yes |
| NFR-002 | Reviewer agreement method with BLOCKED separation | Yes |
| NFR-003 | Required result field completeness threshold | Yes |
| NFR-004 | Deterministic requirement coverage calculations | Yes |
| SC-001 | 100% in-scope requirement mapping | Yes |
| SC-002 | >=95% complete scenario fields | Yes |
| SC-003 | >=95% reviewer outcome agreement | Yes |
| SC-004 | 100% run summaries with coverage + pass rates | Yes |

## Scenario-to-Requirement Mapping Matrix

| Scenario ID | Requirement Refs | Coverage Status |
|---|---|---|
| TXT-001 | FR-001, FR-002, NFR-001 | covered |
| TXT-002 | FR-004, NFR-004, SC-001 | covered |
| TXT-003 | FR-006, FR-005, SC-002 | covered |
| TXT-004 | FR-007, NFR-004, SC-004 | covered |

## Coverage Audit Procedure

1. Check each in-scope requirement appears in at least one scenario mapping row.
2. Flag requirements with zero mappings as unmapped.
3. Flag scenarios with empty requirement refs as orphan scenarios.
4. Record coverage findings in `quickstart-results.md` and run summary metrics.

## Validation Steps

1. Verify every scenario contains ordered turn inputs, expected outcomes, and objective assertions.
2. Verify every scenario includes requirement references.
3. Execute scenarios in canonical order (`TXT-001` to `TXT-004`).
4. Record scenario status as `PASS`, `FAIL`, or `BLOCKED`.
5. Compute summary metrics per contract formulas.
6. Confirm run summary can be independently audited from recorded fields only.

## Execution Reset and Rerun Consistency Policy

- Each run MUST begin with baseline reset.
- If baseline reset is skipped, affected scenarios MUST be marked `BLOCKED`.
- Reruns with identical preconditions and inputs MUST preserve status outcomes for at least 95% of scenarios.

## Reviewer Agreement Protocol

1. Reviewer A and Reviewer B must use the same seeded baseline state and identical scenario execution order.
2. `BLOCKED` scenarios are tracked separately and excluded from pass/fail agreement denominator.
3. Agreement rate is calculated over scenarios executed (not blocked) by both reviewers.
4. Any disagreement requires assertion-level evidence notes from both reviewers.

## Compatibility Boundary Check

- Confirm voice requirement IDs referenced by text-eval specs remain unchanged.
- Confirm text-eval docs do not introduce voice execution steps.
- Confirm compatibility references are documented as non-execution links only.

## Acceptance Checks

- Text scenarios are reproducible with no ambiguous execution steps.
- Result schema supports objective audit for each scenario.
- Coverage and pass-rate calculations are deterministic from recorded data.
- Voice evaluation steps are not required to complete this quickstart.
