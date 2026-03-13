---
name: humanize
description: Convert AI-written text to more human-like writing through subtle edits. Use when text reads "too AI", when the user mentions "humanize", "sounds robotic", "AI-written", "make it natural", or when editing for a more conversational voice.
---

# Humanize Text

Make AI-generated content read like it was written by a human through targeted, subtle edits.

**Why?** AI-written text has telltale patterns—formulaic transitions, passive voice, overly balanced sentences—that make it feel mechanical. This skill fixes those patterns without rewriting the whole document.

**Model Coverage:** Tested on Opus 4.5, Sonnet 4, Haiku. See **[TESTING.md](./TESTING.md)** for details.

## Quick Start

1. `wc -w FILE` (baseline) → 2. Scan for patterns → 3. Make 10-20 targeted edits → 4. Verify ±20 words & 0 em-dashes → 5. Check burstiness

**Supporting Files:** [REFERENCE.md](./REFERENCE.md) (pattern tables) | [TESTING.md](./TESTING.md) (evaluation scenarios)

## Content Integrity Rules (CRITICAL)

> [!CRITICAL]
> **The Cardinal Rule: Transform style, never fabricate content.**
>
> Humanization edits HOW something is expressed, not WHAT is expressed. Every technique must work only with material already present in the source text.

### Allowed (Style Transformation)
- Restructure sentences (change order, split, combine)
- Replace words with synonyms that preserve meaning
- Change punctuation and sentence boundaries
- Add/remove contractions (domain-appropriate)
- Convert passive to active voice
- Vary sentence lengths by restructuring existing content
- Add hedging to soften existing claims ("X is true" → "X appears to be true")
- Convert existing lists to prose or vice versa

### Forbidden (Content Fabrication)
- Invent personal anecdotes, opinions, or experiences not in source
- Add fake citations, names, dates, or statistics
- Create metaphors that introduce claims not in the original
- Insert "I've seen...", "In my experience..." unless source has them
- Make up specific details to replace vague ones
- Add editorial commentary ("surprisingly", "disappointingly") unless source expresses that sentiment

### The Source Material Test
Before any edit, ask: **"Is this information already in the source text?"**
- If YES → transform freely
- If NO → do not add it

## How It Works

### Step 1: Read and Scan for AI Patterns

Read the target file and identify common AI-writing tells. **Priority patterns to scan first:**

1. **"By [gerund]"** — "By implementing...", "By training..."
2. **"That [noun]" connectors** — "That shift...", "That vulnerability..." (linking sentences)
3. **Indirect speech** — "The field is shifting...", "Research suggests...", "A study identifies..."
4. **Em-dashes (—)** — Humans rarely use them; AI overuses them
5. **"This [verb] that"** — "This suggests that...", "This demonstrates that..."
6. **Subordinate smoothness** — "while maintaining X", "thereby reducing Y" (too-smooth connectors)
7. **Framework intro pattern** — "The [X] framework mitigates/addresses..." (robotic combo)
8. **High-risk phrases** — "framework provides" (7x), "maintaining high" (6.4x), "eliminating the need" (5.4x)
9. **"For X, Y does Z"** — "For real-time applications, X optimizes..." (formal opener)
10. **Colon definition splits** — "X decouples A from B: it maintains..." (explanatory colons)
11. **Too-simple declaratives** — Short, direct sentences can also trigger "robotic formality"

See **[REFERENCE.md](./REFERENCE.md#ai-pattern-detection-table)** for the complete pattern detection table.

### Step 2: Apply Targeted Edits

Make 10-20 edits across the document. Do NOT rewrite entire sections.

### Step 2b: Word Count Verification (MANDATORY)

> [!CRITICAL]
> **THE ±20 WORD RULE:** Final word count must be within **±20 words** of the original. Always measure against the ORIGINAL document, not previous iterations.
>
> AI models inherently summarize. You must fight this bias by restructuring, not condensing.

**Workflow:**
1. **Measure:** `wc -w PATH` before editing
2. **Edit:** Apply targeted changes
3. **Verify:** `wc -w PATH` after editing
4. **If > 20 word change:** STOP. Revert and restructure instead of cutting/padding

**How to preserve word count:**
- Restructure sentences: "By analyzing X" → "When analyzing X" (same length)
- Expand expressions: "X happens" → "X happens because Y, which means Z"
- Never pad with filler ("meaningfully", "smartly", "actively")

### Step 2c: Em-Dash Count Verification (MANDATORY)

> [!CRITICAL]
> **NO NEW EM-DASHES:** Em-dash count must NOT increase. Target: 0.

**Verify:** `grep -o '—' PATH | wc -l` (before and after)

**If em-dashes increased, replace with:** periods, commas, colons, or parentheses.

### Step 2d: Anti-Detection (Burstiness & Perplexity)

AI detectors measure statistical uniformity. Disrupt rhythm and predictability using **only existing content**.

**1. Burstiness (Sentence Length Variation):**

> [!CRITICAL]
> AI maintains uniform 12-18 word sentences. Human writing has HIGH variance. This is the #1 detection signal.

Target per 10 sentences: 2-3 very short (2-6 words), 2-3 very long (25-40 words), 4-5 medium. See **[REFERENCE.md](./REFERENCE.md#burstiness-targets)**.

**Techniques:**
- Split: "The model processes data and outputs results" → "The model processes data. Then it outputs results."
- Combine: "X works. Y helps." → "X works, and when combined with Y, it improves significantly."

**2. Vocabulary Entropy:**

Replace 3-5 "AI-typical" words per paragraph with rarer synonyms that preserve meaning exactly. See **[REFERENCE.md](./REFERENCE.md#vocabulary-alternatives)**.

> [!CAUTION]
> Synonym must have EXACT same meaning. If unsure, keep the original.

**3. Visual Structure:** Vary paragraph shapes (dense → bullets, short paragraphs → merged).

### Step 2e: Lexical Diversity

AI text has measurably lower vocabulary diversity. Fix by varying word choice **using only synonyms that preserve meaning**.

**1. Connector Audit:** Each connector should appear **max 2 times per 1000 words**. If more, replace 50% or restructure. See **[REFERENCE.md](./REFERENCE.md#connector-replacements)**.

**2. Verb Repetition:** If any verb appears 3+ times in 500 words, vary it. See **[REFERENCE.md](./REFERENCE.md#verb-repetition-alternatives)**.

**3. Noun Phrase Variation:** After first reference, vary: "The transformer" → "this approach" → "it"

> [!CAUTION]
> Never change meaning. Only vary when semantically equivalent.

### Step 2f: Punctuation Diversity

Humans use more varied punctuation than AI. Increase variety by restructuring. See **[REFERENCE.md](./REFERENCE.md#punctuation-targets)** for targets.

**Techniques:**
- **Questions:** "The implications are significant" → "What are the implications? They're significant."
- **Semicolons:** "X is fast. Y is slow." → "X is fast; Y is slow."
- **Parentheses:** "The approach, which is unconventional, works." → "The approach (unconventional as it is) works."

> [!CAUTION]
> Questions must not imply answers not in the source.

### Condensing vs. Restructuring

> [!CRITICAL]
> **Most common failure mode.** Condensing removes words; restructuring rearranges them.

| Condensing (❌) | Restructuring (✅) |
|---|---|
| "Long sentence" → "Short sentence" | "Long sentence" → "Reworded long sentence" |
| Removes words | Changes arrangement |
| Net content loss | Same content, different pattern |

**When tempted to condense:** Expand expressions, add supporting detail, or break into multiple sentences.

**Multi-Pass for Long Documents (2000+ words):**
1. Scan high-frequency patterns
2. Fix sentence rhythm
3. Verify no new patterns created
4. Word count check (MANDATORY)

**Transition Replacements:** See **[REFERENCE.md](./REFERENCE.md#transition-replacements)**.

**Key Rules:**
- Never use em-dashes. Replace with periods, commas, colons, or parentheses
- Questions only for topic transitions, not rhetorical pauses
- Keep formal register in academic writing (no contractions)
- Remove filler: "It is worth noting that" → just state the thing

### Step 3: Add Human Personality

> [!IMPORTANT]
> **Removing AI patterns is not enough.** Detectors also flag text that lacks "rhetorical flourishes" and feels "impersonal." You must ADD human touches using only existing content.

**Inject Personality (without fabricating):**
- **Mild surprise:** "Interestingly," or "Curiously," before a finding (if the finding IS interesting)
- **Conversational asides:** "—and this matters—" or "(worth noting)"
- **Direct address:** "Here's the thing:" or "Notice that..."
- **Occasional informality:** "pretty effective" instead of "effective", "a lot" instead of "significantly"
- **Opinion hedging:** "seems to", "appears to" (humans hedge more than AI)

**Disrupt S-V-O Order:**
- Invert occasionally: "Effective, this approach was not." → only when natural
- Lead with result: "A 10% gain—that's what the model achieved."
- Fronted adverbials: "In practice, the system fails." instead of "The system fails in practice."

**Break Impersonal Tone:**
- Replace "The field is shifting" → "Researchers are shifting the field" (add human actors)
- Replace "Research suggests" → "Three recent papers suggest" (specificity)
- Replace "The implication is clear" → "What does this mean? It means..." (question form)

**Vary Grammar (Break "Correct but Unvaried"):**
- Avoid repeating sentence structures: if three sentences use "X [verb]s Y", restructure one
- Break parallel semicolon lists: "A does X; B does Y; C does Z" → "A does X. Meanwhile, B does Y. And C? It does Z."
- Use sentence fragments occasionally: "The result? Better accuracy."
- Try rhetorical inversion: "Effective, this was not." (sparingly)
- Interrupt with asides: "The model—surprisingly—failed at basic counting."
- Break colon splits: "X decouples A from B: it maintains..." → "X separates A and B. This lets it..."

**Fix "Too Simple = Robotic":**
- Very short declaratives trigger detection too: "The focus is on X." feels robotic
- Add texture: "The focus? X." or "What's the focus here? X."
- Combine with adjacent sentence to add flow
- Or add mild opinion: "The focus, rightly, is on X."

**Fix Indirect Speech (Still Heavily Flagged):**
- "A study identifies..." → "Smith et al. found...", "Recent work shows...", or just state the finding
- "A protocol called X becomes necessary" → "You need X" or "X becomes essential"
- "Research suggests..." → Name the researchers or say "Three papers this week show..."
- Add human actors: "The field is shifting" → "Researchers are rethinking..."

**Humanize Headings (if editing full documents):**
- Overly clean headings trigger detection ("Multimodal Grounding and Internal Mechanics")
- Add slight informality: "How Models Actually See" instead of "Visual Processing Mechanisms"
- Use questions: "Why Do Models Fail at Counting?" instead of "Enumeration Failures"
- Keep some formal, vary others—consistency in heading style is itself a tell

### Step 4: Vary Your Edits

> [!CAUTION]
> Don't create new patterns. If you replace every "However" with "But", that's just a different pattern. Mix it up:
> - Some "However" → "But"
> - Some "However" → start sentence differently
> - Some "However" → merge with previous sentence using ", but"
> - Some "However" → leave as-is

### Step 5: Final Verification Checklist

> [!IMPORTANT]
> Complete ALL checks before submitting. For detailed validation scenarios, see **[TESTING.md](./TESTING.md)**.

**Content Integrity (DO FIRST):**
- [ ] No anecdotes/experiences fabricated
- [ ] No citations/statistics invented
- [ ] All synonyms preserve exact meaning

**Quantitative (MANDATORY):**
- [ ] Word count within ±20 words of original
- [ ] Em-dash count ≤ original (target: 0)
- [ ] Connectors ≤ 2 per 1000 words each
- [ ] Sentence length varies (<6 and >25 word sentences present)

**Style:**
- [ ] No 2+ consecutive paragraphs start same way
- [ ] Technical terms and citations preserved
- [ ] Contractions match domain register

**Quick Validation:**
```bash
wc -w FILE                    # Word count
grep -o '—' FILE | wc -l      # Em-dashes (target: 0)
```

**Final Test:** Does the edited version claim anything the original didn't? If yes, revert.

## Examples

**Example 1: Formulaic Opening**
- Before: "A systematic evaluation of 53 large language models has revealed that longer reasoning chains do not reliably produce better answers."
- After: "A systematic evaluation of 53 large language models revealed something counterintuitive: longer reasoning chains don't reliably produce better answers."

**Example 2: "This suggests" Pattern**
- Before: "This method proves particularly effective in mathematical reasoning, suggesting that the dichotomy between imitation and exploration is artificial."
- After: "Works especially well for mathematical reasoning, which suggests the imitation vs. exploration dichotomy might be artificial."

**Example 3: Passive + Formal**
- Before: "The deployment of Large Reasoning Models has been hampered by their tendency to apply uniform computational resources."
- After: "Large Reasoning Models have a problem: they apply the same computational effort whether you ask them to add two numbers or prove a theorem."

**Example 4: Conclusion Softening**
- Before: "This week's research reflects a shift from unbounded reasoning capability toward calibrated cognitive efficiency."
- After: "The week's theme: unbounded reasoning isn't always better."

**Example 5: "By [gerund]" Pattern**
- Before: "By employing a margin policy gradient loss and rejection sampling, CompassJudger-2 attempts to create a generalist judge that rivals larger models."
- After: "CompassJudger-2 uses margin policy gradient loss and rejection sampling to create a generalist judge rivaling larger models."

**Example 6: Framework Redundancy**
- Before: "The RefCritic framework employs a long-chain-of-thought critic module trained via reinforcement learning."
- After: "RefCritic employs a long-chain-of-thought critic module trained via RL."

**Example 7: Result Phrasing**
- Before: "This approach achieves a 23.2% improvement in success rates on novel software environments compared to static baselines."
- After: "The result: 23.2% better success rates on novel software environments."

**Example 8: Adding Questions**
- Before: "However, applying these techniques to open-ended domains has remained elusive due to the lack of verifiable signals."
- After: "However, applying these to open-ended domains has remained elusive. Why? No verifiable signals to anchor the training."

**Example 9: Preserving Word Count While Removing "By [gerund]"**
- Before (32 words): "By analyzing synchronous discourse in human-AI triads, researchers found that the educational value of these agents lies not in their ability to generate content, but in their capacity to alter the structure of reasoning."
- After (32 words): "When analyzing synchronous discourse in human-AI triads, researchers found that the educational value of these agents lies not in their ability to generate content, but in their capacity to alter the structure of reasoning."
- Note: Pattern change achieved by substituting "By" → "When" without restructuring, padding, or cutting. Same word count, improved tone.

## Quality Guidelines

- **Preserve meaning**: Edits change tone, not content
- **Stay subtle**: 10-20 targeted edits, not a full rewrite
- **Maintain expertise**: Knowledgeable but not robotic
- **Don't over-correct**: The problem is *overuse* and *uniformity*, not formality itself
- **First-reference rule**: Keep context on first mention; only shorten after established

**Domain-Specific Calibration:** See **[REFERENCE.md](./REFERENCE.md#domain-specific-calibration)**.

**Academic/Research Warnings:**
- Never pad with hollow adverbs ("meaningfully", "smartly")
- Keep technical terminology, section structure, and citations intact
- Vary your pattern replacements (don't swap all "By [gerund]" with "When [verb]")

## Troubleshooting

| Problem | Solution |
|---------|----------|
| **Word count changed >20 words** | STOP. Revert. Restructure instead of cutting/padding. |
| **Em-dash count increased** | STOP. Replace new em-dashes with periods, commas, colons, or parentheses. |
| **Still detected as AI (98%+)** | Increase burstiness aggressively; add more punctuation variety; vary vocabulary more. |
| **Fabricated content** | Revert. Review Content Integrity Rules. Only transform what exists. |
| Text too casual | Scale back conversational asides; keep original phrasing. |
| New repetitive pattern | Vary replacements; use different fixes for same issue. |
| Compounding issues | Always measure against ORIGINAL document, not previous iteration. |

## Edge Cases

**Edge Case 1: Short Document (<200 words)**
- Apply only 3-5 edits maximum
- Focus on the most egregious patterns first
- May not hit all burstiness targets; that's okay for short content

**Edge Case 2: Technical Jargon-Heavy Text**
- Do NOT replace domain-specific terms with synonyms
- Focus on structure (transitions, sentence flow) rather than vocabulary
- Example: "The LLM utilizes attention mechanisms" → keep "attention mechanisms" but change "utilizes" to "uses"

**Edge Case 3: Already Human-Like Text**
- If detector scores <70% AI, minimal changes needed
- Focus only on obvious patterns (em-dashes, "By [gerund]")
- Risk: over-editing good text makes it worse

**Cross-Article Consistency:**
When editing multiple articles, vary replacements across articles; don't use "The key insight:" in every one.
