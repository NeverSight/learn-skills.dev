---
name: test-first-thinking
description: |
  Enforces the discipline of thinking about tests, features, and maintainability BEFORE writing implementation code. Use when starting new classes/methods, refactoring existing code, or when asked to "think about tests first", "design for testability", "what tests do I need", "test-first approach", or "TDD thinking". Promotes simple, maintainable designs by considering testability upfront. Works with any codebase requiring test coverage and quality standards.

---

# Test-First Thinking

## Overview

Test-first thinking is a design discipline that requires thinking about features, testability, and maintainability BEFORE writing implementation code. This is not strict TDD (Test-Driven Development), but rather a mental model that ensures you design simple, testable interfaces from the start.

**Core Principle**: If you can't easily describe what tests you'd write, your design may be too complex.

## When to Use This Skill

### Explicit Triggers
- "Think about tests first"
- "Design for testability"
- "What tests do I need?"
- "Use test-first approach"
- "TDD thinking"
- "How should I test this?"

### Implicit Triggers
- Before creating a new class or method
- Before refactoring existing code
- When starting a new feature implementation
- When reviewing code that lacks tests
- When design feels overly complex

### Debugging Triggers
- Tests are difficult to write for existing code
- Code requires extensive mocking to test
- Implementation has grown too complex
- Edge cases keep surfacing after deployment

## What This Skill Does

This skill guides you through a pre-implementation checklist that ensures:

1. **Feature enumeration** - List all expected behaviors before coding
2. **Simplicity check** - Consider maintainability and complexity
3. **Test identification** - Know what tests validate each behavior
4. **Interface design** - Create signatures that make testing easy
5. **Edge case awareness** - Think through error conditions upfront

## The Test-First Checklist

Run through this checklist BEFORE writing implementation code:

### 1. Enumerate Features and Behaviors

**Ask yourself:**
- What should this class/method do?
- What are the expected inputs and outputs?
- What transformations or side effects occur?

**Example:**
```python
# Before implementing UserRegistration class, list features:
# 1. Validate email format
# 2. Check if email already exists
# 3. Hash password securely
# 4. Store user in database
# 5. Send confirmation email
# 6. Return success/failure result
```

### 2. Consider Edge Cases and Error Conditions

**Ask yourself:**
- What can go wrong?
- How should errors be handled?
- What are the boundary conditions?

**Example:**
```python
# Edge cases for UserRegistration:
# - Invalid email format
# - Duplicate email
# - Weak password
# - Database connection failure
# - Email service unavailable
# - Null/empty inputs
```

### 3. Identify Required Tests

**Ask yourself:**
- What test cases validate each feature?
- How do I verify error handling?
- What mocks/fixtures are needed?

**Example:**
```python
# Tests needed for UserRegistration:
# - test_valid_registration_succeeds()
# - test_invalid_email_raises_validation_error()
# - test_duplicate_email_returns_failure()
# - test_weak_password_raises_validation_error()
# - test_database_failure_returns_failure()
# - test_email_service_failure_logs_warning()
# - test_null_inputs_raise_value_error()
```

### 4. Design for Testability

**Ask yourself:**
- Does this interface make testing easy?
- Can I test without complex mocking?
- Are dependencies explicit and injectable?
- Is the function pure (no hidden side effects)?

**Good Design (Testable):**
```python
def register_user(
    email: str,
    password: str,
    user_repo: UserRepository,
    email_service: EmailService
) -> Result[User, RegistrationError]:
    """Register new user with explicit dependencies."""
    # Dependencies are injected - easy to mock
    # Returns Result type - easy to test both paths
    # Pure function - predictable behavior
```

**Bad Design (Hard to Test):**
```python
def register_user(email: str, password: str) -> None:
    """Register new user."""
    # Hidden dependency on global database connection
    # Hidden dependency on email service
    # No return value - can't verify success
    # Side effects make testing difficult
```

### 5. Look at Existing Tests First

**When editing existing code:**
1. Read the test file BEFORE modifying implementation
2. Existing tests show what features the code should have
3. If tests are missing, write them first
4. If tests are hard to understand, the code is likely too complex

**Example:**
```bash
# Before editing src/auth/registration.py:
# 1. Read tests/unit/auth/test_registration.py
# 2. Understand what behaviors are tested
# 3. Identify what's NOT tested (gaps)
# 4. Add tests for new behavior
# 5. THEN modify implementation
```

### 6. Implement

**Only after completing steps 1-5:**
- Write the implementation
- Run tests continuously as you code
- Refactor based on test feedback
- Add tests if new edge cases emerge

## Quick Reference: Red Flags

Stop and reconsider if you encounter:

- **"I'll write tests later"** - Write tests now or redesign
- **"This needs extensive mocking"** - Dependencies may be too coupled
- **"I can't describe what tests I'd write"** - Design is too complex
- **"Tests would be too complicated"** - Implementation is too complicated
- **"This is hard to test"** - This is hard to maintain
- **"I need to mock everything"** - Too many dependencies
- **"Tests keep breaking"** - Implementation is too fragile

## Benefits

| Aspect | Before Test-First Thinking | After Test-First Thinking |
|--------|---------------------------|---------------------------|
| Design Complexity | Grows organically, becomes tangled | Kept simple by testability constraint |
| Test Coverage | Written after (if at all), incomplete | Designed in from start, comprehensive |
| Edge Cases | Discovered in production | Identified during design |
| Debugging Time | High - complex interactions | Low - isolated, testable units |
| Refactoring Confidence | Low - fear of breaking things | High - tests verify behavior |
| Maintenance Cost | High - difficult to change | Low - clear contracts and tests |

## Integration with Quality Gates

This skill supports:
- **quality-run-quality-gates** - Ensures tests exist before marking complete
- **quality-capture-baseline** - Requires test coverage metrics
- **quality-detect-regressions** - Verifies tests pass consistently
- **test-debug-failures** - Makes test failures easier to diagnose

## Expected Outcomes

### Success
```
Before implementing PaymentProcessor class:

Features enumerated:
✅ Process credit card payment
✅ Validate payment amount
✅ Handle payment gateway response
✅ Store transaction record
✅ Send receipt email

Edge cases identified:
✅ Invalid card number
✅ Insufficient funds
✅ Gateway timeout
✅ Network failure
✅ Duplicate transaction

Tests identified:
✅ test_valid_payment_succeeds()
✅ test_invalid_card_raises_error()
✅ test_insufficient_funds_returns_failure()
✅ test_gateway_timeout_retries()
✅ test_duplicate_transaction_prevented()

Interface designed:
✅ Dependencies injected (gateway, transaction_repo)
✅ Returns Result type for error handling
✅ Pure function - no hidden state
✅ Easy to mock gateway for testing

Ready to implement with confidence!
```

### Failure (Redesign Needed)
```
Before implementing ReportGenerator class:

Attempted to list features:
❌ "Generate reports" - too vague
❌ "Process data" - what data? how?
❌ Multiple responsibilities identified
❌ Can't describe specific behaviors

Attempted to identify tests:
❌ "Test that it works" - not specific enough
❌ Would need to mock 15+ dependencies
❌ No clear success/failure paths
❌ Can't isolate behaviors for testing

Red flags:
❌ Design too complex
❌ Unclear responsibilities
❌ Too many dependencies
❌ Not testable in current form

Action: Break into smaller, focused classes:
- ReportDataFetcher (single responsibility)
- ReportFormatter (single responsibility)
- ReportExporter (single responsibility)

Retry test-first thinking for each class individually.
```

## Notes

1. **This is NOT strict TDD** - You don't have to write tests first, but you must THINK about tests first
2. **Mental model matters** - The discipline of considering testability improves design
3. **Start simple** - If you can't explain it simply, you don't understand it well enough
4. **Tests reveal design flaws** - Hard to test = hard to maintain
5. **Iterate** - If tests are difficult, redesign the interface
6. **Use existing tests as documentation** - They show what the code should do
7. **Testability IS maintainability** - They're the same thing

## Supporting Files

This skill is intentionally minimal - it's a thinking discipline, not a complex workflow. No additional scripts or references are needed.
