---
name: report-download
description: >
  **Financial Report Downloader**: Auto-search and download A-share/HK stock financial report PDFs from Xueqiu (stockn.xueqiu.com) or 同花顺 (notice.10jqka.com.cn).
  - MANDATORY TRIGGERS: download report, 下载财报, 下载年报, 下载中报, annual report download, financial report PDF, 雪球财报, 同花顺财报

version: 0.1.0
---

# Financial Report PDF Downloader

Download A-share and Hong Kong stock financial report PDFs from `stockn.xueqiu.com` (雪球) with `notice.10jqka.com.cn` (同花顺) as fallback. Both sources enable reliable automated downloads.

## Workflow

```
Input (stock code, year, report type)
  → Step 0: Parse & detect market
  → Step 1: WebSearch for PDF on stockn.xueqiu.com
  → Step 2: Extract matching PDF URLs
  → Step 3: Identify correct report (filter out summaries, audit reports, etc.)
  → Step 4: Python script downloads PDF to local disk
  → Output: local PDF file path
```

## Step 0: Parse Input

Parse user input into three parts:
- **stock_code** (required): stock ticker
- **year** (optional): defaults to latest available
- **report_type** (optional): defaults to 年报

### Market Detection

| Pattern | Market | Formatting | Example |
|---------|--------|-----------|---------|
| 6-digit starting with `6` | Shanghai A-share | Prefix `SH` | `600887` → `SH600887` |
| 6-digit starting with `0` or `3` | Shenzhen A-share | Prefix `SZ` | `300750` → `SZ300750` |
| 1-5 digits | Hong Kong | Zero-pad to 5 digits | `700` → `00700` |
| Already has `SH`/`SZ` prefix | Use as-is | — | `SH600887` |

### Report Type Mapping

| User Input | report_type | A-share Search Keyword | HK Search Keyword | Publish Time |
|-----------|-------------|----------------------|-------------------|-------------|
| 年报 / annual | 年报 | 年度报告 | annual report | Next year Mar-Apr |
| 中报 / interim | 中报 | 半年度报告 | interim report | Same year Aug-Sep |
| 一季报 / Q1 | 一季报 | 第一季度报告 | *(A-share only)* | Same year Apr |
| 三季报 / Q3 | 三季报 | 第三季度报告 | *(A-share only)* | Same year Oct |

## Step 1: Search for the Report

Use **WebSearch** with this query pattern:

**A-share:** `site:stockn.xueqiu.com {formatted_code} {search_keyword} {year}`
**HK:** `site:stockn.xueqiu.com {formatted_code} {hk_search_keyword} {year}`

If no year specified: try current year first, then previous year.
If no results from Xueqiu:
1. Retry with **同花顺**: `site:notice.10jqka.com.cn {formatted_code} {search_keyword} {year}`
   - Can also try with company name, e.g.: `site:notice.10jqka.com.cn 伊利股份 2024 年度报告`
2. If still no results: retry without any `site:` prefix as a last resort.

## Step 2: Extract PDF Links

Filter search results for PDF URLs from supported sources:
- `https://stockn.xueqiu.com/.../*.pdf`
- `https://notice.10jqka.com.cn/.../*.pdf`

## Step 3: Identify Correct Report

**Exclude** results with titles containing:
摘要, 审计报告, 公告, 利润分配, 可持续发展, 股东大会, ESG, summary, auditor, dividend, 更正, 补充, 意见, 内部控制

**Prefer** results where:
1. Title contains the report keyword (e.g. "年度报告") WITHOUT "摘要"
2. URL date closest to expected publish date
3. If tied, pick first result

If no candidates remain: inform user and suggest verifying stock code/year/report type.

## Step 4: Download the PDF

Install dependency if needed:
```bash
pip install requests --break-system-packages
```

Run the download script (located at `${CLAUDE_PLUGIN_ROOT}/skills/report-download/scripts/download_report.py`):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/report-download/scripts/download_report.py \
  --url "<PDF_URL>" \
  --stock-code "<formatted_stock_code>" \
  --report-type "<report_type>" \
  --year "<year>" \
  --save-dir "."
```

### Parse Output

The script prints a structured block between `---RESULT---` and `---END---`:
- `status`: SUCCESS or FAILED
- `filepath`: absolute path to downloaded file
- `filesize`: file size in bytes
- `message`: status message

### Report to User

**On success:** Report file path, size (human-readable MB), stock code, year, report type.
**On failure:** Report error message. Suggest checking URL accessibility, retrying, or verifying inputs.
