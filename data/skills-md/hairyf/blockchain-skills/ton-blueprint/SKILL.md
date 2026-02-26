---
name: ton-blueprint
description: TON Blueprint development environment — project layout, build/test/run, NetworkProvider, config, scripts, wrappers, and deploy/testing practices.
metadata:
  author: Hairy
  version: "2026.2.25"
  source: Generated from https://github.com/ton-org/blueprint, scripts located at https://github.com/antfu/skills
---

> Skill is based on Blueprint (ton-org/blueprint), generated at 2026-02-25.

Blueprint is a development environment for the TON blockchain: create projects with `npm create ton@latest`, then build (Tolk/FunC/Tact), test (Sandbox), and run scripts (deploy via TonConnect, deeplink, or mnemonic). Projects use a fixed layout: `contracts/`, `wrappers/`, `compilables/`, `tests/`, `scripts/`, `build/`.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Project structure | Directory layout, contracts/wrappers/compilables/tests/scripts/build | [core-project-structure](references/core-project-structure.md) |
| CLI commands | build, test, run, create, rename, help, pack, snapshot, verify, set, convert | [core-commands](references/core-commands.md) |
| NetworkProvider | sender, open, waitForDeploy, waitForLastTransaction, api, config | [core-network-provider](references/core-network-provider.md) |
| Config | blueprint.config.ts, plugins, network, requestTimeout, recursiveWrappers, manifestUrl | [core-config](references/core-config.md) |
| UIProvider | write, prompt, input, choose, setActionPrompt, inputAddress for scripts | [core-ui-provider](references/core-ui-provider.md) |
| Networks and explorers | Network, Explorer, CustomNetwork, NetworkVersion for run/verify/config | [core-networks-explorers](references/core-networks-explorers.md) |

## Features

### Scripts and compilation

| Topic | Description | Reference |
|-------|-------------|-----------|
| Scripts | run(provider, args), deploy pattern, blueprint run | [features-scripts](references/features-scripts.md) |
| Compilation | compile(), CompilerConfig, compilables, build output, hooks | [features-compilation](references/features-compilation.md) |
| Build API | buildOne, buildAll, buildAllTact, artifact output | [features-build-api](references/features-build-api.md) |
| Wrappers | Contract, createFromConfig, createFromAddress, sendDeploy | [features-wrappers](references/features-wrappers.md) |
| Plugins | Plugin, PluginRunner, custom CLI commands | [features-plugins](references/features-plugins.md) |
| Verify | Verify deployed contract on verifier.ton.org, flags, compiler version | [features-verify](references/features-verify.md) |
| Pack | Publish-ready wrapper package, package.ts, dist, npm publish | [features-pack](references/features-pack.md) |
| Create and rename | Create contract from template, rename across wrappers/scripts/tests | [features-create-rename](references/features-create-rename.md) |

### Best practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Deploy | Deploy flow, TonConnect/deeplink/mnemonic, env vars, verify | [best-practices-deploy](references/best-practices-deploy.md) |
| Testing | Sandbox tests, compile(), coverage, gas report/snapshot | [best-practices-testing](references/best-practices-testing.md) |
