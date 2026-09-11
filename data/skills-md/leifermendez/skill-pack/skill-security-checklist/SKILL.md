---
name: skill-security-checklist
description: "Trigger: security audit, codebase review, technical debt assessment, architecture analysis. Comprehensive audit of any codebase detecting frameworks, languages, architecture patterns, and pain points with pros/cons tables."
license: Apache-2.0
metadata:
  author: leifermendez
  version: "1.0"
  tags: "audit, security, architecture, technical-debt, code-smell, complexity"
---

# Skill: Security & Architecture Checklist

## Activation Contract

Activate this skill when the user needs to:
- **Audit** a codebase for **technical debt**, **security risks**, or **architecture health**
- **Detect** the **tech stack**: frameworks, languages, dependencies, versions
- **Identify** the **software architecture**: DDD, MVC, Hexagonal, Monolith, Microservices, Serverless, or ad-hoc
- **Find** **pain points**: code smells, high complexity, tight coupling, dead code
- **Generate** a **markdown report** with **pros/cons tables** per checklist area
- **Compare** current state against **best practices** and provide **actionable recommendations**

Do not activate for trivial single-file projects or when only linting/formatting is needed.

## Hard Rules

1. **Always run the detection scripts** in `tools/` first; never rely solely on file inspection.
2. **Use bash scripts only** — no JS/Node dependencies in the audit pipeline.
3. **Output MUST be markdown** — human-readable reports with tables, not JSON or YAML.
4. **Report confidence levels** for each detection (High / Medium / Low).
5. **Every checklist item MUST have a pros/cons table** — no exceptions.
6. **Categorize findings** by severity: Critical, Warning, Info.
7. **Respect** `.gitignore` and skip `node_modules`, `vendor`, `dist`, `build`, `.git`.

## Decision Gates

| Situation | Action |
|-----------|--------|
| No `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, `Cargo.toml`, `composer.json` | Use `detect-stack.sh` heuristic mode (file extensions, shebangs, lock files) |
| Framework config found (`next.config.js`, `django/settings.py`, `spring-boot`) | Use `detect-stack.sh` deep mode to extract versions, plugins, customizations |
| Layered folders found (`domain/`, `app/`, `controllers/`, `models/`, `services/`) | Use `detect-architecture.sh` to identify DDD, MVC, Hexagonal, or custom patterns |
| High file count (>500 files) or deep nesting (>6 levels) | Use `analyze-complexity.sh` to flag complexity and coupling |
| `Dockerfile`, `docker-compose.yml`, `k8s/` manifests found | Flag as containerized; add Infrastructure checklist |
| `.env` files, secrets in code, hardcoded credentials | Flag as Critical in Security checklist |
| Multiple conflicting patterns found | Report all with confidence scores; flag as tech debt |

## Execution Steps

### Phase 1: Stack Detection (3 steps)

1. **Detect Languages & Frameworks**
   - Run: `bash assets/detect-stack.sh <project_path>`
   - Detects: languages, frameworks, build tools, package managers, versions
   - Checks: `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, `Cargo.toml`, `composer.json`, `Gemfile`
   - Reports: tech stack summary, versions, dependency count, outdated flags

2. **Detect Architecture Pattern**
   - Run: `bash assets/detect-architecture.sh <project_path>`
   - Detects: DDD, MVC, Hexagonal, Clean Architecture, Monolith, Microservices, Serverless, Event-Driven, CRUD
   - Analyzes: folder structure, file naming, import patterns, layer boundaries
   - Reports: primary pattern, secondary pattern, confidence score, layer violations

3. **Detect Infrastructure & DevOps**
   - Run: `bash assets/detect-infrastructure.sh <project_path>`
   - Detects: Docker, Kubernetes, CI/CD configs, cloud provider, databases, message queues
   - Checks: `Dockerfile`, `docker-compose.yml`, `.github/workflows/`, `terraform/`, `helm/`
   - Reports: deployment strategy, infrastructure maturity, security gaps

### Phase 2: Code Quality Analysis (3 steps)

4. **Analyze Complexity & Code Smells**
   - Run: `bash assets/analyze-complexity.sh <project_path>`
   - Detects: cyclomatic complexity, file length, function length, nesting depth, duplication
   - Flags: God classes, long methods, deep nesting, tight coupling, dead code
   - Reports: complexity hotspots, top 10 risky files, refactoring candidates

5. **Detect Security Risks**
   - Run: `bash assets/detect-security-risks.sh <project_path>`
   - Scans: hardcoded secrets, SQL injection patterns, XSS vulnerabilities, insecure dependencies
   - Checks: `.env` files, API keys, password patterns, dynamic code execution usage, raw SQL strings
   - Reports: critical risks, warnings, mitigation steps

6. **Assess Technical Debt**
   - Run: `bash assets/assess-tech-debt.sh <project_path>`
   - Detects: TODO/FIXME comments, deprecated dependencies, missing tests, broken documentation
   - Flags: legacy code, mixed paradigms, inconsistent naming, missing type safety
   - Reports: debt score, prioritized backlog, quick wins vs major projects

### Phase 3: Report Generation (2 steps)

7. **Aggregate Raw Data**
   - Run: `bash assets/generate-audit-report.sh <project_path>`
   - Combines all phase outputs into a single markdown report
   - Includes: executive summary, detailed findings, pros/cons tables, action items

8. **Generate Final Markdown Report**
   - The LLM reads the aggregated data and generates `AUDIT_REPORT.md`
   - Structure: Executive Summary → Stack Overview → Architecture Analysis → Security Checklist → Quality Checklist → Tech Debt → Action Plan
   - Each section contains: findings, pros/cons table, severity, recommendations

## Output Contract

Return a structured markdown report containing:

```markdown
# Audit Report: {project_name}

## Executive Summary
- **Project**: {path}
- **Languages**: {list}
- **Frameworks**: {list}
- **Architecture**: {pattern} (confidence: {high/medium/low})
- **Overall Health**: {score}/10
- **Critical Issues**: {count}
- **Warnings**: {count}
- **Info**: {count}

## 1. Stack Overview

### Detected Technologies
| Technology | Version | Confidence | Pros | Cons |
|------------|---------|------------|------|------|
| Node.js | 18.2.0 | High | Active LTS, large ecosystem | Version lock-in risk |
| React | 18.1.0 | High | Component model, hooks | Boilerplate, state complexity |
| Prisma | 4.0.0 | Medium | Type-safe ORM | Migration complexity |

### Dependency Analysis
| Category | Count | Outdated | Vulnerable | Recommendation |
|----------|-------|----------|------------|----------------|
| Production | 45 | 12 | 2 | Upgrade `lodash`, `express` |
| Development | 23 | 5 | 0 | Keep devDependencies updated |

## 2. Architecture Analysis

### Detected Pattern: {DDD/MVC/Hexagonal/etc.}
| Aspect | Finding | Pros | Cons | Severity |
|--------|---------|------|------|----------|
| Layer separation | Domain imports Infrastructure | Clear boundaries | Violation of dependency rule | Critical |
| Folder structure | `src/domain`, `src/app` | Organized | Deep nesting (6 levels) | Warning |
| Naming convention | Mixed camelCase/snake_case | Readable | Inconsistent | Info |

### Layer Health Score
| Layer | Score | Issues |
|-------|-------|--------|
| Domain | 8/10 | 1 violation |
| Application | 7/10 | 2 god use cases |
| Infrastructure | 6/10 | 3 hardcoded configs |
| Interface | 7/10 | Missing validation |

## 3. Security Checklist

| Check | Status | Risk | Pros | Cons | Mitigation |
|-------|--------|------|------|------|------------|
| Secrets in code | ❌ FAIL | Critical | Easy config | Leakage risk | Move to env vars |
| SQL injection | ⚠️ WARN | High | Raw queries | Injection risk | Use parameterized queries |
| XSS prevention | ✅ PASS | Low | Input sanitized | - | Maintain current practice |
| Dependency vulns | ⚠️ WARN | Medium | Feature-rich | Known CVEs | Run `npm audit fix` |

## 4. Code Quality Checklist

| Metric | Current | Threshold | Status | Risk | Pros | Cons |
|--------|---------|-----------|--------|------|------|------|
| Cyclomatic complexity | 45 max | 10 | ❌ FAIL | High | Feature-rich | Unmaintainable |
| File length | 800 lines | 300 | ❌ FAIL | High | Complete logic | Hard to review |
| Function length | 150 lines | 50 | ⚠️ WARN | Medium | Complex logic | Testing difficulty |
| Code duplication | 15% | 5% | ⚠️ WARN | Medium | Copy-paste fast | Maintenance nightmare |
| Test coverage | 23% | 70% | ❌ FAIL | Critical | Working features | Regression risk |

## 5. Technical Debt Assessment

| Debt Item | Priority | Effort | Impact | Pros of Fixing | Cons of Delaying |
|-----------|----------|--------|--------|--------------|------------------|
| Missing tests | P0 | 2 weeks | High | Prevents regressions | Bugs accumulate |
| Deprecated deps | P1 | 3 days | Medium | Security patches | Breaking changes |
| Mixed naming | P2 | 1 week | Low | Consistency | Refactoring noise |
| Documentation | P2 | 3 days | Low | Onboarding speed | Knowledge silos |

## 6. Action Plan

### Quick Wins (This Week)
1. [ ] Move secrets to `.env` files
2. [ ] Run `npm audit fix` for vulnerabilities
3. [ ] Add input validation to controllers

### Short Term (This Month)
1. [ ] Extract god use cases into smaller units
2. [ ] Add unit tests for critical paths
3. [ ] Upgrade outdated dependencies

### Long Term (This Quarter)
1. [ ] Refactor architecture to respect dependency rules
2. [ ] Achieve 70% test coverage
3. [ ] Implement CI/CD pipeline with security scanning

---

**Report generated**: {timestamp}
**Auditor**: skill-security-checklist v1.0
**Confidence**: Overall {high/medium/low}
```

Also return:
- Files created (AUDIT_REPORT.md, raw data files)
- Detection confidence levels for each section
- Any errors or skipped files

## References

- `assets/detect-stack.sh` — Detect languages, frameworks, and dependencies
- `assets/detect-architecture.sh` — Identify architecture patterns (DDD, MVC, Hexagonal, etc.)
- `assets/detect-infrastructure.sh` — Detect Docker, K8s, CI/CD, cloud infrastructure
- `assets/analyze-complexity.sh` — Measure cyclomatic complexity, file/function length, duplication
- `assets/detect-security-risks.sh` — Scan for hardcoded secrets, SQL injection, XSS, insecure deps
- `assets/assess-tech-debt.sh` — Find TODOs, deprecated deps, missing tests, documentation gaps
- `assets/generate-audit-report.sh` — Aggregate all data into a single markdown report
- `references/architecture-patterns.md` — Reference guide for architecture pattern detection
- `references/code-smells.md` — Catalog of code smells and anti-patterns
- `references/complexity-metrics.md` — Thresholds and interpretation for complexity metrics
- `references/security-checklist.md` — Comprehensive security checks and mitigation strategies
- `assets/audit-template.md` — Base template for the final markdown report
