---
name: pkg
description: Manage MTHDS packages — initialize, add dependencies, lock, install, and update. Use when user says "init package", "add dependency", "install dependencies", "lock deps", "update packages", "set up METHODS.toml", "manage packages", "mthds init", or wants to manage MTHDS package dependencies.
---

# Manage MTHDS packages

Initialize, add dependencies, lock, install, update, and validate MTHDS packages using the `mthds` CLI.

## Process

**Prerequisite**: See [CLI Prerequisites](../shared/prerequisites.md)

### 1. Initialize a package

Create a `METHODS.toml` manifest:

```bash
mthds package init --directory <pkg-dir>
```

Use `--force` to overwrite an existing manifest:

```bash
mthds package init --force --directory <pkg-dir>
```

### 2. Configure exports

Exports declare which pipes the package makes available to consumers. They are organized by **domain** in `METHODS.toml`:

```toml
[exports.restaurant_analysis]
pipes = ["present_restaurant", "extract_menu", "analyze_menu"]
```

To configure exports:

1. Read the `.mthds` bundle(s) in the package to find the domain codes and pipe codes defined inside them
2. Edit `METHODS.toml` to add an `[exports.<domain>]` section for each domain, listing the pipe codes to export

Rules:

- The `main_pipe` of each bundle is auto-exported — you do not need to list it unless you want to be explicit
- Concepts are always public and do not need to be listed in exports
- Each `[exports.<domain>]` section requires a `pipes` key with a list of pipe code strings

### 3. Add dependencies

Add a dependency to the manifest:

```bash
mthds package add <address> --directory <pkg-dir>
```

Options:

| Flag | Purpose | Example |
|------|---------|---------|
| `--alias` | Set a local alias for the dependency | `mthds package add github.com/org/repo --alias mylib --directory <pkg-dir>` |
| `--version` | Pin a specific version | `mthds package add github.com/org/repo --version 1.2.0 --directory <pkg-dir>` |
| `--path` | Use a local path dependency | `mthds package add ./local-pkg --path --directory <pkg-dir>` |

### 4. Lock dependencies

Resolve all dependencies and generate a lockfile:

```bash
mthds package lock --directory <pkg-dir>
```

### 5. Install from lockfile

Install dependencies from the existing lockfile:

```bash
mthds package install --directory <pkg-dir>
```

### 6. Update dependencies

Re-resolve dependencies and update the lockfile:

```bash
mthds package update --directory <pkg-dir>
```

### 7. List package manifest

Display the current package manifest:

```bash
mthds package list --directory <pkg-dir>
```

### 8. Validate package manifest

Validate the `METHODS.toml` package manifest:

```bash
mthds package validate --directory <pkg-dir>
```

Options:

| Flag | Purpose | Example |
|------|---------|---------|
| `--all` | Validate all packages in the workspace | `mthds package validate --all --directory <pkg-dir>` |
| `--runner` / `-r` | Specify the runner for validation | `mthds package validate --all -r pipelex --directory <pkg-dir>` |

Target a specific package:

```bash
mthds package validate <target> --directory <pkg-dir>
```

> **Note**: `mthds package validate` validates the `METHODS.toml` package manifest. To validate `.mthds` bundle semantics, use `mthds-agent pipelex validate pipe` (see /check skill).

## The `--directory` option

All `mthds package` commands accept `--directory <path>` (short: `-d`) to target a package directory other than the shell's current working directory. This is essential when the agent's CWD differs from the package location.

```bash
# From any directory, target a specific package
mthds package init --directory mthds-wip/restaurant_presenter/
mthds package validate --directory mthds-wip/restaurant_presenter/
```

If `--directory` is omitted, commands default to the current working directory.

## Common Workflows

**Starting a new package**:
1. `mthds package init --directory <pkg-dir>` — create the manifest
2. Read `.mthds` bundles in the package to extract domain codes and pipe codes
3. Edit `METHODS.toml` to set the correct address, description, and `[exports.<domain>]` sections
4. `mthds package validate --directory <pkg-dir>` — validate the manifest

**Adding dependencies to an existing package**:
1. `mthds package add <address> --directory <pkg-dir>` — add the dependency
2. `mthds package lock --directory <pkg-dir>` — resolve and lock
3. `mthds package install --directory <pkg-dir>` — install from lockfile

**Updating dependencies**:
1. `mthds package update --directory <pkg-dir>` — re-resolve and update lockfile
2. `mthds package install --directory <pkg-dir>` — install updated deps

## Reference

- [CLI Prerequisites](../shared/prerequisites.md) — read at skill start to check CLI availability
- [Error Handling](../shared/error-handling.md) — read when CLI returns an error to determine recovery
- [MTHDS Agent Guide](../shared/mthds-agent-guide.md) — read for CLI command syntax or output format details
