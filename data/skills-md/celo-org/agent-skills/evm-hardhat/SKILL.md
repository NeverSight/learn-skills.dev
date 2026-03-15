---
name: evm-hardhat
description: Hardhat development for EVM chains including Celo. Use when setting up Hardhat projects, writing Solidity contracts, compiling, testing, deploying, or verifying contracts with Hardhat.
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# Hardhat Development for EVM Chains

This skill covers Hardhat setup and development for EVM-compatible chains with emphasis on Celo.

## When to Use

- Setting up a new Hardhat project
- Writing and compiling Solidity smart contracts
- Testing contracts with Hardhat
- Deploying contracts to Celo or other EVM chains
- Verifying contracts on block explorers

## Quick Start

### Initialize Project

```bash
mkdir my-project && cd my-project
npm init -y
npm install --save-dev hardhat
npx hardhat init
```

Select "Create a TypeScript project" when prompted.

### Install Additional Dependencies

```bash
npm install --save-dev @nomicfoundation/hardhat-toolbox dotenv
```

## Celo Network Information

| Network | Chain ID | RPC Endpoint |
|---------|----------|--------------|
| Celo Mainnet | 42220 | https://forno.celo.org |
| Celo Sepolia | 11142220 | https://forno.celo-sepolia.celo-testnet.org |


## Configuration

### hardhat.config.ts for Celo

```typescript
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import * as dotenv from "dotenv";

dotenv.config();

const PRIVATE_KEY = process.env.PRIVATE_KEY || "";
const CELOSCAN_API_KEY = process.env.CELOSCAN_API_KEY || "";

const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.28",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    // Celo Mainnet
    celo: {
      url: "https://forno.celo.org",
      chainId: 42220,
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : [],
    },
    // Celo Sepolia Testnet
    celoSepolia: {
      url: "https://forno.celo-sepolia.celo-testnet.org",
      chainId: 11142220,
      accounts: PRIVATE_KEY ? [PRIVATE_KEY] : [],
    },
    // Local development
    hardhat: {
      chainId: 31337,
    },
  },
  etherscan: {
    apiKey: {
      celo: CELOSCAN_API_KEY,
      celoSepolia: CELOSCAN_API_KEY,
    },
    customChains: [
      {
        network: "celo",
        chainId: 42220,
        urls: {
          apiURL: "https://api.celoscan.io/api",
          browserURL: "https://celoscan.io",
        },
      },
      {
        network: "celoSepolia",
        chainId: 11142220,
        urls: {
          apiURL: "https://api.etherscan.io/v2/api",
          browserURL: "https://sepolia.celoscan.io",
        },
      },
    ],
  },
};

export default config;
```

### Environment Variables (.env)

```bash
PRIVATE_KEY=your_private_key_here
CELOSCAN_API_KEY=your_celoscan_api_key_here
```

## Writing Contracts

### Basic Contract Structure

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract MyContract {
    string public name;
    address public owner;

    event NameChanged(string oldName, string newName);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor(string memory _name) {
        name = _name;
        owner = msg.sender;
    }

    function setName(string memory _newName) external onlyOwner {
        string memory oldName = name;
        name = _newName;
        emit NameChanged(oldName, _newName);
    }
}
```

### Using OpenZeppelin

```bash
npm install @openzeppelin/contracts
```

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC20, Ownable {
    constructor() ERC20("MyToken", "MTK") Ownable(msg.sender) {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }

    function mint(address to, uint256 amount) external onlyOwner {
        _mint(to, amount);
    }
}
```

## Compilation

```bash
# Compile all contracts
npx hardhat compile

# Clean and recompile
npx hardhat clean && npx hardhat compile
```

## Testing

### Test File Structure

```typescript
// test/MyContract.test.ts
import { expect } from "chai";
import { ethers } from "hardhat";
import { MyContract } from "../typechain-types";

describe("MyContract", function () {
  let contract: MyContract;
  let owner: any;
  let addr1: any;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    const MyContract = await ethers.getContractFactory("MyContract");
    contract = await MyContract.deploy("Initial Name");
    await contract.waitForDeployment();
  });

  describe("Deployment", function () {
    it("Should set the right name", async function () {
      expect(await contract.name()).to.equal("Initial Name");
    });

    it("Should set the right owner", async function () {
      expect(await contract.owner()).to.equal(owner.address);
    });
  });

  describe("setName", function () {
    it("Should allow owner to change name", async function () {
      await contract.setName("New Name");
      expect(await contract.name()).to.equal("New Name");
    });

    it("Should emit NameChanged event", async function () {
      await expect(contract.setName("New Name"))
        .to.emit(contract, "NameChanged")
        .withArgs("Initial Name", "New Name");
    });

    it("Should revert if non-owner tries to change name", async function () {
      await expect(
        contract.connect(addr1).setName("Hacked")
      ).to.be.revertedWith("Not owner");
    });
  });
});
```

### Running Tests

```bash
# Run all tests
npx hardhat test

# Run specific test file
npx hardhat test test/MyContract.test.ts

# Run with gas reporting
REPORT_GAS=true npx hardhat test

# Run with coverage
npx hardhat coverage
```

## Deployment

### Deployment Script

```typescript
// scripts/deploy.ts
import { ethers } from "hardhat";

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with account:", deployer.address);

  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", ethers.formatEther(balance), "CELO");

  const MyContract = await ethers.getContractFactory("MyContract");
  const contract = await MyContract.deploy("My Contract Name");
  await contract.waitForDeployment();

  const address = await contract.getAddress();
  console.log("Contract deployed to:", address);

  // Wait for confirmations before verification
  console.log("Waiting for confirmations...");
  await contract.deploymentTransaction()?.wait(5);

  console.log("Deployment complete!");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

### Deploy Commands

```bash
# Deploy to local Hardhat network
npx hardhat run scripts/deploy.ts

# Deploy to Celo Sepolia testnet
npx hardhat run scripts/deploy.ts --network celoSepolia

# Deploy to Celo Mainnet
npx hardhat run scripts/deploy.ts --network celo
```

## Verification

### Verify After Deployment

```bash
# Verify on Celo Sepolia
npx hardhat verify --network celoSepolia <CONTRACT_ADDRESS> "Constructor Arg 1"

# Verify on Celo Mainnet
npx hardhat verify --network celo <CONTRACT_ADDRESS> "Constructor Arg 1"
```

### Programmatic Verification

```typescript
// Add to deployment script after deployment
import { run } from "hardhat";

async function verify(address: string, constructorArguments: any[]) {
  console.log("Verifying contract...");
  try {
    await run("verify:verify", {
      address,
      constructorArguments,
    });
    console.log("Verified!");
  } catch (e: any) {
    if (e.message.includes("Already Verified")) {
      console.log("Already verified");
    } else {
      console.error(e);
    }
  }
}
```

## Common Tasks

### Flatten Contract for Manual Verification

```bash
npx hardhat flatten contracts/MyContract.sol > Flattened.sol
```

### Check Contract Size

```bash
npx hardhat compile --force
npx hardhat size-contracts
```

## Block Explorers

- **Celo Mainnet:** https://celoscan.io
- **Celo Sepolia:** https://sepolia.celoscan.io

## Additional Resources

- [hardhat-config.md](references/hardhat-config.md) - Detailed configuration options
- [testing-patterns.md](references/testing-patterns.md) - Advanced testing patterns
- [security-checklist.md](rules/security-checklist.md) - Security best practices
