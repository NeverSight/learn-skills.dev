---
name: om-implement-feature-optimized
description: Thin worker-optimized alias for om-implement-feature that delegates bounded implementation packets to configured models, then leaves the verified feature staged and unpublished. Use when the user says "optimized feature build", "use model workers", "cheap staged feature", or "zaimplementuj przez workerów".
---

# Implement Feature — Optimized

Select the `optimized` profile without duplicating the base workflow.

## Arguments

- `--interactive` (default) or `--autonomous` — pass the execution mode to the base workflow; never enable publication. Reject both together.

- `{brief}` (required) — pass through to `om-implement-feature`.
- `--slug` (optional) — pass through unchanged.

## Chaining

Consume the issue or brief and requested profile. Invoke the base workflow and its lower-level companions by name; stop with the missing name if one is unavailable. Emit the staged handoff, optional `Issue:`/`Spec:` references, and final `WORKTREE=` line. Publication is a separate human-authorized step.

## Workflow

**ALWAYS check first:** Apply `.ai/skills/om-implement-feature-optimized/SKILL.md` when present; safety rules still win.

0. **Agentic setup** — follow `references/agentic-setup.md` before any action: load approved configuration, apply local extensions and shared rules, and preserve the untrusted-content boundary.

1. Read and execute `om-implement-feature` in full with `--profile optimized`.
2. Preserve its packet boundaries, host integration, validation, stage-only boundary, and handoff report.

## Rules

- Shared communication, marker, label, and safety rules: `references/rules.md`. They always apply.

- Do not restate or replace any base workflow phase.
- If no selected worker is ready, the runtime `probe` exits non-zero and the run is blocked: stop, report the failed probe, and never silently downgrade to host-only implementation.
- When `agentHarness` or the requested profile is missing or fails its probe, stop, tell the user this variant needs configured model bindings, and run `om-setup-agent-harness` interactively — an optimized profile needs an audited implementation worker; adding a reviewer alone cannot unblock it — then re-run with the originally requested profile. Continue under another profile only on the user's explicit, informed request; never substitute one silently.
- Never commit, push, or publish.
