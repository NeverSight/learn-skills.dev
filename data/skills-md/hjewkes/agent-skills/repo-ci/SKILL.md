---
name: repo-ci
description: Use when setting up CI/CD workflows, auditing repo CI health, adding GitHub Actions, configuring branch protection, or scaffolding release pipelines for Node.js or Python projects.
---

# Repo CI

Set up and audit CI/CD workflows using the `repo-ci` CLI against the standards defined in [references/standards.md](references/standards.md).

## Modes

### Audit Mode

**Triggers:** "check CI", "audit repo", "what's missing", "CI gaps", "CI health"

Load and follow [references/audit-existing.md](references/audit-existing.md).

Run `repo-ci audit --json` to score the repo across 7 areas, present a scorecard, explain gaps, and offer to fix them.

### Setup Mode

**Triggers:** "set up CI", "add workflows", "new project", "scaffold CI", "add GitHub Actions"

Load and follow [references/setup-new.md](references/setup-new.md).

Run `repo-ci setup --dry-run` first, review with the user, then generate the files and walk through the post-setup checklist.

### Init Mode

**Triggers:** "create repo", "new repo", "init repo", "set up new project"

Load and follow [references/setup-new.md](references/setup-new.md) (init section).

Run `repo-ci init --dry-run` first, review with the user, then execute.

## CLI Reference

| Command | Description |
|---------|-------------|
| `repo-ci init` | Create GitHub repo and fully configure it |
| `repo-ci init --dry-run` | Preview what init would do |
| `repo-ci init --private` | Create as private repo |
| `repo-ci init --skip-ci` | Create repo without CI workflows |
| `repo-ci audit` | Audit CI health (exit 0 = pass, 2 = gaps found) |
| `repo-ci audit --json` | Structured JSON output for parsing |
| `repo-ci setup` | Generate workflow files from templates |
| `repo-ci setup --dry-run` | Preview generated files without writing |
| `repo-ci setup --preset node` | Force Node/TypeScript preset |
| `repo-ci setup --preset python` | Force Python preset |

## Supported Stacks

| Stack | Support level |
|-------|---------------|
| Node/TypeScript | Full — init + CI + release + coverage + rulesets |
| Python | Basic — init + CI + release |

**Unsupported stack?** If `repo-ci setup` outputs an unsupported-stack message (exit 2), follow the exit door handling in [references/setup-new.md](references/setup-new.md) to scaffold manually and extend the skill.

## Source of Truth

All standards (triggers, jobs, thresholds, release steps) are documented in [references/standards.md](references/standards.md). When in doubt, refer there.
