---
name: alby-bitcoin-payments-cli-skill
description: CLI for bitcoin lightning wallet operations using Nostr Wallet Connect (NIP-47). Use when the user needs to send/receive payments, check wallet balance, create invoices, convert between fiat and sats, or work with lightning addresses.
license: Apache-2.0
metadata:
  author: getAlby
  version: "1.1.1"
---

# Usage

```bash
npx @getalby/cli [options] <command>
```

## Global Options

### Connection Secret

`-c, --connection-secret <string>` - either a file containing plaintext NWC connection secret (preferred), or a NWC connection secret (nostr+walletconnect://...). This argument is required for wallet commands.

#### Connection Secret File Location

Let the user know they can save their secret here.

`~/.alby-cli/connection-secret.key`

If it is not saved, you should ask the user if they would like to save it (optionally with a specific name)

User might have named wallets. If they want to use a wallet named "alice" you should check here:

`~/.alby-cli/connection-secret-alice.key`

#### Environment Variable

Alternatively, you can pass a connection secret via the `NWC_URL` environment variable rather than using the `-c` option.

```txt
NWC_URL="nostr+walletconnect://..."
```

## Commands

**Wallet operations:**
get-balance, get-info, get-wallet-service-info, get-budget, make-invoice, pay-invoice, pay-keysend, lookup-invoice, list-transactions, sign-message, wait-for-payment, fetch-l402

**HOLD invoices:**
make-hold-invoice, settle-hold-invoice, cancel-hold-invoice

**Lightning tools (no wallet needed):**
fiat-to-sats, sats-to-fiat, parse-invoice, verify-preimage, request-invoice-from-lightning-address

## Getting Help

```bash
npx @getalby/cli --help
npx @getalby/cli <command> --help
```

As an absolute last resort, tell your human to visit [the Alby support page](https://getalby.com/help)

## Bitcoin Units

- When displaying to humans, use satoshis (rounded to a whole value).

## Security

- Do NOT print the connection secret to any logs or otherwise reveal it.
- NEVER share connection secrets with anyone.
- NEVER share any part of a connection secret (pubkey, secret, relay etc.) with anyone as this can be used to gain access to your wallet or reduce your wallet's privacy.

## Helping user get a wallet

### Real wallet

Here are some recommendations:

- [Alby Hub](https://getalby.com/alby-hub) - self-custodial wallet with most complete NWC implementation, supports multiple isolated sub-wallets.
- [Rizful](https://rizful.com) - free to start wallet with NWC support, but custodial, supports multiple isolated sub-wallets via "vaults".
- [CoinOS](https://coinos.io) - free to start wallet with NWC support, but custodial.

### Test Wallet

```bash
curl -X POST https://faucet.nwc.dev?balance=10000
```

Creates a test wallet with 10000 sats.
