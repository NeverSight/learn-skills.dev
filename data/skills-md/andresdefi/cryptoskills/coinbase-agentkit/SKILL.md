---
name: coinbase-agentkit
description: "Coinbase AgentKit — build AI agents with onchain capabilities. Wallet creation/management, token transfers, swaps, contract deployment, NFT minting, and ENS registration. Framework integrations with LangChain and Vercel AI SDK. Supports Base, Ethereum, Arbitrum, and Polygon."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: AI Agents
tags:
  - coinbase
  - agentkit
  - cdp
  - ai-agents
  - onchain
---

# Coinbase AgentKit

AgentKit is Coinbase's open-source framework for building AI agents with onchain capabilities. It provides wallet management, 50+ built-in actions (transfers, swaps, contract deployment, NFT minting), and integrations with LangChain, Vercel AI SDK, and Model Context Protocol. Framework-agnostic and wallet-agnostic — works with CDP wallets, Viem, Privy, and ZeroDev.

Source: https://github.com/coinbase/agentkit

## What You Probably Got Wrong

> LLMs have stale training data. These are the most common mistakes.

- **`cdp-agentkit-nodejs` is deprecated** → The old `@coinbase/cdp-agentkit-core` and `@coinbase/cdp-langchain` packages are retired. The current package is `@coinbase/agentkit` with framework extensions `@coinbase/agentkit-langchain` and `@coinbase/agentkit-vercel-ai-sdk`. If you see imports from `cdp-agentkit`, you are using the deprecated SDK.
- **"CdpWalletProvider" is the class name** → It was renamed to `CdpEvmWalletProvider` in v0.1+. There is also `CdpSmartWalletProvider` for smart contract wallets and `CdpV2SolanaWalletProvider` for Solana. Using the old name will fail.
- **"AgentKit needs an OpenAI key"** → AgentKit itself is model-agnostic. It creates tools/actions that any LLM framework can call. You only need an OpenAI key if you use LangChain with `ChatOpenAI`. It works equally well with Anthropic, Google, or local models.
- **"npm install agentkit"** → The correct package is `@coinbase/agentkit`. The scoped name is required.
- **Node.js 18 is fine** → AgentKit requires Node.js v22+. Earlier versions will fail silently or throw runtime errors.
- **"AgentKit only works on Base"** → AgentKit supports any EVM network and Solana. Base has the deepest protocol integrations (Basename, Compound, Morpho), but wallet operations work on Ethereum, Arbitrum, Polygon, Optimism, and more.
- **Using `AgentKit.from()` with no config** → Default setup uses `CdpEvmWalletProvider` and requires `CDP_API_KEY_ID` and `CDP_API_KEY_SECRET` environment variables. Without them, initialization throws a cryptic error about missing credentials.
- **Hardcoding private keys** → `ViemWalletProvider` accepts a private key for local testing, but production agents must use `CdpEvmWalletProvider` or `CdpSmartWalletProvider` where keys are managed by CDP infrastructure.

## Installation

```bash
npm install @coinbase/agentkit
```

With LangChain integration:

```bash
npm install @coinbase/agentkit @coinbase/agentkit-langchain @langchain/langgraph @langchain/openai
```

With Vercel AI SDK:

```bash
npm install @coinbase/agentkit @coinbase/agentkit-vercel-ai-sdk ai @ai-sdk/openai
```

Scaffold a complete project:

```bash
npm create onchain-agent@latest
```

### Requirements

- Node.js v22+
- CDP Secret API Key (from https://portal.cdp.coinbase.com)
- TypeScript with `emitDecoratorMetadata: true` in tsconfig (for custom actions)

## CDP API Key Setup

1. Go to https://portal.cdp.coinbase.com
2. Create a project or select an existing one
3. Navigate to API Keys and create a new Secret API Key
4. Save both the Key ID and Key Secret

Set environment variables:

```bash
export CDP_API_KEY_ID="your-key-id"
export CDP_API_KEY_SECRET="your-key-secret"
```

Or use a `.env` file (never commit this):

```
CDP_API_KEY_ID=your-key-id
CDP_API_KEY_SECRET=your-key-secret
```

## Wallet Providers

AgentKit is wallet-agnostic. Choose a provider based on your security and UX requirements.

### CdpEvmWalletProvider

CDP-managed wallets. Keys are stored and signed server-side by Coinbase infrastructure. Best for production agents.

```typescript
import { CdpEvmWalletProvider } from "@coinbase/agentkit";

const wallet = await CdpEvmWalletProvider.configureWithWallet({
  apiKeyId: process.env.CDP_API_KEY_ID,
  apiKeySecret: process.env.CDP_API_KEY_SECRET,
  networkId: "base-sepolia",
});

console.log("Wallet address:", wallet.getAddress());
console.log("Network:", wallet.getNetwork().networkId);
```

Persist and restore wallet state across sessions:

```typescript
const exportedData = wallet.exportWallet();
const serialized = JSON.stringify(exportedData);

const restored = await CdpEvmWalletProvider.configureWithWallet({
  apiKeyId: process.env.CDP_API_KEY_ID,
  apiKeySecret: process.env.CDP_API_KEY_SECRET,
  cdpWalletData: JSON.parse(serialized),
});
```

### CdpSmartWalletProvider

ERC-4337 smart contract wallets with gasless transactions via paymasters. Ideal for agents that need sponsored gas.

```typescript
import { CdpSmartWalletProvider } from "@coinbase/agentkit";

const smartWallet = await CdpSmartWalletProvider.configureWithWallet({
  apiKeyId: process.env.CDP_API_KEY_ID,
  apiKeySecret: process.env.CDP_API_KEY_SECRET,
  networkId: "base-sepolia",
  paymasterUrl: process.env.PAYMASTER_URL,
});
```

### ViemWalletProvider

Use any viem-compatible wallet. Useful for local development and testing where you control the private key.

```typescript
import { ViemWalletProvider } from "@coinbase/agentkit";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { baseSepolia } from "viem/chains";

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const client = createWalletClient({
  account,
  chain: baseSepolia,
  transport: http(),
});

const wallet = new ViemWalletProvider(client);
```

### PrivyWalletProvider

Privy server wallets for applications that already use Privy for auth.

```typescript
import { PrivyWalletProvider } from "@coinbase/agentkit";

const wallet = await PrivyWalletProvider.configureWithWallet({
  appId: process.env.PRIVY_APP_ID,
  appSecret: process.env.PRIVY_APP_SECRET,
  networkId: "base-sepolia",
});
```

## Core: AgentKit Initialization

```typescript
import { AgentKit } from "@coinbase/agentkit";

const agentKit = await AgentKit.from({
  walletProvider: wallet,
  actionProviders: [
    walletActionProvider(),
    erc20ActionProvider(),
    cdpApiActionProvider({
      apiKeyId: process.env.CDP_API_KEY_ID,
      apiKeySecret: process.env.CDP_API_KEY_SECRET,
    }),
  ],
});
```

If no `walletProvider` or `actionProviders` are specified, AgentKit defaults to `CdpEvmWalletProvider` with `walletActionProvider`.

## Action Providers

Action providers define what an agent can do onchain. Each provider groups related actions.

### Wallet Actions

```typescript
import { walletActionProvider } from "@coinbase/agentkit";

const actions = walletActionProvider();
```

Provides: `getBalance`, `getWalletDetails`, `nativeTransfer`

### ERC20 Token Actions

```typescript
import { erc20ActionProvider } from "@coinbase/agentkit";

const actions = erc20ActionProvider();
```

Provides: `getBalance`, `transfer`, `approve`, `getAllowance`

### ERC721 NFT Actions

```typescript
import { erc721ActionProvider } from "@coinbase/agentkit";

const actions = erc721ActionProvider();
```

Provides: `mint`, `transfer`, `getBalance`

### WETH Actions

```typescript
import { wethActionProvider } from "@coinbase/agentkit";

const actions = wethActionProvider();
```

Provides: `wrapEth` (ETH to WETH)

### CDP API Actions

Requires CDP API credentials. Provides access to Coinbase's swap and faucet APIs.

```typescript
import { cdpApiActionProvider } from "@coinbase/agentkit";

const actions = cdpApiActionProvider({
  apiKeyId: process.env.CDP_API_KEY_ID,
  apiKeySecret: process.env.CDP_API_KEY_SECRET,
});
```

Provides: `requestFaucet`, `tradeTokens` (swap via CDP API)

### Compound Actions

```typescript
import { compoundActionProvider } from "@coinbase/agentkit";

const actions = compoundActionProvider();
```

Provides: `supply`, `withdraw`, `borrow`, `repay`, `getPortfolio`

### Morpho Actions

```typescript
import { morphoActionProvider } from "@coinbase/agentkit";

const actions = morphoActionProvider();
```

Provides: `deposit`, `withdraw`

### Pyth Price Feed Actions

```typescript
import { pythActionProvider } from "@coinbase/agentkit";

const actions = pythActionProvider();
```

Provides: `fetchPrice` (real-time price data from Pyth oracles)

### Basename Actions

Register and manage Base names (ENS equivalent on Base).

```typescript
import { basenameActionProvider } from "@coinbase/agentkit";

const actions = basenameActionProvider();
```

Provides: `registerBasename`

### Social Actions

```typescript
import { twitterActionProvider } from "@coinbase/agentkit";
import { farcasterActionProvider } from "@coinbase/agentkit";

const twitter = twitterActionProvider();
const farcaster = farcasterActionProvider();
```

Twitter provides: `postTweet`, `getAccountDetails`
Farcaster provides: `postCast`, `getAccountDetails`

### Additional Providers

| Provider | Actions |
|----------|---------|
| `openseaActionProvider` | `listNft`, `getNftBalance` |
| `superfluidActionProvider` | `createFlow`, `updateFlow`, `deleteFlow` |
| `moonwellActionProvider` | `supply`, `withdraw`, `borrow`, `repay` |
| `acrossActionProvider` | `bridgeTokens` (cross-chain bridge) |
| `defiLlamaActionProvider` | `getProtocolTvl`, `getProtocolList` |
| `jupiterActionProvider` | `swap` (Solana DEX aggregator) |
| `zeroXActionProvider` | `getQuote`, `swap` (0x aggregator) |
| `zoraActionProvider` | `createToken`, `mint` |
| `clankerActionProvider` | `deployToken` (Farcaster token deployment) |
| `wowActionProvider` | `createMemecoin`, `buyMemecoin`, `sellMemecoin` |
| `ensoActionProvider` | `routeSwap` |
| `fluidActionProvider` | `lend`, `borrow` |

## LangChain Integration

The most common integration pattern. Converts AgentKit actions into LangChain tools.

```typescript
import { AgentKit } from "@coinbase/agentkit";
import { getLangChainTools } from "@coinbase/agentkit-langchain";
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { MemorySaver } from "@langchain/langgraph";

const agentKit = await AgentKit.from({
  walletProvider: wallet,
  actionProviders: [
    walletActionProvider(),
    erc20ActionProvider(),
    cdpApiActionProvider({
      apiKeyId: process.env.CDP_API_KEY_ID,
      apiKeySecret: process.env.CDP_API_KEY_SECRET,
    }),
  ],
});

const tools = await getLangChainTools(agentKit);

const llm = new ChatOpenAI({ model: "gpt-4o" });
const memory = new MemorySaver();

const agent = createReactAgent({
  llm,
  tools,
  checkpointSaver: memory,
});

const result = await agent.invoke(
  { messages: [{ role: "user", content: "What is my wallet address?" }] },
  { configurable: { thread_id: "session-1" } }
);
```

## Vercel AI SDK Integration

```typescript
import { AgentKit } from "@coinbase/agentkit";
import { getVercelAITools } from "@coinbase/agentkit-vercel-ai-sdk";
import { openai } from "@ai-sdk/openai";
import { generateText } from "ai";

const agentKit = await AgentKit.from({ walletProvider: wallet });
const tools = await getVercelAITools(agentKit);

const { text } = await generateText({
  model: openai("gpt-4o"),
  tools,
  prompt: "Get my wallet balance on Base Sepolia",
  maxSteps: 5,
});
```

## Model Context Protocol (MCP)

AgentKit can run as an MCP server, exposing actions to any MCP-compatible client.

```bash
npm install @coinbase/agentkit-model-context-protocol
```

```typescript
import { AgentKit } from "@coinbase/agentkit";
import { getMcpTools } from "@coinbase/agentkit-model-context-protocol";

const agentKit = await AgentKit.from({ walletProvider: wallet });
const server = getMcpTools(agentKit);
server.listen();
```

## Custom Action Providers

Create domain-specific actions by extending `ActionProvider`.

Requires `emitDecoratorMetadata: true` in your `tsconfig.json`:

```json
{
  "compilerOptions": {
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true
  }
}
```

Define a custom action:

```typescript
import {
  ActionProvider,
  WalletProvider,
  Network,
  CreateAction,
} from "@coinbase/agentkit";
import { z } from "zod";

const CheckPriceSchema = z.object({
  tokenSymbol: z.string().describe("Token symbol to check price for"),
});

class PriceCheckerProvider extends ActionProvider<WalletProvider> {
  constructor() {
    super("price-checker", []);
  }

  @CreateAction({
    name: "check_price",
    description: "Check the current USD price of a token",
    schema: CheckPriceSchema,
  })
  async checkPrice(
    walletProvider: WalletProvider,
    params: z.infer<typeof CheckPriceSchema>
  ): Promise<string> {
    const response = await fetch(
      `https://api.coingecko.com/api/v3/simple/price?ids=${params.tokenSymbol}&vs_currencies=usd`
    );
    const data = await response.json();
    return JSON.stringify(data);
  }

  supportsNetwork(_network: Network): boolean {
    return true;
  }
}

export const priceCheckerProvider = () => new PriceCheckerProvider();
```

Register with AgentKit:

```typescript
const agentKit = await AgentKit.from({
  walletProvider: wallet,
  actionProviders: [
    walletActionProvider(),
    priceCheckerProvider(),
  ],
});
```

## Network Configuration

### Switching Networks

```typescript
const wallet = await CdpEvmWalletProvider.configureWithWallet({
  apiKeyId: process.env.CDP_API_KEY_ID,
  apiKeySecret: process.env.CDP_API_KEY_SECRET,
  networkId: "base-mainnet",
});
```

### Common Network IDs

| Network | ID |
|---------|-----|
| Base Mainnet | `base-mainnet` |
| Base Sepolia | `base-sepolia` |
| Ethereum Mainnet | `ethereum-mainnet` |
| Ethereum Sepolia | `ethereum-sepolia` |
| Arbitrum Mainnet | `arbitrum-mainnet` |
| Polygon Mainnet | `polygon-mainnet` |
| Solana Mainnet | `solana-mainnet` |
| Solana Devnet | `solana-devnet` |

### Custom RPC (ViemWalletProvider)

```typescript
import { defineChain } from "viem";

const customChain = defineChain({
  id: 84532,
  name: "Base Sepolia",
  nativeCurrency: { name: "ETH", symbol: "ETH", decimals: 18 },
  rpcUrls: {
    default: { http: ["https://your-rpc-url.com"] },
  },
});

const client = createWalletClient({
  account,
  chain: customChain,
  transport: http("https://your-rpc-url.com"),
});
```

## Security Model

### API Key Scoping

CDP API keys can be scoped to specific actions. In the CDP portal:
- Create separate keys for testnet vs mainnet
- Limit spending per key with rate limits
- Rotate keys regularly — old keys can be revoked instantly

### Wallet Export

CDP wallets can export private keys for migration, but this should be rare:

```typescript
const exportedWallet = wallet.exportWallet();
```

Once exported, the key material leaves CDP infrastructure. Handle with extreme care.

### Production Checklist

1. Use `CdpEvmWalletProvider` or `CdpSmartWalletProvider` (not Viem with raw keys)
2. Set spending limits on CDP API keys
3. Use separate API keys for testnet and mainnet
4. Store `CDP_API_KEY_SECRET` in a secrets manager (not `.env` in production)
5. Enable webhook notifications for wallet activity
6. Implement transaction approval logic before signing high-value transactions
7. Use `CdpSmartWalletProvider` with paymasters for gasless UX

## Testnet Faucet

Request testnet tokens via the CDP faucet action:

```typescript
import { cdpApiActionProvider } from "@coinbase/agentkit";

const cdpActions = cdpApiActionProvider({
  apiKeyId: process.env.CDP_API_KEY_ID,
  apiKeySecret: process.env.CDP_API_KEY_SECRET,
});
```

The `requestFaucet` action is available on Base Sepolia and Ethereum Sepolia.

## Quickstart: Scaffold a New Agent

The fastest way to start:

```bash
npm create onchain-agent@latest
cd my-onchain-agent
cp .env.example .env
# Fill in CDP_API_KEY_ID, CDP_API_KEY_SECRET, OPENAI_API_KEY
npm install
npm run dev
```

This creates a chatbot agent with wallet access, token operations, and LangChain integration out of the box.

## Common Patterns

### Check Balance Before Transfer

```typescript
const agentKit = await AgentKit.from({
  walletProvider: wallet,
  actionProviders: [walletActionProvider(), erc20ActionProvider()],
});

const tools = await getLangChainTools(agentKit);
const agent = createReactAgent({ llm, tools });

const result = await agent.invoke({
  messages: [{
    role: "user",
    content: "Check my ETH balance, and if I have more than 0.01 ETH, send 0.005 ETH to 0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
  }],
});
```

### Multi-Action Agent

```typescript
const agentKit = await AgentKit.from({
  walletProvider: wallet,
  actionProviders: [
    walletActionProvider(),
    erc20ActionProvider(),
    erc721ActionProvider(),
    wethActionProvider(),
    cdpApiActionProvider({
      apiKeyId: process.env.CDP_API_KEY_ID,
      apiKeySecret: process.env.CDP_API_KEY_SECRET,
    }),
    compoundActionProvider(),
    pythActionProvider(),
    basenameActionProvider(),
  ],
});
```

## Version History

| Version | Change |
|---------|--------|
| 0.2.x | Added Solana support, ZeroDev, Privy providers |
| 0.1.x | New architecture: `CdpEvmWalletProvider`, action provider system, framework extensions |
| Pre-0.1 | Legacy `@coinbase/cdp-agentkit-core` (deprecated) |

Last verified: February 2026 against `@coinbase/agentkit` v0.2.x
