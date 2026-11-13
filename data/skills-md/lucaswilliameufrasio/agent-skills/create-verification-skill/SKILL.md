---
name: create-verification-skill
description: >-
  Create or adapt a project-local skill that drives an application's real user
  workflows and captures evidence that they work. Use when an app lacks a
  repeatable agent-readable verification path, when setting up browser/CLI/API
  smoke workflows, or when a team wants a maintained feature map. Inspect and
  reuse the target repository's existing harness; do not assume Cursor, require
  Playwright, or install dependencies without approval.
---

# Create an application verification skill

Give future agents a project-specific, repeatable way to start the real app,
drive user-visible behavior, and preserve evidence. This complements unit and
integration tests: it proves a selected user journey through the running
application, not just that code compiles or a test-only endpoint responds.

## 1. Inspect the target repository

Read its `AGENTS.md` and equivalent agent instructions, README, package/build
configuration, test setup, local services, routes/commands, and existing skills.
Determine these facts from the checkout before writing instructions:

- **Surface:** what a user interacts with (web, desktop, CLI/TUI, API, mobile,
  library, or more than one)? Pick the primary surface and list others only if
  they need separate verification.
- **Launch:** the documented local command, required local dependencies, config
  references, seed data, and a reliable ready signal. Do not read or print
  resolved secrets. Never source production environment files.
- **Drive:** the existing way to exercise real behavior. Prefer repository-owned
  tests/helpers or installed tools. For web apps, reuse Playwright/Cypress or an
  enabled browser-control tool if present; do not add a browser framework just
  for this skill. For a CLI/TUI, use its supported invocation in an isolated
  process/PTY; for an API, use its real router and documented local client.
- **Observe:** what concrete output proves success: visible state, response,
  persisted data, emitted file/message, logs, exit status, or screenshot.
- **Isolate:** whether concurrent runs can use separate ports, data directories,
  profiles, and accounts. If not, document serialization or refuse concurrent
  driving; never commandeer a shared user session.

If the app cannot build or reach a usable local state, stop and report the exact
blocker instead of writing a verifier against an imagined setup. Do not create
or start paid, remote, staging, or production resources as a shortcut.

## 2. Choose a native location and name

Inspect how this repository's actual agent harness discovers project-local
skills. Put the generated skill there, using the existing naming/layout
convention. For OpenCode, prefer `.opencode/skills/verify-<app>/SKILL.md` when
that is the repository's active convention. Do not create `.cursor/skills/`
unless Cursor is actually the target harness. If multiple harnesses are
maintained, choose the owner's canonical shared location and explain how each
one discovers it; do not duplicate copies that can drift.

Use `verify-<app>` for the skill directory and frontmatter `name`, with a
description naming the actual app/surface and when an agent should invoke it.
Create no placeholders: every command, selector, route, path, and ready signal
must come from repository evidence. Keep the skill self-contained enough for a
fresh agent who has not seen the setup conversation.

## 3. Write the project-local verifier

Include these sections in the generated `SKILL.md`:

- **Launch:** exact command, prerequisites, readiness check, and teardown. The
  start path must reach a usable app from the documented local state, not merely
  a process that opened a port. Keep configuration values secret-free.
- **Preflight:** one read-only check that confirms the expected build/version,
  process/port ownership, and usable local state before driving. If it fails,
  diagnose rather than steering an unknown or stale instance.
- **Drive:** concrete commands and stable selectors/handles from this project.
  For browser UI, prefer roles, accessible names, labels, and stable test IDs
  over coordinates. Use Playwright only if it is already available or the user
  explicitly approves adding it.
- **Evidence:** state where artifacts go and what is sufficient proof. Exercise
  the normal user path, capture an action and its resulting state, and verify
  relevant side effects (for example persisted data) as well as the screen.
  Test-only shortcuts may supplement but must not replace the user journey.
- **Isolation and cleanup:** name resources the verifier itself creates and
  remove only those. Never kill by process name or clean up neighboring services.
  Preserve evidence after teardown. If the app cannot safely run twice, say so
  and serialize runs.
- **Failure handling:** distinguish an app defect from missing setup, stale
  process, unavailable tool, and blocked external dependency. Record the actual
  error and do not weaken the journey to make it pass.

Also create `features/README.md` plus one file for each of the three to five
highest-value user-facing features supported by repository evidence. Each
feature file should explain what the user can do, how to reach it, how to drive
it with this harness, and the observable end state that proves it works. Note
known preconditions and gotchas. Do not claim comprehensive coverage when only
some journeys are mapped.

## 4. Prove one journey and hand off honestly

Run the generated instructions end to end for one mapped feature: launch,
preflight, drive, capture evidence, clean up, then confirm the evidence still
exists. Use only local/test-scoped data and the repository's documented safe
commands. Do not perform external side effects (payments, email, notifications,
deploys, or production writes). If a safe end-to-end pass needs new tools,
services, credentials, or permission, stop at that boundary and report what
remains unverified; a written plan is not a completed proof.

Report the exact journey and result, artifact location, cleanup, known gaps, and
which checks were not run. Point to the project's existing maintenance workflow
or explain that the feature map should be updated when routes, commands,
selectors, or user-visible behavior change. Do not promise that creating a skill
automatically makes every agent invoke it.
