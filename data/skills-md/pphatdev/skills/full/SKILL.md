---
name: full
description: Load this skill when the user asks for a complete task done end to end - design, implementation, documentation, tests, and e2e verification together. Do not load it for a separated single-phase request; the phase skills (design, implementation, documentation, test, e2e) own those.
user-invocable: true
---

# Full

Category: Design (Product) - Orchestration

## Purpose

Carry a complete task through every phase by composing the phase skills:
design, implementation, documentation, test, e2e. This skill routes and
sequences; the phase skills carry the expertise.

## Request validation (do this first)

Before any work, verify the request is valid. A valid request:

1. States a concrete goal - what will be true when the task is done.
2. Names or clearly implies its target (files, feature, area) so the work
   can start without inventing scope.
3. Spans multiple phases - it needs at least two of design, implementation,
   documentation, test, e2e.

If any check fails, stop and return an error message to the user naming
exactly what is missing or invalid. Do not guess scope, do not proceed on
an ambiguous request.

If the request is a separated single-phase task ("design X only", "write
tests for X", "document X"), do not use this skill - the phase skill
handles it. Say so and load that phase skill instead.

## When a composed skill is missing

If a skill this one needs is not available - the load fails or it is
absent from the session's skill list - do not improvise or continue
without it. Ask the user to install the skill, then retry, for example:

    npx skills add <owner>/agent-workflows-engineering --skill <name> -a <agent> -y

or copy the skill folder into the agent's skills directory (see the
README's Installation section), and reload the session.

## Workflow

Run the phases in order; each phase loads its skill and follows it.

1. **Design.** Load `brainstorming` when options must be generated,
   `research` when facts must be gathered, and `planning` to produce the
   executable plan with acceptance criteria. Do not start building before
   the plan states how it will be verified.
2. **Implementation.** Load `run` to execute the plan step by step,
   `coding-standards` before editing code, and `security-standards` when
   the change touches anything exposed to untrusted input. Load `debug`
   when a defect appears.
3. **Documentation.** Load `user-documentation` for end-user guides,
   `technical-documentation` for engineer-facing docs, or
   `api-documentation` when the change exposes an API.
4. **Test.** Load `test` to derive cases from the acceptance criteria,
   composing `unit-testing` and `integration-testing` for the chosen
   levels.
5. **E2E.** Load `e2e` to verify the complete user journeys through the
   real stack.
6. **Report.** Summarize per phase what was produced, what was verified
   and how, and what is not covered.

## Output

- A result per phase, each traceable to the plan's acceptance criteria.
- An honest final report including coverage gaps and assumptions.

## Anti-patterns

- Running every phase for a single-phase request - separated tasks go to
  the phase skills, not here.
- Skipping a phase silently - if a phase genuinely does not apply, say
  so in the report instead of dropping it.
- Proceeding past an invalid request instead of returning the error.

## Escalate when

- A phase's own escalation criteria fire (blast-radius actions, missing
  information) - surface them to the user before continuing.
