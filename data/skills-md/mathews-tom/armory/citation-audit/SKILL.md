---
name: citation-audit
description: 'Verify that every citation in a manuscript is real, correctly attributed, and accurately described. Detects ghost papers, wrong arXiv IDs, inverted claims, and dead links by fetching each cited work. Optional fix mode applies bib metadata corrections and surfaces prose rewrites for claim errors. Triggers on: "check my citations", "verify references", "citation audit", "are my references real", "check bib", "reference check", "bib audit", "citation verification". Companion to manuscript-review (Pass 5 hygiene); this skill audits factual truth.'
metadata:
  version: 1.0.0
  complements: [manuscript-review, research-critique, literature-review]
  category: review
  tags: [citations, bibliography, fact-check, hallucination, references]
  difficulty: advanced
  phase: review
---

# Citation Audit Skill

## Purpose

Verify every citation in a manuscript against its actual source. LLMs
hallucinate citations, invent arXiv IDs, misattribute findings, and confuse
authors. This skill catches all of that by fetching and reading each cited
work.

## Why This Exists

LLMs are unreliable with citations in three distinct ways:
1. **Ghost papers** — The paper does not exist. Title, authors, or venue are
   fabricated.
2. **Wrong metadata** — The paper exists but the bib entry has the wrong arXiv
   ID, wrong authors, wrong year, or wrong venue.
3. **Inverted claims** — The paper exists and the bib is correct, but the
   manuscript mischaracterizes what the paper says.

All three are invisible to structural audits (cross-reference checks,
compilation tests). They require reading the actual cited work.

## Inputs

- The manuscript `.tex` file(s)
- The `.bib` file
- Web access (to fetch papers from arXiv, conference sites, URLs)

## Execution

### Phase 1: Extract citation contexts

For each `\citep{}`, `\citet{}`, `\cite{}` in the manuscript:
1. Record the bib key
2. Record the surrounding sentence or paragraph (the **claim context**)
3. Classify the claim type:
   - **FACTUAL**: "X et al. found Y" / "X et al. measured Y"
   - **METHODOLOGICAL**: "We follow X" / "We use the benchmark from X"
   - **POSITIONAL**: "Unlike X, we..." / "X does not measure..."
   - **PARENTHETICAL**: "(X, 2024)" — no specific claim, just a reference
4. For FACTUAL and POSITIONAL claims, extract the specific assertion the
   manuscript makes about the cited work

### Phase 2: Verify bib entry metadata

For each bib entry, verify against the actual source:

**For arXiv papers (`eprint` field present):**
1. Fetch `https://arxiv.org/abs/{eprint_id}`
2. Compare: title, authors, year
3. If the fetched paper has a DIFFERENT title/authors than the bib entry,
   this is a **WRONG ID** or **GHOST PAPER**

**For conference/journal papers (`booktitle` or `journal` field):**
1. Search for the paper by title + author on the web
2. Verify: venue, year, author list
3. If the paper cannot be found at the stated venue, flag as
   **UNVERIFIABLE** or **GHOST PAPER**

**For web resources (`howpublished` with URL):**
1. Fetch the URL
2. Verify it loads and the content matches the described resource
3. If the URL is dead or redirects to unrelated content, flag as
   **DEAD LINK**

**For each entry, check:**
- [ ] Paper exists (reachable via arXiv, DOI, URL, or web search)
- [ ] Title matches (exact or near-exact)
- [ ] Authors match (at least first author correct)
- [ ] Year matches
- [ ] Venue matches (if applicable)
- [ ] Entry type appropriate (`@inproceedings` for conferences,
      `@article` for journals, `@misc` for preprints/blogs)

### Phase 3: Verify claim accuracy

For each FACTUAL or POSITIONAL claim:
1. **Read the cited paper** (abstract + relevant sections at minimum)
2. Compare the manuscript's claim against what the paper actually says
3. Classify:
   - **ACCURATE** — The claim faithfully represents the cited work
   - **INACCURATE** — The claim mischaracterizes the cited work
   - **INVERTED** — The claim says the opposite of what the paper found
   - **OVERCLAIMED** — The claim is stronger than what the paper supports
   - **UNDERCLAIMED** — The cited work supports a stronger claim than stated
   - **UNVERIFIABLE** — Cannot access the paper to verify

For INACCURATE and INVERTED findings, provide:
- What the manuscript claims
- What the cited paper actually says
- The specific section/page of the cited paper that contradicts the claim
- A suggested correction

### Phase 4: Check for missing citations

Scan the manuscript for:
1. Claims that cite no source but should (empirical claims without
   attribution)
2. Tools, benchmarks, or datasets mentioned by name without citation
3. Methods described as "standard" or "well-known" that have a canonical
   citation

## Output Format

### Per-citation report

```
### [bib_key] — [VERDICT]

**Bib entry:** [title] by [authors] ([year])
**Actual paper:** [actual title] by [actual authors] ([actual year])
**Metadata match:** title [✓/✗] | authors [✓/✗] | year [✓/✗] | venue [✓/✗]

**Claim in manuscript (line N):** "[exact text]"
**What the paper actually says:** "[summary of actual finding]"
**Claim accuracy:** [ACCURATE / INACCURATE / INVERTED / OVERCLAIMED / UNDERCLAIMED]

**Fix required:** [description of what needs to change, or "None"]
```

### Summary table

```
| Bib Key | Exists | Metadata | Claim | Verdict |
|---------|--------|----------|-------|---------|
| key1    | ✓      | ✓        | ✓     | PASS    |
| key2    | ✓      | ✗        | ✗     | FAIL    |
| key3    | ✗      | —        | —     | GHOST   |
```

### Verdict categories

- **PASS** — Paper exists, metadata correct, claims accurate
- **METADATA** — Paper exists, bib entry has errors (wrong ID, wrong
  authors, wrong year)
- **CLAIM** — Paper exists, metadata correct, but manuscript
  mischaracterizes it
- **GHOST** — Paper does not exist as described
- **DEAD** — URL/link is broken
- **UNVERIFIABLE** — Cannot access the paper to verify

## Severity

- **CRITICAL**: GHOST papers, INVERTED claims
- **HIGH**: Wrong arXiv IDs, wrong authors, INACCURATE claims
- **MEDIUM**: Wrong year, wrong venue, OVERCLAIMED
- **LOW**: Missing citations, incomplete bib entries, UNDERCLAIMED

## Important notes

- NEVER trust your own knowledge of papers. ALWAYS fetch and verify.
  Your training data contains hallucinated citations. The only way to
  verify is to read the actual source.
- For arXiv papers, always fetch the abstract page to confirm the paper
  exists and matches.
- For conference papers, search DBLP, ACM DL, or the conference site.
- WebFetch and WebSearch are your primary tools. Do not skip verification
  because a citation "looks right."
- Blog posts and documentation URLs change. Always check that the URL
  still works and points to the described content.
- When a bib entry has both an `eprint` (arXiv ID) and a `booktitle`
  (venue), verify both independently.

## Phase 5: Fix (when invoked with "fix" or "on")

When the user invokes with an argument containing "fix" or "on", execute
Phases 1–4 as above, then apply fixes for every non-PASS citation.

### What to auto-fix (no user confirmation needed)

These are mechanical corrections with a single correct answer:

**METADATA errors (paper exists, bib entry wrong):**
- Wrong arXiv ID → replace `eprint` with the correct ID
- Wrong authors → replace with authors from the actual paper
- Wrong year → replace with year from the actual paper
- Wrong title → replace with title from the actual paper
- Wrong venue → replace with venue from the actual paper
- Wrong entry type → change `@misc`/`@inproceedings` as appropriate

**DEAD links:**
- URL redirects → update `howpublished` URL to the final destination
- URL 404 but resource found at different URL → update URL
- URL 404 and resource gone → flag as HUMAN-REQUIRED

**Minor author corrections:**
- Misspelled author names → fix spelling
- Missing authors from author list → add them
- Collective author name where individual names are available → replace
  (keep collective name as a note if it is how the group identifies)

### What requires HUMAN-REQUIRED decision

Present these and wait for the user:

**GHOST papers:**
- Paper does not exist at all → present options:
  (a) Replace with a real paper that makes the same point
  (b) Remove the citation and adjust the prose
  (c) The user knows the paper exists and provides the correct reference

**INVERTED or INACCURATE claims:**
- The manuscript says X about a paper that actually says Y → present:
  - What the manuscript claims
  - What the paper actually says
  - A suggested rewrite of the prose that accurately represents the paper
  - Whether the paper still supports the manuscript's argument (and how)
  - Let the user decide the final wording

**Dead URLs with no replacement found:**
- Blog post / resource deleted with no archive or alternative

### Fix procedure

1. Apply all auto-fixes to the `.bib` file
2. For each HUMAN-REQUIRED item, present the options clearly
3. After user decisions, apply prose changes to the `.tex` file
4. Verify: re-read the `.bib` and `.tex` to confirm all fixes applied
5. Update the audit report: mark each finding as `[FIXED]`, `[RESOLVED]`,
   or `[DEFERRED]`

### Safety rules

- NEVER invent a replacement citation. If a ghost paper needs replacing,
  search for real papers that make the cited point. Present candidates
  to the user with abstracts. Let the user choose.
- NEVER change the manuscript's argument. If an inverted claim needs
  fixing, present the rewrite as a suggestion, not an edit.
- NEVER remove a citation without user confirmation, even if it is a
  ghost paper. The user may know something you do not.
- When fixing URLs, always verify the new URL loads and contains the
  expected content before writing it.

## Save report as

`[name]-citation-audit.md` in the manuscript directory.
