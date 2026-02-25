---
name: stratum-v1
description: This skill should be used when the user asks to "implement Stratum v1", "mining pool protocol", "JSON-RPC mining", "pool-miner communication", "mining.subscribe", or needs to build Stratum v1 mining infrastructure.
---

# Stratum v1 Mining Protocol

Stratum v1 is the standard protocol for communication between mining pools and mining hardware (ASICs). It uses JSON-RPC 2.0 over TCP with newline-delimited messages.

## When to Use

- Implementing a BSV mining pool server
- Building mining proxy software
- Creating ASIC firmware/software
- Debugging miner-pool communication
- Understanding pool share validation

## Protocol Overview

### Transport Layer
- Plain TCP socket connection
- JSON-RPC messages terminated by newline (`\n`)
- Persistent connection (not HTTP request/response)
- Optional TLS encryption on separate port

### Message Format

**Request:**
```json
{"id": 1, "method": "mining.subscribe", "params": ["UserAgent/1.0"]}
```

**Response:**
```json
{"id": 1, "result": [...], "error": null}
```

**Notification (no response expected):**
```json
{"id": null, "method": "mining.notify", "params": [...]}
```

## Core Methods

### 1. mining.subscribe

Initial handshake from miner to pool.

**Request:**
```json
{
  "id": 1,
  "method": "mining.subscribe",
  "params": ["UserAgent/1.0.0"]
}
```

**Response:**
```json
{
  "id": 1,
  "result": [
    [["mining.set_difficulty", "subscription_id"], ["mining.notify", "subscription_id"]],
    "extranonce1",
    4
  ],
  "error": null
}
```

**Response fields:**
- `result[0]`: Array of subscription tuples `[method, subscription_id]`
- `result[1]`: Extranonce1 (hex string, typically 8 chars/4 bytes)
- `result[2]`: Extranonce2 size in bytes (typically 4)

### 2. mining.authorize

Authenticate a worker with the pool.

**Request:**
```json
{
  "id": 2,
  "method": "mining.authorize",
  "params": ["ADDRESS.workerName", "password"]
}
```

For BSV pools like GorillaPool, the username format is `BSV_ADDRESS.workerName` where:
- `BSV_ADDRESS` is a valid BSV address (validated at connection)
- `workerName` is an optional identifier for the specific mining device

**Response:**
```json
{"id": 2, "result": true, "error": null}
```

### 3. mining.set_difficulty

Server notification to adjust share difficulty.

**Notification:**
```json
{
  "id": null,
  "method": "mining.set_difficulty",
  "params": [65536]
}
```

The difficulty value represents the minimum share difficulty the pool will accept. Shares below this difficulty are rejected.

### 4. mining.notify

Server sends a new job to miners.

**Notification:**
```json
{
  "id": null,
  "method": "mining.notify",
  "params": [
    "job_id",
    "prevhash",
    "coinb1",
    "coinb2",
    ["merkle_branch_1", "merkle_branch_2"],
    "version",
    "nbits",
    "ntime",
    true
  ]
}
```

**Parameters:**
| Index | Name | Description |
|-------|------|-------------|
| 0 | job_id | Unique job identifier (8-char hex) |
| 1 | prevhash | Previous block hash (word-reversed hex) |
| 2 | coinb1 | First part of coinbase transaction |
| 3 | coinb2 | Second part of coinbase transaction |
| 4 | merkle_branch | Array of merkle tree hashes |
| 5 | version | Block version (big-endian hex) |
| 6 | nbits | Encoded network difficulty target |
| 7 | ntime | Block timestamp (big-endian hex) |
| 8 | clean_jobs | If true, discard previous jobs |

### 5. mining.submit

Miner submits a share (potential block solution).

**Request:**
```json
{
  "id": 3,
  "method": "mining.submit",
  "params": [
    "ADDRESS.workerName",
    "job_id",
    "extranonce2",
    "ntime",
    "nonce",
    "version_bits"
  ]
}
```

**Parameters:**
| Index | Name | Description |
|-------|------|-------------|
| 0 | worker | Worker name (ADDRESS.worker) |
| 1 | job_id | Job ID from mining.notify |
| 2 | extranonce2 | Miner's extranonce2 (hex, length = extranonce2_size * 2) |
| 3 | ntime | Block timestamp (8-char hex) |
| 4 | nonce | 32-bit nonce (8-char hex) |
| 5 | version_bits | Version rolling bits (optional, 8-char hex) |

**Response:**
```json
{"id": 3, "result": true, "error": null}
```

### 6. mining.configure

Extension negotiation (BIP310-style).

**Request:**
```json
{
  "id": 4,
  "method": "mining.configure",
  "params": [
    ["version-rolling", "minimum-difficulty"],
    {"version-rolling.mask": "1fffe000", "minimum-difficulty.value": 2048}
  ]
}
```

**Response:**
```json
{
  "id": 4,
  "result": [true, {
    "version-rolling": true,
    "version-rolling.mask": "1fffe000",
    "minimum-difficulty": true
  }],
  "error": null
}
```

## Byte Order Reference (CRITICAL)

Byte order is the #1 source of bugs in Stratum implementations. This section documents the exact byte order at each stage.

### Terminology
- **BE (Big-Endian)**: Most significant byte first (human-readable, "natural" order)
- **LE (Little-Endian)**: Least significant byte first (Bitcoin internal format)
- **Byte-reversed**: Simple reversal of all bytes
- **Word-reversed**: Reverse 4-byte chunks, then reverse the whole thing (Stratum-specific)

### mining.notify Field Byte Orders

| Field | Stratum JSON Hex | Transformation for Header |
|-------|------------------|---------------------------|
| prevhash | Word-reversed | Use separate byte-reversed version |
| version | BE hex string | Reverse to LE bytes |
| nbits | BE hex string | Reverse to LE bytes |
| ntime | BE hex string | Reverse to LE bytes |
| merkle_branch[] | LE (byte-reversed from node) | Use as-is |
| coinb1, coinb2 | Raw tx bytes | Use as-is |

### Prevhash Transformation (Most Complex)

The prevhash undergoes TWO different transformations:

**From Node (getminingcandidate):**
```
Original: 000000000000000001a2b3c4d5e6f7...  (BE, 64 hex chars)
```

**For Stratum Protocol (mining.notify):**
```go
// Word-reverse: split into 8 4-byte words, reverse each word, then reverse word order
// This is what miners receive in mining.notify params[1]
stratumPrevhash := wordReverse(original)

func wordReverse(hash string) string {
    // Decode to bytes
    bytes, _ := hex.DecodeString(hash)  // 32 bytes

    // Split into 8 words of 4 bytes each
    words := make([][]byte, 8)
    for i := 0; i < 8; i++ {
        words[i] = bytes[i*4 : (i+1)*4]
    }

    // Reverse each word
    for i := range words {
        reverse(words[i])
    }

    // Reverse word order
    reverseSlice(words)

    // Concatenate back
    return hex.EncodeToString(flatten(words))
}
```

**For Block Header Construction:**
```go
// Simple byte-reverse (NOT word-reverse)
// This goes into the actual 80-byte block header
headerPrevhash := reverseBytes(original)
```

**Example:**
```
Node returns:      00000000000000000452b3f2a1c4d5e6f7890abcdef1234567890abcdef12345
Stratum sends:     e6d5c4a1f2b35204000000000000000045123fcdab0987654321fedcab0987...
Header uses:       4523f1cdab0987654321fedcab0987f6e5d4c1a2f3b25400000000000000...
```

### Version, Bits, Time, Nonce

**In Stratum JSON (mining.notify):**
```
version: "20000000"  <- BE hex, 4 bytes
nbits:   "1d00ffff"  <- BE hex, 4 bytes
ntime:   "5f4a3b2c"  <- BE hex, 4 bytes
```

**In Block Header (80 bytes):**
```
All fields stored as LE bytes

version "20000000" -> bytes [0x00, 0x00, 0x00, 0x20]  (reversed)
nbits   "1d00ffff" -> bytes [0xff, 0xff, 0x00, 0x1d]  (reversed)
ntime   "5f4a3b2c" -> bytes [0x2c, 0x3b, 0x4a, 0x5f]  (reversed)
nonce   "12345678" -> bytes [0x78, 0x56, 0x34, 0x12]  (reversed)
```

**Go code:**
```go
// Stratum hex -> header bytes
func stratumHexToHeaderBytes(hexStr string) []byte {
    bytes, _ := hex.DecodeString(hexStr)  // Decode BE hex
    reverseInPlace(bytes)                  // Convert to LE
    return bytes
}
```

### Merkle Branch Byte Order

**From Node (getminingcandidate.merkleProof):**
```
Node returns hashes in BE (natural) order
```

**For Stratum (mining.notify params[4]):**
```go
// Pool must byte-reverse each merkle proof element before sending
for i, proof := range node.MerkleProof {
    proofBytes, _ := hex.DecodeString(proof)
    reverseInPlace(proofBytes)  // Convert to LE
    branches[i] = hex.EncodeToString(proofBytes)
}
```

**When applying branches (share validation):**
```go
// Branches are already LE, use directly
func applyMerkleBranches(coinbaseHash []byte, branches []string) []byte {
    root := coinbaseHash  // Already LE from SHA256d
    for _, branch := range branches {
        branchBytes, _ := hex.DecodeString(branch)  // Already LE
        combined := append(root, branchBytes...)
        root = sha256d(combined)  // Result is LE
    }
    return root  // LE, ready for header
}
```

### Block Hash Byte Order

**After hashing header:**
```go
headerHash := sha256d(header80bytes)  // Returns LE bytes
```

**For display (block explorer, logs):**
```go
displayHash := reverseBytes(headerHash)  // Convert to BE for display
hashString := hex.EncodeToString(displayHash)
```

**For difficulty comparison:**
```go
// Convert LE hash to big.Int (SetBytes expects BE)
hashBE := reverseBytes(headerHash)
hashInt := new(big.Int).SetBytes(hashBE)

// Compare against target
isBlock := hashInt.Cmp(networkTarget) <= 0
```

### Complete Byte Order Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    NODE (getminingcandidate)                     │
├─────────────────────────────────────────────────────────────────┤
│ prevhash:     BE (64 hex chars)                                 │
│ merkleProof:  BE (array of 64-char hex)                         │
│ version:      uint32                                            │
│ nBits:        BE hex string                                     │
│ time:         uint32                                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    POOL (transforms for Stratum)                 │
├─────────────────────────────────────────────────────────────────┤
│ prevhash:     Word-reverse for mining.notify                    │
│               Byte-reverse for header validation (store both)   │
│ merkleProof:  Byte-reverse each element                         │
│ version:      uint32 -> BE hex string (8 chars)                 │
│ nBits:        Already BE hex                                    │
│ ntime:        uint32 -> BE hex string (8 chars)                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    STRATUM JSON (mining.notify)                  │
├─────────────────────────────────────────────────────────────────┤
│ params[1] prevhash:  Word-reversed hex (64 chars)               │
│ params[4] branches:  LE hex strings                             │
│ params[5] version:   BE hex (8 chars)                           │
│ params[6] nbits:     BE hex (8 chars)                           │
│ params[7] ntime:     BE hex (8 chars)                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    MINER (mining.submit)                         │
├─────────────────────────────────────────────────────────────────┤
│ extranonce2: Hex string (length = extranonce2_size * 2)         │
│ ntime:       BE hex (8 chars) - may differ from job             │
│ nonce:       BE hex (8 chars)                                   │
│ versionBits: BE hex (8 chars) - optional                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    POOL (share validation)                       │
├─────────────────────────────────────────────────────────────────┤
│ 1. Coinbase: concat(coinb1, en1, en2, coinb2) - raw bytes       │
│ 2. cbHash:   SHA256d(coinbase) -> LE bytes                      │
│ 3. Root:     Apply LE branches -> LE bytes                      │
│ 4. Header:   [ver_LE, prev_LE, root_LE, time_LE, bits_LE, nonce_LE] │
│ 5. Hash:     SHA256d(header) -> LE bytes                        │
│ 6. Display:  Reverse hash for BE display                        │
└─────────────────────────────────────────────────────────────────┘
```

### Common Byte Order Bugs

1. **Using word-reversed prevhash in header** - Must use simple byte-reversed
2. **Not reversing version/time/bits/nonce** - Stratum sends BE, header needs LE
3. **Reversing merkle branches twice** - They're pre-reversed by pool
4. **Wrong hash comparison endianness** - big.Int.SetBytes expects BE
5. **Displaying hash without reversal** - Internal is LE, display is BE

## Coinbase Construction

The coinbase transaction is built by concatenating:
```
coinbase = coinb1 + extranonce1 + extranonce2 + coinb2
```

Where:
- `coinb1`: Version + input count + prevout + scriptSig length + scriptSig prefix (height, timestamp)
- `extranonce1`: Pool-assigned unique value per connection
- `extranonce2`: Miner-controlled value for nonce space expansion
- `coinb2`: ScriptSig suffix + sequence + outputs + locktime

**All coinbase parts are raw transaction bytes - no byte order transformation needed.**

## Block Header Construction

80-byte header structure (all fields little-endian in final header):

```
Offset  Size  Field       Source                    Transformation
------  ----  ----------  ------------------------  -------------------------
0       4     version     mining.notify params[5]   Decode BE hex, reverse to LE
4       32    prevhash    Store byte-reversed       Use byte-reversed (NOT word-reversed)
36      32    merkleroot  SHA256d of merkle tree    Already LE from hashing
68      4     time        mining.submit params[3]   Decode BE hex, reverse to LE
72      4     bits        mining.notify params[6]   Decode BE hex, reverse to LE
76      4     nonce       mining.submit params[4]   Decode BE hex, reverse to LE
------  ----
        80 bytes total
```

**Go implementation:**
```go
func buildHeader(job *Job, ntime, nonce string, versionMask *uint32, versionBits string) []byte {
    header := make([]byte, 80)

    // Version: BE hex -> LE bytes
    version, _ := hex.DecodeString(job.VersionHex)
    reverseInPlace(version)
    copy(header[0:4], version)

    // Prevhash: Use pre-computed byte-reversed (NOT the word-reversed Stratum format)
    prev, _ := hex.DecodeString(job.PrevHashForHeader)
    copy(header[4:36], prev)

    // Merkle root: Already LE from ApplyMerkleBranches
    copy(header[36:68], merkleRoot)

    // Time: BE hex -> LE bytes
    time, _ := hex.DecodeString(ntime)
    reverseInPlace(time)
    copy(header[68:72], time)

    // Bits: BE hex -> LE bytes
    bits, _ := hex.DecodeString(job.BitsHex)
    reverseInPlace(bits)
    copy(header[72:76], bits)

    // Nonce: BE hex -> LE bytes
    nonceBytes, _ := hex.DecodeString(nonce)
    reverseInPlace(nonceBytes)
    copy(header[76:80], nonceBytes)

    return header
}
```

## Share Validation

```go
// Pseudocode for share validation
func validateShare(job, extranonce1, extranonce2, ntime, nonce, versionBits) bool {
    // 1. Build coinbase
    coinbase := job.Coinb1 + extranonce1 + extranonce2 + job.Coinb2

    // 2. Hash coinbase
    coinbaseHash := SHA256d(coinbase)

    // 3. Calculate merkle root
    merkleRoot := applyMerkleBranches(coinbaseHash, job.Branches)

    // 4. Build 80-byte header
    header := buildHeader(job.Version, job.PrevHash, merkleRoot, ntime, job.Bits, nonce)

    // 5. Apply version rolling if enabled
    if versionBits != "" {
        header.version = (header.version & ~mask) | (versionBits & mask)
    }

    // 6. Hash header
    blockHash := SHA256d(header)

    // 7. Calculate share difficulty
    shareDiff := diff1Target / hashToInt(blockHash)

    // 8. Check against stratum difficulty
    return shareDiff >= session.difficulty
}
```

## Variable Difficulty (VarDiff)

VarDiff dynamically adjusts share difficulty to maintain target share rate.

**Configuration:**
```json
{
  "varDiff": {
    "minDiff": 512,
    "maxDiff": 1000000000,
    "targetTime": 15,
    "retargetTime": 90,
    "variancePercent": 30,
    "maxDelta": 500
  }
}
```

**Algorithm:**
1. Track time between shares in circular buffer
2. Every `retargetTime` seconds, calculate average share time
3. If average outside `targetTime +/- variancePercent`, adjust:
   ```
   newDiff = currentDiff * targetTime / averageTime
   ```
4. Apply `maxDelta` limit and clamp to `[minDiff, maxDiff]`

## Version Rolling (BIP310)

Allows miners to use bits in the version field as additional nonce space.

**Mask:** `0x1fffe000` (bits 13-28, 16 bits = 65536x nonce space)

**Protocol flow:**
1. Miner sends `mining.configure` with `version-rolling` extension
2. Pool responds with allowed mask
3. Miner includes `version_bits` parameter in `mining.submit`
4. Pool validates: `(version_bits & ~mask) == 0`

## Error Codes

| Code | Message | Description |
|------|---------|-------------|
| 20 | Other/Unknown | Generic error |
| 21 | Job not found | Invalid job_id |
| 22 | Duplicate share | Share already submitted |
| 23 | Low difficulty | Share below target |
| 24 | Unauthorized | Worker not authorized |
| 25 | Not subscribed | mining.subscribe not called |

## Implementation Example (Go)

See GorillaNode's implementation at:
- `backend/internal/services/stratum/server.go` - Stratum server
- `backend/internal/services/stratum/templates/gbt.go` - Job construction
- `backend/internal/services/vardiff/manager.go` - VarDiff logic

**Key patterns:**
```go
// Session handling
type session struct {
    conn            net.Conn
    extranonce1     string      // Unique per connection
    extranonce2Size int         // Typically 4 bytes
    difficulty      float64     // Current share difficulty
    authorized      bool        // Has mining.authorize succeeded
    submits         map[string]struct{} // Duplicate detection
}

// Job management
type Job struct {
    Id       string   // Short 8-char hex ID
    Height   int64
    Coinb1   string
    Coinb2   string
    Branches []string
    // ... block header fields
}
```

## Testing

**Connect with netcat:**
```bash
nc pool.example.com 3333
{"id":1,"method":"mining.subscribe","params":["test/1.0"]}
{"id":2,"method":"mining.authorize","params":["1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa.worker1",""]}
```

**Tools:**
- `cpuminer-multi` - CPU miner for testing
- `cgminer` / `bfgminer` - Full-featured miners
- Wireshark with Stratum dissector

## References

- [Stratum Protocol Documentation](https://reference.cash/mining/stratum-protocol)
- [BIP310 - Version Rolling](https://github.com/bitcoin/bips/blob/master/bip-0310.mediawiki)
- [Braiins Stratum V1 Docs](https://braiins.com/stratum-v1/docs)
- [GorillaNode Implementation](https://github.com/b-open-io/gorillanode)
