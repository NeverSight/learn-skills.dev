---
name: ada-config-snapshot
description: Version-control an Ada agent's configuration and promote changes between instances using adacli snapshots (export → git → dry run → import). Use when the user wants to back up, compare, restore, GitOps, or copy config from one Ada instance to another (e.g. staging → production).
require-tools:
  - Bash
  - Read
  - Write
---

# Ada config as version-controlled snapshots

`adacli snapshot` runs Ada's Snapshot engine, the engine of the public Snapshot API
(`/v2/config/`). An export takes the whole AI Agent as one `.tar.gz` archive. Unpacked, the
archive holds `config.json`, `manifest.json` and `articles/`. Keep the unpacked folder in git
for GitOps and promotion between instances.

## Back up / baseline

```bash
adacli <instance> snapshot export -o <instance>/
git add <instance> && git commit -m "baseline config for <instance>"
```

An export always takes the whole AI Agent. `-o <file>.tar.gz` writes the archive. `-o -`
writes it to stdout. Any other `-o` path is a folder. A second export into the same folder replaces only `config.json`,
`manifest.json` and `articles/`, so `git diff` shows what changed.

The export prints the names of the secret values that the snapshot needs. Ask the user for
each value before an import, and pass it with `--secret NAME=VALUE`.

## See what changed

Before an import, show what it would change on the live instance:

```bash
adacli <instance> snapshot import <instance>/ --dry-run
```

`--dry-run` writes nothing. It prints the create, update and delete count of each section,
and the names that an import deletes. Show the user the result and get agreement before any
import.

## Promote between instances (e.g. staging → prod)

Validate first, then apply:

```bash
# Validate only. Writes nothing.
adacli <target> snapshot import staging/ --dry-run

# Apply, only after explicit user confirmation
adacli <target> snapshot import staging/ --confirm

# Promote some sections only. What they reference comes along.
adacli <target> snapshot import staging/ --include playbooks --confirm
```

An import replaces each section that it imports. The apply deletes every item that the archive
does not carry in that section. A section that comes along by reference is only added to.

## Roll back

Import the baseline with `--include` for the section that changed:

```bash
adacli <instance> snapshot import <instance>/ --include knowledge --dry-run
adacli <instance> snapshot import <instance>/ --include knowledge --confirm
```

To restore one item, use the create or update command of that resource.

## Rules

- Run `--dry-run` and get explicit user sign-off before every import. Every delete count is a
  real deletion.
- If the import stops with `SNAPSHOT_BLOCKED` (exit 9), show the user each blocker. Fix them on
  the target, then import again.
- An import needs the admin or owner role. A read_only instance refuses it.
- Commit the snapshot before and after a change so the repo is the source of truth.
- Use `--include` to keep promotions surgical (e.g. promote only `playbooks`).
