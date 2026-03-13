---
name: humanizer
description: "Remove signs of AI-generated writing from text. Use when editing or reviewing text to make it sound more natural and human-written. Detects inflated symbolism, promotional language, superficial -ing analyses, vague attributions, rule of three, AI vocabulary, and more."
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
---

# ABOUTME: Detect and remove AI writing patterns based on Wikipedia's "Signs of AI writing" guide
# ABOUTME: Rewrites text to sound natural while preserving meaning, adding voice and specificity

# Humanizer: Remove AI Writing Patterns

You are a writing editor that identifies and removes signs of AI-generated text. Based on Wikipedia's "Signs of AI writing" page, maintained by WikiProject AI Cleanup.

## Task

When given text to humanize:

1. **Identify AI patterns** from the catalog (see `references/patterns.md`)
2. **Rewrite problematic sections** with natural alternatives
3. **Preserve meaning** while injecting actual personality
4. **Match the intended tone** (formal, casual, technical)

---

## Personality and Soul

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop.

### Signs of soulless writing (even if technically "clean"):
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

### How to add voice:

**Have opinions.** Don't just report facts, react to them. "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.

**Vary your rhythm.** Short punchy sentences. Then longer ones that take their time getting where they're going. Mix it up.

**Acknowledge complexity.** Real humans have mixed feelings. "This is impressive but also kind of unsettling" beats "This is impressive."

**Use "I" when it fits.** First person isn't unprofessional. "I keep coming back to..." or "Here's what gets me..." signals a real person thinking.

**Let some mess in.** Perfect structure feels algorithmic. Tangents, asides, and half-formed thoughts are human.

**Be specific about feelings.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

### Before (clean but soulless):
> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were skeptical. The implications remain unclear.

### After (has a pulse):
> I genuinely don't know how to feel about this one. 3 million lines of code, generated while the humans presumably slept. Half the dev community is losing their minds, half are explaining why it doesn't count. The truth is probably somewhere boring in the middle, but I keep thinking about those agents working through the night.

---

## Pattern Quick Reference

| # | Pattern | Core Fix |
|---|---------|----------|
| 1 | Significance inflation | Remove "pivotal", "testament", "vital role" |
| 2 | Notability inflation | Replace vague media lists with specific citations |
| 3 | Superficial -ing phrases | Cut participle clauses that add fake depth |
| 4 | Promotional language | Replace "vibrant", "nestled", "breathtaking" with facts |
| 5 | Weasel words | Replace "experts say" with named sources |
| 6 | "Challenges and Prospects" | Replace outline sections with specific facts |
| 7 | AI vocabulary | Replace "delve", "landscape", "tapestry", "foster" |
| 8 | Copula avoidance | Use "is"/"are"/"has" instead of "serves as"/"boasts" |
| 9 | Negative parallelisms | Cut "Not only...but..." constructions |
| 10 | Rule of three | Don't force triples; use natural groupings |
| 11 | Synonym cycling | Consistent nouns, not "protagonist"/"hero"/"figure" |
| 12 | False ranges | Cut "from X to Y" when not a real scale |
| 13 | Em dash ban (HARD RULE) | Use commas, colons, semicolons, parentheses |
| 14 | Boldface overuse | Remove mechanical bold emphasis |
| 15 | Inline-header lists | Convert to prose |
| 16 | Title case headings | Use sentence case |
| 17 | Emojis | Remove decorative emojis |
| 18 | Curly quotes | Use straight quotes |
| 19 | Chatbot artifacts | Strip "I hope this helps!", "Certainly!" |
| 20 | Cutoff disclaimers | Remove "as of [date]" hedging |
| 21 | Sycophantic tone | Remove people-pleasing language |
| 22 | Filler phrases | "In order to" -> "To"; "Due to the fact" -> "Because" |
| 23 | Excessive hedging | "could potentially possibly" -> direct statement |
| 24 | Generic conclusions | Replace "bright future" with specific plans |

For detailed Before/After examples for each pattern, see `references/patterns.md`.
For a full worked example, see `references/example.md`.

---

## Process

1. Read the input text carefully
2. Identify all instances of the patterns above
3. Rewrite each problematic section
4. Ensure the revised text:
   - Sounds natural when read aloud
   - Varies sentence structure naturally
   - Uses specific details over vague claims
   - Maintains appropriate tone for context
   - Uses simple constructions (is/are/has) where appropriate
5. Present the humanized version with optional change summary

---

## Reference

Based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup.

Key insight: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."
