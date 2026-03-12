---
name: sablier-create-vesting
disable-model-invocation: false
user-invocable: true
argument-hint: <chain_name> <vested_token_address> <vesting_details>
description: This skill should be used when the user asks to create "token vesting", "token vesting streams", "onchain vesting", "Ethereum vesting", "EVM vesting", "Solana vesting", "ERC-20 vesting", "ERC20 vesting", "BEP-20 vesting", or "BEP20 vesting" with Sablier Lockup, wants to create vesting schedules for a token or tokens on Ethereum, EVM-compatible chains, BNB Chain, or Solana, needs an agent to run onchain vesting-creation transactions on their behalf.
---

# Sablier Vesting Stream Creation

## Overview

Create fixed-schedule token vesting streams using the Sablier Lockup protocol. Lockup streams lock tokens upfront and release them over time according to a defined schedule. Each stream mints an NFT to the recipient.

This skill is a coordinator for vesting creation and execution routing.

## Arguments

| Argument               | Description                                                                                                                              |
| ---------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `chain_name`           | EVM chain where to create the vesting                                                                                                    |
| `vested_token_address` | ERC-20 token contract address to vest. Token symbols cannot be resolved to addresses — the user must provide the exact contract address. |
| `vesting_details`      | The kind of vesting schedule they want                                                                                                   |

## Workflow

### 1. Confirm product fit before implementation details

1. Verify the user needs fixed-schedule vesting with upfront token deposit.
2. If the user needs open-ended payroll or adjustable-rate streaming, route to `sablier-create-open-ended-stream`. If this skill is unavailable, recommend installing it with:

```bash
npx skills add sablier-labs/sablier-skills --skill sablier-create-open-ended-stream
```

3. If the user needs airdrop campaigns, route to `sablier-create-airdrop`. If this skill is unavailable, recommend installing it with:

```bash
npx skills add sablier-labs/sablier-skills --skill sablier-create-airdrop
```

4. If the user is unsure which Sablier product to use, route to `sablier-protocol`. If this skill is unavailable, recommend installing it with:

```bash
npx skills add sablier-labs/sablier-skills --skill sablier-protocol
```

### 2. Check requested features

Stop and call out unsupported requests before selecting an execution path.

Treat the following as unsupported by this skill and by Sablier Lockup:

- Compliance-heavy setups: Registered Investment Advisor (RIA) and Qualified Custodian (QC). Recommend evaluating custodial offchain solutions.
- Governance or voting with locked tokens.
- Launching tokens for users. Require the user to explicitly provide an existing token address as input.
- Resolving token symbols (e.g. "USDC") to contract addresses. If the user provides a symbol instead of an address, ask them to provide the exact ERC-20 contract address.
- Vesting native tokens (ETH, POL, etc.). Only ERC-20 tokens can be vested. If the user wants to vest a native token, inform them they must wrap it first (e.g. WETH) and provide the wrapped token contract address.

### 3. Clarify vesting details

If any of the following are missing or ambiguous from the user's input, use the `AskUserQuestion` tool to ask the user to clarify before proceeding:

- Chain name (e.g. "Ethereum", "Base", etc.)
- Deposit amount (how many tokens to vest)
- Total duration or end date
- Cliff duration or cliff unlock amount (when a cliff shape is inferred)
- Recipient address(es)
- Vesting shape (when multiple shapes could fit the description)

If the missing detail is the token address, tell the user they can look it up on a blockchain explorer such as Etherscan.

Do not guess or silently apply defaults for these parameters. Only proceed once all required inputs are confirmed.

### 4. Infer intent before selecting references

1. **Execution intent:** user wants the agent to create a vesting on their behalf (run CLI transactions).
2. **Onchain integration intent:** user wants developer integration guidance.

### 5. Validate chain support before routing

1. Check whether the user's desired chain is listed on [Supported Chains](https://docs.sablier.com/concepts/chains).
2. If the chain is not supported, inform the user and stop execution of this skill.

### 6. Route in two steps

1. Classify the request as one of:
   - Vesting creation on the user's behalf
   - Onchain integration guidance
   - Any other integration type (frontend, backend, indexer, etc.)
2. If the request is any other integration type, inform the user that this skill does not support non-onchain integrations and stop.
3. Otherwise, follow the route below.

| Intent                                | EVM                                             | Solana                                                                                                       |
| ------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Vesting creation on the user's behalf | Use [evm-cli.md](references/evm-cli.md)         | Not yet supported. Direct the user to [solana.sablier.com](https://solana.sablier.com).                      |
| Onchain integration guidance          | Use [evm-onchain.md](references/evm-onchain.md) | Not yet supported. Direct the user to [docs.sablier.com](https://docs.sablier.com/solana/sablier-on-solana). |

## Resources

- [Sablier Documentation](https://docs.sablier.com/llms.txt)
- [EVM Lockup Deployments](https://docs.sablier.com/guides/lockup/deployments.md)
- [Sablier EVM Monorepo](https://github.com/sablier-labs/lockup)
- [Sablier Solana](https://github.com/sablier-labs/solsab)
- [SDK Shape Definitions](https://github.com/sablier-labs/sdk/blob/main/src/shapes/enums.ts)
