---
name: kdp-typeset-interior
description: Typeset a book interior for KDP with Typst — page geometry, gutter-aware margins, the even-page-count problem, and the Typst behaviours that fail silently. Use when building or debugging an interior PDF, changing a book's layout or typography, or working out why a Typst book build produced the wrong extent, wrong margins or wrong glyphs.
---

# Typesetting the interior

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/build-interior.py
```

Finds the nearest `book.toml`, computes geometry from `[print]`, and compiles
`templates/interior.typ` with every dimension passed in as `sys.inputs`. The
template needs no editing when the trim or the extent moves.

## Why this is not one `typst compile`

**The even page count cannot be decided inside Typst.** Printers require an even
leaf count, and the extent is not known until the document is laid out. A
conditional on `counter(page).final()` oscillates: adding the parity leaf makes
the count even, which makes the condition false, which removes the leaf. The
decision has to be made by something standing outside the document — so the build
compiles, counts, and compiles again.

**The gutter minimum is tiered by page count.** A book at 301 pages needs a wider
inside margin than the same book at 299. So margins cannot be fixed in the
template; the second pass derives them from the first pass's measured extent. A
book sitting exactly on a tier boundary can need a third pass, and the script
handles that.

## Where the text lives

`[paths].body` in `book.toml`. A single `.typ` file or a directory of them.

**The plugin does not write the book.** It typesets a manuscript that already
exists. If asked to draft, outline or expand the text, that is a different task —
say so and do it as a normal request if the user wants it, but it is not part of
this workflow and nothing here assumes AI-written text.

**The body is never hand-edited in the built PDF.** If an entry is wrong, fix the
source. For a generated book — an index, a catalogue, a directory — fix the
generator or its data, never the manuscript, because at that scale a hand-edit is
silently destroyed on the next rebuild.

`templates/interior.typ` is the exception and is hand-written on purpose: it is
layout, not content. The build never rewrites it, so typography changes survive.

## Typst behaviours that fail silently

**Missing glyphs produce no warning.** Typst falls back through the system font
list, renders the character in whatever face it found, and exits 0. On a machine
with a different font set, the same source produces a different book. Always pass
`--font-path` at bundled fonts — `build-interior.py` does — and always run
`/kdp-preflight`, whose round-trip check is the only signal that exists.

**A literal `/*` opens a block comment and eats the rest of the file.** The build
succeeds; the document is just short.

**`pagebreak()` is illegal inside a `columns()` container.** Use page-level
columns if back matter has to start on a fresh page.

**Changing `justify` part-way through an entry starts a new paragraph**, so the
gap that follows is governed by paragraph `spacing`, not `leading`. Invisible at
thumbnail size; check at 300 dpi.

**`binding: left` is what makes `inside`/`outside` margins alternate correctly**
across a spread. Setting plain `left`/`right` margins instead puts the gutter on
the wrong side of every verso page — legal, and wrong on half the book.

## Escaping

Do not hand-roll escaping of Typst syntax characters in generated content. Emit
the data as JSON and read it in the template with `json()`: values arrive as
strings rather than markup, so `#`, `$`, `*`, `_`, `@` and backslashes render
literally. Hand-rolled escaping across thousands of machine-generated strings is
the likeliest source of silent corruption in a book nobody can proofread by eye.

The hazard survives only in the hand-written prose of the template itself.

## Fonts

Bundle them under `[paths].fonts` and list the intended families in
`[print].fonts`. Preflight lists what actually got embedded and flags anything
outside that set, which is how a substitution gets caught before the proof copy
rather than after it.

Libertinus ships with Typst, so the default template compiles on a machine with
no fonts installed at all.
