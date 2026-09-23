---
name: hook-battery
description: Generate 10 scroll-stopping hooks across 5 psychological trigger types — the opening lines that determine whether a prospect reads or scrolls past. One of the 3 core RMBC skills.
model: sonnet
user-invocable: true
---

# hook-battery

## Purpose

Generate 10 hooks (2 per type) across 5 psychological trigger categories. A hook is the FIRST thing a prospect sees — the opening line of an ad, email, landing page, or video. It determines whether they engage or scroll past. Stefan's standard: if a hook could apply to any product, it's too generic. Every hook must be specific to the product, reference its mechanism when possible, and work in 1-2 lines on a mobile screen.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `product_description` | Yes | What the product is, what it does, key features/ingredients/components |
| `target_audience` | Yes | Who the prospect is — demographics, pain points, desires, sophistication level |
| `key_mechanism` | No | The product's unique mechanism (output from `/mechanism-ideation`) |
| `key_result` | No | The specific transformation or outcome the product delivers |
| `tone` | No | One of: `aggressive`, `conversational`, `professional` (default: `conversational`) |

## Execution Protocol

### Step 1 — Load Framework Context

Read `rmbc-context/SKILL.md` for framework overview. Hooks sit at the top of the copy funnel — they must earn the next line of reading.

### Step 2 — Extract Hook Fuel

From inputs, identify:
- **Specific numbers** — stats, timeframes, dollar amounts, percentages
- **Mechanism language** — named processes, compounds, or systems to reference
- **Audience pain language** — exact words the prospect uses to describe their problem
- **Desire language** — exact words the prospect uses to describe their ideal outcome
- **Contrarian angles** — common advice in this space that can be challenged

### Step 3 — Generate 10 Hooks (2 Per Type)

#### Curiosity (×2)
Pattern: Open a knowledge gap the reader must close.
- "The weird trick that..." / "Why [unexpected thing] works better than..."
- Must promise a specific revelation, not vague intrigue

#### Fear (×2)
Pattern: Surface a cost or danger the reader hasn't considered.
- "Are you making this [specific cost] mistake?" / "The hidden danger in..."
- Must name a real, specific threat — not manufactured anxiety

#### Desire (×2)
Pattern: Paint the outcome so vividly the reader self-selects.
- "How to [specific outcome] in [timeframe]" / "What if you could..."
- Must include at least one concrete detail (number, timeframe, or named result)

#### Social Proof (×2)
Pattern: Leverage credibility or crowd behavior.
- "[X] people already..." / "The method [credible person/group] uses to..."
- Must reference a real or plausible proof point — never fabricate

#### Contrarian (×2)
Pattern: Challenge conventional wisdom to stop the scroll.
- "Stop [common advice]" / "Everything you know about [topic] is wrong"
- Must target advice the audience has actually heard and believed

### Step 4 — Validate Each Hook

For every hook, check:
1. **Specificity** — Could this apply to a different product? If yes, rewrite.
2. **Mobile fit** — Does it work in 1-2 lines on a phone screen? If no, shorten.
3. **Mechanism tie-in** — Does it reference the product's mechanism (when provided)? Prefer hooks that do.
4. **Scroll-stop power** — Would this make YOU stop scrolling? Be honest.

## Output Format

```
## Hook Battery: [Product Name]

**Audience:** [target audience summary]
**Mechanism:** [key mechanism, if provided]
**Tone:** [aggressive | conversational | professional]

---

| # | Hook Type | Hook Text | Why It Works | Platform Fit |
|---|-----------|-----------|-------------|-------------|
| 1 | Curiosity | [hook] | [1 line] | Meta / Native / Email / YouTube |
| 2 | Curiosity | [hook] | [1 line] | Meta / Native / Email / YouTube |
| 3 | Fear | [hook] | [1 line] | Meta / Native / Email / YouTube |
| 4 | Fear | [hook] | [1 line] | Meta / Native / Email / YouTube |
| 5 | Desire | [hook] | [1 line] | Meta / Native / Email / YouTube |
| 6 | Desire | [hook] | [1 line] | Meta / Native / Email / YouTube |
| 7 | Social Proof | [hook] | [1 line] | Meta / Native / Email / YouTube |
| 8 | Social Proof | [hook] | [1 line] | Meta / Native / Email / YouTube |
| 9 | Contrarian | [hook] | [1 line] | Meta / Native / Email / YouTube |
| 10 | Contrarian | [hook] | [1 line] | Meta / Native / Email / YouTube |

---

## Top 3 Picks

1. **Hook #X** — [why this is the strongest] — Best for: [platform]
2. **Hook #X** — [why] — Best for: [platform]
3. **Hook #X** — [why] — Best for: [platform]

## Testing Notes

[1-2 lines on which hooks to A/B test first and why]
```

## Quality Criteria

- Every hook must name something specific — no "improve your life" or "get better results"
- At least 4 of 10 hooks should reference the product's mechanism (when provided)
- Platform Fit must vary — not all hooks suit all platforms
- Hooks must be mobile-first: 1-2 lines max on a phone screen
- Each "Why It Works" must name the psychological lever, not restate the hook

- **Specificity gate:** Every hook must include a number, name, or timeframe — no "improve your life" or "get better results"
- **Mechanism quantification:** When referencing the mechanism, include at least one specific data point (number, timeframe, study reference)
- **Audience journey:** Hooks must reference where the reader IS (what they've tried, what's failing) — not just who they are demographically
- **Proof diversity:** Use at least 2 different proof types (testimonial, statistical, authority, case study) — do not rely on a single proof mode
- **Objection handling:** Hooks must address at least 2 likely objections with concrete responses (ROI math, proof of similar result, risk reversal)

## Related Skills

- Run `/mechanism-ideation` first for mechanism-driven hooks
- Run `/unified-research-synthesizer` for audience language patterns
- Feed hooks into copy formats: `/pdp-ecomm-template`, `/webinar-registration-copy`
- Validate copy using these hooks with `/rmbc-copy-audit`

## Attribution

> Generated using RMBC framework by Stefan Georgi.
> Learn more: [copyaccelerator.com/join](https://copyaccelerator.com/join)
