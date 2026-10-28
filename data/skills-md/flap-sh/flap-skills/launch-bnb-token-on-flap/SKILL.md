---
name: launch-bnb-token-on-flap
description: Launch a token on Flap BNB
metadata: {"openclaw": {"always": false, "emoji": "🦋", "homepage": "https://docs.flap.sh", "requires": {"anyBins": ["node", "npx", "npm"]}}}
---

# 🦋 Launch a BNB Token on Flap

Launch a token on [Flap](https://docs.flap.sh) (BNB Chain). Execute each step in order. Read each reference file at the step that requires it — do not pre-load them.

---

## ⚠️ Security Notice

This skill requires sensitive capabilities that must be provided:

- **EVM wallet with signing capability** — hardware wallet, browser wallet, MPC, or other secure signing method for BNB Chain (chain ID 56). The skill mainly focuses on constructing transaction data and then the transaction should be signed by the EVM wallet. Always verify transaction details independently before signing.    
- **BNB mainnet RPC endpoint** — a trusted RPC URL for reading blockchain state and broadcasting transactions. If not presently available, this skill will use the public fallback `https://bsc-dataseed.binance.org/`.  

---

## Directory structure

```
skills/launch-bnb-token-on-flap/
├── SKILL.md                        ← this file
└── references/
    ├── preflight.md                ← Step 0: prerequisites
    ├── quote-tokens.md              ← Step 1: quote token selection
    ├── vault-factory.md            ← Step 2: vault factory setup
    ├── meta-upload.md              ← Steps 3 & 6: metadata upload
    ├── tax-params.md               ← Step 4: tax parameters
    ├── salt-finding.md             ← Step 7: vanity salt mining
    ├── construct-tx.md             ← Step 8: transaction construction
    └── agent-id.md                 ← Optional: Agent ID launch
```

---

## Step 0 — Preflight check

Before starting, verify that all required reference files are present. If any are missing, you **MUST** obtain them before proceeding: 

**Required files:**

- `references/preflight.md`
- `references/quote-tokens.md`
- `references/vault-factory.md`
- `references/meta-upload.md`
- `references/tax-params.md`
- `references/salt-finding.md`
- `references/construct-tx.md`
- `references/agent-id.md`

Check each file exists, then read `references/preflight.md` and verify every prerequisite is satisfied before continuing.

---

## Step 1 — Choose token type and quote token

Every token launched by this skill is a **Flap Tax Token V3** (`TOKEN_TAXED_V3`). Standard
(non-tax) tokens are out of scope for this skill.

Determine the token configuration:

1. **Use a Vault Factory for revenue management?**
2. **Which quote token to launch against?** Read `references/quote-tokens.md` to fetch the
   current list of supported quote tokens on BNB Chain and resolve the `quoteToken` address and
   `decimals` to use in later steps. Defaults to native BNB if the user has no preference.
3. **Should the token use an Agent ID?** Read `references/agent-id.md`. If yes, resolve the
   Agent ID collection and check `newFeatureSwitch()` and `nftWhitelisted(agentId)` before
   building the transaction. The 2% per-origin buy cap is enabled automatically.

Decision map:

| Choice | Contract to call |
|---|---|
| Tax token, no vault | `Portal.newTokenV6` with `tokenVersion = TOKEN_TAXED_V3` |
| Tax token + vault | `VaultPortal.newTokenV6WithVault` with `tokenVersion = TOKEN_TAXED_V3` |

---

## Step 2 — Vault Factory setup *(tax + vault only)*

Read `references/vault-factory.md` to:

1. Determine the vault factory address to use.
2. Call the factory's `vaultDataSchema()` to understand the required `vaultData` encoding.
3. Determine the values needed to encode `vaultData`.

Skip this step for tax tokens without a vault.

---

## Step 3 — Token metadata

Determine the following token metadata fields:

- **Required:** `name`, `symbol`, image file path
- **Optional:** `description`, `twitter` handle, `telegram` handle (omit if not available)

Read `references/meta-upload.md` when ready to upload the image and construct the metadata JSON.

---

## Step 4 — Tax parameters

Read `references/tax-params.md` to determine and validate:

- `buyTaxRate`, `sellTaxRate`
- `taxDuration`, `antiFarmerDuration`
- `mktBps`, `deflationBps`, `dividendBps`, `lpBps`
- `minimumShareBalance`
- `beneficiary` address *(only for tax token without vault)*

---

## Step 5 — Launch buy amount

Determine `quoteAmt`: the amount of the chosen quote token (Step 1) to spend on the initial buy at
launch, in human units. Convert to base units using the quote token's `decimals` (see
`references/quote-tokens.md`) before encoding. If the quote token is native BNB, this also equals
the `msg.value` of the transaction; for any other (ERC-20) quote token, `msg.value` is `0` and the
wallet must instead hold and approve `quoteAmt` of that token beforehand. Use `0` to skip the
initial buy.

For an Agent ID launch, the dev buy is gated too: the buyer must hold the Agent ID collection, and
the 2% per-origin cap applies. A dev buy above the remaining allowance fills to the cap and
refunds the excess; it does not revert. See `references/agent-id.md`.

---

## Step 6 — Upload metadata

Follow `references/meta-upload.md` to upload the image and metadata JSON to Flap's upload API. Store the returned IPFS CID as `meta`.

---

## Step 7 — Find the salt

Read `references/salt-finding.md` to mine a vanity salt using CREATE2 prediction:

- Tax token address must end in `7777`.

Save the resulting `salt` (bytes32) and the predicted `tokenAddress`.

---

## Step 8 — Construct the EVM transaction

Read `references/construct-tx.md` to assemble the full calldata, `value`, and `to` address for the correct contract entry point (`Portal` or `VaultPortal`). For an Agent ID launch, use the `extensionID` / `extensionData` values from `references/agent-id.md`.

---

## Step 9 — Send the transaction

Broadcast the constructed transaction to BNB Chain using the available wallet. After confirmation, report the token address and a link to `https://flap.sh/bnb/<tokenAddress>`. For an Agent ID launch, also verify `nftGate(token)` equals the chosen Agent ID collection.
