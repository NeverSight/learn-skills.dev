---
name: agent-tool-design
description: 'The Agent Tool Contract — 5 principles for designing tools agents call reliably: predictable signature, rich errors, token-efficient output, idempotency, graceful degradation. Includes anti-pattern table with 8 common mistakes.'
version: 1.2.0
category: 'Development'
agents: [developer, architect, tool-creator]
user_invocable: true
invoked_by: both
tools: [Read, Write, Bash]
verified: true
lastVerifiedAt: 2026-03-01T00:00:00.000Z
tags: [tools, design, api, contract, idempotency, errors, agent-tools]
best_practices:
  - Parameters are named not positional
  - Errors include machine-readable code plus human message plus context
  - Output is structured data only — no prose
  - Tools are idempotent (safe to retry)
  - Partial failure returns partial results rather than throws
error_handling: graceful
---

# Agent Tool Design

The Agent Tool Contract — 5 principles for designing tools that agents call reliably.

## The 5 Principles

### Principle 1: Predictable Signature

Tools must have typed, named parameters with clear required/optional distinction. No positional ambiguity.

**Good:**

```javascript
// Clear, named, typed
function searchCode({ query, limit = 20, type = 'semantic' }) { ... }
```

**Bad:**

```javascript
// Positional, ambiguous
function searchCode(q, n, t) { ... }
```

### Principle 2: Rich Errors

Errors must include: error code (machine-readable), message (human-readable), context (debugging data).

**Good:**

```javascript
throw {
  code: 'FILE_NOT_FOUND',
  message: `File not found: ${path}`,
  context: { path, cwd: process.cwd() },
};
```

**Bad:**

```javascript
throw new Error('not found'); // No context for agent to act on
```

### Principle 3: Token-Efficient Output

Tools return structured minimal data. No prose explanations, no redundant wrapping, no verbose status messages. Agents format output themselves.

**Good:**

```javascript
return { files: ['a.js', 'b.js'], total: 2 };
```

**Bad:**

```javascript
return { status: 'success', message: 'Found 2 files successfully', data: { files: [...], metadata: {...} } };
```

**Rule of thumb:** If the output contains prose an agent would re-read to extract facts, it's too verbose.

### Principle 4: Idempotency

Tools must be safe to retry. Running a tool twice should produce the same result as running it once.

**Good:**

```javascript
// Upsert instead of insert
db.upsert({ id, ...data });
// mkdir -p instead of mkdir
fs.mkdirSync(path, { recursive: true });
```

**Bad:**

```javascript
// Fails on retry
db.insert({ id, ...data }); // duplicate key error
fs.mkdirSync(path); // EEXIST error
```

### Principle 5: Graceful Degradation

Partial success > hard failure. Return what succeeded with a clear indication of what didn't.

**Good:**

```javascript
return {
  succeeded: ['file1.js', 'file2.js'],
  failed: [{ file: 'file3.js', reason: 'PERMISSION_DENIED' }],
  partial: true,
};
```

**Bad:**

```javascript
// One file fails -> entire batch throws
throw new Error('Failed to process file3.js');
```

## Anti-Pattern Table

| Anti-Pattern                   | Problem                                        | Fix                                  |
| ------------------------------ | ---------------------------------------------- | ------------------------------------ |
| Verbose status wrapping        | Wastes tokens; agent re-parses to extract data | Return data directly                 |
| Positional args                | Ambiguous; breaks on refactor                  | Named params with types              |
| Swallowed exceptions           | Agent thinks success; work is lost             | Always surface errors explicitly     |
| Non-idempotent mutations       | Retry causes duplicate data or errors          | Upsert semantics; check-then-set     |
| Hard failures on partial input | One bad item breaks entire batch               | Return partial results               |
| Side-effect-heavy reads        | Read tools that trigger writes confuse agents  | Separate reads from writes           |
| String error messages only     | Agent can't programmatically handle errors     | Include machine-readable error codes |
| Untyped return shape           | Agent can't reliably destructure output        | Document and enforce return schema   |

## Review Checklist

Before shipping any tool:

```
[ ] Parameters are named (not positional)
[ ] Required vs optional params are explicit
[ ] All error paths return { code, message, context }
[ ] Output contains no prose — only structured data
[ ] Tool is idempotent (safe to retry)
[ ] Partial failure returns partial results, not throws
[ ] Return shape is documented in JSDoc or TypeScript types
[ ] Token budget for output estimated (< 500 tokens for standard tools)
```

## Iron Laws

1. **ALWAYS use named parameters** — never positional arguments in tool signatures; positional args break on refactor and create ambiguity for agents.
2. **ALWAYS include machine-readable error codes** — never surface plain string errors only; agents need `{ code, message, context }` to handle errors programmatically.
3. **NEVER mix reads and writes in the same tool** — read tools that trigger side effects confuse agents and prevent safe retries.
4. **ALWAYS design for idempotency** — retry must produce the same result as the first call; use upsert semantics and `mkdir -p` patterns.
5. **ALWAYS return partial results on partial failure** — never let one failing item abort the entire batch; return `{ succeeded, failed, partial: true }`.

## Integration

- Used by: `tool-creator` skill when designing new tools
- Reviewed by: `code-reviewer` agent during tool PRs
- Pairs with: `dynamic-api-integration` skill (consuming external tools)
- Complements: `agent-evaluation` skill (evaluating tool output quality)

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
