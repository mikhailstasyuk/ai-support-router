# Tasks: Text-Based Evaluation Specification

**Input**: Design documents from `/specs/001-voice-insurance-assistant/evals/text/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md

**Tests**: This feature requires scenario-based validation tasks because outputs are evaluation artifacts.

**Organization**: Tasks are grouped by user story to enable independent implementation and validation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Task can run in parallel (different file, no unmet dependency)
- **[Story]**: User story label for story-specific tasks (`[US1]`, `[US2]`, `[US3]`)
- Every task includes explicit file path(s)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize documentation scaffolding and result artifact paths for text-only eval pipeline

- [X] T001 Create evaluation-run ledger template with required headers in `specs/001-voice-insurance-assistant/evals/text/quickstart-results.md`
- [X] T002 Create result artifact shell in `specs/001-voice-insurance-assistant/evals/text/quickstart-results.md`
- [X] T003 [P] Create metrics artifact shell in `specs/001-voice-insurance-assistant/evals/text/metrics-summary.md`
- [X] T004 [P] Add feature-level README note for text-eval-only scope and voice-compatibility boundaries in `specs/001-voice-insurance-assistant/evals/text/README.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Define cross-story baseline schema and governance rules before scenario authoring

**⚠️ CRITICAL**: Complete this phase before user story phases

- [X] T005 Define canonical ID rules for scenarios, runs, and requirements in `specs/001-voice-insurance-assistant/evals/text/contracts/requirement-coverage-contract.md`
- [X] T006 [P] Define normalized status semantics (`PASS`/`FAIL`/`BLOCKED`) in `specs/001-voice-insurance-assistant/evals/text/contracts/text-result-contract.md`
- [X] T007 [P] Define required scenario field constraints and validation rules in `specs/001-voice-insurance-assistant/evals/text/contracts/text-scenario-contract.md`
- [X] T008 Define run-summary metric formulas and rounding rules in `specs/001-voice-insurance-assistant/evals/text/data-model.md`
- [X] T009 Define canonical scenario execution order policy and ordering constraints in `specs/001-voice-insurance-assistant/evals/text/quickstart.md`
- [X] T010 Define execution reset prerequisites and rerun consistency policy in `specs/001-voice-insurance-assistant/evals/text/quickstart.md`

**Checkpoint**: Foundation complete; scenario and result authoring can proceed consistently

---

## Phase 3: User Story 1 - Reproducible Text Scenario Scripts (Priority: P1) 🎯 MVP

**Goal**: Produce deterministic, executable text scenario scripts with objective pass/fail assertions

**Independent Test**: Two reviewers can execute the same text scenario set and reach the same pass/fail decision on at least 95% of scenarios.

### Implementation for User Story 1

- [X] T011 [US1] Create scenario catalog section with ordered execution list in `specs/001-voice-insurance-assistant/evals/text/quickstart.md`
- [X] T012 [US1] Define scenario `TXT-001` with explicit preconditions, turn inputs, expected outcomes, and assertions in `specs/001-voice-insurance-assistant/evals/text/quickstart.md`
- [X] T013 [US1] Define scenario `TXT-002` with explicit preconditions, turn inputs, expected outcomes, and assertions in `specs/001-voice-insurance-assistant/evals/text/quickstart.md`
- [X] T014 [P] [US1] Define scenario `TXT-003` with explicit preconditions, turn inputs, expected outcomes, and assertions in `specs/001-voice-insurance-assistant/evals/text/quickstart.md`
- [X] T015 [P] [US1] Define scenario `TXT-004` with explicit preconditions, turn inputs, expected outcomes, and assertions in `specs/001-voice-insurance-assistant/evals/text/quickstart.md`
- [X] T016 [US1] Add reviewer-execution protocol for deterministic script following in `specs/001-voice-insurance-assistant/evals/text/quickstart.md`
- [X] T017 [US1] Add ambiguous-input handling assertions to scenario definitions in `specs/001-voice-insurance-assistant/evals/text/quickstart.md`

**Checkpoint**: US1 text scenarios are reproducible and independently executable

---

## Phase 4: User Story 2 - Requirement-Linked Assertions (Priority: P1)

**Goal**: Ensure every in-scope text requirement is traceably covered by scenario assertions

**Independent Test**: Requirement-to-scenario matrix shows 100% mapping coverage for in-scope text requirements.

### Implementation for User Story 2

- [X] T018 [US2] Add requirement inventory table with in-scope IDs in `specs/001-voice-insurance-assistant/evals/text/quickstart.md`
- [X] T019 [US2] Add scenario-to-requirement mapping matrix in `specs/001-voice-insurance-assistant/evals/text/quickstart.md`
- [X] T020 [P] [US2] Add requirement coverage validation checklist entries in `specs/001-voice-insurance-assistant/evals/text/contracts/requirement-coverage-contract.md`
- [X] T021 [US2] Add orphan-scenario and unmapped-requirement detection rules in `specs/001-voice-insurance-assistant/evals/text/contracts/requirement-coverage-contract.md`
- [X] T022 [US2] Add assertion-to-requirement trace field definitions in `specs/001-voice-insurance-assistant/evals/text/contracts/text-result-contract.md`
- [X] T023 [US2] Add coverage audit procedure in `specs/001-voice-insurance-assistant/evals/text/quickstart.md`

**Checkpoint**: US2 delivers full requirement traceability for text evaluations

---

## Phase 5: User Story 3 - Standardized Results and Metrics (Priority: P2)

**Goal**: Standardize result recording and run-level metric summaries for text evaluation runs

**Independent Test**: A full sample run can be recorded with complete required fields and deterministic metric calculations.

### Implementation for User Story 3

- [X] T024 [US3] Define per-scenario result entry template in `specs/001-voice-insurance-assistant/evals/text/quickstart-results.md`
- [X] T025 [US3] Define run metadata and reviewer metadata fields in `specs/001-voice-insurance-assistant/evals/text/quickstart-results.md`
- [X] T026 [P] [US3] Add BLOCKED-status documentation and evidence examples in `specs/001-voice-insurance-assistant/evals/text/quickstart-results.md`
- [X] T027 [P] [US3] Add FAIL-status assertion mismatch examples in `specs/001-voice-insurance-assistant/evals/text/quickstart-results.md`
- [X] T028 [US3] Create run-summary aggregation template in `specs/001-voice-insurance-assistant/evals/text/metrics-summary.md`
- [X] T029 [US3] Add scenario pass-rate and requirement coverage calculation steps in `specs/001-voice-insurance-assistant/evals/text/metrics-summary.md`
- [X] T030 [US3] Add reviewer-agreement metric calculation method in `specs/001-voice-insurance-assistant/evals/text/metrics-summary.md`

**Checkpoint**: US3 enables standardized, auditable result reporting and metrics

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency pass across contracts, data model, quickstart, and result artifacts

- [X] T031 [P] Align terminology (`scenario`, `assertion`, `blocked`, `coverage`) across all docs in `specs/001-voice-insurance-assistant/evals/text/*.md` and `specs/001-voice-insurance-assistant/evals/text/contracts/*.md`
- [X] T032 [P] Verify all required contract fields are reflected in data model entities in `specs/001-voice-insurance-assistant/evals/text/data-model.md`
- [X] T033 Validate quickstart execution steps against scenario/result contracts in `specs/001-voice-insurance-assistant/evals/text/quickstart.md`
- [X] T034 Validate sample result entries satisfy text-result contract in `specs/001-voice-insurance-assistant/evals/text/quickstart-results.md`
- [X] T035 Validate metrics formulas against coverage contract rules in `specs/001-voice-insurance-assistant/evals/text/metrics-summary.md`
- [X] T036 Run full documentation readiness review and summarize PASS/FAIL in `specs/001-voice-insurance-assistant/evals/text/checklists/requirements.md`
- [X] T037 Validate FR-008 voice-compatibility boundary evidence in `specs/001-voice-insurance-assistant/evals/text/quickstart-results.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: starts immediately
- **Phase 2 (Foundational)**: depends on Setup and blocks all story phases
- **Phases 3-5 (User Stories)**: depend on Foundational completion
- **Phase 6 (Polish)**: depends on user-story completion

### User Story Dependencies

- **US1 (P1)**: starts after Foundational; defines executable scenario scripts
- **US2 (P1)**: depends on US1 scenario catalog for traceability mapping
- **US3 (P2)**: depends on US1 and US2 outputs for result and metric standardization

### Suggested Completion Order

1. US1
2. US2
3. US3

### Dependency Graph

- Setup -> Foundational -> US1 -> US2 -> US3 -> Polish

### Parallel Opportunities

- Setup: T003 and T004 after T001-T002
- Foundational: T006 and T007 after T005 baseline
- US1: T014 and T015 after T011
- US2: T020 after T018-T019
- US3: T026 and T027 after T024-T025
- Polish: T031 and T032 before T033-T037

---

## Parallel Execution Examples

### User Story 1

```bash
Task: "T014 [US1] Define scenario TXT-003 in specs/001-voice-insurance-assistant/evals/text/quickstart.md"
Task: "T015 [US1] Define scenario TXT-004 in specs/001-voice-insurance-assistant/evals/text/quickstart.md"
```

### User Story 2

```bash
Task: "T019 [US2] Add scenario-to-requirement mapping matrix in specs/001-voice-insurance-assistant/evals/text/quickstart.md"
Task: "T020 [US2] Add coverage validation checklist in specs/001-voice-insurance-assistant/evals/text/contracts/requirement-coverage-contract.md"
```

### User Story 3

```bash
Task: "T026 [US3] Add BLOCKED-status evidence examples in specs/001-voice-insurance-assistant/evals/text/quickstart-results.md"
Task: "T027 [US3] Add FAIL-status assertion mismatch examples in specs/001-voice-insurance-assistant/evals/text/quickstart-results.md"
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Setup and Foundational phases
2. Complete US1 reproducible scenario scripts
3. Validate cross-reviewer reproducibility before continuing

### Incremental Delivery

1. Setup + Foundational
2. US1 (reproducible scripts)
3. US2 (requirement-linked assertions)
4. US3 (standardized results and metrics)
5. Polish validation

### Notes

- Tasks are documentation-focused and immediately executable by an LLM.
- Scope remains text-evaluation only; no voice execution work is included.
