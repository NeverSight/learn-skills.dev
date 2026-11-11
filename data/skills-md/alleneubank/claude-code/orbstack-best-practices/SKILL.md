---
name: orbstack-best-practices
description: Use when working with OrbStack Linux VMs, Docker on macOS, orbctl commands, or orb machine lifecycle.
---

# OrbStack Best Practices

OrbStack is a fast Docker and Linux VM runtime for macOS. Replaces Docker Desktop with better performance and seamless macOS integration.

## Core Commands

```bash
# Machine lifecycle
orb list                               # List machines
orb create ubuntu:noble myvm           # Create (distro:version name)
orb create --arch amd64 ubuntu x86vm  # x86 emulation via Rosetta
orb create ubuntu myvm -c cloud.yml   # With cloud-init
orb start/stop/restart/delete myvm
orb default myvm                       # Set default machine

# Shell and exec
orb                           # Shell into default machine
orb -m myvm -u root           # Specific machine + user
orb -m myvm ./script.sh       # Run command in machine

# File transfer
orb push ~/local.txt          # Copy to default machine home
orb pull ~/remote.txt         # Copy from default machine
orb push -m vm ~/f.txt /tmp/  # Specific machine + path

# Docker/K8s
orb restart docker            # Restart Docker engine
orb logs docker               # Docker engine logs
orb start k8s / orb delete k8s

# Config
orb config set memory_mib 8192
orb config set cpu 4
orb config set rosetta true
orb config set network_proxy http://proxy:8080
```

## Key Paths

| Location | Path |
|----------|------|
| Linux files from macOS | `~/OrbStack/<machine>/` |
| Docker volumes from macOS | `~/OrbStack/docker/volumes/` |
| macOS files from Linux | `/mnt/mac/Users/...` (also at same path directly) |
| Other machines from Linux | `/mnt/machines/<name>/` |
| SSH key | `~/.orbstack/ssh/id_ed25519` |
| Docker daemon config | `~/.orbstack/config/docker.json` |

## Networking (OrbStack-Specific)

Servers in Linux machines are **automatically available on `localhost`** on macOS — no port mapping required.

**DNS names:**
| Pattern | Resolves to |
|---------|-------------|
| `<machine>.orb.local` | Linux VM |
| `<container>.orb.local` | Docker container |
| `<svc>.<project>.orb.local` | Compose service |
| `host.orb.internal` | macOS host (from Linux machine) |
| `host.docker.internal` | macOS host (from container) |

All `.orb.local` domains get **zero-config HTTPS** automatically.

Custom container domain: `docker run -l dev.orbstack.domains=myapp.local nginx`

VPN-compatible; follows macOS proxy settings automatically.

## SSH Access

Single multiplexed SSH server — no per-machine setup needed:

```bash
ssh orb                    # Default machine
ssh myvm@orb               # Specific machine
ssh user@myvm@orb          # Specific user + machine
```

IDE config: VS Code "Remote - SSH" → `orb` or `myvm@orb`. JetBrains: host `localhost`, port `32222`, key `~/.orbstack/ssh/id_ed25519`. SSH agent forwarding is automatic.

## Docker Differences from Docker Desktop

- Container domains resolve without port mapping (`web.orb.local` instead of `localhost:8080`).
- Prefer named volumes over bind mounts — data stays in Linux, no cross-filesystem overhead.
- x86 images on Apple Silicon: `docker run --platform linux/amd64 ubuntu` or `export DOCKER_DEFAULT_PLATFORM=linux/amd64`.
- SSH agent in containers: `-v /run/host-services/ssh-auth.sock:/agent.sock -e SSH_AUTH_SOCK=/agent.sock`.
- Kubernetes: all service types accessible from macOS without `kubectl port-forward`; `cluster.local` DNS works directly.

## macOS Commands from Linux

```bash
mac open https://example.com   # Open in macOS browser
mac notify "Build done"        # macOS notification
ORBENV=AWS_PROFILE:EDITOR orb ./deploy.sh  # Forward env vars
```

## Troubleshooting

```bash
orb report              # Generate diagnostic report
orb logs myvm           # Machine boot logs
orb restart docker      # Restart Docker engine
orb reset               # Factory reset (deletes everything)
docker context use orbstack  # Fix "cannot connect to Docker daemon"
```

**Rosetta x86 error**: `sudo dpkg --add-architecture amd64 && sudo apt install libc6:amd64`

Cloud-init debug: `orb -m myvm cloud-init status --long` or `orb -m myvm cat /var/log/cloud-init-output.log`
