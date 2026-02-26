---
name: tronbox
description: Development framework and testing environment for TRON (TVM) and EVM-compatible chains — compile, migrate, test, and console.
metadata:
  author: Hairy
  version: "2026.1.1"
  source: Generated from https://github.com/tronprotocol/tronbox, scripts located at https://github.com/antfu/skills
---

> The skill is based on TronBox v4.5.0, generated at 2026-02-25.

TronBox is a Truffle-style framework for TRON: smart contract compilation, migrations, testing, and an interactive console. It supports both the native TRON Virtual Machine (TVM) and EVM-compatible chains (e.g. BTTC) via a separate config and the `--evm` flag. Migrations and tests use ethers v6 in EVM mode and TronWeb for TVM.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Configuration | tronbox.js / tronbox-evm-config.js, networks, paths, solc | [core-config](references/core-config.md) |
| Migrations & Deployer | Migration scripts, deploy/link/then API, context (artifacts, tronWeb, ethers) | [core-migrations](references/core-migrations.md) |
| Compile | Compiling contracts, --all / --evm, build output | [core-compile](references/core-compile.md) |
| Testing | tronbox test, test discovery, artifacts in tests | [core-testing](references/core-testing.md) |
| Console | Interactive REPL with contract abstractions | [core-console](references/core-console.md) |
| CLI | All commands and options | [core-cli](references/core-cli.md) |
| Artifacts & Resolver | Build output shape, resolver order, artifacts.require / resolve | [core-artifacts-resolver](references/core-artifacts-resolver.md) |
| Contract abstraction | new(), at(), deployed(), call(), link, defaults | [core-contract-abstraction](references/core-contract-abstraction.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| EVM mode | EVM chains, tronbox-evm-config.js, --evm, ethers | [features-evm](references/features-evm.md) |
| Init & Unbox | tronbox init (sample/MetaCoin), unbox templates | [features-init-unbox](references/features-init-unbox.md) |
| Flatten | Flatten contracts and dependencies to single file (verification/auditing) | [features-flatten](references/features-flatten.md) |
| Deploy | Alias for migrate; same options and behavior | [features-deploy](references/features-deploy.md) |
| TronWrap & provider | TronWeb/ethers context, waitForTransactionReceipt, TRE | [features-tronwrap](references/features-tronwrap.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Environment & networks | Environment.detect, default network, network_id/from, common errors | [best-practices-environment](references/best-practices-environment.md) |
| Errors & exit behavior | TaskError, config/compile/migrate errors, exit codes | [best-practices-errors](references/best-practices-errors.md) |
