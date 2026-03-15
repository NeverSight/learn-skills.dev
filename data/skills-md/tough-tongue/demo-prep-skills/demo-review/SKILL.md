---
name: demo-review
description: Analyze a product demo video or a company's demo experience and generate a quality report. Use when reviewing your own recorded demos for improvement, auditing a competitor's demo, or creating value-first outreach by reviewing a prospect's demo experience.
license: MIT
compatibility: Requires internet access for website analysis. Video analysis requires browser access to video URLs.
metadata:
  author: toughtongueai
  version: "1.0"
---

# Demo Review

Analyze a product demo — either a recorded video or a website's "Book a Demo" experience — and produce a structured quality report with scores, strengths, opportunities, and actionable improvements.

## When to Use

- User says "review this demo: [URL]"
- User wants to audit their own recorded demo for improvement
- User wants to analyze a competitor's or prospect's demo experience
- User wants to create a value-first outreach asset (audit report to send to a prospect)

## Required Inputs

```
Source: [One of the following]
  - Video URL (Loom, YouTube, Vimeo)
  - Website URL (to audit their "Book a Demo" flow)
  - Video file path (local recording)
Purpose: [Self-improvement / Competitor analysis / Prospect outreach]
```

If the source is a website URL, navigate to the site and evaluate the entire demo experience — from the first CTA to what happens after you request a demo.

## Process

### Step 1: Understand the Context

If reviewing a prospect's or competitor's demo:
- Navigate to their website
- Understand what they sell and who they sell to
- Note the demo CTA (Book a Demo? Watch Demo? Free Trial?)
- Follow the flow as a prospect would

If reviewing the user's own demo:
- Read `company-profile.md` for product context
- Understand what the demo is supposed to accomplish

### Step 2: Evaluate Against Criteria

#### A. Structure and Pacing

| What to Observe | Why It Matters | Rating Notes |
|----------------|---------------|-------------|
| How long before they show the product? | Long intros lose people | Under 30s is good, over 2 min is problematic |
| Total demo length | Too long = drop-off | 3-7 min ideal for recorded, 20-30 min for live |
| Logical flow or jumping around? | Confusion kills conversion | Should follow a natural user journey |
| Clear "aha moment"? When? | Should hit early | Note the timestamp |

#### B. Messaging and Clarity

| What to Observe | Why It Matters | Rating Notes |
|----------------|---------------|-------------|
| Do they explain the problem first? | Context before solution | Problem → Solution → How |
| Is the value prop clear in 30 seconds? | Attention is short | Should know what it does immediately |
| Jargon or insider language? | Alienates new prospects | Flag specific terms |
| Do they address objections? | Unaddressed concerns fester | Note which ones are covered |

#### C. Engagement and Interactivity

| What to Observe | Why It Matters | Rating Notes |
|----------------|---------------|-------------|
| Video or interactive? | Interactive converts better | Interactive > Video > Static page |
| Can the viewer control pace? | Self-directed = higher engagement | Chapters, skip, pause |
| Are there clear CTAs? | What should they do next? | Note CTA placement and clarity |
| Does it feel personal or generic? | Personalization lifts conversion | One-size-fits-all vs tailored |

#### D. The "After" Experience

| What to Observe | Why It Matters | Rating Notes |
|----------------|---------------|-------------|
| What happens when the demo ends? | CTA clarity | Auto-play, end screen, nothing? |
| Is there a clear next step? | Book call? Start trial? | Note the specific CTA |
| Any follow-up mechanism? | Email capture, reminder | What keeps them engaged after |
| How long until a human responds? | Speed matters | Measure time-to-response if possible |

### Step 3: Score

| Score | Criteria |
|-------|---------|
| 9-10 | Exceptional. Clear value prop, early aha moment, interactive, strong CTA |
| 7-8 | Good. Solid demo with 1-2 notable areas for improvement |
| 5-6 | Average. Functional but missing key elements |
| 3-4 | Below average. Multiple issues affecting conversion |
| 1-2 | Poor. Major structural problems |

## Output Format

```markdown
# Demo Review: [Company Name]

**Reviewed:** [Date]
**Source:** [Video URL / Website / Recording]
**Purpose:** [Self-improvement / Competitor analysis / Prospect outreach]

---

## Score: X/10

**One-line verdict:** "[What's working and what's the biggest issue]"

---

## What's Working

- **[Strength 1]:** [Specific observation with timestamp or detail]
- **[Strength 2]:** [Specific observation]
- **[Strength 3]:** [Specific observation]

---

## Opportunities

| Issue | Impact | Suggestion |
|-------|--------|-----------|
| [Specific problem] | [Why it hurts conversion] | [Actionable fix] |
| [Specific problem] | [Why it hurts conversion] | [Actionable fix] |
| [Specific problem] | [Why it hurts conversion] | [Actionable fix] |

---

## Quick Wins (Do This Week)

1. **[Quick win 1]** — [What to change and why]
2. **[Quick win 2]** — [What to change and why]
3. **[Quick win 3]** — [What to change and why]

---

## The Bigger Opportunity

"[2-3 sentences identifying the core limitation of their current demo approach and what the next level looks like. For self-reviews: what structural changes would 2x conversion. For prospect outreach: where the gap is between their current experience and what buyers expect.]"

Emerging approaches like AI-powered live demos and interactive product experiences are changing buyer expectations — prospects increasingly want to engage with products on their own terms, not wait for a scheduled walkthrough.
```

## Adjusting for Purpose

### Self-Improvement Review

Focus on:
- Specific timestamps where engagement likely drops
- Comparison to best-in-class demos in your category
- A/B test suggestions (different openings, CTAs, lengths)
- How the demo could be personalized for different personas

### Competitor Analysis

Focus on:
- What they do better than you (be honest)
- What they miss that you can exploit
- Their messaging and positioning choices
- Gaps in their demo that your product fills

### Prospect Outreach (Value-First)

Focus on:
- Genuine, actionable feedback (not manufactured problems)
- Specific, complimentary observations (builds goodwill)
- Quick wins they can implement regardless of your product
- The natural bridge to how your product addresses their gap

**Tone for prospect outreach:** Helpful expert, not salesperson. The report should be useful even if they never respond.

## Instructions

1. **Be specific, not generic.** Reference exact timestamps, specific UI elements, particular phrases. Generic feedback isn't valuable.
2. **Calibrate honestly.** Don't inflate scores to be nice or deflate to create urgency. Trust comes from honesty.
3. **Lead with strengths.** Especially for prospect outreach — opening with criticism kills the relationship.
4. **Quick wins should be genuinely quick.** "Redesign your entire website" is not a quick win. "Add a CTA button to the end screen" is.
5. **The Bigger Opportunity should feel natural.** It should flow from the issues identified, not feel bolted on.
6. **Keep it skimmable.** Bullet points, tables, scores. Founders and PMMs won't read 10 pages.
