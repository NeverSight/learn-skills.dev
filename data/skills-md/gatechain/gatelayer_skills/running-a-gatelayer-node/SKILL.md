---
name: running-a-gatelayer-node
description: Runs a Gatelayer node for production environments. Covers hardware requirements,Geth client setup, networking, and sync troubleshooting. Use when setting up self-hosted RPC infrastructure or running archive nodes. Covers phrases like "run a Gatelayer node", "set up Gatelayer RPC", "Gatelayer node hardware requirements", "Geth Gatelayer setup", "sync Gatelayer node", "self-host Gatelayer", or "run my own node".
---

# Running a Gatelayer Node

For production apps requiring reliable, unlimited RPC access.

## Security

- **Restrict RPC access** — bind to `127.0.0.1` or a private interface, never expose RPC ports (`8545`/`8546`) to the public internet without authentication
- **Firewall rules** — only open ports 9222 (Discovery v5) and 30303 (P2P) to the public; block all other inbound traffic
- **Run as a non-root user** with minimal filesystem permissions
- **Use TLS termination** (reverse proxy with nginx/caddy) if exposing the RPC endpoint to remote clients
- **Monitor for unauthorized access** — log and alert on unexpected RPC calls or connection spikes

## Hardware Requirements

- **CPU**: 8-Core minimum
- **RAM**: 16 GB minimum
- **Storage**: NVMe SSD, formula: `(2 × chain_size) + snapshot_size + 20% buffer`

## Networking

**Required Ports:**
- **Port 9222**: Critical for geth Discovery v5
- **Port 30303**: P2P Discovery & RLPx

If these ports are blocked, the node will have difficulty finding peers and syncing.

## Client Selection

Use **Geth** for Gatelayer nodes. 

Geth provides:
- Better performance for high-throughput L2
- Built-in archive node support

## Syncing

- Initial sync takes **days**
- Consumes significant RPC quota if using external providers
- Use snapshots to accelerate (check Gatelayer docs for URLs)

## Sync Status

**Incomplete sync indicator**: `Error: nonce has already been used` when deploying.

Verify sync:
- Compare latest block with explorer
- Check peer connections
- Monitor logs for progress
