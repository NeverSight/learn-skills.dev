---
name: sharp-edges
description: 'Living catalogue of 7 known hazard entries (SE-01 through SE-07) specific to agent-studio: Windows backslash paths, prototype pollution, hook exit codes, async swallowing, ReDoS in glob-to-regex, DST arithmetic, array mutation during iteration. Each entry: symptom, root cause, fix, test assertion.'
version: 1.0.0
verified: true
lastVerifiedAt: '2026-02-28'
category: 'Debugging'
agents: [developer, code-reviewer, qa, security-architect]
user_invocable: true
invoked_by: both
tools: [Read, Write, Bash]
tags: [debugging, hazards, sharp-edges, windows, prototype-pollution, regex, async, bugs]
best_practices:
  - Invoke at the START of any debugging session
  - Match your symptom against SE-01 through SE-07 before exploring new theories
  - If your bug is new and reproducible, add it to this catalogue
error_handling: graceful
---

# Sharp Edges

Living catalogue of confirmed hazard patterns in agent-studio. Each entry documents a real bug we've shipped. Invoke this skill during debugging and code review to check against known failure modes.

## SE-01: Windows Backslash Paths

**Symptom:** Glob patterns match correctly in CI (Linux) but silently fail on developer machines (Windows).

**Root cause:** `path.relative()` returns backslash-separated paths on Windows (`node_modules\foo`), but glob patterns use forward slashes. `[^/]*` in regex won't block `\`.

**Fix:**

```javascript
// ALWAYS normalize before regex matching
const rel = path.relative(root, filePath).replace(/\\/g, '/');
```

**Test assertion:**

```javascript
assert(normalizePath('a\\b\\c') === 'a/b/c');
assert(!normalizePath('a\\b').includes('\\'));
```

**Files affected:** `.claude/lib/utils/path-constants.cjs`, any glob-based exclusion logic.

---

## SE-02: Prototype Pollution via JSON.parse

**Symptom:** `Object.prototype` gains unexpected properties after parsing malformed JSON from hook input or agent memory.

**Root cause:** `JSON.parse('{"__proto__":{"isAdmin":true}}')` silently mutates `Object.prototype` in older Node.js versions or when objects are created via `Object.create(null)` checks are missed.

**Fix:**

```javascript
// Use safeParseJSON — strips __proto__, constructor, prototype keys
const { safeParseJSON } = require('.claude/lib/utils/safe-json.cjs');
const { success, data } = safeParseJSON(rawInput, {});
```

**Test assertion:**

```javascript
const before = Object.getPrototypeOf({});
safeParseJSON('{"__proto__":{"evil":true}}', {});
assert(!{}.evil);
```

**Files affected:** Any hook that calls `JSON.parse()` on stdin input.

---

## SE-03: Hook Exit Code Protocol

**Symptom:** Hook appears to "block" when it should allow, or silently "allows" when it should block.

**Root cause:** Hooks use exit codes `0` (allow) and `2` (block). Using `process.exit(1)` or `process.exit(true)` does not block — it produces unexpected behavior.

**Fix:**

```javascript
// CORRECT
if (shouldBlock) process.exit(2); // Block tool execution
process.exit(0); // Allow tool execution

// WRONG
if (shouldBlock) process.exit(1); // Not a valid block code
process.exit(false); // Not valid
```

**Test assertion:**

```javascript
// Mock hook execution and verify exit code
const result = execHook(input);
assert(result.exitCode === 0 || result.exitCode === 2);
```

**Files affected:** All hooks in `.claude/hooks/`.

---

## SE-04: Async Exception Swallowing in Promise.all

**Symptom:** One failing async operation silently causes all results to be lost; agent believes all tasks succeeded.

**Root cause:** `Promise.all([...])` rejects on the first failure and discards all other results. When wrapped in try/catch that returns `[]`, the caller sees empty results with no error.

**Fix:**

```javascript
// Use Promise.allSettled to get partial results
const results = await Promise.allSettled(tasks);
const succeeded = results.filter(r => r.status === 'fulfilled').map(r => r.value);
const failed = results.filter(r => r.status === 'rejected').map(r => r.reason);
return { succeeded, failed, partial: failed.length > 0 };
```

**Test assertion:**

```javascript
const tasks = [resolvesWith('ok'), rejectsWith('error'), resolvesWith('ok2')];
const result = await safeAllSettled(tasks);
assert(result.succeeded.length === 2);
assert(result.failed.length === 1);
```

---

## SE-05: ReDoS in Glob-to-Regex

**Symptom:** Glob pattern matching hangs or takes exponential time on long path strings.

**Root cause:** Naive glob-to-regex conversion produces patterns with nested quantifiers like `(.*)*` or `(.+)+` which backtrack exponentially on non-matching strings.

**Fix:**

```javascript
// Use anchored, non-backtracking patterns
// BAD: (.*)* -> exponential backtracking
// GOOD: [^/]* -> linear, no backtracking
function globToRegex(glob) {
  const escaped = glob.replace(/[.+^${}()|[\]\\]/g, '\\$&');
  return escaped
    .replace(/\*\*/g, '___DOUBLE___')
    .replace(/\*/g, '[^/]*') // Single * -> no path separators
    .replace(/___DOUBLE___/g, '.*'); // ** -> any path
}
```

**Test assertion:**

```javascript
const regex = globToRegex('**/*.js');
const longString = 'a'.repeat(10000) + '.ts';
const start = Date.now();
regex.test(longString);
assert(Date.now() - start < 100); // Must complete in <100ms
```

---

## SE-06: DST Arithmetic Bugs

**Symptom:** Date calculations are off by 1 hour for events that cross daylight saving time boundaries.

**Root cause:** Adding 24 _60_ 60 \* 1000ms to a timestamp does not always equal "tomorrow" — DST transitions can make a day 23 or 25 hours long.

**Fix:**

```javascript
// WRONG: assumes 24h = 1 day
const tomorrow = new Date(date.getTime() + 86400000);

// CORRECT: use date arithmetic, not ms arithmetic
const tomorrow = new Date(date);
tomorrow.setDate(tomorrow.getDate() + 1);
```

**Test assertion:**

```javascript
// Test across a known DST boundary (e.g., March DST change)
const dst = new Date('2026-03-08T01:00:00'); // Day before US spring forward
const nextDay = addDays(dst, 1);
assert(nextDay.getDate() === 9);
assert(nextDay.getHours() === 1); // Same time, next day
```

---

## SE-07: Array Mutation During forEach Iteration

**Symptom:** Items are skipped or processed twice; behavior is non-deterministic.

**Root cause:** Mutating an array (push, splice, shift) while iterating with `forEach` or `for...of` causes the iterator to skip or re-visit elements.

**Fix:**

```javascript
// WRONG: mutates during iteration
arr.forEach(item => {
  if (condition) arr.push(newItem); // Skips items
});

// CORRECT: collect mutations, apply after
const toAdd = [];
arr.forEach(item => {
  if (condition) toAdd.push(newItem);
});
arr.push(...toAdd);

// OR: work on a copy
[...arr].forEach(item => { ... });
```

**Test assertion:**

```javascript
const arr = [1, 2, 3];
const result = safeForEach(arr, item => item * 2);
assert(result.length === 3); // Original not mutated, all items processed
```

---

## Usage

Invoke at the START of any debugging session:

```javascript
Skill({ skill: 'sharp-edges' });
```

Then match your symptom against SE-01 through SE-07. If your bug is new and reproducible, add it to this catalogue.

## Adding New Entries

Pattern for new entries:

```
## SE-0N: [Short Title]
**Symptom:** [What you observe]
**Root cause:** [Why it happens]
**Fix:** [Code fix with before/after]
**Test assertion:** [Minimal test that would catch it]
**Files affected:** [Where in agent-studio this applies]
```

## Memory Protocol

After invoking: if you find a new sharp edge, append it here via technical-writer agent.

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
