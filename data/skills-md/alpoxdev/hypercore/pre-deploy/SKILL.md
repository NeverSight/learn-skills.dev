---
name: pre-deploy
description: Validate and fix quality/build blockers before deployment for Node.js, Rust, and Python projects.
allowed-tools: Bash Read Edit mcp__sequential-thinking__sequentialthinking
compatibility: Requires local toolchains for at least one supported stack (node/rust/python) and scripts under skills/pre-deploy/scripts.
---

# Pre-Deploy Skill

> Cross-stack pre-deploy validation and remediation for node/rust/python.

<scripts>

## Available scripts

| Script | Purpose |
|------|------|
| `scripts/stack-detect.sh` | Detect project stacks (`node`, `rust`, `python`) |
| `scripts/deploy-check.sh` | Full verification (`lint/type checks + build`) |
| `scripts/lint-check.sh` | Run stack-specific quality checks |
| `scripts/build-run.sh` | Run stack-specific build phase |
| `scripts/pm-detect.sh` | Node package manager detection (`npm/yarn/pnpm/bun`) |

</scripts>

<workflow>

## Workflow

### Full validation (recommended)

```bash
scripts/deploy-check.sh
```

### Step-by-step validation

```bash
# 1) quality checks
scripts/lint-check.sh

# 2) build phase
scripts/build-run.sh
```

### Stack behavior summary

- **Node.js**: typecheck/lint (if configured) + build script (if configured)
- **Rust**: `cargo fmt --check` + `cargo clippy` + `cargo check` + `cargo build --release`
- **Python**: lint (`ruff`/`flake8` if available) + type/syntax check (`mypy` or `compileall`) + build (`poetry build` or `python -m build`, fallback `compileall`)

</workflow>

<required>

| Category | Required |
|------|------|
| **Thinking** | Use Sequential Thinking (3-5 steps per issue) |
| **Tracking** | Track failures with TodoWrite |
| **Strategy** | Run stack checks -> fix sequentially -> rerun checks -> run build |
| **Validation** | Re-check affected targets after each edit |
| **Completion** | Confirm deploy-check passes before completion |

</required>

<execution_plan>

1. Run `scripts/deploy-check.sh`
2. Convert errors into TodoWrite items by stack and priority
3. For each issue:
   - Run sequential-thinking
   - Apply focused fix
   - Re-run relevant check
4. Re-run full deploy check
5. Report final status and remaining risks

</execution_plan>
