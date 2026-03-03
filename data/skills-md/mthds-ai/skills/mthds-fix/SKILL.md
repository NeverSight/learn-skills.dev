---
name: mthds-fix
min_mthds_version: 0.1.0
description: Fix issues in MTHDS bundles. Use when user says "fix this workflow", "fix this method", "repair validation errors", "the pipeline is broken", "fix the .mthds file", after /mthds-check found issues, or when validation reports errors. Automatically applies fixes and re-validates in a loop.
---

# Fix MTHDS bundles

Automatically fix issues in MTHDS method bundles.

## Process

### Step 0 — CLI Check (mandatory, do this FIRST)

Run `mthds-agent --version`. The minimum required version is **0.1.0** (declared in this skill's front matter as `min_mthds_version`).

- **If the command is not found**: STOP. Do not proceed. Tell the user:

> The `mthds-agent` CLI is required but not installed. Install it with:
>
> ```
> npm install -g mthds
> ```
>
> Then re-run this skill.

- **If the version is below 0.1.0**: STOP. Do not proceed. Tell the user:

> This skill requires `mthds-agent` version 0.1.0 or higher (found *X.Y.Z*). Upgrade with:
>
> ```
> npm install -g mthds@latest
> ```
>
> Then re-run this skill.

- **If the version is 0.1.0 or higher**: proceed to the next step.

Do not write `.mthds` files manually, do not scan for existing methods, do not do any other work. The CLI is required for validation, formatting, and execution — without it the output will be broken.

> **No backend setup needed**: This skill works without configuring inference backends or API keys. You can start building/validating methods right away. Backend configuration is only needed to run methods with live inference — use `/pipelex-setup` when you're ready.

### Step 1: Validate and Identify Errors

Always use `-L` pointing to the bundle's own directory to avoid namespace collisions:

```bash
mthds-agent pipelex validate pipe <file>.mthds -L <bundle-directory>/
```

Parse the JSON output:
- If `success: true` — nothing to fix, report clean status
- If `error_type: "ValidateBundleError"` — iterate through `validation_errors` array and fix each (Step 2)
- If model/config error — see [Error Handling Reference](../shared/error-handling.md#model--config-errors) (cannot be fixed by editing the .mthds file)

### Step 2: Fix .mthds Validation Errors

Use the `error_type` field from each validation error to determine the fix:

| Error Type | Fix Strategy |
|------------|-------------|
| `missing_input_variable` | Add the missing variable(s) to the parent pipe's `inputs` line |
| `extraneous_input_variable` | Remove the unused variable(s) from the pipe's `inputs` line |
| `input_stuff_spec_mismatch` | Correct the concept type in `inputs` to match what the sub-pipe expects |
| `inadequate_output_concept` | Change the `output` field to the correct concept type |
| `inadequate_output_multiplicity` | Add or remove `[]` from the output concept |
| `circular_dependency_error` | Restructure the method to break the cycle |
| `llm_output_cannot_be_image` | Use PipeImgGen instead of PipeLLM for image generation |
| `img_gen_input_not_text_compatible` | Ensure PipeImgGen input is text-based (use `ImgGenPrompt`) |
| `invalid_pipe_code_syntax` | Rename the pipe to valid snake_case |
| `unknown_concept` | Add the concept definition to the bundle, or fix the typo |
| `batch_item_name_collision` | Rename `input_item_name` (or `batch_as`) to a distinct singular form of the list name. Also update the branch pipe's `inputs` to use the new item name. |

For error type descriptions, see [Error Handling — Validation Error Types](../shared/error-handling.md#validation-error-types).

### Step 3: Fix TOML Formatting Issues

These aren't always reported by validation but cause problems:

**Multi-line inputs** — must be on a single line:
```toml
# WRONG
inputs = {
    a = "A",
    b = "B"
}

# CORRECT
inputs = { a = "A", b = "B" }
```

**Pipe ordering** — controllers before sub-pipes:
```toml
# CORRECT: main pipe first, then sub-pipes in execution order
[pipe.main_workflow]
type = "PipeSequence"
steps = [
    { pipe = "step_one", result = "intermediate" },
    { pipe = "step_two", result = "final" }
]

[pipe.step_one]
...

[pipe.step_two]
...
```

**Missing required fields** — add with sensible defaults:
- `description` on every pipe and concept
- `type` on every pipe
- `output` on every pipe

### Step 4: Re-validate

After applying fixes, re-validate:

```bash
mthds-agent pipelex validate pipe <file>.mthds -L <bundle-directory>/
```

Continue the fix-validate loop until `success: true` is returned. Some fixes reveal new issues — for example, fixing a `missing_input_variable` may expose an `input_stuff_spec_mismatch` on the newly added input.

If the fix-validate loop gets stuck or errors are unclear, re-run with `--log-level debug` for additional context:

```bash
mthds-agent --log-level debug pipelex validate pipe <file>.mthds -L <bundle-directory>/
```

### Step 5: Report Results

- List all changes made (which pipes were modified and how)
- Show the final validation result
- Flag any remaining warnings or suggestions

## Reference

- [Error Handling](../shared/error-handling.md) — read when CLI returns an error to determine recovery
- [MTHDS Agent Guide](../shared/mthds-agent-guide.md) — read for CLI command syntax or output format details
- [MTHDS Language Reference](../shared/mthds-reference.md) — read when writing or modifying .mthds TOML syntax
- [Native Content Types](../shared/native-content-types.md) — read when fixing type mismatches involving native concepts, to verify available attributes
