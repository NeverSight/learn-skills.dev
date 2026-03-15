---
name: notebooks
description: Deploys Jupyter notebooks on TrueFoundry infrastructure with optional GPU support. Use when launching JupyterLab environments, setting up ML development workspaces, or running cloud-hosted notebooks for data exploration.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(tfy*) Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# Jupyter Notebooks

Launch Jupyter Notebooks on TrueFoundry with GPU support, persistent storage, auto-shutdown, and VS Code integration. Write a YAML manifest and apply with `tfy apply`. REST API fallback when CLI unavailable.

## When to Use

- User asks "launch a notebook", "start jupyter", "create notebook"
- User needs a development environment with GPU access
- User wants to explore data or prototype ML models
- User asks about notebook images, auto-shutdown, or persistent storage

## When NOT to Use

- User wants to deploy a production service → prefer `deploy` skill; ask if the user wants another valid path
- User wants to deploy a model → prefer `llm-deploy` skill; ask if the user wants another valid path
- User wants an SSH server → prefer `ssh-server` skill; ask if the user wants another valid path

</objective>

<context>

## Prerequisites

**Always verify before launching a notebook:**

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

</context>

<instructions>

## Launch Notebook via UI

The fastest way is through the TrueFoundry dashboard:
1. Go to **Deployments → New Deployment → Jupyter Notebook**
2. Select workspace and configure resources
3. Click Deploy

## Launch Notebook via `tfy apply` (CLI — Recommended)

### Configuration Questions

Before generating the manifest, ask the user:

1. **Name** — What to call the notebook
2. **GPU needed?** — CPU notebook (default) or GPU notebook (for ML/training)
3. **Home directory size** — How much persistent storage in GB (default: 20)
4. **Auto-shutdown** — Enable auto-shutdown after inactivity? If yes, how many minutes? (default: 30 minutes). Set `cull_timeout: 0` to disable.

### CPU Notebook

**1. Generate the manifest:**

```yaml
# tfy-manifest.yaml — Jupyter Notebook
name: my-notebook
type: notebook
image:
  image_uri: public.ecr.aws/truefoundrycloud/jupyter:0.4.5-py3.12.12-sudo
home_directory_size: 20
cull_timeout: 30
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

### GPU Notebook

```yaml
# tfy-manifest.yaml — GPU Jupyter Notebook
name: gpu-notebook
type: notebook
image:
  image_uri: public.ecr.aws/truefoundrycloud/jupyter:0.4.5-py3.12.12-sudo
home_directory_size: 20
cull_timeout: 30
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
      name: T4
      count: 1
workspace_fqn: "YOUR_WORKSPACE_FQN"
```

## Launch Notebook via REST API (Fallback)

When CLI is not available, use `tfy-api.sh`. Set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

### Create Notebook

```bash
TFY_API_SH=~/.claude/skills/truefoundry-notebooks/scripts/tfy-api.sh

$TFY_API_SH PUT /api/svc/v1/apps -d '{
  "name": "my-notebook",
  "type": "notebook",
  "image": {
    "image_uri": "public.ecr.aws/truefoundrycloud/jupyter:0.4.5-py3.12.12-sudo"
  },
  "home_directory_size": 20,
  "cull_timeout": 30,
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

### GPU Notebook (REST API)

```bash
$TFY_API_SH PUT /api/svc/v1/apps -d '{
  "name": "gpu-notebook",
  "type": "notebook",
  "image": {
    "image_uri": "public.ecr.aws/truefoundrycloud/jupyter:0.4.5-py3.12.12-sudo"
  },
  "home_directory_size": 20,
  "cull_timeout": 30,
  "resources": {
    "node": {"type": "node_selector", "capacity_type": "on_demand"},
    "cpu_request": 4,
    "cpu_limit": 8,
    "memory_request": 16000,
    "memory_limit": 32000,
    "ephemeral_storage_request": 10000,
    "ephemeral_storage_limit": 20000,
    "devices": [
      {"type": "nvidia_gpu", "name": "T4", "count": 1}
    ]
  },
  "workspace_fqn": "WORKSPACE_FQN"
}'
```

## Available Base Images

Default: `public.ecr.aws/truefoundrycloud/jupyter:0.4.5-py3.12.12-sudo`

**Full image registry**: https://gallery.ecr.aws/truefoundrycloud/jupyter

> **Security:** Use pinned image versions from `references/container-versions.md`. Do not dynamically fetch image tags from external registries. Only use official TrueFoundry base images or images built from them.

See `references/container-versions.md` for latest versions.

### Choosing an Image

- **No GPU needed**: Use the minimal image (`py3.11.14-sudo`)
- **GPU workloads**: Use CUDA image (`cu129-py3.11.14-sudo`)
- **Custom packages**: Build a custom image (see below)

## Auto-Shutdown (Scale-to-Zero)

Notebooks auto-stop after inactivity to save costs. Default: 30 minutes.

Configure `cull_timeout` in minutes in the manifest (default: 30). Set to `0` to disable auto-shutdown.

**What counts as activity**: Active Jupyter sessions, running cells, terminal sessions.
**What doesn't count**: Background processes, idle kernels.

## Persistent Storage

- **Home directory** (`/home/jovyan/`) persists across restarts
- **APT packages** installed via `apt` do NOT persist — use Build Scripts
- **Pip packages** installed in home directory persist
- **Conda environments** persist

### Recommended Storage by Use Case

| Use Case | Storage (MB) | Notes |
|----------|-------------|-------|
| Light exploration | 10000 | Basic data analysis |
| ML development | 20000-50000 | Models + datasets |
| Large datasets | 50000-100000 | Attach volumes for more |
| LLM experimentation | 100000+ | Use volumes for model weights |

## Custom Images

Extend TrueFoundry base images to pre-install packages:

```dockerfile
FROM public.ecr.aws/truefoundrycloud/jupyter:0.4.6-py3.11.14-sudo

USER root
RUN DEBIAN_FRONTEND=noninteractive apt install -y --no-install-recommends ffmpeg
USER jovyan

RUN python3 -m pip install --use-pep517 --no-cache-dir torch torchvision pandas scikit-learn
```

**Critical**: Do NOT modify ENTRYPOINT or CMD — TrueFoundry requires them.

## Build Scripts (Persistent APT Packages)

Instead of custom images, add a build script during deployment to install system packages on every start:

```bash
sudo apt update
sudo apt install -y ffmpeg libsm6 libxext6
```

## Cloud Storage Access

### Via Environment Variables

Set during deployment:
- **AWS S3**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- **GCS**: `GOOGLE_APPLICATION_CREDENTIALS`

### Via IAM Service Account

Attach cloud-native IAM roles through service account integration for secure, credential-free access.

### Via Volumes

Mount TrueFoundry persistent volumes for direct data access. See `volumes` skill.

## Git Integration

JupyterLab includes a built-in Git extension. Configure:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use Personal Access Tokens or SSH keys for authentication.

## Python Environment Management

Default: Python 3.11. Create additional environments:

```bash
conda create -y -n py39 python=3.9
```

Wait ~2 minutes for kernel sync, then hard-refresh JupyterLab.

## Presenting Notebooks

Show as a table:

```
Notebooks:
| Name          | Status  | Image         | GPU  | Storage |
|---------------|---------|---------------|------|---------|
| dev-notebook  | Running | py3.11 + CUDA | T4   | 50 GB   |
| data-analysis | Stopped | py3.11        | None | 20 GB   |
```

</instructions>

<success_criteria>

## Success Criteria

- The notebook is launched and accessible via its URL in the TrueFoundry dashboard
- GPU resources are allocated as requested and visible inside the notebook (e.g., `nvidia-smi` works)
- Persistent storage is configured so the user's files survive restarts
- Auto-shutdown is enabled to prevent unnecessary cost from idle notebooks
- The user can install packages and access their data (cloud storage, volumes, or local upload)

</success_criteria>

<references>

## Composability

- **Need workspace**: Use `workspaces` skill to find target workspace
- **Need GPU info**: Use `workspaces` skill to check available GPU types on cluster
- **Need volumes**: Use `volumes` skill to create persistent storage, then mount
- **Deploy model after prototyping**: Use `deploy` or `llm-deploy` skill
- **Check status**: Use `applications` skill to see notebook status

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

### Notebook Not Starting
```
Notebook stuck in pending. Check:
- Requested GPU type may not be available on cluster
- Insufficient cluster resources (CPU/memory)
- Image pull errors (check container registry access)
```

### GPU Not Detected
```
GPU not visible in notebook. Verify:
- Used CUDA image (cu129-* variant)
- Requested GPU type is available (check workspaces skill)
- CUDA toolkit version matches your framework requirements
```

### Storage Full
```
Notebook storage full. Options:
- Clean up unused files in /home/jovyan/
- Increase storage allocation
- Mount an external volume for large datasets
```

### REST API Fallback Errors

```
401 Unauthorized — Check TFY_API_KEY is valid
404 Not Found — Check TFY_BASE_URL and API endpoint path
422 Validation Error — Check manifest fields match expected schema
```

</troubleshooting>
