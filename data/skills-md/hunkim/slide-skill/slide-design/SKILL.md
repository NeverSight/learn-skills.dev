---
name: slide-design
description: Rules for building presentation slides that people can actually read — applies Alexei Kapterev's "Death by PowerPoint" principles plus a working checklist. Use whenever making or revising slides, decks, presentations, pitch decks, or HTML slide decks, in any format (.pptx, HTML, PDF). Triggers on "슬라이드", "발표자료", "덱", "deck", "slides", "presentation", "pitch deck", or when a slide comes back as "too complex / 복잡해".
---

# Slide design

## The one rule

**One point per slide.** If a slide is making two points, it is two slides.
An extra slide costs $0.00 — splitting is always cheaper than cramming.

Before building any slide, write its single point as one sentence.
If you can't, you don't know what the slide is for yet. Everything that
does not serve that sentence gets deleted.

## Death by PowerPoint — the principles

From Alexei Kapterev's deck (~5M views), the four failure modes are
**significance, structure, simplicity, rehearsal**. Three of them are ours:

**Significance** — why does this slide exist? "Significance creates passion;
passion attracts attention; attention leads to action." A slide that only
transfers information is a handout, not a slide.

**Structure** — give 3–4 reasons, never more. *"They will not remember more
anyway."* Common shapes: Problem → Pathway → Solution, or Problem → Solution
→ Reasoning. The deck should survive being told in 5 minutes or 45.

**Simplicity** — "Everything should be made as simple as possible, but not
simpler."
- Less text. More imagery.
- Few matching colours. Very few fonts.
- Photos, not clipart.
- **"People read faster than you speak. This means you are useless."**
  Dense text on a slide makes the presenter redundant.
- Reject mechanical rules like "7 lines × 7 words" — they produce cramped,
  boring slides. The real test is whether one idea lands in 3 seconds.

**Do not use slides as** a prompter, a handout, or a data dump. If detail is
required, ship two artifacts: visual slides + a separate document with the
detail. Never one file trying to be both.

## What this means in practice

| Instead of | Do |
|---|---|
| A 6×5 table of who passed which round | A funnel of shrinking dots with the survivor highlighted |
| A bullet list of five benefits | Five rows, one bold noun each, one line of support |
| Two charts + notes + a table | Three slides |
| A paragraph as the subtitle | One sentence, ≤ 20 words |
| Explaining the mechanism in text | Draw the mechanism |

**Read the slide from 3 metres away.** If the point isn't obvious before you
read any body copy, the layout is wrong — not the copy.

**Redundancy is clutter.** If the headline says it, the label doesn't need to.
If the next slide covers it, this slide doesn't.

**Detail goes to the footnote.** Sources, caveats, secondary names, exact
dates: one small grey line at the bottom. Present but not competing.

## Checklist before shipping a slide

1. Can I state the slide's point in one sentence? Is that sentence on the slide?
2. Is anything here making a *second* point? → split the slide.
3. Is any element repeating what another element already says? → delete it.
4. Would a picture of the mechanism beat this text? → draw it.
5. Does anything only matter to 5% of the audience? → footnote it.
6. From 3 metres: what do I see first? Is that the point?

## When the feedback is "too complex"

Do not shrink the font or tighten the spacing. Remove content. Pick the single
sentence, delete everything that isn't it, and give the survivor more room.
Move what you deleted to a footnote, to a second slide, or to the appendix.

## Building HTML decks

- Fixed 1280×720 stage, `transform: scale()` to fit the viewport.
- One design system across all slides: kicker → headline → one-line sub → body.
  Same paddings, same type scale, same accent colour everywhere.
- Commit to one background tone for the whole deck. Do not mix dark and light
  slides unless the switch is doing deliberate work (title / section only).
- Animation is sequencing, not decoration: entrance order should follow the
  order you speak in. Quiet slide transitions — a fast fade, nothing 3D.
- Rebuild charts natively (SVG) rather than pasting screenshots, so they can
  animate and stay legible. Screenshots are fine when the screenshot *is*
  the evidence (a leaderboard, a news card).
- No HTML-in-Canvas.
- Self-contained single file: inline CSS/JS, images as base64 data URIs.
- Hide presenter chrome in fullscreen.
- Verify with Playwright: screenshot every slide, check for 0 JS errors,
  0 blank slides, and no element whose `scrollHeight/scrollWidth` exceeds its
  container (measure only the active slide — entrance transforms create false
  positives on inactive ones).

## Source

Alexei Kapterev, *Death by PowerPoint* — https://www.slideshare.net/slideshow/death-by-powerpoint/85551
