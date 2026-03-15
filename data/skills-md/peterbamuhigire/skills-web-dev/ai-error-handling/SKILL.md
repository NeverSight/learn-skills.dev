---
name: ai-error-handling
description: Validation and error handling for AI-generated code. Use when verifying AI output, building production code, or ensuring code correctness. Enforces automatic quality checks and validation loops.
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# AI Error Handling & Validation

## When to Use This Skill

Use when:
- Claude generates code (always validate)
- Building production code (quality gates required)
- Reviewing AI output (systematic verification)
- Ensuring code correctness (automated checks)

**This skill automatically enforces validation patterns.**

---

## The 5-Layer Validation Stack

Every AI-generated code MUST pass through all 5 layers:

```
Layer 1: Syntax Check ─→ Can it parse?
    ↓
Layer 2: Requirement Check ─→ Does it meet specs?
    ↓
Layer 3: Test Check ─→ Do tests pass?
    ↓
Layer 4: Security Check ─→ Any vulnerabilities?
    ↓
Layer 5: Documentation Check ─→ Can Claude explain it?
    ↓
APPROVED ✓
```

---

## Layer 1: Syntax Validation

**Rule:** Code must be syntactically correct before anything else.

### JavaScript/TypeScript
```bash
# Syntax check
node --check file.js

# TypeScript check
tsc --noEmit file.ts

# ESLint
eslint file.js
```

### PHP
```bash
# Syntax check
php -l file.php

# Code style
phpcs file.php

# Static analysis
phpstan analyze file.php
```

### Python
```bash
# Syntax check
python -m py_compile file.py

# Type checking
mypy file.py

# Linting
pylint file.py
```

**If syntax fails:**
```markdown
Ask Claude: "Fix syntax errors in [file]:
[Paste error output]

Correct the code to parse successfully."
```

---

## Layer 2: Requirement Validation

**Rule:** Code must implement ALL requirements, not just some.

### Validation Process

```javascript
/**
 * REQUIREMENT CHECKLIST
 *
 * Requirement 1: Validate user email format
 * ✓ Implemented at line 15 (regex validation)
 * ✓ Test exists: test/user.spec.js:42
 *
 * Requirement 2: Check email uniqueness in database
 * ✓ Implemented at line 23 (database query)
 * ✓ Test exists: test/user.spec.js:58
 *
 * Requirement 3: Return appropriate error codes
 * ✓ 400 for invalid format (line 18)
 * ✓ 409 for duplicate (line 27)
 * ✓ Test exists: test/user.spec.js:71, 85
 *
 * Requirement 4: Hash password before storing
 * ✗ MISSING - Not implemented
 * ✗ No test found
 *
 * STATUS: INCOMPLETE (1/4 requirements missing)
 */
```

**If requirements fail:**
```markdown
Ask Claude: "This code doesn't meet Requirement X:

Expected: [describe requirement]
Actual: [describe what's missing]

Add the missing functionality."
```

---

## Layer 3: Test Validation

**Rule:** Code without tests is unverified code.

### Required Test Categories

```javascript
// Test Category 1: Happy Path
it('should register user with valid data', async () => {
  const result = await registerUser({
    email: 'valid@example.com',
    password: 'SecurePass123'
  });
  expect(result.success).toBe(true);
});

// Test Category 2: Edge Cases
it('should handle email with special characters', async () => {
  const result = await registerUser({
    email: 'user+tag@sub.example.com',
    password: 'SecurePass123'
  });
  expect(result.success).toBe(true);
});

it('should reject email without domain', async () => {
  const result = await registerUser({
    email: 'invalid',
    password: 'SecurePass123'
  });
  expect(result.success).toBe(false);
});

// Test Category 3: Error Cases
it('should handle database connection failure', async () => {
  // Mock database failure
  jest.spyOn(db, 'query').mockRejectedValue(new Error('Connection lost'));

  const result = await registerUser({
    email: 'test@example.com',
    password: 'SecurePass123'
  });

  expect(result.success).toBe(false);
  expect(result.error).toContain('database');
});

// Test Category 4: Security Cases
it('should prevent SQL injection attempts', async () => {
  const result = await registerUser({
    email: "'; DROP TABLE users; --",
    password: 'SecurePass123'
  });
  expect(result.success).toBe(false);
});
```

**If tests fail:**
```markdown
Ask Claude: "These tests are failing:

Test: [name]
Expected: [expected result]
Actual: [actual result]
Error: [error message]

Fix the implementation to make tests pass."
```

---

## Layer 4: Security Validation

**Rule:** Every piece of code must be security-reviewed.

### Security Checklist

```markdown
## Input Validation
□ All user inputs validated
□ Data types enforced
□ Length limits enforced
□ Special characters handled

## SQL Injection Prevention
□ Parameterized queries used
□ No string concatenation for SQL
□ ORM used correctly

## XSS Prevention
□ Output escaped
□ HTML entities encoded
□ Content Security Policy set

## Authentication & Authorization
□ Authentication required where needed
□ Authorization checked before actions
□ Sessions validated
□ Tokens verified

## Data Exposure
□ No secrets in code
□ No sensitive data in logs
□ No password in plain text
□ No API keys hardcoded

## Error Handling
□ No stack traces to users
□ Generic error messages
□ Detailed logs server-side only
```

**Common Security Issues:**

### ❌ SQL Injection
```javascript
// DON'T:
const query = `SELECT * FROM users WHERE email = '${email}'`;
const users = await db.query(query);

// DO:
const query = 'SELECT * FROM users WHERE email = ?';
const users = await db.query(query, [email]);
```

### ❌ XSS (Cross-Site Scripting)
```javascript
// DON'T:
element.innerHTML = userInput;

// DO:
element.textContent = userInput;
// Or use proper escaping library
```

### ❌ Exposed Secrets
```javascript
// DON'T:
const apiKey = 'sk-1234567890abcdef';

// DO:
const apiKey = process.env.API_KEY;
```

**If security fails:**
```markdown
Ask Claude: "Security issues found:

Issue: [describe vulnerability]
Location: [file:line]
Risk: [High/Medium/Low]

Fix this security vulnerability."
```

---

## Layer 5: Documentation Validation

**Rule:** If Claude can't explain the code clearly, it might be wrong.

### Documentation Test

```markdown
Ask Claude: "Explain this function:
- What does it do?
- What are the inputs (with types)?
- What are the outputs (with format)?
- What are possible errors?
- What edge cases does it handle?
- Provide a usage example."

If Claude:
✓ Explains clearly and correctly → Code is probably good
✗ Can't explain or explanation is wrong → Code might be faulty
```

**Example: Good Documentation**

```javascript
/**
 * Registers a new user account
 *
 * PROCESS:
 * 1. Validates email format and password strength
 * 2. Checks email uniqueness in database
 * 3. Hashes password with bcrypt (12 rounds)
 * 4. Creates user record in database
 * 5. Sends welcome email
 *
 * @param {Object} userData - User registration data
 * @param {string} userData.email - Valid email address (RFC 5322)
 * @param {string} userData.password - Password (min 8 chars, 1 upper, 1 number)
 * @param {string} userData.name - Full name (optional)
 *
 * @returns {Promise<{success: boolean, userId?: string, error?: string}>}
 * success=true: User created, userId returned
 * success=false: Creation failed, error message returned
 *
 * @throws {ValidationError} Invalid email or weak password
 * @throws {DuplicateError} Email already registered
 * @throws {DatabaseError} Database operation failed
 *
 * @example
 * // Success case
 * const result = await registerUser({
 *   email: 'john@example.com',
 *   password: 'SecurePass123',
 *   name: 'John Doe'
 * });
 * // result = { success: true, userId: '123' }
 *
 * @example
 * // Failure case (duplicate email)
 * const result = await registerUser({
 *   email: 'existing@example.com',
 *   password: 'SecurePass123'
 * });
 * // result = { success: false, error: 'Email already registered' }
 */
async function registerUser(userData) {
  // Implementation...
}
```

---

## The Validation Loop

**Pattern:** Don't accept poor AI output. Loop until quality threshold met.

```
┌─────────────────────────────┐
│ Claude generates code       │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ Run 5-layer validation      │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│ All layers pass?            │
│ YES → ACCEPT                │
│ NO → REJECT + FEEDBACK      │
└──────────┬──────────────────┘
           │
    ┌──────┴──────┐
    │ NO          │ YES
    ▼             ▼
┌─────────┐   ┌──────┐
│ Ask     │   │ DONE │
│ Claude  │   │      │
│ to fix  │   └──────┘
└────┬────┘
     │
     │ (Loop back)
     └─────────────────────┐
                           │
                           ▼
                  (Try again with feedback)

MAX ITERATIONS: 3
If still failing after 3 attempts:
  → Human review required
```

---

## Quality Scoring System

**Score AI-generated code on a 0-100 scale:**

```
Syntax (20 points):
├─ Parses correctly: 10 points
├─ Follows style guide: 5 points
└─ No linting errors: 5 points

Requirements (30 points):
├─ All requirements met: 20 points
├─ Edge cases handled: 5 points
└─ Error cases handled: 5 points

Tests (20 points):
├─ Happy path covered: 8 points
├─ Edge cases tested: 6 points
└─ Error cases tested: 6 points

Security (20 points):
├─ No SQL injection: 5 points
├─ No XSS: 5 points
├─ Input validation: 5 points
└─ No exposed secrets: 5 points

Documentation (10 points):
├─ Function documented: 5 points
└─ Usage examples: 5 points

TOTAL: 100 points

ACCEPTANCE THRESHOLD: >= 80 points
If < 80: Iterate with Claude
```

---

## Recovery Strategies

| Problem | Recovery Action |
|---------|-----------------|
| Syntax error | Show error → Ask Claude to fix → Re-validate |
| Missing requirement | Point out missing feature → Ask Claude to add → Re-validate |
| Test failure | Show failed test → Ask Claude to fix logic → Re-run |
| Security vulnerability | Describe risk → Ask Claude to secure → Re-check |
| Poor documentation | Ask Claude to document → Verify explanation → Re-validate |
| Logic error | Show expected vs actual → Ask Claude to fix → Re-test |
| Performance issue | Show bottleneck → Ask Claude to optimize → Benchmark |
| Unclear code | Ask Claude to simplify → Verify clarity → Re-validate |

---

## Automated Validation Script

```bash
#!/bin/bash
# validate-ai-code.sh - Automated 5-layer validation

echo "=== 5-LAYER VALIDATION ==="

# Layer 1: Syntax
echo "Layer 1: Syntax check"
php -l $1 || exit 1

# Layer 2: Requirements (manual checklist)
echo "Layer 2: Review requirements manually"
echo "All requirements met? (y/n)"
read requirements
if [ "$requirements" != "y" ]; then
  echo "FAIL: Requirements not met"
  exit 1
fi

# Layer 3: Tests
echo "Layer 3: Running tests"
phpunit tests/ || exit 1

# Layer 4: Security
echo "Layer 4: Security scan"
phpstan analyze $1 --level=8 || exit 1

# Layer 5: Documentation (manual check)
echo "Layer 5: Documentation review"
echo "Code properly documented? (y/n)"
read documentation
if [ "$documentation" != "y" ]; then
  echo "FAIL: Documentation incomplete"
  exit 1
fi

echo "✓ ALL LAYERS PASSED"
echo "Code approved for use"
```

---

## Best Practices

### DO:
✅ **Always validate AI output** - Never blindly accept
✅ **Run all 5 layers** - Skip none
✅ **Loop until quality threshold** - Don't accept poor code
✅ **Provide specific feedback** - Help Claude improve
✅ **Log validation results** - Track quality over time
✅ **Automate where possible** - Scripts for consistency

### DON'T:
❌ **Don't skip validation** - Even if Claude seems confident
❌ **Don't accept failing tests** - Fix before using
❌ **Don't ignore security** - Critical for production
❌ **Don't use undocumented code** - You'll regret it later
❌ **Don't blindly trust** - Validate, verify, test

---

## Integration with Other Skills

**Use this skill WITH:**
- `orchestration-best-practices` - Validate orchestrated code
- `ai-assisted-development` - Validate AI agent outputs
- `api-error-handling` - Validate API implementations
- `vibe-security-skill` - Additional security checks

**This skill ensures:**
- No broken code reaches production
- All requirements are implemented
- Security vulnerabilities caught early
- Quality improves with each iteration

---

## Summary

**The 5 Validation Layers:**
1. **Syntax** - Can it parse?
2. **Requirements** - Does it meet specs?
3. **Tests** - Do tests pass?
4. **Security** - Any vulnerabilities?
5. **Documentation** - Can Claude explain it?

**Quality Threshold:** >= 80/100 points

**Validation Loop:** Generate → Validate → Pass? → Accept | Fail? → Fix → Repeat

**Max Iterations:** 3 (then human review)

**Result:** Production-ready, secure, verified code every time.

---

**Related Skills:**
- `orchestration-best-practices/` - Code structure patterns
- `ai-assisted-development/` - AI agent coordination
- `vibe-security-skill/` - Security best practices
- `api-error-handling/` - API-specific validation

**Last Updated:** 2026-02-07
**Line Count:** ~487 lines (compliant)
