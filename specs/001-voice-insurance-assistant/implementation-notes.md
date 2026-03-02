# Implementation Notes

## Requirement Traceability

- FR-024: Explicit next steps are generated via `src/assistant/prompting/next_step_prompts.py` and fallback handlers.
- FR-029: File-backed mock persistence is implemented in `src/assistant/store/file_backend.py` with domain repositories.
- FR-030: Provider fallback behavior is implemented in `src/assistant/flows/fallback_flow.py` and `src/assistant/voice/chirp3_voice.py`.
- FR-031: Turn-boundary refresh and manual edit reflection are implemented in `src/assistant/store/store.py`.

## Local Runtime Notes

- Start app with `python -m src.assistant.app` for text mode or `python -m src.assistant.app --voice-loop` for live voice loop.
- The store reloads domain files at each turn boundary, so manual edits to files in `data/mock/` are read on next caller turn.
- Seed baseline data with `python scripts/seed_mock_data.py`.
