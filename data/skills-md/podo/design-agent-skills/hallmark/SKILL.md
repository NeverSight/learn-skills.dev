---
name: hallmark
description: |
  Anti-AI-slop design skill for greenfield pages, audits, redesigns, and design extraction from URLs or screenshots. Pushes structural variety, not just colour swaps, so pages built for different briefs stop sharing the same hero → features → CTA rhythm.
triggers:
  - "Hallmark design skill"
  - "hallmark audit"
  - "hallmark redesign"
  - "hallmark study"
  - "structural variety design"
  - "extract design DNA"
das:
  type: skill
  category: design-systems
  upstream: "https://github.com/Nutlope/hallmark"
  version: latest
---

# hallmark

> Catalogue stub — full skill: [Nutlope/hallmark](https://github.com/Nutlope/hallmark)

<!-- das:install:start — generated from stub.yaml by `npm run generate`; edit stub.yaml, not this block -->
## Decision tree

1. **Is the full skill already installed?**
   - Global: `f=~/.agents/skills/hallmark/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - Project: `f=.agents/skills/hallmark/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - `installed` → the skill is installed as `hallmark`, invoke it and proceed
   - `pointer` → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/hallmark ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add Nutlope/hallmark --skill hallmark -g -y
   ```

   **Project:**
   ```bash
   npx skills add Nutlope/hallmark --skill hallmark -y
   ```
   > **Claude Code:** send a command as a chat message starting with `!` to run it without leaving the conversation.

**Heads-up**

- **License:** MIT
- **Large download (~227 MB):** the skills CLI gives up cloning after 300 s; if it times out, retry with `SKILLS_CLONE_TIMEOUT_MS=900000`.
<!-- das:install:end -->

## Invoke after install

- Skill name: `hallmark`
- Verbs: `hallmark audit <target>`, `hallmark redesign <target>`, `hallmark study <screenshot | URL>`
- Trigger phrases: "Hallmark design skill", "hallmark audit", "hallmark redesign", "hallmark study"

## What it does

A short, opinionated design skill that stops AI coding assistants from falling back to the defaults every model was trained on. The default flow designs a new page from a named theme catalogue with locked tokens and a pre-emit self-critique; `audit` scores existing UI against an anti-pattern list and returns a ranked punch list without editing; `redesign` restructures the visual layer inside the existing implementation boundaries; `study` extracts the design DNA (macrostructure, type pairing, colour anchor) from a screenshot or URL and can emit a portable `design.md`. Responsive checks and honest-copy rules (no invented metrics) are built in.

## When NOT to use

- Persistent critique commands, Chrome extension, or Live Mode iteration → use `impeccable`
- Dial-based premium aesthetics (variance, motion, density) → use `taste-skill` or `ui-craft`
- Accessibility or WCAG audits → use `accessibility-catalogue`
- SwiftUI / iOS visual design → use `swiftui-design-skill`
