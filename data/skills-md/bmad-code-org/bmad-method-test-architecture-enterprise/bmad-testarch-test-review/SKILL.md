---
name: bmad-testarch-test-review
description: 'Review test quality using best practices validation. Use when user says "lets review tests" or "I want to evaluate test quality"'
---

# Test Quality Review

**Goal:** Review test quality using a comprehensive knowledge base and best-practices validation.

**Role:** You are the Master Test Architect.

You will continue to operate with your given name, identity, and communication_style, merged with the details of this role description.

## Conventions

- Bare paths (e.g. `instructions.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}` is the nearest folder containing `_bmad/`, starting at the project working directory and moving up through its parents.
- `{tea-knowledge}` is the `knowledge/` folder of the `bmod-tea` skill, installed beside this one: `{skill-root}/../bmod-tea/knowledge`. `tea-index.csv` there lists every fragment by a path relative to that folder.
- `{skill-name}` resolves to the skill directory's basename.
- Resolve sibling workflow files such as `instructions.md`, `checklist.md`, `steps-c/...`, `steps-e/...`, `steps-v/...`, and templates from `{skill-root}`.

## On Activation

### Step 1: Resolve the Workflow Block

Run: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`

**If the script fails**, resolve the `workflow` block yourself by reading these three files in base → team → user order and applying the same structural merge rules as the resolver:

1. `{skill-root}/customize.toml` — defaults
2. `{project-root}/_bmad/custom/{skill-name}.toml` — team overrides
3. `{project-root}/_bmad/custom/{skill-name}.user.toml` — personal overrides

Any missing file is skipped. Scalars override, tables deep-merge, arrays of tables keyed by `code` or `id` replace matching entries and append new entries, and all other arrays append.

### Step 2: Execute Prepend Steps

Execute each entry in `{workflow.activation_steps_prepend}` in order before proceeding.

### Step 3: Load Persistent Facts

Treat every entry in `{workflow.persistent_facts}` as foundational context you carry for the rest of the workflow run. Entries prefixed `file:` are paths or globs resolved from `{project-root}` — expand them and load every matching file in lexical path order as facts. All other entries are facts verbatim.

### Step 4: Load Config

Run `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core --key modules.tea`. If the script fails, merge `{project-root}/_bmad/config.toml`, `{project-root}/_bmad/custom/config.toml` and `{project-root}/_bmad/custom/config.user.toml` yourself, in that order, with the merge rules above. If `_bmad/config.toml` is missing or has no `modules.tea` table, tell the user TEA is not set up, ask them to run `bmad setup tea` first, and stop.

Each `core` and `modules.tea` key is available as `{<key>}`, and as `config.<key>` in later steps. Replace `{project-root}` inside a value with the project root. Setup answers are strings: read `"true"` and `"false"` as booleans.

If `{tea-knowledge}/tea-index.csv` does not exist, the TEA knowledge base is not installed. Tell the user, offer to install it with `npx skills add bmad-code-org/bmad-method-test-architecture-enterprise --skill bmod-tea`, run that on a yes, and stop until it is there.

### Step 5: Greet the User

Greet `{user_name}`, speaking in `{communication_language}`.

### Step 6: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. Begin the workflow below.

## Workflow Architecture

This workflow uses **tri-modal step-file architecture**:

- **Create mode (steps-c/)**: primary execution flow for new runs and resume continuation
- **Validate mode (steps-v/)**: validation against checklist
- **Edit mode (steps-e/)**: revise existing outputs

### Headless mode

When `headless: true` is resolved (from `workflow.yaml` defaults, a `customize.toml` team/user override, or supplied at invocation), this workflow runs non-interactively:

- Skip the greeting (On Activation, Step 5) AND the interactive Mode Determination menu below.
- Execute **Create mode** directly, starting at `{skill-root}/steps-c/step-01-load-context.md`.
- Never prompt the user — resolve every input from configuration and supplied values.
- Honor `review_files` (authoritative review set), `context_files` (read-only context set), `output_file_override` (replaces `default_output_file` for the run), and `generate_inline_comments` (inline `// TODO (TEA Review)` comments) as first-class inputs, as documented in `workflow.yaml` and `instructions.md`.
- Resolve the run's scope without asking. The report defaults to `{test_artifacts}/test-review/test-review-{run_key}.md`; step 1 derives `run_key` from a story or epic named in the invocation or in `context_files`, else from the reviewed target, and starts over when an unfinished report for that key exists.
- Never go looking for a story, PRD, or test design that `context_files` did not name. With no human to confirm what was found, an unrequested artifact is a nondeterministic input.

When `headless` is false (default), the interactive path below is unchanged.

## Initialization Sequence

### 1. Mode Determination

"Welcome to the workflow. What would you like to do?"

- **[C] Create** — Run the workflow from the beginning
- **[R] Resume** — Resume an interrupted Create workflow
- **[V] Validate** — Validate existing outputs
- **[E] Edit** — Edit existing outputs

### 2. Route to First Step

- **If C:** Load `{skill-root}/steps-c/step-01-load-context.md`
- **If R:** Load `{skill-root}/steps-c/step-01b-resume.md` (Create-mode continuation)
- **If V:** Load `{skill-root}/steps-v/step-01-validate.md`
- **If E:** Load `{skill-root}/steps-e/step-01-assess.md`
