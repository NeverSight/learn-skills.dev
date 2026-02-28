---
name: sweepi
description: Runs Sweepi and resolves lint violations using Sweepit rule docs. Trigger when asked to run Sweepi, when linting (or asked to lint), and before proposing commits.
---

# Sweepi Skill

Lint-fix safety workflow and reporting.

## When to run

Run this skill when:

1. The user explicitly asks to run `sweepi`.
2. You are about to commit or recommend committing code changes.
3. You are linting code, or the user asks you to lint code.

## Execution workflow

1. Run in this order:
   - First try global CLI: `sweepi .`
   - If `sweepi` is not found, fallback to: `npx sweepi .`
2. Parse all reported issues.
3. Before making edits, follow the required pre-edit gate in local `AGENTS.md`.
4. For each rule violation, open the rule docs in `./rules/<rule-id>.md` alongside this `SKILL.md`.
   - If one does not exist locally, try:
     - `https://raw.githubusercontent.com/eslint/refs/heads/main/lib/rules/<rule-id>.js`
     - `https://raw.githubusercontent.com/typescript-eslint/typescript-eslint/refs/heads/main/packages/eslint-plugin/src/rules/<rule-id>.ts`
     - `https://raw.githubusercontent.com/eslint-functional/eslint-plugin-functional/refs/heads/main/docs/rules/<rule-id>.md`
     - `https://raw.githubusercontent.com/jsx-eslint/eslint-plugin-react/refs/heads/master/docs/rules/<rule-id>.md`
5. Apply fixes that match documented rule intent, not just a minimal syntax pass.
6. Re-run `sweepi` until issues are resolved (or document blockers if resolution is impossible).

## Boundaries

Use `AGENTS.md` for:

- Hard-gate pre-edit analysis format
- Non-negotiable constraints
- Conflict resolution order
- Required post-edit report format
