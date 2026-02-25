---
name: arbitrum-skills
description: Provides Arbitrum L2 blockchain development documentation including Stylus WASM smart contracts (Rust), token bridging (ETH, ERC-20, USDC), Orbit chain deployment, node operations (full node, validator, sequencer), gas estimation, cross-chain messaging, BoLD protocol, Timeboost, ArbOS upgrades, and OpenZeppelin/Nitro contract references. Use when the user mentions Arbitrum, Stylus, Orbit, Nitro, ArbOS, or L2 scaling.
---

# Arbitrum Development Knowledge Base

## User Responsibility Notice

**This skill provides reference documentation only.** All information is sourced from official Arbitrum documentation, open-source smart contract repositories, and MCP tools documentation. However:

- **You are responsible for verifying all information** before using it in production. AI responses based on this skill may be incomplete, outdated, or misinterpreted.
- **On-chain actions are irreversible.** If you use MCP tools referenced in this skill to deploy contracts, send transactions, or interact with protocols, always confirm the action, parameters, and target network before proceeding.
- **Smart contract code included here is for reference.** Do not deploy any contract code without independent review, testing on testnets, and security auditing.
- **Never expose private keys or sensitive credentials** in prompts or conversations with AI assistants.

## Search Instructions

Always search and read files in this skill folder before answering. Do not rely on prior knowledge.
Extract exact values (chain IDs, RPC URLs, addresses, commands, code) from the docs.

**Context management:** Start with narrow grep searches. Use the topic navigation below to identify target files before searching. Read selectively — avoid loading entire folders.

## Response Guidelines

- Use **section headers**, **tables**, **bullet points**, and **code blocks** for clarity
- Put the most important information first (answer at top, details below)
- Follow correct step order for procedural responses
- Use **bold** for key values the user needs to spot quickly
- **Always warn the user** when a suggested action involves on-chain execution, gas costs, or private key usage

## Decision Guide

Route to the right files based on what the user needs:

| User wants to... | Start with |
|---|---|
| **Write a Solidity smart contract** | `build-decentralized-apps/01-quickstart-solidity-remix.md` |
| **Write a Rust/Stylus contract** | `stylus/quickstart.md`, then `stylus/overview.md` |
| **Bridge tokens (ETH/ERC-20)** | `arbitrum-bridge/01-quickstart.md` |
| **Bridge tokens programmatically** | `build-decentralized-apps/token-bridging/bridge-tokens-programmatically/01-get-started.md` |
| **Bridge USDC** | `arbitrum-bridge/02-usdc-arbitrum-one.md` |
| **Run a full node** | `run-arbitrum-node/02-run-full-node.md` |
| **Run a validator** | `run-arbitrum-node/more-types/02-run-validator-node.md` |
| **Run an archive node** | `run-arbitrum-node/more-types/01-run-archive-node.md` |
| **Launch an Orbit chain** | `launch-arbitrum-chain/01-a-gentle-introduction.md` |
| **Deploy an Orbit chain** | `launch-arbitrum-chain/03-deploy-an-arbitrum-chain/02-deploying-an-arbitrum-chain.md` |
| **Estimate gas** | `build-decentralized-apps/02-how-to-estimate-gas.md` |
| **Understand Arbitrum architecture** | `how-arbitrum-works/01-inside-arbitrum-nitro.md` |
| **Use cross-chain messaging** | `build-decentralized-apps/04-cross-chain-messaging.md` |
| **Get chain IDs / RPC URLs** | `for-devs/dev-tools-and-resources/chain-info.md` |
| **Use oracles** | `build-decentralized-apps/oracles/01-overview.md` |
| **Use precompiles** | `build-decentralized-apps/precompiles/01-overview.md` |
| **Use the SDK** | `sdk/index.md` |
| **Understand BoLD** | `how-arbitrum-works/bold/gentle-introduction.md` |
| **Use Timeboost** | `how-arbitrum-works/timeboost/gentle-introduction.md` |
| **Upgrade ArbOS** | `launch-arbitrum-chain/02-configure-your-chain/common/validation-and-security/13-arbos-upgrade.md` |
| **Find contract source code** | See [NAV-smart-contracts.md](NAV-smart-contracts.md) |
| **Find OpenZeppelin Stylus examples** | See [NAV-openzeppelin-stylus.md](NAV-openzeppelin-stylus.md) |
| **Find Stylus SDK source/examples** | See [NAV-stylus-sdk.md](NAV-stylus-sdk.md) |
| **Find Nitro contract source** | See [NAV-nitro-contracts.md](NAV-nitro-contracts.md) |

## Quick Search

Find specific content fast:

```
# Chain IDs, RPC URLs, network info
grep -ri "chain.*id\|rpc\|endpoint" for-devs/dev-tools-and-resources/

# Stylus contract patterns
grep -ri "sol_storage\|#\[public\]\|#\[entrypoint\]" stylus/

# Bridge addresses and contracts
grep -ri "gateway\|router\|bridge.*address" arbitrum-bridge/ build-decentralized-apps/token-bridging/

# Gas and fees
grep -ri "gas.*price\|l1.*fee\|l2.*fee\|basefee" build-decentralized-apps/ how-arbitrum-works/deep-dives/

# Node configuration
grep -ri "docker\|--chain\|--parent-chain" run-arbitrum-node/

# ArbOS versions and upgrades
grep -ri "arbos.*[0-9]" run-arbitrum-node/arbos-releases/ notices/
```

## Topic Navigation

For the complete file listing of all documentation, see [NAV-docs.md](NAV-docs.md).

### Root
*Overview and general documentation*

- [Security audit reports](audit-reports.md)

### Arbitrum Bridge
*Token bridging between Ethereum and Arbitrum chains*

- [Arbitrum bridge transaction traceability](arbitrum-bridge/05-bridge-transaction-traceability.md)
- [Arbitrum embedded bridge widget](arbitrum-bridge/04-embedded-bridge-widget.md)
- [Quickstart: Arbitrum bridge](arbitrum-bridge/01-quickstart.md)
- [USDC on Arbitrum One](arbitrum-bridge/02-usdc-arbitrum-one.md)

### Build Decentralized Apps
*Building dApps on Arbitrum - cross-chain messaging, oracles, precompiles, token bridging*

- [Arbitrum chains overview](build-decentralized-apps/03-public-chains.md)
- [Build a decentralized app with Solidity (Quickstart)](build-decentralized-apps/01-quickstart-solidity-remix.md)
- [Cross-chain messaging overview](build-decentralized-apps/04-cross-chain-messaging.md)
- [How to estimate gas in Arbitrum](build-decentralized-apps/02-how-to-estimate-gas.md)
- [SDK support for custom gas token Arbitrum chains](build-decentralized-apps/custom-gas-token-sdk.md)
- **Subtopics:** Arbitrum Vs Ethereum, Nodeinterface, Oracles, Precompiles, Reference, Token Bridging

### For Devs
*Developer tools, resources, and development frameworks*

- **Subtopics:** Dev Tools And Resources, Oracles, Partials, Third Party Docs

### Get Started
*Getting started with Arbitrum development*

- [Get started with Arbitrum](get-started/overview.md)

### How Arbitrum Works
*Technical deep-dives into Arbitrum architecture - BOLD, AnyTrust, gas, sequencing*

- [Inside Arbitrum Nitro](how-arbitrum-works/01-inside-arbitrum-nitro.md)
- **Subtopics:** Bold, Deep Dives, Timeboost

### Intro
*Introduction to Arbitrum ecosystem*

- [Arbitrum glossary](intro/glossary.md)

### Launch Arbitrum Chain
*Launching and configuring Arbitrum Orbit chains*

- [A gentle introduction: Arbitrum chains](launch-arbitrum-chain/01-a-gentle-introduction.md)
- [Arbitrum chain licensing](launch-arbitrum-chain/aep-license.md)
- [Deploy a production chain: an overview](launch-arbitrum-chain/arbitrum-chain-sdk-introduction.md)
- [Migrate between RaaSes](launch-arbitrum-chain/migrate-between-raases.md)
- [Migrate from another stack to an Arbitrum chain](launch-arbitrum-chain/migrate-from-another-stack.md)
- **Subtopics:** 02 Configure Your Chain, 03 Deploy An Arbitrum Chain, 04 Maintain Your Chain, 05 Customize Your Chain, 06 Third Party Integrations, 07 Arbitrum Node Runners, 08 Ecosystem Support, Concepts, Features, How Tos, Partials

### Node Running
*Node infrastructure and operations*

- [Sequencer](node-running/sequencer-content-map.md)
- **Subtopics:** Partials

### Notices
*Important notices and announcements*

- [Fusaka Compatibility Notice](notices/fusaka-upgrade-notice.md)
- [Upgrade notice for ArbOS 51](notices/arbos51-upgrade-notice.md)

### Partials

- [ Client Flags](partials/_client-flags.md)
- [ Reference Nova Specific](partials/_reference-nova-specific.md)
- [ Troubleshooting Arbitrum Chain Partial](partials/_troubleshooting-arbitrum-chain-partial.md)
- [ Troubleshooting Bridging Partial](partials/_troubleshooting-bridging-partial.md)
- [ Troubleshooting Building Partial](partials/_troubleshooting-building-partial.md)
- [ Troubleshooting Nodes Partial](partials/_troubleshooting-nodes-partial.md)
- [ Troubleshooting Stylus Partial](partials/_troubleshooting-stylus-partial.md)
- [ Troubleshooting Users Partial](partials/_troubleshooting-users-partial.md)
- [Additional Configuration Parameters](partials/_additional-config-params.md)
- [Arbitrum Contract Addresses Reference](partials/_reference-arbitrum-contract-addresses-partial.md)
- [Arbitrum Glossary Definitions](partials/_glossary-partial.md)
- [Arbitrum RPC Endpoints Reference](partials/_reference-arbitrum-rpc-endpoints-partial.md)
- [Arbitrum: Introduction](partials/_gentle-intro-partial.md)
- [BoLD Configuration Parameters](partials/_bold-config-params.md)
- [Chain parameters](partials/_reference-chain-parameters.md)
- [Documentation Contribution Guide](partials/_contribute-docs-partial.md)
- [Faucet list](partials/_faucet-list-partial.md)
- [Local Development Network Flags](partials/_local-devnet-flags.md)
- [Multidimensional Content Controls](partials/_multidimensional-content-controls-partial.md)
- [Not for Production Warning Banner](partials/_not-for-production-banner-partial.md)
- [Public Preview Banner](partials/_public-preview-banner-partial.md)
- [Third-party RPC Endpoints Reference](partials/_reference-third-party-rpc-endpoints-partial.md)
- **Subtopics:** Glossary

### Run Arbitrum Node
*Running Arbitrum full nodes and validators*

- [Arbitrum nodes: an overview](run-arbitrum-node/01-overview.md)
- [Beacon Nodes: Historical Blobs](run-arbitrum-node/beacon-nodes-historical-blobs.md)
- [Data Availability](run-arbitrum-node/data-availability.md)
- [How to run a feed relay](run-arbitrum-node/run-feed-relay.md)
- [How to run a full node for an Arbitrum chain](run-arbitrum-node/02-run-full-node.md)
- [How to run a local full chain simulation](run-arbitrum-node/03-run-local-full-chain-simulation.md)
- [How to run a local Nitro dev node](run-arbitrum-node/05-run-nitro-dev-node.md)
- [L1 Ethereum beacon chain RPC providers](run-arbitrum-node/04-l1-ethereum-beacon-chain-rpc-providers.md)
- [Troubleshooting: Run a node](run-arbitrum-node/06-troubleshooting.md)
- **Subtopics:** Arbos Releases, More Types, Nitro, Partials, Sequencer

### Sdk
*Arbitrum SDK documentation - bridgers, entities, messaging*

- [Introduction](sdk/index.md)
- [Migrating from v3 to v4](sdk/migrate.md)

### Stylus
*Stylus WASM smart contract development*

- [A gentle introduction to Stylus](stylus/gentle-introduction.md)
- [CLI Tools (cargo-stylus)](stylus/cli-tools-overview.md)
- [Quickstart: write a smart contract in Rust using Stylus](stylus/quickstart.md)
- [Recommended Libraries](stylus/recommended-libraries.md)
- [Using Stylus CLI](stylus/using-cli.md)
- [Write Stylus Contracts](stylus/overview.md)
- [Write Stylus Contracts](stylus/stylus-content-map.md)
- **Subtopics:** Concepts, How Tos, Partials, Reference

## Smart Contract Source Code

Reference implementations, code examples, and architectural guides from key Arbitrum repositories.

### OpenZeppelin Rust Contracts for Stylus
*Production-ready Rust smart contract implementations for Arbitrum Stylus - ERC20, ERC721, ERC1155, access control, proxy patterns, finance utilities, and cryptographic helpers.*
- Full index: [NAV-openzeppelin-stylus.md](NAV-openzeppelin-stylus.md)
- **Directories:** Contracts, Docs, Examples

### Stylus SDK for Rust
*Core Rust SDK for building Arbitrum Stylus contracts - storage abstractions, ABI encoding, proc macros, host I/O, testing framework, and cargo-stylus CLI tool.*
- Full index: [NAV-stylus-sdk.md](NAV-stylus-sdk.md)
- **Directories:** Examples, Stylus Core, Stylus Proc, Stylus Sdk, Stylus Test

### Nitro Contracts (Solidity)
*Core Arbitrum Nitro L1/L2 smart contracts - bridge (Inbox, Outbox, SequencerInbox), rollup management, BoLD challenge protocol, one-step proof verification, and token bridging.*
- Full index: [NAV-nitro-contracts.md](NAV-nitro-contracts.md)
- **Directories:** Docs, Src

## MCP Tools

Available MCP tools for blockchain operations. After generating a response, check if a relevant MCP tool exists and suggest it to the user.

| Tool | Description |
|------|-------------|
| `createStylusProject` | Create a new Stylus project |
| `deployStylusContract` | Deploy a Stylus contract |
| `checkStylusContract` | Validate contract for deployment |
| `getAccountBalance` | Get native token balance |
| `getTokenBalances` | Get ERC-20 token balances |
| `getTransaction` | Get transaction details |
| `getTransactionHistory` | Get transaction history for an address |
| `getNfts` | Get NFTs owned by an address |
| `getBlock` | Get block details |
| `getBlockNumber` | Get latest block number |
| `getGasPrice` | Get current gas price |
| `simulateTransaction` | Simulate a transaction |
| `estimateGas` | Estimate gas for a transaction |
| `getContractEvents` | Query contract events |
| `decodeTransactionCalldata` | Decode transaction input data |
| `getAccountProtocols` | Analyze protocol interactions |

Full documentation: [arbitrum-mcp-tools/index.md](arbitrum-mcp-tools/index.md)

If the MCP tool is not available in the user's environment, suggest the MCP Tools setup guide from the documentation.
