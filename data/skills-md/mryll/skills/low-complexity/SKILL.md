---
name: low-complexity
version: 1.0.0
description: Enforce low Cognitive Complexity (SonarSource) and low Cyclomatic Complexity in ALL code written or modified, in any programming language, framework, or platform. This skill MUST activate automatically whenever code is being written, generated, modified, or refactored — no explicit trigger needed. Triggers include writing any function, method, class, module, script, handler, endpoint, test, or code block. Also triggers on "low complexity", "cognitive complexity", "cyclomatic complexity", "reduce complexity", "simplify code", "too complex", "refactor for readability", "clean code", "implement", "fix bug", "add feature", "generate test", "optimize", "rewrite", "scaffold".
---

# Low Complexity Code

Every function/method written or modified MUST target:
- **Cognitive Complexity <= 5** (SonarSource metric). Acceptable up to 10 for inherently complex logic. Never exceed 15.
- **Cyclomatic Complexity <= 5**. Acceptable up to 10. Never exceed 15.

For full scoring rules, see [cognitive-complexity-spec.md](references/cognitive-complexity-spec.md).

## Cognitive Complexity Quick Reference

**+1 for each:** `if`, ternary (`? :`), `switch` (whole), `for`, `while`, `do while`, `catch`, `else if`, `else`, `goto LABEL`, `break/continue LABEL`, each method in a recursion cycle, each sequence of like boolean operators (`&&` / `||`).

**+1 nesting penalty** on top of structural increment for: `if`, ternary, `switch`, `for`, `while`, `catch` — when nested inside another flow-break structure.

**Free (no increment):** method calls, `try`, `finally`, `case` labels, null-coalescing (`?.`, `??`), early `return`, simple `break`/`continue`, lambdas (but lambdas increase nesting level).

## Cyclomatic Complexity Quick Reference

+1 for the method entry, +1 for each: `if`, `else if`, `for`, `while`, `do while`, `case`, `catch`, `&&`, `||`, ternary `?`. Core definition; some analyzers may vary by language.

## Mandatory Reduction Techniques

Apply these in order of preference:

1. **Extract method/function** — Move a coherent block into a named function. Resets nesting to 0. First choice when the extracted block forms a coherent unit.
2. **Early return / guard clause** — Invert condition, return early, reduce nesting by 1 level.
3. **Replace nested conditions with flat logic** — `if A { if B {` becomes `if A && B {` (saves nesting penalty).
4. **Replace if/else chains with polymorphism, strategy pattern, or lookup table** — Eliminates branching entirely.
5. **Replace loop + condition with declarative pipeline** — `filter/map/reduce` or LINQ or streams instead of `for` + `if`.
6. **Decompose boolean expressions** — Extract complex conditions into named boolean variables or predicate functions.
7. **Replace flag variables with early exit** — Eliminate boolean flags that control flow later.
8. **Use language idioms** — Null-coalescing, optional chaining, pattern matching, destructuring. These are often lower-cost than equivalent if/else chains (destructuring is free; pattern matching is +1 for the whole match vs +1 per branch in if/else).

## How to Apply

When writing any function/method:

1. Write the logic
2. Mentally count: each `if/else if/else/for/while/switch/catch/ternary` = +1, each nesting level on structural ones = +1 more, each boolean operator sequence = +1
3. If score > 5, refactor using the techniques above before finalizing
4. Prefer multiple small functions over one large function
5. Nesting depth > 2 is a smell — extract immediately

## Bad vs Good Examples

### Bad: Nested conditionals (CogC = 9)
```python
def process(user, order):
    if user.is_active:                    # +1
        if order.is_valid:                # +2 (nesting=1)
            if order.total > 100:         # +3 (nesting=2)
                apply_discount(order)
            else:                         # +1
                charge_full(order)
        else:                             # +1
            raise InvalidOrder()
    else:                                 # +1
        raise InactiveUser()              # Total: 1+2+3+1+1+1 = 9
```

### Good: Guard clauses + extraction (process CogC=2, charge CogC=2)
```python
def process(user, order):               # CogC = 2
    if not user.is_active:                # +1
        raise InactiveUser()
    if not order.is_valid:                # +1
        raise InvalidOrder()
    charge(order)

def charge(order):                       # CogC = 2
    if order.total > 100:                 # +1
        apply_discount(order)
    else:                                 # +1
        charge_full(order)
```

### Bad: Loop with nested conditions (CogC = 10)
```javascript
function findFirst(items, criteria) {
  for (const item of items) {              // +1
    if (item.active) {                     // +2 (nesting=1)
      if (item.type === criteria.type) {   // +3 (nesting=2)
        if (item.score > criteria.min) {   // +4 (nesting=3)
          return item;
        }
      }
    }
  }                                        // Total: 1+2+3+4 = 10
  return null;
}
```

### Good: Flat filter + early continue (findFirst CogC=5, matches CogC=1)
```javascript
function findFirst(items, criteria) {      // CogC = 5
  for (const item of items) {              // +1
    if (!item.active) continue;            // +2 (nesting=1)
    if (matches(item, criteria)) return item; // +2 (nesting=1)
  }
  return null;
}

function matches(item, criteria) {         // CogC = 1
  return item.type === criteria.type       // +1 (&& sequence)
    && item.score > criteria.min;
}
```
