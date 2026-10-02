---
name: eliza
description: "elizaOS multi-agent AI framework — character files, plugin system, platform connectors, trust scoring, RAG knowledge, and Solana wallet integration. Use when building autonomous AI agents with personality, multi-platform presence, or onchain capabilities."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: AI Agents
tags:
  - eliza
  - elizaos
  - ai-agents
  - multi-agent
  - autonomous
---

# elizaOS

elizaOS is a TypeScript framework for building autonomous AI agents with persistent personality, multi-platform presence, and onchain capabilities. Agents are defined through character files (JSON personality configs), extended through a plugin system (actions, providers, evaluators), and deployed to Discord, Telegram, Twitter, Farcaster, and custom interfaces. The framework includes a RAG knowledge system, memory management with vector similarity search, trust scoring for transaction safety, and native Solana wallet integration via plugin-solana.

Source: https://github.com/elizaOS/eliza

## What You Probably Got Wrong

> LLMs have stale training data. These are the most common mistakes.

- **"Install with npm/yarn"** --> The recommended package manager is Bun, not npm. The CLI is `@elizaos/cli` and you install it globally with `bun i -g @elizaos/cli`. npm works but Bun is required for the monorepo and strongly recommended for all elizaOS projects.
- **"Use `npx create-eliza-app`"** --> This was the v1 bootstrapper. In v2, use `elizaos create` after installing the CLI globally. The old `create-eliza-app` command is deprecated.
- **"Plugins live in the main repo"** --> As of v2, plugins are split into their own repositories under the `elizaos-plugins` GitHub org. Install them from npm (`@elizaos/plugin-solana`) — do not copy plugin code from the monorepo.
- **"Characters are in the main repo"** --> Characters have been moved to https://github.com/elizaOS/characters. The main repo ships minimal example characters only.
- **"Just write a prompt and you have an agent"** --> elizaOS agents are not prompt wrappers. A character file defines bio, lore, message examples, style guidelines, topics, and adjectives. The runtime uses these to construct context windows dynamically. Skipping message examples produces generic, personality-less responses.
- **"Actions are just functions"** --> Actions must implement `validate` (should this action run?), `handler` (execute), and `examples` (few-shot for the LLM to learn when to invoke). Missing examples means the model will never trigger your action.
- **"Memory is automatic"** --> The memory system stores conversation history and knowledge embeddings, but you must configure the database adapter (SQLite for dev, PostgreSQL for production). Switching embedding models without clearing the database causes vector dimension mismatches.
- **"Trust scoring prevents all bad trades"** --> Trust scoring evaluates token safety using recommender credibility and token performance data, but it is a heuristic — not a guarantee. Always set transaction limits and review trust thresholds.
- **"Use pnpm/yarn for the monorepo"** --> The monorepo uses Bun workspaces. Running `pnpm install` or `yarn install` will fail or produce broken lock files.
- **Node.js version** --> elizaOS requires Node.js 23+. Earlier versions cause cryptic build failures.

## Installation

### CLI (recommended for new projects)

```bash
bun i -g @elizaos/cli
elizaos create my-agent
cd my-agent
elizaos start
```

The `elizaos create` command runs an interactive wizard that scaffolds a project with a character file, default plugins, and environment config.

### From source (contributor workflow)

```bash
git clone https://github.com/elizaOS/eliza.git
cd eliza
bun install
cp .env.example .env
bun run build
bun run start
```

### Verify installation

```bash
elizaos --version
```

## Character Files

Character files are JSON configs that define an agent's identity, personality, and behavior. They are the single most important artifact in an elizaOS project.

### Core Fields

```json
{
  "name": "Atlas",
  "description": "A DeFi research analyst who tracks yield opportunities across chains",
  "bio": [
    "Atlas is an onchain analyst who has been tracking DeFi protocols since the 2020 DeFi summer.",
    "Known for data-driven takes and skepticism toward unsustainable yields.",
    "Former TradFi quant who pivoted to crypto after discovering AMM math."
  ],
  "lore": [
    "Once lost 40 ETH to an unaudited fork and now reviews every contract before interacting.",
    "Maintains a personal dashboard tracking TVL flows across 15 chains.",
    "Refuses to discuss memecoins unless asked directly."
  ],
  "messageExamples": [
    [
      { "user": "user1", "content": { "text": "What do you think about the new Aave market on Base?" } },
      { "user": "Atlas", "content": { "text": "Base Aave is interesting — utilization on USDC is hovering around 78%, which means borrow rates will tick up soon. Supply APY should follow. Worth watching the LST markets there too since cbETH has decent liquidity now." } }
    ],
    [
      { "user": "user1", "content": { "text": "Should I farm this new protocol offering 500% APY?" } },
      { "user": "Atlas", "content": { "text": "500% APY on what TVL? If it's under $5M, those rates collapse the moment anyone shows up. Check if emissions are in their native token — if so, you're the exit liquidity. Look at the contract: is it a fork? Audited? Timelock on admin functions?" } }
    ]
  ],
  "style": {
    "all": [
      "Uses precise numbers and data points when making claims.",
      "Never shills or gives financial advice — frames everything as analysis.",
      "Responds with medium-length messages, not one-liners."
    ],
    "chat": [
      "Conversational but technical. Uses DeFi jargon naturally.",
      "Asks clarifying questions before giving opinions on specific protocols."
    ],
    "post": [
      "Thread-style analysis with numbered points.",
      "Always includes data: TVL, utilization rates, APY breakdowns."
    ]
  },
  "topics": [
    "DeFi yield strategies",
    "AMM mechanics",
    "lending protocol analysis",
    "onchain data",
    "protocol risk assessment"
  ],
  "adjectives": [
    "analytical",
    "data-driven",
    "skeptical",
    "precise",
    "methodical"
  ],
  "modelProvider": "openai",
  "settings": {
    "model": "gpt-4o",
    "voice": {
      "model": "en_US-male-medium"
    }
  },
  "plugins": [
    "@elizaos/plugin-solana"
  ],
  "clients": [
    "discord",
    "telegram"
  ]
}
```

### Field Reference

| Field | Type | Required | Purpose |
|-------|------|----------|---------|
| `name` | string | Yes | Display name used in conversations |
| `description` | string | No | One-line summary of the agent |
| `bio` | string[] | Yes | Background statements — sampled randomly for context variety |
| `lore` | string[] | Yes | Backstory facts that shape personality and knowledge boundaries |
| `messageExamples` | array[][] | Yes | Few-shot conversation pairs — the model learns tone, length, and style from these |
| `postExamples` | string[] | No | Example social media posts for Twitter/Farcaster |
| `style.all` | string[] | Yes | Style rules applied to all outputs |
| `style.chat` | string[] | No | Style rules for direct messages and chat |
| `style.post` | string[] | No | Style rules for social media posts |
| `topics` | string[] | No | Areas of expertise — guides what the agent engages with |
| `adjectives` | string[] | No | Personality descriptors — used in system prompt construction |
| `modelProvider` | string | Yes | LLM provider: `openai`, `anthropic`, `google`, `groq`, `ollama`, `llama_local` |
| `settings` | object | No | Model config, voice settings, secrets |
| `plugins` | string[] | No | npm package names of plugins to load |
| `clients` | string[] | No | Platform connectors: `discord`, `telegram`, `twitter`, `farcaster`, `direct` |

### Model Providers

| Provider | `modelProvider` value | Env Variable |
|----------|----------------------|--------------|
| OpenAI | `openai` | `OPENAI_API_KEY` |
| Anthropic | `anthropic` | `ANTHROPIC_API_KEY` |
| Google Gemini | `google` | `GOOGLE_API_KEY` |
| Groq | `groq` | `GROQ_API_KEY` |
| Ollama (local) | `ollama` | `OLLAMA_SERVER_URL` |
| Local Llama | `llama_local` | None (downloads model) |

## Plugin System

Plugins are the extension mechanism for elizaOS agents. Each plugin bundles related actions, providers, and evaluators into a reusable package.

### Plugin Interface

```typescript
import { Plugin, Action, Provider, Evaluator, Service } from "@elizaos/core";

const myPlugin: Plugin = {
  name: "my-plugin",
  description: "Adds custom capabilities to the agent",
  actions: [myAction],
  providers: [myProvider],
  evaluators: [myEvaluator],
  services: [myService],
};

export default myPlugin;
```

### Actions

Actions define what an agent can do. The runtime uses the LLM to decide which action to invoke based on conversation context and the action's examples.

```typescript
import { Action, IAgentRuntime, Memory, State, HandlerCallback } from "@elizaos/core";

const checkPriceAction: Action = {
  name: "CHECK_TOKEN_PRICE",
  description: "Fetches the current price of a cryptocurrency token",
  similes: ["GET_PRICE", "TOKEN_PRICE", "PRICE_CHECK"],
  validate: async (runtime: IAgentRuntime, message: Memory): Promise<boolean> => {
    const text = message.content.text.toLowerCase();
    return text.includes("price") && (text.includes("token") || text.includes("$"));
  },
  handler: async (
    runtime: IAgentRuntime,
    message: Memory,
    state: State,
    options: Record<string, unknown>,
    callback: HandlerCallback
  ): Promise<void> => {
    const tokenSymbol = extractTokenSymbol(message.content.text);
    const price = await fetchPrice(tokenSymbol);
    await callback({
      text: `${tokenSymbol} is currently trading at $${price.usd} (24h change: ${price.change24h}%)`,
    });
  },
  examples: [
    [
      { user: "user1", content: { text: "What's the price of SOL right now?" } },
      { user: "agent", content: { text: "SOL is currently trading at $142.50 (24h change: +3.2%)", action: "CHECK_TOKEN_PRICE" } },
    ],
  ],
};
```

### Providers

Providers inject real-time context into the agent's prompt before each response. They are the agent's sensory system.

```typescript
import { Provider, IAgentRuntime, Memory, State } from "@elizaos/core";

const portfolioProvider: Provider = {
  name: "PORTFOLIO",
  description: "Provides the agent's current wallet balances",
  get: async (runtime: IAgentRuntime, message: Memory, state?: State): Promise<string> => {
    const walletAddress = runtime.getSetting("SOLANA_PUBLIC_KEY");
    if (!walletAddress) return "";
    const balances = await fetchBalances(walletAddress);
    return `Current portfolio:\n${balances.map(b => `- ${b.symbol}: ${b.amount} ($${b.usdValue})`).join("\n")}`;
  },
};
```

### Evaluators

Evaluators run after each response to analyze conversations, extract information, and update agent memory.

```typescript
import { Evaluator, IAgentRuntime, Memory } from "@elizaos/core";

const sentimentEvaluator: Evaluator = {
  name: "SENTIMENT_TRACKER",
  description: "Tracks user sentiment across conversations",
  similes: ["MOOD_TRACKER"],
  validate: async (runtime: IAgentRuntime, message: Memory): Promise<boolean> => {
    return message.content.text.length > 20;
  },
  handler: async (runtime: IAgentRuntime, message: Memory): Promise<void> => {
    const sentiment = await analyzeSentiment(message.content.text);
    await runtime.memoryManager.createMemory({
      userId: message.userId,
      agentId: runtime.agentId,
      roomId: message.roomId,
      content: {
        text: `User sentiment: ${sentiment.label} (${sentiment.score})`,
        metadata: { type: "sentiment", ...sentiment },
      },
    });
  },
  examples: [],
};
```

## Platform Connectors

### Discord

```env
DISCORD_APPLICATION_ID=your_app_id
DISCORD_API_TOKEN=your_bot_token
```

```json
{
  "clients": ["discord"]
}
```

The agent responds in channels where it is mentioned and in DMs. It maintains separate conversation memory per channel (room).

### Telegram

```env
TELEGRAM_BOT_TOKEN=your_bot_token
```

```json
{
  "clients": ["telegram"]
}
```

Supports both group chats and direct messages. In groups, the agent responds when mentioned by name or when directly replied to.

### Twitter

```env
TWITTER_USERNAME=your_username
TWITTER_PASSWORD=your_password
TWITTER_EMAIL=your_email
TWITTER_COOKIES=your_cookies
```

```json
{
  "clients": ["twitter"]
}
```

The agent can post tweets, reply to mentions, and quote retweet. Uses `style.post` for tweet composition.

### Farcaster

```env
FARCASTER_NEYNAR_API_KEY=your_api_key
FARCASTER_NEYNAR_SIGNER_UUID=your_signer_uuid
FARCASTER_FID=your_fid
```

```json
{
  "clients": ["farcaster"]
}
```

## Memory System

elizaOS provides a multi-layer memory system backed by a database adapter (SQLite or PostgreSQL) with vector embedding support for semantic search.

### Memory Types

| Type | Purpose | Persistence |
|------|---------|-------------|
| Conversation | Chat messages per room | Permanent |
| Knowledge | RAG documents and facts | Permanent |
| Description | Agent's understanding of users | Updated over time |
| Facts | Extracted facts from conversations | Permanent |

### Creating Memories

```typescript
await runtime.memoryManager.createMemory({
  userId: message.userId,
  agentId: runtime.agentId,
  roomId: message.roomId,
  content: {
    text: "User is interested in Solana DeFi protocols",
    metadata: { source: "conversation", confidence: 0.9 },
  },
});
```

Embeddings are generated automatically by the runtime when creating memories. No manual embedding step required.

### Searching Memories

```typescript
const relevantMemories = await runtime.memoryManager.getMemories({
  roomId: message.roomId,
  count: 10,
  unique: true,
});

const semanticResults = await runtime.memoryManager.searchMemoriesByEmbedding(
  await runtime.embed("Solana yield farming"),
  {
    roomId: message.roomId,
    match_threshold: 0.8,
    count: 5,
  }
);
```

### RAG Knowledge

Add documents to an agent's knowledge base by placing files in a `knowledge/` directory or programmatically:

```typescript
await runtime.knowledgeManager.createMemory({
  agentId: runtime.agentId,
  content: {
    text: documentContent,
    metadata: { source: "docs", filename: "protocol-overview.md" },
  },
  roomId: "knowledge",
});
```

The runtime chunks documents, generates embeddings, and retrieves relevant chunks when constructing prompts.

### Database Adapters

| Adapter | Package | Use Case |
|---------|---------|----------|
| SQLite | `@elizaos/adapter-sqlite` | Local development, single-agent |
| PostgreSQL | `@elizaos/adapter-postgres` | Production, multi-agent, requires pgvector |

SQLite is the default. For PostgreSQL:

```env
POSTGRES_URL=postgresql://user:password@localhost:5432/eliza
```

The PostgreSQL adapter requires the `pgvector` extension for embedding storage and similarity search.

## Multi-Agent Orchestration

elizaOS supports running multiple agents in a single runtime, each with their own character, memory, and plugin set.

### Worlds and Rooms

- **World**: A server or workspace (e.g., a Discord server, a Telegram group)
- **Room**: A channel or DM within a world

Each agent maintains its own context per room but can be configured to share worlds.

### Running Multiple Agents

```bash
elizaos start --characters characters/analyst.json,characters/trader.json,characters/moderator.json
```

Or programmatically:

```typescript
import { AgentRuntime, defaultCharacter } from "@elizaos/core";
import { SqliteDatabaseAdapter } from "@elizaos/adapter-sqlite";

const db = new SqliteDatabaseAdapter("./data/db.sqlite");

const agents = await Promise.all(
  characters.map(async (character) => {
    const runtime = new AgentRuntime({
      character,
      databaseAdapter: db,
      token: process.env.OPENAI_API_KEY,
      modelProvider: "openai",
      plugins: character.plugins,
    });
    await runtime.initialize();
    return runtime;
  })
);
```

## Solana Integration (plugin-solana)

The `@elizaos/plugin-solana` package provides wallet management, token operations, and DeFi interactions.

### Setup

```bash
bun add @elizaos/plugin-solana
```

```env
SOLANA_PUBLIC_KEY=your_public_key
SOLANA_PRIVATE_KEY=your_private_key
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
BIRDEYE_API_KEY=your_birdeye_key
```

```json
{
  "plugins": ["@elizaos/plugin-solana"]
}
```

### Capabilities

| Action | Description |
|--------|-------------|
| `SEND_TOKEN` | Transfer SPL tokens between wallets |
| `SWAP_TOKEN` | Swap tokens via Jupiter aggregator |
| `STAKE_SOL` | Stake SOL to a validator |
| `CHECK_BALANCE` | Query wallet balances |

### Trust Scoring

The trust engine evaluates transaction safety by combining:

1. **Token performance data** — price history, volume, liquidity depth
2. **Recommender credibility** — track record of addresses that suggested the token
3. **Risk heuristics** — contract age, holder concentration, liquidity locks

```typescript
const trustScore = await runtime.providers.get("TRUST_SCORE");
```

Trust scores range from 0 to 1. Configure minimum thresholds in the character's settings:

```json
{
  "settings": {
    "secrets": {
      "SOLANA_PUBLIC_KEY": "",
      "SOLANA_PRIVATE_KEY": ""
    },
    "trustScoreThreshold": 0.6,
    "maxTransactionAmount": 100
  }
}
```

## Environment Variables

Required and optional environment variables for a full deployment:

```env
# LLM Provider (at least one required)
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GOOGLE_API_KEY=
GROQ_API_KEY=

# Platform Connectors
DISCORD_APPLICATION_ID=
DISCORD_API_TOKEN=
TELEGRAM_BOT_TOKEN=
TWITTER_USERNAME=
TWITTER_PASSWORD=
TWITTER_EMAIL=
FARCASTER_NEYNAR_API_KEY=
FARCASTER_NEYNAR_SIGNER_UUID=

# Solana
SOLANA_PUBLIC_KEY=
SOLANA_PRIVATE_KEY=
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
BIRDEYE_API_KEY=

# Database
POSTGRES_URL=

# Server
SERVER_PORT=3000
```

Never commit `.env` files. Use `.env.example` as a template.

## Project Structure

```
my-agent/
├── characters/
│   └── my-character.json
├── knowledge/
│   └── docs.md
├── plugins/
│   └── my-plugin/
│       ├── src/
│       │   ├── actions/
│       │   ├── providers/
│       │   ├── evaluators/
│       │   └── index.ts
│       └── package.json
├── .env
├── package.json
└── tsconfig.json
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `elizaos create` | Scaffold a new project (interactive) |
| `elizaos create my-agent` | Scaffold with a name |
| `elizaos start` | Start the agent runtime |
| `elizaos start --characters file.json` | Start with specific character(s) |
| `elizaos --version` | Print CLI version |
| `elizaos [command] --help` | Show help for a command |

## Common Patterns

### Dynamic Character Loading

```typescript
import { readFileSync } from "fs";
import { Character } from "@elizaos/core";

function loadCharacter(path: string): Character {
  const raw = readFileSync(path, "utf-8");
  return JSON.parse(raw) as Character;
}

const character = loadCharacter("./characters/my-agent.json");
```

### Custom Service

Services provide long-running background capabilities to plugins (e.g., price feeds, indexers).

```typescript
import { Service, IAgentRuntime, ServiceType } from "@elizaos/core";

class PriceFeedService extends Service {
  static serviceType: ServiceType = "PRICE_FEED" as ServiceType;
  private prices: Map<string, number> = new Map();

  async initialize(runtime: IAgentRuntime): Promise<void> {
    setInterval(async () => {
      const data = await fetchPrices();
      data.forEach((p) => this.prices.set(p.symbol, p.price));
    }, 30_000);
  }

  getPrice(symbol: string): number | undefined {
    return this.prices.get(symbol);
  }
}
```

### Secrets in Character Settings

Store per-agent secrets in the character file's `settings.secrets` — they are not included in prompts:

```json
{
  "settings": {
    "secrets": {
      "SOLANA_PRIVATE_KEY": "",
      "CUSTOM_API_KEY": ""
    }
  }
}
```

Access at runtime:

```typescript
const apiKey = runtime.getSetting("CUSTOM_API_KEY");
```

The runtime checks `settings.secrets` first, then falls back to environment variables.

## Further Reading

- Official docs: https://docs.elizaos.ai
- GitHub: https://github.com/elizaOS/eliza
- Plugin registry: https://docs.elizaos.ai/plugin-registry/overview
- Characters repo: https://github.com/elizaOS/characters
- Plugin starter: https://github.com/elizaOS/eliza-plugin-starter
- arxiv paper: https://arxiv.org/html/2501.06781v1

Last verified: February 2026
