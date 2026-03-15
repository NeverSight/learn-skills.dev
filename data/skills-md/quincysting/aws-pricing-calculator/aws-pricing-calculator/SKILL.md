---
name: aws-pricing-calculator
description: >
  Generate shareable AWS Pricing Calculator URLs from architecture descriptions,
  blog posts, or solution documents. Discovers service schemas, looks up real
  pricing, builds estimate JSON, and POSTs to the Save API.
triggers:
  - AWS cost estimate
  - pricing calculator
  - calculator URL
  - cost this architecture
  - estimate for blog
  - AWS pricing
  - calculate AWS costs
---

# AWS Pricing Calculator Skill

Generate a shareable AWS Pricing Calculator URL from any architecture description.

## Trigger Terms

| Phrase | Example |
|--------|---------|
| AWS cost estimate | "Give me an AWS cost estimate for this architecture" |
| pricing calculator | "Create a pricing calculator for this blog post" |
| calculator URL | "Generate a calculator URL for these services" |
| cost this architecture | "Cost this architecture on AWS" |
| estimate for blog | "Create an estimate for this AWS blog post" |

## Workflow

Follow these 6 steps in order:

### Step 1: Extract Services

Read the architecture document, blog post, or user description. Identify:
- Each AWS service used
- Instance types, storage sizes, throughput, node counts
- Region (default: us-east-1)
- Grouping (environments, tiers, components)

### Step 2: Discover Schemas

For each service, run the discovery script to get the current schema:

```bash
python ~/.claude/skills/aws-pricing-calculator/scripts/calc_discover.py <serviceCode1> <serviceCode2> ...
```

This fetches the live service definition from CloudFront and extracts all
configurable `calculationComponents` with their IDs, types, options, and defaults.

**Check `references/service_formats.md` first** — if the service has a proven
format there, use it directly instead of discovering from scratch.

### Step 3: Look Up Pricing

Use the AWS Pricing API MCP tool (`get_pricing`) to get current prices:

```
get_pricing(serviceCode, region, filters)
```

Calculate monthly costs: `unit_price * quantity * hours_per_month` (730 hrs).

### Step 4: Build Estimate

Create a JSON spec file defining groups and services, then build:

```bash
python ~/.claude/skills/aws-pricing-calculator/scripts/calc_build.py spec.json -o estimate.json
```

Or use the Python API directly to build the estimate dict programmatically.

### Step 5: Save to API

Upload the estimate to get a shareable URL:

```bash
python ~/.claude/skills/aws-pricing-calculator/scripts/calc_save.py estimate.json
```

### Step 6: Return Results

Provide the user with:
1. The calculator URL
2. A cost summary table (service, monthly, annual)
3. Total monthly and annual costs

## Tools

| Script | Purpose |
|--------|---------|
| `scripts/calc_utils.py` | Shared: curl helpers, UUID, constants, region map |
| `scripts/calc_discover.py` | Fetch service defs, extract configurable components |
| `scripts/calc_build.py` | Build estimate JSON from a spec file |
| `scripts/calc_save.py` | POST to Save API, return shareable URL |

## Critical Rules

1. **`calculationComponents` must NOT be empty** — populate all required fields or the calculator shows $0.00
2. **`serviceCost.monthly` must be pre-calculated** — the calculator displays this value as-is on load; it does not recalculate
3. **`estimateFor` must match the template ID** from the service definition (e.g., `"template"` for EC2, `"appStream2"` for AppStream)
4. **`version` must match the current service definition version** — always fetch fresh via `calc_discover.py`
5. **Use `curl` subprocess, not Python `requests`** — Python 3.14 has SSL issues with CloudFront CDN endpoints
6. **Use AWS Pricing API MCP** (`get_pricing`) for real price lookups — never hardcode prices
7. **Check `references/service_formats.md`** for known working formats before building from scratch

## References

| File | Contents |
|------|----------|
| `references/api_endpoints.md` | CloudFront URLs, Save API request/response format |
| `references/service_formats.md` | Proven `calculationComponents` for 9+ services |
| `references/troubleshooting.md` | Common issues: $0 costs, read-only warnings, SSL errors |

## Quick Start Examples

### From a blog post URL
```
User: "Create an AWS pricing calculator for this blog post: https://aws.amazon.com/blogs/big-data/..."
```
1. Fetch and read the blog post
2. Extract architecture: services, instance types, storage, throughput
3. Run through Steps 2-6

### From a solution document
```
User: "Cost this architecture: 3 EC2 m5.xlarge Windows, 1 RDS Oracle db.m5.xlarge, EBS io1 1400GB"
```
1. Parse the service specs from the description
2. Discover schemas for ec2Enhancement, amazonRdsForOracle, amazonElasticBlockStore
3. Look up pricing, build estimate, save, return URL

### From a CSV/spreadsheet
```
User: "Build a calculator estimate from this CSV with our environment sizing"
```
1. Read the CSV to extract services per environment
2. Map to service codes and calculationComponents
3. Build grouped estimate, save, return URL
