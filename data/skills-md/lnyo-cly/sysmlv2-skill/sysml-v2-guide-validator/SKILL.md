---
name: sysml-v2-guide-validator
description: Provide SysML v2 guidance, examples, and official-first validation for .sysml/.kerml work. Use when Codex needs to generate SysML v2 syntax, review or explain SysML v2 project code, validate single files, validate multi-file imports, validate whole directories, run official Pilot-based checks, or apply bundled SysML v2 standard library context during analysis.
---

# SysML v2 Guide Validator

## Overview

Use this skill to generate, analyze, and validate SysML v2 textual models.

Use `scripts/sysmlv2_validate.py` as the main entrypoint.
The official runtime is bundled in `assets/official-validator/runtime` (jar + `sysml.library`).
Use `scripts/setup_official_validator.sh` only when you want to refresh runtime from source.
Use `references/` for syntax guidance and examples before generating model code.
Use `--stdin` or `--text` when only a code block is available and no file exists yet.

## Workflow Selection

Choose one workflow first:

1. Validation workflow: Run official SysML v2 validation (default), or lightweight fallback checks.
2. Generation workflow: Load syntax and examples, then generate SysML v2 code.
3. Analysis workflow: Explain architecture, imports, package dependencies, and defects.

## Validation Workflow

Official validation works out of the box with bundled runtime.

Optional: refresh bundled runtime from source:

```bash
bash scripts/setup_official_validator.sh
```

Run official validation for a single file (default engine):

```bash
python3 scripts/sysmlv2_validate.py path/to/model.sysml
```

Run official validation for a full project directory:

```bash
python3 scripts/sysmlv2_validate.py path/to/project
```

Run official validation with JSON output:

```bash
python3 scripts/sysmlv2_validate.py path/to/project --format json
```

Override official validator command explicitly:

```bash
python3 scripts/sysmlv2_validate.py path/to/project --official-command "/path/to/validate-sysml"
```

Validate inline code snippet from stdin (no manual file write):

```bash
echo "package Demo { part def A; }" | python3 scripts/sysmlv2_validate.py --stdin
```

Validate first fenced code block from Markdown text:

~~~bash
cat <<'SNIP' | python3 scripts/sysmlv2_validate.py --stdin --extract-fenced
```sysml
package Demo { part def A; }
```
SNIP
~~~

Force lightweight engine for fast lexical/import checks:

```bash
python3 scripts/sysmlv2_validate.py path/to/project --engine lightweight --strict-imports
```

Use automatic fallback (`official` if available, otherwise `lightweight`):

```bash
python3 scripts/sysmlv2_validate.py path/to/project --engine auto
```

Default behavior:

- Default engine is `official`.
- Official command discovery order: `--official-command`, `SYSML_V2_VALIDATE_CMD`, `assets/official-validator/validate-sysml`, then `validate-sysml` in `PATH`.
- Lightweight mode uses bundled SysML library index for import resolution unless disabled.

Use `--no-builtin-library` to disable bundled library lookup in lightweight mode.
Use `--no-follow-imports` to keep lightweight validation scoped to explicit file targets.
Default refresh source is `https://github.com/LnYo-Cly/sysmlv2-validator`.
Use `SYSML_V2_VALIDATOR_REPO` and `SYSML_V2_VALIDATOR_REF` when you want refresh to build from another repository or revision (for example, your own fork).
Use `SYSML_V2_VALIDATOR_BACKUP_KEEP` to control local backup retention for refreshed source/library directories (default `1`).
Use `SYSML_V2_KEEP_BUILD_SRC` to keep build source after refresh (set `1`) or auto-clean it (default `0`).

For full options and exit behavior, read `references/validation.md`.

## Generation Workflow

Before generating SysML v2 code:

1. Read `references/syntax-quick-reference.md`.
2. Read `references/examples.md` and choose the closest pattern.
3. Generate code with explicit package names and import strategy.
4. Run `scripts/sysmlv2_validate.py` and iterate until clean.

Generation rules:

- Keep one primary package per file.
- Keep imports explicit and resolvable.
- Prefer stable package naming and file naming alignment.

## Analysis Workflow

For existing SysML v2 projects:

1. Run official validation on the target file/directory first.
2. Optionally run lightweight validation to expose import graph and project-hygiene issues.
3. Group findings by syntax/semantic errors, unresolved imports, and organization issues.
4. Propose patch sequence in dependency order (shared packages first, dependents second).
5. Re-run validation after each patch batch.

## Resources

Use resources progressively:

- `references/syntax-quick-reference.md`: Core textual syntax rules.
- `references/examples.md`: Reusable patterns and prompt templates.
- `references/validation.md`: Engine behavior, options, and error semantics.
- `references/sources.md`: Upstream specs/repos and maintenance references.
- `scripts/setup_official_validator.sh`: Optional runtime refresh from source repository.
- `scripts/rebuild_library_index.py`: Refresh bundled package index after library updates.

## Bundled Library

This skill bundles `SysML-v2-Release/sysml.library` in `assets/sysml-library/sysml.library`.
This package index is consumed by lightweight import-aware validation.
Official engine behavior comes from the upstream validator implementation.
