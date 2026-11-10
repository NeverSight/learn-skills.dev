---
name: doi-bibtex
user_invocable: true
description: Fetch a BibTeX citation from a DOI and optionally add it to a bibliography. Use when the user provides a DOI or DOI URL and wants the citation displayed or added to a .bib file.
---

# DOI to BibTeX

## Fetch BibTeX

```bash
./scripts/doi2bib.sh <DOI>
```

> Paths are relative to this skill's directory.

Accepts bare DOIs (`10.1038/nature12373`) or full URLs.

## Workflow

1. Fetch and inspect the BibTeX entry.
2. If the user asked only for the citation, return it without modifying files.
3. If the user asked to add it, use an explicit bibliography path when provided. Otherwise, inspect the paper's bibliography declarations and nearby `.bib` files. Ask only when the destination is ambiguous.
4. Search the destination for the normalized DOI before appending. Report an existing entry instead of creating a duplicate, and preserve the file's formatting when adding a new entry.
