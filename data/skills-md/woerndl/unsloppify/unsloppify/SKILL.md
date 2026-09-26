---
name: unsloppify
description: Remove AI writing tells from text. Use when a text artifact is the deliverable or a major part of one, such as documentation, PR or commit text, release notes, reports, marketing copy, code comments, or when asked to de-slop, humanize, or clean up text. Not for chat replies, status updates, or completion summaries around a non-text task.
metadata:
  version: "1.4.0"
---

# unsloppify

Slop is text that performs instead of informs. The fix is never decoration.
State the plain version. This applies to any draft regardless of author,
whether a person or a model wrote it. Judge the writing on its own terms, not
by who produced it.

## When to load

Load this skill when a text artifact is the deliverable or a major part of
one: a document, PR or commit text, release notes, a report, marketing copy,
a substantial set of code comments. Words produced around other work do not
qualify: chat replies, status updates, tool commentary, completion summaries.
Those follow the writing baseline. If the skill is loaded and the task does
not qualify, skip the procedure and continue the task.

## Procedure

Outside the mechanical house rules (em dashes, semicolons, and UTF middle
dots, removed on sight), every flag below is a prompt to check whether the
flagged form is genuinely necessary, the exact word for the exact case that
no plain phrase covers. The form stays available, but only with that reason.
The goal is caught tropes rewritten, not a draft too timid to say anything.

Drafting:
1. Name the context (prose, docs, PR or commit text, code comments, academic).
   Apply its rules below while writing. Load at most one secondary context.
2. Immediately before producing the final text, re-read the six failure modes.
   Rules read early in a long session fade. This step exists for that reason.
3. Self-scan against the six tests. One instance may stand. Repetition or
   clustering is the failure.
4. Sweep the draft for hyphens between words. Every compound modifier is
   either an established term the audience shares, a literal code identifier,
   or gets spelled out in plain words. This tell is frequent enough to earn
   its own pass.

Auditing an existing document:
1. Run scripts/scan.sh on the document (or rg -i -f references/phrases.txt).
   This finds the literal tells at zero reasoning cost. The scanner catches
   phrase-level tells only. Structural tells (banner comments, value echoes,
   bold-first formatting) need your read. The list ends in triage groups
   (bare cannot, never, gate, actually, land, ship, sits, arrows, negation
   tails, hyphen compounds) where many hits are legitimate. Those hits are
   questions to answer per instance, not findings to report.
2. Read the document's structure once: headings, openings, endings. Flag
   repeated shapes, repeated metaphors, template beats.
3. Read the text in sections. Apply the six tests per section. Long documents
   get more than one pass.
4. Collect every candidate in a findings list (location, quote, mode) before
   rewriting anything.
5. Rewrite from the list. Then read the whole result once for voice, facts,
   and coherence. For deep audits, load references/patterns.md.

## Guards

Precedence when rules collide: factual meaning beats quoted material beats
the user's requested voice beats domain register beats any anti-slop rule.
- Facts survive every rewrite: numbers, names, dates, URLs, quotes, units,
  code identifiers, scope words, negations.
- Keep hedges that carry content (legal, medical, security, academic).
- Do not overcorrect into anti-slop register. Staccato punch endings, "Not X.
  Y." fragments, and forced bluntness are tells too.
- Quoted slop being discussed stays as quoted.

## The six failure modes

### 1. Importance inflation
Pull: models pad to sound authoritative, so asserted weight stands in for shown weight.
Test: delete the rating word. If the meaning survives, the word was decoration.
Banned: crucial, essential, vital, paramount, transformative, cannot be overstated, more important than ever, plays a key role, stands as a testament, paving the way, dramatic absolutes (cannot, never, always) where plain "not" states the fact. Escape: a dependency you name in the same sentence, a literal impossibility.
Example: "The cache plays a crucial role in overall system performance." -> "The cache cuts read latency by 40%."
Infer: any word that rates the thing instead of describing it.

### 2. Manufactured drama
Pull: models borrow the rhythm of persuasive copy, so tension gets staged where none exists.
Test: does the sentence build suspense the content does not pay off, or state the fact by denying its alternative?
Banned: "it isn't just X, it's Y", "No X. No Y. Just Z.", "The catch?", self-answered questions, one-line mic-drop fragments, "the truth is", "let that sink in", negation tails (", not X.", ", no X either.") where the positive statement carries the fact. Escape: a contrast that preempts a misreading the positive statement leaves open ("per host, not per request").
Example: "This isn't caching. It's a whole new architecture." -> "The change adds a cache."
Infer: any framing that promises a reveal the facts do not earn.

### 3. Performative register
Pull: models reach for prestige vocabulary and insider slang to signal expertise.
Test: would a plain verb say the same thing? Use it.
Banned: delve, tapestry, seamless, leverage, robust, utilize, facilitate, serves as, functions as, footgun, blast radius, battle-tested, improvised hyphen compounds ("review-shaped output", "genuine-need escape hatch") where plain words spell the idea out. Escape: a term used for its literal, precise meaning, or an established compound the audience shares (thread-local, copy-on-write). Several compounds in one paragraph fail even when each would pass alone.
Example: "The validator serves as a gatekeeper for malformed input." -> "The validator rejects malformed input."
Infer: any word chosen for how it sounds over what it says.

### 4. False precision
Pull: models fill gaps with confident-sounding labels and round attributions instead of the specific mechanism.
Test: name the mechanism, source, or number. If you cannot, cut the claim.
Banned: diagnosis labels (race condition, deadlock, memory leak) without the named mechanism, "studies show", "everything from X to Y", invented concept labels.
Example: "The crash is probably a race condition." -> "The reader thread can see the buffer after the length update but before the payload write."
Infer: any claim that sounds specific but names nothing checkable.

### 5. Template filling
Pull: models complete a familiar essay shape, so openings and closings arrive on reflex.
Test: does the sentence carry content, or only fill a slot the form expects?
Banned: "In conclusion", "In today's fast-paced world", wrap-up headings, reflex triads, bold-first bullet labels.
Example: "**Performance**: The new index makes lookups faster." -> "Lookups now hit the new index and return in under 5 ms."
Infer: any beat present because the template has it, not because the content needs it.

### 6. Process leakage
Pull: models leave the seams of their own production in the artifact, such as chat register, review history, and cross-references.
Test: would this text exist if the document had always looked finished?
Banned: "per review feedback", "as mentioned above", "I hope this helps", "Now also handles ...", conversation residue in code comments.
Example: "// Now also handles empty arrays (per review feedback)" -> "// Empty arrays return zero."
Infer: any trace of how the text was made rather than what it says.

## Context rules

Prose:
- Lead with the specific fact, not a warm-up.
- Vary sentence length. Watch tricolons and anaphora arriving on reflex.
- Cut adverbs that rate instead of measure.
- Hold to one metaphor per idea and drop the dead ones.
- Read the ending. If it restates, stop at the last real point.

Docs:
- Open with what the thing does or how to run it.
- Prefer the imperative ("Run X" over "You can run X").
- No feature gets a benefit tail it did not earn.
- One worked example beats three sentences of description.
- Headings name content, not "Overview" filler.

PR and commit text:
- The subject states the change on its own terms, readable by someone who never saw the plan.
- No plan labels, stage numbers, or references only this session can resolve.
- Drop performative engineering slang. Name the actual mechanism.
- Add a body only when the subject cannot carry the reason.

Code comments (necessity gate first):
- A comment must say what the code cannot show. If the code shows it, delete the comment.
- No banner or divider comments. No label comments over self-describing lines.
- No value echoes beside the literal they restate.
- No review history or conversation residue in the comment.
- State what the code does, not what it does not do. A ", not X" or ", no X
  either" tail stays only when it preempts a misreading the reader would
  actually make.
- Join clauses with the real connective. A bare comma between two clauses
  hides and, so, or but. Write the connective or split the sentence.

Academic:
- Keep hedges that carry real uncertainty. Cut hedges that only soften.
- Cite the specific study, sample, and finding, not "research suggests".
- Plain register beats elevated vocabulary. State the claim directly.
- Define a coined term in plain words on first use.

## Dose rule

Any single pattern once might be fine (mechanical house rules excepted).
Multiple patterns together, or one pattern repeated, is the failure mode.
Write varied, specific, plain.
