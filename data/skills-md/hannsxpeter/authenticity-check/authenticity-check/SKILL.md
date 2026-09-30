---
name: authenticity-check
description: >-
  Score how authentically text reads as a real human author's work, flag
  spans that read as AI-generated, AI-templated, or generically derivative,
  and run a separate read-only scan for suspicious Unicode provenance
  carriers. Return an authenticity band, a 0-100 score, provenance signals,
  and span-level reasons. Use when a user asks whether text is authentic,
  reads like AI or a bot, sounds human, contains machine-written spans, still
  sounds like them or a named author, or contains a hidden AI watermark,
  invisible Unicode, or provenance mark. Trigger on oblique evaluative cues
  even when the skill is not named. This skill is diagnostic only: never
  rewrite, edit, remove or normalize marks, or fix prose. Do not use for
  transformative requests such as humanize, de-slop, de-AI, rewrite, fix,
  remove marks, or make it sound like someone.
allowed-tools: Read, Glob, Grep
metadata:
  version: 1.2.1
  compatibility: claude-code, cursor, codex, antigravity, gemini-cli, pi-coder, opencode, copilot, windsurf, cline, continue, zed, aider
---

# Authenticity Check

Read a piece of text and report how authentically it reads as the work of a
person, then point at the exact spans that do not. The deliverable is a
judgment plus evidence: an authenticity band, a 0-100 score, a separate
Unicode provenance preflight, and a list of flagged spans with the reason each
one reads as AI-generated, AI-templated, or generically derivative. The goal
is an honest read a careful human editor would agree with, not a number tuned
to beat any particular detector. This skill names and targets none.

This is the evaluative half of a pair. The other half, the `humanizer` skill,
is a separate repository that rewrites prose. This skill diagnoses; it does
not rewrite. See "Diagnostic only" below for why that boundary is hard.

## When to use this

Use it when someone wants to *know* something about a text rather than change
it: "is this AI," "does this read like a real person," "how human does this
sound," "which parts sound machine-written," "rate the AI-ness," "audit this
draft for AI tells," "does this still sound like me," or "does this pasted
text contain a hidden AI watermark or invisible Unicode." Use it even when they
do not say "authenticity check" and even when the cue is oblique ("does this
sound like a bot," "something about this feels generated, can you tell"). It
also pairs naturally as a verification step before and after a humanizer pass.

Do not use it to help defeat a plagiarism or AI-detection system, tune text
against a named detector, or remove provenance marks. See "Scope and intended
use" below; reframe such requests toward an honest read of quality, voice,
and inspectable provenance signals, which is what this skill actually
delivers.

## Diagnostic only: the hard boundary

This skill scores and flags. It does not rewrite, edit, paraphrase, strip or
normalize Unicode, remove metadata, or hand back "improved" prose, not even a
single suggested replacement sentence. If the user wants the flagged prose
fixed, that is the `humanizer` skill's job, performed as a separate,
human-judged step. If the user wants provenance removed from content they own,
route that operation to a separate provenance hygiene tool and keep it outside
this scoring workflow.

The split is intentional and load-bearing. A single tool that scores text and
then rewrites it to raise its own score is a detector-gaming loop: it optimizes
prose against a metric instead of improving it for a reader, which is exactly
the failure the humanizer skill explicitly refuses. Keeping diagnosis and
transformation in separate skills, with a human deciding between them, is what
prevents that loop from forming. So the correct shape is a pair, never a
merge:

```
authenticity-check  ->  human reads the flags and decides  ->  humanizer
   (diagnose)              (judgment, not automation)          (rewrite)
        ^                                                          |
        |__________________ re-verify, fresh read ________________|
```

The re-verify pass is a fresh diagnosis of the rewritten text, not a
continuation of the first one. This skill never carries a "target score" into
a rewrite and never instructs the humanizer skill on how to move a number.

## Core principle: uniformity is the signal

The reason AI prose reads as AI is not its vocabulary. It is its uniformity:
even sentence lengths, even rhythm, even hedging, the same shapes resolved the
same way. This is the same principle the humanizer skill is built on, read
from the other side. Humanizer's job is to add genuine structural variance;
this skill's job is to detect the absence of it.

Two consequences follow, and both matter for an honest score:

1. **Flag the signature, not the vocabulary.** A single "delve" is not a tell.
   Uniform rhythm across a whole passage is. Weigh recurrence and
   co-occurrence far above any lone word.
2. **A relocated signature still counts.** Text that swapped every "delve" for
   "explore" but kept the even rhythm is not more authentic; it just moved its
   fingerprint. Do not let surface-level word choice raise a score that the
   underlying uniformity should hold down.

## Step 0: discover the baseline (do this every run, before scoring)

Decide which mode you are in. Announce it in the output header so a wrong
guess is instantly correctable.

1. **Is this a "sounds like me" question?** If the user is asking whether the
   text reads like a specific author (themselves or a named writer) and a
   voice source is available (a pasted sample, a named well-known author, or a
   discovered profile file), enter **voice-deviation mode**. Read
   `references/voice-matching.md` for how to read a voice off a sample or
   profile; here you read it to measure *deviation from* that voice, not to
   reproduce it.
2. **Look for a profile.** `Glob` the working directory and up to two parent
   levels, in this priority order: `VOICE.md`, then `STYLE-GUIDE.md`, then
   `voice-profile.md` / `.yaml` / `.json`, then `.manuscript/STYLE-GUIDE.md`,
   then a voice or style section inside `AGENTS.md` or `CLAUDE.md`. One strong
   match plus a "sounds like me" intent puts you in voice-deviation mode.
   Several plausible matches: ask one short question to pick.
3. **Otherwise, generic mode.** No voice target. Score AI-authenticity against
   the catalog and the internal-consistency heuristics only. Do not invent a
   persona to measure against; an imagined target voice is its own failure.

This discovery is filesystem-generic. It interoperates with Scriveno, Pillars,
or any project that keeps a voice file, without depending on any of them, and
without assuming this skill is the only one installed.

## Step 0a: provenance preflight (inspect, never clean)

Inspect the exact supplied text for suspicious invisible or format Unicode
before judging the prose. Keep this evidence channel separate from style:

1. Look for zero-width and format controls, bidi controls, tag characters,
   variation selectors, unusual spaces, and other `Cf` characters. If the
   interface or read tool does not expose exact codepoints, report the scan as
   `Not inspectable`; never guess from visual spacing.
2. Audit every candidate in context. Script joiners, directional controls,
   variation selectors, file-start byte-order marks, and load-bearing
   characters in visible sequences can be legitimate. Do not flag them just
   because they are invisible.
3. Report surviving candidates with an escaped codepoint such as `<U+200B>`,
   a Unicode name, a count only when reliable, and short escaped context. Do
   not remove, normalize, replace, or re-save anything.

Read `references/provenance-signals.md` when the user asks about watermarks or
hidden marks, when a candidate appears, or when its context is uncertain. If
nothing survives the audit, say so plainly in `Provenance signals`.

This preflight covers deterministic carriers in inspectable text only. It is
not a statistical token-watermark detector and it does not inspect C2PA,
EXIF, XMP, document properties, pixels, audio, or video. A carrier is not
proof of AI authorship, and finding one does not change the authenticity
score by itself.

## Step 0b: density pre-check (match scrutiny to evidence)

Before scoring, skim the whole text once and judge how heavily it is
AI-marked. Count only the **dead-giveaway** tells, not the weak surface
signals: chat-UI contamination (pattern 31), knowledge-cutoff disclaimers
(29), collaborative chatbot artifacts (28), significance inflation (1),
promotional language (5), AI-vocabulary clustering (16), sycophantic tone (7),
generic positive conclusion (13). Estimate roughly how many appear per 100
words, then set the scrutiny level and announce it in the output header:

- **Low (about 0 to 2 per 100 words): light scrutiny**, unless the rhythm is
  uniform and no human markers are present (the relocated-signature override
  below). Likely human-first text (a journal, rough notes, a real draft).
  Bias hard toward a high score and a near-empty flag list. Over-flagging
  genuine human prose is the worst error this skill can make; when density is
  low, restraint is the default. But low lexical density is evidence of a
  human only when the text also carries human markers or variance; clean
  vocabulary with even rhythm and no specificity is laundered prose, not a
  low-density human draft.
- **Medium (about 3 to 5 per 100 words): standard scrutiny.** Mixed
  authorship. Run the full catalog with the restraint of do-not-flag.md.
- **High (6 or more per 100 words): full scrutiny.** AI-first text. Run the
  full catalog thoroughly and weigh the internal-consistency heuristics fully.

This is calibration, not a number you report mechanically. One exception
overrides density: any chat-UI contamination string (pattern 31) is decisive
on its own and is always flagged, whatever the overall density, because its
presence is near-certain confirmation rather than a weak signal.

A second exception overrides density in the other direction, the
relocated-signature override. The trigger: the dead-giveaway count is Low
only because the vocabulary is clean, yet the text shows uniform rhythm or a
templated parallel skeleton (the same shape resolved the same way
throughout) AND carries no concrete specificity or human markers (the
`do-not-flag.md` Part 2 list: a specific detail or number, a dated reference,
mixed feeling, an idiosyncratic sentence-length swing, a strong unhedged
opinion, trade idiolect).

The rationale: this is a relocated signature, not a human-first draft. The
slop words being gone is the laundering itself, not evidence of a person.
Clean vocabulary does not buy a uniform, marker-free passage out of the low
band.

The action: treat scrutiny as at least High, do not apply the low-density
high-score bias, and carry the finding into scoring. Per `scoring.md`,
uniform rhythm with no credited human markers is the Reads AI-generated band
even when no catalog tell fired.

## The multi-pass diagnostic

After the separate Step 0a provenance preflight, run the prose passes in
order. Pass 1 gathers candidates, Pass 2 has veto power over them, Pass 3 adds
internal-consistency evidence, Pass 4 runs only in voice-deviation mode, and
scoring comes last.

### Pass 1: catalog scan

Load `references/tell-patterns.md`. Walk the prose against the 32-pattern
catalog (six families), scoped to the scrutiny level chosen in Step 0b. For
each genuine candidate, record the span (the actual quoted text, kept short),
the pattern family, and what the pattern says about *why* it reads as AI. Do
not rewrite the span; describe it. Recurrence and co-occurrence matter far
more than any single instance; note clusters explicitly.

### Pass 2: false-positive audit (has veto power over Pass 1)

Load `references/do-not-flag.md`. This pass is mandatory and it can overrule
Pass 1. For every candidate from Pass 1, ask:

a. Is this a weak signal standing alone (one em dash, one tricolon, one
   passive, formal register, perfect grammar, a common transition)? If it does
   not recur or co-occur, drop it.
b. Is this actually a human-writing marker (a specific concrete detail or
   number, mixed feeling, a dated reference, a self-corrective aside, an
   idiosyncratic sentence-length swing, strong unhedged opinion, trade
   idiolect)? If so, it is not a flag; it is positive evidence of a human
   author, and it should raise the score, not lower it.

When do-not-flag.md and tell-patterns.md disagree about a span, do-not-flag.md
wins. A diagnosis that flagged genuine human voice as AI has failed even if it
caught every real tell.

### Pass 3: internal-consistency heuristics (read-only)

Beyond the catalog, look for spans that read as borrowed or pasted by
comparing the text against *itself*. This is the network-free adaptation of
stylometric-inconsistency and semantic-drift detection: no web search, no
database, no external lookup. The procedure and weighting are defined in
`references/scoring.md`; in brief, chunk the text, build a rough per-chunk
profile (sentence-length distribution, register, lexical sophistication), and
flag any span whose profile diverges sharply from the document's own
established baseline. A sudden jump in technical sophistication or a register
break that the surrounding prose does not earn is a span-level flag, separate
from any catalog hit, because it suggests inserted or derivative material even
when each sentence is individually clean.

### Pass 4: voice deviation (voice-deviation mode only)

Read the target voice using the dimensions in `references/voice-matching.md`
(cadence, diction, signature moves, punctuation habits, paragraph shape,
stance, the avoid-list). Then flag spans that fall outside that author's
distribution: a passage in a register the writer never uses, a rhythm they
never produce, a move on their avoid-list. Honor the same conflict order
voice-matching.md defines: an authentic author habit is not a tell for that
writer, even when the generic catalog would flag it. In generic mode, skip
this pass entirely.

### Scoring

Compute the authenticity band and the 0-100 score from the surviving flags
and the human markers found, following `references/scoring.md`. The score is a
calibrated heuristic, never a verdict. Do not invent precision the evidence
does not support. Do not raise or lower it solely because Step 0a found or did
not find a Unicode carrier.

## False-positive guardrails

These are inline because every run needs them. Do not flag in isolation:

- Perfect grammar. Correctness is not a confession.
- A single em dash. Only dash frequency and monotony is a tell.
- Curly quotes or smart apostrophes. Word processors insert these for humans;
  never flag this in isolation.
- Formal or elevated vocabulary. Register is not origin.
- Common transitions ("however," "therefore," "for example").
- One passive sentence, one tricolon, one topic sentence.

Escalate to a flag only on recurrence or co-occurrence. When unsure, do not
flag. The full treatment, including human markers to credit and per-model
idiolects, is in `references/do-not-flag.md`; read it during Pass 2.

## Anti-signature guidance

Do not develop diagnostic tics of your own. Do not always flag the first
sentence. Do not force every report to a fixed number of flags. Do not score
to a comfortable middle to avoid committing. Two genuinely human paragraphs
deserve a high score and a near-empty flag list; ten dead-giveaway tells
deserve a low one. Vary the verdict with the evidence, not with a habit. If
your reports are starting to rhyme with each other regardless of input, stop
and re-read the text cold.

## Output contract

Always deliver the report in this exact structure. Never rewrite the text.
Never include a "suggested" or "improved" version of any span, not even
parenthetically. The flag describes the problem; it does not solve it.

```
## Authenticity report
Mode: [generic | voice-deviation vs FILENAME | voice-deviation vs pasted sample | voice-deviation vs author: NAME]
Scrutiny: [low | medium | high] (from the density pre-check)

Authenticity: [Reads human | Mixed signals | Reads AI-generated]   Score: NN/100
(higher means it reads more authentically as a person's own work)

## Provenance signals
- [No suspicious text carriers found in the inspectable text | Not
  inspectable in the current rendering | confidence, escaped codepoint and
  Unicode name, reliable count, escaped context, and context-audit reason]
- Coverage: inspectable text carriers only. Statistical token watermarks,
  file metadata, and media signals were not verified by this skill.
  (keep this channel separate from the authenticity score; never remove or
  normalize a finding)

## Flagged spans
- "short quoted span" -> [pattern family or heuristic name]: why this reads
  as AI-generated, AI-templated, or derivative. Description only, no rewrite.
  (ranked strongest evidence first; group sensibly; about 10 maximum; if there
  are none, say so plainly)

## Reads as human (deliberately not flagged)
- [something that looked like a tell but is an authentic human marker, and
  why it was credited rather than flagged]
  (one to three bullets; this section is required, even on low scores)

## Score basis
A short paragraph: what drove the score (the dead-giveaway tells found, the
internal-consistency findings, the voice deviation if applicable), and the
single biggest factor. Name what would most change the score.

## Caveats
This is a heuristic read, not proof of authorship. It targets and names no
detector. A high score is not a guarantee of human authorship; a low score is
not an accusation against a person. A Unicode carrier is not proof of AI
authorship, and the absence of a carrier finding is not a clean certificate.
Human judgment is required to act on the report.

## Next step
If the user wants the flagged prose improved, state plainly that this skill
does not rewrite, and that the fix is the separate humanizer skill, applied as
a human-judged step, after which this skill can re-verify with a fresh read.
Do not perform the rewrite here and do not hand over a target score. If the
user wants provenance removed from authorized content, state that this skill
does not remove it and route the operation to a separate provenance hygiene
tool.
```

The "Provenance signals," "Reads as human," and "Caveats" sections are not
decoration. They are forcing functions: separating provenance from prose
prevents false attribution, naming what you correctly credited as human makes
over-flagging visible, and the caveat keeps the score from being read as a
verdict. If a text is already essentially human, the correct output is a high
score, a near-empty flag list, and a clear "Reads as human" explanation.

## Scope and intended use

This skill exists to give an honest read of how authentically text reads as a
person's work, point at the weak spots, and report inspectable text-provenance
carriers without altering them. It is not designed or tuned to defeat
plagiarism checkers or AI-detection systems, and it deliberately names and
optimizes against none. If a request is framed as getting AI-written work
past a graded or contractual assessment, do not adopt that framing; give the
honest diagnostic instead, which is what this skill does well.

The diagnostic-only boundary is itself part of the scope guarantee. Because
this skill never rewrites, cleans provenance, or carries a score into a
transformation, it cannot be turned into a score-then-rewrite optimization
loop. That loop is detector-gaming, the humanizer skill refuses it for the
same reason, and keeping the two skills separate with a human in between is
what makes the refusal hold even when both are installed together.

## Reference files

Read these on demand, not upfront:

- `references/provenance-signals.md` during Step 0a when provenance is the
  user's concern, a candidate is present, or classification is uncertain.
  The Unicode carrier classes, mandatory context audit, coverage limits, and
  reporting confidence labels. Native to this repo and adapted at the class
  level from the MIT-licensed `watermarks-remover` project.
- `references/tell-patterns.md` during Pass 1. The 32-pattern catalog in six
  families. A vendored, synced copy of the humanizer repo's canonical file;
  see its header.
- `references/do-not-flag.md` during Pass 2. False positives, human markers to
  credit, model idiolects, hard stop conditions. Vendored and synced; see its
  header.
- `references/voice-matching.md` during Pass 4, in voice-deviation mode only.
  How to read a voice off a sample or profile. Vendored and synced; see its
  header.
- `references/scoring.md` for the band and 0-100 rubric and the
  internal-consistency heuristic definitions. Native to this repo.
- `references/examples.md` when you are unsure what good output looks like.
  Worked diagnostic runs in the exact output contract. Native to this repo.
