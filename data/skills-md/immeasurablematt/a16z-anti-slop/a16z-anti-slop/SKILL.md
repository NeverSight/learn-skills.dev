---
name: a16z-anti-slop
license: MIT
metadata:
  version: "1.0.0"
  author: "Matthew Baggetta"
description: >-
  Audit, explain, or revise prose with a job-first taxonomy of AI-amplified
  writing habits: empty rhetoric, interchangeable voice, imposed structure,
  and repetitive punctuation. Use when the user mentions AI-sounding prose,
  AI tells, the a16z crypto writing-habits article, or wants a humanizing edit
  that distinguishes useful conventions from distracting defaults. Do not use
  it to determine who or what authored a text; it evaluates whether the writing
  is clear, trustworthy, specific, and suited to its reader.
---

# a16z anti-slop

Evaluate prose by the job it must do, not by whether it resembles a model's
output. Treat alleged AI tells as editorial clues. Diagnose the underlying
problem, decide whether the convention helps or hurts, and edit only when the
writing performs its job better afterward.

This skill adapts the practical method in Stephanie Z.'s a16z crypto article,
"The habits of AI writing, and what to do about them." It paraphrases the
method and uses synthetic examples; it does not reproduce the article.

## Operating rules

1. **Judge function, not provenance.** Never claim that a word, punctuation
   mark, detector score, or stylistic cluster proves AI authorship.
2. **Preserve evidence.** Keep every supplied fact, name, number, date,
   quotation, qualification, and commitment exact. Never invent a concrete
   detail to replace vagueness. Use a visible placeholder or request the fact.
3. **Preserve the author's agency.** Keep intentional diction, humor,
   informality, rhythm, and grammatical quirks when they serve the piece.
4. **Use edit-or-embrace decisions.** A convention is not defective merely
   because models overuse it. Headers, bullets, neutral diction, hedges, and em
   dashes all have valid jobs.
5. **Exercise restraint.** If the input already does its job, identify why and
   stop. Do not manufacture changes to demonstrate activity.

## Establish the writing job

Before editing, identify or reasonably infer:

- artifact and genre;
- intended reader and their context;
- what the reader must understand, trust, feel, or do;
- required evidence and any disclosure obligations;
- whether the piece is meant to be read linearly, scanned, or consulted later;
- how much personality should reduce or create friction.

Ask a question only when the missing answer would materially change the edit.
Otherwise state the assumption briefly and proceed.

Run this three-part job test:

1. **Clarity:** Can the intended reader understand the point and its support?
2. **Trust:** Are claims specific, proportionate, and grounded in the supplied
   evidence?
3. **Judgment:** Does the piece show deliberate choices about meaning, voice,
   structure, and emphasis, or merely accept a default shape?

Human involvement matters when disclosure is required, the named human's
authorship is central to the artifact, or a person is using automation to
simulate many independent people. Flag those cases without pretending that
style analysis can prove authorship.

## Choose the request mode

### Audit

Use when the user asks what sounds generic, AI-like, overproduced, or ineffective.

- Read the complete piece first.
- State its likely job.
- Identify only the patterns that materially affect that job.
- Apply an observable test to each finding.
- Mark each finding **edit**, **embrace**, or **needs evidence**.
- Do not produce a detector score or a list of harmless lexical coincidences.

### Revision

Use when the user asks to humanize, improve, or rewrite supplied prose.

- Diagnose before rewriting.
- Work in this order: meaning and rhetoric, diction and voice, structure,
  punctuation and cadence.
- Repair the cause rather than swapping surface tokens. Removing a dash while
  retaining the same overloaded sentence is not a repair.
- Preserve strong passages and intentional conventions.

### Creation

Use when the user wants new prose that avoids generic model defaults.

- Establish the job before drafting.
- Use only supplied or verified facts; mark factual gaps.
- Choose a structure because of the genre and reading behavior, not because a
  familiar template is available.
- Draft in the user's demonstrated voice when samples exist. Without samples,
  prefer plain, specific prose and avoid counterfeit personality.

## Run the four-lens audit

Read `references/editorial-taxonomy.md` for the complete diagnostics,
exceptions, and repairs. Load only the relevant sections when the request is
narrow.

### 1. Rhetoric: does every sentence mean something?

Apply the paraphrase test. Restate a suspicious sentence plainly. If it reduces
to a generic announcement that importance, change, or complexity exists, either
replace it with the actual claim or delete it. Retain a hedge when it accurately
expresses uncertainty, evidentiary limits, or legal/compliance needs.

### 2. Voice: could this sentence belong to anyone?

Apply the transplant test. If a sentence could move unchanged into an unrelated
piece by another author, inspect its generic warmth, recyclable framing,
abstract nouns, vague intensifiers, and low-friction verbs. Replace them only
with details the evidence supports. Neutral, standardized language is often
correct for support, safety, legal, and high-scale service text.

### 3. Structure: does the form serve the idea?

Reverse-outline the draft by recording what each paragraph or section does.
Remove organization that merely announces, repeats, or forces ideas into tidy
groups. Keep strong navigation for explainers, documentation, FAQs, search-led
content, and readers who scan. Structure a narrative for movement and tension,
an announcement for speed, and an explainer for learning dependencies.

### 4. Punctuation and cadence: is the machinery mostly invisible?

Read the passage aloud and treat punctuation as stage direction. Edit repeated
colon-list constructions, clustered asides, or any mark that repeatedly
interrupts the thought. Do not ban em dashes, semicolons, colons, parentheses,
or fragments by category. Prefer periods and commas as defaults; use a more
noticeable mark when its grammatical or rhetorical function earns attention.

## Use models as critics, not automatic finishers

When an LLM is available, it can help surface candidate problems. Use it to:

- identify hedges, fungible sentences, vague abstractions, and business jargon;
- produce a deliberately plain paraphrase so the underlying claim becomes
  visible;
- reverse-outline a strong genre example by paragraph function;
- compare a draft's diction, sentence rhythm, and punctuation with real samples
  from the author;
- transcribe voice notes as raw material whose idiosyncrasies still require
  human selection and editing.

Do not delegate the final decision to a detector, blacklist, readability score,
or one-click rewrite. Examples and counterexamples of the desired writing are
more durable than a growing banned-word list.

## Output contract

### Default audit plus revision

1. **Writing job** — one sentence stating what the piece must accomplish.
2. **Highest-value findings** — a compact set of passage-specific findings,
   each with lens, diagnostic test, and edit/embrace/needs-evidence decision.
3. **Clean revision** — the complete revised text.
4. **Unresolved evidence** — missing facts or qualifications you refused to
   invent.
5. **Reusable lesson** — one principle the writer can apply next time.

### Overrides

- `audit only` or `diagnosis only`: omit the rewrite.
- `rewrite only`, `clean version only`, or `no explanation`: return only the
  revised artifact.
- `show changes`: provide representative before/after excerpts plus the clean
  revision; do not reproduce the entire input twice unless requested.
- `teach the method`: explain the relevant diagnostic and give one synthetic
  example; do not invent a draft to critique.

For difficult calibration cases, read `references/worked-examples.md`.

## Final QA

Before delivering:

- Confirm the piece passes its stated clarity, trust, and judgment tests.
- Confirm each flagged habit impaired the job; remove false positives.
- Confirm every factual detail and qualification survived or became a visible
  unresolved item.
- Confirm the revision did not replace the author's voice with generic polish.
- Confirm structure reflects reader behavior and genre rather than a default
  template.
- Confirm punctuation supports meaning and does not call attention to itself
  through repetition.
- Confirm the output matches the user's requested mode and contains no claim of
  AI-authorship detection.

## Files in this skill

- `references/editorial-taxonomy.md` — full four-lens diagnostics, edit/embrace
  rules, exceptions, and repair techniques.
- `references/worked-examples.md` — synthetic calibrations for specificity,
  compliance hedges, neutral voice, structure, punctuation, and restraint.
