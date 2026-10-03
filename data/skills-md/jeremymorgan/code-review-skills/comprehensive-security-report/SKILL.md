---
name: comprehensive-security-report
description: Aggregates findings from the other security audits into one prioritized security report. Use after running individual security reviews to produce a consolidated report.
license: CC0-1.0
metadata:
  category: security
allowed-tools: Read Grep Glob Write
disable-model-invocation: true
argument-hint: "[path or scope]"
---

**Target:** $ARGUMENTS

If no target path is given above, review the entire codebase.

---

## Comprehensive Security Report

Start by reading all existing audit files in the `audits/` directory (e.g. `audits/*.md`). These were produced by the individual security audit skills. Synthesize their findings into one consolidated report. If no prior audit files exist, perform a fresh analysis of the target codebase before writing the report.

The consolidated report must include:

## Executive Summary
Summarize the overall security posture (Critical/High/Medium/Low), total vulnerability counts by severity, and the top immediate actions required.

## Critical Vulnerabilities (Fix Immediately)
List each critical finding with its source audit file, CWE reference if applicable, and affected code locations.

## High Priority Issues (Fix within 1 week)
List each high-severity finding with code locations and remediation steps.

## Medium Priority Issues (Fix within 1 month)
List each medium-severity finding with recommendations.

## Low Priority Issues (Fix in next release)
List low-severity improvements.

## Security Recommendations
1. Implementation priorities
2. Security tools to adopt
3. Process improvements
4. Training needs

## Compliance Checklist
- OWASP Top 10 coverage
- PCI DSS (if handling payments)
- GDPR (if handling EU data)
- SOC 2 requirements

## Testing Guide
Include curl commands or test scripts to verify each fix.

---

## Constraints & style:

Be concrete and cite exact code locations and identifiers from the source audit files or from direct analysis.

Prefer minimal, drop-in fix snippets over prose.

Do not invent files or functions that aren’t present; if context is missing, mark as Unable to verify and say what code would prove it.

Write this into a markdown file and place it in the audits/ folder.
