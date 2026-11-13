---
name: html-ppt
description: |
  HTML PPT Studio: author static HTML presentations from templates. One theme file is one look, one layout file is one page type, one animation class is one entry effect. Includes full-deck templates, canvas FX, and a presenter mode with speaker script and timer. No build step.
triggers:
  - "HTML PPT Studio"
  - "html-ppt"
  - "HTML presentation themes"
  - "presenter mode slides"
  - "keyboard-navigable HTML deck"
  - "Xiaohongshu image-text cards"
das:
  type: skill
  category: presentations
  upstream: "https://github.com/lewislulu/html-ppt-skill"
  version: latest
---

# html-ppt

> Catalogue stub — full skill: [lewislulu/html-ppt-skill](https://github.com/lewislulu/html-ppt-skill)

<!-- das:install:start — generated from stub.yaml by `npm run generate`; edit stub.yaml, not this block -->
## Decision tree

1. **Is the full skill already installed?**
   - Global: `f=~/.agents/skills/html-ppt/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - Project: `f=.agents/skills/html-ppt/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - `installed` → the skill is installed as `html-ppt`, invoke it and proceed
   - `pointer` → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/html-ppt ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add lewislulu/html-ppt-skill --skill html-ppt -g -y
   ```

   **Project:**
   ```bash
   npx skills add lewislulu/html-ppt-skill --skill html-ppt -y
   ```
   > **Claude Code:** send a command as a chat message starting with `!` to run it without leaving the conversation.

**Heads-up**

- **License:** MIT
<!-- das:install:end -->

## Invoke after install

- Skill name: `html-ppt`
- Trigger phrases: "HTML PPT Studio", "html-ppt", "HTML presentation themes", "presenter mode slides"

## What it does

Authors professional presentations as plain static HTML/CSS/JS, driven by a token-based design system. A deck is assembled from a theme (the look), single-page layouts, full-deck templates, and CSS or canvas animation effects. Keyboard navigation is built in, and pressing `S` opens a synchronised presenter window with a speaker script and timer. Also covers PNG export and image-text card sets (Xiaohongshu style). Pure static output with only CDN web fonts, so decks open anywhere.

## When NOT to use

- Editable `.pptx` output → use `anthropics-skills` (its `pptx` skill)
- Markdown-driven developer decks → use `slidev-skill`, `marp-slides`, or `revealjs-skill`
- A different animation-rich HTML presentation approach → use `frontend-slides`
- Planning the story and auditing delivery before rendering → use `humanize-ppt`
