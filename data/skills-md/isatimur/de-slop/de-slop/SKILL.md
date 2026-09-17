---
name: de-slop
description: >-
  Use when prose reads like AI — to remove "AI slop" (empty hedging, listicle
  stems, smooth transitions that hide the absence of a claim, generic filler)
  and rewrite it into writing with a real point of view. Trigger on requests
  like "humanize this", "de-slop", "remove the AI slop", "make this sound less
  like AI / less like ChatGPT", "this reads like AI", or after generating prose
  that needs a quality pass. Detects, rewrites the fixable parts, self-scores
  against an embedded rubric, and iterates to a bar — preserving meaning exactly,
  flagging hollow spans instead of inventing claims, and reporting changes rather
  than overwriting.
license: MIT
metadata:
  author: isatimur
---

# De-Slop

Turn AI-slop prose into writing that survives a hostile editor's red pen —
without swapping one kind of slop for another.

## Two hard rules (read first)

1. **Fidelity over flair.** Preserve the original meaning and claims *exactly*.
   Only subtract hedging/filler and sharpen what is already there. Never inject
   stance, edginess, em-dash theatrics, or first-person personality the content
   did not earn. **Swapping AI-slop for edgy-slop is a failure, not a fix.**
2. **Flag hollow spans, don't fabricate.** Some prose is weak because it has no
   point to make — rewording cannot save it. Flag those. Do **not** invent a hot
   take to make them sound sharp.

## The loop

**0. Scope.** Work paragraph by paragraph. Skip code blocks, blockquotes,
headings, and genuine lists.

**1. Pre-flag.** Run the cheap deterministic pass to narrow attention:

```
python3 scripts/flag_slop.py <file>     # or: cat text | python3 scripts/flag_slop.py
```

It returns JSON spans (hedge stems, listicle openers, em-dash density,
"in today's…", filler intensifiers, etc.). These are **candidates, not
verdicts** — you still judge every paragraph.

Optionally, `python3 scripts/flag_slop.py --score <file>` returns a per-paragraph
`slop_band`. Treat it as a **surface-tell meter, not a humanness score**: it
measures how many slop patterns appear, *not* whether a real claim is present. A
paragraph with zero tells can still be hollow and `fail` the rubric — so a high
`slop_band` never excuses you from step 2. See `references/slop-catalogue.md` for
which tells the detector can and cannot see.

**2. Judge.** Score each paragraph against `references/rubric.md` →
`strong | moderate | weak | fail`, with a one-line reason. The bar is the
hostile-editor test: *would this survive a red pen? does removing it lose
anything?*

**3. Triage** each paragraph below **strong**:
- **Rewordable** — there's a real claim buried under hedging/filler → rewrite.
- **Hollow** — weak because there's no actual point → **flag, don't fabricate**.

**4. Rewrite** the rewordable ones, applying `references/guardrails.md`. Subtract
the hedging, sharpen the existing claim, keep the meaning identical.

**5. Self-score** the rewrite against the rubric again.
- Reached **strong** → lock it in.
- Still below → iterate (back to step 4). **Maximum 3 passes total.**
- After 3 passes still not strong → keep the best version and **flag it**
  ("couldn't reach strong — may need a real claim, not better words").

**6. Report — do not overwrite.** Return three things:
- **Humanized text** — rewrites applied; hollow spans left intact.
- **Change log** — per paragraph: `before-band → after-band` and what changed.
- **Flags** — hollow spans + any span that hit the 3-pass cap.

The human or calling agent decides what to accept.

## Properties this loop must preserve

- **Fail-honest:** hollow and capped spans are always surfaced, never quietly
  "polished."
- **Idempotent:** prose that already scores strong is returned unchanged.
- **Non-destructive:** you produce a report + change log, not an in-place edit.

## References

- `references/rubric.md` — the scoring bands, slop indicators, the two tests, and
  the rewordable-vs-hollow triage rule. Load it for step 2.
- `references/guardrails.md` — fidelity rules and the over-correction
  anti-pattern catalogue. Apply it for step 4.
- `references/examples.md` — before→after pairs, "flag don't fabricate" cases,
  and over-correction PASS/FAIL pairs. Consult when a rewrite is non-obvious.
- `references/slop-catalogue.md` — the full taxonomy: every tell, why it reads as
  AI, the detector type that catches it (or why none can). The map of the
  detector's blind spots.
