---
name: go-development
description: Go development workflow including verification commands and self-review checklist. Use when modifying Go code in internal/, pkg/, or cmd/ directories.
---

# Go Development Workflow

Workflow for Go code changes in this repository.

## Prerequisites

- **Use `git-workflow` Skill** for branch management, commit conventions, and PR creation.
- **Refer to `.claude/rules/go.md`** for detailed verification commands and coding rules (SSOT).

## Applicable Directories

| Directory   | Description                                |
| ----------- | ------------------------------------------ |
| `internal/` | Core application code (Clean Architecture) |
| `pkg/`      | Reusable shared packages                   |
| `cmd/`      | Application entry points                   |

## Workflow

### 1. Make Changes

Edit Go files following the rules in `.claude/rules/go.md`.

### 2. Verify (from rules/go.md)

```bash
make go-lint && make tidy && make check-build && make go-test
```

### 3. Self-Review Checklist

- [ ] Domain layer has ZERO infrastructure dependencies
- [ ] Error handling uses `fmt.Errorf("context: %w", err)`
- [ ] No private keys or sensitive data logged
- [ ] Auto-generated files not edited

## Database Changes

If modifying database schema, use `db-migration` skill.

## Related

- `.claude/rules/go.md` - Go rules (SSOT)
- `git-workflow` - Branch, commit, PR workflow
- `db-migration` - Database schema workflow
