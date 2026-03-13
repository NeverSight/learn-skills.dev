---
name: generate
description: Run code generation for Isar models, JSON serialization, and i18n
argument-hint: "[type]"
disable-model-invocation: true
allowed-tools: Bash(melos *), Bash(flutter pub run *)
---

Run code generation for the Keychat project.

## Arguments
- `$ARGUMENTS` - Optional: type of generation (all, dart, flutter, intl, runner)

## Generation Commands

| Type | Command | Description |
|------|---------|-------------|
| all | `melos run generate:all` | Run all code generators |
| dart | `melos run generate:dart` | Dart package generators only |
| flutter | `melos run generate:flutter` | Flutter package generators only |
| intl | `melos run intl:generate` | Internationalization strings |
| runner | `melos run build:runner` | App build_runner only |

## Common scenarios

### After modifying Isar model files
Run `melos run build:runner` to regenerate database schemas.

### After adding new translations
Run `melos run intl:generate` to regenerate localization files.

### After modifying any model with @JsonSerializable
Run `melos run generate:all` to regenerate JSON serialization code.

## Workflow

1. If no argument, run `melos run generate:all`
2. If specific type provided, run the corresponding command
3. Report any errors encountered during generation
