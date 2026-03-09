---
name: testing-unit
description: Run unit tests for individual code components
license: MIT
compatibility: opencode
metadata:
  audience: developers
  category: testing
---

# Unit Testing

Test individual functions, methods, and classes in isolation from dependencies.

## When to use me

Use this skill when:
- Writing new code to ensure it works correctly
- Refactoring existing code without breaking functionality
- During continuous integration to catch regressions early
- Following Test-Driven Development (TDD) practices

## What I do

- Identify testable units (functions, methods, classes)
- Set up test fixtures and mock dependencies
- Write test cases covering normal, edge, and error conditions
- Run unit tests and report pass/fail status
- Measure code coverage for tested units
- Integrate with CI/CD pipelines for automated testing

## Examples

```bash
# Run unit tests with common frameworks
npm test                    # Node.js with Jest/Mocha
python -m pytest tests/     # Python with pytest
go test ./...              # Go built-in testing
cargo test                 # Rust with Cargo
dotnet test               # .NET with xUnit/NUnit

# Run specific test files
npm test -- src/utils.test.js
pytest tests/test_auth.py

# Run with coverage reporting
npm test -- --coverage
pytest --cov=src tests/
```

## Output format

```
✓ Test Suite: UserService
  ✓ should create user with valid data
  ✓ should reject duplicate email
  ✗ should handle database connection errors (failed)
    Expected: "Connection error handled"
    Received: "Unhandled database error"

Coverage: 92% (15/16 lines)
Failed: 1 test
```

## Notes

- Unit tests should be fast (milliseconds per test)
- Mock external dependencies (databases, APIs, filesystem)
- Aim for high code coverage (80-90%+)
- Tests should be independent and order-agnostic
- Follow AAA pattern: Arrange, Act, Assert
- Use test doubles (mocks, stubs, spies) appropriately
