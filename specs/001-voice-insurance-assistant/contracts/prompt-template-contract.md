# Prompt Template Contract (Jinja2)

## Engine Rules

- Templates use Jinja2.
- Named variables only.
- Missing required variables must route to explicit fallback messaging.

## Required Template Families

- `intent_clarification`
- `verification_prompt`
- `appointment_alternative_offer`
- `clinic_alternative_offer`
- `missing_information_next_steps`
- `handoff_summary`

## Variable and Safety Rules

- Field names must align with data model entities.
- Optional fields must have deterministic fallback wording.
- Sensitive values are excluded unless caller confirmation requires them.

## Rendering Contract

- One primary prompt render per turn.
- Output remains concise and caller-friendly.
- Template updates must preserve handoff and retry threshold behavior.
