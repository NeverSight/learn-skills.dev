---
name: phpunit-best-practices
description: PHPUnit testing best practices and conventions guide. This skill should be used when writing, reviewing, or refactoring PHPUnit tests to ensure consistent, maintainable, and effective test suites. Triggers on tasks involving test creation, test refactoring, test configuration, code coverage, data providers, mocking, or PHPUnit XML configuration.
license: MIT
metadata:
  author: pentiminax
  version: "1.0.0"
---

# PHPUnit Best Practices

Comprehensive testing best practices guide for PHPUnit applications, maintained by pentiminax. Contains 40 rules across 8 categories, prioritized by impact to guide automated test generation, refactoring, and code review.

## When to Apply

Reference these guidelines when:
- Writing new PHPUnit test classes or test methods
- Reviewing test code for quality and consistency
- Refactoring existing test suites
- Configuring PHPUnit XML settings
- Setting up code coverage and test organization

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Principles & Patterns | CRITICAL | `principle-` |
| 2 | Coding Standards | CRITICAL | `standard-` |
| 3 | Test Attributes | HIGH | `attr-` |
| 4 | Data Management | HIGH | `data-` |
| 5 | Test Documentation | MEDIUM | `doc-` |
| 6 | Mocking | MEDIUM | `mock-` |
| 7 | Integration Testing | MEDIUM | `integration-` |
| 8 | Configuration | LOW-MEDIUM | `config-` |

## Quick Reference

### 1. Principles & Patterns (CRITICAL)

- [rules/principle-aaa-pattern.md](rules/principle-aaa-pattern.md) - Structure tests with Arrange-Act-Assert
- [rules/principle-first-fast.md](rules/principle-first-fast.md) - Keep tests fast
- [rules/principle-first-isolated.md](rules/principle-first-isolated.md) - Ensure tests are independent
- [rules/principle-first-repeatable.md](rules/principle-first-repeatable.md) - Make tests deterministic
- [rules/principle-first-self-validating.md](rules/principle-first-self-validating.md) - Tests must have clear pass/fail
- [rules/principle-first-timely.md](rules/principle-first-timely.md) - Write tests alongside production code
- [rules/principle-dry-vs-damp.md](rules/principle-dry-vs-damp.md) - Balance DRY and readability in tests

### 2. Coding Standards (CRITICAL)

- [rules/standard-strict-types.md](rules/standard-strict-types.md) - Declare strict_types=1 in test files
- [rules/standard-final-classes.md](rules/standard-final-classes.md) - Make test classes final
- [rules/standard-snake-case-methods.md](rules/standard-snake-case-methods.md) - Use snake_case for test method names
- [rules/standard-psr4-naming.md](rules/standard-psr4-naming.md) - Follow PSR-4 naming and namespace conventions
- [rules/standard-psr12-formatting.md](rules/standard-psr12-formatting.md) - Apply PSR-12 code formatting
- [rules/standard-this-over-self.md](rules/standard-this-over-self.md) - Use $this over self:: for assertions
- [rules/standard-visibility-type-hints.md](rules/standard-visibility-type-hints.md) - Explicit visibility and type hints

### 3. Test Attributes (HIGH)

- [rules/attr-test-attribute.md](rules/attr-test-attribute.md) - Use #[Test] attribute with it_ prefix
- [rules/attr-covers-class.md](rules/attr-covers-class.md) - Use #[CoversClass] for coverage boundaries
- [rules/attr-uses-class.md](rules/attr-uses-class.md) - Use #[UsesClass] for dependency documentation
- [rules/attr-size-categories.md](rules/attr-size-categories.md) - Categorize tests by size
- [rules/attr-group.md](rules/attr-group.md) - Use #[Group] for arbitrary categorization
- [rules/attr-no-annotations.md](rules/attr-no-annotations.md) - Prefer PHP 8 attributes over PHPDoc annotations

### 4. Data Management (HIGH)

- [rules/data-provider.md](rules/data-provider.md) - Use #[DataProvider] for multiple scenarios
- [rules/data-provider-external.md](rules/data-provider-external.md) - Use #[DataProviderExternal] for shared data
- [rules/data-test-with.md](rules/data-test-with.md) - Use #[TestWith] for inline datasets
- [rules/data-factory-method.md](rules/data-factory-method.md) - Factory methods for SUT instantiation
- [rules/data-direct-instantiation.md](rules/data-direct-instantiation.md) - Direct instantiation for simple constructors

### 5. Test Documentation (MEDIUM)

- [rules/doc-testdox.md](rules/doc-testdox.md) - Use TestDox for executable specifications
- [rules/doc-testdox-attribute.md](rules/doc-testdox-attribute.md) - #[TestDox] attribute for custom display
- [rules/doc-readable-names.md](rules/doc-readable-names.md) - Readable test names as specifications

### 6. Mocking (MEDIUM)

- [rules/mock-chicago-vs-london.md](rules/mock-chicago-vs-london.md) - Chicago vs London TDD schools
- [rules/mock-prophecy.md](rules/mock-prophecy.md) - Prophecy for expressive test doubles
- [rules/mock-avoid-over-mocking.md](rules/mock-avoid-over-mocking.md) - Avoid over-mocking internal dependencies

### 7. Integration Testing (MEDIUM)

- [rules/integration-smoke-http.md](rules/integration-smoke-http.md) - HTTP controller smoke tests
- [rules/integration-smoke-cli.md](rules/integration-smoke-cli.md) - CLI command smoke tests
- [rules/integration-performance.md](rules/integration-performance.md) - Performance-aware test setup
- [rules/integration-singleton.md](rules/integration-singleton.md) - Singletons for stateless services
- [rules/integration-transactions.md](rules/integration-transactions.md) - Database transactions for test cleanup

### 8. Configuration (LOW-MEDIUM)

- [rules/config-testsuites.md](rules/config-testsuites.md) - Organize tests in named suites
- [rules/config-strictness.md](rules/config-strictness.md) - Enable strict mode settings
- [rules/config-source-coverage.md](rules/config-source-coverage.md) - Source directory for coverage analysis
- [rules/config-order-by.md](rules/config-order-by.md) - Test execution ordering strategies
- [rules/config-cache.md](rules/config-cache.md) - Cache directory for performance
- [rules/config-stop-on-failure.md](rules/config-stop-on-failure.md) - Stop on first failure for fast feedback

## How to Use

Read individual rule files for detailed explanations and code examples:

- [rules/principle-aaa-pattern.md](rules/principle-aaa-pattern.md)
- [rules/standard-final-classes.md](rules/standard-final-classes.md)

Each rule file contains:
- Brief explanation of why it matters
- Incorrect code example with explanation
- Correct code example with explanation
- Additional context and references
