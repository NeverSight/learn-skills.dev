---
name: invariants
description: Finds the state machines and rules an app relies on but never enforces, then returns a numbered report of where to enforce each one.
disable-model-invocation: true
---

# Invariants

This skill reads an app for the rules its code assumes but never writes down. It finds flags that only make sense together and assumptions no line checks, then returns one numbered report.

## Every rule traced to a line

A rule counts only when a line relies on it, such as a read that breaks if the rule is false. Each finding names that line and the line that enforces the rule, or says none does. A rule inferred from naming alone is `Not verified`.

The sweep covers interface state: component state, stores, context, refs, URL params and the server data the interface reads. Server code and databases are in scope only when the user names them.

Showing each state on one page belongs to `lab`. The states of one animation belong to `deconstruct`. A fallback that hid a broken rule cites `restraint-no-fallbacks`. A fix that belongs in a shared component cites `reuse-fix-in-the-primitive`. Opening the result runs in `verify`.

## 1. Group the flags that move together

List every boolean, status string and nullable value in scope with the lines that write it. Flags set in the same handler, or read together in one condition, form one group. Reporting `isOpen` and `isClosing` as two findings is `invariants-group-the-flags`.

## 2. Write the machine each group implies

For each group, write the states it can rest in as a table of state, entered on and left on. Count the combinations the flags allow against the states the table names. "These flags look related" with no count is `invariants-count-the-combinations`.

Every combination no state names is an impossible state. Give each one the line that produces it, such as an error handler that never clears `isLoading`. One that no line reaches is still listed, marked unreachable.

## 3. Collapse each group into one status

Replace the group with one discriminated union or reducer, so an impossible state cannot be written. `isLoading`, `isError` and `data` kept side by side is `invariants-one-status`.

Transitions live in one place: the reducer, or the events that call it. A status set directly from five components is `invariants-one-writer`.

## 4. Find what the code assumes

Run each search across the scope and list every hit. Reading files by eye for assumptions is `invariants-search-every-shape`.

| Shape | Search |
| --- | --- |
| Non-null assertion | `\w!\.` and `\w!\)` |
| Cast past the type | ` as [A-Z]` and `as unknown as` |
| First item read blind | `\[0\]` and `.at(0)` |
| Find used as found | `.find(` with no check before the next read |
| Keys that must be unique | `key={` on a field nothing dedupes |
| Order that must hold | An effect or listener that reads what another one sets |
| One of a kind | "only one", "should never" and "always" in comments |
| Default hiding a gap | `?? []`, `?? ""` and `?? 0` on values that are always set |

## 5. Name where each rule is enforced

For each hit, write the rule in one sentence, the line that relies on it and the line that enforces it. Enforcement is a type, a parse where the data enters, an assertion or a single writer. A comment is not enforcement. "IDs are probably unique" with no lines is `invariants-name-the-enforcer`.

## 6. Enforce once, at the edge

Put each rule where the data enters: a type the compiler checks, a schema parse at the fetch or a guard in the one writer. The same guard repeated at every read is `invariants-enforce-at-the-edge`. A rule left as a comment, such as `// never empty`, is `invariants-enforce-in-code`.

## 7. Number the findings

Number machines and invariants in one list, ranked by severity, then by reach. Each finding gives its rule, both lines and the fix. A finding with no line is `invariants-numbered-report`.

Change nothing until the user picks numbers, as `audit-fix-what-was-picked` requires.

## The pair

Every check is a pair. The broken line sits beside the line that replaces it.

| Rule | Broken | Replacement |
| --- | --- | --- |
| `invariants-group-the-flags` | `isOpen` and `isClosing` reported as two findings | One group: `isOpen`, `isClosing` and `isAnimating` |
| `invariants-count-the-combinations` | "These flags look related" | "3 flags, 8 combinations, 4 named states, 4 impossible" |
| `invariants-one-status` | `isLoading`, `isError` and `data` side by side | `{ status: "error", error }` or `{ status: "done", data }` |
| `invariants-one-writer` | `setStatus("closing")` called from five components | One `close` event handled in the reducer |
| `invariants-search-every-shape` | Files read by eye for assumptions | Every search in the table run, hits listed |
| `invariants-name-the-enforcer` | "IDs are probably unique" | "`rows.tsx:40` keys on `id`, nothing enforces it" |
| `invariants-enforce-at-the-edge` | `if (!items.length) return` in six components | The schema at `api.ts:12` rejects an empty list |
| `invariants-enforce-in-code` | `// never empty` | `items: [Item, ...Item[]]` |
| `invariants-numbered-report` | "State handling is fragile" | "3. `menu.tsx:18`, open and closing both true after Escape" |

## Reporting

**Severity.** `HIGH` is an impossible state a line can reach, or an assumption that crashes or loses work when broken. `MEDIUM` is an ungrouped set of flags, a status with many writers or a rule enforced only by a comment. `LOW` is an impossible state no line reaches, or a guard repeated at every read.

**Format.** One finding per root cause, numbered:

```
1. file:line - [rule-id] the rule, the line that breaks it, where to enforce it
```

Then a `Rule | Count | Severity` summary. `Block` when any `HIGH` remains, `Approve` otherwise. Mark a rule read from naming alone as `Not verified`.
