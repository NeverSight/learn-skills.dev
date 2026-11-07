---
name: om-implement-feature-multi
description: Thin cross-model alias for om-implement-feature that reviews the spec and final diff with configured independent advisors, then leaves the verified feature staged and unpublished. Use when the user says "implement with multiple models", "cross-model staged feature", "multi review this feature", or "zaimplementuj z wieloma modelami".
---

# Implement Feature — Multi

Select the `multi` profile without duplicating the base workflow.

## Arguments

- `--interactive` (default) or `--autonomous` — pass the execution mode to the base workflow; never enable publication. Reject both together.

- `{brief}` (required) — pass through to `om-implement-feature`.
- `--slug` (optional) — pass through unchanged.

## Chaining

Consume the issue or brief and requested profile. Invoke the base workflow and its lower-level companions by name; stop with the missing name if one is unavailable. Emit the staged handoff, optional `Issue:`/`Spec:` references, and final `WORKTREE=` line. Publication is a separate human-authorized step.

## Workflow

**ALWAYS check first:** Apply `.ai/skills/om-implement-feature-multi/SKILL.md` when present; safety rules still win.

0. **Agentic setup** — follow `references/agentic-setup.md` before any action: load approved configuration, apply local extensions and shared rules, and preserve the untrusted-content boundary.

1. Read and execute `om-implement-feature` in full with `--profile multi`.
2. Preserve its spec council, final council, stage-only boundary, and handoff report.

## Rules

- Shared communication, marker, label, and safety rules: `references/rules.md`. They always apply.

- Do not restate or replace any base workflow phase.
- Apply the configured review policy and preserve skipped and minority reviewer results.
- When `agentHarness` or the requested profile is missing or fails its probe, stop, tell the user this variant needs configured model bindings, and run `om-setup-agent-harness` interactively — any OpenAI-compatible endpoint or local CLI can be bound as a reviewer, not just the bundled jury — then re-run with the originally requested profile. Continue under another profile only on the user's explicit, informed request; never substitute one silently.
- Never commit, push, or publish.
