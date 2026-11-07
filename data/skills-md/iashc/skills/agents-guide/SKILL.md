---
name: agents-guide
description: >-
  Create, update, review, shorten, migrate, and organize AGENTS.md and
  CLAUDE.md files. Use when the user asks to write a repository guide for
  coding agents, add or change project instructions, refresh outdated
  instructions, fix inaccurate setup/build/test guidance, split guidance for
  subprojects, packages, apps, or services into nested AGENTS.md files, or make
  existing AGENTS.md/CLAUDE.md content clearer and less noisy.
license: MIT
metadata:
  author: Ash Li
  version: '2026-06-08'
---

# Agents Guide

Maintain `AGENTS.md` and `CLAUDE.md` as concise onboarding documents for coding
agents. Treat `AGENTS.md` as the source of truth; when `CLAUDE.md` is needed,
make it a symlink to `AGENTS.md` instead of maintaining duplicate content.

## Principles

- Use the guide to onboard coding agents to the repository: explain WHAT the
  project is, WHY important parts exist, and HOW agents should work safely.
- Keep root guidance short and broadly applicable. Every line is loaded into
  many sessions, so remove anything that only matters for rare tasks.
- Prefer progressive disclosure. Put task-specific or subsystem-specific details
  in clearly named docs and point agents to them only when relevant.
- Prefer pointers to copies. Link to authoritative files, commands, or docs
  instead of pasting code snippets or generated inventories that will go stale.
- Do not make the guide do a formatter or linter's job. Name the deterministic
  tools and commands agents should run instead of restating all style rules.
- Treat guide changes as high leverage. Do not blindly auto-generate a large
  guide; derive each line from repository evidence or an explicit user request.

## Workflow

1. Classify the request:
   - Create or refresh a whole guide.
   - Add or change one project instruction.
   - Review, shorten, or remove noisy content.
   - Migrate between `CLAUDE.md` and `AGENTS.md`.
   - Split guidance across subprojects, packages, apps, or services.
2. Discover only the facts needed for the request:
   - Read existing `AGENTS.md` and `CLAUDE.md`.
   - Read relevant README files, package manifests, task runners, CI workflows,
     and nearby docs that define setup, build, lint, typecheck, and test
     commands.
   - Inspect the repository shape before deciding whether nested `AGENTS.md`
     files are warranted.
3. Choose the narrowest edit:
   - For a single project instruction, update the nearest applicable guide and
     avoid rewriting unrelated sections.
   - For a new guide, add only instructions explicitly requested by the user or
     strongly supported by repository evidence.
   - For repository-wide guidance, edit the root `AGENTS.md`.
   - For subproject-specific guidance, add or update the nearest nested
     `AGENTS.md` and keep the root guide focused on shared context.
4. Write concise guidance:
   - Include only stable context that helps agents act correctly across common
     tasks: project purpose, important directories, setup commands, verification
     commands, safety constraints, and PR/commit expectations.
   - Move long architecture, testing, deployment, schema, or policy details to
     separate docs and link to them with a brief "read when..." description.
   - Remove stale commands, duplicated content, tool-output dumps, broad
     behavioral patches, and code style rules already enforced by tools.
5. Validate before finishing:
   - Check that listed commands and paths exist or are explicitly documented
     project conventions.
   - Preserve explicit user instructions. If they conflict with repository
     facts, surface the conflict instead of silently overriding them.
   - For revisions, confirm the guide is clearer and more generally applicable
     than the version it replaces.

## Migration

Use `AGENTS.md` as the canonical file whenever both names are involved.

- If only `CLAUDE.md` exists, move its still-valid, broadly applicable content
  into `AGENTS.md`, then replace `CLAUDE.md` with a relative symlink to
  `AGENTS.md`.
- If both files exist, compare them first. Merge only useful, non-duplicative,
  still-valid `CLAUDE.md` content into `AGENTS.md`; then replace `CLAUDE.md`
  with a relative symlink to `AGENTS.md`.
- If `CLAUDE.md` is already a symlink, verify it points to the intended
  `AGENTS.md` and update only when the target is wrong.
- Do not keep two independent copies of the same guidance.
- Do not delete a regular `CLAUDE.md` until its relevant content has been
  preserved in `AGENTS.md`.

For files in the same directory, after preserving content and removing the
regular `CLAUDE.md`, create the symlink with:

```bash
ln -s AGENTS.md CLAUDE.md
```

## Writing Style

- Write `AGENTS.md` and `CLAUDE.md` content in English.
- Use imperative or direct rule form for project instructions.
- Prefer short bullets over paragraphs.
- Keep rationale out unless it changes how an agent should behave.
- Avoid explanatory prose, background narration, and broad behavioral advice.
- Avoid "always" and "never" unless the user explicitly requests them or
  repository evidence makes the rule necessary.

## Creating New Guides

- Do not create a filled-out template just because the file is missing.
- Infer the specific guidance from the user request and authoritative repository
  files. Ask only when the required guidance cannot be determined safely.
- Omit empty categories. For example, do not add a PR section unless the
  repository or user has PR guidance.
- Keep wording direct and instruction-shaped. Prefer "Run `vp run format` before
  finishing" over explanatory prose.
- If the only clear user request is one project instruction, create the smallest
  valid `AGENTS.md` containing that instruction instead of inventing project
  overview, development, verification, or convention sections.

## Review Checklist

Use this checklist when reviewing or compressing an existing guide:

- Keep only instructions that apply to most tasks in this directory scope.
- Move long or task-specific material behind references instead of loading it
  globally.
- Copy build, test, lint, and format commands from authoritative files.
- Delegate code style preferences to deterministic tools where possible.
- Align nested guide boundaries with real subprojects.
- Resolve conflicting instructions by user intent and directory specificity.
- For migrations, keep `AGENTS.md` canonical and make `CLAUDE.md` a symlink
  rather than a duplicate file.
