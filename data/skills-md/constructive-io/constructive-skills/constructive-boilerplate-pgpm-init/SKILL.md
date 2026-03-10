---
name: constructive-boilerplate-pgpm-init
description: Initialize workspaces and modules using the pgpm init command. Supports PGPM (PostgreSQL) and PNPM (TypeScript/JavaScript) templates, interactive and non-interactive modes, and custom template repositories. Use when scaffolding a new workspace or module with pgpm init.
---

Initialize workspaces and modules using the `pgpm init` command. Supports PGPM (PostgreSQL) and PNPM (TypeScript/JavaScript) templates, interactive and non-interactive modes, and custom template repositories.

## When to Apply

Use this skill when:
- Scaffolding a new workspace or module with `pgpm init`
- Using `--template`, `--boilerplate`, or `-w` flags
- Setting up non-interactive `pgpm init` for CI/CD
- Using custom template repositories (e.g., `constructive-io/sandbox-templates`)

## Basic Commands

### Create a Workspace

```bash
pgpm init workspace
```

Creates a new PGPM workspace with `pgpm.json`, `pnpm-workspace.yaml`, `lerna.json`, GitHub Actions workflows, Jest testing setup, and TypeScript configuration.

### Create a Module

```bash
# Inside a workspace
pgpm init

# Or explicitly
pgpm init module
```

Creates a new PGPM module with `pgpm.plan`, `.control` file, `package.json`, `__tests__/`, and `deploy/`, `revert/`, `verify/` directories.

### Create Workspace + Module in One Command

```bash
# Create workspace first, then module inside it
pgpm init -w

# With a specific template variant
pgpm init --dir pnpm -w
pgpm init --template pnpm/module -w
```

The `-w` (or `--create-workspace`) flag creates a workspace first, then automatically creates the module inside it. Useful when starting from scratch outside any workspace.

## Available Templates

### Default Repository (`constructive-io/pgpm-boilerplates`)

#### PGPM Variant (Default)

| Template | Command | Description |
|----------|---------|-------------|
| `pgpm/workspace` | `pgpm init workspace` or `pgpm init -t pgpm/workspace` | PGPM workspace with pgpm.json, migrations support |
| `pgpm/module` | `pgpm init` or `pgpm init -t pgpm/module` | PGPM module with pgpm.plan, .control file |

#### PNPM Variant (Pure TypeScript/JavaScript)

| Template | Command | Description |
|----------|---------|-------------|
| `pnpm/workspace` | `pgpm init workspace --dir pnpm` or `pgpm init -t pnpm/workspace` | Pure PNPM workspace (no pgpm files) |
| `pnpm/module` | `pgpm init --dir pnpm` or `pgpm init -t pnpm/module` | Pure PNPM package (no pgpm.plan/.control) |

### PGPM Templates (pgpm/)

Use for PostgreSQL extension development with migrations:

```bash
pgpm init workspace
pgpm init -t pgpm/workspace
pgpm init -t pgpm/module -w
```

**Creates:** `pgpm.json` / `pgpm.config.js` (workspace), `pgpm.plan` (module), `.control` file (module), migration directories: `deploy/`, `revert/`, `verify/`

### PNPM Templates (pnpm/)

Use for pure TypeScript/JavaScript packages without PostgreSQL:

```bash
pgpm init workspace --dir pnpm
pgpm init -t pnpm/workspace
pgpm init -t pnpm/module -w
```

**Creates:** `pnpm-workspace.yaml` (workspace), `lerna.json` (workspace), standard `package.json`, `src/`, `__tests__/` directories. No pgpm-specific files.

## Using --template (Recommended)

The `--template` flag (or `-t`) provides a cleaner syntax by combining the directory variant and template type into a single path:

```bash
# These are equivalent:
pgpm init workspace --dir pnpm
pgpm init --template pnpm/workspace

# These are equivalent:
pgpm init module --dir pnpm
pgpm init --template pnpm/module

# Short form with -t alias
pgpm init -t pgpm/module
pgpm init -t pnpm/workspace
```

The `--template` flag parses the path by splitting on the first `/`:
- Everything before the slash becomes the `--dir` value
- Everything after becomes the template type (workspace/module)

## Using --boilerplate

```bash
# Interactive selection from all available templates
pgpm init --boilerplate

# Select a specific template path
pgpm init pnpm/workspace --boilerplate
```

When using `--boilerplate` in CI/CD, you must specify the template path:

```bash
# This will error in non-interactive mode
pgpm init --boilerplate --no-tty  # ERROR

# Correct: specify the template path
pgpm init pnpm/workspace --boilerplate --no-tty \
  --name my-workspace \
  --fullName "Your Name" \
  --email "you@example.com" \
  --username your-github-username \
  --license MIT
```

## Custom Template Repositories

```bash
# Use a different repository
pgpm init workspace --repo owner/repo
pgpm init workspace --repo https://github.com/owner/repo.git

# Use a specific branch
pgpm init workspace --repo owner/repo --from-branch develop

# Example: Constructive Next.js app template
pgpm init -w --repo constructive-io/sandbox-templates --template nextjs/constructive-app
```

## Non-Interactive Mode

For CI/CD pipelines and automation, use `--no-tty` or set `CI=true`:

```bash
pgpm init workspace --no-tty \
  --name my-workspace \
  --fullName "Your Name" \
  --email "you@example.com" \
  --username your-github-username \
  --license MIT
```

### Required Parameters for Non-Interactive Workspace

| Parameter | Description |
|-----------|-------------|
| `--name` | Workspace name (becomes directory name) |
| `--fullName` | Author's full name |
| `--email` | Author's email |
| `--username` | GitHub username |
| `--license` | License (MIT, Apache-2.0, etc.) |

### Required Parameters for Non-Interactive Module

| Parameter | Description |
|-----------|-------------|
| `--moduleName` | Module name |
| `--moduleDesc` | Module description |
| `--fullName` | Author's full name |
| `--email` | Author's email |
| `--username` | GitHub username |
| `--repoName` | Repository name |
| `--license` | License |
| `--access` | npm access level (public/restricted) |
| `--extensions` | PostgreSQL extensions (comma-separated) |

Example:

```bash
pgpm init --no-tty \
  --moduleName my-module \
  --moduleDesc "My PostgreSQL module" \
  --fullName "Your Name" \
  --email "you@example.com" \
  --username your-github-username \
  --repoName my-workspace \
  --license MIT \
  --access public \
  --extensions "plpgsql,uuid-ossp"
```

## Workspace Type Requirements

Templates specify what type of workspace they require via `requiresWorkspace`:

| Value | Meaning |
|-------|---------|
| `"pgpm"` | Must be inside a PGPM workspace (has pgpm.json) |
| `"pnpm"` | Must be inside a PNPM workspace (has pnpm-workspace.yaml) |
| `"lerna"` | Must be inside a Lerna workspace (has lerna.json) |
| `"npm"` | Must be inside an npm workspace (package.json with workspaces) |
| `false` | Can be created anywhere |

## CLI Options

| Option | Description |
|--------|-------------|
| `--help, -h` | Show help message |
| `--cwd <directory>` | Working directory (default: current directory) |
| `--repo <repo>` | Template repository (default: constructive-io/pgpm-boilerplates) |
| `--from-branch <branch>` | Branch/tag to use when cloning repo |
| `--dir <variant>` | Template variant directory (e.g., pnpm, supabase) |
| `--template, -t <path>` | Full template path (e.g., pnpm/module) - combines dir and type |
| `--boilerplate` | Prompt to select from available boilerplates |
| `--create-workspace, -w` | Create a workspace first, then create the module inside it |
| `--no-tty` | Run in non-interactive mode |

Note: The `-W` flag is used for the interactive workspace recovery prompt (when you run `pgpm init` outside a workspace and it asks if you want to create one).

## Workflow Examples

### Starting a New Project

```bash
# 1. Create workspace
pgpm init workspace
cd my-workspace

# 2. Create first module
pgpm init
cd packages/my-module

# 3. Add a database change
pgpm add my_first_change

# 4. Deploy to database
pgpm deploy --createdb
```

### Quick Start with -w Flag

```bash
# Create workspace + module in one command
pgpm init -w
# Prompts for workspace name, then module name
# Creates workspace and module inside packages/

# With PNPM template variant
pgpm init --template pnpm/module -w
```

### Create a Pure TypeScript Monorepo

```bash
# 1. Create PNPM workspace
pgpm init workspace --dir pnpm
cd my-workspace

# 2. Create packages
pgpm init --dir pnpm  # Creates TypeScript package
```

### CI/CD Pipeline Setup

```yaml
# .github/workflows/setup.yaml
jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - name: Install pgpm
        run: npm install -g pgpm

      - name: Create workspace
        run: |
          pgpm init workspace --no-tty \
            --name test-workspace \
            --fullName "CI Bot" \
            --email "ci@example.com" \
            --username ci-bot \
            --license MIT
```

## Template Caching

Templates are cached locally under `~/.pgpm/cache/repos` with a one-day TTL. To force a fresh pull:

```bash
pgpm cache clean
```

## Best Practices

1. Use `--template` (or `-t`) for specifying templates — cleaner than `--dir` + positional arg
2. Use `-w` flag to create workspace + module in one command when starting fresh
3. Use `--no-tty` in CI/CD pipelines to avoid hanging on prompts
4. Pin template versions with `--from-branch` for reproducible builds
5. Use `--boilerplate` when exploring available templates interactively
6. Create organization-specific boilerplates for standardized project setup
7. Use `pgpm cache clean` if templates seem outdated
