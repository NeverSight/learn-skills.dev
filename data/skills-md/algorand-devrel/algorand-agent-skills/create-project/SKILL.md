---
name: create-project
description: Bootstraps production-ready AlgoKit projects for Algorand dApps and smart contracts. Use when initializing new Algorand smart contract projects, setting up development environments from scratch, or scaffolding dApps with pre-configured tooling. Strong triggers include "create a new project", "initialize a new Algorand app", "start a new smart contract", "set up AlgoKit", "scaffold a dApp", "algokit init".
---

# AlgoKit Project Initialization

Create new Algorand projects using AlgoKit's official templates.

## Overview / Core Workflow

1. Confirm project details with user (name, template, customizations)
2. Run `algokit init` with appropriate flags
3. Handle any initialization errors
4. Provide next steps for building/testing

## How to proceed

1. **Confirm project details with user:**
   - Project name (directory name)
   - Template choice (TypeScript or Python)
   - Any customizations (`--no-git`, `--no-bootstrap`, author name)
   - For TypeScript: confirm Production preset for production projects

2. **Run initialization command:**

   **TypeScript (Production Preset):**

   ```bash
   algokit init -n <project-name> -t typescript --answer preset_name production --answer author_name "<name>" --defaults
   ```

   **TypeScript (Starter Preset):**

   ```bash
   algokit init -n <project-name> -t typescript --answer author_name "<name>" --defaults
   ```

   **Python (Production Preset):**

   ```bash
   algokit init -n <project-name> -t python --answer preset_name production --answer author_name "<name>" --defaults
   ```

   **Python (Starter Preset):**

   ```bash
   algokit init -n <project-name> -t python --answer author_name "<name>" --defaults
   ```

   **With custom options (no git, no bootstrap):**

   ```bash
   algokit init -n <project-name> -t typescript --no-git --no-bootstrap --defaults
   ```

3. **Handle errors:**
   - Check if project directory already exists
   - Verify AlgoKit is installed: `algokit --version`
   - Ensure target directory is writable
   - Valid templates: `typescript`, `python`, `tealscript`, `react`, `fullstack`, `base`

4. **Provide next steps:**
   - `cd <project-name>`
   - `algokit project run build` — Compile contracts
   - `algokit project run test` — Run test suite
   - `algokit localnet start` — Start local network (if deploying)
   - `algokit project run deploy` — Deploy contracts to local network

## Important Rules / Guidelines

- **Always confirm with user before executing** — Never run `algokit init` without explicit confirmation
- **Default to TypeScript** — Recommended for production applications
- **Use production preset** — For any project because it includes testing framework and deployment scripts
- **Include author name** — Pass `--answer author_name "<name>"` for attribution
- **Use `--defaults`** — Accepts all other default values for non-interactive mode

## Common Variations / Edge Cases

| Scenario | Approach |
|----------|----------|
| Python with TypeScript deployment | `--answer deployment_language "typescript"` |
| Existing directory | Check and warn if directory already exists |
| No Git initialization | Use `--no-git` flag |
| No dependency installation | Use `--no-bootstrap` flag |
| Custom author name | `--answer author_name "Your Name"` |
| Fullstack (frontend + contracts) | Use `-t fullstack` template |
| React frontend only | Use `-t react` template |
| Standalone (no workspace) | Use `--no-workspace` flag |
| Initialize from example | Use `algokit init example` subcommand |

## References / Further Reading

- [CLI Reference](./references/REFERENCE.md)
- [AlgoKit CLI Init Documentation](https://dev.algorand.co/algokit/cli/init/)
- [AlgoKit CLI Init Reference](https://dev.algorand.co/reference/algokit-cli#init)
