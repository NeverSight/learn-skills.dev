---
name: business-research
description: >
  This skill should be used when research is needed before writing business analysis — gathering
  financial data, verifying claims, finding industry benchmarks, or fact-checking social media
  business discussions. Triggers on: "find the financial data", "verify this claim", "search for
  company financials", "check if this is true", "gather industry data", "fact-check", "find the
  source", "what does the financial report say", "pull the numbers", "is this accurate",
  "research before writing", "collect data for analysis". Provides a systematic data collection
  and verification workflow to prevent hallucination and ensure analysis is grounded in public data.
metadata:
  version: 1.9.1
---

# Business Research

Systematic data collection and verification workflow for business analysis. Every claim in a business analysis article must trace back to a verifiable source — public financial reports, government statistics, credible news reporting, or company disclosures. This skill prevents the most common failure mode in AI-generated business analysis: **plausible-sounding claims that have no factual basis**.

## Core Principle: No Unsourced Claims

A business analysis article makes two types of statements:

1. **Factual claims** (revenue numbers, market share, dates, ratios) — these must come from verifiable sources.
2. **Analytical judgments** (this strategy is risky, this margin is unsustainable) — these must be derived from factual claims through explicit reasoning.

The failure mode is when analytical judgments masquerade as factual claims ("the industry standard is 35%") without a traceable source. This skill ensures factual claims are sourced and analytical judgments are flagged as such.

## Data Collection Workflow

### Step 1: Identify What Data Is Needed

Before searching, list the specific data points the analysis requires:

| Data type           | Example                                                     | Why needed                           |
| ------------------- | ----------------------------------------------------------- | ------------------------------------ |
| Financial metrics   | Revenue, gross margin, net margin, EPS                      | Quantify company performance         |
| Industry benchmarks | Average margin, typical cost ratio                          | Provide comparison baseline          |
| Historical data     | Revenue trend over 8+ quarters                              | Distinguish structural from one-time |
| Event timeline      | When did the acquisition happen, when did the policy change | Establish causation sequence         |
| Competitive data    | Peer companies' metrics                                     | Enable cross-company comparison      |

Prioritize: financial metrics and event timelines are highest value (most verifiable); industry benchmarks are medium (often experience-based); qualitative claims are lowest (hardest to verify).

### Step 2: Source Hierarchy

Use sources in order of reliability. Higher-tier sources override lower-tier when they conflict.

| Tier | Source type                  | Reliability | Example                                                         |
| ---- | ---------------------------- | ----------- | --------------------------------------------------------------- |
| 1    | Audited financial statements | Highest     | Annual reports on MOPS, SEC filings                             |
| 2    | Company official disclosures | High        | Earnings calls, investor presentations, press releases          |
| 3    | Government statistics        | High        | Agricultural ministry data, central bank reports, census        |
| 4    | Credible journalism          | Medium-High | Investigative reporting with named sources (報導者, 天下, 商周) |
| 5    | Industry association reports | Medium      | Trade association surveys, industry white papers                |
| 6    | Analyst reports              | Medium      | Brokerage research, but note potential conflicts of interest    |
| 7    | Social media / forums        | Low         | Useful for qualitative signals but never for factual claims     |

**Taiwan-specific sources:**

- **MOPS (公開資訊觀測站)**: Public-reporting (公開發行) company financial statements, material announcements, monthly revenue, insider transactions — covers ALL 公開發行 companies, not only 上市/上櫃-traded ones (see the 公開發行未上市 note under "When the Target Company Has No Public Financials")
- **財報分析工具**: Goodinfo, 財報狗, StockFeel — aggregated financial data with calculated ratios
- **農業部統計**: Livestock counts, crop production, import/export data
- **主計總處**: Industry-level economic statistics
- **公平交易委員會**: Merger approvals, market concentration data

### Step 3: Search Strategy

**For company-specific data:**

1. Search company name + stock code + "財報" + year
2. Search company name + "法說會" (earnings call) for management commentary
3. Cross-reference numbers from at least two independent sources

**For industry data:**

1. Search industry + "產業分析" + year for overview reports
2. Search industry + specific metric (e.g., "毛利率" "市佔率") for benchmarks
3. Check government ministry websites for official statistics

**For event verification:**

1. Search event + date for original reporting
2. Look for follow-up reporting that confirms or corrects initial reports
3. Check for official announcements (company filings, government notices)

### Step 4: Verification Checklist

Before using any data point in analysis, verify:

| Check                       | How                                                 | Red flag                                               |
| --------------------------- | --------------------------------------------------- | ------------------------------------------------------ |
| Source exists               | Can the original document/report be located?        | "Industry sources say" without attribution             |
| Number is current           | Is there a more recent figure available?            | Using 2020 data when 2025 exists                       |
| Context is preserved        | Is the number being used in its original context?   | Gross margin cited as net margin                       |
| Calculation is reproducible | Can the derived number be recalculated from inputs? | "Growth rate of X%" without base and comparison period |
| Conflicts are noted         | Do different sources give different numbers?        | Cherry-picking the most favorable source               |

### Step 5: Hedging Uncertain Claims

When data is incomplete or sources disagree, use explicit hedging:

| Certainty level  | Hedging language                                               | When to use                            |
| ---------------- | -------------------------------------------------------------- | -------------------------------------- |
| Verified         | State directly: "2025 年營收 30.4 億（揚秦年度財報）"          | Tier 1-2 source, cross-verified        |
| Estimated        | "估計" / "推估": "設備投資估計 100 萬（量級估算）"             | Reasonable inference from partial data |
| Experience-based | "經驗法則" / "業界常見": "食材成本 35% 是餐飲業常見的經驗基準" | No single authoritative source         |
| Speculative      | Avoid in analysis; route to "further research needed"          | No supporting data at all              |

**Critical rule**: Never present experience-based benchmarks as verified facts. "The industry standard is 35%" requires either a source or the label "experience-based benchmark."

## Common Verification Failures

| Failure mode                           | How it happens                                                                                                                                                                                                                                    | Prevention                                                                                                                        |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| **Hallucinated statistics**            | AI generates plausible-sounding numbers                                                                                                                                                                                                           | Every number must trace to a search result or calculation                                                                         |
| **Outdated data presented as current** | Using old reports without checking for updates                                                                                                                                                                                                    | Always search with current year; label data with its period                                                                       |
| **Survivorship bias in benchmarks**    | "Average franchise profit is X" based on surviving stores only                                                                                                                                                                                    | Note the bias explicitly when using such data                                                                                     |
| **PR claims as facts**                 | Company press release numbers taken at face value                                                                                                                                                                                                 | Cross-check PR claims against financial statements                                                                                |
| **Single-source dependency**           | Entire analysis built on one article                                                                                                                                                                                                              | Cross-reference key claims from at least two independent sources                                                                  |
| **Confusing revenue with profit**      | "This company makes X billion" without specifying metric                                                                                                                                                                                          | Always specify: revenue, gross profit, operating profit, or net income                                                            |
| **Aggregator derived-value errors**    | A site's derived field (e.g. trailing-4Q EPS) scraped or computed wrong — real instance: an impossible EPS value that matched an adjacent YoY-percentage column; secondary re-publishers' ROE year-values off by 3+ points from the primary table | Recompute derived values from quarterly/raw rows before citing; prefer the primary aggregator's official table over re-publishers |
| **EPS basis mixing**                   | As-reported EPS vs retroactively-adjusted EPS (stock dividends shrink prior-year figures by ~the dividend ratio) differ ~10% for the same year                                                                                                    | Label which basis a series uses; never mix bases within one comparison                                                            |
| **Dividend year mislabeling**          | 發放年度 (payment year) vs 盈餘所屬年度 (earnings year) offset by one year across sources                                                                                                                                                         | Normalize to earnings year before summing or matching against EPS                                                                 |
| **Un-annualized quarterly ratios**     | Single-quarter ROE (~1/4 of annual) read as an annual value                                                                                                                                                                                       | Check the period basis; annualize or use annual rows                                                                              |

## Data Access Layering: "Unavailable" Often Means "Wrong Tool Layer"

Public financial data lives in three access layers. A datum unreachable at one layer is frequently trivial at the next — upgrade the layer before accepting a gap or downgrading the analysis.

| Layer               | Tool                                                       | Yields                                                                              | Misses                                |
| ------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------------------- |
| 1. Search snippets  | Web search                                                 | Headlines, single-point figures, news claims                                        | Historical series, interactive tables |
| 2. Page scraping    | Browser automation on aggregator pages                     | Full multi-year tables from sites that block plain HTTP fetch                       | Login/paywall data, footnote detail   |
| 3. Filings/database | Regulator XBRL filings, paid databases, annual report PDFs | Footnote-level detail (capex split, related-party amounts), authoritative originals | Heavy parsing effort                  |

Rule: before writing "data not available" into an analysis, state which layer was tried. A layer-1 failure alone never justifies the claim. Practical impact observed: an entire class of value-investing inputs (10-year ROE series, historical P/E bands, full dividend history) is invisible at layer 1 and completely available at layer 2.

**Taiwan's layer map and the missing aggregation layer**: Taiwan mandates XBRL filing like the US, but the regulator-side aggregation API does not exist — MOPS is a human-oriented form site with per-file XBRL downloads, and the exchange's official [TWSE OpenAPI](https://openapi.twse.com.tw/) mostly serves current-day snapshots (daily quotes, P/E-P/B-yield, institutional flows) without deep history. Structural reason: the exchange operates the disclosure site AND sells market data feeds — aggregation is left to the private sector. Free API-layer option to try before browser scraping: **FinMind**（open-source, 50+ datasets — three financial statements, dividend history, monthly revenue, historical PER/PBR, shareholding dispersion; free tier ~300-600 requests/hr with token）. FinMind serves raw statements, so derived metrics (ROE series, valuation bands) need computing; Goodinfo's precomputed tables remain the fast path for those. Pledge ratios stay MOPS-only.

Field-tested FinMind usage（`api.finmindtrade.com/api/v4/data?dataset={D}&data_id={code}&start_date={date}`, works without token at reduced rate）:

- `TaiwanStockDividend` — calibrated 11/11 year-values against the primary aggregator's dividend table before use
- `TaiwanStockFinancialStatements` — rows are per-quarter values; annual figure = sum of four quarters. **Validate the summing assumption against one independently-known FY value before trusting a series**（a cumulative-row format would silently overcount）
- `TaiwanStockBalanceSheet` — equity series enables ROE derivation（net income ÷ average equity）for companies the precomputed aggregators lack

Parsing gotchas: years labeled in ROC calendar（`103年` = FY2014）; cash and stock dividends for the same earnings year can arrive as separate records — group by earnings year and sum before comparing to other sources. **ROE numerator for holding companies**: the income-statement `IncomeAfterTaxes` field includes noncontrolling interests — dividing it by parent equity overstates ROE massively for conglomerates with large consolidated-but-partially-owned subsidiaries（field case: a holding company's Q4 total profit was 1.7x its parent-attributable profit, inflating the derived ROE band from ~14-19% to ~22-28%）. Use the income-statement `EquityAttributableToOwnersOfParent` row（parent-attributable profit）as numerator and the balance-sheet row of the same name as denominator; sanity-check by recomputing EPS（numerator ÷ share count）against the reported EPS. Calibrate-then-fill discipline: run the API against a company whose values are already verified, confirm agreement, then use it to fill gaps for companies without baselines.

### Goodinfo Direct-Scrape Playbook (Taiwan listed companies)

Goodinfo's interactive pages block plain fetching but render fully in a real browser. Three pages cover most longitudinal data needs, each mapped to what the data is FOR:

| Page         | URL pattern                               | Data obtained                                                                                                                               | Analytical purpose                                                                                                                                                   |
| ------------ | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 歷年經營績效 | `StockBzPerformance.asp?STOCK_ID={code}`  | 10-20 yr ROE/ROA/EPS/BPS, yearly close price, margins; summary block holds the historical P/E band（一般平均/最低/最高）and current PER/PBR | Capital-efficiency gate (ROE consistency through downturns); valuation-band positioning (current multiple vs own history); market-cap series (close × share capital) |
| 股利政策     | `StockDividendPolicy.asp?STOCK_ID={code}` | Full dividend history with both payment year and earnings year                                                                              | Capital-allocation record; dividend resilience in shock years; retained-earnings test (EPS sum - dividend sum vs market-value gain)                                  |
| 歷年現金流量 | `StockCashFlow.asp?STOCK_ID={code}`       | Yearly operating/investing/financing CF and free cash flow                                                                                  | FCF signature — transforming-under-pressure = OCF positive + FCF negative from expansion capex; distinguish from OCF itself deteriorating                            |

Technique notes:

- Extraction: query `#tblDetail`, or find the table whose text contains "ROE" plus year patterns; serialize rows cell-by-cell
- HTTP 500 responses are rate limiting — wait 5-10 seconds and retry, do not abandon
- These three pages combined are sufficient to compute: 10-year ROE consistency, historical valuation percentile, retained-earnings test, and rough total return vs a market index — the full quantitative half of a value-investing screen
- Remaining layer-3-only items: maintenance-vs-growth capex split (annual report footnotes), pledge ratios at the original regulator disclosure

### Beyond Taiwan: US, International, and Commodities

The layering model is universal but each market's cheap layer differs. Two dedicated references:

- **[`references/us-equities-verification.md`](references/us-equities-verification.md)** — US inverts Taiwan's pattern: layer 3 (SEC EDGAR + free XBRL company-facts JSON API) is cheaper than scraping, so go to filings early. Covers filing types mapped to purposes (10-K capex footnotes, 8-K non-GAAP reconciliation as the normalized-EPS equivalent, DEF 14A + Form 4 as the 質押/insider analog), US-specific failure modes (non-GAAP as GAAP, buybacks ignored in payout, fiscal-year offsets), Japan/Europe briefs, and a Taiwan→US equivalents map.
- **[`references/commodities-futures-verification.md`](references/commodities-futures-verification.md)** — raw-material price claims feeding cost-structure analysis. Source hierarchy (exchange settlement > USDA WASDE/EIA > aggregators), five rules (contract specificity, unit conversion with the bushel/tonne table, term structure, landed cost ≠ futures, recompute spreads before accepting margin narratives), and commodity failure modes (continuous-contract splices, marketing-year vs calendar-year, dual-exchange contracts, peak-as-normal assumptions).

Minimum inline rules when the references are not loaded: name the exchange/contract/unit/date for any commodity price; recompute crush-type spreads from components; for US companies, check whether an EPS figure is GAAP or adjusted before comparing.

## Supply Chain and Competitor Cross-Verification

A company's own financial report is a self-portrait — it shows what the company wants investors to see, within accounting rules. Supply chain verification and competitor lateral checks reveal what the self-portrait omits or distorts. This applies to ALL companies, listed or not.

### Principle: No Single-Company Analysis

Every factual claim about a company should be checkable from at least one external vantage point:

| Vantage point                  | What it reveals                                                                               | Example                                                                                        |
| ------------------------------ | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Upstream supplier              | Whether the company's cost claims are plausible                                               | Fonterra's farmgate milk price confirms the floor cost for any Taiwan importer                 |
| Downstream customer            | Whether the company's revenue claims match observable market presence                         | A chain with 7,000 stores each using 5L/day implies minimum monthly volume                     |
| Competitor with public data    | Whether margins, growth rates, or cost ratios are structurally consistent across the industry | If competitor's margin is 8% and target claims 25% in the same commodity business, investigate |
| Industry regulator/association | Whether volume claims match aggregate statistics                                              | Total import volume from customs data caps how much any single importer can be handling        |

A company reporting 40% gross margin in a commodity industry where peers report 15-21% is either doing something structurally different (verify what) or misrepresenting (flag it). The competitor's report IS the verification tool.

### Competitor Lateral Checks

When analyzing Company A, search for Company B (competitor in the same segment) and compare:

1. **Margin plausibility**: If 大成's feed business has 5-10% gross margin, any competitor claiming 30% in the same feed segment needs explanation
2. **Growth rate consistency**: If the whole industry grew 5% but one company claims 30%, either they took share (verify from whom) or the claim is suspect
3. **Cost structure ratios**: Rent/revenue, labor/revenue, materials/revenue should be in similar bands for same-format businesses (e.g., all convenience stores have ~30% operating expense ratios)
4. **Annual report language cross-check**: When 統一's annual report changes language from "supply shortage" to "demand weakness," check if 光泉 and 味全's reports echo the same shift — consensus among competitors confirms it's structural, not company-specific

### Upstream/Downstream Verification

Verify a company's business logic through its position in the supply chain:

| Direction              | What to look for                                                  | Verification method                                                                                                       |
| ---------------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Upstream (suppliers)   | Does the supplier's public data confirm the claimed relationship? | Global suppliers (Fonterra, Bega) sometimes list distributors; customs data shows import volumes by destination           |
| Downstream (customers) | Do customers' reports or product labels confirm sourcing?         | 7-11's "咖啡專用乳" ingredient label confirms who supplies them; franchisee cost breakdowns confirm mother-company markup |
| Competitor (lateral)   | Do peers' financials bracket the plausible range?                 | Same-industry peers' margins set the ceiling and floor for claims                                                         |
| Aggregate (industry)   | Do individual claims add up to industry totals?                   | If 4 importers each claim 40% market share, someone's lying                                                               |

Physical infrastructure is particularly hard to fabricate: 30 offices nationwide, 100+ delivery trucks, factory automation lines. These serve as floor estimates for business scale even without revenue data.

### Dual-Role Detection

In Taiwan's concentrated industries, the same company often occupies competing positions simultaneously — domestic producer AND importer, brand owner AND private-label manufacturer, retailer AND wholesaler. When a company has dual roles:

1. Its self-reported financials blend two businesses with conflicting incentives
2. Profitability claims for either role are suspect (internal transfer pricing can shift profit between roles)
3. The company's BEHAVIOR (which role is it investing in? which is it shrinking?) reveals its true strategic bet better than reported margins

Detection: check if the company appears in BOTH domestic production registries AND import/export records; search agricultural ministry reports (domestic role) AND customs statistics (import role); look for industry reporting that names them in both capacities.

### When the Target Company Has No Public Financials

**First, confirm it actually has no public financials — do not infer this from the absence of a stock price.** Taiwan has a distinct middle category: 公開發行未上市 (public-reporting, not exchange-listed). These companies have a stock code, file full statements on MOPS, and announce monthly revenue — but do not trade on an exchange, so they show no stock price and no K-line chart, and an aggregator's 市場別 field reads 「公發」, not 上市/上櫃. "No stock price / not listed" is NOT "no public financials." Field case: 中聯油脂 (1246), a soybean-crush co-processing JV, was read as "unlisted, financials only inferable from its shareholders' related-party notes" — when in fact its full income statement (revenue, gross margin, EPS, monthly revenue) is public on MOPS/Goodinfo. Check 公開發行 status (MOPS company lookup, or the aggregator's 市場別 field) before treating a company as financially opaque. The structural-evidence methods below apply only after confirming the company is genuinely 未公開發行.

Many critical supply chain participants are genuinely unlisted family businesses or cooperatives. The verification goal shifts from "find the number" to "verify the business logic through structural evidence." The upstream/downstream and competitor checks above remain the primary tools regardless of jurisdiction.

**Explicit limitation marking in articles:** When a company is important to the story but financially unverifiable:

1. State its supply chain role
2. State what IS verifiable (registry data, infrastructure, upstream/downstream evidence)
3. State what is NOT verifiable (revenue, margins, import volumes)
4. Never estimate financials without a source — "revenue approximately X" is a hallucinated statistic even if directionally correct

### Taiwan-Specific: Corporate Registry and Family Conglomerate Tracing

The following methods are specific to researching Taiwanese companies. Taiwan's traditional industries are relationship-driven — family conglomerates (財團) dominate, private companies frequently interlock with listed groups through board seats and shareholdings, and corporate registry data is unusually accessible compared to other jurisdictions.

**Corporate registry sources:**

| Source                              | What it reveals                                                   |
| ----------------------------------- | ----------------------------------------------------------------- |
| 台灣公司網 (twincn.com)             | Capital, representative, directors, establishment date            |
| 104 人力銀行                        | Employee count, capital, industry classification                  |
| TEJ 台灣經濟新報                    | Corporate group analysis, case studies (covers private companies) |
| 經濟部商工登記 (findbiz.nat.gov.tw) | Official registration, paid-in capital, board changes             |

**Holding structure detection:** Taiwan family businesses commonly layer 控股公司 → 營運公司. The operating company's sole shareholder is a holding company; the family's actual ownership is in the holding company's register.

Check sequence:

1. Find the operating company's shareholder — is it a 法人 (corporate entity)?
2. If yes, look up that entity — that's the holding company
3. Check the holding company's directors and shareholders — that's the ownership family
4. Search whether these individuals appear in any listed company's filings (as directors, major shareholders, or related parties)

If family members or the holding company appear in a listed company's annual report, the private company's activities may be partially visible through related-party transaction disclosures (關係人交易附註).

**Why this matters for verification:** A private company that appears isolated may actually be embedded in a larger group with public reporting obligations. Finding that connection unlocks an indirect verification path — the listed affiliate's related-party disclosures reveal transaction volumes, pricing, and sometimes the private company's revenue contribution to the group. Even when the private company's standalone financials are unavailable, its footprint in the listed affiliate's report provides partial observability.

## Integration with business-analysis Skill

This skill provides the data foundation for [`business-analysis`](../business-analysis/SKILL.md). The workflow:

1. **business-analysis** Step 1 identifies what analysis is needed
2. **business-research** gathers and verifies the data
3. **business-analysis** Steps 2-7 perform the analysis on verified data

When writing business analysis articles, invoke this skill first to collect data, then invoke business-analysis for the analytical framework.

## Output: Source Log

Every research session should produce a source log — a list of all data points used and their sources. Format:

```text
| Data point | Value | Source | Tier | Verified by |
| Revenue 2025 | 30.4 億 | 揚秦年度財報 | 1 | MOPS filing |
| Store count | 955 | 法說會 2025/12 | 2 | Cross-checked with news |
| Food cost benchmark | 35% | Industry experience | 5 | Labeled as experience-based |
```

This log becomes the article's source attribution and enables future verification when data ages.

---

版本紀錄在同目錄的 `CHANGELOG.md`。
