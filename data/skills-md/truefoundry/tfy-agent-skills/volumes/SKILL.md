---
name: volumes
description: Creates and manages persistent volumes on TrueFoundry. Handles creation, listing, mounting, storage class selection, and static volume attachment.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# Volumes

Create and manage persistent volumes on TrueFoundry. Volumes provide shared, low-latency disk storage that persists across container restarts and can be mounted by multiple pods.

## When to Use

Create, list, or mount persistent volumes on TrueFoundry, including dynamic provisioning, static PV attachment, storage class selection, and Volume Browser setup.

## When NOT to Use

- User needs large archival storage or global access -> suggest blob storage (S3/GCS) instead
- User wants ephemeral scratch space -> use `ephemeral_storage` in resource config
- User wants to deploy an app -> prefer `deploy` skill; ask if the user wants another valid path
- User wants to manage secrets -> prefer `secrets` skill; ask if the user wants another valid path

</objective>

<context>

## Volumes vs Blob Storage

Help the user choose the right storage type:

| Aspect | Volumes | Blob Storage (S3/GCS) |
|--------|---------|----------------------|
| **Access method** | Standard file system APIs (open, read, write) | SDK clients (boto3, gcsfs) |
| **Speed** | Faster (local-disk latency) | Slower (network round-trips) |
| **Durability** | High | Extremely high (11 nines) |
| **Cost** | Higher per GB | Lower per GB |
| **Scope** | Region/cluster limited | Global access |
| **Best for** | Shared model weights, training checkpoints, low-latency reads | Large archives, datasets accessed infrequently, cross-region data |

**Choose volumes when:**
- Multiple pods need concurrent file system access to the same data
- You need file system semantics (locking, renaming, directory listing)
- Low-latency access to frequently-read data (model weights, config files)
- ML training checkpointing where write speed matters

**Choose blob storage when:**
- Data is larger than a few hundred GB
- Global or cross-region access is needed
- Data is written once and read occasionally
- Cost is the primary concern

**Warning:** Do not write to the same file path from multiple pods simultaneously -- this can cause data corruption. Coordinate writes across pods or use separate paths.

## Prerequisites

**Always verify before deploying:**

1. **Credentials** -- `TFY_BASE_URL` and `TFY_API_KEY` must be set (env or `.env`)
2. **Workspace** -- `TFY_WORKSPACE_FQN` required. **Never auto-pick. Ask the user if missing.** Volumes are workspace-scoped: a volume created in one workspace can only be used by applications in that same workspace.
3. **Cluster storage class** -- The target cluster must have a storage provisioner configured for the desired storage class.

For credential check commands and .env setup, see `references/prerequisites.md`.

## Volume Types

### Dynamic Volumes (Create New)

TrueFoundry provisions a new Kubernetes PersistentVolumeClaim (PVC). You specify size and storage class; the cluster allocator handles the rest.

**Key properties:**
- Size is expandable after creation but **cannot be reduced**
- Access mode is `ReadWriteMany` (multiple pods can mount simultaneously)
- Reclaim policy is `Retain` (data persists even if the volume resource is deleted from TrueFoundry)

### Static Volumes (Use Existing)

Mount a pre-existing Kubernetes PersistentVolume by name. Use this for:
- **AWS EFS** -- Elastic File System via `efs.csi.aws.com` driver
- **AWS S3** -- S3 buckets via `s3.csi.aws.com` driver
- **GCP Filestore / GCS** -- via `gcsfuse.csi.storage.gke.io` driver
- **Azure Files / Azure Blob** -- via `file.csi.azure.com` or `blob.csi.azure.com` drivers

Static volumes require the PersistentVolume to already exist in the Kubernetes cluster. See the "Static Volume Setup" section below.

## Storage Classes by Cloud Provider

For storage class tables by cloud provider (AWS, GCP, Azure) and discovery commands, see `references/volume-storage-classes.md`.

</context>

<instructions>

## Creating a Volume

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

### Before Creating

**ALWAYS ask the user these questions in order:**

1. **Volume type** -- "Do you want to create a new volume or use an existing Kubernetes PersistentVolume?"
   - **Create new** → proceed with dynamic volume questions below
   - **Use existing** → ask for the PersistentVolume name in Kubernetes, then skip to workspace
2. **Volume name** -- What should the volume be called?
3. **Size** -- How much storage? (integer in GB, e.g. `50`). Cannot be reduced later.
4. **Storage class** -- Which storage class? Present available options from the cluster.
5. **Workspace** -- Which workspace? Volumes are workspace-scoped.
6. **Volume Browser** -- "Do you want to enable Volume Browser? It provides a web UI to browse and manage files in your volume without SSH." (Optional)
   - If yes, ask for:
     - **Endpoint host** -- The hostname where the browser will be accessible (e.g. `my-cluster.example.truefoundry.com`). Present available hosts from the cluster's base domain.
     - **Endpoint path** -- URL path prefix (optional, defaults to `/`)
     - **Username** -- Login username for the browser (optional, defaults to `admin`)
     - **Password secret** -- FQN of a TrueFoundry secret containing the browser password. If user doesn't have one, help them create it using the `secrets` skill first.

Present a summary and ask for confirmation:

```
Volume to create:
  Type:          Create new (dynamic)
  Name:          training-data
  Size:          100 GB
  Storage class: efs-sc
  Workspace:     my-cluster:my-workspace
  Volume Browser: Enabled
    Endpoint:    https://my-cluster.example.truefoundry.com/training-data/
    Username:    admin
    Password:    (secret: my-cluster:my-workspace:vol-browser-pw)

Note: Size can be expanded later but not reduced.
Proceed?
```

For volumes without Volume Browser:
```
Volume to create:
  Type:          Create new (dynamic)
  Name:          training-data
  Size:          100 GB
  Storage class: efs-sc
  Workspace:     my-cluster:my-workspace
  Volume Browser: Disabled

Note: Size can be expanded later but not reduced.
Proceed?
```

### Via Tool Call

```
tfy_applications_create_deployment(
    manifest={"type": "volume", "name": "my-volume", "config": {"type": "dynamic", "size": 100, "storage_class": "efs-sc"}},
    options={"workspace_id": "ws-id-here"}
)
```

For Volume Browser fields and static volume tool-call examples, use the same fields as the Direct API examples below.

### Via Direct API

**Create new volume (without Volume Browser):**

```bash
$TFY_API_SH PUT /api/svc/v1/apps '{
  "manifest": {
    "type": "volume",
    "name": "my-volume",
    "config": {
      "type": "dynamic",
      "size": 100,
      "storage_class": "efs-sc"
    }
  },
  "workspaceId": "ws-id-here"
}'
```

**Create new volume (with Volume Browser):**

```bash
$TFY_API_SH PUT /api/svc/v1/apps '{
  "manifest": {
    "type": "volume",
    "name": "my-volume",
    "config": {
      "type": "dynamic",
      "size": 100,
      "storage_class": "efs-sc"
    },
    "volume_browser": {
      "username": "admin",
      "password_secret_fqn": "my-cluster:my-workspace:vol-browser-pw",
      "endpoint": {
        "host": "my-cluster.example.truefoundry.com",
        "path": "/my-volume/"
      }
    }
  },
  "workspaceId": "ws-id-here"
}'
```

### Using an Existing Kubernetes PersistentVolume

```bash
$TFY_API_SH PUT /api/svc/v1/apps '{
  "manifest": {
    "type": "volume",
    "name": "my-existing-vol",
    "config": {
      "type": "static",
      "persistent_volume_name": "pv-name-in-k8s"
    }
  },
  "workspaceId": "ws-id-here"
}'
```

## Listing Volumes

### Via Tool Call

```
tfy_applications_list(filters={"workspace_fqn": "my-cluster:my-workspace", "application_type": "volume"})
```

### Via Direct API

```bash
# List volumes in a workspace
$TFY_API_SH GET '/api/svc/v1/apps?workspaceFqn=my-cluster:my-workspace&applicationType=volume'

# Get a specific volume by ID
$TFY_API_SH GET /api/svc/v1/apps/VOLUME_APP_ID
```

### Presenting Volumes

```
Volumes in my-cluster:my-workspace:
| Name           | Size   | Storage Class | Status   | Created            |
|----------------|--------|---------------|----------|--------------------|
| training-data  | 100Gi  | efs-sc        | RUNNING  | 2026-02-10 14:30   |
| model-cache    | 50Gi   | premium-rwx   | RUNNING  | 2026-02-08 09:15   |
```

## Attaching Volumes to Services and Jobs

Volumes are mounted into containers at a specified path. The volume must be in the same workspace as the application.

### SDK (in deploy.py)

```python
from truefoundry.deploy import Service, VolumeMount

service = Service(
    name="my-service",
    # ... image, ports, resources ...
    mounts=[
        VolumeMount(
            mount_path="/data",
            volume_fqn="my-cluster:my-workspace:my-volume",
        ),
    ],
)
```

### API Manifest (Service)

```json
{
  "manifest": {
    "kind": "Service",
    "name": "my-service",
    "image": {"type": "image", "image_uri": "my-image:latest"},
    "mounts": [
      {
        "type": "volume",
        "mount_path": "/data",
        "volume_fqn": "my-cluster:my-workspace:my-volume"
      }
    ],
    "resources": {
      "cpu_request": 0.5, "cpu_limit": 1.0,
      "memory_request": 512, "memory_limit": 1024
    }
  },
  "workspaceId": "ws-id-here"
}
```

### API Manifest (Job)

```json
{
  "manifest": {
    "kind": "Job",
    "name": "my-training-job",
    "image": {"type": "image", "image_uri": "my-training:latest"},
    "mounts": [
      {
        "type": "volume",
        "mount_path": "/data",
        "volume_fqn": "my-cluster:my-workspace:training-data"
      },
      {
        "type": "volume",
        "mount_path": "/checkpoints",
        "volume_fqn": "my-cluster:my-workspace:checkpoint-vol"
      }
    ],
    "resources": {
      "cpu_request": 4.0, "cpu_limit": 8.0,
      "memory_request": 16384, "memory_limit": 32768
    }
  },
  "workspaceId": "ws-id-here"
}
```

### Volume FQN Format

The volume FQN follows the pattern: `{cluster}:{workspace}:{volume-name}`

Example: `my-cluster:my-workspace:training-data`

## LLM Cache Volumes

For LLM deployments, TrueFoundry supports a `cache_volume` shorthand that creates a volume for model weight caching. This avoids re-downloading large models on every pod restart. See the `llm-deploy` skill for details.

```yaml
# In LLM deployment manifest
cache_volume:
  cache_size: 50
  storage_class: efs-sc
```

## Volume Sizing Guidelines

| Use Case | Recommended Size | Notes |
|----------|-----------------|-------|
| Small model cache (< 7B params) | 20-50 Gi | 2x the model size in FP16 |
| Large model cache (7B-70B params) | 50-200 Gi | 2x the model size; account for multiple formats |
| Shared training dataset | 50-500 Gi | Depends on dataset size; leave 20% headroom |
| Checkpointing | 20-100 Gi | Depends on checkpoint frequency and model size |
| General shared storage | 10-50 Gi | Start small, expand as needed |

**Sizing tips:**
- Always add 20% headroom above your expected data size
- Volume size can be expanded later but **never reduced** -- start conservatively if unsure
- For model caching, use 2x the model's disk size to account for download + extraction
- Monitor volume usage after deployment and expand proactively before hitting limits

## Static Volume Setup

For detailed setup instructions for AWS EFS, AWS S3, GCP GCS Fuse, and Azure Files/Blob, see `references/static-volume-setup.md`.

## Volume Browser

For Volume Browser configuration fields, setup steps, and access instructions, see `references/volume-browser-setup.md`.

</instructions>

<success_criteria>

- The agent asked "create new or use existing?" before proceeding
- The agent has confirmed volume name, size, storage class, and workspace with the user before creating
- The agent asked whether to enable Volume Browser and collected endpoint/password details if yes
- The volume was successfully created and is in RUNNING status
- The user can list all volumes in their target workspace
- The user can attach the volume to a service or job using the correct volume FQN
- The agent has advised on appropriate sizing based on the user's use case
- The user understands the difference between volumes and blob storage for their scenario

</success_criteria>

<references>

## Composability

- **Before deploying with volumes**: Use `workspaces` skill to get workspace FQN, then create the volume in the same workspace
- **With secrets skill**: Create a password secret before enabling Volume Browser (password_secret_fqn is required)
- **With deploy skill**: After creating a volume, add `VolumeMount` to the service's deploy.py to attach it
- **With llm-deploy skill**: Use `cache_volume` in LLM deployment manifests for model weight caching
- **With jobs skill**: Mount volumes to training jobs for checkpointing and shared data access
- **With applications skill**: List volumes alongside other application types to see what storage exists
- **After creating**: Use `applications` skill to verify the volume was created successfully

</references>

<troubleshooting>

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Volume not found | Wrong name or workspace | Verify FQN; volumes are workspace-scoped |
| Storage class not available | Cluster missing provisioner | Check `GET /api/svc/v1/clusters/CLUSTER_ID` for available classes |
| Size cannot be reduced | PVC limitation | Create new smaller volume and migrate data |
| Workspace mismatch | Volume in different workspace | Create volume in same workspace as the app |
| Permission denied | API key lacks access | Check API key permissions for this workspace |
| PV not found (static) | K8s PV doesn't exist | Verify with `kubectl get pv <pv-name>` |
| Data corruption | Multiple pods writing same path | Use per-pod sub-directories (e.g., `/data/pod-{POD_NAME}/`) |

</troubleshooting>
