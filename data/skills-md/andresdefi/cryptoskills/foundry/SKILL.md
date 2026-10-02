---
name: foundry
description: Foundry toolkit for Solidity development — forge (build/test), cast (chain interaction), anvil (local node), and chisel (REPL). Covers project setup, testing patterns (unit, fuzz, invariant, fork), deployment via forge script, contract verification, gas optimization, and debugging. Works on any EVM chain.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Dev Tools
tags:
  - foundry
  - forge
  - cast
  - anvil
  - solidity
  - testing
---

# Foundry

Foundry is the standard Solidity development toolkit. It compiles, tests, deploys, and interacts with smart contracts — all from the command line, all in Solidity (no JavaScript test wrappers). Four binaries: `forge` (build/test/deploy), `cast` (chain interaction), `anvil` (local EVM node), `chisel` (Solidity REPL).

## What You Probably Got Wrong

> LLMs have stale training data. These are the most common mistakes.

- **`forge create` for deployments** → Use `forge script` with `--broadcast`. `forge create` is for quick one-offs only — scripts are reproducible, support multi-contract deployments, and generate broadcast artifacts for verification.
- **`cast send` returns data** → `cast send` submits a transaction and returns a tx receipt. Use `cast call` to read return values (simulates without sending). Mixing these up is the #1 cast mistake.
- **Old test assertion syntax** → Foundry uses `assertEq`, `assertGt`, `assertLt`, `assertTrue`, `assertFalse`. There is no `assert(a == b)` pattern — it compiles but gives zero debug info on failure.
- **`vm.prank` persists** → `vm.prank` applies to the NEXT call only. Use `vm.startPrank`/`vm.stopPrank` for multiple calls from the same address.
- **Anvil is just Ganache** → Anvil supports mainnet forking at specific blocks (`--fork-url` + `--fork-block-number`), auto-impersonation, tracing, and mining modes. It's a full-featured local node.
- **`forge test -vvvv` is overkill** → Use `-vv` for logs/events, `-vvv` for execution traces on failures, `-vvvv` for full traces including setup. Start with `-vv`.
- **`--rpc-url` with raw URLs** → Use `foundry.toml` `[rpc_endpoints]` section or `--rpc-url $ENV_VAR`. Never paste RPC URLs directly in commands.
- **Missing `--via-ir` for large contracts** → If you hit "stack too deep", add `via_ir = true` in `foundry.toml` under `[profile.default]`. This enables the IR-based compilation pipeline.

## Quick Start

### Installation

```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

Verify installation:

```bash
forge --version
cast --version
anvil --version
```

### Initialize a Project

```bash
forge init my-project
cd my-project
```

This creates:

```
my-project/
├── foundry.toml          # Project config
├── src/
│   └── Counter.sol       # Source contracts
├── test/
│   └── Counter.t.sol     # Test files (*.t.sol)
├── script/
│   └── Counter.s.sol     # Deploy scripts (*.s.sol)
└── lib/                  # Dependencies (git submodules)
```

### Recommended `foundry.toml`

```toml
[profile.default]
src = "src"
out = "out"
libs = ["lib"]
solc = "0.8.28"
optimizer = true
optimizer_runs = 200
ffi = false
fs_permissions = [{ access = "read", path = "./"}]

[rpc_endpoints]
mainnet = "${MAINNET_RPC_URL}"
sepolia = "${SEPOLIA_RPC_URL}"
arbitrum = "${ARBITRUM_RPC_URL}"
base = "${BASE_RPC_URL}"

[etherscan]
mainnet = { key = "${ETHERSCAN_API_KEY}" }
sepolia = { key = "${ETHERSCAN_API_KEY}" }
arbitrum = { key = "${ARBISCAN_API_KEY}" }
base = { key = "${BASESCAN_API_KEY}" }

[fuzz]
runs = 256
max_test_rejects = 65536

[invariant]
runs = 256
depth = 15
fail_on_revert = false
```

### Install Dependencies

```bash
forge install OpenZeppelin/openzeppelin-contracts
forge install transmissions11/solmate
```

Add remappings in `foundry.toml`:

```toml
remappings = [
    "@openzeppelin/=lib/openzeppelin-contracts/",
    "solmate/=lib/solmate/src/",
]
```

## Core Commands

### Build

```bash
forge build                          # Compile all contracts
forge build --sizes                  # Show contract sizes (24576 byte limit)
forge build --via-ir                 # Use IR pipeline (fixes stack too deep)
forge clean && forge build           # Clean rebuild
```

### Test

```bash
forge test                           # Run all tests
forge test --match-test testSwap     # Run tests matching name
forge test --match-contract VaultTest # Run tests in matching contract
forge test --no-match-test testFork  # Exclude tests matching name
forge test -vv                       # Show logs and assertion details
forge test -vvv                      # Show execution traces on failures
forge test -vvvv                     # Show full traces including setup
forge test --gas-report              # Show gas usage per function
```

### Cast — Read from Chain

```bash
# Call a view function (no transaction, free)
cast call 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  "balanceOf(address)(uint256)" \
  0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 \
  --rpc-url $MAINNET_RPC_URL

# Decode calldata
cast 4byte-decode 0xa9059cbb000000000000000000000000...

# Get storage slot value
cast storage 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 0 --rpc-url $MAINNET_RPC_URL

# Check if address has code (is it a contract?)
cast code 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 --rpc-url $MAINNET_RPC_URL

# ABI-encode function arguments
cast abi-encode "transfer(address,uint256)" 0xRecipient 1000000

# Compute function selector
cast sig "transfer(address,uint256)"
# Output: 0xa9059cbb

# Convert between units
cast to-wei 1.5 ether        # 1500000000000000000
cast from-wei 1000000000000000000  # 1.000000000000000000

# Get current block number
cast block-number --rpc-url $MAINNET_RPC_URL

# Get transaction receipt
cast receipt 0xTX_HASH --rpc-url $MAINNET_RPC_URL
```

### Cast — Write to Chain

```bash
# Send a transaction (costs gas, modifies state)
cast send 0xContractAddress \
  "transfer(address,uint256)" \
  0xRecipient 1000000 \
  --rpc-url $SEPOLIA_RPC_URL \
  --private-key $PRIVATE_KEY

# Send ETH
cast send 0xRecipient \
  --value 0.1ether \
  --rpc-url $SEPOLIA_RPC_URL \
  --private-key $PRIVATE_KEY
```

### Anvil — Local Node

```bash
# Start local node (default: http://localhost:8545)
anvil

# Fork mainnet at latest block
anvil --fork-url $MAINNET_RPC_URL

# Fork at specific block
anvil --fork-url $MAINNET_RPC_URL --fork-block-number 19000000

# Custom chain ID and port
anvil --chain-id 1337 --port 8546

# Auto-mine every 12 seconds (simulate real chain)
anvil --block-time 12
```

Anvil provides 10 funded accounts with 10000 ETH each. The default mnemonic is `test test test test test test test test test test test junk`.

## Testing Patterns

### Unit Test

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Test} from "forge-std/Test.sol";
import {Vault} from "../src/Vault.sol";

contract VaultTest is Test {
    Vault vault;
    address alice = makeAddr("alice");
    address bob = makeAddr("bob");

    function setUp() public {
        vault = new Vault();
        vm.deal(alice, 10 ether);
        vm.deal(bob, 10 ether);
    }

    function testDeposit() public {
        vm.prank(alice);
        vault.deposit{value: 1 ether}();
        assertEq(vault.balanceOf(alice), 1 ether);
    }

    function testWithdrawRevertsIfInsufficientBalance() public {
        vm.prank(alice);
        vm.expectRevert(Vault.InsufficientBalance.selector);
        vault.withdraw(1 ether);
    }
}
```

### Fuzz Test

Foundry auto-generates random inputs. The function parameter becomes the fuzz input.

```solidity
function testFuzzDeposit(uint256 amount) public {
    // Bound the fuzz input to a realistic range
    amount = bound(amount, 0.01 ether, 100 ether);

    vm.deal(alice, amount);
    vm.prank(alice);
    vault.deposit{value: amount}();

    assertEq(vault.balanceOf(alice), amount);
}
```

### Fork Test

Test against real mainnet state:

```solidity
contract ForkTest is Test {
    // USDC on Ethereum mainnet
    address constant USDC = 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48;
    address constant WHALE = 0x47ac0Fb4F2D84898e4D9E7b4DaB3C24507a6D503;

    function setUp() public {
        // Fork mainnet — set MAINNET_RPC_URL in foundry.toml [rpc_endpoints]
        vm.createSelectFork("mainnet");
    }

    function testWhaleBalance() public view {
        uint256 balance = IERC20(USDC).balanceOf(WHALE);
        assertGt(balance, 1_000_000e6, "Whale should hold >1M USDC");
    }

    function testImpersonateWhale() public {
        vm.prank(WHALE);
        IERC20(USDC).transfer(alice, 1000e6);
        assertEq(IERC20(USDC).balanceOf(alice), 1000e6);
    }
}

interface IERC20 {
    function balanceOf(address) external view returns (uint256);
    function transfer(address, uint256) external returns (bool);
}
```

Run fork tests:

```bash
forge test --match-contract ForkTest --fork-url $MAINNET_RPC_URL -vvv
```

### Invariant Test

Stateful testing — Foundry calls random functions in random order and checks invariants hold:

```solidity
contract VaultInvariantTest is Test {
    Vault vault;
    VaultHandler handler;

    function setUp() public {
        vault = new Vault();
        handler = new VaultHandler(vault);

        // Only call functions on the handler
        targetContract(address(handler));
    }

    // Invariant: contract balance always equals sum of all deposits
    function invariant_solvency() public view {
        assertEq(
            address(vault).balance,
            handler.totalDeposited() - handler.totalWithdrawn()
        );
    }
}

contract VaultHandler is Test {
    Vault vault;
    uint256 public totalDeposited;
    uint256 public totalWithdrawn;

    constructor(Vault _vault) {
        vault = _vault;
    }

    function deposit(uint256 amount) public {
        amount = bound(amount, 0.01 ether, 10 ether);
        vm.deal(msg.sender, amount);
        vm.prank(msg.sender);
        vault.deposit{value: amount}();
        totalDeposited += amount;
    }

    function withdraw(uint256 amount) public {
        uint256 balance = vault.balanceOf(msg.sender);
        if (balance == 0) return;
        amount = bound(amount, 1, balance);
        vm.prank(msg.sender);
        vault.withdraw(amount);
        totalWithdrawn += amount;
    }
}
```

### Essential Cheatcodes

```solidity
// Identity
address alice = makeAddr("alice");               // Deterministic address from label
(address signer, uint256 pk) = makeAddrAndKey("signer"); // Address + private key

// Impersonation
vm.prank(alice);                                 // Next call as alice
vm.startPrank(alice);                            // All calls as alice until stopPrank
vm.stopPrank();

// Balances
vm.deal(alice, 10 ether);                        // Set ETH balance
deal(address(token), alice, 1000e18);            // Set ERC20 balance (stdcheats)

// Time
vm.warp(block.timestamp + 1 days);               // Set block.timestamp
vm.roll(block.number + 100);                      // Set block.number
skip(3600);                                       // Advance timestamp by seconds
rewind(3600);                                     // Rewind timestamp

// Expect revert
vm.expectRevert();                                // Next call must revert
vm.expectRevert("Insufficient balance");          // Revert with message
vm.expectRevert(Vault.InsufficientBalance.selector); // Revert with custom error
vm.expectRevert(
    abi.encodeWithSelector(Vault.AmountTooLarge.selector, 100)
); // Custom error with args

// Expect event emission
vm.expectEmit(true, true, false, true);           // checkTopic1, checkTopic2, checkTopic3, checkData
emit Transfer(alice, bob, 100);                   // The expected event
vault.transfer(bob, 100);                         // The call that should emit

// Snapshots — save and restore EVM state
uint256 snapshot = vm.snapshotState();
// ... modify state ...
vm.revertToState(snapshot);                       // Restore to snapshot

// Labels — improve trace readability
vm.label(address(vault), "Vault");
vm.label(alice, "Alice");

// Environment variables
string memory rpcUrl = vm.envString("RPC_URL");
uint256 pk = vm.envUint("PRIVATE_KEY");
```

## Deployment

### Deployment Script

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import {Script, console} from "forge-std/Script.sol";
import {Vault} from "../src/Vault.sol";

contract DeployVault is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");

        vm.startBroadcast(deployerPrivateKey);

        Vault vault = new Vault();
        console.log("Vault deployed to:", address(vault));

        vm.stopBroadcast();
    }
}
```

### Deploy Commands

```bash
# Dry run (simulate without broadcasting)
forge script script/DeployVault.s.sol --rpc-url sepolia -vvvv

# Deploy to testnet
forge script script/DeployVault.s.sol \
  --rpc-url sepolia \
  --broadcast \
  --verify \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  -vvvv

# Deploy to mainnet (use --slow for reliability)
forge script script/DeployVault.s.sol \
  --rpc-url mainnet \
  --broadcast \
  --verify \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  --slow \
  -vvvv
```

The `--slow` flag waits for each transaction to be confirmed before sending the next. Always use it on mainnet.

Broadcast artifacts are saved to `broadcast/DeployVault.s.sol/<chainId>/run-latest.json`. These contain deployed addresses and transaction hashes.

### Verify an Already-Deployed Contract

```bash
forge verify-contract 0xDeployedAddress \
  src/Vault.sol:Vault \
  --chain sepolia \
  --etherscan-api-key $ETHERSCAN_API_KEY

# With constructor arguments
forge verify-contract 0xDeployedAddress \
  src/Vault.sol:Vault \
  --chain mainnet \
  --etherscan-api-key $ETHERSCAN_API_KEY \
  --constructor-args $(cast abi-encode "constructor(address,uint256)" 0xOwner 1000)
```

## Advanced

### Gas Snapshots

Capture gas usage per test for regression tracking:

```bash
forge snapshot                          # Create .gas-snapshot file
forge snapshot --check                  # Compare against existing snapshot
forge snapshot --diff                   # Show diff against existing snapshot
```

### Code Coverage

```bash
forge coverage                          # Summary table
forge coverage --report lcov            # Generate lcov report
```

To view in a browser:

```bash
forge coverage --report lcov
genhtml lcov.info -o coverage --branch-coverage
open coverage/index.html
```

### Contract Inspection

```bash
# View ABI
forge inspect src/Vault.sol:Vault abi

# View storage layout
forge inspect src/Vault.sol:Vault storage-layout

# View creation bytecode
forge inspect src/Vault.sol:Vault bytecode

# View function selectors (method IDs)
forge inspect src/Vault.sol:Vault methods
```

### Gas Optimization with `forge inspect`

```bash
# Check contract size (24576 byte limit for deployment)
forge build --sizes

# Compare optimizer runs impact
forge build --optimizer-runs 200
forge build --optimizer-runs 10000
```

### Debug a Transaction

```bash
# Interactive debugger for a failed test
forge test --match-test testDeposit --debug

# Debug a mainnet transaction
cast run 0xTX_HASH --rpc-url $MAINNET_RPC_URL
```

### Chisel — Solidity REPL

```bash
chisel

# Inside chisel:
# !help                           — show commands
# uint256 x = 42;                 — declare variables
# x + 8                           — evaluate expressions
# !source                         — show current session source
```

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `Stack too deep` | Too many local variables for the EVM stack | Add `via_ir = true` to `foundry.toml` |
| `EvmError: OutOfGas` | Function exceeds block gas limit in test | Increase gas limit: `--gas-limit 30000000` |
| `CompilerError: File not found` | Missing remapping for imported path | Add remapping to `foundry.toml` `remappings = [...]` |
| `Failed to get EIP-1559 fees` | RPC doesn't support EIP-1559 (some L2s) | Add `--legacy` flag to `forge script` or `cast send` |
| `(code: -32000, message: nonce too low)` | Pending tx or wrong nonce | Wait for pending txs or use `--nonce <N>` |
| `script failed: transaction reverted` | On-chain state differs from expectation | Run without `--broadcast` first to debug, use `-vvvv` |
| `contract exceeds 24576 bytes` | Contract too large to deploy | Split into libraries, optimize, or use the diamond pattern |
| `forge test` hangs on fork tests | RPC rate limiting or slow responses | Use a dedicated RPC provider, add `--fork-retry-backoff` |
| `permission denied: ffi` | FFI disabled by default (security) | Add `ffi = true` in `foundry.toml` only if you trust all dependencies |
| `Solc version mismatch` | pragma doesn't match config | Set `solc` in `foundry.toml` or use `auto_detect_solc = true` |

## Security

- **Never hardcode private keys** in scripts or CLI commands. Use environment variables: `vm.envUint("PRIVATE_KEY")` in scripts, `--private-key $PRIVATE_KEY` in commands.
- **Use `--slow` on mainnet** to wait for confirmations between transactions.
- **Dry-run before broadcast** — always run `forge script` without `--broadcast` first.
- **Pin fork block numbers** — `--fork-block-number` prevents tests from breaking when chain state changes.
- **Disable FFI unless needed** — `ffi = false` prevents contracts from executing arbitrary shell commands during tests.
- **Review broadcast artifacts** — check `broadcast/*/run-latest.json` before deploying to mainnet.
- **Use `--verify` on deploy** — verified source code is essential for trust and debugging.
- **Store `.env` in `.gitignore`** — never commit RPC URLs with API keys or private keys.

## References

- [Foundry Book](https://book.getfoundry.sh/) — official documentation
- [Foundry GitHub](https://github.com/foundry-rs/foundry) — source code and issues
- [forge-std Reference](https://book.getfoundry.sh/reference/forge-std/) — standard library (Test, Script, cheatcodes)
- [Cheatcodes Reference](https://book.getfoundry.sh/cheatcodes/) — full list of `vm.*` cheatcodes
- [Cast Reference](https://book.getfoundry.sh/reference/cast/) — all cast subcommands
- [Foundry Best Practices](https://book.getfoundry.sh/tutorials/best-practices) — project structure and patterns
