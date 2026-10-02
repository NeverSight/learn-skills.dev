---
name: sei
description: "Sei parallelized EVM L1 — parallel transaction execution, SeiDB optimistic storage, native order matching engine, twin-turbo consensus, EVM and CosmWasm interop via pointer contracts, associated balances, and precompile contracts for staking, governance, and IBC."
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: sei
  category: L2 & Alt-L1
tags:
  - sei
  - evm
  - parallel-evm
  - cosmwasm
  - l1
  - trading
---

# Sei Parallelized EVM L1

## What You Probably Got Wrong

- **Sei V2 is a parallelized EVM, NOT just a Cosmos chain.** Since V2, Sei runs the EVM natively as its primary execution environment. It is not an EVM bridge, sidechain, or rollup on top of Cosmos. The EVM executes directly inside the Sei node with parallel transaction processing.
- **Pointer contracts enable EVM<>CosmWasm interop.** A CW20 token automatically gets a pointer ERC20 contract, and an ERC20 token can get a pointer CW20 contract. This means the same token is accessible from both execution environments without bridging or wrapping. The pointer is a lightweight proxy, not a copy.
- **Associated balances let EVM addresses hold Cosmos-native tokens.** Your EVM address (0x...) can hold native `usei`, IBC denoms, and TokenFactory tokens directly. No wrapping required. This is NOT the same as WSEI -- it is the actual native balance.
- **The native DEX module is deprecated.** Sei originally had a built-in order matching engine (the `dex` module). This is deprecated in favor of standard EVM DEXes like DragonSwap and Yaka Finance. Do NOT build against the native DEX module.
- **Standard EVM tooling works.** Deploy with Hardhat, Foundry, viem, ethers.js -- no custom compiler, no special flags. Sei EVM is bytecode-compatible with Ethereum. The Solidity compiler target is `paris` (no Shanghai-era PUSH0).
- **Parallel execution requires no code changes.** Sei's optimistic parallelization happens at the runtime level. Your Solidity contracts do not need any annotations or special patterns. However, contracts that touch independent storage slots parallelize better.
- **Precompile contracts exist for Cosmos-native operations.** Staking, governance, IBC transfers, address format conversion, and JSON parsing are all available via precompile contracts at fixed addresses. These are callable from Solidity like normal contracts.
- **EVM version target is `paris`, not `shanghai`.** Sei's EVM does not support the `PUSH0` opcode introduced in Shanghai. Set `evmVersion: "paris"` in your compiler config or deployments will fail with opcode errors.

## Chain Configuration

### Mainnet (pacific-1)

| Property | Value |
|----------|-------|
| Chain ID (EVM) | **1329** |
| Chain ID (Cosmos) | `pacific-1` |
| Currency | SEI (6 decimals for Cosmos, 18 decimals for EVM) |
| Block Time | ~390ms |
| Finality | ~390ms (instant, single-slot) |
| EVM Version | `paris` (no PUSH0) |
| Consensus | Twin-Turbo (optimistic block processing) |

#### RPC Endpoints (Mainnet)

| URL | Type |
|-----|------|
| `https://evm-rpc.sei-apis.com` | EVM JSON-RPC |
| `wss://evm-ws.sei-apis.com` | EVM WebSocket |
| `https://rest.sei-apis.com` | Cosmos REST |
| `https://rpc.sei-apis.com` | Cosmos Tendermint RPC |
| `https://grpc.sei-apis.com` | Cosmos gRPC |

#### Block Explorers

| Explorer | URL |
|----------|-----|
| Seistream | https://seistream.app |
| Seitrace | https://seitrace.com |
| Seiscan | https://seiscan.app |

### Testnet (atlantic-2)

| Property | Value |
|----------|-------|
| Chain ID (EVM) | **1328** |
| Chain ID (Cosmos) | `atlantic-2` |
| EVM RPC | `https://evm-rpc-testnet.sei-apis.com` |
| EVM WebSocket | `wss://evm-ws-testnet.sei-apis.com` |
| Cosmos REST | `https://rest-testnet.sei-apis.com` |
| Cosmos RPC | `https://rpc-testnet.sei-apis.com` |
| Explorer | https://seitrace.com/?chain=atlantic-2 |
| Faucet | https://atlantic-2.app.sei.io/faucet |

### Devnet (arctic-1)

| Property | Value |
|----------|-------|
| Chain ID (EVM) | **713715** |
| Chain ID (Cosmos) | `arctic-1` |
| EVM RPC | `https://evm-rpc-arctic-1.sei-apis.com` |
| Explorer | https://seitrace.com/?chain=arctic-1 |

## Key Differences from Ethereum

| Feature | Ethereum | Sei |
|---------|----------|-----|
| Block time | 12s | ~390ms |
| Finality | ~12-18 min | ~390ms (single-slot) |
| Execution model | Sequential | Parallel (optimistic) |
| EVM version | Shanghai+ | `paris` (no PUSH0) |
| Native denom | ETH (18 decimals) | SEI (18 decimals EVM, 6 decimals Cosmos) |
| Cosmos interop | None | Pointer contracts, precompiles |
| IBC | None | Native via precompile |
| Address format | 0x only | 0x (EVM) + sei1... (Cosmos), linked |
| Storage backend | LevelDB/PebbleDB | SeiDB (optimistic parallel) |

## Quick Start: viem Chain Definition

```typescript
import { defineChain } from "viem";

export const sei = defineChain({
  id: 1329,
  name: "Sei",
  nativeCurrency: { name: "SEI", symbol: "SEI", decimals: 18 },
  rpcUrls: {
    default: {
      http: ["https://evm-rpc.sei-apis.com"],
      webSocket: ["wss://evm-ws.sei-apis.com"],
    },
  },
  blockExplorers: {
    default: { name: "Seitrace", url: "https://seitrace.com" },
    seistream: { name: "Seistream", url: "https://seistream.app" },
  },
});

export const seiTestnet = defineChain({
  id: 1328,
  name: "Sei Testnet",
  nativeCurrency: { name: "SEI", symbol: "SEI", decimals: 18 },
  rpcUrls: {
    default: {
      http: ["https://evm-rpc-testnet.sei-apis.com"],
      webSocket: ["wss://evm-ws-testnet.sei-apis.com"],
    },
  },
  blockExplorers: {
    default: { name: "Seitrace", url: "https://seitrace.com/?chain=atlantic-2" },
  },
  testnet: true,
});
```

## Quick Start: Foundry Setup

```toml
# foundry.toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
evm_version = "paris"

[rpc_endpoints]
sei = "https://evm-rpc.sei-apis.com"
sei_testnet = "https://evm-rpc-testnet.sei-apis.com"

[etherscan]
sei = { key = "${SEITRACE_API_KEY}", chain = 1329, url = "https://seitrace.com/api" }
sei_testnet = { key = "${SEITRACE_API_KEY}", chain = 1328, url = "https://seitrace.com/api?chain=atlantic-2" }
```

## Quick Start: Hardhat Configuration

```typescript
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.24",
    settings: {
      evmVersion: "paris",
      optimizer: { enabled: true, runs: 200 },
    },
  },
  networks: {
    sei: {
      url: process.env.SEI_RPC_URL || "https://evm-rpc.sei-apis.com",
      chainId: 1329,
      accounts: [process.env.PRIVATE_KEY!],
    },
    seiTestnet: {
      url: process.env.SEI_TESTNET_RPC_URL || "https://evm-rpc-testnet.sei-apis.com",
      chainId: 1328,
      accounts: [process.env.PRIVATE_KEY!],
    },
  },
  etherscan: {
    apiKey: {
      sei: process.env.SEITRACE_API_KEY!,
    },
    customChains: [
      {
        network: "sei",
        chainId: 1329,
        urls: {
          apiURL: "https://seitrace.com/api",
          browserURL: "https://seitrace.com",
        },
      },
    ],
  },
};

export default config;
```

## Deployment

### Foundry Deploy

```bash
forge create src/MyContract.sol:MyContract \
  --rpc-url https://evm-rpc.sei-apis.com \
  --private-key $PRIVATE_KEY

forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://evm-rpc.sei-apis.com \
  --broadcast \
  --slow
```

### Hardhat Deploy

```bash
npx hardhat run scripts/deploy.ts --network sei
npx hardhat run scripts/deploy.ts --network seiTestnet
```

### Verification

```bash
forge verify-contract <address> src/MyContract.sol:MyContract \
  --chain 1329 \
  --verifier etherscan \
  --etherscan-api-key $SEITRACE_API_KEY \
  --verifier-url https://seitrace.com/api
```

## Parallel Execution

Sei executes EVM transactions in parallel using optimistic concurrency control. No Solidity changes needed.

1. Transactions are ordered by the consensus layer
2. Multiple threads execute transactions concurrently against an optimistic state
3. SeiDB tracks read/write sets for each transaction
4. Conflicts detected at commit time -- conflicting transactions are re-executed
5. Results committed in original transaction order (deterministic)

### Parallel-Friendly Contract Design

| Pattern | Parallelizes Well | Why |
|---------|-------------------|-----|
| Per-user mappings (`mapping(address => uint256)`) | Yes | Independent storage slots per user |
| ERC-20 transfers between different pairs | Yes | Different balance slots accessed |
| Global counter increment | No | All transactions write same slot |
| AMM swaps on same pool | No | Same reserves storage slot |
| Independent NFT mints with per-user counters | Yes | Avoids shared tokenId counter |

## Precompile Contracts

Sei provides precompile contracts for accessing Cosmos-native functionality from Solidity. These are callable like normal contracts but execute native chain logic.

Only `CALL` is supported for state-changing precompiles. `DELEGATECALL` and `STATICCALL` may not work for write operations.

### Address Precompile

Address: `0x0000000000000000000000000000000000001004`

Converts between EVM (0x) and Cosmos (sei1...) address formats.

```solidity
interface IAddrPrecompile {
    function getSeiAddr(address evmAddr) external view returns (string memory);
    function getEvmAddr(string memory seiAddr) external view returns (address);
}
```

```solidity
IAddrPrecompile constant ADDR = IAddrPrecompile(0x0000000000000000000000000000000000001004);

function lookupCosmosAddress(address evmAddr) external view returns (string memory) {
    return ADDR.getSeiAddr(evmAddr);
}

function lookupEvmAddress(string calldata seiAddr) external view returns (address) {
    return ADDR.getEvmAddr(seiAddr);
}
```

### Staking Precompile

Address: `0x0000000000000000000000000000000000001005`

Delegate, undelegate, and claim staking rewards from EVM contracts.

```solidity
interface IStaking {
    function delegate(string memory validator) external payable returns (bool);
    function undelegate(string memory validator, uint256 amount) external returns (bool);
    function redelegate(
        string memory srcValidator,
        string memory dstValidator,
        uint256 amount
    ) external returns (bool);
}
```

```solidity
IStaking constant STAKING = IStaking(0x0000000000000000000000000000000000001005);

function stake(string calldata validator) external payable {
    bool success = STAKING.delegate{value: msg.value}(validator);
    require(success, "Delegation failed");
}
```

### Governance Precompile

Address: `0x0000000000000000000000000000000000001006`

Vote on Cosmos governance proposals from EVM.

```solidity
interface IGov {
    function vote(uint64 proposalId, int32 option) external returns (bool);
    function deposit(uint64 proposalId) external payable returns (bool);
}
```

Vote options: `1` = Yes, `2` = Abstain, `3` = No, `4` = NoWithVeto.

### Distribution Precompile

Address: `0x0000000000000000000000000000000000001007`

Claim staking rewards.

```solidity
interface IDistribution {
    function withdrawDelegationRewards(string memory validator) external returns (bool);
    function setWithdrawAddress(address newAddress) external returns (bool);
}
```

### IBC Precompile

Address: `0x0000000000000000000000000000000000001009`

Transfer tokens cross-chain via IBC directly from EVM contracts.

```solidity
interface IIBC {
    function transfer(
        string memory toAddress,
        string memory port,
        string memory channel,
        string memory denom,
        uint256 amount,
        uint64 revisionNumber,
        uint64 revisionHeight,
        uint64 timeoutTimestamp
    ) external returns (bool);
}
```

```solidity
IIBC constant IBC = IIBC(0x0000000000000000000000000000000000001009);

function ibcTransfer(
    string calldata toAddress,
    string calldata channel,
    uint256 amount
) external {
    // Timeout: 10 minutes from now in nanoseconds
    uint64 timeout = uint64(block.timestamp + 600) * 1_000_000_000;
    bool success = IBC.transfer(
        toAddress,
        "transfer",
        channel,
        "usei",
        amount,
        0,
        0,
        timeout
    );
    require(success, "IBC transfer failed");
}
```

### JSON Precompile

Address: `0x0000000000000000000000000000000000001003`

Parse JSON strings on-chain. Useful for processing CosmWasm query responses in EVM.

```solidity
interface IJson {
    function extractAsBytes(bytes memory input, string memory key) external view returns (bytes memory);
    function extractAsBytesList(bytes memory input, string memory key) external view returns (bytes[] memory);
    function extractAsUint256(bytes memory input, string memory key) external view returns (uint256);
}
```

### Precompile Address Summary

| Precompile | Address | Purpose |
|------------|---------|---------|
| Bank | `0x0000000000000000000000000000000000001001` | Send native Cosmos tokens |
| JSON | `0x0000000000000000000000000000000000001003` | Parse JSON on-chain |
| Address | `0x0000000000000000000000000000000000001004` | Convert EVM <> Cosmos addresses |
| Staking | `0x0000000000000000000000000000000000001005` | Delegate/undelegate/redelegate |
| Governance | `0x0000000000000000000000000000000000001006` | Vote on proposals |
| Distribution | `0x0000000000000000000000000000000000001007` | Claim staking rewards |
| IBC | `0x0000000000000000000000000000000000001009` | Cross-chain IBC transfers |
| Pointer | `0x000000000000000000000000000000000000100b` | Query/register pointer contracts |
| Wasm | `0x0000000000000000000000000000000000001002` | Call CosmWasm contracts from EVM |

## Pointer Contracts

Pointer contracts are the mechanism for EVM<>CosmWasm token interoperability. They are lightweight proxy contracts that allow a token created in one execution environment to be accessed in the other.

### How Pointers Work

1. A CW20 token is deployed on Sei's CosmWasm runtime
2. Anyone calls the Pointer precompile to register a pointer ERC20 for that CW20
3. The pointer ERC20 contract appears at a deterministic address
4. EVM users interact with the pointer ERC20 -- calls are forwarded to the underlying CW20
5. Balances, transfers, and approvals are mirrored across both environments

The same works in reverse: an ERC20 can get a pointer CW20.

### Querying Pointer Contracts

```solidity
interface IPointer {
    function getPointer(uint16 pointerType, string memory tokenId) external view returns (address, uint16, bool);
}
```

`pointerType` values:
- `0` = ERC20 pointer for a CW20 token
- `1` = ERC721 pointer for a CW721 token
- `2` = CW20 pointer for an ERC20 token
- `3` = CW721 pointer for an ERC721 token
- `4` = ERC20 pointer for a native/IBC denom

```solidity
IPointer constant POINTER = IPointer(0x000000000000000000000000000000000000100b);

// Get the ERC20 address for a CW20 token
function getCW20Pointer(string calldata cw20Addr) external view returns (address) {
    (address pointerAddr, , bool exists) = POINTER.getPointer(0, cw20Addr);
    require(exists, "Pointer not registered");
    return pointerAddr;
}

// Get the ERC20 address for a native Cosmos denom
function getNativeDenomPointer(string calldata denom) external view returns (address) {
    (address pointerAddr, , bool exists) = POINTER.getPointer(4, denom);
    require(exists, "Pointer not registered");
    return pointerAddr;
}
```

## Associated Balances

EVM addresses on Sei can hold Cosmos-native tokens (usei, IBC denoms, TokenFactory tokens) directly. These are called "associated balances" because the 0x address is associated with its corresponding sei1... address.

### How It Works

1. Every EVM address has a deterministic Cosmos address (and vice versa)
2. The Address precompile converts between formats
3. When Cosmos-native tokens are sent to the sei1... address, they appear as associated balances on the 0x address
4. The Bank precompile allows EVM contracts to send these native tokens

### Reading Associated Balances

```typescript
import { createPublicClient, http, parseAbi } from "viem";
import { sei } from "./chains";

const client = createPublicClient({ chain: sei, transport: http() });

const bankAbi = parseAbi([
  "function balance(address account, string denom) view returns (uint256)",
  "function all_balances(address account) view returns ((uint256, string)[])",
]);

const BANK = "0x0000000000000000000000000000000000001001" as const;

const seiBalance = await client.readContract({
  address: BANK,
  abi: bankAbi,
  functionName: "balance",
  args: ["0xYourAddress", "usei"],
});

// seiBalance is in usei (6 decimals on Cosmos side)
```

### Sending Native Tokens from EVM

```solidity
interface IBank {
    function send(
        address fromAddress,
        address toAddress,
        string memory denom,
        uint256 amount
    ) external returns (bool);
    function balance(address account, string memory denom) external view returns (uint256);
}

IBank constant BANK = IBank(0x0000000000000000000000000000000000001001);
```

## Calling CosmWasm from EVM

The Wasm precompile lets EVM contracts execute and query CosmWasm contracts.

Address: `0x0000000000000000000000000000000000001002`

```solidity
interface IWasm {
    function instantiate(
        uint64 codeID,
        string memory admin,
        bytes memory msg,
        string memory label,
        bytes memory coins
    ) external returns (string memory contractAddr);

    function execute(
        string memory contractAddress,
        bytes memory msg,
        bytes memory coins
    ) external returns (bytes memory response);

    function query(
        string memory contractAddress,
        bytes memory req
    ) external view returns (bytes memory response);
}
```

```solidity
IWasm constant WASM = IWasm(0x0000000000000000000000000000000000001002);

function queryCosmWasmContract(
    string calldata contractAddr,
    bytes calldata queryMsg
) external view returns (bytes memory) {
    return WASM.query(contractAddr, queryMsg);
}

function executeCosmWasmContract(
    string calldata contractAddr,
    bytes calldata executeMsg,
    bytes calldata coins
) external returns (bytes memory) {
    return WASM.execute(contractAddr, executeMsg, coins);
}
```

## SEI Token Decimals

SEI has different decimal representations depending on context:

| Context | Denom | Decimals | 1 SEI = |
|---------|-------|----------|---------|
| EVM (msg.value, balanceOf) | wei | 18 | 1e18 |
| Cosmos (bank module) | usei | 6 | 1,000,000 |
| Display | SEI | 0 | 1 |

When transferring between EVM and Cosmos contexts, the chain handles decimal conversion automatically. Pointer contracts and precompiles handle the 18<>6 decimal conversion internally.

## Gas Optimization Tips

1. **Design for parallel execution** -- per-user mappings over global counters
2. **Use precompiles for Cosmos operations** -- cheaper than external contract calls through CosmWasm
3. **Batch via multicall** -- reduces per-transaction overhead
4. **Set `evmVersion: "paris"`** -- avoids PUSH0 opcode errors
5. **Keep contracts under 24.576 KB** -- standard EVM limit applies
6. **Minimize storage writes to shared slots** -- reduces parallel execution conflicts

## Pre-Deployment Checklist

- [ ] `evmVersion: "paris"` in compiler config (no PUSH0)
- [ ] Correct chain ID (1329 mainnet / 1328 testnet)
- [ ] Account funded with SEI for gas
- [ ] Private key in environment variable, not hardcoded
- [ ] Contract size under 24.576 KB
- [ ] All Solidity follows CEI pattern (Checks-Effects-Interactions)
- [ ] `bigint` used for all token amounts in TypeScript
- [ ] `msg.sender` used for auth (never `tx.origin`)
- [ ] Verified on Seitrace after deployment
- [ ] Tested pointer contract interaction if using EVM<>CosmWasm interop

## Additional Reference

| File | Contents |
|------|----------|
| `examples/deploy-contract/README.md` | Foundry + Hardhat deploy on Sei |
| `examples/native-dex-order/README.md` | EVM DEX swap on Sei |
| `examples/evm-cosmwasm-interop/README.md` | Pointer contracts, precompile calls |
| `examples/read-chain-state/README.md` | Reading balances, precompile queries, associated balances |
| `resources/contract-addresses.md` | Precompile and token addresses |
| `resources/error-codes.md` | Common errors and fixes |
| `resources/chain-config.md` | Chain IDs, RPCs, explorers |
| `docs/troubleshooting.md` | Common Sei development issues |
| `templates/sei-client.ts` | viem client setup for Sei |

## References

- Sei Docs: https://docs.sei.io
- Sei EVM Docs: https://docs.sei.io/dev-tutorials/evm-general
- Sei Interoperability: https://docs.sei.io/dev-advanced-concepts/interoperability
- Seitrace Explorer: https://seitrace.com
- Sei GitHub: https://github.com/sei-protocol
