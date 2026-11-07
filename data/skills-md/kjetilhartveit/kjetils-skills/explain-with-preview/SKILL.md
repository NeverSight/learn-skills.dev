---
name: explain-with-preview
description: Use when asked to explain visually with a preview.
---

# Explain with Preview

A two-column chapter: a short framing sentence and a few clickable cards on the left, and a sticky panel on the
right that switches when the reader picks a card. Switching back and forth makes the differences obvious.

## Use this skill when

- The user asks for a visual explanation of changes with a preview.
- Used by an orchestrator to explain changes visually with a preview.

## Two modes

| Mode               | Cards                                                      | Starts on              |
| ------------------ | ---------------------------------------------------------- | ---------------------- |
| Options (decision) | One per option, 2–3, including a cautious / low-risk one   | The recommended option |
| Before / after     | Exactly two: "Before · today" and "After · with the change" | After (`"selected"`)   |

## Content

- Every option has the **same rows** in the same order so only the differences change: for a decision usually
  Keeps (`ok`), Loses (`removed`), Fix first (`decision`, concrete actions), Risks (`risk`), plus `effort`
  (hours or days, and what the work is). 2–4 short items per row, real names and numbers from the facts:
  every finding that matters for that option belongs in one of its rows.
- Fragility, dependencies and complexity belong in these rows (e.g. "Fix first: port 3 path checks into the local
  plugin"), not in chapters of their own.
- Gloss a tool or term in the row where it first appears ("nursery (Biome's unstable rules)").
- `code` (optional per option): ≤ 8 real lines of the config or code that option adds or changes, with its file
  path. Give the recommended option one when the change is config or code.
- `flip`: what would change the recommendation (1–3 items). `details`: "How it was measured" (the commands,
  versions, machine, single or repeated runs, what was not measured) and "Sources" (links).
- Use real content. Label an illustration as one.

## Build it from JSON

Write the chapter as JSON and generate the fragment; no HTML, CSS or script by hand:

```bash
python <explainer-kit>/assets/preview.py decide.json --out frag-decide.html
```

The JSON shape is documented at the top of `preview.py` and in the kit's `FRAGMENT-CONTRACT.md` ("Preview
chapters from JSON"). Text fields may contain inline `<b>`, `<code>` and `<a href>`.
