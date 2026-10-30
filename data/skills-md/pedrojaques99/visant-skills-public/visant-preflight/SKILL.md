---
name: visant-preflight
description: 'Preflight for a large client project: one question round with whoever owns the work, plus five premise checks (brand source of truth, loadable fonts, photo resolution, brand files, sourced numbers). Use BEFORE "new site", "redesign", "new proposal", "criar site", "redesenhar", "nova proposta", "montar campanha", "hidratar a marca".'
---

# Visant Preflight

Projects rarely go wrong in execution. They go wrong **in the premise**: the work
comes out well made on top of data that was wrong from the start, and the rework
costs days.

> **Nothing large starts without two things: the question round answered, and
> the five checks green or explicitly waived.**

The whole preflight takes 15 minutes. Each mistake it prevents has already cost
more than a day. The long stories are in [references/cases.md](references/cases.md).

## When to run

Run it when the task is **big enough to hurt**: new site, redesign, proposal with
mockups, campaign, brand hydration, migration. Signal: more than half a day of
work before the first client feedback. Not for a one-off tweak: preflight on a
small task is bureaucracy and you will (rightly) stop running it.

---

## Part 1: the question round

**This part is not optional and cannot be automated.** It is the one most often
missing.

Before designing anything, ask the questions below **to whoever owns the work**
(client, account lead, project owner) and write down the answers. Assume none.
If they answer "whatever", write "whatever": that is an answer too, and it turns
into explicit freedom instead of a silent bet.

Use the harness question tool for closed choices; use conversation for open
ones. **Do it in ONE round**, not drip-fed through the work: a question asked
mid-work always arrives after the rework it would have prevented.

### 1.1 The bet

- **What is the single sentence this work must prove?** If it does not fit in a
  sentence, the scope is not closed yet.
- **Which business variable does it move?** Conversion, retention, ticket, cost
  per meeting. If it moves none, it is decoration, and decoration costs
  attention.
- **Who is on the other side, and at what awareness stage do they arrive?**
  (Schwartz, see `revenue-centric-design`.) The headline speaks to the current
  stage; proof pushes one stage further.
- **What is NOT to be done?** The question that saves the most time and that
  nobody asks.

### 1.2 Reference and taste

- **Is there something the client already approved** (layout, piece, campaign)
  that I should inherit instead of reinventing? Mine before designing.
- **Is there something they hate?** Worth more than ten references they love.
- **What in this brand is untouchable?** A "clean" version that swaps the brand's
  own graphic language for a conventional one gets reverted in one sentence.
- **How much density, and do photos go in this round?** Three full proposals
  rebuilt over "too much text, no images" is the classic cost of skipping this.
- **How many alternatives do they want to see?** One polished or three distinct
  bets. Different jobs; agreeing first avoids delivering the wrong format.

### 1.3 What blocks publishing

- **What still depends on a third party?** Copy, photo, number, legal, domain.
- **Which of those is on the critical path?** It sets the work order: start with
  what depends on no one.
- **Is there a regulatory constraint?** (Professional councils, health agency,
  securities, privacy law such as LGPD.) Finding out after the layout is done
  means redoing the layout.

### 1.4 Definition of done

- **Where will this be seen?** Published link, PDF, Figma, call. Changes
  everything.
- **Is it going live or is it a proposal?** If a proposal, `noindex` and no
  sensitive real data.
- **When is the feedback conversation?** Sets the depth.

> **Required output of Part 1:** the answers written in the project's `.md`,
> before the first line of code or the first frame. An answer that stayed only in
> the conversation becomes an assumption next week.

---

## Part 2: the five checks

The two middle ones (fonts and photos) are automated:

```bash
node ~/.claude/skills/visant-preflight/scripts/preflight-scan.mjs \
  --assets "<client files folder>" \
  --fonts "Display Family,Body Family" \
  --report PREFLIGHT.md
```

The script is plain node, no dependencies, and needs nothing Visant-specific:

| flag | what it does |
|---|---|
| `--assets <dir>` | walks any local folder (synced Drive, Dropbox, a repo's `public/`) and lists every `.png .jpg .jpeg .webp .avif .gif .svg` with width, weight and the role it supports. PNG, JPEG and WebP are measured; SVG is listed as vector; anything whose header it cannot read goes to a "skipped" list with the reason |
| `--fonts "A,B"` | checks each family against Google Fonts (needs network; offline shows as undetermined) |
| `--report <file.md>` | also writes the output to a markdown file |
| `--strict` | exit 1 if any item fails (no image reaches 2000px, or a font is missing from Google Fonts or could not be checked) |
| `--self-test` | validates the script's own parsers and thresholds |

At least one of `--assets` or `--fonts` is required; with neither it prints
usage and exits 2. Output is in English (a markdown report: photography table, skipped list, fonts table).

### 1. Brand source of truth: do the copies agree?

Wherever your brand data is stored for reuse (a brand vault, a tokens file, a
guidelines doc; at Visant, the Visant Labs vault) **is not the truth, it is a
copy**, and copies age or are born wrong. Cross it against the files actually
delivered to the client (the brand folder in Drive or wherever it lives) and the
design file (Figma).

Check in this order: **typography, colors, logo, tagline.** When they disagree,
the folder the client received is stronger evidence than the stored field.

To audit and reconcile Visant's vault, load **[[visant-brand-sync]]**.

> A stored typeface the brand never had shipped as three wrong typefaces over
> months, because nobody opened the client's font folder. See
> [references/cases.md](references/cases.md#1-brand-source-of-truth-client-k).

### 2. Do the fonts load?

Automated in the script. A family not on Google Fonts is not necessarily wrong:
a paid, licensed face is a legitimate decision. What cannot happen is for it to
**vanish silently**: either you have the file and load it via `next/font/local` /
`@font-face`, or you change the family.

Telltale symptom: the layout "is right" but the site looks like another brand.

> If the project consumes Visant's `@visant/brand-tokens`, the token engine
> already checks this at the source: it emits `@import` for what can load and
> **declares** at the top of the CSS what cannot.

### 3. Can the photography carry the layout?

Automated in the script. It lists **every** image with resolution and the role
it supports, and says explicitly what it skipped.

| Role | Minimum file width |
|---|---|
| Full-bleed band | 2000px |
| Hero portrait | 1000px |
| Grid cell | 700px |
| Thumb | 400px |

**Choose the source by resolution BEFORE deciding the framing**, never the other
way round. Upscaling shows, and no layout choice makes up for a small file.

Hence the script's rule: **never filter silently.** A scan that hides is worse
than a scan that does not run, because it produces false confidence, and false
confidence becomes a verdict. The case of the hidden 4562px originals:
[references/cases.md](references/cases.md#2-photo-resolution).

### 4. Do the brand files really exist?

Logo in **vector** (SVG/PDF), not a presentation PNG. Light/dark variants. Square
icon for the favicon. The brand's own graphic elements.

If they do not exist, **do not redraw the brand**: ask for them. A logo redrawn
by approximation is the most expensive failure and the hardest to reverse.

### 5. Does every number have a source?

Every piece of data going live needs its origin noted next to it, in the content
file. A number lifted from a layout **is not a primary source**: it goes up
marked as pending, or it does not go up.

> A number that does not hold up is not proof, it is liability. When the client
> asks where it came from, the answer has to travel with the data, not in the
> memory of whoever assembled it.

---

## Part 3: scars, do not reintroduce the bug you already killed

A visual defect fix **lives in the code as a comment at the fix site**, with the
why. And there is a specific way to lose it: **rewriting the whole file**, which
starts from the new intent and not from the old file.

Two rules, and they are cheap:

1. **Before rewriting a file completely, read it and list the defensive
   comments** (the ones saying "opaque bg is required", "measured in browser",
   "do not swap for", "without this X breaks"). Carry each one to the new
   version, or justify in writing why it no longer applies.
2. **Every fix found in the browser becomes a line in the Scars section** of the
   project's `.md`. It is what survives the rewrite and a change of hands.

```markdown
## Scars
- The bar field belongs to the hero: the proof band needs an opaque `bg`, or the
  decoration cuts through the number. (measured, 08-13)
- Light nav over a light field disappears. Two-tone nav → logo + action only.
- Photo: choose the source by resolution BEFORE framing.
```

**Why it did not become an automatic detector:** a line-based rule cannot tell
the real case from dozens of legitimate edges. A detector that shouts out of
scope is one people turn off; a written scar costs one line and has no false
positives. The story: [references/cases.md](references/cases.md#4-the-scar-that-reopened).

---

## The report

The preflight ends in a block in the project's `.md`:

```markdown
## Preflight: <date>

**The bet:** <the single sentence>
**Variable:** <what it moves>
**Not to be done:** <what was left out>
**Delivery format:** <link / proposal / PDF>, feedback on <when>

| Check | Status |
|---|---|
| Brand source of truth | ✅ / ⚠ <what diverged> |
| Loadable fonts | ✅ / ⚠ <family and plan> |
| Photo resolution | ✅ ceiling <N>px / ⚠ <what cannot be done> |
| Brand files | ✅ / ⚠ <what is missing> |
| Sourced numbers | ✅ / ⚠ <what is pending> |

**Critical path:** <what blocks publishing and who it depends on>
```

A ⚠ does not stop you from starting. It stops you from **pretending it does not
exist**, and sets the order: what does not depend on the blocked item goes first.

---

## Golden rule

**Every check here was born from a mistake that already happened.** A sixth only
goes in after it costs someone a day. One that catches nothing for a whole year
comes out: a checklist that never flags trains people to sign without reading.

## Neighbors

- **[[visant-brand-sync]]**: reconcile the vault when the preflight finds a divergence
- **[[visant-new-site]]**: the client site flow, which starts with this preflight
- **[[revenue-centric-design]]**: awareness stage, ICP, proof
- **[[visant-frontend]]**: classify the surface after the preflight passed
- **[[visant-killer]]**: the exit gate at the end; this is the entry gate
