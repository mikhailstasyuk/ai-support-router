# Feature Specification: Voice-First Insurance Assistant

**Feature Branch**: `001-voice-insurance-assistant`  
**Created**: 2026-03-02  
**Status**: Approved for Implementation  
**Input**: User description: "Create a voice-first insurance assistant that can handle common customer service tasks end-to-end, with clear branching and human handoff when automation is not enough." Additional stakeholder constraint: keep the specified stack (Python 3.11, OpenAI API, Jinja2, Google Chirp-3 STT/TTS, file-backed mock persistence).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Natural Request Intake and Safe Routing (Priority: P1)

As a caller, I can state my request naturally at the start of the interaction (voice or text mode), receive short clarifying prompts when needed, and either continue in automation or be handed to a human when understanding repeatedly fails.

**Why this priority**: This is the entry point for every call and directly determines containment, customer effort, and trust.

**Independent Test**: Can be fully tested by placing calls with clear and ambiguous requests, verifying correct intent routing, concise clarifications, and human transfer after repeated misunderstandings.

**Acceptance Scenarios**:

1. **Given** a caller starts a voice call or text session, **When** they state a clear request in natural language, **Then** the assistant routes the caller to the matching service flow without requiring menu navigation.
2. **Given** a caller request is ambiguous, **When** the assistant asks a short clarifying question and receives an answer, **Then** the assistant routes to the correct flow.
3. **Given** the assistant cannot determine caller intent, **When** 2 consecutive clarification attempts fail in the same request flow, **Then** the caller is transferred to a human support agent with context summary.

---

### User Story 2 - Verified Policy-Holder Service Execution (Priority: P1)

As a policy holder, I can complete sensitive requests only after successful identity verification, and if verification fails repeatedly I am escalated to a human agent.

**Why this priority**: Security and account protection are mandatory for sensitive policy actions and conflict resolution.

**Independent Test**: Can be fully tested by attempting sensitive actions with both successful and failed verification paths and validating escalation behavior.

**Acceptance Scenarios**:

1. **Given** a policy holder requests a sensitive action, **When** verification succeeds, **Then** the assistant continues with the requested transaction.
2. **Given** a policy holder requests a sensitive action, **When** 3 verification attempts fail in the same call session, **Then** the assistant transfers the caller to a human support agent and provides next steps.
3. **Given** a prospective customer requests a non-sensitive action, **When** no policy verification is required, **Then** the assistant proceeds without blocking on policy-holder checks.

---

### User Story 3 - Appointment Scheduling and Management (Priority: P1)

As a policy holder, I can schedule, update, cancel, identify, or rebook appointments using natural voice input and receive alternatives when preferred slots are unavailable.

**Why this priority**: Appointment operations are high-frequency convenience tasks with immediate customer impact.

**Independent Test**: Can be fully tested by completing each appointment operation, including missing appointment ID recovery and alternative slot offers.

**Acceptance Scenarios**:

1. **Given** a verified policy holder provides policy ID, preferred date, doctor name or specialization, and clinic, **When** scheduling is requested, **Then** the assistant confirms a booking or offers valid alternatives.
2. **Given** a verified policy holder wants to update or cancel an appointment but does not know the appointment ID, **When** the assistant offers recent matching appointments, **Then** the caller can identify and complete the requested change.
3. **Given** a verified policy holder wants to rebook a prior appointment, **When** they confirm the prior visit, **Then** the assistant proposes the earliest valid slots and completes rebooking.

---

### User Story 4 - Policy Renewal, Plan Inquiry, and Clinic Change (Priority: P2)

As a caller, I can compare plans and request renewal or clinic changes, including alternatives when selected options are unavailable or ineligible.

**Why this priority**: These flows drive retention and upsell decisions while reducing manual support load.

**Independent Test**: Can be fully tested by running renewal and clinic-change requests with both valid and invalid eligibility outcomes plus plan comparison requests.

**Acceptance Scenarios**:

1. **Given** a verified policy holder provides policy number for renewal, **When** they choose to keep or change tariff plan and clinic, **Then** the assistant records and confirms the renewal request details.
2. **Given** a caller asks about plans by name, cost range, or all plans, **When** plan options are retrieved, **Then** the assistant provides a concise comparison summary suitable for decision-making.
3. **Given** a verified policy holder requests a clinic change by name, location, or nearby metro, **When** the requested clinic is unavailable or ineligible, **Then** the assistant offers valid alternatives.

---

### User Story 5 - Callback, Compensation, and Clear Next Steps (Priority: P2)

As a caller, I can request callbacks, check compensation status, and initiate compensation appeals; when requests cannot be completed, I receive explicit next steps or human handoff.

**Why this priority**: This covers key conflict and follow-up paths where clarity and continuity matter most.

**Independent Test**: Can be fully tested by submitting callback requests (with and without policy ID), checking compensation status, initiating appeals, and validating missing-information guidance.

**Acceptance Scenarios**:

1. **Given** any caller provides topic, phone number, and preferred callback window, **When** callback request is submitted, **Then** the assistant confirms request intake regardless of policy ownership.
2. **Given** a verified policy holder provides policy ID for compensation status, **When** case information is complete, **Then** the assistant returns current status and next expected step.
3. **Given** a verified policy holder initiates a compensation appeal and required information is missing, **When** submission is attempted, **Then** the assistant provides a clear list of missing documents or details and next actions.

### Edge Cases

- Caller speaks mixed intents in one utterance (for example, renewal and callback), requiring intent prioritization and confirmation.
- Caller repeatedly changes requested date, doctor specialization, or clinic during a single appointment flow.
- No appointments match when caller cannot provide appointment ID.
- Requested clinic is valid geographically but incompatible with current or requested tariff plan.
- Plan comparison request contains only vague budget language (for example, “something cheaper”).
- Caller disconnects mid-verification or mid-transaction and calls back.
- Caller disputes compensation outcome but cannot provide enough appeal information in one call.
- Human handoff queue is unavailable; caller must receive alternate next steps and callback fallback.
- Microphone or audio playback device is unavailable at runtime.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST accept free-form spoken requests as the primary call entry interaction.
- **FR-002**: The system MUST identify the most likely caller intent from spoken input and route to the corresponding service flow.
- **FR-003**: The system MUST ask concise clarifying questions when intent or required details are ambiguous, using a single direct question per turn and no more than 18 spoken words.
- **FR-004**: The system MUST trigger human handoff after 2 consecutive unresolved intent clarification attempts in the same request flow.
- **FR-005**: The system MUST provide a concise context summary to the receiving human agent at handoff.
- **FR-006**: The system MUST require identity verification before any sensitive policy-holder action.
- **FR-007**: The system MUST escalate to a human agent after 3 failed identity verification attempts in the same call session.
- **FR-008**: The system MUST schedule appointments when provided policy ID, preferred date, doctor name or specialization, and clinic.
- **FR-009**: The system MUST offer valid alternative appointment options when preferred options are unavailable.
- **FR-010**: The system MUST support appointment updates and cancellations for verified policy holders.
- **FR-011**: The system MUST help identify the correct appointment from recent matches when appointment ID is unknown.
- **FR-012**: The system MUST support quick rebooking from prior appointments for verified policy holders.
- **FR-013**: The system MUST accept policy renewal requests using policy number.
- **FR-014**: The system MUST capture whether renewal keeps or changes tariff plan and clinic.
- **FR-015**: The system MUST answer plan inquiries by plan name, cost criteria, or request for all plans.
- **FR-016**: The system MUST provide concise plan comparison summaries highlighting meaningful differences for caller choice, including at minimum cost band, clinic/network scope, and coverage tier differences in no more than 3 short sentences.
- **FR-017**: The system MUST accept clinic change requests by clinic name, location, or nearby metro for verified policy holders.
- **FR-018**: The system MUST provide eligible clinic alternatives when requested clinic changes are unavailable or ineligible.
- **FR-019**: The system MUST accept callback requests with topic, phone number, and preferred callback time window.
- **FR-020**: The system MUST allow callback request submission when policy ID is not provided.
- **FR-021**: The system MUST provide compensation status when a verified policy holder supplies policy ID.
- **FR-022**: The system MUST allow a verified policy holder to initiate a compensation appeal.
- **FR-023**: The system MUST return a clear list of missing information or documents specifically when compensation status or compensation appeal processing cannot proceed.
- **FR-024**: The system MUST communicate explicit next steps whenever any request cannot be completed automatically, including one immediate caller action and an optional human handoff action (except live-transfer-unavailable handling, which is governed by `FR-038`).
- **FR-025**: The system MUST exclude payment processing from MVP scope.
- **FR-026**: The system MUST use Jinja2 templates for assistant prompt text generation so voice responses and handoff summaries remain consistent across flows.
- **FR-027**: The system MUST use Google Chirp-3: HD voices as the standard voice output profile for all caller-facing spoken responses in this feature.
- **FR-028**: The system MUST use the OpenAI API as the primary agent LLM for intent handling, clarification prompts, and next-step response generation.
- **FR-029**: The system MUST include a lightweight mock persistence layer with editable fake data so agent flows can read and update caller, policy, appointment, renewal, callback, and compensation records during runtime.
- **FR-030**: The system MUST apply deterministic provider-level fallback behavior: when OpenAI API is unavailable, respond with predefined next-step messaging and offer immediate human handoff; when Google Chirp-3 TTS provider service is unavailable, use predefined fallback voice messaging and preserve the same business outcome.
- **FR-031**: The mock persistence layer MUST persist updates made during flow execution and MUST reflect manual data-file edits before the next caller turn is processed.
- **FR-032**: The system MUST support live voice audio input capture from a local microphone or configured call-audio source for each caller turn, where configured call-audio sources are limited to local PCM/mono stream adapters or WAV-file test streams supported by the runtime adapter contract.
- **FR-033**: The system MUST transcribe captured caller audio into text using Google Chirp-3 speech recognition before intent routing.
- **FR-034**: The system MUST synthesize assistant text responses to speech and play audio output back to the caller on each turn.
- **FR-035**: The system MUST provide a local runnable voice loop mode that executes audio input -> STT -> assistant flow -> TTS playback for same-day manual usage.
- **FR-036**: The system MUST apply deterministic turn-level speech fallback behavior in local runtime: when Chirp-3 STT fails for a turn, the assistant asks for a short repeat once and then offers human handoff if transcription still fails; when Chirp-3 TTS fails for a turn, the assistant uses predefined fallback speech output for that turn while preserving the same business outcome path.
- **FR-037**: The system MUST provide a local runnable text conversation mode that supports multi-turn slot collection, verification prompts, and flow completion for the same intents covered in voice mode.
- **FR-038**: The system MUST provide deterministic fallback behavior when live human transfer is unavailable by giving alternate next steps and offering callback capture in the same interaction.
- **FR-039**: The system MUST capture optional end-of-interaction caller clarity feedback (1-5 score) in both text and voice modes and include the captured results in local metrics reporting.
- **FR-040**: The implementation validation pipeline MUST execute Stage A text-evaluation contract scenarios (`TXT-001` to `TXT-004`) and record deterministic coverage/pass/agreement outputs before Stage B runtime matrix sign-off.

### Non-Functional Requirements

- **NFR-001**: In local runnable mode, assistant response text generation and first playback attempt MUST begin within 8 seconds for at least 90% of measured turns.
- **NFR-002**: Intent resolution behavior MUST be deterministic under provider failure conditions (same fallback branch for the same failure type).
- **NFR-003**: Prompt outputs MUST remain bounded for voice clarity: clarification prompts <= 18 words and next-step prompts <= 30 words.
- **NFR-004**: Persistence writes for flow outcomes MUST be visible on subsequent turn reads without process restart.
- **NFR-005**: Voice and text mode journeys MUST preserve equivalent business outcomes and handoff safety rules for the same intent and input completeness.

### Key Entities *(include if feature involves data)*

- **Caller Profile**: Represents the active caller type and known identifiers; includes caller type (policy holder or prospective), contact phone number, and verification state.
- **Policy Record**: Represents policy context used for protected actions; includes policy ID, policy number, tariff plan, associated clinic, and eligibility state.
- **Appointment Request**: Represents scheduling or management intent; includes preferred date, doctor name or specialization, clinic, operation type (book/update/cancel/rebook), and appointment reference.
- **Renewal Request**: Represents renewal transaction details; includes policy number, selected renewal option, tariff plan choice, clinic choice, and request status.
- **Plan Inquiry**: Represents plan discovery input and output; includes plan name criteria, cost range criteria, comparison set, and summary delivered.
- **Clinic Change Request**: Represents requested clinic modification; includes requested clinic identifiers, location or metro reference, eligibility result, and alternative options.
- **Callback Request**: Represents follow-up contact request; includes topic, callback phone number, preferred time window, optional policy ID, and intake status.
- **Compensation Case**: Represents compensation tracking and dispute flow; includes policy ID, current status, appeal request state, missing information list, and next steps.
- **Handoff Summary**: Represents transfer context package for human agents; includes detected intent, verification outcome, collected fields, failed attempts, unresolved blockers, and caller confirmation state.

### Assumptions & Dependencies

- The fixed implementation stack (Python 3.11, OpenAI API, Jinja2, Google Chirp-3 STT/TTS, file-backed mock persistence) is an explicit stakeholder constraint for this feature and is therefore in-scope despite implementation-specific naming.
- The verification method (for example OTP or personal data challenge) is configurable and chosen by business policy; the user experience remains a short verification checkpoint before sensitive actions.
- Sensitive actions requiring verification include appointment management (book/update/cancel/rebook), renewal requests, clinic changes, compensation status checks, and compensation appeal initiation.
- Retry limits use default values defined in requirements (`FR-004`, `FR-007`) and may be configured without changing flow behavior.
- Clinic eligibility and plan compatibility rules are provided by business policy and are available to this assistant during request evaluation.
- Plan inquiry responses use a mock plan catalog data source available in the editable persistence layer.
- Compensation appeals require at least policy ID and reason for dispute; any additional required information is surfaced dynamically as missing items.
- Local runnable mode acceptance target is that callers receive spoken responses in 90% of turns within 8 seconds end-to-end, measured from end of caller speech to start of assistant playback.
- Prompt text rendering depends on a maintained Jinja2 template set mapped to core flow intents and fallback messages.
- Voice output rendering depends on Google Chirp-3: HD voice profiles selected for clear, consistent caller experience across all flows.
- Speech transcription depends on Google Chirp-3 STT availability for runtime turn processing.
- Agent reasoning and response generation depend on OpenAI API availability as the primary LLM provider.
- Mock data persistence uses a simple file-backed store and supports live data edits while the assistant is running.
- Local runnable mode assumes access to an audio input source and an audio playback output device.
- Runtime acceptance measurement protocol for SC-008/SC-009/SC-010 uses a minimum of 50 manual turns across at least 5 scenarios in one run, with deterministic formulas recorded in `quickstart.md` and `metrics-summary.md`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 90% of callers begin their journey without menu navigation and reach the correct service flow within two conversational turns.
- **SC-002**: At least 85% of verified policy-holder service requests (appointment, renewal, clinic change, compensation status) are completed without human intervention when required data is available.
- **SC-003**: At least 95% of calls with repeated misunderstanding or verification failure are successfully handed off to a human agent with context summary and without requiring callers to restate core details.
- **SC-004**: At least 90% of appointment booking attempts with unavailable preferred slots receive alternative options during the same call.
- **SC-005**: At least 95% of incomplete compensation or appeal requests receive a clear missing-information checklist and explicit next steps before call end.
- **SC-006**: Caller-reported clarity score for failed or escalated interactions reaches 4.0/5.0 or higher in post-call feedback.
- **SC-007**: Callback intake success rate is at least 98% for callers with or without policy ID.
- **SC-008**: In local runnable mode, at least 90% of manual voice turns complete audio input -> STT -> response generation -> TTS playback without operator restart.
- **SC-009**: In local runnable mode, at least 90% of manual turns begin assistant spoken playback within 8 seconds after caller speech ends.
- **SC-010**: In local runnable mode, at least 95% of STT failure turns produce deterministic repeat-or-handoff behavior without silent call dead-ends.
