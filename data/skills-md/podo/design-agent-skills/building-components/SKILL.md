---
name: building-components
description: |
  Vercel's guide for building modern, accessible, and composable UI components: accessibility, composable APIs, design tokens, publishing to npm or a registry, and writing component docs. From the components.build project.
triggers:
  - "building components"
  - "build accessible components"
  - "composable component API"
  - "components.build"
das:
  type: skill
  category: visual-components
  upstream: "https://github.com/vercel/components.build"
  upstream_path: "skills/building-components/SKILL.md"
  version: latest
---

# building-components

> Catalogue stub — full skill: [vercel/components.build](https://github.com/vercel/components.build) (`skills/building-components`)

<!-- das:install:start — generated from stub.yaml by `npm run generate`; edit stub.yaml, not this block -->
## Decision tree

1. **Is the full skill already installed?**
   - Global: `f=~/.agents/skills/building-components/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - Project: `f=.agents/skills/building-components/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - `installed` → the skill is installed as `building-components`, invoke it and proceed
   - `pointer` → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/building-components ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add vercel/components.build --skill building-components -g -y
   ```

   **Project:**
   ```bash
   npx skills add vercel/components.build --skill building-components -y
   ```
   > **Claude Code:** send a command as a chat message starting with `!` to run it without leaving the conversation.

**Heads-up**

- **License:** Apache-2.0 (LICENSE notice; GitHub reports NOASSERTION)
<!-- das:install:end -->

## Invoke after install

- Skill name: `building-components`
- Trigger phrases: "building components", "build accessible components", "composable component API", "components.build"

## What it does

Guides building modern UI components that are accessible, composable, and themeable: designing composable APIs, implementing accessibility, setting up design tokens, publishing components to npm or a registry, and writing component documentation. Distilled from the components.build handbook.

## When NOT to use

- A project-aware shadcn/ui workflow (adding and composing registry components) → use `shadcn-ui`
- React/Next.js performance or composition patterns → use `vercel-skills`
- Visual design direction rather than component architecture → use `hallmark` or `taste-skill`
