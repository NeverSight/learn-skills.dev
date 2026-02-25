---
name: provision-nixos-server
description: |
  Provision new NixOS servers on Proxmox for this nix flake project. Guides through the complete workflow: creating Proxmox LXC containers, SSH setup, Colmena configuration (init/full pattern), and application deployment with nginx proxy, PostgreSQL, and container images.

  Use when: (1) Creating a new server/container on Proxmox, (2) Setting up a new NixOS host with Colmena, (3) Deploying applications with nginx SSL proxy and/or PostgreSQL database, (4) Adding new container images to the repository.
---

# Provision NixOS Server

## Workflow Overview

1. Gather requirements from user
2. Create Proxmox container
3. Set up SSH access
4. Create Colmena init configuration
5. Deploy init config and update to static IP
6. Copy infrastructure key for SOPS
7. Configure application (if applicable)
8. Deploy full configuration

## Step 1: Gather Requirements

Ask user for:
- **Hostname**: Server name (e.g., `woodpecker`)
- **Container ID**: Proxmox container ID (e.g., `122`)
- **Proxmox server**: Target Proxmox host (e.g., `thrall`)
- **Storage**: `local-lvm` (fast) or `cephpool1` (distributed, slower)
- **Memory**: RAM in MB (default: `4096`)
- **Disk size**: In GB (default: `100`)
- **Application**: What will run on this server

Verify soft-secrets exist for the new host (`host.<hostname>.admin_ip_address`, etc.) or ask user to create them.

## Step 2: Create Proxmox Container

```bash
PROXMOX_SERVER=<server>
HOSTNAME=<hostname>
CONTAINER_ID=<id>
STORAGE=local-lvm
MEMORY=4096
DISK_SIZE_IN_GB=100

ssh $PROXMOX_SERVER "pct create $CONTAINER_ID \
    --arch amd64 local:vztmpl/nixos-system-x86_64-linux.tar.xz \
    --ostype unmanaged \
    --description nixos \
    --hostname $HOSTNAME \
    --net0 name=eth0,bridge=vmbr3,ip=dhcp,firewall=1 \
    --storage $STORAGE \
    --memory $MEMORY \
    --rootfs $STORAGE:$DISK_SIZE_IN_GB \
    --unprivileged 1 \
    --features nesting=1 \
    --cmode console \
    --onboot 1 \
    --start 1"
```

**Timeout note:** Use longer timeouts (5+ minutes) for `cephpool1` storage.

## Step 3: Set Up SSH Access

Fresh NixOS containers require full paths. Run via `pct exec`:

```bash
ssh $PROXMOX_SERVER "pct exec $CONTAINER_ID -- /run/current-system/sw/bin/bash -c '\
  mkdir -p ~/.ssh && \
  curl -s https://github.com/fred-drake.keys > ~/.ssh/authorized_keys && \
  chmod 700 ~/.ssh && chmod 600 ~/.ssh/authorized_keys'"
```

Get DHCP IP address:
```bash
ssh $PROXMOX_SERVER "pct exec $CONTAINER_ID -- /run/current-system/sw/bin/ip addr show eth0 | grep 'inet '"
```

## Step 4: Create Colmena Init Configuration

Create these files (see [references/colmena-host-template.md](references/colmena-host-template.md) and [references/nixos-config-template.md](references/nixos-config-template.md)):

1. `mkdir -p modules/nixos/host/<hostname>`
2. Create `modules/nixos/host/<hostname>/configuration.nix`
3. Create `colmena/hosts/<hostname>.nix`
4. Update `colmena/default.nix` with imports

**Initial deploy config:** Use DHCP IP and `root` user:
```nix
deployment = {
  targetHost = "<DHCP_IP>";
  targetUser = "root";
};
```

Stage files and build:
```bash
git add colmena/hosts/<hostname>.nix modules/nixos/host/<hostname>/ colmena/default.nix
colmena build --impure --on <hostname>-init
```

## Step 5: Deploy Init and Update IP

Deploy (will hang when network restarts due to IP change):
```bash
colmena apply --impure --on <hostname>-init
```

Kill the hanging command, then update `colmena/hosts/<hostname>.nix`:
```nix
deployment = {
  targetHost = soft-secrets.host.<hostname>.admin_ip_address;
  targetUser = "default";
};
```

Verify with another deploy:
```bash
colmena apply --impure --on <hostname>-init
```

## Step 6: Copy Infrastructure Key

Required for SOPS secret decryption:
```bash
ssh default@<NEW_IP> "mkdir -p ~/.ssh && chmod 700 ~/.ssh"
scp ~/.ssh/id_infrastructure default@<NEW_IP>:~/id_infrastructure
ssh default@<NEW_IP> "chmod 600 ~/id_infrastructure"
```

**Age public key** (for .sops.yaml): `age1rnarwmx5yqfhr3hxvnnw2rxg3xytjea7dhtg00h72t26dn6csdxqvsryg5`

If secrets fail to decrypt, user needs to add this key to `.sops.yaml` and run `sops updatekeys` on the secret files.

## Step 7: Configure Application

See [references/app-templates.md](references/app-templates.md) for patterns.

### Add Container Images

1. Edit `apps/fetcher/containers.toml`
2. Run `just update-container-digests`
3. Stage: `git add apps/fetcher/containers.toml apps/fetcher/containers-sha.nix`

### Create Application Config

Create `apps/<appname>.nix` with:
- Nginx proxy with SSL (if web-facing)
- PostgreSQL container (if database needed)
- Application container(s)
- tmpfiles rules for data directories

### Create Secrets Config

Create `modules/secrets/<hostname>.nix` referencing SOPS files.

User must create SOPS files in secrets repo with:
- `postgresql-env.sops` (POSTGRES_PASSWORD, POSTGRES_USER, POSTGRES_DB)
- `<appname>-env.sops` (app-specific secrets)

### Update Colmena Full Config

In `colmena/hosts/<hostname>.nix`, add to full configuration imports:
```nix
../../modules/secrets/<hostname>.nix
../../apps/<appname>.nix
```

## Step 8: Deploy Full Configuration

```bash
just update-secrets  # Get latest secrets
git add <all-new-files>
colmena apply --impure --on <hostname>
```

## Common Issues

**SOPS decrypt fails:** Age key not in .sops.yaml - user must add key and re-encrypt

**Nginx duplicate directive:** Don't add `proxy_http_version` when using `proxyWebsockets = true`

**PostgreSQL 18 fails:** Mount at `/var/lib/postgresql` not `/var/lib/postgresql/data`

**Container can't reach postgres:** Use `0.0.0.0:5432:5432` for port binding, `host.containers.internal` in connection string
