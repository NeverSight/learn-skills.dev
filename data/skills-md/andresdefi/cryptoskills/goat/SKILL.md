---
name: goat
description: "GOAT (Great Onchain Agent Toolkit) — 200+ protocol integrations across 30+ chains. Tool creation, framework adapters (AI SDK/LangChain/Eliza), DeFi actions (swap/bridge/transfer), wallet management, and modular plugin architecture for building onchain AI agents."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: AI Agents
tags:
  - goat
  - onchain-agent
  - ai-agents
  - defi
  - multichain
---

# GOAT (Great Onchain Agent Toolkit)

GOAT is the leading open-source framework for connecting AI agents to onchain protocols. It provides 200+ protocol integrations across 30+ chains with adapters for every major agent framework — Vercel AI SDK, LangChain, LlamaIndex, Eliza, MCP, and more. Agents get wallets, trade tokens, interact with DeFi protocols, bridge cross-chain, and execute arbitrary smart contract calls through a modular plugin architecture. MIT licensed, sponsored by Crossmint, but fully provider-agnostic.

Source: https://github.com/goat-sdk/goat

## What You Probably Got Wrong

> LLMs have stale training data. These are the most common mistakes.

- **"Import from `goat-sdk`"** → The npm scope is `@goat-sdk/*`. Every package lives under this scope: `@goat-sdk/core`, `@goat-sdk/adapter-vercel-ai`, `@goat-sdk/plugin-erc20`, etc. There is no single `goat-sdk` package.
- **"Install one package for everything"** → GOAT is modular by design. You install only what you need: a core package, one adapter for your framework, one wallet provider, and the specific plugins for protocols you want. A minimal setup needs 3-4 packages, not one.
- **`getTools()` is synchronous** → `getOnChainTools()` from the adapter packages is `async` and must be `await`ed. Missing `await` gives you a Promise instead of tools, and your agent silently has zero capabilities.
- **"GOAT only supports EVM"** → GOAT supports EVM, Solana, Aptos, Chromia, Cosmos, Fuel, Sui, Starknet, Zilliqa, Radix, Zetrix, and Lit. Plugin chain-specificity is declared via `supportsChain()`.
- **"Use the same wallet for all chains"** → Each chain has its own wallet provider. EVM uses `@goat-sdk/wallet-viem`, Solana uses `@goat-sdk/wallet-solana`, Crossmint smart wallets use `@goat-sdk/wallet-crossmint`. You cannot pass a viem wallet to a Solana plugin.
- **"Plugins are functions"** → Plugins are class instances. The convention is a factory function (e.g., `erc20()`, `uniswap()`) that returns a `new PluginBase` subclass. Call the factory; do not pass the class directly.
- **Old `@ai16z/plugin-goat` package** → The Eliza integration moved to `@elizaos/plugin-goat`. The `@ai16z` scope is deprecated.
- **"GOAT handles transaction signing"** → GOAT delegates signing to the wallet provider. You must configure the wallet client (viem, Crossmint, keypair) with the appropriate private key or signer. GOAT orchestrates tool calls; the wallet signs.
- **Missing `maxSteps` in Vercel AI SDK** → When using `generateText` or `streamText`, you must set `maxSteps` (e.g., 10) so the model can make multiple tool calls. Without it, the agent makes one call and stops.

## Installation

### Core + Vercel AI SDK (EVM)

```bash
npm install @goat-sdk/core @goat-sdk/adapter-vercel-ai @goat-sdk/wallet-viem @goat-sdk/plugin-erc20
```

### Core + LangChain (EVM)

```bash
npm install @goat-sdk/core @goat-sdk/adapter-langchain @goat-sdk/wallet-viem @goat-sdk/plugin-erc20
```

### Core + Vercel AI SDK (Solana)

```bash
npm install @goat-sdk/core @goat-sdk/adapter-vercel-ai @goat-sdk/wallet-solana @goat-sdk/plugin-spl-token
```

### Core + MCP

```bash
npm install @goat-sdk/core @goat-sdk/adapter-model-context-protocol @goat-sdk/wallet-viem
```

### Additional Plugins

Install per-protocol as needed:

```bash
npm install @goat-sdk/plugin-uniswap @goat-sdk/plugin-jupiter @goat-sdk/plugin-polymarket
```

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Agent Framework                    │
│  (Vercel AI SDK / LangChain / Eliza / MCP / etc.)  │
├─────────────────────────────────────────────────────┤
│                     Adapter Layer                    │
│  @goat-sdk/adapter-vercel-ai                        │
│  @goat-sdk/adapter-langchain                        │
│  @goat-sdk/adapter-model-context-protocol           │
├─────────────────────────────────────────────────────┤
│                     @goat-sdk/core                   │
│  getTools() · createTool() · PluginBase             │
├──────────────────┬──────────────────────────────────┤
│  Wallet Providers │         Plugins                  │
│  wallet-viem      │  plugin-erc20                    │
│  wallet-solana    │  plugin-uniswap                  │
│  wallet-crossmint │  plugin-jupiter                  │
│  wallet-aptos     │  plugin-polymarket               │
│  wallet-sui       │  plugin-debridge                 │
│  wallet-cosmos    │  plugin-1inch                    │
│  ...              │  ... (200+ total)                │
└──────────────────┴──────────────────────────────────┘
```

## Quick Start: Vercel AI SDK + EVM

```typescript
import { openai } from "@ai-sdk/openai";
import { generateText } from "ai";
import { getOnChainTools } from "@goat-sdk/adapter-vercel-ai";
import { erc20 } from "@goat-sdk/plugin-erc20";
import { sendETH } from "@goat-sdk/plugin-send-eth";
import { viem } from "@goat-sdk/wallet-viem";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const account = privateKeyToAccount(process.env.WALLET_PRIVATE_KEY as `0x${string}`);

const walletClient = createWalletClient({
  account,
  chain: base,
  transport: http(process.env.RPC_URL),
});

const tools = await getOnChainTools({
  wallet: viem(walletClient),
  plugins: [
    sendETH(),
    erc20({
      tokens: [
        {
          name: "USDC",
          symbol: "USDC",
          decimals: 6,
          chains: {
            8453: { contractAddress: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913" },
          },
        },
      ],
    }),
  ],
});

const result = await generateText({
  model: openai("gpt-4o"),
  tools,
  maxSteps: 10,
  prompt: "Send 5 USDC to 0xRecipient...",
});

console.log(result.text);
```

## Quick Start: LangChain + EVM

```typescript
import { ChatOpenAI } from "@langchain/openai";
import { AgentExecutor, createOpenAIFunctionsAgent } from "langchain/agents";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { getOnChainTools } from "@goat-sdk/adapter-langchain";
import { sendETH } from "@goat-sdk/plugin-send-eth";
import { erc20 } from "@goat-sdk/plugin-erc20";
import { viem } from "@goat-sdk/wallet-viem";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const account = privateKeyToAccount(process.env.WALLET_PRIVATE_KEY as `0x${string}`);

const walletClient = createWalletClient({
  account,
  chain: base,
  transport: http(process.env.RPC_URL),
});

const tools = await getOnChainTools({
  wallet: viem(walletClient),
  plugins: [sendETH(), erc20()],
});

const prompt = ChatPromptTemplate.fromMessages([
  ["system", "You are a helpful onchain assistant."],
  ["human", "{input}"],
  ["placeholder", "{agent_scratchpad}"],
]);

const llm = new ChatOpenAI({ model: "gpt-4o" });
const agent = await createOpenAIFunctionsAgent({ llm, tools, prompt });
const executor = new AgentExecutor({ agent, tools });

const response = await executor.invoke({
  input: "What is my ETH balance?",
});
```

## Quick Start: Solana

```typescript
import { openai } from "@ai-sdk/openai";
import { generateText } from "ai";
import { getOnChainTools } from "@goat-sdk/adapter-vercel-ai";
import { solana } from "@goat-sdk/wallet-solana";
import { sendSOL } from "@goat-sdk/plugin-send-solana";
import { splToken } from "@goat-sdk/plugin-spl-token";
import { jupiter } from "@goat-sdk/plugin-jupiter";
import { Connection, Keypair } from "@solana/web3.js";
import bs58 from "bs58";

const keypair = Keypair.fromSecretKey(bs58.decode(process.env.SOLANA_PRIVATE_KEY as string));
const connection = new Connection(process.env.SOLANA_RPC_URL as string);

const tools = await getOnChainTools({
  wallet: solana({ keypair, connection }),
  plugins: [sendSOL(), splToken(), jupiter()],
});

const result = await generateText({
  model: openai("gpt-4o"),
  tools,
  maxSteps: 10,
  prompt: "Swap 1 SOL for USDC on Jupiter",
});
```

## Crossmint Smart Wallets

Crossmint smart wallets provide custodial wallet infrastructure without requiring users to manage private keys.

```typescript
import { getOnChainTools } from "@goat-sdk/adapter-vercel-ai";
import { crossmint } from "@goat-sdk/wallet-crossmint";
import { erc20 } from "@goat-sdk/plugin-erc20";

const tools = await getOnChainTools({
  wallet: crossmint({
    apiKey: process.env.CROSSMINT_API_KEY as string,
    walletAddress: process.env.CROSSMINT_WALLET_ADDRESS as string,
    chain: "base-sepolia",
  }),
  plugins: [erc20()],
});
```

## Plugin System

### Using Plugins

Every plugin is a factory function that returns a `PluginBase` instance:

```typescript
import { sendETH } from "@goat-sdk/plugin-send-eth";
import { erc20 } from "@goat-sdk/plugin-erc20";
import { uniswap } from "@goat-sdk/plugin-uniswap";
import { polymarket } from "@goat-sdk/plugin-polymarket";

const tools = await getOnChainTools({
  wallet: viem(walletClient),
  plugins: [
    sendETH(),
    erc20({ tokens: [USDC, WETH] }),
    uniswap(),
    polymarket(),
  ],
});
```

### Creating a Custom Plugin (Decorator Pattern)

```typescript
import { PluginBase, Tool, createToolParameters } from "@goat-sdk/core";
import type { WalletClientBase, Chain } from "@goat-sdk/core";
import { z } from "zod";

class GetPriceParameters extends createToolParameters(
  z.object({
    tokenAddress: z.string().describe("The token contract address"),
  })
) {}

class PriceFeedTools {
  @Tool({
    name: "get_token_price",
    description: "Get the current USD price of a token by its contract address",
  })
  async getTokenPrice(
    walletClient: WalletClientBase,
    parameters: GetPriceParameters
  ): Promise<string> {
    const response = await fetch(
      `https://api.coingecko.com/api/v3/simple/token_price/ethereum?contract_addresses=${parameters.tokenAddress}&vs_currencies=usd`
    );
    const data = await response.json();
    const price = data[parameters.tokenAddress.toLowerCase()]?.usd;
    if (!price) throw new Error(`Price not found for ${parameters.tokenAddress}`);
    return `$${price}`;
  }
}

export class PriceFeedPlugin extends PluginBase<WalletClientBase> {
  constructor() {
    super("priceFeed", [new PriceFeedTools()]);
  }

  supportsChain = (chain: Chain) => chain.type === "evm";
}

export const priceFeed = () => new PriceFeedPlugin();
```

### Creating a Custom Plugin (createTool Pattern)

```typescript
import { PluginBase, createTool } from "@goat-sdk/core";
import type { WalletClientBase, Chain } from "@goat-sdk/core";
import { z } from "zod";

export class TimestampPlugin extends PluginBase<WalletClientBase> {
  constructor() {
    super("timestamp", []);
  }

  supportsChain = (chain: Chain) => true;

  getTools(walletClient: WalletClientBase) {
    return [
      createTool(
        {
          name: "get_block_timestamp",
          description: "Get the timestamp of the latest block",
          parameters: z.object({}),
        },
        async () => {
          const address = await walletClient.getAddress();
          return `Wallet ${address} queried at ${Date.now()}`;
        }
      ),
    ];
  }
}

export const timestamp = () => new TimestampPlugin();
```

### Plugin Scaffolding CLI

```bash
pnpm create-plugin -n my-protocol
pnpm create-plugin -n my-protocol -t evm
pnpm create-plugin -n my-protocol -t solana
```

This generates the directory structure with `package.json`, TypeScript config, parameter schemas, service class, and plugin class.

## EVM-Specific Plugins

### Token Transfers

```typescript
import { sendETH } from "@goat-sdk/plugin-send-eth";
import { erc20 } from "@goat-sdk/plugin-erc20";

const tools = await getOnChainTools({
  wallet: viem(walletClient),
  plugins: [
    sendETH(),
    erc20({
      tokens: [
        {
          name: "USDC",
          symbol: "USDC",
          decimals: 6,
          chains: {
            1: { contractAddress: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48" },
            8453: { contractAddress: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913" },
          },
        },
      ],
    }),
  ],
});
```

### DEX Swaps

```typescript
import { uniswap } from "@goat-sdk/plugin-uniswap";
import { oneinch } from "@goat-sdk/plugin-1inch";

const tools = await getOnChainTools({
  wallet: viem(walletClient),
  plugins: [uniswap(), oneinch()],
});
```

### Cross-Chain Bridging

```typescript
import { debridge } from "@goat-sdk/plugin-debridge";

const tools = await getOnChainTools({
  wallet: viem(walletClient),
  plugins: [debridge()],
});
```

## Solana-Specific Plugins

```typescript
import { sendSOL } from "@goat-sdk/plugin-send-solana";
import { splToken } from "@goat-sdk/plugin-spl-token";
import { jupiter } from "@goat-sdk/plugin-jupiter";
import { orca } from "@goat-sdk/plugin-orca";
import { meteora } from "@goat-sdk/plugin-meteora";
import { pumpfun } from "@goat-sdk/plugin-pump-fun";

const tools = await getOnChainTools({
  wallet: solana({ keypair, connection }),
  plugins: [sendSOL(), splToken(), jupiter(), orca(), meteora(), pumpfun()],
});
```

## MCP (Model Context Protocol) Adapter

The MCP adapter exposes GOAT tools as an MCP server, making them available to any MCP-compatible client (Claude Desktop, Cursor, etc.).

```typescript
import { createMCPServer } from "@goat-sdk/adapter-model-context-protocol";
import { viem } from "@goat-sdk/wallet-viem";
import { sendETH } from "@goat-sdk/plugin-send-eth";
import { erc20 } from "@goat-sdk/plugin-erc20";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";

const account = privateKeyToAccount(process.env.WALLET_PRIVATE_KEY as `0x${string}`);

const walletClient = createWalletClient({
  account,
  chain: base,
  transport: http(process.env.RPC_URL),
});

const server = await createMCPServer({
  wallet: viem(walletClient),
  plugins: [sendETH(), erc20()],
});

server.listen();
```

## Eliza Integration

```typescript
import { goatPlugin } from "@elizaos/plugin-goat";
import { erc20 } from "@goat-sdk/plugin-erc20";
import { sendETH } from "@goat-sdk/plugin-send-eth";

const character = {
  plugins: [
    goatPlugin({
      plugins: [sendETH(), erc20()],
      wallet: {
        provider: "viem",
        chain: "base",
      },
    }),
  ],
};
```

## Framework Adapters Reference

| Framework | Package | Language |
|-----------|---------|----------|
| Vercel AI SDK | `@goat-sdk/adapter-vercel-ai` | TypeScript |
| LangChain | `@goat-sdk/adapter-langchain` | TypeScript |
| LlamaIndex | `@goat-sdk/adapter-llamaindex` | TypeScript |
| Model Context Protocol | `@goat-sdk/adapter-model-context-protocol` | TypeScript |
| ElevenLabs | `@goat-sdk/adapter-eleven-labs` | TypeScript |
| Mastra | `@goat-sdk/adapter-mastra` | TypeScript |
| Eliza | `@elizaos/plugin-goat` | TypeScript |
| GAME | `@goat-sdk/adapter-game` | TypeScript |
| OpenAI Agents SDK | `goat-sdk-adapter-openai` | Python |
| LangChain (Python) | `goat-sdk-adapter-langchain` | Python |
| CrewAI | `goat-sdk-adapter-crewai` | Python |
| AG2 | `goat-sdk-adapter-ag2` | Python |
| Smolagents | `goat-sdk-adapter-smolagents` | Python |
| ZerePy | `goat-sdk-adapter-zerepy` | Python |

## Wallet Providers Reference

| Chain | Package | Wallet Type |
|-------|---------|-------------|
| EVM (all chains) | `@goat-sdk/wallet-viem` | Key pair via viem |
| EVM (Safe multisig) | `@goat-sdk/wallet-safe` | Gnosis Safe |
| Solana | `@goat-sdk/wallet-solana` | Keypair |
| Crossmint (EVM + Solana) | `@goat-sdk/wallet-crossmint` | Smart wallet |
| Aptos | `@goat-sdk/wallet-aptos` | Key pair |
| Chromia | `@goat-sdk/wallet-chromia` | Key pair |
| Cosmos | `@goat-sdk/wallet-cosmos` | Key pair |
| Fuel | `@goat-sdk/wallet-fuel` | Key pair |
| Lit Protocol | `@goat-sdk/wallet-lit` | PKP wallet |
| Radix | `@goat-sdk/wallet-radix` | Key pair |
| Starknet | `@goat-sdk/wallet-starknet` | Key pair |
| Sui | `@goat-sdk/wallet-sui` | Key pair |
| Zetrix | `@goat-sdk/wallet-zetrix` | Key pair |
| Zilliqa | `@goat-sdk/wallet-zilliqa` | Key pair |

## Key Interfaces

### WalletClientBase

Chain-agnostic base class. All wallet providers extend this:

```typescript
abstract class WalletClientBase {
  abstract getAddress(): string;
  abstract getChain(): Chain;
  abstract signMessage(message: string): Promise<{ signedMessage: string }>;
  abstract balanceOf(address: string): Promise<{ value: bigint; symbol: string; decimals: number }>;
}
```

### EVMWalletClient

Extends `WalletClientBase` with EVM-specific capabilities:

```typescript
abstract class EVMWalletClient extends WalletClientBase {
  abstract sendTransaction(tx: EVMTransaction): Promise<{ hash: string }>;
  abstract read(query: EVMReadQuery): Promise<EVMReadResult>;
}
```

### SolanaWalletClient

Extends `WalletClientBase` with Solana-specific capabilities:

```typescript
abstract class SolanaWalletClient extends WalletClientBase {
  abstract sendTransaction(tx: SolanaTransaction): Promise<{ hash: string }>;
}
```

## Token Configuration

Define tokens once, use across chains:

```typescript
const USDC = {
  name: "USD Coin",
  symbol: "USDC",
  decimals: 6,
  chains: {
    1: { contractAddress: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48" },
    8453: { contractAddress: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913" },
    42161: { contractAddress: "0xaf88d065e77c8cC2239327C5EDb3A432268e5831" },
    10: { contractAddress: "0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85" },
    137: { contractAddress: "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359" },
  },
};

const WETH = {
  name: "Wrapped Ether",
  symbol: "WETH",
  decimals: 18,
  chains: {
    8453: { contractAddress: "0x4200000000000000000000000000000000000006" },
    42161: { contractAddress: "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1" },
    10: { contractAddress: "0x4200000000000000000000000000000000000006" },
  },
};
```

## Error Handling

GOAT errors propagate from the underlying wallet or protocol. Wrap tool execution:

```typescript
const result = await generateText({
  model: openai("gpt-4o"),
  tools,
  maxSteps: 10,
  prompt: userMessage,
  onStepFinish: ({ toolResults }) => {
    for (const result of toolResults ?? []) {
      if (result.type === "tool-result" && result.result?.error) {
        console.error(`Tool ${result.toolName} failed:`, result.result.error);
      }
    }
  },
});
```

## Environment Variables

```bash
# Required: wallet key (NEVER hardcode)
WALLET_PRIVATE_KEY=0x...
RPC_URL=https://mainnet.base.org

# Solana
SOLANA_PRIVATE_KEY=base58_encoded_key
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com

# Crossmint
CROSSMINT_API_KEY=your_api_key
CROSSMINT_WALLET_ADDRESS=0x...

# LLM provider
OPENAI_API_KEY=sk-...
```

## Python SDK

GOAT also ships a Python SDK with equivalent adapters:

```bash
pip install goat-sdk goat-sdk-adapter-langchain goat-sdk-plugin-erc20 goat-sdk-wallet-viem
```

```python
from goat_adapters.langchain import get_on_chain_tools
from goat_plugins.erc20 import erc20
from goat_plugins.send_eth import send_eth
from goat_wallets.viem import viem

tools = get_on_chain_tools(
    wallet=viem(wallet_client),
    plugins=[send_eth(), erc20()],
)
```

## Best Practices

1. **Install only needed plugins** — each plugin adds tools to the agent's context window. More plugins = more tokens = slower and more expensive.
2. **Set `maxSteps`** — without it, Vercel AI SDK agents make exactly one tool call. Set to 5-15 depending on task complexity.
3. **Use testnet first** — always test with Base Sepolia, Sepolia, or Solana Devnet before pointing at mainnet.
4. **Token decimals matter** — USDC has 6 decimals, ETH has 18. Misconfigured decimals send wrong amounts. Always verify the `decimals` field in token configs.
5. **Rate limit RPC calls** — agents can issue dozens of reads per prompt. Use a paid RPC endpoint or implement caching.
6. **Guard against prompt injection** — an agent with a wallet is an economic actor. Validate user inputs, set spending limits, and require confirmation for large transactions.
7. **Log all tool calls** — use `onStepFinish` (Vercel AI SDK) or equivalent callbacks to log every tool invocation for audit trails.
8. **Pin plugin versions** — GOAT moves fast. Pin exact versions in `package.json` to avoid breaking changes.

Last verified: February 2026
