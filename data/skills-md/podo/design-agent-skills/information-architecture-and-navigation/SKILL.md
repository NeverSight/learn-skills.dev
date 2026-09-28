---
name: information-architecture-and-navigation
description: |
  Reference-grade information architecture and navigation: organization/labeling/navigation/
  search systems, taxonomy depth-vs-breadth, every nav pattern per device, wayfinding, findability.
triggers:
  - "information architecture"
  - "navigation design"
  - "site map structure"
  - "card sorting analysis"
  - "tree testing"
  - "findability audit"
das:
  type: skill
  category: interaction-polish
  upstream: "https://github.com/jpoindexter/design-and-ai-skills"
  upstream_path: "design-system-skills/information-architecture-and-navigation/SKILL.md"
  version: latest
---

# information-architecture-and-navigation

> Catalogue stub — full skill: [jpoindexter/design-and-ai-skills](https://github.com/jpoindexter/design-and-ai-skills)

## Decision tree

1. **Is the full skill already installed?**
   - Global: `grep -q "^das:" ~/.agents/skills/information-architecture-and-navigation/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/information-architecture-and-navigation/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/information-architecture-and-navigation ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add jpoindexter/design-and-ai-skills --skill information-architecture-and-navigation -g -y
   ```

   **Project:**
   ```bash
   npx skills add jpoindexter/design-and-ai-skills --skill information-architecture-and-navigation -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.

## What it does

A 23.8KB IA reference built on Rosenfeld/Morville/Arango (the "polar bear book") four-systems model — organization, labeling, navigation, search — with exact-vs-ambiguous schemes, depth/breadth + faceted classification, per-device navigation patterns, wayfinding mechanics, URLs-as-IA, and the research methods (card sort, tree test, first-click) that prove findability. A strict superset of Owl’s IA skill.

## When NOT to use

- Visual nav-bar styling only → a component/design-system concern
- Search interaction details → pair with `search-ux`
