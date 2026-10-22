---
name: qa-automation-test-consolidation
description: Detect redundant tests, duplicated test logic, semantic overlaps, and parameterization opportunities across the entire test suite. Present recommendations and request user approval before refactoring.
license: MIT
metadata:
  author: Testomat.io
  version: 1.0.0
---

## Summary

This skill analyzes an entire test suite to identify duplicate tests, semantic overlaps, duplicated test logic, parameterization opportunities, and overlapping business-rule validations. It prioritizes behavioral similarity over code similarity and recommends refactorings that reduce maintenance effort while preserving test coverage and business intent. No changes are applied without explicit user approval.

## How the Loop Works

- Analyze the entire test suite for consolidation opportunities;
- Group findings by type and confidence level;
- Present a summary of the proposed changes and request user approval;
- Apply the approved refactorings;
- Re-analyze the updated test suite to identify newly exposed consolidation opportunities;
- Repeat until no additional consolidation opportunities with a confidence level greater than 80% remain.

## Definition of Done

- The entire test suite has been analyzed;
- All consolidation opportunities have been presented to the user;
- All approved refactorings have been applied;
- The test suite has been re-analyzed after each iteration;
- No duplicate tests, duplicated test logic, parameterization opportunities, or business-rule overlaps with a confidence level greater than 80% remain.