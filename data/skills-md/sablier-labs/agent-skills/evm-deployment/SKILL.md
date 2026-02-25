---
name: evm-deployment
description: Deploy Sablier EVM contracts (Comptroller, ERC20 Faucet, Flow, Lockup, Airdrops) with full workflow automation. This skill should be used when the user asks to "deploy", "deploy protocol", "deploy to chain", or mentions deployment-related tasks. Handles contract deployment, explorer verification, SDK updates, and sample data creation through Init script.
---

## Overview

End-to-end deployment workflow for Sablier EVM contracts. Supports Comptroller, Flow, Lockup, and Airdrops with
protocol-specific adaptations.

## Prerequisites

### Version Check

Before proceeding, verify Foundry version:

```bash
forge -V
```

**Stop if version is below 1.3.6.**

## Protocol Detection

Detect the current EVM protocol from `package.json`:

| Package Name         | Protocol    | SDK Path                         |
| -------------------- | ----------- | -------------------------------- |
| `@sablier/evm-utils` | Comptroller | `../sdk/deployments/comptroller` |
| `@sablier/flow`      | Flow        | `../sdk/deployments/flow`        |
| `@sablier/lockup`    | Lockup      | `../sdk/deployments/lockup`      |
| `@sablier/airdrops`  | Airdrops    | `../sdk/deployments/airdrops`    |

Extract version from `package.json` → `"version": "x.y.z"` → SDK version is `v<x.y>`

## Workflow

Execute steps **in order**, tracking state between each:

### Step 1: Deploy Contracts

Reference: `./references/deploy.md` | Examples: `./references/examples.md`

Deploy protocol contracts using Foundry. Handles:

- RPC configuration
- Deterministic (CREATE2) vs non-deterministic (CREATE) deployment
- Contract verification on block explorer

### Step 2: Update SDK (optional)

Reference: `./references/copy-to-sdk.md`

Copy broadcast artifacts to SDK repository:

- Broadcast JSON file
- Update README.md with deployment info
- Update deployments.ts with contract addresses

### Step 3: Create Test Data (optional)

Reference: `./references/deploy-streams.md`

For Flow and Lockup protocols only. Creates sample streams for testing:

- Mint or verify ERC20 token balance
- Run Init.s.sol script to create test streams

## State Tracking

Track and carry forward between steps:

| State              | Source                                   |
| ------------------ | ---------------------------------------- |
| Protocol name      | Detected from `package.json`             |
| Chain ID           | From deployment or user input            |
| Chain name         | Lowercase (e.g., `ethereum`, `arbitrum`) |
| Deployment type    | `deterministic` or `non-deterministic`   |
| Contract addresses | From broadcast JSON `returns` field      |
| Block number       | From deployment receipt (hex → decimal)  |
| SDK version        | From `package.json` version              |

## Protocol-Specific Scripts

| Protocol    | Deterministic Script                        | Non-deterministic Script       |
| ----------- | ------------------------------------------- | ------------------------------ |
| Comptroller | `DeployDeterministicComptrollerProxy.s.sol` | `DeployComptrollerProxy.s.sol` |
| Flow        | `DeployDeterministicProtocol.s.sol`         | `DeployProtocol.s.sol`         |
| Lockup      | `DeployDeterministicProtocol.s.sol`         | `DeployProtocol.s.sol`         |
| Airdrops    | `DeployDeterministicFactories.s.sol`        | `DeployFactories.s.sol`        |

## Output Summary

After completion, provide:

- Protocol deployed
- Chain and deployment type
- Contract addresses (factories + campaigns if applicable)
- Verification status
- SDK files updated (if applicable)
- Test data created (if applicable)

### Airdrops Campaign Contracts

When deploying Airdrops test data, campaigns are created via factory:

| Factory                       | Campaign Contract      |
| ----------------------------- | ---------------------- |
| `SablierFactoryMerkleInstant` | `SablierMerkleInstant` |
| `SablierFactoryMerkleLL`      | `SablierMerkleLL`      |
| `SablierFactoryMerkleLT`      | `SablierMerkleLT`      |
| `SablierFactoryMerkleVCA`     | `SablierMerkleVCA`     |

Campaign addresses are returned in broadcast `returns` field, not `contractAddress`.
