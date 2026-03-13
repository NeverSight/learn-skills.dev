---
name: ika-operator
description: Guide for operating Ika network nodes - validators, fullnodes, and notifiers. Use when deploying, configuring, monitoring, or troubleshooting Ika infrastructure. Triggers on tasks involving ika-node, ika-validator, ika-fullnode, ika-notifier, NodeConfig, consensus setup, P2P networking, validator registration, or Ika node operations.
---

# Ika Node Operator Guide

Deploy and operate Ika network nodes (validators, fullnodes, notifiers).

## References (detailed configuration and operations)

- `references/configuration.md` - Complete NodeConfig YAML reference, all fields with defaults
- `references/operations.md` - Deployment, monitoring, admin API, recovery, metrics proxy
- `references/validator-setup.md` - Step-by-step mainnet validator setup with CLI commands

## Node Types

| Binary | Mode | Purpose | Key Config |
|---|---|---|---|
| `ika-node` | Auto-detect | Selects mode from config | Detects automatically |
| `ika-validator` | Validator | Consensus + MPC signing | Requires `consensus-config` |
| `ika-fullnode` | Fullnode | State sync via P2P, no consensus | No `consensus-config`, no `notifier-client-key-pair` |
| `ika-notifier` | Notifier | Submits checkpoints to Sui | Requires `notifier-client-key-pair` |

**Auto-detection order**: `consensus-config` present → Validator; else `notifier-client-key-pair` present → Notifier; else → Fullnode.

## Hardware Requirements (Validator)

| Resource | Minimum |
|---|---|
| CPU | 16 physical cores / 16 vCPUs |
| Memory | 128 GB |
| Storage | 4 TB NVMe |
| Network | 1 Gbps |
| OS | Linux Ubuntu/Debian x64 (or Docker on x64 Linux) |

**Warning**: Hetzner has strict crypto ToS and may close validators without notice.

## Connectivity (Validator Ports)

| Protocol/Port | Direction | Purpose |
|---|---|---|
| TCP/8080 | Inbound | Protocol / Transaction Interface |
| UDP/8081 | Inbound/Outbound | Consensus Interface |
| UDP/8084 | Inbound/Outbound | Peer-to-Peer State Sync |
| TCP/8443 | Outbound | Metrics Pushing |
| TCP/9184 | Inbound/Outbound | Metrics Scraping (both Sui fullnode and Ika node) |

**Critical**: Ports 8080-8084 and 9184 must be open with correct protocols (TCP/UDP).

## Prerequisites

- DNS address for your validator (e.g., `ika-mainnet-1.<your-domain>`)
- Your own Sui fullnode on Sui mainnet, fully synced (at least 2 latest epochs). Use separate DNS for Sui node.
- Sui CLI installed, configured for mainnet, active address with at least 10 SUI
- Minimum 40 million IKA stake to join the committee

## Quick Start: Mainnet Validator

Download binaries from: https://github.com/dwallet-labs/ika/releases

### Step 1: Configure Ika Environment

Get the latest package/object IDs from the canonical source:
- **Mainnet**: `deployed_contracts/mainnet/address.yaml` ([GitHub](https://github.com/dwallet-labs/ika/blob/main/deployed_contracts/mainnet/address.yaml))
- **Testnet**: `deployed_contracts/testnet/address.yaml` ([GitHub](https://github.com/dwallet-labs/ika/blob/main/deployed_contracts/testnet/address.yaml))

```bash
./ika validator config-env \
  --ika-package-id                    <ika_package_id> \
  --ika-common-package-id             <ika_common_package_id> \
  --ika-dwallet-2pc-mpc-package-id    <ika_dwallet_2pc_mpc_package_id> \
  --ika-system-package-id             <ika_system_package_id> \
  --ika-system-object-id              <ika_system_object_id>
# Creates: ~/.ika/ika_config/ika_sui_config.yaml
# Note: ika-dwallet-coordinator-object-id is not set at this stage (defaults to zero);
# it must be configured later in the node's validator.yaml under sui-connector-config.
```

### Step 2: Generate Validator Info & Keys

```bash
./ika validator make-validator-info \
  "My Validator" "Description" \
  "https://example.com/image.png" "https://example.com" \
  "ika-mainnet-1.example.com" \
  10000 \
  <YOUR_SUI_ADDRESS>
# Generates: protocol.key, network.key, consensus.key, root-seed.key, validator.info
```

**CRITICAL**: Back up ALL generated keys. `root-seed.key` is SECRET and IRREPLACEABLE. If lost, it cannot be updated via contract. Other keys (protocol, network, consensus) can be rotated on-chain.

### Step 3: Register as Validator Candidate

```bash
./ika validator become-candidate ./validator.info
# Returns: Validator ID, Validator Cap ID, Validator Operation Cap ID, and Validator Commission Cap ID
```

### Step 4: Stake into Validator

Stake at least 40 million IKA via: https://ika-mainnet-validators-staking.pages.dev/

Verify your Validator ID matches the CLI output.

### Step 5: Join Committee

```bash
./ika validator join-committee --validator-cap-id <VALIDATOR_CAP_ID>
```

You become a pending validator and join the committee at the next epoch.

### Step 6: Run the Validator Node

Directory structure:

```
/opt/ika/
├── bin/ika-node
├── config/validator.yaml
├── key-pairs/
│   ├── protocol.key
│   ├── network.key
│   ├── consensus.key
│   └── root-seed.key
└── db/                        # Created at runtime
    ├── authorities_db/
    └── consensus_db/
```

Before running, edit `validator.yaml`:
- Set `ika-dwallet-coordinator-object-id` to the value from `deployed_contracts/mainnet/address.yaml`
- Ensure: `sui-chain-identifier: mainnet`
- Set metrics: `push-url: "https://mainnet.metrics.ika-network.net:8443/publish/metrics"`

```bash
ika-node --config-path /opt/ika/config/validator.yaml
```

**Logging**: Set `RUST_LOG` for log levels, `RUST_LOG_JSON=1` for JSON output.

### Step 7: Verify

Wait a couple minutes, check logs for:

```
ika_core::checkpoints: Creating checkpoint(s) for 0 messages next_checkpoint_seq=1
```

This confirms the node is running. Additional checkpoints appear only during/after MPC sessions.

## Package & Object IDs

Always get the latest IDs from the canonical source files in the repo:

- **Mainnet**: `deployed_contracts/mainnet/address.yaml` ([GitHub](https://github.com/dwallet-labs/ika/blob/main/deployed_contracts/mainnet/address.yaml))
- **Testnet**: `deployed_contracts/testnet/address.yaml` ([GitHub](https://github.com/dwallet-labs/ika/blob/main/deployed_contracts/testnet/address.yaml))

## Keypairs

| Key | Type | Purpose | Required By | Recoverable? |
|---|---|---|---|---|
| `protocol-key-pair` | AuthorityKeyPair | Protocol signatures | All | Yes (rotate on-chain) |
| `consensus-key-pair` | Ed25519 | Consensus communication | All | Yes (rotate on-chain) |
| `network-key-pair` | Ed25519 | P2P networking | All | Yes (rotate on-chain) |
| `account-key-pair` | SuiKeyPair | Sui interactions | All | Yes |
| `root-seed-key-pair` | RootSeed | MPC cryptographic operations | Validators | **NO - IRREPLACEABLE** |
| `notifier-client-key-pair` | SuiKeyPair | Submit checkpoints to Sui | Notifiers | Yes |

## Validator Config Essentials

```yaml
# Mainnet validator must have:
sui-connector-config:
  sui-chain-identifier: mainnet
  sui-rpc-url: 'http://<your-sui-fullnode>:9000'
  # Get all IDs from deployed_contracts/mainnet/address.yaml
  ika-package-id: '<from address.yaml>'
  ika-dwallet-coordinator-object-id: '<from address.yaml>'
  # ... other package/object IDs

consensus-config:                         # Presence triggers validator mode
  db-path: '/opt/ika/consensus_db'
  db-retention-epochs: 0
  db-pruner-period-secs: 3600
  max-pending-transactions: 20000

root-seed-key-pair:
  path: /opt/ika/key-pairs/root-seed.key

metrics:
  push-url: "https://mainnet.metrics.ika-network.net:8443/publish/metrics"
```

## Admin API (localhost only)

```bash
curl http://127.0.0.1:1337/logging                    # View log filter
curl -X POST 'http://127.0.0.1:1337/enable-tracing?filter=debug&duration=10s'
curl -X POST http://127.0.0.1:1337/reset-tracing      # Reset to env var
curl http://127.0.0.1:1337/node-config                 # View config (keys masked)
curl http://127.0.0.1:1337/capabilities                # View capabilities
```

## Environment Variables

| Variable | Purpose | Default |
|---|---|---|
| `IKA_CONFIG_DIR` | Override config directory | `~/.ika/ika_config/` |
| `RUST_LOG` | Log level filter | — |
| `RUST_LOG_JSON` | JSON log output (`1` to enable) | — |
| `TRACE_FILTER` | Tracing log filter | — |

## Services by Node Type

| Service | Validator | Fullnode | Notifier |
|---|---|---|---|
| AuthorityState | Y | Y | Y |
| ConsensusManager | Y | — | — |
| DWalletMPCService | Y | — | — |
| SuiConnectorService | Y | Y | Y |
| CheckpointServices | Y | Y | Y |
| P2P + StateSync | Y | Y | Y |
| Discovery | Y | Y | Y |

## Key Operational Notes

- **Release mode required**: Always build with `--release` for crypto operations
- **Sui fullnode required**: Run your own Sui fullnode, fully synced (2+ latest epochs)
- **Package IDs must match**: Contract IDs in config must match deployed contracts
- **Minimum stake**: 40 million IKA to join the committee
- **Root seed is sacred**: Back it up securely. Cannot be regenerated or rotated on-chain.
- **Updates**: Monitor `#nodes-updates-mainnet` channel for new releases
- **Recovery**: Use `--run-with-range-epoch` or `--run-with-range-checkpoint` for disaster recovery
- **Checkpoint pinning**: Use `pinned-dwallet-checkpoints` in state-sync config for fork recovery
- **Graceful shutdown**: Send `SIGTERM` or `SIGINT`
