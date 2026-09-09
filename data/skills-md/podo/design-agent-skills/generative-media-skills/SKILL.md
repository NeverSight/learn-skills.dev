---
name: generative-media-skills
description: |
  41 workflow recipes for AI media generation covering Midjourney v7, Flux Kontext, Kling 3.0,
  Veo3, Seedance 2.0, and 100+ models. Covers image generation, video creation, audio (Suno),
  and social media content. Requires a muapi account and muapi-cli.
triggers:
  - "generative media"
  - "Flux Kontext"
  - "Kling 3.0"
  - "Veo3"
  - "SamurAIGPT"
das:
  category: creative-3d
  upstream: "https://github.com/SamurAIGPT/Generative-Media-Skills"
  version: latest
  install: false
---

# generative-media-skills

> Catalogue stub — full platform: [SamurAIGPT/Generative-Media-Skills](https://github.com/SamurAIGPT/Generative-Media-Skills)

## Account requirement

**A muapi account is required.** Sign up at [muapi.ai](https://muapi.ai) before installing. The `muapi-cli` tool provides the runtime bridge to 100+ AI media models.

## Install methods

| Method | Command |
|--------|---------|
| Install all 41 skills | `npx skills add SamurAIGPT/Generative-Media-Skills --all` |
| Install individual skill | `npx skills add SamurAIGPT/Generative-Media-Skills --skill <name>` |
| Authenticate muapi | `npx muapi-cli auth login` |

## Decision tree

1. **Do you have a muapi account?**
   - No → direct user to [muapi.ai](https://muapi.ai) to create an account first.
   - Yes → go to step 2.
2. **Is muapi-cli authenticated?** Run `npx muapi-cli auth status`.
   - No → run `npx muapi-cli auth login`
   - Yes → go to step 3.
3. **Are the skills installed?** Check `~/.design-agent-skills/skills/` for generative-media skill directories.
   - No → run the install command above.
   - Yes → invoke the relevant skill by name.

## What it does

Provides 41 structured workflow recipes that orchestrate 100+ AI media generation models through the muapi platform. Covers text-to-image (Midjourney v7, Flux Kontext, DALL-E), text-to-video (Kling 3.0, Veo3, Seedance 2.0), music and audio generation (Suno), and social media content creation workflows. Each skill encapsulates prompt patterns, parameter tuning, and model selection for a specific media output type.

## When NOT to use

- Without a muapi account — the skills require muapi-cli authentication
- fal.ai model workflows specifically — use fal-ai-skills instead
- Static image editing without AI generation
