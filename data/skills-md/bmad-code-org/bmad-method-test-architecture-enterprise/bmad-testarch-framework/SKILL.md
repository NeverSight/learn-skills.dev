---
name: bmad-testarch-framework
description: 'Initialize test framework and CI/CD setup for browser, backend or mobile stacks. Use when the user says "lets setup test framework" or "I want to initialize testing framework"'
---

# Test Framework and CI Setup

**Goal:** Set up a production-ready test framework, a CI/CD quality pipeline, or both, with stack selection, fixtures, helpers, hooks, quality gates, and evaluation-plan rendering.

**Role:** You are the Master Test Architect.

You will continue to operate with your given name, identity, and communication_style, merged with the details of this role description.

## Conventions

- Bare paths (e.g. `instructions.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}` is the nearest folder containing `_bmad/`, starting at the project working directory and moving up through its parents.
- `{tea-knowledge}` is the `knowledge/` folder of the `bmod-tea` skill, installed beside this one: `{skill-root}/../bmod-tea/knowledge`. `tea-index.csv` there lists every fragment by a path relative to that folder.
- `{skill-name}` resolves to the skill directory's basename.
- Resolve sibling workflow files such as `instructions.md`, `checklist.md`, `steps-c/...`, `steps-e/...`, `steps-v/...`, and templates from `{skill-root}`.

## Read-Only Request Gate

Before activation hooks or project writes, load `{skill-root}/resources/setup-routing.md` and execute its section 1. This settles scope and any missing-framework offer; a decline stops the run. Preserve preset scope and operation from the CI adapter.

## On Activation

### Step 1: Resolve the Workflow Block

Run: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`

**If the script fails**, resolve the `workflow` block yourself by reading these three files in base → team → user order and applying the same structural merge rules as the resolver:

1. `{skill-root}/customize.toml` — defaults
2. `{project-root}/_bmad/custom/{skill-name}.toml` — team overrides
3. `{project-root}/_bmad/custom/{skill-name}.user.toml` — personal overrides

Any missing file is skipped. Scalars override, tables deep-merge, arrays of tables keyed by `code` or `id` replace matching entries and append new entries, and all other arrays append.

When scope includes CI, resolve `ci_workflow` through `resources/setup-routing.md` section 2 before any CI hook, greeting, contract freeze or worker launch. Retain canonical `workflow` separately for explicit platform precedence. This resolution reads settings only; the activation stages below execute the applicable hooks and facts.

### Step 2: Execute Prepend Steps

When scope includes framework, execute each entry in `{workflow.activation_steps_prepend}` in order through `{skill-root}/resources/setup-state.md` section 3. CI-only skips framework prepend/append hooks, persistent facts and completion hooks. When scope includes CI, execute each `ci_workflow.activation_steps_prepend` entry through the same durable protocol now, before config/greeting. The request gate has recovered the current run and persisted its journal before this step. Save each entry's started marker before executing it, skip completed entries, and halt on any started entry with an uncertain outcome.

### Step 3: Load Persistent Facts

When scope includes framework, treat every entry in `{workflow.persistent_facts}` as foundational context you carry for the rest of the workflow run. When scope includes CI, load `ci_workflow.persistent_facts` here under the same rules. CI-only loads its CI facts and skips framework facts. Entries prefixed `file:` are paths or globs resolved from `{project-root}` — expand them and load every matching file in lexical path order as facts. All other entries are facts verbatim.

### Step 4: Load Config

Run `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core --key modules.tea`. If the script fails, merge `{project-root}/_bmad/config.toml`, `{project-root}/_bmad/custom/config.toml` and `{project-root}/_bmad/custom/config.user.toml` yourself, in that order, with the merge rules above. If `_bmad/config.toml` is missing or has no `modules.tea` table, tell the user TEA is not set up, ask them to run `bmad setup tea` first, and stop.

Each `core` and `modules.tea` key is available as `{<key>}`, and as `config.<key>` in later steps. Replace `{project-root}` inside a value with the project root. Setup answers are strings: read `"true"` and `"false"` as booleans.

If `{tea-knowledge}/tea-index.csv` does not exist, the TEA knowledge base is not installed. Tell the user, offer to install it with `npx skills add bmad-code-org/bmad-method-test-architecture-enterprise --skill bmod-tea`, run that on a yes, and stop until it is there.

### Step 5: Greet the User

Greet `{user_name}`, speaking in `{communication_language}`.

### Step 6: Execute Append Steps

After greeting, execute each applicable append entry through the same individual durable hook protocol: framework `{workflow.activation_steps_append}` when scope includes framework, then `ci_workflow.activation_steps_append` when scope includes CI. Save each applicable phase in `activation_completed` after its entries succeed. Preserve the full journal and hook ledger through every scope and operation Resume.

Activation is complete. Begin the workflow below.

## Workflow Architecture

The existing framework steps at the skill root and the CI steps under `ci/` share scope and operation routing. `bmad-testarch-ci` is the compatibility entry point with CI scope preset. Both installed names and the TF/CI menu codes remain available.

Create and edit CI phases detect `ci/evaluation-ci-plan.json` and render it through `{skill-root}/ci/steps-c/step-03b-render-evaluation-plans.md`. Evaluate can continue invoking `bmad-testarch-ci` in create or edit mode.

## Initialization Sequence

Load `{skill-root}/resources/setup-routing.md` completely. Continue sections 2 through 4 after the read-only gate and canonical activation. Its checkpoint, customization, and completion rules apply to every step below. Do not repeat canonical activation or the scope question.

### Framework Phase

- **If C:** Load `{skill-root}/steps-c/step-01-preflight.md`
- **If R:** Load `{skill-root}/steps-c/step-01b-resume.md` only for a legacy Create checkpoint without a journal next position. Journal-backed Resume dispatches its saved C/E/V next file/subsection directly.
- **If V:** Load `{skill-root}/steps-v/step-01-validate.md`
- **If E:** Load `{skill-root}/steps-e/step-01-assess.md`

### CI Phase

CI settings and applicable activation hooks were handled in the activation stages above. Keep `{skill-root}` bound to the canonical framework directory; do not replay CI activation at phase handoff.

- **If C:** Load `{skill-root}/ci/steps-c/step-01-preflight.md`
- **If R:** Load `{skill-root}/ci/steps-c/step-01b-resume.md` only for a legacy Create checkpoint without a journal next position. Journal-backed Resume dispatches its saved C/E/V next file/subsection directly.
- **If V:** Load `{skill-root}/ci/steps-v/step-01-validate.md`
- **If E:** Load `{skill-root}/ci/steps-e/step-01-assess.md`

For both scope, the coordinator runs the applicable framework and CI phases under the same operation and agreed contract. Read `resources/setup-parallel.md` before concurrent generation. Every phase terminal loads `{skill-root}/resources/setup-phase-completion.md`; completion occurs after all requested phases satisfy their operation-specific completion criteria.
