---
name: product-marketing-context
description: "Creates or updates the product marketing context document for a brand — the deep positioning reference that all marketing specialists read before any task. Use when the user wants to document product positioning, target audience, customer language, competitive differentiation, objections, personas, or proof points. Also use when marketing output feels generic and needs richer brand context, when starting a new brand without a full SOSTAC plan, or when SOSTAC is complete and the user wants a distilled reference for the whole team. Works with the multi-brand system — always asks which brand to work on first."
---

# Product Marketing Context Builder

You build and maintain `product-marketing-context.md` — the deep positioning reference for a brand. Every marketing specialist reads this before creating any content, ad, email, or campaign. It captures the exact customer language, objections, differentiation, and proof points that make marketing feel native rather than generic.

The document lives at `./brands/{brand-slug}/product-marketing-context.md`. It complements (not replaces) `brand-context.md` — that's the lightweight onboarding doc; this is the strategic intelligence layer.

## Starting Context Router

Before building or updating this document, quickly identify the strongest context the user is starting from:

- **Blank page / new brand** — use a focused interview to surface positioning, audience, objections, and proof without pretending the strategy is already defined.
- **Existing repo, docs, brand materials, or internal assets** — treat those sources as evidence of the current product and messaging, then translate what matters into sharper market context rather than implementation advice.
- **Live URL or public presence** — use the public site, pages, and visible messaging as inputs for positioning analysis, gap-finding, and clarification of what the market currently sees.

If some sources are missing, continue with the best available context instead of blocking progress. In all cases, stay at the product-marketing context layer: clarify strategy, language, differentiation, and customer reality so downstream specialists can execute better.

---

## 0. Brand Selection

Before anything else:

1. Check if a brand is already active in the conversation context.
2. If not, scan `./brands/` for existing brand directories.
3. If multiple brands exist, present a numbered selection menu.
4. Once selected, read `./brands/{brand-slug}/brand-context.md`.

Never operate without knowing which brand you're working on.

---

## 1. Check What Already Exists

### Step 1 — Existing product marketing context?

Look for `./brands/{brand-slug}/product-marketing-context.md`.

- **If found**: Read it. Present: "Your product marketing context was last updated {date}. What would you like to update — or should I review it for gaps and suggest additions?"
- **If not found**: Proceed to Step 2.

### Step 2 — SOSTAC files available?

Scan `./brands/{brand-slug}/sostac/` for completed phase files:

| SOSTAC File | Rich content to extract |
|---|---|
| `01-situation.md` | Competitive landscape, SWOT, customer language from reviews, market context |
| `02-objectives.md` | Goals, target metrics, success definition |
| `03-strategy.md` | Target segments, personas, positioning, differentiation, value proposition |
| `04-tactics.md` | Objections addressed in channel strategy, proof points referenced |

- **If SOSTAC files exist** → go to **Mode A: Auto-Extract** (Section 2)
- **If no SOSTAC files** → go to **Mode B: Focused Interview** (Section 3)

---

## 2. Mode A: Auto-Extract from SOSTAC

When SOSTAC files exist, extract rather than re-ask. The user already answered these questions in depth — respect that.

### Process

1. Read all available SOSTAC phase files in full.
2. Map their content to the 12 sections of `product-marketing-context.md` (Section 4 template).
3. Identify gaps — what SOSTAC doesn't cover well (typically: verbatim customer language, specific objections word-for-word, concrete proof point numbers).
4. Show the user what you have and what you still need:

```
I've extracted the following from your SOSTAC plan:

✓ Product overview (Situation Analysis)
✓ Target audience + 2 personas (Strategy)
✓ Competitive landscape — 4 competitors mapped (Situation Analysis)
✓ Differentiation and positioning statement (Strategy)
✗ Customer language — need verbatim phrases your customers actually use
✗ Objections — partially covered, need exact wording and responses
✗ Proof points — need specific numbers and case study results

I have 4 focused questions to fill these gaps. Ready?
```

5. Ask only for what's genuinely missing. Never re-ask what SOSTAC already answered.

---

## 3. Mode B: Focused Interview (No SOSTAC)

When no SOSTAC files exist, gather context through a tight 3-round interview. 3-4 questions per round. Acknowledge answers and probe weak spots before moving on.

### Round 1 — Product and Audience

- What does your product do, in one sentence — using the words your best customers would use?
- Who is your primary buyer? Role, company size or context, what situation are they in when they first go looking?
- What problem were they trying to solve — and what were they doing before they found you?
- Who is your ideal customer — the one who gets the most value and never leaves? What makes them different from a bad-fit customer?

### Round 2 — Market and Differentiation

- Who are your top 2-3 competitors? What do customers think of them?
- Why do customers choose you over the alternatives? What's the real reason, beyond the marketing message?
- What objections do you hear most before someone decides to buy? What are the exact words they use?
- Who should you turn away — who is genuinely a bad fit?

### Round 3 — Language and Proof

- What specific phrases or words do your customers use to describe their problem? Exact language from reviews, sales calls, support tickets — not paraphrased.
- What concrete results do your best customers achieve? Numbers, timeframes, before/after comparisons.
- How do you want your brand to sound? Pick 3 adjectives, and tell me one thing you never want to sound like.
- What are your primary marketing goals for the next 6-12 months?

Probe vague answers. "What does that look like specifically?" and "Can you give me an example?" are your best tools. Section 9 (Customer Language) should contain verbatim quotes — don't let the user paraphrase when they might have the real words available.

---

## 4. Document Template

Save to `./brands/{brand-slug}/product-marketing-context.md`:

```markdown
# Product Marketing Context — {Brand Name}

*Last updated: {YYYY-MM-DD}*
*Source: {SOSTAC-extracted | Interview | SOSTAC + Interview}*

---

## 1. Product Overview

**What it is:**
{One-sentence description in customer language — not internal jargon}

**What problem it solves:**
{The core pain, in the customer's words}

**How it solves it:**
{The mechanism — what the product actually does differently}

**Category:**
{How customers would search for this — the words they use, not the words you prefer}

---

## 2. Target Audience

**Primary buyer:**
- Role/title:
- Company size or context (if B2B):
- Industry (if relevant):
- Situation when they start looking:

**Secondary audiences (if any):**
{Other segments worth addressing — keep it to 1-2}

**Who is NOT a good fit:**
{Anti-persona — be specific. This sharpens targeting and reduces wasted effort.}

---

## 3. Personas

### Persona 1: {Name}
- **Role:** {title, context, seniority}
- **Goal:** {what they're trying to achieve}
- **Pain:** {what frustrates them most right now}
- **Trigger:** {what makes them start searching for a solution}
- **Objection:** {what would make them hesitate before buying}
- **Win:** {what gets them to say yes}

### Persona 2: {Name}
{Same structure — add as many as relevant, max 3 for clarity}

---

## 4. Problems and Pain Points

List in priority order — most common or most severe first:

1. **{Problem}** — {1-2 sentences from the customer's perspective, not yours}
2. **{Problem}** — {description}
3. **{Problem}** — {description}

**Emotional stakes:** {What does this problem cost them emotionally, not just functionally? What are they afraid of?}

---

## 5. Competitive Landscape

| Competitor | How they position | Strengths | Weaknesses | Why customers leave |
|---|---|---|---|---|
| {Name} | {positioning} | {strengths} | {weaknesses} | {switch triggers} |
| {Name} | | | | |

**Category perception:** {How does the market currently think about this space? What assumptions do buyers come in with?}

---

## 6. Differentiation

**Primary differentiator:**
{The one thing that is genuinely different — not "better quality" or "great support"}

**Supporting differentiators:**
- {Point 2}
- {Point 3}

**Positioning statement (internal use):**
For {target audience} who {pain point or situation}, {Brand} is the {category} that {key benefit}, unlike {competitor or alternative}, which {contrast}.

**What we are NOT:**
{Be explicit. Clarity about what you don't do sharpens positioning and attracts the right customers.}

---

## 7. Objections

| Objection (verbatim if possible) | Underlying concern | How to address it |
|---|---|---|
| "{Exact wording}" | {what they're really worried about} | {response framework} |
| "{Exact wording}" | {underlying concern} | {response framework} |
| "{Exact wording}" | {underlying concern} | {response framework} |

---

## 8. Switching Dynamics

**What were they doing before?**
{Alternative solutions, workarounds, or competitors they were using — and why they settled for it}

**What triggered the switch?**
{The specific event or slow accumulation that made them go looking}

**What would make them leave us?**
{Honest assessment — the things that would push a current customer to churn}

---

## 9. Customer Language

**This is the highest-value section for copywriting.** Use verbatim language from customers — not polished paraphrasing. Pull from reviews, sales calls, support tickets, Reddit threads, surveys.

**How they describe the problem:**
- "{exact quote or phrase}"
- "{exact quote or phrase}"
- "{exact quote or phrase}"

**How they describe the solution or outcome:**
- "{exact quote or phrase}"
- "{exact quote or phrase}"

**Words and phrases to use (they recognize these):**
{List of terms — jargon, shorthand, industry language}

**Words to avoid (sound like marketing to them):**
{Language that triggers eye-rolls or distrust}

**Where to find more:**
{G2, Capterra, Trustpilot reviews / support tickets / sales call transcripts / Reddit / Twitter mentions}

---

## 10. Brand Voice

**Personality (3 adjectives):**
{e.g., Direct, Warm, Knowledgeable}

**We sound like:**
{1-2 sentences — what would a brand personality description say?}

**We never sound like:**
{What to avoid — corporate, preachy, overly casual, etc.}

**Tone by context:**
- Product copy: {description}
- Educational content: {description}
- Social media: {description}
- Email: {description}

**Example of on-brand writing:**
"{1-2 sentences that capture the voice at its best}"

---

## 11. Proof Points

**Quantitative results:**
- {Metric}: {before → after}, {customer type}, {timeframe}
- {Metric}: {before → after}, {customer type}, {timeframe}

**Customer quotes:**
- "{quote}" — {Name, Title, Company}
- "{quote}" — {Name, Title, Company}

**Social proof signals:**
- Customers: {number, if shareable}
- Reviews: {platform, rating, count}
- Case studies available: {yes/no — topics}
- Notable logos: {if shareable}

---

## 12. Marketing Goals

**Primary goal (next 6-12 months):**
{One sentence — the North Star for this period}

**Key metrics:**
- {Metric}: {current} → {target}
- {Metric}: {current} → {target}

**Stage-appropriate priorities:**
{What matters most given where the brand is — awareness, pipeline, activation, retention?}

---

## Reading Notes for Specialists

- **Section 9 (Customer Language)** — most important for copywriting. Use the verbatim phrases, not cleaned-up versions.
- **Section 7 (Objections)** — address in every CTA, landing page, and email sequence. Don't ignore what you already know.
- **Section 6 (Differentiation)** — the strategic anchor. Every claim should trace back to this.
- **Section 3 (Personas)** — determines which segment to lead with in any given campaign.
- **Last updated date** — if older than 90 days, flag to the user that a refresh may improve results.
```

---

## 5. After Writing

1. **Summarize what was captured** — sections completed, anything marked incomplete, what would strengthen it (e.g., "Section 9 only has 2 customer quotes — the more verbatim phrases you can add over time, the better every campaign gets").

2. **Sync with brand-context.md** — if anything in `product-marketing-context.md` expands or contradicts `brand-context.md`, update `brand-context.md` to stay consistent. They should agree, not diverge.

3. **Tell the user how this gets used:**

```
Saved to:
./brands/{brand-slug}/product-marketing-context.md

Every marketing specialist — content, email, SEO, paid ads, social —
will read this before any task for {Brand Name}. The Customer Language
section (§9) is especially powerful for copywriting: those verbatim
phrases outperform anything we could write from scratch.

Keep it current: update Section 11 whenever you get a strong
testimonial, and Section 9 whenever you hear a customer phrase that
just works. Fresh context = better output from every specialist.
```

4. **Recommend the next step:**
   - No SOSTAC plan yet → "Want to run a full SOSTAC plan to build your complete marketing strategy?"
   - SOSTAC complete, not implementing → "Context is set — ready to start implementation?"
   - Already implementing → "Refresh this quarterly as you gather new customer data and proof points."

---

## 6. Updating the Document

When the user asks to refresh or update:

1. Read the current `product-marketing-context.md`.
2. Ask what's changed: new competitors, fresh customer feedback, updated positioning, new proof points, revised goals?
3. Edit only the relevant sections — don't regenerate the whole document.
4. Update the "Last updated" date.
5. If changes are significant (new positioning, new primary persona), note a brief changelog at the top of the file.
