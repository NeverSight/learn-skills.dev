---
name: finance-report-analyzer
description: |
  Analyze financial data from uploaded Excel/PDF files and generate interactive reports with sparkline trend charts. Supports output to PDF, DOCX, Markdown, and HTML.
  Use when: (1) User uploads Excel/CSV/PDF with financial data, (2) User asks for financial analysis or company report, (3) User wants visual reports from financial statements, (4) User mentions stock ticker + financial analysis, (5) User shares a Feishu sheet/doc link with financial data.
---

# Finance Report Analyzer

Generate financial analysis reports from uploaded Excel/PDF files with LLM-powered analysis, competitor analysis, web search for news, and inline SVG sparkline trend charts.

## Architecture

The tool works in a **hybrid pipeline**:

1. **Python script** → Extract data, build tables/charts, render HTML/PDF (deterministic, zero-cost)
2. **LLM (OpenClaw agent)** → Write in-depth analysis for each section + competitor analysis + news summary
3. **Web search** → Fetch recent company news and hot topics

## Report Sections

| # | Section | Source |
|---|---------|--------|
| 一 | 盈利能力分析 | Script(tables) + LLM(analysis) |
| 二 | 资产负债分析 | Script(tables) + LLM(analysis) |
| 三 | 现金流分析 | Script(tables) + LLM(analysis) |
| 四 | 每股指标与效率 | Script(tables) + LLM(analysis) |
| 五 | 行业分析 | LLM |
| 六 | 关键竞争对手分析 | LLM(competitor) |
| 七 | 风险与机遇分析 | LLM |
| 八 | 近期热点新闻 | Web search + LLM |

## Workflow (OpenClaw Agent)

### Step 1: Acquire Data File

Try in order:

1. **Feishu chat file attachment** — Download via API:
   ```bash
   # Get token
   TOKEN=$(curl -s -X POST 'https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal' \
     -H 'Content-Type: application/json' \
     -d '{"app_id":"APP_ID","app_secret":"APP_SECRET"}' | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")
   # Get file_key from message
   curl -s "https://open.feishu.cn/open-apis/im/v1/messages/{message_id}" -H "Authorization: Bearer $TOKEN"
   # Download
   curl -s "https://open.feishu.cn/open-apis/im/v1/messages/{message_id}/resources/{file_key}?type=file" \
     -H "Authorization: Bearer $TOKEN" -o /tmp/data.xlsx
   ```

2. **Feishu Doc/Bitable link** — Use feishu_doc/feishu_bitable tools
3. **Local file** — Use directly

### Step 2: Extract Financial Data (JSON)

```bash
python3 scripts/generate_report.py /tmp/data.xlsx --company "公司名" --ticker "000001.SZ" --output-dir /tmp/reports --json
```

This outputs structured JSON with all financial metrics organized by category.

### Step 3: Web Search for Company News & Competitors

```
web_search("{company} {year} 最新新闻 业绩 研发 重大事件")
web_search("{company} 竞争对手 市场份额 行业对比")
```

Summarize 5-8 key news items as HTML list. Save to `/tmp/reports/news.html`.

### Step 4: LLM Analysis

Based on the JSON data from Step 2 and search results from Step 3, write professional analysis for **7 sections**. Save as JSON to `/tmp/reports/analysis.json`:

```json
{
  "profitability": "HTML text - revenue trends, margins, profitability inflection points...",
  "balance_sheet": "HTML text - asset structure, leverage, liquidity...",
  "cash_flow": "HTML text - operating CF trends, capex, FCF, cash reserves...",
  "per_share": "HTML text - EPS/BPS trends, efficiency ratios, workforce...",
  "industry": "HTML text wrapped in <div class=\"analysis-box\">...",
  "competitor": "HTML text - competitor table + strategic analysis (see format below)",
  "risk": "...",
  "growth": "增长动力分析 HTML...",
  "rd_analysis": "研发效率分析 HTML...",
  "dupont": "杜邦分析(ROE拆解) HTML..."
}
```

**Analysis guidelines:**
- Use `<strong>` for key conclusions as the opening line
- Use `<br><br>` for paragraph breaks
- Reference specific numbers from the data
- Compare year-over-year trends
- Highlight inflection points and turning points
- For risk section, use the two-column float layout with `.risk-list`

**Competitor section format:**
```html
<div class="analysis-box"><strong>Summary of competitive landscape</strong></div>
<table>
<tr><th style="text-align:left">竞争对手</th><th style="text-align:left">核心竞品</th><th style="text-align:left">竞争领域</th><th style="text-align:left">威胁程度</th></tr>
<tr><td style="text-align:left">Company A</td><td style="text-align:left">Product</td><td style="text-align:left">Domain</td><td style="text-align:left; color:#dc2626">直接竞争</td></tr>
</table>
<div class="analysis-box">Detailed competitive analysis...</div>
```

### Step 5: Generate Final Report

```bash
python3 scripts/generate_report.py /tmp/data.xlsx \
  --company "公司名" --ticker "000001.SZ" \
  --output-dir /tmp/reports \
  --analysis-json /tmp/reports/analysis.json \
  --news-html /tmp/reports/news.html \
  -o html,pdf
```

### Step 6: Deliver Files via Feishu API

```bash
# Upload and send file
FK=$(curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/files' \
  -H "Authorization: Bearer $TOKEN" \
  -F 'file_type=stream' -F "file_name=report.html" -F "file=@/tmp/reports/report.html" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['file_key'])")

curl -s -X POST 'https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id' \
  -H "Authorization: Bearer $TOKEN" -H 'Content-Type: application/json' \
  -d "{\"receive_id\":\"CHAT_ID\",\"msg_type\":\"file\",\"content\":\"{\\\"file_key\\\":\\\"$FK\\\"}\"}"
```

## CLI Reference

```bash
# JSON data export (for LLM pipeline)
python3 scripts/generate_report.py input.xlsx --json --company NAME --ticker TICKER --output-dir DIR

# Full report with LLM analysis + competitor + news
python3 scripts/generate_report.py input.xlsx \
  --analysis-json analysis.json \
  --news-html news.html \
  --company NAME --ticker TICKER \
  -o html,pdf --output-dir DIR

# Standalone (rule-based analysis, no LLM needed)
python3 scripts/generate_report.py input.xlsx --company NAME --ticker TICKER -o html,pdf
```

## Output Formats

| Flag | Output | Requires |
|------|--------|----------|
| `-o html` | HTML only | (built-in) |
| `-o pdf` | HTML + PDF | wkhtmltopdf |
| `-o doc` | HTML + DOCX | pandoc |
| `-o md` | HTML + Markdown | pandoc or markdownify |

## Report Features

- **LLM-powered analysis**: Deep, contextual financial commentary (when using --analysis-json)
- **Competitor analysis**: Key competitors table + strategic competitive assessment
- **Company news section**: Recent hot topics and events (when using --news-html)
- **Sparkline trend charts**: SVG mini-charts in each data row
- **Forecast markers**: Predicted values with ⟡ symbol and yellow background
- **PDF compatible**: No emoji/flex/gradient/CSS variables (works with wkhtmltopdf)
- **Fallback mode**: Rule-based analysis when no LLM analysis is provided
