---
name: fossflow-diagrams
description: Use when creating isometric architecture diagrams, infrastructure visualizations, system topology diagrams, or when the user mentions FossFLOW, Isoflow, or asks for isometric diagram JSON output
---

# FossFLOW Isometric Diagrams

## Overview

Generate isometric architecture diagrams using the **FossFLOW/Isoflow compact JSON format**. This format uses minified keys for token efficiency while producing valid importable diagrams.

**Iron Rule:** The compact format structure defined in `llm-generation-guide.md` (in this skill directory) is the ONLY valid output format. No variations, no "improved" formats, no object-based alternatives. The exact structure must be respected at all costs.

**Canonical reference:** https://raw.githubusercontent.com/stan-smith/FossFLOW/refs/heads/master/LLM-GENERATION-GUIDE.md

## When to Use

- User asks for an architecture diagram, infrastructure diagram, or system topology
- User mentions FossFLOW, Isoflow, or isometric diagrams
- User wants to visualize cloud infrastructure (AWS, Azure, GCP)
- User wants to visualize Kubernetes deployments
- User wants a visual representation of microservices, data pipelines, or any system architecture

**When NOT to use:** For UML diagrams, sequence diagrams, flowcharts, or non-isometric visualizations (use Mermaid or PlantUML instead).

## The Compact Format - MANDATORY Structure

```json
{
  "t": "Title (max 40 chars)",
  "i": [
    ["Item Name (max 30)", "icon_id", "Description (max 100)"]
  ],
  "v": [
    [
      [[itemIndex, x, y], ...],
      [[fromIndex, toIndex], ...]
    ]
  ],
  "_": { "f": "compact", "v": "1.0" }
}
```

### Keys Explained

| Key | Meaning | Type | Constraint |
|-----|---------|------|------------|
| `t` | Title | string | max 40 chars |
| `i` | Items | array of 3-element arrays | `["name", "icon", "desc"]` |
| `v` | Views | array of `[positions, connections]` | Usually 1 view |
| `_` | Metadata | object | **Exactly** `{"f": "compact", "v": "1.0"}` |

### Items (`i`) - Each item is a 3-element array

```
["Display Name", "icon_id", "Brief description"]
     ^max 30        ^valid      ^max 100
```

### Views (`v`) - Each view is a 2-element array

```
[
  [[0, x0, y0], [1, x1, y1], ...],   // positions: [itemIndex, x, y]
  [[0, 1], [1, 2], ...]               // connections: [fromIndex, toIndex]
]
```

## Red Flags - STOP and Fix

If you catch yourself doing ANY of these, delete and start over:

- Using object syntax for items (`{id: ..., type: ...}`) instead of arrays
- Using string references in connections (`"from": "lb-1"`) instead of integer indices
- Adding keys not in the spec (`version`, `components`, `connections` at root)
- Putting positions inside item definitions instead of in the views array
- Using 3D coordinates `[x, y, z]` - positions are `[itemIndex, x, y]`
- Inventing icon names not in the valid icons list
- Omitting the `_` metadata field
- Using `"v": "1.0"` without the enclosing `"_": { "f": "compact", ... }`

## Valid Icons - Quick Reference

### Generic (Isoflow collection)
`storage` `server` `user` `cloud` `network` `security` `api` `queue` `cache` `function` `mobile` `web` `email` `analytics` `backup` `load-balancer` `cdn` `vpn` `firewall` `monitor`

### AWS (prefix: `aws-`)
`aws-ec2` `aws-s3` `aws-rds` `aws-lambda` `aws-api-gateway` `aws-cloudfront` `aws-route-53` `aws-vpc` `aws-elb` `aws-iam` `aws-cloudwatch` `aws-sns` `aws-sqs` `aws-dynamodb` `aws-elasticsearch` `aws-redshift` `aws-kinesis` `aws-eks` `aws-fargate` `aws-cognito`

### Azure (prefix: `azure-`)
`azure-virtual-machine` `azure-storage-account` `azure-sql-database` `azure-app-service` `azure-function-app` `azure-api-management` `azure-cdn` `azure-dns` `azure-load-balancer` `azure-active-directory` `azure-monitor` `azure-service-bus` `azure-cosmos-db` `azure-redis-cache` `azure-kubernetes-service` `azure-container-instances` `azure-logic-apps` `azure-data-factory` `azure-key-vault` `azure-cognitive-services`

### GCP (prefix: `gcp-`)
`gcp-compute-engine` `gcp-cloud-storage` `gcp-cloud-sql` `gcp-app-engine` `gcp-cloud-functions` `gcp-api-gateway` `gcp-cloud-cdn` `gcp-cloud-dns` `gcp-cloud-load-balancing` `gcp-identity-access-management` `gcp-cloud-monitoring` `gcp-cloud-pub-sub` `gcp-cloud-firestore` `gcp-memorystore` `gcp-kubernetes-engine` `gcp-cloud-run` `gcp-cloud-workflows` `gcp-cloud-dataflow` `gcp-secret-manager` `gcp-ai-platform`

### Kubernetes (prefix: `k8s-`)
`k8s-pod` `k8s-service` `k8s-deployment` `k8s-configmap` `k8s-secret` `k8s-ingress` `k8s-namespace` `k8s-node` `k8s-persistent-volume` `k8s-daemonset` `k8s-statefulset` `k8s-job` `k8s-cronjob` `k8s-hpa` `k8s-rbac`

For the **complete icon list** (320 AWS, 369 Azure, 280 GCP, 56 K8s icons), see `llm-generation-guide.md` in this skill directory.

## Positioning Guidelines

- Grid coordinates: X (horizontal), Y (vertical)
- Negative X = left, positive X = right
- Negative Y = up, positive Y = down
- Range: -20 to +20 for both axes
- **Spacing: 3-5 units between components**
- Start main components near (0, 0)
- Arrange in logical flow (left-to-right or top-to-bottom)

## Connection Patterns

| Pattern | Example | Use For |
|---------|---------|---------|
| Linear | `[0,1], [1,2], [2,3]` | Data pipelines, request flow |
| Hub & spoke | `[0,1], [0,2], [0,3]` | Load balancer, API gateway |
| Mesh | `[0,1], [1,0], [1,2], [2,1]` | Microservices communication |
| Layered | `[0,3], [1,3], [2,3]` | Multiple services to shared DB |

## Generation Workflow

1. **Identify components** from the user's description
2. **Map each to a valid icon** (use cloud-specific icons when platform is specified)
3. **Build items array** with concise names and descriptions
4. **Calculate positions** using grid layout with 3-5 unit spacing
5. **Define connections** based on data/control flow
6. **Validate** against the checklist below
7. **Output raw JSON** (no markdown code fences unless explicitly asked)

## Validation Checklist (Run Before Output)

- [ ] Root keys are exactly `t`, `i`, `v`, `_` (no extras)
- [ ] `_` is exactly `{"f": "compact", "v": "1.0"}`
- [ ] Each item in `i` is a 3-element array `[name, icon, description]`
- [ ] All icon names are from the valid icons list
- [ ] Item names <= 30 chars, descriptions <= 100 chars, title <= 40 chars
- [ ] `v` contains at least one view: `[[positions], [connections]]`
- [ ] Each position is `[itemIndex, x, y]` with valid item index
- [ ] Each connection is `[fromIndex, toIndex]` with valid item indices
- [ ] Coordinates are within -20 to +20
- [ ] Number of positions matches number of items
- [ ] JSON is valid (no trailing commas, proper quoting)

## Common Mistakes

| Mistake | Wrong | Correct |
|---------|-------|---------|
| Object items | `{"name": "DB", "icon": "storage"}` | `["DB", "storage", "Main database"]` |
| String connections | `{"from": "lb", "to": "svc1"}` | `[0, 1]` |
| Wrong root keys | `"title"`, `"components"` | `"t"`, `"i"` |
| 3D positions | `[0, 5, 3, 0]` | `[0, 5, 3]` (index, x, y) |
| Missing metadata | (omitted) | `"_": {"f": "compact", "v": "1.0"}` |
| Invented icons | `"database"`, `"microservice"` | `"storage"`, `"server"` |
| Positions in items | `["DB", "storage", "desc", 5, 3]` | Items are 3 elements; positions go in `v` |

## Complete Example

Microservices with load balancer, 3 services, message queue, and database:

```json
{
  "t": "Microservices Architecture",
  "i": [
    ["Load Balancer", "load-balancer", "Distributes incoming traffic"],
    ["User Service", "server", "Handles user management"],
    ["Order Service", "server", "Processes orders"],
    ["Payment Service", "server", "Payment processing"],
    ["Message Queue", "queue", "Async communication between services"],
    ["Shared Database", "storage", "PostgreSQL shared data store"]
  ],
  "v": [
    [
      [[0, 0, -6], [1, -6, 0], [2, 0, 0], [3, 6, 0], [4, 0, 6], [5, 0, 10]],
      [[0, 1], [0, 2], [0, 3], [1, 4], [2, 4], [3, 4], [1, 5], [2, 5], [3, 5]]
    ]
  ],
  "_": { "f": "compact", "v": "1.0" }
}
```
