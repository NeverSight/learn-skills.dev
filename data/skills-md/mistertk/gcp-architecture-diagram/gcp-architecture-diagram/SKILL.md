---
name: gcp-architecture-diagram
description: GCP architecture diagram generator. Creates pixel-perfect SVG with 45 official GCP icons. Use for any request to draw, visualize, or diagram a Google Cloud Platform architecture.
---

# GCP Architecture Diagram Generator

Write a declarative JSON spec describing the diagram. A bundled Python renderer validates it and
produces pixel-perfect SVG with 45 official Google Cloud icons embedded as inline vectors.

**No external dependencies.** Python 3 stdlib only. Icons are pre-bundled.

## Workflow

1. **Understand** the user's architecture — identify GCP services, groupings, data flows
2. **Map** each service to an icon from the catalog below
3. **Write** a JSON spec file (see Spec Format)
4. **Render**: `python ${CLAUDE_SKILL_DIR}/scripts/render.py --spec spec.json --icons ${CLAUDE_SKILL_DIR}/assets/gcp-icons.json -o diagram.svg`
5. **Show** the result; iterate on feedback

For PNG conversion: `rsvg-convert -w 2400 diagram.svg -o diagram.png` (macOS: `brew install librsvg`).
Or output HTML directly: use `-o diagram.html` and it auto-wraps the SVG in an HTML viewer.

## Spec Format

```json
{
  "title": "My GCP Architecture",
  "subtitle": "Production Environment",
  "width": 1200,
  "titleColor": "blue",
  "elements": [ ... ]
}
```

- `title` (string, recommended) — shown in colored header bar
- `subtitle` (string, optional) — gray text below header
- `width` (int, default 1200) — canvas width in pixels
- `titleColor` (string, default "blue") — header bar color name
- `elements` (array, required) — ordered list of diagram elements

### Element Types

**`layer`** — A row of icons with a label. The primary building block.
```json
{"type": "layer", "label": "COMPUTE", "color": "blue", "services": [
  {"icon": "cloud-run", "label": "Cloud Run", "sublabel": "API Gateway"},
  {"icon": "gke", "label": "GKE", "sublabel": "Workers"}
]}
```
- `services` (array, required) — 1-6 icons per row (7+ auto-splits into two sub-rows)
- `icon` — ID from the catalog below (without `gcp:` prefix)
- `sublabel` (optional) — gray description text

**`arrow`** — Downward directional arrow between elements.
```json
{"type": "arrow", "color": "blue"}
```
- `label` (optional) — text below the arrow
- `color` (optional, default "gray")

**`container`** — Colored border wrapping child elements. Use for VPCs, tenants, projects.
```json
{"type": "container", "label": "VPC NETWORK", "color": "green", "elements": [
  {"type": "layer", ...},
  {"type": "arrow", ...},
  {"type": "layer", ...}
]}
```
- `elements` (array, required) — nested layers, arrows, splits, or more containers

**`split`** — Side-by-side columns. Use for parallel concerns at the same level.
```json
{"type": "split", "ratios": [3, 1], "elements": [
  {"type": "layer", "label": "DATA", "color": "purple", "services": [...]},
  {"type": "layer", "label": "CACHE", "color": "gray", "services": [...]}
]}
```
- `ratios` (array, optional) — relative widths (default: equal)
- `elements` (array, required) — 2+ layers or containers

**`bridge`** — Bidirectional arrow with label. Use between tenants or system boundaries.
```json
{"type": "bridge", "label": "A2A Protocol", "sublabel": "Bidirectional", "color": "red"}
```

**`legend`** — Color key bar. Place first in elements for top positioning.
```json
{"type": "legend", "items": [
  {"color": "blue", "label": "Compute"},
  {"color": "green", "label": "Data"},
  {"color": "gray", "label": "Infrastructure"}
]}
```

### Colors

8 named colors: `blue`, `green`, `red`, `yellow`, `purple`, `gray`, `navy`, `orange`.
Each has a border, background tint, and label color matching GCP brand guidelines.

## Icon Catalog

### Product Icons (19)

| Icon ID | Service |
|---------|---------|
| `cloud-run` | Cloud Run |
| `cloud-sql` | Cloud SQL |
| `cloud-spanner` | Cloud Spanner |
| `cloud-storage` | Cloud Storage |
| `bigquery` | BigQuery |
| `compute-engine` | Compute Engine |
| `gke` | GKE |
| `vertex-ai` | Vertex AI |
| `alloydb` | AlloyDB |
| `apigee` | Apigee |
| `anthos` | Anthos |
| `looker` | Looker |
| `hyperdisk` | Hyperdisk |
| `distributed-cloud` | Distributed Cloud |
| `ai-hypercomputer` | AI Hypercomputer |
| `mandiant` | Mandiant |
| `security-command-center` | Security Command Center |
| `security-operations` | Security Operations |
| `threat-intelligence` | Threat Intelligence |

### Category Icons (26)

| Icon ID | Category |
|---------|----------|
| `ai-machine-learning` | AI and Machine Learning |
| `agents` | Agents |
| `business-intelligence` | Business Intelligence |
| `collaboration` | Collaboration |
| `compute` | Compute |
| `containers` | Containers |
| `data-analytics` | Data Analytics |
| `databases` | Databases |
| `devops` | DevOps |
| `developer-tools` | Developer Tools |
| `hybrid-multicloud` | Hybrid and Multicloud |
| `integration-services` | Integration Services |
| `management-tools` | Management Tools |
| `maps-geospatial` | Maps and Geospatial |
| `marketplace` | Marketplace |
| `media-services` | Media Services |
| `migration` | Migration |
| `mixed-reality` | Mixed Reality |
| `networking` | Networking |
| `observability` | Observability |
| `operations` | Operations |
| `security-identity` | Security and Identity |
| `serverless-computing` | Serverless Computing |
| `storage` | Storage |
| `web-mobile` | Web and Mobile |
| `web3` | Web3 |

### Service → Icon Mapping

For GCP services without a dedicated product icon, use the closest category:

| GCP Service | Use Icon ID |
|-------------|-------------|
| Pub/Sub | `integration-services` |
| Cloud Functions | `serverless-computing` |
| Cloud CDN | `networking` |
| Cloud Load Balancer | `networking` |
| Memorystore / Redis | `databases` |
| Dataflow | `data-analytics` |
| Dataproc | `data-analytics` |
| Cloud Composer | `data-analytics` |
| Cloud Armor | `security-identity` |
| IAM | `security-identity` |
| Cloud KMS | `security-identity` |
| Cloud Build | `devops` |
| Artifact Registry | `developer-tools` |
| Cloud Logging | `observability` |
| Cloud Monitoring | `operations` |
| Firestore | `databases` |
| Cloud DNS | `networking` |
| VPC Network | `networking` |
| Cloud Endpoints | `networking` |
| Firebase | `web-mobile` |
| Dialogflow | `ai-machine-learning` |
| Agent Engine | `agents` |
| Cloud Tasks | `integration-services` |
| Cloud Scheduler | `integration-services` |

**NEVER invent icon IDs.** Only use IDs from the tables above. If unsure, use a category icon.

## Common Patterns

### Simple Layered (3 layers)

```json
{
  "title": "Simple Web Application",
  "elements": [
    {"type": "layer", "label": "NETWORKING", "color": "gray", "services": [
      {"icon": "networking", "label": "Cloud CDN"},
      {"icon": "networking", "label": "Load Balancer", "sublabel": "HTTPS L7"}
    ]},
    {"type": "arrow", "color": "blue"},
    {"type": "layer", "label": "COMPUTE", "color": "blue", "services": [
      {"icon": "cloud-run", "label": "Cloud Run", "sublabel": "API Server"}
    ]},
    {"type": "arrow", "color": "green"},
    {"type": "layer", "label": "DATA", "color": "green", "services": [
      {"icon": "cloud-sql", "label": "Cloud SQL", "sublabel": "Primary DB"},
      {"icon": "cloud-storage", "label": "Cloud Storage", "sublabel": "Assets"}
    ]}
  ]
}
```

### VPC-Wrapped

Note: the VPC container is green, so inner layers use *different* colors (blue, purple)
to stand out against the green background.

```json
{
  "title": "VPC Architecture",
  "elements": [
    {"type": "layer", "label": "INGRESS", "color": "gray", "services": [
      {"icon": "networking", "label": "Load Balancer"}
    ]},
    {"type": "arrow", "color": "green"},
    {"type": "container", "label": "VPC NETWORK", "color": "green", "elements": [
      {"type": "layer", "label": "COMPUTE", "color": "blue", "services": [
        {"icon": "cloud-run", "label": "Cloud Run"},
        {"icon": "gke", "label": "GKE"}
      ]},
      {"type": "arrow", "color": "purple"},
      {"type": "layer", "label": "DATA", "color": "purple", "services": [
        {"icon": "cloud-sql", "label": "Cloud SQL"},
        {"icon": "bigquery", "label": "BigQuery"},
        {"icon": "cloud-storage", "label": "Cloud Storage"}
      ]}
    ]}
  ]
}
```

### Multi-Tenant with Bridge

Note: shared services are peer resources, not a pipeline — they stack as adjacent layers
without arrows between them (no data flows from databases into security).

```json
{
  "title": "Multi-Tenant SaaS",
  "elements": [
    {"type": "container", "label": "CUSTOMER TENANT", "color": "green", "elements": [
      {"type": "layer", "label": "FRONTEND", "color": "gray", "services": [
        {"icon": "networking", "label": "Cloud CDN"},
        {"icon": "networking", "label": "Load Balancer"}
      ]},
      {"type": "arrow", "color": "blue"},
      {"type": "layer", "label": "API", "color": "blue", "services": [
        {"icon": "gke", "label": "GKE", "sublabel": "API Gateway"}
      ]}
    ]},
    {"type": "bridge", "label": "gRPC / REST", "sublabel": "Bidirectional", "color": "red"},
    {"type": "container", "label": "SHARED SERVICES", "color": "navy", "elements": [
      {"type": "layer", "label": "DATA", "color": "purple", "services": [
        {"icon": "cloud-sql", "label": "Cloud SQL"},
        {"icon": "cloud-spanner", "label": "Cloud Spanner"},
        {"icon": "cloud-storage", "label": "Cloud Storage"}
      ]},
      {"type": "layer", "label": "AI AND ML", "color": "blue", "services": [
        {"icon": "vertex-ai", "label": "Vertex AI"},
        {"icon": "ai-machine-learning", "label": "Gemini Models"}
      ]},
      {"type": "layer", "label": "SECURITY", "color": "red", "services": [
        {"icon": "security-identity", "label": "IAM"},
        {"icon": "security-identity", "label": "Cloud KMS"},
        {"icon": "security-command-center", "label": "SCC"}
      ]}
    ]}
  ]
}
```

### Split Row

```json
{
  "title": "Data Platform",
  "elements": [
    {"type": "layer", "label": "INGESTION", "color": "red", "services": [
      {"icon": "integration-services", "label": "Pub/Sub"},
      {"icon": "data-analytics", "label": "Dataflow"}
    ]},
    {"type": "arrow", "color": "blue"},
    {"type": "split", "ratios": [3, 1], "elements": [
      {"type": "layer", "label": "PROCESSING", "color": "blue", "services": [
        {"icon": "bigquery", "label": "BigQuery", "sublabel": "Analytics"},
        {"icon": "vertex-ai", "label": "Vertex AI", "sublabel": "ML Training"},
        {"icon": "looker", "label": "Looker", "sublabel": "Dashboards"}
      ]},
      {"type": "layer", "label": "CACHE", "color": "gray", "services": [
        {"icon": "databases", "label": "Memorystore", "sublabel": "Redis"}
      ]}
    ]}
  ]
}
```

## Pitfalls

- **Never invent icon IDs** — only use IDs from the catalog tables above
- **Keep labels short** — under 20 characters to avoid overlap
- **3-6 services per layer** for readability; 7+ auto-splits into double rows
- **Limit to 4-5 colors** per diagram to avoid visual noise
- **Differentiate container and child colors** — inner layers should use different colors
  than their parent container so they stand out against the container's tinted background
  (e.g., green container with blue compute + purple data layers inside)
- **Use containers sparingly** — each adds visual weight; don't over-nest
- **Place legend first** in elements array so it appears at the top
- **Arrows mean directional data flow** — only use arrows between layers when data actually
  flows from one to the next (e.g., Ingestion → Processing → Serving). Peer services that
  exist at the same tier (e.g., databases, AI, storage, security) should be stacked as
  adjacent layers *without* arrows, or grouped into a single layer. Don't imply a pipeline
  where there isn't one
- **Don't split peer services unnecessarily** — if services are all part of the same logical
  tier (e.g., shared backend services), put them in one or two flat layers rather than a
  split. Splits are for genuinely different concerns at the same level that need different
  sizing (e.g., 75% main processing + 25% cache sidebar)
- **Validate before rendering**: use `--validate-only` to catch icon/color errors early

For advanced patterns (deeply nested containers, double rows, complex splits), see
`references/advanced-layouts.md`.
