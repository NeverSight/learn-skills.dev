---
name: tdd
description: Use when implementing any feature or bugfix - write test first, watch it fail, then implement
---

# Test-Driven Development

## The Rule

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

## Red-Green-Refactor Cycle

### RED - Write Failing Test

```python
def test_validates_empty_email():
    result = validate_email("")
    assert result.is_valid is False
    assert result.error == "Email required"
```

Run it. Watch it fail. Confirm it fails for the right reason (missing feature, not typo).

### GREEN - Minimal Code

Write the simplest code that makes the test pass:

```python
def validate_email(email: str) -> ValidationResult:
    if not email:
        return ValidationResult(is_valid=False, error="Email required")
    return ValidationResult(is_valid=True, error=None)
```

Run tests. All pass.

### REFACTOR

Clean up only if needed. Keep tests green.

### Repeat

Next failing test for next behavior.

## Verification

```bash
pytest path/to/test.py -v
```

Must see:
- Test fails first (RED)
- Test passes after implementation (GREEN)
- All other tests still pass

## Quick Checklist

- [ ] Test written before code
- [ ] Watched test fail
- [ ] Minimal implementation
- [ ] All tests pass
- [ ] No skipped steps

## Anti-Patterns

| Bad | Good |
|-----|------|
| Write code, then test | Write test, watch fail, then code |
| "I'll test after" | Test first proves it works |
| Multiple behaviors per test | One behavior per test |
| Test passes immediately | Test must fail first |
