# Contract: Text Scenario Authoring

## Purpose
Define required structure for authoring reproducible text-only evaluation scenarios.

## Required Scenario Fields

Each scenario MUST include:
- `scenario_id`
- `title`
- `preconditions`
- `turn_inputs`
- `expected_outcomes`
- `assertions`
- `requirement_refs`
- `execution_order`

## Field Constraints

- `turn_inputs` MUST list caller text inputs in exact order for execution.
- `expected_outcomes` MUST describe observable branch outcomes only.
- `assertions` MUST be objective checks with stable assertion IDs (`A1`, `A2`, ...).
- `execution_order` MUST be unique per scenario within a run profile.

## Authoring Rules

- Turn inputs MUST be ordered and executable as written.
- Expected outcomes MUST be stated as observable behaviors.
- Assertions MUST be objective checks (not subjective quality statements).
- Preconditions MUST include reset and data-state requirements where relevant.
- Ambiguous input handling MUST include explicit expected clarification or fallback paths.

## Scope Rules

- Scenarios in this feature are text-only.
- Voice-evaluation steps are excluded from execution in this contract.
