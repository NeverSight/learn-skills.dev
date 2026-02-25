---
name: audit-context-building
description: Enables ultra-granular, line-by-line code analysis to build deep architectural context before vulnerability or bug finding.
category: audit-context-building
author: Trail of Bits
source: trailofbits/skills
license: AGPL-3.0
trit: -1
trit_label: MINUS
verified: true
featured: false
---

# Audit Context Building Skill

**Trit**: -1 (MINUS)
**Category**: audit-context-building
**Author**: Trail of Bits
**Source**: trailofbits/skills
**License**: AGPL-3.0

## Description

Enables ultra-granular, line-by-line code analysis to build deep architectural context before vulnerability or bug finding.

## When to Use

This is a Trail of Bits security skill. Refer to the original repository for detailed usage guidelines and examples.

See: https://github.com/trailofbits/skills

## Related Skills

- audit-context-building
- codeql
- semgrep
- variant-analysis


## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 2. Domain-Specific Languages

**Concepts**: DSL, wrapper, pattern-directed, embedding

### GF(3) Balanced Triad

```
audit-context-building (−) + SDF.Ch2 (−) + [balancer] (−) = 0
```

**Skill Trit**: -1 (MINUS - verification)


### Connection Pattern

DSLs embed domain knowledge. This skill defines domain-specific operations.
