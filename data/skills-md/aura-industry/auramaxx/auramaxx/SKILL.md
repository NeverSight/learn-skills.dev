---
name: auramaxx
description: Use when building or modifying AuraMaxx or AuraJS game projects. Helps agents infer game requirements from local project files, pick the right starter-owned edit points, and validate gameplay work with the current CLI and project wrapper commands.
---

# AuraMaxx Skill

Use this skill when working inside an AuraMaxx or AuraJS game project.

## Working Set

Read these files in order:

1. `project-requirements.md`
2. `starter-recipes.md`
3. `validation-checklist.md`
4. the current project files named by those docs

Use `https://www.aurajs.gg/llm.txt` only when you need broader public docs
context than the local project and installed package sources provide.

## Rules

- Treat the current project files as the primary source of truth.
- Keep `src/main.js` thin; prefer the registry-backed runtime flow already in the scaffold.
- Put durable authored data in `config/` or `content/`, not scene-local constants.
- Put mutable runtime state in scenes or `src/runtime/app-state.js`.
- Extend `src/starter-utils/` before inventing one-off helpers.
- Use `auramaxx make` instead of hand-wiring new scaffold nouns when a generator exists.

## Default Loop

1. Infer the current game requirements with `project-requirements.md`.
2. Choose the starter-specific edit path in `starter-recipes.md`.
3. Implement the smallest playable slice that changes one mechanic at a time.
4. Run the relevant checks from `validation-checklist.md`.

## Retrieval Boundary

Open local project files first. If you still need package-level behavior or
template intent, inspect:

- `node_modules/@auraindustry/aurajs/src/`
- `node_modules/@auraindustry/aurajs/templates/`

Use `aurajs.gg/llm.txt` after that, not before.
