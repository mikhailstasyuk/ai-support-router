# Contract: Requirement Coverage Mapping

## Purpose
Define mapping and coverage rules between requirements and text evaluation scenarios.

## Canonical ID Rules

- Scenario IDs MUST follow `TXT-###` with zero-padded numeric suffix (`TXT-001`, `TXT-002`, ...).
- Run IDs MUST follow `RUN-YYYYMMDD-###` where `###` increments per day.
- Requirement IDs MUST use canonical source IDs (`FR-###`, `NFR-###`, `SC-###`) exactly as defined in source specs.
- ID values are case-sensitive and MUST NOT be rewritten in result artifacts.

## Mapping Rules

- Each in-scope requirement MUST map to at least one scenario.
- Each scenario MUST map to at least one requirement.
- Mapping identifiers MUST use canonical requirement IDs from the source spec.
- Scenario mapping tables MUST include a coverage status column (`covered` or `unmapped`).

## Coverage Metrics Rules

- `requirement_coverage_rate = covered_requirements / total_in_scope_requirements`
- `scenario_pass_rate = passed_scenarios / total_executed_scenarios`
- `total_executed_scenarios = PASS + FAIL + BLOCKED`

## Validation Rules

- Unmapped requirements MUST be explicitly listed in run summary.
- Orphan scenarios (no requirement refs) MUST fail contract validation.
- Coverage checklist entries MUST verify: no orphan scenarios, no unmapped in-scope requirements, and formula consistency.
- Coverage recalculation by independent reviewers MUST produce the same value when using identical input records.
