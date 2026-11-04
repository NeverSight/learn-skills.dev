---
name: humanizer
description: >-
  Humanize and de-slop AI-sounding prose while preserving meaning, specific
  detail, and genuine human quirks. When a voice sample or style profile is
  available, rewrite in that writer's actual voice. Remove recurring AI tells
  such as inflated significance, stock vocabulary, uniform rhythm, excessive
  hedging, formulaic structure, and formatting artifacts. Also clean
  suspicious invisible Unicode and copy-paste residue conservatively, without
  treating them as proof of authorship. Use whenever a user wants to humanize,
  de-AI, de-slop, or de-robotify text; fix prose that sounds corporate,
  generic, like ChatGPT, or otherwise off; match a draft to a writer or named
  author; edit for authentic voice and rhythm; or clean zero-width characters,
  exotic spaces, bidi controls, and similar hidden text residue.
license: MIT
allowed-tools: Read Write Edit Glob Grep
metadata:
  version: 1.3.1
---

# Humanizer

Turn AI-flavored or generically smooth prose into writing that reads as the
work of a person. When a writer's voice is available, make it read as the work
of *that* person. The goal is prose a careful human reader would not flag,
with its meaning and its human texture intact. The goal is not to beat any
particular detector, and this skill names and targets none.

The workflow also includes conservative text hygiene. It can remove
suspicious invisible Unicode and normalize copy-paste spacing in the prose it
rewrites, while preserving characters that carry real linguistic or display
meaning. This is not file-provenance or media-watermark tooling.

## When to use this

Use it when someone pastes a draft and says it sounds like AI, asks to
humanize or de-slop text, wants their own draft to sound like them, names an
author to match, or says the writing "feels off," "sounds corporate,"
"reads like a robot," or "is too generic." Use it even when they do not say
the word "humanize." It also pairs well after any drafting step where the
output came out machine-smooth. By default the rewrite stays measured and
faithful; if the user explicitly asks for more voice, edge, or opinion, turn
on Stance mode (see below).

Use the text-hygiene part when prose may contain invisible characters,
zero-width residue, unusual spaces, or direction controls. Treat hygiene as
format cleanup, never as evidence that a person or model wrote the text.

Do not use it to disguise authorship for an assessment or to defeat a
plagiarism or AI-detection system. See Scope and intended use below; reframe
such requests toward genuine quality and voice.

## Core principle: variance over substitution

The reason AI prose reads as AI is not its vocabulary. It is its uniformity:
even sentence lengths, even rhythm, even hedging, the same shapes resolved the
same way. Swapping "delve" for "explore" everywhere does not fix that. It just
moves the signature, and a uniform "humanizer dialect" is still a machine
fingerprint, just a different one.

Real humanization comes from genuine structural variance. Sentences of very
different lengths next to each other. A fragment. Then a long, winding one
that takes its time. Mixed syntax. The occasional asymmetry a tidy model would
smooth away. You are writing for a sharp human reader, not optimizing a score.
Every pass below serves this principle: increase real variance, do not install
a new regularity.

## Step 0: Discover the voice (do this every run, before rewriting)

Decide which mode you are in. Announce it in the output header so a wrong
guess is instantly correctable.

1. **Explicit input wins.** Did the user paste a writing sample, point to a
   file, or name a well-known author to match? Use that. Read
   `references/voice-matching.md` and proceed in voice mode.
2. **Otherwise, look for a profile.** `Glob` the working directory and up to
   two parent levels, in this priority order:
   `VOICE.md`, then `STYLE-GUIDE.md`, then
   `voice-profile.md` / `.yaml` / `.json`, then `.manuscript/STYLE-GUIDE.md`,
   then a voice or style section inside `AGENTS.md` or `CLAUDE.md`. One strong
   match: read it, then read `references/voice-matching.md`, proceed in voice
   mode. Several plausible matches: ask one short question to pick.
3. **Otherwise, generic mode.** No voice target. De-slop toward natural,
   varied human prose. Do not invent a persona or a backstory; an invented
   voice is its own failure. Generic mode skips Pass 1 and starts at Pass 2.

This discovery is filesystem-generic. It interoperates with Scriveno, Pillars,
or any project that happens to keep a voice file, without depending on any of
them.

## Step 0b: Stance mode (opt-in, off by default)

Default output is measured and faithful: it reports the source's content in
clean human prose and does not editorialize. That is the right default,
because the most common failure of livelier humanizers is that "adding voice"
becomes "adding content," and an invented opinion quietly drags an invented
fact in behind it.

Turn stance mode **on only when the user explicitly asks for it**: "give it
some voice," "make it punchier," "have a take," "don't keep it so neutral,"
"add some edge or opinion." Do not turn it on for an ordinary de-slop request,
and never in voice mode (a discovered profile already dictates stance; do not
override it).

When stance mode is on, you may add **attitude toward the existing content**:
a judgment, emphasis, dry understatement, first person as the narrator of the
same facts, an honest "this part is the weak spot," acknowledged ambivalence
about what the source already says, and freer rhythm. This is the same
material, said by someone with a point of view.

The hard line, and the entire reason this mode is safe: **stance is a reaction
to what is there, never the addition of what is not.** You may judge a stated
fact; you may not invent the fact, its cause, its mechanism, an event, a named
person, a quote, or a lived experience to react to. Test every added clause:
"is this an opinion about something the source already states, or a new claim
about the world?" If it is a new claim, it is fabrication wearing a voice, and
it is exactly the failure this skill exists to prevent. When in doubt, the
opinion is allowed and the new fact is not.

Example. Source states only: infrastructure cost rose 18% during the
migration, temporarily.

- Allowed (stance about the stated fact): "An 18% jump is a real line item,
  not a rounding error, and 'temporary' is doing some hopeful work in that
  sentence."
- Forbidden (invented cause dressed as candor): "costs rose because we were
  running the old and new systems in parallel" (the source never says why;
  this is a new fact).

Stance mode raises fabrication risk, so the Pass 3 self-audit and the Meaning
check apply with extra force, and the output header must show stance is on so
the user can dial it back. Stance is a requested change of register, so it
applies even when the density pre-check picks a light pass; density still
decides how hard to hunt for tells.

## Step 0c: Density pre-check (match effort to evidence)

Before rewriting, skim the whole text once and judge how heavily it is
AI-marked. Count only the **dead-giveaway** tells, not the weak surface
signals: chat-UI contamination (pattern 31), knowledge-cutoff disclaimers
(29), collaborative chatbot artifacts (28), significance inflation (1),
promotional language (5), AI-vocabulary clustering (16), sycophantic tone
(7), generic positive conclusion (13). Estimate roughly how many appear per
100 words, then pick the pass intensity and announce it in the output header:

- **Low (about 0 to 2 per 100 words): light pass.** The text is human-first
  (a journal, rough notes, a real person's draft). Fix only the dead-giveaway
  artifacts. Leave lower-tier patterns, rhythm, and voice alone, and bias hard
  toward "Deliberately left alone." All-or-nothing rewriting here is exactly
  what strips the quirks that made the writing sound like a person; that is
  the worst failure this skill can commit, so when density is low, restraint
  is the default and edits are the exception.
- **Medium (about 3 to 5 per 100 words): standard pass.** Mixed authorship.
  Apply the full catalog, but with the restraint of do-not-flag.md; do not
  flatten what already works.
- **High (6 or more per 100 words): full pass.** AI-first text. Apply the
  full catalog thoroughly and push real structural variance.

This is calibration, not a scan you report mechanically. Effort should match
evidence. One exception overrides density: any chat-UI contamination string
(pattern 31) is decisive on its own and is always removed, whatever the
overall density, because its presence is near-certain confirmation rather
than a weak signal.

## Step 0d: Text hygiene preflight (do this every run)

Inspect the source before rewriting so invisible formatting does not survive
or get confused with prose style. Read `references/text-hygiene.md` when the
source contains non-ASCII formatting characters, when the user mentions
hidden characters or text marks, or when the interface reports suspicious
codepoints.

Remove only characters whose lack of semantic purpose is clear. Preserve
script joiners, direction marks needed by multilingual text, variation
selectors used for display, and non-breaking spaces that carry layout or
locale meaning. Do not normalize confusable letters automatically. Invisible
characters do not count toward the density score and do not establish AI
authorship.

This is a pure-prompt skill, so inspection is limited to characters the host
preserves and exposes. When the prose is in a file and a search tool is
available, also run the codepoint search in `references/text-hygiene.md`. If
you can neither see the characters directly nor search a file, say
`not verifiable in this interface` in the output header. Never report the
text as universally watermark-free.

## The multi-pass workflow

Run the passes in order. Voice is generative; de-slopping is subtractive. If
you strip tells first you get flat neutral prose that is then hard to inflect,
so establish voice first when you have one.

### Pass 1: Voice injection (voice mode only)

Rewrite the draft *toward the target voice* before removing any tells. Set the
cadence, diction, sentence-length signature, stance, and characteristic moves
described in `references/voice-matching.md`. Match the writer's instincts and
distribution, never their specific sentences. In generic mode, skip this pass.

### Pass 2: Tell removal

Load `references/tell-patterns.md`. Walk the prose against the 32-pattern
catalog (six families), scoped to the pass intensity chosen in Step 0c. For
each genuine flag, fix the *underlying thought*, not the surface token: ask
"what is actually being said here?" and write that, concretely, at the length
the thought deserves. Preserve meaning exactly.

Concreteness must come from the source or from the user, never from you. If
the source is vague and you have no real detail to restore, the honest fix is
to say less, plainly, not to manufacture a number, date, name, or example to
make it "sound human." An invented specific reads convincingly human, which
makes it more dangerous than the fog it replaced: vague slop merely bores a
reader, a fluent fabrication misleads one. When you are tempted to add a
specific the text does not contain, shorten instead.

While you do this, hold or increase sentence-length variance; do not let
de-slopping homogenize the rhythm. In voice mode, a tell fix that would
flatten the established voice is the wrong fix; find one that keeps the voice.

Humanization changes word choice and syntax, so it may disrupt statistical
token patterns as a side effect. That effect is best-effort and unverifiable
without a public detector and key. Do not intensify a rewrite solely to evade
a detector, promise that a mark was removed, or call the result undetectable.

### Pass 3: Self-audit (has veto power over Passes 1 and 2)

Load `references/do-not-flag.md`. Ask two questions and act on both:

a. If a sharp human read this cold, what one or two things would still tip
   them that a machine touched it? Fix only those.
b. Did I overcorrect? Did I strip a specific detail, flatten a genuine quirk,
   change a meaning, or introduce my own uniform rhythm (every fix the same
   shape)? Revert any such damage.

Finally, recheck the rewritten prose for suspicious characters, including any
your own edits introduced. If Step 0d found or cleaned any, confirm against
`references/text-hygiene.md` that suspicious carriers were removed and
load-bearing Unicode was preserved. Report only changes you could actually
verify.

If Pass 3 conflicts with an earlier pass, Pass 3 wins. A clean rewrite that no
longer sounds like the writer, or that lost a real detail, has failed even if
every tell is gone.

## False-positive guardrails

These are inline because every run needs them. Do not flag in isolation:

- Perfect grammar. Correctness is not a confession; never add errors.
- A single em dash. Only dash frequency and monotony is a tell.
- Curly quotes or smart apostrophes. Word processors insert these for humans;
  normalize only for consistency with the surrounding text, never as evidence.
- Formal or elevated vocabulary. Register is not origin.
- Common transitions ("however," "therefore," "for example").
- One passive sentence, one tricolon, one topic sentence.

Escalate to a flag only on recurrence or co-occurrence. When unsure, do not
cut. The full treatment, including human markers to preserve and per-model
idiolects, is in `references/do-not-flag.md`; read it during Pass 3.

## Anti-signature guidance

Do not develop tics of your own. Not every sentence varied the same way. Not a
fixed "short punchy line, then long winding clause" template repeated down the
page. Not a contraction forced into every paragraph. Not the same three
replacement words for "delve" every time. The tell of a humanizer is
regularity in its irregularity. Vary how you vary. If your edits are starting
to rhyme with each other, stop and break your own pattern.

## Output contract

Always deliver the rewritten prose as the primary artifact, followed by a
short report. Never silently rewrite in place. Never deliver a raw diff as the
main output (prose diffs are unreadable and hide meaning drift). Use this exact
structure:

```
## Humanized draft
Voice: [generic | from FILENAME | matched to pasted sample | author: NAME]
       [append " + stance" when stance mode is on, e.g. "generic + stance"]
       [append ", low-confidence: REASON" when the voice source is thin]
Density: [low -> light pass | medium -> standard pass | high -> full pass]
Text hygiene: [no suspicious characters visible | cleaned: COUNTS AND TYPES |
               not verifiable in this interface]

[the full rewritten text]

## What changed
- [pattern family]: [plain note on what was adjusted and why]
  (group by family; do not list every token; about 8 bullets maximum)
- [text hygiene]: [include only when characters were removed or normalized]

## Deliberately left alone
- [something that looked like a tell but is authentic, and why you kept it]
  (one to three bullets; this section is required, even on heavy rewrites)

## Meaning check
One sentence confirming no facts, numbers, names, claims, or intent changed.
Confirm that text-hygiene edits changed formatting only and preserved
load-bearing Unicode.
Then check soft inference: did you assert any causal, temporal, or
quantitative link ("most of the time went to X", "because of Y", "this drove
Z") that the source only implied or did not state? If so, name it here and
either hedge it ("probably", "as I read it") or cut it back to what the
source actually says. If anything was ambiguous, ask the question here
instead of guessing.

## Next step
If the user gave a file path, offer to write the rewrite into it. Otherwise
stop here.
```

The "Deliberately left alone" and "Meaning check" sections are not optional
decoration. They are forcing functions: naming what you preserved makes
over-editing visible, and the meaning check makes drift visible. Soft
inference is the drift most likely to slip through, precisely because it is
plausible and reads human: an invented cause, or a claim about where the time
or effort went, does not trip a hard-fact scan, so the meaning check has to
look for it on purpose. If a near-miss text is already essentially human, the
correct output is minimal or no edits plus a clear explanation of what you
left and why.

## Scope and intended use

This skill exists to improve prose quality and to help a writer's own work
sound authentically like them. It is not designed or tuned to defeat
plagiarism checkers or AI-detection systems, and it deliberately names and
optimizes against none. If a request is framed as passing AI-written work off
as a person's own for a graded or contractual assessment, do not adopt that
framing; offer the quality-and-voice improvement instead, which is what this
skill actually does well.

Text hygiene in this skill is limited to characters present in supplied
prose. It does not inspect or strip C2PA, EXIF, XMP, PDF or document
properties, image pixels, audio, video, or provenance outside the text layer.
Those operations require dedicated tooling. Do not imply they were performed.

## Reference files

Read these on demand, not upfront:

- `references/tell-patterns.md` during Pass 2. The 32-pattern catalog in six
  families, each with detect / why / before-after / restraint.
- `references/do-not-flag.md` during Pass 3. False positives, human markers to
  preserve, LLM idiolects, and the hard stop conditions.
- `references/voice-matching.md` whenever Step 0 found a voice. How to extract
  and apply a voice, the optional VOICE.md schema, and conflict resolution.
- `references/text-hygiene.md` when Step 0d needs it (suspicious characters,
  a mention of hidden marks, or prose in a file to search) and for the final
  check after a cleanup. Suspicious invisible Unicode, load-bearing
  exceptions, the exact codepoint search, conservative normalization,
  reporting, and prompt-only scope boundaries.
- `references/examples.md` when you are unsure what good output looks like.
  Five full worked runs: generic de-slop, voice-first, a restraint case,
  stance mode, and text hygiene.
