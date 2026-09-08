---
name: pubmed-literature-search
description: >
  Search 36M+ citations from PubMed and PubMed Central. Advanced search with
  boolean operators, MeSH terms, author/journal filters, and full-text
  access.
---

# PubMed Medical Literature Search

Search over 36 million biomedical citations from PubMed and PubMed Central using the NCBI E-utilities API. This skill enables AI agents to perform advanced literature searches with boolean operators, MeSH term expansion, author and journal filtering, date range restrictions, and direct full-text access links -- bringing the power of systematic literature review directly into clinical and research AI workflows.

## Quick Install

```bash
npx skills add Open-Medica/open-medical-skills --skill pubmed-literature-search
```

## What It Does

- **Advanced boolean search** across PubMed's entire 36M+ citation database using AND, OR, NOT operators with field-specific qualifiers (title, abstract, author, journal, MeSH)
- **MeSH term integration** for standardized medical vocabulary searches, including automatic term explosion to capture narrower descriptors in the MeSH hierarchy
- **Citation metadata retrieval** including authors, journal, publication date, DOI, PubMed ID, abstract text, MeSH headings, and publication type
- **Full-text access links** via PubMed Central (PMC) when articles are available open-access, with fallback to DOI resolver links
- **Date-range and filter support** to restrict results by publication year, article type (RCT, meta-analysis, review, case report), language, and species (human/animal)

## Clinical Use Cases

- **Systematic literature review**: A researcher preparing a systematic review on SGLT2 inhibitors in heart failure can construct complex boolean queries with MeSH terms, retrieve all matching citations with abstracts, and export structured results for screening -- replacing hours of manual PubMed navigation.
- **Point-of-care evidence lookup**: A hospitalist encountering an unusual drug reaction can quickly search for case reports and pharmacovigilance studies linking the specific drug and adverse event, receiving summarized abstracts within seconds.
- **Guideline development support**: A clinical guideline committee can programmatically search for all RCTs and meta-analyses on a specific intervention, filter by date range and quality indicators, and generate a structured evidence table for committee review.
- **Research gap identification**: An academic physician planning a grant proposal can query existing literature on a topic, identify the most recent publications, and determine where evidence gaps remain to justify new research.

## Safety & Evidence

- **Safety Classification:** Safe -- This skill queries a public, read-only database (NCBI PubMed). It does not make clinical decisions, alter patient data, or prescribe treatments. All returned data consists of published, peer-reviewed citations.
- **Evidence Level:** High -- PubMed is the gold-standard biomedical literature database maintained by the U.S. National Library of Medicine (NLM). The E-utilities API is the official programmatic interface used by thousands of research institutions worldwide.

## Example Usage

**Search for recent meta-analyses on metformin and cardiovascular outcomes:**
```
Search PubMed for meta-analyses published in the last 5 years
examining metformin's effect on cardiovascular mortality in
type 2 diabetes. Use MeSH terms and restrict to English-language
articles.
```

**Find case reports of a rare adverse drug reaction:**
```
Search PubMed for case reports of pembrolizumab-induced
myocarditis. Include the abstract text and PMC full-text links
where available. Sort by most recent first.
```

## Technical Details

- **Category:** Research
- **Author:** OMS Contributors (original: Augmented-Nature)
- **License:** MIT
- **API:** NCBI E-utilities (ESearch, EFetch, ESummary, ELink)
- **Rate Limits:** NCBI allows 3 requests/second without API key, 10 requests/second with a free NCBI API key
- **Dependencies:** HTTP client (curl/fetch), XML/JSON parser

## References

- NCBI E-utilities Documentation: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- PubMed Help Guide: https://pubmed.ncbi.nlm.nih.gov/help/
- MeSH Browser: https://meshb.nlm.nih.gov/
- NCBI API Key Registration: https://www.ncbi.nlm.nih.gov/account/settings/

---

*This skill is part of [Open Medical Skills](https://github.com/Open-Medica/open-medical-skills), a curated marketplace of medical AI skills maintained by physicians for physicians and the healthcare industry.*
