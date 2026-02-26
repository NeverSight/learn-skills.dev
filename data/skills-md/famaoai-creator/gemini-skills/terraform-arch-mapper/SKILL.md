---
name: terraform-arch-mapper
description: Generates a system architecture diagram from Terraform code. It parses .tf files to identify resources and relationships, then produces a diagram code (Mermaid/PlantUML). Use to visualize infrastructure.
status: implemented
category: Engineering & DevOps
last_updated: '2026-02-13'
tags:
  - automation
  - gemini-skill
---

# Terraform Arch Mapper

## Overview

This skill analyzes Terraform configuration files (`.tf`) to extract infrastructure resources and their dependencies. It then generates a visual representation of the system architecture using **Mermaid.js** or **PlantUML**.

## Capabilities

1.  **Resource Extraction**:
    - Scans all `.tf` files in a directory.
    - Identifies provider resources (e.g., `aws_instance`, `google_storage_bucket`).
2.  **Relationship Mapping**:
    - Detects dependencies between resources (e.g., `vpc_id = aws_vpc.main.id`).
3.  **Diagram Generation**:
    - Outputs Mermaid C4 or flowchart code.
    - Outputs PlantUML code.

## Usage

```bash
# Generate Mermaid diagram (default)
node scripts/generate_diagram.cjs [path/to/terraform/dir]

# Generate PlantUML diagram
node scripts/generate_diagram.cjs [path/to/terraform/dir] --format plantuml
```

## Dependencies

- Node.js environment
- `hcl2-parser` (for parsing Terraform files)

## Knowledge Protocol

- This skill adheres to the `knowledge/orchestration/knowledge-protocol.md`. It automatically integrates Public, Confidential (Company/Client), and Personal knowledge tiers, prioritizing the most specific secrets while ensuring no leaks to public outputs.
