---
name: fal-ai-skills
description: |
  2 official fal.ai skills: image/video generation using fal.ai AI models,
  and 3D model generation from text or images. Requires a fal.ai API key.
triggers:
  - "fal.ai"
  - "fal generate"
  - "fal 3D"
  - "generate image fal"
  - "generate video fal"
  - "3D model from image"
das:
  category: creative-3d
  upstream: "https://github.com/fal-ai-community/skills"
  version: latest
  install: false
---

# fal-ai-skills

> Catalogue stub — full package: [fal-ai-community/skills](https://github.com/fal-ai-community/skills)

## Decision tree

Run this before using fal.ai generation features:

1. **Is a fal.ai skill already installed?**
   Check: `~/.design-agent-skills/skills/fal-generate/SKILL.md` exists.
   - Yes → invoke the specific skill by name and proceed
   - No → go to step 2

2. **Do you have shell access?**
   - Yes → run the install command below, then invoke the skill
   - No → show the install command; in Claude Code, send it as a chat message starting with `!` — add `-g` for global install or omit for project-only

## Install command

```bash
# Generate images and videos using fal.ai models
npx skills add fal-ai-community/fal-generate

# Generate 3D models from text or images
npx skills add fal-ai-community/fal-3d
```

Requires: `FAL_KEY` environment variable set to your fal.ai API key.

## Invoke after install

- `fal-generate` — "generate image", "generate video", "fal generate"
- `fal-3d` — "generate 3D model", "3D from image", "fal 3D"

## What it does

Official fal.ai community skills for AI media generation. `fal-generate` creates images and videos using fal.ai's model zoo (FLUX, Stable Diffusion, video models). `fal-3d` generates 3D models from text descriptions or reference images. Both require a fal.ai API key.
