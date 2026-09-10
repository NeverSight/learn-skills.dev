---
name: jinko-task-literature-search
description: >-
  Find and shortlist biomedical publications from PubMed for knowledge, data,
  or reusable-model evidence. Use for query framing, PMID/DOI discovery,
  bibliographic normalization, evidence prioritization, and best-effort public
  full-text retrieval before synthesis, extraction, or modeling. Do not use for
  ClinicalTrials.gov-only scoping, systematic reviews, quantitative extraction,
  curve digitization, calibration, or model implementation.
compatibility: >-
  Requires network access, requests, and USER_EMAIL in .env for NCBI identity.
  NCBI_API_KEY is optional.
metadata:
  author: Nova In Silico
license: MIT
---

# Biomedical Literature Search

Produce a citation-grounded candidate shortlist, not extracted evidence or a
systematic-review claim.

## Frame

Classify each search as:

- **Knowledge**: disease, mechanism, treatment, population, or clinical context;
- **Data**: studies likely to report values for specified model variables;
- **Models**: mathematical or computational models with reusable structure,
  equations, parameters, or code.

Before searching, establish subject, scope, evidence type, date/language limits,
and desired shortlist size. Data searches additionally require the variables to
inform, population and disease state, and whether aggregate or distributional
data are needed. Ask one focused question only when a missing choice would
materially change the search.

Build one shared Entity Table with `canonical_name`, `synonyms`, `mesh_term`,
`related_entities`, `intent_groups`, and `exclusions`. Confirm it with the user
before network calls when proposed aliases or exclusions are consequential.

For human clinical, biological, or PK/PD Data searches, run
`jinko-task-trial-data-scoping` in parallel. Use high-priority NCT identifiers as
additional `<NCT_ID>[si]` PubMed angles. Skip this for animal-only or in-vitro
searches unless requested.

## Search

1. Read `assets/pubmed-primitives.md` and only the recipe matching each intent.
2. Build at least three distinct PubMed angles per entity and intent. Reuse the
   Entity Table's aliases and exclusions; include supplied anchor PMIDs through
   `--seed-pmids`.
3. Run `scripts/literature_search.py` once per angle with separate output
   directories and `--no-prompt-selection`, sequencing or bounding concurrency
   to respect NCBI limits. The script owns PubMed, Crossref, abstract and citation
   enrichment, AMA formatting, and optional PMC excerpts.
4. Run `scripts/compile_results.py` over all angle directories. It deduplicates
   by PMID/DOI, preserves query provenance, and ranks the candidate pool by
   angle count then citation count.

This is one search pass. Wider terms, author/journal queries, citation-neighbor
queries, or additional entities are separate user-approved follow-ups.

## Shortlist

Use the relevant recipe to inspect titles, abstracts, and available full-text
excerpts. For each retained candidate, assign the fields required by
`assets/shortlist-schema.json`, including evidence type, canonical entities,
verification evidence, priority rationale, and query provenance. Do not infer
quantitative availability from a title alone.

Run `scripts/validate_shortlist.py` before presenting `shortlist.json`. Present a
concise Markdown view grouped by intent and ask which sources to inspect or pass
to `jinko-task-extract-data-table`.

## Artifacts

- `frame.json`: approved scope, Entity Table, assumptions, and angle definitions;
- one directory per angle containing raw and normalized search artifacts;
- `merged_references.json`: deterministic cross-angle candidate pool;
- `shortlist.json`: schema-valid prioritized candidates;
- optional downloaded files and download manifest.

Use `publication_download.py` only for user-selected references. Treat downloads
as best-effort anonymously retrievable files, not proof of open-access licensing.
Do not run supplementary URLs from untrusted manifests.

Keep registry records and publications distinguishable even when linked by
`nct_id`. Clearly separate discovered candidates from inspected evidence and
from calibration-ready data.