---
name: clack
description: Build and maintain interactive Node.js/Bun CLIs with Clack (`@clack/prompts` and `@clack/core`). Use when an AI agent needs to design prompt flows, implement cancellation-safe input handling, add spinners/log/note UX, apply Clack best practices, or generate runnable examples aligned with official Clack docs.
---

# Clack CLI Skill

Implement robust, user-friendly CLI flows with Clack.

## Follow This Workflow

1. Identify the implementation target.
- Use `@clack/prompts` for most interactive CLI flows.
- Use `@clack/core` for low-level/custom prompt rendering and lifecycle control.

2. Load only the relevant references.
- Prompt-centric workflows: `references/prompts-api.md`
- Low-level/core extension work: `references/core-api.md`
- UX and reliability review: `references/best-practices.md`
- Pattern selection and scaffolding: `references/examples.md`
- Source links and freshness checks: `references/sources.md`
- If user asks for a starter file quickly, run `scripts/scaffold-clack.sh`.

3. Build a minimal runnable skeleton first.
- Include imports, `intro()`, flow logic, and `outro()`.
- Add install/run commands for the user's runtime.

4. Add prompts with explicit validation and cancellation paths.
- Validate every user-facing field that can fail constraints.
- Handle cancellation after each prompt result with `isCancel(...)` and `cancel(...)`.

5. Add UX support functions intentionally.
- Use `log.*` for structured feedback.
- Use `spinner()` for long-running single operations.
- Use `note()` for summaries and next actions.

6. For asynchronous multi-step work, use task-oriented patterns.
- Prefer clear status updates and concise task titles.
- Keep success/error messages short and actionable.

7. Finalize with a production-ready answer.
- Return complete runnable code (not fragments) unless user asks otherwise.
- Include quick verification steps.

## Bundled Resources

- `scripts/scaffold-clack.sh`
- Generate a starter CLI from curated templates in JS or TS.
- Usage: `bash scripts/scaffold-clack.sh <target-dir> [basic|spinner] [js|ts] [auto|npm|pnpm|yarn|bun]`

- `assets/templates/basic-cli.mjs`
- Baseline prompt flow with validation, cancellation handling, and summary note.

- `assets/templates/spinner-cli.mjs`
- Prompt flow plus spinner-driven execution pattern for longer operations.

- `assets/templates/basic-cli.ts`
- TypeScript variant of the baseline prompt flow.

- `assets/templates/spinner-cli.ts`
- TypeScript variant of the spinner flow.

## Non-Negotiable Rules

- Always include a cancellation-safe path.
- Never assume valid input; validate and explain fixups in-place.
- Use consistent tone in status and error messages.
- Keep prompt trees shallow; split complex flows into grouped steps.
- Prefer sensible defaults to reduce user typing and errors.

## Freshness Policy

- Treat Clack APIs as evolving.
- Use `references/sources.md` as the source-of-truth link map.
- If the user asks for the latest behavior or version-specific details, re-check the official docs before finalizing.
- If no web access is available, state that constraint explicitly and stick to documented APIs in this skill.
