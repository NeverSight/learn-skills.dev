---
name: stock-copilot-pro
description: OpenClaw stock analysis skill for US/HK/CN markets. Combines QVeris data sources (THS, Caidazi, Alpha Vantage, Finnhub, X sentiment) for quote, fundamentals, technicals, news radar, morning/evening brief, and actionable investment insights.
env:
  - QVERIS_API_KEY
requirements:
  env_vars:
    - QVERIS_API_KEY
credentials:
  required:
    - QVERIS_API_KEY
  primary: QVERIS_API_KEY
  scope: read-only
  endpoint: https://qveris.ai/api/v1
runtime:
  language: nodejs
  node: ">=18"
install:
  mechanism: local-skill-execution
  external_installer: false
  package_manager_required: false
persistence:
  writes_within_skill_dir:
    - config/watchlist.json
    - .evolution/tool-evolution.json
  writes_outside_skill_dir: false
security:
  full_content_file_url:
    enabled: true
    allowed_hosts:
      - qveris.ai
    protocol: https
network:
  outbound_hosts:
    - qveris.ai
metadata: {"openclaw":{"requires":{"env":["QVERIS_API_KEY"]},"primaryEnv":"QVERIS_API_KEY","homepage":"https://qveris.ai"}}
auto_invoke: true
source: https://qveris.ai
examples:
  - "Analyze AAPL with a comprehensive report"
  - "Technical analysis for 0700.HK"
  - "Compare AAPL, MSFT, NVDA"
  - "Give me fundamentals and sentiment for 600519.SS"
---

# Stock Copilot Pro

Global Multi-Source Stock Analysis with QVeris.

## SEO Keywords

OpenClaw, stock analysis skill, AI stock copilot, China A-shares, Hong Kong stocks, US stocks, quantitative analysis, fundamental analysis, technical analysis, sentiment analysis, industry radar, morning evening brief, watchlist, portfolio monitoring, QVeris API, THS iFinD, Caidazi, Alpha Vantage, Finnhub, X sentiment, investment research assistant

## Supported Capabilities

- Single-stock analysis (`analyze`): valuation, quality, technicals, sentiment, risk/timing
- Multi-stock comparison (`compare`): cross-symbol ranking and portfolio-level view
- Watchlist/holdings management (`watch`): list/add/remove for holdings and watchlist
- Morning/Evening brief (`brief`): holdings-focused daily actionable briefing
- Industry hot-topic radar (`radar`): multi-source topic aggregation for investable themes
- Multi-format output: `markdown`, `json`, `chat`
- OpenClaw LLM-ready flow: structured data in code + guided narrative in `SKILL.md`

## Data Sources

- Core MCP/API gateway: `qveris.ai` (`QVERIS_API_KEY`)
- CN/HK quote and fundamentals:
  - `ths_ifind.real_time_quotation`
  - `ths_ifind.financial_statements`
  - `ths_ifind.company_basics`
  - `ths_ifind.history_quotation`
- CN/HK news and research:
  - `caidazi.news.query`
  - `caidazi.report.query`
  - `caidazi.search.hybrid.list`
  - `caidazi.search.hybrid_v2.query`
- Global news sentiment:
  - `alpha_news_sentiment`
  - `finnhub.news`
- X/Twitter sentiment and hot topics:
  - `qveris_social.x_domain_hot_topics`
  - `qveris_social.x_domain_hot_events`
  - `qveris_social.x_domain_new_posts`
  - `x_developer.2.tweets.search.recent`

## What This Skill Does

Stock Copilot Pro performs end-to-end stock analysis with five data domains:

1. Market quote / trading context
2. Fundamental metrics
3. Technical signals (RSI/MACD/MA)
4. News and sentiment
5. X sentiment

It then generates a data-rich analyst report with:
- value-investing scorecard
- event-timing anti-chasing classification
- safety-margin estimate
- thesis-driven investment framework (drivers/risks/scenarios/KPIs)
- multi-style playbooks (value/balanced/growth/trading)
- event radar with candidate ideas from news and X
- scenario-based recommendations
- standard readable output (default) + optional full evidence trace (`--evidence`)

## Key Advantages

- Deterministic tool routing via `references/tool-chains.json`
- Evolution v2 parameter-template memory to reduce recurring parameter errors
- Strong fallback strategy across providers and markets
- US/HK/CN market-aware symbol handling
- Structured outputs for both analyst reading and machine ingestion
- Safety-first handling of secrets and runtime state

## Core Workflow

1. Resolve user input to symbol + market (supports company-name aliases, e.g. Chinese name -> `600089.SH`).
2. Search tools by capability (quote, fundamentals, indicators, sentiment, X sentiment).
3. Route by hardcoded tool chains first (market-aware), then fallback generic capability search.
   - For CN/HK sentiment, prioritize `caidazi` channels (report/news/wechat).
   - For CN/HK fundamentals, prioritize THS financial statements (income/balance sheet/cash flow), then fallback to company basics.
4. Before execution, try evolution parameter templates; if unavailable, use default param builder.
5. Run quality checks:
   - Missing key fields
   - Data recency
   - Cross-source inconsistency
6. Produce analyst report with:
   - composite score
   - safety margin
   - event-driven vs pullback-risk timing classification
   - structured thesis (driver/risk/scenario/KPI)
   - event radar (timeline/theme) and candidate ideas
   - style-specific execution playbooks
   - market scenario suggestions
   - optional parsed/raw evidence sections when `--evidence` is enabled

7. Preference routing (public audience default):
   - If no preference flags are provided, script returns a questionnaire first.
   - You can skip this with `--skip-questionnaire`.

## Command Surface

Primary script: `scripts/stock_copilot_pro.mjs`

- Analyze one symbol:
  - `node scripts/stock_copilot_pro.mjs analyze --symbol AAPL --market US --mode comprehensive`
  - `node scripts/stock_copilot_pro.mjs analyze --symbol "<company-name>" --mode comprehensive`
- Compare multiple symbols:
  - `node scripts/stock_copilot_pro.mjs compare --symbols AAPL,MSFT --market US --mode comprehensive`
- Manage watchlist:
  - `node scripts/stock_copilot_pro.mjs watch --action list`
  - `node scripts/stock_copilot_pro.mjs watch --action add --bucket holdings --symbol AAPL --market US`
  - `node scripts/stock_copilot_pro.mjs watch --action remove --bucket watchlist --symbol 0700.HK --market HK`
- Generate brief:
  - `node scripts/stock_copilot_pro.mjs brief --type morning --format chat`
  - `node scripts/stock_copilot_pro.mjs brief --type evening --format markdown`
- Run industry radar:
  - `node scripts/stock_copilot_pro.mjs radar --market GLOBAL --limit 10`

## OpenClaw scheduled tasks (morning/evening brief and radar)

To set up morning brief, evening brief, or daily radar in OpenClaw, use **only** the official OpenClaw cron format and create jobs via the CLI or Gateway cron tool. Do not edit `~/.openclaw/cron/jobs.json` directly.

- Reference: the `jobs` array in `config/openclaw-cron.example.json`; each item is one `cron.add` payload (fields: `name`, `schedule: { kind, expr, tz }`, `sessionTarget: "isolated"`, `payload: { kind: "agentTurn", message: "..." }`, `delivery`).
- Example (morning brief): `openclaw cron add --name "Stock morning brief" --cron "0 9 * * 1-5" --tz Asia/Shanghai --session isolated --message "Use stock-copilot-pro to generate morning brief: run brief --type morning --max-items 8 --format chat" --announce`. To deliver to Feishu, add `--channel feishu --to <group-or-chat-id>`.
- Incorrect: using the legacy example format (e.g. `schedule` as string, `command`, `delivery.channels` array) or pasting the example into jobs.json will cause Gateway parse failure or crash.

## CN/HK Coverage Details

- Company-name input is supported and auto-resolved to market + symbol for common names.
- Sentiment path prioritizes `caidazi` (research reports, news, wechat/public-account channels).
- Fundamentals path prioritizes THS financial statements endpoints, and always calls THS company basics for profile backfill:
  - `revenue`
  - `netProfit`
  - `totalAssets`
  - `totalLiabilities`
  - `operatingCashflow`
  - `industry`
  - `mainBusiness`
  - `tags`

## Output Modes

- `markdown` (default): human-readable report
- `json`: machine-readable merged payload
- `chat`: segmented chat-friendly output for messaging apps
- `summary-first`: compact output style via `--summary-only`

## Preference & Event Options

- Preference flags:
  - `--horizon short|mid|long`
  - `--risk low|mid|high`
  - `--style value|balanced|growth|trading`
  - `--actionable` (include execution-oriented rules)
  - `--skip-questionnaire` (force analysis without preference Q&A)

- Event radar flags:
  - `--event-window-days 7|14|30`
  - `--event-universe global|same_market`
  - `--event-view timeline|theme`

## Dynamic Evolution

- Runtime learning state is stored in `.evolution/tool-evolution.json`.
- One successful execution can update tool parameter templates.
- Evolution stores `param_templates` and `sample_successful_params` for reuse.
- Evolution does not decide tool priority; tool priority is controlled by `tool-chains.json`.
- Use `--no-evolution` to disable loading/saving runtime learning state.

## Safety and Disclosure

- Uses only `QVERIS_API_KEY`.
- Calls only QVeris APIs over HTTPS.
- `full_content_file_url` fetching is kept enabled for data completeness, but only HTTPS URLs under `qveris.ai` are allowed.
- Does not store API keys in logs, reports, or evolution state.
- Runtime persistence is limited to `.evolution/tool-evolution.json` (metadata + parameter templates only).
- Watchlist state is stored at `config/watchlist.json` (bootstrap from `config/watchlist.example.json`).
- OpenClaw scheduled tasks: see `config/openclaw-cron.example.json`. Create jobs with the official format (`schedule.kind`, `payload.kind`, `sessionTarget`, etc.) via `openclaw cron add` or the Gateway cron tool; do not paste or merge the example JSON into `~/.openclaw/cron/jobs.json` (schema mismatch can cause Gateway parse failure or crash). Set `delivery.channel` and `delivery.to` for your channel (e.g. feishu).
- External source URLs remain hidden by default; only shown when `--include-source-urls` is explicitly enabled.
- No package installation or arbitrary command execution is performed by this skill script.
- Research-only output. Not investment advice.

## Single Stock Analysis Guide

When analyzing `analyze` output, act as a senior buy-side analyst and deliver a **professional but not overlong** report.

### Required Output (7 Sections)

0. **Data Snapshot (required)**
   - Start with a compact metrics table built from `data` fields.
   - Include at least: price/change, marketCap, PE/PB, profitMargin, revenue, netProfit, RSI, 52W range.
   - Example format:

```markdown
| Metric | Value |
|--------|-------|
| Price | $264.58 (+1.54%) |
| Market Cap | $3.89T |
| P/E | 33.45 |
| P/B | 57.97 |
| Profit Margin | 27% |
| Revenue (TTM) | $394B |
| Net Profit | $99.8B |
| RSI | 58.3 |
| 52W Range | $164 - $270 |
```

1. **Key view (30 seconds)**
   - One-line conclusion: buy/hold/avoid + key reason.

2. **Investment thesis**
   - Bull case: 2 points (growth driver, moat/catalyst)
   - Bear case: 2 points (valuation/risk/timing)
   - Final balance: what dominates now.

3. **Valuation and key levels**
   - PE/PB vs peer or history percentile (cheap/fair/expensive)
   - Key levels: current price, support, resistance, stop-loss reference

4. **Recommendation (required)**
   - Different advice by position status:
     - No position
     - Light position
     - Heavy position / underwater
   - Each suggestion must include concrete trigger/price/condition.

5. **Risk monitor**
   - Top 2-3 risks + invalidation condition (what proves thesis wrong).

6. **Data Sources (required)**
   - End with a source disclosure line showing QVeris attribution and data channels actually used.
   - Include generation timestamp and list of source/tool names from payload metadata such as `dataSources`, `meta.sourceStats`, or `data.*.selectedTool`.
   - Example format:

```markdown
> Data powered by [QVeris](https://qveris.ai) | Sources: Alpha Vantage (quote/fundamentals), Finnhub (news sentiment), X/Twitter (social sentiment) | Generated at 2026-02-22T13:00:00Z
```

### Quality Bar

- Avoid data dumping; each key number must include interpretation.
- Every numeric claim must be grounded in actual payload values; do not fabricate numbers.
- Keep concise but complete (target 250-500 characters for narrative).
- Must include actionable guidance and time window.
- Ticker and technical terms in English.

## Daily Brief Analysis Guide

When analyzing `brief` output, generate an actionable morning/evening briefing for OpenClaw conversation.

### Morning Brief

1. **Market overview**: risk-on/off + key overnight move + today's tone, plus an index snapshot table from `marketOverview.indices` (index name, price, % change, timestamp)
2. **Holdings check**: holdings that need action first, with per-holding price/% change/grade when available
3. **Radar relevance**: which radar themes impact holdings
4. **Today's plan (required)**: specific watch levels / event / execution plan
5. **Data Sources (required)**: one-line QVeris attribution and channels used in this brief

### Evening Brief

1. **Session recap**: index + sector + portfolio one-line recap, with key index close/% change
2. **Holdings change**: biggest winners/losers and why, with quantized move (%) where available
3. **Thesis check**: whether thesis changed
4. **Tomorrow's plan (required)**: explicit conditions and actions
5. **Data Sources (required)**: one-line QVeris attribution and channels used in this brief

### Quality Bar

- Prioritize user holdings, not generic market commentary.
- Quantify changes when possible (%, levels, counts).
- Keep concise and decision-oriented.
- Include a short source disclosure line at the end to improve traceability and credibility.

## Hot Topic Analysis Guide

When analyzing `radar` output, cluster signals into investable themes and provide concise actionable conclusions.

### Required Output (per theme)

- **Theme**: clear, investable label
- **Driver**: what changed and why now
- **Impact**: beneficiaries/losers + magnitude + duration
- **Recommendation (required)**: concrete trigger or level
- **Risk note**: key invalidation or monitoring signal
- **Source tag (required)**: include `source` label for each theme (for example: `caidazi_report`, `alpha_news_sentiment`, `x_hot_topics`)

### Execution Rules

- Cluster into 3-5 themes max.
- Cross-verify sources; lower confidence for social-only signals.
- Distinguish short-term trade vs mid-term allocation.
- Keep each theme concise (<200 characters preferred).
- End with a QVeris source disclosure line listing channels that contributed to this radar run.

