---
name: ad-campaigns
description: When the user wants to create, plan, or optimize paid advertising campaigns. Also use when the user mentions "paid ads", "Google Ads", "Meta ads", "Facebook ads", "LinkedIn ads", "ad copy", "ad creative", "PPC", "ROAS", "ad campaign", or "paid media."
version: 1.0.0
---

# Ad Campaign Planner

Plan and create paid advertising campaigns across Google, Meta, LinkedIn, Twitter/X, and TikTok — from strategy to ad copy.

## Before You Start

**Check for product marketing context first:**
If `.claude/product-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered.

## Phase 1: Information Gathering

Collect context by asking the user focused questions in batches of 2-3.

### Required Context

1. **What are you promoting?** Ask: "What product, service, or offer are you advertising? Describe it briefly and include the landing page URL if you have one."

2. **Campaign objective** — Use `AskUserQuestion` with options:
   - Drive signups / free trials
   - Generate leads (demo requests, downloads)
   - Direct sales / purchases
   - Brand awareness / reach
   - App installs
   - Retarget existing visitors

3. **Target audience** — Ask: "Who are you targeting? Describe them: job titles, industries, company size, interests, pain points, demographics."

4. **Platform(s)** — Use `AskUserQuestion` with multiSelect:
   - Google Search Ads
   - Google Display / YouTube
   - Meta (Facebook + Instagram)
   - LinkedIn
   - Twitter / X
   - TikTok
   - Not sure — recommend based on my audience

5. **Budget** — Use `AskUserQuestion` with options:
   - Testing budget ($500-2K/month)
   - Growth budget ($2K-10K/month)
   - Scale budget ($10K-50K/month)
   - Enterprise budget ($50K+/month)

6. **Previous ad experience** — Ask: "Have you run paid ads before? What worked, what didn't? Share any metrics you have (CPC, CPA, ROAS, conversion rate)."

7. **Conversion infrastructure** — Use `AskUserQuestion` with multiSelect:
   - Pixel/tracking installed (Meta, Google, etc.)
   - Conversion events set up
   - Landing page optimized for the offer
   - Retargeting audiences built
   - None of the above yet

8. **Creative assets** — Ask: "What creative assets do you have or can you create? (e.g., product screenshots, lifestyle photos, video, customer testimonials, brand guidelines)"

9. **Competitor context** — Ask: "Who are your top competitors running ads? Have you seen their ads? Any messaging you want to differentiate from?"

## Phase 2: Campaign Design

### Platform Selection Guide

| Platform | Best For | Audience Signal | Ad Format |
|----------|----------|-----------------|-----------|
| Google Search | High-intent demand capture | Keywords (what they search) | Text ads |
| Google Display/YT | Awareness + retargeting | Demographics + interests | Banner, video |
| Meta | Demand generation + retargeting | Interests + behaviors + lookalikes | Image, video, carousel |
| LinkedIn | B2B targeting by role/company | Job title, company, industry | Sponsored content, InMail |
| Twitter/X | Tech audiences, real-time | Interests, followers, keywords | Promoted tweets, video |
| TikTok | Younger demos, viral creative | Interests, behaviors | Short-form video |

### Campaign Structure

For each platform, specify:

1. **Campaign objective** (awareness, consideration, conversion)
2. **Audience targeting** — specific targeting parameters
3. **Ad format** — what the ad looks like
4. **Ad copy** — headline, description, CTA (3 variations minimum)
5. **Budget allocation** — how much of total budget goes here
6. **Bidding strategy** — recommended bid approach
7. **Landing page** — where the click goes

### Ad Copy Framework

For each ad, write 3 variations:

**Variation A — Benefit-led**
- Lead with the primary outcome/benefit
- Direct and clear

**Variation B — Problem-agitation**
- Name the pain point
- Show the consequence of inaction
- Present the solution

**Variation C — Social proof / Authority**
- Lead with credibility (numbers, logos, results)
- Build trust before the ask

### Budget Allocation Strategy

| Phase | Allocation | Purpose |
|-------|-----------|---------|
| Testing (Month 1) | 70% proven / 30% experimental | Find what works |
| Scaling (Month 2-3) | 80% winners / 20% new tests | Double down on winners |
| Optimization (Ongoing) | 90% optimized / 10% testing | Maintain and improve |

## Phase 3: Deliverables

Generate and save:

1. **`ad-campaign-plan.md`** — Complete campaign plan with platform strategy, audience targeting, budget allocation, and timeline
2. **`ad-copy.md`** — All ad copy variations organized by platform and format

Present a summary and suggest next steps (e.g., "Use /conversion-audit to optimize your landing page before launching" or "Use /split-test to plan ad creative tests").

## Guidelines

- Always verify tracking/pixel setup before recommending ad spend
- Start small, test, scale what works — never launch at full budget
- Landing page quality is half the battle — great ads with bad landing pages waste money
- Be platform-specific with ad copy — what works on LinkedIn doesn't work on TikTok
- Recommend UTM parameters for every campaign
- Flag if the budget is too low for meaningful data on the chosen platform

## User Request

$ARGUMENTS
