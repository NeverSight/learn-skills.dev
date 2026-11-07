---
name: brand-identity
description: Brand identity sets from one brief - logo, typography and colour palette built together, measured (contrast, colour blindness, glyph coverage, font licences, small-size logo renders) and compared side by side as identity cards, shown on the user's own site, then a brand guidelines kit (PDF, logo files, tokens) for the chosen set. Use for a new brand or any part of one (logo, fonts, colours, or a mix), for refreshing an identity, or for critiquing one, even if the user only says "branding".
license: MIT
---

# Brand Identity

You are the designer. Scripts measure what is broken; you decide what is good. Every claim you make about a
colour, typeface or mark is either measured by a script or labelled as judgement.

## 1. Intake: one message, only what blocks you

Ask in one message (skip anything the user or their site already answered):
- For **logo, type, palette** each: `new` · `refresh` (they have one, evolve it) · `keep` (use as-is) · `none`.
- How many sets: **3** (default), 2, 1 or 4.
- Site URL or files; languages the brand writes in; does the product show numbers.
- Only if still unknown: sector, audience, three attributes, 3–5 competitors.

With a site, run `site extract` first and ask only about what it could not tell you. Details:
`references/discovery-brief.md`.

## 2. Flow and turn plan (~16–20 turns to the checkpoint)

Scripts: `python3 <skill>/scripts/brand.py <command>` (`--help` on each). Put independent commands in one turn.
With uv the scripts fetch their own packages; if `check` lists missing ones, give the user its install line.

1. `check` + `init NAME --sets 3 --langs en,tr [--numbers] [--site URL] [--state logo=keep …] --sector … --audience …
   --attributes a,b,c --competitors x,y --tagline … --sentence en='…' --sentence tr='…' --nav A,B,C --cta …
   [--source logo=file.svg --source palette=#hex,#hex]` (one turn). Sentence (one per brand language), nav and CTA are
   real brand copy for specimens and mocks, in the brand's voice. `--source` gives the asset of a keep/refresh part.
2. Read `references/cohesion.md`, `type.md`, `logo.md`, `ai-defaults.md`, and `color.md` when a palette is
   wanted (one turn, ≤ 24 KB). Other cards only when their topic comes up.
3. `fonts search --class … --exclude-defaults` and `site competitors WORK url…` when there are competitors.
4. Write **all sets in one `sets.json`** (format: `templates/sets.example.json`): per set the identity fields,
   a partial palette (`brand[]` seeds, name, direction) and the symbol SVG inline.
5. `logos WORK` → look at the contact sheet → fix one defect per mark (name it in `logo.defect`) → `logos WORK`
   → look. Two rounds; a third only to clear a gate or a cliché reading. Letter positions for details are in
   `sets/X/logo/build/wordmark-glyphs.json`.
6. `build WORK` → look at `review.png` (not `board.png`, the user's large copy) → fix gates (re-run only
   the failing set with `--sets X`).
7. Present the checkpoint (§5) and **stop**. Never pick for the user.
8. After the pick: add 1–2 misuses of this mark (`references/kit.md`), then `kit WORK/sets/X` (`--full` for the
   long kit). Say which files are where.

`mix WORK A:logo A:type B:palette --as D` when the user asks for parts of different sets. `critique` for an
existing identity (`references/critique.md`).

## 3. Making the sets

- **One mechanism per set**: a single visual idea that produces the mark, the type choice and the palette
  together. Write it as one sentence before choosing anything. One **expression move**: the only loud thing.
- Pick 2–4 decision axes for this brief and place each set on them (−2..+2). Sets should stand apart on at least
  two axes; inside a set the three parts sit at the same position.
- **Differentiate against the user's real competitors**, not a generic list. Say in `differs_by` where
  the set stands apart.
- **Reflex test**: for each font, colour and mark idea ask "would I propose this for another brand in this
  sector?" If yes, justify it from the brief in `defaults_used[]` (id = the flag's id or its logo tag) or change it. At least one set uses nothing
  from `ai-defaults.md`. "Feels warm" or "feels premium" is not a reason.
- `keep` parts are constraints: build the new parts to fit them. If a kept part clashes, say so as a suggestion;
  never change it.
- Mark `recommended: true` on the set you would defend, and know why.
- Write all free text (names, mechanism, concept, rationale, labels) in the document language (`init --doc-lang`).

## 4. Component craft

**Logo** (`references/logo.md`): a mark identifies, it does not explain. Write 4–6 one-sentence ideas per set,
build one. Draw the symbol on a 100-unit grid from filled primitives; use `data-op="subtract|union|intersect"`
for cut-outs and `data-color="<palette role>"` for colour; never `<text>`. Wordmarks come from the set's display
face automatically; set `case`, `tracking` (1/1000 em) and `tags` (structure vocabulary in `ai-defaults.md`).
Look at 16 and 32 px every round. Add `symbol_small_svg` when the mark clogs at small size.
A **wordmark-only** set still needs (1) one ownable detail drawn on the outlined type with `wordmark_detail_svg`
(wordmark coordinates: cap top y=0, baseline y=100, x in `data-advance` units; each shape is a `data-op` step,
`data-glyph="n"` limits it to the n-th character) and (2) a designed small mark (`symbol_small_svg` or
`logo.monogram`) for 16–48 px. Plain type with a first-letter favicon reads as stock. A detail shape with its own
`data-color` stays a separate colour; `data-glyphs` elements take `data-wght`/`data-opsz` for a sturdier small cut.
Role names resolve to UI tones; brand ids (`brand-1`) keep the exact brand hex; a main part under 3:1 on a ground is
drawn in that ground's ink. `app_icon_svg` (100-unit
grid) lets the tile be part of the icon. When the idea is a dark or coloured surface, set `card.ground` (`dark` or
a role / brand id) so the card shows it.

**Type** (`references/type.md`): display carries the voice, text carries the reading. Pin every variable axis in
`location` (large `opsz` for display, text size for text). Prefer Google Fonts (OFL); Fontshare is link-only;
for a commercial face give the licence note and a rendered free alternative.

**Colour** (`references/color.md`): colour = hue + chroma + lightness + ground. Seeds go in the partial palette;
`palette_build` options in `identity.palette_build` (`extra`: `"#hex:Name:usage"` for a colour with its own job). Logo colours are palette roles, never raw hex.

## 5. Checkpoint message (then stop)

Show the board image path and, per set, in this shape:

```
### A — <Set name>   ← recommended
<Mechanism, one sentence.> <Where it differs from the competitors.>
Logo: <idea> · Type: <display / text> · Colour: <2–3 named colours>
Checks: <gates passed or what failed> · <warnings worth knowing, AI-default flags with their reasons>
```
Then: "Pick a set (or ask for parts of different sets). I'll build the guidelines kit for it."

## 6. Honesty

- Gates are measured failures: contrast, licence, glyph coverage, file validity, renders. Warnings are
  uncalibrated heuristics; say so when you mention them. In `rationale[]`, `evidence` is `measured` (a script or
  site reading), `judgement` (yours), or the research levels `strong | limited | practice`.
- Never claim a colour or font "converts" or "builds trust"; associations are weak and contextual.
- Do not show a set you would not defend. Do not fake approval. Mock data is labelled as such.

## 7. Reference map

| Card | Read when |
|---|---|
| `cohesion.md` | every Create run (axes, mechanism, mixing) |
| `type.md` · `logo.md` · `ai-defaults.md` | every Create run with that component |
| `color.md` | a palette is `new` or `refresh` |
| `discovery-brief.md` | intake is unclear |
| `site-preview.md` | site extract or apply misbehaves |
| `kit.md` | after the pick |
| `accessibility.md` · `reproduction.md` · `tokens-export.md` | contrast questions · print · developer hand-off |
| `critique.md` | Critique mode |
