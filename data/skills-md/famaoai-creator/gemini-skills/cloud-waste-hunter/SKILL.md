---
name: cloud-waste-hunter
description: Actively identifies and eliminates unused or over-provisioned cloud resources. Goes beyond estimation to hunt for actual cost savings in live environments.
status: implemented
arguments:
  - name: dir
    short: d
    type: string
    description: Directory with cloud configs
category: Utilities
last_updated: '2026-02-13'
tags:
  - finops
  - gemini-skill
---

# Cloud Waste Hunter

This skill is the ultimate cost-optimizer, focusing on eliminating actual waste in cloud spend.

## Capabilities

### 1. Waste Identification

- Identifies unattached storage (EBS), idle load balancers, and over-provisioned instances.
- Detects old snapshots or log streams that are consuming excessive budget.

### 2. Autonomous Downsizing

- Suggests or executes downsizing of resources based on actual CPU/Memory utilization history.

## Usage

- "Scan our AWS environment for unattached resources and old snapshots."
- "Recommend the top 5 cost-saving actions we can take right now based on usage logs."

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
