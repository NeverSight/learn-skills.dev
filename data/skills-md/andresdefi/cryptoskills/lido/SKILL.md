---
name: lido
description: Lido liquid staking protocol — stake ETH to receive stETH, wrap to wstETH for DeFi composability, manage withdrawal queue requests, read share rates and protocol state. Covers rebasing token pitfalls, 1-2 wei transfer rounding, wstETH/stETH conversion, and integration patterns for lending protocols and vaults.
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: ethereum
  category: DeFi
tags:
  - lido
  - staking
  - liquid-staking
  - steth
  - wsteth
---

# Lido

Lido is the largest liquid staking protocol on Ethereum. Users deposit ETH and receive stETH, a rebasing token whose balance increases daily as staking rewards accrue. wstETH is the non-rebasing wrapper used in DeFi. The protocol manages a validator set, an oracle-reported share rate, and an on-chain withdrawal queue.

## What You Probably Got Wrong

- **stETH is a rebasing token** — Your stETH balance changes every day when the oracle reports. If you store a balance in a variable and check it later, it will differ. This breaks naive accounting in smart contracts. Use wstETH or track shares, not balances.
- **wstETH is NOT stETH** — wstETH is a non-rebasing ERC-20 wrapper around stETH shares. 1 wstETH != 1 stETH. The exchange rate drifts upward over time as rewards accumulate. Always convert via `stETH.getPooledEthByShares()` or `wstETH.stEthPerToken()`.
- **stETH/ETH is NOT 1:1** — There is a market rate on secondary markets (Curve, Uniswap) that can deviate from the protocol's internal rate, especially during high withdrawal demand or market stress. The 2022 depeg hit ~0.93.
- **stETH transfers lose 1-2 wei** — Due to shares-to-balance rounding, transferring your full `balanceOf` may leave 1-2 wei behind. The recipient may receive 1 wei less than `amount`. This is by design, not a bug. Never assert exact equality on stETH transfers.
- **Withdrawals are NOT instant** — The withdrawal queue processes requests in order. Finalization depends on validator exits and oracle reports. Typical wait: 1-5 days, but can be longer during high demand. You must request, wait for finalization, then claim in a separate tx.
- **Shares are the canonical unit** — stETH balances are derived from shares. `balanceOf(account) = shares[account] * totalPooledEther / totalShares`. All internal accounting uses shares. When integrating, think in shares.
- **`submit()` requires the referral address parameter** — The staking function is `submit(address _referral)` payable, not just a payable fallback. Pass `address(0)` if you have no referral.

## Quick Start

### Stake ETH via Lido (TypeScript)

```typescript
import { createPublicClient, createWalletClient, http, parseAbi, parseEther } from "viem";
import { mainnet } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

const LIDO = "0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84" as const;

const LIDO_ABI = parseAbi([
  "function submit(address _referral) external payable returns (uint256)",
  "function balanceOf(address _account) external view returns (uint256)",
  "function sharesOf(address _account) external view returns (uint256)",
  "function getPooledEthByShares(uint256 _sharesAmount) external view returns (uint256)",
  "function getSharesByPooledEth(uint256 _ethAmount) external view returns (uint256)",
  "function getTotalPooledEther() external view returns (uint256)",
  "function getTotalShares() external view returns (uint256)",
]);

const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);

const publicClient = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const walletClient = createWalletClient({
  account,
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

async function stakeEth(amountEth: string) {
  const { request } = await publicClient.simulateContract({
    address: LIDO,
    abi: LIDO_ABI,
    functionName: "submit",
    args: ["0x0000000000000000000000000000000000000000"],
    value: parseEther(amountEth),
    account,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("Stake tx reverted");

  return hash;
}
```

## Staking

### Submit ETH, Receive stETH (Solidity)

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface ILido {
    function submit(address _referral) external payable returns (uint256 sharesAmount);
    function balanceOf(address _account) external view returns (uint256);
    function sharesOf(address _account) external view returns (uint256);
    function getPooledEthByShares(uint256 _sharesAmount) external view returns (uint256);
    function getSharesByPooledEth(uint256 _ethAmount) external view returns (uint256);
    function transferShares(address _recipient, uint256 _sharesAmount) external returns (uint256);
}

contract LidoStaker {
    ILido public constant LIDO = ILido(0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84);

    event Staked(address indexed user, uint256 ethAmount, uint256 sharesReceived);

    /// @notice Stake ETH via Lido. Returns shares minted, not stETH amount.
    function stake() external payable returns (uint256 shares) {
        if (msg.value == 0) revert ZeroDeposit();

        shares = LIDO.submit{value: msg.value}(address(0));
        emit Staked(msg.sender, msg.value, shares);
    }

    /// @notice Transfer stETH using shares to avoid rounding issues
    /// @dev transferShares is exact — no 1-2 wei rounding loss
    function transferSharesTo(address recipient, uint256 sharesAmount) external {
        LIDO.transferShares(recipient, sharesAmount);
    }

    error ZeroDeposit();
}
```

### Wrap stETH to wstETH

wstETH holds a fixed number of stETH shares. Its balance does not rebase. Use wstETH in DeFi protocols, vaults, and any contract that stores balances.

```typescript
const WSTETH = "0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0" as const;

const WSTETH_ABI = parseAbi([
  "function wrap(uint256 _stETHAmount) external returns (uint256)",
  "function unwrap(uint256 _wstETHAmount) external returns (uint256)",
  "function getStETHByWstETH(uint256 _wstETHAmount) external view returns (uint256)",
  "function getWstETHByStETH(uint256 _stETHAmount) external view returns (uint256)",
  "function stEthPerToken() external view returns (uint256)",
  "function tokensPerStEth() external view returns (uint256)",
]);

async function wrapSteth(stEthAmount: bigint) {
  // Approve stETH spending by wstETH contract first
  const approveHash = await walletClient.writeContract({
    address: LIDO,
    abi: parseAbi(["function approve(address spender, uint256 amount) external returns (bool)"]),
    functionName: "approve",
    args: [WSTETH, stEthAmount],
  });
  await publicClient.waitForTransactionReceipt({ hash: approveHash });

  const { request } = await publicClient.simulateContract({
    address: WSTETH,
    abi: WSTETH_ABI,
    functionName: "wrap",
    args: [stEthAmount],
    account,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("Wrap tx reverted");

  return hash;
}

async function unwrapWsteth(wstEthAmount: bigint) {
  const { request } = await publicClient.simulateContract({
    address: WSTETH,
    abi: WSTETH_ABI,
    functionName: "unwrap",
    args: [wstEthAmount],
    account,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("Unwrap tx reverted");

  return hash;
}
```

### Wrap/Unwrap in Solidity

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IWstETH {
    function wrap(uint256 _stETHAmount) external returns (uint256);
    function unwrap(uint256 _wstETHAmount) external returns (uint256);
    function getStETHByWstETH(uint256 _wstETHAmount) external view returns (uint256);
    function getWstETHByStETH(uint256 _stETHAmount) external view returns (uint256);
}

contract WstETHWrapper {
    IERC20 public constant STETH = IERC20(0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84);
    IWstETH public constant WSTETH = IWstETH(0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0);

    /// @notice Wrap stETH to wstETH. Caller must approve this contract for stETH first.
    function wrapStETH(uint256 stETHAmount) external returns (uint256 wstETHReceived) {
        STETH.transferFrom(msg.sender, address(this), stETHAmount);
        // Rounding may cause actual transferred amount to differ by 1-2 wei
        uint256 actualBalance = STETH.balanceOf(address(this));
        STETH.approve(address(WSTETH), actualBalance);
        wstETHReceived = WSTETH.wrap(actualBalance);
        IERC20(address(WSTETH)).transfer(msg.sender, wstETHReceived);
    }

    error InsufficientBalance();
}
```

## Withdrawals

Lido v2 introduced an on-chain withdrawal queue. Withdrawals mint an NFT (ERC-721) representing the request. Once finalized by the oracle, the NFT can be claimed for ETH.

### Request Withdrawal (TypeScript)

```typescript
const WITHDRAWAL_QUEUE = "0x889edC2eDab5f40e902b864aD4d7AdE8E412F9B1" as const;

const WITHDRAWAL_ABI = parseAbi([
  "function requestWithdrawals(uint256[] _amounts, address _owner) external returns (uint256[])",
  "function requestWithdrawalsWstETH(uint256[] _amounts, address _owner) external returns (uint256[])",
  "function claimWithdrawals(uint256[] _requestIds, uint256[] _hints) external",
  "function getWithdrawalStatus(uint256[] _requestIds) external view returns ((uint256 amountOfStETH, uint256 amountOfShares, address owner, uint256 timestamp, bool isFinalized, bool isClaimed)[])",
  "function findCheckpointHints(uint256[] _requestIds, uint256 _firstIndex, uint256 _lastIndex) external view returns (uint256[])",
  "function getLastCheckpointIndex() external view returns (uint256)",
  "function getLastFinalizedRequestId() external view returns (uint256)",
]);

async function requestWithdrawal(stEthAmounts: bigint[]) {
  // Approve WithdrawalQueue to spend stETH
  const totalAmount = stEthAmounts.reduce((a, b) => a + b, 0n);
  const approveHash = await walletClient.writeContract({
    address: LIDO,
    abi: parseAbi(["function approve(address spender, uint256 amount) external returns (bool)"]),
    functionName: "approve",
    args: [WITHDRAWAL_QUEUE, totalAmount],
  });
  await publicClient.waitForTransactionReceipt({ hash: approveHash });

  const { request } = await publicClient.simulateContract({
    address: WITHDRAWAL_QUEUE,
    abi: WITHDRAWAL_ABI,
    functionName: "requestWithdrawals",
    args: [stEthAmounts, account.address],
    account,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("Withdrawal request reverted");

  return hash;
}
```

### Check Withdrawal Status and Claim

```typescript
async function getWithdrawalStatus(requestIds: bigint[]) {
  const statuses = await publicClient.readContract({
    address: WITHDRAWAL_QUEUE,
    abi: WITHDRAWAL_ABI,
    functionName: "getWithdrawalStatus",
    args: [requestIds],
  });

  return statuses.map((s, i) => ({
    requestId: requestIds[i],
    amountOfStETH: s.amountOfStETH,
    isFinalized: s.isFinalized,
    isClaimed: s.isClaimed,
    owner: s.owner,
  }));
}

async function claimWithdrawals(requestIds: bigint[]) {
  const lastCheckpointIndex = await publicClient.readContract({
    address: WITHDRAWAL_QUEUE,
    abi: WITHDRAWAL_ABI,
    functionName: "getLastCheckpointIndex",
  });

  const hints = await publicClient.readContract({
    address: WITHDRAWAL_QUEUE,
    abi: WITHDRAWAL_ABI,
    functionName: "findCheckpointHints",
    args: [requestIds, 1n, lastCheckpointIndex],
  });

  const { request } = await publicClient.simulateContract({
    address: WITHDRAWAL_QUEUE,
    abi: WITHDRAWAL_ABI,
    functionName: "claimWithdrawals",
    args: [requestIds, hints],
    account,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") throw new Error("Claim tx reverted");

  return hash;
}
```

## Reading Protocol State

### Share Rate, Total Pooled Ether, APR Estimation

```typescript
async function getProtocolState() {
  const [totalPooledEther, totalShares] = await Promise.all([
    publicClient.readContract({
      address: LIDO,
      abi: LIDO_ABI,
      functionName: "getTotalPooledEther",
    }),
    publicClient.readContract({
      address: LIDO,
      abi: LIDO_ABI,
      functionName: "getTotalShares",
    }),
  ]);

  // Share rate: how much ETH one share is worth (18 decimals)
  const shareRate = (totalPooledEther * 10n ** 18n) / totalShares;

  return { totalPooledEther, totalShares, shareRate };
}

async function convertWstethToSteth(wstEthAmount: bigint): Promise<bigint> {
  return publicClient.readContract({
    address: WSTETH,
    abi: WSTETH_ABI,
    functionName: "getStETHByWstETH",
    args: [wstEthAmount],
  });
}

async function convertStethToWsteth(stEthAmount: bigint): Promise<bigint> {
  return publicClient.readContract({
    address: WSTETH,
    abi: WSTETH_ABI,
    functionName: "getWstETHByStETH",
    args: [stEthAmount],
  });
}
```

### Reading Share Rate in Solidity

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface ILido {
    function getTotalPooledEther() external view returns (uint256);
    function getTotalShares() external view returns (uint256);
    function getPooledEthByShares(uint256 _sharesAmount) external view returns (uint256);
    function getSharesByPooledEth(uint256 _ethAmount) external view returns (uint256);
}

contract LidoReader {
    ILido public constant LIDO = ILido(0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84);

    /// @notice Returns ETH value of one stETH share, scaled to 18 decimals
    function getShareRate() external view returns (uint256) {
        return LIDO.getPooledEthByShares(1e18);
    }

    /// @notice Convert stETH amount to underlying shares
    function ethToShares(uint256 ethAmount) external view returns (uint256) {
        return LIDO.getSharesByPooledEth(ethAmount);
    }

    /// @notice Convert shares to stETH amount
    function sharesToEth(uint256 sharesAmount) external view returns (uint256) {
        return LIDO.getPooledEthByShares(sharesAmount);
    }
}
```

## DeFi Integration

### wstETH as Collateral (Aave/Compound Pattern)

When integrating wstETH in lending protocols or vaults, always use wstETH (not stETH) to avoid rebasing accounting complexity.

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IERC20} from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface IWstETH {
    function getStETHByWstETH(uint256 _wstETHAmount) external view returns (uint256);
}

/// @notice Simplified vault accepting wstETH as collateral
/// @dev Uses wstETH to avoid rebasing — balanceOf is stable between oracle reports
contract WstETHVault {
    IERC20 public constant WSTETH = IERC20(0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0);
    IWstETH public constant WSTETH_RATE = IWstETH(0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0);

    mapping(address => uint256) public deposits;

    event Deposited(address indexed user, uint256 wstETHAmount);
    event Withdrawn(address indexed user, uint256 wstETHAmount);

    function deposit(uint256 wstETHAmount) external {
        WSTETH.transferFrom(msg.sender, address(this), wstETHAmount);
        deposits[msg.sender] += wstETHAmount;
        emit Deposited(msg.sender, wstETHAmount);
    }

    function withdraw(uint256 wstETHAmount) external {
        if (deposits[msg.sender] < wstETHAmount) revert InsufficientDeposit();
        deposits[msg.sender] -= wstETHAmount;
        WSTETH.transfer(msg.sender, wstETHAmount);
        emit Withdrawn(msg.sender, wstETHAmount);
    }

    /// @notice Get the ETH value of a user's wstETH collateral
    function getCollateralValueInEth(address user) external view returns (uint256) {
        return WSTETH_RATE.getStETHByWstETH(deposits[user]);
    }

    error InsufficientDeposit();
}
```

### Oracle Considerations for wstETH Pricing

wstETH price = wstETH/stETH exchange rate * stETH/ETH rate * ETH/USD price. Protocols typically use:

1. **Chainlink wstETH/ETH feed** — Available on mainnet at `0x536218f9E9Eb48863970252233c8F271f554C2d0`. Combines the protocol rate with market data.
2. **On-chain rate from wstETH contract** — `wstETH.stEthPerToken()` gives the protocol exchange rate. This does NOT reflect secondary market deviations.
3. **Dual oracle approach** — Use the Chainlink feed as primary, fall back to the on-chain rate with bounds checking.

```typescript
const WSTETH_ETH_FEED = "0x536218f9E9Eb48863970252233c8F271f554C2d0" as const;

const AGGREGATOR_ABI = parseAbi([
  "function latestRoundData() external view returns (uint80 roundId, int256 answer, uint256 startedAt, uint256 updatedAt, uint80 answeredInRound)",
  "function decimals() external view returns (uint8)",
]);

async function getWstethEthPrice() {
  const [roundData, decimals] = await Promise.all([
    publicClient.readContract({
      address: WSTETH_ETH_FEED,
      abi: AGGREGATOR_ABI,
      functionName: "latestRoundData",
    }),
    publicClient.readContract({
      address: WSTETH_ETH_FEED,
      abi: AGGREGATOR_ABI,
      functionName: "decimals",
    }),
  ]);

  const [, answer, , updatedAt] = roundData;
  if (answer <= 0n) throw new Error("Invalid wstETH/ETH price");

  const now = BigInt(Math.floor(Date.now() / 1000));
  // wstETH/ETH feed heartbeat: 86400s
  if (now - updatedAt > 86400n) throw new Error("Stale wstETH/ETH price");

  return { answer, decimals };
}
```

## Contract Addresses

> **Last verified:** 2025-05-01

### Ethereum Mainnet

| Contract | Address |
|----------|---------|
| Lido (stETH proxy) | `0xae7ab96520DE3A18E5e111B5EaAb095312D7fE84` |
| wstETH | `0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0` |
| WithdrawalQueueERC721 | `0x889edC2eDab5f40e902b864aD4d7AdE8E412F9B1` |
| Lido Accounting Oracle | `0x852deD011285fe67063a08005c71a85690503Cee` |
| Lido Execution Layer Rewards Vault | `0x388C818CA8B9251b393131C08a736A67ccB19297` |

### wstETH on L2s

| Chain | wstETH Address |
|-------|----------------|
| Arbitrum | `0x5979D7b546E38E9Ab8F24815DCa0E57E830D4df6` |
| Optimism | `0x1F32b1c2345538c0c6f582fCB022739c4A194Ebb` |
| Base | `0xc1CBa3fCea344f92D9239c08C0568f6F2F0ee452` |
| Polygon | `0x03b54A6e9a984069379fae1a4fC4dBAE93B3bCCD` |

### Chainlink Price Feeds for stETH/wstETH

| Pair | Mainnet Address |
|------|----------------|
| wstETH/ETH | `0x536218f9E9Eb48863970252233c8F271f554C2d0` |
| stETH/ETH | `0x86392dC19c0b719886221c78AB11eb8Cf5c52812` |
| stETH/USD | `0xCfE54B5cD566aB89272946F602D76Ea879CAb4a8` |

## Error Handling

| Error / Symptom | Cause | Fix |
|-----------------|-------|-----|
| `STAKE_LIMIT` revert on `submit()` | Daily staking limit reached | Wait for next day or check `getCurrentStakeLimit()` before submitting |
| Transfer leaves 1-2 wei dust | Shares-to-balance rounding in rebasing math | Use `transferShares()` for exact share transfers; never assert exact stETH balance equality |
| `REQUEST_AMOUNT_TOO_SMALL` | Withdrawal amount below minimum (100 wei) | Ensure each withdrawal request is >= 100 wei of stETH |
| `REQUEST_AMOUNT_TOO_LARGE` | Single request exceeds max (1000 stETH) | Split large withdrawals into multiple requests of <= 1000 stETH each |
| Withdrawal claim reverts | Request not yet finalized, or already claimed | Check `getWithdrawalStatus()` — wait for `isFinalized == true`, verify `isClaimed == false` |
| `findCheckpointHints` returns empty | Invalid range for first/last index | Use `1` as first index and `getLastCheckpointIndex()` as last |
| wstETH `wrap()` returns less than expected | stETH balance changed between approval and wrap due to rebase | Approve slightly more or use the actual balance after transfer |
| `ALLOWANCE_EXCEEDED` on wrap/withdrawal | Insufficient stETH approval for wstETH or WithdrawalQueue contract | Call `approve()` with the exact or higher amount before wrap/request |

## Security Considerations

### Rebasing Accounting

stETH balances change on every oracle report (typically daily). Smart contracts that store stETH balances in mappings will have stale values. Two safe patterns:

1. **Use wstETH** — Non-rebasing. Balance is stable. This is the correct choice for vaults, collateral, and any stored-balance pattern.
2. **Track shares** — Use `sharesOf()` and `getPooledEthByShares()` instead of `balanceOf()`. Shares are the invariant unit.

### The 1-2 Wei Rounding Issue

stETH `transfer(to, amount)` converts `amount` to shares (rounding down), then converts back to balance for the recipient (rounding down again). The sender's balance decreases by `amount`, but the recipient may receive `amount - 1` or `amount - 2` wei. This is inherent to the rebasing design.

Implications:
- Never use `require(balanceAfter - balanceBefore == amount)` with stETH
- Use `transferShares()` when exact amounts matter
- Tolerance of 2 wei on stETH balance checks

### Oracle Manipulation Risks

- The stETH/ETH Chainlink feed reflects market price, which can deviate from the protocol rate during market stress
- The on-chain `stEthPerToken()` rate is controlled by the Lido oracle — it can only change once per oracle report cycle and is bounded by sanity checks
- For highest security, cross-check the Chainlink feed against the on-chain rate and revert if deviation exceeds a threshold (e.g., 5%)

```solidity
/// @notice Revert if Chainlink wstETH/ETH deviates too far from on-chain rate
function validateOracleRate(int256 chainlinkAnswer, uint8 feedDecimals) internal view {
    uint256 onchainRate = IWstETH(0x7f39C581F595B53c5cb19bD0b3f8dA6c935E2Ca0).stEthPerToken();
    uint256 normalizedChainlink = feedDecimals <= 18
        ? uint256(chainlinkAnswer) * 10 ** (18 - feedDecimals)
        : uint256(chainlinkAnswer) / 10 ** (feedDecimals - 18);

    uint256 deviation = normalizedChainlink > onchainRate
        ? normalizedChainlink - onchainRate
        : onchainRate - normalizedChainlink;

    // 5% max deviation threshold
    if (deviation * 100 / onchainRate > 5) revert OracleDeviation();
}
```

### Integration Checklist

1. Use wstETH (not stETH) in any contract that stores balances
2. Never assert exact stETH transfer amounts — allow 2 wei tolerance
3. Check Chainlink feed staleness with per-feed heartbeat
4. Cross-validate oracle price against on-chain rate for critical paths
5. Handle withdrawal queue delays in UX — show estimated wait time
6. Test with a forked mainnet (`anvil --fork-url`) to verify rebase behavior

## References

- [Lido Docs](https://docs.lido.fi)
- [Lido Deployed Contracts](https://docs.lido.fi/deployed-contracts/)
- [stETH Integration Guide](https://docs.lido.fi/guides/steth-integration-guide)
- [wstETH on L2s](https://docs.lido.fi/token-guides/wsteth-bridging-guide)
- [Lido GitHub](https://github.com/lidofinance)
- [Withdrawal Queue Docs](https://docs.lido.fi/contracts/withdrawal-queue-erc721)
- [Chainlink stETH/ETH Feed](https://data.chain.link/ethereum/mainnet/crypto-eth/steth-eth)
