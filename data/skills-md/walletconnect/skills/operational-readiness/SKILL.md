---
name: operational-readiness
description: |
  Operational Readiness Checklist for Reown services. Use when service owners ask to: check production readiness, validate a service before launch, run operational readiness review, audit service compliance, check if service is ready for production, or validate infrastructure/security posture.

  Triggers: "operational readiness", "production readiness", "launch checklist", "service review", "pre-launch audit", "ORC", "is my service ready", "check my service", "readiness review"
---

# Operational Readiness Checklist

Comprehensive checklist to validate services before production launch. Analyzes codebase + asks interactive questions for items that cannot be detected from code.

## Workflow Overview

1. **Gather context** - Identify service type, tech stack, and traffic expectations
2. **Analyze codebase** - Scan for CI/CD configs, infrastructure code, security patterns
3. **Interactive verification** - Ask about items that cannot be detected from code
4. **Generate report** - Produce checklist report with priorities and remediation guidance

## Step 1: Gather Context

Ask the user these questions using `AskUserQuestion`:

**Service Classification:**
- Service type: Backend API, Frontend/Web App, Infrastructure/Platform, or Hybrid
- Expected traffic: <100 req/min (low), 100-1000 req/min (medium), >1000 req/min (high)
- Data handling: Stores user data (yes/no), Processes PII (yes/no)
- Public-facing: Yes/No
- Has email functionality: Yes/No
- Uses database: Yes/No (if yes, which: PostgreSQL, Supabase, DynamoDB, etc.)

**Tech Stack Detection:**
Auto-detect from files:
- `Cargo.toml` → Rust service
- `package.json` → Node.js/TypeScript
- `*.tf` or `*.tfvars` → Terraform
- `cdk.json` or `*.cdk.ts` → AWS CDK
- `.github/workflows/*.yml` → GitHub Actions CI/CD
- `next.config.js` → Next.js frontend
- `Dockerfile` → Containerized service

## Step 2: Codebase Analysis

Analyze the codebase for evidence of checklist items. Use Glob and Grep to find:

**CI/CD Detection:**
```
.github/workflows/*.yml - GitHub Actions
Cargo.toml + [profile.release] - Rust build config
jest.config.* / vitest.config.* - Test configuration
*.tf - Terraform files
cdk.json - CDK configuration
```

**Security Detection:**
```
**/security*.yml - Security scanning workflows
dependabot.yml - Dependency updates
CODEOWNERS - Code ownership
*.lock files - Dependency locking
```

**Observability Detection:**
```
**/tracing*.rs or opentelemetry* - Distributed tracing
sentry.* or @sentry/* - Error tracking
prometheus* or metrics* - Metrics collection
**/logging*.* or log4* or tracing* - Logging config
```

**Infrastructure Detection:**
```
**/autoscaling* in .tf files - Autoscaling config
**/secretsmanager* or **/ssm* - Secrets management
health* endpoints in code - Health checks
```

## Step 3: Interactive Verification

For items that cannot be detected from code, ask yes/no questions. Group questions by category to avoid overwhelming the user.

## Step 4: Generate Report

Output format:

```markdown
# Operational Readiness Report: [Service Name]

**Service Type:** [Backend API / Frontend / Infrastructure]
**Tech Stack:** [Detected stack]
**Generated:** [Date]

## Summary
- **Overall Readiness:** [X/Y items passing] ([Z%])
- **Launch Blockers (P0):** [count]
- **High Priority (P1):** [count]
- **Medium Priority (P2):** [count]
- **Low Priority (P3):** [count]

## Observability
| Item | Status | Priority | Notes |
|------|--------|----------|-------|
| ... | ✅/❌/⚠️ | P0-P3 | ... |

[Repeat for each category]

## Remediation Summary
[List failing items with links to remediation guidance]
```

---

## Checklist Items by Category

### Observability (O11Y)

| Item | Priority | Applies To | Detection Method |
|------|----------|------------|------------------|
| Alarmable top-level metric OR Canary (OpsGenie integrated) | P0 | High traffic (>100 req/min) | Ask |
| Canary coverage (if <100 req/min) | P0 | Low traffic | Ask |
| DB/Queue monitoring (CPU/Disk/Memory) | P1 | Services with DB/Queue | Ask |
| Logging configured and viewable | P1 | All | Grep for logging config |
| Audit/security log retention (min 1 year for SOC 2 Type 2) | P1 | All | Ask |
| Distributed tracing (OpenTelemetry/Jaeger) | P2 | Backend services | Grep for otel/tracing |
| Sentry instrumentation | P1 | Frontend only | Grep for @sentry |
| status.reown.com integration | P3 | Public-facing | Ask |

> **Note on log retention scope:** The 1-year minimum retention applies specifically to **audit/security event logs** — authentication attempts, authorization decisions, admin actions, data access events, and configuration changes. General application logs and error tracking (e.g. Sentry) are not subject to this requirement. This aligns with SOC 2 Type 2 audit trail requirements.

**Remediation:** See [references/remediation-o11y.md](references/remediation-o11y.md)

---

### CI/CD & Testing

| Item | Priority | Applies To | Detection Method |
|------|----------|------------|------------------|
| CI runs unit/functional tests (>80% critical path coverage) | P0 | All | Check workflow files |
| CD runs integration/e2e tests | P1 | All | Check workflow files |
| Load testing performed | P1 | High traffic / user-facing | Ask |
| Rollback procedure documented and tested | P1 | All | Ask |
| Post-deploy health checks | P2 | All | Check workflow files |

**Remediation:** See [references/remediation-cicd.md](references/remediation-cicd.md)

---

### Primitives (Infrastructure)

| Item | Priority | Applies To | Detection Method |
|------|----------|------------|------------------|
| Runbook documented (failure modes, troubleshooting, escalation) | P0 | All | Ask |
| Infrastructure as code (Terraform/CDK) | P0 | All | Check for .tf or cdk files |
| Autoscaling configured | P1 | Backend services | Grep .tf for autoscaling |
| Healthcheck endpoint (memory, filesystem, dependencies) | P1 | All | Grep for /health endpoint |
| Multi-AZ deployment (2+ pods/instances) | P1 | All | Ask |
| Secrets management (AWS SM, Vault) - no secrets in code | P0 | All | Grep for hardcoded secrets, check .tf |
| Configuration management (env separation) | P2 | All | Check for env-specific configs |
| Data Lake integration | P3 | Analytics needs | Ask |

**Remediation:** See [references/remediation-primitives.md](references/remediation-primitives.md)

---

### Security

| Item | Priority | Applies To | Detection Method |
|------|----------|------------|------------------|
| OWASP Top 10 2025 validation | P0 | All | Ask |
| Secure design review (threat modeling) | P1 | All | Ask |
| Dependency scanning enabled + SBOM | P1 | All | Check for dependabot, snyk |
| Software/data integrity (code signing, CI/CD security) | P2 | All | Ask |
| Fail-secure exception handling | P1 | All | Code review |
| Service-to-service auth (mTLS, JWT, API keys) | P1 | Backend with internal APIs | Ask |
| Clickjacking headers (X-Frame-Options, CSP) | P1 | Frontend only | Grep for security headers |
| SPF records | P2 | Services with email | Ask |
| DKIM records | P2 | Services with email | Ask |
| RLS policies (Supabase/DB) | P0 | Services with Supabase | Ask |
| Rate limiting | P1 | Public APIs | Grep for rate limit config |
| DDoS protection (Cloudflare/AWS Shield) | P1 | Public-facing | Ask |
| API authentication | P1 | Public APIs | Grep for auth middleware |
| Audit logging (auth, admin, data access) | P2 | All | Grep for audit log |

**Remediation:** See [references/remediation-security.md](references/remediation-security.md)

---

### 3rd Party Services

| Item | Priority | Applies To | Detection Method |
|------|----------|------------|------------------|
| Metrics integration for 3rd parties | P2 | Services using 3rd parties | Ask |
| Status page integration (Slack channel minimum) | P2 | Services using 3rd parties | Ask |
| RPC rate limits configured | P1 | Services using RPCs | Ask |

**Remediation:** See [references/remediation-dependencies.md](references/remediation-dependencies.md)

---

### Service Dependencies

| Item | Priority | Applies To | Detection Method |
|------|----------|------------|------------------|
| Upstream dependencies documented | P1 | All | Ask |
| Downstream dependencies documented | P1 | All | Ask |
| Dependency health in service health endpoint | P2 | All | Code review |
| Fallback behavior for non-critical deps | P2 | All | Ask |

**Remediation:** See [references/remediation-dependencies.md](references/remediation-dependencies.md)

---

### Data Retention & Privacy

| Item | Priority | Applies To | Detection Method |
|------|----------|------------|------------------|
| Data retention policy defined | P1 | Services with persistent data | Ask |
| GDPR: Personal data identified | P1 | Services handling user data | Ask |
| GDPR: DSAR process defined | P1 | Services handling user data | Ask |
| GDPR: Right to be forgotten process | P1 | Services handling user data | Ask |
| Privacy policy updated | P2 | User-facing services | Ask |
| DPAs with third-party processors | P2 | Services sharing data | Ask |

**Remediation:** See [references/remediation-privacy.md](references/remediation-privacy.md)

---

### Efficiency & Frugality

| Item | Priority | Applies To | Detection Method |
|------|----------|------------|------------------|
| Resource-efficient implementation | P2 | All | Code review |
| Cost scaling model documented | P2 | All | Ask |
| Spend caps / usage alerts configured | P2 | All | Ask |
| FinOps review completed | P3 | All | Ask |

**Remediation:** See [references/remediation-efficiency.md](references/remediation-efficiency.md)

---

## Priority Definitions

| Priority | Meaning | Action Required |
|----------|---------|-----------------|
| **P0** | Launch blocker | Must fix before production |
| **P1** | High priority | Fix within current sprint |
| **P2** | Medium priority | Fix within quarter |
| **P3** | Nice to have | Address when convenient |

## Status Indicators

- ✅ **Pass** - Item verified as compliant
- ❌ **Fail** - Item not compliant, needs remediation
- ⚠️ **Partial** - Partially compliant, improvements needed
- ➖ **N/A** - Not applicable to this service type
