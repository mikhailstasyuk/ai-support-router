# Quickstart Results: Text Evaluation Specification

## Evaluation Run Metadata

- `run_id`: RUN-20260302-001
- `run_date`: 2026-03-02
- `reviewer_a`: codex-a
- `reviewer_b`: codex-b
- `baseline_reset_confirmed`: yes
- `execution_order_confirmed`: yes

## Scenario Result Ledger (Required Headers)

| scenario_id | status (PASS/FAIL/BLOCKED) | expected_summary | actual_summary | requirement_refs | assertion_trace | evidence_notes | executed_at |
|---|---|---|---|---|---|---|---|
| TXT-001 | PASS | One clarification then branch mapping | Clarification prompt issued, mapped to appointment flow after follow-up | FR-001, FR-002, NFR-001 | A1=pass; A2=pass | Clarification wording objective and branch mapped to declared refs | 2026-03-02T19:40:00Z |
| TXT-002 | PASS | Requirement mapping returns linked scenarios | Mapping table links queried requirements; no orphan row observed | FR-004, NFR-004, SC-001 | A1=pass; A2=pass | Coverage matrix includes requirement refs per scenario | 2026-03-02T19:41:00Z |
| TXT-003 | BLOCKED | Run blocked when reset skipped | Marked BLOCKED with explicit unmet precondition note | FR-006, FR-005, SC-002 | A1=pass; A2=pass | Baseline reset intentionally skipped; correctly recorded as BLOCKED | 2026-03-02T19:42:00Z |
| TXT-004 | PASS | Run summary and coverage recalc deterministic | Recalculated percentages matched original summary values | FR-007, NFR-004, SC-004 | A1=pass; A2=pass | Metric formulas reproducible from ledger fields | 2026-03-02T19:43:00Z |

## BLOCKED Example

- `scenario_id`: TXT-003
- `status`: BLOCKED
- `evidence_notes`: "Baseline reset step was skipped; scenario preconditions not met."

## FAIL Example

- `scenario_id`: TXT-001
- `status`: FAIL
- `assertion_trace`: "A1=pass; A2=fail (outcome did not map to expected requirement refs)"
- `evidence_notes`: "Branch output diverged from expected mapping."

## Coverage Audit Evidence

- Unmapped requirements: none
- Orphan scenarios: none
- Coverage checklist result: pass

## FR-008 Compatibility Boundary Evidence

- Voice requirement IDs unchanged: yes
- Voice execution steps introduced in text-eval docs: no
- Non-execution compatibility link-only rule preserved: yes
- Notes: Text-eval artifacts remain non-execution references for voice requirements only.
