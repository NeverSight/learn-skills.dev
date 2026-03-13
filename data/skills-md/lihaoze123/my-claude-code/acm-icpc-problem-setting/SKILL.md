---
name: acm-icpc-problem-setting
description: Use when preparing algorithm competition problems for ACM-ICPC, CCPC, Codeforces, or similar contests, including problem creation, statement writing, test data generation, and contest organization
---

# ACM-ICPC Problem Setting Best Practices

## Overview

Comprehensive guidance for creating high-quality algorithm competition problems, covering the full workflow from idea conception to publication.

## When to Use

- Creating problems for ACM-ICPC, CCPC, Codeforces, or similar contests
- Writing problem statements with LaTeX
- Generating test data using testlib
- Setting up validators and checkers
- Organizing algorithm competitions

## Quick Reference

| Topic | Detailed Rules |
|-------|----------------|
| Problem conception | [rules/problem-conception.md](rules/problem-conception.md) |
| Statement writing | [rules/statement-writing.md](rules/statement-writing.md) |
| Test data generation | [rules/test-data-generation.md](rules/test-data-generation.md) |
| Special Judge | [rules/spj-checker.md](rules/spj-checker.md) |
| Time/memory limits | [rules/limits-subtasks.md](rules/limits-subtasks.md) |
| Contest organization | [rules/contest-organization.md](rules/contest-organization.md) |

## Core Principles

### Problem Quality
- **Original idea** - No duplicates or trivial enhancements
- **Clear statement** - Every concept defined, no ambiguity
- **Complete constraints** - All variable ranges specified
- **Strong samples** - Catch wrong interpretations

### Data Quality
- **Edge cases** - Min/max values, boundary conditions
- **Diverse constructions** - Random + handcrafted
- **Format compliance** - Linux line endings, no trailing whitespace

### Platform-Specific
- **Polygon** - Integrated workflow for teams
- **Codeforces** - Requires 5-25 rated contests
- **Luogu** - Requires competition awards

## Red Flags - STOP

| Anti-pattern | Fix |
|--------------|-----|
| Undefined terms in statement | Add definitions in problem description |
| Inconsistent terminology | Use same word for same concept |
| Weak samples | Include edge cases and wrong interpretations |
| Incomplete data ranges | Specify ALL variables' ranges |
| Wrong time limit | Test std × 2 minimum |
| Poor subtask design | Use clear structure, avoid percentages |

## Essential Code

### testlib Generator
```cpp
#include "testlib.h"
int main(int argc, char* argv[]) {
    registerGen(argc, argv, 1);
    int n = opt<int>("n");
    vector<int> a(n);
    for (int i = 0; i < n; i++)
        a[i] = rnd.next(1, 1000000);
    println(n);
    println(a);
}
```

### Basic Checker
```cpp
#include "testlib.h"
int main(int argc, char* argv[]) {
    registerTestlibCmd(argc, argv);
    int jans = ans.readInt();
    int pans = ouf.readInt();
    if (pans == jans) quitf(_ok, "%d", pans);
    else quitf(_wa, "expected %d, found %d", jans, pans);
}
```

## References

- [OI Wiki - Problem Setting](https://oi-wiki.org/contest/problemsetting/)
- [testlib Documentation](https://github.com/MikeMirzayanov/testlib)
- [Polygon Platform](https://polygon.codeforces.com/)
