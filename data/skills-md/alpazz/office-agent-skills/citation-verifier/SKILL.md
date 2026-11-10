---
name: citation-verifier
description: "Verify citations and references in scientific documents to detect hallucinated, invalid, or mismatched sources. Extracts DOIs, arXiv IDs, PubMed IDs, ISBNs, and URLs from Word (.docx), BibTeX (.bib), Markdown (.md), LaTeX (.tex), and plain text, then validates them using CrossRef, arXiv, PubMed, and Open Library APIs. Detects AI hallucinations where real identifiers are paired with fabricated paper titles."
license: MIT
---

# Citation & Reference Verifier

Detects and flags hallucinated, broken, or mismatched references in academic manuscripts and office documents.

## Purpose

Large Language Models frequently invent convincing but nonexistent citations or pair real DOIs with fabricated paper titles. This skill scans documents, queries authoritative registries (CrossRef, arXiv, PubMed, Open Library), and produces structured audit reports.

---

## When to Use

- Verifying reference lists in research papers, theses, or technical reports.
- Checking Word documents (`.docx`) containing native Zotero or legacy Mendeley Desktop CSL fields.
- Validating BibTeX libraries (`.bib`) before submitting papers to journals.
- Auditing Markdown (`.md`), LaTeX (`.tex`), or text drafts for broken URLs and hallucinated DOIs.
- Running automated CI/CD citation checks on manuscripts.

---

## Supported Identifiers and Registries

| Identifier | Verification Source | Detection Pattern | Notes |
|---|---|---|---|
| **DOI** | CrossRef REST API | `10.xxxx/...` or `doi.org/...` | Checks registry existence and performs fuzzy title comparison. |
| **arXiv ID** | arXiv API | `arXiv:YYMM.NNNNN` or `arxiv.org/abs/...` | Checks official arXiv feed and resolves preprint titles. |
| **PubMed PMID** | NCBI E-utilities | `PMID: NNNNNNN` | Queries PubMed for biomedical literature. |
| **ISBN** | Open Library API | `ISBN: 978-...` | Validates books and monographs. |
| **Publisher URLs** | HTTP GET/HEAD | Nature, IEEE, Springer, ScienceDirect, etc. | Verifies live HTTP 200/300 status codes. |

---

## Command Line Usage

Run the verification script against any manuscript or bibliography file:

```bash
# 1. Standard terminal check (compatible with Windows cp1252)
python scripts/verify_citations.py manuscript.docx

# 2. Generate a clean Markdown audit report for peer review
python scripts/verify_citations.py draft.md --format markdown --output audit_report.md

# 3. Export machine-readable JSON for CI/CD pipelines
python scripts/verify_citations.py library.bib --format json --output audit.json

# 4. Strict mode: exit code 1 on any failure or title mismatch
python scripts/verify_citations.py paper.tex --strict

# 5. Audit every cited sentence against retrieved abstract evidence
python scripts/verify_citations.py manuscript.docx --claim-audit \
  --strict-claims --format markdown --output claim-audit.md

# 6. Add lawful local full text for page/section evidence.
#    Filename must contain the normalized identifier, for example:
#    evidence/10.1234-example.pdf
python scripts/verify_citations.py manuscript.docx --claim-audit \
  --citation-map citation-map.json --evidence-dir evidence \
  --strict-claims --format markdown --output evidence-ledger.md
```

### Options

- `--format {text,markdown,json}`: Report format (default: `text`).
- `-o, --output PATH`: Write report to file instead of stdout.
- `--email EMAIL`: Contact email for the CrossRef polite API pool.
- `--strict`: Return exit code 1 if any citation is missing or has a mismatched title.
- `--claim-audit`: Map each cited sentence to evidence retrieved from the cited source. Numeric or author-year markers that cannot be mapped are reported as `UNMAPPED_CITATION`.
- `--strict-claims`: Return exit code 1 unless every cited sentence reaches `ABSTRACT_SUPPORT`.
- `--evidence-dir PATH`: Read user-supplied full-text PDF, Markdown, or text files and attach page/excerpt evidence to the ledger.
- `--citation-map PATH`: Map numeric markers such as `[1]` to identifiers; unmapped markers remain failures.
- `--no-cache`: Force live API requests bypassing `.citation_cache.json`.
- `--timeout SECONDS`: Network timeout per request (default: 10).

---

## Anti-Hallucination Logic

When verifying DOIs or arXiv papers with title metadata (e.g. from Zotero field codes or BibTeX entries), the verifier compares the local title against the authoritative title in CrossRef:

1. **`[PASS]`**: Identifier exists and the paper title matches (similarity $\ge 0.65$).
2. **`[WARN] METADATA_MISMATCH`**: Identifier exists, but the registry title differs significantly. This catches AI models that attach real DOIs to fake papers.
3. **`[FAIL] NOT_FOUND`**: Identifier does not exist in the official registry.
4. **`[ERR ] LOOKUP_ERROR`**: Temporary network failure or service downtime (never falsely marked as hallucinated).

### Claim-to-evidence rule

Identifier verification and claim verification are separate gates. With
`--claim-audit`, each sentence containing a DOI, PMID, arXiv identifier,
numeric marker, or author-year marker is audited. The verifier only emits
`ABSTRACT_SUPPORT` when the identifier is mapped in the same sentence and the
sentence has conservative lexical overlap with retrieved abstract evidence.
It emits `ABSTRACT_NO_SUPPORT`, `EVIDENCE_UNAVAILABLE`, or
`UNMAPPED_CITATION` otherwise. These statuses are intentionally conservative:
they never prove that a detailed, causal, quantitative, or negative claim is
true. Those claims still require reading the full paper and recording page or
section evidence.

---

## Credits

- Concept and regex patterns based on [`jkitchin/skillz`](https://github.com/jkitchin/skillz) by John Kitchin.
