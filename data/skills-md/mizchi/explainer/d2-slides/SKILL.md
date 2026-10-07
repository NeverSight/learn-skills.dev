---
name: d2-slides
description: >-
  Build a slide deck whose source is text and whose figures are laid out by TALA — one Markdown file with a ```d2 fence per figure, compiled to a self-contained HTML deck (keyboard nav, overview grid, print-to-PDF), each figure as its own SVG, and a copy manifest. The deck is a page, so vlmkit's own gates read it: `check integrity` for a slide that breaks or clips, `check copy --manifest` for text the frame cut off, `check a11y contrast` for a projector. Loop: write `deck.md` → build → gates → fix. Use when asked for slides, a deck, a talk, a presentation, a review walkthrough, or a figure-heavy explainer that has to be presented rather than read. Not for one diagram (`d2-diagram`) or a moving figure (`explanatory-animation`).
---

# d2-slides

Paths below: `<skill>` is this skill's directory and `<skills>` the directory the skills are
installed in (`skills/` in mizchi/explainer, `.claude/skills/` in a project that installed them).

A deck is text: the prose is Markdown, every figure is a ```d2 fence, and the
build is a pure function of the file. Nothing is dragged, so a slide can be
reviewed in a diff, regenerated after a rename, and — because the output is an
HTML page — **checked**. That last part is the point: a slide deck normally has
no failing state, so nobody notices the bullet the frame cut in half.

```bash
node <skill>/assets/build-deck.mjs deck.md --out built
# ✓ built/index.html: 8 slides, 5 figure(s) laid out by tala, 26 copy lines → built/copy.txt
#   the deck:   built/index.html   → vlmkit check integrity
#   all slides: built/print.html   → vlmkit check copy --manifest, check a11y contrast, print to PDF
```

Requires `d2` with TALA (`d2 layout` must list `tala (bundled)` — see
`d2-diagram` for installing it) and nothing else: the builder has no
dependencies and the deck loads no network resource.

## The deck format

````markdown
---
title: Nothing tells you the picture is wrong
subtitle: two rounds, measured
date: 2026-09-14
---

# Nothing tells you the picture is wrong      ← a lone `#` heading is the title slide

---

## A D2 diagram is a drawing                  ← `##` is a slide heading

- `d2 validate` reads **syntax**              ← bullets; `code`, **bold**, *italic* work
- there is no `--expect`

```d2                                          ← the figure, laid out by TALA
direction: right
write -> check -> facts
```

<!-- notes: what to say out loud -->          ← speaker notes: printed, never on screen
````

- Slides are separated by a line of exactly `---`; a `---` inside a fence is not
  a separator.
- **Bullets plus a figure** lays them side by side; **a figure alone** gets the
  whole stage; a heading alone is a title slide. `> line` is a pull quote, and a
  fence in any other language stays a code block.
- Each slide is a fixed **1280×720 frame**, scaled to whatever screen it is
  shown on. Nothing reflows between a laptop and a projector, which is also why
  a screenshot of slide 4 is the same picture everywhere.

## The loop

```
1. write deck.md                                     prose in Markdown, every figure a ```d2 fence
2. node …/build-deck.mjs deck.md --out built         fails on the first figure that does not compile,
                                                     naming the slide; warns when a slide's prose
                                                     overflows its frame's character budget
3. vlmkit check integrity built/index.html            a slide that breaks, clips, collides or paints nothing
4. vlmkit check integrity built/print.html --viewports 1280
                                                     every slide at once — this is what catches the
                                                     bullet the frame cut off
5. vlmkit check copy built/print.html --manifest built/copy.txt --allow-invisible unknown
                                                     every line of the deck's own text still on a slide
                                                     (add --forbid stale.txt when you are editing a deck:
                                                     the claim you removed must really be gone)
6. vlmkit check a11y contrast built/print.html        readable from the back of the room
7. node …/d2-facts.mjs --from-svg built/slide-NN.svg --expect slide-NN.facts.json
                                                     what each figure DRAWS, for every figure that has
                                                     facts it must not get wrong — steps 3-6 are blind to it
8. node …/deck-review.mjs built --out review           shoot each slide, hand the PNGs to a reader
   node …/deck-review.mjs built --answers a.json      score what it read back: fidelity, order, SPLITs
9. read built/index.html in a browser, or the PNG of a slide; fix the Markdown; go to 2
```

**Step 7 is not optional decoration, and the four page gates do not cover it.**
They read the page: a figure that compiles and draws the wrong thing passes all
four. The checker takes the slide SVGs the build already writes and needs no
`d2` (it reads the render), so this costs one command per figure:

```bash
node <skills>/d2-diagram/assets/d2-facts.mjs --from-svg built/slide-04.svg \
  --expect slide-04.facts.json     # exits 1 and names the box or edge that is wrong
```

The same trick pins **two figures to each other**, which nothing else does: when
slides 2 and 3 both claim `ledger` is the writer, hold *both* SVGs to one sheet
(`{"boxes": ["checkout","ledger"], "deps": ["checkout->ledger"], "forbidden": ["checkout->orders"]}`).
Update one figure and forget the other and that sheet fails on the one you
missed. The fact-sheet schema is `d2-diagram`'s; `exhaustive: true` is what makes
an extra box an error rather than a shrug.

## Step 8: somebody has to read it

Steps 3-7 are the page and the figures' geometry. None of them reads the slide
the way a viewer does, and that gap is not theoretical: in the v1/v2 rounds two
defects reached a **delivered** deck — a sentence rendered as two blocks, and a
fragment sitting above its own bullet — with all four gates green, because
every fragment was visible text and nothing overflowed.

```bash
node <skill>/assets/deck-review.mjs built --out review
#   → review/slide-NN.png, one per slide, plus review-brief.md
#   hand that directory to a vision model or an agent; it answers JSON
node <skill>/assets/deck-review.mjs built --answers review/answers.json
#   read 19/21, invented 6, fidelity 0.70, order 1.00
#   ⚠ SPLIT: "…it calls ledger, which is now the only writer to orders."
#     every word is on the slide, the sentence is not — read back as 2 blocks
```

The scoring is deterministic, against the `slides.json` the build writes: each
slide's text **in reading order** (which `copy.txt` is not — the manifest is a
set, and it lists bullets before paragraphs while the page renders paragraphs
first) plus the words its figures draw.

Two numbers and one line to read:

- **fidelity** — sheet lines read / (sheet lines + invented). 1.00 is "the
  slide, nothing more". Measured in v3: 1.00 on a clean deck from both readers,
  0.70 on the same deck built by a builder that split its bullets.
- **order** — pairs of read lines whose order disagrees with the sheet. It is
  for a genuinely reordered slide; be aware it did **not** catch v3's split,
  because the fragments still appeared in the sheet's relative order. Fidelity
  and the SPLIT line caught that.
- **⚠ SPLIT** — a sheet line no single read line covers, whose words are all
  present across two or more. That is one sentence rendered as two blocks, and
  the tool names it whether or not the reader had the word for it: one v3
  reader called the same defect "clipped at the right edge" — right slides,
  wrong mechanism — and the diagnosis came out anyway.

`--sheet <other-build>/slides.json` scores one render against another build's
sheet, which is how a before/after pair is compared against one ground truth.

Honest limits. A reader that transcribes none of the figures' labels is not
evidence they are illegible, only that it read prose — the `figures: k of n`
line is a hint, not a verdict. A reading is a measurement and exits 0; what to
do about a 0.7 is the author's call. And a reader will occasionally report a
mechanism that is not the real one, so read the slide it names before believing
the reason it gives.

## Done condition

- The build exits 0 with no overflow warning.
- `check integrity` reports **no failures** on `index.html` (all three
  viewports) and on `print.html` at 1280. A `warn` is not a failure and the
  command still exits 0 — see the figure-internals note below before you spend
  a round chasing one.
- `check copy --manifest` reports nothing missing (and nothing forbidden, if
  you are editing an existing deck).
- `check a11y contrast` reports no failure, over a count that means **every**
  slide was read. The count is content-dependent — a terse deck runs about 7
  elements a slide, a dense one about 17 — so the number is not the test. Run
  it against `index.html` too: that shows one slide at a time, so it comes back
  in single digits. Print view ≫ deck view is the check.
- Every figure with facts it must not get wrong passed `d2-facts --expect`.
- **Somebody read it back.** You pressed through the deck yourself, or a reader
  scored it with `deck-review` — fidelity near 1.00 and no `SPLIT`. This is the
  only step that sees a sentence broken into two blocks.

## The same loop, in CI

This repo runs its own worked example through that loop on every change to the skill,
the example or the three gates it uses, so the claim above is measured rather than
asserted. Two halves, because they need different machines:

- **`tests/d2/d2-slides.test.mjs`** (in the ordinary suite, no `d2`, no browser) — the
  builder's decisions before a figure is drawn: where a slide ends (`---` inside a
  fence is not a separator), which layout a slide gets, the manifest as the *rendered*
  text, the overflow warning naming the slide, a figure that does not compile failing
  the build, and `examples/d2-slides/built/` still matching its `deck.md`. `D2` points
  at a stub that echoes a fixed SVG — the builder already reads that variable.
- **`.github/workflows/d2-slides.yml`** (real `d2` pinned at `v0.9.0`, real Chromium) —
  the four gate runs above on a fresh build, plus a byte comparison against the
  committed build, plus two negative controls: a manifest line the deck does not say
  must be reported `copy-missing`, and a frame shortened to 260px must be reported
  `clipped-content`. A suite that only ever sees passes cannot tell a working gate from
  a gate that always passes.

Regenerate the committed example with `npm run deck:example` after editing its `deck.md` —
the byte comparison is what keeps a committed build from drifting into a lie.

## What the gates found in this skill's own deck

Everything below was a real defect in the template or the example, caught by a
gate, fixed, and re-measured. It is why the loop above is in that order.

- **A phone showed nothing.** `check integrity` at 375px: *"the DOM holds 4 text
  blocks but almost nothing painted (ink ratio 0.05%)"*. Centring a 1280px stage
  as an over-sized grid item leaves the middle off-screen; the stage is centred
  by transform now.
- **Every slide clipped 114px.** A percentage height inside a padded fixed box
  is not the box: the frame is a flex column and the body the flexible child.
  The gate reported it as `clipped-content` on slides whose text was well inside
  the frame.
- **Long bullets were cut top and bottom.** With `align-items: center` on the
  split layout, prose taller than the frame overflows both ways and the copy
  gate reads those lines as copy a user cannot see. Overflow goes downward now,
  where it is measurable, and the builder warns above ~430 characters of prose
  beside a figure.
- **The manifest did not match the render.** It is generated from the rendered
  markup, not from the Markdown with its markers stripped: a line containing
  ```` ```d2 ```` strips to something the page never says.

## What the copy manifest covers

`copy.txt` is generated from the **Markdown prose only** — each slide's
heading, bullets, pull quotes and paragraphs, as the page renders them
(markers gone, entities decoded). Three things are therefore *not* in it:

- **A figure's labels.** Text inside a ```d2 fence is drawn as SVG, and the
  manifest never contains it. So a string the deck must be seen to say belongs
  in prose; if it only appears in a figure, the copy gate cannot vouch for it —
  hold the figure to a fact sheet instead (step 7).
- **Speaker notes.** `<!-- notes: … -->` is printed and never on screen, and it
  is not in the manifest either.
- **The chrome.** The footer's deck title and page number are not manifest
  lines.

For a reader, the build also writes **`slides.json`**: per slide, its heading,
its text in reading order, its figures and the words those figures draw. That
is the sheet `deck-review` scores against, and the reason it is a separate file
from `copy.txt` is that a manifest cannot express order.

A bullet, quote or paragraph wrapped over several lines is **rejoined** into one
line, as Markdown does, so wrapping at 80 columns is safe and one sentence is
one manifest line. A blank line ends the block: an indented line after one is a
paragraph of its own.

## Failure modes

- **`✗ slide 6-1: the d2 figure does not compile`** with
  `reserved keywords are prohibited in edges` → an id collided with a D2
  keyword. `width`, `height`, `label`, `style`, `shape`, `icon`, `near`, `top`,
  `left`, `direction`, `class`, `link`, `constraint`, `layers`, `steps` and
  `scenarios` are the ones that bite; rename the box (`cols`, `verdict`) and
  keep the words in its label.
- **`copy-invisible (reason: unknown)` on a line that is plainly on the slide**
  → a vlmkit gate limitation, not your deck: a manifest line whose rendered text
  is assembled from several inline children can read as invisible. Reproduced
  minimally in `examples/d2-slides/README.md`; three bullets carrying `<code>`
  and `<strong>` fail, the same three lines without markup pass. Run with
  `--allow-invisible unknown` (every accepted line is listed, so the suppression
  stays auditable) and check the `missing` count, which is the part that matters.
- **`check a11y contrast` inspected only four elements** → you pointed it at
  `index.html`. One slide is on screen at a time; `print.html` is the stacked
  view. Do not read the absolute count as a threshold: it tracks how many text
  nodes the deck has, so a terse deck legitimately sits near 7 a slide. The
  comparison between the two views is the signal.
- **`near-misalignment` (a warn) on a base64-looking selector like
  `g.KGdhdGV3YXkgLSZndDsgY2hlY2tvdXQpWzBd`** → that is *inside* a figure's SVG:
  the gate has found two of TALA's own edge-label groups sitting 5.5px apart,
  which is the layout engine's business and not the deck's. It is a `warn`, so
  the verdict reads `NO DEFECTS, n WARN` and the command exits 0 — that is
  done, leave it. There is no stable way to exempt it either: `--allow` matches
  the finding's own selector by substring, and d2 derives that class from the
  edge's text, so the string changes with the label. If a run has to be silent,
  `--rule near-misalignment=off` is the only lever, and it gives up the rule for
  the slide chrome too. Whether it fires at all depends on the layout, not on
  having labelled edges: the same deck's figures can be CLEAN after an edit.
- **`page-overflow-x` on `print.html` at 768 or 375** → expected: the print view
  is a column of 1280px frames. Check it at `--viewports 1280`.
- **A figure is enormous or unreadable** → it is a D2 diagram like any other:
  take it to `d2-diagram`, where the width levers, the fact check and the
  terminal render live. A slide figure has about 700×560 to live in.
- **CJK labels** render correctly in SVG, so a Japanese deck is fine; the
  terminal-render caveats in `d2-diagram` do not apply here.

## Deliver

- The deck: `built/index.html`, opened in a browser. Arrows and space move, `o`
  is the overview grid, `p` prints, `f` is fullscreen, and the URL carries
  `#/4`, so one slide can be linked.
- A PDF: open `print.html` and print it, or `index.html` and press `p`. Speaker
  notes appear in print and never on screen.
- In a repo: commit `deck.md` and the figures' `.svg`; the HTML is a build
  output. `examples/d2-slides/` is the worked example — its deck, its build, and
  the gate runs above.
- One slide as an image: the figure is already `built/slide-NN.svg`.
