---
name: code-reviewer
description: Performs structured code reviews analyzing diffs or files for bugs, security vulnerabilities, performance issues, style violations, and maintainability concerns. Produces categorized findings with severity levels and actionable fix suggestions. Use when reviewing code, pull requests, merge requests, code changes, or when the user asks for feedback on their code.
---

# Code Reviewer

## Overview

Perform thorough, structured code reviews that catch real issues and provide
actionable feedback. Every finding is categorized by type, assigned a severity
level, and paired with a concrete fix suggestion. The goal is a review that a
developer can act on immediately — not vague observations.

## When to use

- When reviewing a pull request or merge request
- When a user asks for feedback on code they've written
- When examining a diff or changeset for issues
- When auditing code for security, performance, or quality
- When asked to "review this code" or "check this for bugs"

**Do NOT use when:**

- The user wants code written from scratch (use a code generation skill)
- The user wants a refactoring plan (use a refactoring skill)
- The user only wants formatting/linting (suggest an automated tool instead)

## Severity Classification

Every finding MUST have one of these severity levels:

| Severity     | Meaning                                                  | Examples                                                    |
| ------------ | -------------------------------------------------------- | ----------------------------------------------------------- |
| **critical** | Will cause data loss, security breach, or system failure | SQL injection, unvalidated auth, data corruption            |
| **high**     | Likely to cause bugs in production or significant issues | Race conditions, missing error handling, N+1 queries        |
| **medium**   | Code smell or moderate risk that should be addressed     | Magic numbers, overly complex logic, missing validation     |
| **low**      | Minor improvement that would make code better            | Naming conventions, minor style issues, documentation gaps  |
| **info**     | Observation or suggestion, not a problem                 | Alternative approaches, FYI notes, praise for good patterns |

## Category Definitions

Every finding MUST be assigned one category:

| Category            | What it covers                                                |
| ------------------- | ------------------------------------------------------------- |
| **bug**             | Logic errors, off-by-one, null derefs, incorrect conditions   |
| **security**        | Injection, auth bypass, data exposure, insecure defaults      |
| **performance**     | N+1 queries, unnecessary allocations, missing caching, O(n^2) |
| **style**           | Naming, formatting, idiomatic usage, readability              |
| **maintainability** | Complexity, coupling, missing abstractions, testability       |
| **testing**         | Missing tests, untested edge cases, test quality              |

## Workflow

### 1. Understand Context

Before reviewing line-by-line, understand the big picture:

- **What does this code do?** Read the PR description, commit messages, or ask.
- **What language/framework?** Adjust expectations to the ecosystem's
  conventions.
- **What's the scope?** A 10-line utility function gets different scrutiny than
  a 500-line auth module.
- **Are there tests?** Note their presence or absence early.

Output: A 1-2 sentence summary of what the code is doing and its context.

### 2. Scan for Bugs and Logic Errors

Read through the code looking for correctness issues:

- Off-by-one errors in loops and array access
- Null/undefined dereferences
- Incorrect boolean logic or operator precedence
- Missing return statements or unreachable code
- Race conditions in concurrent code
- Incorrect error propagation

For each bug found, note the exact line, what's wrong, and what the fix is.

### 3. Check Security

Systematically check for common vulnerability classes:

- **Injection**: SQL, command, XSS, template injection — any place user input
  reaches a sink
- **Authentication/Authorization**: Missing auth checks, privilege escalation
  paths
- **Data exposure**: Secrets in code, verbose error messages, logging sensitive
  data
- **Insecure defaults**: Disabled TLS verification, permissive CORS, weak crypto
- **Input validation**: Missing or insufficient validation of external input

Security findings are almost always **critical** or **high** severity.

### 4. Evaluate Performance

Look for patterns that will cause performance problems at scale:

- **N+1 queries**: Database calls inside loops
- **Unbounded operations**: Missing pagination, loading entire tables
- **Unnecessary work**: Redundant computations, repeated parsing
- **Missing caching**: Expensive operations that could be cached
- **Algorithmic complexity**: O(n^2) or worse where O(n) or O(n log n) is
  possible
- **Resource leaks**: Unclosed connections, file handles, streams

### 5. Assess Style and Readability

Check that the code is clear and follows conventions:

- Consistent naming (camelCase, snake_case — match the project)
- Functions and variables have descriptive names
- No deeply nested conditionals (> 3 levels)
- Comments explain "why", not "what"
- Dead code or commented-out code removed
- Consistent error handling patterns

Style findings are typically **low** or **info** severity.

### 6. Check Maintainability

Evaluate long-term code health:

- **Function length**: Functions over 50 lines likely need extraction
- **Cyclomatic complexity**: Too many branches = hard to test and reason about
- **Magic numbers/strings**: Unnamed constants scattered through code
- **Coupling**: Does this code depend on too many other modules?
- **Testability**: Can this code be unit tested without mocking the world?
- **Duplication**: Copy-pasted logic that should be extracted

### 7. Produce Structured Report

Compile all findings into the output format below. Order findings by severity
(critical first, info last). Include a summary section with overall assessment.

## Output Format

Structure every review as follows:

````markdown
## Code Review Summary

**Context**: [1-2 sentence summary of what the code does] **Overall
Assessment**: [PASS | PASS WITH CONCERNS | NEEDS CHANGES | REJECT] **Findings**:
[N critical, N high, N medium, N low, N info]

## Findings

### [SEVERITY] [CATEGORY]: [Brief title]

**Location**: [file:line or description of where] **Issue**: [What's wrong and
why it matters] **Suggestion**: [Specific code or approach to fix it]

```diff
- problematic code
+ suggested fix
```

---

[Repeat for each finding, ordered by severity]

## Recommendations

[2-3 sentences on the most important things to address before merging]
````

Also produce a structured `findings.json`:

```json
{
  "summary": {
    "context": "Brief description",
    "overall_assessment": "NEEDS CHANGES",
    "total_findings": 5,
    "by_severity": {
      "critical": 1,
      "high": 1,
      "medium": 2,
      "low": 1,
      "info": 0
    },
    "by_category": {
      "security": 1,
      "bug": 1,
      "performance": 1,
      "style": 1,
      "maintainability": 1
    }
  },
  "findings": [
    {
      "severity": "critical",
      "category": "security",
      "title": "SQL injection via unsanitized user input",
      "location": "app/db.py:42",
      "issue": "User input is concatenated directly into SQL query string",
      "suggestion": "Use parameterized queries instead of string concatenation",
      "fix_diff": "- cursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")\n+ cursor.execute(\"SELECT * FROM users WHERE id = %s\", (user_id,))"
    }
  ]
}
```

## Example

**Input code to review:**

```python
def get_user_orders(db, user_id):
    query = "SELECT * FROM orders WHERE user_id = " + user_id
    results = db.execute(query)
    orders = []
    for row in results:
        product = db.execute(f"SELECT name FROM products WHERE id = {row['product_id']}")
        orders.append({"order": row, "product": product[0]["name"]})
    return orders
```

**Review output:**

## Code Review Summary

**Context**: Function retrieves a user's orders with product names from a
database. **Overall Assessment**: NEEDS CHANGES **Findings**: 1 critical, 1
high, 1 medium, 0 low, 0 info

## Findings

### CRITICAL SECURITY: SQL injection via string concatenation

**Location**: Line 2 **Issue**: `user_id` is concatenated directly into the SQL
query. An attacker can inject arbitrary SQL (e.g.,
`1 OR 1=1; DROP TABLE orders`). This is the #1 web application vulnerability
(OWASP A03:2021). **Suggestion**: Use parameterized queries.

```diff
- query = "SELECT * FROM orders WHERE user_id = " + user_id
+ query = "SELECT * FROM orders WHERE user_id = %s"
+ results = db.execute(query, (user_id,))
```

### HIGH PERFORMANCE: N+1 query pattern

**Location**: Lines 4-6 **Issue**: For each order row, a separate database query
fetches the product name. With 100 orders, this executes 101 queries instead
of 2. This will degrade linearly with data volume. **Suggestion**: Use a JOIN or
batch query.

```diff
- for row in results:
-     product = db.execute(f"SELECT name FROM products WHERE id = {row['product_id']}")
-     orders.append({"order": row, "product": product[0]["name"]})
+ query = """
+     SELECT o.*, p.name as product_name
+     FROM orders o JOIN products p ON o.product_id = p.id
+     WHERE o.user_id = %s
+ """
+ results = db.execute(query, (user_id,))
+ orders = [{"order": row, "product": row["product_name"]} for row in results]
```

### MEDIUM BUG: No error handling for empty results

**Location**: Line 7 **Issue**: If `product` query returns empty results,
`product[0]["name"]` will raise an IndexError. This is likely when products are
deleted but orders remain. **Suggestion**: Add a guard for empty results.

```diff
- orders.append({"order": row, "product": product[0]["name"]})
+ product_name = product[0]["name"] if product else "Unknown Product"
+ orders.append({"order": row, "product": product_name})
```

## Recommendations

Fix the SQL injection immediately — it's a critical security vulnerability. Then
refactor the N+1 query pattern with a JOIN, which will also eliminate the empty
result bug. Add parameterized queries throughout.

---

## Common Mistakes

| Mistake                                      | Fix                                                                               |
| -------------------------------------------- | --------------------------------------------------------------------------------- |
| Vague findings like "this could be improved" | Always state WHAT is wrong, WHY it matters, and HOW to fix it                     |
| Missing severity levels                      | Every finding needs critical/high/medium/low/info                                 |
| Reviewing only for style, ignoring security  | Follow the full workflow: bugs → security → performance → style → maintainability |
| Suggesting fixes without showing code        | Include diff-style code suggestions for non-trivial fixes                         |
| Treating all issues as equal priority        | Order by severity; developers should fix critical/high first                      |
| Reviewing code you don't understand          | Ask for context first; state assumptions explicitly                               |
| Nitpicking style in code with critical bugs  | Focus on what matters most; don't bury critical findings in style noise           |

## Key Principles

1. **Be specific, not vague** — "Line 42 has an SQL injection because user_id is
   concatenated into the query" beats "watch out for security issues." Every
   finding must point to a specific location and explain the concrete problem.

2. **Always suggest a complete fix** — Identifying a problem without a solution
   is only half the job. Include code diffs or clear instructions for every
   finding above info severity. A fix must be concrete enough that a developer
   can implement it without guessing — show the actual code change, not just
   "add error handling." If the fix requires imports, setup, or configuration
   changes, include those too.

3. **Explain the why** — Developers learn and prioritize better when they
   understand consequences. "This N+1 pattern will execute 1001 queries for 1000
   rows" is more compelling than "this is an N+1 query."

4. **Prioritize ruthlessly** — A review with 3 critical findings and 2 high
   findings is more useful than one with 47 low-severity style nits. Lead with
   what matters.

5. **Categorize consistently** — Use the severity and category system for every
   finding. This lets developers filter, triage, and track review feedback
   systematically.
