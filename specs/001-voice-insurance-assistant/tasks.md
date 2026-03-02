# Tasks: Voice-First Insurance Assistant (User-Functional Runtime)

**Input**: Design documents from `/specs/001-voice-insurance-assistant/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/, quickstart.md, evals/text/quickstart.md, evals/text/contracts/

**Tests**: Feature spec requires scenario-based validation; tasks include executable validation and evidence capture.

**Organization**: Tasks are grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Task can run in parallel (different files, no unmet dependency)
- **[Story]**: User-story label (`[US1]` to `[US5]`) for story phases only
- Every task includes an exact file path

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Align local runtime tooling and configs for fully functional text + voice execution

- [X] T001 Create runtime package markers in `src/assistant/flows/__init__.py`, `src/assistant/llm/__init__.py`, `src/assistant/prompting/__init__.py`, `src/assistant/runtime/__init__.py`, `src/assistant/store/__init__.py`, and `src/assistant/voice/__init__.py`
- [X] T002 Update dependency set for functional runtime in `requirements.txt`
- [X] T003 [P] Add complete environment settings for OpenAI, Chirp-3, runtime modes, and data paths in `.env.example`
- [X] T004 [P] Add developer run and troubleshooting commands for text + voice modes in `README.md`
- [X] T005 [P] Add command-line helper script for local startup and validation in `scripts/run_local.sh`
- [X] T006 Add deterministic logging configuration and runtime flags in `src/assistant/config.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build shared conversation/data/provider infrastructure required by all stories

**⚠️ CRITICAL**: Complete this phase before user-story phases

- [X] T007 Implement strict typed domain models and enums aligned to `data-model.md` in `src/assistant/models.py`
- [X] T008 [P] Implement canonical intent, response, and retry constants in `src/assistant/constants.py`
- [X] T009 Implement flow-level input validation and missing-slot detection in `src/assistant/validation.py`
- [X] T010 Implement conversation session state object and state transitions in `src/assistant/runtime/session_state.py`
- [X] T011 Implement turn manager for slot collection and turn-to-turn memory in `src/assistant/runtime/turn_manager.py`
- [X] T012 Implement robust handoff summary schema validation and builder in `src/assistant/handoff.py`
- [X] T013 Implement OpenAI structured intent+response adapter with deterministic parse/repair in `src/assistant/llm/openai_agent.py`
- [X] T014 [P] Implement provider health checker and fallback trigger policy in `src/assistant/runtime/provider_health.py`
- [X] T015 Implement Jinja2 template engine with required-variable contracts in `src/assistant/prompting/template_engine.py`
- [X] T016 [P] Implement prompt fallback text catalog and utility functions in `src/assistant/prompting/fallbacks.py`
- [X] T017 Implement repository interfaces and ID-safe CRUD behavior in `src/assistant/store/repositories.py`
- [X] T018 Implement atomic file backend IO, locking, and error propagation in `src/assistant/store/file_backend.py`
- [X] T019 Implement turn-boundary refresh and write-through persistence manager in `src/assistant/store/store.py`
- [X] T020 [P] Seed complete mock datasets for callers/policies/plans/appointments/renewals/callbacks/compensations/feedback in `data/mock/*.json`
- [X] T021 [P] Update deterministic data reset command in `scripts/seed_mock_data.py`
- [X] T022 Implement central router dispatch contract and payment out-of-scope guard in `src/assistant/router.py`

**Checkpoint**: Shared runtime, provider, and persistence primitives are ready for all user stories

---

## Phase 3: User Story 1 - Natural Request Intake and Safe Routing (Priority: P1) 🎯 MVP

**Goal**: Deliver natural conversation intake with reliable intent routing, clarification, and safe escalation in both text and voice modes

**Independent Test**: Execute quickstart scenarios 1, 8, 11, 13, and 15; verify clear requests route correctly, ambiguity is clarified, unresolved requests hand off after threshold, and text-mode slot capture is functional.

### Implementation for User Story 1

- [X] T023 [US1] Implement high-recall intake intent normalization for natural user phrasing in `src/assistant/flows/intake_flow.py`
- [X] T024 [P] [US1] Implement ambiguity clarification policy and retry counters in `src/assistant/flows/clarification_flow.py`
- [X] T025 [US1] Implement unresolved-intent escalation and handoff trigger in `src/assistant/flows/escalation_flow.py`
- [X] T026 [P] [US1] Implement response builder integrating OpenAI output + Jinja2 prompt rendering in `src/assistant/prompting/response_builder.py`
- [X] T027 [US1] Implement explicit OpenAI-unavailable caller messaging and branch behavior in `src/assistant/flows/fallback_flow.py`
- [X] T028 [US1] Wire end-to-end intake orchestration in `src/assistant/app.py`
- [X] T029 [US1] Implement text-mode interactive slot capture (not raw utterance-only) in `src/assistant/runtime/text_turn_loop.py`
- [X] T030 [US1] Route `python -m src.assistant.app` through text turn loop in `src/assistant/app.py`

**Checkpoint**: US1 works as a real user conversation in text mode and routes correctly

---

## Phase 4: User Story 2 - Verified Policy-Holder Service Execution (Priority: P1)

**Goal**: Enforce identity verification before sensitive actions with deterministic failure escalation and state persistence

**Independent Test**: Execute quickstart scenarios 2 and 13; verify sensitive actions are blocked until verification and handoff occurs after 3 failed attempts.

### Implementation for User Story 2

- [X] T031 [US2] Implement verification challenge orchestration and state machine in `src/assistant/flows/verification_flow.py`
- [X] T032 [P] [US2] Implement verification prompt generation with template contract compliance in `src/assistant/prompting/verification_prompts.py`
- [X] T033 [US2] Implement sensitive-intent guard checks using caller/session state in `src/assistant/guards.py`
- [X] T034 [US2] Integrate verification guard and continuation paths in `src/assistant/router.py`
- [X] T035 [US2] Persist verification attempt counters and outcomes in `src/assistant/store/store.py`
- [X] T036 [US2] Include verification-failure context details in transfer summaries in `src/assistant/handoff.py`

**Checkpoint**: US2 is independently functional and secure in both text and voice request paths

---

## Phase 5: User Story 3 - Appointment Scheduling and Management (Priority: P1)

**Goal**: Support booking, update, cancel, ID recovery, and rebooking with persisted updates and alternatives

**Independent Test**: Execute quickstart scenarios 3 and 4; verify appointment changes persist and unknown appointment ID path succeeds with candidate selection.

### Implementation for User Story 3

- [X] T037 [US3] Implement appointment flow orchestration for book/update/cancel/rebook in `src/assistant/flows/appointment_flow.py`
- [X] T038 [P] [US3] Implement appointment candidate matching and disambiguation in `src/assistant/flows/appointment_matching.py`
- [X] T039 [P] [US3] Implement alternative slot selection and ranking policy in `src/assistant/flows/appointment_alternatives.py`
- [X] T040 [US3] Implement appointment prompt bindings and spoken response shaping in `src/assistant/prompting/appointment_prompts.py`
- [X] T041 [US3] Register and route appointment intents with required field handling in `src/assistant/router.py`
- [X] T042 [US3] Implement appointment repository write/read consistency behavior in `src/assistant/store/repositories.py`

**Checkpoint**: US3 is independently functional with real persisted outcomes

---

## Phase 6: User Story 4 - Policy Renewal, Plan Inquiry, and Clinic Change (Priority: P2)

**Goal**: Enable renewal requests, plan comparisons, and clinic changes with eligibility-aware alternatives

**Independent Test**: Execute quickstart scenario 5; verify renewal capture, plan summary quality, and clinic alternative handling with persisted state updates.

### Implementation for User Story 4

- [X] T043 [US4] Implement renewal capture and validation flow in `src/assistant/flows/renewal_flow.py`
- [X] T044 [P] [US4] Implement plan inquiry parsing and concise comparison summarization in `src/assistant/flows/plan_flow.py`
- [X] T045 [P] [US4] Implement clinic eligibility checks and alternatives generation in `src/assistant/flows/clinic_flow.py`
- [X] T046 [US4] Implement policy-flow prompt bindings for renewal/plan/clinic responses in `src/assistant/prompting/policy_prompts.py`
- [X] T047 [US4] Register renewal/plan/clinic intents and branch handling in `src/assistant/router.py`
- [X] T048 [US4] Persist renewal and clinic update records in `src/assistant/store/repositories.py`

**Checkpoint**: US4 is independently functional with clear alternatives and persistence

---

## Phase 7: User Story 5 - Callback, Compensation, and Clear Next Steps (Priority: P2)

**Goal**: Deliver callback intake, compensation status, appeal initiation, and explicit next-step messaging for incomplete requests

**Independent Test**: Execute quickstart scenarios 6 and 7; verify callback acceptance without policy ID and compensation appeal missing-items behavior.

### Implementation for User Story 5

- [X] T049 [US5] Implement callback capture flow with optional policy identifier in `src/assistant/flows/callback_flow.py`
- [X] T050 [P] [US5] Implement compensation status retrieval and response shaping in `src/assistant/flows/compensation_flow.py`
- [X] T051 [P] [US5] Implement compensation appeal flow with missing-item checklist generation in `src/assistant/flows/compensation_appeal.py`
- [X] T052 [US5] Implement explicit next-step prompt generation for incomplete actions in `src/assistant/prompting/next_step_prompts.py`
- [X] T053 [US5] Register callback and compensation intents with guard behavior in `src/assistant/router.py`
- [X] T054 [US5] Persist callback and compensation updates in `src/assistant/store/repositories.py`

**Checkpoint**: US5 is independently functional with actionable failure guidance

---

## Phase 8: Live Voice Runtime Completion (Cross-Story)

**Purpose**: Provide real user-capable voice conversations with actual STT/TTS adapters and fallback handling

- [X] T055 Implement microphone/call-source capture with real audio frames in `src/assistant/voice/audio_input.py`
- [X] T056 Implement Google Chirp-3 STT adapter with retryable transcription errors in `src/assistant/voice/stt_adapter.py`
- [X] T057 Implement Google Chirp-3 HD TTS synthesis adapter in `src/assistant/voice/chirp3_voice.py`
- [X] T058 Implement audio playback output adapter for synthesized speech in `src/assistant/voice/audio_output.py`
- [X] T059 Integrate real voice turn loop orchestration in `src/assistant/runtime/voice_turn_loop.py`
- [X] T060 Integrate voice loop startup, mode flags, and graceful shutdown in `src/assistant/app.py`
- [X] T061 Implement deterministic STT/TTS fallback messages and handoff offers in `src/assistant/runtime/voice_turn_loop.py`
- [X] T062 Implement handoff-queue-unavailable fallback branch with callback offer in `src/assistant/flows/escalation_flow.py`

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency, user-level validation, and release-readiness for local usage

- [X] T063 [P] Align response schemas, field names, and validation messages across flows in `src/assistant/models.py` and `src/assistant/validation.py`
- [X] T064 [P] Improve branch wording consistency and clarity in `src/assistant/flows/*.py` and `src/assistant/prompting/*.py`
- [X] T065 Implement runtime metrics capture aligned to SC-001..SC-010 in `src/assistant/metrics.py`
- [X] T066 Validate quickstart scenarios 1-17 and capture evidence in `specs/001-voice-insurance-assistant/quickstart-results.md`
- [X] T067 Validate prompt-template contract coverage and required variable handling in `src/assistant/prompting/template_engine.py` and `prompts/*.j2`
- [X] T068 Validate OpenAI primary path behavior and deterministic fallback in `src/assistant/llm/openai_agent.py`
- [X] T069 Validate mock persistence turn-refresh and manual-edit reflection in `src/assistant/store/store.py` and `data/mock/*.json`
- [X] T070 Validate handoff summary completeness and transfer readiness in `src/assistant/handoff.py`
- [X] T071 Produce SC-001..SC-010 metrics summary report in `specs/001-voice-insurance-assistant/metrics-summary.md`
- [X] T072 Update end-user setup/run/debug instructions for text and voice conversations in `README.md`
- [X] T073 Implement optional end-of-interaction clarity feedback capture prompt in `src/assistant/runtime/text_turn_loop.py` and `src/assistant/runtime/voice_turn_loop.py`
- [X] T074 Implement feedback persistence repository and ID mapping in `src/assistant/store/repositories.py` and `data/mock/feedback.json`
- [X] T075 Include clarity feedback aggregation in metrics reporting for SC-006 in `src/assistant/metrics.py` and `specs/001-voice-insurance-assistant/metrics-summary.md`
- [X] T076 Validate handoff-unavailable and clarity-feedback scenarios in `specs/001-voice-insurance-assistant/quickstart-results.md`
- [X] T077 Validate text-mode parity against voice-mode business outcomes in `specs/001-voice-insurance-assistant/quickstart-results.md`
- [X] T078 Execute Stage A text-eval scenarios TXT-001..TXT-004 for `FR-040` and record contract-compliant results in `specs/001-voice-insurance-assistant/evals/text/quickstart-results.md`
- [X] T079 Produce Stage A deterministic coverage/pass/agreement metrics for `FR-040` in `specs/001-voice-insurance-assistant/evals/text/metrics-summary.md`
- [X] T080 Implement prompt-length guard utilities enforcing `FR-003`/`NFR-003` limits in `src/assistant/validation.py`
- [X] T081 Validate prompt-length guard behavior against scenario 17 in `specs/001-voice-insurance-assistant/quickstart-results.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: starts immediately
- **Phase 2 (Foundational)**: depends on Setup and blocks all story work
- **Phases 3-7 (User Stories)**: depend on Foundational completion
- **Phase 8 (Live Voice Runtime Completion)**: depends on Foundational + US1 routing baseline
- **Phase 9 (Polish)**: depends on all target story/runtime phases

### User Story Dependencies

- **US1 (P1)**: starts after Foundational; establishes core interaction loop
- **US2 (P1)**: depends on US1 intake/session routing
- **US3 (P1)**: depends on US1 + US2 verification guards
- **US4 (P2)**: depends on US1 + US2
- **US5 (P2)**: depends on US1 + US2

### Suggested Completion Order

1. US1
2. US2
3. US3
4. US4
5. US5
6. Live Voice Runtime Completion
7. Polish

### Dependency Graph

- Setup -> Foundational -> US1 -> US2 -> {US3, US4, US5} -> Voice Runtime Completion -> Polish

### Parallel Opportunities

- Setup: T003, T004, T005 in parallel after T001-T002
- Foundational: T008, T014, T016, T020, T021 in parallel after T007 baseline
- US1: T024 and T026 in parallel after T023
- US2: T032 and T033 in parallel after T031
- US3: T038 and T039 in parallel after T037
- US4: T044 and T045 in parallel after T043
- US5: T050 and T051 in parallel after T049
- Polish: T063 and T064 in parallel before T065-T081

---

## Parallel Execution Examples

### User Story 1

```bash
Task: "T024 [US1] Implement ambiguity clarification policy in src/assistant/flows/clarification_flow.py"
Task: "T026 [US1] Implement response builder in src/assistant/prompting/response_builder.py"
```

### User Story 2

```bash
Task: "T032 [US2] Implement verification prompts in src/assistant/prompting/verification_prompts.py"
Task: "T033 [US2] Implement sensitive-intent guard checks in src/assistant/guards.py"
```

### User Story 3

```bash
Task: "T038 [US3] Implement appointment candidate matching in src/assistant/flows/appointment_matching.py"
Task: "T039 [US3] Implement alternative slot selection in src/assistant/flows/appointment_alternatives.py"
```

### User Story 4

```bash
Task: "T044 [US4] Implement plan inquiry summarization in src/assistant/flows/plan_flow.py"
Task: "T045 [US4] Implement clinic eligibility alternatives in src/assistant/flows/clinic_flow.py"
```

### User Story 5

```bash
Task: "T050 [US5] Implement compensation status flow in src/assistant/flows/compensation_flow.py"
Task: "T051 [US5] Implement compensation appeal flow in src/assistant/flows/compensation_appeal.py"
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Setup and Foundational phases
2. Complete US1 (natural intake and safe routing)
3. Validate text-mode real conversation path using quickstart scenarios 1 and 8
4. Demo routing/handoff before expanding to other stories

### Incremental Delivery

1. Setup + Foundational
2. US1 (MVP user interaction)
3. US2 (security + verification)
4. US3 (appointments)
5. US4 (renewal/plans/clinic)
6. US5 (callback/compensation)
7. Live Voice Runtime Completion
8. Polish validation and evidence capture

### User-Facing Functional Target

- Text mode must support multi-turn slot collection and completion of all core flows.
- Voice mode must support real audio capture, STT transcription, and TTS playback.
- Data access must persist and rehydrate between turns with manual edit visibility.

---

## Notes

- All tasks follow strict checklist format and include explicit file paths.
- `[P]` tasks are intentionally file-isolated for safe parallel execution.
- Each user story phase remains independently testable using quickstart criteria.
