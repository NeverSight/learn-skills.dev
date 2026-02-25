---
name: remotion-prompt-generator
description: "Generate detailed, production-ready prompts for the Remotion Dev skill to create programmatic React-based videos. MANDATORY TRIGGERS: remotion prompt, video prompt, generate video prompt, remotion video, create video prompt, video brief, video specification, make a video, create a video. Also trigger when user wants to create any kind of video using Remotion, needs help describing a video project, wants a prompt for a video generation tool, or asks for a video brief/spec. When in doubt, use it."
license: MIT
metadata:
  version: "1.1.0"
  author: Abhishek Sharma
  tags: ["remotion", "video-generation", "prompt-engineering", "react-video", "ai-prompts"]
---

# Remotion Prompt Generator — Skill Router

> Generate comprehensive, structured prompts that the Remotion Dev skill can use to produce professional programmatic videos.

## MANDATORY: Always-Load References

**Before generating ANY prompt, you MUST read these two files first:**
1. `references/remotion-capabilities.md` — Core Remotion knowledge (architecture, features, limitations, packages)
2. `references/intelligent-inference.md` — How to analyze vague requests and auto-fill smart defaults

## MANDATORY: Web Search Requirement

**Before generating a prompt, you MUST perform web search** to gather context about what the user is building:
- Search for the user's product/company/industry if mentioned
- Search for current design trends relevant to their video type
- Search for competitor examples or reference videos in their space
- This context makes prompts dramatically better — never skip it

## Reference Files

| Reference | File | Read When |
|-----------|------|-----------|
| **Remotion Capabilities** | `references/remotion-capabilities.md` | **ALWAYS READ FIRST** — core Remotion knowledge needed for every prompt |
| **Intelligent Inference** | `references/intelligent-inference.md` | **ALWAYS READ** — how to handle vague prompts, auto-fill defaults, infer from signals |
| **Video Types (Router)** | `references/video-types.md` | Identifying video category: marketing, social, data-viz, education, e-commerce, etc. |
| **Prompt Engineering** | `references/prompt-engineering.md` | How to structure the final prompt output, 12-section format, scene descriptions |
| **Discovery Workflow** | `references/discovery-workflow.md` | Follow-up questions to ask users, requirement gathering, clarification strategies |
| **Asset & Styling Guide** | `references/asset-styling-guide.md` | Colors, fonts, logos, images, audio, branding, dimensions, platform specs |
| **Animation & Effects** | `references/animation-effects.md` | Spring physics, transitions, easing, text animations, 3D, particles, motion patterns |
| **Domain Examples (Router)** | `references/prompt-engineering/domain-examples.md` | Real prompt examples for specific industries: SaaS, real estate, finance, education |

## How This Skill Works

1. **ALWAYS** read `remotion-capabilities.md` and `intelligent-inference.md` first
2. **ALWAYS** do a web search about what the user wants to build (their product, industry, competitors)
3. Analyze the user's request — extract every signal, infer what you can, auto-fill smart defaults
4. Ask only 2-3 critical questions that cannot be inferred (use AskUserQuestion tool)
5. Read the relevant video-type sub-reference and domain example
6. Generate a complete, detailed, 12-section structured prompt for the Remotion Dev skill
7. The Remotion Dev skill uses that prompt to write React/Remotion code

## Quick Reference

- **Remotion docs:** https://remotion.dev/docs
- **GitHub:** https://github.com/remotion-dev/remotion
- **Templates:** https://remotion.dev/templates
