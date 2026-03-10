---
name: design-serialization-schema
description: >
  Design serialization schemas using JSON Schema, Protocol Buffer definitions,
  or Apache Avro. Covers schema versioning, backwards compatibility, validation
  rules, and evolution strategies for long-lived data formats. Use when defining
  a new API contract or data interchange format, adding fields to an existing
  schema without breaking consumers, migrating between schema versions, choosing
  between schema systems, or documenting data validation rules for automated
  enforcement.
license: MIT
allowed-tools: Read Write Edit Bash Grep Glob
metadata:
  author: Philipp Thoss
  version: "1.0"
  domain: data-serialization
  complexity: intermediate
  language: multi
  tags: json-schema, protobuf, avro, schema-evolution, versioning, compatibility
---

# Design Serialization Schema

Create well-versioned serialization schemas that evolve gracefully without breaking consumers.

## When to Use

- Defining a new API contract or data interchange format
- Adding fields to an existing schema without breaking consumers
- Migrating between schema versions
- Choosing between schema systems (JSON Schema, Protobuf, Avro)
- Documenting data validation rules for automated enforcement

## Inputs

- **Required**: Data model (entity relationships, field types, constraints)
- **Required**: Compatibility requirements (who consumes this data, how long must old formats be readable)
- **Optional**: Existing schema to evolve
- **Optional**: Performance requirements (validation speed, schema registry integration)
- **Optional**: Target serialization format (JSON, binary, columnar)

## Procedure

### Step 1: Choose a Schema System

| System | Format | Strengths | Best For |
|--------|--------|-----------|----------|
| JSON Schema | JSON | Widely supported, flexible validation | REST APIs, config validation |
| Protocol Buffers | Binary | Compact, fast, strong typing, built-in evolution | gRPC, microservices |
| Apache Avro | Binary/JSON | Schema in data, excellent evolution support | Kafka, data pipelines |
| XML Schema (XSD) | XML | Comprehensive typing, namespace support | Enterprise/legacy SOAP |
| TypeBox/Zod | TypeScript | Type inference, runtime validation | TypeScript APIs |

**Expected:** Schema system selected based on ecosystem, performance needs, and evolution requirements.
**On failure:** If uncertain, start with JSON Schema — it has the broadest tooling support and can be layered onto existing JSON APIs.

### Step 2: Design the Core Schema

#### JSON Schema example:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.com/schemas/measurement/v1",
  "title": "Measurement",
  "description": "A sensor measurement reading",
  "type": "object",
  "required": ["sensor_id", "value", "unit", "timestamp"],
  "properties": {
    "sensor_id": {
      "type": "string",
      "pattern": "^[a-z]+-[0-9]+$",
      "description": "Unique sensor identifier (lowercase-digits format)"
    },
    "value": {
      "type": "number",
      "description": "Measured value"
    },
    "unit": {
      "type": "string",
      "enum": ["celsius", "fahrenheit", "kelvin", "percent", "ppm"],
      "description": "Unit of measurement"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 timestamp with timezone"
    },
    "metadata": {
      "type": "object",
      "additionalProperties": true,
      "description": "Optional key-value metadata"
    }
  },
  "additionalProperties": false
}
```

#### Protocol Buffers example:

```protobuf
syntax = "proto3";
package sensors.v1;

import "google/protobuf/timestamp.proto";

// Measurement represents a single sensor reading.
message Measurement {
  string sensor_id = 1;         // Unique sensor identifier
  double value = 2;             // Measured value
  Unit unit = 3;                // Unit of measurement
  google.protobuf.Timestamp timestamp = 4;
  map<string, string> metadata = 5; // Optional key-value metadata
}

enum Unit {
  UNIT_UNSPECIFIED = 0;
  UNIT_CELSIUS = 1;
  UNIT_FAHRENHEIT = 2;
  UNIT_KELVIN = 3;
  UNIT_PERCENT = 4;
  UNIT_PPM = 5;
}
```

#### Apache Avro example:

```json
{
  "type": "record",
  "name": "Measurement",
  "namespace": "com.example.sensors",
  "doc": "A sensor measurement reading",
  "fields": [
    {"name": "sensor_id", "type": "string", "doc": "Unique sensor identifier"},
    {"name": "value", "type": "double", "doc": "Measured value"},
    {"name": "unit", "type": {"type": "enum", "name": "Unit", "symbols": ["CELSIUS", "FAHRENHEIT", "KELVIN", "PERCENT", "PPM"]}},
    {"name": "timestamp", "type": {"type": "long", "logicalType": "timestamp-millis"}},
    {"name": "metadata", "type": ["null", {"type": "map", "values": "string"}], "default": null}
  ]
}
```

**Expected:** Schema is self-documenting with descriptions, constraints, and clear type definitions.
**On failure:** If the data model is not yet stable, mark the schema as `draft` and avoid publishing to a registry.

### Step 3: Plan for Schema Evolution

Compatibility rules:

| Change | Backwards Compatible? | Forwards Compatible? | Safe? |
|--------|----------------------|---------------------|-------|
| Add optional field | Yes | Yes | Yes |
| Add required field | No | Yes | No (breaks existing consumers) |
| Remove optional field | Yes | No | Careful (producers may still send) |
| Remove required field | Yes | No | Careful |
| Rename a field | No | No | No (use alias + deprecation) |
| Change field type | No | No | No (add new field, deprecate old) |
| Add enum value | Yes (if consumers ignore unknown) | No | Depends on implementation |
| Remove enum value | No | Yes | No |

Safe evolution strategy:
1. **Only add optional fields** with sensible defaults
2. **Never remove or rename** — deprecate instead
3. **Version the schema** in the identifier (`v1`, `v2`)
4. **Use a schema registry** for binary formats (Confluent Schema Registry for Avro/Protobuf)

#### Protobuf evolution rules:
```protobuf
// v1 — original
message Measurement {
  string sensor_id = 1;
  double value = 2;
  Unit unit = 3;
}

// v2 — safe evolution
message Measurement {
  string sensor_id = 1;
  double value = 2;
  Unit unit = 3;
  // NEW: added in v2 — old clients ignore this field
  google.protobuf.Timestamp timestamp = 4;
  // DEPRECATED: use sensor_id instead
  reserved 6;
  reserved "old_sensor_name";
}
```

#### JSON Schema versioning:
```json
{
  "$id": "https://example.com/schemas/measurement/v2",
  "allOf": [
    {"$ref": "https://example.com/schemas/measurement/v1"},
    {
      "properties": {
        "location": {
          "type": "string",
          "description": "Added in v2: GPS coordinates"
        }
      }
    }
  ]
}
```

**Expected:** Evolution plan documented: which changes are safe, which require new versions.
**On failure:** If a breaking change is unavoidable, version the schema (v1 → v2) and maintain parallel support during migration.

### Step 4: Implement Schema Validation

```python
# JSON Schema validation (Python)
from jsonschema import validate, ValidationError
import json

schema = json.load(open("measurement_v1.json"))

def validate_measurement(data: dict) -> list[str]:
    """Validate a measurement against the schema. Returns list of errors."""
    errors = []
    try:
        validate(instance=data, schema=schema)
    except ValidationError as e:
        errors.append(f"{e.json_path}: {e.message}")
    return errors

# Usage
errors = validate_measurement({"sensor_id": "s-01", "value": "not_a_number"})
# → ["$.value: 'not_a_number' is not of type 'number'"]
```

```typescript
// TypeScript with Zod (runtime + compile-time)
import { z } from 'zod';

const MeasurementSchema = z.object({
  sensor_id: z.string().regex(/^[a-z]+-[0-9]+$/),
  value: z.number(),
  unit: z.enum(['celsius', 'fahrenheit', 'kelvin', 'percent', 'ppm']),
  timestamp: z.string().datetime(),
  metadata: z.record(z.string()).optional(),
});

type Measurement = z.infer<typeof MeasurementSchema>;

// Validation
const result = MeasurementSchema.safeParse(inputData);
if (!result.success) {
  console.error(result.error.issues);
}
```

**Expected:** Validation runs on all incoming data at system boundaries (API endpoints, file ingestion).
**On failure:** Log validation errors with the full payload (redacting sensitive fields) for debugging.

### Step 5: Document the Schema

Create a schema documentation page:

```markdown
# Measurement Schema (v1)

## Overview
Represents a single sensor reading with metadata.

## Fields
| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| sensor_id | string | Yes | Unique sensor ID | Pattern: `^[a-z]+-[0-9]+$` |
| value | number | Yes | Measured value | Any valid IEEE 754 double |
| unit | enum | Yes | Unit of measurement | One of: celsius, fahrenheit, kelvin, percent, ppm |
| timestamp | string | Yes | Reading time | ISO 8601 with timezone |
| metadata | object | No | Key-value pairs | String keys and values |

## Changelog
| Version | Date | Changes |
|---------|------|---------|
| v1 | 2025-03-01 | Initial schema |

## Compatibility
- **Backwards**: Consumers of v1 will continue to work with future versions
- **Policy**: Only additive, optional field changes between minor versions
```

**Expected:** Documentation is auto-generated or stays in sync with the schema definition.
**On failure:** If docs drift from schema, add a CI check that validates docs against the schema source.

## Validation

- [ ] Schema uses appropriate system for the use case (JSON Schema, Protobuf, Avro)
- [ ] All fields have types, descriptions, and constraints
- [ ] Required vs optional fields are explicitly defined
- [ ] Evolution strategy documented (safe changes, versioning policy)
- [ ] Validation implemented at system boundaries
- [ ] Schema is versioned with a changelog
- [ ] Round-trip test: serialize → deserialize → compare confirms no data loss

## Common Pitfalls

- **Over-constraining too early**: Strict validation on a new schema blocks iteration. Start permissive (`additionalProperties: true`), tighten later.
- **No default values**: Adding a required field without a default breaks all existing data. Always provide defaults for new fields.
- **Ignoring null**: Many schemas don't handle null/missing fields clearly. Be explicit about nullable vs optional.
- **Version in the payload, not the URL**: For long-lived data (storage, events), embed the schema version in the data itself, not just the endpoint URL.
- **Enum exhaustiveness**: Adding a new enum value can crash consumers that use exhaustive switch statements. Document that unknown values should be handled gracefully.

## Related Skills

- `serialize-data-formats` — format selection and encoding/decoding implementation
- `implement-pharma-serialisation` — pharmaceutical serialisation (regulatory schemas)
- `write-validation-documentation` — validation documentation for regulated schemas
