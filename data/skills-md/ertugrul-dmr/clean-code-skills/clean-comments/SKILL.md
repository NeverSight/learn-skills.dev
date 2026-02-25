---
name: clean-comments
description: Use when writing, fixing, editing, or reviewing Python comments and docstrings. Enforces Clean Code principles—no metadata, no redundancy, no commented-out code.
---

# Clean Comments

## C1: No Inappropriate Information

Comments shouldn't hold metadata. Use Git for author names, change history, 
ticket numbers, and dates. Comments are for technical notes about code only.

## C2: Delete Obsolete Comments

If a comment describes code that no longer exists or works differently, 
delete it immediately. Stale comments become "floating islands of 
irrelevance and misdirection."

## C3: No Redundant Comments

```python
# Bad - the code already says this
i += 1  # increment i
user.save()  # save the user

# Good - explains WHY, not WHAT
i += 1  # compensate for zero-indexing in display
```

## C4: Write Comments Well

If a comment is worth writing, write it well:
- Choose words carefully
- Use correct grammar
- Don't ramble or state the obvious
- Be brief

## C5: Never Commit Commented-Out Code

```python
# DELETE THIS - it's an abomination
# def old_calculate_tax(income):
#     return income * 0.15
```

Who knows how old it is? Who knows if it's meaningful? Delete it. 
Git remembers everything.

## The Goal

The best comment is the code itself. If you need a comment to explain 
what code does, refactor first, comment last.
