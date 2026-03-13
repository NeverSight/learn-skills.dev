---
name: codex-claudeception-migration
description: Use when migrating Claude-style skill consolidation workflows into Codex; covers .claude/skills, hooks, and command-template adaptation into AGENTS.md + skills/ structure.
---

# Skill: codex-claudeception-migration

## When to use
- The repository already contains `.claude/skills` or Claude-specific instructions and must be migrated to Codex.
- The team wants to preserve post-task review -> skill extraction, without depending on Claude hooks.
- You need an MVP first (directories + docs + manual flow) before adding automation.

## Inputs
- Existing Claudeception assets (README, SKILL files, templates, scripts)
- Target Codex constraints (writable paths, AGENTS rules, available tools)
- Migration scope (MVP only or full migration)

## Steps
1. Identify non-portable parts: Claude hooks, Claude-specific tool names, Claude command entrypoints.
2. Map structure: `.claude/skills/*` -> `skills/*`; templates -> `docs/` or `scripts/`.
3. Add mandatory post-task review and quality gates in `AGENTS.md`.
4. Standardize skill format with frontmatter + when/steps/validation/anti-patterns.
5. Create one real migrated skill and validate usability before investing in automation.

## Validation
- Checkpoint 1: project includes `AGENTS.md`, `skills/skill-template.md`, and migration checklist docs.
- Checkpoint 2: at least one formal skill exists at `skills/<topic>/SKILL.md`.
- Checkpoint 3: that skill has explicit triggers, executable steps, and observable verification points.
- Checkpoint 4: later tasks can retrieve and reuse the skill by scenario match.

## Anti-patterns
- Copying Claude hook config without Codex-executable replacement.
- Overly generic descriptions that cannot be matched by keyword/semantics.
- Extracting one-off experience as a skill with no reuse value.
- Implementing complex automation before validating examples.

## Example
- Scenario: migrate Claudeception into Codex by building `codexception` first.
- Output: directory scaffold, AGENTS review rules, migration checklist, and one formal migration skill.
- Outcome: team can start manual consolidation now and automate later.

