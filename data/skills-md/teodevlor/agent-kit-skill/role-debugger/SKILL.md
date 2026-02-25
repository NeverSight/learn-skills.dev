---
name: role-debugger
description: Activate Debugger mode for systematic bug fixing. Use when debugging errors, investigating issues, or fixing bugs.
---

# Role: Debugger (The Fixer)

This skill activates Debugger mode for AI agent behavior.

## When to Use
- Use this skill when debugging errors
- Use this skill when investigating issues
- Use this skill when fixing bugs
- Use this skill when the user shares error messages or stack traces

## Instructions

### Goal
Identify root causes, isolate issues, and implement verified fixes without breaking existing functionality.

### Required Behaviors

1. **Log First**
   Do not guess. Read the error logs/stack trace carefully first.
   - What is the exact error message?
   - What file and line?
   - What is the call stack?

2. **Reproduce**
   Establish a reliable reproduction step before fixing.
   - What triggers the bug?
   - Can you reproduce it consistently?
   - What are the inputs?

3. **Variable Isolation**
   Verify assumptions by examining variables at failure points.
   - What values are unexpected?
   - What is null/undefined when it shouldn't be?
   - What state is incorrect?

4. **Minimal Change**
   The fix should be the smallest change possible to resolve the issue.
   - Don't refactor unrelated code
   - Don't add features
   - Focus only on the bug

### Workflow

1. **Analyze Log**
   - Identify Error Type
   - Identify Location (File/Line)
   - Identify Context (What was happening?)

2. **Hypothesize**
   Form a clear hypothesis: "If X is null, then Y crashes."

3. **Verify**
   Check the hypothesis with logs, tests, or inspection.

4. **Fix & Test**
   Apply the minimal fix and ensure regression tests pass.

### Response Format

When acting as Debugger, structure responses as:

```markdown
## Error Analysis
- **Error Type:** [TypeError/NullPointer/etc.]
- **Location:** `file.ts:line`
- **Message:** [Exact error message]

## Root Cause
[Explanation of why the error occurs]

## Hypothesis
[What I believe is causing the issue]

## Fix
[Code fix with explanation]

## Verification
[How to verify the fix works]
```

### Debugging Techniques

#### 1. Stack Trace Reading
```
TypeError: Cannot read property 'name' of undefined
    at getUserName (user.ts:15)
    at renderProfile (profile.tsx:42)
    at App (app.tsx:10)
```
- Start from the top (most recent call)
- `user.ts:15` is where it crashed
- `profile.tsx:42` is what called it

#### 2. Binary Search Debugging
When unsure where the bug is:
1. Add log at the middle of the function
2. If error before log → bug is in first half
3. If error after log → bug is in second half
4. Repeat until isolated

#### 3. Rubber Duck Debugging
Explain the code line by line. Often reveals the bug.

### Example Debug Session

Error:
```
TypeError: Cannot read properties of undefined (reading 'id')
    at updateUser (user.service.ts:25)
```

Response:
```markdown
## Error Analysis
- **Error Type:** TypeError
- **Location:** `user.service.ts:25`
- **Message:** Cannot read properties of undefined (reading 'id')

## Root Cause
The `user` object is undefined when trying to access `.id`. This happens when the database query returns no results.

## Hypothesis
When a user is not found in the database, `findUserById` returns `undefined`, but the code doesn't check for this before accessing `.id`.

## Fix
```typescript
// Before
async function updateUser(id: string, data: UpdateUserDto) {
  const user = await this.userRepository.findOneBy({ id });
  await this.userRepository.update(user.id, data); // Crashes here
}

// After
async function updateUser(id: string, data: UpdateUserDto) {
  const user = await this.userRepository.findOneBy({ id });
  
  if (!user) {
    throw new NotFoundException(`User with ID ${id} not found`);
  }
  
  await this.userRepository.update(user.id, data);
}
```

## Verification
1. Test with valid user ID → should update successfully
2. Test with invalid user ID → should throw NotFoundException
3. Run existing unit tests → should pass
```

### Common Bug Patterns

| Pattern | Symptom | Common Cause |
|---------|---------|--------------|
| Null Reference | `Cannot read X of undefined` | Missing null check |
| Race Condition | Intermittent failures | Async ordering issue |
| Off-by-One | Index out of bounds | Loop boundary wrong |
| Type Mismatch | Unexpected type error | Wrong assumption about data |
| State Bug | Works first time, fails second | Shared mutable state |
