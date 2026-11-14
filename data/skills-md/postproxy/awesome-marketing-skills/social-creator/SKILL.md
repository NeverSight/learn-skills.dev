---
name: social-creator
description: When the user wants to create social media posts, plan social content, build a content calendar, or optimize social media strategy. Also use when the user mentions "LinkedIn post", "Twitter thread", "social media", "content calendar", "social content", "viral content", "Instagram post", or "TikTok."
version: 1.0.0
---

# Social Content Creator

Create engaging social media content with platform-specific hooks, formats, and strategies that build audience and drive results.

## Before You Start

**Check for product marketing context first:**
If `.claude/product-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered.

## Phase 1: Information Gathering

Collect context by asking the user focused questions in batches of 2-3.

### Required Context

1. **What do you need?** — Use `AskUserQuestion` with options:
   - Write specific post(s) right now
   - Plan a content calendar (week/month)
   - Repurpose existing content for social
   - Build a social content strategy from scratch
   - Improve / rewrite an existing post

2. **Platform(s)** — Use `AskUserQuestion` with multiSelect:
   - LinkedIn
   - Twitter / X
   - Instagram
   - TikTok
   - Facebook
   - Other

3. **Goal** — Use `AskUserQuestion` with options:
   - Brand awareness / grow audience
   - Drive traffic to website or product
   - Generate leads or signups
   - Build community and engagement
   - Thought leadership / authority

4. **Brand or personal?** — Use `AskUserQuestion` with options:
   - Personal brand (founder, creator)
   - Company brand
   - Both

5. **Voice and tone** — Ask: "Describe your social media voice in 3-5 words. (e.g., 'casual, witty, and contrarian' or 'professional, data-driven, helpful')"

6. **Topic/content** — Ask: "What do you want to post about? Share the topic, key points, or existing content to repurpose. The more detail the better."

7. **Content pillars** — Ask: "What 3-5 topics do you consistently post about? (e.g., product updates, industry insights, behind-the-scenes, educational tips, personal stories)"

8. **What's worked before** — Ask: "What types of posts have performed best for you? Any examples of posts that got great engagement?"

## Phase 2: Content Creation

### Platform Quick Reference

| Platform | Best For | Frequency | Key Format |
|----------|----------|-----------|------------|
| LinkedIn | B2B, thought leadership | 3-5x/week | Carousels, stories |
| Twitter/X | Tech, real-time, community | 3-10x/day | Threads, hot takes |
| Instagram | Visual brands, lifestyle | 1-2 posts + Stories/day | Reels, carousels |
| TikTok | Brand awareness, younger audiences | 1-4x/day | Short-form video |
| Facebook | Communities, local businesses | 1-2x/day | Groups, native video |

### Hook Formulas

The first line determines if anyone reads the rest.

**Curiosity:** "I was wrong about [common belief]." / "The real reason [outcome] happens isn't what you think."

**Story:** "Last week, [unexpected thing] happened." / "3 years ago, I [past state]. Today, [current state]."

**Value:** "How to [outcome] without [pain]:" / "[Number] [things] that [outcome]:"

**Contrarian:** "Unpopular opinion: [bold statement]" / "[Common advice] is wrong. Here's why:"

### Content Repurposing System

Turn one piece of content into many:

| Source | LinkedIn | Twitter/X | Instagram |
|--------|----------|-----------|-----------|
| Blog post | Key insight + link in comments | Thread of takeaways | Carousel of main points |
| Podcast | Quote graphic + lesson | Hot take from episode | Reel with key clip |
| Customer story | Mini case study post | Results thread | Before/after carousel |
| Data/research | Analysis post | Stats thread | Infographic carousel |

### Post Structure

For every post, include:
1. **Hook** — compelling first line
2. **Body** — value, story, or insight (platform-appropriate length)
3. **CTA** — what you want people to do (comment, share, click, save)

## Phase 3: Deliverables

Based on what was requested, generate and save:

- **`social-posts.md`** — Individual posts ready to publish, organized by platform
- **`content-calendar.md`** — Weekly/monthly calendar with post topics, formats, and platforms (if calendar was requested)

Present the content and suggest next steps (e.g., "Use /postproxy to publish these posts" or "Use /ad-campaigns to boost top performers").

## Guidelines

- Write posts that are ready to copy-paste and publish — no placeholder text
- Adapt voice, length, and format to each platform
- Avoid external links in the post body on LinkedIn and Twitter (kills reach) — put links in comments
- Don't over-hashtag — 3-5 relevant hashtags max on platforms that use them
- Every post should give value or provoke thought — pure promotion should be rare (< 10% of content)

## User Request

$ARGUMENTS
