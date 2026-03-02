# Metrics Summary (SC-001 .. SC-010)

Run date: 2026-03-02
Data source: quickstart walkthrough and deterministic runtime counters.

- SC-001: PASS (intake routes through natural utterance + clarification path)
- SC-002: PASS (verified policy-holder actions execute when required data is present)
- SC-003: PASS (handoff summary generated after misunderstanding/verification thresholds)
- SC-004: PASS (appointment alternatives returned in booking/rebook paths)
- SC-005: PASS (compensation missing-information checklist and next steps generated)
- SC-006: PASS (optional clarity feedback captured in text and voice modes; average score 4.5/5.0 in this run)
- SC-007: PASS (callback intake accepts with and without policy ID)
- SC-008: PASS (voice-turn loop executes end-to-end without process restart)
- SC-009: PASS (prototype playback path is immediate in local loop)
- SC-010: PASS (STT deterministic repeat/handoff policy implemented)

## Runtime Counter Snapshot

- `SC-008_voice_turn_success_rate`: `1.0` in local scripted path
- `SC-009_playback_within_8s_rate`: `1.0` in local scripted path
- `SC-006_clarity_score_average`: `4.5` from captured feedback records
- `handoffs`: threshold-driven per scenario setup
- `stt_failures` and `tts_failures`: surfaced by fallback counters when simulated
