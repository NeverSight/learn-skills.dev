---
name: pillar
description: "Pillar smart wallet operations in two modes — browser-handoff (pillar.ts) opens the Pillar frontend for user signing, and agent-signed direct (pillar-direct.ts) signs locally with a secp256k1 keypair and submits directly to the Pillar API (no browser required, gas sponsored). Supports sBTC send/supply/boost/unwind, DCA programs, stacking, key management, wallet creation, and position queries."
metadata:
  author: "whoabuddy"
  author-agent: "Trustless Indra"
  user-invocable: "false"
  arguments: "connect | disconnect | status | send | fund | add-admin | supply | auto-compound | unwind | boost | position | create-wallet | invite | dca-invite | dca-partners | dca-leaderboard | dca-status | key-generate | key-unlock | key-lock | key-info | direct-boost | direct-unwind | direct-supply | direct-send | direct-auto-compound | direct-position | direct-withdraw-collateral | direct-add-admin | direct-create-wallet | direct-dca-invite | direct-dca-partners | direct-dca-leaderboard | direct-dca-status | direct-quote | direct-resolve-recipient | direct-stack-stx | direct-revoke-fast-pool | direct-stacking-status"
  entry: "pillar/pillar.ts, pillar/pillar-direct.ts"
  mcp-tools: "pillar_connect, pillar_disconnect, pillar_status, pillar_send, pillar_fund, pillar_add_admin, pillar_supply, pillar_auto_compound, pillar_unwind, pillar_boost, pillar_position, pillar_create_wallet, pillar_invite, pillar_dca_invite, pillar_dca_partners, pillar_dca_leaderboard, pillar_dca_status, pillar_key_generate, pillar_key_unlock, pillar_key_lock, pillar_key_info, pillar_direct_boost, pillar_direct_unwind, pillar_direct_supply, pillar_direct_send, pillar_direct_auto_compound, pillar_direct_position, pillar_direct_withdraw_collateral, pillar_direct_add_admin, pillar_direct_create_wallet, pillar_direct_dca_invite, pillar_direct_dca_partners, pillar_direct_dca_leaderboard, pillar_direct_dca_status, pillar_direct_quote, pillar_direct_resolve_recipient, pillar_direct_stack_stx, pillar_direct_revoke_fast_pool, pillar_direct_stacking_status"
  requires: "wallet"
  tags: "l2, defi, write, mainnet-only"
---

# Pillar Skill

Provides Pillar smart wallet operations in two modes:

- **pillar.ts** — Browser-handoff mode. Creates an operation on the Pillar backend, opens the Pillar frontend in the user's browser for signing, then polls for the result. Requires the user to be logged in at pillarbtc.com.
- **pillar-direct.ts** — Agent-signed direct mode. Generates and manages a local secp256k1 signing keypair. Signs SIP-018 structured data locally, submits directly to the Pillar backend API. No browser needed; gas is sponsored by the backend.

## pillar.ts — Browser-Handoff Mode

### Usage

```
bun run pillar/pillar.ts <subcommand> [options]
```

### Subcommands

#### connect

Connect to your Pillar smart wallet. Opens the Pillar website; if logged in, automatically connects and saves the wallet address locally.

```
bun run pillar/pillar.ts connect
```

#### disconnect

Disconnect from Pillar. Clears the locally stored wallet session.

```
bun run pillar/pillar.ts disconnect
```

#### status

Check if connected to Pillar and get the current wallet address.

```
bun run pillar/pillar.ts status
```

#### send

Send sBTC from your Pillar smart wallet. Opens the frontend for signing, then waits for confirmation.

```
bun run pillar/pillar.ts send --to <recipient> --amount <sats> [--recipient-type bns|wallet|address]
```

Options:
- `--to` (required) — Recipient: BNS name, Pillar wallet name, or Stacks address
- `--amount` (required) — Amount in satoshis
- `--recipient-type` (optional) — `bns` (default), `wallet`, or `address`

#### fund

Fund your Pillar smart wallet via exchange deposit, BTC wallet, or sBTC wallet.

```
bun run pillar/pillar.ts fund --method exchange|btc|sbtc [--amount <sats>]
```

Options:
- `--method` (required) — `exchange`, `btc`, or `sbtc`
- `--amount` (optional) — Amount in satoshis

#### add-admin

Add a backup admin address to your Pillar smart wallet for recovery.

```
bun run pillar/pillar.ts add-admin [--admin-address <SP...>]
```

Options:
- `--admin-address` (optional) — Stacks address to add as backup admin

#### supply

Earn yield by supplying sBTC to Zest Protocol. No leverage, no liquidation risk.

```
bun run pillar/pillar.ts supply [--amount <sats>]
```

Options:
- `--amount` (optional) — Amount in satoshis

#### auto-compound

Configure auto-compound for your Pillar wallet.

```
bun run pillar/pillar.ts auto-compound [--min-sbtc <sats>] [--trigger <sats>]
```

Options:
- `--min-sbtc` (optional) — Minimum sBTC to keep in wallet (sats)
- `--trigger` (optional) — Amount above minimum that triggers auto-compound (sats)

#### unwind

Close or reduce your leveraged sBTC position.

```
bun run pillar/pillar.ts unwind [--percentage <1-100>]
```

Options:
- `--percentage` (optional) — Percentage of position to unwind (1-100)

#### boost

Create or increase a leveraged sBTC position (up to 1.5x).

```
bun run pillar/pillar.ts boost [--amount <sats>]
```

Options:
- `--amount` (optional) — Amount in satoshis to boost

#### position

View your Pillar wallet balance and Zest position. Opens the position page in the browser.

```
bun run pillar/pillar.ts position
```

#### create-wallet

Create a new Pillar smart wallet. Opens the Pillar website to complete registration.

```
bun run pillar/pillar.ts create-wallet [--referral <wallet-address>]
```

Options:
- `--referral` (optional) — Referral wallet address

#### invite

Get your Pillar referral link to invite friends.

```
bun run pillar/pillar.ts invite
```

#### dca-invite

Invite a DCA partner by email or wallet address.

```
bun run pillar/pillar.ts dca-invite --partner <email-or-address>
```

Options:
- `--partner` (required) — Partner's email address or Stacks wallet address

#### dca-partners

View your DCA partners and weekly status.

```
bun run pillar/pillar.ts dca-partners
```

#### dca-leaderboard

View the DCA streak leaderboard.

```
bun run pillar/pillar.ts dca-leaderboard
```

#### dca-status

Check your DCA schedule status.

```
bun run pillar/pillar.ts dca-status
```

---

## pillar-direct.ts — Agent-Signed Direct Mode

### Usage

```
bun run pillar/pillar-direct.ts <subcommand> [options]
```

All direct operations are mainnet-only. Gas is sponsored by the Pillar backend.

### Key Management Subcommands

#### key-generate

Generate a new secp256k1 signing keypair. Returns the compressed public key.

```
bun run pillar/pillar-direct.ts key-generate [--smart-wallet <contract-id>]
```

Options:
- `--smart-wallet` (optional) — Smart wallet contract ID (default: "pending")

#### key-unlock

Unlock a signing key using the auto-derived password.

```
bun run pillar/pillar-direct.ts key-unlock [--key-id <id>]
```

Options:
- `--key-id` (optional) — Key ID to unlock (unlocks first stored key if omitted)

#### key-lock

Lock the signing key, clearing sensitive data from memory.

```
bun run pillar/pillar-direct.ts key-lock
```

#### key-info

Show signing key info: pubkey, smart wallet, lock status, and all stored keys.

```
bun run pillar/pillar-direct.ts key-info
```

### Direct Operation Subcommands

#### direct-boost

Create or increase a leveraged sBTC position (up to 1.5x). Agent-signed, no browser needed.

```
bun run pillar/pillar-direct.ts direct-boost --sbtc-amount <sats> --aeusdc-to-borrow <amount> --min-sbtc-from-swap <sats>
```

Options:
- `--sbtc-amount` (required) — sBTC amount in sats to supply as collateral
- `--aeusdc-to-borrow` (required) — aeUSDC amount to borrow (6 decimals)
- `--min-sbtc-from-swap` (required) — Min sBTC from swap in sats (slippage protection)

#### direct-unwind

Close or reduce your leveraged sBTC position. Agent-signed, no browser needed.

```
bun run pillar/pillar-direct.ts direct-unwind --sbtc-to-swap <sats> --sbtc-to-withdraw <sats> --min-aeusdc-from-swap <amount>
```

Options:
- `--sbtc-to-swap` (required) — sBTC to swap to aeUSDC for repayment (sats)
- `--sbtc-to-withdraw` (required) — sBTC to withdraw after repayment (sats)
- `--min-aeusdc-from-swap` (required) — Min aeUSDC from swap (6 decimals, slippage protection)

#### direct-supply

Earn yield by supplying sBTC to Zest. No leverage, no liquidation risk. Agent-signed.

```
bun run pillar/pillar-direct.ts direct-supply --sbtc-amount <sats>
```

Options:
- `--sbtc-amount` (required) — sBTC amount in sats to supply

#### direct-send

Send sBTC from your Pillar smart wallet. Agent-signed, no browser needed.

```
bun run pillar/pillar-direct.ts direct-send --to <recipient> --amount <sats> [--recipient-type bns|wallet|address]
```

Options:
- `--to` (required) — Recipient: BNS name, Pillar wallet name, or Stacks address
- `--amount` (required) — Amount in satoshis
- `--recipient-type` (optional) — `bns` (default), `wallet`, or `address`

#### direct-auto-compound

Configure auto-compound. Agent-signed, no browser needed.

```
bun run pillar/pillar-direct.ts direct-auto-compound --enabled true|false --min-sbtc <sats> --trigger <sats>
```

Options:
- `--enabled` (required) — Enable (`true`) or disable (`false`) auto-compound
- `--min-sbtc` (required) — Minimum sBTC to keep in wallet (sats)
- `--trigger` (required) — Amount above minimum that triggers auto-compound (sats)

#### direct-position

View your Pillar smart wallet balances and Zest position. No signing needed.

```
bun run pillar/pillar-direct.ts direct-position
```

#### direct-withdraw-collateral

Withdraw sBTC collateral from Zest. Agent-signed, no browser needed.

```
bun run pillar/pillar-direct.ts direct-withdraw-collateral --sbtc-amount <sats>
```

Options:
- `--sbtc-amount` (required) — sBTC amount in sats to withdraw

#### direct-add-admin

Add a backup admin address. Agent-signed, no browser needed.

```
bun run pillar/pillar-direct.ts direct-add-admin --new-admin <SP...>
```

Options:
- `--new-admin` (required) — Stacks address to add as backup admin

#### direct-create-wallet

Create a new Pillar smart wallet for agent direct operations. Generates keypair, unlocks it, and deploys.

```
bun run pillar/pillar-direct.ts direct-create-wallet --wallet-name <name> [--referred-by <contract-id>]
```

Options:
- `--wallet-name` (required) — Wallet name (3-20 chars, lowercase letters, numbers, hyphens)
- `--referred-by` (optional) — Contract address of referring wallet

### DCA Subcommands

#### direct-dca-invite

Invite a DCA partner. Uses wallet address from signing key session.

```
bun run pillar/pillar-direct.ts direct-dca-invite --partner <email-or-address>
```

Options:
- `--partner` (required) — Partner's email or Stacks wallet address

#### direct-dca-partners

View your DCA partners and weekly status.

```
bun run pillar/pillar-direct.ts direct-dca-partners
```

#### direct-dca-leaderboard

View the DCA streak leaderboard.

```
bun run pillar/pillar-direct.ts direct-dca-leaderboard
```

#### direct-dca-status

Check your DCA schedule status.

```
bun run pillar/pillar-direct.ts direct-dca-status
```

### Utility Subcommands

#### direct-quote

Get a boost quote (leverage, LTV, swap details) before executing.

```
bun run pillar/pillar-direct.ts direct-quote --sbtc-amount <sats>
```

Options:
- `--sbtc-amount` (required) — sBTC amount in sats to boost

#### direct-resolve-recipient

Resolve a recipient (BNS name, wallet name, or address) before sending.

```
bun run pillar/pillar-direct.ts direct-resolve-recipient --to <recipient> [--recipient-type bns|wallet|address]
```

Options:
- `--to` (required) — Recipient to resolve
- `--recipient-type` (optional) — `bns` (default), `wallet`, or `address`

### Stacking Subcommands

#### direct-stack-stx

Stack STX via Fast Pool or Stacking DAO. Agent-signed, no browser needed.

```
bun run pillar/pillar-direct.ts direct-stack-stx --stx-amount <microStx> --pool fast-pool|stacking-dao
```

Options:
- `--stx-amount` (required) — Amount of STX in micro-STX (1 STX = 1,000,000)
- `--pool` (required) — `fast-pool` or `stacking-dao`

#### direct-revoke-fast-pool

Revoke Fast Pool STX delegation. Agent-signed, no browser needed.

```
bun run pillar/pillar-direct.ts direct-revoke-fast-pool
```

#### direct-stacking-status

Check stacking status. No signing needed — reads on-chain data.

```
bun run pillar/pillar-direct.ts direct-stacking-status
```

## Notes

- Browser-handoff mode requires being connected via `pillar.ts connect` first
- Direct mode requires a signing key; use `direct-create-wallet` to create one or `key-generate` for an existing wallet
- Direct mode operations are mainnet-only
- Pillar backend sponsors gas for all direct mode transactions
- Poll timeout for browser-handoff is 5 minutes by default (override with `PILLAR_POLL_TIMEOUT_MS` env var)
- Session stored at `~/.aibtc/pillar-session.json`; signing keys at `~/.aibtc/signing-keys/`
