---
name: slop-test-detector
description: "Static analyzer that detects 18 slop patterns in test code — tests that compile and pass but catch zero bugs."
---

# Slop Test Detector

Agents generate tests that compile, pass, and increase coverage — but catch zero bugs. This skill detects those patterns programmatically.

**When to use**: Auditing existing test files for quality. Validating generated tests before writing them to disk. Enforcing the `// Defect:` comment convention.

**When not to use**: Evaluating test *strategy* (what to test). Measuring code coverage. Reviewing production code quality.

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "It compiles and passes" | Slop tests always pass — that's the problem | Run `analyzeTestFile()` and check must-fail findings |
| "It has a Defect comment" | Comment can be trivial or copied from the test name | Check `trivial_defect_comment` findings |
| "It has assert.ok(result)" | Truthiness checks pass for any non-null value | Verify assert.equal/deepEqual on specific values |
| "It increases coverage" | Coverage counts lines executed, not bugs caught | Check that assertions verify behavior, not just reachability |

---

## What To Protect (Start Here)

Before auditing or generating tests, identify which slop patterns apply:

| Decision | Question to Answer | If Yes → Check Rule |
|----------|--------------------|---------------------|
| Test body is meaningful | Does the test have at least one assertion that can fail? | `empty_test_body`, `commented_out_assertions` |
| Assertions verify behavior | Do assertions compare computed values to expected values? | `tautological_assertion`, `self_referential_assertion` |
| Defect comment explains impact | Does the comment explain what breaks in production? | `missing_defect_comment`, `trivial_defect_comment` |
| Assertions check values, not types | Is the test checking actual output, not just typeof? | `assert_on_type_not_value`, `truthiness_only` |
| Error paths are tested | Does the describe block include negative test cases? | `no_negative_test` |
| Tests vary their inputs | Do sibling tests exercise different code paths? | `no_input_variation`, `duplicate_assertion_set` |
| Assertions test computed values | Are assertions checking results, not echoing construction literals? | `literal_roundtrip`, `schema_success_only` |
| Assertions always execute | Can the test pass without any assertion running? | `conditional_assertion` |
| Property tests are meaningful | Do fc.property callbacks assert on all paths with varied inputs? | `vacuous_property` |
| Tests exercise production code | Does the test call an imported function, not just builtins? | `no_production_call` |
| Assertions can actually fail | Is the assertion mathematically capable of failing? | `impossible_assertion` |

---

## Assertion API Support

The detector recognizes `node:assert`, vitest/Jest `expect()`, and chai `expect()` patterns:

| `node:assert` | vitest/Jest | chai | Mapped rule check |
|---|---|---|---|
| `assert.equal(x, y)` | `expect(x).toBe(y)` | `expect(x).to.equal(y)` | tautological, self-referential, type-not-value |
| `assert.deepEqual(x, y)` | `expect(x).toEqual(y)` | `expect(x).to.deep.equal(y)` | self-referential, duplicate |
| `assert.ok(x)` | `expect(x).toBeTruthy()` | `expect(x).to.be.ok` | truthiness-only, return-type-only |
| `assert.throws(fn)` | `expect(fn).toThrow()` | `expect(fn).to.throw()` | no-negative-test |
| `assert.rejects(p)` | `expect(p).rejects.toThrow()` | — | no-negative-test |

Chain modifiers `.not`, `.resolves`, `.rejects` and chai language chains (`.to`, `.be`, `.have`, `.been`, etc.) are handled. Multiline chains (matcher on next line) are supported. Commented-out `expect()` calls are detected. Chai property assertions (`expect(x).to.be.true`) are supported.

---

## Included Utilities

```typescript
import {
  analyzeTestFile,
  validateTestBlock,
  formatReport,
  formatReportJSON,
  getPreset,
  parseImports,
  parseTestFile,
} from './slop-detector.ts';
```

## Configuration

### Presets

Three built-in presets control which rules are active:

| Preset | Rules | Default threshold | Use case |
|--------|-------|-------------------|----------|
| `balanced` | 16 rules (no defect-comment rules) | 80 | **Default.** Conservative, low noise |
| `strict` | All 18 rules | 90 | Teams that enforce `// Defect:` comments |
| `advisory` | All 18 rules | 0 | Report everything, fail nothing |

```typescript
import { getPreset } from './slop-detector.ts';

const config = getPreset('balanced'); // default
const strict = getPreset('strict');   // all rules enforced
```

### Custom Configuration

```typescript
import { type SlopConfig, getPreset } from './slop-detector.ts';

const config: SlopConfig = {
  ...getPreset('balanced'),
  assertionEquivalents: ['assertLogEntry', 'assertNoLogsAbove'],
  scoreThreshold: 90,
};
```

- **`enabledRules`**: `Set<SlopRule>` — which rules produce findings
- **`assertionEquivalents`**: `string[]` — function names treated as assertions (prevents false `empty_test_body`)
- **`scoreThreshold`**: `number` — minimum passing score (for CI gating)

### Suppression Comments

Suppress specific findings with a required reason:

```typescript
// slop-ignore: tautological_assertion — intentional canary test for CI pipeline health
it("canary", () => {
  assert.ok(true);
});
```

- The `— reason` is **required** — suppressions without a reason are ignored
- Multiple rules: `// slop-ignore: empty_test_body, truthiness_only — stub pending #1234`
- Place on the line before `it()` or anywhere inside the test body

## Core Workflow

### Step 1: Audit Existing Files

```typescript
import { readFileSync } from 'node:fs';

const source = readFileSync('my-module.spec.ts', 'utf-8');
const report = analyzeTestFile(source, 'my-module.spec.ts');
console.log(formatReport(report));
```

### Step 2: Validate During Generation

Before writing a generated test to disk, check for slop:

```typescript
const findings = validateTestBlock(`
  // Defect: if the parser miscounts blocks then all downstream rules produce wrong results
  it("parses correctly", () => {
    assert.equal(result, expected);
  });
`);

if (findings.some(f => f.severity === 'must-fail')) {
  // Fix before writing
}
```

### Step 3: Machine-Readable Output (CI)

```typescript
const report = analyzeTestFile(source, filePath, getPreset('balanced'));
const json = formatReportJSON(report);
// Outputs structured JSON with filePath, score, summary, findings[]
```

### Step 4: Interpret the Score

The score formula weights must-fail findings (1.0) higher than should-fail (0.3):

```
score = max(0, round(100 × (1 - weightedFindings / testCount)))
```

- **100**: No slop detected
- **90-99**: Minor should-fail findings (missing comments, no negative tests)
- **Below 80**: Significant quality issues — review must-fail findings first

---

## Violation Rules

| Rule | Description | Severity | Default |
|------|-------------|----------|---------|
| `empty_test_body` | `it()` with zero assertions or assertion-equivalent calls | must-fail | on |
| `commented_out_assertions` | All `assert.*` calls commented out, zero active | must-fail | on |
| `tautological_assertion` | `assert.equal(LITERAL, LITERAL)` or `assert.ok(true)` | must-fail | on |
| `self_referential_assertion` | `assert.equal(x, x)` where both args textually identical | must-fail | on |
| `missing_defect_comment` | `it()` with no `// Defect:` in preceding 3 lines | should-fail | **opt-in** |
| `trivial_defect_comment` | `// Defect:` exists but fewer than 10 words | should-fail | **opt-in** |
| `assert_on_type_not_value` | All assertions check `typeof`, no value checks | should-fail | on |
| `truthiness_only` | All assertions are `assert.ok(identifier)` | should-fail | on |
| `no_negative_test` | `describe` with 3+ tests, zero `assert.throws`/`.rejects` | should-fail | on |
| `duplicate_assertion_set` | Two `it()` blocks with identical normalized assertion sequences | should-fail | on |
| `assert_return_type_only` | Sole assertion is `assert.ok(r)` on a return value | should-fail | on |
| `no_input_variation` | Sibling `it()` blocks pass identical args to same function | should-fail | on |
| `literal_roundtrip` | Assertion compares `obj.field` to the same literal used to construct `obj` | should-fail | on |
| `schema_success_only` | `safeParse()` result checked for `.success` but never `.data` or `.error.issues` | should-fail | on |
| `conditional_assertion` | All assertions are inside `if`/`switch` blocks — test may silently pass | must-fail | on |
| `vacuous_property` | `fc.property` callback has `return true` path with zero assertions, or all generators are `fc.constant` | should-fail | on |
| `no_production_call` | Test body calls no imported production function — only builtins or language guarantees | should-fail | on |
| `impossible_assertion` | Assertion is mathematically impossible to fail (e.g., `.length >= 0`) | should-fail | on |

**opt-in** rules are only active in the `strict` preset. Use `getPreset('strict')` or add them to a custom `enabledRules` set.

---

## Definition of Done

- [ ] `analyzeTestFile()` returns zero must-fail findings
- [ ] All should-fail findings are reviewed and either fixed or justified
- [ ] Score is 90 or above
- [ ] `slop-detector.spec.ts` itself passes all its own rules

---

## Companion Skills

- [observability-testing](../observability-testing/) — Structured log assertions that the slop detector validates for completeness
- [fault-injection-testing](../fault-injection-testing/) — Circuit breaker and retry tests where empty_test_body and no_negative_test rules are most likely to fire
- [breaking-change-detector](../breaking-change-detector/) — Contract classification tests where duplicate_assertion_set detects copy-paste patterns
- [model-based-testing](../model-based-testing/) — State machine transition matrix tests where no_input_variation catches redundant transition checks
- [pairwise-test-coverage](../pairwise-test-coverage/) — Combinatorial test generation where truthiness_only and assert_return_type_only are common slop patterns

---

See [patterns.md](./references/patterns.md) for all 12 patterns with before/after code examples.
