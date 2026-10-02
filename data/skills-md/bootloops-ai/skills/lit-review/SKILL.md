---
name: lit-review
description: Deep literature review behind a research project's novelty claims — a protocol whose one job is to prevent shortcuts. It demands the papers be actually read (nothing from memory), makes thoroughness falsifiable (read ledgers, search receipts, gap statements), tracks citation chains in both directions, and lists the places to look. Use before any novelty claim ships, when writing or reviewing a related-work section, and when refereeing.
---

# lit-review — no shortcuts

A literature review fails silently. Every other check in this harness fails
loudly — a control that doesn't recover the planted answer, digits that
disagree with the independent route. A missed paper produces no error message:
the review reads as complete, the claim goes out, and the miss surfaces later,
from a referee or from the missed author.

Examined afterward, every miss traces to a shortcut that felt reasonable at
the time: the searchers verified the papers they already knew instead of
hunting the ones they didn't; queries stopped a year or two short of the
present; abstracts were read where full texts were owed; a paywall quietly
downgraded a paper from "read" to "skimmed". None of these announce
themselves. The protocol's answer is to make each one visible: every form of
thoroughness claimed here is backed by a receipt a second reader can check, or
it does not count.

Refereeing runs the same protocol in reverse — the submission's novelty
claims become C1..Cn and the verdicts belong to someone else's paper. When
refereeing, follow the venue's rules on AI assistance and manuscript
confidentiality; many prohibit sharing a manuscript under review with AI tools.
Where that is the rule, run this protocol on the public literature around the
submission's claims, never on the confidential text itself, and disclose the
assistance to the editor if the venue asks.

## The proximity scale

Grade every candidate work as you go; the heavy obligations below key off the
grade.

- **P0–P1** — same broad area, different question. Note or discard.
- **P2** — shares a component (a technique, a dataset, a subresult) but not
  the question. Goes in the credit list.
- **P3** — attacks the same question with different tools, or a neighboring
  question with the same tools. Full-text read required.
- **P4** — overlaps part of a claim: a special case proved, or the same
  result under different assumptions. Full-text read, verbatim quote, chains
  both directions.
- **P5** — contains the claim. The review's reason for existing.

## The three iron rules (violations invalidate the review)

**1. Read the papers. Nothing from memory.**

- Every work graded P3 or above is read in full text — the PDF fetched and
  read, not the abstract, not another paper's summary of it, not what the
  model remembers. The relevant theorem, definition, or construction is
  quoted verbatim with a page or section number. If the full text cannot be
  obtained (paywall without institutional access, no author-posted copy),
  the work is marked FULL-TEXT-UNREAD and its grade is a ceiling estimate, flagged as such —
  never silently downgraded to what the abstract suggests.
- No citation, date, venue, or claim about what a paper shows comes from
  memory. Memory generates the search query; the source generates the
  sentence. Verification means a live fetch of the primary record (publisher
  page, preprint server, author PDF), with the route recorded.
- Gated or scanned PDFs: use legitimate routes only — an open-access or
  preprint version, the author's own posted copy, your institution's
  subscription, interlibrary loan, or a request to the author; read a scanned
  PDF page by page with vision if that is what it takes. Never bypass access
  controls or use unauthorized repositories. If no legitimate full text is
  available, mark the work FULL-TEXT-UNREAD (grade = ceiling) and list it as
  owed.

**2. Thoroughness is falsifiable, not asserted.** Every review carries
receipts:

- **A search ledger** — every query actually run, on which engine or index,
  with the year range. A query that never named the current year is a defect.
- **A read ledger** — which works were read full-text, which abstract-only,
  which flagged unread. A review whose read ledger is empty at P3+ is not a
  review.
- **A gap statement** — what was NOT searched: fields, languages, venues,
  year ranges, any channel that died on a budget or access wall. Implied
  completeness is the exact lie this skill exists to prevent.
- **Iterate to dry** — rounds continue until a fresh round (a new angle, a
  recency re-sweep, chains run on newly found works) returns nothing at P3+.
  Report the rounds run and what each added. One pass has never been enough.

**3. Track citation chains, both directions.** For every work at P3+:

- **Backward** — mine its reference list for ancestors no search named.
  Record the chain (A cites B cites C): the chain is itself a deliverable,
  because it is how the next reviewer verifies coverage.
- **Forward** — find who cites it: cited-by listings sorted newest first, the
  most recent two or three years read closely. This is how you find the paper
  whose name you don't know — it cites the ancestor you do.
- **Per-author recency** — every author appearing at P3+ gets their last few
  years swept through the current month: personal website (publications and
  preprint pages, including linked working papers — drafts are often posted
  there long before journals), profile pages sorted by date, preprint and
  working-paper listings. Publicly posted drafts and working papers count
  fully.

## Places to look

Use every service within its terms. Prefer documented APIs (Semantic Scholar,
OpenAlex, Crossref, arXiv, INSPIRE, PubMed, ADS); query interactive-only
services such as Google Scholar by hand or at human pace, never from a fan-out
of agents; rate-limit every automated fetch (pause ~2 s between calls) and
honor robots.txt; list any service you could not lawfully query in the gap
statement.

Tick each, or put it in the gap statement:

- **Google Scholar** — keyword and quoted-phrase queries; cited-by chains;
  author profiles sorted by year.
- **Semantic Scholar** (site and API) — citations and references
  programmatically; good recall on preprints.
- **The field's preprint server** — arXiv by category plus full-text search,
  bioRxiv/medRxiv, SSRN, OpenReview for machine-learning-adjacent claims. The
  frontier lives here and on authors' pages, not in journals.
- **Working-paper series**, where the field has them — institutional series,
  author listings, new-paper feeds.
- **Author websites** — read the publications page, CV and any preprints or
  drafts the author has publicly linked; the newest work is often posted there
  before any index has crawled it. Do not guess URLs or enumerate directories.
- **Review articles, surveys, handbook chapters** in the claim's territory —
  a field's own synthesis is a pre-built citation chain; read the newest one
  you can find.
- **Journal tables of contents**, the last couple of years, for the three or
  four venues where the nearest ancestors published.
- **Course syllabi and lecture notes** (site:edu filetype:pdf) — instructors
  track frontier papers faster than journals, and usually link the preprint
  version.
- **Software registries** (CRAN, PyPI, the package archives of statistical
  environments) — a rival method often exists as a package before or beside
  its paper.
- **Dissertations** — when a research line's students are active, the newest
  statement of the line is a thesis.
- **Field review databases** where they exist (zbMATH, MathSciNet,
  INSPIRE, PubMed).
- **The claim's own vocabulary, and every synonym.** Search the project's
  coined terms in quotes, plain paraphrases, and the whole synonym family —
  the same object wears a different name in every field that touched it.
  Build the synonym list as you go and re-run every search under each new
  name found. The phrase hunt does two jobs: it protects your naming, and it
  finds the rival wearing another field's name for your object.

## Procedure

**0. Claims first.** Before any search, write the numbered novelty claims
C1..Cn, plus the exact headline sentences the paper or announcement will
carry. Each headline gets a verdict at the end: survives as worded /
falsified (quote the falsifier) / survives only reworded (propose the
wording). A review run without pinned claims drifts into confirming a mood.

**1. Fan out by lineage.** One searcher per lineage or subfield that could
own the result — six to twelve angles for a serious claim (parallel
subagents if your framework supports them; sequential passes otherwise). Any
known-relevant names in a brief are a floor, never the hunt list: a searcher
told "check Smith and Jones" will verify Smith and Jones and under-search
everyone else. Each angle keeps its own ledgers.

**2. Chains and recency** (iron rule 3) on everything the angles surface at
P3+. This is where the papers no query can name get found.

**3. Synthesize.** A deduplicated table of the closest works — P4/P5 entries
with verbatim quotes and locations — plus a credit list (P2–P3), diffed
against the paper's actual bibliography. Then per-claim novelty verdicts,
stated against interest: (a) new as far as this review can see; (b) new with
required credit — name the ancestor; (c) at risk as worded — name the work,
quote the overlapping passage, propose the wording that survives. No
softening. The verdicts are the product; a review that returns only a reading
list has not finished.

**4. Iterate to dry** (iron rule 2), then carry the findings into the paper.

## Findings into the paper

- **Prior work is motivation, never a rival.** The closest ancestor goes in
  the introduction as the point of departure, credited generously BEFORE the
  delta is stated; the delta is then stated flat. Cut protective register on
  sight ("a referee will note", "to be clear about priority") — prose that
  argues with an imagined referee reads as exactly what it is.
- Every citation added to the paper is copied from the review's verified
  entries only, with the verification route noted (the ref-check skill
  governs entry format and bibliography audits).
- At-risk claims are reworded before anything goes out. A headline that
  failed its verdict never survives on "approximately true".
- P2–P3 works land in the credit list even if never cited — the next
  revision reads the list, not the reviewer's memory.
- Full-text debts that remain (a gated text, a book checked only at page
  level) are listed, not forgotten.

## Failure-mode catalogue

Each of these is a class observed in real reviews. When a review misses
something, find the miss's class here — or add it; a miss without a new
entry is a repeat waiting.

- **Canon anchoring.** The brief names the famous papers; the searchers
  verify the famous papers; the miss is the recent work by an author nobody
  named. Verification effort concentrates on what you already know — hunting
  effort must be budgeted separately.
- **Recency blindness.** Every query implicitly ended a year or two ago
  because the searcher's sense of the field did. A central author's latest
  papers sat unfound because nothing swept their output through the current
  month.
- **Venue bias.** Searches favored journals; the field's actual frontier was
  on preprint servers and authors' own sites, months to years ahead. The
  decisive miss was a working paper posted on an author's own website that no
  index had crawled.
- **The abstract-grade read.** An abstract-level skim reported a prior paper
  as claiming the opposite of the project's result; the full text showed the
  same sign and a different magnitude. A false confrontation was minted and
  repeated before anyone read the paper. Full-text reads are not overhead —
  they are where the review's claims come from.
- **Memory-sourced citations.** An entry written from recall carries a
  paraphrase of the title, a plausible-but-wrong year, a truncated author
  list — and every field of it reads fine. The cure is upstream of any
  bibliography audit: nothing enters the review from memory.
- **Synonym blindness.** The rival existed for years under another field's
  name for the same object. Every query used your field's term; every one
  returned nothing; "nothing found" was true and worthless.
- **The silent dead channel.** A search or fetch budget ran out mid-review
  and a whole channel — the one that finds author drafts, say — went dark
  without any step failing. The angles reported normally; coverage had
  silently shrunk. Any searcher that hits a budget or access wall says so in
  its gap statement (which channel, which queries never ran), and the
  synthesis counts a dead channel as an owed round, never as covered. A
  review is not dry while a named channel died on budget.
- **One-pass certainty.** The first pass found nothing close, and the review
  stopped there. Distance from the literature on pass one usually measures
  the queries, not the literature.
- **Confirmation search.** Queries phrased to confirm novelty ("first proof
  of X") rather than to destroy it ("proof of X", each synonym, each
  ancestor's forward citations). The reviewer's job is to kill the claim; a
  review that wants the claim to survive will let it.
- **The convenience downgrade.** A paywalled P4 candidate quietly became
  "checked" on the strength of its abstract because the PDF was hard to get.
  The grade kept its authority; the reading behind it was gone.
- **Implied completeness.** The review reported everything it found and
  nothing it skipped. The reader took the union to be the whole field; the
  gap statement existed to prevent exactly that inference, and wasn't
  written.

## Two micro-examples

**The synonym family.** A project coins "anchored window" for its object.
The same object, in neighboring literatures, goes by tolerance region,
feasibility band, and admissible set — each in a literature that never
cites the others. A review that searches only the coined term and its
plain paraphrase returns clean and is wrong. The working method: every time a
P3+ paper names the object differently, that name becomes a fresh round of
queries across every engine already used. The synonym list at the end of the
review is a deliverable.

**The chain that finds the unnameable paper.** You cannot query for a paper
you have no words for. But if it exists, it almost certainly cites the
ancestor you DO know. Take the strongest known ancestor, open its forward
citations sorted newest first, and read the last two years of titles
closely. This is the highest-yield single move in the protocol, and it is
exactly the move a keyword-only review never makes.

**Sources and acknowledgments.** The search ledger, read ledger and gap
statement are a lightweight form of the PRISMA 2020 reporting items (Page et
al., BMJ 372 (2021) n71); citation chaining in both directions is the
snowballing procedure of Wohlin (EASE 2014), whose value over database search
alone Greenhalgh and Peacock measured (BMJ 331 (2005) 1064). We thank the teams
behind Semantic Scholar, OpenAlex, Crossref, arXiv, INSPIRE-HEP, PubMed and
NASA ADS, whose open APIs make the ledgers checkable.

## Exit checklist

- [ ] Claims and headline sentences pinned before the first query.
- [ ] Every P3+ work read full-text with a verbatim quote and location, or
      explicitly flagged FULL-TEXT-UNREAD with its grade marked as a ceiling.
- [ ] Search ledger present; queries name the current year.
- [ ] Read ledger present and non-empty at P3+.
- [ ] Gap statement written — including any channel that died on budget or
      access, counted as owed, not as covered.
- [ ] Chains run both directions on every P3+ work; per-author recency swept
      through the current month, authors' own publication pages included.
- [ ] Synonym family built; every engine re-queried under each name found.
- [ ] The final round added nothing at P3+ (iterated to dry); the number of
      rounds reported.
- [ ] Per-claim verdicts stated against interest; at-risk wording fixed
      before anything goes out.
- [ ] Credit list diffed against the actual bibliography; every added
      citation traces to a verified entry.
