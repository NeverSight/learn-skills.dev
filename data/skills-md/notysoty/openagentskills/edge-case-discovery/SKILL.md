---
name: Edge Case Discovery
description: Systematically identifies edge cases and boundary conditions for any function, API, or user flow.
category: coding
tags:
  - testing
  - edge-cases
  - qa
  - boundary-testing
author: simplyutils
---

# Edge Case Discovery

## What this skill does

This skill directs the agent to systematically work through a function, API endpoint, or user flow and enumerate all edge cases and boundary conditions that could cause incorrect behavior, errors, or security issues. It applies a structured checklist across multiple dimensions (data types, boundary values, state, concurrency, authorization) and outputs a prioritized list of cases to test or guard against.

Use this before writing tests, during code review, when designing a new feature, or when a production bug makes you wonder "what else could go wrong here."

## How to use

### Claude Code / Cline

Copy this file to `.agents/skills/edge-case-discovery/SKILL.md` in your project root.

Then ask:
- *"Use the Edge Case Discovery skill on the `transferFunds` function."*
- *"Find edge cases for the `POST /api/orders` endpoint using the Edge Case Discovery skill."*
- *"What edge cases should I handle in the user registration flow? Use the Edge Case Discovery skill."*

Provide the function signature, the code, or a description of the flow.

### Cursor

Add the instructions below to your `.cursorrules` or paste them into the Cursor AI pane before sharing the function or flow you want analyzed.

### Codex

Paste the function or flow description and ask Codex to follow the instructions below to generate the edge case list.

## The Prompt / Instructions for the Agent

When asked to discover edge cases, apply the following checklist systematically. Not every dimension applies to every input — skip the ones that clearly don't apply and note why.

### Dimension 1 — Numeric inputs

For every numeric input or value in the function/flow:
- Zero (0)
- Negative numbers
- Maximum safe integer / maximum allowed value
- Minimum allowed value
- Values just above and just below each boundary (boundary value analysis)
- Non-integer values when integers are expected
- Infinity / NaN (for floating-point)
- Very large numbers that could cause overflow or performance issues

### Dimension 2 — String inputs

For every string input:
- Empty string (`""`)
- Whitespace-only string (`" "`, `"\t"`, `"\n"`)
- Maximum length string (at or beyond any length limit)
- Single character
- Unicode characters (emoji, RTL text, accented characters)
- SQL injection payloads: `' OR 1=1 --`
- XSS payloads: `<script>alert(1)</script>`
- Null bytes and control characters
- Strings that look like other types: `"null"`, `"undefined"`, `"true"`, `"123"`

### Dimension 3 — Collections (arrays, lists, maps)

For every collection input:
- Empty collection (`[]`, `{}`)
- Single item
- Very large collection (performance/timeout risk)
- Duplicate items (if uniqueness is expected)
- Items in unexpected order
- Null or undefined items within the collection
- Collection with all identical values

### Dimension 4 — Null and missing values

- `null` where an object is expected
- `undefined` where a value is expected
- Missing optional fields in a request body
- Fields present but set to `null` explicitly
- Partially populated objects (some required fields missing)

### Dimension 5 — State and ordering

- Running the operation twice (idempotency: does it produce duplicates?)
- Running the operation on already-completed state (e.g., canceling a canceled order)
- Running operations out of expected order
- Concurrent calls (two users doing the same operation at the same time)
- Calling a cleanup/delete before the resource is fully initialized
- Interrupted operations (what happens if the process crashes halfway?)

### Dimension 6 — Authorization and ownership

- Accessing a resource belonging to another user
- Accessing a deleted or expired resource
- Using an expired or revoked token
- Accessing with insufficient permissions (role too low)
- Accessing with no authentication at all
- Privilege escalation attempts (passing someone else's ID in the request body)

### Dimension 7 — External dependencies

- Third-party API returns an error
- Third-party API times out
- Third-party API returns an unexpected response shape
- Database is unavailable or returns a constraint violation
- File system is full or read-only

### Format the output

```markdown
## Edge Cases for [Function/Endpoint/Flow]

### Critical (must handle — will cause data loss, security issue, or crash)
1. [Edge case] — [Why it's critical] — [What currently happens / what should happen]

### High (should handle — causes incorrect behavior or poor UX)
1. [Edge case] — [Expected behavior]

### Medium (nice to handle — minor issues or uncommon paths)
1. [Edge case] — [Expected behavior]

### Out of scope / acceptable to ignore
1. [Edge case] — [Why it's acceptable to not handle]

### Suggested test cases
[List the top 5–7 cases to write as unit/integration tests, in order of priority]
```

## Example

**Input to Agent:**
> "Use the Edge Case Discovery skill on this function:
> ```ts
> async function transferFunds(fromAccountId: string, toAccountId: string, amount: number) {
>   const from = await Account.findById(fromAccountId);
>   const to = await Account.findById(toAccountId);
>   from.balance -= amount;
>   to.balance += amount;
>   await from.save();
>   await to.save();
> }
> ```"

**Output from Agent:**

> ## Edge Cases for `transferFunds`
>
> ### Critical
> 1. **`amount` is negative** — Caller passes `-100`, which silently reverses the transfer direction. Should throw a validation error.
> 2. **`fromAccountId === toAccountId`** — Transferring to the same account: balance unchanged but operation succeeds silently. May indicate a bug in the caller.
> 3. **Insufficient balance** — `from.balance` goes negative. No guard exists. Should check balance before deducting.
> 4. **Race condition on concurrent transfers** — Two simultaneous transfers from the same account can both read the same balance and both succeed, causing a negative balance. Requires a database transaction with row-level locking.
> 5. **`from.save()` succeeds but `to.save()` fails** — Money is deducted from sender but never credited to receiver. The whole operation must be wrapped in a database transaction that rolls back on failure.
>
> ### High
> 6. **`fromAccountId` or `toAccountId` not found** — `Account.findById` returns `null`, and `from.balance` throws `Cannot read properties of null`. Add existence checks.
> 7. **`amount` is `0`** — Technically valid but likely a bug in the caller. Consider throwing a validation error.
> 8. **`amount` is `Infinity` or `NaN`** — JavaScript will not throw; balance becomes `Infinity` or `NaN` silently.
>
> ### Suggested test cases
> 1. Transfer with insufficient balance → expect error thrown, balances unchanged
> 2. Transfer to self → expect error thrown
> 3. Transfer with negative amount → expect validation error
> 4. Either account not found → expect error thrown, no balance changes
> 5. `to.save()` throws → expect `from` balance is rolled back

## Notes

- Run this skill before writing tests, not after — it's faster to discover edge cases analytically than by writing tests and waiting for them to fail.
- For APIs, always run Dimension 6 (authorization) — authorization edge cases are the most commonly missed and the most dangerous.
- Not every edge case needs a test — some can be handled with a single defensive guard at the function boundary.
