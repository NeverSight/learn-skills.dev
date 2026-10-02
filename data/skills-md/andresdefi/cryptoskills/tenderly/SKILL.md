---
name: tenderly
description: "Tenderly blockchain DevOps platform — transaction simulation API, fork environments for testing, Alerts and Webhooks for monitoring, Web3 Actions (serverless functions), contract verification, Gas Profiler, and Transaction Debugger. Covers REST API integration and Tenderly SDK."
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: DevOps
tags:
  - tenderly
  - simulation
  - debugging
  - monitoring
  - devops
  - blockchain
---

# Tenderly

Tenderly is a blockchain DevOps platform providing transaction simulation, debugging, monitoring, and testing infrastructure. It supports Ethereum, Polygon, Arbitrum, Optimism, Base, BSC, Avalanche, Fantom, and 60+ other EVM networks through a unified REST API.

## What You Probably Got Wrong

> LLMs frequently generate outdated Tenderly API calls, confuse v1 and v2 endpoints, and misunderstand how Virtual TestNets differ from simple forks. These corrections are non-negotiable.

- **The API is v2, not v1.** All endpoints use `https://api.tenderly.co/api/v2/`. If you see `/api/v1/` in your code, you are using the deprecated API. The v1 simulation endpoint had a different request/response schema. Stop and switch to v2.
- **"Forks" are now "Virtual TestNets".** Tenderly rebranded forks to Virtual TestNets. The API paths still use `/vnets/` or `/testnet/` in some contexts, but the product name is Virtual TestNet. Do not call them "forks" in user-facing code — the API field names may still say `fork` internally.
- **Authentication uses `X-Access-Key`, not `Authorization: Bearer`.** The primary auth mechanism is a header `X-Access-Key: <your-access-key>`. Bearer tokens exist for OAuth flows but are not the standard integration path. If you set `Authorization: Bearer <access-key>`, the request will 401.
- **Project paths require both account slug AND project slug.** Every project-scoped endpoint is `/api/v2/project/{accountSlug}/{projectSlug}/...`. If you omit either slug, you get a 404. The account slug is your username or org name, NOT your account ID.
- **Simulation `from` field is required.** The v2 simulation endpoint requires a `from` address. Omitting it does not default to zero address — it returns a 400 error. Always specify who is sending the transaction.
- **State overrides use a map keyed by address, not an array.** The `state_objects` field in simulation requests is `{ [address]: { storage: { [slot]: value } } }`, not an array of override objects.
- **Virtual TestNet RPC URLs expire.** When you create a Virtual TestNet, the returned RPC URL is ephemeral. If the VNet is deleted or expires (based on your plan), the URL stops working. Do not hardcode VNet RPC URLs.
- **Web3 Actions are NOT Lambda functions with arbitrary runtimes.** They run in a constrained Node.js environment with a specific set of available packages. You cannot install arbitrary npm packages. The runtime provides `ethers`, `axios`, and the Tenderly SDK. Check the docs for the current package list.
- **Gas Profiler data comes from simulation, not from live transactions.** You must simulate a transaction first, then access the gas breakdown from the simulation result. There is no separate "gas profiler" endpoint.
- **`save` and `save_if_fails` are separate flags.** Setting `save: true` saves every simulation to your dashboard. Setting `save_if_fails: true` only saves failed simulations. They are independent booleans, not mutually exclusive.
- **Simulation `network_id` is a string, not a number.** Pass `"1"` for Ethereum mainnet, not `1`. The API will reject numeric network IDs.
- **`block_number` in simulations is optional.** If omitted, it uses the latest block. If provided, it must be a number (not a string), and it must be a block that has been indexed by Tenderly.

## Quick Start

### Authentication

Every Tenderly API request requires your access key. Generate one from the Tenderly Dashboard under Settings > Authorization > API Access Tokens.

```typescript
const TENDERLY_ACCESS_KEY = process.env.TENDERLY_ACCESS_KEY;
const TENDERLY_ACCOUNT_SLUG = process.env.TENDERLY_ACCOUNT_SLUG;
const TENDERLY_PROJECT_SLUG = process.env.TENDERLY_PROJECT_SLUG;

if (!TENDERLY_ACCESS_KEY) throw new Error("TENDERLY_ACCESS_KEY is required");
if (!TENDERLY_ACCOUNT_SLUG) throw new Error("TENDERLY_ACCOUNT_SLUG is required");
if (!TENDERLY_PROJECT_SLUG) throw new Error("TENDERLY_PROJECT_SLUG is required");

const BASE_URL = `https://api.tenderly.co/api/v2/project/${TENDERLY_ACCOUNT_SLUG}/${TENDERLY_PROJECT_SLUG}`;

const headers = {
  "X-Access-Key": TENDERLY_ACCESS_KEY,
  "Content-Type": "application/json",
};
```

### Installation

```bash
npm install axios
```

No dedicated Tenderly SDK package is required for REST API usage. All interaction is through HTTP requests. The `@tenderly/actions` package is only needed for Web3 Actions development.

## Transaction Simulation API

Simulate any transaction without sending it onchain. Returns full execution trace, state changes, gas usage, event logs, and revert reasons.

### Simulate a Simple ETH Transfer

```typescript
interface SimulationRequest {
  network_id: string;
  from: string;
  to: string;
  input: string;
  value: string;
  gas: number;
  gas_price: string;
  save: boolean;
  save_if_fails: boolean;
  simulation_type: "quick" | "full" | "abi";
  state_objects?: Record<string, {
    balance?: string;
    storage?: Record<string, string>;
  }>;
  block_number?: number;
}

async function simulateTransaction(
  params: SimulationRequest
): Promise<{ simulation: { id: string; status: boolean; gas_used: number; block_number: number }; transaction: { transaction_info: { call_trace: { calls: Array<{ from: string; to: string; input: string; output: string; gas_used: number; type: string }> }; state_diff: Array<{ address: string; original: Record<string, string>; dirty: Record<string, string> }>; logs: Array<{ address: string; topics: string[]; data: string }> } } }> {
  const response = await fetch(`${BASE_URL}/simulate`, {
    method: "POST",
    headers,
    body: JSON.stringify(params),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Simulation failed (${response.status}): ${error}`);
  }

  return response.json() as Promise<SimulationResponse>;
}
```

### Simulate an ERC-20 Transfer

```typescript
import { encodeFunctionData, parseUnits } from "viem";

const erc20TransferAbi = [
  {
    name: "transfer",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "to", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
] as const;

const USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
const SENDER = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045";
const RECIPIENT = "0x1234567890abcdef1234567890abcdef12345678";

const calldata = encodeFunctionData({
  abi: erc20TransferAbi,
  functionName: "transfer",
  args: [RECIPIENT, parseUnits("1000", 6)],
});

const result = await simulateTransaction({
  network_id: "1",
  from: SENDER,
  to: USDC,
  input: calldata,
  value: "0",
  gas: 100_000,
  gas_price: "0",
  save: true,
  save_if_fails: true,
  simulation_type: "full",
});

console.log(`Success: ${result.simulation.status}`);
console.log(`Gas used: ${result.simulation.gas_used}`);
```

### Simulate with State Overrides

Override account balances or storage slots before simulation. Useful for testing as any address without needing its private key.

```typescript
const resultWithOverrides = await simulateTransaction({
  network_id: "1",
  from: SENDER,
  to: USDC,
  input: calldata,
  value: "0",
  gas: 200_000,
  gas_price: "0",
  save: false,
  save_if_fails: true,
  simulation_type: "full",
  // Override sender's ETH balance to 100 ETH
  state_objects: {
    [SENDER]: {
      balance: "0x56BC75E2D63100000", // 100 ETH in hex
    },
  },
});
```

### Simulation Types

| Type | Description | Use Case |
|------|-------------|----------|
| `quick` | Basic pass/fail, gas used, no trace | CI/CD validation, quick checks |
| `full` | Full call trace, state diffs, logs | Debugging, security analysis |
| `abi` | Decoded inputs/outputs using verified ABI | Human-readable output |

### Batch Simulation (Simulate Bundle)

Simulate multiple transactions sequentially, where each transaction sees the state changes from previous ones.

```typescript
interface BundleSimulationRequest {
  simulations: SimulationRequest[];
}

async function simulateBundle(
  simulations: SimulationRequest[]
): Promise<SimulationResponse[]> {
  const response = await fetch(`${BASE_URL}/simulate-bundle`, {
    method: "POST",
    headers,
    body: JSON.stringify({ simulations }),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Bundle simulation failed (${response.status}): ${error}`);
  }

  const data = await response.json();
  return data.simulation_results as SimulationResponse[];
}
```

## Virtual TestNets (Forks)

Virtual TestNets create a copy of any network's state at a specific block. You get a private RPC endpoint that behaves like a real network but is fully isolated. Transactions on a Virtual TestNet do not affect mainnet.

### Create a Virtual TestNet

```typescript
async function createVirtualTestNet(params: {
  slug: string;
  display_name: string;
  fork_config: { network_id: number; block_number?: number };
  virtual_network_config: { chain_config: { chain_id: number } };
  sync_state_config: { enabled: boolean };
  explorer_page_config: { enabled: boolean; verification_visibility: "bytecode" | "src" | "all" };
}): Promise<{ id: string; rpcs: Array<{ name: string; url: string }>; fork_config: { network_id: number; block_number: number } }> {
  const response = await fetch(
    `https://api.tenderly.co/api/v2/project/${TENDERLY_ACCOUNT_SLUG}/${TENDERLY_PROJECT_SLUG}/vnets`,
    { method: "POST", headers, body: JSON.stringify(params) }
  );

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`VNet creation failed (${response.status}): ${error}`);
  }

  return response.json();
}

const vnet = await createVirtualTestNet({
  slug: "mainnet-test",
  display_name: "Mainnet Testing Fork",
  fork_config: {
    network_id: 1,
  },
  virtual_network_config: {
    chain_config: {
      chain_id: 73571, // custom chain ID to avoid collision
    },
  },
  sync_state_config: {
    enabled: false,
  },
  explorer_page_config: {
    enabled: true,
    verification_visibility: "src",
  },
});

// Use the RPC URL with viem or ethers
const rpcUrl = vnet.rpcs[0].url;
console.log(`VNet RPC: ${rpcUrl}`);
```

### Fund an Account on a Virtual TestNet

```typescript
async function fundAccount(
  rpcUrl: string,
  address: string,
  amountHex: string
): Promise<void> {
  const response = await fetch(rpcUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method: "tenderly_setBalance",
      params: [[address], amountHex],
      id: 1,
    }),
  });

  if (!response.ok) {
    throw new Error(`Fund account failed (${response.status})`);
  }
}

// Fund address with 1000 ETH
await fundAccount(
  rpcUrl,
  "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "0x3635C9ADC5DEA00000" // 1000 ETH in hex wei
);
```

### Custom RPC Methods on Virtual TestNets

| Method | Description |
|--------|-------------|
| `tenderly_setBalance` | Set ETH balance for one or more addresses |
| `tenderly_addBalance` | Add ETH to existing balance |
| `tenderly_setErc20Balance` | Set ERC-20 token balance for an address |
| `tenderly_setStorageAt` | Set arbitrary storage slot value |
| `evm_snapshot` | Create a state snapshot (returns snapshot ID) |
| `evm_revert` | Revert to a previous snapshot |
| `evm_increaseTime` | Advance block timestamp |
| `evm_increaseBlocks` | Mine a specified number of blocks |

### Set ERC-20 Balance on Virtual TestNet

```typescript
async function setErc20Balance(
  rpcUrl: string,
  tokenAddress: string,
  walletAddress: string,
  amountHex: string
): Promise<void> {
  const response = await fetch(rpcUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method: "tenderly_setErc20Balance",
      params: [tokenAddress, walletAddress, amountHex],
      id: 1,
    }),
  });

  if (!response.ok) {
    throw new Error(`Set ERC-20 balance failed (${response.status})`);
  }
}
```

### Delete a Virtual TestNet

```typescript
async function deleteVirtualTestNet(vnetId: string): Promise<void> {
  const response = await fetch(
    `https://api.tenderly.co/api/v2/project/${TENDERLY_ACCOUNT_SLUG}/${TENDERLY_PROJECT_SLUG}/vnets/${vnetId}`,
    {
      method: "DELETE",
      headers,
    }
  );

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`VNet deletion failed (${response.status}): ${error}`);
  }
}
```

## Alerts and Webhooks

Monitor onchain events in real time. Alerts trigger when specified conditions are met and can notify via webhook, email, Slack, Telegram, PagerDuty, or Discord.

### Alert Types

| Type | Trigger |
|------|---------|
| `successful_tx` | Transaction executes successfully |
| `failed_tx` | Transaction reverts |
| `function_call` | Specific function is called on a contract |
| `event_emitted` | Specific event is emitted |
| `state_change` | Storage slot value changes |
| `balance_change` | ETH or token balance changes beyond threshold |
| `block_mined` | New block is mined (useful for health checks) |
| `whitelisted_caller` | Transaction from a specific address |
| `blacklisted_caller` | Transaction NOT from a whitelisted address |

### Create an Alert via API

```typescript
async function createAlert(params: {
  name: string;
  network: string;
  type: string;
  enabled: boolean;
  alert_targets: Array<{
    type: "webhook" | "email" | "slack" | "telegram" | "pagerduty" | "discord";
    webhook?: { url: string; secret?: string };
    email?: { address: string };
  }>;
  alert_parameters: {
    contracts?: string[];
    events?: Array<{ name: string; signature: string }>;
    functions?: Array<{ name: string; signature: string }>;
    threshold?: { amount: string; direction: "above" | "below" | "both" };
  };
}): Promise<{ id: string }> {
  const response = await fetch(`${BASE_URL}/alerts`, {
    method: "POST",
    headers,
    body: JSON.stringify(params),
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Alert creation failed (${response.status}): ${error}`);
  }

  return response.json() as Promise<{ id: string }>;
}
```

### Webhook Signature Verification

If you set a secret on the webhook target, Tenderly signs the payload with HMAC-SHA256 in the `x-tenderly-signature` header. Verify with `timingSafeEqual` from `node:crypto`. See the setup-alerts example for a complete webhook receiver implementation.

## Web3 Actions (Serverless Functions)

Web3 Actions are serverless functions that execute in response to onchain events, periodic schedules, or webhook triggers. They run in Tenderly's Node.js runtime with access to ethers, axios, and the Tenderly SDK.

### Project Setup

```bash
npm install -g @tenderly/actions-cli
mkdir my-actions && cd my-actions
tenderly actions init
```

This creates a `tenderly.yaml` configuration file and an `actions` directory.

### Configuration (tenderly.yaml)

```yaml
account_id: ""
actions:
  your-account/your-project:
    runtime: v2
    sources: actions
    specs:
      onTransferDetected:
        description: "Triggers on ERC-20 Transfer events"
        function: actions/transfer:onTransfer
        trigger:
          type: transaction
          transaction:
            status:
              - mined
            filters:
              - network: 1
                eventEmitted:
                  contract:
                    address: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
                  name: Transfer
      periodicCheck:
        description: "Runs every 5 minutes"
        function: actions/health:periodicCheck
        trigger:
          type: periodic
          periodic:
            cron: "*/5 * * * *"
      webhookHandler:
        description: "Handles external webhook calls"
        function: actions/webhook:handleWebhook
        trigger:
          type: webhook
```

### Action Function Signature

```typescript
import {
  ActionFn,
  Context,
  Event,
  TransactionEvent,
  PeriodicEvent,
  WebhookEvent,
} from "@tenderly/actions";

// Transaction-triggered action
export const onTransfer: ActionFn = async (
  context: Context,
  event: Event
) => {
  const txEvent = event as TransactionEvent;
  const txHash = txEvent.hash;
  const logs = txEvent.logs;

  // Access project secrets (stored in Tenderly dashboard)
  const apiKey = await context.secrets.get("EXTERNAL_API_KEY");

  // Access project storage (key-value store persisted between runs)
  const lastProcessed = await context.storage.getStr("lastProcessedBlock");
  await context.storage.putStr("lastProcessedBlock", txEvent.blockNumber.toString());

  console.log(`Processing tx: ${txHash}`);
};

// Periodic action
export const periodicCheck: ActionFn = async (
  context: Context,
  event: Event
) => {
  const periodic = event as PeriodicEvent;
  console.log(`Periodic run at: ${periodic.time}`);
};

// Webhook-triggered action
export const handleWebhook: ActionFn = async (
  context: Context,
  event: Event
) => {
  const webhook = event as WebhookEvent;
  const body = webhook.payload;
  console.log(`Webhook received: ${JSON.stringify(body)}`);
};
```

### Deploy Actions

```bash
tenderly actions deploy
```

### Action Runtime Constraints

| Constraint | Limit |
|------------|-------|
| Execution timeout | 60 seconds |
| Memory | 256 MB |
| Payload size (webhook) | 1 MB |
| Storage (per project) | 10 MB |
| Available packages | ethers, axios, @tenderly/actions (built-in) |

## Contract Verification

Verify contracts on Tenderly for decoded transaction traces and human-readable function calls.

### Verify via API

POST to `/project/{account}/{project}/contracts/verify` with a body containing:

```typescript
{
  contracts: [{
    contractToVerify: "0xAddress:1",          // "address:network_id"
    solcConfig: {
      compiler_version: "v0.8.24+commit.e11b9ed9",
      optimizations_used: true,
      optimizations_count: 200,
    },
    sources: {
      "Contract.sol": { name: "Contract.sol", code: "// solidity source..." },
    },
  }]
}
```

### Verify Using Hardhat Plugin

```bash
npm install @tenderly/hardhat-tenderly
```

```typescript
// hardhat.config.ts
import "@tenderly/hardhat-tenderly";

const config = {
  tenderly: {
    project: process.env.TENDERLY_PROJECT_SLUG,
    username: process.env.TENDERLY_ACCOUNT_SLUG,
  },
};
```

```bash
npx hardhat tenderly:verify --network mainnet ContractName=0x...
```

## Gas Profiler

Gas profiling data is embedded in `simulation_type: "full"` results. There is no separate gas profiler endpoint. Walk the `transaction.transaction_info.call_trace.calls` array to get per-call gas breakdowns including `from`, `to`, `gas_used`, and `type` for each internal call. See the simulate-transaction example for a complete `extractGasProfile` implementation.

## Transaction Debugger

The Transaction Debugger provides step-by-step EVM execution traces for any transaction. Access it via the dashboard or programmatically.

### Get Debug Trace for an Existing Transaction

```typescript
async function getTransactionTrace(
  networkId: string,
  txHash: string
): Promise<{ gas: number; failed: boolean; return_value: string; struct_logs: Array<{ pc: number; op: string; gas: number; gas_cost: number; depth: number; stack: string[]; memory: string[]; storage: Record<string, string> }> }> {
  const response = await fetch(
    `https://api.tenderly.co/api/v2/project/${TENDERLY_ACCOUNT_SLUG}/${TENDERLY_PROJECT_SLUG}/network/${networkId}/transaction/${txHash}/trace`,
    { method: "GET", headers }
  );

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Trace retrieval failed (${response.status}): ${error}`);
  }

  return response.json();
}
```

## Error Handling Pattern

All Tenderly API errors return `{ error: { message, slug, id } }`. Always parse the error body on non-2xx responses to get actionable error slugs. See `resources/error-codes.md` for the complete error reference and `templates/tenderly-client.ts` for a production-ready `tenderlyFetch<T>()` wrapper with proper error extraction.

## Rate Limits and Quotas

| Resource | Free | Pro | Enterprise |
|----------|------|-----|------------|
| Simulations/month | 1,500 | 50,000 | Custom |
| Virtual TestNets (concurrent) | 1 | 10 | Custom |
| Alerts | 5 | 100 | Custom |
| Web3 Actions | 3 | 25 | Custom |
| API rate limit | 10 req/s | 50 req/s | Custom |

Rate limit responses return HTTP 429 with a `Retry-After` header.

## CI/CD Integration

### Simulate Before Deploy (GitHub Actions)

```yaml
name: Simulate Deployment
on:
  pull_request:
    paths:
      - "contracts/**"

jobs:
  simulate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: npm ci
      - run: npx hardhat compile
      - name: Simulate deployment
        env:
          TENDERLY_ACCESS_KEY: ${{ secrets.TENDERLY_ACCESS_KEY }}
          TENDERLY_ACCOUNT_SLUG: ${{ secrets.TENDERLY_ACCOUNT_SLUG }}
          TENDERLY_PROJECT_SLUG: ${{ secrets.TENDERLY_PROJECT_SLUG }}
        run: npx ts-node scripts/simulate-deploy.ts
```

## Further Reading

- Tenderly API v2 docs: https://docs.tenderly.co/reference/api
- Virtual TestNets: https://docs.tenderly.co/virtual-testnets
- Web3 Actions: https://docs.tenderly.co/web3-actions
- Gas Profiler: https://docs.tenderly.co/debugger/gas-profiler
- Hardhat integration: https://docs.tenderly.co/monitoring/smart-contracts/hardhat
