---
name: swap-execute
description: This skill should be used when the user asks to "execute swap", "send swap transaction", "submit swap", "broadcast swap", "run the swap", "execute the trade", or wants to submit a previously built swap transaction on-chain. Uses Foundry's `cast send` to broadcast transactions. Requires swap calldata from swap-build skill output.
metadata:
  tags:
    - defi
    - kyberswap
    - swap
    - execute
    - foundry
    - evm
  provider: KyberSwap
  homepage: https://kyberswap.com
---

# KyberSwap Execute Skill

Execute a swap transaction on-chain using Foundry's `cast send`. This skill takes the output from `swap-build` and broadcasts the transaction.

## Prerequisites

- **Foundry installed**: `cast` must be available in PATH
- **Wallet configured**: One of the methods below
- **ETH for gas**: Sender must have native token for gas fees

### Wallet Setup (One-Time)

> ### ⚠️ USE YOUR EXISTING WALLET MANAGEMENT FIRST ⚠️
>
> **If you or your agent already have wallet management** (key management service, vault, HSM, custodial API, MPC signer, or any secure signing infrastructure), **use that.** Skip the examples below entirely.
>
> The wallet options below are **example setups for development and testing only.** They have known security issues: plaintext password files on disk, private keys in shell environments, no access control, no audit trail, no key rotation. **Do not use them with real funds in production.** Consider this from the very start — not after you've already built around a testing setup.

**Option A: Encrypted Keystore (Recommended)**
```bash
# Import private key to encrypted keystore
cast wallet import mykey --interactive
# Enter private key, then set encryption password

# Create password file securely (prompts without echoing to terminal)
printf "Password: " && read -s pw && printf '\n' && echo "$pw" > ~/.foundry/.password && chmod 600 ~/.foundry/.password

# Verify
cast wallet list
```

**Option B: Environment Variable**
Set the key in your current shell session only (do not persist to shell profiles):
```bash
printf "Enter private key: " && read -s PRIVATE_KEY && printf '\n' && export PRIVATE_KEY
```
See the security section in `${CLAUDE_PLUGIN_ROOT}/skills/swap-execute/references/wallet-setup.md` for details.

**NEVER echo, print, log, or display any private key value, even in error messages or debug output.**

**Option C: Ledger Hardware Wallet**
- Connect Ledger, open Ethereum app
- No setup needed, will prompt for physical confirmation

See `${CLAUDE_PLUGIN_ROOT}/skills/swap-execute/references/wallet-setup.md` for detailed instructions.

## Input

This skill requires the JSON output from `swap-build`:

```json
{
  "type": "kyberswap-swap",
  "chain": "ethereum",
  "tx": {
    "to": "0x6131B5fae19EA4f9D964eAc0408E4408b66337b5",
    "data": "0x...",
    "value": "1000000000000000000",
    "gas": "250000"
  },
  "sender": "0x...",
  "tokenIn": { "symbol": "ETH", "amount": "1" },
  "tokenOut": { "symbol": "USDC", "amount": "2345.67" }
}
```

## Workflow

### Step 1: Validate Input

Ensure the user has provided or you have access to the swap output JSON containing:
- `tx.to` — Router address
- `tx.data` — Encoded calldata
- `tx.value` — Transaction value in wei (for native token swaps)
- `chain` — Chain to execute on
- `sender` — Sender address

If the JSON is not available, ask the user to run `/swap-build` first.

### Step 2: Determine RPC URL

Use the appropriate RPC endpoint for the chain:

| Chain | RPC URL |
|-------|---------|
| ethereum | `https://ethereum-rpc.publicnode.com` |
| arbitrum | `https://arb1.arbitrum.io/rpc` |
| polygon | `https://polygon-rpc.com` |
| optimism | `https://mainnet.optimism.io` |
| base | `https://mainnet.base.org` |
| bsc | `https://bsc-dataseed.binance.org` |
| avalanche | `https://api.avax.network/ext/bc/C/rpc` |
| linea | `https://rpc.linea.build` |
| mantle | `https://rpc.mantle.xyz` |
| sonic | `https://rpc.soniclabs.com` |
| berachain | `https://rpc.berachain.com` |
| ronin | `https://api.roninchain.com/rpc` |
| unichain | `https://rpc.unichain.org` |
| hyperevm | `https://rpc.hyperliquid.xyz/evm` |
| plasma | `https://plasma.drpc.org` |
| etherlink | `https://node.mainnet.etherlink.com` |
| monad | `https://rpc.monad.xyz` |
| megaeth | `https://rpc.megaeth.com` | <!-- MegaETH: state=new in KyberSwap API, RPC not confirmed as of 2026-02-19 --> |

Or the user can specify a custom RPC with `--rpc-url`.

### Step 3: Confirm Execution

**CRITICAL: Always confirm before executing. Transactions are irreversible.**

> **Time-sensitive:** Routes expire in ~30 seconds. If the user takes too long to confirm, re-build with a fresh quote from `/swap-build` before executing. Stale routes cause on-chain reverts that waste gas.

Present the transaction details:

```
## Swap Execution — Final Confirmation

**{tokenIn.amount} {tokenIn.symbol} → {tokenOut.amount} {tokenOut.symbol}** on {chain}

| Field | Value |
|-------|-------|
| Router | `{tx.to}` |
| Value | {tx.value} wei ({value in ETH} ETH) |
| Gas Limit | {tx.gas} |
| Sender | `{sender}` |

⚠️ **WARNING: This action is IRREVERSIBLE.**
- Funds will be sent from your wallet
- Gas fees will be charged even if the swap fails
- Verify the router address is correct: `0x6131B5fae19EA4f9D964eAc0408E4408b66337b5`

**Do you want to execute this swap?** (yes/no)
```

Wait for explicit "yes" confirmation before proceeding.

### Step 3b: Simulate Transaction (Recommended)

Before sending, simulate the transaction with `cast call` to catch reverts without spending gas:

```bash
cast call \
  --rpc-url {RPC_URL} \
  --value {tx.value} \
  --from {sender} \
  {tx.to} \
  {tx.data}
```

If this reverts, the transaction would fail on-chain. Re-build with a fresh route before retrying.

### Step 4: Determine Wallet Method

Ask the user how they want to sign (if not already specified):

```
How do you want to sign this transaction?

1. Keystore (encrypted key at ~/.foundry/keystores/)
2. Environment variable ($PRIVATE_KEY)
3. Ledger hardware wallet
4. Trezor hardware wallet
```

### Step 5: Execute with Cast

Build the `cast send` command based on wallet method:

**Option 1: Keystore + Password File (Recommended)**
```bash
cast send \
  --rpc-url {RPC_URL} \
  --account {keystore_name} \
  --password-file ~/.foundry/.password \
  --gas-limit {tx.gas} \
  --value {tx.value} \
  {tx.to} \
  {tx.data}
```

**Option 2: Environment Variable**
```bash
cast send \
  --rpc-url {RPC_URL} \
  --private-key $PRIVATE_KEY \
  --gas-limit {tx.gas} \
  --value {tx.value} \
  {tx.to} \
  {tx.data}
```

**Option 3: Ledger**
```bash
cast send \
  --rpc-url {RPC_URL} \
  --ledger \
  --gas-limit {tx.gas} \
  --value {tx.value} \
  {tx.to} \
  {tx.data}
```

**Option 4: Trezor**
```bash
cast send \
  --rpc-url {RPC_URL} \
  --trezor \
  --gas-limit {tx.gas} \
  --value {tx.value} \
  {tx.to} \
  {tx.data}
```

**Wallet flags summary:**

| Method | Flags |
|--------|-------|
| Keystore | `--account NAME --password-file ~/.foundry/.password` |
| Env var | `--private-key $PRIVATE_KEY` |
| Ledger | `--ledger` |
| Trezor | `--trezor` |

**Example commands:**

```bash
# Using private key from environment
cast send \
  --rpc-url https://ethereum-rpc.publicnode.com \
  --private-key $PRIVATE_KEY \
  --gas-limit 250000 \
  --value 1000000000000000000 \
  0x6131B5fae19EA4f9D964eAc0408E4408b66337b5 \
  0x...calldata...

# Using Ledger hardware wallet
cast send \
  --rpc-url https://arb1.arbitrum.io/rpc \
  --ledger \
  --gas-limit 250000 \
  --value 0 \
  0x6131B5fae19EA4f9D964eAc0408E4408b66337b5 \
  0x...calldata...
```

### Step 6: Handle Result

**On success**, parse the output and display:

```
## Transaction Submitted ✅

| Field | Value |
|-------|-------|
| Transaction Hash | `{txHash}` |
| Block Number | {blockNumber} |
| Gas Used | {gasUsed} |

**Explorer Link:** {explorerUrl}/tx/{txHash}

Your swap of {tokenIn.amount} {tokenIn.symbol} → {tokenOut.amount} {tokenOut.symbol} has been submitted.
```

**Explorer URLs by chain:**

| Chain | Explorer |
|-------|----------|
| ethereum | https://etherscan.io |
| arbitrum | https://arbiscan.io |
| polygon | https://polygonscan.com |
| optimism | https://optimistic.etherscan.io |
| base | https://basescan.org |
| bsc | https://bscscan.com |
| avalanche | https://snowtrace.io |
| linea | https://lineascan.build |
| mantle | https://mantlescan.xyz |
| sonic | https://sonicscan.io |
| berachain | https://berascan.com |
| ronin | https://app.roninchain.com |
| unichain | https://uniscan.xyz |
| hyperevm | https://explorer.hyperliquid.xyz |
| plasma | https://plasmascan.io |
| etherlink | https://explorer.etherlink.com |
| monad | https://explorer.monad.xyz |
| megaeth | https://explorer.megaeth.com |

**On failure**, display the error:

```
## Transaction Failed ❌

**Error:** {error message}

Common issues:
- Insufficient gas: Increase gas limit
- Insufficient balance: Check native token balance for gas
- Slippage exceeded: Route expired, rebuild with fresh quote
- Approval needed: Run token approval first for ERC-20 inputs
```

## ERC-20 Approval (if needed)

If the swap input is an ERC-20 token (not native), the user may need to approve first:

```bash
cast send \
  --rpc-url {RPC_URL} \
  {WALLET_FLAG} \
  {tokenIn.address} \
  "approve(address,uint256)" \
  {router_address} \
  {amountInWei}
```

Check current allowance:

```bash
cast call \
  --rpc-url {RPC_URL} \
  {tokenIn.address} \
  "allowance(address,address)(uint256)" \
  {sender} \
  {router_address}
```

## Important Notes

- **Never expose private keys** in command output or logs
- **Always confirm** before executing — transactions cannot be undone
- **Check balances before executing** — verify native token balance covers `tx.value` + gas cost, and ERC-20 balance covers `amountInWei`:
  ```bash
  # Check native balance (returns wei)
  cast balance --rpc-url {RPC_URL} {sender}
  # Check current gas price (returns wei)
  cast gas-price --rpc-url {RPC_URL}
  # Check ERC-20 balance
  cast call --rpc-url {RPC_URL} {tokenIn.address} "balanceOf(address)(uint256)" {sender}
  ```
- **Apply a 20% gas limit buffer** — use `gas_limit = tx.gas + tx.gas / 5` to reduce out-of-gas failures
- **Verify router address** matches expected: `0x6131B5fae19EA4f9D964eAc0408E4408b66337b5`
- **Routes expire quickly (~30 seconds)** — execute promptly after building. Stale routes are the most common cause of on-chain failures.
- **Verify chain ID when using custom RPCs** — before sending, run `cast chain-id --rpc-url {RPC_URL}` and confirm it matches the expected chain ID to avoid sending transactions to the wrong chain

## Common Errors

### Pre-Transaction Errors (transaction not sent, no gas spent)

| Error | Cause | Quick Fix |
|-------|-------|-----------|
| Gas estimation failed | RPC node issue or stale route | Retry, or re-run `/swap-build` for a fresh route. Try a different RPC if persistent. |
| Simulation revert | Insufficient balance, missing approval, or stale route | Check token balance >= `amountIn`, check approval for router, then re-build with fresh route. |
| Transaction submission failed | RPC rejected tx, nonce conflict, or insufficient gas balance | Check native token balance covers gas. Reset nonce if stuck transactions exist. Try a different RPC. |

### On-Chain Errors (transaction sent, gas spent)

| Error | Cause | Quick Fix |
|-------|-------|-----------|
| `TRANSFER_FROM_FAILED` | Router can't pull input tokens | Approve the router (`routerAddress`) to spend at least `amountInWei` of the input token. Check token balance. |
| `ETH_TRANSFER_FAILED` | Insufficient ETH for swap + gas | Ensure wallet has enough ETH for both `tx.value` and gas fees. Send exactly the `transactionValue` from the build response. |
| `Return amount is not enough` | Price moved beyond slippage | Re-build with a fresh route. Or increase `slippageTolerance`. For MEV protection, use a private RPC (e.g., Flashbots). |
| Out of gas | Gas limit too low for the route | Use `gas_limit = tx.gas + tx.gas / 5` (20% buffer). Do not cap gas limit below the build response's estimate. |
| Call failed (internal) | Pool state changed or pool issue | Re-build with a fresh route. Use `excludedSources` to skip the failing DEX. |

## Troubleshooting

For errors not covered above (API errors during build, PMM/RFQ failures, full error code catalog), refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.
