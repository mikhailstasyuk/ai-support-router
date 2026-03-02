# Feature Specification: Text-Based Evaluation Specification

**Feature Branch**: `001-voice-insurance-assistant/evals/text`  
**Created**: 2026-03-02  
**Status**: Approved for Implementation  
**Input**: User description: "Ok, add text based evals (without voice part) to the specs. I"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reproducible Text Scenario Scripts (Priority: P1)

As a spec reviewer, I can run clearly defined text-only evaluation scenarios with explicit inputs and expected outputs so pass/fail decisions are reproducible.

**Why this priority**: Without reproducible scenario scripts, evaluation outcomes are subjective and cannot be trusted for implementation decisions.

**Independent Test**: Can be fully tested by running the documented text scenarios end-to-end and verifying that two independent reviewers produce the same pass/fail results.

**Acceptance Scenarios**:

1. **Given** a text scenario definition, **When** a reviewer follows the exact turn-by-turn inputs, **Then** the expected branch outcomes are unambiguous and verifiable.
2. **Given** two reviewers execute the same text scenario independently, **When** they record results, **Then** they reach the same pass/fail decision for that scenario.

---

### User Story 2 - Requirement-Linked Assertions (Priority: P1)

As a product owner, I can see each text evaluation scenario mapped to specific requirement IDs so coverage gaps are visible before implementation.

**Why this priority**: Requirement traceability prevents false confidence and exposes missing validation coverage early.

**Independent Test**: Can be fully tested by checking each requirement in scope and confirming at least one mapped scenario and assertion exists.

**Acceptance Scenarios**:

1. **Given** the requirement list in the feature spec, **When** mapping is reviewed, **Then** each in-scope text requirement has linked scenarios and explicit assertions.
2. **Given** a scenario result entry, **When** it is inspected, **Then** referenced requirement IDs match the scenario intent and assertions.

---

### User Story 3 - Standardized Results and Metrics (Priority: P2)

As a QA lead, I can collect text-evaluation evidence in a standard format so metrics are consistent and trendable across runs.

**Why this priority**: Standardized result structure is required to aggregate outcomes and judge readiness objectively.

**Independent Test**: Can be fully tested by recording one full evaluation run and verifying all required fields and summary metrics are present.

**Acceptance Scenarios**:

1. **Given** a completed text evaluation run, **When** results are reviewed, **Then** each scenario includes required evidence fields (inputs, expected, actual, pass/fail, requirement links).
2. **Given** a run summary, **When** metrics are computed, **Then** the reported coverage and pass-rate values are traceable to recorded scenario results.

### Edge Cases

- Scenario input includes ambiguous phrasing and must still have objective pass/fail criteria.
- Required scenario preconditions are missing (for example seed data not reset) before execution.
- One scenario depends on prior scenario state and produces inconsistent outcomes across reruns.
- A scenario result is recorded without requirement links or expected outcome evidence.
- New requirements are added but no text scenario mapping is updated.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The specification set MUST include text-only evaluation scenarios with explicit preconditions, turn-by-turn inputs, and expected outcomes.
- **FR-002**: Each text evaluation scenario MUST define objective pass/fail assertions that can be verified by a reviewer without implementation knowledge.
- **FR-003**: The specification set MUST include a standard results format for text evaluations that records scenario ID, inputs, expected outcome, actual outcome, pass/fail, and requirement references.
- **FR-004**: Each in-scope text interaction requirement MUST map to at least one text evaluation scenario.
- **FR-005**: The specification set MUST define execution order and reset conditions for text evaluation scenarios to ensure rerun consistency.
- **FR-006**: The specification set MUST define how to mark scenarios as blocked when prerequisites are not met, separate from pass/fail.
- **FR-007**: The specification set MUST define summary metrics for text evaluation runs, including scenario pass rate and requirement coverage rate.
- **FR-008**: The specification set MUST explicitly exclude voice-evaluation execution from this feature scope while preserving compatibility with existing voice requirements by: (a) retaining existing voice requirement IDs unchanged, (b) not removing or redefining voice requirement meaning, and (c) documenting any text-eval references to voice requirements as non-execution compatibility links only.

### Non-Functional Requirements

- **NFR-001**: Text evaluation reruns using identical preconditions, inputs, and requirement mappings MUST yield identical scenario status outcomes (`PASS`, `FAIL`, or `BLOCKED`) for at least 95% of scenarios.
- **NFR-002**: Reviewer-agreement measurement MUST use a documented comparison method where `BLOCKED` scenarios are counted separately and agreement is computed on scenarios executed by both reviewers.
- **NFR-003**: Result records MUST include all required fields defined by the result contract for at least 95% of scenarios in each run.
- **NFR-004**: Requirement coverage calculations MUST be deterministic from recorded mapping data and produce the same percentage when recalculated independently by two reviewers.

### Assumptions & Dependencies *(mandatory)*

- **Assumption 1**: Text mode remains available as a runnable local interaction mode during evaluation.
- **Assumption 2**: Existing requirement IDs in the parent feature remain stable during this refinement work.
- **Dependency 1**: Current feature artifacts (`spec.md`, `tasks.md`, `quickstart.md`, and result documents) are accessible and editable.
- **Dependency 2**: Reviewers have access to a local environment capable of running text interaction commands.
- **Dependency 3**: Reviewer comparison runs use the same seeded baseline state and the same scenario execution order.
- **Out of Scope**: Defining or expanding voice-mode evaluation scripts, audio fixtures, or voice-provider benchmarking.

### Key Entities *(include if feature involves data)*

- **TextEvaluationScenario**: Represents one text-only validation case; includes scenario ID, preconditions, ordered user inputs, expected branching, and assertion rules.
- **TextEvaluationResult**: Represents observed outcome for one executed scenario; includes expected outcome, actual outcome, pass/fail/blocked status, evidence notes, and requirement references.
- **EvaluationRunSummary**: Represents aggregate run-level metrics; includes total scenarios, passed count, blocked count, pass rate, and requirement coverage rate.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of in-scope text interaction requirements have at least one mapped text evaluation scenario.
- **SC-002**: At least 95% of text evaluation scenarios contain complete execution fields (preconditions, inputs, expected outcomes, and assertions) with no missing required fields.
- **SC-003**: Two independent reviewers executing the same text scenario set reach the same pass/fail outcome for at least 95% of scenarios.
- **SC-004**: Text evaluation run summaries are produced with requirement coverage rate and scenario pass rate for 100% of recorded runs.
