---
name: sarif-issue-reporter
description: Analyze SARIF files and generate security reports with CVSS scoring, exploitation scenarios, and remediation guidance. Use when reviewing static analysis results.
disable-model-invocation: true
aliases:
  - sarif-analyzer
  - security-report
  - sarif-reporter
version: 0.0.1
author: Herman Stevens
tags: [security, sarif, vulnerability-analysis, reporting]
---

# SARIF Issue Reporter

Analyze SARIF files and generate comprehensive security reports.

**Target:** $ARGUMENTS (path to SARIF file)

## When to Use This Skill

- Reviewing static analysis results from security scanners
- Generating vulnerability reports with CVSS scoring
- Validating SAST findings (true vs false positives)
- Mapping vulnerabilities to compliance frameworks
- Creating remediation guidance with code examples

## Core Capabilities

| Capability | Description |
|------------|-------------|
| SARIF Parsing | Read SARIF 2.1.0 format from any scanner |
| Verification | Confirm findings, identify false positives |
| CVSS Scoring | Calculate scores with vector strings |
| Standards Mapping | OWASP, CWE, CAPEC, compliance frameworks |
| Remediation | Code examples and implementation steps |

## Workflow

### Phase 1: Parse SARIF
1. Load SARIF file at $ARGUMENTS
2. Extract tool metadata from `runs[].tool.driver`
3. Get all results from `runs[].results[]`
4. Categorize by severity level

### Phase 2: Verify Each Issue
1. **Extract**: Location, snippet, codeFlows, related locations
2. **Verify**: Confirm issue exists, check for false positives, assess exploitability
3. **Enhance**: Request additional code context if needed

### Phase 3: Security Assessment

**CVSS 3.1 Scoring** - Calculate and justify each metric:
- Attack Vector (AV): N/A/L/P
- Attack Complexity (AC): L/H
- Privileges Required (PR): N/L/H
- User Interaction (UI): N/R
- Scope (S): U/C
- Impact (C/I/A): N/L/H each

Vector format: `CVSS:3.1/AV:_/AC:_/PR:_/UI:_/S:_/C:_/I:_/A:_`

**Impact Analysis**: Technical impact, business impact, exploitability, affected assets.

### Phase 4: Standards Mapping

Map each verified issue to:

| Standard | Action |
|----------|--------|
| **OWASP Top 10** | Identify category (A01-A10) |
| **CWE** | Specific ID + parent/child |
| **CAPEC** | Attack patterns |
| **Compliance** | PCI-DSS, GDPR, SOC 2, HIPAA, ISO 27001, NIST |

Reference: [OWASP Top 10](https://owasp.org/www-project-top-ten/) | [CWE](https://cwe.mitre.org/) | [CAPEC](https://capec.mitre.org/)

### Phase 5: Report Generation

For each verified issue, generate this report structure:

```markdown
## [ISSUE-XXX] {Title}

**Severity**: {Critical|High|Medium|Low} | **CVSS**: {Score} ({Vector}) | **Status**: Verified

### Summary
{2-3 sentence overview}

### Code Evidence
**Location**: `{file}:{line}`
```{language}
{code snippet with context}
```

### Exploitation
**Attack Vector**: {Description}
**PoC**: {Example exploit code or request}
**Prerequisites**: {What attacker needs}

### Impact
- **C/I/A**: {Confidentiality/Integrity/Availability impacts}
- **Business**: {Consequences}

### Standards Mapping
- **OWASP**: {Category}
- **CWE**: CWE-{ID}
- **CAPEC**: CAPEC-{ID}
- **Compliance**: {PCI-DSS/GDPR/SOC2 requirements}

### Security Patterns Violated
- **{Pattern}**: Expected {X}, found {Y}

### Remediation
**Priority**: {Level}
```{language}
{Fix code}
```
**Steps**: {Implementation guidance}

### Validation
{Test commands or verification steps}
```

## Implementation Steps

1. **Load SARIF** - Parse JSON at $ARGUMENTS path
2. **Extract Issues** - Get `runs[].results[]` array
3. **For Each Issue**:
   - Get location from `physicalLocation`
   - Read code context if snippet missing
   - Verify finding exists in source
   - Calculate CVSS with justification
   - Map to standards (OWASP/CWE/CAPEC)
   - Generate remediation code
4. **Output Report** - Markdown format (primary)

### Quality Checklist

Before finalizing each issue:
- [ ] CVSS score calculated with justification
- [ ] Code evidence with context
- [ ] Realistic exploitation scenario
- [ ] Security pattern identified
- [ ] OWASP/CWE/CAPEC mapped
- [ ] Working remediation code

**SARIF Reference**: [SARIF 2.1.0 Spec](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)

## Example Usage

```
User: Analyze results.sarif and report critical/high issues
Claude:
1. Parse SARIF → 2. Filter by severity → 3. Verify each finding
4. Calculate CVSS → 5. Map to standards → 6. Generate report
```

## Best Practices

| Practice | Why |
|----------|-----|
| Always verify | SAST tools produce false positives |
| Realistic exploitation | Theoretical attacks aren't useful |
| Working remediation code | Not pseudo-code |
| Complete standards mapping | OWASP/CWE/CAPEC/Compliance |
| Sufficient code context | Understand the full picture |

## Executive Summary Template

```markdown
# Security Analysis Report
**Tool**: {name} | **Date**: {date} | **Scope**: {files scanned}

## Overview
| Metric | Count |
|--------|-------|
| Total Issues | {n} |
| Verified | {n} |
| False Positives | {n} |

## Severity Distribution
Critical (9.0-10.0): {n} | High (7.0-8.9): {n} | Medium (4.0-6.9): {n} | Low (0.1-3.9): {n}

## Top Risks
1. {Issue} - CVSS {score}
2. {Issue} - CVSS {score}
3. {Issue} - CVSS {score}
```

## Anti-Patterns

- Reporting unverified issues
- Generic remediation advice
- Missing exploitation scenarios
- Incomplete CVSS justification
- Ignoring code context

## Success Criteria

- [ ] All critical/high issues verified
- [ ] CVSS scores justified
- [ ] Working exploitation examples
- [ ] Production-ready remediation code
- [ ] Complete standards mapping

## References

- [SARIF Spec](https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html)
- [CVSS Calculator](https://www.first.org/cvss/calculator/3.1)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)

Helper script available: `scripts/sarif_helper.py`
