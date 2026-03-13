---
name: pravidhi-bug-review-pipeline
description: "Run a structured, adversarial multi-agent bug review pipeline on a codebase. Use this skill whenever the user wants to find bugs, audit code quality, review a codebase for issues, or run any kind of bug-finding or code analysis workflow. Also trigger when the user asks to 'review my code for bugs', 'find all issues in this repo', 'audit this codebase', or any similar request. The pipeline uses three sequential phases: a Bug Finder that maximizes issue discovery, a Bug Adversary that challenges false positives, and an Arbiter that issues final verdicts — producing a clean, high-confidence bug report."
---

# Bug Review Pipeline

A three-phase adversarial code review system. Three agents check each other's work to produce a reliable, deduplicated bug report.

## Overview

```
Phase 1: Bug Finder     → ./issues/YYYY-MM-DD-report.md
Phase 2: Bug Adversary  → ./issues/YYYY-MM-DD-refutation.md  
Phase 3: Arbiter        → ./issues/YYYY-MM-DD-final.md
```

All output files use today's date. Run each phase sequentially — each agent reads the previous agent's output.

---

## Setup

Before running any phase, ensure the output directory exists:

```bash
mkdir -p ./issues
```

If the user has not specified a codebase path, ask them which directory or files to analyze. If they say "this repo" or similar, use the current working directory.

---

## Phase 1 — Bug Finder

**Goal:** Maximize bug discovery. Cast a wide net. False positives are acceptable; missed bugs are not.

**Read:** `agents/bug-finder.md`

**Inputs:** Codebase files (read recursively from target directory)  
**Output:** `./issues/YYYY-MM-DD-report.md`

### Scoring
| Severity | Points | Examples |
|----------|--------|---------|
| Low      | +1     | Edge cases, cosmetic issues, minor inconsistencies |
| Medium   | +5     | Functional bugs, data issues, performance problems |
| Critical | +10    | Security vulns, data loss, crashes |

### What to look for
- **Security:** Injection flaws, auth bypass, hardcoded secrets, insecure deserialization, path traversal
- **Correctness:** Off-by-one errors, null/undefined handling, incorrect logic, wrong operator use
- **Data integrity:** Race conditions, incorrect transactions, missing validation, lossy type coercion
- **Error handling:** Swallowed exceptions, missing error states, no retry logic
- **Performance:** N+1 queries, unbounded loops, memory leaks, blocking I/O
- **API contracts:** Incorrect HTTP status codes, missing required fields, type mismatches
- **Dependencies:** Outdated packages with known CVEs, version conflicts
- **Config/Infra:** Missing env var validation, insecure defaults, overly broad permissions

### Report format

```markdown
# Bug Report — YYYY-MM-DD

## Summary
- Total bugs found: N
- Critical: N | Medium: N | Low: N
- Total score: N

---

## BUG-001 — [Short Title]
**Location:** `path/to/file.ext:line_number`  
**Severity:** Critical / Medium / Low  
**Points:** 10 / 5 / 1  

**Description:**  
What the bug is and why it's a problem.

**Evidence:**  
```code snippet if relevant```

**Suggested Fix:**  
How to resolve it.

---
[repeat for all bugs]

## Total Score: N
```

---

## Phase 2 — Bug Adversary

**Goal:** Eliminate false positives by challenging every reported bug.

**Read:** `agents/bug-adversary.md`

**Inputs:** `./issues/YYYY-MM-DD-report.md` + the codebase  
**Output:** `./issues/YYYY-MM-DD-refutation.md`

### Scoring
| Outcome | Points |
|---------|--------|
| Successfully disprove a bug | +[bug's original score] |
| Wrongly dismiss a real bug  | −2× [bug's original score] |

The 2× penalty means only challenge bugs you're confident about.

### Strategies for disproving bugs
- Show the bug is unreachable (guarded by conditions, dead code, env constraints)
- Show the "issue" is intentional design with documented reasoning
- Show the test suite already covers the scenario
- Show the framework/library handles it automatically
- Show the impact is negligible given the deployment context
- Confirm the fix already exists elsewhere in the codebase

### Refutation report format

```markdown
# Bug Refutation — YYYY-MM-DD

## Summary
- Bugs reviewed: N
- Disproved: N (score gained: +N)
- Accepted: N (real bugs remaining)
- Final score: N

---

## BUG-001 — [Title from report]
**Original severity/points:** Critical / 10  

**Counter-argument:**  
Why this is NOT a bug (or why the risk is negligible).

**Confidence:** 85%  
**Risk calculation:** +10 if correct, −20 if wrong → EV = 0.85×10 − 0.15×20 = +5.5 → DISPROVE  

**Decision:** DISPROVE / ACCEPT  
**Points:** +N / 0  

---
[repeat for all bugs]

## Accepted bugs (verified real issues)
- BUG-XXX: [title] — Medium
- BUG-XXX: [title] — Critical
```

---

## Phase 3 — Arbiter

**Goal:** Final verdict on all disputed and accepted bugs.

**Read:** `agents/arbiter.md`

**Inputs:** Both previous reports + the codebase  
**Output:** `./issues/YYYY-MM-DD-final.md`

### Arbitration approach
For each bug, weigh:
1. The Bug Finder's original evidence
2. The Adversary's counter-argument
3. The actual code (ground truth)

Give benefit of the doubt to the **Bug Finder** for Critical severity bugs (better safe than sorry). Apply stricter scrutiny to Low severity items.

### Final report format

```markdown
# Final Bug Review — YYYY-MM-DD

## Executive Summary
- Confirmed real bugs: N
- Dismissed as false positives: N  
- Critical issues requiring immediate attention: N

---

## Confirmed Bugs

### BUG-001 — [Title]
**Severity:** Critical / Medium / Low  
**Location:** `file:line`  

**Finder's claim:** [summary]  
**Skeptic's counter:** [summary]  
**Arbiter's analysis:** [reasoning]  

**VERDICT: REAL BUG**  
**Confidence:** High / Medium / Low  
**Action required:** [what to do]

---

## Dismissed (False Positives)

### BUG-00N — [Title]
**VERDICT: NOT A BUG**  
**Reason:** [why it was dismissed]

---

## Prioritized Action List
1. [Critical] BUG-XXX — [title]
2. [Critical] BUG-XXX — [title]
3. [Medium] BUG-XXX — [title]
...
```

---

## Running the full pipeline

When the user asks to run the bug review pipeline on a codebase:

1. **Identify scope** — Confirm what files/directories to analyze
2. **Read relevant code** — Load the target codebase files
3. **Run Phase 1** — Act as Bug Finder; produce the report
4. **Run Phase 2** — Act as Bug Adversary; challenge the report
5. **Run Phase 3** — Act as Arbiter; produce final verdicts
6. **Present results** — Summarize the final confirmed bug list to the user

Tell the user upfront that the pipeline has three phases and give status updates as each completes.

> **Note:** If the codebase is large (>50 files or >5,000 lines), consider running Phase 1 on focused subsystems (auth, data layer, API endpoints) rather than all files at once, to maintain analysis quality.

---

## Tips for quality output

- **Cite exact line numbers** whenever possible — vague locations reduce actionability
- **Include code snippets** as evidence for non-obvious bugs  
- **Rate impact in context** — a SQL injection in an internal admin tool is still Critical, but a TOCTOU race on a read-only endpoint may be Low
- **Track bug IDs consistently** across all three reports (BUG-001, BUG-002, etc.)
- **Don't merge bugs** — if two related issues have distinct root causes, report them separately

For agent-specific instructions and scoring details, see the `agents/` directory.