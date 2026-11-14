---
name: copywriting-frameworks
description: Framework-driven copywriting for ads, landing pages, emails, sales pages, and CTAs. Includes AIDA, PAS, BAB, 4Ps, StoryBrand, QUEST, FAB, and more. Use when writing conversion-focused copy, ad creative, headlines, email sequences, sales pages, or when the user mentions copywriting frameworks, persuasive writing, or direct response copy.
license: MIT
origin: custom
author: Rebecca Rae Barton
author_url: https://github.com/thatrebeccarae
metadata:
  version: 1.0.0
  category: content
  domain: copywriting
  updated: 2026-03-18
  tested: 2026-03-18
  tested_with: "Claude Code v2.1"
---

# Copywriting Frameworks

Framework-driven copy for ads, landing pages, emails, and sales pages.

## Install

```bash
git clone https://github.com/thatrebeccarae/claude-marketing.git && cp -r claude-marketing/skills/copywriting-frameworks ~/.claude/skills/
```

## Framework Selection Guide

| Situation | Best Framework | Why |
|-----------|---------------|-----|
| Short ad copy (social, search) | **PAS** or **AIDA** | Compact, hook-driven |
| Landing page hero | **4Ps** or **BAB** | Benefit-focused, drives action |
| Email sequence | **QUEST** or **PAS** | Builds momentum across messages |
| Sales page (long-form) | **StoryBrand** or **AIDA** | Narrative structure for sustained attention |
| Product description | **FAB** | Feature-to-benefit translation |
| Cold outreach | **BAB** or **PAS** | Quick empathy, clear value |
| CTA buttons and microcopy | **Action-Outcome** | Specific, benefit-driven action |

## Core Frameworks

### AIDA — Attention, Interest, Desire, Action

```
A — ATTENTION: Hook with a bold claim, question, or surprising stat
I — INTEREST: Build curiosity with specifics and proof
D — DESIRE: Make them want the outcome (paint the after-state)
A — ACTION: Clear, specific CTA
```

**Best for:** Sales pages, long-form ads, email sequences, landing pages

**Example (SaaS landing page):**
```
[A] Your email campaigns are leaving $80K on the table every year.
[I] We analyzed 500 DTC brands and found that 73% are missing at least 3 critical
    automated flows — each worth $2K-5K/month in recovered revenue.
[D] Imagine recapturing that revenue automatically, while you sleep. No extra
    headcount, no complex setup. Just the flows your customers expect, running
    24/7.
[A] Start your free 14-day trial — see your first recovered revenue in 48 hours.
```

### PAS — Problem, Agitate, Solution

```
P — PROBLEM: Name the pain your audience feels
A — AGITATE: Make the pain vivid and urgent (what happens if they do nothing?)
S — SOLUTION: Present your offer as the relief
```

**Best for:** Short ads, social posts, cold emails, landing page headlines

**Example (Google Ad):**
```
[P] Wasting ad spend on unqualified clicks?
[A] Every month, the average account wastes 26% of budget on irrelevant search
    terms — that is $2,600 per $10K spent, gone.
[S] Our Wasted Spend Audit finds and eliminates waste in 48 hours. Free for
    first-time clients.
```

### BAB — Before, After, Bridge

```
B — BEFORE: Describe their current painful state
A — AFTER: Paint the desirable future state
B — BRIDGE: Show how your product/service bridges the gap
```

**Best for:** Email sequences, testimonial-driven copy, case studies, cold outreach

**Example (cold email):**
```
[B] Right now, your team spends 10+ hours/week manually building reports
    from 4 different analytics platforms.
[A] What if those reports generated themselves every Monday morning —
    accurate, formatted, and ready for your exec meeting?
[B] That is exactly what [Product] does. Connect your data sources once,
    and never build another manual report.
```

### 4Ps — Promise, Picture, Proof, Push

```
P — PROMISE: Make a bold, specific promise
P — PICTURE: Help them visualize the result
P — PROOF: Back it up with evidence
P — PUSH: Drive to action with urgency
```

**Best for:** Landing pages, webinar promotion, launch copy

### QUEST — Qualify, Understand, Educate, Stimulate, Transition

```
Q — QUALIFY: Filter for the right audience ("If you are a...")
U — UNDERSTAND: Show you get their situation
E — EDUCATE: Teach something valuable
S — STIMULATE: Create desire through the education
T — TRANSITION: Bridge to your offer naturally
```

**Best for:** Email sequences, content marketing, webinar scripts

### FAB — Features, Advantages, Benefits

```
F — FEATURE: What the product has/does
A — ADVANTAGE: Why that feature matters (vs alternatives)
B — BENEFIT: What it means for the customer (outcome/feeling)
```

**Best for:** Product descriptions, feature pages, comparison copy

**Example:**
```
[F] Automated email flows triggered by customer behavior
[A] Unlike batch campaigns, these reach customers at the exact right moment
[B] You recover abandoned carts and win back churned customers without lifting
    a finger — adding $5-15K/month in passive revenue
```

### StoryBrand (Donald Miller)

```
1. CHARACTER: The customer is the hero (not your brand)
2. PROBLEM: External (what they face), internal (how it feels), philosophical (why it is wrong)
3. GUIDE: Your brand as the wise guide (empathy + authority)
4. PLAN: Simple 3-step plan to follow
5. CALL TO ACTION: Direct ("Buy Now") and transitional ("Download Guide")
6. SUCCESS: What winning looks like
7. FAILURE: What happens if they do not act
```

**Best for:** Brand messaging, website copy, sales pages, brand narratives

## Headline Formulas

| Formula | Template | Example |
|---------|----------|---------|
| How-to | How to [Achieve X] Without [Pain Y] | How to 3x Email Revenue Without Hiring |
| Number | [N] Ways to [Achieve X] in [Timeframe] | 7 Ways to Cut Ad Waste in 30 Days |
| Question | Are You Making These [N] [Mistake] Mistakes? | Are You Making These 5 Checkout Mistakes? |
| Negative | Stop [Bad Thing] — Here Is What to Do Instead | Stop Sending Batch Emails — Here Is What to Do Instead |
| Social proof | How [Company] [Achieved Result] | How Glossier Grew 600% With Email Alone |
| Curiosity gap | The [Adjective] [Thing] Most [People] Overlook | The Simple Metric Most Marketers Overlook |
| Direct benefit | Get [Benefit] in [Timeframe] | Get Your First 1,000 Subscribers in 30 Days |
| Comparison | [X] vs [Y]: Which [Outcome]? | Klaviyo vs Mailchimp: Which Drives More Revenue? |

## CTA Best Practices

### CTA Text Formulas

| Pattern | Example | When |
|---------|---------|------|
| Action + Benefit | Start Saving Today | Primary conversion |
| Action + Timeframe | Get Results in 48 Hours | Urgency-driven |
| Action + Risk Reversal | Try Free for 14 Days | Reducing anxiety |
| First Person | Start My Free Trial | Ownership language |
| Specificity | See My Wasted Spend Report | Personalized |

### CTA Anti-Patterns (Never Use)

- "Submit" — most hated CTA word
- "Click Here" — vague, inaccessible
- "Learn More" as primary CTA — too passive (OK as secondary)
- "Sign Up" without benefit context
- "Buy Now" without trust signals nearby

## Integration with Other Skills

- **cro-auditor** — Apply frameworks to pages flagged by CRO audit
- **seo-content-writer** — SEO-optimized copy using these frameworks
- **content-creator** — Brand voice consistency when writing framework-driven copy
- **email-composer** — Email-specific applications of PAS, BAB, QUEST
