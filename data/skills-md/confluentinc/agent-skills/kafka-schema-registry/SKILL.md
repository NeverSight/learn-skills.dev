---
name: kafka-schema-registry
description: Scan a project to identify Kafka applications, extract schemas from data models, tag PII fields, generate Terraform for Confluent Schema Registry registration, and produce a migration report with rollout ordering. Use this skill when a user asks to analyze a folder or repo for Kafka usage, extract schemas, audit producer/consumer configurations, or generate Terraform for Schema Registry.
metadata:
  version: "1.0.0"
---

# Kafka Schema Registry Skill

Scan a project to identify Kafka applications, extract schemas, generate Terraform for Schema Registry registration, and produce a comprehensive analysis report.

## When to Use

Invoke this skill when:
- A user asks to analyze a project for Kafka usage in order to add event schemas or integrate Schema Registry
- A user wants to extract schemas from Kafka producers
- A user wants Terraform to register schemas to Schema Registry
- A user wants to audit Kafka producer/consumer configurations

## Deliverables

This skill produces 3 outputs in the target project:

1. **`schema-report.md`** — Full analysis report with findings, risks, and upgrade recommendations
2. **`schemas/`** — Extracted schema files (Avro, JSON Schema, Protobuf) with PII tagging
3. **`terraform/`** — Terraform configs using Confluent provider to register schemas

### Optional: Code Migration Assistance

If the user asks for their application code to be updated to integrate Schema Registry, use the [Code Migration Reference](references/code-migration.md) to update the code with proper Schema Registry integration patterns.

---

## High-Level Workflow

### Phase 0: Initialize

- Check for existing `schema.yaml` and `schemas/` directory manually
- Note any existing schema infrastructure in the report

### Phase 1: Project Scan & Kafka Detection

1. **Find build files** — Search for `pom.xml`, `build.gradle`, `requirements.txt`, `package.json`, etc.
2. **Detect Kafka dependencies** — Look for `spring-kafka`, `confluent-kafka`, `kafkajs`, etc.
3. **Find producers & consumers** — Grep for `KafkaTemplate`, `Producer(`, `producer.send`, etc.
4. **Extract topic names** — From string literals, config properties, YAML files
5. **Identify serializers** — Find `value.serializer`, `KafkaAvroSerializer`, custom serializers
6. **Build app catalog** — Compile findings: app name, language, role, topics, serializer, category

**Detailed patterns:** [Detection Patterns Reference](references/detection-patterns.md)

**App catalog structure:**
```yaml
app_name: module name
language: Java | Python | .NET | Go | Node/TS
role: producer | consumer | both
topics: [list of topics]
serializer_class: value.serializer used
custom_serializer: true | false
schema_format: AVRO | JSON | PROTOBUF | UNKNOWN
sr_integrated: true | false
category: A | B | C | D | E  # REQUIRED
```

**Multi-schema topic detection:**
- If multiple data models produce to the same topic, create a wrapper schema with `oneOf`/union/`oneof`
- Generate Terraform with `schema_reference` blocks
- Flag prominently in report

### Phase 2: Risk Detection

Search for:
- **`auto.register.schemas=true`** — Uncontrolled schema evolution (Category C)
- **`use.latest.version`** — Eases migration when set
- **Custom serializers** — Bypass SR entirely (Category E)

Record file path, line number, and affected topics for each occurrence.

**Patterns:** [Detection Patterns Reference](references/detection-patterns.md#risk-detection)

### Phase 3: Schema Inference

For each producer:
1. **Check for existing schema files** — `**/*.avsc`, `**/*.proto`, `**/*.schema.json`
2. **Infer from data models** — Java classes, Pydantic models, TypeScript interfaces, Go structs
3. **Infer from inline data** — HashMap, dict literals, map[string]any, plain objects, JSON strings
4. **Convert to schemas** — Map language types to JSON Schema / Avro / Protobuf
5. **Tag PII fields** — Scan field names for `email`, `ssn`, `phone`, `address`, etc.

**PII tagging:** Add `confluent:tags` (`PII`, `PRIVATE`, `SENSITIVE`, `PHI`) to detected fields.

**Detailed inference patterns:** [Schema Inference Reference](references/schema-inference.md)

### Phase 4: Categorize Producers

Classify each producer:

| Category | Criteria |
|----------|----------|
| **A: Compliant** | Confluent serializer + SR + no auto.register |
| **A→Header** | Already on SR, migrating to headers |
| **B: Schema in code, no SR** | Data models exist, but no SR integration |
| **C: Auto-register** | `auto.register.schemas=true` |
| **D: No schema** | Raw strings/bytes, no data model |
| **E: Custom serializer** | Custom `Serializer<T>` or inline serialization without SR |

**CRITICAL:** Use exact phrase "Category X" in:
- App catalog field
- Applications Discovered table
- Report section headers
- Terraform comments
- Risk sections

**Details:** [Categorization Reference](references/categorization.md)

### Phase 5: Create Schema Files

**Directory structure:**
```
schemas/
├── avro/
│   └── {topic}-value.avsc
├── json/
│   └── {topic}-value.json
└── proto/
    └── {topic}-value.proto
```

**File naming:** MUST use **kebab-case** (lowercase with hyphens):
- Value: `{topic}-value.{ext}`
- Key: `{topic}-key.{ext}`
- Examples: `order-events-value.avsc`, `user-notifications-value.json`

**Initialize:** Create `schema.yaml`.

**Validate:** Call `schema_lint(path: schemas/, fix: true)` if available.

### Phase 6: Generate Terraform

**File structure (MANDATORY separate files):**
```
terraform/
├── providers.tf              # Provider config
├── variables.tf              # Variable definitions
├── tags.tf                   # confluent_tag resources (if PII exists)
├── schemas.tf                # Active schemas (A, B, E)
├── flagged-auto-register.tf  # Category C only (commented out)
├── outputs.tf                # Output values
└── import.sh                 # Import script
```

**CRITICAL:**
- `schemas.tf` = Categories A, B, E — NOT commented out
- `flagged-auto-register.tf` = Category C ONLY — MUST be commented out
- `tags.tf` = MUST exist if ANY schema uses `confluent:tags`
- Each schema resource MUST have comment block: Topic, App, Source, Category

**Templates:** [Terraform Templates Reference](references/terraform-templates.md)

### Phase 7: Generate Report

Create `schema-report.md` with:
- Executive Summary (metrics + category breakdown)
- **Applications Discovered table** (EXACT format, Category column MANDATORY)
- RISKS (auto-register, custom serializers)
- Producer Upgrade Recommendations (per app, with "Category X" in heading)
- Migration Rollout Ordering (by category)
- PII Fields Detected
- Terraform Resources Generated
- Next Steps checklist

**CRITICAL formatting requirements:**
1. Applications Discovered = markdown table, NOT narrative sections
2. Every app section MUST say "Category X" explicitly
3. Terraform comment blocks required for every resource

**Template:** [Report Template Reference](references/report-template.md)

---

## Migration Rollout by Category

- **Category B** (JSON, no SR): Producers first → consumers
- **Category A→Header** (already on SR): Verify consumer versions → producers only
- **Category C** (auto-register): Register via Terraform → disable auto-register → producers fetch latest
- **Category E** (custom serializers): Consumers first (composite deserializer) → producers

**Details:** [Categorization Reference](references/categorization.md#migration-rollout-order-by-category)

---

## Edge Cases

- **Monorepos:** Treat each service/module with Kafka deps as separate app
- **Multi-topic producers:** Generate one schema resource per topic
- **Shared schemas:** One schema file, multiple Terraform resources reference it
- **No topic names:** If loaded from env vars, use placeholders with TODO
- **Test code:** Skip test directories unless they contain only schema definitions
- **Multiple serializers:** Create separate schema files per format

---

## Output Organization

```
{project_root}/
├── schema-report.md              # Analysis report
├── schemas/
│   ├── schema.yaml               # Schema project config
│   ├── avro/
│   │   └── {topic}-value.avsc
│   ├── json/
│   │   └── {topic}-value.json
│   └── proto/
│       └── {topic}-value.proto
└── terraform/
    ├── providers.tf
    ├── variables.tf
    ├── tags.tf                    # PII/PRIVATE/SENSITIVE tags
    ├── schemas.tf                 # Active schemas (depends_on tags)
    ├── flagged-auto-register.tf   # Commented-out Category C
    ├── outputs.tf
    └── import.sh                  # Import existing schemas
```

---

## Reference Documentation

- [Detection Patterns](references/detection-patterns.md) — Patterns for finding Kafka apps, dependencies, producers, consumers, serializers
- [Schema Inference](references/schema-inference.md) — Extract schemas from data models, inline data, PII tagging
- [Categorization](references/categorization.md) — Category definitions, rollout order, client version requirements
- [Terraform Templates](references/terraform-templates.md) — File structure, templates, naming conventions
- [Report Template](references/report-template.md) — Required sections, formatting rules, validation checklist
- [Code Migration](references/code-migration.md) — Serializer/deserializer implementation patterns for Python, Java, JavaScript, Go, and .NET

---

## Execution Approach

1. Use **Glob** to find build files and schema files
2. Use **Grep** for pattern detection (dependencies, producers, serializers, risks)
3. Use **Read** to inspect source files and data models
4. Use **Write** to create schema files, Terraform configs, and report

**No need to use Agent tool** — this skill is self-contained and uses direct tool calls.
