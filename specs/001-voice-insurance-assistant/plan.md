# Implementation Plan: Voice-First Insurance Assistant

**Branch**: `001-voice-insurance-assistant` | **Date**: 2026-03-02 | **Spec**: [/home/rhuu/mygit/ai-prompter/specs/001-voice-insurance-assistant/spec.md](/home/rhuu/mygit/ai-prompter/specs/001-voice-insurance-assistant/spec.md)
**Input**: Feature specification from `/specs/001-voice-insurance-assistant/spec.md`

## Summary

Deliver a non-production, voice-first insurance assistant with full user-facing
conversation support in both voice and text modes, covering natural intake,
sensitive-flow verification, appointment/policy/compensation/callback requests,
deterministic fallback messaging (including handoff-unavailable paths), and
explicit human handoff with context summary.

## Technical Context

**Language/Version**: Python 3.11  
**Primary Dependencies**: OpenAI API SDK, Jinja2, Google Chirp-3 STT/TTS clients, local audio I/O libs  
**Storage**: File-backed JSON mock persistence (`data/mock/*.json`)  
**Testing**: Two-stage validation: Stage A text-eval contract checks (`evals/text/quickstart.md`) then Stage B runtime checks (`quickstart.md`) for text and voice loops  
**Target Platform**: Local development runtime (Linux/macOS terminal)  
**Project Type**: Single-process CLI voice-assistant prototype  
**Performance Goals**: Align with SC-008/SC-009 from spec (>=90% turn completion, <=8s start-of-playback in >=90% of turns)  
**Constraints**: Non-production scope, deterministic branching, mandatory handoff on defined thresholds, no payment processing  
**Scale/Scope**: One feature branch implementing five user-story groups in one assistant runtime, including optional caller-clarity feedback capture for metrics

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Pre-Design Gate Review

- [x] Business logic is primary; non-essential infrastructure is excluded.
- [x] Plan is understandable in one pass and uses the simplest viable design.
- [x] Voice journeys include clear branching and deterministic next steps.
- [x] Human handoff is explicit for unresolved or unsafe automation paths.
- [x] Non-production scope is preserved; deployment/hardening work is excluded unless requested.
- [x] Implementation-specific stack naming is explicitly stakeholder-requested for this feature scope.

Result: PASS

## Project Structure

### Documentation (this feature)

```text
specs/001-voice-insurance-assistant/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── evals/
│   └── text/
│       ├── quickstart.md
│       ├── quickstart-results.md
│       ├── metrics-summary.md
│       └── contracts/
├── contracts/
│   ├── voice-flow-contract.md
│   ├── prompt-template-contract.md
│   └── mock-persistence-contract.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── assistant/
    ├── app.py
    ├── config.py
    ├── constants.py
    ├── router.py
    ├── models.py
    ├── validation.py
    ├── handoff.py
    ├── metrics.py
    ├── guards.py
    ├── flows/
    ├── llm/
    ├── prompting/
    ├── runtime/
    ├── store/
    └── voice/

data/
└── mock/
    ├── callers.json
    ├── policies.json
    ├── plans.json
    ├── appointments.json
    ├── renewals.json
    ├── callbacks.json
    ├── compensations.json
    └── feedback.json

prompts/
scripts/
```

**Structure Decision**: Single-project Python CLI prototype with feature-focused
modules and file-backed mock data to keep behavior explicit and easy to validate.

## Phase 0: Outline & Research

1. Validate provider, fallback, and runtime assumptions against spec requirements.
2. Capture decisions and alternatives in `research.md`.
3. Confirm no unresolved technical context clarifications remain.

## Phase 1: Design & Contracts

1. Define entities, validation rules, and transitions in `data-model.md`.
2. Define voice interaction, handoff, and fallback interfaces in `contracts/voice-flow-contract.md`.
3. Define prompt rendering contract in `contracts/prompt-template-contract.md`.
4. Define editable mock persistence contract in `contracts/mock-persistence-contract.md`.
5. Define scenario-based validation in `quickstart.md`.
6. Define Stage A text-eval contract validation and evidence artifacts in `evals/text/`.
7. Update agent context using `.specify/scripts/bash/update-agent-context.sh codex`.

## Post-Design Constitution Re-Check

- [x] Business logic remains the primary artifact focus.
- [x] Flows and rules remain simple and understandable.
- [x] Voice branch handling and next-step messages are explicit.
- [x] Human handoff path includes required context summary.
- [x] No production deployment/hardening requirements were introduced.

Result: PASS

## Complexity Tracking

No constitution violations requiring justification.
