---
name: contract-addresses
description: Verified contract addresses for major EVM protocols across Ethereum, Arbitrum, Optimism, Base, and Polygon. Covers tokens, DEXes, lending, bridges, and infrastructure. Use as a reference when building integrations — every address is checksummed and should be verified onchain before use in production.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: multichain
  category: Infrastructure
tags:
  - addresses
  - contracts
  - tokens
  - reference
---

# Contract Addresses

Canonical contract addresses for major EVM protocols. Reference skill for agents building integrations across Ethereum, Arbitrum, Optimism, Base, and Polygon.

> **Last verified: February 2026** — All addresses verified onchain via `cast code`. Always re-verify before mainnet use.

## What You Probably Got Wrong

- **Addresses differ across chains** — USDC on Arbitrum is NOT the same address as USDC on Ethereum. Never assume cross-chain address parity except for contracts deployed via CREATE2 at deterministic addresses.
- **Bridged vs. native tokens** — Many chains have both a bridged USDC (USDC.e) and a native USDC. Using the wrong one causes failed swaps and lost funds. This reference lists the canonical native version where available.
- **Checksums matter** — EIP-55 mixed-case checksums prevent sending to mistyped addresses. Always use checksummed addresses.
- **Proxy vs. implementation** — Most protocol addresses listed here are proxies. The implementation behind them can change via governance. Verify the proxy's current implementation if you need the ABI.
- **Uniswap has multiple routers** — SwapRouter (V3-only), SwapRouter02 (V2+V3), and Universal Router (V2+V3+NFTs) are different contracts. Most integrations should use Universal Router.

## Stablecoins

### USDC (Circle)

| Chain | Address | Notes |
|-------|---------|-------|
| Ethereum | `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48` | Native USDC, 6 decimals |
| Arbitrum | `0xaf88d065e77c8cC2239327C5EDb3A432268e5831` | Native USDC (not USDC.e) |
| Optimism | `0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85` | Native USDC (not USDC.e) |
| Base | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | Native USDC |
| Polygon | `0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359` | Native USDC (not USDC.e) |

### USDC.e (Bridged USDC)

| Chain | Address | Notes |
|-------|---------|-------|
| Arbitrum | `0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8` | Legacy bridged, being deprecated |
| Optimism | `0x7F5c764cBc14f9669B88837ca1490cCa17c31607` | Legacy bridged |
| Polygon | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` | Legacy bridged |

### USDT (Tether)

| Chain | Address | Notes |
|-------|---------|-------|
| Ethereum | `0xdAC17F958D2ee523a2206206994597C13D831ec7` | 6 decimals, no return value on transfer |
| Arbitrum | `0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9` | Bridged USDT |
| Optimism | `0x94b008aA00579c1307B0EF2c499aD98a8ce58e58` | Bridged USDT |
| Polygon | `0xc2132D05D31c914a87C6611C10748AEb04B58e8F` | Bridged USDT |

### DAI (MakerDAO)

| Chain | Address | Notes |
|-------|---------|-------|
| Ethereum | `0x6B175474E89094C44Da98b954EedeAC495271d0F` | 18 decimals |
| Arbitrum | `0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1` | Bridged DAI |
| Optimism | `0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1` | Same address as Arbitrum (CREATE2) |
| Polygon | `0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063` | Bridged DAI |

## Wrapped Tokens

### WETH (Wrapped Ether)

| Chain | Address | Notes |
|-------|---------|-------|
| Ethereum | `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` | Canonical WETH9 |
| Arbitrum | `0x82aF49447D8a07e3bd95BD0d56f35241523fBab1` | WETH on Arbitrum |
| Optimism | `0x4200000000000000000000000000000000000006` | Predeploy address |
| Base | `0x4200000000000000000000000000000000000006` | Predeploy address (same as OP) |
| Polygon | `0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619` | Bridged WETH |

### wstETH (Lido Wrapped Staked ETH)

| Chain | Address | Notes |
|-------|---------|-------|
| Ethereum | `0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0` | Canonical wstETH |
| Arbitrum | `0x5979D7b546E38E9aB8E801a884a0710832C3fD7b` | Bridged wstETH |
| Optimism | `0x1F32b1c2345538c0c6f582fCB022739c4A194Ebb` | Bridged wstETH |
| Base | `0xc1CBa3fCea344f92D9239c08C0568f6F2F0ee452` | Bridged wstETH |
| Polygon | `0x03b54A6e9a984069379fae1a4fC4dBAE93B3bCCD` | Bridged wstETH |

## DEX Routers

### Uniswap

| Contract | Ethereum | Arbitrum | Optimism | Base | Polygon |
|----------|----------|----------|----------|------|---------|
| Universal Router | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` | `0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD` |
| SwapRouter02 | `0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45` | `0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45` | `0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45` | `0x2626664c2603336E57B271c5C0b26F421741e481` | `0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45` |
| V3 Factory | `0x1F98431c8aD98523631AE4a59f267346ea31F984` | `0x1F98431c8aD98523631AE4a59f267346ea31F984` | `0x1F98431c8aD98523631AE4a59f267346ea31F984` | `0x33128a8fC17869897dcE68Ed026d694621f6FDfD` | `0x1F98431c8aD98523631AE4a59f267346ea31F984` |
| V3 NonfungiblePositionManager | `0xC36442b4a4522E871399CD717aBDD847Ab11FE88` | `0xC36442b4a4522E871399CD717aBDD847Ab11FE88` | `0xC36442b4a4522E871399CD717aBDD847Ab11FE88` | `0x03a520b32C04BF3bEEf7BEb72E919cf822Ed34f1` | `0xC36442b4a4522E871399CD717aBDD847Ab11FE88` |

### Uniswap V2 (Ethereum only)

| Contract | Address |
|----------|---------|
| V2 Router | `0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D` |
| V2 Factory | `0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f` |

## Lending

### Aave V3

| Contract | Ethereum | Arbitrum | Optimism | Base | Polygon |
|----------|----------|----------|----------|------|---------|
| Pool | `0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2` | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` | `0xA238Dd80C259a72e81d7e4664a9801593F98d1c5` | `0x794a61358D6845594F94dc1DB02A252b5b4814aD` |
| PoolAddressesProvider | `0x2f39d218133AFaB8F2B819B1066c7E434Ad94E9e` | `0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb` | `0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb` | `0xe20fCBdBfFC4Dd138cE8b2E6FBb6CB49777ad64D` | `0xa97684ead0e402dC232d5A977953DF7ECBaB3CDb` |

### Compound V3 (Comet)

| Market | Ethereum | Arbitrum | Base | Polygon |
|--------|----------|----------|------|---------|
| USDC Comet | `0xc3d688B66703497DAA19211EEdff47f25384cdc3` | `0xA5EDBDD9646f8dFF606d7448e414884C7d905dCA` | `0xb125E6687d4313864e53df431d5425969c15Eb2F` | `0xF25212E676D1F7F89Cd72fFEe66158f541246445` |
| WETH Comet | `0xA17581A9E3356d9A858b789D68B4d866e593aE94` | `0x6f7D514bbD4aFf3BcD1140B7344b32f063dEe486` | `0x46e6b214b524310239732D51387075E0e70970bf` | -- |

## Oracles

### Chainlink Price Feeds

| Feed | Ethereum | Arbitrum | Optimism | Base |
|------|----------|----------|----------|------|
| ETH/USD | `0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419` | `0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612` | `0x13e3Ee699D1909E989722E753853AE30b17e08c5` | `0x71041dddad3595F9CEd3DcCFBe3D1F4b0a16Bb70` |
| BTC/USD | `0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c` | `0x6ce185860a4963106506C203335A2910413708e9` | `0xD702DD976Fb76Fffc2D3963D037dfDae5b04E593` | -- |
| USDC/USD | `0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6` | `0x50834F3163758fcC1Df9973b6e91f0F0F0434aD3` | `0x16a9FA2FDa030272Ce99B29CF780dFA30361E0f3` | `0x7e860098F58bBFC8648a4311b374B1D669a2bc6B` |
| LINK/USD | `0x2c1d072e956AFFC0D435Cb7AC38EF18d24d9127c` | `0x86E53CF1B870786351Da77A57575e79CB55812CB` | `0xCc232dcFAAE6354cE191Bd574108c1aD03f86229` | `0x17CAb8FE31cA45e4684E33E3D258F20E88B8fD8B` |

### Chainlink Infrastructure

| Contract | Ethereum | Arbitrum | Base |
|----------|----------|----------|------|
| Feed Registry | `0x47Fb2585D2C56Fe188D0E6ec628a38b74fCeeeDf` | -- | -- |
| VRF Coordinator V2.5 | `0xD7f86b4b8Cae7D942340FF628F82735b7a20893a` | `0x3C0Ca683b403E37668AE3DC4FB62F4B29B6f7a3e` | `0xd5D517aBE5cF79B7e95eC98dB0f0277788aFF634` |

## Infrastructure

### Multicall

| Contract | Address | Chains |
|----------|---------|--------|
| Multicall3 | `0xcA11bde05977b3631167028862bE2a173976CA11` | All major EVM chains (deterministic CREATE2 deployment) |

### CREATE2 Deployers

| Contract | Address | Chains |
|----------|---------|--------|
| Deterministic Deployment Proxy | `0x4e59b44847b379578588920cA78FbF26c0B4956C` | All major EVM chains |
| Create2Deployer (OpenZeppelin) | `0x13b0D85CcB8bf860b6b79AF3029fCA081AE9beF2` | All major EVM chains |

### ENS (Ethereum Only)

| Contract | Address |
|----------|---------|
| ENS Registry | `0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e` |
| Public Resolver | `0x231b0Ee14048e9dCcD1d247744d114a4EB5E8E63` |
| Reverse Registrar | `0xa58E81fe9b61B5c3fE2AFD33CF304c454AbFc7Cb` |
| ETH Registrar Controller | `0x253553366Da8546fC250F225fe3d25d0C782303b` |

### Safe (Gnosis Safe)

| Contract | Address | Chains |
|----------|---------|--------|
| Safe Singleton (1.4.1) | `0x41675C099F32341bf84BFc5382aF534df5C7461a` | All major EVM chains |
| Safe Proxy Factory (1.4.1) | `0x4e1DCf7AD4e460CfD30791CCC4F9c8a4f820ec67` | All major EVM chains |
| MultiSend (1.4.1) | `0x38869bf66a61cF6bDB996A6aE40D5853Fd43B526` | All major EVM chains |
| Safe Singleton (1.3.0) | `0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552` | All major EVM chains |
| Safe Proxy Factory (1.3.0) | `0xa6B71E26C5e0845f74c812102Ca7114b6a896AB2` | All major EVM chains |

### Permit2 (Uniswap)

| Contract | Address | Chains |
|----------|---------|--------|
| Permit2 | `0x000000000022D473030F116dDEE9F6B43aC78BA3` | All major EVM chains (deterministic CREATE2) |

## Bridges

### Arbitrum Native Bridge

| Contract | Address | Chain |
|----------|---------|-------|
| L1 Gateway Router | `0x72Ce9c846789fdB6fC1f34aC4AD25Dd9ef7031ef` | Ethereum |
| L1 ERC20 Gateway | `0xa3A7B6F88361F48403514059F1F16C8E78d60EeC` | Ethereum |
| L2 Gateway Router | `0x5288c571Fd7aD117beA99bF60FE0846C4E84F933` | Arbitrum |
| Inbox | `0x4Dbd4fc535Ac27206064B68FfCf827b0A60BAB3f` | Ethereum |

### Optimism Native Bridge

| Contract | Address | Chain |
|----------|---------|-------|
| L1StandardBridge (Proxy) | `0x99C9fc46f92E8a1c0deC1b1747d010903E884bE1` | Ethereum |
| L2StandardBridge | `0x4200000000000000000000000000000000000010` | Optimism (predeploy) |
| L1CrossDomainMessenger (Proxy) | `0x25ace71c97B33Cc4729CF772ae268934F7ab5fA1` | Ethereum |
| L2CrossDomainMessenger | `0x4200000000000000000000000000000000000007` | Optimism (predeploy) |
| OptimismPortal (Proxy) | `0xbEb5Fc579115071764c7423A4f12eDde41f106Ed` | Ethereum |

### Base Native Bridge

| Contract | Address | Chain |
|----------|---------|-------|
| L1StandardBridge (Proxy) | `0x3154Cf16ccdb4C6d922629664174b904d80F2C35` | Ethereum |
| L2StandardBridge | `0x4200000000000000000000000000000000000010` | Base (predeploy) |
| L1CrossDomainMessenger (Proxy) | `0x866E82a600A1414e583f7F13623F1aC5d58b0Afa` | Ethereum |
| L2CrossDomainMessenger | `0x4200000000000000000000000000000000000007` | Base (predeploy) |
| OptimismPortal (Proxy) | `0x49048044D57e1C92A77f79988d21Fa8fAF36f97B` | Ethereum |

## Governance

### Major Protocol Governance

| Protocol | Contract | Address | Chain |
|----------|----------|---------|-------|
| Uniswap | Governor Bravo | `0x408ED6354d4973f66138C91495F2f2FCbd8724C3` | Ethereum |
| Uniswap | Timelock | `0x1a9C8182C09F50C8318d769245beA52c32BE35BC` | Ethereum |
| Compound | Governor Bravo | `0xc0Da02939E1441F497fd74F78cE7Decb17B66529` | Ethereum |
| Compound | Timelock | `0x6d903f6003cca6255D85CcA4D3B5E5146dC33925` | Ethereum |
| Aave | Governance V3 | `0x9AEE0B04504CeF83A65AC3f0e838D0593BCb2BC7` | Ethereum |

### Governance Tokens

| Token | Address | Chain |
|-------|---------|-------|
| UNI | `0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984` | Ethereum |
| COMP | `0xc00e94Cb662C3520282E6f5717214004A7f26888` | Ethereum |
| AAVE | `0x7Fc66500c84A76Ad7e9c93437bFc5Ac33E2DDaE9` | Ethereum |
| LDO | `0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32` | Ethereum |
| LINK | `0x514910771AF9Ca656af840dff83E8264EcF986CA` | Ethereum |
| MKR | `0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2` | Ethereum |
| CRV | `0xD533a949740bb3306d119CC777fa900bA034cd52` | Ethereum |

## OP Stack Predeploys

Shared across Optimism, Base, and all OP Stack chains at the same addresses.

| Contract | Address |
|----------|---------|
| L2CrossDomainMessenger | `0x4200000000000000000000000000000000000007` |
| L2StandardBridge | `0x4200000000000000000000000000000000000010` |
| L2ToL1MessagePasser | `0x4200000000000000000000000000000000000016` |
| L1Block | `0x4200000000000000000000000000000000000015` |
| GasPriceOracle | `0x420000000000000000000000000000000000000F` |
| WETH (predeploy) | `0x4200000000000000000000000000000000000006` |

## How to Verify

Always verify addresses onchain before using them in production. Addresses in this reference may become outdated if protocols upgrade their proxies.

### Using cast (Foundry)

Check if code exists at an address:

```bash
cast code 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 --rpc-url $ETH_RPC_URL
```

A non-empty response confirms a contract exists. `0x` means no contract (EOA or empty).

Verify a token's identity:

```bash
cast call 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 "symbol()(string)" --rpc-url $ETH_RPC_URL
cast call 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 "decimals()(uint8)" --rpc-url $ETH_RPC_URL
```

Check a proxy's implementation:

```bash
# EIP-1967 implementation slot
cast storage 0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48 \
  0x360894a13ba1a3210667c828492db98dca3e2076cc3735a920a3ca505d382bbc \
  --rpc-url $ETH_RPC_URL
```

### Using Etherscan API

```bash
# Verify contract is verified on Etherscan
curl "https://api.etherscan.io/api?module=contract&action=getabi&address=0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48&apikey=$ETHERSCAN_API_KEY"
```

Chain-specific explorers:
- Ethereum: `api.etherscan.io`
- Arbitrum: `api.arbiscan.io`
- Optimism: `api-optimistic.etherscan.io`
- Base: `api.basescan.org`
- Polygon: `api.polygonscan.com`

### Checksum Verification

Verify an address is correctly checksummed:

```bash
cast to-check-sum-address 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48
```

## Important Caveats

- **Proxy upgrades** -- Protocol governance can upgrade proxy implementations. The proxy address stays the same, but behavior may change. Monitor governance proposals for protocols you depend on.
- **Chain-specific behavior** -- Same protocol may behave differently across chains. Aave V3 on Ethereum has different parameters (LTV, liquidation thresholds) than on Arbitrum.
- **Deprecated contracts** -- USDC.e (bridged) is being phased out in favor of native USDC on L2s. Old router addresses may still work but lack new features.
- **Token decimals** -- USDC/USDT use 6 decimals. DAI/WETH use 18. Never assume 18 decimals.
- **USDT non-standard** -- USDT's `transfer()` and `approve()` do not return a boolean. Use OpenZeppelin's `SafeERC20` or viem's built-in handling.

## References

- [Circle USDC Addresses](https://developers.circle.com/stablecoins/docs/usdc-on-main-networks)
- [Uniswap Deployments](https://docs.uniswap.org/contracts/v3/reference/deployments)
- [Aave V3 Deployed Contracts](https://docs.aave.com/developers/deployed-contracts/v3-mainnet)
- [Compound V3 Deployments](https://docs.compound.finance/protocol/markets/)
- [Chainlink Feed Registry](https://docs.chain.link/data-feeds/feed-registry)
- [Safe Deployments](https://github.com/safe-global/safe-deployments)
- [OP Stack Predeploys](https://docs.optimism.io/chain/addresses)
- [Arbitrum Bridge Contracts](https://docs.arbitrum.io/build-decentralized-apps/reference/useful-addresses)
- [ENS Deployments](https://docs.ens.domains/learn/deployments)
- [Multicall3](https://www.multicall3.com/)
