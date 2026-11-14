---
name: go-to-market
description: When the user wants to plan a product launch, go-to-market strategy, or release campaign. Also use when the user mentions "launch plan", "GTM", "go-to-market", "product launch", "release strategy", "launch checklist", or "launch timeline."
version: 1.0.0
---

# Go-to-Market Launch Planner

Plan and execute a phased product launch using the ORB Framework (Owned, Rented, Borrowed channels) and a structured multi-phase approach.

## Before You Start

**Check for product marketing context first:**
If `.claude/product-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered.

## Phase 1: Information Gathering

Collect launch details by asking the user focused questions. Ask in batches of 2-3 using `AskUserQuestion` where applicable.

### Required Context

1. **What are you launching?** Ask: "What exactly are you launching? (e.g., new product, major feature, redesign, new pricing, beta program)"

2. **Launch stage** — Use `AskUserQuestion` with options:
   - Brand new product (first launch ever)
   - New feature or major update
   - Entering a new market/segment
   - Re-launch or repositioning
   - Beta / early access program

3. **Target audience** — Ask: "Who is this launch aimed at? Describe your ideal customer — their role, company size, pain points."

4. **Core value proposition** — Ask: "In one sentence, why should someone care about this launch? What's the transformation or key benefit?"

5. **Launch timeline** — Use `AskUserQuestion` with options:
   - Less than 2 weeks
   - 2-4 weeks
   - 1-2 months
   - 3+ months

6. **Existing audience** — Ask: "What existing channels do you have? (e.g., email list size, social followers, community members, blog traffic)"

7. **Budget & resources** — Use `AskUserQuestion` with options:
   - Bootstrapped (time only, no ad spend)
   - Small budget ($500-2K for ads/tools)
   - Moderate budget ($2K-10K)
   - Significant budget ($10K+)

8. **Launch platforms** — Use `AskUserQuestion` with multiSelect:
   - Product Hunt
   - Hacker News
   - Social media (LinkedIn, Twitter/X)
   - Email to existing list
   - Press / media outreach
   - Influencer partnerships
   - Paid ads

9. **Previous launches** — Ask: "Have you launched before? What worked and what didn't?"

## Phase 2: ORB Channel Strategy

Based on the gathered context, build a channel plan across three categories:

### Owned Channels (Direct access, no algorithms)
- Email list
- Blog / content
- Community (Discord, Slack, forum)
- Product itself (in-app announcements)

### Rented Channels (Platform-dependent visibility)
- LinkedIn, Twitter/X, Instagram, TikTok
- Product Hunt, Hacker News
- YouTube, podcasts

### Borrowed Channels (Leveraging others' audiences)
- Influencer/creator partnerships
- Guest posts, podcast appearances
- Co-marketing with complementary products
- Press and media coverage

For each channel, specify: what content to create, when to publish, and expected outcome.

## Phase 3: Five-Phase Launch Plan

Structure the launch across these phases:

### 1. Internal Launch (Week -4 to -3)
- Friendly user testing
- Gather testimonials and case studies
- Fix critical issues before public exposure

### 2. Alpha Launch (Week -3 to -2)
- Controlled external access (invite-only)
- Collect feedback from power users
- Build initial social proof

### 3. Beta Launch (Week -2 to -1)
- Expand access with buzz-building
- Seed content across owned channels
- Warm up email list and community

### 4. Early Access (Week -1 to Launch)
- Validation at scale
- Activate borrowed channels (influencers, partners)
- Pre-launch content push

### 5. Full Launch (Launch Day + Week 1)
- Open signup / general availability
- Maximum visibility push across all channels
- Coordinate all ORB channels simultaneously

## Phase 4: Deliverables

Generate and save the following files:

1. **`launch-plan.md`** — The complete phased launch plan with timeline, channels, and content calendar
2. **`launch-checklist.md`** — A checklist of everything to prepare before launch day

Present a summary and suggest next steps (e.g., "Use /social-creator to draft launch posts" or "Use /email-flows to build your launch email sequence").

## Guidelines

- Not every launch needs all five phases — adapt to the user's timeline
- Always emphasize converting rented/borrowed attention into owned relationships (email signups)
- Launches aren't one-time events — suggest ongoing "micro-launches" for features and updates
- Be specific about content types and timing, not vague about "create content"

## User Request

$ARGUMENTS
