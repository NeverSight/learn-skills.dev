---
name: business-analysis
description: >
  This skill should be used when the user asks to "analyze a company", "read a financial report",
  "evaluate a business", "assess an industry", "compare companies", "check if a stock is worth buying",
  or shares a P&L / financial statement / social media business discussion for analysis. Also triggers
  on: "franchise evaluation", "supply chain analysis", "valuation", "is this profit real", "why did
  earnings drop", "external shock", "industry transformation", "related party transaction",
  "normalized EPS", "one-time vs structural". Provides a systematic 7-step business analysis workflow
  from report reading through value chain tracing.
metadata:
  portable: true
  version: 1.4.1
---

# Business Analysis

Systematic business analysis workflow for evaluating companies from financial reports, social media discussions, industry events, or earnings announcements. The workflow moves from observable data to actionable judgment through seven steps, each with specific decision points and analytical tools.

## Core Workflow

Every analysis follows this sequence. Start from whichever step matches the available data, but complete all downstream steps before concluding.

### Step 1: Reconstruct the Numbers

Before interpreting, verify the data. Raw financial data from social media posts, self-prepared reports, or press releases often has implicit assumptions that change the conclusion.

Key checks:
- **Denominator identification**: The same cost produces different percentages depending on the base (store revenue vs customer spending, gross vs net recognition). Identify which base each percentage uses before comparing.
- **Accounting basis**: Is the report using purchases or COGS? Cash basis or accrual? Has inventory been adjusted?
- **Hidden costs**: Equipment depreciation, insurance misplacement, loan interest, periodic renovation obligations, hidden franchise fees embedded in ingredient markups.
- **Totals verification**: Do line items add up to the stated total? Small business self-prepared reports frequently have attribution overlaps or calculation errors.

Apply the adjustment table: list each missing cost, estimate its monthly impact, and restate the operating profit. If the restated profit flips from positive to negative, flag this as a critical finding.

Detailed checklist: `references/report-reading.md`

### Step 2: Position the Company

Determine what type of company this is before selecting analysis tools. The same metric means different things for different company types.

**Two-axis positioning:**
- **Business model axis**: Product company / Distributor-agent / Service provider / Platform / Manufacturer / Vertically integrated / Franchise (franchisor vs franchisee)
- **Lifecycle axis**: Seed / Growth / Mature / Transformation-decline

Cross-reference the position to determine which metrics matter most and what constitutes "normal" for this type. A growth-stage SaaS company with negative FCF is normal; a mature manufacturer with negative FCF is a red flag.

Detailed positioning tables and cross-reference matrix: `references/positioning-and-benchmarking.md`

### Step 3: Build Industry Benchmarks

Establish what "normal" looks like before judging whether a company is performing well or poorly. Social media consensus ("this industry's margin is just X%") often carries survivorship bias, scale bias, or outdated data.

**Benchmark construction:**
1. Select peer group: Filter by sub-industry, scale, lifecycle stage, geography, and **value-chain span** (full-process vs reseller vs OEM). Minimum 5-8 companies. A full-process producer and a reseller in the same nominal industry are not margin peers — their gross margins cover different spans of the chain (see `references/value-chain-analysis.md`, Value-Chain Span section).
2. Calculate median (not average) for key metrics.
3. Pull 8-12 quarters of trend data, not just the latest snapshot.
4. Note survivorship bias: public data only includes surviving companies.

**Deviation analysis:**
- Single metric deviation is not conclusive. Look for multi-metric patterns (high margin + high cash flow = genuine efficiency; high margin + low cash flow = aggressive revenue recognition).
- Distinguish structural improvement from one-time benefit from external windfall. See Step 5.
- Complete the deviation analysis by mapping the company's key metrics against peer medians, then cross-read multiple deviations to form a pattern conclusion before proceeding to Step 4.
- If fewer than 5 listed peers exist, substitute with industry association averages or franchise HQ benchmark data, noting the lower precision.

Detailed peer group construction and deviation tables: `references/positioning-and-benchmarking.md`

### Step 4: Assess Capital Returns and Viability

Translate P&L profit into investment return language.

**Key decompositions:**
- **Capital vs labor return**: If the owner stops working, does the capital alone generate acceptable returns? Small business profit often mixes both. Separate them by pricing the owner's labor at market rate.
- **Continue vs exit**: Monthly loss x remaining contract months vs one-time exit cost. Sunk costs (already paid franchise fees, renovation) do not affect this calculation.
- **Contribution margin**: A high-commission channel with positive contribution margin is still better than no channel. Closing it shifts fixed cost burden to remaining channels.

**Valuation methods** (for listed companies or investment targets):
- Absolute: DCF (sensitive to discount rate and terminal value assumptions)
- Relative: P/E, EV/EBITDA, P/S (must use comparable companies in same stage and model)
- **Normalized EPS**: Strip one-time gains/losses to estimate sustainable earnings. Using peak-year EPS for valuation overstates value.

Detailed valuation frameworks: `references/valuation-and-investment.md`

### Step 5: Decompose Changes — Structural vs One-Time

When a company's margin jumps or drops sharply, decompose the sources before drawing conclusions. This is the most frequently skipped step and the most common source of misjudgment.

**Three categories:**
- **Structural improvement**: Product mix shift toward higher margin (processing capacity expansion), vertical integration infrastructure (self-owned farms, automated factories), new high-value channels. These persist because the underlying assets and capabilities remain.
- **External windfall**: Commodity price swings (pig disease reducing supply and spiking prices), favorable exchange rates, one-time government subsidies. These reverse when external conditions change.
- **Financial engineering**: Asset disposals, accounting policy changes, workforce restructuring. These do not repeat.

**Verification method**: Check if the improvement source is an asset that stays (structural), an external condition that changes (windfall), or a one-time action (engineering). When the three categories are mixed, estimate each one's contribution in percentage points.

Real-world validation pattern: Analyze in period N, predict which components will persist, check actuals in period N+1. Adjust the framework when predictions miss.

Detailed decomposition framework and tracking indicators: `references/external-shock.md`

### Step 6: Trace the Value Chain

A single company's financials tell only part of the story. Tracing upstream (suppliers) and downstream (customers, franchisees) reveals structural pressures and hidden profit transfers.

**Three-sided squeeze identification:**
At every level of a value chain, participants face pressure from three directions — upstream suppliers (controlling input costs), downstream customers (controlling pricing), and lateral competitors or platforms (taking a cut). This pattern recurs across industries and value chain levels.

**Related party transactions:**
When upstream and downstream companies belong to the same group, transfer pricing shifts profit between entities. Estimate the transfer by comparing each entity's margin against independent peers. If the upstream company's margin is 5 points above peers, that margin may be extracted from the downstream company's cost structure.

**Escape paths from commodity squeeze:**
1. Upstream integration (control raw material costs)
2. Downstream integration (control end pricing, build brand premium)
3. Scale-driven cost reduction

Track which path each competitor chose and whether their financial metrics confirm the path is working. Select path based on available assets: existing upstream capacity suggests upstream integration; brand capability or channel relationships suggest downstream integration; neither suggests scale reduction as the default.

**International commodity supply chain:**
When the target company depends on imported raw materials, add a supply chain geography layer:
- **Import dependency ratio**: What percentage of key inputs is imported? High dependency (e.g., 95% for Taiwan animal feed) means the entire domestic industry is exposed to international price shocks.
- **Source concentration**: How concentrated are import sources? Top-2 countries supplying 80%+ = single-point-of-failure risk at the country level.
- **Transmission path**: Origin event (war, drought, export ban) → international commodity price → import cost → domestic production cost → end product price. Each link adds lag and amplification.
- **Procurement strategies**: Strategic inventory (stockpile at low prices), long-term contracts (lock price but forfeit downside benefit), futures hedging (requires financial capability), supplier geographic diversification, vertical integration into upstream.

These procurement dimensions map directly to the electronics industry's risk management framework (component shortage = commodity shortage at a different scale), making the analysis portable across industries.

Trace one level upstream and one level downstream from the target company. Go further only if related party transactions, vertical integration structures, or import dependency are identified at the first level.

Detailed value chain analysis patterns: `references/value-chain-analysis.md`

### Step 7: Cross-Validate Claims Against Data

Companies and media produce narratives (digital transformation, AI adoption, aggressive expansion targets). Cross-validate every claim against financial data. Also assess management track record: compare historical guidance vs actuals, check insider ownership trends, and review compensation structure alignment with shareholder interests.

**Common validation checks:**
- "Revenue growth of X%" — Is this from new stores or same-store growth? Net store additions vs gross (what's the closure rate)?
- "AI improved productivity by Y%" — Is this from the best-performing pilot store or the fleet average?
- "Target Z stores by year-end" — What's the historical actual vs target gap?
- "Margin improvement" — Decompose per Step 5. How much is structural vs windfall?

When a company is actively pushing PR about transformation, increase scrutiny on Step 5 decomposition and look for non-financial red flags: management turnover timing, insider selling patterns, contingent liabilities in footnotes.

Detailed PR claim validation checklist: `references/value-chain-analysis.md` (PR Claim Validation section).

## Key Analytical Patterns (Quick Reference)

| Pattern | When to Apply | Core Logic |
| --- | --- | --- |
| Denominator awareness | Any percentage-based analysis | Same cost, different base = different conclusion |
| Contribution margin | Channel or product line decisions | Positive contribution covers fixed costs, even if margin is thin |
| Normalized EPS | Valuation after earnings spike/drop | Strip one-time items to estimate sustainable earnings power |
| Related party transfer pricing | Group companies with intercompany transactions | Compare each entity's margin to independent peers |
| Value-chain span | Cross-company gross-margin comparison in the same industry | Margin gap is often structural (how many value-add layers captured in-house) not efficiency; margins across different spans aren't comparable as efficiency |
| Three-sided squeeze | Any value chain participant analysis | Upstream/downstream/lateral pressure constrains margin structurally |
| Structural vs one-time | Any significant margin change | Assets that stay = structural; conditions that change = one-time |
| Supply shock vs cycle | Commodity industry with price volatility | Shock reverses in 1-2 quarters; cycle persists for years |
| Import dependency | Company using imported raw materials | High dependency + source concentration = exposed to geopolitical and trade risk |

## Output Structure

Every analysis should produce:
1. **Restated financials** (if raw data needs adjustment)
2. **Company positioning** (stage x model, with justification)
3. **Benchmark comparison** (peer group, key metric deviations)
4. **Change decomposition** (structural / one-time / windfall breakdown)
5. **Actionable judgment** (continue/exit for operators; buy/hold/avoid for investors) with **confidence level** (high/medium/low based on data completeness — SME with no audited statements = low; listed company with 8 quarters of data = high)
6. **Tracking indicators** (what to monitor for the judgment to change)

## Reference Files

Detailed checklists and frameworks for each step:
- **`references/report-reading.md`** — P&L reading, three-statement analysis, hidden cost identification, accounting adjustment table
- **`references/positioning-and-benchmarking.md`** — Two-axis positioning matrix, peer group construction, deviation analysis, benchmark sources
- **`references/valuation-and-investment.md`** — DCF mechanics, multiples selection by stage/model, capital vs labor return, continue/exit formula
- **`references/value-investing-assessment.md`** — Buffett-style three-gate screen (moat durability / management capital allocation / margin of safety), 10-year ROE and DuPont screen, holding-company ROE numerator discipline, Taiwan governance signals (董監質押), value window identification, value trap taxonomy, valuation-band derating vs cheapness, compounder vs special-situation school routing, point-in-time verdicts with mandatory flip-condition output. Use when the goal is a buy/avoid judgment on a listed company — and note the boundary: business analysis without price/valuation-band data cannot support an investment conclusion
- **`references/external-shock.md`** — Shock type classification, structural vs one-time decomposition, escape path tracking, cross-industry validation
- **`references/value-chain-analysis.md`** — Upstream/downstream tracing, related party transaction estimation, three-sided squeeze identification, vertical integration comparison

---

版本紀錄在同目錄的 `CHANGELOG.md`。
