---
name: reading-contract
description: Sources-only discipline for any instrument or agent that reads documents and asserts facts from them — literature audits, record replays, data extraction, citation of prior work.
---

# reading-contract — assert only what the record supports

**THE CONTRACT: an instrument that reads documents asserts only what the
record in front of it supports, with the citation attached at the level of
page, table, equation, or line. Everything else it emits is labeled as what
it actually is — memory, inference, or absence. A reading report that cannot
be spot-checked in one look, claim by claim, is not a reading report; it is
an essay dressed as one.**

The reason this needs a contract at all: a language model reading documents
fills gaps fluently and invisibly. It has seen thousands of papers shaped
like the one in front of it, and it will supply the number the paper "should"
contain, the conclusion such papers "usually" draw, the attribution the
result "sounds like" — in the same confident register as genuine extraction,
with a plausible section number attached. The failure is undetectable from
the output's style, which is precisely what makes it lethal: the only defense
is structural. Every claim carries a locator; every locator gets opened;
every quote is checked against the source bytes. Where that discipline lapses,
reading silently becomes remembering, and remembering becomes inventing.

## The procedure

**1. Open the actual record.** "Read" means the source bytes are in front of
the instrument in this session — not a recollection of the title, not a
secondary account, not an abstract standing in for the body. If the source
cannot be opened, the honest output is "not checked," stated as such. An
answer from memory dressed in a citation is worse than no answer, because it
poisons every later check that trusts the citation.

**2. Extract with locators.** Every asserted fact carries its source plus a
locator precise enough that a checker lands on the sentence: page, table row,
equation number, figure panel. A claim you cannot point to is not extracted
yet — go back and find it, or downgrade it to a labeled inference. Record
which version of the source the locator refers to (preprint versus published;
edition; revision date): locators rot when versions shift, and a broken
locator quietly breaks the entire audit trail behind it.

**3. Quote before paraphrase for load-bearing claims.** When an assertion
will carry weight in later work, carry the verbatim sentence next to the
paraphrase, copied from the source text — never re-typed from memory, which
is where drift enters. The check on the claim is then one look instead of a
search. Quotation marks are a legal instrument: they promise the string
occurs literally in the source. A fair paraphrase inside quotation marks is
a fabrication, however faithful its content.

**4. Preserve the hedge at source strength.** "Consistent with" is not
"confirms"; "suggests" is not "shows"; a conjecture in the source stays a
conjecture in your note. The modal is part of the claim. Restatements are
checked against the carried quote, never against the previous restatement —
chains of summaries strengthen monotonically, one fair-sounding notch at a
time, until the source is credited with a result it explicitly declined to
claim.

**5. Classify outcomes honestly.** When checking a published value against
its own stated inputs, there are exactly four honest outcomes: it
*reproduces*; it is *determined only under conventions the record does not
state* (name the assumed convention); it is *undetermined* by what the record
provides; or it is *uncheckable* with what you have. "Probably meant" is not
an outcome. A mismatch you can erase by guessing a normalization is not a
reproduction — it is the second category, reported as the second category.

**6. Scope every attribution.** A claim belongs to the sentence's actual
author at the sentence's actual strength. One paper is not the field; the
boldest sentence in one introduction is not a consensus. "It is known that"
requires either a source that says so or deletion. Absence claims scope to
the search performed: "these records do not state X" is assertable after
actually searching them; "the literature contains no X" is a claim about a
search you must be able to describe.

**7. Type retrieval as retrieval.** A result found in a source during
reading is recorded as retrieved, with the source — never re-presented as
something derived here. This holds even when you could have derived it: the
provenance of *how you actually got it* is the fact being recorded. A value
copied from a table and later "independently confirmed" against that same
table is a copy agreeing with itself. Never claim independent derivation of
a published result.

**8. Verify bibliographic identity.** Authors, title, venue, year,
identifier — checked against the canonical databases before the entry is
cited, not copied from a previous citer. Folklore errors propagate precisely
because each citer trusts the one before; the chain breaks only where
someone opens the record.

**9. Separate the layers in the report.** Three bins, visibly labeled:
*read* (facts with locators, quotes verified); *inferred* (labeled, resting
on named read facts); *background* (memory, unverified — quarantined, and
either verified against a source before use or excluded from anything that
carries weight). A report that mixes the bins forces every reader to re-do
the reading to find out which sentences are load-bearing.

## Failure-mode catalogue

The classes this contract exists to catch. Each reads fluently; none survives
opening the source.

- **Memory dressed as reading.** The report cites a section for a claim the
  instrument pulled from its recollection of similar papers; the section,
  opened, says something narrower, later, or nothing of the kind.
- **Paraphrase drift.** Each restatement strengthens the hedge one notch —
  consistent-with becomes finds becomes establishes — and the final summary
  credits the source with a claim it explicitly avoided.
- **The phantom quote.** Quotation marks around a fair-sounding paraphrase;
  the string occurs nowhere in the source, and the marks convert a summary
  into manufactured evidence.
- **Abstract-for-body citation.** The abstract's headline is cited for a
  quantitative claim that lives only in the body, under assumptions the
  abstract omits — or that appears nowhere in the paper at all.
- **One-paper-to-field promotion.** A single group's statement becomes "the
  field believes"; a second source would refute the consensus being invented.
- **Secondary-source laundering.** A review's summary of a paper is
  extracted and cited as the paper itself; the review's simplification now
  travels with the original's authority.
- **Convention smuggling.** A published value "fails to reproduce" because
  the reader silently assumed a normalization or sign convention the record
  never states — the honest outcome was "determined only under unstated
  conventions," not "wrong."
- **Locator rot.** The claim is genuine but the pointer is to a different
  version — equations renumbered between preprint and journal — so every
  later checker fails to verify and the trail dies silently.
- **Negative claim without a search.** "Not addressed in the literature"
  asserted after reading three papers; the claim's true scope was those
  three papers and the one query that found them.
- **Retrieval passed as derivation.** A value found in a table during the
  reading pass is later presented as computed here, and its "independent
  confirmation" is its own reference.
- **Version skew.** A claim read in the preprint is attributed to the
  published version, and the two differ at exactly the sentence in question.
- **Bibliography folklore.** Year, author list, or venue copied from a
  previous citer's error and propagated, because nobody in the chain ever
  opened the canonical record.

## Worked micro-example: the drift chain

Source sentence: *"our results are consistent with a vanishing correction."*

- Note, first pass: "they find the correction consistent with zero." — fair.
- Second pass, summarizing the note: "they find no correction." — a claim
  the authors did not make.
- Third pass, citing the summary: "it is known that the correction
  vanishes." — folklore, three steps from birth, each step a fair-sounding
  summary of the one before.

Only the first restatement is a fair summary *of the source*. The cure is
mechanical, not moral: the verbatim quote travels with the claim, and every
restatement is checked against the quote. The chain cannot drift when every
link is forged against the same original.

## Worked micro-example: the extraction record

The format that makes spot-checking one look instead of an afternoon:

```
CLAIM:    the second-order coefficient is given in closed form
SOURCE:   [Author, Year], published version, Eq. (3.12), p. 9
VERBATIM: "the coefficient at second order reduces to [expression]"
          (copied from the source text, not re-typed)
STATUS:   read — quote verified against source
```

and, kept visibly apart from it:

```
BACKGROUND (memory, unverified): expansions of this type typically
converge inside the unit disk. Not asserted; verify before use.
```

The second block is not a weakness in the report — it is the report being
honest about which of its sentences were read and which were remembered. The
failure is not having background knowledge; the failure is letting it wear
a locator.

## Closing checklist

Before a reading report ships:

- [ ] Every asserted fact carries source plus locator (page / table /
      equation / line), with the source version identified.
- [ ] Every locator was verified by opening the record in this session —
      none inherited from memory or a previous citer.
- [ ] Load-bearing claims carry verbatim quotes copied from the source
      bytes; every quotation-marked string literally occurs in the source.
- [ ] Hedges preserved at source strength; restatements checked against
      the quote, not against earlier restatements.
- [ ] Every check outcome is one of: reproduces / determined only under
      unstated conventions / undetermined / uncheckable — no "probably
      meant."
- [ ] Attributions scoped to the actual author and paper; no one-paper
      claims promoted to the field.
- [ ] Abstracts cited only for what the abstract itself supports.
- [ ] Negative claims scoped to the records actually searched, with the
      search describable.
- [ ] Everything retrieved is typed as retrieval; no found result is
      presented as derived here.
- [ ] Read / inferred / background layers visibly separated; background is
      quarantined from anything that carries weight.
- [ ] Bibliographic identity of every cited entry checked against a
      canonical database, not a previous citer.

The test of the whole report: hand it to a skeptic with the sources open.
If any sentence sends them searching rather than looking, the contract was
not met for that sentence.
