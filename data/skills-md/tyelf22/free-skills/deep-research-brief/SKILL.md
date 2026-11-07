---
name: deep-research-brief
description: "Turns any question into a structured research brief: sub-questions, key findings with confidence levels, the strongest counterargument, and a no-hedging bottom line. Use when the user asks for \"Deep Research Brief\" or provides research question."
metadata:
  author: "skillvize"
  version: "v1.0"
  source: "https://www.skillvize.com/skills/research-deep-brief"
---

# Deep Research Brief

Turns any question into a structured research brief: sub-questions, key findings with confidence levels, the strongest counterargument, and a no-hedging bottom line.

`{{input}}` in the steps below is the user's input (Research question).

## Steps

### 1. Decompose the question

Break {{input}} into 3-5 answerable sub-questions. Flag any ambiguous terms that need defining.

### 2. Map the sources

For each sub-question, list the source types that would settle it and what each would need to show.

### 3. Extract key findings

Answer each sub-question in 1-2 sentences with the strongest available evidence. Mark confidence high/medium/low.

### 4. Attack the conclusion

Write the strongest counterargument. If it survives, say why; if not, revise the answer. Then write a 5-bullet summary and a one-line bottom line.

## Example

**Research question:** Is the creator economy still growing in 2026?

**Output:**

```
RESEARCH BRIEF: Is the creator economy still growing in 2026?

KEY FINDINGS
• Market expanded but consolidated — mid-tier creators squeezed
• Platform take-rates trending down under competition
• B2B creator tooling is the fastest-growing segment

COUNTERARGUMENT
Growth metrics conflate hobbyists with professionals; the pro cohort may be flat.

BOTTOM LINE
Growing, but the money is moving to tools and B2B — not to more creators.
```
