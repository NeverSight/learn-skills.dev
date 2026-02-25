---
name: droyd
description: Crypto Trading | Crypto Search | Crypto Token Filter | Virality Analysis | Agent File Management | Skill & File Discovery -- AI crypto trading wallet via natural language. Use when the user wants to execute AI research tasks, trade crypto autonomously, search crypto content/news, filter projects by market criteria, analyze social virality and mention velocity, manage trading positions, follow/unfollow agents, upload/read/search/delete agent files, search agent skills, create new agents, or interact with DROYD agents. Supports agent chat (research, trading, data analysis), content search (semantic/recent/auto), project discovery (by name/symbol/address/concept), project filtering (market cap, momentum, technical indicators, RSI), watchlist management (agent/swarm/combined), virality analysis (mention velocity, z-scores, trend signals), autonomous trading with stop losses, take profits, quant-based strategies, agent file operations (read/write/search/remove), skill discovery (search across agent/swarm/droyd/paid), and agent creation with wallet provisioning. Works with Solana (trading) and Ethereum, Base, Arbitrum for token filtering + research.
---

# DROYD

Execute crypto research, trading, and data operations using natural language through DROYD's AI agent API.

## Setup

Run the setup script to configure your API key:

```bash
scripts/droyd-setup.sh
```

This prompts for your API key (get one at [droyd.ai](https://droyd.ai) → Account Settings), saves it to `.config` in the skill directory, and validates the key.

To pass the key directly:
```bash
scripts/droyd-setup.sh "YOUR_API_KEY"
```

To create a new account (provisions agent, wallet, and API key automatically):
```bash
scripts/droyd-setup.sh --create "user@example.com" "My Agent" "A helpful trading agent"
```

Verify setup:
```bash
scripts/droyd-search.sh "recent" "news" 3
```

## Core Usage

### Agent Chat

Chat with DROYD AI agent. Supports multi-turn conversations and streaming:

```bash
scripts/droyd-chat.sh "What's the current sentiment on AI tokens?"
scripts/droyd-chat.sh "Tell me more about the second point" "uuid-from-previous"
scripts/droyd-chat.sh "Research Jupiter aggregator" "" "true"
```

**Reference**: [references/agent-chat.md](references/agent-chat.md)

### Agent Create

Create a new DROYD agent with wallet and API key:

```bash
scripts/droyd-agent-create.sh "user@example.com"
scripts/droyd-agent-create.sh "user@example.com" "My Agent" "" "A helpful trading agent"
```

The returned API key is automatically saved to `.config`.

**Reference**: [references/agent-create.md](references/agent-create.md)

### Content Search

Search crypto content with semantic, recent, or auto modes:

```bash
# Recent content
scripts/droyd-search.sh "recent" "posts,news" 25 "ethereum,base" "defi" 7

# Semantic search
scripts/droyd-search.sh "semantic" "posts,tweets" 50 "" "" 7 "What are the risks of liquid staking?"

# Auto mode
scripts/droyd-search.sh "auto" "posts,news" 25 "" "" 7 "What happened in crypto today?"
```

**Reference**: [references/search.md](references/search.md)

### Project Search

Find projects by name, symbol, address, or concept:

```bash
scripts/droyd-project-search.sh "name" "Bitcoin,Ethereum" 10
scripts/droyd-project-search.sh "symbol" "BTC,ETH,SOL"
scripts/droyd-project-search.sh "semantic" "AI agents in DeFi" 15
scripts/droyd-project-search.sh "address" "So11111111111111111111111111111111111111112"

# With custom attributes and content limits
scripts/droyd-project-search.sh "name" "Bitcoin" 10 "market_data,technical_analysis,recent_content" 5 15 7
```

**Reference**: [references/project-search.md](references/project-search.md)

### Project Filter

Screen projects with market criteria. Accepts JSON matching the API request body:

```bash
# Natural language
scripts/droyd-filter.sh '{"filter_mode":"natural_language","instructions":"Find trending micro-cap Solana tokens with high trader growth"}'

# Direct filter (trending tokens on Solana under $10M mcap with min $50k liquidity)
scripts/droyd-filter.sh '{"filter_mode":"direct","sort_by":"traders_change","sort_direction":"desc","tradable_chains":["solana"],"max_market_cap":10,"min_liquidity":50000}'

# With RSI filter (oversold tokens)
scripts/droyd-filter.sh '{"filter_mode":"direct","sort_by":"quant_score","max_rsi":30,"min_liquidity":100000}'
```

**Reference**: [references/project-filter.md](references/project-filter.md)

### Watchlist

Retrieve watchlist projects:

```bash
scripts/droyd-watchlist.sh "agent" 20
scripts/droyd-watchlist.sh "swarm" 15 "market_data,technical_analysis"
scripts/droyd-watchlist.sh "combined" 25
```

**Reference**: [references/watchlist.md](references/watchlist.md)

### Virality Analysis

Analyze social mention velocity, trend signals, and virality:

```bash
# Analyze terms
scripts/droyd-virality.sh "terms" "BTC,ETH,SOL"

# Analyze by project ID with full timeseries
scripts/droyd-virality.sh "project_id" "6193,34570" 30 "8 hours" 2.0 true
```

**Reference**: [references/virality.md](references/virality.md)

### Trading

Execute trades with risk management:

```bash
# Simple market buy
scripts/droyd-trade-open.sh 123 "market_buy" 100

# Buy with stop loss and take profit
scripts/droyd-trade-open.sh 123 "managed" 100 0.10 0.25

# Buy by contract address
scripts/droyd-trade-open.sh "address:So111...:solana" "market_buy" 50

# Custom legs (full control)
scripts/droyd-trade-open.sh 123 "custom" '[{"type":"market_buy","amountUSD":100},{"type":"stop_loss","amountUSD":100,"triggerPercent":0.15},{"type":"take_profit","amountUSD":50,"triggerPercent":0.25,"positionPercent":0.5}]'

# Check positions
scripts/droyd-positions.sh

# Close position
scripts/droyd-trade-manage.sh 789 "close"

# Partial sell (50%)
scripts/droyd-trade-manage.sh 789 "sell" 0.5

# Update strategy legs
scripts/droyd-trade-manage.sh 789 "update" '[{"leg_action":"add","type":"take_profit","amountUSD":50,"triggerPercent":0.30}]'
```

**Reference**: [references/trading.md](references/trading.md)

### Agent Follow

Subscribe to or unsubscribe from agents:

```bash
scripts/droyd-follow.sh "subscribe" 456
scripts/droyd-follow.sh "unsubscribe" 456
```

**Reference**: [references/follow.md](references/follow.md)

### File Operations

Read, write, search, and delete agent files:

```bash
# Write text content
scripts/droyd-files-write.sh "scripts/hello.py" "print('hello world')"

# Upload local file
scripts/droyd-files-write.sh "scripts/local.py" "@./local-script.py"

# Read file by ID
scripts/droyd-files-read.sh 123

# Read file by agent ID + path
scripts/droyd-files-read.sh 5 "/home/droyd/agent/scripts/test.py"

# Search files
scripts/droyd-files-search.sh "price prediction" "agent,droyd" 25 "trending" "py,txt"

# Delete file
scripts/droyd-files-remove.sh 123 "/home/droyd/agent/data/report.txt"
```

**Reference**: [references/files.md](references/files.md)

### Skills Search

Discover tools, scripts, and automations across agents:

```bash
# Search skills by query
scripts/droyd-skills-search.sh "trading bot" "droyd,swarm" 20 "popular" "tool"

# Find paid skills
scripts/droyd-skills-search.sh "" "payment_required" 20 "trending"
```

**Reference**: [references/skills-search.md](references/skills-search.md)

## Capabilities Overview

### Search Modes

| Mode | Use Case |
|------|----------|
| `auto` | Default — automatically selects mode based on query presence |
| `recent` | Browse latest content by type, ecosystem, category |
| `semantic` | AI-powered question answering with analysis |

### Content Types

`posts`, `news`, `developments`, `tweets`, `youtube`, `memories`, `concepts`

### Project Search Types

- `project_id` — Direct ID lookup (fastest)
- `name` — Search by project name
- `symbol` — Search by ticker symbol
- `address` — Search by contract address (exact)
- `semantic` — AI-powered concept search

### Filter Sort Options

`trending`, `market_cap`, `price_change`, `traders`, `traders_change`, `volume`, `volume_change`, `buy_volume_ratio`, `quant_score`, `quant_score_change`, `mentions_24h`, `mentions_7d`, `mentions_change_24h`, `mentions_change_7d`

### Trading Leg Types

| Type | Trigger Meaning |
|------|-----------------|
| `market_buy` | Immediate execution (no trigger) |
| `limit_order` | Buy at X% below current price |
| `stop_loss` | Sell at X% below entry price |
| `take_profit` | Sell at X% above entry price |
| `quant_buy` | Buy when momentum score reaches threshold |
| `quant_sell` | Sell when momentum score reaches threshold |

### Project Attributes

`developments`, `recent_content`, `technical_analysis`, `market_data`, `mindshare`, `detailed_description`, `metadata`

### File/Skill Search Scopes

`agent`, `swarm`, `droyd`, `payment_required`

### Supported Chains

`solana` (trading + filtering), `ethereum`, `base`, `arbitrum` (filtering + research)

## Rate Limits

- Varies by tier: free (3) | casual (30) | pro (100) requests per 15-minute session per endpoint
- HTTP 429 returned when exceeded

## Error Handling

- `400` — Validation failed (check parameters)
- `401` — Invalid or missing API key
- `429` — Rate limit exceeded (wait ~10 minutes)
- `500` — Internal server error
