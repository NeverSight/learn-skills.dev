---
name: develop-pyrevit-extensions
description: Build, plan, review, and document pyRevit extensions. Use when Codex needs the pyRevit development workflow, templates, prompts, checklists, or scripts for creating or updating pyRevit commands in this repo. Pair with a version-specific Revit skill (e.g., 2023/2024/2025) for API constraints.
---

# Develop pyRevit Extensions

Use this skill to navigate the pyRevit knowledge base, planning workflow, and reusable assets in this repo.

## Quick Start
- Open `references/docs_overview.md` for the index.
- For setup and first-button walkthroughs, read `CodexWorkspace/human/README.md`.
- For the full dual-model workflow, read `references/agent_ai_orchestrated_dev_methodology.md`.

## Versioned Guidance
- For version-specific API patterns and constraints, use the appropriate `pyrevit-revit-20xx` skill in `CodexWorkspace/skills/`.
- Use the related pyRevit notes in `references/pyrevit_overview.md` when scaffolding a new command.

## Planning + Prompts
- Copy planning templates from `assets/templates/` into `CodexWorkspace/workspace/`.
- Use prompts from `assets/prompts/` as instructed in `references/prompts_overview.md`.

## Scripts + Checklists
- Start new commands from `scripts/new_command_template.py`.
- Use `references/checklists_overview.md` before reviews and merges.

## Workspace
- Project-specific artifacts live in `CodexWorkspace/workspace/` (plans, tasks, reviews, development.md, backlog.md).
- Edit workspace copies only; keep skill references and assets static.
