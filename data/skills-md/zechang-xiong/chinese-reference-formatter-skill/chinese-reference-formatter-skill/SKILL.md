---
name: chinese-reference-formatter-skill
description: 根据中英文文献题名核验公开元数据，生成通用中文参考文献和 BibTeX。Use for Chinese academic references, GB/T 7714-style bibliography formatting, and citation completion from literature titles.
license: MIT
compatibility: Requires an agent with web search, file access, and Python execution. The offline formatter uses Python 3.9+ standard library only.
metadata:
  author: Zechang-Xiong
  version: "1.1.1"
  repository: https://github.com/Zechang-Xiong/chinese-reference-formatter-skill
  tags: chinese-references, bibliography, bibtex, gb-t-7714, academic-writing
---

# Chinese Reference Formatter

## Overview

Convert one or more Chinese or English reference titles into 通用中文论文参考文献条目 and BibTeX. Verify bibliographic metadata from public sources before formatting; do not invent missing references. When search is unavailable, explain that verification cannot be completed; do not describe unverified input as confirmed.

The formatter implements the common numeric templates in the reference file. It is not a complete implementation of GB/T 7714—2015 or GB/T 7714—2025. For a specified edition or institutional style, compare the requested rules with the output and adapt it before claiming compliance. See the reference file for version scope.

## Workflow

1. Read `references/chinese-reference-rules.md` before formatting.
2. For each input title, search public metadata sources and compare title, authors, year, venue, DOI/ISBN/URL.
3. Prefer DOI, publisher, university repository, official journal, official conference, official standards, or patent pages over aggregators.
4. If no DOI or official page exists, require a strong title match plus matching author/year/venue from at least one credible source.
5. If sources conflict and no source is clearly authoritative, return an ambiguity note instead of choosing.
6. If no clear match exists, output `未找到与“<title>”明确对应的公开文献。`
7. Normalize confirmed metadata to JSON and run `scripts/format_reference.py` to produce the reference entry plus BibTeX. Preserve the verified source title's capitalization. Set `language` (`zh` or `en`) when known, especially when the author script differs from the document language.

## Search Sources

Use sources appropriate to the document type:

- DOI and publisher metadata: Crossref, DataCite, official publisher pages.
- Broad scholarly metadata: OpenAlex, Semantic Scholar.
- Computer science papers: DBLP, arXiv, conference/open-review pages.
- Biomedical papers: PubMed/NCBI and official journal pages.
- Chinese references: DOI/publisher pages, university repositories, official journal pages; use CNKI/Wanfang metadata when reachable from web search.
- Standards, patents, books, theses: official standards bodies, patent offices, publishers, library catalogs, university repositories.

## Formatting

The formatter accepts a JSON object, a JSON list, or `{ "items": [...] }` through stdin or `--input`.

```bash
python3 /path/to/chinese-reference-formatter-skill/scripts/format_reference.py --start 1 < metadata.json
```

Resolve the script and reference paths relative to this installed skill, not the user's working directory. Replace the example absolute path above with the actual skill directory.

Common normalized fields (plain text, not pre-escaped LaTeX):

For ambiguous personal names, prefer `{ "family": "Smith", "given": "John", "suffix": "Jr." }` or the explicit string `Smith, Jr., John`. Use `{ "literal": "Organization name" }` for institutions. Omit unknown authors; blank placeholders are ignored.

```json
{
  "type": "article",
  "title": "Paper title",
  "authors": ["Family, Given", "中文作者"],
  "journal": "Journal name",
  "booktitle": "Proceedings name",
  "year": 2026,
  "language": "en",
  "volume": "12",
  "issue": "3",
  "pages": "1-10",
  "doi": "10.xxxx/example",
  "url": "https://example.org",
  "access_date": "2026-05-07",
  "sources": ["https://source.example"]
}
```

Supported `type` values include `article`, `inproceedings`, `book`, `chapter`, `thesis`, `mastersthesis`, `phdthesis`, `report`, `standard`, `patent`, `newspaper`, and `online`. For `thesis`, set `degree` to `master` or `phd` only when verified; an unknown degree uses `@misc` in BibTeX. Set `mark` to `J/OL`, `C/OL`, etc. when the requested style needs an online carrier, and supply the actual `access_date` and `url` (or DOI). A URL alone does not change a traditional document into an online resource.

Default output for each resolved item:

````text
标准参考文献：[1] ...
BibTeX：
```bibtex
...
```
核验来源：...
````

Preserve the user's input order. Start numbering at `[1]` unless the user gives a different starting number. Send a batch in one formatter invocation so duplicate citation keys receive unique suffixes. Do not append to a project `.bib` file unless the user explicitly asks; when updating existing entries, preserve their keys to avoid breaking manuscript citations.

## Conflict Rules

- DOI or official source metadata wins over aggregator metadata.
- Publisher version wins over preprint metadata when formatting the published version.
- Preprint metadata is valid only when the user asks for the preprint or no published version exists.
- Keep type, venue, year, URL, and DOI from the same publication version. An arXiv-issued DOI identifies the preprint record; do not attach it to a conference or journal record as that publication's DOI.
- If author order, year, venue, or page range conflicts, state the conflict and cite the competing sources.
- Use the actual current date for online access dates unless the source provides a citation access date or the user specifies one.

## Common Mistakes

- Do not format from title guesses alone.
- Do not silently translate titles or author names.
- Do not list more than three authors before `等` or `et al`.
- Do not force a school-specific thesis requirement unless the user explicitly provides that institution's rules.
- Do not count online resources or standards as ordinary journal/conference papers unless the user's style guide explicitly says to.
