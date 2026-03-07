---
name: coding-router
description: "Compatibility entry skill for plan-first coding work in OpenClaw."
metadata: {"openclaw":{"emoji":"💻","requires":{"bins":["gh"],"anyBins":["codex","claude"],"env":[]}}}
---

# Coding Router Skill 💻

This file exists for backward compatibility with single-entry skill setups (for example `/coding`).
Canonical sibling skills live at:

- `skills/plan-issue/SKILL.md`
- `skills/coding-agent/SKILL.md`

## Routing Rules

1. If user asks to plan/scope/estimate/design, follow `plan-issue` behavior.
2. For non-trivial implementation requests, produce a plan first and wait for exact `APPROVE` before any writes.
3. Only after `APPROVE`, follow `coding-agent` behavior with ACP-aware execution routing and CLI fallback.

## Command Routing (Channel Aliases)

When invoked via channel aliases:

- `/coding` → use this compatibility skill as router.
- `/plan` → route directly to `plan-issue` behavior.
- `/plan-review` → route to plan review flow using `scripts/plan-review`.
- `/plan-review-live` → route to interactive plan review checkpoints using `scripts/plan-review-live` (Lobster in-repo workflow first, legacy fallback).
- `/review_pr` → route to review flow using `references/reviews.md`.

## Runtime Status Contract

When wrappers are used for planning/review:
- Emit `RUN_EVENT start` at run start.
- If the run exceeds 30s, emit `RUN_EVENT heartbeat` every 20s.
- If interrupted or timed out, emit `RUN_EVENT interrupted` immediately with exit code.
- On non-interruption failure, emit `RUN_EVENT failed`.
- On success, emit `RUN_EVENT done`.

## Known ACP Runtime Limitation

Issue #43 (upstream) may affect spawned ACP run observability and browser relay
profile alias mapping. Use repo-side mitigations and bounded fallback guidance in:
- `references/acp-troubleshooting.md`

## Non-Negotiable Gates

1. Never write files, install packages, commit, or open PRs before explicit `APPROVE`.
2. Never default to bypass flags (`--yolo`, `--dangerously-skip-permissions`).
3. Use bypass flags only when the user explicitly asks to bypass approvals.
