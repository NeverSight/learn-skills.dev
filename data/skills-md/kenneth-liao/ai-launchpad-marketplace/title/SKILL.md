---
name: title
description: Generate optimized titles and headlines for any content type. Maximizes engagement through curiosity, complementarity with visual assets, and audience targeting.
---

# Title Generation

## Overview

This skill generates high-performing titles and headlines optimized for engagement across any content type. Titles are designed to spark curiosity, complement visual assets where applicable, and compel the audience to click, open, or engage.

**Core Principle**: Every title must prompt a specific question in the audience's mind. Description alone is insufficient — curiosity is non-negotiable.

## When to Use

Use this skill when:
- The user asks to create a title, headline, or subject line
- The user requests title ideas or brainstorming for content
- The user wants to improve or optimize an existing title
- Working on content creation and a title is needed
- The user asks for multiple title variations to test

## Content Type Resolution

Before generating titles, determine the content type and load the appropriate platform-specific reference file:

| Content Type | Reference File | Key Focus |
|---|---|---|
| YouTube video | `references/youtube-title-formulas.md` | CTR, curiosity, thumbnail complementarity |
| Newsletter / email | `references/newsletter-subject-lines.md` | Open rate, preview text, inbox competition |
| Social media post | `references/social-headlines.md` | Scroll-stopping, platform-specific hooks |

**MANDATORY**: Read the relevant reference file before generating titles. These references contain platform-specific patterns, forbidden patterns, and quality standards that are non-negotiable.

If the content type does not match any reference file, apply the universal principles below and adapt to the format.

## Prerequisites

### Gather Context

Before generating titles, gather the following information from conversation context, the user's filesystem, or by asking the user directly.

**Required Information:**
- **Content topic**: What is the content about?
- **Target audience**: Who is this for?
- **Key message**: What is the main takeaway or hook?

**Highly Recommended Information:**
- **Visual asset description**: What does the thumbnail, header image, or preview show?
- **Target emotion**: What emotion should the title evoke? (curiosity, shock, excitement, urgency)
- **Content type**: Video, newsletter, social post, blog article, etc.

## Title Generation Workflow

### Step 1: Gather Context

Collect required information if not already provided. Ask the user for anything missing:

```
To create an optimized title, I need to understand:
1. What is the content about? (topic)
2. Who is your target audience?
3. What is the main hook or takeaway?
4. Do you have a visual asset (thumbnail, header image)? If so, what does it show?
5. What emotion should the title evoke?
```

### Step 2: Load Platform Reference

**MANDATORY ACTION**: Read the appropriate platform-specific reference file based on the content type identified in Step 1.

### Step 3: Identify the Question

Before writing any title, identify the specific question you want in the audience's mind:

- What question will make them curious enough to engage?
- Does this question align with the content?
- Is the curiosity gap strong enough to drive action?

**Examples of effective questions to prompt:**
- "What mistakes am I making?" (mistake framing)
- "What happened?" (outcome uncertainty)
- "Why would someone do that?" (extreme behavior)
- "How is that possible?" (surprising claim)

### Step 4: Generate Title Options

Generate 3-5 title variations that:
1. Prompt the identified question
2. Complement (not duplicate) any visual assets
3. Align with the target emotion
4. Follow platform-specific best practices from the reference file

### Step 5: Verify Against Checklist

**For each title, verify against the universal checklist:**
- [ ] **Curiosity Test**: Does this prompt a specific question?
- [ ] **Complementarity Test**: Does this work WITH visual assets (not duplicate them)?
- [ ] **Click/Open Compulsion Test**: Is the curiosity gap strong enough?
- [ ] **Non-Descriptive Test**: Does this go beyond merely describing content?
- [ ] **Target Audience Test**: Will this resonate with the intended audience?

### Step 6: Present and Refine

Present title options to the user with:
1. The title itself
2. The question it prompts in the audience's mind
3. How it complements the visual asset (if applicable)
4. Why it should drive engagement

Example presentation:

```
Here are 3 optimized title options:

1. "The AI Agent Mistake That Cost Me 10 Hours"
   - Prompts: "What mistake? How can I avoid it?"
   - Complements thumbnail showing frustrated face + error message
   - Creates urgency through time cost

2. "I Built This AI Agent Wrong (Here's What I Learned)"
   - Prompts: "What did they do wrong? What's the lesson?"
   - Personal experience framing creates relatability

3. "Why Your AI Agents Keep Breaking (And Mine Don't)"
   - Prompts: "Why do mine break? What's their secret?"
   - Creates contrast and curiosity
```

### Step 7: Iterate Based on Feedback

If the user requests changes:
1. Understand what aspect needs adjustment (curiosity, tone, length, etc.)
2. Regenerate while maintaining checklist compliance
3. Re-verify against the checklist

## Voice Application

Before finalizing any written output, invoke the `writing:voice` skill to apply voice rules. Titles should sound authentic to the user's voice, not generic.

## Brand Compliance

When creating assets for The AI Launchpad, invoke `branding-kit:brand-guidelines` to resolve the correct design system and check anti-patterns.

## Quality Assurance

### Priority Order
1. **Spark curiosity** (highest priority)
2. **Complement visual asset**
3. **Raise audience question**
4. **Create click/open compulsion**

### Rejection Criteria

**REJECT and regenerate if the title:**
- Merely describes the content without sparking curiosity
- Duplicates text that appears on the visual asset
- Answers the question instead of raising it
- Uses generic patterns without intrigue
- Fails the "What question does this raise?" test

### Success Criteria

**A successful title:**
- Prompts a specific, compelling question in the audience's mind
- Works synergistically with any visual asset
- Creates a curiosity gap strong enough to drive engagement
- Aligns with the target audience and content type
- Passes all 5 universal checklist items

## Common Pitfalls

1. **Generic Description**: "AI Agents Tutorial" describes but does not intrigue. Add curiosity.
2. **Answering the Question**: "How to Fix AI Agent Memory in 3 Steps" gives away too much. Tease, do not tell.
3. **Ignoring Platform**: A YouTube title and a newsletter subject line have different constraints. Load the right reference.
4. **Thumbnail/Asset Duplication**: If the thumbnail says "BROKEN", the title should not also say "broken." Complement, do not repeat.
5. **Single Option**: Always provide 3-5 variations for the user to choose from.
