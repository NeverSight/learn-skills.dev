---
name: "speckit"
description: "Complete guide and CLI reference for Spec Kit (specify CLI) and Zero-Clone Spec-Driven Development (SDD). Use when initializing projects, running specify CLI commands, managing feature specs in docs/specs/, or explaining Spec Kit installation and workflows to the user."
argument-hint: "Ask about specify CLI commands, installation, or SDD workflow"
compatibility: "Works with specify CLI (installed via uv tool install or run on the fly via uvx)"
metadata:
  author: "github-spec-kit"
  source: "README.md"
user-invocable: true
disable-model-invocation: false
---

# Spec Kit (`specify` CLI) Reference & Guide

Spec Kit is a **zero-clone, zero-footprint** toolkit for Spec-Driven Development (SDD).
- **Zero repository pollution**: You never need to clone the `spec-kit` repo into a project, and `specify init` does **not** copy internal shell scripts (`.specify/scripts/`), templates (`.specify/templates/`), or workflows into your repository.
- **Clean specification directory**: All feature specifications, implementation plans, and task lists live under `docs/specs/<NNN>-<feature-name>/` (with automatic fallback to `specs/` if already present in the repository root).
- **Direct CLI execution**: All templates and feature state are resolved in memory directly by the `specify` CLI.

---

## 1. Installing & Running the `specify` CLI

If `specify` is not yet installed on `PATH`, install it or run it ephemerally with `uv`:

### Option A: Install Globally with `uv` (Recommended)
```bash
uv tool install specify-cli --from git+https://github.com/juftin/spec-kit.git
```

### Option B: Run On-the-Fly with `uvx` (No Permanent Install Needed)
Any `specify <subcommand>` can be run without prior installation by prefixing with:
```bash
uvx --from git+https://github.com/juftin/spec-kit.git specify <subcommand>
```

### Option C: Install Locally (Development / Editable)
```bash
git clone https://github.com/juftin/spec-kit.git
cd spec-kit
uv tool install --editable .
# or: pip install -e .
```

### Option D: Install Agent Skills Globally via `npx skills`
```bash
npx skills add juftin/spec-kit -g
```
Installs `/speckit` and `/speckit-*` skills globally into your coding agent (Claude Code, Cursor, GitHub Copilot, etc.).

---

## 2. Core `specify` CLI Commands

### Project Initialization & Environment Check

| Command | Description |
| --- | --- |
| `specify init [PATH] --integration <agent>` | Initialize a project in clean zero-footprint mode (`--bare` is default). Writes `.specify/init-options.json` and agent skills without copying internal scripts or templates. |
| `specify init . --integration copilot` | Initialize Spec Kit in the current directory (`--here`). |
| `specify init . --scaffold --script sh` | Legacy scaffold mode: copies `.specify/scripts/` and `.specify/templates/` into the repo. |
| `specify check` | Check that required developer and agent tools are installed. |
| `specify version [--json]` | Print the installed Specify CLI version and runtime info. |

### Zero-Clone SDD Workflow Commands (`feature`, `plan`, `tasks`, `template`)

| Command | Description |
| --- | --- |
| `specify feature init <name> [--json]` | Create a new sequentially numbered feature directory `docs/specs/<NNN>-<name>/`, populate `spec.md` from the composed `spec-template`, and set `.specify/feature.json` to point to the active feature. |
| `specify feature current [--json]` | Print the currently active feature directory from `.specify/feature.json`. |
| `specify feature check [--json] [OPTIONS]` | Validate feature prerequisites and return `FEATURE_DIR` and `AVAILABLE_DOCS`. Flags: `--paths-only`, `--require-spec`, `--require-tasks`, `--include-tasks`, `--template <name>`. |
| `specify plan setup [--json]` | Preflight `spec.md` in the active feature directory, idempotently create `plan.md` from `plan-template`, and output `FEATURE_DIR`, `FEATURE_SPEC`, `IMPL_PLAN`, and `BRANCH`. |
| `specify tasks setup [--json]` | Preflight `plan.md` in the active feature directory, idempotently create `tasks.md` from `tasks-template`, and output `FEATURE_DIR`, `IMPL_PLAN`, `TASKS_FILE`, `AVAILABLE_DOCS`, and `TASKS_TEMPLATE_CONTENT`. |
| `specify template <name> [--json]` | Resolve and output any template (`spec-template`, `plan-template`, `tasks-template`, `checklist-template`, `constitution-template`) in memory across project overrides, presets, extensions, and core pack. |

### Integrations, Extensions, Presets & Workflows

| Command Group | Key Subcommands | Description |
| --- | --- | --- |
| `specify integration` | `list`, `install [--global] <agent>`, `use <agent>`, `switch <agent>`, `status`, `upgrade`, `uninstall` | Manage coding agent integrations locally in the project or globally (`--global` / `-g`). |
| `specify extension` | `list`, `search`, `info`, `add <name>`, `remove <name>`, `enable`, `disable`, `update` | Install and manage modular extensions (e.g., `specify extension add bug`, `specify extension add assess`, `specify extension add git`). |
| `specify preset` | `list`, `search`, `info`, `add <name>`, `remove <name>`, `resolve <template>` | Manage template/command presets and inspect composed template layers. |
| `specify workflow` | `list`, `run <id>`, `resume <run_id>`, `status`, `definition`, `add`, `remove` | Execute and inspect automated multi-step SDD workflows. |
| `specify artifact` | `list [--json]`, `info <id> [--json]` | Inspect which layer (core, extension, preset, override) supplies any command, template, script, or hook. |

---

## 3. End-to-End Spec-Driven Development (SDD) Flow

Run these skills in your coding agent chat in order, reviewing each artifact under `docs/specs/<NNN>-<feature>/` before continuing:

1. **`/speckit-constitution`** — Establish or update project governance principles in `.specify/memory/constitution.md` (resolved via `specify template constitution-template --json`).
2. **`/speckit-specify <description>`** — Create `docs/specs/<NNN>-<feature>/spec.md` and `.specify/feature.json` (via `specify feature init <name> --json` or `specify template spec-template --json`).
3. **`/speckit-clarify`** *(optional)* — Identify up to 5 high-impact underspecified areas in `spec.md` and encode answers directly into the spec (uses `specify feature check --json --paths-only`).
4. **`/speckit-plan <tech stack / constraints>`** — Generate `plan.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md` in the active feature directory (uses `specify plan setup --json`).
5. **`/speckit-checklist <domain>`** *(optional)* — Generate a requirements-quality checklist under `checklists/` (uses `specify feature check --json --template checklist-template`).
6. **`/speckit-tasks`** — Generate a dependency-ordered `tasks.md` organized by user story (uses `specify tasks setup --json`).
7. **`/speckit-analyze`** *(optional)* — Run a non-destructive cross-artifact consistency check across `spec.md`, `plan.md`, and `tasks.md` (uses `specify feature check --json --require-spec --require-tasks --include-tasks`).
8. **`/speckit-implement`** — Execute the implementation plan phase-by-phase according to `tasks.md` (uses `specify feature check --json --require-tasks --include-tasks`).
9. **`/speckit-converge`** — Audit the implementation against `spec.md`, `plan.md`, and `tasks.md`, appending any remaining gaps to `tasks.md` until `Converged`.

---

## 4. Directory Layout Created in User Repositories

```text
<project-root>/
├── .specify/
│   ├── init-options.json       # Minimal project settings ("footprint": "bare")
│   ├── feature.json            # Active feature pointer: {"feature_directory": "docs/specs/001-..."}
│   └── memory/
│       └── constitution.md     # Project constitution (when created)
└── docs/
    └── specs/
        └── 001-feature-name/
            ├── spec.md         # Feature specification (/speckit-specify)
            ├── plan.md         # Implementation plan (/speckit-plan)
            ├── research.md     # Phase 0 research (/speckit-plan)
            ├── data-model.md   # Phase 1 data model (/speckit-plan)
            ├── quickstart.md   # Phase 1 validation scenarios (/speckit-plan)
            ├── contracts/      # API/interface contracts (/speckit-plan)
            ├── checklists/     # Quality checklists (/speckit-specify, /speckit-checklist)
            └── tasks.md        # Actionable task list (/speckit-tasks)
```
