---
name: make-poster
description: >-
  Creates and checks conference research posters and short poster-session
  pitches. Use when the user asks to make a poster, prepare a research poster,
  adapt a paper into a poster, fit a poster to A0/A1/36x48in, check a
  beamerposter or tikzposter file, reuse paper figures, or write a 2-minute or
  5-minute poster pitch. Bundled scripts resolve poster dimensions, inventory
  reusable figures, lint print-day problems, and time spoken pitches.
---

# Make Poster

Turn a paper or poster draft into a print-ready conference poster plan, with
real dimensions, readable typography, figure reuse, and a timed short pitch.
This skill is for posters and poster-session delivery; use `make-slides` for
podium talks.

## When to use

- The user needs a research poster for a conference, workshop, demo session, or
  department event.
- The venue gives a size such as A0, A1, 36x48in, 48x36in, or a custom board.
- A LaTeX poster already exists and needs a print-day lint pass.
- The user wants a 2-minute or 5-minute pitch for visitors.

## Inputs

- Poster size from presenter instructions or the acceptance email. Do not guess
  the board size from memory.
- Optional: the paper's main `.tex` file, so figures can be inventoried and
  copied from the source tree.
- Optional: existing poster source, usually beamerposter or tikzposter.
- Optional: draft pitch text in markdown or plain text.

## Process

1. Confirm the physical size and orientation. Run:

   ```bash
   python3 scripts/poster_size.py --size 36x48in
   python3 scripts/poster_size.py --size a0 --orientation portrait
   ```

   If the venue also gives a board limit, include it:

   ```bash
   python3 scripts/poster_size.py --size 36x48in --board 48x96in
   ```

2. Inventory paper figures when a LaTeX paper source is available:

   ```bash
   python3 scripts/poster_figures.py paper/main.tex --copy-to poster/assets
   ```

   Prefer figures that are central to the paper's claim, cited often, and still
   readable when enlarged. Avoid cramming full paper multi-panel figures onto
   the poster without simplification.

3. Draft or revise the poster around a small number of claims. A good poster is
   not a paper pasted onto a board: use claim-style section headings, one hero
   visual, short method/evaluation blocks, and a clear takeaway with contact
   information or a QR code.

4. Lint the poster source:

   ```bash
   python3 scripts/poster_lint.py poster/poster.tex --expect-size 36x48in
   ```

   Fix every `RISK` finding before sending to print. With `--strict`, warnings
   also fail the run.

5. Time the pitch:

   ```bash
   python3 scripts/pitch_check.py poster/pitch-2min.md --minutes 2
   python3 scripts/pitch_check.py poster/pitch-5min.md --minutes 5
   ```

   Keep the short pitch conversational. It should end by inviting the visitor
   into the discussion rather than dumping every result.

## Output

- Exact poster dimensions and suggested LaTeX invocation.
- Figure inventory and recommended hero-figure candidates.
- Lint report with print-day risks and warnings.
- A timed 2-minute or 5-minute pitch, or feedback on an existing pitch.

## Guardrails

- Never invent venue size, board size, or print requirements.
- Never alter data values, axes, or results to make a figure look better.
- Do not reproduce third-party figures unless the user has rights to use them.
- Keep posters readable from a distance: if text only fits at tiny sizes, cut it.
