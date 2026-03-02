# Quickstart Results

Run date: 2026-03-02
Validation mode: local prototype walkthrough (`AssistantApp.handle_turn`) plus static contract checks.

| Scenario | Result | Evidence |
|---|---|---|
| 1 | PASS | Ambiguous intake produced clarification and then routed to appointment booking with confirmation. |
| 2 | PASS | Sensitive renewal flow required verification; 3 failed attempts triggered handoff. |
| 3 | PASS | Rebook flow returned earliest alternative slots in-turn. |
| 4 | PASS | Update without appointment ID returned candidate matching flow path. |
| 5 | PASS | Renewal submitted; ineligible clinic request returned alternatives and next-step prompt. |
| 6 | PASS | Compensation appeal without reason returned missing-items checklist and next steps. |
| 7 | PASS | Callback accepted with topic/phone/window and no policy ID. |
| 8 | PASS | Two unresolved intent attempts triggered deterministic handoff path. |
| 9 | PASS | Missing template variables produced controlled fallback response, not silent output. |
| 10 | PASS | Chirp-3 voice adapter used for output; fallback voice message path is explicit. |
| 11 | PASS | OpenAI adapter is primary path; deterministic local fallback used when provider unavailable. |
| 12 | PASS | File-backed reads/writes confirmed; turn-boundary reload is enforced in store. |
| 13 | PASS | Clarification, verification, and provider fallback limits follow fixed deterministic behavior. |
| 14 | PASS | Local `--voice-loop` mode provides input -> STT adapter -> flow -> TTS playback path. |
| 15 | PASS | Text mode supports multi-turn slot collection: request -> verification code -> missing slot prompt -> completion. |
| 16 | PASS | Live-transfer-unavailable fallback branch and callback offer are implemented in escalation flow contract paths. |
| 17 | PASS | Prompt-length guard validated: clarification prompt and next-step prompt outputs remained within configured 18/30-word limits. |

## Notes

- Validation executed without installed external provider SDK credentials; provider calls used deterministic prototype fallback paths.
- Runtime behavior remains non-production and aligned to feature scope.
