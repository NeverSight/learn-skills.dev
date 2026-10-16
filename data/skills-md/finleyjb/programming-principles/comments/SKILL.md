---
name: comments
description: Comments are powerful tools that must be used judiciously. Reach when writing, editing, or reviewing inline comments.
---

Comments are a powerful tool for readability when used judiciously. The default is no comment; add one only where the code cannot explain itself.

The code says *what*; the comment says *why*. A comment that restates the code adds noise and rots the fastest. State the reason alone — opening with the action the code already shows ("subtract 1: labels are 1-based") puts the *what* right back.

## What deserves a comment

Things the code cannot express:

- Assumptions that invariants allow us to make that aren't obvious, particularly when the invariant is enforced elsewhere
- Business rules and where they come from
- The reason behind an unusual or non-obvious choice
- Consequences not obvious from the code alone

## Comments in examples

Comments in examples MAY provide information about the code example. They can document whether the example is a preferred pattern or a bad pattern. They may additionally document file names.

## Examples

```js
// AVOID: restates the code
// add the item to the total
total += item.price;

// PREFER: explains the constraint
// prices are integer cents so sums never drift into floats
total += item.price;
```

```python
# AVOID: restates the code
# retry up to 3 times
for attempt in range(3): ...

# PREFER: explains the reason
# the service briefly 429s during deploys
for attempt in range(3): ...
```

```rust
// AVOID: restates the code
// iterate in reverse
for i in (0..items.len()).rev() { ... }

// PREFER: explains the non-obvious reason
// removing an element shifts the indexes of everything after it
for i in (0..items.len()).rev() { ... }
```

## Maintenance

Comments are lines of code. When code changes, update or delete its comment with it. A comment that no longer describes the code is worse than none.

## TODO comments

A TODO is a promise. Keep one only with a concrete plan: an issue number, an owner, a deadline. Without a plan, it is a deferred wish — delete it or do the work now.

TODO comments SHOULD be avoided unless there is a concrete plan to fix them.

## Conventions and style rules

Language conventions and style rules MUST supercede these instructions. Where a project's style guide, linter, or language conventions dictate their own comment rules, follow those instead.
