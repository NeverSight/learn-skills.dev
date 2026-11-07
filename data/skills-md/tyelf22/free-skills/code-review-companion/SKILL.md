---
name: code-review-companion
description: "Paste in a diff and get a structured review: bugs, edge cases, naming, and the one thing worth fixing before merge. Use when the user asks for \"Code Review Companion\" or provides paste a diff or code snippet."
metadata:
  author: "skillvize"
  version: "v1.0"
  source: "https://www.skillvize.com/skills/tech-code-review"
---

# Code Review Companion

Paste in a diff and get a structured review: bugs, edge cases, naming, and the one thing worth fixing before merge.

`{{input}}` in the steps below is the user's input (Paste a diff or code snippet).

## Steps

### 1. Scan for bugs

Read {{input}} line by line and flag anything that looks like a bug: logic errors, typos, off-by-ones, wrong comparisons. Quote the line.

### 2. Check edge cases

Identify unhandled inputs: null/undefined, empty collections, zero, negatives, unexpected types. List what's missing.

### 3. Review naming and clarity

Flag names, structures, or conditions that would confuse the next reader. Suggest a clearer alternative for each.

### 4. Pick the one fix that matters

Name the single issue that should block merging and explain its impact in one sentence.

## Example

**Paste a diff or code snippet:** function getDiscount(user) {
  if (user.role = 'admin') return 1;
  return user.tier === 'gold' ? 0.2 : 0;
}

**Output:**

```
CODE REVIEW

BUGS
• Line 2 uses `=` (assignment) not `===` — always sets role to 'admin' and returns true.

EDGE CASES
• No handling for missing `user.tier` — falls through to 0, which may be fine but isn't explicit.

NAMING
• `getDiscount` returning 1 (100%) for admins is surprising — consider `getDiscountRate` or a comment.

FIX FIRST
The `=` vs `===` bug — it grants every user an admin-level discount.
```
