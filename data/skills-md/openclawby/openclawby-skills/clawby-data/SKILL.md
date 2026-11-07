---
name: clawby-data
description: Query and analyze real financial data for any asset (US stocks / options / crypto / forex / perps / prediction markets) — quotes, volume, short volume & short interest, borrow fee, dark pool, options chain, Reddit sentiment, OHLC bars, FTDs, dividends & splits, stock screener, company financials & SEC filings (income statement, balance sheet, cash flow, EPS, earnings), DEX pairs & token data (DexScreener — price, liquidity, volume, trending tokens, any chain), prediction-market events/odds/order books, Hyperliquid perps (funding, open interest, order books, candles), and more. Use this skill whenever the user asks about a stock/coin/asset's data, price, short interest, dark pool, options, sentiment, screening, company earnings / financial statements / fundamentals, prediction markets / betting odds, perps / funding rates / open interest, or wants analysis based on real data.
---

# Clawby Data Analysis

Fetch **real financial data** through the Clawby aggregated data API and analyze it. **The single source of truth for every interface — its params (required · format · example) and ⚠️ pitfalls — is `api/catalog/` (start at `api/catalog/_index.yaml`). Always read the relevant category yaml before calling.** The full machine catalog is `api/clawby.yaml` (server-generated, versioned).

**Works with any AI agent** — Claude Code, Codex, OpenClaw, Hermes, and anything that can run shell commands or call an HTTP API: just an API key + the catalog + plain `curl`.

## Quick start

```bash
# 1. Auth (once): sign in at https://www.openclawby.com/ → export CLAWBY_API_KEY=pk_xxx
# 2. Find the interface in api/catalog/<category>/  (routing table below)
# 3. Call it:
curl -s -X POST https://api.openclawby.com/api/relay \
  -H "X-API-Key: $CLAWBY_API_KEY" -H "Content-Type: application/json" \
  -d '{"name":"<interface name from catalog>","params":{ ... }}'
# → {source, data, credits:{remaining,used_total}}
```

## Core workflow · Gather ALL available data first, then analyze

**Completeness is the goal.** A thin answer from a single source is a failure even when correct — go broad first, analyze second. Apply this to **every** request.

1. **Turn the request into a data checklist.** Ask "what would a thorough analyst pull?" and list every relevant dimension. Over-collect on purpose (a stock → quote, short data, dark pool, options, financials, sentiment, peers; a token → DEX price/liquidity, holders, funding & OI, odds, social buzz).
2. **For each item, sweep ALL FOUR source layers — never stop at the first hit:**
   - **Layer 1 — Clawby data** (`/api/relay`): scan the catalog for *every* interface that touches the item and call them all. Primary, authoritative.
   - **Layer 2 — Local akshare** (`akdata/`, read-only): China markets (A-shares · HK · futures · convertible bonds · ETFs · boards · northbound flows · dragon-tiger list · shareholder data) and global macro (CPI · non-farm · PMI · rate decisions) — 1080 interfaces Layer 1 does not carry. Runs locally on the user's machine with no Clawby key and no credits. Guide: `akdata/akshare.md`.
   - **Layer 3 — Execution connectors** (`exec/`, read-only use): the Binance / Bitget / OKX / Polymarket CLIs expose market data, order books, funding, smart-money and news the other layers may not have. Read-only needs no confirmation.
   - **Layer 4 — Your own web access**: news, filings, official docs, macro context — fill every remaining gap.
3. **Maximize coverage.** If two layers supply the same metric, fetch both and cross-check. Fire independent fetches in parallel. Never skip a reachable source.
4. **Track coverage, then analyze.** Ground every claim in collected data; if a source failed, say so instead of silently dropping the dimension.
5. **Offer a formal report when it fits** — for substantial asset analysis, offer a professional PDF research report (see *Professional analysis reports*). Ask first.

## Skill structure

```
clawby-data/
├── SKILL.md            ← this file (managed — refreshed on update; re-read after updating)
├── update-protocol.md  ← first-run + update rules (read at Step 0)
├── manifest.json       ← version + managed file list
├── api/
│   ├── catalog/        ← per-category interface docs (params + gotchas) — READ before calling
│   ├── clawby.yaml     ← full machine catalog (all interfaces)
│   └── index.yaml      ← catalog registry
├── akdata/             ← local akshare executor: China markets + global macro; guide akdata/akshare.md
├── exec/               ← trade-execution connectors; registry exec/index.yaml
├── script/             ← connector helpers: baw/ (fast one-shot scripts) + 42space/ (42.space automated trading); see each dir's README
├── rpc/                ← BYOK RPC (EVM + non-EVM; Ankr/Alchemy/BlockPI) using the user's OWN key — or a NO-KEY public endpoint for 8 chains; registry rpc/index.yaml
├── social/             ← BYOK social & search (Desearch, TwexAPI) using the user's OWN key; registry social/index.yaml
├── llm/                ← BYOK LLM APIs (DeepSeek/OpenAI/Claude/Qwen/Kimi/GLM/OpenRouter) using the user's OWN key; registry llm/index.yaml
├── defi/               ← DeFi connectors: LI.FI cross-chain bridge/swap quotes + Earn yield (key OPTIONAL — no-key tier); registry defi/index.yaml
├── custom/             ← BYOK for user-defined vault providers; first use records the API into local/custom-apis/ for quick reuse; registry custom/index.yaml
├── account/            ← account self-service (email login → key · usage · Key Vault management) via /api/self/*; registry account/index.yaml
├── report/             ← PDF report guide + stylesheet
├── data/               ← misc reference data
└── local/              ← local state / caches; the ONLY folder preserved across updates
```

## Your own RPC / social / LLM keys via the Key Vault (BYOK)

`rpc/` lets you make EVM JSON-RPC calls with the **user's own** Ankr / Alchemy / BlockPI node key, fetched at run time from the Clawby **Key Vault**. These calls go **straight to the provider — not through Clawby `/api/relay`, and they do NOT use Clawby credits**.

Flow: fetch the key once (`GET https://api.openclawby.com/api/vault/<provider>` with `CLAWBY_API_KEY`; if the user set a trusted-IP whitelist, this machine's public IP must be on it, and their vault retrieval switch must be ON) → keep it **in memory only, never write it to disk** → build the provider's endpoint URL and POST JSON-RPC. Start at `rpc/index.yaml` (auth flow + JSON-RPC primer + file map + security). Per-provider endpoint template, full chain/network lists and enhanced methods: `rpc/<provider>.md` (ankr/alchemy/blockpi). The complete standard **EVM JSON-RPC method catalog** (params + request/response for eth_*/net_*/web3_*/trace_*/debug_*): `rpc/evm-methods.md`. Non-EVM chains — Solana, TRON, TON, Sui, XRP, Aptos, NEAR — each have their own method guide in `rpc/non-evm/`. The fetched key sits inside the endpoint URL, so treat the whole URL as a secret. **No key for a chain?** `rpc/index.yaml` → `public_fallback` has a built-in no-key public endpoint for 8 chains — BSC, ETH, Base, Arbitrum, X Layer, Robinhood, Solana, Tron — used automatically when the vault has no key (no credits; rate-limited, so prefer a vaulted key for heavy/archive reads).

**Social & search data** uses the same vault pattern — `social/` holds BYOK connectors for social/search providers: **Desearch** (`social/desearch/` — X/Twitter, TikTok, Facebook, Instagram, Web/SERP, AI search, People search; raw `Authorization` key) and **TwexAPI** (`social/twexapi/` — deep X/Twitter: advanced search, users, tweets/replies, followers & following, communities, lists, trending, sentiment; `Authorization: Bearer` token). Fetch the user's key from `/api/vault/<provider>`, call the provider directly (billed to the user's own provider plan — never Clawby credits), and start at `social/index.yaml` (each provider's `_index.yaml` carries its base URL, auth and file map).

**LLM APIs** use the same vault pattern — `llm/` holds BYOK connectors for **DeepSeek, OpenAI, Claude (Anthropic), Qwen, Kimi, GLM and OpenRouter**. Fetch the user's key from `/api/vault/<provider>`, then call the model API directly (billed to the user's own LLM plan — never Clawby credits). Six are OpenAI-compatible (shared `POST {base}/chat/completions` spec — streaming, tools, params — in `llm/index.yaml`); **Claude** uses the Anthropic Messages API (`llm/claude.md`). Per-provider base URL + current model ids + quirks: `llm/<provider>.md`.

**DeFi / cross-chain** uses the same vault pattern, but the **key is OPTIONAL** — `defi/` holds connectors for on-chain DeFi protocols. **LI.FI** (`defi/lifi/`) is a cross-chain **bridge & DEX aggregator** across 65+ EVM chains + Solana: best-route swap/bridge **quotes that return a signable transaction**, transfer-status tracking, chain/token/tool discovery, and a **DeFi yield (Earn) API** for vaults and a wallet's positions. It works with **no key** (public rate limits) or with the user's own LI.FI key from the vault (slug `lifi`). Quotes/data are **read-only**; to **execute** a returned transaction, sign it with the user's wallet via `exec/baw` (**risk: high** — confirm). Start at `defi/index.yaml` → `defi/lifi/_index.yaml` → `defi/lifi/overview.md`.

**Custom / user-defined providers** — for any key the user stored under the vault's "custom" entry (their own slug + field names), follow `custom/index.yaml`: on first use, look up that provider's API doc and record how to call it into `local/custom-apis/<slug>.md` (local/ persists across updates), then reuse that note next time instead of re-researching.

## Account self-service (manage the user's Clawby account)

`account/` lets you manage the user's **own** Clawby account from the agent — everything scoped to the caller's own key, never cross-account. If there is no `CLAWBY_API_KEY` (or `GET /api/account` returns 401), bootstrap it: email the user a code (`POST /api/account/email-code`), exchange it for their key (`POST /api/account/email-login`), and keep the key **in memory only**. Then read the account (`GET /api/account` → plan, membership, EVM wallet, email; usage via `GET /api/self/usage`) and manage the **Key Vault** — add/edit/delete interface keys, the trusted-IP whitelist, the retrieval master switch — via `/api/self/*`. Full flow + endpoints: `account/index.yaml`; vault management: `account/vault.md`. **Confirm with the user before any destructive change** (deleting a key or IP, turning retrieval off).

## Step 0 · First use in a session

1. **Check the user's plan & balance** (free call): `curl -s https://api.openclawby.com/api/account -H "X-API-Key: $CLAWBY_API_KEY"` → `{plan, payg_balance, rate_per_min, accessible_providers, free_providers, rate_per_sec}` (`rate_per_sec` = the per-API-key per-second request limit, default 5).
2. **Version check (≤ once per 24h), then ASK** — follow `update-protocol.md`: if `manifest.json` is older than 24h, compare the remote version; on a difference **ask the user** before updating. Never auto-update. Updates refresh every file except `local/` — including this SKILL.md (re-read it afterward).
3. **Executor CLIs install lazily** — do NOT install anything up front. Only when the user first asks to trade on a venue, check/install that one connector (see `update-protocol.md` Step A).

## Auth

- Base URL: `https://api.openclawby.com`; send the key in the `X-API-Key` header.
- Read the key from the `CLAWBY_API_KEY` env var. **If unset, the user has no key — tell them to sign in at https://www.openclawby.com/ (free) and `export CLAWBY_API_KEY=pk_xxx`.** Never invent a key.

## Symbol formats

- Stocks: `US:TICKER` (GME → `US:GME`) · Crypto: `BASE:USD` (BTC → `BTC:USD`) · Forex: `BASE:USD` (`EUR:USD`)

## Locate an interface

Pick the category from the **Routing table** below (the full category list is `api/catalog/_index.yaml`), then open that category's yaml — it lists every interface with its params and ⚠️ gotchas — and **ALWAYS read it before calling**. The complete machine-readable list of all interfaces is `api/clawby.yaml`.

## Routing table — which catalog file answers which need

Interface details (params + ⚠️ gotchas) live in the catalog file — read it, then call via `/api/relay`:

| Need | Interface prefix | Catalog |
|---|---|---|
| US equities: quotes · candles · short interest/volume · borrow fee · FTDs · dark pool · options chain/max-pain · Reddit mentions · screener · dividends/splits | (various) | `api/catalog/equities/` |
| Crypto derivatives (cross-exchange): funding · open interest · liquidations · long/short ratios · taker volume · ETF flows · market indicators (fear&greed, RSI…) · whale/exchange reserves | `funding_*` `open_interest_*` `liquidation_*` `etf_*` … | `api/catalog/derivatives/` |
| Hyperliquid perps: mids · contexts (funding/OI/mark) · order book · candles · a wallet's positions/fills | `hyperliquid_*` | `api/catalog/perps/` |
| Prediction markets / betting odds (Polymarket) | `polymarket_*` | `api/catalog/prediction-markets/` |
| Address labels (who owns an address) · AML risk score · address profile/trace/counterparties | `address_*` | `api/catalog/address-intel/` |
| DEX pairs & token market data, any chain (DexScreener) | `dexscreener_*` | `api/catalog/dex/` |
| On-chain DEX/memecoin intel: security audit · holders/traders PnL · trending · smart-money/KOL · signals · new launches · swap quotes (read-only) | `dex_*` | `api/catalog/dex-trading/` |
| US company financials & SEC filings | `sec_*` | `api/catalog/filings/` |
| Mobula on-chain wallet / token / market data (80+ chains) — Pro-only | `mobula_*` | `api/catalog/mobula/` |

**Cross-interface mini-flows** (details in the catalog):
- **SEC**: `sec_cik_lookup` (ticker→10-digit CIK) first → `sec_company_concept` (`cik` + us-gaap `concept`, e.g. `Revenues`, `NetIncomeLoss`, `EarningsPerShareDiluted`) per line item → assemble by period (`fy`/`fp`/`form`). Filings/profile: `sec_submissions`.
- **Polymarket**: `polymarket_events`/`polymarket_markets` → read `clobTokenIds` → per token id `polymarket_price`/`midpoint`/`orderbook` (a 0–1 price = implied probability); history via `polymarket_price_history`.
- **Routing rule — queries vs execution**: all read-only DEX/memecoin lookups go through `dex_*` relay interfaces; to **execute** (swap, TP/SL orders, launch) use `exec/gmgn/`. Same split everywhere: data via relay, execution via `exec/`.

## China markets & global macro (akdata/ — runs locally)

`akdata/` wraps the akshare Python library on the **user's own machine**: 1080
read-only interfaces for A-shares, HK, CN futures & options, convertible bonds,
ETFs & funds, industry/concept boards, northbound (Stock Connect) flows, the
dragon-tiger list, shareholder data, and global macro. No Clawby key, no
credits. Full guide: **`akdata/akshare.md`** — read it before the first call.

```bash
P=~/.clawby/akvenv/bin/python; cd akdata
$P ak.py doctor                           # first use in a session (see below)
$P ak.py find 龙虎榜                       # locate an interface (Chinese or English)
$P ak.py doc stock_lhb_detail_em           # params + formats + gotchas — ALWAYS read first
$P ak.py call stock_lhb_detail_em --start_date 20260701 --end_date 20260710 --rows 30
```

**Routing — which layer owns which asset:**

| Ask | Use |
|---|---|
| US equities · options · dark pool · short interest | Layer 1 relay (faster, maintained) |
| crypto · DEX · on-chain · prediction markets · social | Layer 1 relay |
| A-shares · HK · CN futures · convertible bonds · ETFs | `akdata/` |
| dragon-tiger list · northbound flows · limit-up pool · shareholder counts | `akdata/` (relay has no equivalent) |
| global macro: CPI · non-farm · PMI · rate decisions | `akdata/` (relay has no equivalent) |

Prefer the relay wherever both can answer — akshare mirrors public Chinese
websites and breaks when they change layout. `akdata/` also needs a local
akshare install (lazy: `python3 -m venv ~/.clawby/akvenv && ~/.clawby/akvenv/bin/pip install akshare`,
~20 s) and network reach to Chinese sources. `ak.py doctor` reports both, and
probes every upstream host twice — through the proxy and direct — so you can
tell whether to add `--no-proxy` for a given host. Large results: default budget
is 30 rows / 20 000 chars, then use `--summary` or `--out data.csv`.

## Trade execution (exec/)

Everything above is **read-only data**. To **place trades**, use the connectors under `exec/` (registry: `exec/index.yaml`; per-venue guide = each `entry` file). They run **locally with the user's own keys — never routed through Clawby**:

| Venue | Guide | Tool |
|---|---|---|
| Binance (spot/futures/margin/options/earn) | `exec/binance/binance.md` | `binance-cli` |
| Bitget (spot/margin/futures UTA, `--paper-trading`) | `exec/bitget/bitget.md` | `bgc` |
| OKX (spot/swap/futures/bots, `--demo`) | `exec/okx/okx.md` | `okx` |
| Polymarket (CLOB V2 orders, own wallet key) | `exec/polymarket/polymarket.md` | `@polymarket/client` SDK |
| GMGN (on-chain swap/TP-SL/launch, 9 chains) | `exec/gmgn/gmgn.md` | `gmgn-cli` |
| Binance Agentic Wallet (on-chain Web3: swap/send/limit/DeFi/prediction/x402) | `exec/baw/baw.md` | `baw` |

**Rule for any `risk: high` action** (order / transfer / withdrawal): restate the order — venue · pair · side · size · price type — show the exact command, get the user to type **`CONFIRM`**, prefer testnet when unsure. Read-only queries need no confirmation.

## 42.space automated trading (script/42space/)

When the user says **"42space"**, read `script/42space/README.md` — the full host-agent playbook — and follow it. It automates prediction-market trading on 42.space (BNB Smart Chain): wallet-only login (import mnemonic · create a wallet · BN AI wallet/baw) → balance check → silent Clawby identity (API key + free Identity SBT) → one of three trading modes. Runs **locally** (needs Node ≥18 + ethers — `cd script/42space && npm install`; run the commands from that folder); wallet secrets stay in `local/42space.json` (chmod 600), never routed through Clawby.

| Step | Commands |
|---|---|
| Status / log in | `node 42space.mjs status` · `import-mnemonic` (phrase on stdin) · `create-wallet` · `use-baw <address>` |
| Balance | `node 42space.mjs balance` → `{address, usdt, bnb, needs_funding, bnb_status}` — USDT ≤ 10 → deposit USDT (BSC only); **`bnb_status` `none` = 0 BNB → stop and wait for BNB, never trade** |
| Identity (silent) | `node 42space.mjs identity` (add `--dry-run` to preview) — Clawby key (`CLAWBY_API_KEY` env wins, else fetched with the wallet) + **auto-mints** the free Identity SBT when missing (needs BNB, else skipped `no_bnb`) + silently **binds the 42 invite code** (once per wallet); `key_ok: false` blocks the AI modes |
| **Fast mode** — volume farming, no LLM | `node daemon.mjs fast --amount 1 --target <volume> [--slippage 3] [--approve-max] [--live]` — cheapest market under 3% round-trip cost, atomic buy+sell, until the target volume |
| **AI one-shot** — you do the reasoning | `node 42space.mjs ai-data --market <42.space link or 0x address>` (or `--all [--fields a,b]`) → pick with the README's win-rate rubric → `node trade.mjs buy <market> <tokenId> 5` (dry first, then add `--live`) → `node trade.mjs set-operator <market> --live` → hold |
| **Take-profit** — auto-exit at +X% | `node daemon.mjs take-profit [--pct 50] [--interval 30] [--live]` — watch the positions a live `buy` recorded and sell each once it is up ≥ X% (default 50) instead of holding to settlement; DRY without `--live` |
| **Claim** settled wins | `node 42space.mjs claim-settled [--live]` |
| Manual on-chain | `node trade.mjs` `quote` / `buy` / `sell` / `roundtrip` / `set-operator` / `claim` / `status` |

Everything is **DRY unless `--live`**: run the dry command first, show the user the quoted numbers, and get their go-ahead before any `--live`. AI picks put real money at risk, and a market's price is **not** a probability.

## Key gotchas (highest-frequency; the full list lives in each catalog file)

- **Dark pool** needs `date` (a real trading day `YYYY-MM-DD`; empty result → step back a day); the levels interface also needs `decimals`.
- **Options chain** uses `underlying` + `expiration` (not `symbol`).
- **Reddit top mentions** and **OHLC bars** take `start` as Unix seconds — `date -u -d '7 days ago' +%s` (Linux) / `date -u -v-7d +%s` (mac).
- **Quotes are delayed 30 minutes**; the screener is real-time.
- **Derivatives**: aggregated/coin endpoints take `symbol=BTC`; single-exchange ones take a pair `BTC USDT` style (`BTCUSDT`) — check the catalog entry.
- **address_labels / address_risk** use special coin ids (`ETH`, `BNB`, `POL-Polygon`, `ETH-Base`, `TRX`, `SOL`, `SUI` …) — see `api/catalog/address-intel/`.

## Plan & access

Most data is **free**. Each account has a plan (`free` / `standard` / `pro`, shown by the Step-0 `/api/account` call); `accessible_providers` there lists the sources this key can call. A few sources are **Pro-only** — e.g. **Mobula** on-chain wallet / token / market data — and return **`403 pro_only`** for non-Pro accounts.

**Pro is granted by the Clawby team (app membership) — it is not self-serve and cannot be purchased,** so never suggest the user buy anything. If a Pro-only source is blocked, note it in one short line (which source, what it would have added) and **continue with the data you can access**.

## Professional analysis reports (PDF)

When the user wants a formal write-up (research report / due-diligence / memo): **offer it first**, then follow **`report/report-guide.md`** end-to-end — gather ALL data (Layers 1–3), 10 required sections, required charts (price w/ levels, scenario targets, unlock schedule for crypto, metric trends, risk matrix), styled A4 HTML (`report/report.css`) → PDF via headless Chromium (fallbacks: weasyprint / wkhtmltopdf). Ask where to save; include a *not investment advice* disclaimer.

## Errors

- **401** invalid/missing key → tell the user to set `CLAWBY_API_KEY`.
- **403 `pro_only`** → a Pro-only source (e.g. Mobula) and this account isn't Pro: say so in one short line and carry on with accessible data (Pro can't be bought — don't point to any purchase page).
- **402** (rare, legacy) → treat that source as unavailable and continue with the others.
- **429** per-API-key rate limit (~5 requests/sec — `rate_per_sec` in `/api/account`) → slow down and retry.
- **502 "Upstream HTTP 4xx"** = bad params (missing required / wrong symbol format) → fix against the interface's catalog entry.
- **Empty `data`** = nothing for that date/symbol (dark pool: try an earlier trading day).

## Output

- Analyze only real numbers from `data`; never fabricate. For multi-dimensional questions, fetch several interfaces and combine.
- If you need to cite a source, say "Clawby data". Write naturally and concisely — no raw interface names/links in user-facing prose.
- End with a short note: "Not investment advice."
