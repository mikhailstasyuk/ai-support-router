# Contract: Text Evaluation Results

## Purpose
Define normalized result recording schema for text-evaluation execution.

## Status Model

Allowed statuses:
- `PASS`
- `FAIL`
- `BLOCKED`

## Status Semantics

- `PASS`: All scenario assertions are satisfied.
- `FAIL`: At least one scenario assertion mismatch is observed.
- `BLOCKED`: Scenario could not execute due to unmet prerequisite(s); this is not counted as pass/fail.

## Required Result Fields

Each scenario result MUST record:
- `run_id`
- `scenario_id`
- `status`
- `expected_summary`
- `actual_summary`
- `evidence_notes`
- `requirement_refs`
- `assertion_trace` (assertion-by-assertion outcome list)
- `executed_at`

## Recording Rules

- `FAIL` results MUST cite at least one failed assertion.
- `BLOCKED` results MUST cite unmet precondition(s).
- Requirement references MUST match scenario requirement links.
- Assertion traces MUST indicate which assertion IDs passed/failed/skipped.
- Result entries MUST be sufficient for independent reviewer audit.
