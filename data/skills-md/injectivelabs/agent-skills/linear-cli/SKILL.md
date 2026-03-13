---
name: linear-cli
description: Enables management of Linear issues, teams, projects, comments, or configuration via the `linear` CLI
license: Apache-2.0
metadata:
  author: InjectiveLabs
  version: "1.9.1"
---

# Linear CLI, Skill Guide

## Overview

Use the `linear` CLI to manage Linear issues, teams, and projects from the terminal. Prefer CLI flows over raw GraphQL when a command exists.

## Quick Start

1. Verify the CLI is available: `linear --version`.
2. Install the CLI if needed (see Install Linear CLI).
3. Configure the API key and repo settings (see Configure API Key).
4. Use `linear issue list`, `linear issue start`, and `linear issue view` for day-to-day workflows.

## Install Linear CLI

Prefer NPM-distributed version from Injective Labs:

```bash
npm i -g @injectivelabs/linear-cli
```

One-time commands can be run via `npx @injectivelabs/linear-cli`.

### If NPM is not available

Fetch binary for current platform using <https://github.com/InjectiveLabs/linear-cli/releases/latest> install it so it available in `$PATH`.

## Configure API Key

- Create a personal API key in Linear account settings: `https://linear.app/settings/account/security`.
- If `linear auth login` exists, run it to authenticate. Otherwise export the key for the CLI session: `export LINEAR_API_KEY=...`.
- Run `linear config` inside the repo to generate `.linear.toml` interactively.
- Use `linear auth token` or `linear auth whoami` to verify authentication.
- Note: API key creation requires member access (not guest).

## Common Workflows

- List issues: `linear issue list` with filters like `--state`, `--assignee`, `--team`, or `--limit`.
- Start work on an issue: `linear issue start ABC-123` (use `-b` to specify a branch).
- View an issue: `linear issue view ABC-123` (use `-w` for web or `-a` for app).
- Create an issue: `linear issue create --title "..." --team TEAM` (add `--project`, `--label`, `--priority`, or `--estimate` as needed).
- Update an issue: `linear issue update ABC-123 --state STATE --assignee USER`.
- Add a comment: `linear issue comment add ABC-123 --body "..."`.
- Browse teams/projects: `linear team list`, `linear project list`, then `linear project view`.

## Command Reference

Instead of guessing flag and command arguments, check the reference.

See `references/commands.md` for the full command and flag list extracted from `linear completions bash`.

When some command feels missing try `npx @injectivelabs/linear-cli@latest completions bash` to refresh the completions.

## Safety

- Confirm destructive actions explicitly before running `linear issue delete`.
- Avoid raw schema dumps unless needed; prefer regular commands to inspect data.
