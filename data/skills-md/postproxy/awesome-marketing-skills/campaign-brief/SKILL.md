---
name: campaign-brief
description: This skill should be used when the user asks to "create a campaign brief", "build a marketing brief", "plan a campaign", "create ad brief", "brief me on a campaign", "generate campaign prompts", "create marketing prompts", or wants to define campaign strategy for content generation.
version: 1.0.0
---

# Campaign Brief Builder

Build a structured campaign brief through guided conversation, then generate master prompts for image and text content creation.

## Overview

A campaign brief captures the strategic foundation for marketing content: what is being advertised, why, to whom, and with what message. This skill gathers that information interactively and produces reusable master prompts for AI-powered image generation and copywriting.

## Before You Start

**Check for product marketing context first:**
If `.claude/product-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered.

## Workflow

### Phase 1: Information Gathering

Collect campaign details by asking the user focused questions. Ask questions in batches of 2-3 to avoid overwhelming the user. Use the `AskUserQuestion` tool for structured choices where applicable, and open-ended questions for descriptive fields.

#### Required Fields

Gather the following information in order:

1. **What is advertised** — The product, service, brand, or offer being promoted. Ask: "What are we advertising? (e.g., a product, service, event, brand)"

2. **Product/service description** — A concise description of the product or service, including key features and differentiators. Ask: "Describe the product/service briefly — what makes it unique or noteworthy?"

3. **Communication purpose** — Why this campaign exists. Use `AskUserQuestion` with options:
   - Product/service promotion
   - Brand awareness
   - Event promotion
   - Seasonal/holiday campaign
   - Launch announcement
   - Re-engagement / win-back

4. **Communication goal** — The desired business outcome. Use `AskUserQuestion` with options:
   - Drive sales / conversions
   - Generate leads
   - Increase brand awareness
   - Drive website traffic
   - Grow social following
   - Educate audience

5. **Target audience** — Who the campaign is aimed at. Ask: "Who is the target audience? (e.g., young professionals, parents, small business owners)"

6. **Target audience description** — Psychographic and behavioral details. Ask: "Describe this audience — what do they value, what motivates them, what are their pain points?"

7. **Main message** — The single most important takeaway. Ask: "What is the main message or key takeaway for the audience? (e.g., 'Save 20% this weekend', 'The easiest way to manage your finances')"

#### Optional Context

If the user provides additional context, incorporate it:
- **Brand voice/tone** — Formal, playful, bold, minimal, etc.
- **Visual style preferences** — Photography style, color palette, mood
- **Platform targets** — Instagram, LinkedIn, Facebook, etc.
- **Campaign duration / timing** — Seasonal, limited-time, evergreen

### Phase 2: Brief Assembly

After gathering all information, assemble the brief as a structured markdown document. Present it to the user for review and confirmation before proceeding to prompt generation.

Use this format:

```markdown
# Campaign Brief

## What is Advertised
[whatIsAdvertised]

## Product/Service Description
[productDescription]

## Communication Purpose
**Primary:** [communicationPurpose]

## Communication Goal
**Primary:** [communicationGoal]

## Target Audience
**Segment:** [targetAudience]
**Description:** [targetAudienceDescription]

## Main Message
[mainMessage]

## Additional Context
- **Tone:** [if provided]
- **Visual style:** [if provided]
- **Platforms:** [if provided]
- **Timing:** [if provided]
```

Ask the user to confirm or request changes before proceeding.

### Phase 3: Master Prompt Generation

Once the brief is confirmed, generate two master prompts and save them to files in the current working directory.

#### Image Generation Master Prompt

Generate a file called `image-prompt.md` containing a master prompt for AI image generation tools (Midjourney, DALL-E, Flux, etc.). The prompt should:

- Describe the visual scene, composition, and mood that communicates the main message
- Include the product/service as the visual focus
- Reflect the target audience's aesthetic preferences
- Specify style direction (photography, illustration, 3D, etc.)
- Include technical parameters (aspect ratio suggestions, lighting, color palette)
- Provide 3 prompt variations: hero image, social media square, and story/vertical format

Use the template structure from `references/prompt-templates.md`.

#### Text Generation Master Prompt

Generate a file called `text-prompt.md` containing a master prompt for AI copywriting. The prompt should:

- Define the brand voice and tone based on the brief
- Include the main message as the core copy direction
- Specify audience-appropriate language and references
- Provide prompt templates for: headline, body copy, CTA, social media caption, and short-form ad copy
- Include 3 variations per format: direct/benefit-driven, emotional/storytelling, urgency/action-oriented

Use the template structure from `references/prompt-templates.md`.

### Phase 4: Save and Summary

Save all outputs:
- `campaign-brief.md` — The assembled brief
- `image-prompt.md` — Image generation master prompt
- `text-prompt.md` — Text generation master prompt

Present a summary of what was created and suggest next steps (e.g., "Use the image prompt with your preferred image generation tool" or "Use /postproxy to publish content based on the text prompts").

## Guidelines

- Keep questions conversational and concise
- If the user is unsure about a field, suggest reasonable defaults based on context
- Adapt language complexity to match what's being advertised (B2B vs B2C, luxury vs everyday)
- The master prompts should be immediately usable — no placeholder text
- When generating prompts, think like a creative director: be specific about visual composition, emotional tone, and copy structure

## Additional Resources

### Reference Files

- **`references/prompt-templates.md`** — Template structures for image and text master prompts with examples

## User Request

$ARGUMENTS
