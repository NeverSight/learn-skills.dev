---
name: base
description: Base L2 development (Coinbase) — deployment, OnchainKit, Paymaster (gasless transactions), Smart Wallet, Base Account SDK, and OP Stack integration. Built on Optimism's OP Stack.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: base
  category: L2 & Alt-L1
tags:
  - base
  - coinbase
  - layer-2
  - op-stack
  - onchainkit
  - smart-wallet
---

# Base L2 Development

Base is Coinbase's L2 built on Optimism's OP Stack. It shares Ethereum security, uses ETH as gas, and settles to L1. If you can deploy to Ethereum, you can deploy to Base with zero code changes — just point at a different RPC.

## What You Probably Got Wrong

- **Base is NOT a separate EVM** — It is an OP Stack rollup. Same opcodes, same Solidity compiler, same tooling. There is nothing "Base-specific" about contract development. If your contract works on Ethereum or Optimism, it works on Base.
- **Gas has two components** — L2 execution gas (cheap, ~0.001 gwei base fee) plus L1 data fee (variable, depends on Ethereum blob fees). The L1 data fee is the dominant cost for most transactions. After EIP-4844 (Dencun), L1 data costs dropped ~100x.
- **msg.sender works differently with Smart Wallet** — Coinbase Smart Wallet is a smart contract account (ERC-4337). `msg.sender` is the smart wallet address, not the EOA. If your contract checks `tx.origin == msg.sender` to block contracts, it will block Smart Wallet users.
- **OnchainKit is NOT a wallet library** — It is a React component library for building Base-native UIs. It handles identity resolution, transaction submission, token swaps, and Farcaster frames. You still need wagmi/viem for the underlying wallet connection.
- **Paymaster does NOT mean free transactions** — A paymaster sponsors gas on behalf of users. Someone still pays. You configure a Coinbase Developer Platform paymaster policy that defines which contracts and methods are sponsored, with spend limits.
- **Block time is 2 seconds** — Not 12 seconds like Ethereum L1. Plan your polling and confirmation logic accordingly.
- **Basescan and Blockscout are both available** — Basescan (Etherscan-based) is the primary explorer. Blockscout is the alternative. Contract verification works on both but uses different APIs.

## Quick Start

```bash
# Add Base to Foundry project
forge create src/Counter.sol:Counter \
  --rpc-url https://mainnet.base.org \
  --private-key $PRIVATE_KEY

# Check balance
cast balance $ADDRESS --rpc-url https://mainnet.base.org

# Deploy to testnet
forge script script/Deploy.s.sol \
  --rpc-url https://sepolia.base.org \
  --broadcast --verify \
  --etherscan-api-key $BASESCAN_API_KEY
```

```typescript
import { createPublicClient, createWalletClient, http } from 'viem';
import { base, baseSepolia } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';

const publicClient = createPublicClient({
  chain: base,
  transport: http(),
});

const walletClient = createWalletClient({
  chain: base,
  transport: http(),
  account: privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`),
});

const blockNumber = await publicClient.getBlockNumber();
```

## Chain Configuration

### Base Mainnet

| Parameter | Value |
|-----------|-------|
| Chain ID | 8453 |
| Currency | ETH |
| RPC (public) | `https://mainnet.base.org` |
| RPC (Coinbase) | `https://api.developer.coinbase.com/rpc/v1/base/$CDP_API_KEY` |
| WebSocket | `wss://mainnet.base.org` |
| Explorer | `https://basescan.org` |
| Blockscout | `https://base.blockscout.com` |
| Bridge | `https://bridge.base.org` |
| Block time | 2 seconds |
| Finality | ~12 minutes (L1 finality) |

### Base Sepolia (Testnet)

| Parameter | Value |
|-----------|-------|
| Chain ID | 84532 |
| Currency | ETH |
| RPC (public) | `https://sepolia.base.org` |
| RPC (Coinbase) | `https://api.developer.coinbase.com/rpc/v1/base-sepolia/$CDP_API_KEY` |
| Explorer | `https://sepolia.basescan.org` |
| Faucet | `https://www.coinbase.com/faucets/base-ethereum-goerli-faucet` |

### Viem Chain Definitions

viem includes Base chains out of the box:

```typescript
import { base, baseSepolia } from 'viem/chains';

// base.id === 8453
// baseSepolia.id === 84532
```

### Hardhat Network Config

```typescript
// hardhat.config.ts
const config: HardhatUserConfig = {
  networks: {
    base: {
      url: process.env.BASE_RPC_URL || 'https://mainnet.base.org',
      accounts: [process.env.PRIVATE_KEY!],
      chainId: 8453,
    },
    baseSepolia: {
      url: process.env.BASE_SEPOLIA_RPC_URL || 'https://sepolia.base.org',
      accounts: [process.env.PRIVATE_KEY!],
      chainId: 84532,
    },
  },
  etherscan: {
    apiKey: {
      base: process.env.BASESCAN_API_KEY!,
      baseSepolia: process.env.BASESCAN_API_KEY!,
    },
    customChains: [
      {
        network: 'base',
        chainId: 8453,
        urls: {
          apiURL: 'https://api.basescan.org/api',
          browserURL: 'https://basescan.org',
        },
      },
      {
        network: 'baseSepolia',
        chainId: 84532,
        urls: {
          apiURL: 'https://api-sepolia.basescan.org/api',
          browserURL: 'https://sepolia.basescan.org',
        },
      },
    ],
  },
};
```

### Foundry Config

```toml
# foundry.toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]

[rpc_endpoints]
base = "https://mainnet.base.org"
base_sepolia = "https://sepolia.base.org"

[etherscan]
base = { key = "${BASESCAN_API_KEY}", url = "https://api.basescan.org/api", chain = 8453 }
base_sepolia = { key = "${BASESCAN_API_KEY}", url = "https://api-sepolia.basescan.org/api", chain = 84532 }
```

## Deployment

Base uses the OP Stack. Deployment is identical to Ethereum — no special compiler flags, no custom precompiles for basic use cases.

### Foundry

```bash
# Deploy to Base Sepolia
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://sepolia.base.org \
  --broadcast \
  --verify \
  --etherscan-api-key $BASESCAN_API_KEY

# Deploy to Base Mainnet
forge script script/Deploy.s.sol:DeployScript \
  --rpc-url https://mainnet.base.org \
  --broadcast \
  --verify \
  --etherscan-api-key $BASESCAN_API_KEY \
  --slow
```

### Verification on Basescan

```bash
# Verify after deployment
forge verify-contract $CONTRACT_ADDRESS src/MyContract.sol:MyContract \
  --chain base \
  --etherscan-api-key $BASESCAN_API_KEY

# With constructor args
forge verify-contract $CONTRACT_ADDRESS src/MyContract.sol:MyContract \
  --chain base \
  --etherscan-api-key $BASESCAN_API_KEY \
  --constructor-args $(cast abi-encode "constructor(address,uint256)" $TOKEN_ADDR 1000)

# Verify on Blockscout (no API key needed)
forge verify-contract $CONTRACT_ADDRESS src/MyContract.sol:MyContract \
  --chain base \
  --verifier blockscout \
  --verifier-url https://base.blockscout.com/api/
```

## OnchainKit

OnchainKit is Coinbase's React component library for building onchain apps on Base. It provides ready-made components for identity, transactions, swaps, wallets, and Farcaster frames.

### Installation

```bash
npm install @coinbase/onchainkit
# Peer dependencies
npm install viem wagmi @tanstack/react-query
```

### Provider Setup

```tsx
import { OnchainKitProvider } from '@coinbase/onchainkit';
import { base } from 'viem/chains';

function App({ children }: { children: React.ReactNode }) {
  return (
    <OnchainKitProvider
      apiKey={process.env.NEXT_PUBLIC_CDP_API_KEY}
      chain={base}
    >
      {children}
    </OnchainKitProvider>
  );
}
```

### Identity Components

Resolve onchain identity (ENS, Basenames, Farcaster):

```tsx
import {
  Identity,
  Name,
  Avatar,
  Badge,
  Address,
} from '@coinbase/onchainkit/identity';

function UserProfile({ address }: { address: `0x${string}` }) {
  return (
    <Identity address={address} schemaId="0x...">
      <Avatar />
      <Name>
        <Badge />
      </Name>
      <Address />
    </Identity>
  );
}
```

### Transaction Component

Submit transactions with built-in status tracking:

```tsx
import { Transaction, TransactionButton, TransactionStatus } from '@coinbase/onchainkit/transaction';
import { baseSepolia } from 'viem/chains';

const contracts = [
  {
    address: '0xContractAddress' as `0x${string}`,
    abi: contractAbi,
    functionName: 'mint',
    args: [1n],
  },
];

function MintButton() {
  return (
    <Transaction
      chainId={baseSepolia.id}
      contracts={contracts}
      onStatus={(status) => console.log('tx status:', status)}
    >
      <TransactionButton text="Mint NFT" />
      <TransactionStatus />
    </Transaction>
  );
}
```

### Swap Component

Token swaps powered by 0x/Uniswap:

```tsx
import { Swap, SwapAmountInput, SwapButton, SwapToggle } from '@coinbase/onchainkit/swap';
import type { Token } from '@coinbase/onchainkit/token';

const ETH: Token = {
  name: 'Ethereum',
  address: '',
  symbol: 'ETH',
  decimals: 18,
  image: 'https://...',
  chainId: 8453,
};

const USDC: Token = {
  name: 'USD Coin',
  address: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
  symbol: 'USDC',
  decimals: 6,
  image: 'https://...',
  chainId: 8453,
};

function SwapWidget() {
  return (
    <Swap>
      <SwapAmountInput label="Sell" token={ETH} type="from" />
      <SwapToggle />
      <SwapAmountInput label="Buy" token={USDC} type="to" />
      <SwapButton />
    </Swap>
  );
}
```

### Wallet Component

```tsx
import {
  ConnectWallet,
  Wallet,
  WalletDropdown,
  WalletDropdownDisconnect,
} from '@coinbase/onchainkit/wallet';

function WalletConnect() {
  return (
    <Wallet>
      <ConnectWallet>
        <Avatar />
        <Name />
      </ConnectWallet>
      <WalletDropdown>
        <Identity />
        <WalletDropdownDisconnect />
      </WalletDropdown>
    </Wallet>
  );
}
```

## Smart Wallet

Coinbase Smart Wallet is a smart contract wallet using passkeys (WebAuthn) for authentication. It follows ERC-4337 (account abstraction) so users do not need a seed phrase or browser extension.

### How It Works

1. User creates wallet via passkey (fingerprint, Face ID, or security key)
2. A smart contract wallet is deployed on Base (counterfactual — deployed on first transaction)
3. Transactions are signed with the passkey and submitted as UserOperations
4. Compatible with ERC-4337 bundlers and paymasters

### wagmi + Smart Wallet

```typescript
import { http, createConfig } from 'wagmi';
import { base, baseSepolia } from 'wagmi/chains';
import { coinbaseWallet } from 'wagmi/connectors';

export const config = createConfig({
  chains: [base, baseSepolia],
  connectors: [
    coinbaseWallet({
      appName: 'My Base App',
      // preference: 'smartWalletOnly' forces smart wallet (no extension)
      preference: 'smartWalletOnly',
    }),
  ],
  transports: {
    [base.id]: http(),
    [baseSepolia.id]: http(),
  },
});
```

### Sending Transactions from Smart Wallet

```typescript
import { useWriteContract } from 'wagmi';

function MintWithSmartWallet() {
  const { writeContract } = useWriteContract();

  const handleMint = () => {
    writeContract({
      address: '0xContractAddress',
      abi: contractAbi,
      functionName: 'mint',
      args: [1n],
    });
  };

  return <button onClick={handleMint}>Mint</button>;
}
```

### Batch Transactions (EIP-5792)

Smart Wallet supports `wallet_sendCalls` for atomic batching:

```typescript
import { useWriteContracts } from 'wagmi/experimental';

function BatchMint() {
  const { writeContracts } = useWriteContracts();

  const handleBatch = () => {
    writeContracts({
      contracts: [
        {
          address: '0xTokenAddress',
          abi: erc20Abi,
          functionName: 'approve',
          args: ['0xSpender', 1000000n],
        },
        {
          address: '0xSpender',
          abi: spenderAbi,
          functionName: 'deposit',
          args: [1000000n],
        },
      ],
    });
  };

  return <button onClick={handleBatch}>Approve + Deposit</button>;
}
```

## Paymaster (Gasless Transactions)

A paymaster sponsors gas fees so users pay zero gas. Coinbase Developer Platform provides a paymaster service for Base.

### Setup

1. Create a project at [portal.cdp.coinbase.com](https://portal.cdp.coinbase.com)
2. Enable the Paymaster service
3. Configure a paymaster policy (which contracts/methods to sponsor)
4. Get your paymaster URL: `https://api.developer.coinbase.com/rpc/v1/base/$CDP_API_KEY`

### wagmi + Paymaster (EIP-5792)

```typescript
import { useWriteContracts } from 'wagmi/experimental';
import { base } from 'viem/chains';

const PAYMASTER_URL = `https://api.developer.coinbase.com/rpc/v1/base/${process.env.NEXT_PUBLIC_CDP_API_KEY}`;

function SponsoredMint() {
  const { writeContracts } = useWriteContracts();

  const handleMint = () => {
    writeContracts({
      contracts: [
        {
          address: '0xContractAddress',
          abi: contractAbi,
          functionName: 'mint',
          args: [1n],
        },
      ],
      capabilities: {
        paymasterService: {
          url: PAYMASTER_URL,
        },
      },
    });
  };

  return <button onClick={handleMint}>Mint (Gasless)</button>;
}
```

### Viem + Paymaster (Direct UserOperation)

```typescript
import { createPublicClient, http, encodeFunctionData } from 'viem';
import { base } from 'viem/chains';

const PAYMASTER_URL = `https://api.developer.coinbase.com/rpc/v1/base/${process.env.CDP_API_KEY}`;

async function sponsoredCall(
  smartWalletAddress: `0x${string}`,
  target: `0x${string}`,
  calldata: `0x${string}`
) {
  const client = createPublicClient({
    chain: base,
    transport: http(),
  });

  // pm_getPaymasterStubData returns gas estimates for the UserOp
  const paymasterResponse = await fetch(PAYMASTER_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 1,
      method: 'pm_getPaymasterStubData',
      params: [
        {
          sender: smartWalletAddress,
          callData: calldata,
          callGasLimit: '0x0',
          verificationGasLimit: '0x0',
          preVerificationGas: '0x0',
          maxFeePerGas: '0x0',
          maxPriorityFeePerGas: '0x0',
        },
        // EntryPoint v0.7
        '0x0000000071727De22E5E9d8BAf0edAc6f37da032',
        `0x${base.id.toString(16)}`,
      ],
    }),
  });

  return paymasterResponse.json();
}
```

### Paymaster Policy

Configure which transactions are sponsored in the Coinbase Developer Platform dashboard:

- **Contract allowlist** — Only sponsor calls to specific contract addresses
- **Method allowlist** — Only sponsor specific function selectors
- **Spend limits** — Max gas per user per day/week/month
- **Rate limits** — Max sponsored txs per user per time window

## Bridging

Base uses the OP Stack standard bridge. ETH and ERC-20 tokens can be bridged between Ethereum L1 and Base L2.

### Bridge ETH to Base (L1 -> L2)

```typescript
import { createWalletClient, http, parseEther } from 'viem';
import { mainnet } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';

// OptimismPortal on L1 (Ethereum mainnet)
const OPTIMISM_PORTAL = '0x49048044D57e1C92A77f79988d21Fa8fAF36f97B' as const;

const walletClient = createWalletClient({
  chain: mainnet,
  transport: http(),
  account: privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`),
});

// Deposit ETH to Base — sends to OptimismPortal with value
const hash = await walletClient.sendTransaction({
  to: OPTIMISM_PORTAL,
  value: parseEther('0.1'),
  // depositTransaction calldata for simple ETH transfer
  data: '0x',
});
// ETH arrives on Base in ~1-5 minutes
```

### Bridge ETH from Base (L2 -> L1)

L2-to-L1 withdrawals follow the OP Stack withdrawal flow:

1. **Initiate withdrawal** on L2 (sends message to L2ToL1MessagePasser)
2. **Wait for state root** to be posted on L1 (~1 hour)
3. **Prove withdrawal** on L1 (submit Merkle proof)
4. **Wait for challenge period** (~7 days on mainnet)
5. **Finalize withdrawal** on L1

```typescript
import { createPublicClient, createWalletClient, http, parseEther } from 'viem';
import { base } from 'viem/chains';

// L2ToL1MessagePasser predeploy on Base
const L2_TO_L1_MESSAGE_PASSER = '0x4200000000000000000000000000000000000016' as const;

const l2WalletClient = createWalletClient({
  chain: base,
  transport: http(),
  account: privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`),
});

// Step 1: Initiate withdrawal on L2
const hash = await l2WalletClient.writeContract({
  address: L2_TO_L1_MESSAGE_PASSER,
  abi: [
    {
      name: 'initiateWithdrawal',
      type: 'function',
      stateMutability: 'payable',
      inputs: [
        { name: '_target', type: 'address' },
        { name: '_gasLimit', type: 'uint256' },
        { name: '_data', type: 'bytes' },
      ],
      outputs: [],
    },
  ],
  functionName: 'initiateWithdrawal',
  args: [
    l2WalletClient.account.address, // send to self on L1
    100_000n, // L1 gas limit for the relay
    '0x',
  ],
  value: parseEther('0.1'),
});
// Steps 2-4 require waiting and L1 transactions (use the Base Bridge UI or OP SDK)
```

## Gas Model

Base follows the OP Stack gas model: **L2 execution fee + L1 data fee**.

### L2 Execution Fee

Same as Ethereum: `gasUsed * baseFee`. Base uses EIP-1559 with a 2-second block time. Base fees are typically very low (0.001-0.01 gwei).

### L1 Data Fee

Every L2 transaction is posted to Ethereum L1 as calldata or blobs. The L1 data fee covers this cost.

After EIP-4844 (Dencun upgrade, March 2024), L1 data is posted as blobs, reducing costs ~100x.

```typescript
import { createPublicClient, http } from 'viem';
import { base } from 'viem/chains';

// GasPriceOracle predeploy
const GAS_PRICE_ORACLE = '0x420000000000000000000000000000000000000F' as const;

const gasPriceOracleAbi = [
  {
    name: 'getL1Fee',
    type: 'function',
    stateMutability: 'view',
    inputs: [{ name: '_data', type: 'bytes' }],
    outputs: [{ name: '', type: 'uint256' }],
  },
  {
    name: 'baseFeeScalar',
    type: 'function',
    stateMutability: 'view',
    inputs: [],
    outputs: [{ name: '', type: 'uint32' }],
  },
  {
    name: 'blobBaseFeeScalar',
    type: 'function',
    stateMutability: 'view',
    inputs: [],
    outputs: [{ name: '', type: 'uint32' }],
  },
] as const;

const client = createPublicClient({ chain: base, transport: http() });

// Estimate L1 data fee for a transaction
const l1Fee = await client.readContract({
  address: GAS_PRICE_ORACLE,
  abi: gasPriceOracleAbi,
  functionName: 'getL1Fee',
  args: ['0x...serializedTxData'],
});
```

### Gas Estimation Tips

- Total cost = L2 execution fee + L1 data fee
- L1 data fee dominates for simple transactions
- Minimize calldata size to reduce L1 costs (pack structs, use shorter data)
- `eth_estimateGas` returns L2 gas only — add L1 data fee separately
- viem's `estimateTotalFee` on OP Stack chains handles both components

## Ecosystem

### Major Base Protocols

| Protocol | Category | Description |
|----------|----------|-------------|
| Aerodrome | DEX | Dominant DEX on Base (ve(3,3) model, Velodrome fork) |
| Uniswap V3 | DEX | Deployed on Base with full feature set |
| Aave V3 | Lending | Lending/borrowing on Base |
| Compound III | Lending | USDC lending market |
| Extra Finance | Yield | Leveraged yield farming |
| Moonwell | Lending | Fork of Compound, native to Base |
| Seamless | Lending | Integrated lending protocol |
| BaseSwap | DEX | Native Base DEX |
| Morpho | Lending | Permissionless lending vaults |

### Key Token Addresses (Base Mainnet)

| Token | Address |
|-------|---------|
| WETH | `0x4200000000000000000000000000000000000006` |
| USDC (native) | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| USDbC (bridged) | `0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6D` |
| cbETH | `0x2Ae3F1Ec7F1F5012CFEab0185bfc7aa3cf0DEc22` |
| DAI | `0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb` |
| AERO | `0x940181a94A35A4569E4529A3CDfB74e38FD98631` |

> Last verified: 2025-04. Always verify onchain with `cast code <address> --rpc-url https://mainnet.base.org` before production use.

## Key Differences from Other OP Stack Chains

| Aspect | Base | Optimism | Other OP Chains |
|--------|------|----------|-----------------|
| Sequencer operator | Coinbase | Optimism Foundation | Varies |
| Fee recipient | Coinbase multisig | Optimism Foundation | Varies |
| Smart Wallet | Native Coinbase integration | Not default | Not default |
| Paymaster | Coinbase Developer Platform | Third-party only | Third-party only |
| OnchainKit | Full support | Partial (identity only) | None |
| Superchain membership | Yes | Yes (leader) | Varies |
| Fault proofs | Stage 1 (planned) | Stage 1 | Varies |

## Useful Commands

```bash
# Check L1 data fee for a tx
cast call 0x420000000000000000000000000000000000000F \
  "getL1Fee(bytes)(uint256)" 0x... \
  --rpc-url https://mainnet.base.org

# Read GasPriceOracle scalars
cast call 0x420000000000000000000000000000000000000F \
  "baseFeeScalar()(uint32)" \
  --rpc-url https://mainnet.base.org

# Check if address is a contract (smart wallet check)
cast code $ADDRESS --rpc-url https://mainnet.base.org

# Get current L2 base fee
cast base-fee --rpc-url https://mainnet.base.org

# Decode L1 batch data
cast call 0x4200000000000000000000000000000000000015 \
  "l1BlockNumber()(uint64)" \
  --rpc-url https://mainnet.base.org
```

## References

- Base Docs: https://docs.base.org
- OnchainKit: https://onchainkit.xyz
- Coinbase Developer Platform: https://portal.cdp.coinbase.com
- Basescan: https://basescan.org
- Base Bridge: https://bridge.base.org
- OP Stack Docs: https://docs.optimism.io
- ERC-4337 Spec: https://eips.ethereum.org/EIPS/eip-4337
- EIP-5792 (wallet_sendCalls): https://eips.ethereum.org/EIPS/eip-5792
