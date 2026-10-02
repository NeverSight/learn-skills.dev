---
name: maker
description: "MakerDAO / Sky protocol -- Maker Vaults (CDPs) for DAI minting against collateral, DAI Savings Rate (DSR), Liquidation 2.0 with Dutch auctions, MKR governance, and Sky rebranding (USDS/SKY tokens). Covers DssProxyActions, Vat core accounting, Jug stability fees, and Spark Protocol integration."
license: Apache-2.0
metadata:
  author: cryptoskills
  version: "1.0"
  chain: ethereum
  category: DeFi
tags:
  - maker
  - makerdao
  - dai
  - vault
  - cdp
  - defi
  - sky
  - usds
---

# MakerDAO / Sky Protocol

MakerDAO is the protocol behind DAI, the largest decentralized stablecoin on Ethereum. Users lock collateral in Maker Vaults (formerly CDPs) to mint DAI. The protocol charges a stability fee (interest) on outstanding DAI debt and maintains a target price of $1 through the DAI Savings Rate (DSR) and liquidation mechanisms. In 2024, MakerDAO rebranded to Sky Protocol, introducing USDS (upgraded DAI) and SKY (upgraded MKR). Both old and new tokens coexist -- DAI/MKR are not deprecated.

## What You Probably Got Wrong

> LLMs consistently hallucinate Maker contract interfaces. The system is complex: all accounting happens in the Vat using internal `rad`/`wad`/`ray` units. Users interact through DSProxy + DssProxyActions, NOT directly with the Vat. These corrections are non-negotiable.

- **Maker is mid-rebrand to Sky.** DAI is becoming USDS. MKR is becoming SKY. Both coexist on mainnet. The old contracts still work. The new Sky contracts wrap/unwrap between old and new tokens. If someone says "Maker" they might mean either system. Always check which token set they need.

- **You do NOT call the Vat directly.** Normal users interact through a DSProxy contract that delegates calls to DssProxyActions. The Vat uses internal accounting units (rad = 10^45) that require precise math. DssProxyActions handles this conversion. If you see raw `Vat.frob()` calls, you are writing low-level code that will almost certainly have precision errors.

- **DAI has two representations.** Internal DAI in the Vat (`vat.dai(address)`) is measured in `rad` (10^45). External DAI (the ERC-20 token) is measured in `wad` (10^18). The DaiJoin adapter converts between them. Never confuse the two.

- **Stability fees accrue continuously.** The Jug contract compounds the stability fee rate into an ever-increasing `rate` accumulator per collateral type (ilk). Debt is stored as normalized debt (`art`) in the Vat. Actual debt = `art * rate`. You MUST call `jug.drip(ilk)` to update the rate before calculating accurate debt.

- **Liquidation 2.0 uses Dutch auctions, not English auctions.** The old Flipper (English auctions) was replaced by the Clipper (Dutch auctions) in Liquidation 2.0. Dutch auctions start at a high price and decrease over time. Bidders call `clipper.take()`, not `bid()`.

- **Vault IDs (cdpId) are NOT the same as ilk identifiers.** An ilk (e.g., `ETH-A`, `WBTC-A`) defines the collateral type and its risk parameters. A vault (CDP) is a specific user position within an ilk. The CdpManager maps vault IDs to (ilk, urn address) pairs.

- **DSR and USDS Savings Rate (sUSDS) are different contracts.** The original DSR uses DsrManager/Pot. The new Sky system uses the sUSDS token (ERC-4626 vault). They are separate yield sources with potentially different rates.

## Architecture Overview

```
User -> DSProxy -> DssProxyActions -> | CdpManager (vault management)
                                      | Vat (core accounting)
                                      | Jug (stability fees)
                                      | DaiJoin (DAI minting)
                                      | GemJoin (collateral locking)

User -> DsrManager -> Pot (DAI Savings Rate)

User -> DaiUsds (upgrade) -> USDS token
User -> MkrSky (upgrade) -> SKY token
User -> sUSDS vault -> USDS Savings Rate (ERC-4626)

Keepers -> Dog (liquidation trigger) -> Clipper (Dutch auction)
```

## Unit System (CRITICAL)

Maker uses three fixed-point number types internally. Getting these wrong causes silent precision loss or reverts.

| Unit | Decimals | Used For | Example |
|------|----------|----------|---------|
| `wad` | 10^18 | Token amounts (DAI, collateral), normalized debt (`art`) | 1.5 DAI = `1500000000000000000` |
| `ray` | 10^27 | Rate accumulators, per-second rates | 1.0 rate = `1000000000000000000000000000` |
| `rad` | 10^45 | Internal DAI balance in Vat (`vat.dai()`) | wad * ray = rad |

Arithmetic rules:
- `wad * wad / WAD = wad`
- `wad * ray / RAY = wad` (used for debt calculation: `art * rate`)
- `rad / ray = wad` (converting internal DAI to external)
- `rad / wad = ray`

```typescript
const WAD = 10n ** 18n;
const RAY = 10n ** 27n;
const RAD = 10n ** 45n;

function wmul(x: bigint, y: bigint): bigint {
  return (x * y + WAD / 2n) / WAD;
}

function rmul(x: bigint, y: bigint): bigint {
  return (x * y + RAY / 2n) / RAY;
}

function rdiv(x: bigint, y: bigint): bigint {
  return (x * RAY + y / 2n) / y;
}
```

## Core Contracts

### Vat -- Core Accounting Engine

The Vat is the central ledger. All collateral positions and DAI balances are recorded here. It never touches external tokens directly.

Key state:
- `ilks[ilk].Art` -- total normalized debt for this collateral type (wad)
- `ilks[ilk].rate` -- accumulated stability fee rate (ray)
- `ilks[ilk].spot` -- collateral price with safety margin (ray)
- `ilks[ilk].line` -- debt ceiling for this ilk (rad)
- `ilks[ilk].dust` -- minimum debt per vault (rad)
- `urns[ilk][urn].ink` -- locked collateral (wad)
- `urns[ilk][urn].art` -- normalized debt (wad)
- `dai[address]` -- internal DAI balance (rad)

The core function `frob(ilk, urn, dink, dart)` modifies a vault's collateral (`dink`) and debt (`dart`). Positive values add, negative values remove.

### CdpManager -- Vault Registry

Maps sequential vault IDs to `(ilk, urn)` pairs. Users create vaults through `CdpManager.open(ilk, usr)` which returns a `cdpId`. The manager owns the Vat urns and delegates control via `CdpManager.cdpCan`.

```typescript
const cdpManagerAbi = [
  {
    name: "open",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "ilk", type: "bytes32" },
      { name: "usr", type: "address" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "ilks",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "cdpId", type: "uint256" }],
    outputs: [{ name: "", type: "bytes32" }],
  },
  {
    name: "urns",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "cdpId", type: "uint256" }],
    outputs: [{ name: "", type: "address" }],
  },
  {
    name: "owns",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "cdpId", type: "uint256" }],
    outputs: [{ name: "", type: "address" }],
  },
  {
    name: "count",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "usr", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "first",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "usr", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "list",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "cdpId", type: "uint256" }],
    outputs: [
      { name: "prev", type: "uint256" },
      { name: "next", type: "uint256" },
    ],
  },
] as const;
```

### DssProxyActions -- User-Facing API

DssProxyActions is a library contract called via `delegatecall` from a user's DSProxy. It bundles multi-step vault operations into single transactions.

Key functions (called through DSProxy):
- `open(cdpManager, ilk, dsProxy)` -- create a new vault
- `lockETH(cdpManager, ethJoin, cdpId)` -- deposit ETH collateral (payable)
- `lockGem(cdpManager, gemJoin, cdpId, wad)` -- deposit ERC-20 collateral
- `draw(cdpManager, jug, daiJoin, cdpId, wad)` -- generate DAI from vault
- `wipe(cdpManager, daiJoin, cdpId, wad)` -- repay DAI debt
- `wipeAll(cdpManager, daiJoin, cdpId)` -- repay all DAI debt
- `freeETH(cdpManager, ethJoin, cdpId, wad)` -- withdraw ETH collateral
- `freeGem(cdpManager, gemJoin, cdpId, wad)` -- withdraw ERC-20 collateral
- `lockETHAndDraw(cdpManager, jug, ethJoin, daiJoin, cdpId, wadDai)` -- lock ETH + draw DAI in one tx
- `openLockETHAndDraw(cdpManager, jug, ethJoin, daiJoin, ilk, wadDai)` -- open vault + lock ETH + draw DAI

### Jug -- Stability Fee Accumulator

The Jug tracks per-ilk stability fee rates. Calling `jug.drip(ilk)` updates `vat.ilks[ilk].rate` by compounding the fee since the last update.

```typescript
const jugAbi = [
  {
    name: "drip",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "ilk", type: "bytes32" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "ilks",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "ilk", type: "bytes32" }],
    outputs: [
      { name: "duty", type: "uint256" },
      { name: "rho", type: "uint256" },
    ],
  },
] as const;
```

`duty` is the per-second stability fee rate (ray). `rho` is the last drip timestamp.

### Join Adapters

Join adapters move tokens between the external ERC-20 world and the internal Vat accounting.

- **GemJoin** -- locks collateral tokens. One per collateral type. `join(urn, wad)` moves tokens into the Vat. `exit(usr, wad)` withdraws them.
- **DaiJoin** -- converts between internal rad-denominated DAI and external ERC-20 DAI. `join(urn, wad)` burns ERC-20 DAI and credits internal DAI. `exit(usr, wad)` mints ERC-20 DAI from internal DAI.
- **ETHJoin** -- special join adapter that wraps native ETH into the Vat (no ERC-20 needed).

## Opening a Vault via DSProxy

The standard flow for opening a vault and generating DAI:

```typescript
import {
  createPublicClient,
  createWalletClient,
  http,
  parseEther,
  encodeFunctionData,
  type Address,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { mainnet } from "viem/chains";

const publicClient = createPublicClient({
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const account = privateKeyToAccount(
  process.env.PRIVATE_KEY as `0x${string}`
);

const walletClient = createWalletClient({
  account,
  chain: mainnet,
  transport: http(process.env.RPC_URL),
});

const CDP_MANAGER = "0x5ef30b9986345249bc32d8928B7ee64DE9435E39" as const;
const MCD_JUG = "0x19c0976f590D67707E62397C87829d896Dc0f1F1" as const;
const MCD_JOIN_ETH_A = "0x2F0b23f53734252Bda2277357e97e1517d6B042A" as const;
const MCD_JOIN_DAI = "0x9759A6Ac90977b93B58547b4A71c78317f391A28" as const;
const PROXY_ACTIONS = "0x82ecD135Dce65Fbc6DbdD0e4237E0AF93FFD5038" as const;

// ETH-A ilk identifier (bytes32)
const ETH_A_ILK = "0x4554482d41000000000000000000000000000000000000000000000000000000" as const;

const proxyActionsAbi = [
  {
    name: "openLockETHAndDraw",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "manager", type: "address" },
      { name: "jug", type: "address" },
      { name: "ethJoin", type: "address" },
      { name: "daiJoin", type: "address" },
      { name: "ilk", type: "bytes32" },
      { name: "wadD", type: "uint256" },
    ],
    outputs: [{ name: "cdp", type: "uint256" }],
  },
  {
    name: "lockETHAndDraw",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "manager", type: "address" },
      { name: "jug", type: "address" },
      { name: "ethJoin", type: "address" },
      { name: "daiJoin", type: "address" },
      { name: "cdp", type: "uint256" },
      { name: "wadD", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "wipeAllAndFreeETH",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "manager", type: "address" },
      { name: "ethJoin", type: "address" },
      { name: "daiJoin", type: "address" },
      { name: "cdp", type: "uint256" },
      { name: "wadC", type: "uint256" },
    ],
    outputs: [],
  },
] as const;

const dsProxyAbi = [
  {
    name: "execute",
    type: "function",
    stateMutability: "payable",
    inputs: [
      { name: "_target", type: "address" },
      { name: "_data", type: "bytes" },
    ],
    outputs: [{ name: "response", type: "bytes32" }],
  },
] as const;
```

### Execute via DSProxy

All DssProxyActions calls go through your DSProxy's `execute(target, data)`:

```typescript
async function openVaultAndDrawDai(
  dsProxy: Address,
  ethAmount: bigint,
  daiAmount: bigint
): Promise<`0x${string}`> {
  const calldata = encodeFunctionData({
    abi: proxyActionsAbi,
    functionName: "openLockETHAndDraw",
    args: [CDP_MANAGER, MCD_JUG, MCD_JOIN_ETH_A, MCD_JOIN_DAI, ETH_A_ILK, daiAmount],
  });

  const { request } = await publicClient.simulateContract({
    address: dsProxy,
    abi: dsProxyAbi,
    functionName: "execute",
    args: [PROXY_ACTIONS, calldata],
    value: ethAmount,
    account: account.address,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") {
    throw new Error("openLockETHAndDraw reverted");
  }

  return hash;
}
```

## Reading Vault State

```typescript
const vatAbi = [
  {
    name: "ilks",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "ilk", type: "bytes32" }],
    outputs: [
      { name: "Art", type: "uint256" },
      { name: "rate", type: "uint256" },
      { name: "spot", type: "uint256" },
      { name: "line", type: "uint256" },
      { name: "dust", type: "uint256" },
    ],
  },
  {
    name: "urns",
    type: "function",
    stateMutability: "view",
    inputs: [
      { name: "ilk", type: "bytes32" },
      { name: "urn", type: "address" },
    ],
    outputs: [
      { name: "ink", type: "uint256" },
      { name: "art", type: "uint256" },
    ],
  },
  {
    name: "dai",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "usr", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const MCD_VAT = "0x35D1b3F3D7966A1DFe207aa4514C12a259A0492B" as const;

async function getVaultInfo(cdpId: bigint) {
  const [ilk, urn] = await Promise.all([
    publicClient.readContract({
      address: CDP_MANAGER,
      abi: cdpManagerAbi,
      functionName: "ilks",
      args: [cdpId],
    }),
    publicClient.readContract({
      address: CDP_MANAGER,
      abi: cdpManagerAbi,
      functionName: "urns",
      args: [cdpId],
    }),
  ]);

  const [ilkData, urnData] = await Promise.all([
    publicClient.readContract({
      address: MCD_VAT,
      abi: vatAbi,
      functionName: "ilks",
      args: [ilk],
    }),
    publicClient.readContract({
      address: MCD_VAT,
      abi: vatAbi,
      functionName: "urns",
      args: [ilk, urn],
    }),
  ]);

  const ink = urnData[0]; // locked collateral (wad)
  const art = urnData[1]; // normalized debt (wad)
  const rate = ilkData[1]; // accumulated rate (ray)
  const spot = ilkData[2]; // price with safety margin (ray)

  // Actual debt = art * rate (result in rad, divide by RAY for wad)
  const RAY = 10n ** 27n;
  const debt = (art * rate + RAY - 1n) / RAY; // round up
  // Collateral value = ink * spot (result in rad, divide by RAY for wad)
  const collateralValue = (ink * spot) / RAY;

  return { ilk, urn, ink, art, rate, spot, debt, collateralValue };
}
```

## DAI Savings Rate (DSR)

The DSR lets DAI holders earn yield by depositing into the Pot contract. DsrManager simplifies the Pot interaction.

```typescript
const DSR_MANAGER = "0x373238337Bfe1146fb49989fc222523f83081dDb" as const;
const MCD_POT = "0x197E90f9FAD81970bA7976f33CbD77088E5D7cf7" as const;

const dsrManagerAbi = [
  {
    name: "join",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "dst", type: "address" },
      { name: "wad", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "exit",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "dst", type: "address" },
      { name: "wad", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "exitAll",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "dst", type: "address" }],
    outputs: [],
  },
  {
    name: "pieOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "usr", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

const potAbi = [
  {
    name: "chi",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "dsr",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "rho",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "drip",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

async function getDsrInfo() {
  const [dsr, chi, rho] = await Promise.all([
    publicClient.readContract({
      address: MCD_POT,
      abi: potAbi,
      functionName: "dsr",
    }),
    publicClient.readContract({
      address: MCD_POT,
      abi: potAbi,
      functionName: "chi",
    }),
    publicClient.readContract({
      address: MCD_POT,
      abi: potAbi,
      functionName: "rho",
    }),
  ]);

  // DSR APY = dsr^(seconds_per_year) - 1
  // dsr is a per-second rate in ray (10^27)
  const RAY = 10n ** 27n;
  const dsrFloat = Number(dsr) / Number(RAY);
  const dsrApy = (Math.pow(dsrFloat, 31536000) - 1) * 100;

  return { dsr, chi, rho, dsrApy };
}

async function depositToDsr(daiAmount: bigint): Promise<`0x${string}`> {
  const DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F" as const;

  // Approve DsrManager to spend DAI
  const approveHash = await walletClient.writeContract({
    address: DAI,
    abi: [
      {
        name: "approve",
        type: "function",
        stateMutability: "nonpayable",
        inputs: [
          { name: "spender", type: "address" },
          { name: "amount", type: "uint256" },
        ],
        outputs: [{ name: "", type: "bool" }],
      },
    ] as const,
    functionName: "approve",
    args: [DSR_MANAGER, daiAmount],
  });
  const approveReceipt = await publicClient.waitForTransactionReceipt({
    hash: approveHash,
  });
  if (approveReceipt.status !== "success") {
    throw new Error("DAI approval for DSR failed");
  }

  // Deposit DAI into DSR
  const { request } = await publicClient.simulateContract({
    address: DSR_MANAGER,
    abi: dsrManagerAbi,
    functionName: "join",
    args: [account.address, daiAmount],
    account: account.address,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") {
    throw new Error("DSR deposit reverted");
  }

  return hash;
}

async function getDsrBalance(user: Address): Promise<bigint> {
  const RAY = 10n ** 27n;

  const [pie, chi] = await Promise.all([
    publicClient.readContract({
      address: DSR_MANAGER,
      abi: dsrManagerAbi,
      functionName: "pieOf",
      args: [user],
    }),
    publicClient.readContract({
      address: MCD_POT,
      abi: potAbi,
      functionName: "chi",
    }),
  ]);

  // DAI balance = pie * chi / RAY
  return (pie * chi) / RAY;
}
```

## Liquidation 2.0 (Dutch Auctions)

When a vault's collateral ratio drops below the liquidation ratio, keepers trigger liquidation via the Dog contract. The Dog starts a Dutch auction via the Clipper for that ilk.

### Liquidation Flow

1. `Dog.bark(ilk, urn, keeper)` -- triggers liquidation, creates a Clipper auction
2. Clipper starts at a high price (using `calc` -- an AbacI price calculator)
3. Price decreases over time according to the price curve
4. Anyone calls `Clipper.take(id, amt, max, who, data)` to buy collateral
5. Remaining collateral (if any) returns to the vault owner

```typescript
const MCD_DOG = "0x135954d155898D42C90D2a57824C690e0c7BEf1B" as const;

const dogAbi = [
  {
    name: "bark",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "ilk", type: "bytes32" },
      { name: "urn", type: "address" },
      { name: "kpr", type: "address" },
    ],
    outputs: [{ name: "id", type: "uint256" }],
  },
  {
    name: "ilks",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "ilk", type: "bytes32" }],
    outputs: [
      { name: "clip", type: "address" },
      { name: "chop", type: "uint256" },
      { name: "hole", type: "uint256" },
      { name: "dirt", type: "uint256" },
    ],
  },
] as const;

const clipperAbi = [
  {
    name: "take",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "id", type: "uint256" },
      { name: "amt", type: "uint256" },
      { name: "max", type: "uint256" },
      { name: "who", type: "address" },
      { name: "data", type: "bytes" },
    ],
    outputs: [],
  },
  {
    name: "sales",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "id", type: "uint256" }],
    outputs: [
      { name: "pos", type: "uint256" },
      { name: "tab", type: "uint256" },
      { name: "lot", type: "uint256" },
      { name: "usr", type: "address" },
      { name: "tic", type: "uint96" },
      { name: "top", type: "uint256" },
    ],
  },
  {
    name: "getStatus",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "id", type: "uint256" }],
    outputs: [
      { name: "needsRedo", type: "bool" },
      { name: "price", type: "uint256" },
      { name: "lot", type: "uint256" },
      { name: "tab", type: "uint256" },
    ],
  },
  {
    name: "count",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "list",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256[]" }],
  },
] as const;
```

### Participating in a Dutch Auction

```typescript
async function takeFromAuction(
  clipperAddress: Address,
  auctionId: bigint,
  collateralAmount: bigint,
  maxPrice: bigint
): Promise<`0x${string}`> {
  // Check auction status
  const status = await publicClient.readContract({
    address: clipperAddress,
    abi: clipperAbi,
    functionName: "getStatus",
    args: [auctionId],
  });

  const [needsRedo, currentPrice, lot, tab] = status;

  if (needsRedo) {
    throw new Error("Auction needs redo -- price has gone stale");
  }

  if (currentPrice > maxPrice) {
    throw new Error(
      `Current price ${currentPrice} exceeds max ${maxPrice}. Wait for price to decrease.`
    );
  }

  if (lot === 0n || tab === 0n) {
    throw new Error("Auction is complete -- no collateral remaining");
  }

  // take() requires DAI approval to the Vat (internal DAI)
  // Keepers typically pre-approve the Clipper in the Vat
  const { request } = await publicClient.simulateContract({
    address: clipperAddress,
    abi: clipperAbi,
    functionName: "take",
    args: [auctionId, collateralAmount, maxPrice, account.address, "0x"],
    account: account.address,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") {
    throw new Error("Auction take reverted");
  }

  return hash;
}
```

## MKR Governance

MKR holders vote on protocol parameters through the Chief contract. The voting flow uses a delegate + hat pattern.

### Executive Voting

Executive votes change live protocol parameters. They are spell contracts that are `cast` when enough MKR is staked on them.

```typescript
const MCD_GOV = "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2" as const; // MKR token
const MCD_ADM = "0x0a3f6849f78076aefaDf113F5BED87720274dDC0" as const; // DSChief

const chiefAbi = [
  {
    name: "vote",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "yays", type: "address[]" }],
    outputs: [{ name: "", type: "bytes32" }],
  },
  {
    name: "lock",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "wad", type: "uint256" }],
    outputs: [],
  },
  {
    name: "free",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [{ name: "wad", type: "uint256" }],
    outputs: [],
  },
  {
    name: "hat",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "address" }],
  },
  {
    name: "approvals",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "candidate", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "deposits",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "usr", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;
```

### Governance Flow

1. Lock MKR in Chief: `chief.lock(amount)`
2. Vote for a spell: `chief.vote([spellAddress])`
3. If the spell gets the most MKR, it becomes the `hat`
4. Anyone can `lift` the hat to make it the active authority
5. The spell is `cast` to execute parameter changes

## Sky Protocol Rebranding

MakerDAO rebranded to Sky Protocol in 2024. New tokens:
- **USDS** -- upgraded DAI (1:1 convertible)
- **SKY** -- upgraded MKR (1 MKR = 24,000 SKY)
- **sUSDS** -- USDS savings token (ERC-4626), replaces DSR for USDS holders

### Token Migration

```typescript
const DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F" as const;
const USDS = "0xdC035D45d973E3EC169d2276DDab16f1e407384F" as const;
const MKR = "0x9f8F72aA9304c8B593d555F12eF6589cC3A579A2" as const;
const SKY = "0x56072C95FAA7932F4D8Aa042BE0611d2a2CE73a5" as const;
const DAI_USDS = "0x3225737a9Bbb6473CB4a45b7244ACa2BeFdB276A" as const; // DaiUsds converter
const MKR_SKY = "0xBDcFCA946b6CDd965f99a839e4435Bcdc1bc470B" as const; // MkrSky converter
const SUSDS = "0xa3931d71877C0E7a3148CB7Eb4463524FEc27fbD" as const; // sUSDS vault

const daiUsdsAbi = [
  {
    name: "daiToUsds",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "usr", type: "address" },
      { name: "wad", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "usdsToDai",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "usr", type: "address" },
      { name: "wad", type: "uint256" },
    ],
    outputs: [],
  },
] as const;

const mkrSkyAbi = [
  {
    name: "mkrToSky",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "usr", type: "address" },
      { name: "mkrAmt", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "skyToMkr",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "usr", type: "address" },
      { name: "skyAmt", type: "uint256" },
    ],
    outputs: [],
  },
  {
    name: "rate",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;

// sUSDS is an ERC-4626 vault for USDS savings
const susdsAbi = [
  {
    name: "deposit",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "assets", type: "uint256" },
      { name: "receiver", type: "address" },
    ],
    outputs: [{ name: "shares", type: "uint256" }],
  },
  {
    name: "withdraw",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "assets", type: "uint256" },
      { name: "receiver", type: "address" },
      { name: "owner", type: "address" },
    ],
    outputs: [{ name: "shares", type: "uint256" }],
  },
  {
    name: "redeem",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "shares", type: "uint256" },
      { name: "receiver", type: "address" },
      { name: "owner", type: "address" },
    ],
    outputs: [{ name: "assets", type: "uint256" }],
  },
  {
    name: "convertToAssets",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "shares", type: "uint256" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "convertToShares",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "assets", type: "uint256" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "totalAssets",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
] as const;
```

### Upgrading DAI to USDS

```typescript
async function upgradeDaiToUsds(amount: bigint): Promise<`0x${string}`> {
  // Approve DaiUsds converter to spend DAI
  const approveHash = await walletClient.writeContract({
    address: DAI,
    abi: [
      {
        name: "approve",
        type: "function",
        stateMutability: "nonpayable",
        inputs: [
          { name: "spender", type: "address" },
          { name: "amount", type: "uint256" },
        ],
        outputs: [{ name: "", type: "bool" }],
      },
    ] as const,
    functionName: "approve",
    args: [DAI_USDS, amount],
  });
  const approveReceipt = await publicClient.waitForTransactionReceipt({
    hash: approveHash,
  });
  if (approveReceipt.status !== "success") {
    throw new Error("DAI approval for upgrade failed");
  }

  // Convert DAI -> USDS (1:1)
  const { request } = await publicClient.simulateContract({
    address: DAI_USDS,
    abi: daiUsdsAbi,
    functionName: "daiToUsds",
    args: [account.address, amount],
    account: account.address,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") {
    throw new Error("DAI to USDS conversion reverted");
  }

  return hash;
}
```

### USDS Savings Rate (sUSDS)

```typescript
async function depositToSusds(usdsAmount: bigint): Promise<{
  hash: `0x${string}`;
  shares: bigint;
}> {
  // Approve sUSDS vault to spend USDS
  const approveHash = await walletClient.writeContract({
    address: USDS,
    abi: [
      {
        name: "approve",
        type: "function",
        stateMutability: "nonpayable",
        inputs: [
          { name: "spender", type: "address" },
          { name: "amount", type: "uint256" },
        ],
        outputs: [{ name: "", type: "bool" }],
      },
    ] as const,
    functionName: "approve",
    args: [SUSDS, usdsAmount],
  });
  const approveReceipt = await publicClient.waitForTransactionReceipt({
    hash: approveHash,
  });
  if (approveReceipt.status !== "success") {
    throw new Error("USDS approval for sUSDS failed");
  }

  // Deposit USDS into sUSDS vault
  const { request, result } = await publicClient.simulateContract({
    address: SUSDS,
    abi: susdsAbi,
    functionName: "deposit",
    args: [usdsAmount, account.address],
    account: account.address,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") {
    throw new Error("sUSDS deposit reverted");
  }

  return { hash, shares: result };
}
```

## Spark Protocol

Spark Protocol is an Aave V3 fork maintained by the Maker/Sky ecosystem. It uses DAI/USDS as its primary lending asset with preferential rates backed by the Maker D3M (Direct Deposit Module).

Key difference from vanilla Aave V3: Spark has a direct credit line from Maker, so DAI/USDS liquidity is deep and rates are governance-controlled.

Spark uses standard Aave V3 interfaces -- see the Aave skill for integration patterns. The Pool contract address for Spark on Ethereum mainnet is `0xC13e21B648A5Ee794902342038FF3aDAB66BE987`.

## DSProxy Setup

Most users need a DSProxy before interacting with Maker Vaults. The ProxyRegistry creates one per address.

```typescript
const PROXY_REGISTRY = "0x4678f0a6958e4D2Bc4F1BAF7Bc52E8F3564f3fE4" as const;

const proxyRegistryAbi = [
  {
    name: "build",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [],
    outputs: [{ name: "proxy", type: "address" }],
  },
  {
    name: "proxies",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "owner", type: "address" }],
    outputs: [{ name: "", type: "address" }],
  },
] as const;

async function getOrCreateProxy(): Promise<Address> {
  const existing = await publicClient.readContract({
    address: PROXY_REGISTRY,
    abi: proxyRegistryAbi,
    functionName: "proxies",
    args: [account.address],
  });

  const ZERO_ADDRESS = "0x0000000000000000000000000000000000000000" as Address;
  if (existing !== ZERO_ADDRESS) {
    return existing;
  }

  const { request } = await publicClient.simulateContract({
    address: PROXY_REGISTRY,
    abi: proxyRegistryAbi,
    functionName: "build",
    account: account.address,
  });

  const hash = await walletClient.writeContract(request);
  const receipt = await publicClient.waitForTransactionReceipt({ hash });
  if (receipt.status !== "success") {
    throw new Error("DSProxy creation reverted");
  }

  const proxyAddress = await publicClient.readContract({
    address: PROXY_REGISTRY,
    abi: proxyRegistryAbi,
    functionName: "proxies",
    args: [account.address],
  });

  return proxyAddress;
}
```

## Common Patterns

### Calculate Vault Collateralization Ratio

```typescript
async function getCollateralizationRatio(cdpId: bigint): Promise<{
  ratio: number;
  isUnsafe: boolean;
}> {
  const vault = await getVaultInfo(cdpId);
  const RAY = 10n ** 27n;

  if (vault.art === 0n) {
    return { ratio: Infinity, isUnsafe: false };
  }

  // debt = art * rate (in rad), collateralValue = ink * spot (in rad)
  const debt = vault.art * vault.rate;
  const collateralValue = vault.ink * vault.spot;

  if (debt === 0n) {
    return { ratio: Infinity, isUnsafe: false };
  }

  const ratio = Number(collateralValue * 10000n / debt) / 100;
  const isUnsafe = collateralValue < debt;

  return { ratio, isUnsafe };
}
```

### Encode Ilk Name

```typescript
import { toHex, padHex } from "viem";

function encodeIlk(name: string): `0x${string}` {
  return padHex(toHex(name), { size: 32, dir: "right" });
}

// encodeIlk("ETH-A") = 0x4554482d41000000000000000000000000000000000000000000000000000000
```

### List User's Vaults

```typescript
async function listUserVaults(user: Address): Promise<bigint[]> {
  const count = await publicClient.readContract({
    address: CDP_MANAGER,
    abi: cdpManagerAbi,
    functionName: "count",
    args: [user],
  });

  if (count === 0n) return [];

  const first = await publicClient.readContract({
    address: CDP_MANAGER,
    abi: cdpManagerAbi,
    functionName: "first",
    args: [user],
  });

  const vaults: bigint[] = [first];
  let current = first;

  for (let i = 1n; i < count; i++) {
    const [, next] = await publicClient.readContract({
      address: CDP_MANAGER,
      abi: cdpManagerAbi,
      functionName: "list",
      args: [current],
    });
    if (next === 0n) break;
    vaults.push(next);
    current = next;
  }

  return vaults;
}
```

## Security Considerations

- **Dust limit**: Every vault must maintain at least `dust` amount of debt (or zero debt). Partial repayments that leave debt below dust will revert.
- **Oracle delay**: Maker uses OSM (Oracle Security Module) which delays price updates by 1 hour. This means liquidations use prices that are up to 1 hour old.
- **Liquidation penalty**: The `chop` parameter (typically 13%) is added on top of the debt during liquidation. Maintain safe collateralization ratios.
- **DSProxy ownership**: Your DSProxy is a smart contract wallet. If you lose access, you lose control of all vaults owned by that proxy.
- **Governance attacks**: The Chief contract is vulnerable to flash loan governance attacks. The GSM (Governance Security Module) imposes a 48-hour delay on spell execution.

## References

- [Maker Technical Docs](https://docs.makerdao.com/)
- [Sky Protocol Docs](https://docs.sky.money/)
- [Maker GitHub](https://github.com/makerdao)
- [DssProxyActions Source](https://github.com/makerdao/dss-proxy-actions)
- [Liquidation 2.0 Module](https://github.com/makerdao/dss/blob/master/src/clip.sol)
- [Sky Token Migration](https://github.com/makerdao/sdai)
- [Spark Protocol](https://spark.fi/)
- [Maker Changelog (addresses)](https://chainlog.makerdao.com/)
