---
name: create-parser-package
description: >-
  Create a Tenzir parser package from sample data. Use when the user wants to
  parse a new log format, scaffold a package, write parse/clean operators, or
  says "create a parser", "build a package for this data", "parse this log
  format", "write a parser for X", or "scaffold a package."
metadata:
  requires:
    skills:
      - tenzir-docs
---

# Create a Parser Package

Build a package that parses and cleans log events. The workflow scaffolds a
Tenzir package directory, adds user-defined operators for parsing and cleaning,
writes tests, and adds end-to-end examples.

## Workflow

Execute each step in order. Verify the **Results** before moving on.

### 1. Understand your data

Analyze the sample data to determine the log format, vendor, and product. Search
the web for additional samples or documentation when the format is unfamiliar.

**Results:**

- Context around the given samples (format, fields, semantics)
- Vendor and product names for the package

### 2. Create the package scaffold

Set up the directory structure and manifest file for the package.

**Results:**

- Package directory named after the vendor (e.g., `acme/`)
- Package manifest: `acme/package.yaml`
- Event samples saved to `acme/tests/inputs/`

**Resources** (read via `tenzir-docs`):

- `guides/packages/create-a-package.md`

### 3. Add operators

Create user-defined operators for parsing and cleaning. Use the testing
framework to validate each step.

**Resources** (read via `tenzir-docs`):

- `guides/packages/add-operators.md`
- `guides/packages/test-packages.md`

#### 3.1 Parsing operator

Translate unstructured data into structured events. Only needed when the data is
raw text or contains unparsed fields (e.g., a JSON with an embedded `payload`
string).

**Results:**

- Operator: `acme::product::parse`
- Test(s): `acme/tests/product/parse.{tql,txt}`

**Resources** (read via `tenzir-docs`):

- `guides/parsing/parse-delimited-text.md`
- `guides/parsing/parse-string-fields.md`
- `tutorials/learn-idiomatic-tql.md`

#### 3.2 Cleaning operator

Ensure semantically rich types, replace sentinel values, and assign a proper
schema name.

**Results:**

- Operator: `acme::product::clean`
- Test(s): `acme/tests/product/clean.{tql,txt}`

**Resources** (read via `tenzir-docs`):

- `guides/normalization/clean-up-values.md`
- `guides/transformation/work-with-time.md`
- `tutorials/learn-idiomatic-tql.md`

### 4. Add examples

Add end-to-end examples showing how to use the operators. Reflect the collection
method typical for the vendor–product combination:

```tql
from_* {
  acme::product::parse
  acme::product::clean
}
```

**Results:**

- Examples that demonstrate the full pipeline

**Resources** (read via `tenzir-docs`):

- `guides/collecting.md`

### 5. Finalize package

Update the package manifest with accurate descriptions. Review operators for
idiomatic TQL. Verify all tests pass.

**Results:**

- TQL code adheres to idiomatic best practices
- All tests pass
- Updated and descriptive package manifest

**Resources** (read via `tenzir-docs`):

- `tutorials/learn-idiomatic-tql.md`
