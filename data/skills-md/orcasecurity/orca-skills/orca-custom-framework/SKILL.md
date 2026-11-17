---
name: orca-custom-framework
description: Creates custom compliance frameworks from existing frameworks, alert lists, or security themes — organizes controls into sections, maps alerts, and pushes the framework to Orca. Suggests creating custom discovery alerts for gaps not covered by existing rules. Use when user asks to create, build, or generate a custom compliance framework.
trigger: When user asks to create, build, generate, or design a custom compliance framework, or wants to combine alerts into a new framework, or asks about custom compliance (e.g., "create custom framework", "build compliance for supply chain", "custom framework from CIS controls", "generate security framework")
---

# Orca Custom Framework Skill

Answers the question: **"How do I create a custom compliance framework tailored to my organization's specific security requirements?"**

Given a source (existing framework, list of alert IDs, or a security theme), this skill gathers relevant controls and alerts, organizes them into a structured custom compliance framework with logical sections, and creates it in Orca Security. When gaps exist — controls the user wants but Orca doesn't have a built-in rule for — the skill suggests creating custom discovery alerts to fill them.

## Usage

```
/orca-custom-framework Supply Chain Security Controls
/orca-custom-framework from:cis_docker_v.1.3.1
/orca-custom-framework alerts:orca-1234,orca-5678,orca-9012
/orca-custom-framework "Zero Trust Architecture"
```

Or natural language:
- "create a custom compliance framework for supply chain security"
- "build a framework based on CIS Docker + EKS controls"
- "generate a custom framework from these alerts: orca-1234, orca-5678"
- "create a supply chain security framework"
- "build custom compliance from our failing container controls"

## How It Works

The skill operates in **three phases**, using different tools at each stage:

### Phase 1: Read (Orca MCP tools — read-only)

Queries the Orca environment to gather existing controls and alerts:

- **`get_enabled_compliance_frameworks`** — lists all frameworks and their IDs
- **`get_compliance_framework_control_tests`** — pulls controls from relevant source frameworks, each containing a `rule_id`
- **`discovery_search`** — finds alerts matching the theme (e.g., "container registry", "image scanning")
- **`get_alert`** — gets full alert details when working from alert IDs

These are read-only MCP queries. They provide the `rule_id` values needed for the framework.

### Phase 2: Organize (assistant logic — no API calls)

Groups the gathered `rule_id` values into logical sections based on alert categories, asset types, and the requested theme. Assigns priority weights (`high`/`medium`/`low`) and dotted-notation IDs (e.g., `1.1`, `2.3`).

Also identifies **gaps** — security domains the user wants covered but where no existing Orca rule exists. For these, suggests creating custom discovery alerts (see Step 7).

### Phase 3: Create (Orca REST API — via curl)

There is **no MCP tool** for creating custom frameworks. The skill calls the Orca REST API directly:

```
POST https://api.orcasecurity.io/api/compliance/frameworks
Authorization: <token from .mcp.json>
```

The token is extracted from `.mcp.json` (`orca-security.headers.Authorization`).

## Processing Logic

### Step 1: Determine Input Mode

Parse user input to determine the source:

- **Theme/Topic mode**: User provides a theme (e.g., "Supply Chain Security", "Zero Trust", "Data Protection Baseline") → search across multiple existing frameworks for relevant controls
- **From-framework mode**: User says "from:cis_docker_v.1.3.1" or "based on CIS Docker" → query that framework's controls and adapt/subset them
- **Alert-list mode**: User provides alert IDs → query each alert and organize into controls/sections
- **Hybrid mode**: User provides a theme + reference framework → combine both sources

### Step 2: Gather Source Data (run queries in parallel based on mode)

#### Theme Mode — run ALL in parallel:

**Query 1-5: Discovery searches with different angles**
```
discovery_search:
  search_phrase: "<theme> security alerts"
  limit: 10
```
Run 5+ searches with different angle terms simultaneously to maximize coverage. Vary the search terms across the theme's domains (infrastructure, IAM, data, network, logging).

**Query 6: All enabled frameworks**
```
get_enabled_compliance_frameworks:
  (no filters)
```

**Query 7+: Control tests from relevant frameworks**
For each framework that relates to the theme, pull all controls:
```
get_compliance_framework_control_tests:
  framework_id: <id>
```

Identify which existing frameworks are most relevant to the theme and pull their controls. For example, a container-focused theme would query `cis_docker_v.1.3.1` and `cis_eks_1.5.0`, while an IAM-focused theme would query `aws_cis_6.0.0` and `orca_best_practices_2.0.0`.

#### From-Framework Mode — run in parallel:

```
get_enabled_compliance_frameworks → get framework IDs
get_compliance_framework_control_tests → pull source controls
get_framework_assets_with_failed_controls_count → context on impact
```

#### Alert-List Mode — run in parallel:

```
get_alert → for each alert ID, extract rule_id and metadata
get_enabled_compliance_frameworks → for cross-referencing
```

### Step 3: Extract rule_ids and Organize into Sections

**CRITICAL:** The Orca custom framework API requires `rule_id` values (internal Orca rule identifiers like `r40aa617ef4`), NOT alert IDs. Extract rule_ids from:

1. **From framework control tests:** Each test returned by `get_compliance_framework_control_tests` has a `rule_id` field — use these directly. This is the **primary and most reliable method**.
2. **From alerts:** Each Orca alert has a `RuleId` field in its data — query with `get_alert` and extract it.
3. **From discovery_search:** Results may reference rules — extract rule IDs from the returned data.

#### Section Generation

Group controls into logical sections using alert categories, asset types, and domain keywords. Adapt sections to the user's theme — the section names, groupings, and keyword mappings should all reflect what the user asked for.

**Default section taxonomy** (adapt based on theme):

| Section | Maps to Alert Categories | Example Controls |
|---------|------------------------|------------------|
| Identity & Access Management | IAM, permissions, roles, service accounts | Least-privilege, MFA enforcement, key rotation |
| Compute Security | VMs, instances, containers, serverless | Instance hardening, patching, secure boot |
| Network Security | VPC, firewalls, endpoints, load balancers | Network segmentation, TLS enforcement, ingress rules |
| Data Protection | Storage, databases, encryption, secrets | Encryption at rest, key management, data classification |
| Logging & Monitoring | Audit logs, alerts, metrics | Audit trail completeness, log retention |
| Vulnerability Management | CVEs, packages, images | Patch management, image scanning, dependency updates |
| Configuration Management | Misconfigurations, best practices | Secure defaults, hardened configurations |

Use the alert `category`, `description`, and `asset_types` fields from control tests to assign each rule_id to the appropriate section. When the user's theme implies specialized sections (e.g., "Container Image Security" for supply chain, "Training Infrastructure" for AI/ML), create those instead of the generic defaults.

### Step 4: Present Framework Preview

ALWAYS show a preview before creating. Display the framework structure, control counts, priority breakdown, and source frameworks.

### Step 5: Create Custom Framework via REST API

**Only proceed after user confirms the preview.**

#### API Endpoint

**Create:** `POST /api/compliance/frameworks`
**Update:** `PUT /api/compliance/frameworks/{id}`
**Delete:** `DELETE /api/compliance/frameworks/{id}`

#### Request Body

```json
{
  "name": "<framework_name>",
  "description": "<framework_description>",
  "checkedKeys": [],
  "sections": [
    {
      "name": "1. <Section Name>",
      "section_id_in_framework": "1",
      "tests": [
        {
          "rule_id": "<orca_rule_id>",
          "rule_id_in_framework": "1.1",
          "reference_id": "1.1",
          "origin_framework_id": "<source_framework_id>",
          "priority": "high"
        }
      ],
      "sections": []
    }
  ]
}
```

**Field reference:**
- `rule_id` (required) — Orca internal rule ID, NOT an alert ID
- `rule_id_in_framework` (required) — Dotted control number (e.g., `"1.1"`, `"3.4"`)
- `reference_id` (optional) — Typically same as `rule_id_in_framework`
- `origin_framework_id` (optional) — Source framework ID for traceability
- `priority` (optional) — `"high"` / `"medium"` / `"low"` — affects framework scoring weight
- `section_id_in_framework` (optional) — Dotted section number
- `sections` can be nested recursively for hierarchical frameworks
- `checkedKeys` — pass `[]` for API-created frameworks

#### Execution

```bash
curl -X POST "https://api.orcasecurity.io/api/compliance/frameworks" \
  -H "Authorization: <token>" \
  -H "Content-Type: application/json" \
  -d '<json_body>'
```

**Response:** `{"data": {"id": <framework_id>, "name": "<framework_name>", ...}}`

#### Important Notes

- **Sections are write-only** — GET responses return tests as a flat list, not the section hierarchy
- **Priority affects scoring** — `"high"` priority controls impact the overall score more heavily
- Show preview and get explicit user confirmation before creating
- Extract the auth token from `.mcp.json` (`orca-security.headers.Authorization`)

### Step 6: Post-Creation Validation

Query `get_enabled_compliance_frameworks` to verify the framework appears. Show the user:
- Framework ID and name
- Initial compliance score
- Number of controls mapped
- Suggest next steps: `/orca-compliance-gap <framework_name>`

### Step 7: Suggest Custom Alerts for Coverage Gaps

After organizing controls, identify security domains the user wants covered but where **no existing Orca rule exists**. For these gaps, suggest creating custom discovery alerts.

#### When to Suggest

- The user's theme includes a domain (e.g., "SBOM validation", "code signing verification") but no matching `rule_id` was found in any framework
- The coverage map shows unmapped areas
- The user explicitly asks for more controls

#### How to Suggest

Present the gap and offer to create a custom discovery alert:

```
GAP DETECTED: No existing Orca rule for "SBOM generation validation"

You can fill this gap by creating a custom discovery alert:
  POST /api/sonar/rules

  {
    "name": "Container image deployed without SBOM attestation",
    "details": "Detects container images in production registries that lack
                an associated SBOM attestation or provenance record.",
    "category": "Best practices",
    "orca_score": 6.0,
    "context_score": false,
    "rule_json": {
      "models": ["ContainerImage"],
      "type": "object_set",
      "with": { ... discovery query ... }
    },
    "compliance_frameworks": [
      {
        "compliance_framework": "<framework_name>",
        "category": "5. Build Pipeline & Artifact Integrity",
        "priority": "high"
      }
    ]
  }

This creates a custom alert AND automatically maps it to the framework.
Want me to create this custom alert?
```

#### Custom Discovery Alert API Reference

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/sonar/rules` | Create custom alert rule |
| `GET` | `/api/sonar/rules/{rule_id}` | Read alert rule |
| `PUT` | `/api/sonar/rules/{rule_id}` | Update alert rule |
| `DELETE` | `/api/sonar/rules/{rule_id}` | Delete alert rule |
| `GET` | `/api/alerts/catalog/category` | List available alert categories |

**Key fields:**
- `name` — Alert title
- `details` — Description (note: API uses `details`, not `description`)
- `category` — From `/api/alerts/catalog/category` (e.g., "Best practices", "Network misconfigurations")
- `orca_score` — Severity score (float, e.g., `6.0`)
- `rule_json` — Discovery query in Orca sonar DSL (object_set with models, keys, operators)
- `compliance_frameworks[]` — Auto-map to framework sections:
  - `compliance_framework` — Framework name (must match exactly)
  - `category` — Section name within the framework
  - `priority` — `"high"` / `"medium"` / `"low"`

The response returns a `rule_id` which can then be added to the custom framework via `PUT /api/compliance/frameworks/{id}`.

## Example: Supply Chain Security Controls

This example was tested live and created as framework ID 3104 with a 28% initial score.

**Input:** "create a custom compliance framework for supply chain security"

**Source frameworks queried:**
- `cis_docker_v.1.3.1` — Container/Docker controls
- `cis_eks_1.5.0` — Kubernetes/EKS controls
- `stig_k8s` — Kubernetes STIG controls
- `aws_cis_6.0.0` — AWS infrastructure controls
- `aws_foundational_security_best_practices` — AWS security baselines

**Result: 39 controls across 6 sections:**

| Section | Controls | Source |
|---------|----------|--------|
| 1. Container Image & Registry Security | 6 | CIS Docker, EKS, K8s STIG |
| 2. Container Runtime Protection | 8 | CIS Docker, EKS |
| 3. Kubernetes Admission & Policy Controls | 8 | K8s STIG, EKS |
| 4. Secrets & Credential Management | 7 | EKS, AWS Foundational, AWS CIS |
| 5. Build Pipeline & Artifact Integrity | 4 | AWS Foundational, EKS, AWS CIS |
| 6. Audit Logging & Monitoring | 6 | CIS Docker, K8s STIG, EKS |

**Coverage gaps identified** (candidates for custom discovery alerts):
- SBOM generation and validation
- Container image signing and provenance verification (SLSA)
- Dependency vulnerability scanning in CI/CD pipelines
- Third-party library allowlist enforcement
- Build environment isolation and reproducibility

## Output Format

### Layer 1: Framework Preview (before creation)

```
=====================================================================
CUSTOM FRAMEWORK BUILDER
=====================================================================

FRAMEWORK: <framework_name>
DESCRIPTION: <1-2 sentence description>
SOURCE: <theme | framework_name | alert list>

---------------------------------------------------------------------
FRAMEWORK STRUCTURE
---------------------------------------------------------------------

  Section                          Controls    Priority Breakdown
  -----------------------------------------------------------------
  <section 1>                      <N>         <H> high, <M> med
  <section 2>                      <N>         <H> high, <M> med
  ...
  -----------------------------------------------------------------
  TOTAL                            <N>         <H> high, <M> med

SOURCES: <framework_1> (<N> rules), <framework_2> (<N> rules), ...

COVERAGE GAPS (no existing rule — can create custom alerts):
  - <gap 1 description>
  - <gap 2 description>

=====================================================================
Ready to create? (yes / modify / add section / remove)
Drill down: all controls | <section name> | coverage gaps
=====================================================================
```

### Layer 2: Post-Creation Confirmation

```
=====================================================================
CUSTOM FRAMEWORK CREATED
=====================================================================

  FRAMEWORK     <framework_name>
  ID            <framework_id>
  CONTROLS      <N> total across <M> sections
  INITIAL SCORE <X>%
  CLOUD         <vendors>

NEXT STEPS:
  - View in Orca Console: Compliance -> <framework_name>
  - Run /orca-compliance-gap <framework_name> for gap analysis
  - Create custom alerts for coverage gaps (see below)

COVERAGE GAPS — fill with custom alerts:
  [1] <gap description>
      Want me to create a custom discovery alert for this? (yes/no)
  [2] <gap description>
      ...

=====================================================================
```

## Edge Cases

### No Matching Controls Found
```
No controls found matching "<theme>" in any enabled framework.

Try:
  - /orca-custom-framework with specific alert IDs
  - /orca-custom-framework from:<existing_framework>
  - Provide more specific terms
```

### Duplicate Framework Name
```
Framework "<name>" already exists (ID: <id>, Score: <X>%).

Options:
  1. Choose a different name
  2. Update existing: PUT /api/compliance/frameworks/<id>
  3. View it: /orca-compliance-gap <name>
```

## MCP Tools Used

### Reading data (MCP — read-only)

| Tool | Purpose | Parameters |
|------|---------|------------|
| `discovery_search` | Find alerts matching a theme | `search_phrase`, `limit` (1-10) |
| `get_enabled_compliance_frameworks` | List all frameworks | optional `filters` |
| `get_compliance_framework_control_tests` | Get controls from a framework | `framework_id`, optional `filters` |
| `get_alert` | Get alert details | `alert_id` (e.g., "orca-1234") |

### Writing data (REST API — no MCP tool available)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `POST` | `/api/compliance/frameworks` | Create custom framework |
| `PUT` | `/api/compliance/frameworks/{id}` | Update custom framework |
| `DELETE` | `/api/compliance/frameworks/{id}` | Delete custom framework |
| `POST` | `/api/sonar/rules` | Create custom discovery alert |
| `PUT` | `/api/sonar/rules/{rule_id}` | Update custom discovery alert |

> Framework creation and custom alert creation both use the Orca REST API via `curl`. The auth token is extracted from `.mcp.json`.

## Implementation Notes

1. **Parallelize queries** — run discovery searches and framework control queries simultaneously.
2. **Deduplicate rule_ids** — the same rule may appear in multiple frameworks. Deduplicate before building sections.
3. **Smart section assignment** — use alert category, asset type, and title keywords to assign controls to the correct section.
4. **Cross-framework traceability** — always set `origin_framework_id` so users know where each control came from.
5. **Preview before create** — ALWAYS show the preview and get user confirmation. This is a write operation.
6. **Identify gaps proactively** — after organizing, compare the framework sections against the user's theme to find missing domains. Suggest custom discovery alerts for each gap.
7. **Link to other skills** — after creation, suggest `/orca-compliance-gap <framework>` for gap analysis and `/orca-impact-analysis` for fix planning.
