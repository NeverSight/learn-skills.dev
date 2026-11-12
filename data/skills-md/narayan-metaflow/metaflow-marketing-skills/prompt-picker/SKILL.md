---
name: prompt-picker
description: "Build a prompt library that reveals how a brand shows up across the full buyer journey in AI search systems. The library is designed for actual LLM visibility tracking, not theoretical SEO keyword research."
---

## Why this skill exists

When buyers use ChatGPT, Gemini, Perplexity, or Claude to research purchases, the
prompts they type are not the same as Google search queries. They are longer, more
contextual, more conversational, and more likely to include role, budget, or use-case
constraints. A brand that monitors only "best [category]" prompts misses the majority
of decision-shaping moments. This skill produces a prompt set that covers discovery,
consideration, evaluation, and action — and separates branded from non-branded prompts
so metrics stay clean.

## Required inputs

Collect these from the user. If any are missing, infer what you can (see the inference
section below) and label those items as assumptions.

| Input                  | Why it matters                                                  |
|------------------------|-----------------------------------------------------------------|
| Brand name             | Anchors all branded and comparison prompts                      |
| Category               | Frames the non-branded discovery and consideration prompts      |
| Top competitors (3–6)  | Powers head-to-head comparison and alternative prompts           |
| Business model         | B2B / B2C / SaaS / ecommerce / services — changes prompt style  |
| ICPs / personas (2–4)  | Drives persona-variant prompts and contextual modifiers          |
| Core use cases / JTBD  | Ensures prompts match real buying reasons, not just features     |
| Differentiators        | Shapes prompts that test whether the brand's positioning lands   |
| Objections / fears     | Generates prompts buyers ask when they are hesitating            |

## Inference when inputs are incomplete

If the user gives only a brand name and category (or just a URL), you can still produce
a useful first draft. Do the following:

1. Search the web for the brand's website, product pages, pricing page, and any review
   sites or comparison articles.
2. From what you find, infer:
   - likely customer segments from pricing tiers and messaging
   - likely competitors from comparison content and review roundups
   - likely objections from FAQ pages, review complaints, and competitor positioning
   - likely use cases from feature pages and case studies
3. Generate the prompt library using these inferences.
4. Clearly label every inference as an assumption at the top of the output so the user
   can correct before finalising.

## Step-by-step method

### Step 1 — Collect and confirm the seed inputs

Present the input table to the user. If they have already supplied everything, confirm
your understanding in a short summary before generating. If gaps exist, state what you
will infer and from where.

### Step 2 — Map the prompt architecture

Organize prompts into five buckets. Within each bucket, use the subcategories below.
Not every subcategory applies to every brand — skip those that do not fit the business
model.

**Bucket 1 — Awareness (non-branded)**
The buyer does not yet know the brand. They are experiencing a problem, exploring a
need, or seeking an outcome. Subcategories:

- Problem-led: "How do I solve [pain]?"
- Objection-led: "Is [fear] a real risk with [category]?"
- Need-discovery: "What kind of tool helps with [job]?"
- Pain-point: "Why is [current approach] so hard?"
- Outcome-seeking: "How can I [desired result] faster?"

**Bucket 2 — Consideration (non-branded)**
The buyer knows the category exists and wants to narrow options. Subcategories:

- Best-of lists: "Best [category] for [persona/use case]"
- Category leaders: "Top [category] companies in [year]"
- Use-case recommendations: "What [category] works best for [specific job]?"
- Feature comparisons: "Which [category] has [key feature]?"
- Budget-aware: "[Category] for [small teams / startups / enterprise]"

**Bucket 3 — Brand evaluation (branded)**
The buyer has heard of the brand and is deciding whether to trust it. These prompts
should be tracked in a separate project so they do not inflate non-branded visibility
scores. Subcategories:

- Head-to-head: "[Brand] vs [Competitor]"
- Worth-it checks: "Is [Brand] worth it for [use case]?"
- Alternative hunts: "[Brand] alternatives for [persona/constraint]"
- Objection probes: "Does [Brand] really [claim/differentiator]?"
- Review / reputation: "[Brand] reviews [year]", "What do people say about [Brand]?"
- Pros/cons: "Pros and cons of [Brand] for [context]"

**Bucket 4 — Purchase / action (branded or non-branded)**
Only include when the business model has a clear purchase or conversion moment.

- Where-to-buy: "Where can I buy [Brand/product]?"
- How-to-start: "How do I get started with [Brand]?"
- Demo / trial: "Does [Brand] have a free trial?"
- Hiring: "Who should I hire for [service category]?"

**Bucket 5 — Persona / context variants**
Take the strongest prompts from Buckets 1–4 and create variants that shift the context.
Vary by:

- Role (CMO vs IC, developer vs product manager, founder vs procurement)
- Company size (startup, mid-market, enterprise)
- Budget sensitivity ("affordable," "cheap," "enterprise-grade")
- Technical maturity ("no-code," "for developers," "easy to set up")
- Industry vertical (healthcare, fintech, ecommerce, etc.)
- Geography or regulation (if relevant)

The point of persona variants is that AI systems return different recommendations
depending on context. A prompt about "best CRM for a 10-person startup" yields
different brands than "best CRM for enterprise sales teams." These variants expose
positioning gaps that a single generic prompt would hide.

### Step 3 — Write each prompt with metadata

For every prompt in the library, attach:

| Field                  | Value                                                           |
|------------------------|-----------------------------------------------------------------|
| Prompt text            | The exact natural-language prompt a user would type into an LLM |
| Funnel stage           | Awareness / Consideration / Evaluation / Purchase               |
| Intent type            | Problem exploration / Option discovery / Brand comparison / Action |
| Target persona         | Which ICP this prompt maps to (or "general")                    |
| JTBD                   | Which job-to-be-done this prompt relates to                     |
| Competitor included    | Yes / No (and which one if yes)                                 |
| Branded vs non-branded | Branded / Non-branded                                           |
| Why it matters         | 1–2 sentences: what positioning signal this prompt reveals       |
| Tracking project       | Main visibility / Brand evaluation / Persona tracking           |

### Step 4 — Build the master prompt table

Compile all prompts into a single table (or structured list) ordered by funnel stage,
then by subcategory within each stage. Target 20–40 prompts depending on the brand's
scope. The table should be copy-paste-ready for import into a tracking tool.

### Step 5 — Write the executive summary

Before the table, provide a short strategic overview:

- What buyer journey stages are well-covered
- Where the biggest visibility gaps are likely to be
- Where the brand is most vulnerable to competitors
- What kinds of prompts are missing and should be tested next

### Step 6 — Recommend a tracking setup

Split the prompt library into three tracking groups:

1. **Main visibility project** — all non-branded prompts. This is the core share-of-
   voice metric. Track whether the brand appears, where it ranks, and how it is
   described.
2. **Brand evaluation project** — all branded prompts (vs competitors, reviews,
   alternatives). Keep these separate so branded searches do not inflate the non-branded
   visibility score.
3. **Persona tracking project** — persona-variant prompts. Use these to detect
   positioning gaps by segment.

### Step 7 — Identify gaps and next prompts

End with a section listing:

- Prompt categories that were thin due to missing inputs
- Emerging prompt patterns worth testing (seasonal, event-driven, regulation-driven)
- Suggested next batch of prompts once first-round data comes back

## Output schema

Structure the final output in this order:

```
## Assumptions (if any inferences were made)
## Executive summary
## Prompt architecture (visual or tabular overview of buckets and subcategories)
## Master prompt table (the full library with all metadata columns)
## Recommended tracking setup
## Gaps and next prompts to test
```

## Quality checklist (apply before delivering)

- [ ] No two prompts test the same positioning signal
- [ ] At least 40% of prompts are non-branded awareness or consideration
- [ ] Persona variants exist for at least two different ICPs
- [ ] Branded comparison prompts are flagged for a separate tracking project
- [ ] Every prompt sounds like something a real person would type into ChatGPT
- [ ] Objection-led and fear-led prompts are included
- [ ] The library is not just synonyms of "best [category]"
- [ ] Purchase/action prompts are included only where the business model warrants them
- [ ] The executive summary states where the brand is most vulnerable
- [ ] The "why it matters" field is filled in for every prompt

## Worked example

See `references/worked-example.md` for a complete worked example using a fictional
B2B SaaS brand. Read that file if you want to see the full output format before
generating for a real brand.
