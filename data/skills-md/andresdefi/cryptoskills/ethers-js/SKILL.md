---
name: ethers-js
description: "ethers.js v6 TypeScript/JavaScript Ethereum library — Provider, Signer, Contract interaction, ABI encoding/decoding, event filters, ENS resolution, and BigNumber-to-bigint migration from v5. Covers JsonRpcProvider, BrowserProvider, Wallet, ContractFactory, and typed contract interfaces."
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Dev Tools
tags:
  - ethers
  - ethers-js
  - javascript
  - typescript
  - ethereum
  - provider
---

# ethers.js v6

ethers.js is a TypeScript/JavaScript library for interacting with EVM-compatible blockchains. Version 6 is a ground-up rewrite with native ES2020 bigint, tree-shakeable exports, and a cleaner API surface. It provides Providers (read-only chain access), Signers (transaction authorization), and Contract objects (typed on-chain interaction).

## What You Probably Got Wrong

> LLMs consistently produce v5 code when asked for ethers.js. Every pattern below is a v6 correction. If you see `BigNumber`, `ethers.utils`, or `ethers.providers` in your output, you are writing v5. Stop and use the v6 equivalents.

- **v6 uses native `bigint`, NOT `BigNumber`.** There is no `BigNumber` class in v6. All uint256 values are returned as `bigint`. Do not import `BigNumber` from anywhere. Do not call `.toNumber()`, `.toString()`, or `.mul()` on return values -- use native bigint operators (`+`, `-`, `*`, `/`, `%`, `**`).
- **`ethers.parseEther()`, NOT `ethers.utils.parseEther()`.** The `utils` namespace does not exist in v6. All utility functions are top-level exports: `parseEther`, `formatEther`, `parseUnits`, `formatUnits`, `id`, `keccak256`, `toUtf8Bytes`, `AbiCoder`, etc.
- **`ethers.providers` does not exist.** Provider classes are top-level: `JsonRpcProvider`, `BrowserProvider`, `WebSocketProvider`, `FallbackProvider`, `InfuraProvider`, `AlchemyProvider`. Do not write `new ethers.providers.JsonRpcProvider()`.
- **`BrowserProvider` replaced `Web3Provider`.** To wrap a browser wallet (MetaMask's `window.ethereum`), use `new BrowserProvider(window.ethereum)`, not `new Web3Provider(window.ethereum)`.
- **Contract constructor changed.** v5: `new ethers.Contract(address, abi, signerOrProvider)`. v6: same signature, but the third argument is now called a "runner" and can be a Provider (read-only) or Signer (read-write). The `.connect()` method returns a new Contract instance with a different runner.
- **`contract.getFunction("name")` for explicit method access.** v6 still supports `contract.functionName()` but the recommended pattern for clarity is `contract.getFunction("transfer")`.
- **`Wallet` extends `AbstractSigner`, NOT `Signer`.** The class hierarchy changed. `Wallet` takes a private key and a Provider. `new Wallet(privateKey, provider)`.
- **`getDefaultProvider()` is still available but rate-limited.** For production, always use an explicit `JsonRpcProvider` with your own RPC endpoint.
- **Event filters use `contract.on("EventName", callback)`.** The v6 event API is similar to v5 but the filter builder changed. Use `contract.filters.EventName(arg1, arg2)` -- returns an ethers `DeferredTopicFilter`.
- **`receipt.status` is a number (0 or 1), not a string.** Check `receipt.status === 1` for success.
- **`TransactionResponse.wait()` can return `null`.** If the transaction is dropped or replaced, `wait()` returns `null`. Always handle this case.
- **ENS resolution only works on networks that support it.** Calling `provider.resolveName("vitalik.eth")` on a non-mainnet provider without ENS deployment returns `null`, not an error.
- **`Interface` replaced `ethers.utils.Interface`.** Use `new Interface(abi)` directly, imported from `ethers`.

## Installation

```bash
npm install ethers
```

v6 requires Node.js 16+ and TypeScript 5.0+ (if using TypeScript).

```json
{
  "dependencies": {
    "ethers": "^6.13.0"
  }
}
```

## Quick Start

### Create a Provider (Read-Only)

```typescript
import { JsonRpcProvider } from "ethers";

const RPC_URL = process.env.RPC_URL;
if (!RPC_URL) throw new Error("RPC_URL environment variable required");

const provider = new JsonRpcProvider(RPC_URL);

const blockNumber = await provider.getBlockNumber();
console.log(`Current block: ${blockNumber}`);
```

### Create a Wallet (Read-Write)

```typescript
import { JsonRpcProvider, Wallet } from "ethers";

const RPC_URL = process.env.RPC_URL;
const PRIVATE_KEY = process.env.PRIVATE_KEY;
if (!RPC_URL) throw new Error("RPC_URL required");
if (!PRIVATE_KEY) throw new Error("PRIVATE_KEY required");

const provider = new JsonRpcProvider(RPC_URL);
const wallet = new Wallet(PRIVATE_KEY, provider);

console.log(`Address: ${wallet.address}`);
```

### Browser Wallet (MetaMask, etc.)

```typescript
import { BrowserProvider } from "ethers";

// window.ethereum is the EIP-1193 provider injected by the wallet
if (!window.ethereum) throw new Error("No wallet detected");

const provider = new BrowserProvider(window.ethereum);
const signer = await provider.getSigner();
console.log(`Connected: ${await signer.getAddress()}`);
```

## Providers

### JsonRpcProvider

Direct connection to any JSON-RPC endpoint. Use for server-side scripts, bots, and backends.

```typescript
import { JsonRpcProvider } from "ethers";

const provider = new JsonRpcProvider("https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY");

const balance = await provider.getBalance("vitalik.eth");
console.log(`Balance: ${balance} wei`);

const network = await provider.getNetwork();
console.log(`Chain ID: ${network.chainId}`);
```

### WebSocketProvider

Persistent connection for real-time event subscriptions. Required for `provider.on("block", ...)`.

```typescript
import { WebSocketProvider } from "ethers";

const wsProvider = new WebSocketProvider("wss://eth-mainnet.g.alchemy.com/v2/YOUR_KEY");

wsProvider.on("block", (blockNumber: number) => {
  console.log(`New block: ${blockNumber}`);
});
```

### BrowserProvider

Wraps any EIP-1193 provider (MetaMask, WalletConnect, Coinbase Wallet). Use in frontend dApps.

```typescript
import { BrowserProvider } from "ethers";

const provider = new BrowserProvider(window.ethereum);

// Request account access (triggers wallet popup)
const signer = await provider.getSigner();
const address = await signer.getAddress();
const balance = await provider.getBalance(address);
```

### FallbackProvider

Redundant provider with quorum voting. Uses multiple backends and returns the result agreed upon by a quorum.

```typescript
import { FallbackProvider, JsonRpcProvider } from "ethers";

const providers = [
  new JsonRpcProvider("https://rpc1.example.com"),
  new JsonRpcProvider("https://rpc2.example.com"),
  new JsonRpcProvider("https://rpc3.example.com"),
];

// quorum: 2 means at least 2 providers must agree
const fallbackProvider = new FallbackProvider(providers, undefined, { quorum: 2 });
```

## Signers and Wallets

### Wallet from Private Key

```typescript
import { Wallet, JsonRpcProvider } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);
const wallet = new Wallet(process.env.PRIVATE_KEY!, provider);

console.log(`Address: ${wallet.address}`);
console.log(`Chain: ${(await wallet.provider!.getNetwork()).chainId}`);
```

### Wallet from Mnemonic

```typescript
import { Wallet, Mnemonic } from "ethers";

// BIP-39 mnemonic to HD wallet (default path: m/44'/60'/0'/0/0)
const mnemonic = Mnemonic.fromPhrase("test test test test test test test test test test test junk");
const wallet = Wallet.fromPhrase(mnemonic.phrase);

console.log(`Address: ${wallet.address}`);
console.log(`Private key: ${wallet.privateKey}`);
```

### Random Wallet

```typescript
import { Wallet } from "ethers";

const randomWallet = Wallet.createRandom();
console.log(`Address: ${randomWallet.address}`);
console.log(`Mnemonic: ${randomWallet.mnemonic?.phrase}`);
```

### Signing Messages

```typescript
import { Wallet, verifyMessage } from "ethers";

const wallet = new Wallet(process.env.PRIVATE_KEY!);

const message = "Hello, Ethereum!";
const signature = await wallet.signMessage(message);

// Recover signer address from signature
const recovered = verifyMessage(message, signature);
console.log(`Signer: ${recovered}`);
console.log(`Match: ${recovered === wallet.address}`);
```

### Signing Typed Data (EIP-712)

```typescript
import { Wallet } from "ethers";

const wallet = new Wallet(process.env.PRIVATE_KEY!);

const domain = {
  name: "MyDApp",
  version: "1",
  chainId: 1n,
  verifyingContract: "0xCcCCccccCCCCcCCCCCCcCcCccCcCCCcCcccccccC",
};

const types = {
  Transfer: [
    { name: "to", type: "address" },
    { name: "amount", type: "uint256" },
    { name: "nonce", type: "uint256" },
  ],
};

const value = {
  to: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  amount: 1000000n,
  nonce: 0n,
};

const signature = await wallet.signTypedData(domain, types, value);
```

## Contracts

### Read-Only Contract (Provider)

```typescript
import { Contract, JsonRpcProvider } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);

const ERC20_ABI = [
  "function name() view returns (string)",
  "function symbol() view returns (string)",
  "function decimals() view returns (uint8)",
  "function balanceOf(address) view returns (uint256)",
  "function totalSupply() view returns (uint256)",
];

const USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
const contract = new Contract(USDC, ERC20_ABI, provider);

const [name, symbol, decimals, totalSupply] = await Promise.all([
  contract.name(),
  contract.symbol(),
  contract.decimals(),
  contract.totalSupply(),
]);

// decimals returns bigint in v6
console.log(`${name} (${symbol}), decimals: ${decimals}`);
console.log(`Total supply: ${totalSupply}`); // bigint
```

### Read-Write Contract (Signer)

```typescript
import { Contract, Wallet, JsonRpcProvider, parseUnits } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);
const wallet = new Wallet(process.env.PRIVATE_KEY!, provider);

const ERC20_ABI = [
  "function transfer(address to, uint256 amount) returns (bool)",
  "function approve(address spender, uint256 amount) returns (bool)",
  "function allowance(address owner, address spender) view returns (uint256)",
  "function balanceOf(address) view returns (uint256)",
];

const USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
const contract = new Contract(USDC, ERC20_ABI, wallet);

const recipient = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045";
// 100 USDC (6 decimals)
const amount = parseUnits("100", 6);

const tx = await contract.transfer(recipient, amount);
console.log(`TX hash: ${tx.hash}`);

const receipt = await tx.wait();
if (receipt === null) throw new Error("Transaction dropped or replaced");
if (receipt.status !== 1) throw new Error("Transaction reverted");

console.log(`Confirmed in block ${receipt.blockNumber}`);
```

### Human-Readable ABI

v6 supports human-readable ABI strings. Use these for simple interactions instead of full JSON ABIs.

```typescript
const abi = [
  "function name() view returns (string)",
  "function transfer(address to, uint256 amount) returns (bool)",
  "event Transfer(address indexed from, address indexed to, uint256 value)",
  "error InsufficientBalance(uint256 available, uint256 required)",
];
```

### Full JSON ABI

For complex contracts or when you need type generation, use the full JSON ABI.

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
```

### ContractFactory (Deploying Contracts)

```typescript
import { ContractFactory, Wallet, JsonRpcProvider } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);
const wallet = new Wallet(process.env.PRIVATE_KEY!, provider);

const abi = [
  "constructor(string name, string symbol, uint8 decimals)",
  "function name() view returns (string)",
  "function symbol() view returns (string)",
];

// bytecode from solc compilation output
const bytecode = "0x608060...";

const factory = new ContractFactory(abi, bytecode, wallet);

const contract = await factory.deploy("MyToken", "MTK", 18);
const deployTx = contract.deploymentTransaction();
if (!deployTx) throw new Error("No deployment transaction");

console.log(`Deploying: ${deployTx.hash}`);
await contract.waitForDeployment();

const address = await contract.getAddress();
console.log(`Deployed at: ${address}`);
```

### Connecting a Contract to a Different Runner

```typescript
import { Contract, JsonRpcProvider, Wallet } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);
const wallet = new Wallet(process.env.PRIVATE_KEY!, provider);

const abi = ["function transfer(address to, uint256 amount) returns (bool)"];
const address = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";

// Read-only contract
const readContract = new Contract(address, abi, provider);

// Connect to signer for write operations -- returns a NEW instance
const writeContract = readContract.connect(wallet) as Contract;
```

## Utility Functions

### Parsing and Formatting

```typescript
import { parseEther, formatEther, parseUnits, formatUnits } from "ethers";

// ETH (18 decimals)
const weiAmount: bigint = parseEther("1.5");       // 1500000000000000000n
const ethAmount: string = formatEther(weiAmount);   // "1.5"

// Custom decimals (USDC = 6)
const usdcWei: bigint = parseUnits("100.50", 6);   // 100500000n
const usdcStr: string = formatUnits(usdcWei, 6);   // "100.5"

// Gwei (9 decimals)
const gweiWei: bigint = parseUnits("30", "gwei");   // 30000000000n
const gweiStr: string = formatUnits(gweiWei, "gwei"); // "30.0"
```

### Hashing

```typescript
import { keccak256, toUtf8Bytes, id, solidityPackedKeccak256 } from "ethers";

// keccak256 of raw bytes
const hash = keccak256(toUtf8Bytes("Hello"));

// id() is shorthand for keccak256(toUtf8Bytes(...))
const eventTopic = id("Transfer(address,address,uint256)");

// Solidity-style packed encoding then keccak256
const packed = solidityPackedKeccak256(
  ["address", "uint256"],
  ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", 42n]
);
```

### ABI Encoding and Decoding

```typescript
import { AbiCoder } from "ethers";

const coder = AbiCoder.defaultAbiCoder();

// Encode
const encoded = coder.encode(
  ["address", "uint256", "bool"],
  ["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045", 1000n, true]
);

// Decode
const [addr, amount, flag] = coder.decode(
  ["address", "uint256", "bool"],
  encoded
);
console.log(`Address: ${addr}, Amount: ${amount}, Flag: ${flag}`);
```

### Interface for Encoding Function Calls

```typescript
import { Interface } from "ethers";

const iface = new Interface([
  "function transfer(address to, uint256 amount) returns (bool)",
  "function approve(address spender, uint256 amount) returns (bool)",
]);

// Encode a function call
const calldata = iface.encodeFunctionData("transfer", [
  "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  parseUnits("100", 6),
]);

// Decode a function call
const decoded = iface.decodeFunctionData("transfer", calldata);
console.log(`To: ${decoded[0]}, Amount: ${decoded[1]}`);

// Decode function result
const resultData = "0x0000000000000000000000000000000000000000000000000000000000000001";
const result = iface.decodeFunctionResult("transfer", resultData);
console.log(`Success: ${result[0]}`);
```

## Transactions

### Send ETH

```typescript
import { Wallet, JsonRpcProvider, parseEther } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);
const wallet = new Wallet(process.env.PRIVATE_KEY!, provider);

const tx = await wallet.sendTransaction({
  to: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  value: parseEther("0.1"),
});

console.log(`TX hash: ${tx.hash}`);

const receipt = await tx.wait();
if (receipt === null) throw new Error("Transaction dropped or replaced");
if (receipt.status !== 1) throw new Error("Transaction reverted");

console.log(`Gas used: ${receipt.gasUsed}`);
console.log(`Effective gas price: ${receipt.gasPrice}`);
```

### EIP-1559 Transaction with Gas Control

```typescript
import { Wallet, JsonRpcProvider, parseEther, parseUnits } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);
const wallet = new Wallet(process.env.PRIVATE_KEY!, provider);

const feeData = await provider.getFeeData();

const tx = await wallet.sendTransaction({
  to: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  value: parseEther("0.1"),
  maxFeePerGas: feeData.maxFeePerGas,
  maxPriorityFeePerGas: feeData.maxPriorityFeePerGas,
});

const receipt = await tx.wait();
if (receipt === null) throw new Error("Transaction dropped or replaced");
if (receipt.status !== 1) throw new Error("Transaction reverted");
```

### Transaction Receipt Details

```typescript
import { JsonRpcProvider } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);

const receipt = await provider.getTransactionReceipt("0x...");
if (!receipt) throw new Error("Transaction not found");

console.log(`Status: ${receipt.status === 1 ? "success" : "reverted"}`);
console.log(`Block: ${receipt.blockNumber}`);
console.log(`Gas used: ${receipt.gasUsed}`);
console.log(`Logs: ${receipt.logs.length}`);
```

## Events

### Listening to Events (Real-Time)

```typescript
import { Contract, WebSocketProvider } from "ethers";

const provider = new WebSocketProvider("wss://eth-mainnet.g.alchemy.com/v2/YOUR_KEY");

const USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
const abi = [
  "event Transfer(address indexed from, address indexed to, uint256 value)",
];

const contract = new Contract(USDC, abi, provider);

contract.on("Transfer", (from: string, to: string, value: bigint, event) => {
  console.log(`Transfer: ${from} -> ${to}: ${value}`);
  console.log(`Block: ${event.log.blockNumber}`);
});
```

### Querying Past Events

```typescript
import { Contract, JsonRpcProvider } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);

const USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
const abi = [
  "event Transfer(address indexed from, address indexed to, uint256 value)",
];

const contract = new Contract(USDC, abi, provider);

// Query last 1000 blocks
const currentBlock = await provider.getBlockNumber();
const events = await contract.queryFilter("Transfer", currentBlock - 1000, currentBlock);

for (const event of events) {
  if (event.args) {
    console.log(`${event.args.from} -> ${event.args.to}: ${event.args.value}`);
  }
}
```

### Filtered Events

```typescript
import { Contract, JsonRpcProvider } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);

const USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
const abi = [
  "event Transfer(address indexed from, address indexed to, uint256 value)",
];

const contract = new Contract(USDC, abi, provider);

// Filter: transfers FROM a specific address
const fromFilter = contract.filters.Transfer("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045");

// Filter: transfers TO a specific address
const toFilter = contract.filters.Transfer(null, "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045");

const currentBlock = await provider.getBlockNumber();
const transfers = await contract.queryFilter(fromFilter, currentBlock - 5000, currentBlock);
console.log(`Found ${transfers.length} transfers`);
```

## ENS Resolution

```typescript
import { JsonRpcProvider } from "ethers";

// ENS resolution requires a mainnet provider (or a network with ENS deployed)
const provider = new JsonRpcProvider(process.env.RPC_URL);

// Forward resolution: name -> address
const address = await provider.resolveName("vitalik.eth");
if (address === null) throw new Error("ENS name not found");
console.log(`vitalik.eth = ${address}`);

// Reverse resolution: address -> name
const name = await provider.lookupAddress("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045");
console.log(`Name: ${name}`); // may be null if no reverse record
```

### ENS Avatar

```typescript
import { JsonRpcProvider } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);

const resolver = await provider.getResolver("vitalik.eth");
if (!resolver) throw new Error("No resolver for this name");

const avatar = await resolver.getAvatar();
console.log(`Avatar: ${avatar}`);

const contentHash = await resolver.getContentHash();
console.log(`Content hash: ${contentHash}`);
```

## Error Handling

### Catching Contract Reverts

```typescript
import { Contract, JsonRpcProvider, isError } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);

const abi = [
  "function transfer(address to, uint256 amount) returns (bool)",
  "error InsufficientBalance(uint256 available, uint256 required)",
];

const contract = new Contract("0x...", abi, provider);

try {
  const tx = await contract.transfer("0x...", 1000n);
  const receipt = await tx.wait();
  if (receipt === null) throw new Error("Transaction dropped");
  if (receipt.status !== 1) throw new Error("Transaction reverted");
} catch (error: unknown) {
  if (isError(error, "CALL_EXCEPTION")) {
    // Contract revert with reason or custom error
    console.error(`Revert reason: ${error.reason}`);
    console.error(`Error data: ${error.data}`);
  } else if (isError(error, "INSUFFICIENT_FUNDS")) {
    console.error("Not enough ETH for gas + value");
  } else if (isError(error, "NONCE_EXPIRED")) {
    console.error("Nonce already used -- transaction may be a duplicate");
  } else if (isError(error, "REPLACEMENT_UNDERPRICED")) {
    console.error("Replacement transaction gas price too low");
  } else if (isError(error, "NETWORK_ERROR")) {
    console.error("Network connectivity issue");
  } else if (isError(error, "TIMEOUT")) {
    console.error("Request timed out");
  } else {
    throw error;
  }
}
```

### The `isError` Utility

v6 provides `isError(error, code)` for type-safe error checking. This replaces the v5 pattern of checking `error.code` directly.

```typescript
import { isError } from "ethers";

try {
  await provider.getBlock("invalid");
} catch (error: unknown) {
  if (isError(error, "INVALID_ARGUMENT")) {
    console.error(`Invalid argument: ${error.argument} = ${error.value}`);
  } else if (isError(error, "SERVER_ERROR")) {
    console.error(`RPC error: ${error.info}`);
  } else {
    throw error;
  }
}
```

## Multicall Pattern

Batch multiple read calls into a single RPC request using Multicall3.

```typescript
import { Contract, JsonRpcProvider, Interface } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);

// Multicall3 is deployed at the same address on all major EVM chains
const MULTICALL3 = "0xcA11bde05977b3631167028862bE2a173976CA11";

const multicallAbi = [
  "function aggregate3(tuple(address target, bool allowFailure, bytes callData)[] calls) view returns (tuple(bool success, bytes returnData)[])",
];

const multicall = new Contract(MULTICALL3, multicallAbi, provider);

const erc20Iface = new Interface([
  "function balanceOf(address) view returns (uint256)",
  "function decimals() view returns (uint8)",
]);

const tokens = [
  "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48", // USDC
  "0xdAC17F958D2ee523a2206206994597C13D831ec7", // USDT
  "0x6B175474E89094C44Da98b954EedeAC495271d0F", // DAI
];

const wallet = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045";

const calls = tokens.map((token) => ({
  target: token,
  allowFailure: false,
  callData: erc20Iface.encodeFunctionData("balanceOf", [wallet]),
}));

const results = await multicall.aggregate3(calls);

for (let i = 0; i < tokens.length; i++) {
  const balance = erc20Iface.decodeFunctionResult("balanceOf", results[i].returnData)[0];
  console.log(`${tokens[i]}: ${balance}`);
}
```

## v5 to v6 Migration Quick Reference

| v5 Pattern | v6 Equivalent |
|-----------|--------------|
| `ethers.providers.JsonRpcProvider` | `JsonRpcProvider` (top-level import) |
| `ethers.providers.Web3Provider` | `BrowserProvider` |
| `ethers.utils.parseEther("1.0")` | `parseEther("1.0")` |
| `ethers.utils.formatEther(wei)` | `formatEther(wei)` |
| `ethers.utils.parseUnits("100", 6)` | `parseUnits("100", 6)` |
| `ethers.utils.formatUnits(val, 6)` | `formatUnits(val, 6)` |
| `ethers.utils.keccak256(...)` | `keccak256(...)` |
| `ethers.utils.id(...)` | `id(...)` |
| `ethers.utils.Interface` | `Interface` |
| `ethers.utils.AbiCoder` | `AbiCoder` |
| `ethers.BigNumber.from(...)` | Native `BigInt(...)` or `123n` |
| `bn.add(other)` | `a + b` |
| `bn.mul(other)` | `a * b` |
| `bn.div(other)` | `a / b` |
| `bn.eq(other)` | `a === b` |
| `bn.gt(other)` | `a > b` |
| `bn.isZero()` | `a === 0n` |
| `bn.toNumber()` | `Number(a)` (only if value fits in Number.MAX_SAFE_INTEGER) |
| `bn.toString()` | `a.toString()` |
| `contract.deployed()` | `contract.waitForDeployment()` |
| `contract.address` | `await contract.getAddress()` |
| `tx.wait()` returns receipt | `tx.wait()` returns receipt or `null` |
| `receipt.status === 1` | Same (unchanged) |

## Common Patterns

### Check Balance Before Transfer

```typescript
import { JsonRpcProvider, Wallet, parseEther, formatEther } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);
const wallet = new Wallet(process.env.PRIVATE_KEY!, provider);

async function safeTransferEth(to: string, ethAmount: string): Promise<string> {
  const value = parseEther(ethAmount);
  const balance = await provider.getBalance(wallet.address);

  const feeData = await provider.getFeeData();
  // 21000 gas for simple ETH transfer
  const estimatedGasCost = 21000n * (feeData.maxFeePerGas ?? feeData.gasPrice ?? 0n);
  const totalCost = value + estimatedGasCost;

  if (balance < totalCost) {
    throw new Error(
      `Insufficient balance. Have: ${formatEther(balance)} ETH, Need: ${formatEther(totalCost)} ETH`
    );
  }

  const tx = await wallet.sendTransaction({ to, value });
  const receipt = await tx.wait();
  if (receipt === null) throw new Error("Transaction dropped or replaced");
  if (receipt.status !== 1) throw new Error("Transaction reverted");

  return tx.hash;
}
```

### ERC-20 Approve and Transfer

```typescript
import { Contract, Wallet, JsonRpcProvider, parseUnits, MaxUint256 } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);
const wallet = new Wallet(process.env.PRIVATE_KEY!, provider);

const ERC20_ABI = [
  "function approve(address spender, uint256 amount) returns (bool)",
  "function allowance(address owner, address spender) view returns (uint256)",
  "function transferFrom(address from, address to, uint256 amount) returns (bool)",
];

async function ensureAllowance(
  tokenAddress: string,
  spender: string,
  amount: bigint
): Promise<void> {
  const token = new Contract(tokenAddress, ERC20_ABI, wallet);
  const currentAllowance: bigint = await token.allowance(wallet.address, spender);

  if (currentAllowance >= amount) return;

  const tx = await token.approve(spender, amount);
  const receipt = await tx.wait();
  if (receipt === null) throw new Error("Approval transaction dropped");
  if (receipt.status !== 1) throw new Error("Approval reverted");
}
```

### Wait for N Confirmations

```typescript
import { Wallet, JsonRpcProvider, parseEther } from "ethers";

const provider = new JsonRpcProvider(process.env.RPC_URL);
const wallet = new Wallet(process.env.PRIVATE_KEY!, provider);

const tx = await wallet.sendTransaction({
  to: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  value: parseEther("0.01"),
});

// Wait for 3 confirmations
const receipt = await tx.wait(3);
if (receipt === null) throw new Error("Transaction dropped or replaced");
if (receipt.status !== 1) throw new Error("Transaction reverted");

console.log(`Confirmed with ${3} confirmations at block ${receipt.blockNumber}`);
```

## Reference Links

- Official docs: https://docs.ethers.org/v6/
- Migration guide: https://docs.ethers.org/v6/migrating/
- GitHub: https://github.com/ethers-io/ethers.js
- NPM: https://www.npmjs.com/package/ethers
- Changelog: https://github.com/ethers-io/ethers.js/blob/main/CHANGELOG.md
