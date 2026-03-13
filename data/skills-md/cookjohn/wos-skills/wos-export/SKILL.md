---
name: wos-export
description: Export WoS records to Zotero, RIS, BibTeX, or Excel.
argument-hint: "[zotero/ris/bibtex/excel] [WoS IDs or 'current']"
user-invocable: true
disable-model-invocation: true
---

# WoS Export

Export WoS paper records. Two modes: direct Zotero push (preferred) or file export via UI.

## Mode A: Push to Zotero (preferred, no UI interaction)

Collect paper metadata (from prior search/detail results) and push to Zotero via the `push_to_zotero.py` script.

### Step 1: Prepare Paper Data

Build a JSON object from data already available in the conversation (from `wos-search` API results or `wos-paper-detail` extraction). The script accepts WoS paper fields directly:

```json
{
  "title": "Value co-creation in service logic",
  "authors": "Grönroos, C",
  "source": "MARKETING THEORY",
  "year": 2011,
  "volume": "11",
  "issue": "3",
  "pages": "279-301",
  "doi": "10.1177/1470593111408177",
  "issn": "1470-5931",
  "abstract": "The underpinning logic of...",
  "language": "English",
  "accessionNumber": "WOS:000295471900004",
  "authorKeywords": ["value co-creation", "service logic"],
  "keywordsPlus": ["DOMINANT LOGIC"],
  "citedCount": "992",
  "alldbCited": "1,254",
  "jif": "2.8",
  "jifYear": "2024",
  "jcrQuartile": "Q3",
  "researchAreas": "Business & Economics",
  "wosCategories": "Business",
  "docType": "Article"
}
```

For multiple papers, wrap in an array or `{"items": [...]}`.

### Step 2: Push via Script

```bash
echo '{JSON_DATA}' | python "e:\wos-skills\.claude\skills\wos-export\scripts\push_to_zotero.py"
```

Or save to temp file first (recommended for large data or Chinese characters):
```bash
python "e:\wos-skills\.claude\skills\wos-export\scripts\push_to_zotero.py" /tmp/wos_export.json
```

### Step 3: Report Result

- `OK: Saved (session: xxx)` → success
- `OK: Already saved (session: xxx)` → idempotent, no duplicates
- `Error: Zotero not running` → tell user to start Zotero desktop

The script auto-detects Zotero's currently selected collection. User can change target by selecting a different folder in Zotero before exporting.

To list collections: `python push_to_zotero.py --list`

## Mode B: File Export via UI (fallback)

When Zotero is not available or user specifically wants a file.

### Prerequisites

Browser must be on a WoS results page (`/summary/...`) or full record page (`/full-record/...`).

### Supported Formats

| Format | Menu Item | File |
|--------|-----------|------|
| RIS | "RIS (other reference software)" | .ris |
| BibTeX | "BibTeX" | .bib |
| Excel | "Excel" | .xlsx |
| Plain Text | "Plain text file" | .txt |
| Fast 5000 | "Fast 5000" | Quick export |

### Steps

1. `take_snapshot` → find Export button (`button` with `haspopup="menu"` containing "Export") → `click`
2. `take_snapshot` → find format menuitem → `click`
3. Handle export dialog (record range, content options) → click download button

### Notes on UI Export

- Uses 3-4 tool calls: snapshot + click Export + snapshot + click format + dialog
- "Fast 5000" exports up to 5000 records with basic fields
- On full-record page, exports only the current record

## Zotero Script Features

- **Deterministic session ID**: Same papers always produce the same session ID (content hash). Prevents duplicates on retry (409 → treated as success).
- **WoS metadata mapping**: Automatically maps WoS fields to Zotero's journalArticle schema.
- **Extra field**: Stores WoS-specific data (WoS ID, citation counts, JIF, JCR quartile, research areas) in Zotero's Extra field.
- **Author parsing**: Handles WoS standard format "LastName, Initials" → Zotero firstName/lastName.
- **Keywords**: Both Author Keywords and Keywords Plus are added as Zotero tags.

## Notes

- Mode A (Zotero push) requires no browser interaction — uses data from prior API calls
- Mode A works even when browser is not on a WoS page
- Script path: `e:\wos-skills\.claude\skills\wos-export\scripts\push_to_zotero.py`
- Zotero must be running on localhost:23119
