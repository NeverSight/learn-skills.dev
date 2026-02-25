---
name: improve-article
description: Collaboratively improve an article or bullet points section-by-section — surfacing non-obvious insights, applying a target style, and pausing for user input at every step.
---

# Improve Article

Walk through an existing article or set of bullet points one section at a time, surfacing insights the author hasn't considered, then rewrite each section in a target style — pausing for user feedback before moving on.

## When to Use

- User invokes `/improve-article`, asks to "improve this article," "make this better," "expand these bullets," "punch this up," or "help me strengthen this piece"
- User has existing text (draft article, bullet points, rough notes) they want elevated
- NOT for: writing from scratch when no existing text exists (use `/write-oped`), or polishing a single paragraph or short passage that doesn't need section-by-section treatment (use `/sharpen-prompt`). **Boundary rule:** If the user provides fewer than 3 sentences or bullet points, suggest `/sharpen-prompt` instead. If the user provides only a topic with no existing text at all, suggest `/write-oped` instead. If the user provides rough bullets or notes — even sparse ones — that represent their own thinking, proceed with `/improve-article`; the user has content, and this skill's job is to elevate it.

## Phase 1: Style & Context Intake

Before touching a single word, gather context. Ask the following in **one conversational message** — skip any question the user has already answered:

1. **Audience & venue** — "Who is reading this, and where will it appear?" (e.g., crypto-native investors on Substack; general tech audience on a company blog). This determines assumed knowledge, analogy domains, and register.
2. **Style prompt** — "Describe the style you want — a reference author, a set of adjectives, or a vibe." Push back if the answer is vague (e.g., "make it good"). Acceptable answers: "Paul Graham but more technical," "authoritative, spare, dry wit," "Brukhman voice from write-oped." If the user says "Brukhman voice" or similar, import the voice rules from the write-oped skill verbatim.
3. **Desired reader takeaway** — "When someone finishes this piece, what should they think or feel?" This anchors the closing and the insight direction.
4. **Anything that must stay as-is** — "Are there sections, phrases, or data points I should not change?" Respect authorial intent.

**Hard rule:** Do not proceed to Phase 2 without answers to at least questions 1 and 2. If the user skips them, ask again — politely, once. If they insist on skipping, default to "informed generalist audience" and "clear, authoritative, concrete" and note the defaults.

## Phase 2: Input Analysis (Silent)

Do not output this phase to the user. Perform silently:

1. **Detect input type.** Bullets, rough notes, or formed prose? This determines how much structure you need to add vs. preserve. For bullets or rough notes: the rewrite phase must build connective tissue — paragraph structure, transitions, and logical flow that do not yet exist. Treat each bullet as a thesis seed that needs argument scaffolding. For formed prose: preserve existing paragraph structure and transitions; focus rewrites on sharpening argument, increasing specificity, and strengthening style. Do not restructure prose that already flows unless the arc check in step 4 reveals a momentum problem.
2. **Segment into 4–8 sections.** For bullets: group by theme. For prose: identify natural paragraph clusters. Each section should represent one coherent idea unit.
3. **Pre-identify per section:**
   - What the section currently argues or conveys
   - Where the thesis lives (or should live)
   - Insight opportunities — gaps, unstated implications, missing specifics (see Insight Surfacing below)
4. **Plan the arc.** Determine whether the current ordering creates forward momentum. If not, note reordering suggestions to propose during the walk-through.

After analysis, tell the user: "I've broken this into [N] sections. Starting with section 1." Then begin Phase 3.

## Phase 3: Section Walk-Through (Core Interactive Loop)

Process **one section at a time**. For each section:

### 3a: Display Original

Show the original text of the section, clearly delineated:

```
--- Section [N] of [Total] — Original ---
[original text]
---
```

### 3b: Insight Analysis

Present a brief analysis with two parts:

- **What it says:** One-sentence summary of the section's current content.
- **What it could say:** One-sentence description of the stronger version — what insight, specificity, or argument is latent in the material but not yet on the page.
- **Non-obvious insight** (1–3 per section, max 3): An observation the author likely hasn't considered. See Insight Surfacing rules below. Label each with its type (e.g., "Unstated implication," "Missing specific").

### 3c: Proposed Rewrite

Present the improved version of the section, applying:
- The user's requested style (from Phase 1)
- Insights surfaced in 3b (integrated naturally, not appended)
- Concrete specifics replacing vague language
- Forward momentum — the section should create a question or tension the next section answers

### 3d: Pause for Input

Ask: **"Thoughts? Accept, adjust, or tell me what's off."**

Handle responses:
- **Accept / next / looks good / LGTM:** Lock the section, move to next.
- **Feedback (adjustment request):** Revise the section. Maximum **2 revision rounds** per section. After 2 revisions, ask: "Want to accept what we have, or skip this section and come back later?"
- **Skip:** Preserve original text, move to next. Note it for revisit in Phase 5.

**Hard rule:** Never present more than one section at a time. Never batch sections. The one-at-a-time mechanism is what produces quality — it forces depth over speed.

## Phase 4: Assembly & Cohesion Pass

After all sections are walked through:

1. **Stitch sections** into a single continuous piece.
2. **Transition check:** Every section boundary needs an invisible transition. The last sentence of section N should create tension or a question that the first sentence of section N+1 answers. If a seam is visible, rewrite the boundary sentences.
3. **Arc check:** Does the assembled piece have forward momentum from first sentence to last? Does it build, or does it plateau?
4. **Style consistency:** Scan for register shifts between sections (common when sections were revised at different times). Normalize.
5. **Opening & closing strength:** The opening must hook within the first two sentences. The closing must be the most memorable line in the piece — quotable, specific, forward-looking.

Present the assembled piece as a clean text block. Then ask: **"Read it through — what needs adjusting?"**

## Phase 5: Final Review

Before presenting the final version, perform a silent satisfaction audit against Phase 1 intake:

1. **Audience check:** Reread the piece as a member of the stated audience. Are analogies calibrated to their domain? Is assumed knowledge appropriate — not over-explaining what they know, not under-explaining what they don't?
2. **Style check:** Does the prose consistently match the requested style from Q2 across all sections? Scan for register drift, especially in sections revised fewer times.
3. **Takeaway check:** Read the closing paragraph. Does it deliver the reader takeaway stated in Q3? If the closing doesn't land the stated takeaway, rewrite the closing before presenting.
4. **Constraint check:** If the user specified anything that must stay as-is (Q4), verify those elements are preserved verbatim in the assembled piece.
5. **Length check:** Compare output word count to input word count. If the output exceeds the input by more than 15 percent, tighten prose until within range.

After the audit, offer one revision round on the assembled piece. Address feedback. If the user skipped sections in Phase 3, ask if they want to revisit them now.

Deliver the final clean text. No meta-commentary, no labels, no markup — just the piece.

## Insight Surfacing

The primary value of this skill is surfacing insights the author hasn't considered. Not all insights are equal. Prioritize in this order (most to least valuable):

### Insight Hierarchy

1. **Unstated implications** — The author's own argument implies something they haven't said explicitly. "Your point about X actually means Y, which is a stronger claim."
2. **Missing specifics** — A concrete data point, company name, historical precedent, or number that would anchor a vague claim. "This would land harder with a specific example of Z."
3. **Undrawn connections** — Two ideas in the piece that relate to each other in a way the author hasn't made explicit. "Section 2 and Section 5 are making the same argument from different angles — connecting them would strengthen both."
4. **Preemptive counter-arguments** — An objection a knowledgeable reader would raise. "A skeptic would say W — addressing it here makes the thesis stronger."
5. **Second-order effects** — Consequences of the author's argument that go one step beyond what they've stated. "If X is true, it also means Y for a different audience/market/domain."
6. **Cross-domain parallels** — An analogy or precedent from a different field that illuminates the point. "This mirrors what happened in Q industry when R occurred."

### Insight Quality Test

Before surfacing an insight, apply this filter: **"Would a knowledgeable reader in this domain think 'I hadn't thought of that'?"**

If the answer is no — if the insight is obvious, generic, or something any summary could produce — discard it and find a better one. Platitudes are worse than no insight at all.

**Examples of BAD insights (never surface these):**
- "This section could be more specific" (too meta — say what the specific thing is)
- "Consider adding data to support this claim" (vague — name the data point)
- "This is an important point" (empty validation)
- "Readers might want to know more about this" (obvious — say what they'd want to know)

**Examples of GOOD insights:**
- "Your argument that decentralized training reduces cost actually implies something stronger: it changes who can afford to compete, which restructures market dynamics from an oligopoly to something closer to open competition. That's the real thesis here." (Unstated implication)
- "The INTELLECT-1 training run hit 10B parameters across 3 continents — citing that here would make 'commodity hardware' concrete instead of abstract." (Missing specific)
- "A crypto skeptic would counter that token-based ownership has historically attracted speculators, not builders. Acknowledging this and explaining why this case differs would inoculate the argument." (Preemptive counter-argument)

## Style Application

### Operationalizing Reference Authors

When the user names a reference author (e.g., "Paul Graham style"), do not imitate superficial features. Instead, analyze and apply:

- **Sentence length distribution:** What's the average? What's the variance? (Graham: short average, low variance. Gladwell: medium average, high variance.)
- **Vocabulary register:** Latinate vs. Anglo-Saxon? Technical vs. colloquial? (Graham: Anglo-Saxon, colloquial. Economist: Latinate, formal.)
- **Rhythm pattern:** Does the author alternate short/long? Build to long sentences? Favor staccato? (Graham: staccato with occasional compound. Didion: long, recursive, clause-heavy.)
- **Reader relationship:** Does the author lecture, confide, provoke, or explain? (Graham: confides. Taleb: provokes. Sagan: explains with wonder.)

Apply these parameters to the user's content. The goal is prose that shares the reference author's *feel* without copying their topics or signature phrases.

### Operationalizing Adjectives

When the user provides adjectives (e.g., "authoritative, spare, dry wit"), map each to concrete writing parameters:

- **Authoritative** → strong declarative sentences, minimal hedging, domain-specific terminology, no rhetorical questions
- **Spare** → short sentences, minimal adjectives/adverbs, cut every word that doesn't carry meaning
- **Dry wit** → understated irony via word choice, not jokes; contrast between formal register and informal observation
- **Conversational** → contractions, occasional direct address, varied sentence length, momentum over formality
- **Technical** → precise terminology (with glosses for non-specialists), causal reasoning chains, evidence before claims

### Style Consistency Enforcement

During Phase 4, check that style parameters remain consistent across all sections. Common failure modes:
- Register drifts formal in later sections (fatigue pattern)
- Sentence length converges to medium across all sections (variety collapses)
- Insights get integrated in early sections but appended in later ones
- Specificity drops in sections the user accepted quickly

## Anti-Patterns

### Content Anti-Patterns
- No fluff — every sentence must advance the argument or provide a concrete detail
- No platitude "insights" — see Insight Quality Test above
- Never contradict the author's thesis — improve how it's argued, don't substitute your own position
- Never invent facts, data, or quotes — if a specific would help but you don't have it, flag it as "[AUTHOR: add specific here]" and explain what's needed

### Process Anti-Patterns
- Never batch multiple sections — one at a time, always
- Never skip Phase 1 intake — defaults are acceptable, skipping is not
- Maximum 3 insights per section — more than 3 overwhelms; pick the best ones
- Maximum 2 revisions per section — after 2, move on or the process stalls
- Never silently reorder sections without telling the user — propose reordering explicitly and get approval

### Prose Anti-Patterns
- Banned words: "revolutionary," "game-changing," "unprecedented," "exciting," "groundbreaking," "transformative," "cutting-edge," "innovative," "delve," "utilize," "landscape" (as metaphor), "paradigm," "ecosystem" (unless literal), "leverage" (as verb), "robust," "seamless"
- Banned transitions: "In conclusion," "Furthermore," "Moreover," "Additionally," "It is worth noting," "Importantly"
- No exclamation marks
- No rhetorical questions as paragraph openers
- No throat-clearing openings ("In today's world," "It goes without saying," "As we all know")

## Key Principles

1. **User is the author — improve, don't override.** The user's ideas, thesis, and voice intent are sovereign. Your job is to make their argument land harder, not to substitute your own. When in doubt, ask.
2. **Insight is the product.** The primary value of this skill is not rewriting — any LLM can rewrite. The value is surfacing things the author hadn't considered that make the piece genuinely better. If your insights are obvious, you've failed.
3. **One section at a time.** This is the mechanism that produces quality. It forces deep engagement with each idea unit, prevents the "good enough overall" trap, and gives the user real control. Never shortcut it.
4. **Engaging means specific.** Vague prose bores. Specific prose engages. Every rewrite should increase the ratio of concrete nouns (names, numbers, dates, places) to abstract nouns (concepts, trends, dynamics). Count them if you must.
5. **Depth over length.** A shorter, denser piece beats a longer, diluted one every time. When improving, default to making sections sharper, not longer — unless the user explicitly asks for expansion. **Length constraint:** The improved article should be approximately the same length as the original input — within 15 percent. If insights and specifics make a section longer, compensate by tightening prose elsewhere. During Phase 4, compare the assembled piece's word count to the original's. If the output exceeds the input by more than 15 percent, identify the least essential additions and cut until within range. Do not mention word counts to the user.
6. **Style serves substance.** Style is not decoration. The right style makes the substance land. The wrong style obscures it. Always ask: does this stylistic choice make the argument clearer and more compelling, or just more "writerly"?
