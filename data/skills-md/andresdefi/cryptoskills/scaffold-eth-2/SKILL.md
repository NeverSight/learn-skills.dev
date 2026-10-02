---
name: scaffold-eth-2
description: "Full-stack dApp development framework — quick start with npx create-eth@latest, Foundry/Hardhat monorepo, custom React hooks (useScaffoldWriteContract, useScaffoldReadContract, useDeployedContractInfo, useTransactor), contract hot reload, auto-generated debug page, three-phase build (Local to Testnet to Production), external contract integration, and deployment patterns."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: ethereum
  category: Dev Tools
tags:
  - scaffold-eth
  - dapp
  - full-stack
  - foundry
  - hardhat
  - react
  - nextjs
  - rapid-prototyping
---

# Scaffold-ETH 2

Full-stack Ethereum dApp development framework. Monorepo with Foundry (or Hardhat) for contracts and Next.js for the frontend. Ships custom React hooks that auto-wire contract ABIs and addresses from deployment artifacts -- no manual ABI imports, no address management. Includes an auto-generated debug page that gives you read/write UI for every public function on every deployed contract.

## What You Probably Got Wrong

> Agents trained on pre-2024 data generate Scaffold-ETH 1 code. SE2 is a complete rewrite -- different stack, different hooks, different project structure. Every pattern below is SE2-specific.

- **SE2 is NOT SE1** -- SE1 used Create React App + ethers.js + Hardhat. SE2 uses Next.js 14+ + wagmi + viem + Foundry (default). The codebases share nothing. If you see `useContractReader` or `scaffold-eth/hooks`, that is SE1 and will not work.
- **Foundry is the default, not Hardhat** -- `npx create-eth@latest` defaults to Foundry. Hardhat is available via `--hardhat` flag but Foundry is the recommended path. Do not assume Hardhat unless the user explicitly chose it.
- **Hooks read from `deployedContracts.ts`, not raw ABI + address** -- SE2 hooks take `contractName` as a string (e.g., `"YourContract"`). The hook resolves the ABI and address from the auto-generated `deployedContracts.ts` file. Never pass `address` and `abi` directly to SE2 hooks.
- **The debug page reads AND writes** -- It auto-generates a UI for ALL public/external functions on every deployed contract. You can call view functions and send transactions directly from the browser. This is not just a read-only viewer.
- **You do NOT need to write frontend boilerplate** -- SE2 hooks handle wallet connection, transaction lifecycle, error display, and loading states. A complete contract interaction is 5-10 lines of JSX. Do not recreate wagmi provider setup or wallet connect logic.
- **`yarn deploy` regenerates `deployedContracts.ts`** -- Every time you deploy, the contract addresses and ABIs are written to `packages/nextjs/contracts/deployedContracts.ts`. The frontend picks up changes on next page load (hot reload in dev).
- **`externalContracts.ts` is for contracts you did NOT deploy** -- To interact with Uniswap, Aave, or any already-deployed protocol, add the ABI and address to `externalContracts.ts`. SE2 hooks then treat them the same as your own contracts.

## Quick Start

### Create a New Project

```bash
npx create-eth@latest
```

The CLI prompts for project name and framework choice (Foundry or Hardhat). Foundry is the default.

### Start Development

```bash
cd your-project

# Terminal 1: Start local chain
yarn chain

# Terminal 2: Deploy contracts
yarn deploy

# Terminal 3: Start frontend
yarn start
```

The frontend runs at `http://localhost:3000`. The debug page is at `http://localhost:3000/debug`.

### With Hardhat Instead

```bash
npx create-eth@latest --hardhat
```

Same commands apply. The only difference is `packages/hardhat` instead of `packages/foundry`.

## Project Structure

```
your-project/
├── packages/
│   ├── foundry/                      # Smart contracts (default)
│   │   ├── contracts/                # Solidity source files
│   │   ├── script/                   # Deploy scripts (Deploy.s.sol)
│   │   ├── test/                     # Foundry tests
│   │   └── foundry.toml              # Foundry configuration
│   │
│   └── nextjs/                       # Frontend
│       ├── app/                      # Next.js App Router pages
│       │   ├── page.tsx              # Home page
│       │   ├── debug/                # Auto-generated debug page
│       │   └── blockexplorer/        # Built-in block explorer
│       ├── components/               # Reusable UI components
│       │   └── scaffold-eth/         # SE2 component library
│       ├── contracts/
│       │   ├── deployedContracts.ts  # Auto-generated from deploys
│       │   └── externalContracts.ts  # Manually added external ABIs
│       ├── hooks/
│       │   └── scaffold-eth/         # SE2 custom hooks
│       ├── utils/
│       │   └── scaffold-eth/         # SE2 utilities
│       └── scaffold.config.ts        # Global SE2 configuration
│
├── package.json                      # Workspace root
└── yarn.lock
```

### Key Files

| File | Purpose |
|------|---------|
| `scaffold.config.ts` | Target network, polling interval, wallet autoconnect |
| `deployedContracts.ts` | Auto-generated ABI + address map keyed by chainId and contract name |
| `externalContracts.ts` | Manually configured ABIs for third-party contracts |
| `Deploy.s.sol` | Foundry deploy script (or `00_deploy.ts` for Hardhat) |

## Custom Hooks Deep Dive

SE2 hooks wrap wagmi hooks with contract name resolution from `deployedContracts.ts`. They eliminate the need to pass ABI and address manually.

### useScaffoldReadContract -- Read On-Chain State

Reads a view/pure function from a deployed contract. Auto-refreshes on new blocks.

```tsx
import { useScaffoldReadContract } from "~~/hooks/scaffold-eth";

function GreetingDisplay() {
  const { data: greeting, isLoading } = useScaffoldReadContract({
    contractName: "YourContract",
    functionName: "greeting",
  });

  if (isLoading) return <span>Loading...</span>;

  return <span>{greeting}</span>;
}
```

With arguments:

```tsx
function BalanceOf({ account }: { account: string }) {
  const { data: balance } = useScaffoldReadContract({
    contractName: "YourToken",
    functionName: "balanceOf",
    args: [account],
  });

  return <span>{balance?.toString()}</span>;
}
```

### useScaffoldWriteContract -- Send Transactions

Sends a transaction to a deployed contract. Handles wallet prompts, gas estimation, and confirmation tracking.

```tsx
import { useScaffoldWriteContract } from "~~/hooks/scaffold-eth";

function SetGreeting() {
  const { writeContractAsync, isMining } = useScaffoldWriteContract("YourContract");

  async function handleSetGreeting() {
    await writeContractAsync({
      functionName: "setGreeting",
      args: ["Hello from SE2"],
    });
  }

  return (
    <button onClick={handleSetGreeting} disabled={isMining}>
      {isMining ? "Mining..." : "Set Greeting"}
    </button>
  );
}
```

With ETH value:

```tsx
function BuyTokens() {
  const { writeContractAsync, isMining } = useScaffoldWriteContract("Vendor");

  async function handleBuy() {
    await writeContractAsync({
      functionName: "buyTokens",
      value: parseEther("0.1"),
    });
  }

  return (
    <button onClick={handleBuy} disabled={isMining}>
      {isMining ? "Buying..." : "Buy Tokens (0.1 ETH)"}
    </button>
  );
}
```

### useDeployedContractInfo -- Get ABI and Address

Returns the full contract info (ABI, address) for a deployed contract on the current chain.

```tsx
import { useDeployedContractInfo } from "~~/hooks/scaffold-eth";

function ContractInfo() {
  const { data: contractInfo, isLoading } = useDeployedContractInfo("YourContract");

  if (isLoading) return <span>Loading contract info...</span>;
  if (!contractInfo) return <span>Contract not found on this chain</span>;

  return (
    <div>
      <p>Address: {contractInfo.address}</p>
      <p>Functions: {contractInfo.abi.filter(item => item.type === "function").length}</p>
    </div>
  );
}
```

### useScaffoldMultiWriteContract -- Batch Transactions

Executes multiple contract writes in sequence. Useful for approve-then-execute patterns.

```tsx
import { useScaffoldMultiWriteContract } from "~~/hooks/scaffold-eth";

function ApproveAndDeposit() {
  const { writeContractsAsync, isMining } = useScaffoldMultiWriteContract();

  async function handleDeposit() {
    await writeContractsAsync({
      calls: [
        {
          contractName: "YourToken",
          functionName: "approve",
          args: ["0xVaultAddress", parseEther("100")],
        },
        {
          contractName: "Vault",
          functionName: "deposit",
          args: [parseEther("100")],
        },
      ],
    });
  }

  return (
    <button onClick={handleDeposit} disabled={isMining}>
      {isMining ? "Processing..." : "Approve & Deposit"}
    </button>
  );
}
```

### useTransactor -- Transaction Lifecycle Management

Low-level hook for custom transaction flows. Handles notifications, error display, and block explorer links.

```tsx
import { useTransactor } from "~~/hooks/scaffold-eth";
import { usePublicClient, useWalletClient } from "wagmi";

function CustomTransaction() {
  const writeTx = useTransactor();
  const { data: walletClient } = useWalletClient();
  const publicClient = usePublicClient();

  async function handleSend() {
    if (!walletClient) return;

    const hash = await walletClient.sendTransaction({
      to: "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
      value: parseEther("0.01"),
    });

    await writeTx(
      () => publicClient.waitForTransactionReceipt({ hash }),
      { blockConfirmations: 1 }
    );
  }

  return <button onClick={handleSend}>Send 0.01 ETH</button>;
}
```

### useScaffoldEventHistory -- Read Past Events

Fetches historical events from a deployed contract.

```tsx
import { useScaffoldEventHistory } from "~~/hooks/scaffold-eth";

function TransferHistory() {
  const { data: events, isLoading } = useScaffoldEventHistory({
    contractName: "YourToken",
    eventName: "Transfer",
    fromBlock: 0n,
    // Optional filters
    filters: { from: "0xSenderAddress" },
    // Fetch block timestamps
    blockData: true,
  });

  if (isLoading) return <p>Loading events...</p>;

  return (
    <ul>
      {events?.map((event, i) => (
        <li key={i}>
          {event.args.from} sent {event.args.value?.toString()} to {event.args.to}
        </li>
      ))}
    </ul>
  );
}
```

### useScaffoldWatchContractEvent -- Live Event Subscription

Subscribes to new events in real time.

```tsx
import { useScaffoldWatchContractEvent } from "~~/hooks/scaffold-eth";

function LiveTransfers() {
  useScaffoldWatchContractEvent({
    contractName: "YourToken",
    eventName: "Transfer",
    onLogs: (logs) => {
      logs.forEach((log) => {
        console.log("Transfer:", log.args.from, "->", log.args.to, log.args.value);
      });
    },
  });

  return <p>Listening for transfers...</p>;
}
```

## Contract Hot Reload

When you modify a Solidity file and run `yarn deploy`:

1. Foundry compiles the contracts and runs `Deploy.s.sol`
2. The deploy script writes deployment artifacts to `packages/foundry/deployments/`
3. A post-deploy hook reads artifacts and regenerates `packages/nextjs/contracts/deployedContracts.ts`
4. Next.js hot-reloads the page with the new ABI and address

The entire cycle takes seconds. No manual ABI copying, no address pasting.

### Deploy Script (Foundry)

```solidity
// packages/foundry/script/Deploy.s.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import {ScaffoldETHDeploy} from "./DeployHelpers.s.sol";
import {YourContract} from "../contracts/YourContract.sol";

contract DeployScript is ScaffoldETHDeploy {
    function run() external ScaffoldEthDeployerRunner {
        YourContract yourContract = new YourContract(msg.sender);
        deployments.push(Deployment("YourContract", address(yourContract)));
    }
}
```

### Deploy Script (Hardhat)

```typescript
// packages/hardhat/deploy/00_deploy_your_contract.ts
import { HardhatRuntimeEnvironment } from "hardhat/types";
import { DeployFunction } from "hardhat-deploy/types";

const deployYourContract: DeployFunction = async function (hre: HardhatRuntimeEnvironment) {
  const { deployer } = await hre.getNamedAccounts();
  const { deploy } = hre.deployments;

  await deploy("YourContract", {
    from: deployer,
    args: [deployer],
    log: true,
    autoMine: true,
  });
};

export default deployYourContract;
deployYourContract.tags = ["YourContract"];
```

## Debug Page

The debug page at `/debug` auto-generates a complete UI for every deployed contract. For each public function it renders:

- **Read functions**: Input fields for arguments, a "Read" button, and the return value displayed inline
- **Write functions**: Input fields for arguments, a "Send" button, transaction status, and block explorer link
- **Payable functions**: An additional ETH value input field

This is the fastest way to test contract logic without writing any frontend code. During development, deploy your contract and immediately interact with every function from the browser.

The debug page reads from the same `deployedContracts.ts` that the hooks use, so it always reflects your latest deployment.

## Three-Phase Build

### Phase 1: Local Development (Anvil / Hardhat Network)

```bash
yarn chain    # Starts Anvil (Foundry) or Hardhat Network
yarn deploy   # Deploys to local chain
yarn start    # Starts Next.js at localhost:3000
```

Local chain provides:
- Instant block mining (no waiting for confirmations)
- Pre-funded test accounts (10,000 ETH each)
- Automatic transaction logging in terminal
- The burner wallet in SE2 auto-connects to the local chain

### Phase 2: Testnet Deployment

1. Configure the target network in `scaffold.config.ts`:

```typescript
// packages/nextjs/scaffold.config.ts
import { defineConfig } from "@scaffold-eth/config";

const scaffoldConfig = defineConfig({
  targetNetworks: [chains.sepolia],
  pollingInterval: 30000,
  onlyLocalBurnerWallet: false,
  walletAutoConnect: true,
});

export default scaffoldConfig;
```

2. Set deployer private key:

```bash
# Foundry
cd packages/foundry
echo "DEPLOYER_PRIVATE_KEY=0x..." > .env

# Hardhat
cd packages/hardhat
echo "DEPLOYER_PRIVATE_KEY=0x..." > .env
```

3. Deploy to testnet:

```bash
# Foundry
yarn deploy --network sepolia

# Hardhat
yarn deploy --network sepolia
```

4. Get testnet ETH from faucets:
   - Sepolia: https://sepoliafaucet.com
   - Holesky: https://holesky-faucet.pk910.de

### Phase 3: Production Deployment

1. Deploy contracts to mainnet (see Deployment section below)
2. Update `scaffold.config.ts` to target mainnet
3. Deploy frontend to Vercel (see Deployment section below)

## External Contracts Pattern

To interact with contracts you did not deploy (Uniswap, Aave, ENS, etc.), add them to `externalContracts.ts`.

```typescript
// packages/nextjs/contracts/externalContracts.ts
import { GenericContractsDeclaration } from "~~/utils/scaffold-eth/contract";

const externalContracts = {
  1: {
    // Mainnet chain ID
    DAI: {
      address: "0x6B175474E89094C44Da98b954EedeAC495271d0F",
      abi: [
        {
          name: "balanceOf",
          type: "function",
          stateMutability: "view",
          inputs: [{ name: "account", type: "address" }],
          outputs: [{ name: "", type: "uint256" }],
        },
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
      ] as const,
    },
  },
} as const;

export default externalContracts;
```

Once configured, SE2 hooks treat external contracts exactly like your own:

```tsx
function DaiBalance({ account }: { account: string }) {
  const { data: balance } = useScaffoldReadContract({
    contractName: "DAI",
    functionName: "balanceOf",
    args: [account],
  });

  return <span>{balance?.toString()}</span>;
}
```

External contracts also appear on the debug page.

## Deployment

### Vercel Deployment

```bash
# From project root
yarn vercel
```

Or connect the GitHub repo to Vercel:

1. Push code to GitHub
2. Import the repo in Vercel dashboard
3. Set framework preset to **Next.js**
4. Set root directory to `packages/nextjs`
5. Add environment variables:
   - `NEXT_PUBLIC_ALCHEMY_API_KEY` (or your RPC provider key)
   - `NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID`
6. Deploy

### Contract Verification

```bash
# Foundry -- after deploying to a live network
yarn verify --network sepolia

# Hardhat
yarn hardhat-verify --network sepolia
```

Verification requires an Etherscan API key set in the environment:

```bash
# packages/foundry/.env or packages/hardhat/.env
ETHERSCAN_API_KEY=your_api_key
```

### Production Checklist

1. Contracts deployed to target chain and verified on Etherscan
2. `scaffold.config.ts` targeting the production chain
3. `onlyLocalBurnerWallet` set to `false` (or `true` to disable burner wallet)
4. RPC endpoints configured (Alchemy, Infura, or custom)
5. Frontend deployed to Vercel with environment variables set
6. Wallet connection tested on production URL
7. All contract interactions verified on the live deployment

## Configuration

### scaffold.config.ts

```typescript
import { defineConfig } from "@scaffold-eth/config";
import * as chains from "viem/chains";

const scaffoldConfig = defineConfig({
  // Chain(s) your dApp targets -- first chain is the default
  targetNetworks: [chains.hardhat],

  // RPC polling interval in milliseconds
  pollingInterval: 30000,

  // Alchemy API key for production RPCs
  alchemyApiKey: process.env.NEXT_PUBLIC_ALCHEMY_API_KEY ?? "",

  // WalletConnect project ID
  walletConnectProjectId: process.env.NEXT_PUBLIC_WALLET_CONNECT_PROJECT_ID ?? "",

  // Show burner wallet only on local chains
  onlyLocalBurnerWallet: true,

  // Auto-connect wallet on page load
  walletAutoConnect: true,
});

export default scaffoldConfig;
```

### Network Configuration

Target multiple chains by adding them to the array:

```typescript
const scaffoldConfig = defineConfig({
  targetNetworks: [chains.mainnet, chains.sepolia, chains.optimism],
  // ...
});
```

SE2 uses the first chain in the array as the default. Users can switch chains via the built-in network switcher component.

### Burner Wallet

SE2 includes a built-in burner wallet for local development. It auto-generates a private key stored in `localStorage` and funds itself from the local chain faucet. The burner wallet is disabled on live networks when `onlyLocalBurnerWallet` is `true`.

## SE2 Component Library

SE2 ships reusable components in `packages/nextjs/components/scaffold-eth/`:

| Component | Purpose |
|-----------|---------|
| `<Address>` | Displays an address with ENS resolution, copy button, and block explorer link |
| `<Balance>` | Shows ETH balance for an address |
| `<EtherInput>` | Input field with ETH/USD conversion |
| `<AddressInput>` | Input field with ENS resolution and address validation |
| `<IntegerInput>` | Input field for uint256 with bigint handling |
| `<RainbowKitCustomConnectButton>` | Wallet connect button with chain info |
| `<BlockieAvatar>` | Blockie identicon for addresses |

Usage:

```tsx
import { Address, Balance, EtherInput } from "~~/components/scaffold-eth";

function AccountCard({ address }: { address: string }) {
  return (
    <div>
      <Address address={address} />
      <Balance address={address} />
    </div>
  );
}
```

## Common Patterns

### Reading Contract State with Auto-Refresh

```tsx
function ContractDashboard() {
  const { data: owner } = useScaffoldReadContract({
    contractName: "YourContract",
    functionName: "owner",
  });

  const { data: totalSupply } = useScaffoldReadContract({
    contractName: "YourContract",
    functionName: "totalSupply",
  });

  const { data: isPaused } = useScaffoldReadContract({
    contractName: "YourContract",
    functionName: "paused",
  });

  return (
    <div>
      <p>Owner: <Address address={owner} /></p>
      <p>Total Supply: {totalSupply?.toString()}</p>
      <p>Status: {isPaused ? "Paused" : "Active"}</p>
    </div>
  );
}
```

### Form with Contract Write

```tsx
import { useState } from "react";
import { useScaffoldWriteContract } from "~~/hooks/scaffold-eth";
import { AddressInput, IntegerInput } from "~~/components/scaffold-eth";

function TransferForm() {
  const [to, setTo] = useState("");
  const [amount, setAmount] = useState<string | bigint>("");
  const { writeContractAsync, isMining } = useScaffoldWriteContract("YourToken");

  async function handleTransfer() {
    await writeContractAsync({
      functionName: "transfer",
      args: [to, BigInt(amount)],
    });
  }

  return (
    <div>
      <AddressInput value={to} onChange={setTo} placeholder="Recipient" />
      <IntegerInput value={amount} onChange={setAmount} placeholder="Amount" />
      <button onClick={handleTransfer} disabled={isMining || !to || !amount}>
        {isMining ? "Sending..." : "Transfer"}
      </button>
    </div>
  );
}
```

## References

- Scaffold-ETH 2 docs: https://docs.scaffoldeth.io
- Scaffold-ETH 2 GitHub: https://github.com/scaffold-eth/scaffold-eth-2
- SE2 extensions: https://extensions.scaffoldeth.io
- BuidlGuidl: https://buidlguidl.com
- SpeedRunEthereum (tutorials): https://speedrunethereum.com
- wagmi docs: https://wagmi.sh
- viem docs: https://viem.sh
- Foundry book: https://book.getfoundry.sh

Last verified: February 2026
