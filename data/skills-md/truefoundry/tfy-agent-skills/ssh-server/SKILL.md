---
name: ssh-server
description: Deploys remote development environments with SSH access on TrueFoundry. Use when setting up VS Code Remote workspaces, cloud development machines, GPU dev boxes, or remote coding environments with SSH access.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(tfy*) Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# SSH Server

Launch an SSH server on TrueFoundry for remote development. Write a YAML manifest and apply with `tfy apply`. REST API fallback when CLI unavailable. Connect with VS Code Remote-SSH or any SSH client, with full GPU access and persistent storage.

## When to Use

- User asks "launch ssh server", "start ssh server", "remote dev environment"
- User wants to connect VS Code remotely to cloud GPUs
- User needs SSH access for development/debugging
- User asks about remote development environments

## When NOT to Use

- User wants Jupyter notebooks → prefer `notebooks` skill; ask if the user wants another valid path
- User wants to deploy a service → prefer `deploy` skill; ask if the user wants another valid path
- User wants to deploy a model → prefer `llm-deploy` skill; ask if the user wants another valid path

</objective>

<context>

## Prerequisites

**Always verify before launching an SSH server:**

1. **Credentials** — `TFY_BASE_URL` and `TFY_API_KEY` must be set (env or `.env`)
2. **Workspace** — `TFY_WORKSPACE_FQN` required. **Never auto-pick. Ask the user if missing.**
3. **CLI** — Check `tfy --version`. Install if missing: `pip install 'truefoundry==0.5.0' && tfy login --host "$TFY_BASE_URL"`

For credential check commands and .env setup, see `references/prerequisites.md`.

### CLI Detection

```bash
tfy --version
```

| CLI Output | Status | Action |
|-----------|--------|--------|
| `tfy version X.Y.Z` (>= 0.5.0) | Current | Use `tfy apply` as documented below. |
| `tfy version X.Y.Z` (0.3.x-0.4.x) | Outdated | Upgrade: install a pinned version (e.g. `pip install 'truefoundry==0.5.0'`). Core `tfy apply` should still work. |
| Command not found | Not installed | Install: `pip install 'truefoundry==0.5.0' && tfy login --host "$TFY_BASE_URL"` |
| CLI unavailable (no pip/Python) | Fallback | Use REST API via `tfy-api.sh`. See `references/cli-fallback.md`. |

## Launch SSH Server via UI

1. Go to **Deployments → New Deployment → SSH Server**
2. Add your SSH public key
3. Select workspace and configure resources
4. Click Deploy

</context>

<instructions>

## Launch SSH Server via `tfy apply` (CLI — Recommended)

### Configuration Questions

Before generating the manifest, ask the user:

1. **Name** — What to call the SSH server
2. **GPU needed?** — CPU server (default) or GPU server (for ML development). If GPU, use the CUDA image variant.
3. **Home directory size** — Persistent storage in GB (default: 20)
4. **Image variant** — CPU (`ssh-server:0.4.5-py3.12.12`) or CUDA (`ssh-server:0.4.5-cu129-py3.12.12`)

### CPU SSH Server

**1. Generate the manifest:**

```yaml
# tfy-manifest.yaml — SSH Server (CPU)
name: my-ssh-server
type: ssh-server
image:
  image_uri: public.ecr.aws/truefoundrycloud/ssh-server:0.4.5-py3.12.12
home_directory_size: 20
resources:
  node:
    type: node_selector
    capacity_type: on_demand
  cpu_request: 1
  cpu_limit: 3
  memory_request: 4000
  memory_limit: 6000
  ephemeral_storage_request: 5000
  ephemeral_storage_limit: 10000
workspace_fqn: "YOUR_WORKSPACE_FQN"
```

**2. Preview:**

```bash
tfy apply -f tfy-manifest.yaml --dry-run --show-diff
```

**3. Apply:**

```bash
tfy apply -f tfy-manifest.yaml
```

### GPU SSH Server

```yaml
# tfy-manifest.yaml — GPU SSH Server (CUDA)
name: gpu-dev-server
type: ssh-server
image:
  image_uri: public.ecr.aws/truefoundrycloud/ssh-server:0.4.5-cu129-py3.12.12
home_directory_size: 20
resources:
  node:
    type: node_selector
    capacity_type: on_demand
  cpu_request: 4
  cpu_limit: 8
  memory_request: 16000
  memory_limit: 32000
  ephemeral_storage_request: 10000
  ephemeral_storage_limit: 20000
  devices:
    - type: nvidia_gpu
      name: A10_24GB
      count: 1
workspace_fqn: "YOUR_WORKSPACE_FQN"
```

## Launch SSH Server via REST API (Fallback)

When CLI is not available, use `tfy-api.sh`. Set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

### Create SSH Server

```bash
TFY_API_SH=~/.claude/skills/truefoundry-ssh-server/scripts/tfy-api.sh

$TFY_API_SH PUT /api/svc/v1/apps -d '{
  "name": "my-ssh-server",
  "type": "ssh-server",
  "image": {
    "image_uri": "public.ecr.aws/truefoundrycloud/ssh-server:0.4.5-py3.12.12"
  },
  "home_directory_size": 20,
  "resources": {
    "node": {"type": "node_selector", "capacity_type": "on_demand"},
    "cpu_request": 1,
    "cpu_limit": 3,
    "memory_request": 4000,
    "memory_limit": 6000,
    "ephemeral_storage_request": 5000,
    "ephemeral_storage_limit": 10000
  },
  "workspace_fqn": "WORKSPACE_FQN"
}'
```

### GPU SSH Server (REST API)

```bash
$TFY_API_SH PUT /api/svc/v1/apps -d '{
  "name": "gpu-dev-server",
  "type": "ssh-server",
  "image": {
    "image_uri": "public.ecr.aws/truefoundrycloud/ssh-server:0.4.5-cu129-py3.12.12"
  },
  "home_directory_size": 20,
  "resources": {
    "node": {"type": "node_selector", "capacity_type": "on_demand"},
    "cpu_request": 4,
    "cpu_limit": 8,
    "memory_request": 16000,
    "memory_limit": 32000,
    "ephemeral_storage_request": 10000,
    "ephemeral_storage_limit": 20000,
    "devices": [
      {"type": "nvidia_gpu", "name": "A10_24GB", "count": 1}
    ]
  },
  "workspace_fqn": "WORKSPACE_FQN"
}'
```

## SSH Key Setup

### Prerequisites

You need an SSH key pair. Check for existing keys:

```bash
# macOS/Linux
cat ~/.ssh/id_rsa.pub

# Windows PowerShell
type $home\.ssh\id_rsa.pub
```

### Generate a New Key (if needed)

```bash
ssh-keygen -t rsa
```

### Add Key to SSH Server

Add your public key during deployment configuration (preferred). Avoid manual key-file edits unless strictly necessary.

> **Security:** SSH public keys authorize remote access to this container only. Never add keys you don't recognize. The user must confirm their public key before it is added. Each key grants full shell access to the deployed dev environment — not to the host machine or any other system.

Use the dashboard key-management flow so keys are audited and less likely to be misconfigured.

### Multi-User Access

For multi-user access, add each teammate key via the platform UI and review ownership before enabling access.

## VS Code Remote-SSH Setup

1. Install **Remote-SSH** extension in VS Code
2. Open Command Palette → "Remote-SSH: Connect to Host"
3. Enter the SSH connection string from TrueFoundry dashboard
4. Authenticate with your SSH key

### ProxyTunnel Installation

Required for SSH tunneling through TrueFoundry:

> **Security: Privileged Operations** — The `sudo` commands below install a networking tool on the user's local machine to enable SSH tunneling. The user should confirm they want to install this package before proceeding.

| Platform | Command |
|----------|---------|
| macOS | `brew install proxytunnel` |
| Ubuntu | Install `proxy-tunnel` with your distro package manager (run manually by a trusted admin) |
| Alternative | Use `nc` (netcat) for proxy without proxytunnel |

## File Transfer

### SCP (Secure Copy)

```bash
# Download from server
scp -r <deploymentName>:<remote-path> <local-path>

# Upload to server
scp -r <local-path> <deploymentName>:<remote-path>
```

### rsync (Incremental Sync)

```bash
# Upload
rsync -avz <local-path> <deploymentName>:<remote-path>

# Download
rsync -avz <deploymentName>:<remote-path> <local-path>
```

## Scale-to-Zero

SSH servers may auto-stop after inactivity to save costs.

**Activity detection**: Active SSH connections and foreground applications.
**Not detected**: Background processes.

Requires SSH server image v0.3.10+.

## Persistent Storage

- **Home directory** (`/home/jovyan/`) persists across restarts
- **APT packages** do NOT persist — use Build Scripts
- **Pip packages** in home directory persist
- **Conda environments** persist

## Custom Images

Extend TrueFoundry's SSH server images:

> **Security: Privileged Operations** — The Dockerfile commands below run as root during the container image build phase only (not on the user's local machine or the host system). The `USER root` / `USER jovyan` pattern is standard for installing system packages into a container image. Only install packages from trusted sources. Pin package versions where possible to prevent supply-chain attacks.

```dockerfile
FROM public.ecr.aws/truefoundrycloud/ssh-server:0.4.5-py3.12.12

USER jovyan

RUN python3 -m pip install --no-cache-dir torch numpy pandas
```

**Critical**: Do NOT modify ENTRYPOINT or CMD.

## Build Scripts

Install system packages through a reviewed image build process handled by your platform team instead of ad-hoc commands:

> **Security: Privileged Operations** — The `sudo` commands below run inside the deployed container (not on the user's local machine). The SSH server container requires package installation for system tooling. These commands do not affect the host system. The user must confirm they want these packages installed.

```bash
# Example: coordinate package additions through a reviewed Dockerfile PR.
```

## Python Environment Management

Create isolated environments:

```bash
conda create -y -n ml-env python=3.11
conda activate ml-env
pip install torch transformers
```

</instructions>

<success_criteria>

## Success Criteria

- The user can launch an SSH server on a specified TrueFoundry workspace
- The user can connect to the server via VS Code Remote-SSH or a standard SSH client
- The agent has configured SSH keys and verified connectivity
- The user can transfer files to and from the remote server
- The agent has set up auto-shutdown to avoid unnecessary costs
- The user can access GPU resources from the remote environment if requested

</success_criteria>

<references>

## Composability

- **Need workspace**: Use `workspaces` skill to find target workspace
- **Need GPU info**: Use `workspaces` skill to check available GPUs on cluster
- **Need persistent volumes**: Use `volumes` skill to create and mount storage
- **Deploy after development**: Use `deploy` or `llm-deploy` skill
- **Check status**: Use `applications` skill to see SSH server status

</references>

<troubleshooting>

## Error Handling

### CLI Errors

```
tfy: command not found
Install the TrueFoundry CLI:
  pip install 'truefoundry==0.5.0'
  tfy login --host "$TFY_BASE_URL"
```

```
Manifest validation failed.
Check:
- YAML syntax is valid
- Required fields: name, type, workspace_fqn
- Image URI exists and is accessible
- Resource values use correct units (memory in MB)
```

### Cannot Connect

```
SSH connection failed. Check:
- SSH key is correctly configured
- ProxyTunnel is installed (macOS: brew install proxytunnel)
- SSH server is in Running state (check applications skill)
- Network/VPN connectivity
```

### GPU Not Available

```
GPU not accessible. Verify:
- Requested GPU type is available on cluster (check workspaces skill)
- Used the correct SSH server image with CUDA support
```

### Server Stopped Unexpectedly

```
SSH server stopped. Possible causes:
- Auto-shutdown triggered (no active SSH connections)
- Check if auto-shutdown is configured on the server
- Resource limits exceeded (increase memory/CPU)
```

### REST API Fallback Errors

```
401 Unauthorized — Check TFY_API_KEY is valid
404 Not Found — Check TFY_BASE_URL and API endpoint path
422 Validation Error — Check manifest fields match expected schema
```

</troubleshooting>
