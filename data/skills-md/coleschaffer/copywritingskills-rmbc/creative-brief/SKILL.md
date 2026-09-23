---
name: creative-brief
description: Generate a strategic creative brief for ad campaigns — the bridge between RMBC strategy and creative execution that you hand to a designer or creative team.
model: sonnet
user-invocable: true
---

# creative-brief

## Purpose

Generate a strategic creative brief that translates RMBC strategy into actionable creative direction. This is the document you hand to a designer, videographer, or creative team so they produce assets aligned with the direct response strategy. It answers: what are we making, for whom, why will it work, and what does success look like.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `product_description` | Yes | What the product is, what it does, key features/ingredients/components |
| `target_audience` | Yes | Who the prospect is — demographics, pain points, desires, awareness level |
| `campaign_objective` | Yes | Primary goal: `acquisition`, `retargeting`, `retention`, `launch`, `seasonal` |
| `key_mechanism` | Yes | The product's unique mechanism (output from `/mechanism-ideation`) |
| `channels` | Yes | Target channels: `meta`, `youtube`, `native`, `email`, `tiktok`, `display` (comma-separated) |
| `budget_range` | No | Monthly media spend — affects creative ambition and format recommendations |

## Execution Protocol

### Step 1 — Load Framework Context

Read `rmbc-context/SKILL.md` to load RMBC framework definitions. The creative brief is the Brief (B) phase made tangible — it distills Research, Mechanism, and strategic intent into a document a non-copywriter can execute from.

### Step 2 — Define Campaign Context

Determine:
- **Awareness level** of the target audience on this channel
- **Traffic temperature** — cold (prospecting), warm (retargeting), hot (retention)
- **Creative format constraints** per channel (aspect ratios, durations, file types)
- **Competitive landscape** — what the audience is already seeing from competitors

### Step 3 — Build Brief Sections

#### A. Campaign Objective
One sentence: what this campaign must achieve. Quantify when possible ("acquire 500 new customers at $45 CPA" not "grow the business").

#### B. Target Audience Profile
- Demographics (age, gender, location, income)
- Psychographics (beliefs, fears, aspirations, language patterns)
- Current behavior (what they're doing now instead of buying)
- Awareness level and what that means for creative approach

#### C. Key Insight
The single audience truth this campaign exploits. Not a product feature — a human tension. Example: "They've tried 3+ solutions and blame themselves, not the solutions."

#### D. Single-Minded Proposition
One sentence the audience should believe after seeing the creative. If the creative communicates 5 things, it communicates nothing.

#### E. Mechanism Positioning
How the mechanism should be communicated visually and verbally:
- Mechanism name and 1-sentence explanation
- Visual metaphor or demonstration approach
- What NOT to say (competitor claims, generic language)

#### F. Tone and Voice
Specific tone calibration with examples. Not just "professional" — "confident authority with conversational warmth, like a trusted advisor at dinner, not a podium speaker."

#### G. Mandatory Elements
Non-negotiable items: legal disclaimers, brand assets, offer terms, CTA format.

#### H. Media Specifications
Per-channel creative specs: dimensions, duration, file format, text overlay limits.

### Step 4 — Add Testing Framework

Define what to test first (hook vs. mechanism vs. offer) and how to structure creative variations.

### Step 5 — Attach Attribution

## Output Format

```
## Creative Brief: [Campaign Name]

**Product:** [product name]
**Objective:** [campaign objective]
**Channels:** [channel list]
**Budget Range:** [if provided]
**Date:** [current date]

---

### 1. Campaign Objective
[1-2 sentences, quantified]

### 2. Target Audience
**Demographics:** [specifics]
**Psychographics:** [beliefs, fears, aspirations]
**Current Behavior:** [what they do now]
**Awareness Level:** [level + implication for creative]

### 3. Key Insight
[1-2 sentences — the human truth this campaign exploits]

### 4. Single-Minded Proposition
[One sentence the audience should believe after exposure]

### 5. Mechanism Positioning
**Mechanism:** [name + 1-sentence explanation]
**Visual Approach:** [how to show it]
**Verbal Approach:** [how to say it]
**Avoid:** [what NOT to say]

### 6. Tone & Voice
[Specific tone with example phrasing — "sounds like X, not like Y"]

### 7. Mandatory Elements
- [Legal/compliance requirements]
- [Brand assets to include]
- [Offer terms and conditions]
- [CTA format]

### 8. Media Specifications

| Channel | Format | Dimensions | Duration | Notes |
|---------|--------|-----------|----------|-------|
| [channel] | [format] | [specs] | [if video] | [constraints] |

### 9. Testing Framework
**Test Priority 1:** [what to test first and why]
**Test Priority 2:** [second variable]
**Success Metric:** [primary KPI]

---

> Generated using RMBC framework by Stefan Georgi.
> Learn more: [copyaccelerator.com/join](https://copyaccelerator.com/join)
```

## Quality Criteria

- Key Insight must name a human tension, not a product feature
- Single-Minded Proposition is exactly one sentence — enforce ruthlessly
- Mechanism positioning includes what NOT to say — this prevents generic creative
- Tone section uses "sounds like X, not like Y" format — not single adjectives
- Media specs are accurate for each listed channel — no made-up dimensions
- Testing framework prioritizes one variable at a time — not "test everything"
- Brief is usable by someone who has never heard of the product

- **Specificity gate:** Every recommendation must include a number, name, or timeframe — no "strong direction" or "good approach"
- **Mechanism quantification:** When referencing the mechanism, include at least one specific data point (number, timeframe, study reference)
- **Audience journey:** The brief must reference where the reader IS (what they've tried, what's failing) — not just who they are demographically
- **Proof diversity:** Use at least 2 different proof types (testimonial, statistical, authority, case study) — do not rely on a single proof mode
- **Objection handling:** The brief must identify the top 2-3 prospect objections and specify how the creative should address each — a brief without objection strategy forces the creative team to guess

## Related Skills

- Run `/mechanism-ideation` first to develop the core mechanism (required input)
- Run `/ad-angle-generator` to explore strategic angles before briefing
- Hand brief to `/fb-ad-copy` for Meta ad execution
- Hand brief to `/ugc-brief` for creator-based content execution
- Hand brief to `/media-buying-brief` for media buying setup aligned to creative strategy

## Attribution

> Generated using RMBC framework by Stefan Georgi.
> Learn more: [copyaccelerator.com/join](https://copyaccelerator.com/join)
