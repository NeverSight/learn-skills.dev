---
name: tapcart-blocks
description: Create, pull, push, and manage versions of Tapcart blocks and global components using the Tapcart CLI. Use when the user wants to create a block or component, pull blocks from the dashboard, push changes, start a dev server, list versions, or set a version live.
---

# Tapcart Blocks & Components

Manage Tapcart blocks and global components. Blocks and components have identical operations — this skill covers both. All commands run from the root of the Tapcart project directory.

**You (the agent) run all commands directly** unless noted otherwise.

---

## Create

Run the create command, then confirm to the user what was created:

```bash
# Block
tapcart block create <BlockFolderName>

# Component
tapcart component create <ComponentFolderName>
```

After creating, tell the user how to start the dev server (see Dev Server below).

---

## Pull

Run the pull command to sync from the Tapcart dashboard to the local `./blocks` or `./components` folder:

```bash
# Pull all blocks
tapcart block pull -a

# Pull specific block(s)
tapcart block pull -b MyBlock
tapcart block pull -b BlockOne -b BlockTwo

# Pull a specific version of a block
tapcart block pull -b MyBlock -v 2

# Pull all components
tapcart component pull -a

# Pull specific component(s)
tapcart component pull -c ProductCard
tapcart component pull -c ProductCard -c Button

# Pull a specific version of a component
tapcart component pull -c ProductCard -v 3
```

Constraints:
- `-a` and `-b`/`-c` cannot be combined
- `-v` can only be used with a single block/component name

---

## Push

Before pushing, read the local `code.jsx` and `config.json` to confirm the changes look correct, then confirm with the user before running.

```bash
# Push a specific block (creates new version, not live)
tapcart block push -b MyBlock

# Push and set the new version live immediately
tapcart block push -b MyBlock --live

# Push multiple blocks
tapcart block push -b BlockOne -b BlockTwo

# Push all blocks
tapcart block push -a

# Push a specific component
tapcart component push -c ProductCard

# Push and set live
tapcart component push -c ProductCard --live

# Push all components
tapcart component push -a
```

> **Warning**: `--live` makes the new version immediately visible to all app users. Default to pushing without `--live` and then using `versions set` after the user has verified the result.

---

## Dev Server

Run the dev server in the background and tell the user it is running. Keep it running until the user asks you to stop it.

```bash
# Block dev server
tapcart block dev -b MyBlock
tapcart block dev -b MyBlock -p 4995   # custom port, default is 4995

# Component dev server
tapcart component dev -c ProductCard
tapcart component dev -c ProductCard -p 4996   # default is 4996
```

The dev server opens at `http://localhost:<port>` (block default: 4995, component default: 4996).

When the user asks to stop the dev server, terminate the process.

---

## Versions

### List versions

Run this and show the output to the user:

```bash
tapcart block versions list -b MyBlock
tapcart component versions list -c ProductCard
```

Output shows each version number, which is local, and which is live on the dashboard.

### Set a version live

Confirm with the user which version to promote, then run:

```bash
tapcart block versions set -b MyBlock -v 2
tapcart component versions set -c ProductCard -v 3
```

Version numbers are 1-based (version 1 is the first push).
