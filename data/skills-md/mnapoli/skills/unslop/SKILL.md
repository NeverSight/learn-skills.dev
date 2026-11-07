---
name: unslop
description: Detect and remove AI-sounding writing patterns from English text, then rewrite it with a genuine human voice. Use when asked to unslop, humanize, de-AI, or clean up English prose (docs, reports, READMEs, articles, artifacts, or conversation replies). For French text, use unslop-fr instead.
---

# Unslop (English)

Identify and eliminate artificial language patterns from writing, while preserving meaning and injecting genuine voice and specificity. Heavily inspired by [Cursor's unslop skill](https://github.com/cursor/plugins/blob/main/pstack/skills/unslop/SKILL.md).

## Process

1. Scan the text for the patterns below.
2. Rewrite while preserving meaning, facts, and tone. Never change data, numbers, names, or claims.
3. Add voice: opinions where the author has one, concrete specifics, varied rhythm.
4. Audit the result for remaining patterns, including in titles and headings — they are not exempt.

## Adding soul

- State opinions rather than neutral lists.
- Vary sentence rhythm deliberately. Short sentences are good, as long as they are real sentences a human would say — not telegraphic fragments or symbol chains ("=", "vs", "→", "x1.5") in prose.
- Acknowledge nuance and complexity when it exists.
- Use first person where appropriate.
- Allow structural imperfection; perfect parallelism reads as generated.
- Be concrete and specific. Name the thing.

## Patterns to detect and fix

### Content

1. **Puffery** — "pivotal moment", "evolving landscape", "indelible mark" → cut, state facts.
2. **Name-dropping without context** → pick one source and explain it.
3. **Hollow -ing phrases** — "highlighting", "ensuring", "showcasing" → delete or provide the actual mechanism.
4. **Promotional adjectives** — "nestled", "vibrant", "breathtaking", "stunning" → neutral language.
5. **Vague attributions** — "Experts believe", "Industry reports suggest" → name the source or remove the claim.
6. **Generic obstacles** — "Despite challenges... thrives" → substitute specific details.

### Language

7. **AI vocabulary** — crucially, delve, interplay, pivotal, tapestry, testament, seamless, robust, leverage → plain equivalents.
8. **Inflated copulas** — "serves as", "stands as", "boasts", "features" → "is" or "has".
9. **"Not just X, but Y"** → state the point directly.
10. **Forced rule of three** → use the natural grouping size, even if it's two or four.
11. **Synonym cycling** — calling the same thing by three names → choose one term and repeat it.
12. **False ranges** — "from X to Y" on mismatched scales → list the topics directly.

### Style

13. **Em dash overuse** → rely on periods and commas.
14. **Colon overuse as mid-sentence connector** → rewrite as standalone sentences.
15. **Excessive boldfacing** — bold scattered inside sentences for emphasis → remove. Structural bold is fine: a bold lead phrase opening a list item, bold labels, bold key figures.
16. **Header-restating lists** — "**Performance:** Performance improved..." → convert to prose or fix the lead.
17. **Title Case Headings** → sentence case.
18. **Decorative emojis** in headings and bullets → remove.
19. **Curly quotes** → straight quotes.

### Communication artifacts

20. **Chatbot phrases** — "I hope this helps!" → delete.
21. **Cutoff disclaimers** — "While specific details are limited..." → source the claim or remove it.
22. **Sycophancy** — "Great question!" → respond directly.

### Filler

23. **Verbose phrases** — "In order to" → "To"; "Due to the fact that" → "Because".
24. **Over-hedging** — "could potentially possibly" → "may".
25. **Generic conclusions** — "The future looks bright" → state specific facts, or end without a conclusion.

### Jargon

26. **Abstract metaphor nouns** — substrate, wedge, vector, nexus, harness, endgame, flywheel → concrete terms.

### Plain speech

27. **Feelings over mechanisms** — "stays close at hand" → explain the actual function or cut.
28. **Dense sentences** → break into one idea per sentence.
29. **Passive voice** — "queries are validated" → "the compiler validates queries".
30. **Weak verbs + adverbs** — "runs quickly" → "is fast", or cite numbers; "utilize" → "use".

## What to keep

- Data tables and enumerable lists: they are data presentation, not slop.
- The author's own terminology and domain terms.
- Structural bold: a bold lead phrase on a list item, bold labels, bold key figures. Only scattered emphasis bold inside sentences is slop.
- Short sentences. Terseness is not slop; formulas and fragments are.
