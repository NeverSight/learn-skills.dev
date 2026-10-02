---
name: hardhat
description: Hardhat Solidity development framework — project setup, plugin ecosystem, testing with Mocha/Chai, deployment with Hardhat Ignition, contract verification, Hardhat Network forking, TypeScript configuration, and custom task creation. Works on any EVM chain.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Dev Tools
tags:
  - hardhat
  - solidity
  - testing
  - deployment
  - ethereum
  - dev-tools
---

# Hardhat

Hardhat is the dominant Solidity development framework. It provides compilation, testing, deployment, and debugging for EVM smart contracts. The core value is Hardhat Network — a local EVM that supports console.log, stack traces, and mainnet forking. All configuration lives in `hardhat.config.ts`.

## What You Probably Got Wrong

> LLMs frequently generate Hardhat code mixing v1 patterns, ethers v5 syntax, and deprecated plugins. These corrections are non-negotiable.

- **ethers v6, not v5 — the API changed fundamentally** — Hardhat toolbox now bundles ethers v6. `ethers.getContractFactory()` returns a different type. `parseEther()` is a standalone import, not `ethers.utils.parseEther()`. `BigNumber` is gone — ethers v6 uses native `bigint`. If you see `BigNumber.from()` or `ethers.utils.*`, you are writing v5 code. Stop.
- **`hardhat-deploy` is NOT the official deployment tool** — The official deployment system is Hardhat Ignition (`@nomicfoundation/hardhat-ignition`). `hardhat-deploy` by wighawag is a community plugin that is not maintained by the Hardhat team. Use Ignition for new projects.
- **`@nomicfoundation/hardhat-toolbox` replaces individual plugins** — Do not install `@nomiclabs/hardhat-ethers`, `@nomiclabs/hardhat-waffle`, or `hardhat-gas-reporter` individually. The `hardhat-toolbox` meta-plugin includes ethers, chai matchers, coverage, gas reporter, and typechain. The old `@nomiclabs/` scoped packages are deprecated.
- **`npx hardhat compile` does NOT generate TypeScript types by default** — You must have `@nomicfoundation/hardhat-toolbox` (or `@typechain/hardhat`) installed AND run `npx hardhat compile` to generate types in `typechain-types/`. The types are not checked into source control.
- **`hardhat.config.ts` is NOT optional for TypeScript** — If you use `.ts` config, you must have `ts-node` and `typescript` installed. Hardhat uses ts-node to transpile the config at runtime. Without it, Hardhat silently falls back to looking for `.js`.
- **`ethers.getSigners()` returns `HardhatEthersSigner`, not raw ethers Signer** — The signer type is `HardhatEthersSigner` which extends ethers `AbstractSigner`. It has additional properties like `.address` as a direct property (not a method). Type your test variables accordingly.
- **Hardhat Network resets between test files, not between `it()` blocks** — State persists across `it()` blocks within the same `describe()`. Use `loadFixture()` from `@nomicfoundation/hardhat-toolbox/network-helpers` to get clean state per test. Do not rely on `beforeEach` deploying fresh contracts — it is slower and error-prone.
- **Forking requires an archive node RPC** — `hardhat_reset` and `forking.blockNumber` require archive data. Standard RPC endpoints only serve recent state. Use Alchemy or Infura archive tier, or a local archive node.
- **`console.log` in Solidity only works on Hardhat Network** — `import "hardhat/console.sol"` is a Hardhat-specific feature. It does nothing on mainnet, testnets, or other local nodes. Do not leave `console.log` in production contracts — it wastes gas on the import.
- **Constructor arguments for verification must match exactly** — `npx hardhat verify` fails silently when constructor args do not match the deployed bytecode. Use the `--constructor-args` flag pointing to a JS file that exports the exact arguments used during deployment.

## Quick Start

### New Project

```bash
mkdir my-project && cd my-project
npx hardhat init
```

Select "Create a TypeScript project". This generates:

```
my-project/
  contracts/          # Solidity source files
  ignition/modules/   # Hardhat Ignition deployment modules
  test/               # Mocha test files
  hardhat.config.ts   # Central configuration
  package.json
  tsconfig.json
```

### Install Dependencies

```bash
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
```

`hardhat-toolbox` includes:
- `@nomicfoundation/hardhat-ethers` — ethers.js integration
- `@nomicfoundation/hardhat-chai-matchers` — Chai matchers for reverts, events, balance changes
- `@nomicfoundation/hardhat-network-helpers` — `loadFixture`, `time`, `mine`
- `@typechain/hardhat` — TypeScript type generation
- `hardhat-gas-reporter` — gas usage per function
- `solidity-coverage` — code coverage

### Minimal Config

```typescript
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config: HardhatUserConfig = {
  solidity: "0.8.27",
};

export default config;
```

### First Compile + Test

```bash
npx hardhat compile
npx hardhat test
```

## Configuration

### Multi-Network Setup

```typescript
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.27",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
      viaIR: false,
    },
  },
  networks: {
    hardhat: {
      chainId: 31337,
    },
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL ?? "",
      accounts: process.env.DEPLOYER_PRIVATE_KEY
        ? [process.env.DEPLOYER_PRIVATE_KEY]
        : [],
    },
    mainnet: {
      url: process.env.MAINNET_RPC_URL ?? "",
      accounts: process.env.DEPLOYER_PRIVATE_KEY
        ? [process.env.DEPLOYER_PRIVATE_KEY]
        : [],
    },
    arbitrum: {
      url: process.env.ARBITRUM_RPC_URL ?? "",
      accounts: process.env.DEPLOYER_PRIVATE_KEY
        ? [process.env.DEPLOYER_PRIVATE_KEY]
        : [],
      chainId: 42161,
    },
    base: {
      url: process.env.BASE_RPC_URL ?? "",
      accounts: process.env.DEPLOYER_PRIVATE_KEY
        ? [process.env.DEPLOYER_PRIVATE_KEY]
        : [],
      chainId: 8453,
    },
  },
  etherscan: {
    apiKey: {
      mainnet: process.env.ETHERSCAN_API_KEY ?? "",
      sepolia: process.env.ETHERSCAN_API_KEY ?? "",
      arbitrumOne: process.env.ARBISCAN_API_KEY ?? "",
      base: process.env.BASESCAN_API_KEY ?? "",
    },
  },
  gasReporter: {
    enabled: process.env.REPORT_GAS === "true",
    currency: "USD",
    coinmarketcap: process.env.COINMARKETCAP_API_KEY,
  },
};

export default config;
```

### Compiler Settings

```typescript
solidity: {
  compilers: [
    {
      version: "0.8.27",
      settings: {
        optimizer: { enabled: true, runs: 200 },
        evmVersion: "cancun",
      },
    },
    {
      version: "0.8.20",
      settings: {
        optimizer: { enabled: true, runs: 1000 },
      },
    },
  ],
  overrides: {
    "contracts/Legacy.sol": {
      version: "0.8.17",
    },
  },
},
```

Multiple compiler versions let you compile contracts with different Solidity requirements in the same project.

### Forking Configuration

```typescript
networks: {
  hardhat: {
    forking: {
      url: process.env.MAINNET_RPC_URL ?? "",
      blockNumber: 19_000_000,
      enabled: true,
    },
  },
},
```

Pin `blockNumber` for deterministic tests. Without it, tests depend on live chain state and break when state changes.

## Testing

### Test Structure with Fixtures

```typescript
import { expect } from "chai";
import { ethers } from "hardhat";
import { loadFixture } from "@nomicfoundation/hardhat-toolbox/network-helpers";

describe("Token", function () {
  async function deployTokenFixture() {
    const [owner, alice, bob] = await ethers.getSigners();
    const initialSupply = ethers.parseEther("1000000");

    const Token = await ethers.getContractFactory("Token");
    const token = await Token.deploy(initialSupply);

    return { token, owner, alice, bob, initialSupply };
  }

  describe("Deployment", function () {
    it("should set the correct total supply", async function () {
      const { token, initialSupply } = await loadFixture(deployTokenFixture);
      expect(await token.totalSupply()).to.equal(initialSupply);
    });

    it("should assign total supply to owner", async function () {
      const { token, owner, initialSupply } = await loadFixture(deployTokenFixture);
      expect(await token.balanceOf(owner.address)).to.equal(initialSupply);
    });
  });

  describe("Transfers", function () {
    it("should transfer tokens between accounts", async function () {
      const { token, owner, alice } = await loadFixture(deployTokenFixture);
      const amount = ethers.parseEther("100");

      await expect(token.transfer(alice.address, amount))
        .to.changeTokenBalances(token, [owner, alice], [-amount, amount]);
    });

    it("should revert on insufficient balance", async function () {
      const { token, alice, bob } = await loadFixture(deployTokenFixture);
      const amount = ethers.parseEther("1");

      await expect(token.connect(alice).transfer(bob.address, amount))
        .to.be.revertedWithCustomError(token, "ERC20InsufficientBalance");
    });
  });
});
```

### Key Testing Patterns

#### Event Assertions

```typescript
await expect(token.transfer(alice.address, amount))
  .to.emit(token, "Transfer")
  .withArgs(owner.address, alice.address, amount);
```

#### Custom Error Assertions

```typescript
await expect(vault.withdraw(amount))
  .to.be.revertedWithCustomError(vault, "InsufficientBalance")
  .withArgs(currentBalance, amount);
```

#### Ether Balance Changes

```typescript
await expect(payable.withdraw())
  .to.changeEtherBalances([payable, owner], [-amount, amount]);
```

#### Time Manipulation

```typescript
import { time } from "@nomicfoundation/hardhat-toolbox/network-helpers";

await time.increase(3600);
await time.increaseTo(targetTimestamp);
await time.latestBlock();
const latest = await time.latest();
```

#### Impersonating Accounts

```typescript
import { impersonateAccount, setBalance } from "@nomicfoundation/hardhat-toolbox/network-helpers";

const whaleAddress = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045";
await impersonateAccount(whaleAddress);
await setBalance(whaleAddress, ethers.parseEther("100"));

const whale = await ethers.getSigner(whaleAddress);
await token.connect(whale).transfer(recipient, amount);
```

#### Mining Control

```typescript
import { mine, mineUpTo } from "@nomicfoundation/hardhat-toolbox/network-helpers";

await mine(10);
await mineUpTo(20_000_000);
```

### Gas Reporter

Enable gas reporting in tests:

```bash
REPORT_GAS=true npx hardhat test
```

Output shows gas per function call and deployment cost.

### Coverage

```bash
npx hardhat coverage
```

Generates `coverage/` directory with HTML report. Coverage runs on a modified EVM — some tests may behave differently under coverage (gas-dependent assertions will fail).

## Deployment with Hardhat Ignition

Hardhat Ignition is the declarative deployment system. Define what to deploy, Ignition handles execution order, retries, and state tracking.

### Basic Module

```typescript
// ignition/modules/Token.ts
import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";
import { parseEther } from "ethers";

const TokenModule = buildModule("TokenModule", (m) => {
  const initialSupply = m.getParameter("initialSupply", parseEther("1000000"));

  const token = m.contract("Token", [initialSupply]);

  return { token };
});

export default TokenModule;
```

### Deploy Command

```bash
npx hardhat ignition deploy ignition/modules/Token.ts --network sepolia
```

### Module with Dependencies

```typescript
// ignition/modules/Protocol.ts
import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

const ProtocolModule = buildModule("ProtocolModule", (m) => {
  const registry = m.contract("Registry");

  const vault = m.contract("Vault", [registry]);

  m.call(registry, "setVault", [vault]);

  const controller = m.contract("Controller", [registry, vault]);

  m.call(registry, "setController", [controller]);

  return { registry, vault, controller };
});

export default ProtocolModule;
```

Ignition resolves the dependency graph automatically. `vault` deploys after `registry` because it takes `registry` as a constructor arg. `m.call()` executes after the contract it references is deployed.

### Parameters

```typescript
const owner = m.getParameter("owner");
const fee = m.getParameter("fee", 300n);
```

Pass parameters via JSON file or CLI:

```bash
npx hardhat ignition deploy ignition/modules/Token.ts \
  --network sepolia \
  --parameters ignition/parameters.json
```

```json
{
  "TokenModule": {
    "initialSupply": "1000000000000000000000000"
  }
}
```

### Deployment State

Ignition stores deployment state in `ignition/deployments/<deployment-id>/`. This directory tracks which contracts deployed, their addresses, and which calls executed. Do not delete it — Ignition uses it for resumption and verification.

### Verify After Deploy

```bash
npx hardhat ignition verify <deployment-id>
```

This reads constructor args from the deployment state. No need to specify them manually.

## Contract Verification

### Automatic (After Ignition Deploy)

```bash
npx hardhat ignition verify sepolia-deployment
```

### Manual

```bash
npx hardhat verify --network sepolia \
  0xYOUR_CONTRACT_ADDRESS \
  "constructor_arg_1" \
  "constructor_arg_2"
```

### Complex Constructor Args

Create a file for arguments:

```typescript
// arguments.ts
export default [
  "0xTokenAddress",
  1000n,
  "My Token",
];
```

```bash
npx hardhat verify --network sepolia \
  --constructor-args arguments.ts \
  0xYOUR_CONTRACT_ADDRESS
```

### Multi-Chain Verification

The `etherscan.apiKey` config accepts a map:

```typescript
etherscan: {
  apiKey: {
    mainnet: process.env.ETHERSCAN_API_KEY ?? "",
    arbitrumOne: process.env.ARBISCAN_API_KEY ?? "",
    optimisticEthereum: process.env.OPTIMISTIC_ETHERSCAN_API_KEY ?? "",
    base: process.env.BASESCAN_API_KEY ?? "",
    polygon: process.env.POLYGONSCAN_API_KEY ?? "",
  },
},
```

### Custom Chain Verification

For chains not natively supported by hardhat-verify:

```typescript
etherscan: {
  apiKey: {
    monad: process.env.MONAD_EXPLORER_API_KEY ?? "",
  },
  customChains: [
    {
      network: "monad",
      chainId: 10143,
      urls: {
        apiURL: "https://explorer.monad.xyz/api",
        browserURL: "https://explorer.monad.xyz",
      },
    },
  ],
},
```

## Hardhat Network

### Console.log in Solidity

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.27;

import "hardhat/console.sol";

contract Vault {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        console.log("Deposit from %s: %s wei", msg.sender, msg.value);
        balances[msg.sender] += msg.value;
    }
}
```

Remove `console.log` before deploying to production. It compiles to no-ops on non-Hardhat networks but the import still costs deployment gas.

### Stack Traces

Hardhat Network provides Solidity stack traces on reverts. No configuration needed — revert reasons and the exact line number appear in test output automatically.

### JSON-RPC Methods

Hardhat Network exposes additional JSON-RPC methods:

```typescript
// Snapshot and revert (alternative to fixtures for special cases)
const snapshotId = await ethers.provider.send("evm_snapshot", []);
await ethers.provider.send("evm_revert", [snapshotId]);

// Set block timestamp
await ethers.provider.send("evm_setNextBlockTimestamp", [1700000000]);
await ethers.provider.send("evm_mine", []);

// Set account balance
await ethers.provider.send("hardhat_setBalance", [
  "0xAddress",
  "0xDE0B6B3A7640000", // 1 ETH in hex
]);

// Set storage slot directly
await ethers.provider.send("hardhat_setStorageAt", [
  contractAddress,
  "0x0", // slot 0
  "0x0000000000000000000000000000000000000000000000000000000000000001",
]);

// Reset fork
await ethers.provider.send("hardhat_reset", [
  {
    forking: {
      jsonRpcUrl: process.env.MAINNET_RPC_URL,
      blockNumber: 19_000_000,
    },
  },
]);
```

### Mainnet Forking

Fork mainnet to test against real protocol state:

```typescript
// hardhat.config.ts
networks: {
  hardhat: {
    forking: {
      url: process.env.MAINNET_RPC_URL ?? "",
      blockNumber: 19_500_000,
    },
  },
},
```

```typescript
// test/ForkTest.ts
import { ethers } from "hardhat";

const USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48";
const WHALE = "0x47ac0Fb4F2D84898e4D9E7b4DaB3C24507a6D503"; // Binance hot wallet

describe("Fork Tests", function () {
  it("should read USDC balance on fork", async function () {
    const usdc = await ethers.getContractAt("IERC20", USDC);
    const balance = await usdc.balanceOf(WHALE);
    expect(balance).to.be.greaterThan(0n);
  });
});
```

## Custom Tasks

### Basic Task

```typescript
// hardhat.config.ts (or tasks/accounts.ts if you split tasks into files)
import { task } from "hardhat/config";

task("accounts", "Prints the list of accounts", async (_taskArgs, hre) => {
  const accounts = await hre.ethers.getSigners();
  for (const account of accounts) {
    console.log(account.address);
  }
});
```

```bash
npx hardhat accounts
```

### Task with Arguments

```typescript
import { task } from "hardhat/config";

task("balance", "Prints an account's balance")
  .addParam("account", "The account's address")
  .setAction(async (taskArgs, hre) => {
    const balance = await hre.ethers.provider.getBalance(taskArgs.account);
    console.log(hre.ethers.formatEther(balance), "ETH");
  });
```

```bash
npx hardhat balance --account 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266
```

### Task Calling Other Tasks

```typescript
task("deploy-and-verify", "Deploys and verifies a contract")
  .addParam("name", "Contract name")
  .setAction(async (taskArgs, hre) => {
    await hre.run("compile");

    const Contract = await hre.ethers.getContractFactory(taskArgs.name);
    const contract = await Contract.deploy();
    await contract.waitForDeployment();

    const address = await contract.getAddress();
    console.log(`${taskArgs.name} deployed to: ${address}`);

    if (hre.network.name !== "hardhat" && hre.network.name !== "localhost") {
      console.log("Waiting for block confirmations...");
      await contract.deploymentTransaction()?.wait(5);

      await hre.run("verify:verify", {
        address,
        constructorArguments: [],
      });
    }
  });
```

## TypeScript Configuration

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "commonjs",
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "strict": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "outDir": "./dist",
    "declaration": true
  },
  "include": [
    "./scripts",
    "./test",
    "./typechain-types"
  ],
  "files": [
    "./hardhat.config.ts"
  ]
}
```

### Type-Safe Contract Interaction

After `npx hardhat compile`, TypeChain generates types in `typechain-types/`:

```typescript
import { Token } from "../typechain-types";

describe("Token", function () {
  let token: Token;

  async function deployFixture() {
    const Token = await ethers.getContractFactory("Token");
    token = await Token.deploy(ethers.parseEther("1000000"));
    return { token };
  }
});
```

The `Token` type provides autocomplete for all contract methods with proper argument and return types.

### Importing Artifacts

```typescript
import TokenArtifact from "../artifacts/contracts/Token.sol/Token.json";

const token = new ethers.Contract(address, TokenArtifact.abi, signer);
```

## Plugin Ecosystem

### Essential Plugins

| Plugin | Purpose |
|--------|---------|
| `@nomicfoundation/hardhat-toolbox` | Meta-plugin: ethers, chai, coverage, gas, typechain |
| `@openzeppelin/hardhat-upgrades` | Proxy deployment (UUPS, Transparent) |
| `@nomicfoundation/hardhat-verify` | Etherscan/Blockscout verification |
| `@nomicfoundation/hardhat-ignition` | Declarative deployments |
| `hardhat-contract-sizer` | Report contract bytecode sizes |
| `hardhat-abi-exporter` | Export ABIs to separate files |

### Installing a Plugin

```bash
npm install --save-dev @openzeppelin/hardhat-upgrades @openzeppelin/contracts
```

```typescript
// hardhat.config.ts
import "@openzeppelin/hardhat-upgrades";
```

All plugins are activated by importing them in `hardhat.config.ts`. No other registration needed.

## Common Patterns

### Environment Variable Handling

```typescript
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import * as dotenv from "dotenv";

dotenv.config();

function getRequiredEnv(key: string): string {
  const value = process.env[key];
  if (!value) {
    throw new Error(`Missing required environment variable: ${key}`);
  }
  return value;
}

const config: HardhatUserConfig = {
  solidity: "0.8.27",
  networks: {
    mainnet: {
      url: getRequiredEnv("MAINNET_RPC_URL"),
      accounts: [getRequiredEnv("DEPLOYER_PRIVATE_KEY")],
    },
  },
};

export default config;
```

### Contract Size Check

```bash
npm install --save-dev hardhat-contract-sizer
```

```typescript
// hardhat.config.ts
import "hardhat-contract-sizer";

const config: HardhatUserConfig = {
  contractSizer: {
    alphaSort: true,
    runOnCompile: true,
    disambiguatePaths: false,
    strict: true, // fail if any contract exceeds 24KB
  },
};
```

### Parallel Test Execution

```bash
npx hardhat test --parallel
```

Tests must be isolated (use `loadFixture`) for parallel execution. Shared mutable state between tests will cause flaky failures.

## Hardhat vs Foundry

| Feature | Hardhat | Foundry |
|---------|---------|---------|
| Language | TypeScript/JavaScript | Solidity |
| Speed | Slower compilation | Faster compilation |
| Testing | Mocha/Chai (JS) | Solidity tests |
| Debugging | console.log, stack traces | Traces, cheatcodes |
| Deployment | Hardhat Ignition | forge script |
| Plugins | NPM ecosystem | Less extensible |
| Forking | Built-in | Built-in |

Use Hardhat when: TypeScript integration matters, complex deployment orchestration, large plugin ecosystem needed, team knows JS/TS better than Solidity.

Use Foundry when: Speed matters, fuzz testing needed, team prefers Solidity-native tooling.

Both can coexist in the same project with `hardhat-foundry` plugin.

## Reference

- Official Docs: https://hardhat.org/docs
- Hardhat Ignition: https://hardhat.org/ignition
- GitHub: https://github.com/NomicFoundation/hardhat
- Plugin Directory: https://hardhat.org/hardhat-runner/plugins
- Hardhat Network Reference: https://hardhat.org/hardhat-network/docs/reference
- ethers v6 Docs: https://docs.ethers.org/v6/
