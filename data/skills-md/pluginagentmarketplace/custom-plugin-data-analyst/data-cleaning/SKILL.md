---
name: data-cleaning
description: Data cleaning, preprocessing, and quality assurance techniques
version: "2.0.0"
sasmp_version: "2.0.0"
bonded_agent: 05-programming-expert
bond_type: SECONDARY_BOND

# Skill Configuration
config:
  atomic: true
  retry_enabled: true
  max_retries: 3
  backoff_strategy: exponential

# Parameter Validation
parameters:
  tool_preference:
    type: string
    required: true
    enum: [python, r, excel, sql]
    default: python
  data_size:
    type: string
    required: false
    enum: [small, medium, large]
    default: medium

# Observability
observability:
  logging_level: info
  metrics: [rows_cleaned, missing_handled, duplicates_removed]
---

# Data Cleaning Skill

## Overview
Master data cleaning and preprocessing techniques essential for reliable analytics.

## Topics Covered
- Missing value handling (imputation, deletion)
- Outlier detection and treatment
- Data type conversion and validation
- Duplicate identification and removal
- String cleaning and normalization

## Learning Outcomes
- Clean messy datasets
- Handle missing data appropriately
- Detect and treat outliers
- Ensure data quality

## Error Handling

| Error Type | Cause | Recovery |
|------------|-------|----------|
| Memory error | Dataset too large | Use chunking or sampling |
| Type conversion failed | Invalid data format | Apply preprocessing first |
| Encoding issues | Wrong character encoding | Detect and specify encoding |
| Validation failure | Data doesn't meet schema | Review and adjust validation rules |

## Related Skills
- programming (for automation)
- foundations (for data quality concepts)
- databases-sql (for SQL-based cleaning)
