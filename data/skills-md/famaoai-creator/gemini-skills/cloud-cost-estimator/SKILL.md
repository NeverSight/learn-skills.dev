---
name: cloud-cost-estimator
description: Estimates monthly cloud infrastructure costs from IaC files (Terraform, CloudFormation). Helps align architecture with budget constraints.
status: implemented
category: Utilities
last_updated: '2026-02-13'
tags:
  - finops
  - gemini-skill
---

# Cloud Cost Estimator

This skill adds financial awareness to infrastructure design by estimating costs for AWS, Azure, and GCP resources.

## Capabilities

### 1. Cost Projection

- Parses `.tf` files to identify resource types and counts.
- Provides estimated monthly costs based on standard pricing models.

### 2. Efficiency Recommendations

- Suggests cost-saving alternatives (e.g., "Use Spot instances for this worker group").
- Identifies "expensive" architectural choices.
- Validates if the projected infrastructure cost is within the typical range (e.g., 5-8% of ARR for SaaS) defined in [IT Cost Benchmarks](../knowledge/economics/it_cost_benchmarks.md).

## Usage

- "How much will this Terraform configuration cost per month on AWS?"
- "Compare the estimated cost of this multi-region setup vs a single-region setup."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
- References [IT Cost Benchmarks](../knowledge/economics/it_cost_benchmarks.md) for infrastructure spending standards relative to company size.
