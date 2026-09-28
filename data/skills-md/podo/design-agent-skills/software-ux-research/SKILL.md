---
name: software-ux-research
description: |
  De-risk product decisions with rigorous UX research. Deep reference guides for survey
  design, research repository/ops, and usability testing (ISO 9241-grounded), plus JTBD.
triggers:
  - "software UX research"
  - "UX research ops"
  - "usability test plan"
  - "survey design methodology"
  - "research repository setup"
das:
  type: skill
  category: design-research
  upstream: "https://github.com/vasilyu1983/AI-Agents-public"
  upstream_path: "frameworks/shared-skills/skills/software-ux-research/SKILL.md"
  version: latest
---

# software-ux-research

> Catalogue stub — full skill: [vasilyu1983/AI-Agents-public](https://github.com/vasilyu1983/AI-Agents-public)

## Decision tree

1. **Is the full skill already installed?**
   - Global: `grep -q "^das:" ~/.agents/skills/software-ux-research/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - Project: `grep -q "^das:" .agents/skills/software-ux-research/SKILL.md 2>/dev/null && echo "pointer" || echo "installed"`
   - No `das:` block → full skill installed, invoke and proceed
   - `das:` block present → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/software-ux-research ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add vasilyu1983/AI-Agents-public --skill software-ux-research -g -y
   ```

   **Project:**
   ```bash
   npx skills add vasilyu1983/AI-Agents-public --skill software-ux-research -y
   ```
   > **Claude Code:** send either command as a chat message starting with `!` to run it without leaving the conversation.

## What it does

A research-ops powerhouse (~15–19KB per topic): survey-design (Likert/NPS/SUS, sample-size math with finite-population correction, bias rewrites, full stats), research-repository management (governance, taxonomy ownership, decay/freshness, GDPR/PII classification, adoption ROI), and usability testing (think-aloud protocols, SEQ/ASQ/SUS, severity matrices, reporting). Web research picked this over Owl’s thinner research skills.

## When NOT to use

- Lightweight single-method help → may be heavier than needed
- AI-moderated/synthetic interviews → use `user-research-cookiy`
