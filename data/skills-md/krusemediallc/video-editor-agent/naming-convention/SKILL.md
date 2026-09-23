---
name: naming-convention
description: >-
  Name a batch of video deliverables so each filename says what the file actually is —
  subject, variant axis, and treatment — instead of `render-final-v3.mp4`. Use whenever more
  than two files are being handed over, and whenever someone says "rename these", "give these
  descriptive names", "I can't tell these apart", "name them so I know which is which", "put
  the product in the filename", "which one is the captioned version?", or is about to deliver
  a folder of variants, renders, exports, or cutdowns. Also use when naming a NEW batch
  before it ships, not just fixing an existing one — deciding the pattern up front is the
  cheap moment. Covers choosing the axes that vary, verifying the facts in a name before
  baking them into 40 files, keeping the subject map as data, and renaming idempotently
  without breaking a review canvas that already points at the old names.
---

# naming-convention — filenames that carry the work

A filename is the only metadata that survives every tool: Finder, an upload dialog, a
Slack drop, a folder someone opens in six months. When a batch ships as
`ad-v5-hook-01.mp4 … ad-v5-hook-21.mp4`, the person receiving it has to open all 21 to do
anything, and the numbers mean nothing a week later.

The job of this skill is that someone can pick the right file **without opening it**.

## The rule

**The filename carries every axis that varies across the batch, plus a stable sort key.**

Anything constant across the batch belongs in the folder name, not in 40 filenames. Anything
that varies and is *not* in the name is a thing the user has to open files to discover.

```
<index>-<subject>-<descriptor>-<treatment>.<ext>
```

- **index** — zero-padded, first, so disk order matches whatever ordering the review used
  (canvas cards, a shot list, the order they were cut). This is worth a lot: "card 7" on the
  review page and the 7th file in the folder should be the same thing.
- **subject** — what the thing is *about*. The product, the client, the topic.
- **descriptor** — the axis that distinguishes near-duplicates: style, format, angle, take.
- **treatment** — what was done to it: `body-edited` / `body-unedited`, `captioned` /
  `clean`, `9x16` / `1x1`, `draft` / `approved`.

Worked example, from a hook A/B batch:

```
hook-07-lookalike-cinematic-body-unedited.mp4
hook-07-lookalike-cinematic-body-edited.mp4
     │  │          │         └ treatment: which body cut (captioned vs clean)
     │  │          └ descriptor: the ad style
     │  └ subject: the product being advertised
     └ index: matches card 7 on the review canvas
```

Two files, same hook, and you can tell them apart in a Finder list without a preview.

**Spell the axis out when a bare word is ambiguous.** `…-unedited.mp4` reads as though the
*hook* is unedited; `…-body-unedited.mp4` cannot be misread. Length is cheap; a wrong reading
is not.

## Verify the facts before you bake them into 40 files

This is the part that actually costs time when skipped.

**Labels inherited from an upstream step are evidence, not truth.** A cut list, a shot list,
a client spreadsheet, an earlier session's JSON — each was written by someone solving a
different problem, and mislabels survive because nothing downstream ever checks them.

Two real examples from one batch of 21, both wrong in the upstream cut list:

- A hook titled **"sparkling water"** was actually an ad for a **cap**. The generation had
  two references: a reference *image* (the cap — the product) and a reference *video* (a
  sparkling-water ad — the style). The upstream title had named the style reference.
- A hook titled **"Gut Check"** was actually the **Thumb-Stopper** protein bar. Gut Check was
  a different hook's product, one slot away.

Both would have shipped into four filenames and a review canvas.

**How to check cheaply, in order:**

1. **Find where the source states it.** In generated-ad work the tool's own prompt panel
   shows the prompt and a legible reference-image thumbnail a few seconds into most clips —
   that settles it outright. The equivalent elsewhere: a slate, a title card, a project file,
   an order form.
2. **Look at the artifact itself.** Pull frames from where the subject is on screen. Be aware
   this is the *harder* path for close-up product work: extreme close-ups crop wordmarks, and
   picture-in-picture bubbles cover them. Four escalating crops of one bar wrapper still only
   read "THUMB…"; the prompt panel gave the full name in one frame.
3. **Cross-check the transcript.** Someone usually says the product name out loud.

Spend the ten minutes. Renaming is cheap; a wrong product name on a client deliverable is
not, and neither is the credibility hit when they spot it.

When you do correct an inherited label, **say so explicitly in the handover** — the user may
have that wrong label in their own notes, and a silent fix reads as an inconsistency later.

## Slug rules

Keep names shell-safe, URL-safe, and sortable:

- lowercase, hyphen-separated, ASCII; no spaces, apostrophes, `&`, or parentheses
- zero-pad indexes (`07`, not `7`) so lexical sort matches numeric sort
- prefer the name a human would say ("hyperfocus", "gut-check") over an internal code
- keep the subject slug **stable across batches** — same product, same slug, so a later
  `ls *lookalike*` finds every one
- resist stuffing: if the name needs four descriptors you probably have two batches, and the
  extra axis belongs in the folder

## Keep the map as data

Put the per-item facts in a small JSON file next to the batch, not inside a rename script:

```json
{"_note": "read off the tool's prompt panel, NOT the upstream cut list — two of those were wrong",
 "items": {
   "1": {"subject": "cap",        "style": "cinematic"},
   "5": {"subject": "thumb-stopper", "style": "asmr"}
 }}
```

Batches get relabelled. When the mapping is data, a correction is a one-line edit and a
re-run; baked into a script it is a rewrite; left in a chat transcript it is gone. Include a
note about where the facts came from — the next person will wonder whether to trust it.

## Rename safely

```bash
python3 scripts/rename_batch.py --dir variants/ --map subjects.json \
    --pattern "hook-{index:02d}-{subject}-{style}-body-{treatment}" \
    --set treatment=unedited --manifest variants.json          # dry run
python3 scripts/rename_batch.py ... --apply                    # commit
```

The script refuses to run rather than half-finish: it checks every source exists, that no
target collides with a different file, and that the pattern actually produces unique names.
It is idempotent — a second run reports "already named" instead of double-renaming — and it
updates the build manifest so later steps still find the files.

Four things to get right around a rename:

- **Dry run first, always.** The output is the review; read it before `--apply`.
- **Update the manifest** (`variants.json` or equivalent), or the next tool in the chain
  looks for files that no longer exist.
- **Republish the review canvas** if the batch is already on one, and print the filename on
  each card so canvas ↔ disk is a direct match. A reviewer saying "number 7 is the one" and a
  folder where 7 is something else is exactly the confusion this skill exists to remove.
- **Do not rename a file someone already has.** If it has been delivered and downloaded,
  ship the new name as a new copy or tell them plainly that the names changed. The repo rule
  that delivered files are never overwritten applies to their names too.

## House patterns

| Batch | Pattern |
|---|---|
| hook variants (one body × N hooks) | `hook-NN-<product>-<style>-body-<edited\|unedited>` |
| ratio cutdowns of one edit | `<project>-<ratio>` e.g. `acme-9x16` |
| revision rounds | keep the name, bump a version segment; never overwrite a delivered file |
| stills / frame grabs for review | `<project>-<timecode>` e.g. `arcads-0m17s2` |

If a new batch does not fit these, choose the axes first and write them down in the handover
before renaming 40 files — the pattern is much cheaper to change before it exists.

## Files

| Path | What it is |
|---|---|
| `scripts/rename_batch.py` | pattern + map → renames; dry run by default, idempotent, refuses to clobber or collide |
| `assets/subjects.example.json` | a real 21-item map, including the note about where the facts came from |

Related skills: **hook-variations** (produces the batch this most often names),
**video-review-canvas** (where the names need to match the cards).
