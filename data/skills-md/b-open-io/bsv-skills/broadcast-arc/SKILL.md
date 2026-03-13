---
name: broadcast-arc
description: This skill should be used when the user asks to "broadcast transaction", "submit to ARC", "broadcast via ARC", "broadcast BEEF", "broadcast EF", "use GorillaPool ARC", "use TAAL ARC", "arc.gorillapool.io", "arc.taal.com", "ArcConfig", "broadcastMany", or needs to submit a signed BSV transaction to the network using the ARC broadcaster from @bsv/sdk.
allowed-tools: "Bash(bun:*)"
disable-model-invocation: true
---

# ARC Transaction Broadcasting

Broadcast signed BSV transactions using the ARC (Application Runtime & Certificate) protocol via `@bsv/sdk`.

## ARC Overview

ARC is the production-grade transaction broadcaster for BSV. Unlike simple REST broadcast endpoints, ARC:
- Connects to multiple nodes simultaneously (no single point of failure)
- Accepts Extended Format (EF) transactions for script/fee validation
- Returns structured status responses with `txStatus`
- Supports callback webhooks for confirmation events
- Handles rebroadcast automatically

Two public ARC endpoints are available:

| Provider | URL | API Key Required |
|----------|-----|-----------------|
| **GorillaPool** | `https://arc.gorillapool.io` | No (mainnet, public beta) |
| **TAAL** | `https://api.taal.com/arc` | Yes — get from [console.taal.com](https://console.taal.com) |

GorillaPool is the default for development. Use TAAL for production if a guaranteed SLA is needed.

## Basic Usage

```typescript
import { Transaction, ARC } from '@bsv/sdk'

// GorillaPool — no API key needed
const result = await tx.broadcast(new ARC('https://arc.gorillapool.io'))

// TAAL — API key required
const result = await tx.broadcast(new ARC('https://api.taal.com/arc', 'mainnet_xxxxxx'))

// Check result
if (result.status === 'success') {
  console.log('txid:', result.txid)
  console.log('status:', result.message) // e.g. "SEEN_ON_NETWORK"
} else {
  console.error('broadcast failed:', result.description)
}
```

## ArcConfig Options

Use `ArcConfig` for advanced configuration:

```typescript
import { ARC, ArcConfig } from '@bsv/sdk'

const config: ArcConfig = {
  apiKey: 'mainnet_xxxxxx',          // Optional for GorillaPool
  callbackUrl: 'https://myapp.com/arc-callback',  // Webhook for confirmations
  callbackToken: 'my-secret-token',  // Sent as Authorization header in callbacks
  deploymentId: 'my-app-v1',         // Identifies your app in ARC logs
  headers: { 'X-Custom': 'value' },  // Extra headers on all requests
}

const broadcaster = new ARC('https://arc.gorillapool.io', config)
await tx.broadcast(broadcaster)
```

### Callback Webhook

When `callbackUrl` is set, ARC will POST to that URL when the transaction is:
- Seen in mempool (`SEEN_ON_NETWORK`)
- Mined in a block (`MINED`)
- Double-spent (`DOUBLE_SPEND_ATTEMPTED`)

The callback body contains `{ txid, txStatus, blockHash?, blockHeight? }`.

## Transaction Formats

The `ARC` broadcaster internally calls `tx.toHexEF()` (Extended Format). EF includes source transaction data so ARC can validate scripts and fees without looking up inputs separately.

If EF serialization fails (source transactions not attached), it falls back to raw hex.

```typescript
// Manually build with source tx attached (enables EF)
tx.addInput({
  sourceTXID: '...',
  sourceOutputIndex: 0,
  sourceTransaction: parentTx,  // Attaches parent → enables EF
  unlockingScriptTemplate: new P2PKH().unlock(key),
})
```

## Batch Broadcasting

Broadcast multiple transactions in one call:

```typescript
const broadcaster = new ARC('https://arc.gorillapool.io')
const results = await broadcaster.broadcastMany([tx1, tx2, tx3])

for (const r of results) {
  console.log(r)
}
```

`broadcastMany` posts to `/v1/txs` (vs `/v1/tx` for single). Results are mixed — some may succeed while others fail.

## Broadcasting a BEEF Transaction

When using `WalletClient` with `noSend: true`, the wallet returns a BEEF transaction. To broadcast it via ARC:

```typescript
import { Transaction, ARC } from '@bsv/sdk'

// Parse BEEF bytes from WalletClient
const tx = Transaction.fromBEEF(beefBytes)

// Or from hex BEEF string
const tx = Transaction.fromHexBEEF(beefHex)

// Broadcast
const result = await tx.broadcast(new ARC('https://arc.gorillapool.io'))
```

## Script Usage

```bash
# Broadcast a raw/EF tx hex
bun run skills/broadcast-arc/scripts/broadcast.ts <tx-hex>

# Broadcast BEEF hex
bun run skills/broadcast-arc/scripts/broadcast.ts --beef <beef-hex>

# Use TAAL with API key
bun run skills/broadcast-arc/scripts/broadcast.ts <tx-hex> --key mainnet_xxxxxx --url https://api.taal.com/arc
```

## Error Codes

| Code | Meaning |
|------|---------|
| `200` | Success — transaction accepted |
| `409` | Already known — txid exists (not an error) |
| `422` | Invalid transaction — script/fee error |
| `465` | Cumulative fee too low |
| `473` | Double spend detected |

A `409` response (already known) should be treated as success — the tx is already on the network.

## txStatus Values

| Status | Meaning |
|--------|---------|
| `STORED` | Received, not yet validated |
| `ANNOUNCED_TO_NETWORK` | Propagated to nodes |
| `SEEN_ON_NETWORK` | Seen by multiple nodes |
| `MINED` | Included in a block |
| `SEEN_IN_ORPHAN_MEMPOOL` | In an orphan branch |
| `DOUBLE_SPEND_ATTEMPTED` | Competing transaction detected |

## Related Skills

- `wallet-brc100` — create transactions with `WalletClient` including `noSend: true` BEEF pattern
- `wallet-send-bsv` — build and sign transactions with a WIF key before broadcasting
- `decode-bsv-transaction` — inspect a transaction before or after broadcast
