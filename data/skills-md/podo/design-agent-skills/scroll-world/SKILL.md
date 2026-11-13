---
name: scroll-world
description: |
  Build a scroll-scrubbed "fly through the world" landing page: AI-generated scenes wired
  into one continuous camera flight, where scrolling only drives time. Use when someone
  wants a 3D world hero, a diorama landing page, a scroll cinematic, or to turn a brand or
  industry into a scrollable world. Bills per generated clip.
triggers:
  - "scroll scrubbed landing page"
  - "3d scroll landing page"
  - "diorama landing page"
  - "fly through world"
das:
  type: skill
  category: creative-3d
  upstream: "https://github.com/oso95/scroll-world"
  upstream_path: "skills/scroll-world/SKILL.md"
  version: latest
---

# scroll-world

> Catalogue stub — full skill: [oso95/scroll-world](https://github.com/oso95/scroll-world)

<!-- das:install:start — generated from stub.yaml by `npm run generate`; edit stub.yaml, not this block -->
## Decision tree

1. **Is the full skill already installed?**
   - Global: `f=~/.agents/skills/scroll-world/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - Project: `f=.agents/skills/scroll-world/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - `installed` → the skill is installed as `scroll-world`, invoke it and proceed
   - `pointer` → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/scroll-world ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add oso95/scroll-world --skill scroll-world -g -y
   ```

   **Project:**
   ```bash
   npx skills add oso95/scroll-world --skill scroll-world -y
   ```
   > **Claude Code:** send a command as a chat message starting with `!` to run it without leaving the conversation.

**Heads-up**

- **Requires:** a paid Higgsfield account with credits, plus the higgsfield CLI installed and authenticated (higgsfield auth login is an interactive OAuth step the agent cannot run for you); the monid CLI with a funded balance for the default video chain: Seedance 2.0 is billed per clip in USD (a 1080p six-scene chain is roughly $27), with Higgsfield credits as the fallback biller; ffmpeg and ffprobe on PATH
- **License:** MIT
<!-- das:install:end -->

## Invoke after install

- Skill name: `scroll-world`
- Trigger phrases: "scroll scrubbed landing page", "3d scroll landing page", "diorama landing page"

## What it does

Produces a landing page where **scroll drives a camera**, not a parallax offset: the view dives from outside each scene into its interior, flies back out and into the next one, continuously, with no visible cuts. It interviews for topic, story beats and brand kit, then generates N scene stills, N "dive-in" clips and N−1 "connector" clips, and drops in a self-contained vanilla-JS scrub engine (`references/scrub-engine.js`) that builds its own DOM, so it works in plain HTML, Next.js, Vue or anything else.

The skill's central discipline is the seamless chain: consecutive clips must be frame-identical at the seam, and it documents the seam method, the ffmpeg frame checks, and the prompts that keep scenes cohesive. Visuals come from Higgsfield stills plus a video chain rendered through Monid by default (Seedance 2.0, billed per clip in USD — roughly $27 for a 1080p six-scene chain) with Higgsfield credits as the fallback biller.

## When NOT to use

- Someone without a funded Higgsfield/Monid account, or a budget for generated video: this is the most expensive skill in the catalogue per output
- Scroll animation built from DOM, CSS or SVG rather than pre-rendered video (use `gsap-skills` for ScrollTrigger work, or `oil-motion` for scroll-driven video and sprite sequences)
- Real-time WebGL or three.js scenes the user can orbit (use `threejs-claude-skill-package` or `shader-dev`)
- Pieces and clips to reuse elsewhere rather than one landing page — `fal-ai-skills` and `generative-media-skills` cover media generation on its own
