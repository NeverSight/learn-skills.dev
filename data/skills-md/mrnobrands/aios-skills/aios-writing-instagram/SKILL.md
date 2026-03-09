---
name: aios-writing-instagram
description: >
  Write Instagram captions and carousel content. Use when asked to write,
  create, draft, or produce an Instagram post, Instagram caption, Instagram
  carousel, Instagram reel caption, or Instagram story text. Also use when
  user mentions Instagram in a social media writing context. Outputs captions
  with hashtag blocks and image prompts.
metadata:
  author: claim-supply
  version: 1.0.0
---

# Writing Instagram

## Purpose
Produce publish-ready Instagram captions and carousel outlines that match brand voice with a warmer, more accessible tone suited to the visual platform.

## When to Use
- User asks to write an Instagram post, caption, or carousel
- User mentions Instagram in a writing context
- Orchestrator (aios-writing-social) delegates an Instagram post

### Do NOT Use For
- Other platforms (use aios-writing-linkedin, aios-writing-twitter, etc.)
- Instagram ads (use writing-ads)

## Context Loading
Read all context files listed in aios-writing-social.

## Process

### Step 1: Parse the Request
Extract topic, content pillar, audience, type.

Defaults if unspecified:
- Content Pillar: Pillar 4 — Product/Visual content (20%)
- Audience: All audiences
- Type: Educational or Social Proof

### Step 2: Write the Post

Caption Rules:
- 150-300 words, conversational tone
- 2,200 character max
- CTA works well as "Save this" or "Share with..."
- 10-15 hashtags in a separate comment block (not in caption)
- Include IMAGE PROMPT for visual direction

Carousel Rules:
- Outline each slide with title and content
- Slide 1 is hook/title
- Final slide is CTA
- 5-10 slides typical
- Each slide should work visually (short text, bold statements)

Tone:
- Warmer and more accessible than LinkedIn
- Visual-first language (describe what they will see)
- Conversational, relatable
- Emojis acceptable but not excessive

### Step 3: Self-Review
Apply all quality gates from aios-writing-social.

Additional Instagram checks:
- Caption under 2,200 characters
- 10-15 hashtags in separate block
- IMAGE PROMPT included for visual direction
- Carousel slides are scannable (short text per slide)
- Tone is warmer than LinkedIn

## Output Format

Single post:

    PLATFORM: Instagram
    CONTENT PILLAR: [pillar]
    AUDIENCE: [segment]
    ---
    [CAPTION TEXT]
    ---
    HASHTAGS: [10-15 in comment block]
    IMAGE PROMPT: [visual direction]
    NOTES: [reviewer notes]

Carousel:

    PLATFORM: Instagram (Carousel)
    SLIDE 1: [Hook/Title]
    SLIDE 2: [Content]
    ...
    SLIDE [N]: [CTA]
    CAPTION: [full caption]
    HASHTAGS: [in comment block]
    IMAGE PROMPT: [visual direction per slide]

## References
- references/hook-patterns.md
- references/post-templates.md
- shared/platform-specs.md
- shared/compliance-rules.md
