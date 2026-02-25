---
name: knowledgelm-nse
description: >
  Batch download Indian company filings (transcripts, investor presentations,
  credit ratings, annual reports, share issuance documents) from NSE and valuepickr threads. Optionally add to NotebookLM.
  Use when user asks to: (1) Download investor materials for Indian publicly 
  listed companies, (2) Research Indian stocks/companies, (3) Create research 
  notebooks with company filings, or (4) Analyze NSE-listed company documents.
metadata:
  author: eggmasonvalue
  version: 1.1.0
  homepage: https://github.com/eggmasonvalue/knowledgelm-nse
---

# KnowledgeLM NSE

Batch download Indian company filings from NSE and optionally integrate with NotebookLM.

## Installation

Check if installed: `knowledgelm --version`
If not: `uv tool install knowledgelm`
To upgrade: `uv tool upgrade knowledgelm`

## Skill Upgrade

To keep this skill up-to-date, run:
```bash
npx skills update
```

## Command Discovery

**Use `--help` extensively to discover options and to determine the next steps**

```bash
knowledgelm --help
knowledgelm download --help
```

## Core Workflow

### 1. Gather Required Information

**NSE Symbol:** If not provided, use `web_search` to find it.

**Date Range:** If not provided, ask for clarification. Accept various formats:
- Explicit: `"2023-01-01 to 2025-01-26"`, `"2023 to 2025"`, `"from 2023"`
- Relative: `"last 2 years"`
- Milestones: `"Since IPO"`, `"since <event>"` (use `web_search` to resolve dates)

Convert to `YYYY-MM-DD` for CLI.

**Categories:** Default to all categories if not specified. Use `--annual-reports-all` by default.

Available: `transcripts`, `investor_presentations`, `credit_rating`, `annual_reports`, `related_party_txns`, `press_releases`, `issue_documents`

**Share Issuance Documents note:** Use the `issue_documents` when the user asks about docs related to events involving issuance of shares: IPO prospectus, rights issues, QIP placements, information memoranda, or scheme of arrangement documents.

### 2. Download Filings

Use `knowledgelm download` with appropriate flags. Files save to `./{SYMBOL}_filings/`.

### 3. List Files (if needed)

Use `knowledgelm list-files` with `--json` flag to get file paths (excludes `.pkl` cookies).

## NotebookLM Integration

**The below is a comprehensive CLI for Google NotebookLM - offers full programmatic access to NotebookLM's features from the command line**

Follow this if the user wants to create a notebook

### 1. Ensure Latest Package Version

Check if installed and upgrade to latest:

```bash
notebooklm --version
```

If not installed:
```bash
uv tool install notebooklm-py
```

If installed, upgrade to latest:
```bash
uv tool upgrade notebooklm-py
```

**Browser extras (for first-time setup):** If user hasn't authenticated with NotebookLM before, they need browser login support:

```bash
uv tool install --reinstall "notebooklm-py[browser]"
playwright install chromium
```

### 2. Create Notebook

**Use `--help` extensively to discover options and to determine the next steps**

```bash
notebooklm --help
notebooklm source add --help
```

Use the notebooklm CLI to create a **new** notebook and add downloaded files to that notebook(exclude `.pkl` files).

## 6. Follow-up:

### Highly likely add-on - Valuepickr forum as a source

- Use `web_search` to find the company's thread URL on `forum.valuepickr.com`.
- Run `knowledgelm forum <URL> --symbol <SYMBOL>`. Files saved to `./{SYMBOL}_valuepickr/`. 
- **Artifacts:** 1. thread  2. popular links in the thread in a .md
- **Note**:
  - This is a forum thread and may not fit as an upload to notebookLM as a source of truth. 
  - The output is well-formatted to be vastly more distraction-free and print-friendly compared to the site.

  Make the user understand both and offer it as just a download or as a potential source

```bash
knowledgelm forum "https://forum.valuepickr.com/t/nrb-bearings-ev-and-exports-to-drive-growth/106674" --symbol NRBBEARING
```

### Add-on - Resignations query

Offer to check KMP resignations and cessations. Returns structured JSON (no files downloaded) — useful as a quick governance signal.

```bash
knowledgelm resignations SYMBOL --from 2020-01-01 --to 2025-12-31
```

### Optional - Audio Overview Generation:
For generating audio overviews focused on fundamental analysis, use the prompt template at `references/notebooklm_audio_prompt.md` as a system prompt to notebookLM. This provides structured guidance for creating investor-focused audio summaries.

### General:
End with a call-to-action to help the user benefit further from the available features.

## Exception Handling

- **Invalid symbol:** CLI returns `"success": false` in JSON
- **Network issues:** Retry once after 5 seconds
- **Incomplete data:** May indicate newly listed company on the NSE mainboard or corporate action. Use `web_search` to verify.
