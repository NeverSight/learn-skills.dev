---
name: ref-check
description: Careful bibliography verification and entry-addition for papers — verify every author, title, journal, volume, pages, year, arXiv ID, and DOI against authoritative online sources (INSPIRE, arXiv, CrossRef/DOI, zbMATH, publisher) before anything enters or stays in a .bib file. Use whenever adding bib entries, auditing a bibliography, checking citations, fixing references, or when asked to "check the references". Encodes the report-then-fix pattern for full-file audits and the folklore-error traps (wrong years, truncated author lists, mislabeled keys).
---

# ref-check — careful reference verification

## The iron rule, and why it exists

**NEVER guess or trust-from-memory an arXiv ID, journal reference, year,
author list, page range, or title.** Every factual field is verified against a
fetched authoritative record before an entry is added, approved, or "fixed."
Training-data recall of bibliographic details is a *hypothesis to verify*,
never a source. If a field cannot be verified after trying at least two
sources, it is FLAGGED, not silently kept or invented.

The rule is this severe because bibliographies are not copied from sources —
they are copied from *other bibliographies*. An error, once printed, outlives
its origin: the next hundred authors copy the entry, not the paper, and the
error acquires the authority of repetition. A language model trained on that
literature has learned the majority text, which for a propagated error IS the
error — model recall of a reference reproduces the folklore version with full
confidence. This is why "it looks right" is worthless here, and why an entry
that half the field cites one way can still be wrong. Verification means
fetching the record closest to the publisher and comparing field by field;
nothing else counts.

A second consequence: an entry that a model *drafted* from memory is not a
degraded citation — it is a fabrication with correct formatting. The observed
pattern (see traps below) is a real identifier carrying invented co-authors,
a paraphrased title, or another paper's journal block. Plausibility is the
failure mode, not the reassurance.

## Authoritative sources, by literature

The universal spine is **CrossRef / the publisher's DOI landing page** —
canonical journal, volume, pages, year for anything with a DOI. Around it,
use the registry native to the literature:

1. **INSPIRE-HEP** (physics/hep) — fetch BibTeX directly:
   `https://inspirehep.net/api/literature?sort=mostrecent&size=1&q=arxiv%3A<ID>&format=bibtex`
   (URL-encode `:` as `%3A`; old-style IDs URL-encode the slash: `q=arxiv%3Ahep-ph%2F<YYMMNNN>`).
   Cross-check the arXiv abs page.
2. **arXiv abs page** (`https://arxiv.org/abs/<ID>`) — title, full author
   list, journal-ref line. v1 titles sometimes differ from the published
   title; **the published title wins** when the entry cites the journal.
3. **CrossRef / publisher DOI page** — the arbiter for journal fields.
4. **zbMATH / MathSciNet / Project Euclid / numdam** — mathematics.
5. **ADS** — astronomy; **PubMed/PMC** — life sciences; **DBLP** — computer
   science (conference/proceedings metadata that CrossRef often garbles).
6. **Zenodo / the software's own CITATION file** — software and datasets.
7. **Gallica / archive.org / WorldCat / publisher record** — classical books
   and pre-DOI literature.

**Search aggregators (Google Scholar, Semantic Scholar) are for FINDING a
work, never for verifying it.** They merge records, inherit upstream errors,
and invent metadata for scraped PDFs. Once found, verify against the native
registry or publisher.

Sleep ~2s between external calls; try a second source before declaring
anything unverifiable. When two authoritative sources disagree, the one
closest to the publisher wins for journal fields, and the disagreement itself
goes in the audit log — it usually marks a folklore error in the losing
source.

## Field-by-field comparison (semantic, not textual)

- **Authors** — every author present, correct order, correct spelling
  *including diacritics*. TeX escapes vs unicode (`{\'e}` = `é`) are equal. A
  missing, extra, or misspelled author = FIX. Watch homonyms: same-surname
  collaborators are routinely merged into one person, and given names swapped
  between them.
- **Title** — word-level. Brace/capitalization/TeX-markup differences =
  formatting. Wrong, missing, or extra words = FIX.
- **Journal, volume, number, pages, year** — exact. Standard abbreviation vs
  full journal name = MINOR. Wrong volume/pages/year = FIX. Translated-journal
  pairs (Russ. Math. Surv./Uspekhi Mat. Nauk; Sov. Phys. JETP/ZhETF): either
  is fine if internally consistent; a mismatched year between the pair = FIX.
- **arXiv ID, DOI** — exact, and the DOI must *resolve to the right work*:
  fetch the landing page and compare its title. A syntactically valid DOI
  pointing at an erratum, a comment, or a different paper by the same group
  is a FIX that no string comparison catches.
- **Entry type and roles** — chapters in collections credit the chapter
  authors, with editors as editors; proceedings carry the conference year vs
  publication year distinction explicitly.

Classify each entry: **OK** (every factual field compared against a fetched
record and matching) · **MINOR** (formatting only, no action) · **FIX** (any
factual discrepancy — record `field: ours -> authoritative` + source URL) ·
**UNVERIFIABLE** (state exactly what was tried) · **INTERNAL**
(self-references/companion notes — list, exempt).

Never mark OK without having actually fetched and compared. "Looks right" is
not a verification.

## Folklore traps (all observed in practice)

Each of these is a measured failure mode from real bibliography audits, not a
hypothetical. They are the classes that survive casual checking because the
entry *looks* healthy.

- **Wrong years that circulate** — a result becomes attached to the wrong
  year and the whole literature repeats it: e.g. a landmark irrationality
  theorem published in 2001 that half the citing literature dates to 2004 —
  the journal record, not the majority citation, is the evidence.
- **Truncated author lists** — the field remembers the famous pair and drops
  the rest (e.g. a four-author paper that the field routinely cites by its
  two most famous authors). Verify the FULL list even when the short form is
  universal.
- **Merged authors** — two distinct people fused into one: same surname,
  averaged initials, one entry where the record shows two names. The inverse
  also occurs — one author split into two by an initials variant.
- **Phantom page numbers** — a plausible page range attached to a paper that
  the journal published under an article number, or a first page copied from
  a different paper in the same issue. Article-number journals take the
  article number, not an invented range.
- **Mislabeled keys** — the entry under a key can be a *different paper* than
  the key name suggests (observed: a key naming one author trio holding a
  paper by a different trio). The key is part of the audit: check that key ≈
  actual authors.
- **Announcement vs final version** — cite the cleanly citable version
  (book/journal), not a short announcement note, and say which in a comment.
- **Preprint v1 title drift** — published title wins.
- **Prose initials vs keys** — before renaming a key, grep every `\cite`
  usage AND read the surrounding prose: initials in prose may already refer
  to the *correct* authors even when the key is wrong.
- **Another paper's journal block** — an entry can carry the correct
  preprint ID/title with the journal/volume/pages/year of a *different* paper
  by the same authors (observed in practice). Verify the journal ref against
  the preprint server's own journal-ref line or CrossRef, not just "a" record
  by those authors.
- **Descriptive phrase as title** — entries written from memory often carry a
  paraphrase of the paper's subject instead of its actual title (observed
  five times in a single audit). Titles must be copied from the fetched
  record, never composed.
- **Invented co-authors / wrong given names on real papers** — LLM-drafted
  entries can attach plausible-but-wrong names to a correct identifier
  (observed: wrong given names on 3 entries, an extra co-author on 1, in one
  audit). Check every name against the record even when the ID resolves.
- **Entirely wrong paper under a plausible key** — key, note, and citing
  prose describe paper X while the entry's fields are paper Y (observed: an
  entry on one subject sitting under a key naming a different subject
  entirely). When key/note/prose disagree with the entry, read the *citing
  prose* to determine intent before fixing — the correct fix may be a new
  entry, not a field repair.
- **A "verified" pass is not immune** — one same-day verified addition
  carried wrong volume/pages from a hasty read of the abstract page (an
  off-by-one volume number). Volume/pages come from the journal-ref line or
  CrossRef, not from adjacent metadata on a page that lists several versions.

## The claim check — does the cited work say what the sentence says?

A bibliography can be field-perfect and still lie, because the citation's
real payload is the *sentence attached to it*. A full ref-check audits both
layers. For every citation that carries factual weight — "X proved Y [12]", a
number with a bracket after it, a definition attributed to a source, a
"first shown in" — do this:

1. **Open the work.** Full text where available; the preprint version
   otherwise (note the version skew). The abstract alone verifies only
   abstract-level claims.
2. **Locate the claim**: the theorem number, equation, table, or page where
   the cited statement actually appears. Record the locator in the audit log
   — a claim check without a locator is an impression, not a check.
3. **Verdict per claim**: **SUPPORTED** (locator recorded) · **DRIFTED** (the
   claim is true but lives in a different work — often an earlier or later
   paper in the same series; fix the citation, not the prose) · **INFLATED**
   (the work proves a special case or a weaker form than the sentence
   asserts) · **ABSENT** (nothing in the work matches) · **CONTRADICTED**
   (the work says the opposite — it happens, usually via a sign, a
   convention, or a negation lost in paraphrase).
4. **Report, never silently rewrite.** For DRIFTED the fix is the citation;
   for INFLATED/ABSENT/CONTRADICTED the fix may be the prose, and that is the
   author's call. A checker who "fixes" meaning has exceeded the mandate.

The claim-layer traps mirror the field-layer ones: **secondhand laundering**
(the citation and its misreading were both copied from an intermediary paper
that itself never checked); **review-article telephone** (a survey's
compressed paraphrase gets cited as if it were the original's claim);
**attribution creep** ("first proved by" pointing at the famous paper when
the record shows an earlier, obscurer proof); **convention mismatch** (the
cited formula is right in the source's normalization and wrong in the citing
paper's). None of these are visible from the bibliography file; they only
fall to actually opening the work.

## Process

### Adding entries (small batches)
Verify each work per the rules above; match the house entry style of the
target .bib; add under a dated comment block
(`%% ----- <purpose> (added <date>, verified)`) with a per-entry
`% VERIFIED <date> <source-URL>` comment; run a duplicate-key check
(`grep '^@' | extract keys | sort | uniq -d` must be empty); never modify
existing entries in the same pass. Also run a duplicate-*work* check: the
same paper can already sit in the file under a different key, and two keys
for one work will bite at citation time.

### Full-file audit (report-then-fix pattern)
1. **Chunk** the .bib by entry boundaries (~15–20 entries per verifier;
   compute line ranges from `grep -n '^@'`).
2. **Verify in parallel, REPORT-ONLY** — if your agent framework supports
   parallel subagents, fan the chunks out; verifiers never edit the .bib
   (concurrent writes corrupt it). Each returns structured per-entry verdicts
   with verbatim diffs and source URLs.
3. **Fix serially** — one pass (human-reviewed, or a single agent working
   from the approved diff list) applies FIX items only, keys unchanged unless
   a rename is explicitly approved.
4. **Key renames are load-bearing** — grep all `\cite` usages across the tex
   tree, update them atomically with the .bib, check prose initials (see
   traps).
5. **Rebuild** — full compile-plus-bibliography cycle (e.g. pdflatex+bibtex);
   zero errors, zero missing/undefined citations is the exit gate. A clean
   exit code is not the gate — read the log for warnings, and confirm the
   rendered bibliography actually carries the fixes (stale .bbl files
   survive successful-looking builds).
6. **Record** — stamp fixed entries `% VERIFIED <date> <source>`; log the
   audit (date, counts by verdict, fixes applied) wherever the project tracks
   provenance. The log is what lets the next audit skip re-fetching two
   hundred already-verified records — an unstamped verification evaporates.

## Exit checklist

- [ ] Every entry has a verdict; zero entries skipped.
- [ ] Every FIX applied cites its source URL; every UNVERIFIABLE is flagged
      to the user, not silently retained.
- [ ] Every DOI resolved and its landing page compared, not just
      string-checked.
- [ ] Claim check done on every load-bearing citation, with locators
      (theorem/equation/page) recorded; DRIFTED/INFLATED/ABSENT/CONTRADICTED
      verdicts reported to the author, prose untouched.
- [ ] Duplicate-key and duplicate-work checks clean; all `\cite` keys in the
      tex tree resolve (bibliography log has no missing-entry warnings).
- [ ] Full rebuild passes with zero errors and zero undefined citations, and
      the rendered output carries the fixes.
- [ ] Audit logged with date, counts by verdict, and fixes applied.

Acknowledgment. This procedure leans entirely on open bibliographic
infrastructure — INSPIRE-HEP, arXiv, Crossref, zbMATH Open, MathSciNet, NASA
ADS, PubMed and DBLP; we are grateful to the people who maintain them. Work that
relied on ADS should carry the acknowledgment its FAQ asks for ("This research
has made use of the Astrophysics Data System, funded by NASA under Cooperative
Agreement 80NSSC21M00561").
