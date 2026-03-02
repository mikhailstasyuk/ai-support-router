# Mock Persistence Contract

## Scope

Domain files:
- callers
- policies
- plans
- appointments
- renewals
- callbacks
- compensations
- feedback

## Required Behavior

- Read latest domain data at each turn boundary.
- Persist writes from flow actions immediately.
- Reflect manual data-file edits on the next turn.
- Support create/update/delete behavior required by flows.

## Consistency Rules

- Record identifiers remain stable across linked domains.
- Required data-model fields must remain valid after writes.
- Invalid writes return explicit next-step guidance.

## Failure Behavior

- Persistence failure returns deterministic fallback text.
- Fallback includes immediate handoff offer option.

## Out of Scope

- Production database integration
- Distributed consistency guarantees
