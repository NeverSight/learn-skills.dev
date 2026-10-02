---
name: starknet
description: StarkNet development with Cairo — smart contract patterns, native account abstraction, Scarb package manager, starknet.js integration, deployment, testing, and L1-L2 messaging.
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: starknet
  category: L2 & Alt-L1
tags:
  - starknet
  - cairo
  - zk-rollup
  - layer-2
  - account-abstraction
---

# StarkNet Development Guide

StarkNet is a permissionless validity rollup (ZK-rollup) on Ethereum. Smart contracts are written in Cairo, a provable computation language that compiles to Sierra (Safe Intermediate Representation) and then to CASM (Cairo Assembly) for execution. Every account on StarkNet is a smart contract — there are no EOAs.

## What You Probably Got Wrong

> AI agents trained on EVM patterns make critical errors when generating StarkNet/Cairo code. Fix these first.

- **StarkNet is NOT EVM-compatible** — Cairo is a completely different language from Solidity. There is no `msg.value`, no `payable`, no `receive()`. ETH is an ERC-20 token on StarkNet, transferred via the ETH token contract like any other token.
- **`felt252` is not `uint256`** — The native type is `felt252`, a field element modulo a 252-bit prime. It wraps on overflow (not revert). For safe arithmetic or values > 252 bits, use `u256` (which is a struct of two `u128` values internally).
- **Every account is a smart contract** — There are no externally owned accounts. Deploying your first contract requires a pre-funded account contract. Account contracts implement `__validate__` and `__execute__` entrypoints.
- **Deployment is two steps: declare then deploy** — First you declare the contract class (uploading the code). Then you deploy instances of that class. Multiple contracts can share one class hash. This is fundamentally different from EVM's single `CREATE`/`CREATE2`.
- **There is no `constructor` keyword** — Cairo contracts use a `#[constructor]` attribute on a function. It runs once at deployment and cannot be called again.
- **Sierra compilation is mandatory** — You write Cairo, Scarb compiles to Sierra (safe bytecode), and the sequencer compiles Sierra to CASM. You never deploy raw Cairo. Sierra guarantees provability — every execution path can be proven.
- **Transaction fees are paid in STRK or ETH** — StarkNet supports fee payment in either STRK (native token) or ETH. The fee token is specified per transaction.
- **Storage is `felt252`-based, not 32-byte slots** — StarkNet storage maps `felt252` keys to `felt252` values. Complex types like `Map<K, V>` use Pedersen hashing of the key + variable address for slot computation.
- **Function selectors use `sn_keccak`** — Unlike Solidity's 4-byte keccak256 selectors, StarkNet uses `sn_keccak(function_name)` which is the first 250 bits of keccak256.

## Quick Start

### Install Scarb (Cairo Package Manager + Build Tool)

```bash
# Install via asdf (recommended)
asdf plugin add scarb
asdf install scarb latest
asdf global scarb latest

# Or via the official installer
curl --proto '=https' --tlsv1.2 -sSf https://docs.swmansion.com/scarb/install.sh | sh

# Verify
scarb --version
```

### Install Starknet Foundry (Testing + Deployment)

```bash
# Install snfoundryup
curl -L https://raw.githubusercontent.com/foundry-rs/starknet-foundry/master/scripts/install.sh | sh

# Install latest snforge and sncast
snfoundryup

# Verify
snforge --version
sncast --version
```

### Install starkli (CLI for StarkNet Interaction)

```bash
# Install starkliup
curl https://get.starkli.sh | sh

# Install starkli
starkliup

# Verify
starkli --version
```

### Create a New Cairo Project

```bash
scarb new my_contract
cd my_contract
```

This generates:

```
my_contract/
  src/
    lib.cairo
  Scarb.toml
```

### Scarb.toml Configuration

```toml
[package]
name = "my_contract"
version = "0.1.0"
edition = "2024_07"

[dependencies]
starknet = ">=2.9.0"

[[target.starknet-contract]]
sierra = true
casm = true
```

## Chain Configuration

### Mainnet

| Property | Value |
|----------|-------|
| Chain ID | `SN_MAIN` |
| Currency | STRK / ETH (18 decimals) |
| Block Time | ~6 minutes (L2 blocks), with continuous proving |
| RPC (Public) | `https://starknet-mainnet.public.blastapi.io/rpc/v0_7` |
| RPC (Alchemy) | `https://starknet-mainnet.g.alchemy.com/starknet/version/rpc/v0_7/<KEY>` |
| RPC (Infura) | `https://starknet-mainnet.infura.io/v3/<KEY>` |
| Explorer (Voyager) | `https://voyager.online` |
| Explorer (Starkscan) | `https://starkscan.co` |

### Sepolia Testnet

| Property | Value |
|----------|-------|
| Chain ID | `SN_SEPOLIA` |
| Currency | STRK / ETH (test tokens) |
| RPC (Public) | `https://starknet-sepolia.public.blastapi.io/rpc/v0_7` |
| Faucet | `https://starknet-faucet.vercel.app` |
| Explorer (Voyager) | `https://sepolia.voyager.online` |
| Explorer (Starkscan) | `https://sepolia.starkscan.co` |

## Cairo Language Basics

### Primitive Types

| Type | Description |
|------|-------------|
| `felt252` | Field element, native type (~252 bits). Wraps on overflow. |
| `u8`, `u16`, `u32`, `u64`, `u128`, `u256` | Unsigned integers. Panic on overflow. |
| `i8`, `i16`, `i32`, `i64`, `i128` | Signed integers. |
| `bool` | `true` or `false` |
| `ContractAddress` | StarkNet address type |
| `ClassHash` | Hash of a declared contract class |
| `ByteArray` | Dynamic byte array for strings |

### Storage Types

```cairo
#[storage]
struct Storage {
    owner: ContractAddress,
    balance: u256,
    name: ByteArray,
    // Map is the equivalent of Solidity's mapping
    balances: Map<ContractAddress, u256>,
    // Nested maps
    allowances: Map<(ContractAddress, ContractAddress), u256>,
}
```

### Interfaces

```cairo
#[starknet::interface]
pub trait IMyContract<TContractState> {
    fn get_balance(self: @TContractState, account: ContractAddress) -> u256;
    fn transfer(ref self: TContractState, to: ContractAddress, amount: u256);
}
```

- `self: @TContractState` = read-only (view) function
- `ref self: TContractState` = state-mutating (external) function

### Events

```cairo
#[event]
#[derive(Drop, starknet::Event)]
pub enum Event {
    Transfer: Transfer,
    Approval: Approval,
}

#[derive(Drop, starknet::Event)]
pub struct Transfer {
    #[key]
    pub from: ContractAddress,
    #[key]
    pub to: ContractAddress,
    pub amount: u256,
}
```

`#[key]` fields are indexed (like Solidity's `indexed`).

## Smart Contract Patterns

### Basic Contract

```cairo
#[starknet::contract]
pub mod Counter {
    use starknet::storage::{StoragePointerReadAccess, StoragePointerWriteAccess};

    #[storage]
    struct Storage {
        count: u128,
    }

    #[event]
    #[derive(Drop, starknet::Event)]
    pub enum Event {
        CountIncremented: CountIncremented,
    }

    #[derive(Drop, starknet::Event)]
    pub struct CountIncremented {
        pub new_count: u128,
    }

    #[constructor]
    fn constructor(ref self: ContractState, initial_count: u128) {
        self.count.write(initial_count);
    }

    #[abi(embed_v0)]
    impl CounterImpl of super::ICounter<ContractState> {
        fn get_count(self: @ContractState) -> u128 {
            self.count.read()
        }

        fn increment(ref self: ContractState) {
            let current = self.count.read();
            let new_count = current + 1;
            self.count.write(new_count);
            self.emit(CountIncremented { new_count });
        }
    }
}
```

### Ownable Pattern

```cairo
#[starknet::contract]
pub mod OwnableContract {
    use starknet::{ContractAddress, get_caller_address};
    use starknet::storage::{StoragePointerReadAccess, StoragePointerWriteAccess};
    use core::num::traits::Zero;

    #[storage]
    struct Storage {
        owner: ContractAddress,
    }

    #[event]
    #[derive(Drop, starknet::Event)]
    pub enum Event {
        OwnershipTransferred: OwnershipTransferred,
    }

    #[derive(Drop, starknet::Event)]
    pub struct OwnershipTransferred {
        pub previous_owner: ContractAddress,
        pub new_owner: ContractAddress,
    }

    mod Errors {
        pub const NOT_OWNER: felt252 = 'Caller is not the owner';
        pub const ZERO_ADDRESS: felt252 = 'New owner is zero address';
    }

    #[constructor]
    fn constructor(ref self: ContractState, owner: ContractAddress) {
        assert(owner.is_non_zero(), Errors::ZERO_ADDRESS);
        self.owner.write(owner);
    }

    #[generate_trait]
    impl InternalImpl of InternalTrait {
        fn assert_only_owner(self: @ContractState) {
            let caller = get_caller_address();
            assert(caller == self.owner.read(), Errors::NOT_OWNER);
        }
    }

    #[abi(embed_v0)]
    impl OwnableImpl of super::IOwnable<ContractState> {
        fn get_owner(self: @ContractState) -> ContractAddress {
            self.owner.read()
        }

        fn transfer_ownership(ref self: ContractState, new_owner: ContractAddress) {
            self.assert_only_owner();
            assert(new_owner.is_non_zero(), Errors::ZERO_ADDRESS);
            let previous_owner = self.owner.read();
            self.owner.write(new_owner);
            self.emit(OwnershipTransferred { previous_owner, new_owner });
        }
    }
}
```

### Component Pattern (Reusable Modules)

Components are StarkNet's answer to Solidity's inheritance — reusable contract logic that can be embedded into any contract. A component defines its own storage, events, and implementations. The host contract uses `component!()` macro to embed it.

```cairo
// Define a component
#[starknet::component]
pub mod OwnableComponent {
    #[storage]
    struct Storage { owner: ContractAddress }

    #[embeddable_as(OwnableImpl)]
    impl Ownable<TContractState, +HasComponent<TContractState>>
        of super::IOwnable<ComponentState<TContractState>> { /* ... */ }
}

// Use in a contract
#[starknet::contract]
pub mod MyContract {
    component!(path: OwnableComponent, storage: ownable, event: OwnableEvent);

    #[abi(embed_v0)]
    impl OwnableImpl = OwnableComponent::OwnableImpl<ContractState>;

    #[storage]
    struct Storage {
        #[substorage(v0)]
        ownable: OwnableComponent::Storage,
    }

    #[event]
    #[derive(Drop, starknet::Event)]
    pub enum Event {
        #[flat]
        OwnableEvent: OwnableComponent::Event,
    }
}
```

See `examples/cairo-contract/` for full component implementations.

## Native Account Abstraction

Every StarkNet account is a smart contract. There are no EOAs. Account contracts must implement these entrypoints:

### Account Contract Interface

```cairo
#[starknet::interface]
pub trait IAccount<TContractState> {
    fn __validate__(ref self: TContractState, calls: Array<Call>) -> felt252;
    fn __execute__(ref self: TContractState, calls: Array<Call>) -> Array<Span<felt252>>;
    fn is_valid_signature(
        self: @TContractState, hash: felt252, signature: Array<felt252>,
    ) -> felt252;
}

#[starknet::interface]
pub trait IAccountDeployable<TContractState> {
    fn __validate_deploy__(
        self: @TContractState,
        class_hash: felt252,
        salt: felt252,
        public_key: felt252,
    ) -> felt252;
}
```

### How Account Transactions Work

1. User signs a transaction with their private key
2. Sequencer calls `__validate__` on the account contract — this verifies the signature
3. If validation passes, sequencer calls `__execute__` — this dispatches the actual calls
4. `__validate__` must return `VALID` (`'VALID'` as a felt252) to proceed

### Multicall is Native

Because `__execute__` receives an `Array<Call>`, every account natively supports batching multiple calls in a single transaction. No multicall contract needed.

```cairo
// Account's __execute__ iterates through calls
fn __execute__(ref self: ContractState, calls: Array<Call>) -> Array<Span<felt252>> {
    let mut results: Array<Span<felt252>> = array![];
    for call in calls {
        let result = starknet::call_contract_syscall(
            call.to, call.selector, call.calldata.span(),
        ).unwrap();
        results.append(result);
    };
    results
}
```

## Deployment

### Step 1: Build with Scarb

```bash
scarb build
```

Outputs Sierra JSON to `target/dev/<package_name>_<contract_name>.contract_class.json`.

### Step 2: Declare (Upload Class)

```bash
# Using starkli
starkli declare target/dev/my_contract_Counter.contract_class.json \
  --account ~/.starkli-wallets/deployer/account.json \
  --keystore ~/.starkli-wallets/deployer/keystore.json \
  --rpc https://starknet-sepolia.public.blastapi.io/rpc/v0_7

# Returns: class hash 0x...
```

### Step 3: Deploy (Instantiate Contract)

```bash
# Deploy with constructor args
starkli deploy <CLASS_HASH> \
  <constructor_arg_1> <constructor_arg_2> \
  --account ~/.starkli-wallets/deployer/account.json \
  --keystore ~/.starkli-wallets/deployer/keystore.json \
  --rpc https://starknet-sepolia.public.blastapi.io/rpc/v0_7

# Returns: deployed contract address 0x...
```

### Using sncast (Starknet Foundry)

```bash
# Declare
sncast declare --contract-name Counter

# Deploy
sncast deploy --class-hash <CLASS_HASH> --constructor-calldata 0x0

# Invoke a function
sncast invoke --contract-address <ADDRESS> --function increment

# Call a view function
sncast call --contract-address <ADDRESS> --function get_count
```

### Universal Deployer Contract (UDC)

The UDC allows deploying contracts from other contracts or with deterministic addresses (like CREATE2).

Address: `0x041a78e741e5af2fec34b695679bc6891742439f7afb8484ecd7766661ad02bf` (same on mainnet and testnet).

## Testing with snforge

### Unit Tests

```cairo
#[cfg(test)]
mod tests {
    use super::{Counter, ICounterDispatcher, ICounterDispatcherTrait};
    use snforge_std::{declare, ContractClassTrait, DeclareResultTrait};

    fn deploy_counter(initial_count: u128) -> ICounterDispatcher {
        let contract = declare("Counter").unwrap().contract_class();
        let mut calldata: Array<felt252> = array![];
        calldata.append(initial_count.into());
        let (address, _) = contract.deploy(@calldata).unwrap();
        ICounterDispatcher { contract_address: address }
    }

    #[test]
    fn test_initial_count() {
        let counter = deploy_counter(42);
        assert(counter.get_count() == 42, 'Wrong initial count');
    }

    #[test]
    fn test_increment() {
        let counter = deploy_counter(0);
        counter.increment();
        assert(counter.get_count() == 1, 'Should be 1');
    }
}
```

### Testing with Cheatcodes

```cairo
use snforge_std::{start_cheat_caller_address, stop_cheat_caller_address};
use starknet::contract_address_const;

#[test]
fn test_owner_only() {
    let owner = contract_address_const::<0x1>();
    let not_owner = contract_address_const::<0x2>();
    let contract = deploy_ownable(owner);

    // Prank caller to be not_owner
    start_cheat_caller_address(contract.contract_address, not_owner);

    // This should panic
    contract.transfer_ownership(not_owner);

    stop_cheat_caller_address(contract.contract_address);
}

#[test]
#[should_panic(expected: 'Caller is not the owner')]
fn test_non_owner_reverts() {
    let owner = contract_address_const::<0x1>();
    let attacker = contract_address_const::<0x2>();
    let contract = deploy_ownable(owner);

    start_cheat_caller_address(contract.contract_address, attacker);
    contract.transfer_ownership(attacker);
}
```

### Running Tests

```bash
# Run all tests
snforge test

# Run specific test
snforge test test_increment

# Run with gas reporting
snforge test --detailed-resources
```

## Starknet.js Integration

### Installation

```bash
npm install starknet
```

### Provider Setup

```typescript
import { RpcProvider } from "starknet";

const provider = new RpcProvider({
  nodeUrl: "https://starknet-mainnet.public.blastapi.io/rpc/v0_7",
});

const block = await provider.getBlockLatestAccepted();
const chainId = await provider.getChainId();
```

### Account Setup

```typescript
import { Account, RpcProvider } from "starknet";

const provider = new RpcProvider({
  nodeUrl: process.env.STARKNET_RPC_URL!,
});

const account = new Account(
  provider,
  process.env.ACCOUNT_ADDRESS!,
  process.env.PRIVATE_KEY!,
);
```

### Contract Interaction

```typescript
import { Contract, RpcProvider } from "starknet";

const provider = new RpcProvider({
  nodeUrl: process.env.STARKNET_RPC_URL!,
});

const abi = [/* ABI JSON from compiled contract */];
const contract = new Contract(abi, contractAddress, provider);

// Read (call)
const balance = await contract.get_balance(accountAddress);

// Write (invoke) — requires account, not just provider
contract.connect(account);
const tx = await contract.increment();
await provider.waitForTransaction(tx.transaction_hash);
```

### Multicall

```typescript
// Execute multiple calls in a single transaction
const tx = await account.execute([
  {
    contractAddress: tokenAddress,
    entrypoint: "approve",
    calldata: [spenderAddress, amountLow, amountHigh],
  },
  {
    contractAddress: routerAddress,
    entrypoint: "swap",
    calldata: [/* swap params */],
  },
]);

await provider.waitForTransaction(tx.transaction_hash);
```

## L1-L2 Messaging

### L2 to L1 (Cairo)

```cairo
use starknet::syscalls::send_message_to_l1_syscall;

fn send_to_l1(ref self: ContractState, to_l1_address: felt252, payload: Span<felt252>) {
    send_message_to_l1_syscall(to_l1_address, payload).unwrap();
}
```

### L1 to L2 (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IStarknetCore {
    function sendMessageToL2(
        uint256 toAddress,
        uint256 selector,
        uint256[] calldata payload
    ) external payable returns (bytes32 msgHash, uint256 nonce);

    function consumeMessageFromL2(
        uint256 fromAddress,
        uint256[] calldata payload
    ) external returns (bytes32);
}
```

### Message Lifecycle

1. **L2->L1**: Cairo contract calls `send_message_to_l1_syscall`. Message is included in the L2 state update posted to L1. L1 contract calls `consumeMessageFromL2` on StarkNet Core to process it.
2. **L1->L2**: Solidity contract calls `sendMessageToL2` on StarkNet Core (with fee). StarkNet sequencer automatically invokes the `#[l1_handler]` function on the target L2 contract.

### L1 Handler in Cairo

```cairo
#[l1_handler]
fn handle_deposit(
    ref self: ContractState,
    from_address: felt252,
    // Payload fields follow
    user: ContractAddress,
    amount: u256,
) {
    // from_address is the L1 sender contract address — validate it
    assert(from_address == self.l1_bridge_address.read(), 'Invalid L1 sender');
    self.balances.write(user, self.balances.read(user) + amount);
}
```

## Key Differences from EVM

| Concept | EVM (Solidity) | StarkNet (Cairo) |
|---------|---------------|-----------------|
| Account model | EOA + contract accounts | All accounts are contracts |
| Native token transfer | `msg.value`, `payable` | Call ETH token contract (ERC-20) |
| Compilation | Solidity -> EVM bytecode | Cairo -> Sierra -> CASM |
| Deployment | Single tx deploys contract | Declare class, then deploy instance |
| Integer type | `uint256` native | `felt252` native, `u256` is a struct |
| Overflow | Reverts (Solidity 0.8+) | `felt252` wraps, `u128`/`u256` panics |
| Function selector | `bytes4(keccak256("fn(types)"))` | `sn_keccak("fn_name")` (first 250 bits) |
| Reentrancy | Major concern | No direct reentrancy (sequential execution) |
| Inheritance | `contract A is B, C` | Component pattern |
| Constructor | `constructor()` | `#[constructor] fn constructor()` |
| Events | `event Transfer(...)` | `#[derive(starknet::Event)] struct Transfer` |
| Storage | 32-byte slots, keccak256 | felt252-based, Pedersen hash |
| Proxy pattern | Delegatecall proxy | Class hash replacement (`replace_class_syscall`) |
| Batch calls | Multicall contract | Native via `__execute__` |
| Block timestamp | `block.timestamp` | `starknet::get_block_timestamp()` |
| Caller | `msg.sender` | `starknet::get_caller_address()` |
| This address | `address(this)` | `starknet::get_contract_address()` |

## OpenZeppelin Cairo Contracts

OpenZeppelin provides audited, production-ready components for StarkNet. Add to `Scarb.toml`:

```toml
[dependencies]
openzeppelin_token = "0.20.0"
openzeppelin_access = "0.20.0"
```

Available components: ERC20, ERC721, ERC1155, Ownable, AccessControl, Pausable, Upgradeable, ReentrancyGuard, and more. Each is a `#[starknet::component]` that you embed via `component!()` macro. See `examples/cairo-contract/` for a full ERC-20 token example using OpenZeppelin.

## Ecosystem

### Major Protocols

| Protocol | Category | Description |
|----------|----------|-------------|
| JediSwap | DEX | AMM based on Uniswap V2/V3 model |
| Ekubo | DEX | Concentrated liquidity DEX, highest TVL on StarkNet |
| mySwap | DEX | AMM with concentrated liquidity |
| Nostra | Lending | Lending and borrowing protocol |
| zkLend | Lending | Money market protocol |
| Carmine | Options | Options AMM |
| Braavos | Wallet | Smart wallet with hardware signer |
| Argent X | Wallet | Most popular StarkNet wallet |
| Pragma | Oracle | Native StarkNet oracle network |
| Realms/Loot | Gaming | On-chain game ecosystem (Dojo framework) |

### Development Tools

| Tool | Purpose |
|------|---------|
| Scarb | Package manager + build tool (like Cargo for Cairo) |
| snforge | Testing framework (Starknet Foundry) |
| sncast | CLI for contract interaction (Starknet Foundry) |
| starkli | Low-level CLI for StarkNet |
| Voyager | Block explorer |
| Starkscan | Block explorer (alternative) |
| Katana | Local StarkNet node (from Dojo) |
| Dojo | On-chain game engine framework |

### RPC Providers

| Provider | Free Tier | URL |
|----------|-----------|-----|
| Blast API | Yes | `https://starknet-mainnet.public.blastapi.io` |
| Alchemy | Yes | `https://starknet-mainnet.g.alchemy.com/starknet/version/rpc/v0_7/` |
| Infura | Yes | `https://starknet-mainnet.infura.io/v3/` |
| Chainstack | Yes | `https://starknet-mainnet.core.chainstack.com/` |
| Nethermind | Yes | Via Juno node |

## References

- [Cairo Book](https://book.cairo-lang.org/)
- [StarkNet Documentation](https://docs.starknet.io/)
- [Starknet Foundry Book](https://foundry-rs.github.io/starknet-foundry/)
- [starknet.js Documentation](https://starknetjs.com/)
- [OpenZeppelin Cairo Contracts](https://docs.openzeppelin.com/contracts-cairo/)
- [Voyager Explorer](https://voyager.online/)
- [Starkscan Explorer](https://starkscan.co/)
