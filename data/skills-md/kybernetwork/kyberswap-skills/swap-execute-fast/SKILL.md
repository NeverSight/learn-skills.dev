---
name: swap-execute-fast
description: This skill should ONLY be used when the user explicitly asks for immediate, no-confirmation execution using phrases like "fast swap", "execute immediately", "swap with no confirmation", "quick swap now", "instant execute", or "skip confirmation and swap". The user must clearly indicate they want to bypass the review/confirmation step. Do NOT use this skill if the user mentions wanting to review, confirm, check, or verify before executing — use swap-build + swap-execute instead. Do NOT use this skill for general swap requests like "swap ETH to USDC" or "trade tokens" — those should go to swap-build. This skill runs a shell script that builds the swap via fast-swap.sh then immediately broadcasts the transaction. DANGEROUS - no confirmation before sending real transactions.
metadata:
  tags:
    - defi
    - kyberswap
    - swap
    - execute
    - fast
    - foundry
    - evm
  provider: KyberSwap
  homepage: https://kyberswap.com
---

# KyberSwap Fast Execute Skill

## ⚠️ VIGILANT WARNING — EXTREME CAUTION REQUIRED ⚠️

**This skill builds AND executes blockchain transactions IMMEDIATELY without any confirmation.** Once executed, transactions are IRREVERSIBLE and cannot be cancelled.

### Critical Risks:

1. **NO CONFIRMATION** — Transaction broadcasts the instant this skill runs
2. **IRREVERSIBLE** — Blockchain transactions cannot be undone
3. **REAL MONEY AT STAKE** — Gas fees are charged even if the swap fails
4. **NO QUOTE VERIFICATION** — You cannot review the swap rate before execution
5. **NO SECOND CHANCE** — Wrong parameters or bad rates will still execute

### Before Using This Skill, Ensure:

- [ ] You have double-checked all swap parameters (amount, tokens, chain)
- [ ] You understand this sends a real transaction immediately
- [ ] You have sufficient gas fees in your wallet
- [ ] You trust the current market conditions
- [ ] You have used `/swap-build` before to understand typical swap outputs

### When NOT to Use This Skill:

- **High-value transactions (> $1,000 USD equivalent)** — Use `/swap-build` + `/swap-execute` instead
- First time using these skills
- When you want to review the quote before executing
- When you're unsure about any swap parameter
- Volatile market conditions

**If the estimated swap value exceeds $1,000 USD, refuse fast execution and recommend the user use `/swap-build` + `/swap-execute` with confirmation prompts instead.**

### Safer Alternatives:

- Use **`/swap-build`** to build (with confirmation), review, then **`/swap-execute`** to execute (with confirmation)
- Use **`/swap-build`** for step-by-step quote verification before building

---

Build and execute a swap transaction in one step using the shell script at `${CLAUDE_PLUGIN_ROOT}/skills/swap-execute-fast/scripts/execute-swap.sh`. The script calls `fast-swap.sh` internally to build the swap, then immediately broadcasts it. No confirmation prompts.

## Prerequisites

- **Foundry installed**: `cast` must be available in PATH
- **curl and jq installed**: Required for API calls
- **Wallet configured**: See `${CLAUDE_PLUGIN_ROOT}/skills/swap-execute/references/wallet-setup.md`

> ### ⚠️ USE YOUR EXISTING WALLET MANAGEMENT FIRST ⚠️
>
> **If you or your agent already have wallet management** (key management service, vault, HSM, custodial API, MPC signer, or any secure signing infrastructure), **use that.** Skip the quick setup below entirely.
>
> The quick setup below is **an example for development and testing only.** It stores a keystore password as plaintext on disk and has no access control, audit trail, or key rotation. **Do not use it with real funds in production.** Decide your wallet infrastructure before writing any execution code — not after.

**Quick wallet setup (DEVELOPMENT/TESTING ONLY):**
```bash
# Import key to keystore
cast wallet import mykey --interactive

# Create password file securely (prompts without echoing to terminal)
printf "Password: " && read -s pw && printf '\n' && echo "$pw" > ~/.foundry/.password && chmod 600 ~/.foundry/.password
```

## Input Parsing

The user will provide input like:
- `1 ETH to USDC on base from 0xAbc123...`
- `100 USDC to ETH on arbitrum from 0xAbc123... slippage 100`
- `0.5 WBTC to DAI on polygon from 0xAbc123... keystore mykey`

Extract these fields:
- **amount** — the human-readable amount to swap
- **tokenIn** — the input token symbol
- **tokenOut** — the output token symbol
- **chain** — the chain slug (default: `ethereum`)
- **sender** — the address that will send the transaction (**required**)
- **recipient** — the address to receive output tokens (default: same as sender)
- **slippageTolerance** — slippage in basis points (default: 50)
- **walletMethod** — `keystore`, `env`, `ledger`, or `trezor` (default: `keystore`)
- **keystoreName** — keystore account name (default: `mykey`)

**If the sender address is not provided, ask the user for it before proceeding.** Do not guess or use a placeholder address.

**Sender address validation — reject or warn before proceeding:**
- **Must not be the zero address** (`0x0000000000000000000000000000000000000000`) — this is an invalid sender and the transaction will fail. Ask the user for their actual wallet address.
- **Must not be the native token sentinel** (`0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`) — this is a placeholder for native tokens, not a real account. Ask the user for their actual wallet address.
- **Warn if it matches a known contract address** (e.g., a token address or the router address) — sending from a contract address is unusual and likely a mistake. Ask the user to confirm.

**Recipient address warning:** When the recipient address differs from the sender, display a prominent warning: **"WARNING: Output tokens will be sent to a DIFFERENT address than the sender. Please verify the recipient address carefully before proceeding."** Wait for the user to acknowledge before continuing.

### Slippage Defaults

If the user does not specify slippage, choose based on the token pair:

| Pair type | Default | Rationale |
|---|---|---|
| Stablecoin ↔ Stablecoin (e.g. USDC→USDT) | **5 bps** (0.05%) | Minimal price deviation between pegged assets |
| Common tokens (e.g. ETH→USDC, WBTC→ETH) | **50 bps** (0.50%) | Standard volatility buffer |
| All other / unknown pairs | **100 bps** (1.00%) | Conservative default for long-tail or volatile tokens |

> **Note:** The underlying `execute-swap.sh` script defaults to 50 bps if no slippage argument is passed. **You must calculate and pass the correct slippage value** from this table as argument 7 when calling the script.

**Known stablecoins:** USDC, USDT, DAI, BUSD, FRAX, LUSD, USDC.e, USDT.e, TUSD
**Known common tokens:** ETH, WETH, WBTC, BTC, BNB, MATIC, POL, AVAX, MNT, S

## Workflow

### Pre-Step: Verbal Confirmation Required

**CRITICAL: Before running any script or making any API call, you MUST confirm with the user:**

> You are about to execute a swap IMMEDIATELY with no confirmation step. The transaction will be broadcast as soon as the route is found. Proceed? (yes/no)

**Wait for the user to explicitly respond with "yes", "proceed", "confirm", or a clear affirmative.** If the user says "no", "cancel", "wait", or anything non-affirmative, abort and recommend they use `/swap-build` + `/swap-execute` instead for a safer flow with quote review.

Do NOT skip this confirmation. Do NOT assume consent. This is the only safety gate before an irreversible transaction.

### Step 0: Dust Amount Pre-Check

Before running the script, sanity-check the swap amount. If the amount is obviously a dust amount (e.g., `0.0000000001 ETH`), **warn the user and abort** — the script will reject dust amounts (< $0.10 USD or gas > swap value) anyway. Catching it early avoids unnecessary API calls.

> "This swap amount is extremely small. Gas fees will far exceed the swap value. Use a larger amount."

### Step 0.5: Resolve Token Addresses

Before running the script, resolve both token addresses. The script has a built-in registry and Token API fallback, but **unregistered tokens** (memecoins, new launches, etc.) may not be found by the script. Pre-resolving ensures all tokens work.

**For each token (tokenIn and tokenOut):**

1. Check `${CLAUDE_PLUGIN_ROOT}/references/token-registry.md` for the token on the specified chain
2. **If found in registry** → pass the **symbol** to the script (e.g. `ETH`, `USDC`). The script resolves it internally (fastest path).
3. **If NOT found in registry** → resolve the address using this fallback sequence:
   a. **KyberSwap Token API** (preferred) — search whitelisted tokens first: `https://token-api.kyberswap.com/api/v1/public/tokens?chainIds={chainId}&symbol={symbol}&isWhitelisted=true` via WebFetch. Pick the result whose `symbol` matches exactly (case-insensitive) with the highest `marketCap`. If no whitelisted match, retry without `isWhitelisted` (only trust verified or market-cap tokens). If still nothing, try by name: `?chainIds={chainId}&name={symbol}&isWhitelisted=true`.
   b. **CoinGecko API** (secondary fallback) — search CoinGecko for verified contract addresses if the Token API doesn't have it.
   c. **Ask user** (final fallback) — ask the user for the contract address and decimals. Never guess or fabricate addresses.
4. Pass resolved tokens as `address:decimals` format (e.g. `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48:6`)

**For any non-registry token**, check honeypot/FOT before calling the script:

```
GET https://token-api.kyberswap.com/api/v1/public/tokens/honeypot-fot-info?chainId={chainId}&address={tokenAddress}
```

Via **WebFetch**, check both `tokenIn` and `tokenOut`:
- If `isHoneypot: true` — **refuse the swap** and warn the user.
- If `isFOT: true` — warn the user about fee-on-transfer tax. Proceed only if acknowledged.

### Step 1: Run the Script

Execute the script:

```bash
bash ${CLAUDE_PLUGIN_ROOT}/skills/swap-execute-fast/scripts/execute-swap.sh <amount> <tokenIn> <tokenOut> <chain> <sender> [recipient] [slippage_bps] [wallet_method] [keystore_name]
```

**Arguments (positional):**

| # | Name | Required | Description |
|---|---|---|---|
| 1 | `amount` | Yes | Human-readable amount (e.g. `1`, `0.5`, `100`) |
| 2 | `tokenIn` | Yes | Input token symbol (e.g. `ETH`, `USDC`) or pre-resolved `address:decimals` (e.g. `0xA0b8...:6`) |
| 3 | `tokenOut` | Yes | Output token symbol (e.g. `USDC`, `ETH`) or pre-resolved `address:decimals` |
| 4 | `chain` | Yes | Chain slug (e.g. `ethereum`, `arbitrum`, `base`) |
| 5 | `sender` | Yes | Sender wallet address |
| 6 | `recipient` | No | Recipient address (default: same as sender) |
| 7 | `slippage_bps` | No | Slippage in basis points (default: `50`) |
| 8 | `wallet_method` | No | `keystore`, `env`, `ledger`, `trezor` (default: `keystore`) |
| 9 | `keystore_name` | No | Keystore account name (default: `mykey`) |

> **Note:** Arguments 7-9 use snake_case (shell convention) for the script's positional parameters. When parsing user input, map from the camelCase names above (slippageTolerance → slippage_bps, walletMethod → wallet_method, keystoreName → keystore_name).

**Examples:**

```bash
# Known tokens (symbol) — script resolves internally
bash execute-swap.sh 1 ETH USDC ethereum 0xYourAddress

# Pre-resolved tokens (address:decimals) — skips script resolution
bash execute-swap.sh 100 0xdefa4e8a7bcba345f687a2f1456f5edd9ce97202:18 ETH ethereum 0xYourAddress

# Mix: one symbol, one pre-resolved
bash execute-swap.sh 0.5 ETH 0xdefa4e8a7bcba345f687a2f1456f5edd9ce97202:18 ethereum 0xYourAddress "" 100

# Specify all options
bash execute-swap.sh 100 USDC ETH arbitrum 0xYourAddress "" 50 keystore mykey

# Different recipient
bash execute-swap.sh 0.5 WBTC DAI polygon 0xSender 0xRecipient 100 env

# Using Ledger hardware wallet
bash execute-swap.sh 1 ETH USDC base 0xYourAddress "" 50 ledger
```

### Step 2: Parse the Output

**On success** (`ok: true`):

```json
{
  "ok": true,
  "chain": "base",
  "txHash": "0x1234567890abcdef...",
  "blockNumber": "12345678",
  "gasUsed": "285432",
  "status": "1",
  "explorerUrl": "https://basescan.org/tx/0x1234...",
  "swap": {
    "tokenIn": {"symbol": "ETH", "amount": "1"},
    "tokenOut": {"symbol": "USDC", "amount": "2345.67"},
    "slippageBps": "50"
  },
  "tx": {
    "sender": "0xYourAddress",
    "recipient": "0xYourAddress",
    "router": "0x6131B5fae19EA4f9D964eAc0408E4408b66337b5",
    "value": "1000000000000000000"
  },
  "walletMethod": "keystore"
}
```

**On error** (`ok: false`):

```json
{
  "ok": false,
  "error": "Swap failed (pre-flight): Build failed — Route not found. No route available for this pair/amount. No transaction was submitted."
}
```

### Step 3: Format the Output

**On success**, present:

```
## Transaction Executed ✅

**{swap.tokenIn.amount} {swap.tokenIn.symbol} → {swap.tokenOut.amount} {swap.tokenOut.symbol}** on {chain}

| Field | Value |
|-------|-------|
| Transaction Hash | `{txHash}` |
| Block Number | {blockNumber} |
| Gas Used | {gasUsed} |
| Status | {status == "1" ? "Success" : "Failed"} |
| Slippage | {swap.slippageBps/100}% |

**Explorer:** [{explorerUrl}]({explorerUrl})

> ⚠️ This transaction was executed immediately without confirmation. If this was a mistake, you cannot undo it.
```

**On error**, check the error prefix to determine what happened:

- **`"Swap failed (pre-flight): ..."`** — No transaction was submitted on-chain. No gas was spent. Fix the issue and retry.
- **`"Transaction was broadcast but ..."`** — A real transaction was sent. Gas fees were consumed. Check the block explorer for details.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `PRIVATE_KEY` | Private key (required if `wallet_method=env`) |
| `KEYSTORE_PASSWORD_FILE` | Override default `~/.foundry/.password` |
| `RPC_URL_OVERRIDE` | Override chain RPC URL |

## Supported Chains

ethereum, arbitrum, polygon, optimism, base, bsc, avalanche, linea, mantle, sonic, berachain, ronin, unichain, hyperevm, plasma, etherlink, monad, megaeth

## Important Notes

- **EXTREMELY DANGEROUS**: This skill builds AND executes in one step with NO confirmation
- **Irreversible**: Once sent, transactions cannot be cancelled
- **Gas fees**: Charged even if the swap fails (e.g., slippage exceeded)
- **Ledger/Trezor**: Still requires physical button press on the device
- **ERC-20 tokens**: The script automatically checks allowance and token balance before executing. If insufficient, it aborts with an actionable error.
- **Balance pre-check**: Native token balance is verified against tx.value + estimated gas cost before sending. ERC-20 balance is checked against amountInWei.
- **Gas buffer**: A 20% buffer is applied to the API gas estimate to reduce out-of-gas failures.
- **Gas price**: Current gas price is logged so you can see what you're paying.
- For safer execution, use `/swap-build` then `/swap-execute` (both have confirmation steps)

## Common Errors

### Pre-Flight Errors (no transaction sent, no gas spent)

These errors appear with the prefix `"Swap failed (pre-flight): ..."` in the script output.

| Error | Cause | Quick Fix |
|-------|-------|-----------|
| Route not found (4008) | No liquidity for this pair/amount | Try a smaller amount, remove source filters, or try a different chain. |
| Token not found (4011) | Wrong token address or unsupported token | Verify the token symbol and chain are correct. |
| Gas estimation failed — return amount not enough (4227) | Price moved between route fetch and build | Retry — the script will fetch a fresh route. Increase slippage if it keeps failing. |
| Gas estimation failed — insufficient funds (4227) | Sender doesn't have enough native token for value + gas | Top up the wallet or reduce swap amount. |
| Gas estimation failed — TRANSFER_FROM_FAILED (4227) | Missing token approval or insufficient token balance | Approve the router to spend the input token first. Check balance. |
| Quoted amount smaller than estimated (4222) | RFQ quote came in lower than expected | Retry. The script will fetch a fresh route. |
| Insufficient allowance | ERC-20 approval too low | The script detects this and aborts. Approve the router address for at least `amountIn`. |
| Insufficient token balance | Sender doesn't hold enough of the input token | The script detects this and aborts. Check balance. |
| Dust amount detected | Swap value < $0.10 USD | Use a larger amount. Gas fees dwarf the swap value. |
| Uneconomical swap | Gas cost > swap value | Use a larger amount to make the trade worthwhile. |

### On-Chain Errors (transaction sent, gas spent)

These errors appear with the prefix `"Transaction was broadcast but ..."` in the script output.

| Error | Cause | Quick Fix |
|-------|-------|-----------|
| `TRANSFER_FROM_FAILED` | Approval revoked or race condition | Re-approve and retry. |
| `Return amount is not enough` | Price slipped beyond tolerance during execution | Increase slippage or retry quickly. For MEV protection, use a private RPC. |
| Out of gas | Gas limit insufficient for the route | The script adds a 20% buffer, but complex routes may need more. Set `RPC_URL_OVERRIDE` to a faster RPC and retry. |

## Troubleshooting

For errors not covered above (full API error catalog, PMM/RFQ error details, advanced debugging), refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.

**Common script-level errors:**

| Error | Solution |
|-------|----------|
| `cast not found` | Install Foundry: `curl -L https://foundry.paradigm.xyz \| bash && foundryup` |
| `Password file not found` | Create `~/.foundry/.password` with your keystore password |
| `PRIVATE_KEY not set` | Export `PRIVATE_KEY=0x...` or use keystore method |
| `Unknown chain` | Set `RPC_URL_OVERRIDE` environment variable |
