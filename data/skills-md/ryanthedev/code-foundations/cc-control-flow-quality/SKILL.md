---
name: cc-control-flow-quality
description: "Audits and restructures control flow using Code Complete's nesting, cyclomatic complexity, loop design, guard-clause, and boolean simplification rules. Covers deep nesting, loop exit design, index naming, and callback chains. For statement-level flow inside a routine; not for routine/class structure (use cc-routine-and-class-design) or staging a broader refactor (use cc-refactoring-guidance)."
user-invocable: false
---

# cc-control-flow-quality

## Thresholds

| Threshold | Value | Source |
|---|---|---|
| Max nesting depth | 3 levels | Yourdon 1986a |
| McCabe complexity | >10 decision points → redesign | McCabe 1976 |
| Else-clause consideration | 50–80% of ifs need an else | Elshoff 1976 |
| Loop-with-exit comprehension | 25% better than top/bottom test | Soloway 1983 |
| Mental entity limit | 5–9 items | Miller 1956 |

Shared numeric thresholds and the cohesion/coupling vocabulary: `Read(${CLAUDE_PLUGIN_ROOT}/references/cc-foundations.md)`.

The full audit checklists (conditionals, structure, loops, tables): `Read(${CLAUDE_SKILL_DIR}/checklists/conditionals-and-structure.md)` and `Read(${CLAUDE_SKILL_DIR}/checklists/loops-and-advanced.md)`.

**Principles:**
- Use `true`/`false`, not `0`/`1`, for booleans.
- `for`/`foreach` when the iteration count is known; `while` when not.
- Test at the beginning (may not execute) vs the end (executes at least once).
- Put the nominal case in `if`, the error case in `else` — except guard clauses, which invert this intentionally.
- Fully parenthesize complex boolean expressions.

## Core patterns

### Deep nesting → guard clauses

Guard clauses are an exception pattern: error/invalid cases exit early at the top so the nominal path flows without nesting. Use them at function entry; use "nominal in if" for conditionals within the body.

```cpp
// BEFORE: arrow-shaped (4 levels), nominal case buried
if (file.validName()) {
    if (file.open()) {
        if (encryptionKey.valid()) {
            if (file.decrypt(encryptionKey)) { /* lots of code */ }
        }
    }
}

// AFTER: guard clauses flatten it
if (!file.validName()) return;
if (!file.open()) return;
if (!encryptionKey.valid()) return;
if (!file.decrypt(encryptionKey)) return;
// lots of code (nominal case at top level)
```

### Complex boolean → named intermediate variables

```cpp
bool printerCanPrint = printerReady && !printerBusy &&
                       paperAvailable && paperLevel > MIN_PAPER;
bool documentCanBePrinted = documentValid && !documentEmpty &&
                            documentSize < MAX_SIZE;
if (inputStatus == SUCCESS && printerCanPrint && documentCanBePrinted) { print(); }
```

### Meaningless loop indexes → descriptive names

```java
// BEFORE: transaction[j][i][k] — is this right? who knows
// AFTER: self-documenting and verifiable
for (int payCodeIdx = 0; payCodeIdx < numPayCodes; payCodeIdx++)
    for (int month = 0; month < 12; month++)
        for (int divisionIdx = 0; divisionIdx < numDivisions; divisionIdx++)
            sum += transaction[month][payCodeIdx][divisionIdx];
```

### Single-use test → named boolean function

Putting a test into a well-named function improves readability, and that alone justifies it — even for a single use [p.433].

```cpp
bool isProcessableLetter(char c) {
    bool isLetter = (('a' <= c) && (c <= 'z')) || (('A' <= c) && (c <= 'Z'));
    bool isExcluded = (c == 'X') || (c == 'x');
    return isLetter && !isExcluded;
}
if (isProcessableLetter(inputChar)) { processLetter(inputChar); }
```

### Number-line ordering and zero comparisons

```cpp
if (MIN_VALUE <= count && count <= MAX_VALUE)  // in-range: variable between bounds
if (count < MIN_VALUE || MAX_VALUE < count)    // out-of-range: variable on the outside

while (!done)                  // boolean: compare implicitly
while (balance != 0)           // numeric: compare explicitly
while (*charPtr != '\0')       // character: compare to the terminator
while (bufferPtr != NULL)      // pointer: compare to NULL
```

### Loop-with-exit avoids duplication

```cpp
// AFTER: while(true) + break eliminates the duplicated read at top and bottom
while (true) {
    GetNextRating(&ratingIncrement);
    rating += ratingIncrement;
    if (!((score < targetScore) && (ratingIncrement != 0))) break;
    GetNextScore(&scoreIncrement);
    score += scoreIncrement;
}
```

## Decision guidance

### Loop selection

1. Iteration count known ahead of time? → `for`/`foreach`, else `while`.
2. Must the body execute at least once? → test at END (`do-while`)/MIDDLE, else test at BEGINNING.
3. Simple iteration through a container? → `foreach` (eliminates housekeeping arithmetic errors).
4. Need to exit from the middle? → loop-with-exit (`while(true)` + `break`).

### Nesting reduction (least to most invasive — choose by fit, not strict order)

1. Guard clauses — exit early on error conditions.
2. Extract nested code into a well-named routine.
3. Combine nested ifs into a single compound test.
4. Convert to case/switch when testing the same variable repeatedly.
5. Polymorphism — replace type-checking conditionals with dispatch.
6. Table-driven methods — when logic maps data to outcomes.

#5 and #6 are context-dependent, not ranked: tables can be simpler than polymorphism. "The fact that a design uses inheritance and polymorphism doesn't make it a good design" [p.423].

### Table-driven methods

Consider a table instead of branching logic when: writing the 4th+ branch in an if-else chain for the same classification; creating a subclass just to change a data value; rules change often without wanting code changes; or the same lookup is duplicated in several places.

Access method: direct (data keys straight into the table, e.g. month 1–12) → indexed (large/sparse keyspace, few entries) → stair-step (entries valid for ranges, e.g. grade thresholds).

### McCabe complexity

Count: start at 1, add 1 per `if`/`while`/`for`/`and`/`or` and per case branch.

| Count | Verdict |
|---|---|
| 0–5 | Probably fine |
| 6–10 | Start simplifying |
| 10–20 | Strong justification needed; review for extraction |
| 20+ | Mandatory refactor |

A routine in the 10–20 range is acceptable only when all of: it's a flat dispatch (switch/case, no nesting within cases); each case is ≤3 lines (ideally a single call); cases are exhaustive and unlikely to grow unboundedly; and cognitive complexity is low. Inherent-complexity or "just a big if-else chain" do not qualify — extract instead.

## Modern equivalents

The same flatten-the-structure principle applies beyond Code Complete's era: async/await replaces callback nesting, and exhaustiveness-checked pattern matching is the valid high-McCabe flat dispatch.

## Chain

| After | Next |
|---|---|
| Control flow verified | `Skill(code-foundations:code-clarity-and-docs)` |
