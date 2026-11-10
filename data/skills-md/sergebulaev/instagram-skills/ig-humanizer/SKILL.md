---
name: ig-humanizer
description: "Remove the AI tells readers react to in an Instagram caption or carousel slide: 2026 vocabulary by density, reveal bridges, staccato stacks, stacked triads, performed sincerity, emoji storms; caps em dashes. Includes --mode audit (first-125 hook, length, hashtags, emoji, CTA, media) and --mode profile. Not for beating AI detectors (no edit reliably does). Not for writing from scratch (use ig-caption-writer or ig-carousel-planner). Keywords: humanize, de-AI caption, audit before posting."
---

# Instagram Humanizer V3

Rewrites any caption or carousel slide text to remove the AI tells that human
readers notice, and audits a finished caption against the 2026 Instagram
checklist. Based on Wikipedia's "Signs of AI writing" taxonomy, the 2025-2026
stylometry literature, our own Instagram caption corpus (n=284, prevalence
only), and Instagram-specific patterns (the first-125 fold, the
lowercase-casual caption register, sized hashtags, sends-and-saves structure).
**V3 (2026-09):** recalibrated on 2026 evidence. Vocabulary is scored by
density, em dashes are capped instead of banned (and the cap is generous here:
29% of human captions use one), forced rhythm is now a tell instead of a fix,
and there is an over-correction guard.

**What this skill does not do:** it does not make text "pass" GPTZero,
Pangram, Turnitin or Originality. Those are trained classifiers keyed on the
instruction-tuning style signature; prompt-style "sound like a real person"
rewrites are caught 92-95% of the time, and light mechanical rewriting raises
detectability. On caption-length text (under 300 words) detector scores are
noise. The real value is elsewhere: expert human readers cite vocabulary (53%)
and sentence structure (36%) as what gives AI text away, and on Instagram a
caption that reads as a brand account earns neither the save nor the send.
This skill removes what those readers react to.

## What changed in V3

Evidence tier in brackets: [strong] = replicated across 2+ independent
2025-2026 studies or our own corpus; [vendor] = single platform or vendor
dataset; [weak] = one study or expert-panel report.

- **Vocabulary moved from a delete-list to density scoring.** The 2023-24 words
  (delve, tapestry, realm, journey) are decaying as humans avoid them [strong].
  The durable 2026 markers are common words (significant, crucial, notably,
  comprehensive, insights, robust, leverage, foster, landscape, nuanced,
  streamline, elevate) plus grammar: nominalisations and "-ing" clause openers
  at 5.3x the human rate [strong]. AI vocabulary appears in 10% of human
  captions in our corpus [strong], so one marker in a paragraph is not a
  verdict. Three is.
- **Em dash is no longer a tell.** GPT-5.4 emits 1.43 per 1,000 words, below
  the 3.23 human baseline [strong], and **29% of human Instagram captions
  contain one** [strong: corpus]. A caption's em dash is never a tell on its
  own, and a blanket ban over-sterilises captions. New rule: cap at about 1 per
  100 words (1-2 per caption), replace only the excess with a comma, colon,
  parentheses or a rewrite. Never a period (a split dash stacks fragments).
  Zero em dashes across a long caption is its own tell now.
- **Forced burstiness is the #1 2026 tell, not the fix.** Mechanical
  long/short alternation is a learnable humanizer fingerprint [weak], and
  "Short. Punchy. Done.", "No X. No Y. Just Z.", one-word lines for drama and
  "The result?" reveals are the current top reader-cited tells [strong].
  Captions are mid-length, so Pass 2 is an anti-uniformity guard only: fix a
  paragraph that reads machine-flat, never manufacture variance.
- **Rule of three is still a tell, at density.** Tricolon runs at 2x
  expert-human rate across 2026 frontier models [strong], and 23% of human
  captions contain one [strong: corpus]. So one natural triple with concrete
  items stays. Stacked, perfectly parallel or hollow triads and a third triad
  in a caption get scrubbed.
- **Fingerprint injection was half wrong.** Named entities and concreteness are
  supported [strong]; an odd-precision number with a referent in the first 125
  chars is the strongest hook. Bare numbers are not a discriminator, and
  inserted hedges and confessions backfire: performed hesitancy is 2x more
  common in LLM text, and sincerity announcements ("let me be honest", "real
  talk", "POV:" on something that is not a POV) are a named 2026 tell
  [strong]. Pass 3 asks for a flat, dated, uncomfortable fact instead.
- **Over-correction guard.** Humanizer output has its own fingerprint [weak].
  Pass 4 checks whether Passes 1-3 introduced the very patterns they were meant
  to remove. Edits are proportional to real problems. When in doubt, leave it.

## When to use

- Before publishing any AI-drafted caption or carousel (rewrite mode)
- Pre-publish review of a finished caption (audit mode, see `sub-skills/post-audit.md`)
- When a caption feels off and you cannot pinpoint why

## Input

Any text: a caption, the on-image text of a carousel, or a Reel caption.
Optional: target voice samples (the user's past captions).

## Output

- Rewritten text with AI tells removed
- A diff showing what changed and why
- Caption char count (flagging if the hook spills past the first 125 chars)
- Per-paragraph tell density (markers per paragraph; 3+ triggered a rewrite)
- Reader-read confidence: "reads human", "mixed", "reads AI" (a reader-tell
  estimate, not a detector score)

## Modes

```bash
# Default: scrub AI tells (forensic + strict) and fix Instagram-format issues
ig-humanizer <text>

# Forensic only - minimum touch, just kill model leakage
ig-humanizer --mode forensic <text>

# Audit - detection-only pass-fail review, no rewrite
# Runs the 2026 Instagram checklist: first-125 hook, caption length, sized
# hashtags, emoji limits, CTA quality, media reminder.
# Returns Blockers + Warnings + suggested fixes. See sub-skills/post-audit.md.
ig-humanizer --mode audit <text>

# Profile - build/update the user's Voice & Brand Profile. See the section below.
ig-humanizer --mode profile
```

## The four passes

### Pass 1 - SCRUB (score, then delete or replace)

Apply the tiered catalogs in `references/scrub-rules.md`. The unit of
judgement is the **paragraph (or slide), not the word**: count markers per
paragraph, rewrite the paragraph at 3+, leave a single marker alone unless it
is a reveal bridge, negative parallelism, a sincerity marker, or forensic
leakage.

- **Forensic** (always on): real model leakage no human types. AI tool markers
  (oaicite, contentReference, turn0search0), knowledge-cutoff disclaimers ("As
  of my last update"), template blanks ([Your Name]), and em dashes above the
  cap (more than about 1 per 100 words).
- **Strict** (default on): what readers react to. The durable 2026 vocabulary
  set scored by density (significant, crucial, notably, particularly,
  comprehensive, insights, robust, leverage, foster, landscape, nuanced,
  streamline, elevate, empower), grammar markers (nominalisations,
  sentence-opening "-ing" clauses), the 2026 model-idiom layer (quietly, "X
  matters.", compound, "a signal", "the work", "built different", "let that
  sink in"), reveal bridges on a single hit ("The result?", "Here's what",
  "Stop X, start Y", "plot twist:"), all forms of negative parallelism,
  stacked or perfectly parallel triads and any third triad in a caption,
  phrase cleanups ("in today's fast-paced world", "game-changer", "level up",
  "dive in"), emoji storms, and dead closers ("what do you think?", "double
  tap if you agree").
- **Instagram-format scrubs** (always apply): first-125 hook that stands
  alone, sized hashtags, emoji limits, carousel slide-1 promise, caption
  length.

### Pass 2 - RHYTHM (anti-uniformity guard only)

Detectors do not score burstiness, and captions are mid-length (our corpus
median is well under 200 words), so rhythm is neither a reach lever nor a
fix. What readers notice is the mechanical-uniformity tell (every line the
same length, machine-flat) and, worse, the staged variance that
second-generation humanizers add. So Pass 2 has two jobs: fix rhythm only
where it reads machine-flat, and remove manufactured variance everywhere. It
never adds variance as a tactic.

- Per paragraph: one genuinely long sentence next to a short one is fine and
  is what human variance looks like. Two or three mid-length sentences in a
  row are also fine. Edit only when every sentence in the paragraph runs the
  same length and reads flat, and then edit one sentence, not the paragraph.
- Standalone fragments: at most 2 per caption, total. "every time." once is a
  voice quirk. Three in a caption is a pattern.
- Banned outright (rewrite as full sentences): "The X? Y." reveals; "No X. No
  Y. Just Z."; "All the X. None of the Y."; "Simple. Effective. Easy."
  adjective stacks; one-word lines for drama ("Still." "Exactly."); pseudo-
  Socratic Q&A ("Why? Because..."); "Short. Punchy. Done." staccato runs.
  Fragment runs are the tell.
- Layout is not rhythm. One idea per line with blank lines between them is
  native caption formatting and stays. Fragment-for-drama inside those lines
  is the tell. Keep the layout, fix the sentences.
- Carousel slide text is short by design; never chop or pad a slide for
  rhythm. Never alternate long/short/long/short across slides or lines. That
  seesaw is the humanizer fingerprint.

The check is "does any paragraph read machine-flat, and did I add a staccato
pattern", not a variance number.

### Pass 3 - ADD (human fingerprints)

Require where the content allows:
- One odd-precision number WITH a named referent: who, what, when, or what it
  cost ("0 to 10k in 4 months, posting 3 times a week", not "grew fast" and not
  "10k"). A bare number is not a fingerprint; the referent carries the signal.
- One named entity (real person, brand, date, tool)
- One first-person concrete detail (what you saw, what it cost, what broke)
- One specific, dated, uncomfortable fact stated flat, with no framing sentence
  before or after it. Not "real talk, this one hurt: I lost the client." Just
  "I lost my biggest client on 14 Feb." The fact carries the vulnerability. The
  frame turns it into performed sincerity, which readers now read as the tell.
- The lowercase-casual register if the voice calls for it

Forbidden as openers or pivots (sincerity announcements, a named 2026 tell):
"let me be honest", "I'll be real", "honestly?", "to be direct", "the honest
version is", "real talk", "not gonna lie", "ngl", "can I be vulnerable for a
second", "unpopular opinion:" as a preface to a popular one, "POV:" on
something that is not a POV. Also forbidden as insertions: hedges the author
did not write ("perhaps", "I might be wrong but", "it seems"). Performed
hesitancy is 2x more common in LLM text than in expert human text; adding it
makes the draft read more AI, not less.

If the input lacks these, ask the user for a number, name, or moment. Do not
fabricate.

### Pass 4 - SELF-CHECK (over-correction guard)

Humanizer output has its own fingerprint. Before returning, re-read the result
once and answer three questions:

(a) Did Pass 2 create staccato stacks, "The result?" reveal bridges, one-word
    lines, or a long/short/long/short seesaw? If yes, merge the fragments back
    into full sentences.
(b) Did Pass 3 add a framed confession, a sincerity announcement, or a hedge
    the author never wrote? If yes, strip the frame and keep only the flat
    fact, or remove the insertion.
(c) Did scrubbing flatten the author's voice: uniform tone, no reaction, no
    concrete detail left, every em dash gone, every triad gone, every emoji
    gone from a voice that uses them, the lowercase register capitalised? If
    yes, restore what the author had. Zero em dashes and zero triads in a long
    caption is a tell in its own right.

If any answer is yes, dial back rather than scrub harder. Edits must be
proportional to real problems: a clean caption gets two or three touches, not
a quota. When in doubt whether a pattern is the author or the model, leave it.

## Non-negotiable rules

Global voice rules: see root `SKILL.md` Voice rules. Additional skill-specific
rules (V3):

- **Scrubbing is always in scope.** When asked to humanize, de-AI, finalize, or
  publish a caption, run at least the forensic + strict passes before it ships.
  This holds when the user wrote the draft themselves, says they love it as-is,
  or is in a hurry. Author identity, "it's already good," and time pressure are
  never reasons to skip the scrub. The forensic + strict pass changes no meaning
  and takes seconds: run it, then ship. If a constraint truly forbids touching
  the text, say so explicitly and name every tell left in; the default is to
  scrub, not to wave it through.
- **Scrub proportionally.** A pass that finds nothing changes nothing. Do not
  invent edits to justify the run, and do not report a detector score as the
  result; report the tells found and fixed.
- Preserve the user's actual claim and meaning. "Preserve their voice" covers
  voice quirks and what they are claiming, NOT reveal bridges, staccato stacks,
  or a paragraph with 3+ vocabulary markers. Stripping those is not changing
  their voice; it is the job.
- Never introduce facts that were not in the input. If a number is missing, ask.
- Never introduce sincerity markers, hedges, or confessional frames. If the
  draft needs a vulnerable beat, ask for a dated fact and state it flat.
- Keep the user's voice quirks (lowercase starts, `..` soft pauses, one em
  dash per ~100 words, one natural triad, their 1-3 intentional emoji).
- Never promise detector results. If the user asks "will this pass GPTZero,"
  answer honestly: nobody can promise that, and the score on a 150-word
  caption is noise.
- Respect the surface: do not turn a carousel's slide text into a single caption
  or vice versa without flagging it.
- Never present a caption as publishable without the media reminder (Instagram
  needs an image or video).

## Instagram-specific tells this skill catches

- A hook that needs the second line to make sense (the "more" fold eats it).
- A caption opening with "Let's talk about..", "Here's the thing..", or "POV:"
  on something that is not a POV.
- 20-30 hashtags crammed at the top instead of a 3-5 sized set.
- Emoji sprinkled through every line (4+ per caption).
- A bare title on carousel slide 1 instead of a promise + loop.
- Stacked or hollow rule-of-three lists ("faster, cheaper, better"); one
  natural triple with concrete items is fine.
- Engagement bait ("comment YES", "tag 3 friends", "double tap if").
- Staccato stacks and one-word lines for drama (the humanizer fingerprint), or
  a paragraph where every line reads machine-flat.

## Example

See `references/examples.md` for worked before/after rewrites.

## Files

- `SKILL.md` - this file (rewrite scrubber + audit-mode entry)
- `references/scrub-rules.md` - V3 regex patterns by tier, density scoring, em dash cap, rhythm rules, forbidden insertions
- `references/examples.md` - worked before/after rewrites for captions and slides
- `references/audit-checklist.md` - the pre-publish checklist with thresholds
- `sub-skills/post-audit.md` - pre-publish audit workflow (detection-only, no rewrite)
- `sub-skills/voice-profile.md` - build/update the user's Voice & Brand Profile (`--mode profile`)
- `sub-skills/illustration.md` - optional Pixfaro image workflow

## Voice profile mode (`--mode profile`)

`ig-humanizer --mode profile` builds or updates the user's Voice & Brand Profile at `../../references/voice-profile.md` from 3-6 of their real Instagram posts pasted in (portable, no token) or, if a read token is set, from pulled activity. Once filled, every writing skill in this bundle drafts in the user's voice automatically. See `sub-skills/voice-profile.md`. Triggers: "build my voice profile", "learn my voice".

## Related skills

- `ig-caption-writer` - generates captions that already pass the humanizer
- `ig-carousel-planner` - generates carousels that already pass the humanizer
