---
name: zod-contract-testing
description: "Validates Zod schema parsing at boundaries. Tests valid/invalid inputs, schema evolution, refinement coverage, and compound state matrices (2^N optional field combinations)."
---

# Zod Contract Testing

Test schemas at boundaries — not just happy-path inputs.

Schemas define contracts between systems. A schema that accepts invalid data is a security hole. A schema that rejects valid data is a broken integration. This skill teaches you to systematically test schemas at system boundaries.

**When to use**: Testing API request/response schemas, WebSocket message validation, database record parsing, external data ingestion, any Zod schema at a system boundary.

**When not to use**: Internal type assertions, UI component props, type definitions without runtime validation.

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "The type system ensures correctness" | TypeScript doesn't exist at runtime | Test Zod parsing with real data |
| "I tested valid inputs" | Invalid inputs cause production errors | Test rejection of invalid inputs |
| "Refinements are simple" | `.refine()` failures are easy to miss | Test BOTH passing and failing cases |
| "Optional fields are optional" | 2^N combinations have hidden bugs | Use compound state matrix |

---

## What To Protect (Start Here)

Before generating schema tests, identify which data integrity decisions apply to your code:

| Decision | Question to Answer | If Yes → Use |
|----------|--------------------|--------------|
| Invalid data must be rejected with specific errors | What malformed inputs could reach this boundary? | `testInvalidInput` with `expectedPath` |
| Schema changes must not break old data | Is there serialized/stored data in the old format? | `testSchemaEvolution` |
| Version upgrades must be backward compatible | Do multiple schema versions coexist in production? | `generateVersionCompatibilityMatrix` |
| Optional field combinations have hidden bugs | Does this schema have 3+ optional fields with interacting refinements? | `generateCompoundStateMatrix` |
| Refinements must reject specific threats | What invalid-but-plausible input does each `.refine()` guard against? | `testRefinement` |

**Do not generate tests for decisions the human hasn't confirmed.** A schema test that checks "valid input passes" without naming the threat it guards against is slop — it'll pass even if the schema accepts everything.

---

## Included Utilities

```typescript
import {
  testValidInput,
  testInvalidInput,
  testSchemaEvolution,
  generateVersionCompatibilityMatrix,
  assertVersionCompatibility,
  testRefinement,
  generateCompoundStateMatrix,
  formatStateMatrix,
  applyCompoundState,
} from './schema-boundary.ts';
```

## Core Workflow

### Step 1: Test Valid Inputs

Verify the schema accepts all valid input shapes:

```typescript
import { z } from 'zod';

const UserSchema = z.object({
  name: z.string(),
  age: z.number().optional(),
});

it('accepts valid user', () => {
  testValidInput(UserSchema, { name: 'Alice', age: 30 });
  testValidInput(UserSchema, { name: 'Bob' });  // age optional
});
```

### Step 2: Test Invalid Inputs

Verify the schema rejects invalid data and errors at the correct path:

```typescript
it('rejects missing required field', () => {
  testInvalidInput(UserSchema, {}, 'name');  // Error at 'name' path
});

it('rejects wrong type', () => {
  testInvalidInput(UserSchema, { name: 123 }, 'name');
});

it('rejects unknown fields with strict schema', () => {
  const StrictUserSchema = UserSchema.strict();
  testInvalidInput(StrictUserSchema, { name: 'Alice', role: 'admin' });
});
```

### Step 3a: Test Schema Evolution

When schemas change, old serialized data must still parse:

```typescript
// Old schema: { name: string }
// New schema: { name: string, email?: string }

const NewUserSchema = z.object({
  name: z.string(),
  email: z.string().email().optional(),
});

it('backward compatible with old data', () => {
  const oldData = { name: 'Alice' };  // No email field
  testSchemaEvolution(NewUserSchema, oldData);
});
```

### Step 3b: Build Version Compatibility Matrix

For evolving contracts, check `vN -> vN+1` and `vN -> vN+2` explicitly:

```typescript
const versions = [
  { version: 'v1', schema: V1Schema, fixtures: [v1Payload] },
  { version: 'v2', schema: V2Schema, fixtures: [v2Payload] },
  { version: 'v3', schema: V3Schema, fixtures: [v3Payload] },
];

const matrix = generateVersionCompatibilityMatrix(versions);

// Enforce only adjacent upgrades (vN -> vN+1)
assertVersionCompatibility(versions, 1);

// Optionally enforce two-hop upgrades (vN -> vN+2)
assertVersionCompatibility(versions, 2);
```

### Step 4: Test Refinements

Every `.refine()` MUST have tests for both passing and failing cases:

```typescript
const PositiveNumberSchema = z.object({
  value: z.number().refine(n => n > 0, 'Value must be positive'),
});

it('refinement: positive vs non-positive', () => {
  testRefinement(
    PositiveNumberSchema,
    { value: 10 },           // Passing case
    { value: -5 },           // Failing case
    'must be positive',      // Expected error message
  );
});
```

### Step 5: Generate Compound State Matrix

For schemas with N optional fields, there are 2^N possible combinations. For 3-4 fields, test exhaustively. For 5+, switch to pairwise coverage (see decision table below):

```typescript
// Cell schema: value?, candidates?, isGiven?
// 2^3 = 8 combinations

const matrix = generateCompoundStateMatrix(['value', 'candidates', 'isGiven']);
console.log(formatStateMatrix(matrix));
/*
| # | value | candidates | isGiven | Label |
|---|-------|------------|---------|-------|
| 0 | -     | -          | -       | (empty) |
| 1 | Y     | -          | -       | value |
| 2 | -     | Y          | -       | candidates |
| 3 | Y     | Y          | -       | value + candidates |
| 4 | -     | -          | Y       | isGiven |
| 5 | Y     | -          | Y       | value + isGiven |
| 6 | -     | Y          | Y       | candidates + isGiven |
| 7 | Y     | Y          | Y       | value + candidates + isGiven |
*/
```

### Step 6: Apply Matrix to Schema Tests

Generate test inputs from the matrix:

```typescript
const CellSchema = z.object({
  value: z.number().optional(),
  candidates: z.array(z.number()).optional(),
  isGiven: z.boolean().optional(),
}).refine(
  cell => !(cell.isGiven && cell.value === undefined),
  'Given cells must have a digit value',
);

describe('cell schema compound states', () => {
  const matrix = generateCompoundStateMatrix(['value', 'candidates', 'isGiven']);
  const template = { value: 5, candidates: [1, 3, 7], isGiven: true };

  for (const entry of matrix) {
    const input = applyCompoundState(entry, template);
    const shouldFail = input.isGiven && input.value === undefined;

    it(`${entry.label}: ${shouldFail ? 'rejects' : 'accepts'}`, () => {
      if (shouldFail) {
        testInvalidInput(CellSchema, input);  // Object-level .refine() reports at root path
      } else {
        testValidInput(CellSchema, input);
      }
    });
  }
});
```

---

## Compound State Matrix Decision

| Optional Fields | Combinations | Testing Approach |
|-----------------|--------------|------------------|
| 0-2 | 1-4 | Enumerate manually |
| 3 | 8 | Use matrix, manageable |
| 4 | 16 | Use matrix, essential |
| 5+ | 32+ | Switch to [pairwise-test-coverage](https://github.com/apankov1/quality-engineering/tree/main/skills/pairwise-test-coverage) — covers all field pairs in near-minimal test cases |

---

## Violation Rules

### missing_invalid_input_test
Every Zod schema MUST have tests for invalid inputs, not just valid ones.
**Severity**: must-fail

### missing_refinement_coverage
Every `.refine()` or `.superRefine()` MUST have tests for both the passing AND failing case.
**Severity**: must-fail

### missing_compound_state_test
Schemas with 3+ optional fields SHOULD use compound state matrix. For 5+ fields, switch to [pairwise-test-coverage](https://github.com/apankov1/quality-engineering/tree/main/skills/pairwise-test-coverage) rather than testing all 2^N individually.
**Severity**: should-fail

### schema_not_at_boundary
Zod parsing MUST happen at system boundaries (API handlers, WebSocket messages, database reads), not inside business logic.
**Severity**: should-fail

### type_assertion_instead_of_parse
Use `Schema.parse()` or `Schema.safeParse()`, NEVER `as Type` casts for external data.
**Severity**: must-fail

### missing_schema_version_test
Event schemas with `schemaVersion` field MUST have contract tests verifying that each version parses correctly and upcasters produce valid output for the target version.
**Severity**: must-fail

### missing_boundary_contract_test
Typed RPC interfaces used for cross-service or cross-DO communication MUST have contract tests verifying request/response schemas parse correctly at both caller and callee boundaries.
**Severity**: should-fail

---

## Companion Skills

This skill teaches **testing methodology**, not Zod API usage. For broader methodology:

- Search `zod` on [skills.sh](https://skills.sh) for schema authoring, transforms, error handling, and framework integrations
- Our utilities work with any Zod version (v3, v4) via the `ZodLikeSchema` interface — no version lock-in
- Schemas with 5+ optional fields produce 32+ combinations — use [pairwise-test-coverage](https://github.com/apankov1/quality-engineering/tree/main/skills/pairwise-test-coverage) for near-minimal coverage of all field pairs
- Schema parsing at boundaries often logs errors — use [observability-testing](https://github.com/apankov1/quality-engineering/tree/main/skills/observability-testing) to assert structured log output on validation failures
- Schema evolution testing pairs with resilience — use [fault-injection-testing](https://github.com/apankov1/quality-engineering/tree/main/skills/fault-injection-testing) for retry and circuit breaker testing around schema-validated endpoints

---

## Quick Reference

| Utility | When | Example |
|---------|------|---------|
| `testValidInput` | Verify acceptance | `testValidInput(schema, { name: 'Alice' })` |
| `testInvalidInput` | Verify rejection | `testInvalidInput(schema, {}, 'name')` |
| `testSchemaEvolution` | Backward compat | `testSchemaEvolution(newSchema, oldData)` |
| `generateVersionCompatibilityMatrix` | Version matrix | `generateVersionCompatibilityMatrix(versions)` |
| `assertVersionCompatibility` | Enforce vN->vN+K | `assertVersionCompatibility(versions, 2)` |
| `testRefinement` | Pass + fail | `testRefinement(schema, passing, failing, message)` |
| `generateCompoundStateMatrix` | Optional fields | `generateCompoundStateMatrix(['a', 'b', 'c'])` |
| `applyCompoundState` | Generate input | `applyCompoundState(entry, template)` |

See [patterns.md](./references/patterns.md) for Zod-specific patterns, boundary testing methodology, and integration with TypeScript strict mode.
