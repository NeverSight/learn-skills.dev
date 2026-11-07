---
name: sciwrite-prose
description: >
  Edit and tighten scientific or technical prose at the sentence and paragraph
  level, using the method taught in Stanford's Writing in the Sciences. Use this
  skill whenever someone asks you to review, edit, tighten, clean up, polish or
  improve any piece of research writing — a paper, thesis chapter, abstract,
  grant paragraph, cover letter or report — and whenever they say a passage
  "sounds wrong", "reads badly", "is too long", "is too dense", or needs to fit
  a word limit. Also use it for targeted requests: fix the passive voice, cut
  the clutter, kill the jargon, check acronyms, make the terminology consistent,
  fix parallelism, or shorten an abstract. Use it proactively when you are asked
  to write scientific prose yourself, so the draft follows the same rules. Do
  NOT use it to judge whether the science is correct, to restructure a whole
  manuscript into IMRaD sections (use sciwrite-manuscript), or to plan the
  writing process (use sciwrite-process).
---

# Editing scientific prose

You are editing in the tradition of Kristin Sainani's *Writing in the Sciences*.
The goal is not elegance for its own sake: it is that a reader gets the idea
with the least effort, and that nothing in the prose obscures who did what.

Two commitments frame everything below.

**You improve delivery, not substance.** Never change a claim, a number or a
technical assertion. If something looks scientifically wrong, say so separately
as a note and leave the text alone.

**Never say "consider improving clarity."** Every observation comes with the
original text and a concrete rewrite. A suggestion the author cannot act on is
not a suggestion.

Answer in whatever language the user writes to you in. Course examples stay in
their original English.

---

## Start by deciding what kind of job this is

| The user's text | What they need |
|---|---|
| A sentence or two | Rewrite it, show the diff, name the two or three rules involved. Do not produce a report. |
| A paragraph | The upshot method (below), then sentence-level edits. |
| A section or chapter | Structure pass first, then prose pass. Report by finding, not by rule. |
| A whole manuscript | Ask which section matters most, or start with the one they named. A full audit of 8,000 words as a flat list is unusable. |
| "Cut this to N words" | Clutter and nominalisations first — they usually get you there without losing content. Report the word count you reached. |

If they gave you a file, run the scripts before reading closely. If they pasted
text, just read it.

---

## The scripts do the grep so you can do the judgment

```bash
# The scripts ship in sciwrite-prose/scripts/. Find that skill wherever it was
# installed: plugin, `npx skills add` (project or global), or a manual copy.
SCIWRITE=$(for d in "${CLAUDE_PLUGIN_ROOT:-.}/skills" .claude/skills .agents/skills \
                    ~/.claude/skills ~/.agents/skills; do
  [ -f "$d/sciwrite-prose/scripts/prose_audit.py" ] && { (cd "$d/sciwrite-prose/scripts" && pwd); break; }
done)

python "$SCIWRITE/extract_text.py" paper.tex
python "$SCIWRITE/prose_audit.py" paper.tex --section discussion
python "$SCIWRITE/keyword_consistency.py" paper.tex
python "$SCIWRITE/numeric_consistency.py" paper.tex
```

If `$SCIWRITE` comes back empty, the sciwrite-prose skill is not installed: do
these checks by reading, and tell the user that
`npx skills add dvdsosa/scientific-writing-skills` adds the scripts.

`extract_text.py` handles `.tex`, `.docx`, `.md` and `.txt`, and gives you a
section map so `--section discussion` works without anyone pasting anything.
Everything accepts `--json`.

**These produce candidates, not verdicts.** Every pattern they find has
legitimate uses. A passive in Methods is usually correct. A repeated keyword is
mandatory. `PSNR` may be standard in the target venue. Read each hit and decide;
reporting the script's output verbatim is not editing.

If a script is unavailable, do the same passes by reading. The passes are the
method; the scripts are only faster.

---

## For a paragraph: the upshot method

Bloated paragraphs happen because deciding *what to say* and deciding *how to
say it* get done at the same time. Separate them.

1. **Reduce every sentence to one plain line** — its upshot. Do not preserve
   detail, do not make it sound good.
2. **List the upshots together.** Repetition invisible across 200 words of prose
   is unmissable across eight short lines.
3. **Delete duplicates, group like with like, put the main point first.**
4. **Write the paragraph from the reordered list**, applying the sentence passes.
5. **Check back against the list.** Every point present, nothing invented.

Show the user the list. It is usually the moment they see their own repetition,
and it makes your cuts checkable rather than arbitrary.

Deciding *which details survive* is part of the edit. In one course example the
author name and journal of each cited study were dropped, because in that
paragraph they competed with the point.

`references/paragraphs.md` has two full worked examples (212→91 words, 139→76)
plus the paragraph rules: one idea each, two to five sentences, punchline early,
logic instead of signposts, and only *but* and *and* as transitions.

---

## For longer text: structure before prose

This is the order Sainani uses on a whole essay, and it matters — polishing
sentences in a paragraph that should not exist is wasted work.

**Pass A — structure.** Tag each paragraph in the margin with a phrase naming its
one idea. Then look at the tags alone:

- Do two paragraphs carry the same tag in different places? Move them together;
  merging usually reveals repetition.
- Does the sequence make a logical argument?
- Does a paragraph carry two tags? Split it.
- Is the significance of the work stated early, or buried in the last paragraph?
  (In the course's demo edit, the key statement of significance sat at the end
  and was moved up to paragraph two.)
- Does a controversy bounce pro/con/pro/con? Group all the arguments, then all
  the counterarguments, then all the rebuttals.

**Pass B — prose.** Then the sentence-level passes below.

---

## The five audit passes

Run them in this order. Earlier passes remove text that later passes would have
wasted effort on.

### Pass 1: Clutter

Strip every sentence to its cleanest components. Look for dead-weight openers
(*As it is well known*, *It should be noted that*), blobs (*basic tenets of*, *a
profile of*, *in terms of*), long-for-short (*due to the fact that* → *because*),
redundancy where the adjective already lives in the noun (*successful
solutions*), negatives with a positive form (*did not have* → *lacks*),
superfluous *there is/there are*, needless prepositions, and adverbs — especially
*very*, *really*, *quite*, *basically*, *clearly*.

Full tables with course examples: **`references/clutter-lexicon.md`**.

### Pass 2: Verbs and Voice

Passive verbs (a *to be* form plus a past participle) — ask *who does what to
whom?* Nominalisations, especially `noun + of` (*provides a review of* →
*reviews*). Overuse of *to be* verbs. Weak verb choices where a precise one would
absorb an adverb (*reports approximately* → *estimates*). Buried predicates,
where the reader waits too long for the main verb.

Converting to active often shortens the sentence by itself and exposes
ambiguities the passive was concealing. *We* and *I* are correct in scientific
writing; journal style guides ask for them.

Full treatment with the conversion protocol and the legitimate uses of passive:
**`references/verbs-and-voice.md`**.

### Pass 3: Punctuation and Rhythm

Stripping clutter does not mean writing only short sentences — that is
monotonous. Vary structure with the colon, semicolon, dash and parentheses. Each
does something the others cannot: parentheses tell the reader they may skip;
a dash keeps the emphasis a comma would lose; a colon sets up what follows.
Check that paired ideas and every list are parallel.

The dash is a legitimate tool here, not a defect. Use it deliberately and
sparingly, the way the course teaches.

Full guidance and the parallelism examples: **`references/punctuation.md`**.

### Pass 4: Terminology

Keywords — group names, variable names, instrument names — must be identical
everywhere: abstract, methods, results, discussion, table titles, column
headings, figure legends. A synonym for a defined term makes the reader ask
whether a new category appeared. Flag every non-standard acronym; if it is
unavoidable, it must be defined in each section, because readers do not read
linearly.

Grammar points worth getting right: *data are*, affect/effect, *compared with*
vs *compared to*, that/which, singular-they, principle/principal.

Full reference: **`references/grammar-and-keywords.md`**.

### Pass 5: Consistency of Fact

Sample sizes, percentages and means must agree between abstract, body, tables and
figures. A mismatch does not read as a typo to a reviewer — it reads as more than
one version of the dataset in circulation. Check that no citation is a "reference
to nowhere", and that key statistics come from primary sources rather than a
chain of reviews citing reviews.

`numeric_consistency.py` covers the mechanical part. Table-to-figure agreement
still needs eyes.

---

## Output

**For a sentence or paragraph**, show before and after, then a short list of what
changed and why. Name the rule, briefly. Do not pad.

**For a section or longer**, structure the report by what you found, not by which
pass found it:

```
## Writing review: <section>

<Two or three sentences: the dominant problem, and the single change that
would most improve this text.>

### Structure
<Only if there is something to say. Paragraph tags, merges, splits, moves.>

### Edits
<Grouped by paragraph or line. Each one: original → revision → one-line why.
Lead with the ones that matter.>

### Consistency
<Terminology drift, acronyms, numbers — with locations.>

### Content notes (not edited)
<Anything that looked scientifically off. Flagged, never changed.>
```

Rank by impact. Three edits that fix the argument beat forty that fix commas, and
a reader who has to wade through forty minor items will not reach the three.

**If the text is already good, say so** and stop. Manufacturing findings to look
thorough wastes the author's time and trains them to ignore you.

---

## Where the rules stop

Respect these, or the edits come out mechanical:

- **Methods** may use the passive voice and jargon liberally, and may be dull.
- **Repeating a keyword is required**, not a flaw to fix.
- **The dash, colon, semicolon and parentheses are tools**, not informalities to
  remove.
- **A sentence that works despite breaking a rule stays.** The goal is clarity,
  not uniformity, and the author's voice is worth preserving. The course
  explicitly encourages taking risks — something funny, something provocative.
- **Target-venue conventions win.** If the journal's style guide or the user's
  supervisor says otherwise, they are right and you are not. Ask which venue if
  it matters and you do not know.

If the user states a convention of their own — their supervisor's, their group's,
their target journal's — follow it for the rest of the conversation and say which
of the course's rules it overrides, so they can see the trade they are making.

---

## Reference files

| File | Read it when |
|---|---|
| `references/clutter-lexicon.md` | cutting words — the full lookup tables |
| `references/verbs-and-voice.md` | passive voice, nominalisations, buried predicates, the verb check |
| `references/punctuation.md` | varying sentence structure, colons and dashes, parallelism |
| `references/paragraphs.md` | a paragraph meanders; the upshot method in full |
| `references/grammar-and-keywords.md` | terminology drift, acronyms, grammar points |
| `references/engineering-examples.md` | the text is engineering, embedded systems or computer vision |
| `references/oceanography-examples.md` | the text is oceanography, hydrography or any field reporting transports and sections |
