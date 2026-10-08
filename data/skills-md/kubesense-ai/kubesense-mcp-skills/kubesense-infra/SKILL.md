---
name: kubesense-infra
description: Inventory and topology of the monitored Kubernetes estate via KubeSense MCP — clusters, nodes, pods, workloads, detected issues, infra failures (OOM/CrashLoop/probe/scheduling), and recent deploys/scaling changes. Use for "what is running", "what is broken at the k8s layer", and "what changed".
metadata:
  version: "2.0.0"
  author: kubesense
  repository: https://github.com/kubesense-ai/kubesense-mcp-skills
  tags: kubesense,kubernetes,inventory,topology,pods,nodes,workloads,issues,oomkill,crashloop,changes,deploys
---

# KubeSense Infrastructure & Inventory

Telemetry tells you a service is unhealthy. These tools tell you **what exists**,
**what is failing at the Kubernetes layer**, and **what changed** — the context that
turns a symptom into a cause.

Requires the KubeSense MCP server. See **[kubesense-mcp](../kubesense-mcp/SKILL.md)**
for connection and auth.

## Routing — Read This First

| The user is asking… | Call | Not |
|---|---|---|
| "which clusters / what cluster names can I use?" | `list-clusters` | guessing a cluster name — every other tool's `clusters` filter is free-text with **no validation**, so a typo silently returns nothing |
| "what's running / how many pods / pod inventory" | `list-pods` | `search-logs` — logs only show pods that logged |
| "why is this pod restarting / crashlooping / OOMKilled" | `get-infra-issues` | `list-pods` (gives the restart *count*, not the *reason*) |
| "what changed / did someone deploy / why did it break at 14:00" | `get-recent-changes` | anything else — **check this first**, it is the cheapest root cause |
| "what's broken across the estate" | `list-issues` (platform's own detection) | re-deriving issues from raw traces |
| "node pressure / eviction / scheduling failures" | `list-nodes`, then `get-node-detail` | `analyze-metrics` (use it to confirm, not to discover) |
| "service health: RPS, p95, error rate per app" | `list-workloads` | `analyze-traces` (right answer for arbitrary slicing, overkill for a health sweep) |
| "container exit code / last state / restart reason" | `get-pod-detail` | `list-pods` |

**Discovery order.** `list-clusters` → `list-workloads` / `list-pods` → `get-*-detail`.
Names flow forward: never type a cluster, namespace, workload, or pod name you have
not read out of a previous call.

## Tools

| Tool | Purpose | Required args |
|---|---|---|
| `list-clusters` | Clusters this deployment monitors | — |
| `list-nodes` | Nodes with CPU/mem/disk pressure and readiness | — |
| `get-node-detail` | One node: conditions, taints, addresses, capacity | `name` |
| `list-pods` | Pods with phase, restarts, usage | — |
| `get-pod-detail` | One pod: container statuses, exit codes, last state, QoS | `name`, `namespace`, `cluster` |
| `list-workloads` | Workloads with golden signals (RPS, p95, error rate) | — |
| `get-workload-detail` | One workload: replicas, 4xx/5xx counts, RPS | `workload`, `namespace` |
| `list-issues` | Problems KubeSense already detected | — |
| `get-infra-issues` | K8s-layer failures: OOM, crashes, probes, scheduling, image pull | — |
| `get-recent-changes` | Image updates (deploys) and replica scaling | — |

Every tool defaults to **the last 1 hour** and **all accessible clusters**. Pass
`from_time`/`to_time` (RFC3339) to widen; pass `clusters` to narrow.

## list-clusters

Call this first when you need a cluster name. It is the *only* discovery for the
`clusters` filter that every other tool accepts.

```json
{ "search": "prod" }
```

Returns TSV: `name`, `source`, `env_type`, `updated_at`.

## Nodes

```json
{ "clusters": ["prod-us"], "sort_by": "memory_usage_precent", "sort_direction": "DESC" }
```

> [!WARNING]
> `sort_by` for nodes is spelled **`_precent`**, not `_percent` — the accepted values
> are `memory_usage_precent`, `disk_usage_precent`, `cpu_usage_precent`. The *output*
> columns use the correct spelling (`memory_usage_percent`). Passing `_percent` to
> `sort_by` does not sort.

Output: `name`, `cluster`, `ready`, `running_pods`, `cpu_usage_percent`,
`memory_usage_percent`, `disk_usage_percent`, `kubelet_version`, `instance_type`,
`uid`, `creation_timestamp`.

`get-node-detail` takes `name` (required) and optional `clusters` to disambiguate a
name present in several clusters. It returns conditions, addresses, labels, taints,
and capacity/usage as a record with `## conditions` / `## addresses` sub-tables.

## Pods

```json
{ "namespace": "production", "status": "Pending", "sort_by": "memory_usage", "sort_direction": "DESC" }
```

- `status` filters on pod **phase**: `Running`, `Pending`, `Failed`, `Succeeded`, `Unknown`.
- `sort_by` accepts `memory_usage` or `cpu_usage` only.

Output: `name`, `namespace`, `cluster`, `status`, `owner_kind`, `owner`, `node`,
`restarts`, `cpu_usage`, `memory_usage`, `creation_time`.

`get-pod-detail` needs **all three** of `name`, `namespace`, `cluster`. It is the tool
that answers *why* a pod restarted — container statuses carry the restart reason, exit
code, and last terminated state, which `list-pods` does not.

## Workloads

The application-level view — one row per Deployment/StatefulSet/DaemonSet with its
golden signals already joined from traces.

```json
{ "namespace": "production", "kind": "Deployment", "sort_by": "error_rate", "sort_direction": "DESC" }
```

`sort_by` accepts `rps`, `p95`, `errors`, `error_rate`, `restarts`.

Output: `name`, `namespace`, `cluster`, `kind`, `ready`, `desired`, `restarts`, `rps`,
`p95`, `error_rate`, `issue_count`, `service_protocols`.

Use this for a **health sweep** — it is one call for what would otherwise be an
`analyze-traces` per workload. Drop to `analyze-traces` when you need a slice the
summary doesn't have (by endpoint, by status code, by attribute).

## list-issues

KubeSense's own issue detection — errors, latency, and connectivity problems between
workloads. Prefer it over re-deriving problems from raw telemetry.

Output: `issue_id`, `kind`, `cluster`, `primary_workload`, `primary_namespace`,
`associate_workload`, `issue_reason`, `return_code`, `subtype`, `sum_issue_count`,
`max_last_seen`.

`associate_workload` is the *other* side of a connectivity issue — the dependency that
`primary_workload` failed to reach.

## get-infra-issues

Kubernetes-layer **failures**, from cluster events. This is the OOM / CrashLoop /
probe-failure tool.

```json
{ "namespace": "production", "workload": "checkout", "reason": "OOMKilling" }
```

Known `reason` values: `OOMKilling`, `BackOff`, `Unhealthy`, `FailedScheduling`,
`FailedMount`, `ImagePullBackOff`, `NodeNotReady`. **Omit `reason` to see all failure
modes** — narrow only once you know which one you're chasing.

Output: `reason`, `type`, `workload`, `object`, `namespace`, `exit_code` (crashes only),
`message`, `count`, `last_seen`. Defaults to limit 50, max 200.

**Layer routing:** infra failures → this tool. Application errors and latency →
`analyze-traces` / `search-traces`. What changed → `get-recent-changes`.

## get-recent-changes

Image updates (deploys) and replica scaling, from cluster events. **Usually the first
thing to check in any investigation** — "what changed right before it broke" is the
cheapest hypothesis you will test.

```json
{ "namespace": "production", "workload": "checkout", "kind": "image_update" }
```

`kind` is `image_update` or `scaling`; omit for both. Output: `kind`, `workload`,
`namespace`, `object`, `detail`, `when` — where `detail` reads like
`kubesense: dev-v1.2.1279 -> dev-v1.2.1280` or `replicas 1 -> 0`. Defaults to limit 50,
max 200.

Scope with `namespace` + `workload`. Both are optional but strongly recommended — an
unscoped call across a busy cluster returns mostly noise.

## Investigation Pattern

Symptom → context → cause, cheapest signal first:

```
1. get-recent-changes    namespace+workload → did we just deploy or scale?
2. get-infra-issues      same scope        → is the platform killing it (OOM, probes, sched)?
3. list-pods / get-pod-detail               → restart counts, exit codes, last state
4. analyze-traces / search-logs              → application-level errors and latency
5. analyze-metrics                           → confirm resource pressure quantitatively
```

Steps 1–2 are two cheap calls that resolve a large share of incidents outright. Reach
for telemetry once they come back clean.

## Rules

1. **`list-clusters` before any `clusters` filter.** The filter is unvalidated free
   text — a wrong name returns an empty result that looks exactly like "no data".
2. Names flow forward from list → detail calls. Never invent a pod, node, workload, or
   namespace name.
3. `get-pod-detail` requires `name` + `namespace` + `cluster`; `get-workload-detail`
   requires `workload` + `namespace`. Discover them with the matching `list-*` call.
4. Node `sort_by` uses the misspelling `_precent`; output columns use `_percent`.
5. Prefer `list-issues` / `get-infra-issues` over re-deriving problems from raw
   telemetry — the platform already did the detection.
6. Scope `get-recent-changes` and `get-infra-issues` with `namespace` + `workload`;
   unscoped calls are noisy.
7. Default window is 1 hour. If a result set looks empty, widen the window before
   concluding nothing happened.
