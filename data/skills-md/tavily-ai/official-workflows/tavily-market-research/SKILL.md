---
name: tavily-market-research
description: |
  Write a sourced market sizing report for a market or industry, using Tavily. Covers size and growth estimates with their source, year and method, the segments, the main players with filed revenue or funding, market share, trends, and regulation. Reads industry trackers, company filings in any country, IPO prospectuses, government statistics and analyst report pages, and shows conflicting size estimates side by side. Use when the user asks for market research, a market size or TAM, an industry overview, market share, or who the players in a market are. For a general topic report use tavily-research. For only a table of companies use tavily-list. For a feature and pricing comparison of named competitors use tavily-competitor-analysis. For one company in depth use tavily-due-diligence.
license: MIT
metadata:
  author: tavily
  version: "0.1.0"
  homepage: https://tavily.com
  source: https://github.com/tavily-ai/official-workflows
allowed-tools: Bash(tvly *)
---

# Tavily market research

Produce a market report in which every figure carries its source, its period,
what it measures and the market definition behind it.

Run the research as `tavily-research` describes, build the players table as
`tavily-list` describes, and identify each player as `tavily-entity` does.
Write the report in this skill's template. If any of them isn't installed,
run `npx skills add tavily-ai/skills --skill <name>` and read its SKILL.md
before continuing.

## Intake

Infer the market, the geography and the base year from the request. Default to
the global market, the latest full year with published figures, and 10
players. When the latest full year is more than 6 months old, also report the
latest quarter or half-year the players have filed; check each company's
results date before searching for it.

Ask at most 2 questions, and only when the answer changes which numbers count:

- Value basis: net or list price, order value or revenue, the product alone or
  the installed system.
- Scope: standalone products or also the capability inside broader products,
  which product types count, retail or wholesale.
- Players: makers, carriers or brands.

Name the countries a region covers.

## Pick the sizing route

| Market | Best size source |
|---|---|
| Physical units counted by a tracker | The tracker or industry federation. When it publishes units and an average price but no value, multiply them. |
| Packaged goods sold in stores | Retail scanner trackers (Circana, NielsenIQ) as quoted by trade press, with the tracker's own period |
| Regulated line (insurance, banking, telecom) | The regulator's statutory data. For named shares, also the competition authority's merger reports. |
| A few companies sell nearly all of it | Sum of the players' filed product revenue |
| Early category with no tracker | Companies' own cumulative counts, differenced between dates, and trade-press pages with sourced tables |
| Software | Analyst pages and spend surveys, plus a floor from vendor revenue |

Use every route that applies. A sum of filings is a floor, so drop estimates
below it when both cover the same period and basis. Annualized run-rate (ARR)
is not calendar-year revenue; keep it in its own rows. Label sums, run-rates
and volume times price as derived or self-reported.

When players sell through one another, count each sale once, at the seller to
the end customer. When a merger closes mid-period, state how many months of
the target each figure holds.

## Sources

| Need | Query shape | Filters |
|---|---|---|
| Trackers | `'{market} installations {year} record'`, or `shipments`, `orders` | none, then `--time-range year` on the tracker's name |
| Tracker's own figures | `'{report name} executive summary'`, `'{tracker} {market} method'` | `--include-domains {tracker domain}` |
| Paid trackers | `'{tracker} {product A} {product B}'`, or the market leader's annual report | `--topic news` |
| Analyst estimates | `'{market} market size {year} CAGR'` | none |
| Official statistics | the statistic's name | `--include-domains {agency}` |
| Company figures | `'{company} {product} revenue {year}'`, or the results release title | `--include-domains sec.gov` for US filers |
| Market share | `'{market} market share {year} {measure}'` | none |
| Players | see `references/players.md` | |
| Regulation | the rule's name or code section | `--include-domains {regulator}` |
| Enforcement | `'{programme} {agency}'` | `--topic news --time-range year` |

**Local language.** In a non-English market, also run the tracker, statistic,
company and regulation queries in the local language. For a unit of a foreign
parent, query in the parent's language.

**Trackers.** Query by units, not by market size. Look for the dollar value
and method in the tracker's executive summary on its own domain. Record what
each tracker counts (installations, shipments, orders, production). Use the
latest full-year release and state its coverage.

**Analyst report pages.** Take the figure, base year and CAGR from the
snippet. For the method, extract with `--query 'base year forecast period
segments covered'`. If the page fails at both depths, write "method not
public".

**Extracts.** Confirm the extracted text is about the market before using it.

**Company filings.** Extract the filing with a `--query` that names the
product or segment and its unit. Read `references/filings.md` for non-US
filers, currency, fiscal years, prospectuses and extracts that come back
without the numbers.

**Market share.** Put the measure and the product in the query, then search
the dataset by name. Merger reports, regulator data, usage surveys and
marketplace sales reports carry shares. Report a redacted range as given.
Record what each dataset counts, its year, and who published or paid for it.
When two searches find no share dataset, say so in Gaps and stop.

## Collect

1. **Define.** Write the market definition in one sentence, with what is in
   and out. Check every figure against it.
2. **Split** into size and growth, segments, players, share, trends and
   regulation. Drop regulation when the market has none of its own, and say
   so.
3. **Size.** Run each sizing route that applies and put every estimate in the
   size table in its own unit. Never average them. Name one best-matched
   figure and say why it matches the definition. Convert power to energy only
   with a duration the source states. Label forecasts with their target year.
4. **Segments.** Take splits from tracker releases, filings and prospectuses
   before analyst segment tables.
5. **Players.** Build the table as `tavily-list` does, with the inclusion rule
   set by the definition, then follow `references/players.md`. Pull figures
   for the 5 largest players; for the rest, name, domain and owner are
   enough.
6. **Share.** Show each share basis in its own row. Compute a revenue share
   from filings when the players cover most of the market, label it derived,
   and say when the players' periods or segment scopes differ.
7. **Trends and regulation.** Take trend drivers from tracker releases and
   filings, and search news from the last 12 months for the rest. Keep a trend
   only when two independent sources describe it. When a regulator's notice
   and the news disagree on a rule's status, cite both with their dates.
8. **Stop** when each subtopic has at least two independent sources, or when
   two more searches add nothing. Say which.

Sources are independent only when each did its own counting. Articles quoting
the same tracker count as one source.

## Parallel work

With subagents, give one each to size, players and share, and trends plus
regulation, passing the definition, geography, base year and value basis.

## Deliverable

Show the report in the reply and save it to `reports/{title}.md`, where the
title is 3 to 6 words in sentence case.

```markdown
# Market report: {market}

Definition: {one sentence, with what is in and out}
Geography: {region}
As of: {YYYY-MM-DD}
Defaults assumed: {base year, value basis, currency rates, any others}
Questions not asked: {the intake questions you defaulted, and the default}

## Summary
{2 to 3 paragraphs: the best-matched size and why, how fast it grows, who
leads on which basis, and what is changing}

## Size and growth
| Publisher | Figure | Measures | Year measured | Published | Forecast | CAGR | Definition | Method | Source |
|---|---|---|---|---|---|---|---|---|---|

{Which estimate matches the definition above, and why the others differ}

## Segments
| Segment | Size or share | Year | Source |
|---|---|---|---|

## Players
| Company | Website | Owner | Revenue or volume (metric, period, scope, currency) | Funding (latest round, total) | Source |
|---|---|---|---|---|---|

## Share
| Basis | Period | {player} | {player} | Others | Dataset and who published it | Source |
|---|---|---|---|---|---|---|

## Trends
- {trend}: {evidence, dated} ({source}, {source})

## Regulation
- {rule, body or enforcement action}: {what it requires or did, date} ({source})

## Gaps
- {figure or player that could not be sourced, and what was tried}

## Coverage
Searches: {the queries and domain filters used}
Stop: {each subtopic had two sources | two searches added nothing}

## Rerun inputs
workflow: tavily-market-research
market: {market}
definition: {one sentence}
geography: {region}
base_year: {YYYY or FY}
value_basis: {basis}
player_cap: {N}
trackers: {tracker names and domains found}
```

## Quality bar

- Every figure has a unit, what it measures, the period it measures and a
  source URL. A figure with no period does not go in the report.
- Forecasts, derived figures, run-rates, converted currency and revenue
  broader than the market carry a label saying so.
- Revenue for a listed company comes from its filing, shareholder letter or
  results release. If only a news article can be read, mark it quoted. If the
  filer doesn't break out the market, write "not disclosed".
- A market share states its basis, its period and its source dataset.
- Do not give investment advice.
