---
name: x402
description: "HTTP 402 payment protocol for AI agent commerce — three-actor model (Client, Resource Server, Facilitator), ERC-3009 transferWithAuthorization, server middleware (@x402/express), client patterns in TypeScript and Python, facilitator integration, agent-to-agent payments, pricing strategies, and replay protection. Works on Base, Ethereum, Arbitrum, Optimism, Polygon, and Solana."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: multichain
  category: AI Agents
tags:
  - x402
  - http-402
  - payment-protocol
  - ai-agents
  - agent-commerce
  - erc-3009
  - coinbase
---

# x402

x402 is an open payment protocol that revives the HTTP 402 "Payment Required" status code to enable instant stablecoin payments directly over HTTP. It uses a three-actor model — Client (buyer), Resource Server (seller), and Facilitator (settlement) — to let any HTTP endpoint accept payment without API keys, sessions, or accounts. The protocol is built on EIP-3009 `transferWithAuthorization` for gasless USDC transfers, meaning clients sign an off-chain authorization and the facilitator broadcasts the on-chain settlement.

Package ecosystem:
- **Server (TypeScript)**: `@x402/express`, `@x402/hono`, `@x402/next`
- **Client (TypeScript)**: `@x402/fetch`, `@x402/axios`
- **Client (Python)**: `pip install x402`
- **Client (Go)**: `go get github.com/coinbase/x402/go`
- **Core**: `@x402/core`, `@x402/evm`, `@x402/svm`

CDP Facilitator endpoint: `https://api.cdp.coinbase.com/platform/v2/x402`

## What You Probably Got Wrong

> LLMs have stale training data. These are the most common mistakes.

- **"x402 requires API keys or OAuth"** -- There are no API keys. Payment IS authentication. The client signs a USDC transfer authorization, includes it in the `X-PAYMENT` header, and the server verifies it. If the signature and balance check pass, the request is authorized. No accounts, no sessions, no bearer tokens.

- **"x402 only works on Base"** -- The protocol supports any EVM chain where USDC implements EIP-3009 (Base, Ethereum, Arbitrum, Optimism, Polygon) and Solana. Network identifiers use CAIP-2 format: `eip155:8453` for Base mainnet, `eip155:1` for Ethereum, `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` for Solana mainnet.

- **"Nonces are sequential counters"** -- x402 nonces are random 32-byte values (`bytes32`), not incrementing integers. Each authorization generates a fresh random nonce. The ERC-3009 contract tracks used nonces on-chain to prevent replay. Using sequential nonces or reusing a nonce will cause settlement to revert.

- **"The client pays gas"** -- The client never submits an on-chain transaction. The client signs an off-chain EIP-712 authorization. The facilitator broadcasts the `transferWithAuthorization` call and pays gas. CDP's hosted facilitator absorbs gas costs on Base mainnet for free-tier usage (1,000 tx/month).

- **"x402 supports any ERC-20 token"** -- The primary path uses USDC via EIP-3009 `transferWithAuthorization` for truly gasless transfers. A Permit2 fallback exists for arbitrary ERC-20 tokens, but it requires the user to have previously approved the Permit2 contract, which needs native gas. For the simplest integration, use USDC.

- **"The old package name is @coinbase/x402"** -- The current packages use the `@x402/*` namespace (e.g., `@x402/express`, `@x402/fetch`). Earlier versions used `x402-express` and `x402-fetch` without the scope. The `@coinbase/x402` name was never published.

- **"The payment header is called PAYMENT-SIGNATURE"** -- The header name is `X-PAYMENT`. It contains a base64-encoded JSON payload with the authorization, signature, scheme, and network. The server responds with `X-PAYMENT-RESPONSE`.

## Core Concepts

### Three-Actor Model

```
┌──────────┐      1. Request resource       ┌─────────────────┐
│          │ ─────────────────────────────► │                 │
│          │      2. HTTP 402 + payment     │   Resource      │
│  Client  │ ◄───────────────────────────── │   Server        │
│ (Buyer)  │      3. Request + X-PAYMENT    │   (Seller)      │
│          │ ─────────────────────────────► │                 │
│          │      6. HTTP 200 + resource    │                 │
│          │ ◄───────────────────────────── │                 │
└──────────┘                                └────────┬────────┘
                                                     │
                                              4. Verify │ 5. Settle
                                                     │
                                            ┌────────▼────────┐
                                            │                 │
                                            │  Facilitator    │
                                            │  (Settlement)   │
                                            │                 │
                                            └─────────────────┘
```

### Payment Flow Lifecycle

1. **Client** sends a standard HTTP request to a protected endpoint
2. **Resource Server** responds with HTTP 402 and payment requirements in the response body (scheme, network, amount, asset, payTo address)
3. **Client** constructs an EIP-3009 authorization (from, to, value, validAfter, validBefore, nonce), signs it with EIP-712, and retries the request with the `X-PAYMENT` header containing the base64-encoded payload
4. **Resource Server** forwards the payment to the **Facilitator** for verification (`/verify` endpoint)
5. **Facilitator** validates the signature, checks balance, and simulates the transfer
6. **Resource Server** serves the resource
7. **Resource Server** requests settlement from the **Facilitator** (`/settle` endpoint)
8. **Facilitator** calls `transferWithAuthorization` on the USDC contract to move funds on-chain

### HTTP 402 Response Format

When a client hits a paid endpoint without a payment header, the server returns:

```
HTTP/1.1 402 Payment Required
Content-Type: application/json

{
  "x402Version": 2,
  "accepts": [
    {
      "scheme": "exact",
      "network": "eip155:8453",
      "amount": "10000",
      "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
      "payTo": "0xSELLER_ADDRESS",
      "maxTimeoutSeconds": 60,
      "extra": {
        "assetTransferMethod": "eip3009",
        "name": "USDC",
        "version": "2"
      }
    }
  ],
  "error": "X-PAYMENT header is required"
}
```

The `amount` is in the token's smallest unit. For USDC (6 decimals), `10000` = $0.01.

## ERC-3009 transferWithAuthorization

EIP-3009 enables gasless token transfers by separating authorization from execution. The token holder signs an off-chain message; anyone can submit the signed authorization to the contract.

### Function Signature

```solidity
function transferWithAuthorization(
    address from,
    address to,
    uint256 value,
    uint256 validAfter,
    uint256 validBefore,
    bytes32 nonce,
    bytes   signature
) external;
```

### EIP-712 Domain

```solidity
EIP712Domain({
    name: "USDC",
    version: "2",
    chainId: <chain_id>,
    verifyingContract: <usdc_address>
})
```

### Authorization Struct (for signing)

```solidity
TransferWithAuthorization({
    from: address,
    to: address,
    value: uint256,
    validAfter: uint256,
    validBefore: uint256,
    nonce: bytes32
})
```

Key properties:
- `nonce` is a random `bytes32`, not a sequential counter. The contract maintains a mapping of `(authorizer, nonce) => bool` to track used nonces.
- `validAfter` and `validBefore` define a time window. Set `validAfter` to `0` (or current timestamp) and `validBefore` to current timestamp + `maxTimeoutSeconds`.
- The facilitator calls this function — the signer never needs native gas.
- USDC on Base, Ethereum, Arbitrum, Optimism, and Polygon all implement EIP-3009.

## Server Setup (TypeScript)

### Express Middleware

```bash
npm install @x402/core @x402/evm @x402/express
```

```typescript
import express from "express";
import { paymentMiddleware, x402ResourceServer } from "@x402/express";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { HTTPFacilitatorClient } from "@x402/core/server";

const app = express();

const facilitatorClient = new HTTPFacilitatorClient({
  url: "https://api.cdp.coinbase.com/platform/v2/x402",
});

const resourceServer = new x402ResourceServer(facilitatorClient)
  .register("eip155:8453", new ExactEvmScheme());

app.use(
  paymentMiddleware(
    {
      "GET /api/weather": {
        accepts: {
          scheme: "exact",
          network: "eip155:8453",
          price: "$0.01",
          payTo: process.env.PAYMENT_ADDRESS as `0x${string}`,
        },
        description: "Current weather data",
      },
      "POST /api/analyze": {
        accepts: {
          scheme: "exact",
          network: "eip155:8453",
          price: "$0.05",
          payTo: process.env.PAYMENT_ADDRESS as `0x${string}`,
        },
        description: "AI text analysis",
      },
    },
    resourceServer,
  ),
);

app.get("/api/weather", (_req, res) => {
  res.json({ temperature: 72, unit: "F", location: "San Francisco" });
});

app.post("/api/analyze", (req, res) => {
  res.json({ sentiment: "positive", confidence: 0.92 });
});

app.listen(3000, () => {
  console.log("x402 server running on port 3000");
});
```

Hono and Next.js middleware follow the same pattern — install `@x402/hono` or `@x402/next` and use the same `paymentMiddleware` + `x402ResourceServer` setup with framework-specific imports.

## Client Setup (TypeScript)

### Using @x402/fetch (Recommended)

The `wrapFetchWithPaymentFromConfig` function wraps the native `fetch` API to automatically handle 402 responses — detect the payment requirement, sign the authorization, and retry with the `X-PAYMENT` header.

```bash
npm install @x402/core @x402/evm @x402/fetch viem
```

```typescript
import { wrapFetchWithPaymentFromConfig } from "@x402/fetch";
import { ExactEvmScheme } from "@x402/evm";
import { privateKeyToAccount } from "viem/accounts";
import type { Hex } from "viem";

const account = privateKeyToAccount(process.env.PRIVATE_KEY as Hex);

const fetchWithPayment = wrapFetchWithPaymentFromConfig(fetch, {
  schemes: [
    {
      network: "eip155:8453",
      client: new ExactEvmScheme(account),
    },
  ],
});

const response = await fetchWithPayment("https://api.example.com/api/weather");
if (!response.ok) {
  throw new Error(`Request failed: ${response.status}`);
}

const data = await response.json();
console.log(data);
```

### Multi-Network Client

```typescript
import { x402Client, wrapFetchWithPayment } from "@x402/fetch";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { registerExactSvmScheme } from "@x402/svm/exact/client";
import { privateKeyToAccount } from "viem/accounts";
import { Keypair } from "@solana/web3.js";
import type { Hex } from "viem";

const evmAccount = privateKeyToAccount(process.env.EVM_PRIVATE_KEY as Hex);
const solanaKeypair = Keypair.fromSecretKey(
  Buffer.from(process.env.SOLANA_PRIVATE_KEY as string, "base64")
);

const client = new x402Client();
registerExactEvmScheme(client, { signer: evmAccount });
registerExactSvmScheme(client, { signer: solanaKeypair });

const fetchWithPayment = wrapFetchWithPayment(fetch, client);

// Automatically handles both EVM and Solana payment requirements
const evmResponse = await fetchWithPayment("https://api.example.com/evm-data");
const solResponse = await fetchWithPayment("https://api.example.com/sol-data");
```

For manual header construction without the wrapper, see the `agent-client` and `python-client` examples in this skill's `examples/` directory.

## Client Setup (Python)

```bash
pip install "x402[evm,requests]"
```

### Using the x402 Client

```python
from x402 import x402ClientSync
from x402.evm import ExactEvmScheme
from eth_account import Account

wallet = Account.from_key("0xYOUR_PRIVATE_KEY")

client = x402ClientSync()
client.register("eip155:*", ExactEvmScheme(signer=wallet))

# Make a paid request — the client handles the 402 flow automatically
import requests

session = requests.Session()
response = session.get("https://api.example.com/api/weather")

if response.status_code == 402:
    payment_required = response.json()
    payload = client.create_payment_payload(payment_required)
    response = session.get(
        "https://api.example.com/api/weather",
        headers={"X-PAYMENT": payload.to_header()},
    )

print(response.json())
```

For manual EIP-712 signing without the `x402` package, see the `python-client` example in this skill's `examples/` directory.

## Facilitator Patterns

### CDP Hosted Facilitator (Default)

Coinbase Developer Platform provides a hosted facilitator with two endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/verify` | POST | Validate signature, check balance, simulate transfer |
| `/settle` | POST | Execute `transferWithAuthorization` on-chain |

Pricing:
- **Free tier**: 1,000 transactions/month
- **Standard**: $0.001 per transaction thereafter
- **Base mainnet**: Zero gas fees (gas absorbed by facilitator)

```typescript
import { HTTPFacilitatorClient } from "@x402/core/server";

const facilitator = new HTTPFacilitatorClient({
  url: "https://api.cdp.coinbase.com/platform/v2/x402",
});
```

### Custom Facilitator

Run your own facilitator for full control over settlement:

```typescript
import { createFacilitatorServer } from "@x402/core/facilitator";
import { ExactEvmScheme } from "@x402/evm/exact/server";
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base } from "viem/chains";
import type { Hex } from "viem";

// Facilitator wallet pays gas for settlement
const facilitatorAccount = privateKeyToAccount(
  process.env.FACILITATOR_PRIVATE_KEY as Hex
);

const walletClient = createWalletClient({
  account: facilitatorAccount,
  chain: base,
  transport: http(),
});

const server = createFacilitatorServer({
  schemes: {
    "eip155:8453": new ExactEvmScheme({ walletClient }),
  },
});

server.listen(4000, () => {
  console.log("Custom facilitator on port 4000");
});
```

### Settlement Flow

1. Resource server sends the payment payload to facilitator `/verify`
2. Facilitator checks: signature validity, signer balance, authorization parameters, transfer simulation
3. If valid, resource server serves the response and calls facilitator `/settle`
4. Facilitator submits `transferWithAuthorization(from, to, value, validAfter, validBefore, nonce, signature)` to the USDC contract
5. Facilitator returns the transaction hash and receipt

The facilitator cannot modify the amount or destination. It serves only as the transaction broadcaster.

## Agent-to-Agent Payments

x402 enables autonomous agent commerce where AI agents discover services, negotiate prices, and pay without human intervention.

### Discovery Pattern

```typescript
// Agent discovers paid endpoints via standard HTTP
const discoveryResponse = await fetch("https://agent-service.com/.well-known/x402");
const services = await discoveryResponse.json();

// services contains available endpoints with pricing
// {
//   "endpoints": [
//     { "path": "/api/summarize", "price": "$0.02", "network": "eip155:8453" },
//     { "path": "/api/translate", "price": "$0.01", "network": "eip155:8453" }
//   ]
// }
```

### Autonomous Payment Execution

```typescript
import { wrapFetchWithPaymentFromConfig } from "@x402/fetch";
import { ExactEvmScheme } from "@x402/evm";
import { privateKeyToAccount } from "viem/accounts";
import type { Hex } from "viem";

const agentAccount = privateKeyToAccount(process.env.AGENT_PRIVATE_KEY as Hex);

const agentFetch = wrapFetchWithPaymentFromConfig(fetch, {
  schemes: [
    { network: "eip155:8453", client: new ExactEvmScheme(agentAccount) },
  ],
});

// Agent autonomously pays for another agent's service
async function callPaidService(url: string, body: Record<string, unknown>): Promise<unknown> {
  const response = await agentFetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`Service call failed: ${response.status}`);
  }

  return response.json();
}

// Multi-step agent workflow: summarize -> translate -> store
const summary = await callPaidService("https://summarizer.agent/api/summarize", {
  text: "Long document content...",
});

const translation = await callPaidService("https://translator.agent/api/translate", {
  text: summary,
  targetLanguage: "es",
});
```

## Pricing Strategies

### Per-Request (Fixed Price)

Charge a flat fee per API call. Simplest model.

```typescript
"GET /api/weather": {
  accepts: {
    scheme: "exact",
    network: "eip155:8453",
    price: "$0.01",
    payTo: process.env.PAYMENT_ADDRESS as `0x${string}`,
  },
  description: "Weather data — $0.01 per request",
},
```

### Tiered Pricing

Different prices per endpoint based on compute cost.

```typescript
const routes = {
  "GET /api/basic-query": {
    accepts: {
      scheme: "exact",
      network: "eip155:8453",
      price: "$0.001",
      payTo: paymentAddress,
    },
    description: "Basic database query",
  },
  "POST /api/ai-analysis": {
    accepts: {
      scheme: "exact",
      network: "eip155:8453",
      price: "$0.05",
      payTo: paymentAddress,
    },
    description: "AI-powered analysis — higher compute cost",
  },
  "POST /api/image-generation": {
    accepts: {
      scheme: "exact",
      network: "eip155:8453",
      price: "$0.10",
      payTo: paymentAddress,
    },
    description: "Image generation — GPU cost",
  },
};
```

### Dynamic Pricing

Adjust prices based on demand, time of day, or resource utilization.

```typescript
function getDynamicPrice(basePrice: number, currentLoad: number): string {
  // Surge pricing: 1x at 0% load, up to 3x at 100% load
  const multiplier = 1 + (currentLoad / 100) * 2;
  const price = basePrice * multiplier;
  return `$${price.toFixed(4)}`;
}
```

## Replay Protection

x402 uses two mechanisms to prevent payment replay:

### Random Nonces

Every authorization includes a random 32-byte nonce. The USDC contract's `authorizationState` mapping tracks whether a `(from, nonce)` pair has been used. Attempting to settle with a used nonce reverts with `authorization is used or canceled`.

```typescript
import { keccak256, encodePacked, toHex } from "viem";

// Generate a unique nonce per authorization
function generateNonce(): Hex {
  const randomBytes = crypto.getRandomValues(new Uint8Array(32));
  return toHex(randomBytes);
}
```

### Expiration Timestamps

The `validBefore` field ensures authorizations cannot be settled after their time window. Best practice: set `validBefore` to `now + maxTimeoutSeconds` (typically 30-60 seconds).

```typescript
const now = Math.floor(Date.now() / 1000);
const authorization = {
  validAfter: BigInt(0),
  validBefore: BigInt(now + 60), // 60-second window
  nonce: generateNonce(),
  // ... other fields
};
```

If a facilitator does not settle within the `validBefore` window, the authorization expires and the client's funds are never moved. The client can safely retry with a new authorization.

## Permit2 Fallback

For ERC-20 tokens that do not implement EIP-3009, x402 supports a Permit2-based fallback.

### How It Differs

| Feature | EIP-3009 | Permit2 |
|---------|----------|---------|
| Gasless setup | Yes (native) | Requires one-time approval tx |
| Token support | USDC only | Any ERC-20 |
| Contract | Token contract itself | Uniswap Permit2 contract |
| Proxy | None | `x402ExactPermit2Proxy` at `0x4020CD856C882D5fb903D99CE35316A085Bb0001` |

The Permit2 path requires the user to have approved the Permit2 contract (`0x000000000022D473030F116dDEE9F6B43aC78BA3`). If the allowance is missing, the server returns HTTP 412 with error code `PERMIT2_ALLOWANCE_REQUIRED`.

## Supported Networks

| Network | CAIP-2 Identifier | USDC Address | Status |
|---------|-------------------|--------------|--------|
| Base | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | Primary |
| Base Sepolia | `eip155:84532` | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` | Testnet |
| Ethereum | `eip155:1` | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` | Supported |
| Arbitrum | `eip155:42161` | `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` | Supported |
| Optimism | `eip155:10` | `0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85` | Supported |
| Polygon | `eip155:137` | `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359` | Supported |
| Solana | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | Supported |

Last verified: February 2026

## References

- **Spec**: https://github.com/coinbase/x402/tree/main/specs
- **TypeScript SDK**: https://github.com/coinbase/x402/tree/main/typescript
- **Python SDK**: https://pypi.org/project/x402/
- **Go SDK**: https://github.com/coinbase/x402/tree/main/go
- **CDP Docs**: https://docs.cdp.coinbase.com/x402/welcome
- **EIP-3009**: https://eips.ethereum.org/EIPS/eip-3009
- **x402.org**: https://www.x402.org
- **Cloudflare x402 Foundation**: https://blog.cloudflare.com/x402/
