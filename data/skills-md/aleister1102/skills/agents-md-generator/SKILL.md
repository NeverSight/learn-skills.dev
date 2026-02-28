---
name: agents-md-generator
description: Generate or update AGENTS.md files for any repository, including migration from CLAUDE.md/COPILOT.md and monorepo-aware nested AGENTS.md placement. Use when creating, refreshing, or standardizing agent instructions from repo signals (manifests, scripts, CI, docs).
---

# AGENTS.md Generator

Create, update, and migrate `AGENTS.md` files using repo signals and a scaffold script. Supports monorepos (nested files take precedence by directory proximity). If the file grows unwieldy, hand off to `agent-md-refactor` for progressive disclosure.

## Quick Start
- Inspect repo facts (manifests, CI, scripts), then run the scaffold script without writing: `python agents-md-generator/scripts/scaffold_agents_md.py --repo-root . > /tmp/AGENTS.md`
- Fill TODOs, verify commands, then write: `python agents-md-generator/scripts/scaffold_agents_md.py --repo-root . --write --output AGENTS.md --force`
- For monorepos, place nested `AGENTS.md` alongside each package; nearest file wins.

## When to Use
- No `AGENTS.md` exists and you need a fresh one.
- Migrating from `CLAUDE.md`, `COPILOT.md`, or similar files.
- Monorepo needs per-package instructions with directory-precedence behavior.
- Existing `AGENTS.md` is stale after commands/tests/CI changed.

## Workflow
1) Gather truth: package manager, scripts, CI workflows, README/CONTRIBUTING, Makefile, common entrypoints.
2) Choose placement: root for repo-wide rules; add nested `AGENTS.md` for packages so nearest file applies.
3) Generate draft: run scaffold script (stdout by default). Use `--mode standard|minimal|comprehensive` if needed.
4) Fill TODOs and verify commands are the ones you want agents to run; trim anything irrelevant.
5) Write file with `--write` (add `--force` to overwrite). Keep diffs focused.
6) Migration (if legacy files found): rename legacy file to `AGENTS.md`, optionally add symlink aliases, and re-run scaffold to refresh content.

## Script Reference
- Script: `agents-md-generator/scripts/scaffold_agents_md.py`
- Defaults: stdlib-only; reads repo signals; prints Markdown to stdout.
- Flags:
  - `--repo-root PATH` (default `.`)
  - `--mode standard|minimal|comprehensive` (default `standard`)
  - `--write` to create/overwrite `--output` (default `AGENTS.md`)
  - `--force` required to overwrite existing files when `--write`
  - `--output PATH` to change target filename
- Safety: without `--write` never modifies disk; with `--write` refuses to clobber unless `--force`.

## Migration Guidance
- Rename legacy files: `mv CLAUDE.md AGENTS.md` (or similar), then re-run scaffold with `--force` to refresh sections.
- Optional symlinks for compatibility: `ln -s AGENTS.md CLAUDE.md` (only if desired by tooling).
- Remove obsolete references to old filenames in READMEs/CI after migration.

## Quality Bar
- Keep it scannable (1–2 pages standard). Prefer runnable commands over prose.
- No secrets; prefer env var placeholders (e.g., `API_TOKEN`), not values.
- Commands must be the ones agents should actually run (install, dev, build, test, lint/typecheck).
- For monorepos, mention where nested `AGENTS.md` live and how precedence works.

## References
- `references/agents_md_spec.md`: key rules from agents.md (precedence, migration, formatting flexibility).
- `references/repo_detection_heuristics.md`: where to look for install/build/test commands when heuristics are unsure.
- `assets/templates/agents.standard.md`: base template the script fills; edit if house style changes.
