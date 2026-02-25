---
name: junglebus
description: This skill should be used when the user asks about "JungleBus", "transaction streaming", "BSV subscriptions", "real-time blockchain data", "GorillaPool API", or needs to subscribe to blockchain events.
---

# JungleBus

Real-time BSV blockchain data streaming from GorillaPool. Indexes all Bitcoin transactions with special handling for data protocols.

## When to Use

- Subscribe to transactions matching specific patterns
- Stream real-time mempool and block data
- Build indexers or notification systems
- Monitor addresses or script patterns
- Track 1Sat Ordinals, MAP, BAP, and other protocols

## Creating a Subscription

### Step-by-Step (Dashboard)

1. Visit https://junglebus.gorillapool.io
2. Sign in or create an account
3. Navigate: **Dashboard > Subscriptions > Create New**
4. Fill in subscription details:
   - **ID**: Auto-generated unique identifier
   - **Name**: Descriptive name for your subscription
   - **Description**: What this subscription monitors

### Subscription Filters

Define what transactions to capture using AND logic (all conditions must match):

| Filter | Description | Examples |
|--------|-------------|----------|
| **Addresses** | Comma-separated Bitcoin addresses | `1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa` |
| **Input types** | Input script types | `ordlock`, `sigil` |
| **Output types** | Output classifications | `aip`, `bap`, `bitcom`, `map`, `ord`, `run`, `token_stas`, `pubkeyhash`, `nulldata` |
| **Contexts** | Main data from OP_RETURN outputs | Protocol-specific identifiers |
| **Sub contexts** | Secondary data from outputs | Depends on output type |
| **Data keys** | Key=value pairs from transactions | `app=junglebus`, `type=post` |

**Note**: Multiple values in a single field use AND logic - all must be present in the transaction.

### Common Subscription Patterns

**Monitor 1Sat Ordinals:**
- Output types: `ord`
- Contexts: `image/png`, `text/plain` (content types)

**Monitor BAP Identity:**
- Output types: `bap`
- Contexts: `1BAPSuaPnfGnSBM3GLV9yhxUdYe4vGbdMT` (BAP address)

**Monitor MAP Protocol:**
- Output types: `map`
- Contexts: `1PuQa7K62MiKCtssSLKy1kh56WWU7MtUR5` (MAP prefix)

**Monitor Specific Address:**
- Addresses: `1YourAddressHere`

## JavaScript Client

### Installation

```bash
npm install @gorillapool/js-junglebus
```

### Basic Usage

```typescript
import { JungleBusClient, ControlMessageStatusCode } from '@gorillapool/js-junglebus';

const client = new JungleBusClient("junglebus.gorillapool.io", {
  useSSL: true,
  onConnected(ctx) { 
    console.log("Connected", ctx); 
  },
  onConnecting(ctx) { 
    console.log("Connecting", ctx); 
  },
  onDisconnected(ctx) { 
    console.log("Disconnected", ctx); 
  },
  onError(ctx) { 
    console.error("Error", ctx); 
  }
});

// Subscribe to a subscription ID
const subscriptionId = "your-subscription-id";
const fromBlock = 750000;

client.Subscribe(
  subscriptionId,
  fromBlock,
  (tx) => {
    // Confirmed transaction received
    console.log("TX:", tx.id, "at height", tx.block_height);
    console.log("Output types:", tx.output_types);
    console.log("Contexts:", tx.contexts);
  },
  (status) => {
    // Status updates
    if (status.statusCode === ControlMessageStatusCode.BLOCK_DONE) {
      console.log("Block done:", status.block);
    } else if (status.statusCode === ControlMessageStatusCode.WAITING) {
      console.log("Waiting for new block...");
    } else if (status.statusCode === ControlMessageStatusCode.REORG) {
      console.log("Reorg triggered:", status);
    }
  },
  (error) => {
    // Subscription errors
    console.error("Subscription error:", error);
  },
  (mempoolTx) => {
    // Unconfirmed mempool transaction
    console.log("Mempool TX:", mempoolTx.id);
  }
);
```

### Lite Mode (Lower Bandwidth)

```typescript
// Last parameter = true for lite mode
client.Subscribe(
  subscriptionId, 
  fromBlock, 
  onTx, 
  onStatus, 
  onError, 
  onMempool, 
  true // Lite mode - only txid and block height
);
```

## Transaction Data Format

### Full Transaction Object

```json
{
  "id": "e597af34eb78b599b7d458110a3cc602a40dedd020db684992b40926217612a4",
  "block_hash": "000000000000000006296f1e5437dd6c01b9b5471691a89a9c7d8e9f06920da5",
  "block_height": 750000,
  "block_time": 1658878267,
  "block_index": 3,
  "transaction": "0100000002...",
  "merkle_proof": "AAOkEnYhJgm0kklo2yDQ7Q2kAsY8ChFY1LeZtXjrNK+X...",
  "addresses": [
    "18FJd9tDLAC2S6PCzfnqNfUMXhZuPfsFUm",
    "1P7UWRLdL5pH2Si1GauwASYAA1LQHs2z45"
  ],
  "inputs": [],
  "outputs": [
    "76a9144f7d6a485e09770f947c0ba38d15050a5a80b6fa88ac",
    "76a914f28c3992dd6a43eccaed16f3f7fb6ac8da1bc3c288ac"
  ],
  "input_types": [],
  "output_types": ["nulldata", "pubkeyhash", "run"],
  "contexts": [
    "555aad1953bcfef8c7779d246fa03efae0412ed700b955435831814f5be3a82b_o1",
    "c2c4c971e85b499c29a8ab2148fd324fe12b550b8f4f57658a4686e011d8fd58_o1"
  ],
  "sub_contexts": [
    "2e729d39a9cd300f5100044a54204e6d8b43fe49555309361fdc3d8565323499"
  ],
  "data": []
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Transaction ID (txid) |
| `block_hash` | string | Block hash where transaction was mined |
| `block_height` | number | Block height |
| `block_time` | number | Unix timestamp |
| `block_index` | number | Position of transaction in block |
| `transaction` | string | Full transaction in hex |
| `merkle_proof` | string | TSC-compatible binary merkle proof |
| `addresses` | string[] | All addresses found in transaction |
| `outputs` | string[] | Output scripts (capped to 1024 chars) |
| `output_types` | string[] | Classifications (aip, bap, map, ord, etc.) |
| `contexts` | string[] | Main data from OP_RETURN outputs |
| `sub_contexts` | string[] | Secondary data from outputs |
| `data` | string[] | Other key=value attributes |

## Supported Protocols

JungleBus automatically recognizes and indexes these protocols:

| Protocol | Output Type | Context | Description |
|----------|-------------|---------|-------------|
| **1Sat Outputs** | `1sat` | none | 1 satoshi outputs |
| **1Sat Ordinals** | `ord` | content-type | Inscriptions with content type |
| **AIP** | `aip` | protocol data | Bitcoin Attestation Protocol |
| **B Protocol** | `b` | protocol data | B:// file storage |
| **BAP** | `bap` | `1BAPSuaPnfGnSBM3GLV9yhxUdYe4vGbdMT` | BAP identity |
| **Bitcom** | `bitcom` | protocol data | Bitcom protocol |
| **Boost** | `boost` | protocol data | Boost POW |
| **MAP** | `map` | `1PuQa7K62MiKCtssSLKy1kh56WWU7MtUR5` | MAP protocol |
| **Run** | `run` | protocol data | Run tokens |
| **STAS** | `token_stas` | protocol data | STAS tokens |

## REST API Endpoints

### Get Transaction

```bash
curl https://junglebus.gorillapool.io/v1/transaction/get/{txid}
```

Returns full transaction with parsed data.

### Get Address History

```bash
curl https://junglebus.gorillapool.io/v1/address/get/{address}
```

Returns:
```json
[
  {
    "id": "8859250950ecbb7025731c1206e277e344a6db5f285274b7a1d2817980ab8e64",
    "address": "13qRymPwRxAr7oRdAoFdo5Wp8815sstHE5",
    "transaction_id": "eb197a43a7c4ed230a7125d7e7bf5990cd60be8ff0f59b8fffdfd91d52dfce82",
    "block_hash": "0000000000000000002be95240df5e4215e6878259dce8b9df08650641fdd40a",
    "block_index": 50545
  }
]
```

### Get Block Header

```bash
curl https://junglebus.gorillapool.io/v1/block_header/get/{block_hash}
```

Returns:
```json
{
  "hash": "000000000000000006296f1e5437dd6c01b9b5471691a89a9c7d8e9f06920da5",
  "coin": 1,
  "height": 750000,
  "time": 1658878267,
  "nonce": 4188280238,
  "version": 671080448,
  "merkleroot": "e88b40ac9367eb11dd918416b668e67f09bf24550eac93de7f2d68a0ca0c6eae",
  "bits": "180f4e90",
  "synced": 8971
}
```

## Control Message Status Codes

```typescript
import { ControlMessageStatusCode } from '@gorillapool/js-junglebus';

// Available codes:
ControlMessageStatusCode.BLOCK_DONE    // Block processing complete
ControlMessageStatusCode.WAITING       // Waiting for new block
ControlMessageStatusCode.REORG         // Blockchain reorganization
ControlMessageStatusCode.ERROR         // Error occurred
```

## Go Client

```bash
go get github.com/GorillaPool/go-junglebus
```

```go
package main

import (
    "github.com/GorillaPool/go-junglebus"
)

func main() {
    client, _ := junglebus.New(
        junglebus.WithHTTP("https://junglebus.gorillapool.io"),
    )

    client.Subscribe("subscription-id", 750000, func(tx *junglebus.Transaction) {
        fmt.Printf("TX: %s at height %d\n", tx.Id, tx.BlockHeight)
        fmt.Printf("Types: %v\n", tx.OutputTypes)
    })
}
```

## JungleBus vs WhatsOnChain

| Feature | JungleBus | WhatsOnChain |
|---------|-----------|--------------|
| Real-time streaming | ✅ Yes | ❌ No |
| Transaction history | ✅ Yes | ✅ Yes |
| Address balance | ❌ No | ✅ Yes |
| UTXOs | ❌ No | ✅ Yes |
| Price data | ❌ No | ✅ Yes |
| Parsed tx data | ✅ Yes | ⚠️ Limited |
| Protocol indexing | ✅ Yes | ❌ No |

**Use JungleBus for**: Streaming, protocol monitoring, real-time indexing
**Use WhatsOnChain for**: Balances, UTXOs, price data

## Dashboard Workflow

```
junglebus.gorillapool.io
    ↓
Dashboard → Subscriptions → Create New
    ↓
Configure filters:
  - Addresses (optional)
  - Input types (optional)
  - Output types (required for protocol filtering)
  - Contexts (required for specific protocols)
  - Sub contexts (optional)
  - Data keys (optional)
    ↓
Save subscription
    ↓
Copy subscription ID
    ↓
Use in your code
```

## Links

- **Dashboard**: https://junglebus.gorillapool.io
- **Documentation**: https://junglebus.gorillapool.io/docs
- **JavaScript Client**: https://www.npmjs.com/package/@gorillapool/js-junglebus
- **Go Client**: https://github.com/GorillaPool/go-junglebus
- **GitHub**: https://github.com/GorillaPool/js-junglebus
