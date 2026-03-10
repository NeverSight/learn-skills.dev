---
name: marketing-content
description: Content strategy, copywriting frameworks (AIDA/PAS/BAB/4Ps/FAB), editorial calendar management, platform-specific content, A/B testing, campaign planning, audience targeting, and content performance measurement.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Bash]
agents: [marketing-strategist]
category: domain-specific
tags: [marketing, content, copywriting, editorial, campaign, A/B-testing, audience, platform]
best_practices:
  - Match copywriting framework to audience awareness stage
  - Test every content variant before scaling
  - Adapt content format to platform algorithm requirements
  - Track engaged sessions not just pageviews
  - Use human-AI collaboration model for highest quality
error_handling: graceful
streaming: supported
---

# Marketing Content Skill

## Overview

Enable `marketing-strategist` agents to produce high-quality, data-driven marketing content using proven frameworks, structured workflows, and measurable performance loops.

This skill covers the full content lifecycle:

- **Strategy** → audience mapping, funnel alignment, channel selection
- **Creation** → copywriting frameworks, platform adaptation
- **Operations** → editorial calendar, scheduling, workflow
- **Optimization** → A/B testing, iteration, performance KPIs
- **Measurement** → engagement, conversion, retention, ROI

## When to Use

Invoke when asked to:

- Write or plan marketing copy (ads, emails, blog posts, social)
- Build or maintain an editorial calendar
- Design a content campaign with objectives and KPIs
- Optimize existing content performance
- Conduct audience segmentation for content targeting
- A/B test content variants
- Adapt content for a specific platform (LinkedIn, TikTok, Email, etc.)

## Enforcement Hooks

Input validated against `schemas/input.schema.json` before execution.
Output contract defined in `schemas/output.schema.json`.

Pre-execution hook: `hooks/pre-execute.cjs`
Post-execution hook: `hooks/post-execute.cjs`

---

## Content Strategy Framework

### Step 1: Audience Mapping

Before writing a single word, define:

- **Who**: Primary audience segment (demographics, psychographics, intent signals)
- **Where**: Platform/channel they are on
- **When**: Buying stage / funnel position (Awareness → Consideration → Decision)
- **Why**: Pain point or aspiration driving search/scroll

**Audience Awareness Stages → Framework Match:**

| Awareness Stage | Best Framework | Why                                         |
| --------------- | -------------- | ------------------------------------------- |
| Unaware (cold)  | AIDA, PAS      | Build attention first; introduce problem    |
| Problem-aware   | PAS, BAB       | Lead with pain, show resolution             |
| Solution-aware  | 4Ps, FAB       | Evidence-based; translate features to value |
| Product-aware   | FAB, BAB       | Show transformation; competitor contrast    |
| Most aware      | Direct CTA     | Skip education; they are ready              |

### Step 2: Content Pillar Definition

Organize content into 3-5 pillars per brand/product:

1. **Educational**: Solves a problem (SEO-driven, evergreen)
2. **Inspirational**: Shows aspiration, transformation (social-first)
3. **Promotional**: Drives direct action (conversion-focused)
4. **Community**: User-generated, testimonials (trust signals)
5. **Behind-the-Scenes**: Builds brand personality (engagement)

### Step 3: Channel Selection

| Channel      | Content Type                          | Goal                      | Cadence    |
| ------------ | ------------------------------------- | ------------------------- | ---------- |
| Blog/SEO     | Long-form evergreen, 1500-3000 words  | Organic traffic           | 2-4x/month |
| LinkedIn     | Thought leadership, case studies      | B2B awareness             | 3-5x/week  |
| Email        | Segmented newsletters, drip sequences | Retention + conversion    | 1-3x/week  |
| TikTok/Reels | Short-form video, <60s hooks          | Discovery + top-of-funnel | Daily      |
| Facebook     | Carousel, events, community posts     | Community + retargeting   | 3-5x/week  |

---

## Copywriting Patterns

### AIDA Framework (Cold Audience)

```
ATTENTION: Grab with bold claim, stat, or question
INTEREST:  Explain relevance to reader's situation
DESIRE:    Show transformation, testimonials, proof
ACTION:    Single clear CTA (avoid multiple options)
```

**Example (Email subject + body)**:

```
Subject: "68% of marketers are wasting their content budget"
[ATTENTION] Most companies publish content nobody reads.
[INTEREST]  The difference? A documented content strategy.
[DESIRE]    Teams using structured content plans see 3x ROI.
[ACTION]    Download the 2025 Content Strategy Playbook →
```

### PAS Framework (Problem-Aware Audience)

```
PROBLEM:   Name the exact pain point
AGITATE:   Amplify the consequences of inaction
SOLUTION:  Present your offer as the logical answer
```

### BAB Framework (Transformation Stories)

```
BEFORE:    Describe life with the problem
AFTER:     Paint the aspiration/desired state
BRIDGE:    Explain how your product/service creates the bridge
```

### 4Ps Framework (Informed/Warm Audience)

```
PROBLEM:   State the problem (brief; audience already aware)
PROMISE:   Make a specific, believable claim
PROOF:     Evidence (stats, case studies, testimonials)
PROPOSAL:  Concrete offer with CTA
```

### FAB Framework (Product Copy)

```
FEATURE:   What the product has/does
ADVANTAGE: Why that feature matters
BENEFIT:   How it improves the customer's life
```

---

## Platform-Specific Content Guidelines

### TikTok / Instagram Reels

- **Hook in first 1-3 seconds** — text overlay + strong visual
- Ideal length: 15-30s (watch-through rate drops sharply after 30s)
- Use trending audio (2x engagement lift vs. original audio)
- Captions: conversational, 3-5 sentences, include 3-5 relevant hashtags
- CTA: "Follow for more", "Comment your answer", "Link in bio"
- Content types: tutorials, trends, POV, behind-the-scenes

### LinkedIn

- Long-form posts: 1200-1500 characters for maximum reach
- Hook (first line must standalone as preview): bold claim or question
- Structure: Hook → Story/Data → Insight → CTA
- Posting time: Tuesday–Thursday, 8-10am or 12-2pm (business timezone)
- Images: native documents (carousels) outperform external links by 3x
- Avoid: external links in post body (kills reach); put in comments

### Email

- **Subject line** (A/B test mandatory): 40-60 characters, include power word
- **Preview text**: 85-100 characters, extends subject line promise
- **Single CTA** per email (multiple CTAs reduce click rate by 25%)
- Segmentation: separate sequences by funnel stage and behavior
- Cadence: max 3x/week; nurture sequences: 7-10 emails over 2-4 weeks
- Mobile-first layout: single column, 600px max width, 16px minimum font

### Blog / SEO

- Primary keyword in H1, URL slug, first 100 words, at least 2 H2s
- Target featured snippet with direct answer paragraph (40-60 words)
- Internal links: minimum 3 relevant internal links per post
- Word count: 1500-3000 words for competitive SERP positions
- Schema markup: Article or HowTo depending on content type
- Update cadence: refresh top posts every 12-18 months

---

## Editorial Calendar Management

### Calendar Structure

```
Month View:
- Content pillars assigned to week blocks
- Platform rotation (ensures channel balance)
- Campaign anchors (product launches, seasonal events, holidays)
- Buffer capacity (20% reserved for reactive/trending content)

Week View:
- Monday: Brief writer + assign assets
- Tuesday-Wednesday: Draft creation
- Thursday: Review + edits
- Friday: Schedule/publish
```

### Content Brief Template

```markdown
## Content Brief

**Title/Working Headline**: [H1 target]
**Content Type**: Blog / Email / Social / Ad
**Platform**: [channel]
**Pillar**: Educational / Inspirational / Promotional / Community
**Framework**: AIDA / PAS / BAB / 4Ps / FAB
**Target Audience**: [segment + awareness stage]
**Primary Goal**: [Awareness / Traffic / Lead / Conversion]
**Primary Keyword/Topic**: [keyword or topic]
**CTA**: [exact text + destination]
**Due Date**: YYYY-MM-DD
**Assigned To**: [human / AI / both]
**Word Count / Length**: [target]
**Assets Needed**: [images, video, graphics]
```

### Workflow States

1. `IDEATION` → Content brief drafted
2. `IN_PROGRESS` → Draft being written
3. `REVIEW` → Awaiting approval
4. `SCHEDULED` → Approved + in queue
5. `PUBLISHED` → Live
6. `MEASURING` → Post-publish tracking window (7-30 days)

---

## A/B Testing Workflow

### Test Design Protocol

```
1. HYPOTHESIS: "Changing X to Y will increase Z because [reason]"
2. VARIABLE: Isolate ONE variable per test (subject line, CTA, headline, image)
3. SAMPLE: Minimum 500 impressions per variant for statistical significance
4. DURATION: Run minimum 7 days to account for day-of-week variance
5. METRIC: Define primary metric BEFORE running (CTR, conversion rate, open rate)
```

### Test Backlog (Priority Order)

| Variable                          | Impact | Effort | Recommended Order |
| --------------------------------- | ------ | ------ | ----------------- |
| Email subject line                | High   | Low    | 1st               |
| Ad headline                       | High   | Low    | 2nd               |
| CTA text                          | High   | Low    | 3rd               |
| Landing page hero                 | High   | Medium | 4th               |
| Email send time                   | Medium | Low    | 5th               |
| Content format (video vs. static) | High   | High   | 6th               |

### Test Result Logging

```json
{
  "test_id": "email-subject-2026-03",
  "variable": "subject_line",
  "variant_a": "68% of marketers waste their budget",
  "variant_b": "Is your content strategy costing you money?",
  "metric": "open_rate",
  "result_a": 0.24,
  "result_b": 0.31,
  "winner": "b",
  "confidence": 0.95,
  "applied_to": "all future campaign emails",
  "date": "2026-03-01"
}
```

---

## Campaign Planning

### Campaign Structure

```
CAMPAIGN NAME: [descriptive + date range]
OBJECTIVE:     [SMART goal: Awareness / Traffic / Leads / Revenue]
AUDIENCE:      [Primary segment + targeting parameters]
BUDGET:        [total + channel allocation]
CHANNELS:      [ranked by expected ROI]
TIMELINE:      [start → warm-up → peak → wind-down → analysis]
KPIs:          [primary metric + 2-3 supporting metrics]
CONTENT MAP:   [content pieces by channel and funnel stage]
```

### Campaign Content Map (Example)

| Funnel Stage  | Channel | Content Type             | Framework   | Goal                    |
| ------------- | ------- | ------------------------ | ----------- | ----------------------- |
| Awareness     | TikTok  | 30s tutorial video       | AIDA        | Reach 50k               |
| Awareness     | Blog    | SEO article              | Educational | 1000 organic visits     |
| Consideration | Email   | Drip sequence (5 emails) | PAS         | 500 nurture enrollments |
| Conversion    | Email   | Offer email              | 4Ps         | 50 conversions          |
| Retention     | Email   | Onboarding sequence      | FAB         | 80% activation rate     |

---

## Content Performance KPIs

### Tier 1: Engagement (Content Quality Signal)

| KPI              | Definition                     | Target Benchmark       |
| ---------------- | ------------------------------ | ---------------------- |
| Engaged sessions | Sessions >10s with interaction | >60% of sessions       |
| Scroll depth     | % of page scrolled             | >50% to 75% mark       |
| Time on page     | Average seconds spent          | Varies by content type |
| Social shares    | Organic amplification          | >1% of views           |

### Tier 2: Conversion (Business Impact Signal)

| KPI                     | Definition                   | Target Benchmark |
| ----------------------- | ---------------------------- | ---------------- |
| CTR (organic)           | Click-through rate from SERP | >3%              |
| Email open rate         | Opens / delivered            | >25%             |
| Email CTR               | Clicks / opened              | >3%              |
| Content conversion rate | CTA completions / visitors   | >2%              |

### Tier 3: Retention & Loyalty

| KPI                    | Definition                  | Target Benchmark |
| ---------------------- | --------------------------- | ---------------- |
| Return visit rate      | % of visitors who return    | >20% in 30 days  |
| Email list growth rate | Net new subscribers / total | >5% monthly      |
| Unsubscribe rate       | Churned / sent              | <0.5%            |

### Tier 4: ROI

| KPI                                   | Definition                           | Target Benchmark   |
| ------------------------------------- | ------------------------------------ | ------------------ |
| Content ROI                           | (Revenue attributable - cost) / cost | >200%              |
| Cost per lead                         | Total content cost / leads           | Varies by industry |
| Customer acquisition cost via content | Total cost / customers               | Trending down      |

---

## Iron Laws

1. **ALWAYS match copywriting framework to audience awareness stage** — using AIDA for a product-aware audience wastes attention; using FAB for a cold audience loses them before they care.
2. **NEVER publish content without a measurable KPI defined first** — content without a success metric cannot be optimized and cannot prove ROI.
3. **ALWAYS A/B test one variable at a time** — testing multiple variables simultaneously makes it impossible to attribute performance changes to a single cause.
4. **NEVER use a one-size-fits-all content format across platforms** — each platform's algorithm rewards native content formats; cross-posting without adaptation produces 50-80% lower organic reach.
5. **ALWAYS maintain human editorial oversight for AI-drafted content** — AI handles research, structure, and drafts; human editors ensure brand voice, factual accuracy, and strategic alignment.

---

## Anti-Patterns

| Anti-Pattern                                     | Why It Fails                                                      | Correct Approach                                    |
| ------------------------------------------------ | ----------------------------------------------------------------- | --------------------------------------------------- |
| Using AIDA for product-aware audience            | Over-educates audience that already knows the problem             | Use 4Ps or FAB; lead with proof and offer           |
| Cross-posting identical content to all platforms | Platform algorithms penalize non-native formats                   | Adapt format, length, and tone per platform         |
| No A/B testing before scaling ad spend           | Intuition-based creative selection leaves 30-40% CTR on the table | Test headlines + CTAs first; scale winners          |
| Measuring pageviews as content success           | Pageviews measure traffic not content quality                     | Track engaged sessions and conversion rate          |
| Publishing without a content brief               | Inconsistent messaging, poor SEO, no clear CTA                    | Require brief for every piece before writing starts |
| Writing for search engines, not humans           | High bounce rate, low engagement, penalized by Google             | Write for humans first; optimize secondarily        |

---

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern → `.claude/context/memory/learnings.md`
- Issue found → `.claude/context/memory/issues.md`
- Decision made → `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
