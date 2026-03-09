---
name: data-validation
description: Use when you need to validate data quality, types, schemas, and consistency across systems
license: MIT
compatibility: opencode
metadata:
  audience: data-engineers, developers
  category: data
---

# Data Validation

Validate data quality, types, schemas, and consistency across systems. This skill helps ensure data accuracy, completeness, and reliability through comprehensive validation rules, schema validation, data quality checks, and anomaly detection.

## When to use me

Use this skill when:
- You need to ensure data quality and consistency across systems
- You're building data pipelines and need validation rules
- You're migrating data between systems and need to validate accuracy
- You need to implement data quality monitoring and alerting
- You're designing data schemas and need validation rules
- You need to detect data anomalies and inconsistencies
- You're implementing data governance and quality standards
- You need to validate data against business rules and constraints

## What I do

- **Schema validation**: Validate data against schemas (JSON Schema, Avro, Protobuf, XML Schema)
- **Data type validation**: Validate data types (strings, numbers, dates, booleans, etc.)
- **Data quality checks**: Check data completeness, accuracy, consistency, timeliness
- **Business rule validation**: Validate data against business rules and constraints
- **Referential integrity validation**: Validate relationships between data entities
- **Anomaly detection**: Detect data anomalies and outliers
- **Data profiling**: Profile data to understand characteristics and quality
- **Data lineage validation**: Validate data lineage and transformation accuracy
- **Data consistency validation**: Validate consistency across multiple data sources
- **Data validation rule management**: Manage and version validation rules

## Examples

```bash
# Validate data against JSON schema
./scripts/analyze-data-validation.sh --schema schema.json --data data.json

# Perform data quality checks
./scripts/analyze-data-validation.sh --quality-checks --source database --rules rules.yaml

# Detect data anomalies
./scripts/analyze-data-validation.sh --anomaly-detection --data data.csv --threshold 3

# Validate data consistency across sources
./scripts/analyze-data-validation.sh --consistency --sources source1.csv source2.csv

# Generate data validation report
./scripts/analyze-data-validation.sh --report --output validation-report.json
```

## Output format

```
Data Validation Report
─────────────────────────────────────
Validation Date: 2025-01-15T10:30:00Z
Data Source: customer_data.csv
Total Records: 1,250,847
Validation Duration: 45s

SCHEMA VALIDATION RESULTS:
───────────────────────────
✅ Valid: 1,200,543 records (96%)
❌ Invalid: 50,304 records (4%)

Schema Violations:
• Missing required field "customer_id": 12,847 records
• Invalid email format: 18,542 records
• Invalid date format (birth_date): 8,925 records
• Invalid phone number format: 10,090 records

DATA QUALITY METRICS:
──────────────────────
Completeness: 97.8%
  • Customer name: 99.2% complete
  • Email address: 96.5% complete
  • Phone number: 95.8% complete
  • Address: 92.4% complete

Accuracy: 95.3%
  • Email deliverability: 94.8% valid
  • Phone number validity: 96.2% valid
  • Address validity: 95.0% valid

Consistency: 98.1%
  • Date formats consistent: 99.2%
  • Country codes consistent: 97.8%
  • Currency formats consistent: 97.3%

Timeliness: 99.5%
  • Data freshness: 99.8% updated within 24 hours
  • Update frequency: 99.2% updated daily

BUSINESS RULE VALIDATION:
─────────────────────────
✅ Valid: 1,245,120 records (99.5%)
❌ Invalid: 5,727 records (0.5%)

Business Rule Violations:
• Customer age < 18: 1,247 records
• Invalid order amount (negative): 842 records
• Duplicate customer records: 2,150 records
• Inconsistent region-country mapping: 1,488 records

REFERENTIAL INTEGRITY VALIDATION:
─────────────────────────────────
✅ Valid: 1,248,950 references (99.8%)
❌ Invalid: 1,897 references (0.2%)

Referential Integrity Issues:
• Orphaned order records (missing customer): 892 references
• Invalid product references: 1,005 references

ANOMALY DETECTION:
──────────────────
⚠️ Detected: 3,842 anomalies (0.3%)

Anomaly Types:
• Unusual customer age distribution: 1,250 anomalies
• Abnormal order amounts: 1,892 anomalies
• Unexpected geographic distribution: 700 anomalies

DATA PROFILING SUMMARY:
───────────────────────
Numeric Fields:
  • order_amount: Min=$1, Max=$15,250, Avg=$245.75, StdDev=$125.42
  • customer_age: Min=18, Max=95, Avg=42.3, StdDev=12.8

Categorical Fields:
  • country: 45 distinct values (US: 45%, UK: 12%, CA: 8%, ...)
  • product_category: 12 distinct values (Electronics: 35%, Clothing: 25%, ...)

Date Fields:
  • order_date: Range=2024-01-01 to 2025-01-15
  • customer_since: Range=2018-03-15 to 2025-01-15

DATA CONSISTENCY ACROSS SOURCES:
────────────────────────────────
• Customer database vs CRM: 98.7% consistent
• Product catalog vs inventory: 97.2% consistent
• Order system vs payment gateway: 99.1% consistent

RECOMMENDATIONS:
────────────────
1. IMMEDIATE ACTION:
   • Fix missing customer_id field (12,847 records)
   • Clean invalid email addresses (18,542 records)
   • Remove duplicate customer records (2,150 records)

2. SHORT TERM (1-2 weeks):
   • Implement data validation in ingestion pipeline
   • Set up data quality monitoring and alerting
   • Establish data quality SLA (target: 99.5% quality)

3. MEDIUM TERM (1-3 months):
   • Implement data profiling and anomaly detection
   • Establish data governance framework
   • Implement data lineage tracking

4. LONG TERM (3-12 months):
   • Implement master data management
   • Establish data quality improvement program
   • Implement predictive data quality monitoring

VALIDATION RULE COVERAGE:
─────────────────────────
• Schema validation: 100% coverage
• Data type validation: 100% coverage
• Business rule validation: 85% coverage
• Referential integrity: 90% coverage
• Anomaly detection: 75% coverage

Overall Data Quality Score: 92.8/100
```

## Notes

- Data validation should be implemented as close to data entry as possible
- Validation rules should be versioned and managed like code
- Consider performance implications of data validation, especially for large datasets
- Implement incremental validation for streaming data
- Use statistical methods for anomaly detection to reduce false positives
- Data quality metrics should be tracked over time to identify trends
- Validation failures should trigger appropriate remediation workflows
- Consider data privacy and security when validating sensitive data