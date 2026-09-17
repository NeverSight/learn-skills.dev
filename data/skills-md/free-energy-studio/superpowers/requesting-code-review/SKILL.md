---
name: requesting-code-review
description: Use when a material change needs independent scrutiny before delivery, or when repository policy or the user requires review.
---

# Request Useful Review

Review should find consequential mistakes and unnecessary complexity, not add
features or ceremony.

Choose review depth based on the change's risk, scope, and repository policy.
A small local edit may need only self-review and its test; changes to permissions,
shared contracts, data integrity, or broad behavior warrant independent scrutiny.

Give the reviewer the requirement, actual diff or commit range, relevant context,
verification results, and specific uncertainties. Ask them to check correctness,
scope, necessity, and integration. `code-reviewer.md` is a compact prompt template.

If agents are available and delegation is permitted, a read-only reviewer can do
this work independently. Do not create a review hierarchy for every task. If
independent review is required but unavailable, report that gap.

Evaluate findings against evidence. Fix real defects and recheck affected behavior.
Challenge speculative additions and distinguish preferences from blockers.
A review verdict is not merge authorization.
