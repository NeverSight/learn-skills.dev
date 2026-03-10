---
name: obsidian-cli-automation
description: Use when users need terminal automation for Obsidian, including note and vault operations, daily notes, tasks, properties, search, plugin or theme management, and sync or history recovery.
---

# Obsidian CLI Automation

## Overview

Automate Obsidian workflows with deterministic CLI commands.
Use this skill to map natural-language requests into safe, repeatable `obsidian` command sequences with explicit verification.

## When to Use

Use this skill when requests include any of the following intents:

- Automate Obsidian workflows from terminal scripts
- Batch create, update, move, rename, or delete notes
- Operate daily notes, tasks, links, tags, aliases, properties
- Query vault structure, search content, generate hygiene reports
- Manage plugins, themes, snippets, tabs, workspace, bookmarks
- Inspect or recover history and Obsidian Sync versions
- Execute developer diagnostics commands such as `dev:*` or `eval`

## Quick Start

1. Confirm CLI availability:
   ```bash
   command -v obsidian
   obsidian version
   ```
2. Discover vault names:
   ```bash
   obsidian vaults
   ```
3. Pin target vault and run a read-only probe:
   ```bash
   VAULT='My Vault'
   obsidian vault="$VAULT" vault info=path
   obsidian vault="$VAULT" files total
   ```

## Execution Workflow

1. Discover command surface before automation.
   - Run `obsidian --help`.
   - Run `scripts/collect_obsidian_help.sh` for a complete snapshot.
2. Resolve targets with deterministic selectors.
   - Prefer `path=` over `file=` when ambiguity exists.
   - Use `vault=<name>` on all non-trivial runs.
3. Execute read-first probes.
   - Use `read`, `file`, `tasks`, `properties`, `search`, `sync:history` before mutation.
4. Execute minimal mutation steps.
   - Apply `append`, `prepend`, `create`, `property:set`, `task`, `move`, `rename` in small steps.
5. Verify post-change state.
   - Re-run read/query commands and compare expected vs actual output.

## Command Families

- Vault discovery and structure: `vaults`, `vault`, `folders`, `files`, `folder`, `file`
- Note lifecycle: `create`, `read`, `append`, `prepend`, `move`, `rename`, `delete`, `open`
- Daily workflow: `daily`, `daily:path`, `daily:read`, `daily:append`, `daily:prepend`
- Tasks and links: `tasks`, `task`, `links`, `backlinks`, `orphans`, `deadends`, `unresolved`
- Metadata: `tags`, `tag`, `aliases`, `properties`, `property:read`, `property:set`, `property:remove`
- Search and outline: `search`, `search:context`, `search:open`, `outline`
- Bases: `bases`, `base:views`, `base:query`, `base:create`
- UI/system controls: `tabs`, `tab:open`, `workspace`, `command`, `commands`, `reload`, `restart`
- Theme/snippet/plugin management: `themes`, `theme:*`, `snippets`, `snippet:*`, `plugins`, `plugin:*`, `plugins:restrict`
- Sync/history and recovery: `sync:*`, `history:*`, `diff`
- Developer diagnostics: `dev:*`, `devtools`, `eval`, `dev:console`, `dev:errors`, `dev:screenshot`

## High-Value Automation Patterns

### Daily planning block

```bash
VAULT='My Vault'
obsidian vault="$VAULT" daily:append content=$'## Plan\n- [ ] Top 1\n- [ ] Top 2\n'
obsidian vault="$VAULT" daily:read
```

### Batch frontmatter update for a folder

```bash
VAULT='My Vault'
obsidian vault="$VAULT" files folder='Projects' ext=md | while IFS= read -r p; do
  [ -z "$p" ] && continue
  obsidian vault="$VAULT" property:set path="$p" name=reviewed value=false type=checkbox
done
```

### Vault hygiene snapshot

```bash
VAULT='My Vault'
obsidian vault="$VAULT" unresolved total
obsidian vault="$VAULT" orphans total
obsidian vault="$VAULT" deadends total
obsidian vault="$VAULT" recents total
```

### Sync inspection before restore

```bash
VAULT='My Vault'
TARGET='Projects/Example.md'
obsidian vault="$VAULT" sync:history path="$TARGET"
obsidian vault="$VAULT" sync:read path="$TARGET" version=1
```

## Safety Guardrails

- Avoid destructive commands (`delete permanent`, `sync:restore`, `history:restore`, `theme:uninstall`, `plugin:uninstall`) without explicit confirmation.
- Use mutation commands only after a read probe confirms target scope.
- Split large automations into idempotent, restart-safe steps.
- Log command output for rollback decisions when running bulk operations.

## Bundled Resources

- `scripts/collect_obsidian_help.sh`: Dump top-level help, all command helps, and a markdown report.
- `references/automation-recipes.md`: Copy-paste automation recipes for recurring workflows.
- `references/obsidian-cli-full-help.md`: Full command traversal output for `obsidian` CLI.

## Validation Checklist

1. Run target command(s) with explicit `vault=` and `path=`.
2. Run verification command(s) immediately after each mutation step.
3. Report changed files, properties, tasks, or sync versions with exact command evidence.
