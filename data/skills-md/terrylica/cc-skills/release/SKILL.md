---
name: release
description: Run semantic-release with preflight checks. TRIGGERS - npm run release, version bump, changelog, release automation.
allowed-tools: Read, Bash, Glob, Grep, Edit, AskUserQuestion, TodoWrite
argument-hint: "[--dry] [--status]"
disable-model-invocation: true
---

# /itp:release

Delegate to the repository's **mise release tasks**. Every repo should define its own release DAG in `.mise/tasks/release/`.

## First Action: Detect Repo's Release Tasks

```bash
# Check if the repo has mise release tasks
mise tasks ls 2>/dev/null | grep -i release
```

- **If tasks exist**: Delegate to `mise run release:full` (or the repo's equivalent)
- **If no tasks**: Fall back to reading the semantic-release skill for guidance

## Arguments

| Flag       | Short | Description                              |
| ---------- | ----- | ---------------------------------------- |
| `--dry`    | `-d`  | Dry-run mode (preview, no modifications) |
| `--status` | `-s`  | Show current version and release state   |

## Execution

```bash
# Full release (preflight → version → sync → verify)
mise run release:full

# Dry-run (preview what would be released)
mise run release:dry

# Check current state
mise run release:status
```

## Why mise Tasks Over Prescriptive Skills

| Concern             | Prescriptive Skill   | mise Task Delegation              |
| ------------------- | -------------------- | --------------------------------- |
| Repo-specific logic | Duplicated in skill  | Lives in `.mise/tasks/`           |
| DAG enforcement     | Manual ordering      | `depends` array enforced          |
| Maintainability     | Update skill + tasks | Single source in tasks            |
| Portability         | Assumes npm/bun      | Uses whatever the repo configures |
| Secrets             | Hardcoded patterns   | `[env]` in `.mise.toml`           |

## Expected mise Release Task Structure

Repos should follow the hub-and-spoke pattern:

```
.mise.toml                      # Hub: [env] + [tools] + task docs
.mise/tasks/
  └── release/
      ├── _default              # Help / navigation
      ├── preflight             # Phase 1: Validate prerequisites
      ├── version               # Phase 2: Bump version (semantic-release)
      ├── sync                  # Phase 3: Sync artifacts (marketplace, cache)
      ├── verify                # Phase 4: Verify release artifacts
      ├── full                  # Orchestrator: depends on all phases
      ├── dry                   # Dry-run preview
      └── status                # Current version info
```

### Task DAG

```
            ┌──────────┐
            │ preflight│
            └─────┬────┘
                  │ depends
            ┌─────▼────┐
            │ version  │
            └─────┬────┘
                  │ sequential
            ┌─────▼────┐
            │   sync   │
            └─────┬────┘
                  │ sequential
            ┌─────▼────┐
            │  verify  │
            └──────────┘
```

### Key Patterns

```toml
# .mise/tasks/release/full (orchestrator)
depends = ["release:preflight"]
# Chains: preflight → version → sync → verify

# .mise/tasks/release/preflight (guard)
# Checks: clean dir, auth, plugins, releasable commits

# .mise/tasks/release/version (core)
depends = ["release:preflight"]
# Runs: semantic-release (or language-specific versioning)
```

## Fallback: No mise Tasks

If the repo has no mise release tasks, read the semantic-release skill:

```
Read: ${CLAUDE_PLUGIN_ROOT}/skills/semantic-release/SKILL.md
Read: ${CLAUDE_PLUGIN_ROOT}/skills/semantic-release/references/local-release-workflow.md
```

Then follow the 4-phase workflow documented there.

---

## Error Recovery

| Error                  | Resolution                                            |
| ---------------------- | ----------------------------------------------------- |
| `mise tasks` not found | Install mise: `curl https://mise.run \| sh`           |
| No release tasks       | Create `.mise/tasks/release/` or use fallback skill   |
| Working dir not clean  | `git stash` or commit changes                         |
| Not on main branch     | `git checkout main`                                   |
| No releasable commits  | Create a `feat:` or `fix:` commit first               |
| Wrong account          | Check `GH_TOKEN` / `GH_ACCOUNT` in `.mise.toml [env]` |

## Reference

- [mise Task Configuration](https://mise.jdx.dev/tasks/task-configuration.html)
- [Release Workflow Patterns](../skills/mise-tasks/references/release-workflow-patterns.md)
- [semantic-release Skill](../skills/semantic-release/SKILL.md) (fallback)
