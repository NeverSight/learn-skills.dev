---
name: migrate-to-rslint
description: Migrate ESLint or other linters to Rslint. Use when asked to replace ESLint flat config, lint scripts, VS Code ESLint settings, inline directives, rules, presets, plugins, or lint dependencies with Rslint equivalents.
---

<!-- cspell:words Rslint rslint -->

# Migrate to Rslint

## Goal

Migrate lint tooling to Rslint with minimal behavior changes and clear validation.

## Supported source linters

- ESLint flat config

## Migration principles (must follow)

1. **Official docs first**: treat Rslint docs as source of truth for CLI, config, inline directives, VS Code settings, rules, and presets.
2. **Smallest-change-first**: migrate package, command, config, and editor wiring before changing source files.
3. **Preserve lint intent**: keep supported rule severities/options where Rslint supports them; call out unsupported rules/plugins instead of silently dropping behavior.
4. **Do not rewrite inline directives by default**: Rslint supports `eslint-disable` and `rslint-disable`; replace prefixes only when the user asks.
5. **Validate before cleanup**: keep old linter dependencies/config until the Rslint command passes for the migrated scope, then remove obsolete linter-only artifacts.

## Workflow

1. **Detect source linter**
   - ESLint flat config: `eslint.config.*`, `eslint` dependency, or package scripts that run `eslint`.
   - If the source linter is not covered by a reference yet, inventory the current behavior and explain that no dedicated migration reference exists.

2. **Apply source-specific migration guide**
   - ESLint flat config: `references/eslint-flat-config.md`

3. **Validate behavior**
   - Run the migrated lint command.
   - If the project had a fix command, run the migrated fix command only when appropriate for the task.
   - Resolve config, rule, and editor-setting issues before removing legacy files.

4. **Cleanup and summarize**
   - Remove obsolete linter dependencies/config after Rslint is green.
   - Summarize changed files, migrated presets/plugins, unsupported gaps, and remaining manual follow-ups.
