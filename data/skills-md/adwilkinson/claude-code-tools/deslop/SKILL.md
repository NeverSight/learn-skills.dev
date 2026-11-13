---
name: deslop
author: Andrew Wilkinson (github.com/ADWilkinson)
description: Remove AI-generated slop from diffs. Includes confidence scoring and false positive lists.
disable-model-invocation: true
---

# Remove AI Code Slop

> **Quick Reference**: Check diff against main, identify AI-generated patterns with confidence ≥75, remove surgically, run linter.

Check the diff against main (or specified base branch) and remove AI-generated slop.

## Confidence Scoring

Rate each potential slop item before removing:

| Score | Meaning | Action |
|-------|---------|--------|
| 0-25 | Might be intentional | Leave it |
| 50 | Probably slop, context-dependent | Investigate |
| 75-100 | Definitely slop | Remove it |

**Only remove items with confidence ≥75.** When in doubt, leave it.

## What to Remove (with Examples)

### 1. Extra Comments
Comments that a human wouldn't add or that are inconsistent with the file's existing style.

**Words to watch:** "This function", "This method", "Helper function", "Utility to", "Used to"

```typescript
// Before (slop)
// This function validates the user input and returns a boolean
function validateInput(input: string): boolean {
  return input.length > 0;
}

// After (clean)
function validateInput(input: string): boolean {
  return input.length > 0;
}
```

### 2. Defensive Checks for Impossible Cases
Null checks on required params, type guards where TypeScript already guarantees the type.

**Words to watch:** `if (!param)` on required params, `typeof x === 'undefined'` after initialization

```typescript
// Before (slop) - userId is required in the type
function getUser(userId: string): User {
  if (!userId) {
    throw new Error('userId is required');
  }
  return db.users.findById(userId);
}

// After (clean)
function getUser(userId: string): User {
  return db.users.findById(userId);
}
```

### 3. Silent Try/Catch Blocks
Error swallowing without justification or logging.

**Words to watch:** `catch (e) {}`, `catch { }`, `catch (error) { /* ignore */ }`

```typescript
// Before (slop)
try {
  await saveData(data);
} catch (error) {
  // Handle error
}

// After (clean)
await saveData(data);
// OR if error handling is needed:
try {
  await saveData(data);
} catch (error) {
  logger.error('Failed to save data', { error, data });
  throw error;
}
```

### 4. Type Escapes
Bypassing TypeScript's type system without explanation.

**Words to watch:** `as any`, `as unknown as`, `// @ts-ignore`, `// @ts-expect-error`, `# type: ignore`

```typescript
// Before (slop)
const data = response.data as any;
const user = data as User;

// After (clean)
const data: ApiResponse<User> = response.data;
const user = data.payload;
```

### 5. Console.logs and Debug Statements
Debug output that wasn't intentionally left for development.

**Words to watch:** `console.log`, `console.debug`, `print(`, `debugger;`

```typescript
// Before (slop)
function processOrder(order: Order) {
  console.log('Processing order:', order);
  const result = calculate(order);
  console.log('Result:', result);
  return result;
}

// After (clean)
function processOrder(order: Order) {
  return calculate(order);
}
```

### 6. Style Inconsistencies
Code that doesn't match the rest of the file's conventions.

**Words to watch:** Mixed quote styles, inconsistent semicolons, different brace placement

```typescript
// If file uses single quotes everywhere:
// Before (slop)
const name = "John";

// After (clean)
const name = 'John';
```

### 7. Over-Documentation
Excessive JSDoc or comments explaining obvious code.

**Words to watch:** JSDoc on simple getters/setters, `@param` restating the parameter name, `@returns` stating "returns the result"

```typescript
// Before (slop)
/**
 * Gets the user's name
 * @param user - The user object
 * @returns The name of the user
 */
function getName(user: User): string {
  return user.name;
}

// After (clean)
function getName(user: User): string {
  return user.name;
}
```

### 8. Backwards-Compat Shims
Compatibility code for things that weren't there before (renamed unused variables, re-exports of removed items).

**Words to watch:** `_unused`, `// deprecated`, `// removed`, `// legacy`, re-exports that reference deleted code

```typescript
// Before (slop)
export const oldFunctionName = newFunctionName; // backwards compat
const _unusedParam = param; // preserve for future use

// After (clean)
// Just delete these entirely
```

## False Positives (Do NOT Remove)

- Comments that match the existing file's documentation style
- Defensive checks the codebase consistently uses (check other files)
- Type assertions with explanatory comments justifying them
- Console.logs in designated debug/logging utilities
- Console.logs in test files
- Try/catch with proper error handling or logging
- JSDoc required by linter rules or API documentation generators
- Backwards-compat code that was explicitly requested

## Process

1. Get diff: `git diff main...HEAD` (or specified branch)
2. For each changed file:
   - Read the full file to understand its style
   - Score each potential slop item (0-100)
   - Only remove items with confidence ≥75
3. Remove slop surgically - don't refactor unrelated code
4. Run linter/formatter after changes

## Output

Report a 1-3 sentence summary of what was changed. Include count of items removed by category.

```
Removed 3 unnecessary comments, 2 console.logs, and 1 empty try/catch.
```
