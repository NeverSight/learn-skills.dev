---
name: pd-design-lead
description: >-
  Use when a product-design request spans more than one discipline, when it's unclear which pd-* skill
  applies, when starting design work on a new project, or when running a design effort end-to-end
  (research through QA and handoff). Start here for any non-trivial design task.
metadata:
  team: product-design
  role: orchestrator
  version: "2.0.0"
---

# pd-design-lead — the design team's orchestrator

## Overview

The lead does no discipline work itself. It scopes the request, sets up the project profile if needed,
proposes the smallest pipeline that does the job, routes the work through the specialists, and keeps
`INDEX.md` current. Think of a design director assembling the right people — and only those — for the job.

## Before you start

Load `pd-foundations` and follow its working agreement. Then read `docs/design/PROJECT.md` (or the
repo's existing profile elsewhere). If it doesn't exist, create it with the user as described in
`project-profile.md` — infer what you can from the repo and the connected tools, ask only for what's
left, and confirm. Every specialist depends on it. Paths below are relative to `artifacts_dir`.

## When to use

- The request touches two or more disciplines ("design the onboarding flow").
- It's unclear which specialist applies.
- An end-to-end effort needs coordinating and tracking.

**Not for:** requests that map cleanly to one discipline. "Fix this error message" goes straight to
`pd-ux-writing`; the lead is for coordination, not ceremony.

## Process

0. **Check the session.** See which tools are actually connected and what this model can do here
   (`adaptation.md`), pick the adapter for the project's design tool (`tools/README.md`), and note
   fallbacks for anything missing. Update `capabilities` in `PROJECT.md`.
1. **Intake.** Pull the real requirement from the tracker named in `PROJECT.md` (`integrations.md`), or
   treat the user's message as the brief. Capture goal, constraints, acceptance criteria, and the unit of
   work: one element, one screen, a feature, or a system change.
2. **Check what exists.** Read `INDEX.md` and `LEARNINGS.md`. Reuse approved upstream artifacts instead
   of redoing them, and carry relevant learnings into the specialists' briefs. If
   `design_system.source` is `none` and no provisional system exists, plan `pd-design-system-ops` first,
   before any visual work.
3. **Plan and confirm.** Choose the specialists and order with `references/routing-playbook.md`. Present
   the plan — who runs, in what order, which artifact each writes, what you'll skip and why, and which
   checks the session can't perform — and wait for the user's agreement before routing anything.
4. **Route.** Run specialists in order. Give each one the exact paths (resolved through `INDEX.md`) to
   its input artifacts, and handle a missing input per `handoff-protocol.md`; give each the
   instruction to load `pd-foundations`. If your runtime can run subagents in parallel, run independent
   stages (writing ∥ visual) concurrently; otherwise run them in sequence.
5. **Track.** Add an `INDEX.md` row the moment each artifact is created and keep its status in sync with
   the artifact header. Check that each specialist read its inputs and wrote its output.
6. **Close.** For efforts that produce screens, mocks, or a built UI, run `pd-ux-qa` before calling
   anything done. For artifact-only efforts (research, architecture, flows), review each artifact against
   its skill's Common mistakes and `principles.md`, and have `pd-ux-qa` run a heuristic pass on flows
   when they exist. Make sure every flagged design-system gap
   reached `SYSTEM-BACKLOG.md`. Summarize what was produced, what's open, and what needs the user.
7. **Retro.** Group QA findings and user corrections by root cause and update `LEARNINGS.md` — add new
   rules, retire wrong ones. Note anything that looks like a flaw in a skill itself as a proposed upstream
   fix rather than editing installed skills (`adaptation.md`).

## The team

| Skill | Does |
|-------|------|
| `pd-ux-research` | Discovery, synthesis, personas, JTBD, opportunities |
| `pd-ux-architecture` | Content model, taxonomy, sitemap, navigation |
| `pd-ux-flows` | User flows, task flows, journey maps |
| `pd-ux-design` | Layout, interaction, screen specs, every state |
| `pd-ux-writing` | Microcopy, errors, voice and tone |
| `pd-visual-design` | Type, color, spacing, hierarchy through tokens |
| `pd-design-system` | Map the design to real system parts |
| `pd-design-system-ops` | Grow and guard the system; triage flagged gaps |
| `pd-mocks` | Build mocks in the project's design tool or in code |
| `pd-prototyping` | Interactive prototypes and motion |
| `pd-responsive` | Breakpoints, adaptive and cross-platform behavior |
| `pd-ux-qa` | Heuristic, accessibility, regulatory, and design-vs-spec QA |
| `pd-handoff` | Engineering-ready specs and token/component→code mapping |
| `pd-metrics` | Success metrics, instrumentation, impact |

Inputs, outputs, and call/skip guidance for each: `references/roster.md`.

## Default pipeline

`research → architecture → flows → design → (writing ∥ visual → design-system) → mocks → qa`

Skip architecture when the content and navigation structure exists and isn't changing. Add responsive,
prototyping, handoff, and metrics as the request needs. `pd-design-system-ops` runs as a side loop fed by
gaps flagged anywhere in the chain.

## Common mistakes

- Routing before the user has agreed to the plan.
- Running the full chain for a one-discipline request — pick the smallest pipeline that does the job.
- Skipping the profile, so specialists guess the toolchain and the domain.
- Planning from last session's tool list — a disconnected MCP turns into fabricated audit results.
- Closing without a retro, so the same correction has to be made again next time.
- Sending structure questions (taxonomy, sitemap, navigation) to `pd-ux-flows` instead of
  `pd-ux-architecture`.
- Jumping to mocks without the design, content, visual, and components artifacts they join.
- Letting `INDEX.md` drift from artifact headers, or letting flagged gaps die before they reach the
  backlog.
