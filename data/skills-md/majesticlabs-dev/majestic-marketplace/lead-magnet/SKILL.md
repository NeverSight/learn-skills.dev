---
name: lead-magnet
description: Create high-converting lead magnets that generate email subscribers. Supports checklists, templates, swipe files, mini-courses, and guides with landing page copy.
triggers:
  - lead magnet
  - create lead magnet
  - freebie
  - opt-in
  - email opt-in
  - gated content
allowed-tools: Read Write Edit Grep Glob WebSearch AskUserQuestion
disable-model-invocation: true
---

# Lead Magnet Builder

Create lead magnets that people actually want—and that convert visitors into subscribers.

## The Three Principles

### 1. The Specificity Principle

**Narrow beats broad. Every time.**

"5-Step Framework to Land Your First 10 Clients in 30 Days (Even If You Hate Networking)" converts dramatically better than "Marketing Guide for Freelancers."

When generating concepts, push toward:
- Specific outcome (not "grow your business" but "add $10k MRR")
- Specific timeframe (not "eventually" but "in 30 days")
- Specific audience (not "entrepreneurs" but "B2B SaaS founders")
- Specific method (not "marketing tips" but "The LinkedIn DM Framework")

### 2. The Bridge Principle

**The lead magnet must logically connect to the paid offer.**

If someone downloads a lead magnet about Instagram growth and you sell SEO services, there's no bridge.

The best lead magnets are "Step 1" of what you sell:
- Course on copywriting → Lead magnet: "The Headline Formula" (first skill)
- Agency doing SEO audits → Lead magnet: Free mini-audit (demonstrates full audit)
- Coach on productivity → Lead magnet: "Morning Routine Builder" (taste of methodology)

The bridge should be obvious: "If you liked this free thing, the paid thing is more/deeper/complete."

### 3. The Quick Win Principle

**Solve one specific problem completely.**

The best lead magnets deliver immediate value:
- A checklist they complete in 10 minutes that reveals gaps
- A template they customize in an hour for their business
- An assessment that gives them a score and action items immediately
- A calculator that shows their specific numbers right now

Quick wins create reciprocity.

## Conversation Starter

Use `AskUserQuestion` to gather context:

"I'll help you create a lead magnet that converts.

**Tell me:**

1. **Business/Niche**: What do you sell or teach?
2. **Target audience**: Who are you trying to attract?
3. **Biggest pain point**: What's their #1 struggle?
4. **Your expertise**: What can you help with quickly?
5. **Lead magnet type** (pick one):
   - **Checklist** - Step-by-step verification list
   - **Template** - Fill-in-the-blank document
   - **Swipe file** - Collection of examples to copy
   - **Mini-guide** - Short how-to (5-10 pages)
   - **Cheat sheet** - Quick reference one-pager
   - **Toolkit** - Bundle of resources
   - **Quiz** - Interactive assessment
   - **Calculator** - Solve a math problem for them

I'll create the content plus landing page copy."

## Lead Magnet Types

For detailed templates and structures, see [references/templates.md](references/templates.md).

| Type | Best For | Title Formula Example |
|------|----------|----------------------|
| **Checklist** | Process outcomes, compliance | "The Complete [Outcome] Checklist" |
| **Template** | Documents, emails, scripts | "Copy-Paste [Document] Template" |
| **Swipe File** | Examples to model, inspiration | "[Number] [Type] Swipe File" |
| **Mini-Guide** | Teaching a skill, thought leadership | "How to [Outcome] (Even If [Objection])" |
| **Cheat Sheet** | Quick reference, reminders | "[Topic] Cheat Sheet (One-Pager)" |
| **Toolkit** | Comprehensive value, multiple use cases | "The Ultimate [Topic] Toolkit" |

### 4. Mini-Guide

**Best for:** Teaching a skill, explaining a process, thought leadership

**Structure:**
```markdown
# [Outcome]: A Quick Guide for [Audience]

---

## Introduction

[2-3 paragraphs on why this matters and what they'll learn]

**By the end, you'll know:**
- [Outcome 1]
- [Outcome 2]
- [Outcome 3]

---

## Chapter 1: [Foundation Topic]

[3-5 paragraphs teaching the concept]

### Key Takeaway
> [Quotable summary]

---

## Chapter 2: [Core Concept]

[Teaching content with examples]

### Action Step
[Specific thing to do]

---

## Chapter 3: [Application]

[How to apply what they've learned]

### Common Mistakes
1. [Mistake + correction]
2. [Mistake + correction]

---

## Quick Reference

| Situation | Do This |
|-----------|---------|
| [Scenario] | [Action] |
| [Scenario] | [Action] |

---

## What's Next?

You now know [summary].

The next step is [action that leads to your offer].

[CTA to product/service]

---

## About [Author]

[2-3 sentences establishing credibility + link to more resources]
```

**Title formulas:**
- "The [Audience]'s Guide to [Outcome]"
- "[Outcome] in [Timeframe]: A Quick Guide"
- "How to [Outcome] (Even If [Objection])"

### 5. Cheat Sheet

**Best for:** Reference material, quick lookups, reminders

**Structure:**
```markdown
# [Topic] Cheat Sheet

**Save this:** Reference when you need to [action]

---

## [Category 1]

| [Column A] | [Column B] | [Column C] |
|------------|------------|------------|
| [Item] | [Detail] | [Tip] |
| [Item] | [Detail] | [Tip] |

---

## [Category 2]

**Quick formulas:**
- [Formula 1]: [Explanation]
- [Formula 2]: [Explanation]

---

## [Category 3]

**Do:**
✅ [Best practice]
✅ [Best practice]

**Don't:**
❌ [Mistake]
❌ [Mistake]

---

## Quick Wins

| Need This | Do This |
|-----------|---------|
| [Goal] | [Shortcut] |
| [Goal] | [Shortcut] |

---

## Remember

> [The one key principle to never forget]
```

**Title formulas:**
- "[Topic] Cheat Sheet (One-Pager)"
- "The [Outcome] Quick Reference"
- "[Audience]'s [Topic] Cheat Sheet"

### 6. Toolkit/Bundle

**Best for:** Comprehensive value, multiple use cases

**Structure:**
```markdown
# The [Outcome] Toolkit

**Inside this toolkit:**
1. [Resource 1] - [Brief description]
2. [Resource 2] - [Brief description]
3. [Resource 3] - [Brief description]
(3-7 resources ideal)

---

## How to Use This Toolkit

**Start here:** [First resource]
**Then:** [Second resource]
**When you need:** [Third resource for specific situation]

---

## Resource 1: [Name]

[Full resource content]

---

## Resource 2: [Name]

[Full resource content]

---

(Continue for all resources)

---

## Toolkit Roadmap

| Stage | Use This | Goal |
|-------|----------|------|
| Getting started | [Resource] | [Outcome] |
| Scaling up | [Resource] | [Outcome] |
| Optimizing | [Resource] | [Outcome] |

---

## What's Next?

You have everything you need to [outcome].

When you're ready to [next level], check out [your offer].
```

**Title formulas:**
- "The Ultimate [Topic] Toolkit"
- "[Outcome] Starter Kit"
- "The [Audience] Toolkit"

## Hook Generators

Every lead magnet needs a hook — the reason someone gives their email.

| Hook Type | Formula | Example |
|-----------|---------|---------|
| **Shortcut** | "Get [outcome] without [pain]" | "The 5-Minute Routine That Replaced My 2-Hour Gym Sessions" |
| **Secret** | "The [hidden thing] that [result]" | "The Pricing Secret That Doubled My Agency's Revenue" |
| **System** | "The [named method] for [outcome]" | "The PASTOR Framework: Write Sales Pages in 30 Minutes" |
| **Specific Number** | "[Number] [things] to [outcome]" | "7 Subject Lines That Get 40%+ Open Rates" |
| **Assessment** | "Discover your [type/score/level]" | "What's Your Entrepreneur Personality Type?" |
| **Transformation** | "From [current state] to [desired]" | "From $5k/month to Consistent $20k Months" |
| **Case Study** | "How [person] achieved [result]" | "How Sarah Built a 10K Email List in 90 Days" |

## Landing Page Copy

For every lead magnet, generate landing page copy with:

- **3 headline options** (benefit-focused, problem/solution, curiosity)
- **Subheadline** expanding on headline with specificity
- **3-4 benefit bullets** (specific outcomes, not features)
- **Social proof** (testimonial or download count)
- **CTA button** (action verb + outcome: "Get the Checklist", "Send Me the Guide")
- **Privacy line** ("No spam. Unsubscribe anytime.")
- **Objection handling** (1-2 common objections with responses)

## Output Format

```markdown
# LEAD MAGNET: [Title]

## Overview
- **Type:** [Checklist/Template/etc.]
- **Target audience:** [Who it's for]
- **Problem solved:** [Core pain point]
- **Time to consume:** [X minutes]

---

## Lead Magnet Content

[Full content using appropriate structure]

---

## Landing Page Copy

[Headline options, bullets, CTA, etc.]

---

## Delivery Email

**Subject:** [Your [Lead Magnet Name] is ready]

[Email body with download link + next step]

---

## Follow-Up Sequence Preview

**Email 1 (Day 2):** [Topic - drive consumption]
**Email 2 (Day 4):** [Topic - add value]
**Email 3 (Day 7):** [Topic - soft pitch]

---

## Promotion Ideas

- [ ] Blog post leading to opt-in
- [ ] Social post series
- [ ] Partner/affiliate shares
- [ ] Exit-intent popup
- [ ] Content upgrade in related posts
```

## Quality Checklist

Before finalizing:

- [ ] Solves ONE specific problem (not everything)
- [ ] Delivers quick win (<10 min to value)
- [ ] Attracts ideal customer (not everyone)
- [ ] Has high perceived value (worth email)
- [ ] Title creates curiosity/desire
- [ ] Landing page copy is benefit-focused
- [ ] Clear path to your paid offer
- [ ] Mobile-friendly format

## Integration

Works with:
- `irresistible-offer` - Position the lead magnet
- `landing-page-builder` - Create full landing page
- `email-nurture` - Follow-up sequence after download
- `content-atomizer` - Promote across platforms
