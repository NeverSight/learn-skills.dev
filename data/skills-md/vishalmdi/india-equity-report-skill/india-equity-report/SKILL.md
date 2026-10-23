---
name: india-equity-report
description: Generate a detailed Buy/Sell/Hold equity research report for Indian stock market (NSE/BSE listed companies). Use this skill whenever the user asks for a stock analysis, equity research, investment recommendation, target price, fundamental analysis, technical analysis, or buy/sell/hold opinion on any Indian company or stock. Triggers on phrases like "analyse [stock]", "should I buy [stock]", "research report for [company]", "target price for [stock]", "is [stock] a good buy", "NSE/BSE stock analysis", etc. Always use this skill for any Indian equity research request — even if the user just names a stock ticker or company and asks "what do you think?"
---

# India Equity Research Report Skill

Generates institutional-quality Buy / Sell / Hold research reports for NSE/BSE-listed stocks, grounded entirely in **live data fetched from authoritative sources**. Never hallucinate financial figures.

---

## 0. Pre-flight: Read the data sources reference

Before writing a single word of the report, read `/mnt/skills/user/india-equity-report/references/data-sources.md` (or the bundled copy at `references/data-sources.md`) for the definitive list of approved sources and fetch URLs. **Do not use any source not listed there.**

---

## 1. Workflow

### Step 1 — Identify the stock
- Resolve the company name → NSE ticker (e.g., RELIANCE, INFY, HDFCBANK).
- Confirm exchange: NSE preferred; BSE fallback (prefix `BSE:` if NSE unavailable).
- If ambiguous, ask the user to confirm before proceeding.

### Step 1.5 — Fetch the Live CMP (MANDATORY — do this before anything else)

> ⚠️ **CRITICAL**: Screener.in's page often displays a **stale cached price** (e.g., it may show "13 Feb - close price" even when the report is run on Feb 27). **Never use the price shown on the Screener.in page as the CMP.** It is unreliable.

> ⚠️ **CRITICAL**: Yahoo Finance (HDFCBANK.NS etc.) shows **US-session delayed quotes** that can differ from the NSE close price by 10–15%. **Do NOT use Yahoo Finance as a CMP source.** It is structurally unreliable for Indian stocks.

#### The canonical CMP fetch method

Claude cannot execute GOOGLEFINANCE (that runs only in a live Google Sheet). Instead, use web search — Google's search result card pulls from the same Google Finance data feed and is equally reliable:

**Step-by-step:**

1. Run `web_search: "[TICKER] NSE share price [CURRENT MONTH YEAR]"` (e.g., "HDFCBANK NSE share price March 2026")
2. **Read the price number from the Google Finance card in the search snippet** — this is the current or last-close price from Google Finance.
3. If the search snippet doesn't show a clear price, run `web_fetch: https://www.tickertape.in/stocks/[company-slug]-[TICKER]` — Tickertape shows a clearly date-stamped last NSE closing price.
4. As an additional fallback: `web_fetch: https://www.5paisa.com/stocks/[company-slug]-share-price` — 5Paisa also shows confirmed NSE close with date.
5. **Confirm the date**: The price must be from the most recent trading day. If the date shown is more than 3 trading days old, flag it as "last available closing price as of [DATE]".
6. **Record it as a concrete number**: e.g., `CMP: ₹869.05 [Source: Tickertape/NSE, 4 Mar 2026]`

> ⚠️ **DO NOT** write raw formulas like `=GOOGLEFINANCE("NSE:HDFCBANK","price")` as the CMP in the report. Always resolve these to actual fetched numbers before writing the report. The report must display real prices (e.g., ₹869.05), never spreadsheet formulas.

**Do not proceed to Step 2 until you have a concrete ₹ price with a date.**

### Step 2 — Fetch all raw data (do this BEFORE writing the report)

Use `web_search` and `web_fetch` tools sequentially. Fetch **every** section below. Log each fetch with the source URL so the report can cite it.

| Data needed | Primary source | Fallback |
|---|---|---|
| Current price, 52w high/low, market cap | **Step 1.5 above** (dedicated CMP fetch — NOT Screener.in or Yahoo Finance) | See Step 1.5 fallback chain |
| Quarterly & annual P&L, balance sheet, cash flow | Screener.in — `https://www.screener.in/company/[TICKER]/consolidated/` | Tickertape.in |
| Key ratios (P/E, P/B, ROE, ROCE, D/E, EV/EBITDA) | Screener.in same page | Trendlyne.com |
| Promoter & institutional shareholding | Screener.in shareholding tab | BSE filings |
| Latest quarterly results (numbers + commentary) | BSE corporate filings: `https://www.bseindia.com/stock-share-price/[COMPANY]/[TICKER]/[BSE_CODE]/` | NSE: `https://www.nseindia.com/get-quotes/equity?symbol=[TICKER]` |
| Annual report / investor presentation | Company IR page (search: `"[COMPANY]" investor relations annual report site:[company].com`) | BSE filings PDF |
| Management commentary & concall highlights | Screener.in concall transcripts tab OR `web_search: "[COMPANY] Q[N] FY[YY] earnings call transcript"` | Trendlyne concall |
| News (last 90 days) | `web_search: "[TICKER] news 2026"` — use only ET Markets, Mint, Business Standard, Hindu BusinessLine, CNBCTV18, Moneycontrol | — |
| Sector / industry data | CMIE / MOSPI / RBI reports via `web_search` | IBEF.org sector reports |
| Technical indicators | `web_search: "[TICKER] technical analysis tradingview"` then fetch | Chartink.com screener |
| **Peer valuation (P/E, P/B, ROE vs sector peers)** | `web_search: "[COMPANY] vs peers valuation comparison [SECTOR] 2026"` then fetch Trendlyne peers tab OR Tickertape comparison | Screener.in peer comparison |
| **Analyst consensus target price** | `web_fetch: https://trendlyne.com/equity/[TICKER]/` — look for analyst target section (e.g., "38 analysts, target ₹1,154") | `web_search: "[TICKER] analyst target price consensus 2026"` |
| Credit ratings (if applicable) | `web_search: "[COMPANY] credit rating CRISIL ICRA CARE 2026"` | — |
| Regulatory / SEBI filings | `https://www.sebi.gov.in/` or BSE announcements | — |

> ⚠️ **Rule**: Every number in the report must be followed by `[Source: <URL or publication name, date>]`. If a number cannot be sourced, write "data unavailable" — never estimate or infer.

### Step 3 — Analyse

Run the analysis frameworks in `references/analysis-frameworks.md`.

### Step 4 — Write the report

Follow the report template in `references/report-template.md` exactly.

**Mandatory additions to the Valuation section (v1.1):**
- Include a **peer comparison table** (minimum 3 peers) showing P/E, P/B, ROE, Revenue Growth for each peer alongside the subject stock. Source from Trendlyne peers tab or Screener.in comparison.
- Include the **analyst consensus target** (if fetched) as a reference data point alongside your independently derived target. Do not adopt it — just cite it as market context.

### Step 5 — Quality Check (MANDATORY before publishing)

Before saving the .docx and presenting it to the user, perform a self-audit across these dimensions:

#### 5a. Price & Formula Check
- [ ] CMP is a real ₹ number (e.g., ₹869.05) — **not** a formula like `=GOOGLEFINANCE(...)`
- [ ] No spreadsheet formula syntax anywhere in the report body
- [ ] Price Snapshot box contains actual fetched numbers, not placeholders
- [ ] CMP date is the most recent trading day (flag if >3 days old)
- [ ] CMP source is Tickertape, Google Finance card, or 5Paisa — **NOT** Yahoo Finance or Screener.in price field

#### 5b. Data Integrity Check
- [ ] Every financial figure has an inline source tag `[Source: URL, date]`
- [ ] No figures marked "data unavailable" that could reasonably be found with one more search — if so, do that search now
- [ ] Screener.in price field was ignored (only historical financials used from there)
- [ ] Yahoo Finance was not used for CMP
- [ ] No analyst consensus figures invented — only cited if fetched from Trendlyne or news articles
- [ ] Peer comparison table is present in the Valuation section with sourced figures

#### 5c. Formatting & Structure Check
- [ ] All section headers from the report template are present
- [ ] Scenario Analysis table (Bull/Base/Bear) is included
- [ ] Investment Verdict has separate guidance for (a) existing holders and (b) new investors, with specific price levels
- [ ] Executive Summary opens with a specific, compelling observation — not a generic company description
- [ ] SEBI disclaimer is present at the end
- [ ] No misplaced or broken markdown (stray `#`, `**`, `>` outside intended sections)
- [ ] Tables are properly formatted and all columns align

#### 5d. Docx-Specific Check
- [ ] Read `/mnt/skills/public/docx/SKILL.md` before generating the .docx
- [ ] File saved to `/mnt/user-data/outputs/` and presented via `present_files` tool
- [ ] Markdown summary also pasted in chat

> If any check fails, fix it before presenting the report. Do not skip this step even under time pressure — a report with raw formulas or missing data is worse than a shorter but accurate one.

---

## 2. Hallucination Prevention Rules

1. **No fabricated figures** — All EPS, revenue, margins, P/E ratios must come from fetched pages.
2. **Cite every number** — Inline source tag `[Source: URL, date]` mandatory.
3. **No stale data** — If a fetch returns data older than 6 months for financials, flag it explicitly.
4. **No analyst consensus invention** — Only cite consensus if fetched from Trendlyne, Bloomberg Quint, or Refinitiv (via news articles).
5. **Uncertainty disclosure** — If a key data point (e.g., FY25 guidance) is not found after 2 search attempts, state "Not available at time of report."
6. **No price targets from thin air** — Target price must be derived from a visible DCF, P/E re-rating, or EV/EBITDA model using fetched numbers.
7. **Never display raw spreadsheet formulas in the report** — The CMP and all prices must appear as concrete ₹ numbers (e.g., ₹869.05) fetched via web search/Tickertape. Never write `=GOOGLEFINANCE(...)` or any formula syntax in the report body — this is a spreadsheet tool, not a report element. **Never use Screener.in's displayed CMP or Yahoo Finance** — both are unreliable for current NSE prices. Always obtain CMP via the Step 1.5 procedure.

---

## 3. Output format

Deliver the report as a **downloadable `.docx` file** using the `docx` skill, AND paste a markdown summary in chat.

Read `/mnt/skills/public/docx/SKILL.md` before generating the .docx output.

Report length: 1,500–3,000 words (excluding data tables).

### Mandatory: Include a Live Price Snapshot box

Every report must include a clearly visible **Price Snapshot** box near the top (in the cover/snapshot section) showing the actual fetched prices:

```
📊 PRICE SNAPSHOT (as of [DATE])
  CMP:         ₹[actual price]
  Prev. Close: ₹[actual price]
  52W High:    ₹[actual price]
  52W Low:     ₹[actual price]
  Market Cap:  ₹[actual value] Cr
  Source:      Google Finance / Tickertape (NSE)
Note: Prices reflect last NSE close. Verify current price on NSE/BSE before trading.
```

> ⚠️ All values in this box must be **real numbers fetched in Step 1.5** — never write raw spreadsheet formulas (e.g. `=GOOGLEFINANCE(...)`) anywhere in the report. Source must be Tickertape, Google Finance card, or 5Paisa — not Yahoo Finance.

---

## 4. Tone & Style

- Write in the style of a Tier-1 Indian brokerage research report (e.g., ICICI Securities, Kotak Institutional, Motilal Oswal style).
- The reference benchmark for style and depth is a Macfos Ltd. (BSE: 543787) style report — institutional quality, conviction-driven narrative, callout boxes for key insights and risks, specific dates/numbers throughout.
- Use **callout boxes** (blockquotes `>`) for: key channel checks or "Practitioner's Edge" insights, ⚠️ critical financial risks (e.g. negative OCF paradox), valuation risk warnings, and anomaly explanations (one-time orders, base effects).
- The **Executive Summary** should open with the most interesting real-world observation about the company — not a generic "Company X is a leading provider of Y." Lead with WHY the stock matters NOW.
- The **Investment Verdict section** must include separate, actionable guidance for (a) existing holders and (b) new investors — with specific price levels, tranching strategy, and stop-losses.
- The **Scenario Analysis table** (Bull/Base/Bear) is mandatory in every report.
- The **Valuation section** must include a peer comparison table (≥3 peers) sourced from Trendlyne or Tickertape.
- End every report with the standard SEBI disclaimer as shown in the template.

---

## 5. Benchmark Quality Dimensions

Use these 5 dimensions to self-assess report quality before delivering:

| Code | Dimension | Pass criteria |
|------|-----------|---------------|
| D1 | **Data Sourcing** | CMP from Step 1.5 (Tickertape/Google Finance, not Yahoo/Screener); all financials from Q-period filings with dates |
| D2 | **Structure** | Price Snapshot box ✓, Bull/Base/Bear table ✓, split Verdict ✓, peer comparison table ✓ |
| D3 | **Anti-Hallucination** | 100% of figures carry `[Source: URL, date]`; no invented consensus targets |
| D4 | **Actionability** | Specific ₹ entry/exit/tranche levels for both new investors and existing holders |
| D5 | **Output** | `.docx` file in `/mnt/user-data/outputs/` + markdown summary in chat |

A report scoring < 5/5 on this rubric should not be delivered. Fix failing dimensions first.
