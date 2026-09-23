---
name: talking-head-image-overlays
description: >-
  Edit a talking-head video in the "uncut take + stacked image overlays" style:
  ONE continuous take that is never cut, with the entire sense of pace carried
  by hard-cut overlays landing on content nouns — a short serif title plate,
  found-footage rectangles above the eyeline, opaque full-frame skeleton-UI
  cards, raw prompt text on black, word-by-word karaoke captions, and a CTA
  banner that arrives early and never leaves. Use when someone says "edit this
  like that reel where images pop up while he talks", "add image overlays to my
  talking head", "make the cards that build themselves", "that style where a
  graphic appears on every keyword", "uncut talking head with graphics", or
  hands over a reference reel in this style. Also use to add a single act of it
  (just the cards, just the inserts) to existing footage. NOT for plain
  subtitles (embedded-captions), a banner + karaoke reel (reel-recut), unbranded
  overlay cards on untouched footage (talking-head-recut), or a fully branded
  motion-graphics ad (branded-ad-edit).
---

# talking-head-image-overlays

A style where **the footage is never cut and every visual change is a composite.**
One continuous talking-head take runs the whole video; overlays hard-cut in and
out on the nouns the speaker says. Retention comes from information changing,
not from shots changing.

Reverse-engineered by pixel measurement from a reference reel in this style and
proven end to end on unrelated footage. The full measured spec is
**[references/style-system.md](references/style-system.md)**; the build pipeline
is **[references/method.md](references/method.md)**. This file is the map.

## The four acts

Overlay structure is not uniform across the runtime. It moves through four acts,
and getting the act boundaries right matters more than any single graphic.

| Act | Share of runtime | Overlay kind | Face covered? |
|---|---|---|---|
| 1 — Title plate | first ~3 % | serif title + small pill | no |
| 2 — Found footage | next ~20 % | recycled clips, memes, stills | no, parked above the eyeline |
| 3 — Designed cards | the body, ~65 % | skeleton-UI cards, prompt-on-black | **yes, completely** |
| 4 — CTA | last ~8 % | one banner, nothing else | no |

The serif face appears **exactly twice** — the opening plate and the closing
banner. The top band is bare for everything in between. A persistent banner
across the body is the single most common way to get this style wrong.

## The five load-bearing rules

1. **Never cut the footage.** Zero camera cuts. Everything is composited over
   one take. If you silence-cut the base to the bone you destroy the format.
2. **Hard-cut every container.** Cards and images appear at full opacity in one
   frame. No fades, no scale-ins, no slides, ever, at container level.
   *Interiors* animate; containers never do.
3. **Land on the noun.** A container cuts in within ±0.2 s of the onset of the
   word it depicts. Never on a function word.
4. **Empty skeletons, not real text.** Every string inside a card is a grey bar.
   The card carries the *shape* of a system without asking anyone to read.
5. **Ship no audio assets.** No music bed, no SFX — not even on overlay cuts.
   This is measured, not stylistic preference.

## Pipeline

```
reference reel (optional) + talking-head footage
        │
        ▼
[1] deconstruct the reference  (only if one was given)
      ffmpeg forensics → contact sheets → parallel vision passes → style-system
      (reel-style-clone owns the general version of this; this skill's
       references/style-system.md IS the finished output for THIS style)
        │
        ▼
[2] base cut — the inverted-pacing step
      target ~15 % retained silence, median gap ~0.32 s, breaths left in.
      Cap each pause rather than removing it. See method.md §2.
        │
        ▼
[3] derive the overlay band FROM THIS FOOTAGE
      scripts/measure-face-band.py → cap-top and eye-line distributions
      → EYE_FLOOR and HEAD_FLOOR. Never copy the reference's y-values.
        │
        ▼
[4] storyboard against measured word onsets
      one card per concept noun; inserts on concrete nouns; CTA on the first
      outro verb (NOT on the keyword)
        │
        ▼
[5] build  (HyperFrames composition; see method.md §5 for the component kit)
        │
        ▼
[6] QA on the RENDERED file → master to -14.5 LUFS → deliver on a review canvas
```

## The two decisions to raise before building

**1. The cards cover the face.** In the reference they are opaque and 80 % of
frame in both axes — the speaker disappears for about a third of the runtime.
If the creator has a no-face-covering rule, or a "no full-screen takeover" rule,
this style conflicts with it head-on and you must get an explicit call. The
fallback is Act 3 cards inset into the band above the eyeline, which costs most
of the card's impact; say so rather than quietly shrinking them.

**2. The reference has no face-avoidance logic at all.** Its rects are absolutely
positioned while the speaker moves, so the same rect clears the brow in one shot
and cuts through the eyebrows in another. Do not reproduce that. Derive the floor
from the *minimum* eye line across the whole take (step 3).

## Costs and dependencies

- ffmpeg/ffprobe, a word-level transcriber, and a HyperFrames toolchain.
- No generation APIs are required. This style uses **recycled** footage, not
  generated B-roll — if you reach for a generation lane you have left the style.
- If a reference reel is on a platform, the user must supply the file or their
  own authenticated session; anonymous downloads get a login wall.
