---
name: generate-test-cases
description: "Use when the user asks to analyze code for test coverage, list what test cases are needed, or review testing strategy — WITHOUT generating actual test code."
allowed-tools: Read, Glob, Grep
argument-hint: "<file-path-or-class>"
---

# Generate Test Cases Skill

You will analyze code and generate a list of test cases that should be written for a given method/class. This skill outputs test case descriptions only — it does NOT generate actual test code.

**Target to analyze:** $ARGUMENTS

## Quality Standards

- Take your time to analyze the code thoroughly before listing test cases.
- Quality is more important than speed — read all relevant source files and rules carefully.
- Do not skip reading the dependency classes. Understanding the full context produces better test cases.

---

## Instructions

### Step 1: Read Rules and Analyze Context

1. **Read the rules** from `./rules/general/` directory (see Rules Reference below)
2. **Read the target** source file/class/method specified above
3. **Read dependencies**: Follow imports to read DTOs, entities, enums, and other types referenced by the target (as specified in `code-context-analysis` rule)
4. **Check for existing tests**: Search for existing test classes covering this target (as specified in `existing-test-awareness` rule) — if found, read it fully and focus only on behaviors not yet covered

### Step 2: Generate Test Cases

1. Analyze ALL code branches, including:
   - Success paths
   - Error/exception paths
   - Validation logic
   - Private/protected methods called by the target
   - Security annotations (if present)
2. Apply the INCLUDE/EXCLUDE rules strictly
3. Output the list of test cases in the specified format
4. Stop at the descriptions — the list itself is this skill's deliverable
5. Close by naming the next step: `generate-tests <target>` takes this list as its plan
   and writes the code from it. Hand the list forward as it stands — the user can review
   or amend it first

---

## Output Format

For each test case, provide:

```
## Test Cases for {ClassName}.{methodName}

### 1. {testMethodName}
- **Given:** {preconditions/input state}
- **When:** {action being tested}
- **Then:** {expected outcome}
- **Code branch:** {which code path this covers}

### 2. {testMethodName}
...
```

### Naming Convention
Test method name format: `{testedMethod}_{givenState}_{expectedOutcome}`

Examples:
- `calculateTotal_validProducts_returnsSum`
- `calculateTotal_emptyList_throwsIllegalArgumentException`
- `getUser_unauthorized_returns401`
- `getUser_forbidden_returns403`

---

## Troubleshooting

### Target file not found
If the specified target does not exist, inform the user with the exact path you searched and ask for clarification.

### Unsupported language
If the target code is in a language without specific rules, apply only the general rules and inform the user.

### All behaviors already covered
If the existing test class already covers all identified behaviors, output a summary stating that coverage is complete. List what is already tested. Do not invent additional test cases to justify the analysis.

---

## Example

```
User says: "/generate-test-cases src/main/java/com/example/service/OrderService.java"

Step 1: Agent reads rules, reads OrderService.java, reads OrderRequest.java,
        Order.java (dependencies), checks for existing OrderServiceTest.java.

Step 2: Agent outputs:

## Test Cases for OrderService.createOrder

### 1. createOrder_validRequest_savesAndReturnsOrder
- **Given:** Valid OrderRequest with productId "product-1" and quantity 5
- **When:** createOrder is called
- **Then:** Order is saved to repository and returned with generated ID
- **Code branch:** Success path

### 2. createOrder_nullProductId_throwsIllegalArgumentException
- **Given:** OrderRequest with null productId
- **When:** createOrder is called
- **Then:** IllegalArgumentException is thrown
- **Code branch:** Validation — productId null check
...
```

---

## Rules Reference

**CRITICAL: You MUST read and apply all rules from the following files before generating test cases:**

> **Maintenance note:** General rules in `./rules/general/` are shared with the `generate-tests` skill (which has copies in `rules/tests/general/`). When updating rules, keep both locations in sync.

### General Rules (Always Apply)
- `./rules/general/test-case-generation-strategy.md` - INCLUDE/EXCLUDE criteria for test cases
- `./rules/general/naming-conventions.md` - Test naming format
- `./rules/general/general-principles.md` - Core testing principles
- `./rules/general/what-makes-good-test.md` - Clarity, Completeness, Conciseness, Resilience
- `./rules/general/keep-tests-focused.md` - One scenario per test
- `./rules/general/test-behaviors-not-methods.md` - Separate tests for behaviors
- `./rules/general/prefer-public-apis.md` - Test public APIs over private methods
- `./rules/general/cleanly-create-test-data.md` - Use helpers and builders for test data
- `./rules/general/keep-cause-effect-clear.md` - Effects follow causes immediately
- `./rules/general/no-logic-in-tests.md` - KISS > DRY, avoid logic in assertions
- `./rules/general/technology-stack-detection.md` - Detect language and framework
- `./rules/general/verify-relevant-arguments-only.md` - Only verify relevant mock arguments
- `./rules/general/existing-test-awareness.md` - Check for existing tests, avoid duplicates
- `./rules/general/code-context-analysis.md` - Read dependencies before analyzing
