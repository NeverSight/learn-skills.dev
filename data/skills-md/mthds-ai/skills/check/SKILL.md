---
name: check
description: Check and validate MTHDS bundles for issues. Use when user says "validate this", "check my workflow", "check my method", "does this .mthds make sense?", "review this pipeline", "any issues?", "is this correct?". Reports problems without modifying files. Read-only analysis.
---

# Check MTHDS bundles

Validate and review MTHDS bundles based on the MTHDS standard without making changes.

## Process

**Prerequisite**: See [CLI Prerequisites](../shared/prerequisites.md)

1. **Read the .mthds file** — Load and parse the method

2. **Run CLI validation** (use `-L` pointing to the bundle's own directory to avoid namespace collisions):
   ```bash
   mthds-agent pipelex validate pipe <file>.mthds -L <bundle-directory>/
   ```

3. **Parse the JSON output**:
   - If `success: true` — all pipes validated, report clean status
   - If error — see [Error Handling Reference](../shared/error-handling.md) for error types and recovery

4. **Cross-domain validation** — when the bundle references pipes from other domains, use `--library-dir` (see [Error Handling — Cross-Domain](../shared/error-handling.md#cross-domain-validation))

5. **Analyze for additional issues** (manual review beyond CLI validation):
   - Unused concepts (defined but never referenced)
   - Unreachable pipes (not in main_pipe execution path)
   - Missing descriptions on pipes or concepts
   - Inconsistent naming conventions
   - Potential prompt issues (missing variables, unclear instructions)

6. **Report findings by severity**:
   - **Errors**: Validation failures from CLI (with `error_type` and `pipe_code`)
   - **Warnings**: Issues that may cause problems (e.g., model availability)
   - **Suggestions**: Improvements for maintainability

7. **Do NOT make changes** — This skill is read-only

## What Gets Checked

- TOML syntax validity
- Concept definitions and references
- Pipe type configurations
- Input/output type matching
- Variable references in prompts
- Cross-domain references
- Naming convention compliance
- Model preset resolution (dry run)

## Reference

- [CLI Prerequisites](../shared/prerequisites.md) — read at skill start to check CLI availability
- [Error Handling](../shared/error-handling.md) — read when CLI returns an error to determine recovery
- [MTHDS Agent Guide](../shared/mthds-agent-guide.md) — read for CLI command syntax or output format details
- [MTHDS Language Reference](../shared/mthds-reference.md) — read when reviewing .mthds TOML syntax
- [Native Content Types](../shared/native-content-types.md) — read when checking `$var.field` references in prompts to verify the attribute exists on the content type
