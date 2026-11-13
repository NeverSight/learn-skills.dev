---
name: wpds
description: |
  WordPress Design System (WPDS) skill. Build and review UI that uses WPDS components, design tokens, and patterns across Gutenberg, WooCommerce, WordPress.com, and Jetpack. Reads canonical documentation from the WPDS MCP server instead of the web.
triggers:
  - "WordPress Design System"
  - "WPDS"
  - "WordPress design tokens"
  - "WordPress UI components"
  - "Gutenberg UI design"
das:
  type: skill
  category: design-systems
  upstream: "https://github.com/WordPress/agent-skills"
  version: latest
---

# wpds

> Catalogue stub — full skill: [WordPress/agent-skills](https://github.com/WordPress/agent-skills) (`skills/wpds`)

<!-- das:install:start — generated from stub.yaml by `npm run generate`; edit stub.yaml, not this block -->
## Decision tree

1. **Is the full skill already installed?**
   - Global: `f=~/.agents/skills/wpds/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - Project: `f=.agents/skills/wpds/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - `installed` → the skill is installed as `wpds`, invoke it and proceed
   - `pointer` → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/wpds ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add WordPress/agent-skills --skill wpds -g -y
   ```

   **Project:**
   ```bash
   npx skills add WordPress/agent-skills --skill wpds -y
   ```
   > **Claude Code:** send a command as a chat message starting with `!` to run it without leaving the conversation.

**Heads-up**

- **Requires:** WPDS MCP server (@wordpress/design-system-mcp, experimental); the skill is small and defers to it instead of web lookups
- **License:** GPL-2.0-or-later
<!-- das:install:end -->

## Invoke after install

- Skill name: `wpds`
- Trigger phrases: "WordPress Design System", "WPDS", "WordPress design tokens", "WordPress UI components"
- Needs the WPDS MCP server configured and running; it targets WordPress 7.0+. Ask the user before adding it. For Claude Code the upstream package documents: `claude mcp add wordpress-design-system -- npx -y --ignore-scripts @wordpress/design-system-mcp@latest` (the package is WordPress/gutenberg `packages/design-system-mcp`, still experimental)

## What it does

Guides building and reviewing WordPress-related UI against the official WordPress Design System: components (including `@wordpress/components` and `@wordpress/ui`), design tokens, colour primitives, spacing scales, and typography presets. It retrieves canonical component and token documentation from the WPDS MCP server rather than searching the web, assumes TypeScript, React, and CSS unless told otherwise, validates with the project's lint scripts when available, and closes each answer with a recap of decisions and what was left out of scope.

## When NOT to use

- Non-UI WordPress work (plugins, REST API, WP-CLI, blocks logic) → install the other skills in `WordPress/agent-skills` directly
- General design-system governance or token tooling → use `design-system-governance` or `design-tokens-skill`
- Component library work with shadcn/ui → use `shadcn-ui`
