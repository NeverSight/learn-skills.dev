---
name: tapcart-project
description: Set up and manage a Tapcart CLI project. Use when the user wants to get started with Tapcart development for the first time, or manage an existing project — including auth, dependencies, linting, logs, and layout dev server. The user only needs to provide their App ID for first-time setup — the agent handles everything else.
---

# Tapcart Project

Project-wide operations for a Tapcart CLI project. All commands run from the root of the Tapcart project directory.

**You (the agent) run all commands directly** unless noted otherwise.

---

## First-Time Setup

Walk through these steps in order to get the user from nothing to a working local environment.

### Step 1 — Check Node.js

```bash
node --version
```

Node 23 or higher is required. If missing or outdated, tell the user to install it from https://nodejs.org (latest LTS ≥ 23). Node.js is a one-time system prerequisite — wait for them to confirm it is installed before continuing.

### Step 2 — Install the Tapcart CLI globally

```bash
npm install -g @tapcart/tapcart-cli
```

Verify it installed:

```bash
tapcart --version
```

### Step 3 — Get the App ID

Ask the user for their **Tapcart App ID**. They can find it at:
**https://app.tapcart.com/settings** → Tapcart CLI API Key section

### Step 4 — Create the project (skip if one already exists)

Check whether a `tapcart.config.json` already exists in the current directory. If it does, skip to Step 5.

If no project exists, create one:

```bash
npm init @tapcart/tapcart-app@latest -- -a <app-id> -f <folder-name>
cd <folder-name>
npm install
```

### Step 5 — Authenticate

Run this command — it opens a browser window automatically and blocks until the user completes the OAuth login:

```bash
tapcart auth login
```

Once the command exits, authentication is complete. Continue to the next step.

### Step 6 — Pull existing blocks and components

```bash
tapcart block pull -a
tapcart component pull -a
```

The project is now ready.

---

## Auth

```bash
# Log in (opens browser automatically, blocks until complete)
tapcart auth login

# Log out
tapcart auth logout
```

Credentials are stored locally and persist across sessions.

---

## Dependencies

Dependencies are npm packages that can be imported inside blocks. They must be added locally and pushed to the remote app config before they work in the dashboard or mobile app.

```bash
# Add a dependency
tapcart dependency add lodash 4.17.21

# Remove a dependency
tapcart dependency remove lodash

# List local dependencies
tapcart dependency list

# Pull dependencies from remote app config
tapcart dependency pull

# Push local dependency list to remote app config
tapcart dependency push
```

After adding a dependency, remind the user to add the package name to the relevant block's `config.json` under `"dependencies": []`, then run `tapcart dependency push`.

---

## Lint

Run lint and show the output to the user:

```bash
# Lint all blocks and components
tapcart lint --all

# Lint specific blocks
tapcart lint -b MyBlock -b AnotherBlock

# Lint specific components
tapcart lint -c ProductCard

# Lint with auto-fix (writes changes to disk)
tapcart lint --all --fix
tapcart lint -b MyBlock --fix
```

Show the lint output to the user and confirm before running with `--fix`.

---

## Logs

```bash
tapcart log
```

---

## Layout Dev Server

Run the layout dev server in the background and tell the user it is running. Keep it running until the user asks you to stop it.

```bash
# Prompts interactively for layout type if not provided
tapcart layout dev

# Specify layout type
tapcart layout dev -l home

# Specify layout type and a particular layout ID
tapcart layout dev -l home -v <layoutId>

# Override specific blocks with their local version
tapcart layout dev -l home -b MyBlock -b AnotherBlock

# Override all blocks with local versions
tapcart layout dev -l home -a

# Custom port (default is 4995)
tapcart layout dev -l home -p 4995
```

By default the dev server renders blocks using the live dashboard version. Use `-b <BlockFolderName>` to use a local block instead, or `-a` to use all local blocks.

When the user asks to stop the dev server, terminate the process.
