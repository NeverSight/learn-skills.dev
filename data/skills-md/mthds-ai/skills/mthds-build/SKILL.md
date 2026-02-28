---
name: mthds-build
min_mthds_version: 0.0.13
description: Build new AI method from scratch using the MTHDS standard (.mthds bundle files). Use when user says "create a pipeline", "build a workflow", "new .mthds file", "make a method", "design a pipe", or wants to create any new method from scratch. Guides the user through a 10-phase construction process.
---

# Build AI Method using the MTHDS standard (Agentic)

Create new MTHDS bundles through an adaptive, phase-based approach. This skill guides you through drafting (markdown), structuring (CLI/JSON), and assembling complete .mthds bundles.

## Philosophy

1. **Drafting phases**: Generate human-readable markdown documents
2. **Structuring phases**: Use agent CLI commands for JSON-to-TOML conversion
3. **Visualization**: Present ASCII graphs at overview and detail levels
4. **Iterative**: Refine at each phase before proceeding

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

**Default**: Automatic for simple-to-moderate methods. Interactive for complex multi-step methods or when the user's request is ambiguous.

**Detection heuristics**:
- User provides a clear one-sentence goal → automatic
- User describes a complex multi-step process → interactive
- User mentions batching, conditions, or parallel execution → interactive
- User says "create a pipeline for X" with no elaboration → automatic

---

## Step 0 — CLI Check (mandatory, do this FIRST)

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

---

## Existing Method Detection

**Goal**: Before starting a new build, check whether the project already contains methods that overlap with the user's request.

**When to check**: Always, before entering automatic or interactive mode — with these exceptions:

- **Skip entirely** if the user's request signals intent to create something new. This includes phrases like "new method", "a new method", "brand new", "from scratch", "create a method", or similar.
- **Targeted search** if the user references a specific existing method by name or path, search specifically for that method instead of scanning broadly. If the specific method cannot be found, fall back to the general search approach below.

For the general case, scan `mthds-wip/` and any other directories containing `.mthds` files in the project.

**How to check**:
1. List all `.mthds` files in the project (glob for `**/*.mthds`)
2. For each file found, read the file header (domain, main pipe code, description) to understand what it does
3. Compare with the user's current request — look for overlap in topic, domain, or purpose

**If no existing methods overlap**: Proceed normally with the build.

**If one or more existing methods overlap**, present the user with three options:

> I found an existing method that seems related to what you're asking for:
> - **`<path/to/bundle.mthds>`** — *<brief description of what it does>*
>
> How would you like to proceed?
> 1. **Start fresh** — Create a wholly new method from scratch (ignoring the existing one)
> 2. **Use the existing method** — It already does what you need; cancel this build
> 3. **Build upon it** — Extend the existing method by adding pipes before or after the current flow

**Handling each choice**:
- **Start fresh**: Proceed with the build as normal (automatic or interactive path below).
- **Use the existing method**: End the build. Remind the user they can run it with `/mthds-run` and point them to its `inputs.json` if available.
- **Build upon it**: Switch to the /mthds-edit skill, framing the task as an extension — ask the user what additional processing they want to add (e.g., a preprocessing step before the main pipe, a postprocessing step after, or additional parallel branches). Pass the existing `.mthds` file path to the edit workflow.

---

## Phase 1: Understand Requirements

**Goal**: Gather complete information before planning.

Ask the user:
- What are the method's inputs? (documents, images, text, structured data)
- What outputs should it produce?
- What transformations are needed?
- Are there conditional branches or parallel operations?
- Should items be processed in batches?

**Output**: Requirements summary (keep in context)

---

## Phase 2: Draft the Plan

**Goal**: Create a pseudo-code narrative of the method.

Draft a plan in markdown that describes:
- The overall flow from inputs to outputs
- Each processing step with its purpose
- Variable names (snake_case) for inputs and outputs of each step
- Where structured data or lists are involved

**Rules**:
- Name variables consistently across steps
- Use plural names for lists (e.g., `documents`), singular for items (e.g., `document`)
- Don't detail types yet - focus on the flow

**Show ASCII Overview** — see [Manual Build Phases](references/manual-build-phases.md#phase-2-ascii-overview-diagram) for the diagram template.

**Output**: Plan draft (markdown)

---

## Phase 3: Draft Concepts

**Goal**: Identify all data types needed in the method.

From the plan, identify input, intermediate, and output concepts.

For each concept, draft:
- **Name**: PascalCase, singular noun (e.g., `Invoice` not `Invoices`)
- **Description**: What it represents
- **Type**: Either `refines: NativeConcept` OR `structure: {...}`

**Native concepts** (built-in, do NOT redefine): `Text`, `Html`, `Image`, `Document`, `Number`, `Page`, `TextAndImages`, `ImgGenPrompt`, `JSON`, `Anything`, `Dynamic`. See [MTHDS Language Reference — Native Concepts](../shared/mthds-reference.md#native-concepts)

> **Note**: `Document` is the native concept for any document (PDF, Word, etc.). `Image` is for any image format (JPEG, PNG, etc.). File formats like "PDF" or "JPEG" are not concepts.

Each native concept has accessible attributes (e.g., `Image` has `url`, `public_url`, `filename`, `caption`...; `Document` has `url`, `public_url`, `filename`...; `Page` has `text_and_images` and `page_view`). See [Native Content Types](../shared/native-content-types.md) for the full attribute reference — essential for `$var.field` prompts and `construct` blocks.

**Concept naming rules**:
- No adjectives: `Article` not `LongArticle`
- No circumstances: `Argument` not `CounterArgument`
- Always singular: `Employee` not `Employees`

**Output**: Concepts draft (markdown)

---

## Phase 4: Structure Concepts

**Goal**: Convert concept drafts to validated TOML using the CLI.

Prepare JSON specs for all concepts, then convert them **in parallel** by making multiple concurrent tool calls.

**Example** (3 concepts converted in parallel):
```bash
# Call all three in parallel (single response, multiple tool calls):
mthds-agent pipelex concept --spec '{"the_concept_code": "Invoice", "description": "A commercial invoice document", "structure": {"invoice_number": "The unique identifier", "vendor_name": {"type": "text", "description": "Vendor name", "required": true}, "total_amount": {"type": "number", "description": "Total amount", "required": true}}}'
mthds-agent pipelex concept --spec '{"the_concept_code": "LineItem", "description": "A single line item on an invoice", "structure": {"description": "Item description", "quantity": {"type": "integer", "required": true}, "unit_price": {"type": "number", "required": true}}}'
mthds-agent pipelex concept --spec '{"the_concept_code": "Summary", "description": "A text summary of content", "refines": "Text"}'
```

**Field types**: `text`, `integer`, `boolean`, `number`, `date`, `concept`, `list`

**Choices (enum-like constrained values)**:
```toml
status = {choices = ["pending", "processing", "completed"], description = "Order status", required = true}
score = {type = "number", choices = ["0", "0.5", "1", "1.5", "2"], description = "Score on a half-point scale"}
```
When `choices` is present, `type` defaults to `text` if omitted. You can also pair choices with `integer` or `number` types explicitly.

**Nested concept references** in structures:
```toml
field = {type = "concept", concept_ref = "my_domain.OtherConcept", description = "...", required = true}
items = {type = "list", item_type = "concept", item_concept_ref = "my_domain.OtherConcept", description = "..."}
```

**Output**: Validated concept TOML fragments

> **Partial failures**: If some commands fail, fix the failing specs using the error JSON (`error_domain: "input"` means the spec is wrong). Re-run only the failed commands.

---

## Phase 5: Draft the Flow

**Goal**: Design the complete pipeline structure with controller selection.

### Controller Selection Guide

| Controller | Use When | Key Pattern |
|------------|----------|-------------|
| **PipeSequence** | Steps must execute in order | step1 → step2 → step3 |
| **PipeBatch** | Same operation on each list item | map(items, transform) |
| **PipeParallel** | Independent operations run together | fork → join |
| **PipeCondition** | Route based on data values | if-then-else |

### Operator Selection Guide

| Operator | Use When |
|----------|----------|
| **PipeLLM** | Generate text or structured objects with AI |
| **PipeExtract** | Extract content from PDF/Image → Page[] |
| **PipeCompose** | Template text or construct objects |
| **PipeImgGen** | Generate images from text prompts |
| **PipeFunc** | Custom Python logic |

> **Note**: `Page[]` outputs from PipeExtract automatically convert to text when inserted into prompts using `@variable`.

**Show detailed ASCII flow** — see [Manual Build Phases](references/manual-build-phases.md#phase-5-controller-flow-diagrams) for all controller flow diagrams.

**Output**: Flow draft with pipe contracts (markdown)

---

## Phase 6: Review & Refine

**Goal**: Validate consistency before structuring.

Check:
- [ ] Main pipe is clearly identified and handles method inputs
- [ ] Variable names are consistent across all pipes
- [ ] Input/output types match between connected pipes
- [ ] PipeBatch branches receive singular items, not lists
- [ ] PipeBatch: `input_item_name` (singular) differs from `input_list_name` (plural) and all `inputs` keys
- [ ] PipeSequence batch steps: `batch_as` (singular) differs from `batch_over` (plural)
- [ ] PipeImgGen inputs are text (add PipeLLM if needed to generate prompt)
- [ ] No circular dependencies

**Confirm with user** before proceeding to structuring.

---

## Phase 7: Structure Pipes

**Goal**: Convert pipe drafts to validated TOML using the CLI.

Default to talent names from [Talents and Presets](references/talents-and-presets.md). Only look up specific model presets when the user has explicit instructions about model choice. In all cases, verify that referenced presets exist:
```bash
mthds-agent pipelex models --type llm          # when structuring PipeLLM pipes
mthds-agent pipelex models --type extract      # when structuring PipeExtract pipes
mthds-agent pipelex models --type img_gen      # when structuring PipeImgGen pipes
```

Prepare JSON specs for all pipes, then convert them **in parallel** by making multiple concurrent tool calls.

For detailed CLI examples for each pipe type (PipeLLM, PipeSequence, PipeBatch, PipeCondition, PipeCompose, PipeParallel, PipeExtract, PipeImgGen), see [Manual Build Phases](references/manual-build-phases.md#phase-7-pipe-type-cli-examples).

**Output**: Validated pipe TOML fragments

> **Partial failures**: Fix failing specs using the error JSON. Re-run only the failed commands.

---

## Phase 8: Assemble Bundle

**Goal**: Combine all parts into a complete .mthds file.

**Save location**: Always save method bundles to `mthds-wip/`. Do not ask the user for the save location.

For the assemble CLI command and direct .mthds writing examples, see [Manual Build Phases](references/manual-build-phases.md#phase-8-assemble-bundle).

---

## Phase 9: Validate & Test

**Goal**: Ensure the bundle is valid and works correctly.

Always use `-L` pointing to the bundle's own directory to avoid namespace collisions with other bundles in the project.

```bash
# Validate (isolated from other bundles)
mthds-agent pipelex validate pipe mthds-wip/pipeline_01/bundle.mthds -L mthds-wip/pipeline_01/

# Generate example inputs
mthds-agent pipelex inputs pipe mthds-wip/pipeline_01/bundle.mthds -L mthds-wip/pipeline_01/

# Dry run (directory mode: auto-detects bundle, inputs, library dir)
mthds-agent pipelex run pipe mthds-wip/pipeline_01/ --dry-run --mock-inputs
```

Fix any validation errors and re-validate. If validation fails unexpectedly or errors are unclear, re-run with `--log-level debug` for additional context:

```bash
mthds-agent --log-level debug pipelex validate pipe mthds-wip/pipeline_01/bundle.mthds -L mthds-wip/pipeline_01/
```

---

## Phase 10: Deliver

**Goal**: Generate input template after a successful build.

After validation passes (Phase 9), generate the input template:

```bash
# Input template (extracts the input schema as JSON)
mthds-agent pipelex inputs pipe <mthds_file> -L <output_dir>/
```

Replace `<mthds_file>` and `<output_dir>` with actual paths from the build output.

### Present Results

After the command succeeds:

1. **Input template**: Show the `inputs` JSON from the inputs command output. Save it to `<output_dir>/inputs.json` for the user to fill in.

2. **Next steps — try it now**: If the method requires inputs, the saved `inputs.json` still contains placeholder values, so suggest a dry run first:
   > To try this method right now, use /mthds-run or from the terminal:
   > ```
   > mthds run pipe <output_dir>/ --dry-run --mock-inputs
   > ```

3. **Next steps — run with real data**: Explain how to prepare real inputs, then run for real:
   > To run with real data, use /mthds-inputs to prepare your inputs (provide your own files, or generate synthetic test data), then:
   > ```
   > mthds run pipe <output_dir>/
   > ```

   Replace `<output_dir>` with the actual output directory path used throughout the build.

---

## Quick Reference

### Multiplicity Notation
- `Text` - single item
- `Text[]` - variable-length list
- `Text[3]` - exactly 3 items

### Prompt Variables
- `@variable` - Block insertion (multi-line, with delimiters)
- `$variable` - Inline insertion (short text)
- `$var.field` - Access nested field

### Naming Conventions
- **Domain**: `snake_case`
- **Concepts**: `PascalCase`, singular
- **Pipes**: `snake_case`
- **Variables**: `snake_case`

---

## Reference

- [Error Handling](../shared/error-handling.md) — read when CLI returns an error to determine recovery
- [MTHDS Agent Guide](../shared/mthds-agent-guide.md) — read for CLI command syntax or output format details
- [MTHDS Language Reference](../shared/mthds-reference.md) — read when writing or modifying .mthds TOML syntax
- [Native Content Types](../shared/native-content-types.md) — read when using `$var.field` in prompts or `from` in construct blocks, to know which attributes each native concept exposes
- [Manual Build Phases](references/manual-build-phases.md) — read for detailed ASCII diagrams and CLI examples per phase
- [Talents and Presets](references/talents-and-presets.md) — read when selecting model talents for pipe structuring
