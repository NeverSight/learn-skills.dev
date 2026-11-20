---
name: motion
description: |
  Official animation skill from the Motion team (Motion, formerly Framer Motion, plus
  plain CSS animation): animation best practices for vanilla JS, React, Vue, Base UI and
  Radix, Motion docs and example search, CSS spring and bounce generation, performance
  audits, and upgrade guides.
triggers:
  - "Motion animation skill"
  - "motion.dev"
  - "MotionScore"
  - "CSS spring easing"
  - "Motion AI Kit"
das:
  category: motion-animation
  upstream: "https://github.com/motiondivision/ai-kit"
  upstream_path: "plugins/motion/skills/motion/SKILL.md"
  version: latest
  install: true
---

# motion

> Catalogue stub — full skill: [motiondivision/ai-kit](https://github.com/motiondivision/ai-kit)

<!-- das:install:start — generated from stub.yaml by `npm run generate`; edit stub.yaml, not this block -->
## Decision tree

1. **Is the full skill already installed?**
   - Global: `f=~/.agents/skills/motion/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - Project: `f=.agents/skills/motion/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - `installed` → the skill is installed as `motion`, invoke it and proceed
   - `pointer` → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/motion ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add motiondivision/ai-kit --skill motion -g -y
   ```

   **Project:**
   ```bash
   npx skills add motiondivision/ai-kit --skill motion -y
   ```
   > **Claude Code:** send a command as a chat message starting with `!` to run it without leaving the conversation.

**Heads-up**

- **Requires:** Optional, for docs search and CSS spring generation: Motion's free hosted MCP server (no API key). A skills-only install does not configure it; upstream's own installer is `npx motion-ai`; Optional, for MotionScore performance audits and Motion UI source code: a Motion+ membership and its MCP server
- **License:** no LICENSE file in the upstream repo
<!-- das:install:end -->

## Invoke after install

- Skill name: `motion`
- Slash command: `/motion` with a question or subcommand, for example `/motion audit src/Modal.tsx`, `/motion spring bounce 0.3`, `/motion upgrade`
- Trigger phrases: "Motion animation skill", "motion.dev", "MotionScore", "CSS spring easing"

## What it does

The official Motion AI Kit skill from the Motion team (Motion is the library formerly called Framer Motion, imported from `motion/react`). One skill with several modes:

- **Animation best practices**, hand-written by the creator of Motion, for vanilla JS, React, Vue, Base UI and Radix, for both Motion and plain CSS, including when to choose each.
- **Docs, example and Motion UI search** so the agent works from current Motion documentation.
- **CSS spring and bounce generation** using the `linear()` easing.
- **MotionScore performance audits** (code and runtime) that grade an animation and suggest cheaper alternatives.
- **Upgrade guidance** for moving from `framer-motion` to `motion` and between Motion versions.
- **Transition preview** for tuning curves and springs.

Best practices work with the plain skills install. Docs search and spring generation use Motion's free hosted MCP server, which a skills-only install does not set up (upstream's own `npx motion-ai` installer configures it). Audits and Motion UI source code need a paid Motion+ membership.

## When NOT to use

- Third-party Framer Motion skills split by topic (gestures, scroll, layout, variants) → use `framer-motion-skills`
- GSAP-specific projects or complex timeline orchestration → use `gsap-skills`
- Vanilla CSS animation without any library → use `animate-css-skill`
- Choosing between animation approaches → use `motion-catalogue`
