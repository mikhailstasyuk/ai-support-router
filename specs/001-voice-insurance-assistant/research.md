# Research: Voice-First Insurance Assistant

## Unknown/Clarification Resolution

No unresolved `NEEDS CLARIFICATION` entries remain from technical context.
All core context values are resolved from specification constraints.

## Decision 1: Intent handling provider strategy
- Decision: Use OpenAI API as the primary intent/clarification/next-step provider with deterministic local fallback messaging.
- Rationale: Meets FR-028 and FR-030 while preserving predictable outcomes when provider is unavailable.
- Alternatives considered:
  - Heuristic-only classification: rejected because it does not satisfy primary-provider requirement.
  - Multi-provider orchestration: rejected as unnecessary complexity for MVP.

## Decision 2: Prompt rendering standard
- Decision: Use a single Jinja2 template family for all caller-facing prompt classes and handoff summaries.
- Rationale: Keeps branching language consistent and auditable across flows (FR-026).
- Alternatives considered:
  - Inline string assembly: rejected due to drift and inconsistency risk.
  - Multiple template engines: rejected for added complexity without business benefit.

## Decision 3: Voice IO runtime approach
- Decision: Support local runnable voice loop (capture -> STT -> flow -> TTS playback) using Google Chirp-3 contracts and deterministic fallback semantics.
- Rationale: Directly matches FR-032 through FR-036 while staying non-production.
- Alternatives considered:
  - Text-only mode as final runtime: rejected because it does not satisfy voice-loop requirements.
  - Browser telephony integration in MVP: rejected as out-of-scope complexity.

## Decision 4: Persistence model
- Decision: Use file-backed JSON mock persistence with turn-boundary refresh and immediate write visibility.
- Rationale: Satisfies FR-029 and FR-031, keeps data editable for same-day testing.
- Alternatives considered:
  - In-memory store only: rejected because manual edits are not persisted.
  - Database-backed persistence: rejected due to non-production scope discipline.

## Decision 5: Verification and escalation thresholds
- Decision: Keep fixed thresholds of 2 unresolved clarifications and 3 verification failures before handoff.
- Rationale: Required by FR-004 and FR-007; deterministic behavior reduces caller confusion.
- Alternatives considered:
  - Per-flow custom thresholds: rejected as unnecessary complexity.
  - Unlimited retries: rejected due to poor caller experience.

## Decision 6: Validation method
- Decision: Use quickstart scenario walkthroughs as the baseline acceptance method, including explicit pass/fail evidence.
- Rationale: Aligns with plan/testing context while preserving simple, feature-focused validation.
- Alternatives considered:
  - Full production performance/load testing: rejected as outside MVP scope.
  - No scenario validation: rejected as insufficient confidence for branching behavior.

## Decision 7: Dual-mode user conversation support
- Decision: Keep voice-first interaction as primary while requiring a fully functional text-mode conversation loop for local operation and troubleshooting.
- Rationale: Preserves product direction while ensuring user-completable flows when voice environment is unavailable.
- Alternatives considered:
  - Voice-only implementation: rejected because it blocks practical local validation and user fallback.
  - Text-only fallback for debugging only: rejected because it leaves user-level acceptance untestable.

## Decision 8: Clarity feedback instrumentation
- Decision: Capture optional end-of-interaction clarity score (1-5) in both text and voice modes and include it in metrics output.
- Rationale: Provides measurable support for SC-006 while keeping user friction low (optional capture).
- Alternatives considered:
  - No direct feedback capture: rejected because SC-006 becomes unverifiable.
  - Mandatory feedback after every interaction: rejected due to poor user experience.
