---
name: solidity-development
description: Solidity smart contract development workflow. Use when modifying smart contracts in apps/eth-contracts/contracts/.
---

# Solidity Development Workflow

Workflow for Solidity smart contract changes in the `apps/eth-contracts/` Foundry project.

## Prerequisites

**Use `git-workflow` Skill** for branch management, commit conventions, and PR creation.

## Applicable Directories

| Path | Description |
|------|-------------|
| `apps/eth-contracts/contracts/` | Smart contract source files |
| `apps/eth-contracts/script/` | Foundry deployment scripts |
| `apps/eth-contracts/test/` | Foundry test files (`*.t.sol`) |

## Toolchain

| Tool | Version | Role |
|------|---------|------|
| Foundry (`forge`) | 1.6.0-nightly | Compile, test, deploy |
| Solidity | `^0.8.34` | Smart contract language |
| OpenZeppelin Contracts | `^5.6.1` | ERC-20 / standard base contracts |
| bun | primary | npm package manager |
| solhint | `^6.0.3` | Solidity linter |
| dprint | `^0.52.0` | JS/TS formatter |

> **Note**: `forge` is installed at `~/.foundry/bin/forge` (may not be in PATH). Run with full path or add `~/.foundry/bin` to `PATH`.

## Setup (first time)

```bash
cd apps/eth-contracts

# 1. Install forge-std (Foundry testing/scripting library)
forge install foundry-rs/forge-std

# 2. Install npm dependencies (@openzeppelin/contracts, solhint, dprint)
bun install
```

## Verification Commands

```bash
cd apps/eth-contracts

forge build          # Compile all contracts (artifacts → out/)
forge test -v        # Run Foundry unit tests
bun run lint         # Solidity lint via solhint (must exit 0, zero errors)
bun run fmt          # Format JS/TS files via dprint (must exit 0)
```

## Deployment (local)

```bash
cd apps/eth-contracts
export PRIVATE_KEY=0x<deployer-private-key>
forge script script/DeployHYC.s.sol --rpc-url http://localhost:8545 --broadcast
# → outputs contract address, tx hash, gas usage
```

Compatible with both `anvil` and `geth` nodes at `http://localhost:8545`.

## Self-Review Checklist

### Code Quality

- [ ] Named imports used (`import {Foo} from "..."`) — no global imports
- [ ] NatSpec tags present (`@title`, `@author`, `@notice`, `@param`) on contracts and public functions
- [ ] Explicit visibility on all functions (constructors exempt in Solidity ≥0.8)
- [ ] Gas optimization considered
- [ ] Events emitted for state changes

### Security

- [ ] No reentrancy vulnerabilities
- [ ] No hardcoded private keys or sensitive values — use env vars
- [ ] `.env` added to `.gitignore`
- [ ] Access control properly implemented
- [ ] Integer overflow protection (Solidity ≥0.8 has built-in checks)

### Testing

- [ ] Foundry test file (`test/*.t.sol`) covers all acceptance criteria
- [ ] `forge test` passes with zero failures
- [ ] `bun run lint` exits 0 with zero solhint errors

## ABI / Go Bindings

After contract changes, if Go bindings are needed:

```bash
# 1. Compile
cd apps/eth-contracts
forge build

# 2. Regenerate Go bindings (if target ABI changed)
make gen-abi
```

## Related Chain Context

- ETH (Ethereum)
- ERC-20 token standard
- Local nodes: `anvil`, `geth` at `http://localhost:8545`

## Related Skills

- `git-workflow` - Branch, commit, PR workflow
- `github-issue-creation` - Task classification
