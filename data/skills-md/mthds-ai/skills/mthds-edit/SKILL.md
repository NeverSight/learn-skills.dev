---
name: mthds-edit
min_mthds_version: 0.0.13
description: Edit existing MTHDS bundles (.mthds files). Use when user says "change this pipe", "update the prompt", "rename this concept", "add a step", "remove this pipe", "modify the workflow", "modify the method", "refactor this pipeline", or wants any modification to an existing .mthds file. Supports automatic mode for clear changes and interactive mode for complex modifications.
---

# Edit MTHDS bundles

Modify existing MTHDS method bundles.

## Mode Selection

### How mode is determined

1. **Explicit override**: If the user states a preference, always honor it:
   - Automatic signals: "just do it", "go ahead", "automatic", "quick", "don't ask"
   - Interactive signals: "walk me through", "help me", "guide me", "step by step", "let me decide"

2. **Skill default**: Each skill defines its own default based on the nature of the task.

3. **Request analysis**: If no explicit signal and no strong skill default, assess the request:
   - Detailed, specific requirements → automatic
   - Brief, ambiguous, or subjective → interactive

### Mode behavior

**Automatic mode:**
- State assumptions briefly before proceeding
- Make reasonable decisions at each step
- Present the result when done
- Pause only if a critical ambiguity could lead to wasted work

**Interactive mode:**
- Ask clarifying questions at the start
- Present options at decision points
- Confirm before proceeding at checkpoints
- Allow the user to steer direction

### Mode switching

- If in automatic mode and the user asks a question or gives feedback → switch to interactive for the current phase
- If in interactive mode and the user says "looks good, go ahead" or similar → switch to automatic for remaining phases

**Default**: Automatic for clear, specific changes. Interactive for ambiguous or multi-step modifications.

**Detection heuristics**:
- "Rename X to Y" → automatic
- "Update the prompt in pipe Z" with new text provided → automatic
- "Add a step to do X" (open-ended) → interactive
- "Refactor this pipeline" (subjective) → interactive
- Multiple changes requested at once → interactive (confirm the plan)

---

## Process

### Step 0 — CLI Check (mandatory, do this FIRST)

Run `mthds-agent --version`. The minimum required version is **0.0.13** (declared in this skill's front matter as `min_mthds_version`).

- **If the command is not found**: STOP. Do not proceed. Tell the user:

> The `mthds-agent` CLI is required but not installed. Install it with:
>
> ```
> npm install -g mthds
> ```
>
> Then re-run this skill.

- **If the version is below 0.0.13**: STOP. Do not proceed. Tell the user:

> This skill requires `mthds-agent` version 0.0.13 or higher (found *X.Y.Z*). Upgrade with:
>
> ```
> npm install -g mthds@latest
> ```
>
> Then re-run this skill.

- **If the version is 0.0.13 or higher**: proceed to the next step.

Do not write `.mthds` files manually, do not scan for existing methods, do not do any other work. The CLI is required for validation, formatting, and execution — without it the output will be broken.

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
   If errors, see [Error Handling Reference](../shared/error-handling.md) for recovery strategies by error domain. Use /mthds-fix skill for automatic error resolution.

5. **Regenerate inputs if needed**:
   - If inputs changed, run `mthds-agent pipelex inputs pipe <file>.mthds -L <bundle-dir>/`
   - Update existing inputs.json if present

6. **Present completion**:
   - If inputs were regenerated (step 5 triggered), show the path to the updated file.
   - Provide a concrete CLI example. If `inputs.json` contains placeholder values, suggest the safe dry-run command first:
     > To try the updated method now, use /mthds-run or from the terminal:
     > ```
     > mthds run pipe <bundle-dir>/ --dry-run --mock-inputs
     > ```
     >
     > To run with real data, use /mthds-inputs to prepare your inputs (provide your own files, or generate synthetic test data), then:
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

- [Error Handling](../shared/error-handling.md) — read when CLI returns an error to determine recovery
- [MTHDS Agent Guide](../shared/mthds-agent-guide.md) — read for CLI command syntax or output format details
- [MTHDS Language Reference](../shared/mthds-reference.md) — read when writing or modifying .mthds TOML syntax
- [Native Content Types](../shared/native-content-types.md) — read when using `$var.field` in prompts or `from` in construct blocks, to know which attributes each native concept exposes
- [Talents & Presets](references/talents-and-presets.md) — read when setting or changing the `model` field in a pipe, to find the correct preset name
