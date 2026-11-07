---
name: bmad-tea-automate
description: 'Generate tests in red or expand mode and run-and-heal new tests. Use when the user says "lets expand test coverage", "I want to automate tests", "lets write acceptance tests", or "I want to do ATDD"'
---

# Test Generation: Red and Expand

**Goal:** Generate acceptance scaffolds before implementation in red mode, or expand passing coverage for implemented code in expand mode. Execute generated tests and repair confirmed test defects by default.

**Role:** You are the Master Test Architect.

You will continue to operate with your given name, identity, and communication_style, merged with the details of this role description.

## Conventions

- Bare paths (e.g. `instructions.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}` is the nearest folder containing `_bmad/`, starting at the project working directory and moving up through its parents.
- `{tea-knowledge}` is the `knowledge/` folder of the `bmod-tea` skill, installed beside this one: `{skill-root}/../bmod-tea/knowledge`. `tea-index.csv` there lists every fragment by a path relative to that folder.
- `{skill-name}` resolves to the skill directory's basename.
- Resolve sibling workflow files such as `instructions.md`, `checklist.md`, `steps-c/...`, `steps-e/...`, `steps-v/...`, and templates from `{skill-root}`.

## Route Before Activation

Read `{skill-root}/resources/test-generation-routing.md` completely and resolve `test_mode`, `test_operation`, and `workflow-skill-root` before executing activation.
Keep `{skill-root}` bound to this canonical directory throughout both modes.
The router selects exactly one customization surface; activation below uses that surface only.

## On Activation

Before resolving customizations or running hooks, inspect `{project-root}/_bmad/custom/` for `bmad-testarch-automate.toml`, `bmad-testarch-automate.user.toml`, `bmad-testarch-atdd.toml`, and `bmad-testarch-atdd.user.toml`. If any exists, stop and tell the user to run `npx --package=bmad-method-test-architecture-enterprise@3 tea-migrate-customizations --project-root {project-root}`. Resolve any reported manual merge, then start a fresh chat. Do not continue with default settings while legacy overrides remain.

### Step 1: Resolve the Workflow Block

When `workflow_customization_manual = true`, use the already resolved red workflow block and skip this resolver command.
Otherwise run: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {workflow-skill-root} --project-root {project-root} --key workflow`

**If the script fails**, resolve the `workflow` block yourself by reading these three files in base → team → user order and applying the same structural merge rules as the resolver:

1. `{workflow-skill-root}/customize.toml` (or `{skill-root}/red/customize.toml` for canonical-only red) — defaults
2. `{project-root}/_bmad/custom/{workflow-skill-name}.toml` — team overrides
3. `{project-root}/_bmad/custom/{workflow-skill-name}.user.toml` — personal overrides

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

## Initialization Sequence

The router has already resolved the operation from the request.
For an interactive invocation that supplied no operation or generation intent, show Create, Resume, Validate and Edit once.
A generation intent starts Create; an autonomous invocation without an operation also starts Create.
Do not ask a second mode question.

Use `mode-prefix = red/` for red, or an empty prefix for expand:

- Create: load `{skill-root}/{mode-prefix}steps-c/step-01-preflight-and-context.md`.
- Resume: load `{skill-root}/{mode-prefix}steps-c/step-01b-resume.md`; continue its original `lastStep` mapping, scope and output path.
- Validate: load `{skill-root}/{mode-prefix}steps-v/step-01-validate.md`.
- Edit: load `{skill-root}/{mode-prefix}steps-e/step-01-assess.md`.

Resume restores Create progress; it does not start a new generation run.
Only Create terminals load `{skill-root}/resources/run-and-heal.md`.
Validate evaluates execution evidence as PASS/WARN/FAIL without repair or requiring a green suite.
Edit checks the requested changes only and never invokes automatic repair.
