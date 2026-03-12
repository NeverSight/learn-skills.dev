---
name: claudian-installer
description: Install Claudian Obsidian plugin which embeds Claude Code as an AI collaborator in your vault. Use when the user wants to install Claudian plugin to their Obsidian vault, or mentions "Claudian", "Claude Code in Obsidian", or "install Claudian plugin".
---

# Claudian Installer

Install Claudian - an Obsidian plugin that embeds Claude Code as an AI collaborator in your vault, giving it full agentic capabilities: file read/write, search, bash commands, and multi-step workflows.

## Installation Workflow

### Step 1: Confirm Vault Path

Ask the user to confirm the Obsidian vault path. The default is the current working directory:

```
Default: <current working directory>
```

If the user specifies a different path, use that instead.

### Step 2: Create Plugin Directory

Create the claudian plugin folder in the vault's plugins directory:

```bash
mkdir -p /path/to/vault/.obsidian/plugins/claudian
```

### Step 3: Copy Plugin Files

Copy the plugin files from this skill's assets to the plugin directory:

```bash
cp <skill-path>/assets/main.js /path/to/vault/.obsidian/plugins/claudian/
cp <skill-path>/assets/manifest.json /path/to/vault/.obsidian/plugins/claudian/
cp <skill-path>/assets/styles.css /path/to/vault/.obsidian/plugins/claudian/
```

### Step 4: Enable the Plugin

Remind the user to enable the plugin in Obsidian:

1. Open Obsidian
2. Go to Settings → Community plugins
3. Find "Claudian" in the list
4. Click to enable it

## Assets

This skill includes the following plugin files in `assets/`:

- `main.js` - Plugin main code
- `manifest.json` - Plugin manifest
- `styles.css` - Plugin styles
