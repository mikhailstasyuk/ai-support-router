<!--
Sync Impact Report
- Version change: N/A (template) -> 1.0.0
- Modified principles:
  - PRINCIPLE_1_NAME -> I. Business Logic First
  - PRINCIPLE_2_NAME -> II. Simplicity Is Mandatory
  - PRINCIPLE_3_NAME -> III. Voice Journey Clarity
  - PRINCIPLE_4_NAME -> IV. Human Handoff Safety Net
  - PRINCIPLE_5_NAME -> V. Non-Production Scope Discipline
- Added sections: None
- Removed sections: None
- Templates requiring updates:
  - ✅ updated: .specify/templates/plan-template.md
  - ✅ updated: .specify/templates/spec-template.md
  - ✅ updated: .specify/templates/tasks-template.md
  - ⚠ pending (not present): .specify/templates/commands/*.md
- Follow-up TODOs:
  - None
-->
# AI Prompter Constitution

## Core Principles

### I. Business Logic First
All feature work MUST prioritize user-visible business behavior and decision rules.
Implementation mechanics MAY be documented only when needed to clarify business
outcomes. Proposals that are mostly infrastructure and not tied to a user flow
MUST be rejected or deferred.
Rationale: The project goal is to model service behavior clearly, not to
optimize system engineering concerns.

### II. Simplicity Is Mandatory
Specifications, plans, and tasks MUST be understandable by non-specialists in
one reading pass. Any design that introduces unnecessary layers, abstractions,
or optional paths MUST be simplified before approval.
Rationale: Simple artifacts reduce ambiguity and speed up iteration.

### III. Voice Journey Clarity
Voice-first features MUST define clear caller journeys, concise clarification
questions, and deterministic next steps for unresolved requests. Every flow
MUST explicitly describe what the caller hears at success, partial success,
and failure points.
Rationale: Voice interactions fail without short, explicit branching and
caller guidance.

### IV. Human Handoff Safety Net
Human handoff MUST be treated as a first-class completion path. If automation
cannot safely complete a request, the system MUST transfer with a concise
context summary instead of forcing repeated retries.
Rationale: Service continuity and caller trust require graceful escalation.

### V. Non-Production Scope Discipline
This project MUST remain non-production by default. Artifacts MUST NOT require
deployment architecture, operational hardening, or enterprise-grade compliance
unless explicitly requested for a specific feature. Out-of-scope production
work MUST be recorded as deferred.
Rationale: The user intends a learning/prototyping workflow focused on business
logic rather than deployable systems.

## Project Constraints

- Outputs MUST stay implementation-agnostic unless the task explicitly requests
  technical internals.
- Payment processing is out of scope unless a feature explicitly reintroduces
  it.
- Performance and reliability targets SHOULD be expressed as user outcomes,
  not infrastructure metrics.
- Assumptions MUST be documented when requirements are incomplete.

## Workflow & Quality Gates

- Every spec MUST include: prioritized user scenarios, edge cases, functional
  requirements, measurable success criteria, key entities when data is involved,
  and assumptions/dependencies.
- Every plan MUST pass a Constitution Check before design work proceeds.
- Every task list MUST map tasks to user stories and preserve independent
  testability of each story.
- Compliance review is required at spec completion and again before task
  generation.

## Governance

This constitution supersedes local workflow preferences for this repository.
Amendments require:

1. A documented rationale and impact summary.
2. Updates to affected templates and guidance documents in the same change.
3. A semantic version update using the policy below.

Versioning policy:

- MAJOR: Backward-incompatible governance changes or principle removals.
- MINOR: New principle/section or materially expanded mandatory guidance.
- PATCH: Clarifications, wording improvements, and non-semantic refinements.

Compliance expectations:

- Reviewers MUST verify Constitution Check gates in generated plans.
- Specs and tasks that violate core principles MUST be corrected before
  progression to `/speckit.plan` or `/speckit.tasks`.

**Version**: 1.0.0 | **Ratified**: 2026-03-02 | **Last Amended**: 2026-03-02
