---
name: agent-wallet-cli
description: Manage crypto wallets (Ethereum & Solana) — create wallets, check balances, send tokens, sign messages. Supports gasless ERC-20 transfers via relay and x402 HTTP payments.
---

# agent-wallet-cli

A CLI wallet for Ethereum and Solana. All commands return JSON with `--format json`. Always check `"ok": true` before proceeding.

Always invoke via `npx` to ensure the CLI is available without requiring a global install:

```bash
npx agent-wallet-cli <command> [options]
```

## Create a Wallet

If no wallet exists yet, generate a strong random password and create a wallet:

```bash
npx agent-wallet-cli init --password "<generated-password>" --format json
```

After creating the wallet you MUST:
1. Store the password in a `.env` file (e.g. `WALLET_PASSWORD=...`) or another project-local secret store so you can use it for future `unlock` commands. Never hard-code it in source files.
2. Read the `mnemonic_file` from the response and present the mnemonic to the user.
3. Instruct the user to back up the mnemonic in a safe, offline location (e.g. written on paper, stored in a password manager).
4. Make clear that this mnemonic is the ONLY way to recover the wallet. It cannot be recovered by anyone — not by the CLI, not by any service, not by the developer. If it is lost, the funds are gone forever.
5. After the user confirms they have saved it, delete the mnemonic file.

Options: `--word-count 12` (default) or `--word-count 24` for a longer phrase.

## Unlock

The wallet must be unlocked before use. Unlock creates a time-limited session token:

```bash
npx agent-wallet-cli unlock --password "$WALLET_PASSWORD" --format json
```

Response:
```json
{ "ok": true, "token": "wlt_...", "expires_at": "..." }
```

Save the `token` value. Pass it to all subsequent commands with `--token <token>`, or set the environment variable:

```bash
export AGENT_WALLET_CLI_TOKEN="wlt_..."
```

## Check Balance

Native balance:
```bash
npx agent-wallet-cli balance --token <token> --chain ethereum --network mainnet --format json
```

ERC-20 / SPL token balance (use alias or contract address):
```bash
npx agent-wallet-cli balance --token <token> --chain ethereum --network base --token-address usdc --format json
```

## Send Funds

Native transfer:
```bash
npx agent-wallet-cli send --token <token> --chain ethereum --to <address> --amount <amount> --yes --format json
```

Token transfer:
```bash
npx agent-wallet-cli send --token <token> --chain ethereum --token-address usdc --to <address> --amount <amount> --yes --format json
```

Use `--dry-run` to simulate without sending. Always use `--dry-run` first when uncertain about amounts.

### Gasless Relay

Token transfers on EVM chains automatically use a gasless relay when the wallet has no native tokens (ETH/MATIC) for gas. The relay fee (e.g. 0.01 USDC) is deducted from the token amount. Check the response for:
- `"relay_used": true` — relay was used
- `"relay_fee"` — fee deducted
- `"amount_received"` — net amount sent after fee

To disable the relay for a specific transfer, add `--no-relay`.

## Show Addresses

Show all wallet addresses (Ethereum + Solana):
```bash
npx agent-wallet-cli address --token <token> --format json
```

Show a specific chain:
```bash
npx agent-wallet-cli address --token <token> --chain ethereum --format json
```

## Sign Messages

Plain text message:
```bash
npx agent-wallet-cli sign --token <token> --chain ethereum --message "Hello World" --format json
```

EIP-712 typed data (JSON string or file path with `@` prefix):
```bash
npx agent-wallet-cli sign --token <token> --chain ethereum --typed-data '{"types":...}' --format json
npx agent-wallet-cli sign --token <token> --chain ethereum --typed-data @typed-data.json --format json
```

Raw bytes (hex):
```bash
npx agent-wallet-cli sign --token <token> --chain ethereum --data 0xdeadbeef --format json
```

## ERC-20 Approve & Allowance

Approve a spender:
```bash
npx agent-wallet-cli approve --token <token> --chain ethereum --token-address usdc --spender <address> --amount <amount> --yes --format json
```

Check allowance (no session token needed):
```bash
npx agent-wallet-cli allowance --chain ethereum --token-address usdc --owner <address> --spender <address> --format json
```

Delegated transfer (transferFrom):
```bash
npx agent-wallet-cli transfer-from --token <token> --chain ethereum --token-address usdc --from <owner> --to <recipient> --amount <amount> --yes --format json
```

## x402 Payments (HTTP 402)

Make HTTP requests to x402-enabled endpoints with automatic stablecoin payment. When the server returns `402 Payment Required`, the wallet signs an EIP-3009 `TransferWithAuthorization` and retries the request with the payment header.

Preview payment requirements (no payment):
```bash
npx agent-wallet-cli x402 https://example.com/api/paid-resource --token <token> --dry-run --format json
```

Make a paid request (auto-confirm):
```bash
npx agent-wallet-cli x402 https://example.com/api/paid-resource --token <token> --yes --format json
```

With a maximum payment cap:
```bash
npx agent-wallet-cli x402 https://example.com/api/paid-resource --token <token> --yes --max-amount 0.10 --format json
```

POST request with custom headers and body:
```bash
npx agent-wallet-cli x402 https://example.com/api/paid-resource --token <token> --method POST --header "Content-Type:application/json" --body '{"query":"data"}' --yes --format json
```

Read body from a file:
```bash
npx agent-wallet-cli x402 https://example.com/api/paid-resource --token <token> --method POST --body @request.json --yes --format json
```

Options:
- `--method <method>` — HTTP method (default: GET)
- `--header <header...>` — HTTP headers in `Key:Value` format (repeatable)
- `--body <body>` — Request body (prefix with `@` to read from file)
- `--account-index <index>` — Account index (default: 0)
- `--dry-run` — Show payment requirements without paying
- `--yes` — Skip payment confirmation (required for non-interactive agent use)
- `--max-amount <amount>` — Maximum amount willing to pay in human-readable units (e.g. "0.10" for $0.10 USDC)

Response includes `"paid": true` with payment details and settlement info when a payment was made, or `"paid": false` if the endpoint did not require payment.

Always use `--dry-run` first to inspect payment requirements before committing to a payment. Use `--max-amount` as a safety cap to prevent overpaying.

## Lock

Always lock the wallet when done:
```bash
npx agent-wallet-cli lock --format json
```

## Token Aliases

Use short names instead of contract addresses:

| Alias | Ethereum | Base | Polygon | Arbitrum | Solana |
|-------|----------|------|---------|----------|--------|
| usdc  | yes      | yes  | yes     | yes      | yes    |
| usdt  | yes      | -    | yes     | yes      | yes    |
| dai   | yes      | -    | -       | -        | -      |
| weth  | yes      | -    | -       | -        | -      |
| wbtc  | yes      | -    | -       | -        | -      |

## Conventions

- Always use `--format json` and parse the JSON output.
- Always check `"ok": true` in the response before proceeding.
- Use `--yes` to skip interactive confirmation prompts (required for non-interactive agent use).
- Never send more than the user instructed. Always confirm amounts with the user first.
- Use `--dry-run` for send commands when uncertain about the amount or recipient.
- Use `--network` to specify the network (default: `mainnet`). Available: mainnet, sepolia, polygon, arbitrum, base, base-sepolia.
- Solana networks: mainnet, devnet.
