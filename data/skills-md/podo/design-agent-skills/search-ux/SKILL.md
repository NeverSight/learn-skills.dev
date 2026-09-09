---
name: search-ux
description: |
  Design search experiences that help users find, recover from failure, and refine.
  Query input, autocomplete, results, ranking, filtering, zero-results, and analytics.
triggers:
  - "search UX"
  - "search experience design"
  - "zero results state"
  - "autocomplete design"
  - "faceted search UX"
das:
  type: skill
  category: interaction-polish
  upstream: "https://github.com/Owl-Listener/designer-skills"
  upstream_path: "interaction-design/skills/search-ux/SKILL.md"
  version: latest
---

# search-ux

> Catalogue stub — full skill: [Owl-Listener/designer-skills](https://github.com/Owl-Listener/designer-skills)

## Decision tree

1. **Is the full skill already installed?**
   - Global: `grep -q "^das:" ~/.agents/skills/search-ux/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/search-ux/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/search-ux ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add Owl-Listener/designer-skills --skill search-ux -g -y
   ```

   **Project:**
   ```bash
   npx skills add Owl-Listener/designer-skills --skill search-ux -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.

## What it does

Owls end-to-end search-UX skill: search input and autocomplete, results layout and ranking, faceted filtering, the often-neglected zero-results state (treated as a retention moment), and search analytics (zero-result queries, click position, abandonment). Web research found NO dedicated public search-UX agent skill — this fills a real catalogue gap.

## When NOT to use

- Backend search indexing/relevance tuning → an engineering concern, not this skill
- General navigation IA → use `information-architecture-and-navigation`
