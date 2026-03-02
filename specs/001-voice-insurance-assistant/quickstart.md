# Quickstart Validation: Voice-First Insurance Assistant

This is the canonical evaluation entry point for `001-voice-insurance-assistant`.

## Evaluation Flow (Required Order)

1. Execute **Stage A: text evaluation contract checks** (required before implementation changes are accepted).
2. Execute **Stage B: runtime behavior validation matrix** (required for app-ready milestones).

## Stage A: Text Evaluation Contract Checks (Primary)

Use these artifacts as the source of truth:

- Scenario execution spec: `evals/text/quickstart.md`
- Scenario/result contracts:
  - `evals/text/contracts/text-scenario-contract.md`
  - `evals/text/contracts/text-result-contract.md`
  - `evals/text/contracts/requirement-coverage-contract.md`
- Result ledger template: `evals/text/quickstart-results.md`
- Metrics template: `evals/text/metrics-summary.md`

Execution requirements:

1. Run scenarios in canonical order (`TXT-001` -> `TXT-004`).
2. Record status and assertion trace for every scenario (`PASS`, `FAIL`, `BLOCKED`).
3. Validate coverage and metrics formulas from contract rules.
4. Store run output in:
   - `evals/text/quickstart-results.md`
   - `evals/text/metrics-summary.md`

## Stage B: Runtime Behavior Validation Matrix (Implementation Gate)

Prerequisites:

- Read `spec.md`, `plan.md`, `research.md`, `data-model.md`, and all files in `contracts/`.
- Ensure mock data is seeded and editable in `data/mock/`.

Run commands:

```bash
python scripts/seed_mock_data.py
python -m src.assistant.app
python -m src.assistant.app --voice-loop
```

Runtime measurement protocol (for SC-008, SC-009, SC-010):

1. Execute at least 50 manual turns across at least 5 scenarios in this matrix.
2. Measure turn timing from end of caller input to start of assistant playback attempt.
3. Compute:
   - `voice_turn_completion_rate = completed_turns_without_restart / total_voice_turns`
   - `playback_within_8s_rate = turns_with_playback_start_le_8s / total_measured_turns`
   - `stt_fallback_determinism_rate = deterministic_repeat_or_handoff_stt_failures / total_stt_failures`
4. Record raw counts and computed rates in `metrics-summary.md`.
5. A Stage B pass requires thresholds from `SC-008`, `SC-009`, and `SC-010`.

Validate this matrix:

1. Natural intake with ambiguous first request resolves within clarification threshold.
2. Sensitive intent requires verification and escalates after 3 failures.
3. Appointment booking confirms or provides alternatives.
4. Update/cancel works when appointment ID is unknown via candidate matches.
5. Renewal + clinic eligibility conflict returns alternatives and next steps.
6. Compensation appeal with missing details returns checklist and next actions.
7. Callback intake succeeds with optional policy ID omitted.
8. Repeated misunderstanding triggers handoff with summary.
9. Template missing-variable path returns deterministic fallback text.
10. Voice output uses Chirp-3 profile, with explicit fallback behavior.
11. OpenAI path handles intent and next-step generation; unavailable provider triggers fallback messaging.
12. Manual edit to `data/mock/*.json` is visible on next turn.
13. Clarification/verification/provider fallback limits remain deterministic.
14. Local voice loop executes capture -> STT -> flow -> TTS playback.
15. Text mode executes multi-turn slot collection and completes at least one sensitive flow with verification.
16. Simulated handoff queue unavailability produces alternate next steps and callback offer; optional caller clarity feedback (1-5) is captured at interaction end.
17. Clarification prompts remain <= 18 words and explicit next-step prompts remain <= 30 words in sampled validation turns.

Record runtime evidence in:

- `quickstart-results.md`
- `metrics-summary.md`
