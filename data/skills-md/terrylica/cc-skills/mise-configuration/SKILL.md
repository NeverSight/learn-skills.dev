---
name: mise-configuration
description: "Configure environment variables and project settings using mise [env] as the single source of truth. Use whenever the user needs to set up mise.toml, centralize environment variables, configure Python venvs through mise, use mise templates, or structure hub-spoke and monorepo mise configurations with subfolder overrides. Do NOT use for mise task orchestration (use mise-tasks instead) or for runtime version management unrelated to environment configuration."
allowed-tools: Read, Bash, Glob, Grep, Edit, Write
---

# mise Configuration as Single Source of Truth

Use mise `[env]` as centralized configuration with backward-compatible defaults.

## When to Use This Skill

Use this skill when:

- Centralizing environment variables in mise.toml
- Setting up Python venv auto-creation with mise
- Implementing hub-spoke configuration for monorepos
- Creating backward-compatible environment patterns

## Core Principle

Define all configurable values in `.mise.toml` `[env]` section. Scripts read via environment variables with fallback defaults. Same code path works WITH or WITHOUT mise installed.

**Key insight**: mise auto-loads `[env]` values when shell has `mise activate` configured. Scripts using `os.environ.get("VAR", "default")` pattern work identically whether mise is present or not.

## Quick Reference

### Language Patterns

| Language   | Pattern                            | Notes                       |
| ---------- | ---------------------------------- | --------------------------- |
| Python     | `os.environ.get("VAR", "default")` | Returns string, cast if int |
| Bash       | `${VAR:-default}`                  | Standard POSIX expansion    |
| JavaScript | `process.env.VAR \|\| "default"`   | Falsy check, watch for "0"  |
| Go         | `os.Getenv("VAR")` with default    | Empty string if unset       |
| Rust       | `std::env::var("VAR").unwrap_or()` | Returns Result<String>      |

### Special Directives

| Directive       | Purpose                 | Example                                             |
| --------------- | ----------------------- | --------------------------------------------------- |
| `_.file`        | Load from .env files    | `_.file = ".env"`                                   |
| `_.path`        | Extend PATH             | `_.path = ["bin", "node_modules/.bin"]`             |
| `_.source`      | Execute bash scripts    | `_.source = "./scripts/env.sh"`                     |
| `_.python.venv` | Auto-create Python venv | `_.python.venv = { path = ".venv", create = true }` |

For detailed directive examples with options (redact, tools, multi-file): [Code Patterns](./references/patterns.md#special-directives)

## Python Venv Auto-Creation (Critical)

Auto-create and activate Python virtual environments:

```toml
[env]
_.python.venv = { path = ".venv", create = true }
```

This pattern is used in ALL projects. When entering the directory with mise activated:

1. Creates `.venv` if it doesn't exist
2. Activates the venv automatically
3. Works with `uv` for fast venv creation

**Alternative via [settings]**:

```toml
[settings]
python.uv_venv_auto = true
```

## Hub-Spoke Architecture (CRITICAL)

Keep root `mise.toml` lean by delegating domain-specific tasks to subfolder `mise.toml` files. Applies to monorepos, ML/research projects, infrastructure, and data pipelines.

**Key rules**:

- Hub owns `[tools]` and orchestration tasks
- Spokes inherit hub's `[tools]` automatically
- Spoke `[env]` extends hub's `[env]` (can override per domain)
- `.mise.local.toml` applies at directory level (secrets stay local)

**Full guide with directory structures, examples, and anti-patterns**: [Hub-Spoke Architecture](./references/hub-spoke-architecture.md)

> **Wiki Reference**: [Pattern-mise-Configuration](https://github.com/terrylica/cc-skills/wiki/Pattern-mise-Configuration)

## Monorepo Workspace Pattern

For Python monorepos using `uv` workspaces, the venv is created at the **workspace root**. Dev dependencies should be hoisted to root `pyproject.toml` using `[dependency-groups]` (PEP 735).

**Full guide**: [Monorepo Workspace Pattern](./references/monorepo-workspace.md)

## Template Syntax (Tera)

mise uses Tera templating. Delimiters: `{{ }}` expressions, `{% %}` statements, `{# #}` comments.

### Built-in Variables

| Variable              | Description                     |
| --------------------- | ------------------------------- |
| `{{config_root}}`     | Directory containing .mise.toml |
| `{{cwd}}`             | Current working directory       |
| `{{env.VAR}}`         | Environment variable            |
| `{{mise_bin}}`        | Path to mise binary             |
| `{{mise_pid}}`        | mise process ID                 |
| `{{xdg_cache_home}}`  | XDG cache directory             |
| `{{xdg_config_home}}` | XDG config directory            |
| `{{xdg_data_home}}`   | XDG data directory              |

For functions (`get_env`, `exec`, `arch`, `read_file`, `hash_file`), filters (`snakecase`, `trim`, `absolute`), and conditionals: [Code Patterns - Template Syntax](./references/patterns.md#template-syntax-tera)

## Required & Redacted Variables

```toml
[env]
# Required - fails if not set
DATABASE_URL = { required = true }
API_KEY = { required = "Get from https://example.com/api-keys" }

# Redacted - hides from output
SECRET = { value = "my_secret", redact = true }
_.file = { path = ".env.secrets", redact = true }

# Pattern-based redactions
redactions = ["*_TOKEN", "*_KEY", "PASSWORD"]
```

For combined patterns and detailed examples: [Code Patterns - Required & Redacted](./references/patterns.md#required--redacted-variables)

## Lazy Evaluation (`tools = true`)

By default, env vars resolve BEFORE tools install. Use `tools = true` to access tool-generated paths:

```toml
[env]
GEM_BIN = { value = "{{env.GEM_HOME}}/bin", tools = true }
_.file = { path = ".env", tools = true }
```

## [settings] and [tools]

```toml
[settings]
experimental = true
python.uv_venv_auto = true

[tools]
python = "<version>"
node = "latest"
uv = "latest"
rust = { version = "<version>", profile = "minimal" }

# SSoT-OK: mise min_version directive, not a package version
min_version = "2024.9.5"
```

For full settings reference and version pinning options: [Code Patterns - Settings & Tools](./references/patterns.md#settings-section)

## Implementation Steps

1. **Identify hardcoded values** - timeouts, paths, thresholds, feature flags
2. **Create `.mise.toml`** - add `[env]` section with documented variables
3. **Add venv auto-creation** - `_.python.venv = { path = ".venv", create = true }`
4. **Update scripts** - use env vars with original values as defaults
5. **Add ADR reference** - comment: `# ADR: 2025-12-08-mise-env-centralized-config`
6. **Test without mise** - verify script works using defaults
7. **Test with mise** - verify activated shell uses `.mise.toml` values

## GitHub Token Multi-Account Patterns {#github-token-multi-account-patterns}

For multi-account GitHub setups, mise `[env]` provides per-directory token configuration that overrides gh CLI's global authentication.

**Rule**: Always set BOTH `GH_TOKEN` and `GITHUB_TOKEN` pointing to the same token file.

| Variable       | Usage Context                                 |
| -------------- | --------------------------------------------- |
| `GH_TOKEN`     | mise [env], Doppler, verification tasks       |
| `GITHUB_TOKEN` | npm scripts, GitHub Actions, semantic-release |

**Full guide with templates, verification, and 1Password integration**: [GitHub Token Patterns](./references/github-tokens.md)

## Anti-Patterns

| Anti-Pattern                   | Why                             | Instead                           |
| ------------------------------ | ------------------------------- | --------------------------------- |
| `mise exec -- script.py`       | Forces mise dependency          | Use env vars with defaults        |
| Secrets in `.mise.toml`        | Visible in repo                 | Use Doppler or `redact = true`    |
| No defaults in scripts         | Breaks without mise             | Always provide fallback           |
| `[env]` secrets for pueue jobs | Pueue runs clean shell, no mise | Use `python-dotenv` + `.env` file |
| `__MISE_DIFF` leaks via SSH    | Remote trust errors             | `unset __MISE_DIFF` before SSH    |

**Critical detail on non-interactive shell secrets**: [Anti-Patterns Guide](./references/anti-patterns.md)

## Task Orchestration Integration

When detecting multi-step project workflows during mise configuration, invoke the `mise-tasks` skill for task definitions with dependency management.

**Detection triggers**: multi-step workflows, repeatable commands, dependency chains, file-tracked builds.

**Full guide with examples**: [Task Orchestration](./references/task-orchestration.md) | [mise-tasks skill](../mise-tasks/SKILL.md)

---

## Additional Resources

- **[Code Patterns & Templates](./references/patterns.md)** - Complete code examples for Python, Bash, JS, Go, Rust, and full `.mise.toml` template
- **[Hub-Spoke Architecture](./references/hub-spoke-architecture.md)** - Directory structures, hub/spoke responsibilities, inheritance rules
- **[GitHub Token Patterns](./references/github-tokens.md)** - Multi-account setup, verification, 1Password integration
- **[Anti-Patterns Guide](./references/anti-patterns.md)** - Non-interactive shell secrets, pueue/cron/systemd gotchas
- **[Task Orchestration](./references/task-orchestration.md)** - Workflow detection triggers, environment-to-tasks example
- **[Monorepo Workspace](./references/monorepo-workspace.md)** - uv workspaces, hoisted dev dependencies (PEP 735)
- **Wiki**: [Pattern-mise-Configuration](https://github.com/terrylica/cc-skills/wiki/Pattern-mise-Configuration)

**ADR Reference**: When implementing mise configuration, create an ADR at `docs/adr/YYYY-MM-DD-mise-env-centralized-config.md` in your project.

---

## Troubleshooting

| Issue                    | Cause                    | Solution                                    |
| ------------------------ | ------------------------ | ------------------------------------------- |
| Env vars not loading     | mise not activated       | Add mise activate to shell rc file          |
| Venv not created         | Python not installed     | Run `mise install python`                   |
| Tasks not found          | Wrong mise.toml location | Ensure mise.toml is in project root         |
| PATH not updated         | Shims not in PATH        | Add mise shims to ~/.zshenv                 |
| \.file not loading       | .env file missing        | Create .env file or remove \.file directive |
| Subfolder config ignored | Missing min_version      | Add min_version to subfolder mise.toml      |
