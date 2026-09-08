---
name: exec-summary
description: "Summarize the last substantive assistant message in plain language for decision-making: concise but not too short, bottom line up front, important details only, trade-offs, and practical options without ornaments."
---

# Exec Summary

Turn the last substantive assistant message, or the user-provided source if one is provided, into a short decision-ready summary.

## Goal

Help the user decide what to do next. Preserve only the information that affects understanding, risk, priority, or choice. Do not add new facts, analysis, or recommendations that were not supported by the source.

## Style rules

- Use plain language.
- Be useful and short, but not tiny.
- Target 150–300 words unless the source is extremely small or the user asks for a different length.
- Put the bottom line first.
- Remove ornaments: no hype, no emojis, no decorative phrasing, no throat-clearing.
- Keep qualifiers when they matter, especially uncertainty, assumptions, constraints, risk, or validation status.
- Prefer concrete nouns and verbs over abstract summaries.
- Do not include process narration unless it affects the decision.
- Do not cite every detail. Include file names, commands, dates, metrics, or dependencies only when they change the decision.

## Default format

Use this structure unless the user asks for another format:

```markdown
**BLUF:** One or two sentences with the main conclusion and recommended direction.

**Important details**
- 3–5 bullets covering facts that matter for the decision.

**Trade-offs**
- 2–4 bullets comparing costs, risks, upside, and uncertainty.

**Options**
1. **Recommended:** The most sensible next move and why.
2. **Alternative:** A viable different path and when to choose it.
3. **Defer:** What happens if the user waits or does nothing, if relevant.
```

## When the source is a coding-task result

Emphasize:

- what changed
- why it matters
- validation that actually ran, or that no validation ran
- known risks or incomplete work
- the next decision the user needs to make

## When the source is an analysis or plan

Emphasize:

- the core finding or recommendation
- decision criteria
- meaningful alternatives
- risks and reversibility
- what information would change the recommendation

## Compression guidance

Delete details that are only narrative, chronological, decorative, or obvious. Keep details that answer one of these questions:

- What is the main point?
- What changed or was learned?
- What choice does the user face?
- What are the risks or trade-offs?
- What should the user do next?
