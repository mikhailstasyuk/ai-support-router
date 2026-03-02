# Research: Text-Based Evaluation Specification

## Decision 1: Scenario script granularity
- Decision: Define text scenarios as deterministic turn-by-turn scripts with explicit preconditions, ordered inputs, expected branch outcomes, and assertion checks.
- Rationale: This enables reproducibility across reviewers and eliminates subjective interpretation.
- Alternatives considered:
  - High-level scenario statements only: rejected due to ambiguous pass/fail outcomes.
  - Free-form reviewer notes without a fixed script: rejected because cross-reviewer consistency cannot be verified.

## Decision 2: Result status model
- Decision: Use a three-state outcome model (`PASS`, `FAIL`, `BLOCKED`) with required evidence fields.
- Rationale: Distinguishes product behavior failures from execution-precondition failures.
- Alternatives considered:
  - Binary pass/fail only: rejected because blocked scenarios are not true product failures.
  - Open-ended status labels: rejected due to reporting inconsistency.

## Decision 3: Requirement traceability method
- Decision: Require each text scenario to reference one or more requirement IDs, and require each in-scope requirement to map to at least one scenario.
- Rationale: Supports measurable coverage and prevents hidden validation gaps.
- Alternatives considered:
  - Story-only mapping: rejected because FR-level coverage could still be incomplete.
  - Optional requirement linking: rejected because coverage metrics would be unreliable.

## Decision 4: Metrics calculation boundaries
- Decision: Define run metrics using scenario counts and requirement mapping counts only (pass rate, blocked rate, requirement coverage rate).
- Rationale: Maintains technology-agnostic measurement aligned to specification outcomes.
- Alternatives considered:
  - Tool-specific telemetry metrics: rejected as implementation detail.
  - Narrative-only summary with no calculation rules: rejected due to unverifiable readiness.

## Decision 5: Voice-scope boundary
- Decision: Exclude voice-evaluation execution steps from this feature, while preserving references needed for compatibility with existing voice-first requirements.
- Rationale: Matches requested scope and avoids accidental expansion into audio testing work.
- Alternatives considered:
  - Include partial voice checks in same feature: rejected as scope creep.
  - Remove all voice references: rejected because parent requirement context must remain coherent.
