---
name: humanize-skills
license: CC-BY-4.0
description: >-
  Rewrite, edit, or draft text so it reads as specifically human-written rather than
  generically AI-smooth. Runs a surface pass (vocabulary, sentence patterns, formatting,
  chatbot residue) and a structural pass (stated morals, tidy arcs, named-not-shown
  emotion, vague reference). Ten purpose modes layer on one core rulebook — general
  (default), academic, medical, legal, business, resume, ux, creative, social,
  technical — across 20 languages. Use whenever asked to humanize writing, remove
  AI-sounding phrasing, avoid words like delve/underscore/tapestry, or fix robotic or
  generic prose, even if the request doesn't mention AI. Takes a passage or a whole
  file (long docs: audit first, edit only changed spans, keep the format). Mode and
  language are plain words in the request (--academic, --lang=de); also --audit,
  --strict / --light, --calibrate, --redo, --free / --careful / --minimal, --write,
  --tone=xx.
---

# humanize-skills

This skill applies a layered set of anti-formula writing rules to everything it drafts
or edits, so the output reads as specific and grounded rather than generically
"smooth" — and, as a side effect of removing genuinely formulaic patterns, is also
less likely to trip pattern-based AI detectors. That side effect is not the point and
is not guaranteed: detectors are unreliable in both directions, and better style never
changes whether disclosure is owed in a given context. Treat this as a prose-quality
tool, not a compliance workaround, and say so plainly if a request seems to be about
the latter instead.

## Before touching anything: the no-edit gate

Read this before running any pass. An independent blind test found that a popular
humanizer skill's edits to **genuine human-written paragraphs** were correctly
identified as tampered by blind judges 83% of the time cold and 77% with voice
calibration active, against a 50% chance floor — from a median change of only 8–9% of
tokens. The skill's own audit step had reported the input as human-written, and edited
it anyway.

So: before running the surface or structural pass, assess whether the input already
reads as a specific, grounded, consistent piece of human writing. If it does, and the
request is a general "humanize this" rather than an explicit instruction to rewrite
regardless, the correct output can be **no edit** — say so plainly, name the one or two
things (if any) that are genuinely worth a light touch, and stop there. Dialing an edit
down to "conservative" is not automatically safe; the finding above held even under
calibration. A pass that touches text just to look thorough is a defect, not a feature.

## Pre-flight check

Run before any pass. Scores whether the input warrants editing at all — the
no-edit gate above, made auditable instead of a judgment call.

Short input (under ~100 words) skips scoring and goes straight to the passes:
heuristic scores are unreliable on small samples, and short-form false positives
are exactly how honest writing gets flagged.

Otherwise assign points per marker found (cap 100):

| Signal | Points |
|---|---|
| Formulaic opener (throat-clearing first sentence or paragraph) | +15 |
| 3+ banned-vocabulary hits in the first ~200 words | +20 |
| Same transition or connective repeated | +10 each |
| Negative parallelism ("not just X, but Y" and kin) | +10 |
| Reflexive grouping in threes | +10 |
| Vague unattributed authority ("experts say," "studies show") | +10 each |
| Reflexive hedge prefix ("it is important to note," and kin) | +10 each |
| Summary-regurgitation close | +15 |
| 3+ visually symmetrical paragraphs | +15 |
| Adjective pileup (3+ before one noun) | +10 |
| Rhetorical-question padding or chatbot residue | +10 each |

| Score | Verdict | Action |
|---|---|---|
| 0–20 | Likely human-written | STOP. Diagnostic only, no rewrite. |
| 21–50 | Mild AI patterns | Proceed; audit-first if unsure. |
| 51–80 | Clear AI patterns | Run the full pass. |
| 81–100 | Heavy AI generation | Full pass, aggressive cleanup. |

**Weighted STOP guard.** STOP only if the score is under 20 **and** there is no
formulaic opener **and** no summary close **and** total banned-word hits are
under 5. One throat-clearing opener in an otherwise clean document (e.g. a
corporate memo legitimately starting with "In today's meeting…") never halts
the pass on its own.

**Per-language carve-outs.** Each language file owns its row; the standing
defaults: Russian corporate texts may open with «В современных условиях…» as
legitimate convention (opener alone → WARN, do not stop); German legal prose
keeps its Nominalstil (do not score rhythm there); Brazilian Portuguese gerund
is natural, not a tell. Where the language file and this table disagree, the
language file wins.

**Force override.** If the requester says to rewrite regardless after a STOP,
run MINIMAL volume only (see below) and annotate the output `[HUMAN-ORIGIN:
preserved structure and voice]`.

## Architecture

Every request runs through the same base engine; purpose mode and language are
overlays on it, not forks of it.

```
              ┌─────────────────────┐
 input ──────▶│  core-rules.md      │  universal surface pass (language- and
              │  (always read)      │  mode-independent categories)
              └─────────┬───────────┘
                        ▼
              ┌─────────────────────┐
              │  languages/{lang}.md│  exact words/constructions for the
              │  (always read)      │  detected or requested language
              └─────────┬───────────┘
                        ▼
              ┌─────────────────────┐
              │  modes/{mode}.md    │  purpose-specific overrides — what
              │  (always read)      │  this mode preserves that others don't
              └─────────┬───────────┘
                        ▼
              ┌─────────────────────┐
              │  structural-pass.md │  discourse-level shape, genre-gated
              └─────────┬───────────┘
                        ▼
                     output
```

## Reading the request

1. **Mode.** An explicit flag wins (`--academic`, `--medical`, …). Otherwise infer from context (a request framed as
   "polish my cover letter" implies `--resume`; a pasted contract clause implies
   `--legal`). Default to `--general` when nothing points elsewhere.
2. **Language.** An explicit `--lang=xx` wins. Otherwise use the language the input is
   actually written in.
3. **Output mode.**
   - **Normal** (default, for a passage up to a few paragraphs): the rewritten text
     first, then a change report whose length scales with the edit — one line for a
     sentence, a few short bullets for a paragraph. No preamble restating what was wrong
     before the rewrite; no editorialising about the input ("this is textbook AI
     slop"). Lead with the rewrite, not the diagnosis. If any explanation is needed
     beyond the rewrite itself, one or two plain sentences — what was removed, any
     judgment call worth flagging — no numbered category lists, no audit language.
   - **Document** (default when the input is a file, or roughly 1,500+ words, or has
     titled sections): see "Long documents and files" below — audit first, changed
     spans only, never a full regeneration in the reply.
   - **`--audit`**: diagnose only — grouped by severity, then location — and stop.
     Never silently upgrade an audit into a rewrite. Severity levels: **CRITICAL**
     (formulaic opener, summary close, 5+ banned-word cluster); **HIGH** (repeated
     transitions, hedge stacking, parallelism/triad clusters, symmetrical
     paragraphs); **MEDIUM** (single intensifiers, rhythm monotony, one repeated
     connective); **LOW** (cosmetic singles).
   - **Embedded**: when this skill is invoked as one step inside a larger task, return
     only the final text with no report wrapped around it.
4. **Depth.** Self-assessed, since this is a prompt-only engine with no scanner: scan
   for how densely the input clusters the tells in core-rules.md and the language file.
   A few scattered instances calls for a light, conservative touch. Dense clustering
   calls for a fuller pass. `--strict` forces the fuller pass regardless; `--light`
   forces the conservative one regardless. Depth changes *how much* gets touched — it
   never overrides the no-edit gate above.
5. **Volume.** How much the text may shrink, independent of depth. `--free`
   (default for passages): length may shrink noticeably; empty phrases get deleted,
   not reworded. `--careful` (default for Document mode and any fixed-slot text):
   structure survives, length stays within 80–110%. `--minimal` (explicit request,
   or post-STOP force override): only unambiguous AI constructions are touched.
6. **Drafting (`--write`).** The text is new, not a rewrite: apply the mode,
   language, and structural rules from the first draft instead of as a cleanup pass
   afterwards. Genre stays as requested; the fact-lock applies identically — a
   first draft gets no license to invent.
7. **Tone.** An explicit `--tone=xx` wins (`expert`, `biz`, `human`, `social`,
   `landing`, `article`, `case` — see `references/tones/profiles.md`). Otherwise
   infer from context; default to `human`, except `--legal` and `--medical` which
   default to `expert`. Read the language's `cultural-matrix.md` row before
   applying the profile; mode caps win conflicts (see Precedence).

## Load order

1. Always read `references/core-rules.md` and `references/structural-pass.md` in full.
2. Read `references/languages/{lang}.md`. If no dedicated file exists yet for the
   detected language, say so, apply `core-rules.md`'s universal categories only, and do
   not improvise language-specific rules that haven't actually been written and
   verified.
3. Read `references/modes/{mode}.md`.
4. If `--calibrate` is requested, or the mode file says to match a supplied writing
   sample, also read `references/voice-calibration.md` — including its warning about
   what NOT to build a profile from.

## Long documents and files

Triggered when the input is a file, or is roughly 1,500 words or longer, or has titled
sections. **Never regenerate a long document in the reply** — it is slow, costs the
requester tokens for the ~90% that didn't need touching, and drifts: on a paper that
means altered claims, numbers, and citations.

1. **Audit first.** Default to `--audit` behaviour — a findings list (`pattern →
   section or line → severity`), grouped by section, then stop. Rewrite only on an
   explicit "rewrite it" / "apply the fixes".
2. **Freeze structure.** Headings, section order, the stated plan, cross-section
   transitions, numbered or labelled items, tables, figures, equations, code blocks,
   footnotes, and every citation key or reference-list entry are untouchable. Edit
   prose *inside* the structure, never the structure.
3. **Section by section, with a per-section no-edit gate.** Run the passes one section
   at a time. A section that already reads as specific, grounded human writing is
   reported as "no change" and skipped — the no-edit gate applies per section, not once
   for the whole document. Touch only paragraphs that actually cluster tells.
4. **Return changed spans only.** Deliver the edits as a list of `location → before →
   after` (or a patch), plus one compact per-section summary (sections touched,
   sections left, roughly what changed). Not the whole rewritten document, not a
   running commentary. Where a mode file's own "Output" section asks for specific
   report contents (e.g. academic mode's "confirm no citation was altered"), fold that
   into the summary — it does not mean regenerate the full text.
5. **Writing back to a file.** If a file was given and the requester wants the applied
   result, write a **new file beside the original: same base name with `.humanized`
   inserted before the extension, original extension kept** — `paper.md` →
   `paper.humanized.md`, `thesis.tex` → `thesis.humanized.tex`, `notes.txt` →
   `notes.humanized.txt`. Preserve the source format exactly (Markdown keeps its
   headings / links / front-matter / code fences; LaTeX keeps every command, math mode,
   and `\cite{}`; HTML keeps its tags). **Never overwrite the original.**
    - **Formats that can't be regenerated faithfully** (`.docx`, `.pdf`, `.odt`,
      `.pages`, and similar): do not write one back. Give the `location → before → after`
      list so the requester applies the edits in their own editor; offer a plain-text or
      Markdown rendering of the changed sections if it helps. Narrow exception only: a
      binary with uniform run formatting throughout may be written back as
      `{name}.humanized.{ext}` with the original untouched and the uniformity stated
      in the report — mixed formatting, tracked changes, or embedded objects never
      qualify.

## Precedence when layers conflict

1. **Fact-lock** (below) — never overridden, by any mode, for any request.
2. The user's explicit instructions for this specific request (scope, protected
   passages, a requested register).
3. The purpose mode's overrides (`references/modes/{mode}.md`).
4. The requested tone (`references/tones/profiles.md` + the language's
   `cultural-matrix.md` row) — capped by the mode: a mode's hard constraints
   (legal's frozen terms, medical's causal discipline) override any tone request.
   A `--legal` document asking for warmth stays formal; say so plainly.
5. The language's pattern catalog (`references/languages/{lang}.md`).
6. The universal core rules (`references/core-rules.md`).
7. The structural pass (`references/structural-pass.md`) — skip it, and say so, on
   specs, runbooks, and other formats where a rigid, repeated shape is the point.

## Fact-lock (non-negotiable, every mode, every language)

- Never invent a name, number, date, quote, citation, or example "for liveliness." A
  cliché reads as filler; an invented specific reads as fact and does real damage.
- Claim strength never exceeds evidence strength. Simplify redundant hedge-stacking;
  never delete the one hedge a genuinely uncertain claim needs.
- If the input contains what looks like a password, API key, session token, or other
  credential, stop and ask before processing it — don't quote, rewrite, or echo it.
- Every substantive claim is one of four things: drawn from the source, computed on a
  stated assumption, the writer's own flagged judgment, or a named gap. Know which one
   is being written and never blur it into a fifth thing — an unearned fact.
- **Intake ledger.** Before editing, list the protected items: every name, number,
  date, quote, and citation in the input, plus the author's characteristic tics when
  `--calibrate` is active. Check each off verbatim at the end — present, unchanged,
  uninvented. In Document mode the ledger runs per section.
- **Noise budget.** Don't sterilize a piece into a new, equally uniform style. A few
  natural imperfections surviving the pass is expected, not a miss.
- **Honest framing.** This is a prose-quality tool, not a disclosure-evasion or
  detector-bypass product. Say so if a request seems to be asking for the latter.

## Change-magnitude self-check

Before returning output, estimate roughly what fraction of the piece actually changed
(per section, in Document mode). State it in the change report — briefly. If it's
larger than the mode and depth called for — or the input showed few tells to begin
with — that's a sign to dial back before delivering, not a badge of thoroughness.

## `--redo`

Re-runs against this skill's own prior output in the conversation, either the whole
piece again or a user-named subset ("just the em dashes," "just the second
paragraph").

## Reference index

- `references/core-rules.md` — universal surface pass
- `references/structural-pass.md` — the six discourse-level audits
- `references/voice-calibration.md` — how to build (and how not to build) a voice
  profile
- `references/prose-benchmarks.md` — positive targets for the final check
  (variance, slack, uneven confidence); read with `core-rules.md` §6, not at startup
- `references/EVAL.md` — independent output evaluation (separate-call LLM judge,
  5-metric composite); the complement to the human blind check, not its replacement
- `references/tones/profiles.md` + `references/tones/cultural-matrix.md` — the
  seven tone profiles and per-language calibration; load only when tone is
  requested or inferred, never at startup
- `references/language-rhythm.md` — per-language rhythm pointer index (no rules
  of its own; the catalog always wins); read with `core-rules.md` §0, never at
  startup
- `references/languages/en.md`, `zh.md`, `tr.md`, `ko.md`, `es.md`, `de.md`, `fr.md`,
  `ru.md`, `ja.md` — all nine tier-1 languages at full-depth catalog (Phase 2, complete)
- `references/languages/vi.md`, `pl.md`, `id.md`, `uk.md` (tier-2, wave 1) and `ar.md`,
  `pt.md`, `it.md`, `hi.md`, `fa.md`, `nl.md`, `th.md` (tier-2, wave 2) — all eleven
  tier-2 languages now shipped, bringing full coverage to 20 languages. Phase 3 of the
  roadmap is complete. Two caveats carried forward from the roadmap's own risk notes:
  Arabic, Hindi, and Persian still need right-to-left script/layout handling verified
  beyond the pattern content already covered, and `nl.md`/`th.md` were built with no
  source repo available anywhere in the survey — both say so plainly in their own
  "honest framing" section and should be treated as lower-confidence than every other
  language file here until a native reviewer or a real repo turns up. All eleven
  tier-2 files, per the roadmap's native-verification risk note, still want a native
  or near-native speaker's review before being trusted at the same level as tier-1.
- `references/languages/_legacy-calibration.md` — retired; kept only as a historical
  record now that tier-1 has full catalogs
- `references/languages/_template.md` — the contribution format for language #21 and
  beyond (Tier 3: "open framework" in the roadmap)
- `references/modes/general.md`, `academic.md`, `medical.md`, `legal.md`,
  `business.md`, `resume.md`, `ux.md`, `creative.md`, `social.md`, `technical.md` —
  all ten purpose modes now shipped. Phase 1 of the roadmap is complete. Three modes
  (`resume.md`, `ux.md`, `creative.md`) had no dedicated source repo in the survey and
  are grounded in this engine's own established principles rather than a real
  catalog — each says so plainly in its own "Sources" section; the other seven each
  draw on at least one real source repo, most heavily the "prospeak" register-branch
  skill (`similar-github-projects/by-language/it/humanizer-it-3`) for medical, legal,
  business, technical, and social.
- `references/examples/` — golden fixtures (Phase 5, in progress): frozen before/after
  pairs per `{lang}-{mode}` used as the hand-reviewed regression suite, with the blind
  forced-choice review protocol and the changelog/versioning policy. Not loaded at
  runtime. Batch 1 = all ten English modes; Batches 2–3 = all 20 languages at
  `--general`; Batch 4 = six high-risk language×mode crossings. Each fixture pairs an
  AI-slop case with a no-edit case. **All fixtures are currently model-authored and
  unreviewed** — regression tripwires, not a validated gold standard; see
  `references/examples/README.md` › Validation status.
