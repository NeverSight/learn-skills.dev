---
name: test-namer
version: 1.0.0
description: "Guide for writing expressive, behavior-focused tests following Vladimir Khorikov's testing principles. Apply when writing, reviewing, or renaming any test (unit, integration, e2e) in any programming language. Triggers: writing tests, creating test files, adding test cases, reviewing test names, 'test naming', 'rename tests', 'Khorikov', or any test creation task. Covers: naming conventions (plain English over rigid policies), what to test (behavior not implementation), testing styles (output > state > communication), and pragmatic test investment."
---

# Test Namer

Write tests that describe **behavior in plain English**, not implementation details. Based on Vladimir Khorikov's testing principles.

## Naming Guidelines

### Rules

1. **No rigid naming policy** — never use `[MethodUnderTest]_[Scenario]_[ExpectedResult]` or similar templates
2. **Describe behavior to a non-programmer** familiar with the problem domain — a domain expert should understand the test name
3. **Separate words with underscores** in function/method names (not needed in string-based test names like JS/TS)
4. **Do not include the SUT's method name** in the test name — test behavior, not a method
5. **Use plain facts, not wishes** — write `is_invalid`, not `should_be_invalid`
6. **Use basic English grammar** — articles (`a`, `the`) improve readability
7. **Be specific** — `Delivery_with_a_past_date_is_invalid` beats `Delivery_with_invalid_date_is_invalid`

### Naming Progression Example

Starting from a rigid convention — progressively improve:

```
IsDeliveryValid_InvalidDate_ReturnsFalse     -- rigid, cryptic
Delivery_with_invalid_date_should_be_invalid  -- plain English (good start)
Delivery_with_past_date_should_be_invalid     -- more specific
Delivery_with_past_date_is_invalid            -- fact, not wish
Delivery_with_a_past_date_is_invalid          -- natural grammar (final)
```

### Exception: Utility Code

For utility/helper code without business logic, referencing the method name is acceptable since the behavior doesn't mean anything to business people:

```
Sum_of_two_numbers
Trimmed_string_has_no_leading_whitespace
```

## Language-Specific Adaptations

### Go

Test functions MUST start with `Test` (language requirement). Append the descriptive name:

```go
func TestDelivery_with_a_past_date_is_invalid(t *testing.T) { ... }
```

Subtests via `t.Run` have full naming freedom:

```go
func TestDelivery(t *testing.T) {
    t.Run("with a past date is invalid", func(t *testing.T) { ... })
    t.Run("with a future date is valid", func(t *testing.T) { ... })
}
```

Table-driven tests — use descriptive `name` fields, not method signatures:

```go
tests := []struct {
    name string
    // ...
}{
    {"delivery with a past date is invalid", ...},
    {"delivery for tomorrow is valid", ...},
}
```

### Python (pytest)

Functions must start with `test_`. Append the descriptive name in snake_case:

```python
def test_delivery_with_a_past_date_is_invalid():
    ...

def test_new_customer_starts_in_pending_state():
    ...
```

### Java / Kotlin (JUnit)

`@Test` annotation handles discovery. Method names are fully descriptive:

```java
@Test
void Delivery_with_a_past_date_is_invalid() { ... }

@Test
void New_customer_starts_in_pending_state() { ... }
```

Kotlin supports backtick-quoted names for natural language:

```kotlin
@Test
fun `delivery with a past date is invalid`() { ... }
```

### JavaScript / TypeScript (Jest, Vitest, Mocha)

String-based names — use natural language directly, no underscores needed:

```javascript
it("delivery with a past date is invalid", () => { ... });

test("new customer starts in pending state", () => { ... });

describe("delivery validation", () => {
    it("rejects past dates", () => { ... });
    it("accepts future dates", () => { ... });
});
```

### C# / .NET

`[Fact]` or `[Test]` attribute. Full freedom with underscores:

```csharp
[Fact]
public void Delivery_with_a_past_date_is_invalid() { ... }
```

### Rust

`#[test]` attribute. Standard snake_case identifiers:

```rust
#[test]
fn delivery_with_a_past_date_is_invalid() { ... }
```

## Test Class / File Naming

Use `[ClassName]Tests` or `[feature]_test` as an **entry point**, not a boundary. The unit in unit testing is a unit of behavior, not a class — it can span multiple classes.

## What to Test — Behavior, Not Implementation

- **Test observable behavior**: outputs, state changes, side effects visible to clients
- **Never test implementation details**: internal collaborations, private methods, exact SQL queries, specific method call sequences
- Renaming an internal method should never break a test
- If a test fails during a legit refactoring, the test is coupled to implementation

## Testing Styles (in order of preference)

1. **Output-based** — feed input, verify output. Best false-positive resistance. Use for pure functions and domain logic.
2. **State-based** — perform operation, verify resulting state via public API. Good when output verification isn't possible.
3. **Communication-based (mocks)** — verify interactions with dependencies. Use ONLY for uncontrolled external dependencies (SMTP, message bus, third-party APIs). Never mock domain objects or stable dependencies.

For deeper guidance on testing styles, value proposition, and pragmatic testing strategies, see [testing-philosophy.md](references/testing-philosophy.md).

For common anti-patterns to avoid, see [anti-patterns.md](references/anti-patterns.md).
