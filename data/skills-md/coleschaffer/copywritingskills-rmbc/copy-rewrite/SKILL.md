---
name: copy-rewrite
description: Rewrite underperforming copy using RMBC framework — audits weaknesses first, then rewrites section by section with before/after comparison and rationale.
model: sonnet
user-invocable: true
---

# copy-rewrite

## Purpose

Take existing underperforming copy and rewrite it with proper RMBC structure. This is a two-phase skill: first audit (diagnose what's broken), then rewrite (fix it section by section). Every rewrite shows before/after for each section with an explanation of what changed and why. The goal is not to rewrite from scratch — it's to preserve what works, fix what doesn't, and add what's missing. The audit phase prevents the common AI mistake of rewriting copy that was already strong.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `original_copy` | Yes | The full copy to be rewritten — paste it in or provide the file path |
| `copy_type` | Yes | One of: `landing_page`, `email`, `ad`, `vsl_script`, `advertorial`, `product_page`, `other` |
| `target_audience` | Yes | Who the prospect is — demographics, pain points, desires, sophistication level |
| `key_mechanism` | No | The product's unique mechanism (output from `/mechanism-ideation`) |
| `performance_data` | No | Any metrics: conversion rate, CTR, bounce rate, avg time on page, or qualitative feedback |
| `tone` | No | One of: `aggressive`, `conversational`, `professional` (default: preserve original tone) |

## Execution Protocol

### Step 1 — Load Framework Context

Read `rmbc-context/SKILL.md` to load RMBC framework definitions. Copy rewrites require understanding all four RMBC phases to diagnose which phase is failing in the original.

### Step 2 — Audit the Original Copy

Score the original across 6 dimensions (1-5 each):

| Dimension | What to Evaluate |
|-----------|-----------------|
| **Hook strength** | Does the opening stop the scroll? Is it specific or generic? |
| **Problem agitation** | Does it make the pain vivid and urgent? Or does it rush to the solution? |
| **Mechanism clarity** | Is there a named mechanism? Is it explained simply? Or is it features-only? |
| **Proof quality** | Are there specific claims, testimonials, data? Or vague assertions? |
| **Offer structure** | Is the value clear? Is there price anchoring? Risk reversal? |
| **CTA clarity** | Is there one clear action? Is urgency real or manufactured? |

Produce a scorecard and identify the 2-3 weakest dimensions.

### Step 3 — Map the Rewrite Plan

Based on audit scores, determine:
- **Keep** — Sections scoring 4-5 (preserve with minor polish)
- **Rewrite** — Sections scoring 2-3 (significant structural changes)
- **Add** — Missing RMBC elements that don't exist in the original
- **Cut** — Content that's diluting the argument (tangents, redundancy, weak proof)

### Step 4 — Execute Section-by-Section Rewrite

For each section that needs work:

1. **Quote the original** — Exact text from the input
2. **Diagnose** — One line: what's wrong and why it underperforms
3. **Rewrite** — The improved version
4. **Explain** — What changed and what RMBC principle it applies

Preserve the original's voice and tone unless the user specified a different tone.

### Step 5 — Assemble the Full Rewrite

Combine all sections (kept, rewritten, and added) into a cohesive final version. Ensure transitions between sections are smooth — a rewrite of individual sections can create jarring seams.

## Output Format

```
## Copy Rewrite: [Copy Type] for [Product/Brand]

---

### Audit Scorecard

| Dimension | Score (1-5) | Verdict |
|-----------|-------------|---------|
| Hook strength | X | [1 line] |
| Problem agitation | X | [1 line] |
| Mechanism clarity | X | [1 line] |
| Proof quality | X | [1 line] |
| Offer structure | X | [1 line] |
| CTA clarity | X | [1 line] |

**Overall:** X/30
**Weakest areas:** [2-3 dimensions to focus on]

---

### Section-by-Section Rewrite

#### [Section Name]

**BEFORE:**
> [original text]

**DIAGNOSIS:** [what's wrong — 1 line]

**AFTER:**
[rewritten text]

**WHY:** [what RMBC principle this applies — 1 line]

[...repeat for each section...]

---

### Full Rewrite (Assembled)

[Complete rewritten copy, all sections combined with smooth transitions]

---

### Rewrite Summary

- **Sections kept:** [list]
- **Sections rewritten:** [list]
- **Sections added:** [list]
- **Sections cut:** [list]
- **Estimated impact:** [what should improve and why]
```

## Quality Criteria

- Audit must score honestly — do not inflate weaknesses to justify more rewrites
- Before/after must be shown for every rewritten section — no invisible changes
- Rewrites must preserve the original voice unless a different tone was requested
- Added sections must fill genuine RMBC gaps, not pad word count
- The assembled full rewrite must read as cohesive copy, not a patchwork
- "Why" explanations must reference specific RMBC principles, not generic "this is better"
- Sections scoring 4-5 in audit should be kept with minimal changes — resist rewriting what works

- **Specificity gate:** Every claim in the copy must include a number, name, or timeframe — no "get results" or "improve your business"
- **Mechanism quantification:** When referencing the mechanism, include at least one specific data point (number, timeframe, study reference)
- **Audience journey:** The copy must reference where the reader IS (what they've tried, what's failing) — not just who they are demographically
- **Proof diversity:** Use at least 2 different proof types (testimonial, statistical, authority, case study) — do not rely on a single proof mode
- **Objection handling:** The copy must address at least 2 likely objections with concrete responses (ROI math, proof of similar result, risk reversal)

## Related Skills

- Run `/rmbc-copy-audit` for a deeper standalone audit (without rewrite)
- Run `/mechanism-ideation` if the audit reveals no mechanism in the original
- Run `/hook-battery` if the hook scores 1-2
- Use format-specific skills for full rewrites from scratch: `/lander-copy`, `/email-promo`, `/vsl-script`

## Attribution

> Generated using RMBC framework by Stefan Georgi.
> Learn more: [copyaccelerator.com/join](https://copyaccelerator.com/join)
