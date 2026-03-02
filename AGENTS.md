# ai-prompter Agent Entry Point

Last updated: 2026-03-03

## Purpose
This file is the implementation entry point for agents working in this repo.
It defines execution order, boundaries, and where source-of-truth context lives.
Do not duplicate feature details here. Follow referenced artifacts.

## Source of Truth (Read First)
Use the active feature branch/spec directory first.

For `001-voice-insurance-assistant`, read in this order:
1. Constitution: `.specify/memory/constitution.md`
2. Feature spec: `specs/001-voice-insurance-assistant/spec.md`
3. Implementation plan: `specs/001-voice-insurance-assistant/plan.md`
4. Task backlog and sequence: `specs/001-voice-insurance-assistant/tasks.md`
5. Contracts: `specs/001-voice-insurance-assistant/contracts/`
6. Canonical validation entry point: `specs/001-voice-insurance-assistant/quickstart.md`
7. Text evaluation pipeline (Stage A, required before runtime matrix):
   - `specs/001-voice-insurance-assistant/evals/text/quickstart.md`
   - `specs/001-voice-insurance-assistant/evals/text/contracts/`
   - `specs/001-voice-insurance-assistant/evals/text/quickstart-results.md`
   - `specs/001-voice-insurance-assistant/evals/text/metrics-summary.md`
8. Research and assumptions: `specs/001-voice-insurance-assistant/research.md`
9. Data model: `specs/001-voice-insurance-assistant/data-model.md`

## Implementation Roadmap (Pointer-Only)
- Phase order and dependencies are defined in `tasks.md` under `Dependencies & Execution Order`.
- Build order is mandatory: Setup -> Foundational -> US1..US5 -> Polish -> Live Voice Runtime.
- For deliverable scope and acceptance, use `spec.md` Functional Requirements and Success Criteria.

## System Boundaries
- Non-production prototype only.
- Focus on business logic and deterministic voice flow behavior.
- Payment processing is out of scope.
- Human handoff is a first-class outcome.
- Use editable mock persistence as defined in contracts/spec.

## Current Stack (Do Not Expand Without Spec/Plan Update)
- Python 3.11
- OpenAI API (primary agent LLM)
- Jinja2 prompt templating
- Google Chirp-3 STT/TTS
- File-backed mock data persistence

## Agent Working Rules
- Before coding, load the source-of-truth files above in order.
- During coding, implement only tasks from `tasks.md` unless user approves scope change.
- If a task conflicts with constitution or spec, stop and resolve the spec/plan/tasks mismatch first.
- Validate in two stages: Stage A (`evals/text`) then Stage B (`quickstart.md` runtime matrix); record results in feature docs.
- Keep changes minimal, explicit, and traceable to task IDs.
- When setup, run commands, or user-facing behavior changes, update `README.md` in the same change.

## Change Control
- If scope, architecture, or behavior changes, update:
  - `spec.md` for requirements/outcomes
  - `plan.md` for design decisions
  - `tasks.md` for execution sequence
  - `contracts/` for interface behavior
  - `README.md` for developer/operator entry instructions
- Do not treat this file as a replacement for those artifacts.

## Quick Start for Implementers
1. Open `tasks.md` and pick the next unchecked task in dependency order.
2. Cross-check relevant requirement IDs in `spec.md`.
3. Cross-check behavior contract in `contracts/`.
4. Implement.
5. Validate with `quickstart.md`.
6. Document outcome in feature artifacts.

## Active Technologies
- Python 3.11 + OpenAI API SDK, Jinja2, Google Chirp-3 STT/TTS clients, local audio I/O libs (001-voice-insurance-assistant)
- File-backed JSON mock persistence (`data/mock/*.json`) (001-voice-insurance-assistant)
- Markdown specification artifacts (docs-only) for text evaluation pipeline support docs under `specs/001-voice-insurance-assistant/evals/text/`

## Recent Changes
- 001-voice-insurance-assistant: Added Python 3.11 + OpenAI API SDK, Jinja2, Google Chirp-3 STT/TTS clients, local audio I/O libs
- 001-voice-insurance-assistant: Added text-only evaluation pipeline support docs in `evals/text/` (scenario contracts, result schema, and coverage/metrics workflow)
- 001-voice-insurance-assistant: Improved voice/text slot extraction for spoken policy IDs (`p o l minus ###`) and natural-language dates (for example, `March 15th 2026`)
