---
name: taiko-node
description: Set up, run, and manage Taiko nodes on Hoodi testnet or mainnet using Docker or from source. Use when "run node", "node operator", "simple-taiko-node", "taiko-geth", "taiko-client", or "sync" is mentioned.
---

# Taiko Node Operations

Run Taiko nodes. A node = `taiko-geth` (execution) + `taiko-client` (consensus).

> **Network Selection:** Always ask which network if user hasn't specified "hoodi" or "mainnet".

## Quick Decision Guide

| Task | Resource |
|------|----------|
| Network config, chain IDs, RPCs | [Networks Reference](../taiko/references/networks.md) |
| Run node (Docker, recommended) | [Docker setup](./references/docker-setup.md) |
| Build from source | [Source build](./references/source-build.md) |
| Run Ethereum Hoodi L1 | [eth-docker](https://github.com/ethstaker/eth-docker) |
| Debug issues | [Troubleshooting](./references/node-troubleshooting.md) |

## Prerequisites

- **Hardware:** 16 GB RAM, 2 TB SSD, quad-core CPU
- **Software:** Docker `^24.0`, git `^2` (source: also Go `^1.21`, make `^4`)
- **L1 node required** — local strongly recommended (remote RPCs rate-limit)

## Quick Start (Docker)

```bash
git clone https://github.com/taikoxyz/simple-taiko-node.git && cd simple-taiko-node
cp .env.sample .env              # mainnet (.env.sample.hoodi for testnet)
# Edit .env: set L1_ENDPOINT_WS, L1_BEACON_HTTP, COMPOSE_PROFILES
docker compose up -d             # mainnet
docker compose -f docker-compose-hoodi.yml up -d  # testnet
```

**L1 endpoints:** Use `host.docker.internal` or machine's private IP, not `127.0.0.1`.

## CLI Quick Reference

Use `taiko --json` for structured output:

```bash
taiko node status --json                                      # health: block, peers, sync %, L1 anchor
taiko node logs --service taiko_client_driver --tail 50       # taiko-client logs
taiko node logs --service l2_execution_engine --tail 50       # taiko-geth logs
taiko node restart --json                                     # restart with structured confirmation
```

All commands return: `{ schema_version, command, status, network, data, errors, warnings, metrics }`

## Related Skills

- **L2 contract addresses & RPCs:** [taiko/references/networks.md](../taiko/references/networks.md)
- **Smart contract development:** [taiko skill](../taiko/SKILL.md)

## Resources

- **Docs**: https://docs.taiko.xyz/guides/node-operators/
- **Releases**: https://github.com/taikoxyz/simple-taiko-node/releases
- **Discord**: https://discord.gg/aGZYtKqMjj
