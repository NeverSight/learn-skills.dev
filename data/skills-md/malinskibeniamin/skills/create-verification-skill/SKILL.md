---
name: create-verification-skill
description: Create a project-local skill that launches, drives, observes, and cleans up the real app. Use when a repository lacks a repeatable way to prove UI, CLI, API, or service behavior.
---

# Create a verification skill

Generate one project-local verifier for the next agent to run cold. Use the repository's existing canonical skill root; otherwise default to `.agents/skills/verify-<app>/`. Never mirror the skill into several host-specific roots.

## Interview the repository

Discover before asking:

- **Surface:** primary user entrypoint and any secondary UI, CLI, API, mobile, desktop, or library surface.
- **Launch:** repository-native command, readiness signal, ports, environment, seed data, and authentication.
- **Drive:** existing Playwright, PTY, HTTP, debug, or application harness before a generic tool.
- **Observe:** screenshots, accessibility snapshots, transcripts, responses, logs, exit codes, and durable side effects.
- **Isolate:** per-run ports, profiles, data directories, and fixtures. Refuse to drive a shared human instance.

A checkout that cannot run is a blocker, not a basis for invented instructions. Report the exact failing prerequisite.

For agent-DX or worktree setup requests, use [the capability-gap and cold-start checks](references/agent-dx.md).

## Generate

Write `SKILL.md` with matching `name: verify-<app>` frontmatter and concrete **Launch**, **Doctor**, **Drive**, **Evidence**, and **Cleanup** sections:

- **Launch:** exact start and teardown commands plus an observable ready condition.
- **Doctor:** one read-only check for app identity, build, process or port ownership, data isolation, and auth.
- **Drive:** literal commands and stable handles from this repository. Prefer roles, accessible names, routes, prompt strings, and public APIs over coordinates or internals.
- **Evidence:** capture the action and resulting state. Verify side effects through a second public view. Mocks are allowed only at an existing production boundary.
- **Cleanup:** stop only processes and scratch state this run created. Never kill by process name. Evidence survives cleanup.

Document every bundled helper's invocation and make executable helpers executable.

## Seed the feature map

Create `features/README.md` and one file for each of the top 3-5 user-facing features. Start from [the feature-map example](references/feature-map-example/README.md), then replace every example with repository evidence. Each feature owns:

1. `Sub-features`
2. `How to get to it (user POV)`
3. `Driving it with <harness>`
4. `Gotchas`

Map every real entrypoint separately; verifying a convenient path does not cover another path.

## Prove the generated skill

Execute the generated skill end to end: launch, doctor, drive one mapped feature through the real user path, capture evidence, and clean up. After cleanup, confirm the evidence still exists and no created process or state remains. Repair instructions that fail and replay the entire path. An unexecuted verifier is a draft.

Point later drift audits to `/maintain-verification-skill` and normal feature work to `/dogfood`.
