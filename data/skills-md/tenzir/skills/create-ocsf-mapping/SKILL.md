---
name: create-ocsf-mapping
description: >-
  Create OCSF mapping operators for a Tenzir parser package. Use when the user
  wants to map parsed events to OCSF, normalize security data to OCSF, or says
  "map to OCSF", "add OCSF mapping", "normalize this to OCSF", "create OCSF
  operators", or "add OCSF support to this package."
metadata:
  requires:
    skills:
      - create-parser-package
      - ocsf
      - tenzir-docs
---

# Create an OCSF Mapping

Add OCSF mapping operators to a parser package. This workflow builds on a
working parser package, adding a dispatcher and per-event-type mapping operators
that transform cleaned events into OCSF-compliant output.

## Workflow

Execute each step in order. Verify the **Results** before moving on.

### 1. Ensure a parser package exists

Before mapping to OCSF, you need a package that can parse and clean the source
data. If one does not exist yet, complete the `create-parser-package` workflow
first.

**Results:**

- A working parser package with parse and clean operators
- All parsing tests passing

### 2. Identify the OCSF event class

Analyze the source events to determine which OCSF event class best represents
them. Consider the event semantics, not just field names. Use the `ocsf` skill
to look up event classes, required attributes, and profiles.

**Results:**

- The OCSF event class (e.g., `network_activity`, `authentication`)
- Understanding of required vs. optional attributes
- Any applicable profiles (e.g., `host`, `network_proxy`)

**Resources:**

- Use the `ocsf` skill to look up event classes, attributes, and profiles

### 3. Write mapping operators

For each log type, create a user-defined operator that transforms cleaned events
into the OCSF schema. Map source fields to OCSF attributes, handling type
conversions and nested structures.

**Results:**

- Main dispatching operator: `acme::product::ocsf::map`
- Test: `acme/tests/product/ocsf/map.{tql,txt}`
- Event-specific operator(s): `acme::product::ocsf::event::foo`
- Test(s): `acme/tests/product/ocsf/event/foo.{tql,txt}`

**Resources** (read via `tenzir-docs`):

- `guides/normalization/map-to-ocsf.md`
- `tutorials/map-data-to-ocsf.md`

### 4. Add end-to-end examples

Add examples showing the complete pipeline from raw data to OCSF output:

```tql
from_* {
  acme::product::parse
  acme::product::clean
  acme::product::ocsf::map
}
```

**Results:**

- Examples demonstrating the full normalization pipeline

**Resources** (read via `tenzir-docs`):

- `guides/collecting.md`

### 5. Finalize package

Update the package manifest to include the OCSF mapping operators. Review
operators for idiomatic TQL patterns. Verify all tests pass, including OCSF
validation via `ocsf::cast`.

**Results:**

- TQL code adheres to idiomatic best practices
- All tests pass and `ocsf::cast` emits no warnings
- Updated package manifest with OCSF operator documentation

**Resources** (read via `tenzir-docs`):

- `tutorials/learn-idiomatic-tql.md`
