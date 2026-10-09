---
name: codependix-navigate
description: Answer dependency navigation and architecture questions using codependix CLI commands or committed graphs. Use when finding dependency paths between projects, files, or NestJS modules, tracing blast radius, determining what touches or imports a file or package, choosing narrowing flags to minimize run costs, or reading committed README diagrams across packages without running commands.
license: MIT
---

# Navigating a codebase with codependix

Codependix builds and queries dependency graphs across Nx workspaces, NestJS
containers, and file-level TypeScript and Python imports. When asking "how does X
reach Y?", "what breaks if I change Z?", or "what does this package depend
on?", use codependix commands to query relationships directly, or inspect
committed graphs already on disk.

## Command first: querying dependency paths

Reach for `codependix path` to trace directed dependency paths between two
nodes without parsing diagrams or grepping source files by hand.

```bash
# How does project-a reach project-c?
codependix path project-a project-c

# How does one file import another?
codependix path src/modules/auth/auth.service.ts src/modules/users/user.entity.ts

# What NestJS modules connect two modules in a container?
codependix path AuthModule DatabaseModule
```

### Path query flags and narrowing

Running across a full workspace can be expensive because it parses Nx projects,
TypeScript ASTs, and container registrations across the entire monorepo. Use
narrowing flags to scope the run and minimize execution time:

| Flag | Purpose |
| ---- | ------- |
| `-f, --format <format>` | Output format: `markdown` (default), `json`, or `mermaid` |
| `--nx-projects` / `--no-nx-projects` | Toggle Nx workspace project dependency graph search |
| `--file-imports` / `--no-file-imports` | Toggle internal file-level import graph search |
| `--nestjs-modules` / `--no-nestjs-modules` | Toggle NestJS container module graph search |
| `--projects <names>` | Comma-separated project names or globs to search across |
| `-d, --directory <dir>` | Directory whose Nx workspace to read |
| `--include <globs>` / `--exclude <globs>` | Override configured project inclusion or exclusion globs |
| `--tags <tags>` | Comma-separated Nx project tags to filter by |
| `--config <path>` | Path to a specific `codependix.config.ts` |

### Path results

- **Path found**: Prints the shortest directed path connecting `<from>` to
  `<to>` (for example `project-a → project-b → project-c`).
- **No path**: Reports `_No path connects "<from>" to "<to>"._` (or an empty
  list in JSON) and exits 0. A missing path is an answer, not an error.

## When to read a committed diagram instead of running the CLI

Running the CLI builds graph representations from source files. Before running
a command, check if the question is already answered by committed artifacts on
disk:

1. **Every package in the monorepo commits its own graphs.** Look in any
   project's `README.md` under the `## 🕸️ Codependix` section or between
   `<!-- codependix:start name="..." -->` markers.
2. **Immediate blast radius (1 hop):** The project's committed **Nx
   Neighborhood** diagram lists all immediate `dependencies` (what it reaches)
   and `dependents` (what breaks if its public API changes).
3. **Internal file structure:** The project's committed **File import graph**
   lists all file-to-file imports and isolated files within that project.
4. **Container structure:** The project's committed **NestJS module graph**
   lists wired container modules.
5. **Whole-workspace structure:** The repository root `README.md` carries the
   committed workspace graph.

**Cost rule of thumb:**

- **Read README diagrams or JSON** for single-hop dependencies, immediate blast
  radius, or local file layout (zero build cost, instant answer on disk).
- **Run `codependix path`** for multi-hop transitive paths, cross-project
  reachability, verifying unstaged changes, or generating machine-readable JSON.

## The four graph types and their questions

| Graph | Scope | Answers |
| ----- | ----- | ------- |
| **Nx Neighborhood** | Project | What one project reaches (dependencies) and who breaks if it changes (dependents) |
| **Workspace graph** | Workspace | High-level architectural layering and cross-package relationships |
| **NestJS module graph** | Container | What modules the DI container wires together at runtime |
| **File import graph** | Project files | File-to-file import relationships, cycles, and local refactoring fan-out |

## Interpreting graph artifacts

### Nx Neighborhood: blast radius

A Neighborhood covers **one hop in each direction** from the focal project
(highlighted in diagrams):

- **`dependents` is the blast radius** of a breaking change: every listed
  project must build against the new shape. For breaking changes spanning
  deeper layers, walk outward neighborhood by neighborhood or run `codependix
  path`.
- **`dependencies` is the allowed surface:** A project may only import what is
  declared here.
- Edges marked `implicit` are Nx workspace configuration dependencies rather
  than code imports.

### File import graph: refactoring and moves

Edges are strictly **between files inside the same project**:

- External packages and cross-project imports are excluded by design (they live
  in the Nx Neighborhood).
- **`isolatedFileNames` is a shortlist to investigate, not dead code.** An
  isolated file may be an entry point, an external export, or a configuration
  file.
- **Cycles are real:** An import cycle within a project produces runtime
  `undefined` bindings or initialization order bugs. Walk the cycle edges to
  locate where to decouple.
- Renaming a file? Edges pointing to the old relative path show the exact blast
  radius.

### NestJS module graph: DI container wiring

Built by evaluating container modules:

- **Global or ambient modules:** Modules imported by nearly all others (for
  example core logging or configuration) have individual edges omitted to
  reduce visual noise; they are listed under `ambientModuleNames` and drawn
  with rounded corners.
- **Dynamic wrapper modules:** Private internal host modules created by
  `forRoot` or dynamic providers are collapsed into the declaring module.
- A missing module was never registered in the container hierarchy, meaning
  its exported providers are unavailable.

## Confirming freshness before trusting committed graphs

A committed graph reflects the repository state at the last `codependix map
--write`. To check whether committed graphs are up to date:

```bash
# Check if any committed reports are stale without modifying files
codependix map --check reports

# Update all committed graphs across the workspace
codependix map --write
```

If committed graphs are stale with respect to recent local edits, either
re-run `codependix map --write` or use `codependix path` for real-time queries.
