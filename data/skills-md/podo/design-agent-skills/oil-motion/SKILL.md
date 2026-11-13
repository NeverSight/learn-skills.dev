---
name: oil-motion
description: |
  Turns AI-generated or existing video and image sequences into web animation that responds to scroll, pointer, drag, touch, device orientation, audio, data, or state. Designs the motion, produces keyframes and clips, packs sprite sheets or video, compiles a timeline, and wires up a runtime. Docs are in Chinese.
triggers:
  - "oil motion"
  - "scroll-driven video animation"
  - "sprite sequence web animation"
  - "pointer-driven video"
  - "scroll-scrubbed video"
das:
  type: skill
  category: motion-animation
  upstream: "https://github.com/oil-oil/oil-motion"
  upstream_path: "SKILL.md"
  version: latest
---

# oil-motion

> Catalogue stub — full skill: [oil-oil/oil-motion](https://github.com/oil-oil/oil-motion)

<!-- das:install:start — generated from stub.yaml by `npm run generate`; edit stub.yaml, not this block -->
## Decision tree

1. **Is the full skill already installed?**
   - Global: `f=~/.agents/skills/oil-motion/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - Project: `f=.agents/skills/oil-motion/SKILL.md; [ -f "$f" ] && ! grep -q "^das:" "$f" && echo "installed" || echo "pointer"`
   - `installed` → the skill is installed as `oil-motion`, invoke it and proceed
   - `pointer` → go to step 2

2. **Detect scope, then install:**

   ```bash
   [ -e ~/.agents/skills/oil-motion ] && echo "global" || echo "project"
   ```

   **Global:**
   ```bash
   npx skills add oil-oil/oil-motion --skill oil-motion -g -y
   ```

   **Project:**
   ```bash
   npx skills add oil-oil/oil-motion --skill oil-motion -y
   ```
   > **Claude Code:** send a command as a chat message starting with `!` to run it without leaving the conversation.

**Heads-up**

- **Requires:** Python 3.10+, Pillow, ffmpeg and ffprobe (the skill has the agent run `pip install -r scripts/requirements.txt` at use time); For AI keyframe and video generation only (local processing of existing media needs no key): a ZenMux API key, billed per generation. Prompts, reference images and key frames are sent to ZenMux and the model providers behind it. The key-entry setup page needs Node.js 22.18+ and upstream says it has so far been verified on macOS only
- **License:** MIT
<!-- das:install:end -->

## Invoke after install

- Skill name: `oil-motion`
- Trigger phrases: "oil motion", "scroll-driven video animation", "sprite sequence web animation", "pointer-driven video"

## What it does

Converts an interaction intent into verified animation assets, a timeline manifest, and a web runtime. AI generation handles semantic changes such as a character turning, a product exploding into parts, or a camera flying through a scene; deterministic code handles input mapping, playback control, media processing, and performance. It also cleans up, keys out, frame-interpolates, and compresses green-screen video and sprite sheets. Four single sources of truth (concept contract, motion brief, timeline, motion budget) keep the pipeline consistent. AI generation defaults to ZenMux and needs an API key (and sends prompts and images to a third party), while local processing of existing media does not; see the heads-up above. Skill text is in Chinese.

## When NOT to use

- Transitions and micro-interactions achievable with plain CSS, JS, SVG, or Lottie → use `css-animation-skill`, `gsap-skills`, or `framer-motion-skills`
- Real-time 3D scenes → use `cloudai-threejs`
- Standalone video editing or composition → use `remotion` or `hyperframes`
