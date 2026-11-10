---
name: voice-editor
version: 1.0.0
description: "Edit draft or auto-generated prose to match an existing personal voice profile. Use when transforming generic text into the profiled author's wording, cadence, and style. Not for creating the profile or matching a journal; use $voice-analyzer or $journal-voice."
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Voice Editor: Transform Content to Match Your Voice

Transform generic or auto-generated content into voice-matched writing using a VOICE.md profile. Voice doesn't live in first drafts — it lives in editing choices. This skill guides the multi-pass editing process that turns generic output into something distinctively yours.

## Quick Start

Provide:
1. **Content to edit** (paste or file path)
2. **VOICE.md location** (default: `.context/voice/voice.md` or project's `.context/voice/voice.md`)

The skill will:
1. Run slop detection on the content
2. Identify voice mismatches against your profile
3. Perform multi-pass editing (Structure > Voice > Polish)
4. Output edited content with change annotations
5. Suggest VOICE.md updates based on patterns found

---

## The 30-40% Rule

Even with a perfect style guide, expect to edit 30-40% of AI output to make it distinctively yours. This isn't a problem — it's the feature.

30-40% editing effort is dramatically less than 100% writing-from-scratch effort, while producing work that sounds more like you than unguided AI ever could.

**If you're editing more than 50%:** Your style guide needs refinement, or your prompts need work.

**If you're editing less than 20%:** You might be accepting too much generic content.

---

## Editing Modes

See [`references/editing-modes.md`](references/editing-modes.md) for mode selection (light, standard, heavy, rescue) and expected effort per mode.

---

## Editing Workflow

### Pass 1: Structure Check

**Focus:** Does the organization serve the content?

**Questions to ask:**
- Does the opening hook or just clear throat?
- Is there a clear progression of ideas?
- Does each section earn its place?
- Is anything redundant or missing?
- Does the conclusion land or just stop?

**Actions:**
- Cut throat-clearing openings ("In this article, we'll explore...")
- Reorder sections for better flow
- Merge redundant sections
- Add missing transitions
- Strengthen weak conclusions

**Academic mode:** Skip opening mechanics checks for papers — academic openings follow different conventions (context-gap-contribution is standard, not a flaw). Focus on logical flow between sections instead.

### Pass 2: Voice Alignment

**Focus:** Does this sound like the voice profile?

**Check against VOICE.md:**
- Sentence length patterns (matching variance?)
- Vocabulary fingerprint (right formality level?)
- Tone markers (humor, directness, reader relationship?)
- Structural habits (lists vs prose, formatting?)
- Opinion expression (appropriate confidence level?)

**Actions:**
- Replace formal language with conversational equivalents (or vice versa for academic)
- Vary sentence lengths to match profile
- Add characteristic phrases from the voice profile
- Adjust opinion strength to match profile
- Fix paragraph rhythm

**Academic mode:**
- Use "we" not "I" (standard academic first person)
- Precision over punchiness — specific claims with citations beat colorful prose
- Preserve appropriate hedging ("our results suggest", "we find evidence consistent with")
- Cut filler, don't add flavor — a tight 20-word sentence beats a loose 35-word one

### Pass 3: Slop Removal

**Focus:** Eliminate AI tells and forbidden phrases

**Scan for:**
- Tier 1 phrases (remove immediately): "delve", "game-changing", "it's worth noting", "moreover"
- Tier 2 patterns (check context): repeated transitions, paired adjectives
- Tier 3 clusters (OK in isolation, problematic together): every paragraph starting with "However"
- Structural tells: uniformity, over-balance
- Staccato fragment spam: 3+ consecutive short declarative sentences in parallel structure
- Comparator sentences: "This isn't X. It's Y." rhetorical crutch

**Actions:**
- Delete or replace all Tier 1 phrases
- Evaluate Tier 2 in context, remove if generic
- Redistribute Tier 3 to avoid clustering
- Vary sentence lengths if too uniform
- Rebalance sections if all equal weight
- Combine staccato fragments into flowing prose with commas, em-dashes, or conjunctions
- Rewrite comparators directly — just say what something IS, don't waste words on what it isn't



### Pass 4: Specificity Injection

**Focus:** Replace generic with specific

**What to cut:**
- Generic superlatives without claims ("game-changing", "revolutionary")
- Hedging that adds no value ("it might be argued that")
- Corporate platitudes ("leverage synergies")
- Anything that sounds like a press release

**What to add:**
- Your actual opinion (not the diplomatic version)
- Specific examples from your experience
- Honest acknowledgment of limitations
- Your characteristic quirks and phrases
- Conversational asides that show how you think

**Academic mode:** Add specific claims with citations. Replace vague "the literature shows" with "Sant'Anna and Zhao (2020) show that...". Use precise terminology over accessible synonyms.

### Pass 5: Rhythm and Flow

**Focus:** Does it read naturally aloud?

**The read-aloud test:**
- Read the piece aloud (or use text-to-speech)
- Mark every place you stumble
- Note where you'd naturally pause vs. where punctuation forces pauses
- Identify sentences that feel too long or choppy

**Hemingway Principles:**
- Emphasize nouns
- Choose active verbs
- Adjectives: few but apt
- Short sentences by default
- Long sentences ONLY for: speeding action, describing flow, making short sentences pop

**Actions:**
- Break sentences where you ran out of breath
- Combine choppy sentences that flow together
- Add rhythm variation (short punch, longer exploration)
- Fix awkward transitions
- Smooth unnatural phrasing
- Convert passive to active where possible
- Replace abstract with specific

### Pass 6: Final Authenticity Check

**Focus:** The ultimate test

**Ask yourself:**
"Would someone who knows me recognize this as mine before seeing my name?"

**If no:**
- What's missing? Add it.
- What's wrong? Fix it.
- What's generic? Make it specific.

**If yes:**
- You're done. Ship it.

---

## Output Format

For edited content, provide:

```markdown
## Edited Content

[Full edited content here]

---

## Edit Summary

**Passes completed:** 6/6
**Estimated edit percentage:** [X]%
**Voice match confidence:** [Low/Medium/High]

### Major Changes
1. [Most significant change and why]
2. [Second major change]
3. [Third major change]

### Slop Removed
- [List of AI patterns found and removed]

### Voice Elements Added
- [List of voice-specific additions]

### Remaining Concerns
- [Any areas that still feel off]
- [Suggestions for further refinement]

### VOICE.md Update Suggestions
- [Patterns discovered that should be added to voice profile]
- [Phrases that worked well — consider adding to "use freely" list]
```

---

See [`references/common-problems.md`](references/common-problems.md) for diagnosis and fix guides: too formal, too uniform, too hedged, too balanced, voice drift.

---

## Integration

**Before voice-editor:**
- Run `voice-analyzer` to create VOICE.md (if none exists)

**After voice-editor:**
- Update VOICE.md with new patterns discovered

**Quick workflow (already clean content):**
```
[Draft] → voice-editor (light mode) → [Final]
```

**Heavy workflow (generic AI output):**
```
```

---

## Success Criteria

Editing is complete when:
- [ ] All applicable passes have been applied
- [ ] No Tier 1 slop phrases remain
- [ ] Sentence length varies naturally
- [ ] Content matches VOICE.md characteristics
- [ ] Read-aloud test passes (no stumbling)
- [ ] The authenticity question is answered "yes"
- [ ] Edit summary documents all changes
- [ ] VOICE.md update suggestions provided if patterns discovered

**The ultimate test:** Would someone who knows the author recognize this as theirs before seeing the name?

---

## Core Principle

The style guide gives AI direction — it helps produce output closer to your voice than generic defaults. Your editing gives the work your actual voice — the quirks, opinions, personality, and rough edges that make it distinctively yours.

This is why "zero effort" AI fails. The promise of finished content without touching it misunderstands what makes writing valuable. Effort isn't the enemy. Wasted effort is.

You're redirecting effort from blank-page generation to voice-preservation editing. That redirection is the entire point.
