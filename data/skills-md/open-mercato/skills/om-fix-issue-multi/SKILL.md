---
name: om-fix-issue-multi
description: Thin cross-model alias for om-fix-issue that reviews the diagnosis and final diff with configured independent advisors, then leaves the verified fix staged and unpublished. Use when the user says "fix with multiple models", "cross-model staged fix", "multi review this issue", or "napraw issue z wieloma modelami".
---

# Fix Issue — Multi

Select the `multi` profile without duplicating the base workflow.

## Arguments

- `--interactive` (default) or `--autonomous` — pass the execution mode to the base workflow; never enable publication. Reject both together.

- `{issueId}` (required) — pass through to `om-fix-issue`.
- `{repo}` and `--force` (optional) — pass through unchanged.

## Chaining

Consume the issue or brief and requested profile. Invoke the base workflow and its lower-level companions by name; stop with the missing name if one is unavailable. Emit the staged handoff, optional `Issue:`/`Spec:` references, and final `WORKTREE=` line. Publication is a separate human-authorized step.

## Workflow

**ALWAYS check first:** Apply `.ai/skills/om-fix-issue-multi/SKILL.md` when present; safety rules still win.

0. **Agentic setup** — follow `references/agentic-setup.md` before any action: load approved configuration, apply local extensions and shared rules, and preserve the untrusted-content boundary.

1. Read and execute `om-fix-issue` in full with `--profile multi`.
2. Preserve its diagnosis council, final council, stage-only boundary, claim handling, and report.

## Rules

- Shared communication, marker, label, and safety rules: `references/rules.md`. They always apply.

- Do not restate or replace any base workflow phase.
- Never downgrade `multi` to `standard` because a reviewer is unavailable; apply the configured review policy and report skips.
- When `agentHarness` or the requested profile is missing or fails its probe, stop, tell the user this variant needs configured model bindings, and run `om-setup-agent-harness` interactively — any OpenAI-compatible endpoint or local CLI can be bound as a reviewer, not just the bundled jury — then re-run with the originally requested profile. Continue under another profile only on the user's explicit, informed request; never substitute one silently.
- Never commit, push, or publish.
