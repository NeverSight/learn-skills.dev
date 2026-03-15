---
name: sablier-create-open-ended-stream
disable-model-invocation: false
user-invocable: true
argument-hint: <chain_name> <token_address> <payment_details>
description: This skill should be used when the user asks to create "payment streams", "token streaming", "onchain salary", "onchain payroll", "open-ended streams", "Sablier Flow streams", "adjustable-rate streams", "recurring payments", "continuous payments", "salary streaming", "EVM payment streams", "ERC-20 streaming", "ERC20 streaming", or "BEP-20 streaming", or "BEP20 streaming" with Sablier Flow, wants to stream tokens without an end date on Ethereum or EVM-compatible chains.
---

# Sablier Payment Stream Creation

## Overview

Create open-ended token payment streams using the Sablier Flow protocol. Flow streams accrue debt at a configurable rate per second with no predefined end date. Anyone can deposit tokens into a stream at any time to keep it solvent — no upfront funding is required. Each stream mints an NFT to the recipient.

This skill is a coordinator for payment stream creation and execution routing.

## Arguments

| Argument          | Description                                                                                                                                |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `chain_name`      | EVM chain where to create the payment stream                                                                                               |
| `token_address`   | ERC-20 token contract address to stream. Token symbols cannot be resolved to addresses — the user must provide the exact contract address. |
| `payment_details` | The streaming rate, recipient, and funding preference                                                                                      |

## Workflow

### 1. Confirm product fit before implementation details

1. Verify the user needs open-ended, rate-based token streaming with no predefined end date.
2. If the user needs fixed-schedule vesting, route to `sablier-create-vesting`. If this skill is unavailable, recommend installing it with:

```bash
npx skills add sablier-labs/sablier-skills --skill sablier-create-vesting
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

Treat the following as unsupported by this skill and by Sablier Flow:

- Tokens with more than 18 decimals. The Flow contract requires token decimals ≤ 18.
- Fixed-schedule vesting with upfront deposit and defined end date. Route to `sablier-create-vesting`.
- Launching tokens for users. Require the user to explicitly provide an existing token address as input.
- Resolving token symbols (e.g. "USDC") to contract addresses. If the user provides a symbol instead of an address, ask them to provide the exact ERC-20 contract address.
- Streaming native tokens (ETH, POL, etc.). Only ERC-20 tokens can be streamed. If the user wants to stream a native token, inform them they must wrap it first (e.g. WETH) and provide the wrapped token contract address.

### 3. Clarify payment details

If any of the following are missing or ambiguous from the user's input, use the `AskUserQuestion` tool to ask the user to clarify before proceeding:

- Chain name (e.g. "Ethereum", "Base", etc.)
- Streaming rate (amount of tokens per time period, e.g. "1000 USDC per month")
- Recipient address(es)
- Whether to fund the stream upfront (determines `create` vs `createAndDeposit`)
- If funding upfront: deposit amount

If the missing detail is the token address, tell the user they can look it up on a blockchain explorer such as Etherscan.

Do not guess or silently apply defaults for the streaming rate, recipient, or upfront funding decision. Only proceed once all required inputs are confirmed.

If the user explicitly requests a streaming amount `"per month"`:

- Inform the user that Sablier cannot deliver the exact same amount for each calendar month.
- Before the final broadcast confirmation, show a caveat that Flow uses a fixed per-second rate, calendar months have unequal numbers of seconds, and exact calendar-month equality is not possible.
- State that the requested `"per month"` amount will be implemented using a 30-day month approximation for the `ratePerSecond` calculation.
- Only add this caveat when the user explicitly used `"per month"` in their request.

### 4. Infer intent before selecting references

1. **Execution intent:** user wants the agent to create a payment stream on their behalf (run CLI transactions).
2. **Onchain integration intent:** user wants developer integration guidance.

### 5. Validate chain support before routing

1. Check whether the user's desired chain is listed on [Supported Chains](https://docs.sablier.com/concepts/chains).
2. If the chain is not supported, inform the user and stop execution of this skill.

### 6. Route in two steps

1. Classify the request as one of:
   - Open-ended stream creation on the user's behalf
   - Onchain integration guidance
   - Any other integration type (frontend, backend, indexer, etc.)
2. If the request is any other integration type, inform the user that this skill does not support non-onchain integrations and stop.
3. Otherwise, follow the route below.

| Intent                                          | EVM                                             | Solana                                                                                                       |
| ----------------------------------------------- | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Open-ended stream creation on the user's behalf | Use [evm-cli.md](references/evm-cli.md)         | Not yet supported. Direct the user to [solana.sablier.com](https://solana.sablier.com).                      |
| Onchain integration guidance                    | Use [evm-onchain.md](references/evm-onchain.md) | Not yet supported. Direct the user to [docs.sablier.com](https://docs.sablier.com/solana/sablier-on-solana). |

## Resources

- [Sablier Documentation](https://docs.sablier.com/llms.txt)
- [EVM Flow Deployments](https://docs.sablier.com/guides/flow/deployments.md)
- [Sablier Flow Monorepo](https://github.com/sablier-labs/flow)
- [EVM Integration Examples](https://github.com/sablier-labs/evm-examples/tree/main/flow)
