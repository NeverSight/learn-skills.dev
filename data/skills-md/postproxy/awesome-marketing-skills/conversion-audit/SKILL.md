---
name: conversion-audit
description: When the user wants to optimize a page for conversions, audit a landing page, or improve signup/purchase rates. Also use when the user mentions "CRO", "conversion rate", "optimize this page", "landing page review", "page audit", "why isn't this converting", or "improve conversions."
version: 1.0.0
---

# Conversion Audit

Analyze any marketing page and provide prioritized, actionable recommendations to improve conversion rates.

## Before You Start

**Check for product marketing context first:**
If `.claude/product-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered.

## Phase 1: Information Gathering

Collect context by asking the user focused questions in batches of 2-3.

### Required Context

1. **Share the page** — Ask: "Share the URL or paste the page content you want audited."

2. **Page type** — Use `AskUserQuestion` with options:
   - Homepage
   - Landing page (paid traffic)
   - Landing page (organic traffic)
   - Pricing page
   - Feature / product page
   - Signup / registration page
   - Blog post with conversion goal

3. **Primary conversion goal** — Use `AskUserQuestion` with options:
   - Sign up (free trial / freemium)
   - Request a demo / talk to sales
   - Purchase / checkout
   - Subscribe (newsletter / waitlist)
   - Download (lead magnet / resource)
   - Other

4. **Traffic sources** — Use `AskUserQuestion` with multiSelect:
   - Organic search (SEO)
   - Paid ads (Google, Meta, etc.)
   - Social media
   - Email campaigns
   - Direct / referral
   - Not sure

5. **Current performance** — Ask: "What's your current conversion rate? (Even a rough estimate helps.) How much traffic does the page get monthly?"

6. **Known issues** — Ask: "Have you noticed any specific problems? (e.g., high bounce rate, users dropping off at a specific point, complaints, heatmap data, session recordings)"

7. **What you've tried** — Ask: "Have you made any changes or run tests already? What happened?"

8. **Audience context** — Ask: "Who visits this page? How aware are they of their problem and your solution when they land here?"

## Phase 2: CRO Analysis

Analyze the page across these 7 dimensions, in order of impact:

### 1. Value Proposition Clarity (Highest Impact)
- Can a visitor understand what this is and why they should care in 5 seconds?
- Is the benefit clear, specific, and differentiated?
- Written in customer language, not company jargon?

### 2. Headline Effectiveness
- Communicates core value proposition?
- Specific enough to be meaningful?
- Matches the traffic source's messaging?

### 3. CTA Placement, Copy, and Hierarchy
- One clear primary action?
- Visible without scrolling?
- Button copy communicates value, not just action? (e.g., "Start Free Trial" not "Submit")
- Repeated at key decision points?

### 4. Visual Hierarchy & Scannability
- Can someone scanning get the main message?
- Most important elements visually prominent?
- Enough white space?
- Images support (not distract from) the message?

### 5. Trust & Social Proof
- Customer logos, testimonials, case studies, review scores?
- Placed near CTAs and after benefit claims?
- Specific and attributed (not generic)?

### 6. Objection Handling
- Price/value concerns addressed?
- "Will this work for me?" answered?
- Implementation difficulty reduced?
- Risk reversal (guarantees, free trial)?

### 7. Friction Points
- Too many form fields?
- Unclear next steps?
- Mobile experience issues?
- Slow load time?

## Phase 3: Deliverables

Generate and save:

1. **`conversion-audit.md`** — Structured audit report with:
   - **Quick Wins** — Easy changes with likely immediate impact
   - **High-Impact Changes** — Bigger effort, significant improvement
   - **Test Ideas** — Hypotheses worth A/B testing
   - **Copy Alternatives** — 2-3 alternatives for key elements (headlines, CTAs) with rationale

Present a summary and suggest next steps (e.g., "Use /split-test to test the top recommendation" or "Use /marketing-copy to rewrite the page copy").

## Guidelines

- Be specific and actionable — "improve your headline" is not useful, "change headline from X to Y because Z" is
- Prioritize ruthlessly — not everything matters equally
- Back recommendations with reasoning (psychology, data, best practices)
- Don't recommend changes for the sake of change — if something works, say so
- Consider the full funnel, not just the page in isolation

## User Request

$ARGUMENTS
