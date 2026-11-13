---
name: huashu-art-motion
description: |
  Art and explainer video animation driven by code. Storyboard-first pipeline with many implemented art styles, reusable explainer-animation grammars that render from voice-over parameters, QA gates, and a delivery check. Docs are in Chinese.
triggers:
  - "huashu art motion"
  - "art style animation"
  - "explainer animation grammar"
  - "storyboard to animation video"
  - "recreate an animation in code"
das:
  type: skill
  category: motion-animation
  upstream: "https://github.com/alchaincyf/huashu-art-motion"
  version: latest
---

# huashu-art-motion

> Catalogue stub — full skill: [alchaincyf/huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion)

<!-- das:install:start — generated from stub.yaml by `npm run generate`; edit stub.yaml, not this block -->
## Decision tree

1. **Is the full skill already installed?**
   - Global: `f=~/.agents/skills/huashu-art-motion/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - Project: `f=.agents/skills/huashu-art-motion/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - `installed` → the skill is installed as `huashu-art-motion`, invoke it and proceed
   - `pointer` → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/huashu-art-motion ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add alchaincyf/huashu-art-motion --skill huashu-art-motion -g -y
   ```

   **Project:**
   ```bash
   npx skills add alchaincyf/huashu-art-motion --skill huashu-art-motion -y
   ```
   > **Claude Code:** send a command as a chat message starting with `!` to run it without leaving the conversation.

**Heads-up**

- **Requires:** uv; ffmpeg; Playwright Chromium (first run: uv run --with playwright playwright install chromium); Skill text and references are in Chinese
- **License:** MIT; bundled stroke data is Arphic Public License, fonts are SIL OFL, and the Huashu character artwork and demo videos are demo-use only (not MIT)
- **Large download (~154 MB):** the skills CLI gives up cloning after 300 s; if it times out, retry with `SKILLS_CLONE_TIMEOUT_MS=900000`.
<!-- das:install:end -->

## Invoke after install

- Skill name: `huashu-art-motion`
- Trigger phrases: "huashu art motion", "art style animation", "explainer animation grammar", "storyboard to animation video"

## What it does

Turns the agent into director, storyboarder, animator, and editor, with code as the paintbrush. The pipeline writes a shot list first (one visual style per film, a colour palette, shot-by-shot nouns and verbs), lints it, renders each shot as a video clip, concatenates, runs frame QA, and only delivers on a green check. It ships a library of implemented art styles and transferable style recipes, plus explainer-animation grammars that can render clips from voice-over parameters. AI-generated frames, existing recordings, and voice cloning are optional. Needs `uv`, Playwright, and `ffmpeg` locally; the skill text and references are written in Chinese.

## When NOT to use

- Magazine-grade typography and animated design prototypes → use `huashu-design`
- HTML-to-video rendering of existing web compositions → use `hyperframes` or `remotion`
- Interface micro-interactions and UI motion → use `design-motion-principles` or `emilkowalski-skill`
