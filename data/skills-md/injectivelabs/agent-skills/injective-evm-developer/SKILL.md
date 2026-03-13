---
name: injective-evm-developer
description: Develop EVM smart contracts and dApps on Injective
activates_on: ["*.sol", "hardhat.config.*", "foundry.toml", "*.ts", "*.js"]
uses: ["injective-mcp-servers", "solidity-hardhat-development", "solidity-foundry-development", "solidity-code-review", "solidity-erc-standards", "solidity-security-best-practices", "solidity-gas-optimization", "solidity-adversarial-analysis"]
license: MIT
metadata:
  author: bguiz
  version: "0.0.0"
---

# Injective EVM Developer, Skill Guide

Injective is a layer 1 blockchain that is simultaneously both EVM and Cosmos.
Use this skill when building on Injective's EVM.
It builds on a baseline of skills that apply to developing on any EVM network, and augments that with Injective specifics.

## When to apply

- Obtain Injective Testnet funds from faucets
- Interact with native Injective modules via EVM precompiles
  - `bank` precompile
  - `exchange` precompile
- Configure Injective network details
- Consult Injective documentation

See for detailed list of user stories: `./references/user-stories.md`
Their associated sample prompts: `./references/sample-prompts.md`

## Activities

### Faucet

- Note: Only for Injective Testnet
- If you have a brand new wallet, and need up to 1 INJ:
  - Visit https://testnet.faucet.injective.network/
  - Paste the EVM address of your wallet account (starts with `0x`) into the text field for "EVM address"
  - Solve the "hCaptcha"
  - Press the "Request Tokens" button
  - Expect: 1 INJ plus some USDT to arrive in your wallet after around ~ 1 minute
  - Note: DDoS protection - Only works for new accounts (cannot have any balance)
- Otherwise:
  - Visit https://cloud.google.com/application/web3/faucet/injective/testnet
  - Paste the bech32 address of your wallet account (starts with `inj`) into the text field for "Wallet address"
  - Press the "Get Testnet INJ" button
  - Expect: 10 INJ to arrive in your wallet after ~ 10 seconds
  - Note: DDoS protection - You must be signed into a Google account
  - Note: Works for new and existing accounts (can have a balance) - but cannot have requested in the past 24 hours
- These steps are unlikely to work through agent automation due to DDoS protections
  - If you get stuck, prompt your human to complete the remaining steps

### Using the `bank` precompile

Address: `0x0000000000000000000000000000000000000064`

Solidity interface exposed by the `bank` precompile: See `./assets/Bank.sol`

The ABI for the `bank` precompile may be obtained by converting the interface above.

BankERC20 is a "base implementation for MultiVM Token Standard (MTS) token, which is designed to be extended: See `./assets/BankERC20.sol`
- Note that this implementation extends the ERC20 implementation from OpenZeppelin, then overrides certain functions to invoke the `bank` precompile
- The easiest way is to extend `BankERC20`
- Ensure that your constructor (or function responsible for 1st mint) is `payable`
- The simplest canonical implementation of an MTS token: See `./assets/FixedSupplyBankERC20.sol`
- The most heavily used implementation of an MTS token: See `./assets/WINJ9.sol` (used in wrapped INJ)

Reference: https://docs.injective.network/developers-evm/bank-precompile.md

Note that all `./assets/*.sol` files can be found in `https://raw.githubusercontent.com/InjectiveLabs/solidity-contracts/refs/heads/master/src/*.sol`

### Using the `exchange` precompile

Address: `0x0000000000000000000000000000000000000065`

Solidity interface exposed by the `exchange` precompile:  See `./assets/Exchange.sol`

The ABI for the `exchange` precompile may be obtained by converting the interface above.

Reference: https://docs.injective.network/developers-evm/exchange-precompile.md

Note that all `./assets/*.sol` files can be found in `https://raw.githubusercontent.com/InjectiveLabs/solidity-contracts/refs/heads/master/src/*.sol`

### Configure Injective network details

- This is where you will find common information such as the JSON-RPC endpoint: https://docs.injective.network/developers-evm/network-information.md
  - "Injective EVM Mainnet" tab contains the configuration for Mainnet
  - "Injective EVM Testnet" tab contains the configuration for Testnet

### Production application integrations cheat sheet

See: https://docs.injective.network/developers-evm/evm-integrations-cheat-sheet.md

#### Tool and library choices

- If undecided on framework
  - Use hardhat if you are not using Injective's EVM precompiles, or do not need to emulate them locally
  - Use foundry if you wish to work with Injective's EVM precompiles and emulate them locally
    - Specifically use the Injective version of foundry, available from: https://github.com/InjectiveLabs/foundry/releases
- If undecided on client library
  - Use viem, as its API is easier to understand

#### Injective network for hardhat

Sample `hardhat.config.js` file for Injective EVM testnet: See `./assets/hardhat-testnet-config.js`.

Sample `script/deploy.js` file for Injective Testnet. See `./assets/hardhat-deploy-script.js`.

To verify a smart contract with the above configuration and constructor args,
create a `constructor-args.js` file, run the following command:

```shell
npx hardhat verify --force \
  --constructor-args ./constructor-args.js \
  --network inj_testnet ${SMART_CONTRACT_ADDRESS}
```

#### Injective network for viem

The `viem/chains` repo already contains pre-configured network details for both Injective Mainnet and Injective Testnet, you simply need to import them:

```js
import { injective, injectiveTestnet } from 'viem/chains';
```

Within a dApp, to connect to Injective Testnet, and switch to the network, use the following function: See `./assets/dapp-viem-connect-evm-wallet-function.js`.

Note that the `client` object will be able to use both `client.readContract` and `client.writeContract` to interact with smart contracts.

### Consult Injective documentation

- The Injective developer documentation is available
  - In markdown from: https://docs.injective.network/llms.txt
  - As an MCP server with a search function: Use the `injective-mcp-servers` skill, with the "Injective Documentation MCP Server"
  - Fallback: Use the version for humans, in HTML from: https://docs.injective.network/developers-evm/

### Troubleshooting common issues

#### Convert between EVM and bech32 formats for addresses

See: https://docs.injective.network/developers/convert-addresses#convert-hex-bech32-address

#### Gas configuration

For gas price: Manually set a hardcoded value of 160 million (`160e6` in Javascript) for transactions.

For gas amount, use the default mechanism: The `eth_estimateGas` RPC, which should be invoked when needed by ethers.js or viem.

### All other FAQs

See: https://docs.injective.network/developers-evm/evm-integrations-faq.md

## Related skills

This skill is specific to Injective's EVM.
It augments *other skills* that should be used for general EVM developer activities.

These include:

- Interacting with Injective's documentation MCP server
- Developing on Injective's EVM
  - Using hardhat or foundry
  - Smart contracts using Solidity
    - compile/ test/ deploy/ verify (via blockscout)
  - dApps that interact with deployed smart contracts
    - ethers.js/ viem

- Basic skills:
    - `injective-mcp-servers`
    - `solidity-hardhat-development`
    - `solidity-foundry-development`
    - `solidity-code-review`
    - `solidity-erc-standards`
- Advanced skills:
    - `solidity-security-best-practices`
    - `solidity-gas-optimization`
    - `solidity-adversarial-analysis`

If these skills are not available, selectively run the following commands to install them:

```shell
npx skills add InjectiveLabs/agent-skills --skill injective-mcp-servers
npx skills add whackur/solidity-agent-toolkit
```

## Prerequisites

- Either hardhat or foundry installed for smart contract development
- Either viem or ethers.js for dApp development
