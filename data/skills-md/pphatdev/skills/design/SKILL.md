---
name: design
description: Load this skill when the user asks for design work only - ideation, research, or an executable plan, without implementation. Composes brainstorming, research, and planning. Do not load it when implementation, testing, or documentation is also requested; the full skill owns complete tasks.
user-invocable: true
---

# Design

Category: Design (Product) - Orchestration

## Purpose

Produce the design for a request - options, findings, or a plan - and
stop there. This skill routes to the design-phase skills; it does not
implement.

## Request validation (do this first)

Before any work, verify the request is valid. A valid request:

1. States a concrete goal - what is being designed and why.
2. Is a design-only ask - the user wants the thinking, not the build.
3. Contains enough context to design against (constraints, target area),
   or the missing context can be discovered by reading the codebase.

If any check fails, stop and return an error message to the user naming
exactly what is missing or invalid. Do not guess, do not proceed.

If the request also asks for implementation, tests, or documentation, it
is a complete task - the `full` skill owns it, not this one.

## When a composed skill is missing

If a skill this one needs is not available - the load fails or it is
absent from the session's skill list - do not improvise or continue
without it. Ask the user to install the skill, then retry, for example:

    npx skills add <owner>/agent-workflows-engineering --skill <name> -a <agent> -y

or copy the skill folder into the agent's skills directory (see the
README's Installation section), and reload the session.

## Workflow

1. **Route by what the request needs:**
   - Open-ended "what should we do / give me options" - load
     `brainstorming`.
   - Facts needed before deciding (codebase behavior, external options,
     dependency evaluation) - load `research`.
   - A goal that must become a sequenced plan - load `planning`.
   Most real requests need research before planning; compose accordingly.
2. **Execute the design.** Follow the loaded skill's workflow fully.
3. **Stop at the boundary.** The deliverable is the design artifact
   (options with trade-offs, findings, or a plan with acceptance
   criteria). No code changes, no test authoring, no documentation
   files.
4. **Report.** State the deliverable, the options considered, the
   assumptions relied on, and what the next phase (implementation) would
   need.

## Output

- The design artifact the phase skills produce: options, findings, or a
  numbered plan with acceptance criteria and risks.

## Anti-patterns

- Implementing "just a small piece" - design-only means design-only.
- Designing without reading the relevant code or context - a plan built
  on an unexamined codebase is fiction.

## Escalate when

- The request cannot be designed without decisions only the user can
  make - return the open questions instead of choosing silently.
