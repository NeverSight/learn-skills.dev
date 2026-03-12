---
name: aster-deposit-fund
description: Deposit funds to Aster from a wallet; private key from env. Use when the user wants to deposit to Aster or fund an Aster account.
---

# Aster Deposit Fund

**Base URL:** `https://www.asterdex.com/bapi/futures/v1/public/future/`. Public endpoints; no auth.

## Env

| Var | Required | Description |
|-----|----------|-------------|
| `ASTER_DEPOSIT_PRIVATE_KEY` | Yes (deposit) | Wallet private key (0x + 64 hex). Used to sign on-chain deposit txs. Never log or echo. |
| `ASTER_WALLET_ADDRESS` | Yes (balance) | Public wallet address. Used by `balance.mjs` for read-only queries. |
| `ETH_RPC_URL` | Recommended | Private Ethereum RPC (Alchemy, Infura). Public fallback used if unset. |
| `BSC_RPC_URL` | Recommended | Private BSC RPC. |
| `ARBITRUM_RPC_URL` | Recommended | Private Arbitrum RPC. |

## Supported chains

| Chain | chainId |
|-------|---------|
| ETH (Ethereum) | 1 |
| BSC | 56 |
| Arbitrum | 42161 |

## User confirmation

**MANDATORY** — Before executing ANY deposit transaction, the agent MUST:

1. Display a clear summary to the user:
   - Chain and chainId
   - Asset symbol and contract address (for ERC20)
   - Amount (human-readable AND raw wei/units)
   - Deposit (treasury) address
   - Broker ID (if non-default)
   - Estimated gas cost
2. Ask for **explicit textual confirmation** (e.g. "Type 'confirm' to proceed" or "yes/no").
3. **Do NOT** assume consent from a prior message, implicit agreement, or context.
4. **Do NOT** batch multiple deposits without individual confirmation for each.
5. If the user cancels or does not confirm, abort immediately with no on-chain action.

Failure to confirm is a critical safety violation in an autonomous agent context.

## Flow

1. **Supported assets** — GET `aster/withdraw/assets?chainIds=<chainId>&networks=EVM&accountType=perp`. Response `data[]`: name, contractAddress, decimals, isNative, chainId. Use to pick asset and token contract for ERC20.
2. **Deposit address** — GET `web3/ae/deposit-address?chainId=<chainId>`. Response `data` = deposit address (string). Same address for native and ERC20 on that chain. **The address is validated against a hardcoded whitelist in `common.mjs` (SEC-01).**
3. **Balance check** — Verify the wallet has sufficient balance for the deposit amount + gas BEFORE submitting any transaction (SEC-06).
4. **User confirmation** — See above. Always confirm before executing.
5. **On-chain send** — From wallet (key from env), sign with appropriate RPC for chain:
   - **Native:** `treasury.depositNative(broker)` with `value = amount` (wei).
   - **ERC20:** `token.approve(treasury, amount)` then `treasury.deposit(token, amount, broker)`.
   - All transactions use an explicit gas limit (SEC-09) and wait for multiple confirmations per chain (SEC-10).

## Security

- Private key only from env; never log, echo, or pass via CLI args.
- Key is validated (0x + 64 hex chars) and removed from `process.env` after account derivation (SEC-02).
- Error output is sanitized to prevent accidental key leakage in logs (SEC-02).
- Deposit address is checked against a hardcoded whitelist to prevent oracle attacks (SEC-01).
- Public RPCs emit a warning; use private RPCs (Alchemy, Infura) in production (SEC-04).
- `balance.mjs` never loads the private key; it uses the public address only (SEC-07).

## Broker ID

The `--broker` parameter (default: `1`) identifies the Aster broker account that the deposit is attributed to. Broker `1` is the primary/default Aster broker. Only change this if you know the target broker ID. An incorrect broker ID may result in funds being inaccessible from the expected account (SEC-11).

## Scripts (viem)

Optional: `scripts/` — Bun + viem. Install: `cd skills/aster-deposit-fund/scripts && bun install`.

| Script | Purpose |
|--------|---------|
| `deposit.mjs` | Deposit: `ASTER_DEPOSIT_PRIVATE_KEY=0x... bun run deposit.mjs --chain <eth\|bsc\|arbitrum> --asset <SYMBOL> --amount <amount> [--broker <id>] [--dry-run]` |
| `balance.mjs` | Wallet balances (read-only): `bun run balance.mjs --chain <eth\|bsc\|arbitrum> --address <0x...>` |

See `.env.example` in the repo root for all env vars.

Payload shapes: [reference.md](reference.md).
