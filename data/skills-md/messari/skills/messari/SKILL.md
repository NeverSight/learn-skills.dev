---
name: messari
description: "Use this skill whenever the user asks any question about crypto assets, blockchain networks, DeFi protocols, token unlocks, fundraising rounds, market data, social sentiment, news, or governance — and live data from the Messari API would improve the answer. This includes questions like \"what's the price of X\", \"who invested in Y\", \"what are the top DeFi protocols by TVL\", \"what's trending in crypto\", \"show me upcoming token unlocks\", \"what's the latest news on Ethereum\", \"compare L1 network activity\", \"which exchanges have the most volume\", and any other crypto query. Always use this skill proactively when the user's query could benefit from real-time or historical crypto data — don't wait for the user to explicitly ask to \"use Messari\". If the user asks a general crypto question that requires synthesis or research, route to the Messari AI service first."
---

# Messari — Leading Crypto Data Platform

Answer crypto questions using the Messari API: 34,000+ assets, 210+ exchanges, 14 data services
covering market metrics, social sentiment, research, on-chain analytics, fundraising, governance,
and more.

**Base URL for all endpoints:** `https://api.messari.io`

---

## Step 1: Confirm Authentication

Follow this decision tree **before every session**. Do not skip to Step 2 until auth is confirmed.

```
1. Is `payments-mcp` available as a tool?
   ├── YES → Run `payments-mcp:get_wallet_balance`
   │          ├── Success → x402 is ready. Proceed to Step 2.
   │          └── Error   → Run `payments-mcp:show_wallet_app`, then prompt user (see Setup below)
   └── NO  → Is $MESSARI_API_KEY set or has the user provided an API key?
              ├── YES → API key mode. Include `x-messari-api-key: <key>` on all requests. Proceed to Step 2.
              └── NO  → Neither auth is configured. Prompt user (see Setup below).
```

### x402 Setup (Recommended — wallet-based, no API key needed)

If x402 is not yet configured, tell the user:

> **To use Messari, you'll need to set up a payment wallet first. Here's how:**
>
> 1. Run this command to install the payments connector (replace `claude` with your client if different):
>    ```
>    npx @coinbase/payments-mcp --client claude --auto-config
>    ```
>    Supported clients: `claude` | `claude-code` | `codex` | `gemini`
>
> 2. Restart your AI client to load the connector.
>
> 3. Come back and I'll open the wallet app for you to sign in.
>
> Once signed in, deposit some Base USDC to cover API requests (costs are fractions of a cent per call).

After the user has installed and restarted, run `payments-mcp:show_wallet_app` to open the wallet and prompt them to sign in and deposit USDC.

### API Key (Alternative)

If the user has a Messari API key, include this header on every request:
```
x-messari-api-key: <MESSARI_API_KEY>
```
Note: some endpoints are **only** available via API key (marked `api_key only` below).

---

## Step 2: Route to the Right Service

| User is asking about... | Service | Auth |
|---|---|---|
| General crypto question, synthesis, open-ended research | **AI** | api_key, x402 |
| Price, volume, market cap, ROI, ATH, performance comparison | **Metrics** | api_key, x402 |
| Sentiment, mindshare, trending tokens, social buzz | **Signal** | api_key, x402 |
| Headlines, recent events, breaking news | **News** | api_key, x402 |
| Analyst reports, deep dives, sector overviews | **Research** | api_key only |
| Stablecoin supply, flows, chain breakdowns | **Stablecoins** | api_key, x402 |
| Exchange volumes, comparisons | **Exchanges** | api_key only |
| L1/L2 network activity, fees, active addresses | **Networks** | api_key, x402 |
| DeFi protocols, TVL, lending, DEX volume | **Protocols** | api_key only |
| Token unlocks, vesting schedules | **Token Unlocks** | api_key, x402 |
| Fundraising rounds, investors, VC activity, M&A | **Fundraising** | api_key, x402 |
| Governance events, protocol upgrades | **Intel** | api_key only |
| Trending narratives, topic momentum | **Topics** | api_key only |
| Crypto influencers, X/Twitter accounts | **X-Users** | api_key, x402 |

**When in doubt, start with the AI service** — it synthesizes across all sources and handles
open-ended questions well.

### Example query routing
```
"Tell me about x402 and how it works."              → AI       /ai/v2/chat/completions
"What are upcoming token unlocks this month?"       → Unlocks  /token-unlocks/v1/assets
"10 most recent AI/compute fundraising rounds"      → Funding  /funding/v1/rounds
"Latest crypto regulation headlines"                → News     /news/v1/news/feed
"Recent DePIN sector developments"                  → Research /research/v1/reports
"Most active seed investor over last year"          → Funding  /funding/v1/rounds/investors
"Top AAVE events last quarter"                      → Intel    /intel/v1/events
"Solana ecosystem map"                              → Networks /metrics/v2/networks
"Recent a16z crypto investments"                    → Funding  /funding/v1/projects
"Compare BitTensor vs Render native assets"         → Metrics  /metrics/v2/assets/details
```

---

## Step 3: Call the Endpoint

### AI Service
Chat completions trained on 30TB+ of structured crypto data. Handles synthesis, comparisons,
and open-ended research. x402 access does not require pre-purchased credits.

| Endpoint | Method |
|---|---|
| `/ai/v2/chat/completions` | POST |

**Body:** `{ "messages": [{"role": "user", "content": "..."}], "stream": false }`

---

### Metrics Service
Price, volume, market cap, fundamentals for 34,000+ assets. Use for quantitative questions,
performance comparisons, ROI, ATH, and historical timeseries.

| Endpoint | Description |
|---|---|
| `/metrics/v2/assets` | List assets with market + fundamental metrics |
| `/metrics/v2/assets/details` | Rich point-in-time details for selected assets |
| `/metrics/v2/assets/ath` | All-time-high snapshots and drawdown context |
| `/metrics/v2/assets/roi` | Multi-window ROI snapshots |
| `/metrics/v2/assets/metrics` | List available dataset slugs + granularities |
| `/metrics/v2/assets/{assetID}/metrics/{datasetSlug}/time-series` | Historical timeseries |
| `/metrics/v2/assets/{assetID}/metrics/{datasetSlug}/time-series/{granularity}` | Timeseries at explicit granularity (`5m`, `15m`, `1h`, `1d`) |

**Key params:** `slugs`, `assetIds`, `metrics`, `start`, `end`, `interval`, `limit`, `page`

---

### Signal Service
Real-time social intelligence: sentiment scoring, mindshare tracking, trending.

| Endpoint | Description |
|---|---|
| `/signal/v1/assets` | Ranked asset signal feed (mindshare, sentiment, momentum) |
| `/signal/v1/assets/{assetID}` | Detailed social-signal profile for one asset |
| `/signal/v1/assets/mindshare-gainers-24h` | Biggest mindshare gains last 24h |
| `/signal/v1/assets/mindshare-gainers-7d` | Biggest mindshare gains last 7d |
| `/signal/v1/assets/mindshare-losers-24h` | Biggest mindshare losses last 24h |
| `/signal/v1/assets/mindshare-losers-7d` | Biggest mindshare losses last 7d |
| `/signal/v1/assets/time-series/1h` | Hourly social-signal timeseries |
| `/signal/v1/assets/time-series/1d` | Daily social-signal timeseries |

**Key params:** `assetIds`, `sort`, `sortDirection`, `limit`, `page`, `start`, `end`

---

### News Service

| Endpoint | Auth | Description |
|---|---|---|
| `/news/v1/news/feed` | api_key, x402 | Paginated cross-source crypto news feed |
| `/news/v1/news/sources` | api_key, x402 | List source metadata for filtering |
| `/news/v1/news/assets` | api_key only | Assets currently tagged in news |

**Key params:** `assetSlugs`, `sourceIds`, `limit`, `page`

---

### Research Service *(api_key only)*
Institutional reports, sector deep dives, protocol diligence.

| Endpoint | Description |
|---|---|
| `/research/v1/reports` | List reports (filter by asset, tags) |
| `/research/v1/reports/{reportId}` | Retrieve a specific report |
| `/research/v1/reports/tags` | List available report tags |

**Key params:** `tags`, `assetSlugs`, `limit`, `page`

---

### Stablecoins Service

| Endpoint | Description |
|---|---|
| `/metrics/v2/stablecoins` | List stablecoins with supply + market metrics |
| `/metrics/v2/stablecoins/metrics` | List dataset slugs + granularities |
| `/metrics/v2/stablecoins/{entityIdentifier}/metrics/{datasetSlug}/time-series` | Historical timeseries |
| `/metrics/v2/stablecoins/{entityIdentifier}/metrics/{datasetSlug}/time-series/1d` | Daily timeseries |

**Key params:** `metrics`, `chains`, `start`, `end`, `interval`, `limit`, `page`

---

### Exchanges Service *(api_key only)*

| Endpoint | Description |
|---|---|
| `/metrics/v1/exchanges` | List exchanges with spot/futures volume |
| `/metrics/v1/exchanges/{exchangeIdentifier}` | Single exchange with current metrics |
| `/metrics/v1/exchanges/metrics` | Available metric datasets |
| `/metrics/v1/exchanges/{entityIdentifier}/metrics/{datasetSlug}/time-series/{granularity}` | Exchange timeseries |

**Key params:** `type`, `granularity`, `start`, `end`, `limit`, `page`

---

### Networks Service
L1/L2 on-chain activity — fees, active addresses, usage metrics.

| Endpoint | Description |
|---|---|
| `/metrics/v2/networks` | List networks with activity + fee metrics |
| `/metrics/v2/networks/metrics` | List available dataset slugs + granularities |
| `/metrics/v2/networks/{entityIdentifier}/metrics/{datasetSlug}/time-series` | Historical timeseries |
| `/metrics/v2/networks/{entityIdentifier}/metrics/{datasetSlug}/time-series/{granularity}` | Timeseries at `5m`, `15m`, `1h`, `1d` |

**Key params:** `networkSlugs`, `metrics`, `start`, `end`, `interval`, `limit`, `page`

---

### Protocols Service *(api_key only)*
DeFi protocols: TVL, DEX, lending, liquid staking, bridges.

| Endpoint | Description |
|---|---|
| `/metrics/v2/protocols` | All protocols with aggregated core metrics |
| `/metrics/v2/protocols/dex` | DEX protocols |
| `/metrics/v2/protocols/lending` | Lending protocols |
| `/metrics/v2/protocols/liquid-staking` | Liquid staking protocols |
| `/metrics/v2/protocols/interop` | Bridge/interop protocols |
| `/metrics/v2/protocols/{protocolIdentifier}/metrics/core/time-series/{granularity}` | Core timeseries |
| `/metrics/v2/protocols/{protocolIdentifier}/metrics/dex/time-series/{granularity}` | DEX timeseries |
| `/metrics/v2/protocols/{protocolIdentifier}/metrics/lending/time-series/{granularity}` | Lending timeseries |
| `/metrics/v2/protocols/{protocolIdentifier}/metrics/liquid-staking/time-series/{granularity}` | Liquid staking timeseries |
| `/metrics/v2/protocols/{protocolIdentifier}/metrics/interop/time-series/{granularity}` | Interop timeseries |

**Key params:** `sort`, `order`, `limit`, `page`, `granularity`, `start`, `end`

---

### Token Unlocks Service

| Endpoint | Description |
|---|---|
| `/token-unlocks/v1/assets` | Assets covered by unlock datasets |
| `/token-unlocks/v1/allocations` | Allocation breakdown by category |
| `/token-unlocks/v1/assets/{assetId}/events` | Upcoming unlock events |
| `/token-unlocks/v1/assets/{assetId}/unlocks` | Historical unlock timeseries |
| `/token-unlocks/v1/assets/{assetId}/vesting-schedule` | Forward-looking vesting schedule |

**Key params:** `assetSlugs`, `start`, `end`, `limit`, `page`

---

### Fundraising Service

| Endpoint | Description |
|---|---|
| `/funding/v1/rounds` | Funding rounds by stage, date, amount, participants |
| `/funding/v1/rounds/investors` | Investors in matching rounds |
| `/funding/v1/mergers-and-acquisitions` | Crypto M&A deals |
| `/funding/v1/organizations` | Organizations in fundraising/investment |
| `/funding/v1/projects` | Projects and fundraising attributes |
| `/funding/v1/funds` | Investment funds and fund metadata |
| `/funding/v1/funds/managers` | Fund managers |

**Key params:** `assetSlugs`, `investorSlugs`, `roundTypes` (`seed`, `series-a`, …), `start`, `end`, `limit`, `page`

---

### Intel Service *(api_key only)*
Governance events, protocol upgrades, project milestones.

| Endpoint | Method | Description |
|---|---|---|
| `/intel/v1/events` | GET | List events (legacy; prefer POST) |
| `/intel/v1/events` | POST | Preferred — body-based filters |
| `/intel/v1/events/{eventId}` | GET | Single event with update history |
| `/intel/v1/assets` | GET | Assets covered by Intel dataset |

**Key params:** `assetSlugs`, `eventTypes`, `start`, `end`, `limit`, `page`

---

### Topics Service *(api_key only)*

| Endpoint | Description |
|---|---|
| `/topics/v1/classes` | Available topic taxonomy labels |
| `/topics/v1/current` | Currently trending topics with rank |
| `/topics/v1/daily` | Historical topic timeseries |

**Key params:** `classes`, `assetIDs`, `start`, `end`, `granularity`, `sort`, `limit`, `page`

---

### X-Users Service
Crypto X/Twitter influencer metrics and rankings.

| Endpoint | Description |
|---|---|
| `/signal/v1/x-users` | Ranked crypto X-user feed (engagement, mindshare) |
| `/signal/v1/x-users/time-series/1d` | Daily X-user signal timeseries |
| `/signal/v1/x-users/{xUserID}` | Detailed profile for one X user |

**Key params:** `sort`, `sortDirection`, `accountType`, `limit`, `page`, `start`, `end`
