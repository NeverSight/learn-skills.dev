---
name: wire-shared-package
description: "Add or repair an editable shared Python-package dependency across consuming projects, including clone-local configuration and verification. Use when multiple repositories must import the same local package source. Not for one project's ordinary environment setup; use $python-env."
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(uv*), Bash(ls*), Bash(mkdir*), AskUserQuestion
argument-hint: "<package-path> [--downstream project1,project2,...] [--tier 1|2]"
---

# Wire Shared Package

Wire a shared Python package as an editable local dependency across multiple research projects. Handles pyproject.toml creation, CLAUDE.md documentation, and Atlas infrastructure tracking.

## When to Use

- A shared package exists and needs to be wired into downstream projects
- "Add collusion-sim as a dependency to these projects"
- "Wire up the shared package"
- "Set up cross-project dependency"
- After creating a shared package with `computational-experiments` scaffold mode

## Phase 1: Discover

1. **Identify the shared package:**
   - Read its `pyproject.toml` to get name, version, and what it provides
   - Read its `CLAUDE.md` or `README.md` for module inventory
   - Confirm it installs cleanly: `uv pip install -e ".[dev]"`

2. **Identify downstream projects:**
   - If not specified, ask which projects should depend on this package
   - For each project, classify the dependency tier:

| Tier | Meaning | Action |
|------|---------|--------|
| **1 — Direct** | Uses the package's core modules in active code | Full wiring: `pyproject.toml` + CLAUDE.md + Atlas |
| **2 — Partial** | Will use specific modules when code work begins | CLAUDE.md note + Atlas only (no pyproject.toml yet) |
| **3 — Pattern only** | Borrows design patterns, no code dependency | Atlas note only |

3. **Check prerequisites for each downstream project:**
   - Does it have a `pyproject.toml`? (Tier 1 projects need one)
   - Does it have a `CLAUDE.md`? (all tiers need one)
   - Does it have an Atlas topic file? (locate via `project_path` in frontmatter)

## Phase 2: Wire Tier 1 Projects

For each Tier 1 downstream project:

### 2a. Create or update `pyproject.toml`

If no `pyproject.toml` exists, create one:

```toml
[project]
name = "{project-kebab-name}"
version = "0.1.0"
description = "{one-line from CLAUDE.md}"
requires-python = ">=3.11"
dependencies = [
    "{shared-package-name}",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "ruff>=0.3",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/{project_underscored_name}"]

[tool.ruff]
line-length = 99
target-version = "py311"

[tool.uv.sources]
{shared-package-name} = { path = "{relative-path-to-package}", editable = true }
```

If `pyproject.toml` already exists, add the dependency to `[project] dependencies` and add the `[tool.uv.sources]` entry.

**Key:** The `[tool.uv.sources]` section tells uv to resolve the package from a local path instead of PyPI. The relative path must be correct from the downstream project to the shared package (typically `../package-name`).

### 2b. Update CLAUDE.md

Add a "Shared Package Dependency" section under `## Setup`:

```markdown
### Shared Package Dependency
- **`{package-name}`** installed as editable dependency from `{relative-path}/`
- Provides: {list key modules this project uses}
- Install: `uv pip install -e ".[dev]"` (resolves {package-name} via `[tool.uv.sources]`)
- Project-specific code goes in `src/{project_name}/` — shared simulation code stays in {package-name}
```

### 2c. Verify install

```bash
cd "{project-path}" && uv pip install -e ".[dev]"
```

Then verify imports:

```bash
uv run python -c "from {package_module} import {key_class}; print('OK')"
```

## Phase 3: Document Tier 2 Projects

For each Tier 2 downstream project, add to CLAUDE.md under `## Setup`:

```markdown
### Shared Package Dependency (Tier 2)
- **`{package-name}`** at `{relative-path}/` — provides {what this project will use}
- When code work begins, add `{package-name}` as editable dependency via `[tool.uv.sources]` in `pyproject.toml`
- This project will extend the framework with {project-specific extensions}
```

No `pyproject.toml` changes — the dependency is documented but not yet wired.

## Phase 4: Track in Atlas

For each downstream project that has an Atlas topic file, add a `## Shared Infrastructure` section between the Description and Key References sections:

```markdown
## Shared Infrastructure

- **`{package-name}`** (Tier {N} — {direct reuse|partial reuse|pattern only}): {what components are used}
- Location: `{theme}/{package-dir}/`
{if Tier 1:}
- Install: editable dependency via `pyproject.toml` `[tool.uv.sources]`
```

**Placement:** After `## Description` (or `## Portfolio Bridge` if present), before `## Key References`.

**Finding the right topic file:** Search Atlas by `project_path` frontmatter field:

```bash
grep -rl "project_path.*{project-folder}" ~/vault/atlas/
```

## Phase 5: Update Shared Package Documentation

If the shared package has a `CLAUDE.md` or `README.md`, update its downstream project table to reflect all wired projects:

```markdown
## Downstream Projects

| Project | Tier | Uses |
|---------|------|------|
| {Project Name} | {1/2/3} | {components used} |
```

## Anti-Patterns

- **Never wire a dependency that doesn't install cleanly.** Verify `uv pip install -e .` on the shared package first.
- **Never create `pyproject.toml` for Tier 2 projects.** They don't have active code yet — premature wiring creates broken installs.
- **Never use absolute paths in `[tool.uv.sources]`.** Always use relative paths from the downstream project.
- **Never skip the Atlas update.** The whole point is cross-project tracking.
- **Never put the shared package's code in a downstream project.** Shared code stays in the shared package; project-specific code goes in the project's own `src/`.

## Verification

After completing all phases:

1. All Tier 1 projects install without errors
2. Key imports from the shared package work in each Tier 1 project
3. Every downstream project's CLAUDE.md mentions the dependency
4. Every downstream project's Atlas topic has a `## Shared Infrastructure` section
5. The shared package's documentation lists all downstream projects

Quick check: `grep -rl "{package-name}" ~/vault/atlas/` should return all expected topic files.

## Defaults

| Setting | Default | Override |
|---------|---------|----------|
| Build backend | hatchling | Specify in args |
| Python version | >=3.11 | Match shared package |
| Source layout | `src/` | Match shared package |
| Relative path | `../package-name` | Auto-detect from directory structure |
| Atlas section placement | After Description, before Key References | — |
