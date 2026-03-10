---
name: citation-verifier
description: |
  Verify citations and references in scientific documents to detect hallucinated or invalid sources.
  Extracts DOIs, URLs, arXiv IDs, PubMed IDs, and ISBNs from Markdown, LaTeX, org-mode, and plain text,
  then validates them using API lookups and web fetches.

  Use this skill when:
  - Reviewing AI-generated content for citation accuracy
  - Validating references in papers, reports, or documentation
  - Checking if DOIs/URLs resolve to actual papers
  - Auditing a document for broken or fake citations

allowed-tools:
  - Read
  - WebFetch
  - WebSearch
  - Grep
  - Glob
  - TodoWrite
---

# Citation Verifier

Detect and verify citations in scientific documents to identify hallucinated, broken, or invalid references.

## Purpose

AI-generated content sometimes includes plausible-looking but fake citations. This skill systematically extracts all citation identifiers from a document and verifies each one against authoritative sources, producing a detailed report with verification status and suggestions for fixing invalid citations.

## When to Use

This skill should be invoked when:
- User asks to "verify citations" or "check references" in a document
- User suspects hallucinated citations in AI-generated content
- User wants to validate DOIs, URLs, or other identifiers in a paper
- User asks to audit a document for broken links or fake references
- User mentions "citation verification", "reference checking", or "DOI validation"

## Supported Document Formats

1. **Markdown** (.md): Inline links `[text](url)`, reference links `[text][ref]`, bare URLs, DOIs
2. **LaTeX/BibTeX** (.tex, .bib): `\cite{}`, `@article{}`, DOI fields, URL fields
3. **Org-mode** (.org): `[[url][text]]` links, `#+BIBLIOGRAPHY`, cite links
4. **Plain text** (.txt): Bare URLs, DOIs, arXiv IDs, author-year patterns

## Citation Identifiers Detected

### DOIs (Digital Object Identifiers)
- Pattern: `10.\d{4,}/[^\s]+` or `doi.org/10.\d{4,}/[^\s]+`
- Example: `10.1038/nature12373`, `https://doi.org/10.1126/science.abc1234`
- Verification: CrossRef API at `https://api.crossref.org/works/{doi}`

### URLs to Papers
- Patterns: Links to known publishers and repositories
- Domains: nature.com, science.org, sciencedirect.com, springer.com, wiley.com, acs.org, rsc.org, pnas.org, cell.com, plos.org, mdpi.com, frontiersin.org, academic.oup.com, tandfonline.com
- Verification: HTTP HEAD/GET request, check for 200 status and paper metadata

### arXiv IDs
- Pattern: `arXiv:\d{4}\.\d{4,5}(v\d+)?` or `arxiv.org/abs/\d{4}\.\d{4,5}`
- Example: `arXiv:2301.07041`, `https://arxiv.org/abs/2301.07041v2`
- Verification: arXiv API or direct URL check

### PubMed IDs (PMIDs)
- Pattern: `PMID:\s*\d+` or `pubmed.ncbi.nlm.nih.gov/\d+`
- Example: `PMID: 12345678`
- Verification: PubMed URL `https://pubmed.ncbi.nlm.nih.gov/{pmid}/`

### ISBNs
- Pattern: `ISBN[:\s]*[\d-]{10,17}` (ISBN-10 or ISBN-13)
- Example: `ISBN: 978-0-13-468599-1`
- Verification: Open Library API `https://openlibrary.org/isbn/{isbn}.json`

### Author-Year Citations
- Pattern: `([A-Z][a-z]+(?:\s+(?:et\s+al\.?|and|&)\s+[A-Z][a-z]+)?,?\s*\d{4})`
- Example: `(Smith et al., 2023)`, `(Johnson and Lee, 2022)`
- Verification: WebSearch to find matching paper (lower confidence)

## Verification Procedure

### Step 1: Read and Parse Document

Use the Read tool to load the document. Extract all citation identifiers using pattern matching:

```
DOI patterns:
- https?://(?:dx\.)?doi\.org/(10\.\d{4,}/[^\s\])"'>]+)
- doi:\s*(10\.\d{4,}/[^\s\])"'>]+)
- (10\.\d{4,9}/[-._;()/:A-Z0-9]+)  (bare DOI)

arXiv patterns:
- arXiv:(\d{4}\.\d{4,5}(?:v\d+)?)
- arxiv\.org/abs/(\d{4}\.\d{4,5}(?:v\d+)?)

PubMed patterns:
- PMID:\s*(\d+)
- pubmed\.ncbi\.nlm\.nih\.gov/(\d+)

URL patterns:
- https?://[^\s\])"'<>]+  (filter for academic domains)

ISBN patterns:
- ISBN[:\s-]*((?:\d[-\s]?){9}[\dXx]|(?:\d[-\s]?){13})
```

### Step 2: Deduplicate and Categorize

Create a list of unique identifiers, categorized by type:
- DOIs
- arXiv IDs
- PubMed IDs
- ISBNs
- URLs (academic)
- Author-year citations (text-based)

### Step 3: Verify Each Identifier

For each identifier, perform verification in order of reliability:

#### DOI Verification
1. Construct CrossRef API URL: `https://api.crossref.org/works/{doi}`
2. Use WebFetch to check the API
3. If successful, extract: title, authors, journal, year
4. If 404 or error: mark as INVALID

#### arXiv Verification
1. Construct URL: `https://arxiv.org/abs/{arxiv_id}`
2. Use WebFetch to verify page exists
3. Extract: title, authors, abstract snippet
4. If 404: mark as INVALID

#### PubMed Verification
1. Construct URL: `https://pubmed.ncbi.nlm.nih.gov/{pmid}/`
2. Use WebFetch to verify
3. Extract: title, authors, journal
4. If 404: mark as INVALID

#### ISBN Verification
1. Construct URL: `https://openlibrary.org/isbn/{isbn}.json`
2. Use WebFetch to check
3. Extract: title, authors, publisher
4. If 404: mark as INVALID

#### URL Verification
1. Use WebFetch to access the URL
2. Check for HTTP 200 and academic content indicators
3. Look for: paper title, authors, DOI on page
4. If unreachable or non-academic: mark as SUSPICIOUS

#### Author-Year Verification (lowest confidence)
1. Use WebSearch with query: `"{author}" "{year}" paper`
2. Look for matching papers in results
3. If found: mark as LIKELY VALID with source
4. If not found: mark as UNVERIFIED

### Step 4: Generate Report

Produce a structured verification report:

```markdown
# Citation Verification Report

**Document:** [filename]
**Date:** [date]
**Total citations found:** [count]

## Summary
- Valid: [count]
- Invalid: [count]
- Suspicious: [count]
- Unverified: [count]

## Detailed Results

### Valid Citations
| ID | Type | Title | Source |
|----|------|-------|--------|
| 10.1038/xxx | DOI | Paper Title | CrossRef |

### Invalid Citations (HALLUCINATED)
| ID | Type | Error | Suggestion |
|----|------|-------|------------|
| 10.9999/fake | DOI | 404 Not Found | Remove or find correct DOI |

### Suspicious Citations
| ID | Type | Issue | Recommendation |
|----|------|-------|----------------|
| https://... | URL | Timeout | Verify manually |

### Unverified Citations
| Citation | Type | Notes |
|----------|------|-------|
| (Smith, 2023) | Author-year | No matching paper found via search |
```

## Verification Status Definitions

- **VALID**: Identifier resolves to a real paper with matching metadata
- **INVALID**: Identifier does not exist or returns 404 (likely hallucinated)
- **SUSPICIOUS**: Could not fully verify; may be rate-limited, paywalled, or temporarily unavailable
- **UNVERIFIED**: Text-based citation that couldn't be confirmed (conservative approach)

## Best Practices

1. **Batch similar requests**: Group DOI checks together to minimize API calls
2. **Respect rate limits**: Add delays between requests if hitting rate limits
3. **Cross-reference**: If a URL contains a DOI, verify the DOI directly
4. **Context matters**: Note where citations appear (methods vs. claims)
5. **Report uncertainty**: Always distinguish between "confirmed invalid" and "could not verify"

## Output Suggestions for Invalid Citations

For each invalid citation, provide actionable suggestions:

- **Wrong DOI format**: "DOI appears malformed. Check for typos or extra characters."
- **Non-existent DOI**: "No paper found. This may be hallucinated. Search for the actual paper title."
- **Dead URL**: "URL returns 404. Try searching for the paper title on Google Scholar."
- **Suspicious journal**: "Publisher not recognized. Verify this is a legitimate source."
- **Author-year not found**: "Could not verify. Add DOI or URL for confirmation."

## Example Verification Session

**User request:** "Verify the citations in my-paper.md"

**Expected behavior:**
1. Read my-paper.md
2. Extract all DOIs, URLs, arXiv IDs, etc.
3. Report: "Found 15 citations: 8 DOIs, 5 URLs, 2 arXiv IDs"
4. Verify each identifier using appropriate API/fetch
5. Generate report showing:
   - 10 valid citations with metadata
   - 3 invalid citations (404 errors) marked as likely hallucinated
   - 2 suspicious citations (timeouts) requiring manual check
6. Provide suggestions for fixing invalid citations

## Limitations

- **Rate limits**: CrossRef and other APIs may rate-limit requests
- **Paywalled content**: Cannot verify full content behind paywalls
- **New papers**: Very recent papers may not be indexed yet
- **Author-year citations**: Low confidence without additional identifiers
- **Non-English sources**: Limited support for non-English citation formats
- **Private/institutional URLs**: Cannot access authenticated content

## Related Skills

- literature-review: For conducting systematic literature searches
- scientific-reviewer: For reviewing scientific document quality
- scientific-writing: For writing with proper citations
