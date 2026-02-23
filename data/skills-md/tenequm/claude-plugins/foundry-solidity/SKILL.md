---
name: foundry-solidity
description: Build and test Solidity smart contracts with Foundry toolkit. Use when developing Ethereum contracts, writing Forge tests, deploying with scripts, or debugging with Cast/Anvil. Triggers on Foundry commands (forge, cast, anvil), Solidity testing, smart contract development, or files like foundry.toml, *.t.sol, *.s.sol.
---

# Foundry Solidity Development

Complete guide for building secure, efficient smart contracts with **Foundry 1.5.0** and **Solidity 0.8.30**.

## When to Use This Skill

- Developing Ethereum/EVM smart contracts
- Writing Forge tests (unit, fuzz, invariant, fork)
- Deploying contracts with scripts
- Using Foundry tools (forge, cast, anvil, chisel)
- Working with `foundry.toml`, `*.t.sol`, `*.s.sol` files
- Debugging transactions and contract interactions

## Quick Start

```bash
# Create new project
forge init my-project && cd my-project

# Build contracts
forge build

# Run tests
forge test

# Deploy (dry-run)
forge script script/Deploy.s.sol --rpc-url sepolia

# Deploy (broadcast)
forge script script/Deploy.s.sol --rpc-url sepolia --broadcast --verify
```

## Project Structure

```
my-project/
├── foundry.toml          # Configuration
├── src/                  # Contracts
│   └── Counter.sol
├── test/                 # Tests (*.t.sol)
│   └── Counter.t.sol
├── script/               # Deploy scripts (*.s.sol)
│   └── Deploy.s.sol
└── lib/                  # Dependencies
    └── forge-std/
```

## Core Commands

### Build & Test

```bash
forge build                          # Compile
forge test                           # Run all tests
forge test -vvvv                     # With traces
forge test --match-test testDeposit  # Filter by test name
forge test --match-contract Vault    # Filter by contract
forge test --fork-url $RPC_URL       # Fork testing
forge test --gas-report              # Gas usage report
```

### Deployment

```bash
# Single contract
forge create src/Token.sol:Token --rpc-url sepolia --private-key $KEY --broadcast

# Script deployment (recommended)
forge script script/Deploy.s.sol:Deploy --rpc-url sepolia --broadcast --verify

# Verify existing contract
forge verify-contract $ADDRESS src/Token.sol:Token --chain sepolia
```

### Cast - Blockchain Interactions

```bash
cast call $CONTRACT "balanceOf(address)" $USER --rpc-url mainnet
cast send $CONTRACT "transfer(address,uint256)" $TO $AMOUNT --private-key $KEY
cast decode-tx $TX_HASH
cast storage $CONTRACT 0 --rpc-url mainnet
```

### Anvil - Local Node

```bash
anvil                           # Start local node
anvil --fork-url $RPC_URL       # Fork mainnet
anvil --fork-block-number 18000000
```

## Basic Test Contract

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

import {Test, console} from "forge-std/Test.sol";
import {Counter} from "../src/Counter.sol";

contract CounterTest is Test {
    Counter public counter;
    address public user;

    function setUp() public {
        counter = new Counter();
        user = makeAddr("user");
        deal(user, 10 ether);
    }

    function test_Increment() public {
        counter.increment();
        assertEq(counter.number(), 1);
    }

    function test_RevertWhen_Unauthorized() public {
        vm.expectRevert("Unauthorized");
        vm.prank(user);
        counter.adminFunction();
    }

    function testFuzz_SetNumber(uint256 x) public {
        x = bound(x, 0, 1000);
        counter.setNumber(x);
        assertEq(counter.number(), x);
    }
}
```

## Essential Cheatcodes

```solidity
// Identity & ETH
address alice = makeAddr("alice");          // Create labeled address
deal(alice, 10 ether);                      // Give ETH
deal(address(token), alice, 1000e18);       // Give ERC20

// Impersonation
vm.prank(alice);                            // Next call as alice
vm.startPrank(alice);                       // All calls as alice
vm.stopPrank();

// Time & Block
vm.warp(block.timestamp + 1 days);          // Set timestamp
vm.roll(block.number + 100);                // Set block number

// Assertions
vm.expectRevert("Error message");           // Expect revert
vm.expectRevert(CustomError.selector);      // Custom error
vm.expectEmit(true, true, false, true);     // Expect event
emit Transfer(from, to, amount);            // Must match next emit

// Storage
vm.store(addr, slot, value);                // Write storage
vm.load(addr, slot);                        // Read storage
```

## Deploy Script

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.30;

import {Script, console} from "forge-std/Script.sol";
import {Counter} from "../src/Counter.sol";

contract Deploy is Script {
    function run() external {
        uint256 deployerKey = vm.envUint("PRIVATE_KEY");

        vm.startBroadcast(deployerKey);
        Counter counter = new Counter();
        counter.setNumber(42);
        vm.stopBroadcast();

        console.log("Deployed to:", address(counter));
    }
}
```

## Modern Solidity Patterns (0.8.30)

```solidity
// Custom errors (gas efficient)
error InsufficientBalance(uint256 available, uint256 required);

// Transient storage (0.8.28+) - cheap reentrancy guard
bool transient locked;
modifier nonReentrant() {
    require(!locked, "Reentrancy");
    locked = true;
    _;
    locked = false;
}

// Immutable variables (cheap reads)
address public immutable owner;

// Named mapping parameters
mapping(address user => uint256 balance) public balances;

// require with custom error (0.8.26+)
require(amount <= balance, InsufficientBalance(balance, amount));
```

## Configuration (foundry.toml)

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
solc = "0.8.30"
optimizer = true
optimizer_runs = 200
evm_version = "prague"

fuzz.runs = 256
invariant.runs = 256
invariant.depth = 50

[rpc_endpoints]
mainnet = "${MAINNET_RPC_URL}"
sepolia = "${SEPOLIA_RPC_URL}"

[etherscan]
mainnet = { key = "${ETHERSCAN_API_KEY}" }
sepolia = { key = "${ETHERSCAN_API_KEY}" }

[profile.ci]
fuzz.runs = 10000
invariant.runs = 1000
```

## References

For detailed guides, see:

- **Testing**: See `references/testing.md` for complete testing patterns (unit, fuzz, invariant, fork), all cheatcodes, and best practices
- **forge-std API**: See `references/forge-std-api.md` for complete library reference (150+ functions)
- **Solidity 0.8.30**: See `references/solidity-modern.md` for new features and modern syntax
- **Deployment**: See `references/deployment.md` for scripting, verification, and multi-chain deployment
- **Configuration**: See `references/configuration.md` for all foundry.toml options
- **Gas Optimization**: See `references/gas-optimization.md` for storage packing, compiler settings, and profiling
- **Patterns**: See `references/patterns.md` for access control, reentrancy guards, factories, and common idioms
- **Security**: See `references/security.md` for vulnerabilities, defensive patterns, and audit preparation
- **Resources**: See `references/resources.md` for official docs, libraries, security tools, and learning paths
- **Debugging**: See `references/debugging.md` for traces, breakpoints, console.log, and the interactive debugger
- **Dependencies**: See `references/dependencies.md` for forge install, remappings, and Soldeer package manager
- **CI/CD**: See `references/cicd.md` for GitHub Actions workflows, caching, and gas tracking
- **Chisel**: See `references/chisel.md` for the interactive Solidity REPL
- **Cast Advanced**: See `references/cast-advanced.md` for decoding, encoding, wallet management, and batch operations
- **Anvil Advanced**: See `references/anvil-advanced.md` for impersonation, state manipulation, and mining modes
