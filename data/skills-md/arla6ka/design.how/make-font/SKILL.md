---
name: make-font
description: Use when someone wants their own font made from fonts they like, such as "make me a font like these", "/make-font" or "build a typeface from these screenshots". It measures the references, fits the closest open-licence font to them, checks it, and delivers an OFL font with web files and a font book. It never copies outlines.
---

# Make a font

The person names fonts they like. This skill measures them, picks an open-licence (OFL or Apache) font as the
base, and bends that base to the measured numbers. Every outline in the result comes from the open base. The
references give numbers only: proportions, stem and stroke thickness, class-mean widths and spacing. The output
ships under the OFL with a new family name.

## The line it holds

Say this to the person at the start, in plain words: "I match proportions, widths and spacing on an open font.
I don't trace or copy the outlines of the fonts you send." Then hold it.

- Never open a reference font in the build step. `fit_font.py` and `space_font.py` read only the base font and
  `targets.json`.
- Never take a per-glyph advance, a kerning pair or a point from a reference. Targets are font-wide numbers and
  class means.
- Refuse a request to clone, trace, convert or "rebuild exactly" a commercial font, or to rename one. Offer the
  proportional match instead.
- A screenshot of a commercial font is fine to measure. Its file is fine to measure if the person has it. Neither
  is copied into the output or committed anywhere.

Scripts are in `scripts/`. They need Python 3.9+ with `fonttools`, `brotli`, `uharfbuzz`, `numpy` and `pillow`
(`skia-pathops` to remove overlaps, `fontbakery` for its checks if wanted), and Node 18+ with Playwright for the
PDF. Run Python as `python3 -I` and pass paths: every script reads `--help`. Downloaded fonts go in their own
folder and are only read, never run.

## Steps

1. **Ask once.** In one message ask for: the fonts they like, as font files or screenshots (two to four is
   plenty), what the font is for (text, display or UI), which scripts and languages it must cover, which weights,
   and a new family name. If they can type in the font (a foundry's type tester, a design tool), ask them to
   screenshot the four lines of `SAMPLE_LINES` in `scripts/fontlib.py`, large, cap height 80 px or more. Take
   defaults for anything unanswered and say which: text, Latin, Regular and Medium, a name you propose.
   Done when the references, use, scripts, weights and name are written down.

2. **Measure.** Files: `measure_font.py <file> --out m1.json`. Screenshots:
   `measure_image.py <shot.png> --text "line|line" --out m2.json`. Before trusting a screenshot, run
   `measure_image.py --selftest <any open font> --px <its px per em>` at the screenshot's size: it prints how far
   pixel readings land from the file's numbers. Report every number marked low confidence. Method, definitions
   and error sizes: `references/measuring.md`.
   Done when each reference has a measurement file and the person has seen the main numbers.

3. **Targets.** `make_targets.py m1.json m2.json --family "New Name" --use text --scripts latin
   --style Regular:400 --style Medium:500 --out targets.json`. Where references disagree, the script lists the
   spread. Ask which way to lean instead of averaging a serif with a sans.
   Done when `targets.json` exists and every spread has an answer or a stated default.

4. **Find the foundation.** `find_foundation.py targets.json --cache <dir> --out shortlist.json`. It ranks open
   families from the Google Fonts catalogue by distance to the targets, with variable fonts ahead
   (`references/foundation.md`). Show the person the top three to five with their deltas and axes, render each
   beside a reference if you can, recommend one, and wait for a yes. Note any Reserved Font Name.
   Done when the person confirmed a base. Do not build before that.

5. **Fit.** `fit_font.py <base-vf.ttf> targets.json --out-dir build/ [--loc opsz=..]`. It solves a y instance for
   stems and contrast, an x instance per width class for widths, merges them into one static per weight, and
   iterates until every class mean is within 0.3 percent, never stretching more than 3 percent
   (`references/fitting.md`). If a class hits the stretch limit, tell the person what that letter class will be
   and offer a base with a width axis.
   Done when every style is written and `fit-log.json` shows each class within tolerance or explained.

6. **Space.** `space_font.py build/X-Regular.fit.ttf targets.json --out build/X-Regular.ttf [--track -4]`.
   Class sidebearings to the targets, an optional global track, kerning carried and scaled, then the collision
   guard (`references/spacing.md`). More than 150 guard pairs means the spacing is too tight. Loosen and rerun.
   Done when the guard count is under 150 and its log is saved.

7. **Package and check.** `package.py build/*.ttf --targets targets.json --base <vf> --base-licence <OFL.txt>
   --holder "<who owns the modifications>" --out-dir dist/ --fit-log build/fit-log.json --space-log ...`
   (`references/licensing.md`), then `check_font.py dist/ttf/*.ttf --targets targets.json --base <vf>
   --reference <ref file> --package dist/ --fit-log build/fit-log.json --out-dir checks/`
   (`references/checks.md`). Look at every overlay
   render yourself, at the text and the display size. A failed gate goes back to the step that owns it.
   Done when the check exits 0, or each failure is listed for the person with its number and the reason.

8. **Font book.** `font_book.py dist/ttf/*.ttf --webfonts dist/webfonts --targets targets.json --fit-log ...
   --space-log ... --check-report checks/check-report.json --out-dir book/`, then
   `node scripts/render_book.mjs book/`. It prints the pages as PNG and one PDF and fails on a fallback glyph or
   an overflow (`references/font-book.md`). Open three pages and look before you hand it over.
   Done when `book/fontbook.pdf` exists and render_book.mjs exits 0.

## Hand-off

Tell the person, in this order: what was made (family, weights, glyph count, scripts), the base and its licence,
the gates with their numbers (pass and fail), what still differs from the references and why (the base's own
drawing: terminals, serif shape, a letter that reads differently), and where the files are. Attach or link the
PDF. Name the fonts' provenance plainly: built on an open font, fitted to measurements.

## Never

- Copy, trace, auto-trace or convert outlines from a reference. Copy a reference's kerning or per-glyph widths.
- Ship under any licence but the OFL, keep the base's name or a Reserved Font Name, or keep its trademark record.
- Put a reference font's name in the output files, the font book or the package README.
- Call a gate passed that was not run in this session. fontbakery not installed is "not run", not "passed".
- Stretch a glyph more than the limit to hit a number. Report the gap instead.
- Commit or publish font files unless the person asks, and never a reference font.

## Files

- `scripts/fontlib.py` shared geometry, classes, sample lines, rasteriser.
- `scripts/measure_font.py`, `measure_image.py`, `make_targets.py`: steps 2 and 3.
- `scripts/find_foundation.py`: step 4. `fit_font.py`: step 5. `space_font.py`: step 6.
- `scripts/package.py`, `check_font.py`: step 7. `font_book.py`, `book.css`, `render_book.mjs`: step 8.
- `references/`: measuring, foundation, fitting, spacing, checks, licensing, font-book.
