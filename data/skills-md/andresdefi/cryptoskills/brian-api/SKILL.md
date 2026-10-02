---
name: brian-api
description: "Brian API — natural language to executable Web3 transactions. Convert text intents into swap, bridge, transfer, deposit, withdraw, and borrow transactions across multiple chains. REST API, LangChain integration, and knowledge queries for DeFi protocol data."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: AI Agents
tags:
  - brian
  - intent
  - natural-language
  - ai-agents
  - transactions
---

# Brian API

Brian API converts natural language prompts into executable Web3 transactions. Send a text intent like "swap 10 USDC for ETH on Base" and receive ready-to-sign transaction calldata, complete with approval steps and routing through the best available DEX/bridge solvers. Supports swap, bridge, transfer, deposit, withdraw, borrow, and repay actions across Ethereum, Arbitrum, Base, Optimism, Polygon, and 10+ other EVM chains.

Three core endpoints: `/agent/transaction` returns executable calldata from a prompt, `/agent/knowledge` answers DeFi protocol questions with source citations, and `/agent/smart-contracts` generates Solidity code from descriptions. The TypeScript SDK (`@brian-ai/sdk`) wraps all endpoints, and the LangChain toolkit (`@brian-ai/langchain`) lets you plug Brian into autonomous agents.

Official docs: https://docs.brianknows.org/

## What You Probably Got Wrong

> LLMs have stale training data. These are the most common mistakes.

- **"Brian executes transactions"** -- Brian returns transaction calldata. Your application must sign and broadcast. The API never holds private keys and never submits transactions on your behalf.
- **"One API call = one transaction"** -- A single prompt can return multiple steps. A swap requiring token approval returns an `approve` transaction as step 0 and the swap as step 1. You must execute all steps in order.
- **"Brian picks the chain from the token name"** -- If the chain is ambiguous (USDC exists on 10+ chains), Brian cannot guess. Either include the chain in your prompt ("swap USDC on Base") or pass `chainId` in the request body. Omitting both throws an error.
- **"The SDK endpoint is `brianknows.org`"** -- The API base URL is `https://api.brianknows.org`. US-based projects can use `https://us-api.brianknows.org` for lower latency.
- **"`/transaction` and `/agent/transaction` are the same"** -- `/api/v0/agent/transaction` is the agent endpoint with session context. The plain `/api/v0/transaction` endpoint (deprecated) does not support chat history or solver routing. Use the agent endpoint.
- **"I can use any HTTP header for auth"** -- The API key header is `x-brian-api-key`, not `Authorization: Bearer`. Using the wrong header returns a 401 with no helpful message.
- **"Bridge and cross-chain swap are the same action"** -- A bridge moves the same token across chains. A cross-chain swap bridges AND swaps in one step (e.g., ETH on Ethereum to USDC on Base). Brian handles both, but the solver routing differs.
- **"Deposit/withdraw work on all chains"** -- DeFi actions (deposit, withdraw, borrow, repay) are only supported on Ethereum, Arbitrum, Optimism, Polygon, Base, and Avalanche via the Enso solver. Other chains only support swap, bridge, and transfer.
- **`npm install brian`** -- The package is `@brian-ai/sdk`. There is no `brian` package on npm related to this project.

## Setup

### Get an API Key

1. Go to https://brianknows.org
2. Create an account or sign in
3. Navigate to API Keys section
4. Generate a new API key
5. Store it in your environment:

```bash
export BRIAN_API_KEY="brian_..."
```

### Install the SDK

```bash
npm install @brian-ai/sdk
```

### Initialize

```typescript
import { BrianSDK } from "@brian-ai/sdk";

const brian = new BrianSDK({
  apiKey: process.env.BRIAN_API_KEY!,
});
```

For US-based projects, override the API URL:

```typescript
const brian = new BrianSDK({
  apiKey: process.env.BRIAN_API_KEY!,
  apiUrl: "https://us-api.brianknows.org",
});
```

## Core Endpoints

### Transaction Endpoint

Convert a natural language prompt into executable transaction calldata.

**POST** `https://api.brianknows.org/api/v0/agent/transaction`

```typescript
const response = await brian.transact({
  prompt: "Swap 10 USDC for ETH on Base",
  address: "0xYourWalletAddress",
  chainId: "8453",
});
```

#### Raw HTTP

```bash
curl -X POST "https://api.brianknows.org/api/v0/agent/transaction" \
  -H "Content-Type: application/json" \
  -H "x-brian-api-key: $BRIAN_API_KEY" \
  -d '{
    "prompt": "Swap 10 USDC for ETH on Base",
    "address": "0xYourWalletAddress",
    "chainId": "8453"
  }'
```

#### Request Body

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | string | Yes | Natural language transaction intent |
| `address` | string | Yes | Sender wallet address (checksummed) |
| `chainId` | string | No | Source chain ID. If omitted, inferred from prompt. Throws error if ambiguous. |

#### Response Structure

```json
{
  "result": [
    {
      "solver": "Enso",
      "action": "swap",
      "type": "write",
      "data": {
        "description": "Swap 10 USDC for ETH on Base",
        "steps": [
          {
            "chainId": 8453,
            "to": "0xUSDC_CONTRACT",
            "from": "0xYourWalletAddress",
            "data": "0x095ea7b3...",
            "value": "0",
            "gasLimit": "60000"
          },
          {
            "chainId": 8453,
            "to": "0xROUTER_CONTRACT",
            "from": "0xYourWalletAddress",
            "data": "0x5ae401dc...",
            "value": "0",
            "gasLimit": "250000"
          }
        ],
        "fromToken": {
          "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
          "chainId": 8453,
          "symbol": "USDC",
          "decimals": 6
        },
        "toToken": {
          "address": "0x0000000000000000000000000000000000000000",
          "chainId": 8453,
          "symbol": "ETH",
          "decimals": 18
        },
        "fromAmount": "10000000",
        "toAmount": "3200000000000000"
      }
    }
  ]
}
```

The `steps` array contains transactions that must be executed in order. Step 0 is typically a token approval when swapping from an ERC-20.

### Knowledge Endpoint

Ask protocol questions and get answers with source citations.

**POST** `https://api.brianknows.org/api/v0/agent/knowledge`

```typescript
const response = await brian.ask({
  prompt: "What is the current TVL of Aave V3 on Arbitrum?",
  kb: "public-knowledge-box",
});
```

#### Raw HTTP

```bash
curl -X POST "https://api.brianknows.org/api/v0/agent/knowledge" \
  -H "Content-Type: application/json" \
  -H "x-brian-api-key: $BRIAN_API_KEY" \
  -d '{
    "prompt": "What is the current TVL of Aave V3 on Arbitrum?",
    "kb": "public-knowledge-box"
  }'
```

#### Response Structure

```json
{
  "result": {
    "answer": "The current TVL of Aave V3 on Arbitrum is...",
    "context": [
      {
        "pageContent": "...",
        "metadata": {
          "source": "https://docs.aave.com/...",
          "title": "Aave V3 Documentation"
        }
      }
    ]
  }
}
```

### Smart Contracts Endpoint

Generate Solidity contracts from natural language descriptions.

**POST** `https://api.brianknows.org/api/v0/agent/smart-contracts`

```typescript
const response = await brian.generateContract({
  prompt: "Create an ERC-20 token with a max supply of 1 million and a 2% transfer tax",
});
```

## Executing Transactions

Brian returns calldata but does not execute. You must sign and send each step.

### With viem

```typescript
import { createWalletClient, http } from "viem";
import { base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";
import { BrianSDK } from "@brian-ai/sdk";

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);

const walletClient = createWalletClient({
  account,
  chain: base,
  transport: http(),
});

const brian = new BrianSDK({
  apiKey: process.env.BRIAN_API_KEY!,
});

async function executeIntent(prompt: string) {
  const response = await brian.transact({
    prompt,
    address: account.address,
    chainId: "8453",
  });

  for (const result of response) {
    for (const step of result.data.steps) {
      const hash = await walletClient.sendTransaction({
        to: step.to as `0x${string}`,
        data: step.data as `0x${string}`,
        value: BigInt(step.value),
        gas: step.gasLimit ? BigInt(step.gasLimit) : undefined,
      });

      const publicClient = createPublicClient({
        chain: base,
        transport: http(),
      });

      const receipt = await publicClient.waitForTransactionReceipt({ hash });
      if (receipt.status !== "success") {
        throw new Error(`Transaction failed: ${hash}`);
      }
    }
  }
}
```

### With ethers.js

```typescript
import { ethers } from "ethers";
import { BrianSDK } from "@brian-ai/sdk";

const provider = new ethers.JsonRpcProvider(process.env.RPC_URL);
const wallet = new ethers.Wallet(process.env.PRIVATE_KEY!, provider);

const brian = new BrianSDK({
  apiKey: process.env.BRIAN_API_KEY!,
});

async function executeIntent(prompt: string) {
  const response = await brian.transact({
    prompt,
    address: wallet.address,
    chainId: "8453",
  });

  for (const result of response) {
    for (const step of result.data.steps) {
      const tx = await wallet.sendTransaction({
        to: step.to,
        data: step.data,
        value: BigInt(step.value),
        gasLimit: step.gasLimit ? BigInt(step.gasLimit) : undefined,
      });

      const receipt = await tx.wait();
      if (!receipt || receipt.status === 0) {
        throw new Error(`Transaction reverted: ${tx.hash}`);
      }
    }
  }
}
```

## Supported Actions

| Action | Description | Solver | Chains |
|--------|-------------|--------|--------|
| `swap` | Exchange tokens on the same chain | Enso, LI.FI, Portals | All supported chains |
| `bridge` | Move tokens across chains | Bungee, LI.FI, Symbiosis | All EVM chains |
| `transfer` | Send tokens to another address | Native | All supported chains |
| `deposit` | Deposit into DeFi protocols (Aave, Compound, etc.) | Enso | Ethereum, Arbitrum, Optimism, Polygon, Base, Avalanche |
| `withdraw` | Withdraw from DeFi protocols | Enso | Ethereum, Arbitrum, Optimism, Polygon, Base, Avalanche |
| `borrow` | Borrow from lending protocols (Aave) | Enso | Ethereum, Arbitrum, Optimism, Polygon, Base, Avalanche |
| `repay` | Repay borrowed positions | Enso | Ethereum, Arbitrum, Optimism, Polygon, Base, Avalanche |
| `cross-chain swap` | Bridge + swap in one intent | LI.FI, Bungee | All EVM chains |

## Prompt Engineering

Brian's NLP model extracts structured parameters from natural language. Better prompts produce more accurate results.

### Effective Prompts

```
"Swap 100 USDC for WETH on Arbitrum"
"Bridge 0.5 ETH from Ethereum to Base"
"Deposit 1000 USDC into Aave on Polygon"
"Transfer 50 USDT to 0xRecipientAddress on Optimism"
"Borrow 500 USDC from Aave on Ethereum with ETH as collateral"
```

### Ineffective Prompts

```
"Buy some crypto"              -- no token, no amount, no chain
"Move my tokens"               -- no specifics
"Do something with USDC"       -- no action
"Swap USDC"                    -- no target token, no amount
```

### Rules

1. Always specify the **amount** and **token symbol**
2. Include the **chain name** when the token exists on multiple chains
3. For bridge/cross-chain: specify both **source** and **destination** chains
4. For DeFi actions: name the **protocol** (e.g., "Aave", "Compound")
5. Use standard token symbols (USDC, WETH, DAI), not contract addresses

## LangChain Integration

The `@brian-ai/langchain` package provides a toolkit for building autonomous Web3 agents.

### Install

```bash
npm install @brian-ai/langchain @langchain/openai langchain
```

### Create an Agent

```typescript
import { createBrianAgent } from "@brian-ai/langchain";
import { ChatOpenAI } from "@langchain/openai";

const agent = await createBrianAgent({
  apiKey: process.env.BRIAN_API_KEY!,
  privateKeyOrAccount: process.env.PRIVATE_KEY as `0x${string}`,
  llm: new ChatOpenAI({
    modelName: "gpt-4o",
    temperature: 0,
  }),
});

const result = await agent.invoke({
  input: "Swap 10 USDC for ETH on Base",
});

console.log(result.output);
```

### Use BrianToolkit Directly

```typescript
import { BrianToolkit } from "@brian-ai/langchain";

const toolkit = new BrianToolkit({
  apiKey: process.env.BRIAN_API_KEY!,
  privateKeyOrAccount: process.env.PRIVATE_KEY as `0x${string}`,
});

const tools = toolkit.getTools();
```

The toolkit exposes individual tools for swap, bridge, transfer, deposit, withdraw, borrow, and repay. Each tool can be added to any LangChain agent.

### With Coinbase CDP Wallet

```typescript
import { BrianCDPToolkit } from "@brian-ai/langchain";

const cdpToolkit = new BrianCDPToolkit({
  apiKey: process.env.BRIAN_API_KEY!,
  coinbaseApiKeyName: process.env.CDP_API_KEY_NAME!,
  coinbaseApiKeySecret: process.env.CDP_API_KEY_SECRET!,
});

const tools = cdpToolkit.getTools();
```

## Error Handling

```typescript
import { BrianSDK } from "@brian-ai/sdk";

const brian = new BrianSDK({
  apiKey: process.env.BRIAN_API_KEY!,
});

async function safeTransact(prompt: string, address: string) {
  try {
    const response = await brian.transact({
      prompt,
      address,
    });

    if (!response || response.length === 0) {
      throw new Error("Brian returned no results. Rephrase your prompt with more detail.");
    }

    return response;
  } catch (error: unknown) {
    if (error instanceof Error) {
      if (error.message.includes("401")) {
        throw new Error("Invalid API key. Check BRIAN_API_KEY environment variable.");
      }
      if (error.message.includes("429")) {
        throw new Error("Rate limited. Wait before retrying.");
      }
      if (error.message.includes("chain")) {
        throw new Error("Chain could not be determined. Include chain name in prompt or pass chainId.");
      }
    }
    throw error;
  }
}
```

## Rate Limits

| Plan | Requests/Minute | Requests/Day |
|------|-----------------|--------------|
| Free | 30 | 1,000 |
| Pro | 120 | 10,000 |
| Enterprise | Custom | Custom |

Rate limit headers are returned on every response:

```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 28
X-RateLimit-Reset: 1709001600
```

## Security Considerations

1. **Never expose your API key client-side.** Route all Brian API calls through a backend server.
2. **Validate transaction calldata** before signing. Brian returns calldata from third-party solvers (Enso, LI.FI). Verify the `to` address is the expected contract.
3. **Set allowances carefully.** Approval steps may request unlimited allowance. Override with a specific amount if your security policy requires it.
4. **Simulate transactions** before broadcasting on mainnet. Use `eth_call` or Tenderly simulation to catch reverts.
5. **Never log or store the full transaction response** in production -- it contains calldata that could be replayed.

## References

- Brian API Documentation: https://docs.brianknows.org/
- Brian TypeScript SDK: https://github.com/brian-knows/brian-sdk
- Brian LangChain Toolkit: https://github.com/brian-knows/langchain-toolkit
- `@brian-ai/sdk` on npm: https://www.npmjs.com/package/@brian-ai/sdk
- `@brian-ai/langchain` on npm: https://www.npmjs.com/package/@brian-ai/langchain
- LangChain Toolkit Docs: https://langchain.brianknows.org/
- API Swagger: https://api.brianknows.org/swagger

Last verified: February 2026
