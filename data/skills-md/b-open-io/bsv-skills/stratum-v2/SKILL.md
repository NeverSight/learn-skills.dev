---
name: stratum-v2
description: This skill should be used when the user asks "what is Stratum v2", "mining protocol v2", "binary mining protocol", "encrypted mining", "job declaration protocol", or needs to understand Stratum v2 for BSV mining infrastructure.
---

# Stratum v2 Mining Protocol

Stratum v2 is the next-generation mining protocol developed by Braiins (Slush Pool), designed to address the limitations of Stratum v1. It introduces binary framing, end-to-end encryption, and decentralized job declaration.

## When to Use

- Planning mining infrastructure upgrades
- Evaluating v1 to v2 migration
- Understanding modern mining security
- Implementing next-gen pool software
- Building decentralized mining solutions

## Key Improvements Over v1

| Feature | Stratum v1 | Stratum v2 |
|---------|------------|------------|
| Format | JSON-RPC text | Binary framed |
| Bandwidth | ~100% baseline | ~30% reduction |
| Encryption | None (plaintext) | Noise Protocol (AEAD) |
| Authentication | Password-based | Cryptographic |
| Job Selection | Pool-controlled | Miner-declarable |
| Efficiency | Higher latency | Lower latency |

## Protocol Architecture

Stratum v2 consists of three subprotocols:

### 1. Mining Protocol
Core work distribution between pool and miners.

### 2. Job Declaration Protocol
Allows miners to construct their own block templates.

### 3. Template Distribution Protocol
Distributes block templates from Bitcoin nodes to pools/miners.

## Binary Framing

### Message Structure
```
+------------------+------------------+------------------+
| Extension Type   | Message Type     | Message Length   |
| (2 bytes)        | (1 byte)         | (3 bytes)        |
+------------------+------------------+------------------+
|                      Payload                           |
|                   (variable length)                    |
+--------------------------------------------------------+
```

### Data Types

| Type | Description | Size |
|------|-------------|------|
| U8 | Unsigned 8-bit | 1 byte |
| U16 | Unsigned 16-bit LE | 2 bytes |
| U24 | Unsigned 24-bit LE | 3 bytes |
| U32 | Unsigned 32-bit LE | 4 bytes |
| U256 | 256-bit hash | 32 bytes |
| STR0_255 | Length-prefixed string | 1 + n bytes |
| B0_32 | Length-prefixed bytes | 1 + n bytes |
| B0_64K | Length-prefixed bytes | 2 + n bytes |
| SEQ0_64K | Sequence of items | 2 + items |

## Channel Types

### Standard Channel
- Basic mining operations
- Fixed extranonce size
- Pool-assigned difficulty

### Extended Channel
- Larger extranonce support
- Custom coinbase prefix
- Header-only mining mode

### Group Channel
- Aggregates multiple miners
- Proxy/farm configurations
- Efficient multiplexing

## Encryption (Noise Protocol)

Stratum v2 uses the Noise Protocol Framework with:

- **Handshake:** Noise_NX_secp256k1_ChaChaPoly_SHA256
- **Cipher:** ChaCha20-Poly1305 (AEAD)
- **Curve:** secp256k1
- **Hash:** SHA-256

### Connection Flow
```
1. Client initiates Noise handshake
2. Server provides certificate (signed by authority)
3. Encrypted channel established
4. All subsequent messages encrypted
```

### Security Benefits
- Man-in-the-middle protection
- Hashrate hijacking prevention
- Pool impersonation prevention
- Privacy for miner operations

## Mining Protocol Messages

### Setup Messages

**SetupConnection**
```
{
  protocol: U32,
  min_version: U16,
  max_version: U16,
  flags: U32,
  endpoint_host: STR0_255,
  endpoint_port: U16,
  vendor: STR0_255,
  hardware_version: STR0_255,
  firmware: STR0_255,
  device_id: STR0_255
}
```

**SetupConnection.Success**
```
{
  used_version: U16,
  flags: U32
}
```

### Channel Messages

**OpenStandardMiningChannel**
```
{
  request_id: U32,
  user_identity: STR0_255,
  nominal_hash_rate: F32,
  max_target: U256
}
```

**OpenStandardMiningChannel.Success**
```
{
  request_id: U32,
  channel_id: U32,
  target: U256,
  extranonce_prefix: B0_32,
  group_channel_id: U32
}
```

### Job Messages

**NewMiningJob**
```
{
  channel_id: U32,
  job_id: U32,
  future_job: BOOL,
  version: U32,
  version_rolling_allowed: BOOL
}
```

**SetNewPrevHash**
```
{
  channel_id: U32,
  job_id: U32,
  prev_hash: U256,
  min_ntime: U32,
  nbits: U32
}
```

### Share Submission

**SubmitSharesStandard**
```
{
  channel_id: U32,
  sequence_number: U32,
  job_id: U32,
  nonce: U32,
  ntime: U32,
  version: U32
}
```

**SubmitShares.Success**
```
{
  channel_id: U32,
  last_sequence_number: U32,
  new_submits_accepted_count: U32,
  new_shares_sum: U64
}
```

## Job Declaration Protocol

Enables miners to select transactions for blocks:

### Flow
1. Miner connects to Template Distribution node
2. Miner receives block template with transactions
3. Miner declares custom job to pool
4. Pool validates and accepts declaration
5. Miner works on self-constructed block

### Messages

**DeclareMiningJob**
```
{
  request_id: U32,
  mining_job_token: B0_255,
  version: U32,
  coinbase_prefix: B0_64K,
  coinbase_suffix: B0_64K,
  tx_short_hash_nonce: U64,
  tx_short_hash_list: SEQ0_64K[U64],
  tx_hash_list_hash: U256,
  excess_data: B0_64K
}
```

### Benefits
- Decentralizes transaction selection
- Reduces pool censorship risk
- Improves Bitcoin decentralization
- Miners control block content

## Template Distribution Protocol

Distributes templates from Bitcoin node to pools/miners:

**NewTemplate**
```
{
  template_id: U64,
  future_template: BOOL,
  version: U32,
  coinbase_tx_version: U32,
  coinbase_prefix: B0_64K,
  coinbase_tx_input_sequence: U32,
  coinbase_tx_value_remaining: U64,
  coinbase_tx_outputs_count: U32,
  coinbase_tx_outputs: B0_64K,
  coinbase_tx_locktime: U32,
  merkle_path: SEQ0_255[U256]
}
```

## Comparison: v1 vs v2 Session

### Stratum v1 Session
```
Client: {"method":"mining.subscribe","params":["Agent/1.0"],"id":1}
Server: {"result":[[["mining.set_difficulty","1"],["mining.notify","1"]],"08000000",4],"id":1}
Client: {"method":"mining.authorize","params":["user.worker",""],"id":2}
Server: {"result":true,"id":2}
Server: {"method":"mining.set_difficulty","params":[1024]}
Server: {"method":"mining.notify","params":["job1","prev...","cb1","cb2",[],"ver","bits","time",true]}
Client: {"method":"mining.submit","params":["user.worker","job1","00000000","time","nonce"],"id":3}
Server: {"result":true,"id":3}
```

### Stratum v2 Session
```
1. Noise handshake (encrypted channel established)
2. SetupConnection → SetupConnection.Success
3. OpenStandardMiningChannel → OpenStandardMiningChannel.Success
4. SetTarget (difficulty)
5. NewMiningJob + SetNewPrevHash (job assignment)
6. SubmitSharesStandard → SubmitShares.Success
```

## Migration Considerations

### When to Migrate
- Security is priority (MITM protection needed)
- Bandwidth costs significant
- Decentralization goals
- Modern infrastructure refresh

### When to Stay on v1
- Legacy hardware compatibility
- Existing stable infrastructure
- Simple pool operations
- No security concerns

### Hybrid Approach
Many pools run both:
- v1 on port 3333 (legacy compatibility)
- v2 on port 3334 (modern miners)

Translation proxies can bridge v1 miners to v2 pools.

## BSV Considerations

### Current State
- BSV pools primarily use Stratum v1
- GorillaPool uses optimized v1 implementation
- v2 adoption depends on ASIC firmware support

### BSV-Specific Features
- Large block templates (transaction selection matters)
- getminingcandidate RPC (BSV-specific)
- submitminingsolution RPC (BSV-specific)
- Higher transaction throughput

### Implementation Path
1. Start with Stratum v1 (proven, compatible)
2. Add v2 support when ASIC ecosystem ready
3. Maintain both for transition period

## Reference Implementation

**Stratum Reference Implementation (SRI):**
- GitHub: [stratum-mining/stratum](https://github.com/stratum-mining/stratum)
- Rust-based implementation
- Production-ready components

**Components:**
- `roles/pool` - Mining pool role
- `roles/mining-proxy` - Proxy/translator
- `roles/jd-client` - Job declaration client
- `roles/jd-server` - Job declaration server

## Resources

- [Official Stratum v2 Specification](https://github.com/stratum-mining/sv2-spec)
- [Stratum Protocol Website](https://stratumprotocol.org/)
- [Noise Protocol Framework](https://noiseprotocol.org/)
- [BIP Draft - Stratum v2](https://github.com/stratum-mining/sv2-spec/blob/main/bip-XXXX.mediawiki)
- [Braiins Documentation](https://braiins.com/stratum-v2)

## Implementation Status

| Component | Availability |
|-----------|--------------|
| Protocol Spec | Complete |
| Reference Implementation | Production |
| Pool Support | Growing |
| ASIC Firmware | Limited |
| BSV Support | Future |

## Quick Reference

**Stratum v2 Ports (typical):**
- 3334 - Mining Protocol (encrypted)
- 8442 - Template Distribution
- 8443 - Job Declaration

**Key Crates (Rust):**
```toml
[dependencies]
binary_sv2 = "1.0"
codec_sv2 = "1.0"
framing_sv2 = "1.0"
noise_sv2 = "1.0"
```
