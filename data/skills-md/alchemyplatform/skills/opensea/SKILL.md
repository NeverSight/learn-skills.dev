---
name: opensea
description: Query OpenSea marketplace data — listings, offers, sales / events, floor prices, collection stats, drops, traits — and execute Seaport trades via the official `@opensea/cli` and OpenSea REST API across Ethereum, Base, Arbitrum, Optimism, Polygon, and more. Includes search across collections / NFTs / tokens / accounts. NOT for general NFT metadata reads (name, image, traits, ownership), token metadata, current wallet balances, transaction history, or live RPC reads — for those use `alchemy-cli` (live), `alchemy-mcp`, `alchemy-api` (app code), or `agentic-gateway` (no API key). For pure cross-chain token swaps (no marketplace context), prefer the `lifi` ecosystem skill. Requires `OPENSEA_API_KEY` (instant via API).
license: MIT
compatibility: API key required via `$OPENSEA_API_KEY` (instant — `curl -X POST https://api.opensea.io/api/v2/auth/keys` returns a key with no signup, or sign up at https://opensea.io/settings/developer for higher limits). Optional `$PRIVY_APP_ID` / `$PRIVY_APP_SECRET` / `$PRIVY_WALLET_ID` for write / fulfillment flows. Needs Node.js (≥ 18), `curl`, `jq` (recommended).
metadata:
  author: opensea
  version: "0.1"
  provider: opensea
  partner: "true"
---

# OpenSea (NFT Marketplace Data + Seaport Trades)

OpenSea is the dominant NFT marketplace. This skill queries marketplace data — listings, offers, sales / events, floor prices, drops, traits — and executes Seaport trades via the official `@opensea/cli`. For NFT metadata (name, image, traits, ownership) outside the marketplace context, use Alchemy's NFT API instead. For pure cross-chain token swaps (no marketplace context), use the `lifi` ecosystem skill.

| | |
| --- | --- |
| **Primary tool** | `npx @opensea/cli@latest <command>` (or `npm install -g @opensea/cli`) |
| **REST API base** | `https://api.opensea.io/api/v2` |
| **Auth** | `OPENSEA_API_KEY` header — instant via `POST /api/v2/auth/keys`, or signup at the developer portal |
| **Optional Privy** | `PRIVY_APP_ID` / `PRIVY_APP_SECRET` / `PRIVY_WALLET_ID` for write / fulfillment flows |
| **Chains** | Ethereum, Base, Arbitrum, Optimism, Polygon, and more |

## When to use this skill

Use `opensea` when **any** of the following are true:

- The user wants **marketplace data** — listings, offers, floor prices, sales history, collection stats
- The user wants to **buy / sell an NFT** via Seaport (fulfill listing or accept offer)
- The user wants to **search** across OpenSea (collections / NFTs / tokens / accounts)
- The user wants to **monitor events** — sales, transfers, mints, listings, offers — for a collection or NFT
- The user wants to **explore drops** or build a mint transaction for a SeaDrop contract
- The user wants **token discovery** in the OpenSea-curated context (top, trending, by group)

## When NOT to use this skill (handoff)

| Need | Use instead |
| --- | --- |
| NFT metadata (name, image, traits, ownership lookup) outside a marketplace context | `alchemy-api` (NFT API) — broader coverage, fewer rate limits |
| Pure cross-chain token swap (no NFT marketplace need) | `lifi` (ecosystem skill) — broader bridge / DEX aggregation |
| Token spot prices for valuation | `alchemy-api` (Prices API) |
| Token metadata, search, list by chain (general) | `alchemy-api` (Token API) |
| Current wallet balances (token + native) | `alchemy-api` (Portfolio / Token API) |
| Transaction history (transfers in / out) | `alchemy-api` (Transfers API) |
| Live blockchain reads (block #, gas, `eth_call`) | `alchemy-cli` (live) or `alchemy-api` (JSON-RPC) |
| Pre-execution simulation | `alchemy-api` (Simulation API) |
| Account abstraction (bundlers, gas managers) | `alchemy-api` |
| Smart wallet / embedded wallet flows | `alchemy-api` (Wallets / Account Kit) |

## Scope contract

**This skill covers (`scope_in`):**

- **Marketplace data:** `opensea listings best`, `opensea listings best-for-nft`, `opensea offers best-for-nft`, `opensea offers all`, `opensea collections stats`, `opensea collections trending`, `opensea collections top`, `opensea collections traits`
- **Seaport trades:** fulfillment data for buying (`opensea-fulfill-listing.sh`) and selling (`opensea-fulfill-offer.sh`); creating listings / offers via `opensea-post.sh` with the Seaport order structure
- **Events / monitoring:** `opensea events list`, `events by-collection`, `events by-nft`, `events by-account` — sale / transfer / mint / listing / offer / trait_offer / collection_offer
- **Drops + minting:** `opensea drops list`, `opensea drops get`, `opensea drops mint`
- **Search:** `opensea search` across collections / NFTs / tokens / accounts
- **Account utilities:** `opensea accounts resolve` (ENS / username / address)

**This skill does NOT cover (`scope_out`):**

- General NFT metadata reads (name, image, traits, ownership, contract metadata) outside the marketplace context → handoff: `alchemy-api` (NFT API). OpenSea's NFT data is marketplace-flavored and rate-limited; Alchemy's NFT API is broader and cheaper for pure metadata.
- Pure cross-chain token swaps (no NFT marketplace use case) → handoff: `lifi` (ecosystem skill). OpenSea's swap aggregator works, but `lifi` covers more bridges and chains.
- Token spot prices for valuation / display → handoff: `alchemy-api` (Prices API)
- General token metadata, search, list → handoff: `alchemy-api` (Token API)
- Wallet balances (token + native) → handoff: `alchemy-api` (Portfolio / Token API)
- Transaction transfer history → handoff: `alchemy-api` (Transfers API)
- Live RPC reads → handoff: `alchemy-cli` or `alchemy-api` (JSON-RPC)
- Pre-execution simulation → handoff: `alchemy-api` (Simulation API)
- Account abstraction → handoff: `alchemy-api` (Wallets / Bundler / Gas Manager)
- Embedded / smart wallet onboarding → handoff: `alchemy-api` (Account Kit)
- Signed tx submission → user wallet (or Privy if configured for OpenSea write flows)

## Setup

API key is required. Get one instantly via the auth endpoint (no signup) or register at the developer portal for higher limits:

```bash
# Instant key (no signup needed)
export OPENSEA_API_KEY=$(curl -s -X POST https://api.opensea.io/api/v2/auth/keys | jq -r '.api_key')

# Or set an existing key
# export OPENSEA_API_KEY="..."
```

Install the CLI globally (optional — `npx @opensea/cli` works without install):

```bash
npm install -g @opensea/cli
```

For write / fulfillment flows that sign with Privy:

```bash
export PRIVY_APP_ID="..."
export PRIVY_APP_SECRET="..."
export PRIVY_WALLET_ID="..."
```

> **Security:** never expose `OPENSEA_API_KEY` or Privy credentials in client-side code. Server-side only.

## Endpoint reference → [references/marketplace.md](./references/marketplace.md)

### Marketplace queries (most-used)

| Task | CLI |
| --- | --- |
| Best listings for a collection | `opensea listings best <slug> [--limit <n>]` |
| Best listing for a specific NFT | `opensea listings best-for-nft <slug> <token_id>` |
| Best offer for an NFT | `opensea offers best-for-nft <slug> <token_id>` |
| All listings on a collection | `opensea listings all <slug> [--limit <n>]` |
| All offers on a collection | `opensea offers all <slug> [--limit <n>]` |
| Trait offers | `opensea offers traits <slug> --type <type> --value <value>` |
| Collection stats (floor, volume) | `opensea collections stats <slug>` |
| Trending collections | `opensea collections trending [--timeframe <tf>] [--chains <chains>]` |
| Top collections by sort | `opensea collections top [--sort-by <field>] [--chains <chains>]` |
| Collection traits | `opensea collections traits <slug>` |

### Seaport trade execution

| Task | Script |
| --- | --- |
| Get fulfillment data to **buy** an NFT | `opensea-fulfill-listing.sh <chain> <order_hash> <buyer>` |
| Get fulfillment data to **sell** (accept offer) | `opensea-fulfill-offer.sh <chain> <order_hash> <seller> <contract> <token_id>` |
| Generic POST to OpenSea API | `opensea-post.sh <path> <json_body>` |

### Events / monitoring

| Task | CLI |
| --- | --- |
| Recent events (filterable by type) | `opensea events list [--event-type <type>]` |
| Events for a collection | `opensea events by-collection <slug> [--event-type <type>]` |
| Events for a specific NFT | `opensea events by-nft <chain> <contract> <token_id>` |
| Events for an account | `opensea events by-account <address>` |

Event types: `sale`, `transfer`, `mint`, `listing`, `offer`, `trait_offer`, `collection_offer`.

For real-time event streaming: `opensea-stream-collection.sh <slug>` (requires `websocat`).

### Drops + minting

| Task | CLI |
| --- | --- |
| List drops (featured / upcoming / recent) | `opensea drops list [--type <type>]` |
| Drop details + stages | `opensea drops get <slug>` |
| Build mint tx | `opensea drops mint <slug> --minter <address> [--quantity <n>]` |

### Search

| Task | CLI |
| --- | --- |
| Search collections | `opensea search <query> --types collection` |
| Search NFTs | `opensea search <query> --types nft` |
| Search tokens | `opensea search <query> --types token` |
| Search accounts | `opensea search <query> --types account` |
| Multi-type search | `opensea search <query> --types collection,nft,token` |

## Quick examples

### Get the floor + 24h volume for Bored Apes

```bash
opensea collections stats boredapeyachtclub
```

### Find the cheapest listing for a collection

```bash
opensea listings best boredapeyachtclub --limit 1
```

### Buy an NFT (fulfill a listing)

```bash
# 1. Get the best listing for a specific NFT
opensea listings best-for-nft boredapeyachtclub 1234

# 2. Get fulfillment data — order_hash from above response
./scripts/opensea-fulfill-listing.sh ethereum 0xORDER_HASH 0xYOUR_WALLET

# 3. Sign + submit the returned tx data via your wallet
```

### Stream sales for a collection in real time

```bash
./scripts/opensea-stream-collection.sh boredapeyachtclub
# Filters to sale events; pipe through jq to format
```

### Search across types

```bash
opensea search "cool cats" --types collection,nft --chains ethereum,base
```

## Common gotchas

- **API key is mandatory** — even the "instant" tier requires one. The bare REST API will 401 without `X-API-KEY`.
- **OpenSea's NFT data overlaps with Alchemy's NFT API** for metadata reads. Prefer Alchemy for *general* NFT metadata (name, image, traits, ownership across many wallets) — OpenSea is rate-limited harder and adds marketplace flavoring you may not want. Use OpenSea when the marketplace context (listings, offers, sales history, drops) is the actual need.
- **Token swap aggregator** exists in the OpenSea API (`opensea swaps quote`), but for pure swap flows without marketplace context, `lifi` aggregates more bridges + DEXs and is the better default. Use OpenSea swaps when the user is already in an NFT-buying flow that involves a token swap.
- **Privy is optional** but required for end-to-end write flows. The skill returns fulfillment calldata; how it gets signed is up to the app (user wallet, Privy, or any other signer).
- **Order hashes** from `listings best-for-nft` / `offers best-for-nft` are needed for fulfillment. Don't lose them between API calls.
- **Event streaming** requires `websocat`; if not installed, fall back to polling `events by-collection` with the same filters.
- **Slug vs. address**: collections are addressed by slug (e.g., `boredapeyachtclub`), NFTs by `(chain, contract, tokenId)`. Don't mix.

## Routing back to Alchemy

If during a session the user's need shifts to surfaces this skill doesn't cover:

- **NFT metadata reads** (name, image, traits, ownership) — `alchemy-api` (NFT API) is the right path. OpenSea's NFT API is marketplace-flavored and rate-limited; Alchemy's is broader and faster.
- **Token prices, balances, transfer history, general token metadata** — `alchemy-api`
- **Live RPC, gas, simulation, AA, Account Kit** — `alchemy-cli` (live) or `alchemy-api` (app code) or `agentic-gateway` (no API key)
- **Pure cross-chain token swaps** — `lifi` (ecosystem skill); covers 27 bridges + 31 DEXs across 60+ chains

---

> **Maintenance:** OpenSea maintains `@opensea/cli` and the underlying API; this skill itself is maintained jointly by Alchemy and OpenSea. File issues against `alchemyplatform/skills` with `[ecosystem/opensea]` in the title.
