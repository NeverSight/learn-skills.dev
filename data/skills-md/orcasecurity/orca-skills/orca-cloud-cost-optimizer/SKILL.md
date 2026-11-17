---
name: orca-cloud-cost-optimizer
description: Cloud cost optimization analysis using Orca Security asset data. Discovers all cloud assets (AWS, GCP, Azure) through Orca MCP tools, compares current configurations against cheaper alternatives using live public pricing, and produces a prioritized cost reduction report with exact asset evidence. Use when the user asks about cloud cost optimization, reducing cloud spend, rightsizing instances, saving money on cloud infrastructure, cost reduction opportunities, unused resources, oversized VMs, reserved instances, storage tiering, or wants to know what changes would lower their cloud bill.
trigger: When user asks about cloud costs, wasted cloud spend, rightsizing, "where can we save money?", "what's wasting money?", "cost optimization report", "how do we cut our AWS/GCP/Azure bill?", "unused resources", "oversized instances", "give me a cost report", or any question about reducing infrastructure spend.
---

# Cloud Cost Optimizer

Answers the question: **"Where are we overspending and what should we fix first?"**

Analyzes all cloud assets via Orca Security MCP data to identify actionable cost reduction opportunities across compute, databases, storage, networking, and serverless resources. Delivers a dual-audience report: executive summary with total savings range, and per-asset action plan with specific IDs, Orca links, console links, CLI commands, and projected monthly savings.

**The key rule: never generalize.** "You have some oversized instances" is useless. "Your `db-prod-us-east-1` RDS instance is a `db.r5.4xlarge` ($1,752/month) and could be `db.r5.2xlarge` ($876/month)" is what this report delivers.

## Usage

```
/orca-cloud-cost-optimizer
```

Or natural language:
- "give me a cost optimization report"
- "where are we wasting money on cloud?"
- "how do we cut our AWS bill?"
- "find unused resources"
- "what can we rightsize?"

---

## Phase 1: Asset Discovery

Use the Orca MCP `discovery_search` tool to enumerate assets. Run these searches **in parallel** to save time.

### Compute
- AWS: EC2 instances
- GCP: Compute Engine VM instances
- Azure: Virtual Machines

### Containers & Orchestration
- AWS: ECS tasks, EKS nodes, Fargate tasks
- GCP: GKE node pools
- Azure: AKS node pools

### Serverless
- AWS: Lambda functions
- GCP: Cloud Functions, Cloud Run services
- Azure: Azure Functions, Container Apps

### Databases
- AWS: RDS instances, Aurora clusters, ElastiCache clusters, DynamoDB tables
- GCP: Cloud SQL, Spanner, Bigtable, Memorystore
- Azure: Azure SQL Managed Instance, Azure Database for PostgreSQL/MySQL, Cosmos DB, Azure Cache for Redis

### Storage
- AWS: S3 buckets, EBS volumes, EFS file systems
- GCP: GCS buckets, Persistent Disks, Filestore
- Azure: Azure Blob Storage containers, Azure Managed Disks, Azure Files shares

### Networking
- AWS: Elastic IPs, NAT Gateways, Classic/Application/Network Load Balancers
- GCP: Cloud NAT, External IPs, Cloud Load Balancing
- Azure: Azure Public IPs, NAT Gateways, Application/Load Balancers

**For each asset, capture:**
- Asset ID and Orca `app_url` (always present in discovery_search results — this is the direct Orca platform deep-link)
- Asset name and type
- Cloud provider, region/zone, and account/project/subscription ID
- Current configuration: instance type or SKU, size class, storage tier, pricing model (on-demand/reserved/spot)
- Associated tags — especially environment (prod/staging/dev), team, and service name
- Creation date when available

If `discovery_search` returns limited fields, use the Orca MCP `get_asset_by_id` tool to fetch full details on assets where you need more configuration data.

---

## Phase 2: Pricing Research

Accurate savings calculations require current pricing. Always attempt live pricing first — baked-in tables become stale.

**Web search approach** (run in parallel per provider):
```
AWS EC2 pricing on-demand [instance-type] [region] site:aws.amazon.com/ec2/pricing
GCP compute engine machine types pricing site:cloud.google.com/compute/vm-instance-pricing
Azure virtual machines pricing site:azure.microsoft.com/en-us/pricing/details/virtual-machines
```

For each resource type present in the environment, fetch:
- Current on-demand price of the existing configuration
- Price of the recommended alternative (one size down, or newer generation)
- 1-year reserved/committed use price for stable workloads
- Spot/Preemptible price for interruptible workloads

**Fallback:** If web search fails or returns inconsistent data, use approximate pricing from training data. When using fallback prices, mark estimates with `~` and note the source date.

---

## Phase 3: Optimization Analysis

For each discovered asset, evaluate all applicable optimization patterns below. An asset may qualify for multiple optimizations — include all of them, and total the savings.

### Pattern 1: Idle and Orphaned Resources
**What to look for:** Unattached EBS/Managed Disk/Persistent Disk volumes; Elastic IPs with no associated instance; load balancers with no registered targets; NAT gateways serving zero or one instance; instances with names suggesting temporary use (test, tmp, scratch, demo) and old creation dates.
**Recommendation:** Delete or terminate. Snapshot storage volumes before deletion as a safety measure.
**Savings:** 100% of current cost. Zero risk for truly idle resources.

### Pattern 2: Rightsizing (Oversized Instances)
**What to look for:** Instances with sizes of xlarge or larger (2xlarge, 4xlarge, 8xlarge, etc.) where the name or tags don't suggest a memory- or compute-intensive workload. Flag especially any development or staging instances running on large types.
**Recommendation:** Move down one size within the same family (e.g., m5.2xlarge → m5.xlarge).
**Savings:** ~50% of compute cost per instance.
**Risk:** Low for dev/staging. Medium for production — flag as needing load testing.

### Pattern 3: Previous Generation → Current Generation
**What to look for:**
- AWS: Instance families m3, m4, c3, c4, r3, r4, t1, t2, i2, d2
- GCP: n1 machine types
- Azure: Av1, Dv1, Dv2, Dv3, Dsv3, Ev3, Esv3 series
**Recommendation:**
- AWS m4 → m6i, c4 → c6i, r4 → r6i, t2 → t3 (same or lower price, better performance)
- GCP n1 → n2 or e2 (10-30% cheaper for same specs)
- Azure Dv3 → Dv4/Dsv4 (up to 15% cheaper)
**Savings:** 10-25% cost reduction with zero performance regression. Often requires only a stop/start.
**Risk:** Low. This is one of the safest optimizations.

### Pattern 4: On-Demand → Reserved / Committed Use
**What to look for:** Production instances (environment tag = prod, or no dev/staging tag) that appear to be long-running (creation date > 30 days ago). Databases are especially good candidates since they almost never stop.
**Recommendation:** Purchase 1-year reserved instance (AWS) or committed use discount (GCP/Azure).
**Savings:** ~40% for 1-year, ~60% for 3-year. Calculate based on actual hourly rate × 730 hours/month.
**Risk:** Low — financial commitment only. If the instance is likely to be needed for a year (especially databases, core production services), this is a no-brainer.
**Note:** Do not recommend 3-year commitments unless the user specifically asks — they reduce flexibility.

### Pattern 5: On-Demand → Spot / Preemptible
**What to look for:** Development, staging, or testing instances (env tags: dev, staging, test, qa). Batch processing workloads. Any non-production database replicas.
**Recommendation:** Convert to AWS Spot Instances, GCP Preemptible/Spot VMs, or Azure Spot VMs.
**Savings:** 60-90% cost reduction.
**Risk:** Medium. Spot instances can be interrupted with 2-minute notice. Only appropriate for fault-tolerant workloads. Always flag this risk prominently.

### Pattern 6: Database Rightsizing
**What to look for:** RDS, Cloud SQL, or Azure SQL instances with types larger than db.t3.medium / db.m5.large that are serving development or staging environments. Also flag production databases that are significantly larger than the application compute instances they serve.
**Recommendation:** Move to a smaller instance class. For dev/staging, consider switching to burstable types (db.t3.medium for RDS).
**Savings:** 40-60% of database cost.
**Risk:** Medium. Requires monitoring after change. Always recommend doing this during a maintenance window.

### Pattern 7: Multi-AZ / High Availability in Non-Production
**What to look for:** RDS or Azure SQL instances with Multi-AZ enabled in non-production environments (env tags: dev, staging, test). Read replicas in dev environments.
**Recommendation:** Disable Multi-AZ for non-production databases.
**Savings:** ~50% of database cost (Multi-AZ doubles the cost).
**Risk:** Low for non-production. **NEVER recommend disabling Multi-AZ for production databases** — state this explicitly.

### Pattern 8: EBS gp2 → gp3 Migration
**What to look for:** Any AWS EBS volumes using the `gp2` volume type. This is a very common finding.
**Recommendation:** Migrate to `gp3`. Same baseline performance (3,000 IOPS, 125 MiB/s throughput included), but 20% cheaper. Can be done live with zero downtime via the `aws ec2 modify-volume` command.
**Savings:** 20% of EBS volume cost. gp2 costs $0.10/GB/month → gp3 costs $0.08/GB/month.
**Risk:** Very low. Zero downtime migration.

### Pattern 9: S3 / Object Storage Tiering
**What to look for:** S3 buckets, GCS buckets, or Azure Blob containers without lifecycle policies (or with no tiering configured). Large volumes of data that aren't frequently accessed (backup buckets, log archives, data lake cold partitions).
**Recommendation:**
- S3: Enable S3 Intelligent-Tiering or add lifecycle policy (Standard → Standard-IA after 30 days → Glacier after 90 days)
- GCS: Enable Autoclass or set Nearline/Coldline for archival data
- Azure: Enable lifecycle management with Cool or Archive tier transitions
**Savings:** 40-90% of storage cost depending on access patterns.
**Risk:** Low. Lifecycle policies don't delete data, they move it to cheaper tiers.
**Note:** If access pattern data isn't available (it won't be from Orca config data alone), recommend Intelligent-Tiering (AWS) or Autoclass (GCP) which auto-optimize without requiring access pattern knowledge.

### Pattern 10: Oversized Networking Resources
**What to look for:** NAT Gateways in regions or VPCs serving very few instances; load balancers with no instances registered; multiple NAT Gateways where one would suffice.
**Recommendation:** Consolidate or remove. For small dev environments, consider using NAT instances instead of managed NAT gateways.
**Savings:** AWS NAT Gateway costs $0.045/hour ($32/month) plus data transfer. LB costs $0.008/LCU-hour.
**Risk:** Low for unused resources. Medium for consolidation — requires routing changes.

---

## Phase 4: Report Generation

Structure your output **exactly** as follows.

**Critical formatting rules:**
1. The Executive Summary appears **twice**: once at the very top (before all details), and once at the very bottom (as a recap for readers who scroll to the end).
2. Every asset recommendation must include both an **Orca platform link** and a **cloud provider console/portal link** as clickable evidence.
3. Fill in every section with real data. If no opportunities exist in a category, say so explicitly.

---

### How to Generate Asset Links

**Orca platform link:** Use the `app_url` field returned by `discovery_search` for each asset. Format it as: `[View in Orca](<app_url>)`

**Cloud provider console deep-links:**

| Provider | Resource | URL Template |
|----------|---------|--------------|
| AWS | EC2 instance | `https://console.aws.amazon.com/ec2/v2/home?region={region}#Instances:instanceId={instance-id}` |
| AWS | EBS volume | `https://console.aws.amazon.com/ec2/v2/home?region={region}#Volumes:volumeId={volume-id}` |
| AWS | RDS instance | `https://console.aws.amazon.com/rds/home?region={region}#database:id={db-name}` |
| AWS | S3 bucket | `https://s3.console.aws.amazon.com/s3/buckets/{bucket-name}` |
| AWS | NAT Gateway | `https://console.aws.amazon.com/vpc/home?region={region}#NatGateways:natGatewayId={ngw-id}` |
| AWS | Elastic IP | `https://console.aws.amazon.com/ec2/v2/home?region={region}#Addresses:AllocationId={eipalloc-id}` |
| AWS | Load Balancer (v2) | `https://console.aws.amazon.com/ec2/v2/home?region={region}#LoadBalancers:search={lb-name}` |
| GCP | VM instance | `https://console.cloud.google.com/compute/instancesDetail/zones/{zone}/instances/{name}?project={project-id}` |
| GCP | Cloud SQL | `https://console.cloud.google.com/sql/instances/{name}/overview?project={project-id}` |
| GCP | GCS bucket | `https://console.cloud.google.com/storage/browser/{bucket-name}?project={project-id}` |
| Azure | Virtual Machine | `https://portal.azure.com/#resource/subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Compute/virtualMachines/{name}/overview` |
| Azure | Managed Disk | `https://portal.azure.com/#resource/subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Compute/disks/{name}/overview` |
| Azure | SQL Database | `https://portal.azure.com/#resource/subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Sql/servers/{server}/databases/{db}/overview` |

When exact IDs are not available from Orca metadata, use the search-based URL (e.g., `#Instances:search={name}`) and note the asset name.

---

### Report Template

```
# ☁️ Cloud Cost Optimization Report

**Generated:** [today's date]
**Environment:** [cloud providers + regions present]
**Assets analyzed:** [total count by provider]

---

## 📊 Executive Summary

*(This summary also appears at the end of the report for quick reference)*

| | |
|---|---|
| Total assets analyzed | X |
| Assets with savings opportunities | X (X%) |
| **Estimated monthly savings** | **$X,XXX – $X,XXX/month** |
| **Estimated annual savings** | **$XX,XXX – $XX,XXX/year** |
| Immediate low-risk savings (this week) | $X,XXX/month |
| Implementation effort | Low / Moderate / Significant |

[2-3 sentences of narrative]

### 🏆 Top 5 Quick Wins
*Highest impact, lowest risk — can be done this week*

| # | Action | Asset(s) | Monthly Savings | Risk |
|---|--------|----------|----------------|------|
| 1 | | | $X,XXX | Low |
...

### Savings by Category

| Category | Opportunities | Monthly Savings | Risk Level |
|----------|--------------|-----------------|------------|
| Idle/unused resources | X | $X,XXX | Low |
| gp2 → gp3 migration | X | $XXX | Very Low |
| Generation upgrades | X | $X,XXX | Low |
| Rightsizing (compute) | X | $X,XXX | Low–Med |
| Reserved instance purchases | X | $X,XXX | Low |
| Database optimization | X | $X,XXX | Medium |
| Storage tiering | X | $X,XXX | Low |
| Spot/Preemptible migration | X | $X,XXX | Medium |
| Networking cleanup | X | $XXX | Low |
| **Total** | **X** | **$X,XXX** | |

---

## 🔍 Detailed Recommendations

*Listed in order of monthly savings (highest first).*

### [#N] [Short Title]

| Field | Value |
|-------|-------|
| **Asset name** | `[name]` |
| **Asset ID** | `[Orca asset ID]` |
| **Orca link** | [View in Orca]([app_url]) |
| **Console link** | [Open in Console]([deep-link]) |
| **Type** | [e.g., EC2 instance, EBS volume] |
| **Provider / Region** | AWS us-east-1 |
| **Current config** | [e.g., m4.2xlarge, gp2 500GB] |
| **Current est. monthly cost** | $X,XXX |
| **Recommended change** | [e.g., Migrate to m6i.2xlarge, gp3] |
| **Est. monthly savings** | **$X,XXX** |
| **Risk** | Low / Medium / High |

**Why this change:**
[1-2 sentences]

**How to implement:**
1. [Specific CLI command or console action]
2. [Next step]
3. [Verification step]

**Evidence from Orca:**
> [Relevant data from the Orca asset record]

**Pricing reference:** [URL or "fallback table (~Apr 2025)"]

---

## 🗺️ Implementation Roadmap

**Phase 1 — This week (zero downtime, immediate savings)**
- EBS gp2 → gp3 migrations (live, zero downtime)
- Delete truly idle resources (unattached volumes, unused IPs)
- Remove dev/staging Multi-AZ database configurations
- Terminate clearly orphaned instances/resources

**Phase 2 — Next 2–4 weeks (requires maintenance windows)**
- Instance generation upgrades (stop/start required)
- Compute rightsizing for non-production environments
- Add storage lifecycle policies to object storage buckets

**Phase 3 — Month 2+ (financial commitments and architecture)**
- Purchase reserved instances / committed use discounts for stable production workloads
- Convert appropriate dev/staging workloads to Spot/Preemptible
- Production rightsizing after performance validation

---

## ⚠️ Caveats

- Cost estimates are based on **configuration data only**, not measured utilization. Rightsizing recommendations assume instances are not CPU/memory constrained — validate before downsizing production systems.
- Reserved instance savings assume **continuous 24/7 operation**.
- Pricing data: [state whether live or fallback, and date]
- Spot/Preemptible instances are only appropriate for **fault-tolerant, stateless workloads** that can handle 2-minute interruption notices.
- This report covers configuration-based optimizations. Usage-pattern analysis (CPU utilization metrics) may reveal additional opportunities not captured here.

---

## 📊 Executive Summary (Recap)

*(Repeated here for readers who scroll to the end)*

[repeat the summary table and Top 5 Quick Wins table]

[1 closing sentence: the single most important action to take first.]
```

## MCP Tools Used

### Primary (always called in parallel)

| Tool | Purpose |
|------|---------|
| `discovery_search` | Enumerate EC2 instances, EBS volumes, S3 buckets, RDS, NAT Gateways, EIPs, Lambda, load balancers, ECS/EKS, ElastiCache |
| `get_asset_by_id` | Fetch full configuration details when discovery_search fields are insufficient |

### Optional

| Tool | When Called |
|------|------------|
| `get_asset_alerts_count_grouped_by_risk_level` | Check alert posture for assets flagged for rightsizing |
| `get_asset_related_alerts_summary` | Verify an asset is truly idle before recommending deletion |
| `get_aws_effective_permissions_policy_on_asset` | Assess IAM complexity before recommending termination |

### Tool Parameter Reference

#### discovery_search
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `search_phrase` | string | Yes | Natural language query, e.g., "EC2 instances", "EBS volumes", "S3 buckets" |
| `limit` | integer (1-50) | No | Max results (default 5, use 50 for full inventory) |

**Important:** `discovery_search` returns at most 50 results per query. For environments with many assets, results represent a sample. Always note the `total_items` field and include the `app_url` from results to link to the full Orca filtered view.

#### get_asset_by_id
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `asset_unique_id` | string | Yes | The Orca asset unique ID from discovery_search results |

## Implementation Notes

1. **Parallelize Phase 1 searches** — run all category discovery searches simultaneously. With 9 parallel queries, Phase 1 completes in a single round of MCP calls.
2. **Large result sets** — when discovery_search returns 50 results out of a larger `total_items`, note the limitation and extrapolate savings estimates proportionally.
3. **No utilization data** — Orca provides configuration data, not CPU/memory metrics. Always include the caveat that rightsizing recommendations are configuration-based and require utilization validation before applying to production.
4. **Pricing freshness** — always try live web search for pricing first. Fall back to training data only if web search fails. Mark fallback estimates with `~`.
5. **Risk classification** — never recommend deleting production databases or disabling Multi-AZ for prod RDS. Always check for `prod` / `production` tags or names before making recommendations that could affect availability.
6. **Link quality** — the `app_url` field from discovery_search is always the authoritative Orca platform link. Never construct Orca URLs manually.
