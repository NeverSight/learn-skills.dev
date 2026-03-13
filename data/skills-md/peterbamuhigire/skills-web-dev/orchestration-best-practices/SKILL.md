---
name: orchestration-best-practices
description: Master skill for orchestrating multi-step workflows. Use when generating code for complex processes, agent coordination, or system design. Ensures proper step definition, dependency tracking, error handling, and validation.
---

## Required Plugins

**Superpowers plugin:** MUST be active for all work using this skill. Use throughout the entire build pipeline — design decisions, code generation, debugging, quality checks, and any task where it offers enhanced capabilities. If superpowers provides a better way to accomplish something, prefer it over the default approach.

# Orchestration Best Practices

## When to Use This Skill

Use when generating code for:
- Multi-step workflows
- Agent coordination
- Complex processes
- System design
- Feature implementation

**This skill automatically enforces orchestration patterns.**

---

## The 10 Commandments of Orchestration

Every multi-step operation MUST follow these rules:

### 1. ALWAYS Define Steps Explicitly

**Rule:** Break work into clear, numbered steps with comments.

```javascript
// DON'T: Everything in one block
function doEverything() {
  const data = fetchData();
  const processed = processData(data);
  const validated = validateData(processed);
  return saveData(validated);
}

// DO: Clear step-by-step structure
async function orchestratedWorkflow() {
  console.log("=== ORCHESTRATION START ===");

  // STEP 1: Data Acquisition
  console.log("STEP 1: Fetching data");
  const data = await fetchData();

  // STEP 2: Data Processing
  console.log("STEP 2: Processing data");
  const processed = await processData(data);

  // STEP 3: Data Validation
  console.log("STEP 3: Validating results");
  const validated = await validateData(processed);

  // STEP 4: Data Persistence
  console.log("STEP 4: Saving results");
  const result = await saveData(validated);

  console.log("=== ORCHESTRATION COMPLETE ===");
  return result;
}
```

---

### 2. ALWAYS Identify Dependencies

**Rule:** Show which steps depend on which outputs.

```javascript
// STEP 1: Get user data (no dependencies)
const user = await getUserData();

// STEP 2: Get user permissions (depends on STEP 1)
const permissions = await getPermissions(user.id);

// STEP 3: Load dashboard (depends on STEP 1 and STEP 2)
const dashboard = await loadDashboard(user, permissions);

// Dependency diagram in comments:
/*
STEP 1 (user data)
  ↓
STEP 2 (permissions) ← depends on STEP 1
  ↓
STEP 3 (dashboard) ← depends on STEP 1 + STEP 2
*/
```

---

### 3. ALWAYS Validate Inputs

**Rule:** Never trust input. Always validate at entry point.

```javascript
async function processOrder(order) {
  // STEP 0: Input Validation (ALWAYS FIRST)
  try {
    validateOrderInput(order);
  } catch (error) {
    return {
      success: false,
      error: `Invalid input: ${error.message}`,
      step: "INPUT_VALIDATION"
    };
  }

  // Continue with orchestration...
}

function validateOrderInput(order) {
  if (!order) throw new Error("Order is required");
  if (!order.items || order.items.length === 0) {
    throw new Error("Order must have items");
  }
  if (!order.customerId) {
    throw new Error("Customer ID is required");
  }
  // Validate each item
  order.items.forEach((item, index) => {
    if (!item.productId) {
      throw new Error(`Item ${index}: productId required`);
    }
    if (item.quantity <= 0) {
      throw new Error(`Item ${index}: quantity must be > 0`);
    }
  });
}
```

---

### 4. ALWAYS Handle Errors

**Rule:** Every step must have error handling with recovery strategy.

```javascript
async function orchestratedWorkflow() {
  // STEP 1: Fetch data
  let data;
  try {
    data = await fetchData();
  } catch (error) {
    console.error("STEP 1 FAILED:", error);
    return {
      success: false,
      step: "STEP_1_FETCH_DATA",
      error: error.message,
      recovery: "Check API endpoint and credentials"
    };
  }

  // STEP 2: Process data
  let processed;
  try {
    processed = await processData(data);
  } catch (error) {
    console.error("STEP 2 FAILED:", error);
    return {
      success: false,
      step: "STEP_2_PROCESS_DATA",
      error: error.message,
      recovery: "Validate data format and processing logic"
    };
  }

  // Continue with remaining steps...
}
```

---

### 5. ALWAYS Validate Outputs

**Rule:** After each step, validate output before continuing.

```javascript
// STEP 1: Fetch user
const user = await fetchUser(userId);
if (!user || !user.id) {
  throw new Error("STEP 1: Invalid user data returned");
}

// STEP 2: Get permissions
const permissions = await getPermissions(user.id);
if (!Array.isArray(permissions)) {
  throw new Error("STEP 2: Permissions must be array");
}

// STEP 3: Check authorization
const hasAccess = permissions.includes('admin');
if (typeof hasAccess !== 'boolean') {
  throw new Error("STEP 3: Authorization check failed");
}
```

---

### 6. ALWAYS Log Progress

**Rule:** Log start and completion of each step for debugging.

```javascript
console.log("=== ORCHESTRATION START ===");
console.log(`Request ID: ${requestId}`);

// STEP 1
console.log("STEP 1: Starting data fetch");
const data = await fetchData();
console.log(`STEP 1: Complete - fetched ${data.length} records`);

// STEP 2
console.log("STEP 2: Starting data processing");
const processed = await processData(data);
console.log(`STEP 2: Complete - processed ${processed.length} records`);

console.log("=== ORCHESTRATION COMPLETE ===");
console.log(`Total time: ${Date.now() - startTime}ms`);
```

---

### 7. ALWAYS Document

**Rule:** Every function must have JSDoc with inputs, outputs, errors.

```javascript
/**
 * Orchestrates user registration workflow
 *
 * STEPS:
 * 1. Validate input
 * 2. Check email uniqueness
 * 3. Hash password
 * 4. Create user record
 * 5. Send welcome email
 *
 * @param {Object} userData - User registration data
 * @param {string} userData.email - User email (required)
 * @param {string} userData.password - Plain password (required)
 * @param {string} userData.name - User name (required)
 *
 * @returns {Promise<{success: boolean, userId?: string, error?: string}>}
 *
 * @throws {ValidationError} If input validation fails
 * @throws {DuplicateError} If email already exists
 * @throws {DatabaseError} If user creation fails
 *
 * @example
 * const result = await registerUser({
 *   email: 'user@example.com',
 *   password: 'SecurePass123',
 *   name: 'John Doe'
 * });
 */
async function registerUser(userData) {
  // Implementation...
}
```

---

### 8. ALWAYS Test Thoroughly

**Rule:** Test happy path, edge cases, and error cases.

```javascript
describe('User Registration Orchestration', () => {
  // Test 1: Happy path
  it('should register user successfully', async () => {
    const result = await registerUser({
      email: 'new@example.com',
      password: 'SecurePass123',
      name: 'John Doe'
    });
    expect(result.success).toBe(true);
    expect(result.userId).toBeDefined();
  });

  // Test 2: Edge case - duplicate email
  it('should reject duplicate email', async () => {
    await registerUser({ email: 'existing@example.com', ... });
    const result = await registerUser({ email: 'existing@example.com', ... });
    expect(result.success).toBe(false);
    expect(result.error).toContain('already exists');
  });

  // Test 3: Error case - invalid input
  it('should reject invalid password', async () => {
    const result = await registerUser({
      email: 'test@example.com',
      password: '123',  // Too short
      name: 'John'
    });
    expect(result.success).toBe(false);
    expect(result.error).toContain('password');
  });

  // Test 4: Error case - database failure
  it('should handle database errors gracefully', async () => {
    // Mock database failure
    jest.spyOn(db, 'createUser').mockRejectedValue(new Error('DB down'));
    const result = await registerUser({...});
    expect(result.success).toBe(false);
    expect(result.error).toContain('database');
  });
});
```

---

### 9. ALWAYS Have Fallback

**Rule:** Critical operations must have fallback for failures.

```javascript
async function sendNotification(userId, message) {
  try {
    // Primary: Send via email
    await sendEmail(userId, message);
    console.log("Notification sent via email");
  } catch (error) {
    console.error("Email failed:", error);

    try {
      // Fallback 1: Send via SMS
      await sendSMS(userId, message);
      console.log("Notification sent via SMS (fallback)");
    } catch (smsError) {
      console.error("SMS failed:", smsError);

      // Fallback 2: Queue for later
      await queueNotification(userId, message);
      console.log("Notification queued (final fallback)");
    }
  }
}
```

---

### 10. ALWAYS Consider Parallelization

**Rule:** If steps are independent, run in parallel for speed.

```javascript
// DON'T: Sequential when independent
const user = await fetchUser(userId);
const products = await fetchProducts();
const categories = await fetchCategories();
// Total time: 300ms (100ms each)

// DO: Parallel when independent
const [user, products, categories] = await Promise.all([
  fetchUser(userId),      // 100ms
  fetchProducts(),        // 100ms
  fetchCategories()       // 100ms
]);
// Total time: 100ms (67% faster!)

// Show parallelization in comments:
/*
PARALLELIZATION:
├─ fetchUser ──┐
├─ fetchProducts ──┼─→ All run together (100ms)
└─ fetchCategories ──┘

Sequential would take: 300ms
Parallel takes: 100ms
Speedup: 67% faster
*/
```

---

## Decision Tree: When to Use What

```
Is this a multi-step operation?
├─ NO → Use simple function
└─ YES → Continue

Do steps depend on each other?
├─ YES → Sequential orchestration
└─ NO → Parallel orchestration

Can it fail?
├─ YES → Add error handling + fallback
└─ NO → Add error handling anyway (Murphy's Law)

Is it critical?
├─ YES → Add retry logic + multiple fallbacks
└─ NO → Add single fallback

Does quality matter?
├─ YES → Add output validation loops
└─ NO → Add output validation anyway (quality always matters)
```

---

## Checklist: Before Finishing

Every time you generate orchestration code, verify:

```
□ Steps clearly defined (numbered comments)
□ Dependencies identified (diagram in comments)
□ Inputs validated (at entry point)
□ Error handling added (try-catch per step)
□ Outputs validated (after each step)
□ Progress logged (start + complete per step)
□ Documentation added (JSDoc with examples)
□ Tests included (happy + edge + error cases)
□ Fallback included (for critical operations)
□ Parallelization considered (Promise.all if independent)
```

**If all checked → Good to go!**
**If any missing → Add before finishing!**

---

## Anti-Patterns (What NOT to Do)

| Anti-Pattern | Why It Fails | Do This Instead |
|-------------|-------------|-----------------|
| Everything in one function | No clear steps, no error handling, impossible to debug | Break into numbered steps |
| Silent failures (`catch {}`) | Errors disappear, bugs become invisible | Always log and return error details |
| No input validation | Crashes on unexpected data, security vulnerabilities | Validate at every entry point |
| Generic error messages ("Something went wrong") | Useless for debugging and user support | Include step name, specific error, recovery hint |
| No logging | Can't trace what happened when things fail | Log start + completion of every step |

- `feature-planning` - Implementation plans should follow these patterns
- `ai-assisted-development` - AI agents should generate orchestrated code
- `api-error-handling` - API endpoints need orchestration
- `prompting-patterns-reference` - Better prompts = better orchestrated code

**This skill ensures:**
- Consistent code structure across all AI-generated code
- Better debugging (clear logs, error messages)
- Higher reliability (error handling, fallbacks)
- Faster execution (parallelization where possible)

---

## Summary

**The 10 Commandments:**
1. Define steps explicitly
2. Identify dependencies
3. Validate inputs
4. Handle errors
5. Validate outputs
6. Log progress
7. Document thoroughly
8. Test comprehensively
9. Have fallbacks
10. Consider parallelization

**When Claude generates code:**
- Claude MUST follow all 10 rules
- Claude MUST include checklist verification
- Claude MUST explain orchestration strategy
- Claude MUST show dependency diagram

**Result:** Production-ready, debuggable, reliable code every time.

---

**Related Skills:**
- `ai-assisted-development/` - AI agent orchestration patterns
- `api-error-handling/` - API-specific error handling
- `feature-planning/` - Implementation planning with orchestration
- `prompting-patterns-reference.md` - Better AI instructions

**Last Updated:** 2026-02-07
**Line Count:** ~476 lines (compliant)
