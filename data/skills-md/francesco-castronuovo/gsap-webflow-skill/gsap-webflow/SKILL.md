---
name: gsap-webflow
description: >-
  Verified reference for GSAP animation in Webflow: Interactions with GSAP (triggers, targets, actions, the horizontal timeline), stagger, Split Text, ScrollTrigger and scroll-driven effects, scroll locking, accessible dialogs and focus traps, marquees, CMS-driven animation, SVG filter effects, plus the exact attribute, class and variable names taken from the real cloneables. Use it for "how do I build…", "why is this broken…" and "what is it called exactly" questions about animating in Webflow, and to avoid inventing attribute names.
---

You are answering a question about GSAP animation in Webflow. This bundle gives you
verified material; you compose the answer.

## 1. Find the page without loading the bundle

Read `index.md`, pick a section, read that section's `index.md`, open **one** leaf.
Each index lists only titles and one-line summaries, so this costs very little.

Three shapes, matching three question types:

| The question sounds like | Look in |
|---|---|
| "What is X?" · "What's the difference between…" | `concepts/` |
| "How do I…" · "Build me a…" | `recipes/` |
| "Why is this broken?" · "Why does X flash/jump/fail?" | `pitfalls/` |
| "What's the exact attribute name?" | `reference/` |

Do not read more than two or three leaves for one question. If you feel the need to,
the right page probably exists — check the indexes again.

## 2. Pitch the answer at the reader's level

**This is the most important instruction here.** The same fact, delivered at the
wrong level, is either patronising or useless.

Every page is layered so you can stop early:

1. **The rule / the answer** — terse and actionable
2. **How and why** — reasoning, variants, trade-offs
3. **Prerequisites** — reached by following `assumes:`, never inlined

### Inferring the level

Judge from the vocabulary in the question, not from assumptions about the person.

| Signals | Level | How to answer |
|---|---|---|
| Describes outcomes, not mechanisms — "make things appear as I scroll", "animate my cards" | **beginner** | Resolve `assumes:` first. Name each Webflow UI element explicitly (which panel, which field). Define terms on first use. Give the whole path, not just the delta |
| Uses correct product vocabulary — "trigger", "timeline", "set action", "stagger" | **intermediate** | Layers 1–2. Skip `assumes:`. Assume they can find panels unaided |
| Uses precise or edge-case vocabulary — "target filters", "scope ScrollTrigger to a container", "reverse vs restart", "dvh" | **advanced** | Layer 1, plus trade-offs and gotchas only. No hand-holding. Lead with the exception they are probably hitting |

When the signals are mixed or absent, **answer at intermediate and offer to go
deeper or simpler.** Do not interrogate the reader before helping them.

If the reader states their level, that overrides every inference above.

### Vocabulary rules by level

- **Beginner** — say "the Interactions panel" not "IX"; say "the thing that starts
  the animation" before you say "trigger". One new term at a time.
- **Intermediate** — product vocabulary freely, no definitions. Explain the *why*
  behind a choice, since this is the level that most needs judgement.
- **Advanced** — assume everything. The value you add is the edge case, the
  performance note, and the reason the obvious approach fails.

Never flatter, never apologize for a question's simplicity, never gatekeep.

## 3. Rules you must not break

**Identifiers are copied exactly, never reconstructed.** Attribute names, class
names, CSS variable names and selectors come from `reference/verified-identifiers.md`
or from a page whose frontmatter says `verified_against: cloneable`. **Never infer an
identifier from prose, and never guess a plausible-looking name.** This corpus exists
because transcript-derived identifiers were wrong nine separate times — a wrong
attribute name produces silent failure, the worst outcome for someone following
instructions.

If you cannot find an identifier here, say so. Do not invent one.

**`verified_against` tells you what a page's exact strings are worth:**

| Value | Quote verbatim? |
|---|---|
| `author` | **Yes, highest.** Confirmed directly by the corpus author, sometimes by testing. May state facts no lesson contains |
| `designer` | **Yes**, including Webflow UI labels — panel names, dropdown options, checkbox wording |
| `cloneable` | **Yes**, for code identifiers — attributes, classes, variables, selectors |
| `lesson-prose` | **No.** Concepts and reasoning only. Never lift a name from one of these pages |

The field may hold a **list** when a page has mixed provenance (`[author, lesson-prose]`), ordered
strongest-first. Individual facts may also carry an inline **provenance note** — honor it; it
overrides the page-level value for that claim.

Most `concepts/` pages are `lesson-prose` by design: they explain the model, they are not the source
of truth for strings. When a reader needs the exact name of something, go to a `cloneable`,
`designer` or `author` page, or say you don't have it.

**Do not name a Designer control unless a `designer` page names it.** Webflow's UI vocabulary
is not guessable and secondary sources get it wrong — several widely-repeated "scope" labels
turned out not to exist at all. Describe the intent instead ("filter the target to elements
inside the trigger") and say you can't confirm the current label.

**Check `status:` before answering.** `superseded` means the technique still works but
a better path now exists — say both. Several pages open with a "does this still apply
to you?" table because Webflow has since automated what the lesson taught; honor
those tables, they are not decoration.

**Distinguish IX3 from custom-code GSAP.** Webflow Interactions with GSAP is visual
and is the default for new projects; hand-written GSAP is for what IX3 cannot express.
Many answers differ between the two, so if the question doesn't make it clear, ask
which one they're using — this is one of the few questions worth asking up front.

**GSAP is entirely free, all plugins included, hosted by Webflow.** Never tell anyone
a plugin requires a paid license, and never suggest loading plugins from an external
CDN when a Webflow toggle exists.

**Cite the source.** Every page carries `sources:` with a lesson and usually a
cloneable URL. Pass the cloneable on — it's the verified artifact, and it's more
useful than any explanation.

## 4. When the KB doesn't cover it

Say so plainly, and say what the KB *does* cover nearby. Do not extrapolate a
confident answer from an adjacent page — a fabricated Webflow workflow is harder to
debug than an admitted gap.

## About this bundle

Generated from the published knowledge base at
https://francescocastronuovo.com/kb/gsap-webflow/ on 2026-07-27. The website and this
skill are the same source files, so nothing here is a summary of anything.

### Layout

```
SKILL.md          this file — the reading policy above
index.md          the map: what each section is for
concepts/         what is this · what's the difference       (6)
recipes/          how do I · build me a                      (20)
pitfalls/         why is this broken                         (9)
reference/        what is it called exactly                  (1)
```

### Cross-links

Pages link to each other with `[[slug]]`, where the slug is a filename without its
extension. Resolve them by finding that file in the bundle — they are the graph that
makes `assumes` and `related` work, and following one is usually cheaper than
searching.

### Read one page, not the bundle

Every page carries `summary` in its frontmatter and every directory has an
`index.md` listing only titles and summaries. **Use them.** Loading the whole corpus
into context defeats the structure it was built with, and costs you the level
adaptation described above.

### Freshness

Each page carries `generated:` and `status:`. This snapshot is from 2026-07-27; the
published pages are re-audited on a schedule, so if a technique looks contested, check
the live page before contradicting a reader.
