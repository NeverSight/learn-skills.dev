---
name: distinctdeer
description: Claim an unused project name with distinctdeer and create an empty git repo for it. Use when starting a new project, when a new project needs a name, or when creating a fresh project directory.
---

## distinctdeer

distinctdeer owns the pool of project names and hands out an unused one.

Treat it as the sole authority on names, and let it record the claim itself.

It runs straight from GitHub, so no local checkout is involved and nothing on disk needs to be kept in sync.

## Base directory

New projects live under one root, `PDEV_ROOT`, which defaults to `$HOME/pdev/taylormonacelli`.

Shell state does not persist between tool calls, so the command below expands the root inline rather than relying on an exported variable.

## Claim a name

```
uv tool run --from git+https://github.com/gkwa/distinctdeer distinctdeer use --out json rand
```

This prints `{"name": "<name>"}` and marks the name used in one step.

Read `<name>` out of that JSON and use it for the rest of the run.

## Create the project

```
git init "${PDEV_ROOT:-$HOME/pdev/taylormonacelli}/<name>"
```

`git init` creates the directory itself, so this is the entire step.

Report the resolved absolute path when done.

The result is an empty repository with no commit, which is where this skill stops.

Scaffolding what goes inside it belongs to the language-specific skills.

## Reference

`--from` belongs to `uv tool run`, and `uv run` rejects it while suggesting `--frozen`.

`--out` belongs to the `use` subcommand and comes before `rand`.

`use --out json rand` works, while `use rand --out json` exits with an unrecognized-arguments error.

distinctdeer copies the claimed name to the clipboard, replacing whatever was there.

distinctdeer records the claim in the Obsidian vault and leaves that change uncommitted, which is expected; leave it as it stands.
