---
name: arbitrum-stylus
description: Arbitrum Stylus development — write smart contracts in Rust, C, and C++ compiled to WASM. Covers Stylus SDK, storage patterns, ABI export, deployment, testing, and Solidity interop.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: arbitrum
  category: L2 & Alt-L1
tags:
  - arbitrum
  - stylus
  - rust
  - wasm
  - smart-contracts
---

# Arbitrum Stylus

Stylus is Arbitrum's second virtual machine — a WASM-based execution environment that runs alongside the EVM on Arbitrum One and Nova. Write smart contracts in Rust, C, or C++, compile to WASM, and deploy them to the same chain as Solidity contracts. Both VMs share the same state, so Stylus contracts can call Solidity contracts and vice versa through standard ABI-encoded calls.

## What You Probably Got Wrong

> LLMs trained before late 2024 carry stale assumptions about Stylus. These corrections are critical.

- **Stylus is NOT a separate chain** — Stylus contracts deploy to Arbitrum One (chain ID 42161) and Arbitrum Nova (42170). They share state, addresses, and the block space with EVM contracts. There is no "Stylus chain."
- **Stylus contracts need activation after deployment** — Deploying a WASM contract is a two-step process: (1) deploy the contract bytecode, (2) activate it by calling `ArbWasm.activateProgram()`. The `cargo stylus deploy` CLI handles both steps, but if you deploy manually, you must activate separately. Unactivated contracts revert on every call.
- **Storage layout is EVM-compatible** — Stylus uses the same 256-bit storage slots as Solidity. `StorageU256` at slot 0 in Stylus is the same as `uint256` at slot 0 in Solidity. This enables proxy patterns and shared storage between Solidity and Stylus.
- **Gas is measured in "ink", not gas directly** — Stylus WASM execution uses "ink" internally (1 gas = 10,000 ink by default). This finer granularity allows cheaper metering of WASM opcodes. You still pay in ETH gas from the user's perspective.
- **You cannot use CREATE/CREATE2 from Stylus** — Stylus contracts cannot deploy other contracts. Factory patterns must be implemented in Solidity. This is a fundamental limitation of the WASM VM.
- **The SDK crate is `stylus-sdk`, not `arbitrum-sdk`** — The Rust crate is `stylus-sdk` on crates.io. `arbitrum-sdk` is the TypeScript SDK for cross-chain messaging (different thing entirely).
- **`sol_storage!` is the old macro** — As of stylus-sdk 0.6+, use `#[storage]` attribute and `#[entrypoint]` derive macro instead of the older `sol_storage!` block. Both work, but the attribute-based API is the current standard.
- **No floating point in WASM contracts** — The deterministic WASM environment disallows floating-point operations. Use fixed-point math (e.g., `U256` with scaling factors).

## Quick Start

### Prerequisites

```bash
# Install Rust (if not already installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Add the WASM target
rustup target add wasm32-unknown-unknown

# Install cargo-stylus CLI
cargo install cargo-stylus
```

### Verify Installation

```bash
cargo stylus --version
# cargo-stylus 0.5.x

rustup target list --installed | grep wasm32
# wasm32-unknown-unknown
```

### Create a New Project

```bash
cargo stylus new my-stylus-contract
cd my-stylus-contract
```

This scaffolds a project with the correct `Cargo.toml`, WASM target configuration, and a starter contract.

## Project Structure

```
my-stylus-contract/
├── Cargo.toml
├── src/
│   └── lib.rs          # Contract code
├── .cargo/
│   └── config.toml     # WASM build target config
└── rust-toolchain.toml  # Pinned Rust version
```

### Cargo.toml

```toml
[package]
name = "my-stylus-contract"
version = "0.1.0"
edition = "2021"

[dependencies]
stylus-sdk = "0.6"
alloy-primitives = "0.7"
alloy-sol-types = "0.7"

[features]
export-abi = ["stylus-sdk/export-abi"]

[profile.release]
codegen-units = 1
strip = true
lto = true
panic = "abort"
opt-level = "s"

[lib]
crate-type = ["lib", "cdylib"]
```

### .cargo/config.toml

```toml
[build]
target = "wasm32-unknown-unknown"

[target.wasm32-unknown-unknown]
rustflags = ["-C", "link-arg=-zstack-size=8192"]
```

## Storage Patterns

Stylus provides typed storage primitives that map directly to EVM 256-bit storage slots. Each type occupies a deterministic slot position, identical to Solidity's storage layout.

### Basic Storage Types

```rust
use stylus_sdk::prelude::*;
use stylus_sdk::storage::{
    StorageAddress, StorageBool, StorageU256, StorageU128, StorageU64,
};
use alloy_primitives::{Address, U256};

#[storage]
#[entrypoint]
pub struct Counter {
    count: StorageU256,
    owner: StorageAddress,
    paused: StorageBool,
}

#[public]
impl Counter {
    pub fn get_count(&self) -> U256 {
        self.count.get()
    }

    pub fn increment(&mut self) {
        let current = self.count.get();
        self.count.set(current + U256::from(1));
    }

    pub fn owner(&self) -> Address {
        self.owner.get()
    }

    pub fn is_paused(&self) -> bool {
        self.paused.get()
    }
}
```

### Collections: StorageVec and StorageMap

```rust
use stylus_sdk::prelude::*;
use stylus_sdk::storage::{StorageVec, StorageMap, StorageU256, StorageAddress};
use alloy_primitives::{Address, U256};

#[storage]
#[entrypoint]
pub struct Registry {
    // Dynamic array — like Solidity's address[]
    members: StorageVec<StorageAddress>,
    // Mapping — like Solidity's mapping(address => uint256)
    balances: StorageMap<Address, StorageU256>,
    // Nested mapping — like mapping(address => mapping(address => uint256))
    allowances: StorageMap<Address, StorageMap<Address, StorageU256>>,
}

#[public]
impl Registry {
    pub fn add_member(&mut self, member: Address) {
        let mut slot = self.members.grow();
        slot.set(member);
    }

    pub fn member_count(&self) -> U256 {
        U256::from(self.members.len())
    }

    pub fn get_balance(&self, account: Address) -> U256 {
        self.balances.get(account)
    }

    pub fn set_balance(&mut self, account: Address, amount: U256) {
        let mut slot = self.balances.setter(account);
        slot.set(amount);
    }

    pub fn get_allowance(&self, owner: Address, spender: Address) -> U256 {
        self.allowances.get(owner).get(spender)
    }

    pub fn set_allowance(&mut self, owner: Address, spender: Address, amount: U256) {
        let mut inner = self.allowances.setter(owner);
        let mut slot = inner.setter(spender);
        slot.set(amount);
    }
}
```

### StorageString and StorageBytes

```rust
use stylus_sdk::prelude::*;
use stylus_sdk::storage::{StorageString, StorageBytes};

#[storage]
#[entrypoint]
pub struct Metadata {
    name: StorageString,
    data: StorageBytes,
}

#[public]
impl Metadata {
    pub fn get_name(&self) -> String {
        self.name.get_string()
    }

    pub fn set_name(&mut self, name: String) {
        self.name.set_str(&name);
    }

    pub fn get_data(&self) -> Vec<u8> {
        self.data.get_bytes()
    }

    pub fn set_data(&mut self, data: Vec<u8>) {
        self.data.set_bytes(&data);
    }
}
```

## ABI Export

Stylus contracts expose a Solidity-compatible ABI. Any tool that can call a Solidity contract (viem, ethers.js, cast, Remix) can call a Stylus contract.

### Entrypoint and External Functions

```rust
use stylus_sdk::prelude::*;
use stylus_sdk::storage::StorageU256;
use alloy_primitives::U256;

// #[entrypoint] marks this struct as the contract's main dispatch target.
// #[storage] maps its fields to EVM storage slots.
#[storage]
#[entrypoint]
pub struct MyContract {
    value: StorageU256,
}

// #[public] exposes all methods in this impl block as external ABI functions.
#[public]
impl MyContract {
    // View function — does not modify state
    pub fn get_value(&self) -> U256 {
        self.value.get()
    }

    // State-mutating function
    pub fn set_value(&mut self, new_value: U256) {
        self.value.set(new_value);
    }

    // Payable function — can receive ETH
    #[payable]
    pub fn deposit(&mut self) -> U256 {
        let received = msg::value();
        let current = self.value.get();
        self.value.set(current + received);
        received
    }
}
```

### Generating the ABI

```bash
# Export the Solidity ABI JSON
cargo stylus export-abi

# Output is a Solidity interface you can use from other contracts:
# interface IMyContract {
#     function getValue() external view returns (uint256);
#     function setValue(uint256 new_value) external;
#     function deposit() external payable returns (uint256);
# }
```

### Using msg Context

```rust
use stylus_sdk::prelude::*;
use stylus_sdk::{msg, block};
use alloy_primitives::{Address, U256};

#[public]
impl MyContract {
    pub fn caller(&self) -> Address {
        msg::sender()
    }

    pub fn sent_value(&self) -> U256 {
        msg::value()
    }

    pub fn current_timestamp(&self) -> U256 {
        U256::from(block::timestamp())
    }
}
```

## Contract Patterns

### ERC20 Token

```rust
use stylus_sdk::prelude::*;
use stylus_sdk::storage::{StorageMap, StorageString, StorageU256, StorageU8};
use stylus_sdk::{evm, msg};
use alloy_primitives::{Address, U256};
use alloy_sol_types::sol;

sol! {
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

#[storage]
#[entrypoint]
pub struct Erc20 {
    name: StorageString,
    symbol: StorageString,
    decimals: StorageU8,
    total_supply: StorageU256,
    balances: StorageMap<Address, StorageU256>,
    allowances: StorageMap<Address, StorageMap<Address, StorageU256>>,
}

#[derive(Debug)]
pub enum Erc20Error {
    InsufficientBalance,
    InsufficientAllowance,
    ZeroAddress,
}

#[public]
impl Erc20 {
    pub fn name(&self) -> String {
        self.name.get_string()
    }

    pub fn symbol(&self) -> String {
        self.symbol.get_string()
    }

    pub fn decimals(&self) -> u8 {
        self.decimals.get()
    }

    pub fn total_supply(&self) -> U256 {
        self.total_supply.get()
    }

    pub fn balance_of(&self, account: Address) -> U256 {
        self.balances.get(account)
    }

    pub fn allowance(&self, owner: Address, spender: Address) -> U256 {
        self.allowances.get(owner).get(spender)
    }

    pub fn transfer(&mut self, to: Address, amount: U256) -> Result<bool, Vec<u8>> {
        let from = msg::sender();
        self._transfer(from, to, amount)?;
        Ok(true)
    }

    pub fn approve(&mut self, spender: Address, amount: U256) -> Result<bool, Vec<u8>> {
        let owner = msg::sender();
        self._approve(owner, spender, amount)?;
        Ok(true)
    }

    pub fn transfer_from(
        &mut self,
        from: Address,
        to: Address,
        amount: U256,
    ) -> Result<bool, Vec<u8>> {
        let spender = msg::sender();
        let current_allowance = self.allowances.get(from).get(spender);
        if current_allowance < amount {
            return Err(b"InsufficientAllowance".to_vec());
        }
        self._approve(from, spender, current_allowance - amount)?;
        self._transfer(from, to, amount)?;
        Ok(true)
    }
}

impl Erc20 {
    fn _transfer(&mut self, from: Address, to: Address, amount: U256) -> Result<(), Vec<u8>> {
        if to == Address::ZERO {
            return Err(b"ZeroAddress".to_vec());
        }
        let from_balance = self.balances.get(from);
        if from_balance < amount {
            return Err(b"InsufficientBalance".to_vec());
        }
        self.balances.setter(from).set(from_balance - amount);
        let to_balance = self.balances.get(to);
        self.balances.setter(to).set(to_balance + amount);
        evm::log(Transfer { from, to, value: amount });
        Ok(())
    }

    fn _approve(
        &mut self,
        owner: Address,
        spender: Address,
        amount: U256,
    ) -> Result<(), Vec<u8>> {
        if spender == Address::ZERO {
            return Err(b"ZeroAddress".to_vec());
        }
        self.allowances.setter(owner).setter(spender).set(amount);
        evm::log(Approval { owner, spender, value: amount });
        Ok(())
    }
}
```

### Access Control (Ownable)

```rust
use stylus_sdk::prelude::*;
use stylus_sdk::storage::StorageAddress;
use stylus_sdk::msg;
use alloy_primitives::Address;
use alloy_sol_types::sol;

sol! {
    event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);
}

#[storage]
pub struct Ownable {
    owner: StorageAddress,
}

impl Ownable {
    pub fn owner(&self) -> Address {
        self.owner.get()
    }

    pub fn only_owner(&self) -> Result<(), Vec<u8>> {
        if msg::sender() != self.owner.get() {
            return Err(b"NotOwner".to_vec());
        }
        Ok(())
    }

    pub fn transfer_ownership(&mut self, new_owner: Address) -> Result<(), Vec<u8>> {
        self.only_owner()?;
        if new_owner == Address::ZERO {
            return Err(b"ZeroAddress".to_vec());
        }
        let old_owner = self.owner.get();
        self.owner.set(new_owner);
        evm::log(OwnershipTransferred {
            previousOwner: old_owner,
            newOwner: new_owner,
        });
        Ok(())
    }

    pub fn init(&mut self, owner: Address) {
        self.owner.set(owner);
    }
}
```

### Events

```rust
use stylus_sdk::prelude::*;
use stylus_sdk::evm;
use alloy_primitives::{Address, U256};
use alloy_sol_types::sol;

// Define events using the sol! macro — these produce Solidity-compatible event signatures.
sol! {
    event Deposit(address indexed sender, uint256 amount);
    event Withdrawal(address indexed recipient, uint256 amount);
    event ConfigUpdated(uint256 oldValue, uint256 newValue);
}

// Emit events with evm::log()
fn emit_deposit(sender: Address, amount: U256) {
    evm::log(Deposit { sender, amount });
}
```

## Deployment

### Check WASM Validity

```bash
# Validate that your contract compiles to valid WASM for Stylus
cargo stylus check \
  --endpoint https://sepolia-rollup.arbitrum.io/rpc

# This checks:
# 1. Compiles to valid WASM
# 2. No disallowed opcodes (floating point, etc.)
# 3. Fits within size limits
# 4. ABI is well-formed
```

### Deploy to Testnet

```bash
# Deploy and activate in one step
cargo stylus deploy \
  --endpoint https://sepolia-rollup.arbitrum.io/rpc \
  --private-key $PRIVATE_KEY

# Output:
# contract address: 0x...
# deployment tx:    0x...
# activation tx:    0x...
```

### Deploy to Mainnet

```bash
# Deploy to Arbitrum One
cargo stylus deploy \
  --endpoint https://arb1.arbitrum.io/rpc \
  --private-key $PRIVATE_KEY
```

### Activation

Every Stylus contract must be activated before it can execute. `cargo stylus deploy` handles this automatically. If you deployed the WASM bytecode manually (e.g., via a proxy pattern), activate separately:

```bash
# Activate an already-deployed contract
cargo stylus activate \
  --address 0xYourContractAddress \
  --endpoint https://arb1.arbitrum.io/rpc \
  --private-key $PRIVATE_KEY
```

Activation compiles the WASM to native machine code on-chain via the `ArbWasm` precompile. This is a one-time cost (~14M gas on mainnet, varies by contract size). Until activated, calling the contract reverts with "program not activated."

### Interacting with Deployed Contracts

Stylus contracts expose a standard Solidity ABI. Use any Ethereum tool:

```bash
# Read a value using cast
cast call 0xYourContract "getValue()(uint256)" \
  --rpc-url https://arb1.arbitrum.io/rpc

# Write a value
cast send 0xYourContract "setValue(uint256)" 42 \
  --rpc-url https://arb1.arbitrum.io/rpc \
  --private-key $PRIVATE_KEY
```

```typescript
import { createPublicClient, http } from "viem";
import { arbitrum } from "viem/chains";

const client = createPublicClient({
  chain: arbitrum,
  transport: http(process.env.ARBITRUM_RPC_URL),
});

// Same ABI as a Solidity contract — Stylus is transparent to callers
const abi = [
  {
    name: "getValue",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "setValue",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "new_value", type: "uint256" }],
    outputs: [],
  },
] as const;

const value = await client.readContract({
  address: "0xYourContract",
  abi,
  functionName: "getValue",
});
```

## Testing

### Unit Tests with motsu

`motsu` is the unit testing framework for Stylus contracts. It provides a mock EVM environment for testing storage and logic without deploying.

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use motsu::test;

    #[motsu::test]
    fn test_increment(contract: Counter) {
        let initial = contract.get_count();
        assert_eq!(initial, U256::ZERO);

        contract.increment();
        assert_eq!(contract.get_count(), U256::from(1));

        contract.increment();
        assert_eq!(contract.get_count(), U256::from(2));
    }

    #[motsu::test]
    fn test_set_value(contract: Counter) {
        contract.set_value(U256::from(100));
        assert_eq!(contract.get_value(), U256::from(100));
    }
}
```

### Testing ERC20

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use motsu::test;
    use alloy_primitives::address;

    #[motsu::test]
    fn test_transfer(contract: Erc20) {
        let alice = address!("A11CEbadF00dbadF00dbadF00dbadF00dbadF00db");
        let bob = address!("B0BbadF00dbadF00dbadF00dbadF00dbadF00dba0");

        // Mint initial balance to alice
        contract.balances.setter(alice).set(U256::from(1000));
        contract.total_supply.set(U256::from(1000));

        // Transfer from alice to bob
        // Note: motsu sets msg::sender() based on the test context
        let result = contract._transfer(alice, bob, U256::from(200));
        assert!(result.is_ok());

        assert_eq!(contract.balance_of(alice), U256::from(800));
        assert_eq!(contract.balance_of(bob), U256::from(200));
    }

    #[motsu::test]
    fn test_transfer_insufficient_balance(contract: Erc20) {
        let alice = address!("A11CEbadF00dbadF00dbadF00dbadF00dbadF00db");
        let bob = address!("B0BbadF00dbadF00dbadF00dbadF00dbadF00dba0");

        contract.balances.setter(alice).set(U256::from(100));

        let result = contract._transfer(alice, bob, U256::from(200));
        assert!(result.is_err());
    }

    #[motsu::test]
    fn test_approve_and_transfer_from(contract: Erc20) {
        let owner = address!("A11CEbadF00dbadF00dbadF00dbadF00dbadF00db");
        let spender = address!("B0BbadF00dbadF00dbadF00dbadF00dbadF00dba0");
        let recipient = address!("CCCF00dbadF00dbadF00dbadF00dbadF00dbad000");

        contract.balances.setter(owner).set(U256::from(1000));

        // Approve spender
        let approve_result = contract._approve(owner, spender, U256::from(500));
        assert!(approve_result.is_ok());
        assert_eq!(contract.allowance(owner, spender), U256::from(500));
    }
}
```

### Running Tests

```bash
# Run unit tests (compiles for native target, not WASM)
cargo test

# Run a specific test
cargo test test_transfer

# Run with output
cargo test -- --nocapture
```

### End-to-End Tests

For full integration testing, deploy to Arbitrum Sepolia and test with RPC calls:

```bash
# Deploy to Sepolia
cargo stylus deploy \
  --endpoint https://sepolia-rollup.arbitrum.io/rpc \
  --private-key $PRIVATE_KEY

# Test via cast
cast call $CONTRACT_ADDRESS "getValue()(uint256)" \
  --rpc-url https://sepolia-rollup.arbitrum.io/rpc

cast send $CONTRACT_ADDRESS "setValue(uint256)" 42 \
  --rpc-url https://sepolia-rollup.arbitrum.io/rpc \
  --private-key $PRIVATE_KEY
```

## Solidity Interop

### Calling Solidity from Stylus

Use `sol_interface!` to define the Solidity contract's interface, then call it via a low-level call:

```rust
use stylus_sdk::prelude::*;
use stylus_sdk::storage::StorageAddress;
use stylus_sdk::call::Call;
use alloy_primitives::{Address, U256};

sol_interface! {
    interface IERC20 {
        function balanceOf(address account) external view returns (uint256);
        function transfer(address to, uint256 amount) external returns (bool);
        function approve(address spender, uint256 amount) external returns (bool);
    }
}

#[storage]
#[entrypoint]
pub struct StylusSwapper {
    token: StorageAddress,
}

#[public]
impl StylusSwapper {
    pub fn check_balance(&self, account: Address) -> Result<U256, Vec<u8>> {
        let token_addr = self.token.get();
        let token = IERC20::new(token_addr);
        let config = Call::new();
        let balance = token.balance_of(config, account)?;
        Ok(balance)
    }

    pub fn send_tokens(
        &mut self,
        to: Address,
        amount: U256,
    ) -> Result<bool, Vec<u8>> {
        let token_addr = self.token.get();
        let token = IERC20::new(token_addr);
        let config = Call::new();
        let success = token.transfer(config, to, amount)?;
        Ok(success)
    }
}
```

### Calling Stylus from Solidity

Stylus contracts are ABI-compatible. Call them from Solidity exactly like any other contract:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// This interface matches the Stylus contract's exported ABI
interface IStylusCounter {
    function getCount() external view returns (uint256);
    function increment() external;
    function setValue(uint256 newValue) external;
}

contract SolidityConsumer {
    IStylusCounter public immutable stylusContract;

    constructor(address _stylusContract) {
        stylusContract = IStylusCounter(_stylusContract);
    }

    function readAndIncrement() external returns (uint256) {
        uint256 before = stylusContract.getCount();
        stylusContract.increment();
        return before;
    }
}
```

### Calling Stylus with ETH Value

```rust
use stylus_sdk::call::Call;
use alloy_primitives::U256;

sol_interface! {
    interface IPayable {
        function deposit() external payable returns (uint256);
    }
}

// Send ETH with the call
let config = Call::new_in(self).value(U256::from(1_000_000_000_000_000_000u128));
let result = payable_contract.deposit(config)?;
```

### Shared Storage Pattern

Stylus and Solidity contracts on the same address (via proxy) share the same storage layout. Slot positions must match exactly:

```
Slot 0: StorageU256 in Stylus  =  uint256 in Solidity
Slot 1: StorageAddress in Stylus  =  address in Solidity
Slot 2: StorageMap<Address, StorageU256>  =  mapping(address => uint256) in Solidity
```

This enables upgradeable proxy patterns where the implementation can switch between Solidity and Stylus.

## Gas Model

### Ink Pricing

Stylus uses "ink" as its internal gas metering unit for WASM execution. The conversion rate is configurable per chain:

| Parameter | Default Value |
|-----------|--------------|
| Ink per gas | 10,000 |
| WASM memory page cost | 50,000 gas |
| Activation base cost | ~14M gas |

From the user's perspective, gas is gas — they pay in ETH. The ink conversion happens internally.

### Cost Comparison

| Operation | EVM (Solidity) | WASM (Stylus) | Savings |
|-----------|---------------|---------------|---------|
| Memory allocation | ~3 gas/byte | ~0.003 gas/byte | ~1000x |
| Keccak256 | 30 + 6/word gas | ~11.5 gas/word | ~3x |
| Storage read (SLOAD) | 2100 gas (cold) | 2100 gas (cold) | Same |
| Storage write (SSTORE) | 20000 gas (cold) | 20000 gas (cold) | Same |
| Compute-heavy math | High | 10-100x cheaper | 10-100x |

Storage costs are identical because both VMs use the same EVM storage layer. The savings come from compute, memory, and complex logic.

### When Stylus Wins

- **Cryptographic operations**: Custom hash functions, signature verification, ZK proof verification
- **Data processing**: Parsing, encoding/decoding large payloads, compression
- **Complex math**: Financial models, AMM curves, options pricing
- **Memory-heavy operations**: Sorting, large array manipulation, string processing

### When Solidity is Fine

- Simple token contracts (ERC20, ERC721)
- Basic governance and voting
- Straightforward DeFi (lending, staking with standard math)
- Contracts that are mostly storage reads/writes

## Key Advantages

1. **10-100x gas savings for compute** — WASM opcodes are dramatically cheaper than EVM opcodes for math, memory, and cryptography.
2. **Rust safety guarantees** — No reentrancy bugs from accidental state mutation. The borrow checker catches classes of bugs that Solidity cannot.
3. **Existing Rust ecosystem** — Use any `no_std` Rust crate. Cryptographic libraries, parsers, math libraries — all available.
4. **Same chain, same state** — No bridging. Stylus contracts coexist with Solidity contracts on Arbitrum One. They share liquidity and composability.
5. **Standard ABI** — Callers cannot tell if a contract is Solidity or Stylus. Same tools, same interfaces, same explorers.
6. **Memory efficiency** — WASM memory costs ~1000x less than EVM memory, enabling data-intensive applications.

## Limitations

- **No CREATE/CREATE2** — Cannot deploy contracts from Stylus. Factory patterns must be Solidity.
- **No delegatecall from Stylus** — Proxy implementations in Stylus have constraints. The proxy itself should be in Solidity.
- **Activation cost** — Each contract must be activated (~14M gas). This is a one-time cost but can be significant.
- **No floating point** — WASM determinism requirement forbids IEEE 754 floats. Use fixed-point.
- **Limited precompile access** — Some EVM precompiles may not be available from WASM. Check the Stylus docs for the current supported set.
- **Debugging is harder** — No equivalent of Foundry's `console.log`. Use events for debugging, or test with `cargo test` locally.
- **Smaller ecosystem** — Fewer auditors, fewer examples, fewer battle-tested patterns compared to Solidity.

## ArbWasm Precompile

The `ArbWasm` precompile (address `0x0000000000000000000000000000000000000071`) manages Stylus programs on-chain.

| Function | Description |
|----------|-------------|
| `activateProgram(address)` | Compile WASM to native code (required before first call) |
| `programVersion(address)` | Get the Stylus version of a deployed program |
| `codehashVersion(bytes32)` | Check if a codehash is activated |
| `stylusVersion()` | Current Stylus VM version on the chain |
| `inkPrice()` | Current ink-to-gas conversion ratio |

```bash
# Check if a contract is activated
cast call 0x0000000000000000000000000000000000000071 \
  "programVersion(address)(uint16)" \
  0xYourContract \
  --rpc-url https://arb1.arbitrum.io/rpc
```

## References

- [Stylus Documentation](https://docs.arbitrum.io/stylus/stylus-gentle-introduction)
- [stylus-sdk crate](https://crates.io/crates/stylus-sdk)
- [stylus-sdk API docs](https://docs.rs/stylus-sdk)
- [cargo-stylus CLI](https://github.com/OffchainLabs/cargo-stylus)
- [Stylus Examples (Offchain Labs)](https://github.com/OffchainLabs/stylus-sdk-rs/tree/main/examples)
- [Stylus by Example](https://stylus-by-example.org)
- [Arbitrum One Explorer](https://arbiscan.io)
- [Arbitrum Sepolia Faucet](https://faucet.quicknode.com/arbitrum/sepolia)
