---
name: project-analyzer
description: "Deeply analyzes an existing software project and generates 3-4 comprehensive reports in the docs/analyze/ folder. Trigger when phrases like 'analyze the project', 'do code analysis', 'project review', 'architecture report', 'technical debt', 'project evaluation', 'codebase analysis' occur. Works when a project directory or repo URL is provided. If API endpoints are detected, it automatically generates a 4th report."
---

# Project Analyzer Skill

**Outputs:**
- `docs/analyze/01-project-overview.md`
- `docs/analyze/02-architecture-and-code-quality.md`
- `docs/analyze/03-risks-and-recommendations.md`
- `docs/analyze/04-api-endpoint-list.md` (only if API exists)

Systematically scan the project, perform a deep analysis, turn your findings into 3 (4 if an API exists) separate reports, and save them to the `docs/analyze/` folder.

**Core rule:** Do not perform a superficial review. Actually look at the code, read the files, and provide examples for every heading. The report must contain concrete findings — do not make generic assessments.

---

## PHASE 1 — Project Discovery (Do This First)

Get to know the project before the analysis starts. Execute the discovery script:

```bash
bash ~/.gemini/antigravity/skills/project-analyzer/scripts/phase1_discovery.sh
```

**Note the following after discovery:**
- Main language(s) and framework(s)
- Project type: monolith / microservice / monorepo / library
- Package manager
- Test presence: does it exist, is it prevalent?
- API type: REST / GraphQL / gRPC / WebSocket / none

---

## PHASE 2 — Deep Analysis

Dive into the code in each category, read it, and extract concrete findings. Execute the analysis script:

```bash
bash ~/.gemini/antigravity/skills/project-analyzer/scripts/phase2_analysis.sh
```

Review the outputs of this script carefully. The script outputs details regarding:
- Architecture (folder structures, large files, circular dependencies clues)
- Code Quality (TODOs, `any` usage in TS, console logs, duplicate functions, error handling)
- Security (hardcoded secrets, committed .envs, raw SQL injection risks, vulnerable deps, auth middleware)
- Performance (N+1 query risks, large bundles, caching, async/await usages)
- Tests (test files layout, config presence)
- APIs (REST endpoints, GraphQL, Swagger files)

---

## PHASE 3 — Report Generation

Create the `docs/analyze/` folder and save the 3 (or 4) reports.

```bash
mkdir -p docs/analyze
```

---

### REPORT 1: `01-project-overview.md`

```markdown
# Project Overview

> Analysis Date: [DATE]
> Analyzed by: Project Analyzer Skill v1.0

## Summary Card

| Feature | Value |
|---------|-------|
| Project name | [package.json name or folder name] |
| Project type | [Monolith / Microservice / Monorepo / Library] |
| Main language | [TypeScript / Python / Go / ...] |
| Framework | [Hono / FastAPI / Express / Next.js / ...] |
| Package manager | [bun / pnpm / yarn / pip / ...] |
| Total source files | [N] |
| Total lines of code | [N] |
| Test coverage | [Yes / No / Partial] |
| API type | [REST / GraphQL / gRPC / None] |
| Last commit | [date] |
| Active developers | [N people] |

## Project Purpose

[summary from package.json description or README — explain in your own words]

## Folder Structure

[show a clean tree from the find output, explain the purpose of each folder in one line]

## Technology Stack

### Production Dependencies
[List each important package and write its purpose]

### Development Tools
[List test, lint, and build tools]

## Development Process Indicators

| Indicator | Value | Comment |
|-----------|-------|---------|
| Commits last 3 months | [N] | [active / low / none] |
| Test / source ratio | [%N] | [good / moderate / inadequate] |
| Number of TODOs | [N] | [clean / caution / problematic] |
| Documentation | [Yes / Partial / No] | |

## Strengths

[Write about what is genuinely good — be concrete, provide code references]

## Weaknesses

[Concrete issues — not "generally bad", but "there is a Y issue in file X"]
```

---

### REPORT 2: `02-architecture-and-code-quality.md`

```markdown
# Architecture and Code Quality Analysis

## Architecture Assessment

### Layer Structure
[Are there layers? Controller/Service/Repository separation? Give concrete examples]

### Dependency Management
[Is there circular dependency? Is the import chain logical?]

### Modularity Score
[ ⭐⭐⭐⭐⭐ ] — [justification]

## Code Quality Metrics

| Metric | Value | Status |
|--------|-------|--------|
| Largest file | [file name: N lines] | [✅ / ⚠️ / 🔴] |
| 'any' usage (TS) | [N found] | [✅ / ⚠️ / 🔴] |
| TODO/FIXME count | [N] | [✅ / ⚠️ / 🔴] |
| console.log (prod) | [N] | [✅ / ⚠️ / 🔴] |
| try/catch ratio | [N try, N catch] | [✅ / ⚠️ / 🔴] |

## Files Requiring Attention

[List the largest, most complex files and those with the most TODOs — explain why they are risky]

### [file-name.ts] — [N lines]
> Reason for attention: [explanation]
> Recommendation: [what should be done]

## Duplicate Code (DRY Violations)

[Is similar logic written in different places? Concrete examples]

## Error Handling Quality

[Is try/catch prevalent? Are error messages meaningful? Unhandled promise rejection risk?]

## Type Safety (TypeScript)

[Usage of 'any', is strict mode enabled, are type definitions complete?]

## Overall Code Quality Score

```
Architecture     : [1-10] / 10
Readability      : [1-10] / 10  
Maintainability  : [1-10] / 10
Test Coverage    : [1-10] / 10
─────────────────────────
Overall          : [average] / 10
```

## Best Written Sections

[Parts of the code that are genuinely good — give concrete examples]

## Sections Most in Need of Improvement

[Concrete, prioritized improvement suggestions — state the estimated effort for each]
```

---

### REPORT 3: `03-risks-and-recommendations.md`

```markdown
# Risks and Recommendations

## Risk Matrix

| Risk | Category | Impact | Probability | Priority |
|------|----------|--------|-------------|----------|
| [risk name] | [Security/Performance/Tech Debt/Operations] | [High/Medium/Low] | [H/M/L] | [🔴/🟡/🟢] |

## 🔴 Critical Risks (Immediate Action Required)

### [Risk Name]
**Category:** [Security / Performance / ...]
**Location:** [file:line or module]
**Issue:** [concrete explanation]
**Evidence:** [grep output or code example]
**Fix:** [step-by-step what needs to be done]
**Estimated Effort:** [1 hour / 1 day / 1 week]

## 🟡 Significant Risks (Address in the Short Term)

[Same format — 3-5 risks]

## 🟢 Improvement Recommendations (Long Term)

[Same format — 3-5 recommendations]

## Security Analysis

### Positive Findings
[Good security practices — concrete]

### Concerning Findings
[Concrete security vulnerabilities or risks]

## Performance Analysis

### Bottleneck Candidates
[N+1 query, heavy package, lack of cache, async issues]

### Optimization Opportunities
[Concrete recommendations and expected gains]

## Technical Debt Inventory

| Debt | File/Module | Estimated Effort | Priority |
|------|-------------|------------------|----------|
| [explanation] | [location] | [effort] | [🔴/🟡/🟢] |

## Proposed Action Plan

### This Week
1. [most critical, concrete step]
2. [...]

### This Month
1. [important improvements]
2. [...]

### Long Term (3-6 Months)
1. [architectural improvements]
2. [...]

## Overall Health Score

```
Security         : [1-10] / 10
Performance      : [1-10] / 10
Maintainability  : [1-10] / 10
Test Coverage    : [1-10] / 10
Documentation    : [1-10] / 10
─────────────────────────────
Project Health   : [average] / 10
```
```

---

### REPORT 4: `04-api-endpoint-list.md` (Only if API Exists)

```markdown
# API Endpoint List

> Generated automatically by code scanning.
> Date: [DATE]

## Summary

| Metric | Value |
|--------|-------|
| Total endpoints | [N] |
| GET | [N] |
| POST | [N] |
| PUT/PATCH | [N] |
| DELETE | [N] |
| Requires Auth | [N] (estimated) |
| Documented | [N] |

## Endpoint Catalog

### [/api/auth] — Authentication
| Method | Path | Description | Auth | Source File |
|--------|------|-------------|------|-------------|
| POST | /api/auth/register | User registration | ❌ | src/routes/auth.ts:12 |
| POST | /api/auth/login | Login | ❌ | src/routes/auth.ts:28 |
| POST | /api/auth/logout | Logout | ✅ | src/routes/auth.ts:45 |
| GET | /api/auth/me | Current user | ✅ | src/routes/auth.ts:58 |

### [/api/...] — [other groups]
[same format — group the endpoints]

## Auth Requirements Analysis

[Which endpoints are protected, which are open? Are there missing auth rules?]

## Missing Documentation

[Endpoints without Swagger/OpenAPI definitions]

## Security Notes

[Is rate limit missing? Is there input validation? How are CORS settings?]

## Recommendations

[OpenAPI spec generation, versioning strategy, missing endpoints]
```

---

## PHASE 4 — Save Files

```bash
# Create the directory
mkdir -p docs/analyze

# Save the reports
# (Save each report separately using the write_file tool)

# Show summary
echo "✅ Analysis complete"
echo "📁 docs/analyze/"
ls -la docs/analyze/
```

---

## Quality Control

Perform the following checks before saving each report:

```
□ No generic statements — every sentence is based on concrete data or findings
□ Code references exist — "File X line N", "Function Y has problem Z"
□ Numeric metrics are real (from grep/wc output)
□ Risk priorities are logical — not everything is red
□ Recommendations are actionable — not "improve code", but "do X"
□ Scores are justified — why 7/10? because...
□ API report: source file reference exists for each endpoint
```

---

## Error Scenarios

**If not a Git repo:**
→ Skip Git statistics, analyze everything else.

**Very large project (>50K lines):**
→ Take a sample from each category, state this clearly in the report.

**If no tests exist:**
→ Report test coverage as 0%, add a test strategy to the recommendations section.

**If API detection is unclear:**
→ Write "API could not be detected", do not generate the 4th report — list suspicious files instead.

**Permission error:**
→ Skip inaccessible files, note it in the report.

---

## When to Skip

- If no project directory is provided and the user is just asking a general question.
- If there is no code to analyze (empty project, only configuration files).
