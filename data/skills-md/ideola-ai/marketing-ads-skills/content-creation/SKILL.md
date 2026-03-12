---
name: content-creation
description: Create social media content assets with ready-to-use copy and visual direction. Use when user asks to create content, write captions, make posts, or generate social media assets. Triggers on - "buat konten", "content create", "buat caption", "/content-create" command, or requests to create specific social media posts with copy and visuals.
---

# Content Creation Assistant

## Overview

This skill generates ready-to-publish social media content including copy, scripts, and visual direction. It transforms content queue items from content-plan into fully developed content assets.

## Marketing OS Workflow Position

```
brand-voice → content-brief → content-planning → content-creation
                                          ↓
                                        marketing-campaign
                                          ↓
                                          ads-audit
```

**This skill is FOURTH** - Create content assets after planning, for immediate publishing or as reference for ad creatives.

**Input from:**
- `/brand-voice` - Voice attributes and tone guidelines
- `/content-brief` - Visual direction, brand voice, key messages
- `/content-planning` - Content queue with topics, pillars, CTAs

**Output for:**
- Direct use for posting
- Brief for designers
- `/ads-audit` - Creative quality reference

## Workflow

### Step 1: Gather Content Requirements

Before creating content, collect these inputs:

**From Content Plan (if available):**
- Content ID/Topic from queue
- Platform and format
- Pillar and key message
- CTA specified

**Additional Information Needed:**
- Specific topic or angle to focus on
- Brand voice preference (casual, professional, playful, etc.)
- Any specific assets or references
- Hashtag requirements

**Ask if not provided:**
1. Konten untuk platform dan format apa?
2. Topik spesifik apa yang mau diangkat?
3. Ada brand voice atau tone tertentu?
4. Butuh berapa banyak hashtag?

### Step 2: Select Content Format

Generate content based on the requested format. See `rules/formats.md` for detailed specifications for each format type.

**Supported Formats:**
- Static posts (single image)
- Carousels (multi-slide)
- Videos/Reels (short-form video)
- Stories (ephemeral content)
- Threads (Twitter/X, LinkedIn)

### Step 3: Generate Copy/Script

Create compelling copy or script following platform best practices. See `rules/copywriting.md` for frameworks and techniques.

### Step 4: Define Visual Direction

Provide clear visual direction for designers or AI image generation. See `rules/visuals.md` for guidelines.

### Step 5: Add Metadata

Complete the content with hashtags, alt text, and posting metadata.

## Output Structure

Each content asset should include:

```markdown
# [Content ID] - [Platform] [Format]

## Content Overview
- **Platform:** [Platform]
- **Format:** [Format]
- **Topic:** [Topic]
- **Pillar:** [Pillar]

## Copy/Script
[Ready-to-use copy or script]

## Visual Direction
[Detailed visual instructions]

## Metadata
- **Hashtags:** [10-30 relevant hashtags]
- **Alt Text:** [Accessibility description]
- **CTA:** [Call to action]
- **Best Post Time:** [Optimal time]
```

## Platform-Specific Guidelines

See `rules/` folder for detailed platform specifications:
- `rules/platforms/instagram.md`
- `rules/platforms/tiktok.md`
- `rules/platforms/linkedin.md`
- `rules/platforms/twitter.md`

## Format-Specific Guidelines

See `rules/formats.md` for:
- Static post specifications
- Carousel structure and flow
- Video script templates
- Story interactive elements
- Thread structure

## Copywriting Frameworks

See `rules/copywriting.md` for:
- Hook formulas
- CTA templates
- Storytelling structures
- Platform-specific tones

## Visual Direction Guidelines

See `rules/visuals.md` for:
- Composition guidelines
- Color theory for social
- Typography best practices
- Brand element integration

## Best Practices

1. **Hook first** - First 1-3 seconds determine if people stop scrolling
2. **Platform-native** - Each platform has unique conventions
3. **Value upfront** - Don't bury the lead
4. **Clear CTA** - Always tell them what to do next
5. **Mobile-first** - Most content is consumed on mobile

## Quick Start Example

```bash
# User runs:
/content-create

# Agent asks:
1. Platform/format? "Instagram Carousel"
2. Topic? "5 tips produktivitas untuk WFH"
3. Brand voice? "Casual, friendly"

# Agent produces:
- Full carousel copy with slide-by-slide breakdown
- Visual direction for each slide
- Hashtags and metadata
- Posting recommendations
```

## Integration with Marketing OS Workflow

**Input from:**
- `/brand-voice` - Voice attributes and tone guidelines
- `/content-brief` - Visual direction, brand voice, key messages
- `/content-planning` - Content queue with topics, pillars, CTAs

**Output for:**
- Direct use for posting
- Brief for designers
- Script for video production
- `/ads-audit` - Creative quality reference when auditing ad creatives

## Quick Start Example
