# AI Support Router: Voice-First Insurance Assistant Prototype

## Requirements

- Python 3.11
- Optional API credentials (prototype also runs in deterministic fallback mode)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/seed_mock_data.py
```

## Run (Text Mode)

```bash
python -m src.assistant.app
```

or:

```bash
./scripts/run_local.sh
```

## Run (Local Voice Loop)

```bash
python -m src.assistant.app --voice-loop
```

Voice loop input behavior:
- Provide a `.wav` file path each turn.
- The app transcribes the `.wav` via Google STT and runs the normal assistant flow.
- Assistant returns text responses in the terminal.
- Slot parsing accepts spoken policy IDs like `p o l minus 101` and natural dates like `March 15th 2026`.

## Troubleshooting

- Reset deterministic mock data: `python scripts/seed_mock_data.py`
- If provider credentials are missing, the app uses deterministic fallback behavior.
- For real Google STT calls, ensure `GOOGLE_APPLICATION_CREDENTIALS` and `GOOGLE_CLOUD_PROJECT` are set.
- If runtime files become inconsistent after manual edits, reseed mock data and rerun.

## Local Voice Loop Behavior

- Turn path: audio input -> STT -> intent/flow handling -> TTS playback.
- In this prototype environment, typed input is accepted for predictable local simulation.
- STT fallback: one repeat prompt, then handoff offer.
- TTS fallback: deterministic fallback message preserving business outcome.

## Mock Data Editing During Runtime

- Data files are in `data/mock/*.json`.
- Store refreshes files at every turn boundary.
- Manual edits become visible on the next caller turn.

## Validation Artifacts

- Canonical validation entry point: `specs/001-voice-insurance-assistant/quickstart.md`
- Text-eval contract pipeline (Stage A): `specs/001-voice-insurance-assistant/evals/text/quickstart.md`
- Quickstart results: `specs/001-voice-insurance-assistant/quickstart-results.md`
- Metrics summary: `specs/001-voice-insurance-assistant/metrics-summary.md`
