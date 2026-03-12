---
name: workspaces
description: Lists TrueFoundry workspaces and clusters. Provides workspace FQNs for deployment, cluster connectivity status, available GPU types, and base domains.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# Workspaces & Clusters

List TrueFoundry workspaces and clusters. Workspaces are the deploy targets; clusters are the underlying infrastructure.

## When to Use

List workspaces and clusters, find workspace FQNs for deployment, check cluster connectivity, or discover available GPU types and base domains.

</objective>

<instructions>

## Execution Priority

For simple read/list operations in this skill, always use MCP tool calls first:
- `tfy_clusters_list`
- `tfy_workspaces_list`

If tool calls are unavailable because the MCP server is not configured, or a tool is missing, fall back automatically to direct API via `tfy-api.sh`.

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

## Recommended Flow: Cluster → Workspace

**Never ask users to set `TFY_CLUSTER_ID` manually.** Instead, list clusters and let the user pick — then filter workspaces by that cluster.

### Step 1: List Clusters

```
# Via Tool Call
tfy_clusters_list()

# Via Direct API
$TFY_API_SH GET /api/svc/v1/clusters
```

Present as a table and ask the user to pick one:

```
Clusters:
| Name             | ID               | Connected |
|------------------|------------------|-----------|
| prod-cluster     | prod-cluster     | Yes       |
| dev-cluster      | dev-cluster      | Yes       |

Which cluster would you like to use?
```

### Step 2: List Workspaces (Filtered by Cluster)

Once the user picks a cluster, list workspaces filtered to that cluster:

```
# Via Tool Call
tfy_workspaces_list(filters={"cluster_id": "selected-cluster-id"})

# Via Direct API
$TFY_API_SH GET '/api/svc/v1/workspaces?clusterId=SELECTED_CLUSTER_ID'
```

Present as a table and ask the user to pick one:

```
Workspaces in prod-cluster:
| Name       | FQN                        |
|------------|----------------------------|
| dev-ws     | prod-cluster:dev-ws        |
| staging-ws | prod-cluster:staging       |

Which workspace would you like to use?
```

**Key field**: `fqn` — this is what `TFY_WORKSPACE_FQN` needs for deploy.

### Shortcut: If Only One Cluster

If the user has access to only one cluster, skip the cluster selection step — go straight to listing workspaces.

## List All Workspaces (Unfiltered)

```
# Via Tool Call
tfy_workspaces_list()

# Via Direct API
$TFY_API_SH GET /api/svc/v1/workspaces
```

## Get Specific Workspace

```bash
# Via Tool Call
tfy_workspaces_list(workspace_id="ws-id-here")

# Via API
$TFY_API_SH GET /api/svc/v1/workspaces/WORKSPACE_ID
```

## Get Cluster Details

```
# Via Tool Call
tfy_clusters_list(cluster_id="cluster-id")  # with status + addons

# Via Direct API
$TFY_API_SH GET /api/svc/v1/clusters/CLUSTER_ID
$TFY_API_SH GET /api/svc/v1/clusters/CLUSTER_ID/is-connected
$TFY_API_SH GET /api/svc/v1/clusters/CLUSTER_ID/get-addons
```

## Cluster Base Domains (for Public URLs)

When a user wants to expose a service publicly, you need the cluster's base domains to construct a valid hostname. Invalid hosts cause deploy failures. See `references/cluster-discovery.md` for how to look up base domains, extract cluster ID from workspace FQN, and construct public URLs.

## Available GPU Types

When a user needs GPU resources, discover what's available on the cluster before offering options.

### How to Discover

**Option A: Check cluster addons/node pools**
```bash
$TFY_API_SH GET /api/svc/v1/clusters/CLUSTER_ID/get-addons
```

**Option B: The SDK/API error message tells you**

If you deploy with an unsupported GPU type, the error message lists all valid ones:
```
"None of the nodepools support A10G. Valid devices are [T4, A10_4GB, A10_8GB, A10_12GB, A10_24GB, H100_94GB]"
```

**Not all types are available on every cluster.** Always check before presenting options to the user.

For the full GPU type reference table and SDK usage examples, see `references/gpu-reference.md`.

</instructions>

<success_criteria>

- The user can see a formatted table of available workspaces with their FQNs
- The agent has identified the correct workspace FQN for the user's intended deployment target
- The user can see cluster connectivity status and available infrastructure
- The agent has discovered and presented available GPU types if the user needs GPU resources
- The user has the cluster base domain if they need to expose a service publicly

</success_criteria>

<references>

## Composability

- **Need workspace for deploy**: Use this skill first, then `deploy` skill with the `fqn`
- **Need cluster for filtering**: Pass `cluster_id` to workspaces or applications
- **Check infra status**: Get cluster + addons for monitoring

</references>

<troubleshooting>

## Error Handling

### No Workspaces Found
```
No workspaces found. Check:
- The selected cluster may not have any workspaces
- Your API key may not have access to this cluster
- Try listing clusters first to pick a different one
```

### Permission Denied
```
Cannot list workspaces. Your API key may lack workspace permissions.
```

</troubleshooting>
