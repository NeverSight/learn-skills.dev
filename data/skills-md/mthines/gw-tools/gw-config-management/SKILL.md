---
name: gw-config-management
description: >
  Configure and optimize gw-tools for different project types and team needs.
  Use when setting up gw for new projects, configuring auto-copy files, troubleshooting configuration issues, or customizing gw for Next.js, Node.js APIs, monorepos, or React SPAs.
  Triggers on .gw/config.json, auto-copy patterns, environment files, or gw init commands.
license: MIT
metadata:
  author: mthines
  version: '2.0.0'
  workflow_type: advisory
---

# gw Configuration Management

Configure gw-tools for optimal workflows across different project types and team environments.

## Rules

| Rule                                              | Description                                               |
| ------------------------------------------------- | --------------------------------------------------------- |
| [fundamentals](./rules/fundamentals.md)           | **HIGH** - Config file location, creation, and precedence |
| [options-reference](./rules/options-reference.md) | **HIGH** - Complete reference for all config options      |
| [setup](./rules/setup.md)                         | **HIGH** - Initial setup flow, secrets, team onboarding   |
| [auto-copy](./rules/auto-copy.md)                 | **HIGH** - File patterns to copy, what to include/exclude |
| [team-config](./rules/team-config.md)             | **MEDIUM** - Sharing config, documentation, onboarding    |
| [advanced](./rules/advanced.md)                   | **LOW** - Multiple sources, secret management integration |
| [troubleshooting](./rules/troubleshooting.md)     | **HIGH** - Common issues and solutions                    |

## Project-Type Patterns

| Pattern                                           | Description                                 |
| ------------------------------------------------- | ------------------------------------------- |
| [nextjs](./rules/project-types/nextjs.md)         | **MEDIUM** - Next.js with Vercel deployment |
| [nodejs-api](./rules/project-types/nodejs-api.md) | **MEDIUM** - Node.js backend/API services   |
| [monorepo](./rules/project-types/monorepo.md)     | **MEDIUM** - pnpm/Yarn/npm workspaces       |
| [react-spa](./rules/project-types/react-spa.md)   | **MEDIUM** - React Single Page Applications |

## Quick Reference

| Task                    | Command                                   |
| ----------------------- | ----------------------------------------- |
| Initialize config       | `gw init`                                 |
| Initialize with options | `gw init --auto-copy-files .env,secrets/` |
| Interactive setup       | `gw init --interactive`                   |
| Clone and initialize    | `gw init git@github.com:user/repo.git`    |
| Sync files to worktree  | `gw sync feature-branch`                  |
| Show setup command      | `gw show-init`                            |

## Configuration Options

| Option           | Purpose                 | Default       |
| ---------------- | ----------------------- | ------------- |
| `root`           | Repository root path    | Auto-detected |
| `defaultBranch`  | Source for file copying | `"main"`      |
| `autoCopyFiles`  | Files to auto-copy      | `[]`          |
| `updateStrategy` | merge or rebase         | `"merge"`     |
| `cleanThreshold` | Days before stale       | `7`           |
| `autoClean`      | Prompt for cleanup      | `false`       |

## Key Principles

- **Set up secrets in defaultBranch first**: Source must exist before auto-copy works.
- **Commit config to version control**: Team gets it automatically.
- **Copy secrets, not dependencies**: `.env` yes, `node_modules` no.
- **Use `gw show-init` for documentation**: Generate setup command.

## Related Skills

- [git-worktree-workflows](../git-worktree-workflows/) - Using worktrees effectively
- [autonomous-workflow](../autonomous-workflow/) - Autonomous development workflows

## Resources

- [Project-Type Guides](./rules/project-types/) - Configuration guides for common project types
- [Next.js Setup Example](./references/nextjs-setup.md)
- [Monorepo Setup Example](./references/monorepo-setup.md)
- [Troubleshooting Guide](./references/troubleshooting-config.md)
