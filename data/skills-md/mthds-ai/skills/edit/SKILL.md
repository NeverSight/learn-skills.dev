---
name: edit
description: Edit existing MTHDS bundles (.mthds files). Use when user says "change this pipe", "update the prompt", "rename this concept", "add a step", "remove this pipe", "modify the workflow", "modify the method", "refactor this pipeline", or wants any modification to an existing .mthds file. Supports automatic mode for clear changes and interactive mode for complex modifications.
---

# Edit MTHDS bundles

Modify existing MTHDS method bundles.

## Mode Selection

See [Mode Selection](../shared/mode-selection.md) for general mode behavior.

**Default**: Automatic for clear, specific changes. Interactive for ambiguous or multi-step modifications.

**Detection heuristics**:
- "Rename X to Y" → automatic
- "Update the prompt in pipe Z" with new text provided → automatic
- "Add a step to do X" (open-ended) → interactive
- "Refactor this pipeline" (subjective) → interactive
- Multiple changes requested at once → interactive (confirm the plan)

---

## Process

**Prerequisite**: See [CLI Prerequisites](../shared/prerequisites.md)

1. **Read the existing .mthds file** — Understand current structure before making changes

2. **Understand requested changes**:
   - What pipes need to be added, removed, or modified?
   - What concepts need to change?
   - Does the method structure need refactoring?

   **Interactive checkpoint**: Present a summary of planned changes. Ask "Does this plan look right?" before proceeding to step 3.

   **Automatic**: Proceed directly to step 3. State planned changes in one line.

3. **Apply changes**:
   - Maintain proper pipe ordering (controllers before sub-pipes)
   - Keep TOML formatting consistent
   - Preserve cross-references between pipes
   - Keep inputs on a single line
   - Maintain POSIX standard (empty line at end, no trailing whitespace)

4. **Validate after editing**:
   ```bash
   mthds-agent pipelex validate pipe <file>.mthds -L <bundle-dir>/
   ```
   If errors, see [Error Handling Reference](../shared/error-handling.md) for recovery strategies by error domain. Use /fix skill for automatic error resolution.

5. **Regenerate inputs if needed**:
   - If inputs changed, run `mthds-agent pipelex inputs pipe <file>.mthds -L <bundle-dir>/`
   - Update existing inputs.json if present

6. **Present completion**:
   - If inputs were regenerated (step 5 triggered), show the path to the updated file.
   - Provide a concrete CLI example. If `inputs.json` contains placeholder values, suggest the safe dry-run command first:
     > To try the updated method now, use /run or from the terminal:
     > ```
     > mthds run pipe <bundle-dir>/ --dry-run --mock-inputs
     > ```
     >
     > To run with real data, use /inputs to prepare your inputs (provide your own files, or generate synthetic test data), then:
     > ```
     > mthds run pipe <bundle-dir>/
     > ```

## Common Edit Operations

- **Add a pipe**: Define concept if needed, add pipe in correct order
- **Modify a prompt**: Update prompt text, check variable references
- **Change inputs/outputs**: Update type, regenerate inputs
- **Add batch processing**: Add `batch_over` (plural list name) and `batch_as` (singular item name) to step — they must be different
- **Refactor to sequence**: Wrap multiple pipes in PipeSequence

## Reference

- [CLI Prerequisites](../shared/prerequisites.md) — read at skill start to check CLI availability
- [Error Handling](../shared/error-handling.md) — read when CLI returns an error to determine recovery
- [MTHDS Agent Guide](../shared/mthds-agent-guide.md) — read for CLI command syntax or output format details
- [MTHDS Language Reference](../shared/mthds-reference.md) — read when writing or modifying .mthds TOML syntax
- [Native Content Types](../shared/native-content-types.md) — read when using `$var.field` in prompts or `from` in construct blocks, to know which attributes each native concept exposes
- [Talents & Presets](../build/references/talents-and-presets.md) — read when setting or changing the `model` field in a pipe, to find the correct preset name
