---
name: viem
description: TypeScript interface for Ethereum and EVM chains. Use for reading blockchain state, sending transactions, interacting with contracts, encoding/decoding ABI data, and building dApp backends. Transport-based architecture with full type safety over ABIs.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Dev Tools
tags:
  - viem
  - ethereum
  - typescript
  - abi
  - client
---

# viem

TypeScript interface for Ethereum and EVM-compatible chains. Provides low-level primitives for blockchain interaction with end-to-end type safety, minimal abstraction overhead, and tree-shakeable modules. The default client library for wagmi.

## What You Probably Got Wrong

> AI agents trained before 2024 confuse viem with ethers.js patterns. These are the critical differences.

- **viem uses native `bigint`, not `BigNumber`** -- There is no `BigNumber` class. All wei values are `bigint`. Use `100n` literal syntax or `BigInt("100")`. Never use `ethers.BigNumber.from()`.
- **`Address` type is `` `0x${string}` ``, not plain `string`** -- viem enforces checksummed `0x`-prefixed addresses at the type level. Use `getAddress()` to normalize.
- **Clients are not providers** -- viem has `PublicClient` (reads), `WalletClient` (writes), and `TestClient` (anvil). There is no `Provider` or `Signer` concept.
- **Transports replace connection URLs** -- You pass `http()`, `webSocket()`, or `custom()` transports to clients, not raw RPC URLs as strings.
- **ABIs must be `as const`** -- For type inference to work, ABI arrays must use `as const` assertion. Without it, you lose all parameter/return type safety.
- **`simulateContract` before `writeContract`** -- viem separates simulation from execution. Always simulate first to catch reverts before sending a transaction.
- **No default chain** -- Every client requires an explicit `chain` parameter. There is no implicit mainnet default.
- **`parseEther` returns `bigint`, not a wrapper** -- `parseEther("1.0")` returns `1000000000000000000n`, a raw `bigint`.

## Quick Start

### Installation

```bash
npm install viem
```

### Create a Public Client (read-only)

```typescript
import { createPublicClient, http } from "viem";
import { mainnet } from "viem/chains";

const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const blockNumber = await client.getBlockNumber();
```

### Create a Wallet Client (write)

```typescript
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet } from "viem/chains";

const account = privateKeyToAccount(
  process.env.PRIVATE_KEY as `0x${string}`
);

const walletClient = createWalletClient({
  account,
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});
```

## Core Concepts

### Transports

Transports define how the client communicates with the RPC node.

```typescript
import { http, webSocket, fallback } from "viem";

const httpTransport = http("https://eth.llamarpc.com");

const wsTransport = webSocket("wss://eth.llamarpc.com");

// Fallback tries transports in order
const resilientTransport = fallback([
  http("https://eth.llamarpc.com"),
  http("https://rpc.ankr.com/eth"),
]);
```

### Chains

Viem ships chain definitions for 50+ networks. Each chain object contains chain ID, RPC URLs, block explorer, native currency, and ENS registry address.

```typescript
import { mainnet, arbitrum, optimism, base, polygon } from "viem/chains";

// Chain objects carry all config
mainnet.id;            // 1
arbitrum.id;           // 42161
base.id;               // 8453
```

### Client Types

| Client | Purpose | Created With |
|--------|---------|--------------|
| `PublicClient` | Read blockchain state, call view functions, watch events | `createPublicClient` |
| `WalletClient` | Sign and send transactions, deploy contracts | `createWalletClient` |
| `TestClient` | Anvil/Hardhat node control (mine, setBalance, impersonate) | `createTestClient` |

### Account Types

```typescript
// Local account -- private key in memory, signs locally
import { privateKeyToAccount } from "viem/accounts";
const localAccount = privateKeyToAccount("0x...");

// JSON-RPC account -- delegates signing to the wallet (browser, hardware)
import { createWalletClient, custom } from "viem";
const walletClient = createWalletClient({
  chain: mainnet,
  transport: custom(window.ethereum!),
});
const [address] = await walletClient.getAddresses();
```

## Reading Blockchain State

### Basic Reads

```typescript
import { createPublicClient, http, formatEther } from "viem";
import { mainnet } from "viem/chains";

const client = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const balance = await client.getBalance({
  address: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
});
console.log(`${formatEther(balance)} ETH`);

const block = await client.getBlock({ blockTag: "latest" });

const txCount = await client.getTransactionCount({
  address: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
});
```

### Read Contract (view/pure functions)

```typescript
const abi = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const balance = await client.readContract({
  address: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", // USDC
  abi,
  functionName: "balanceOf",
  args: ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"],
});
// balance is typed as bigint
```

### Multicall (batch reads in a single RPC call)

```typescript
const erc20Abi = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "decimals",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint8" }],
  },
] as const;

const results = await client.multicall({
  contracts: [
    {
      address: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      abi: erc20Abi,
      functionName: "balanceOf",
      args: ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"],
    },
    {
      address: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      abi: erc20Abi,
      functionName: "decimals",
    },
  ],
});

// results[0].result is bigint (balance)
// results[1].result is number (decimals)
// Each result has { result, status: "success" | "failure" }
```

## Writing Transactions

### Send Native ETH

```typescript
import { parseEther } from "viem";

const hash = await walletClient.sendTransaction({
  to: "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
  value: parseEther("0.1"),
});
```

### Simulate Then Write Contract

```typescript
const abi = [
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

// Simulate first to catch reverts without spending gas
const { request } = await client.simulateContract({
  address: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  abi,
  functionName: "transfer",
  args: [
    "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
    1000000n, // 1 USDC (6 decimals)
  ],
  account: walletClient.account,
});

// Execute -- pass the validated request directly
const hash = await walletClient.writeContract(request);
```

### Wait for Transaction Receipt

```typescript
const receipt = await client.waitForTransactionReceipt({ hash });

if (receipt.status === "reverted") {
  throw new Error(`Transaction reverted in block ${receipt.blockNumber}`);
}

console.log(`Confirmed in block ${receipt.blockNumber}`);
console.log(`Gas used: ${receipt.gasUsed}`);
```

## Contract Interaction

### Typed ABIs with `as const`

The `as const` assertion is what enables viem's type inference. Without it, TypeScript widens the ABI to generic types and you lose autocomplete on function names, argument types, and return types.

```typescript
// Correct -- full type inference
const abi = [
  {
    name: "approve",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "spender", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
  {
    name: "Transfer",
    type: "event",
    inputs: [
      { name: "from", type: "address", indexed: true },
      { name: "to", type: "address", indexed: true },
      { name: "value", type: "uint256", indexed: false },
    ],
  },
] as const;

// functionName autocompletes to "approve"
// args is typed as [address, bigint]
// return is typed as boolean
```

### Watching Events

```typescript
const unwatch = client.watchEvent({
  address: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  event: {
    name: "Transfer",
    type: "event",
    inputs: [
      { name: "from", type: "address", indexed: true },
      { name: "to", type: "address", indexed: true },
      { name: "value", type: "uint256", indexed: false },
    ],
  },
  onLogs: (logs) => {
    for (const log of logs) {
      console.log(`${log.args.from} -> ${log.args.to}: ${log.args.value}`);
    }
  },
});

// Stop watching
unwatch();
```

### Getting Past Logs

```typescript
import { parseAbiItem } from "viem";

const logs = await client.getLogs({
  address: "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  event: parseAbiItem(
    "event Transfer(address indexed from, address indexed to, uint256 value)"
  ),
  fromBlock: 18000000n,
  toBlock: 18001000n,
});

for (const log of logs) {
  console.log(log.args.from, log.args.to, log.args.value);
}
```

## Utility Functions

### Value Conversion

```typescript
import {
  parseEther,
  formatEther,
  parseUnits,
  formatUnits,
  parseGwei,
  formatGwei,
} from "viem";

// ETH conversion (18 decimals)
parseEther("1.0");         // 1000000000000000000n
formatEther(1000000000000000000n); // "1"

// Custom decimals (e.g., USDC has 6)
parseUnits("100", 6);     // 100000000n
formatUnits(100000000n, 6); // "100"

// Gas price
parseGwei("20");           // 20000000000n
formatGwei(20000000000n);  // "20"
```

### ABI Encoding/Decoding

```typescript
import {
  encodeFunctionData,
  decodeFunctionData,
  encodeAbiParameters,
  decodeAbiParameters,
  parseAbi,
} from "viem";

const abi = parseAbi([
  "function transfer(address to, uint256 amount) returns (bool)",
]);

// Encode calldata for a raw transaction
const data = encodeFunctionData({
  abi,
  functionName: "transfer",
  args: ["0x70997970C51812dc3A010C7d01b50e0d17dc79C8", 1000000n],
});

// Decode calldata back to function name and args
const { functionName, args } = decodeFunctionData({ abi, data });

// Encode raw ABI parameters (for constructors, etc.)
const encoded = encodeAbiParameters(
  [
    { name: "x", type: "uint256" },
    { name: "y", type: "address" },
  ],
  [123n, "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"]
);
```

### Address Utilities

```typescript
import { getAddress, isAddress, isAddressEqual } from "viem";

// Normalize to checksummed address
getAddress("0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48");
// "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"

// Validate
isAddress("0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"); // true
isAddress("not-an-address"); // false

// Case-insensitive comparison
isAddressEqual(
  "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
  "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
); // true
```

### Hashing

```typescript
import { keccak256, toBytes, toHex } from "viem";

keccak256(toBytes("hello"));
// 0x1c8aff950685c2ed4bc3174f3472287b56d9517b9c948127319a09a7a36deac8

toHex(420);    // "0x1a4"
toBytes("0x1a4"); // Uint8Array
```

## Chain Configuration

### Built-in Chains

```typescript
import {
  mainnet,
  sepolia,
  arbitrum,
  arbitrumSepolia,
  optimism,
  base,
  polygon,
  avalanche,
  bsc,
  gnosis,
  zksync,
  scroll,
  linea,
} from "viem/chains";
```

### Custom Chain Definition

```typescript
import { defineChain } from "viem";

const myChain = defineChain({
  id: 12345,
  name: "My Chain",
  nativeCurrency: {
    name: "Ether",
    symbol: "ETH",
    decimals: 18,
  },
  rpcUrls: {
    default: {
      http: ["https://rpc.mychain.io"],
      webSocket: ["wss://rpc.mychain.io"],
    },
  },
  blockExplorers: {
    default: {
      name: "MyChainScan",
      url: "https://scan.mychain.io",
    },
  },
});

const client = createPublicClient({
  chain: myChain,
  transport: http(),
});
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `ContractFunctionExecutionError` | Contract call reverted | Check revert reason in `error.cause`, verify args and state |
| `ContractFunctionRevertedError` | Revert with reason string or custom error | Decode `error.data` for custom error details |
| `InsufficientFundsError` | Account lacks ETH for value + gas | Check balance before sending |
| `NonceAlreadyUsedError` | Nonce conflict from concurrent transactions | Use `getTransactionCount` with `blockTag: "pending"` |
| `TransactionReceiptNotFoundError` | Receipt unavailable (dropped or pending) | Retry `waitForTransactionReceipt` with higher `timeout` |
| `InvalidAddressError` | Malformed address passed | Validate with `isAddress()` before use |
| `ChainMismatchError` | Wallet is on a different chain than client | Switch chain or create client for correct chain |
| `HttpRequestError` | RPC node unreachable or rate-limited | Use `fallback` transport with multiple RPCs |
| `InvalidAbiError` | ABI is malformed or missing `as const` | Verify ABI structure and add `as const` assertion |

### Catching Contract Errors

```typescript
import { BaseError, ContractFunctionRevertedError } from "viem";

try {
  await client.simulateContract({ address, abi, functionName, args, account });
} catch (err) {
  if (err instanceof BaseError) {
    const revertError = err.walk(
      (e) => e instanceof ContractFunctionRevertedError
    );
    if (revertError instanceof ContractFunctionRevertedError) {
      const errorName = revertError.data?.errorName;
      console.error(`Contract reverted: ${errorName}`, revertError.data?.args);
    }
  }
}
```

## Common Patterns

### ERC-20 Token Balance Check

```typescript
import { createPublicClient, http, formatUnits } from "viem";
import { mainnet } from "viem/chains";

const erc20Abi = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "decimals",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint8" }],
  },
  {
    name: "symbol",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "string" }],
  },
] as const;

async function getTokenBalance(
  client: ReturnType<typeof createPublicClient>,
  token: `0x${string}`,
  wallet: `0x${string}`
) {
  const [balance, decimals, symbol] = await Promise.all([
    client.readContract({
      address: token,
      abi: erc20Abi,
      functionName: "balanceOf",
      args: [wallet],
    }),
    client.readContract({
      address: token,
      abi: erc20Abi,
      functionName: "decimals",
    }),
    client.readContract({
      address: token,
      abi: erc20Abi,
      functionName: "symbol",
    }),
  ]);

  return {
    raw: balance,
    formatted: formatUnits(balance, decimals),
    symbol,
    decimals,
  };
}
```

### Approve + Swap Pattern (simulate-then-execute)

```typescript
import { maxUint256, parseUnits } from "viem";

const tokenAbi = [
  {
    name: "approve",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "spender", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
] as const;

async function approveToken(
  publicClient: ReturnType<typeof createPublicClient>,
  walletClient: ReturnType<typeof createWalletClient>,
  token: `0x${string}`,
  spender: `0x${string}`,
  amount: bigint
) {
  const { request } = await publicClient.simulateContract({
    address: token,
    abi: tokenAbi,
    functionName: "approve",
    args: [spender, amount],
    account: walletClient.account,
  });

  const hash = await walletClient.writeContract(request);

  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status === "reverted") {
    throw new Error("Approval transaction reverted");
  }

  return receipt;
}
```

### Deploy a Contract

```typescript
import { createWalletClient, http } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { sepolia } from "viem/chains";

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);

const walletClient = createWalletClient({
  account,
  chain: sepolia,
  transport: http(process.env.RPC_URL),
});

const hash = await walletClient.deployContract({
  abi: contractAbi,
  bytecode: contractBytecode,
  args: [arg1, arg2],
});

const receipt = await publicClient.waitForTransactionReceipt({ hash });
console.log(`Deployed at ${receipt.contractAddress}`);
```

### Gas Estimation

```typescript
const gasEstimate = await client.estimateGas({
  account: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  to: "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
  value: parseEther("0.1"),
});

const gasPrice = await client.getGasPrice();
const maxFeePerGas = await client.estimateFeesPerGas();
```

### Batch JSON-RPC Requests

```typescript
const batchClient = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL, {
    batch: true,
  }),
});

// These fire as a single batched JSON-RPC request
const [balance, blockNumber, gasPrice] = await Promise.all([
  batchClient.getBalance({
    address: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  }),
  batchClient.getBlockNumber(),
  batchClient.getGasPrice(),
]);
```

## References

- [Official Docs](https://viem.sh)
- [GitHub](https://github.com/wevm/viem)
- [API Reference](https://viem.sh/docs/actions/public/introduction)
- [Chain List](https://viem.sh/docs/chains/introduction)
- [TypeScript ABI Utilities](https://viem.sh/docs/abi/parseAbi)
- [wagmi Integration](https://wagmi.sh)
