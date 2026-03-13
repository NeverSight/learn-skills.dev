---
name: openapi-format
description: Configure and run openapi-format CLI workflows for OpenAPI/AsyncAPI documents. Use when you need to sort fields, filter operations/tags/flags/content, change casing, generate operationIds, apply overlays, convert OpenAPI versions (3.0/3.1 to 3.1/3.2), rename titles, split specs, bundle refs, or manage .openapiformatrc/--configFile driven formatting pipelines with minimal config overrides.
---

# openapi-format

Follow this skill when a user asks to transform an OpenAPI document with the `openapi-format` CLI.

## Core workflow

1. Identify the target outcome first.
- Determine exactly what should change: order, filtering, casing, generation, overlay, conversion, rename, output format, split.
- Determine input source (local file, remote URL, or overlay `extends` fallback).

2. Choose command shape.
- Prefer a single command with explicit input/output unless the user asks for stdout.
- Use `--configFile` for reusable workflows.
- Use `.openapiformatrc` for project defaults.

3. Keep config minimal.
- Start from defaults.
- Add only keys required for requested behavior.
- Avoid writing exhaustive config unless requested.

4. Apply correct precedence.
- Load `.openapiformatrc` only when `--configFile` is not supplied.
- Load and merge `--configFile` values.
- Apply CLI options last.
- Normalize `--no-sort` and `--no-bundle` into `sort=false` and `bundle=false`.

5. Respect processing order.
- `generate -> filter -> overlay -> sort -> casing -> convertTo -> rename -> write/split/stdout`

6. Produce the output safely.
- Use `--output` for file writes.
- If `--split` is true, require `--output` and treat it as split target root.
- Use `--json` or `--yaml` for stdout output formatting.

## Decision rules

### Filter semantics
- Treat `methods`, `tags`, `operationIds`, `operations`, `flags`, `flagValues`, `responseContent`, and `requestContent` as removal filters.
- Treat `inverseMethods`, `inverseTags`, `inverseOperationIds`, `inverseFlags`, `inverseFlagValues`, `inverseResponseContent`, and `inverseRequestContent` as keep filters.
- Use `unusedComponents` to remove unreferenced components recursively (iterative cleanup).
- Use `stripFlags` to delete marker fields after filtering.

### Overlay behavior
- Accept `--overlayFile` with `actions`.
- If input file is omitted and overlay has `extends`, use `extends` as effective input.
- Resolve local `extends` relative to overlay file directory.

### Sorting and components
- Default sorting comes from `defaultSort.json`.
- `sortPathsBy` controls path ordering (`original`, `path`, `tags`).
- `--sortComponentsFile` controls which component groups are alphabetized.
- `--sortComponentsProps` alphabetizes schema properties in `components.schemas.*.properties`.

### Output constraints
- `--split` requires `--output`.
- `--keepComments` only affects YAML comment preservation.
- `--lineWidth` controls YAML line wrapping (`-1` means unlimited).

## Use references

Open only what is needed:
- `references/feature-matrix.md` for option behavior, defaults, and interactions.
- `references/config-patterns.md` for minimal config templates.
- `references/command-recipes.md` for runnable command patterns.
- `references/troubleshooting.md` for failure diagnosis and fixes.

## Delivery checklist

1. Return the exact command(s) to run.
2. Return minimal config file contents if config files are needed.
3. Explain expected transformation result in plain terms.
4. Call out side effects (component pruning, split output tree, version conversion changes).
5. Highlight any assumptions (input path, output path, format, bundle behavior).
