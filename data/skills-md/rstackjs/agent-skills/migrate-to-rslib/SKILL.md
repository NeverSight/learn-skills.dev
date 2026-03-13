---
name: migrate-to-rslib
description: Migrate tsc or tsup library projects to Rslib.
---

# Migrate to Rslib

## Goal

Migrate `tsc` and `tsup` projects to Rslib with minimal behavior changes and clear verification.

## Supported source frameworks

- tsc
- tsup

## Migration principles (must follow)

1. **Official guide first**: treat Rslib migration docs as source of truth.
2. **Smallest-change-first**: complete baseline migration first, then migrate advanced or custom behavior.
3. **Do not change business logic**: avoid touching source or business logic unless user explicitly asks.
4. **Validate before cleanup**: keep old tool dependencies/config temporarily if needed; remove only after Rslib is green.

## Workflow

1. **Detect source tool**
   - `tsup`
     - Config: `tsup.config.*`
     - Dependency: `tsup`
     - Build script: uses `tsup` to build projects
   - `tsc`
     - Config: `tsconfig.json` or `tsconfig.*.json`
     - Dependency: `typescript`
     - Build script: uses `tsc` to build projects. And it should be noted that `tsc` used only for type checking (e.g., `tsc --noEmit`) does not make it a `tsc` build project.

2. **Apply tool-specific migration deltas**
   - tsc: `references/tsc.md`
   - tsup: `references/tsup.md`

3. **Validate behavior**
   - Run build command to verify the project builds successfully.
   - If issues remain, compare the old project configuration with the migration guide and complete any missing mappings.

4. **Cleanup and summarize**
   - Remove obsolete dependencies/config only after validation passes.
   - Summarize changed files, mapped options, and any remaining manual follow-ups.
