---
name: nova-wallet
description: Safely operate the nova CLI wallet for authentication, balance checks, sending funds, withdrawals, and key management across mainnet and testnet. Enforces deterministic JSON/TOON parsing, exit code validation, financial confirmations, network verification, and strict secret-handling rules. Use when performing nova wallet automation, stablecoin transfers, claim links, exports, or any blockchain transaction via the nova CLI.
compatibility: Requires nodejs 24 and access to the internet
metadata:
  homepage: https://github.com/MynthAI/nova
  package: https://www.npmjs.com/package/@mynthai/nova
---

- If `nova` is not installed, install with:

  ``` bash
  npm install @mynthai/nova
  ```

Or run without installing via npx (replace all `nova` usage with
`npx @mynthai/nova`)

## Deterministic Parsing (MUST)

- Use structured output: `-j/--json` or `-t/--toon` (never parse human
  output).

- Always evaluate BOTH:

  - Process exit code (`0` success, `1` error)
  - Structured `status` (`ok` or `error`)

- On error: read `error.message` and `error.exitCode` (if present).

## Safety / Financial Safeguards (MUST)

- Before **any** financial action (`send`, `withdraw`):

  - Confirm current network via `nova config get network`.
  - Confirm intended network with user (mainnet vs testnet).
  - Confirm amount and destination/address (and blockchain for
    withdraw).

- `send` is **non-idempotent**:

  - Never retry `nova send` blindly.
  - If outcome is uncertain, verify via `nova -t balance` (safe).

- Treat `claimUrl` as a **secret credential**:

  - Never paste into shared chats/tickets/docs or persistent logs.

- Key material is **secret**:

  - Never log/export keys or phrases into shared/persistent contexts.
  - Warn user before `export` operations.

## Wallet Types

- Email wallet: created via `nova login` (email + verification code).

- Private-key wallet (default if not logged in): auto-created; user must
  back up:

  - `nova export key`
  - `nova export phrase`

## Networks

- `nova` operates on `mainnet` or `testnet`.
- Fresh install default: `testnet`.
- Network setting persists; funds/addresses/balances are isolated per
  network.

Commands:

``` bash
nova config get network
nova config set network <mainnet|testnet>
```

## Exit Codes

- `0` = success (still parse `status`).
- `1` = error (inspect `error.message`).

## Output Modes (for agents)

- JSON: `-j`, `--json`
- TOON: `-t`, `--toon`

## Commands (syntax preserved)

### Auth

Request login code:

``` bash
nova login request <email>
```

Confirm code:

``` bash
nova login confirm <code>
```

Options:

- `-j`, `--json`
- `-t`, `--toon`
- `-f`, `--force` (request only): overwrites existing private-key
  wallet; warn user.

### Account

Address:

``` bash
nova address [blockchain]
```

- Default blockchain: `mynth`

- Supported blockchains:

  - `base`
  - `cardano`
  - `hyperliquid`
  - `mynth`
  - `plasma`
  - `solana`
  - `stable`
  - `sui`
  - `tron`

Balance:

``` bash
nova balance
```

Notes:

- `balance` is USD-denominated.
- `currency` is always USD.

### Send (FINAL ACTION)

``` bash
nova send <amount> [destination]
```

Options:

- `-d`, `--dry-run` — Validate and preview without submitting

Behavior:

- If `destination` omitted:

  - Creates claim link (`claimUrl`)
  - Funds leave wallet immediately.

- If `destination` provided:

  - Sends directly.

  - `destination` may be:

    - An email address (creates or targets an email wallet).
    - A nova wallet address.
    - A supported external blockchain wallet address
      (network-dependent).

Rules:

- No interactive confirmation.
- Non-idempotent: re-running sends again.
- Use `--dry-run` (`-d`) to validate inputs and preview without
  submitting.
- Always confirm with user whether `destination` is an email address or
  wallet address before execution.

Post-check:

- Parse `status` and confirm `result.sent: true`.
- Surface `result.txId` when present.
- If `claimUrl` present, treat as secret.

Success example (TOON):

``` bash
status: ok
result:
  sent: true
  amount: "1"
  txId: d32c966fd4302673455eb790b66e3efc331ef7aace412c73b8917ba0bb37ace8
  claimUrl: "https://preview.mynth.ai/c/mto3M1JEa6Hr0UFRCBGjOg"
```

### Claim Links

Properties (when `nova send <amount>` has no destination):

- One-time use.
- Do not expire.
- Revocation: creator must claim it themselves (redeem back to own
  wallet).

### Withdraw (FINAL ACTION)

``` bash
nova withdraw <amount> <stablecoin> <address> <blockchain>
```

Options:

- `-d`, `--dry-run` — Validate and preview without submitting

Rules:

- Confirm:

  - Sufficient balance
  - Network
  - Stablecoin support
  - Address + blockchain compatibility

- Parse `status`.

- Surface `result.txId` when present.

Verification (safe):

``` bash
nova -t balance
```

#### Stablecoin Support

**Mainnet:**

- `base`: USDC
- `cardano`: USDC, USDA, USDM
- `hyperliquid`: USDC
- `solana`: USDC, USDT
- `stable`: USDT
- `sui`: USDC
- `tron`: USDT

**Testnet:**

- `base`: USDC
- `cardano`: USDC, USDA, USDM
- `hyperliquid`: USDC
- `solana`: USDC
- `stable`: USDT
- `sui`: USDT
- `tron`: USDT

## Fees

- Internal transfers / claim links: fee-free; recipient gets full
  amount.

- Direct sends to email or nova wallet addresses: fee-free; recipient
  gets full amount.

- External withdrawals:

  - May incur chain fees.
  - Fees are calculated at execution.
  - Fees are deducted from withdrawal amount (not separate).

## Rate Limits

If rate-limited, structured output indicates an error and includes a
message like: “Rate limited. Try again in N seconds”.

Rules:

- Do not retry immediately; respect the wait time.
- Never retry `send` blindly after a rate-limit error.
- If unsure whether `send` executed, verify via `nova -t balance`.

Error example (TOON, insufficient balance):

``` bash
status: error
error:
  message: 3tkv5qrm43jtjf86x3ks5l6jpjgpyw7n8424pm must have at least balance of 1000000
  exitCode: 1
```

## Key Management (security-critical)

Export:

``` bash
nova export key
nova export phrase
```

Import:

``` bash
nova import key
nova import phrase
```

Rules:

- Warn user: exporting reveals secrets.
- Never store or share exported key/phrase.
