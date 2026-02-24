---
name: glean-plugin-checklist
description: Use when creating, adding, or modifying plugins in this Glean Claude Plugins marketplace repository. Triggers on "create plugin", "add plugin", "new plugin", "plugin checklist", "marketplace", or when working with plugin.json, marketplace.json, or the plugins/ directory. Ensures all required files are updated correctly.
---

# Glean Plugin Marketplace Checklist

This skill provides the checklist for correctly adding or modifying plugins in the glean-claude-plugins marketplace repository.

## Repository Structure

```
glean-claude-plugins/
├── .claude-plugin/
│   └── marketplace.json      # CRITICAL: Plugin registry - must list all plugins
├── plugins/
│   └── <plugin-name>/
│       ├── .claude-plugin/
│       │   └── plugin.json   # Plugin manifest with version
│       ├── README.md         # Plugin documentation
│       ├── commands/         # Slash commands
│       ├── skills/           # Auto-triggered skills
│       └── agents/           # Autonomous agents
├── README.md                 # Main repo README - must list all plugins
└── package.json              # NPM package with version
```

## Adding a New Plugin Checklist

When creating a new plugin, you MUST complete ALL of these steps:

### 1. Create Plugin Directory Structure

```bash
mkdir -p plugins/<plugin-name>/.claude-plugin
mkdir -p plugins/<plugin-name>/commands
mkdir -p plugins/<plugin-name>/skills
mkdir -p plugins/<plugin-name>/agents
```

### 2. Create plugin.json (REQUIRED)

Path: `plugins/<plugin-name>/.claude-plugin/plugin.json`

```json
{
  "name": "<plugin-name>",
  "version": "<MATCH MARKETPLACE VERSION>",
  "description": "<Brief description>. Requires glean-core.",
  "author": {
    "name": "Glean",
    "email": "steve.calvert@glean.com",
    "url": "https://glean.com"
  },
  "homepage": "https://docs.glean.com/administration/platform/mcp/about",
  "repository": "https://github.com/gleanwork/claude-plugins",
  "license": "MIT",
  "keywords": ["glean", "mcp", "<relevant-keywords>"]
}
```

**CRITICAL**: The version MUST match the version in `.claude-plugin/marketplace.json`.

### 3. Add to marketplace.json (REQUIRED)

Path: `.claude-plugin/marketplace.json`

Add entry to the `plugins` array:

```json
{
  "name": "<plugin-name>",
  "source": "./plugins/<plugin-name>",
  "description": "<One-line description for marketplace listing>"
}
```

### 4. Create Plugin README.md (REQUIRED)

Path: `plugins/<plugin-name>/README.md`

Include:
- Plugin description
- Prerequisites (usually "Requires glean-core")
- Available commands
- Available skills
- Available agents
- Usage examples

### 5. Update Main README.md (REQUIRED)

Path: `README.md`

Update THREE sections:

**a) Quick Start section** - Add install command:
```markdown
/plugin install <plugin-name>
```

**b) Plugins table** - Add row:
```markdown
| **[<plugin-name>](plugins/<plugin-name>)** | <Description> | [README](plugins/<plugin-name>/README.md) |
```

**c) "Which Plugin Do I Need?" section** - Add use case:
```markdown
| <Use case description> | `glean-core` + `<plugin-name>` |
```

## Version Management

All plugins should have the same version as the marketplace:

1. Check current version: `jq '.version' .claude-plugin/marketplace.json`
2. Set plugin version to match in `plugins/<plugin-name>/.claude-plugin/plugin.json`

When releasing a new version:
1. Update `.claude-plugin/marketplace.json` version
2. Update `package.json` version
3. Update ALL `plugins/*/.claude-plugin/plugin.json` versions

### 6. Add to .release-it.json bumper (REQUIRED)

Path: `.release-it.json`

Add an entry to the `plugins["@release-it/bumper"].out` array, after the last existing entry:

```json
{
  "file": "plugins/<plugin-name>/.claude-plugin/plugin.json",
  "path": "version"
}
```

**If you skip this step**, the plugin version will fall behind the marketplace version on every future release. This failure is silent — no error will be thrown and no CI check will catch it.

Verify the entry was added:

```bash
node .claude/skills/glean-plugin-checklist/scripts/check-bumper.mjs <plugin-name>
```

## Verification Commands

After adding a plugin, verify with:

```bash
# Check marketplace.json is valid JSON
jq . .claude-plugin/marketplace.json

# List all plugins in marketplace
jq -r '.plugins[].name' .claude-plugin/marketplace.json

# Check all plugin versions match
for p in plugins/*/.claude-plugin/plugin.json; do
  echo "$p: $(jq -r '.version' "$p")"
done

# Check README mentions the plugin
grep "<plugin-name>" README.md

# Check .release-it.json bumper includes the plugin
node .claude/skills/glean-plugin-checklist/scripts/check-bumper.mjs <plugin-name>
```

## Common Mistakes to Avoid

1. **Forgetting marketplace.json** - Plugin won't appear in marketplace
2. **Version mismatch** - Can cause installation issues
3. **Missing README update** - Users won't know plugin exists
4. **Wrong source path** - Use `./plugins/<name>` not `plugins/<name>`

## Using plugin-dev:create-plugin

The `/plugin-dev:create-plugin` command can help scaffold the plugin, but you MUST still:
1. Add to `.claude-plugin/marketplace.json` manually
2. Update the main `README.md` manually
3. Ensure versions match

Always run the verification commands after using `/plugin-dev:create-plugin`.
