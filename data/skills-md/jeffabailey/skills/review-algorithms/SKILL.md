---
name: review-algorithms
description: Analyzes code for algorithm/data structure correctness, concurrency safety, and edge case handling, producing fitness scores (1-10) across algorithm choice, data structure selection, complexity awareness, concurrency safety, edge case handling, and correctness patterns. Use when the user says /review:review-algorithms, requests an algorithm review, asks about correctness of data structure choices, wants a concurrency safety check, asks about edge case coverage, or wants to verify algorithmic complexity. This is NOT a performance review -- it asks "is this correct and appropriate?" not "is this fast enough?" Only reports findings with confidence >= 7/10.
metadata:
  version: "1.0.0"
---

# Algorithm & Data Structure Fitness Review

Analyze the codebase (or the files, modules, or questions the user names) for algorithm and data structure fitness. Identify correctness risks, inappropriate structure choices, concurrency hazards, and edge case gaps using evidence from the code. This review asks "is this correct? is this the right approach? will this break?" -- not "is this fast enough?"

Reference: [Fundamentals of Algorithms](https://jeffbailey.us/blog/2025/12/04/fundamentals-of-algorithms/) — see also [Fundamental Algorithmic Patterns](https://jeffbailey.us/blog/2025/12/12/fundamental-algorithmic-patterns/), [Fundamental Data Structures](https://jeffbailey.us/blog/2025/12/10/fundamental-data-structures/), and [Fundamentals](https://jeffbailey.us/categories/fundamentals/)

## Domain Knowledge

- `references/rubric.md` is the scoring source: severity definitions, the proof required for HIGH and CRITICAL, 1-10 anchors per dimension, the N/A rule, and how to compute the overall score. Read it first; it is short.
- `references/checklist.md` is what to look for during steps 4-6.
- `references/wisdom.md` is optional background generated from the blog posts linked above (4,000+ lines). Grep it by heading for a specific question (for example `grep -n "^### " references/wisdom.md`); never read it whole.

## Configuration

Invoke the resolver CLI to obtain effective weights and thresholds for the review target. Never load `fitness-config.json` directly.

```bash
python3 "${CLAUDE_SKILL_DIR}/../../scripts/fitness-config.py" show --path <target>
```

`${CLAUDE_SKILL_DIR}` is this skill's directory; the resolver ships two levels up in the plugin's `scripts/`. If your agent does not expand the variable, substitute the directory containing this `SKILL.md`.

Where `<target>` is the file or directory under review. The CLI walks up to discover any module override and merges it with the root config. Include the `Config:` and `Effective weights:` lines from the resolver output within the first 10 lines of the final report as the provenance trail (AC-03.1, AC-08.2). The `effective` object inside the JSON block delimited by `<!-- BEGIN_EFFECTIVE_CONFIG_JSON -->` / `<!-- END_EFFECTIVE_CONFIG_JSON -->` carries weights, status thresholds, security, and scoring for any programmatic needs.

## Workflow

1. **Read the rubric and checklist** -- `references/rubric.md`, then skim `references/checklist.md`.

2. **Scope the review** -- The target is what the user named (files, directory, or question), else the repository. If the user asked specific questions ("is it deterministic?", "any races?"), note them; the report answers them first.

3. **Decide which dimensions apply** -- For each of the six dimensions, decide whether anything in scope can be evaluated. Mark the rest `N/A -- <reason>` with evidence for the absence (rubric.md, "N/A"). Concurrency Safety is N/A for single-threaded code; do not fill it with hypothetical races between overlapping runs.

4. **Map the logic that can be wrong** -- Algorithms are not only sorts, graphs, and DP. Include:
   - sorting, searching, traversal, recursion, nested loops, custom data structures;
   - merge, override, and precedence logic (config chains, layered defaults, dict merges);
   - validation and parsing: what a validator accepts versus what downstream code assumes;
   - path, slice, and index arithmetic (walk-up-to-root loops, `[:n]` vs `[:n+1]`);
   - dedupe, ordering, and anything whose output is stored, diffed, or compared between runs;
   - loops bounded by a stop condition: what happens when the input starts outside the expected tree (a path above or beside the project root);
   - parallel lists re-paired with `zip`, and error messages: does the message name the file or value that is actually wrong?
   Use Grep/Glob to find these, then read the code around each. Where one rule is enforced on one path (single file, proposal, write) but not on another (merged chain, read), check whether the other path can reach the same bad state.

5. **Evaluate each applicable dimension** against `references/checklist.md`: algorithm choice, data structure fit, complexity, concurrency, edge cases, correctness patterns.

6. **Probe edge inputs** -- Running the code finds bugs that reading misses. For each hotspot, call the function or run the CLI on edge inputs: empty, one element, boundary index, the root or top level, a target outside the project, `null` / `[]` / a scalar where an object is expected, wrong-typed values (`"1"` for `1`), unknown keys, values the validator accepts that the consumer might not, and a second `PYTHONHASHSEED` (or equivalent) where output order matters. Work in a scratch directory or temp files; never modify the user's files. Every edge input a user can type or put in a file is supported input, so a defect it triggers is a finding at whatever severity its impact earns, including LOW.

7. **Confirm HIGH and CRITICAL findings** -- Every HIGH or CRITICAL finding needs a minimal reproduction: the command or snippet you ran and the output you observed. A finding you cannot reproduce but can see plainly in the code stays in the report at MEDIUM or LOW with "not reproduced: <why>" in its Reproduction field; drop it only when the code does not support it (rubric.md, "Proof for HIGH and CRITICAL"). Severity follows impact, so a reproduced finding keeps the severity its impact earns: a validator that passes input the next command crashes on is still that, even when the fix is one line.

8. **Score** each applicable dimension with file:line evidence, using the anchors in `references/rubric.md`. Compute the overall per rubric.md.

9. **Self-check, then write the report** (see Output Format). Before writing, check that:
   - every cited file:line exists and says what the finding claims;
   - every finding has confidence >= 7, and every HIGH/CRITICAL has a Reproduction;
   - no finding depends on an unsupported setup (rubric.md, "Not a finding"), and no reproduced or code-evident defect was left out just because it is LOW;
   - the overall equals the stated computation over the named dimensions;
   - no secret values are reproduced (refer to secrets by file:line only).

## Confidence and Severity

Only report findings with confidence >= 7/10. For each finding, ask:
- Is this a real pattern in the code, not a guess about runtime behavior?
- Can you point to a specific file and line?
- Is it reachable in normal, supported use of this code?

If any answer is no, do not report it. Missing a theoretical issue costs less than a report full of noise, because readers stop trusting the real findings. The filter is about whether a defect is real, not how important it is: a reproduced bug, or one the code plainly shows, is not noise even at LOW, and leaving it out hides real defects from the reader. Noise is speculation: guesses about runtime behavior, setups the code does not support, and style. Severity levels (CRITICAL, HIGH, MEDIUM, LOW), with algorithm-specific examples, are defined in `references/rubric.md`.

## Scoring Dimensions (1-10 each)

Score anchors for each dimension are in `references/rubric.md`; what to check is in `references/checklist.md`.

1. **Algorithm Choice** -- Whether algorithms match problem structure: sorting strategy, search approach, graph traversal, merge/precedence logic, divide-and-conquer, dynamic programming, greedy, batching
2. **Data Structure Selection** -- Whether collections match access patterns, ordered vs unordered, bounded vs unbounded, mutable vs immutable, concurrent structures where needed
3. **Complexity Awareness** -- Hidden quadratic behavior, unnecessary recomputation, unbounded growth, string concatenation in loops, amortized cost awareness
4. **Concurrency Safety** -- Shared mutable state protection, race conditions, lock ordering, atomic operations, thread-safe collections, ownership model (N/A when nothing in scope is concurrent)
5. **Edge Case Handling** -- Empty collections, null inputs, boundary values, off-by-one errors, validator/consumer agreement, integer overflow, floating-point comparison, division by zero, Unicode
6. **Correctness Patterns** -- Invariant maintenance, idempotency, determinism, error propagation, loop termination, precondition/postcondition checks, equality/hash consistency

## Output Format

Write the report to `docs/algorithms-review.md` at the root of the repository that contains the target, unless the user gives a path. For a review scoped to a subdirectory or a set of files, write `docs/algorithms-review-<scope-slug>.md` instead (for example `docs/algorithms-review-scripts-fitness-config.md`) so a scoped run does not replace the whole-repo report.

```markdown
# Algorithm & Data Structure Fitness Review

**Target:** <path(s) or scope reviewed>
Config: <copied from resolver output>
Effective weights: <copied from resolver output>

## Direct Answer

(Only when the user asked specific questions. Answer each in one to three sentences, citing the finding numbers below.)

## Summary

Overall fitness score: X.X / 10 (mean of <named scored dimensions>; status <band>)

| Dimension | Score | Key Finding |
|-----------|-------|-------------|
| Algorithm Choice | X/10 | ... |
| Data Structure Selection | X/10 | ... |
| Complexity Awareness | X/10 | ... |
| Concurrency Safety | X/10 or N/A -- reason | ... |
| Edge Case Handling | X/10 | ... |
| Correctness Patterns | X/10 | ... |

## Detailed Findings

### Finding 1: [Title]
- **Severity:** CRITICAL / HIGH / MEDIUM / LOW
- **Confidence:** X/10
- **Dimension:** [which scoring dimension]
- **Location:** file:line
- **Description:** What the issue is and why it matters.
- **Evidence:** The specific code pattern found.
- **Reproduction:** (required for HIGH/CRITICAL) command or snippet run, and the observed output.
- **Impact:** What goes wrong, and on which input.
- **Remediation:** Concrete fix with code example or specific steps.

(repeat for each finding, ordered by severity)

### Algorithm Choice (X/10)
- Evidence: file:line references, including what was checked and found sound
- Issues found
- Recommendations

(repeat for each dimension; for N/A dimensions give the reason and evidence of absence)

## Top Action Items (up to 5, by impact)

1. [CRITICAL/HIGH/MEDIUM] Description -- file:line
2. ...

## Reference

Based on [Fundamentals of Algorithms](https://jeffbailey.us/blog/2025/12/04/fundamentals-of-algorithms/), [Fundamental Algorithmic Patterns](https://jeffbailey.us/blog/2025/12/12/fundamental-algorithmic-patterns/), [Fundamental Data Structures](https://jeffbailey.us/blog/2025/12/10/fundamental-data-structures/), and guidance from https://jeffbailey.us/categories/fundamentals/
```
