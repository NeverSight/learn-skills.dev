---
name: de-slop
description: "Remove LLM-isms and AI writing patterns from text. This skill should be used when editing prose to sound less like AI output — removing overused words, fixing structural tells, and restoring natural human voice. Triggers: \"de-slop\", \"remove AI writing\", \"humanize this\", \"sounds too AI\", \"LLM-isms\", \"AI slop\", or when reviewing text that reads like chatbot output."
license: MIT
metadata:
  author: petekp
  version: "0.1.0"
---

# De-Slop

Strip AI writing patterns from text to restore natural, human-sounding prose.

Based on [Wikipedia: Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and [WikiProject AI Cleanup](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_AI_Cleanup).

## When to Use

- Editing any prose that sounds like chatbot output
- Reviewing drafts generated with AI assistance
- Self-check before publishing AI-assisted writing
- When text feels "off" but the reason is hard to pinpoint

## Process

### Step 1: Diagnose

Read the full text before changing anything. Load `references/word-list.md` and `references/structural-patterns.md` to identify which patterns are present.

Categorize findings into three severity levels:

**Red — Immediate tells** (fix first)
- Chatbot leakage ("I hope this helps", "Certainly!", template blanks)
- Grandiose filler ("stands as a testament", "in today's fast-paced world")
- Synonym cycling (same entity referred to by 4+ different names)

**Yellow — Statistical signals** (fix in clusters)
- 3+ words from the overused word list appearing in close proximity
- Rule of three used more than twice
- Tailing participle phrases ("emphasizing the significance of")
- Em-dash density higher than ~1 per 200 words

**Green — Structural patterns** (require rewriting, not word swaps)
- Relentless balance (every section same length)
- Uniform register (no tonal variation)
- Generic specificity (hypothetical examples, no real names)
- Excessive hedging (qualifiers every third sentence)
- Risk aversion (no specific claims, no edge)

Present the diagnosis as a brief summary before making changes. Example:

```
Diagnosis: 4 red flags (chatbot leakage, grandiose filler), 7 yellow signals
(word clusters in paragraphs 2, 5, 8), 2 green patterns (relentless balance,
uniform register).
```

### Step 2: Fix Red Flags

Remove or replace all Red items. These are unambiguous AI artifacts.

**Chatbot leakage:** Delete entirely.

**Grandiose filler:** Replace with plain statements or delete.
- "stands as a testament to" -> "shows" or "is"
- "plays a vital role in shaping" -> "shapes" or "affects"
- "in today's fast-paced world" -> delete (it never adds meaning)

**Synonym cycling:** Pick one term and stick with it. Use pronouns for variety.

### Step 3: Fix Yellow Signals

Work through clusters. The goal is not to ban specific words but to break up detectable patterns.

**Word clusters:** Replace overused words with plain alternatives.
- "delve into" -> "look at" / "examine" / (often just delete)
- "leverage" -> "use"
- "robust" -> "strong" / "solid" / (ask: is this adjective needed at all?)
- "nuanced" -> "detailed" / "complicated" / (often delete)
- "landscape" -> name the actual domain
- "multifaceted" -> drop it; describe the actual facets instead
- "crucial" / "pivotal" / "paramount" -> "important" or delete

**Copula avoidance:** Restore simple verbs.
- "serves as" -> "is"
- "features" / "offers" / "boasts" -> "has"

**Transition abuse:** Remove mechanical connectives.
- "Moreover," / "Furthermore," / "In addition," -> start the sentence without them, or use "and" / "also"

**Rule of three:** Break at least half of them. Use two items, or four, or one.

**Tailing participles:** Rewrite as separate sentences or delete.
- "..., emphasizing the importance of X" -> delete, or: "X matters because..."

### Step 4: Fix Green Patterns

These require actual rewriting, not substitution.

**Relentless balance:** Redistribute weight. Expand important sections. Trim or collapse unimportant ones. A 3-sentence paragraph next to a 12-sentence paragraph is fine.

**Uniform register:** Inject tonal shifts. A blunt short sentence after a complex one. A casual aside in a technical passage. Let the writing breathe.

**Generic specificity:** Replace hypothetical examples with real ones, or remove examples that add nothing.

**Excessive hedging:** Remove qualifiers that don't reflect genuine uncertainty. If something is true, state it without "often" / "generally" / "can be."

**Risk aversion:** Sharpen claims. Add an opinion. Allow an imperfect sentence to stand if it has energy.

**Enthusiasm gap:** Vary paragraph investment. Spend more words where the writer (or subject) is more interesting.

### Step 5: Final Read

Read the entire edited text once more. Check for:

1. **Overcorrection** — Did fixes make the text choppy or too informal? Restore where needed.
2. **Meaning preservation** — Does every sentence still say what it originally meant?
3. **New patterns** — Did edits introduce their own repetitive patterns?
4. **Voice consistency** — Does the text sound like one person wrote it?

## Principles

- **Prefer plain words.** "Use" over "leverage." "Is" over "serves as." "Important" over "crucial."
- **Prefer short sentences.** Break long compounds. Not every thought needs a clause.
- **Preserve meaning.** Never change what the text says, only how it says it.
- **Don't over-correct.** Some em dashes are fine. An occasional "furthermore" is fine. The goal is to break patterns, not ban words.
- **Real > hypothetical.** A named example beats "consider a scenario where..."
- **Uneven > balanced.** Spend more words on what matters more.
- **Specific > vague.** "Response time dropped from 200ms to 50ms" beats "significantly improved performance."
