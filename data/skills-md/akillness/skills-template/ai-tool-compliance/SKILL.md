---
name: ai-tool-compliance
description: Automation skill for designing, verifying, and improving auth, cost, logging, and security compliance based on the internal AI tool mandatory implementation guide (P0/P1). Supports the full lifecycle of RBAC design, Gateway principles, Firestore policy, behavior logs, cost transparency, and the criteria verification system.
compatibility: "Requires python3 (stdlib only), jq, bash, bc, curl, git. PyYAML required only for install.sh (pip install pyyaml). Optional: Notion MCP tool for Notion workspace integration."
allowed-tools: Read Bash Grep Glob
metadata:
  tags: compliance, RBAC, security, cost-tracking, audit-log, gateway, firestore, deploy-gate, P0, quick, full, improve, slash-command
  platforms: Claude, Gemini, Codex, OpenCode
  keyword: compliance
  version: 1.0.0
  source: user-installed skill
---


# ai-tool-compliance - Internal AI Tool Compliance Automation

## When to use this skill

- **Starting a new AI project**: When scaffolding the compliance foundation (RBAC, Gateway, logs, cost tracking) from scratch
- **Pre-deploy P0 full verification**: When automatically evaluating all 13 P0 mandatory requirements as pass/fail and computing a compliance score
- **RBAC design and permission matrix generation**: When defining the 5 roles (Super Admin/Admin/Manager/Viewer/Guest) + granular access control per game/menu/feature unit
- **Auditing existing code for compliance**: When inspecting an existing codebase against the guide and identifying violations
- **Implementing cost transparency**: When building a tracking system for model/token/BQ scan volume/cost per action
- **Designing a behavior log schema**: When designing a comprehensive behavior log recording system (Firestore/BigQuery)
- **Role-based verification workflow**: When configuring the release approval process based on Section 14 (ServiceStability/Engineer/PM/CEO)
- **Building a criteria verification system**: When setting up the Rule Registry + Evidence Collector + Verifier Engine + Risk Scorer + Gatekeeper architecture

---

## Installation

```bash
npx skills add https://github.com/supercent-io/skills-template --skill ai-tool-compliance
```

---

## Quick Reference

| Action | Command | Description |
|--------|---------|-------------|
| Project initialization | `/compliance-init` | Generate RBAC matrix, Gateway boilerplate, log schema, cost tracking interface |
| Quick scan | `/compliance-scan`, `/compliance-quick`, `/quick` | Quick inspection of P0 key items (code pattern-based) |
| Full verification | `/compliance-verify`, `/compliance-full`, `/full` | Full verification of 11 P0 rules + compliance score computation |
| Score check | `/compliance-score` | Display current compliance score (security/auth/cost/logging) |
| Deploy gate | `/compliance-gate` | Green/Yellow/Red verdict + deploy approve/block decision |
| Improvement guide | `/compliance-improve`, `/improve` | Specific fix suggestions per violation + re-verification loop |

### Slash Mode Router

Mode slash commands are mapped as follows.

- `/quick`, `/compliance-quick` -> Quick Scan (`/compliance-scan`)
- `/full`, `/compliance-full` -> Full Verify (`/compliance-verify`)
- `/improve` -> Improve (`/compliance-improve`)

---

## 3 Execution Modes

### 1. Quick Scan (`quick-scan`)

Statically analyzes the codebase to quickly identify potential P0 violations.

**How to run**: `/compliance-scan`, `/compliance-quick`, `/quick` or trigger keywords `compliance scan`, `quick scan`

**What it does**:
- Grep/Glob-based code pattern search
- Detect direct external API calls (whether Gateway is bypassed)
- Detect direct Firestore client access
- Detect hardcoded sensitive data
- Check for missing Guest role

**Output**: List of suspected violations (file path + line number + rule ID)

**Duration**: 1–3 minutes

### 2. Full Verify (`full-verify`)

Fully verifies all 11 P0 rules and computes a quantitative compliance score.

**How to run**: `/compliance-verify`, `/compliance-full`, `/full` or trigger keywords `P0 verification`, `full verify`, `deploy verification`

**What it does**:
- Collect Evidence and evaluate pass/fail for each of the 11 P0 rules
- Compute scores per 4 domains (Security 40pts / Auth 25pts / Cost 20pts / Logging 15pts)
- Calculate total compliance score (out of 100)
- Determine deploy gate grade (Green/Yellow/Red)
- Generate role-based approval checklist

**Output**: Compliance report (`compliance-report.md`)

```
## Compliance Report
- Date: 2026-03-03
- Project: my-ai-tool
- Score: 92/100 (Green)

### Rule Results
| Rule ID | Rule Name | Result | Evidence |
|---------|-----------|--------|----------|
| AUTH-P0-001 | Force Guest for New Signups | PASS | signup.ts:45 role='guest' |
| AUTH-P0-002 | Block Guest Menu/API Access | PASS | middleware.ts:12 guestBlock |
| ... | ... | ... | ... |

### Score Breakdown
- Security: 33/40
- Auth: 25/25
- Cost: 17/20
- Logging: 12/15
- Total: 92/100

### Gate Decision: GREEN - Deploy Approved
```

**Duration**: 5–15 minutes (varies by project size)

### 3. Improve (`improve`)

Provides specific fix guides for violations and runs a re-verification loop.

**How to run**: `/compliance-improve`, `/improve` or trigger keywords `compliance improvement`, `fix violations`

**What it does**:
- Code-level fix suggestions for each FAIL item (file path + before/after code)
- Re-verify the rule after applying the fix
- Track score changes (Before -> After)
- Guide for gradually introducing P1 recommended requirements after passing P0

**Output**: Fix proposal + re-verification results

### Improve Mode Auto-Fix Logic

```
/compliance-improve runs
       |
  1. Load latest verification-run.json
       |
  2. Extract FAIL items (rule_id + evidence)
       |
  3. For each FAIL:
       |
     a. Read violation code from evidence file:line
     b. Derive fix direction from rule.remediation + rule.check_pattern.must_contain
     c. Generate before/after code diff
     d. Apply fix via Write (after user confirmation)
     e. Re-verify only that rule (re-run Grep pattern)
     f. Confirm transition to PASS
       |
  4. Full re-verification (/compliance-verify)
       |
  5. Output Before/After score comparison
       |
  6. If no remaining FAILs → present guide for introducing P1 recommended requirements
```

**Fix application priority**:
1. `must_not_contain` violations (requires immediate removal) → delete the code or replace with server API call
2. `must_contain` unmet (pattern needs to be added) → insert code per the remediation guide
3. Warning (partially met) → apply supplement only to unmet files

---

## P0 Rule Catalog

11 P0 rules based on the internal AI tool mandatory implementation guide v1.1:

| Rule ID | Category | Rule Name | Description | Score |
|---------|----------|-----------|-------------|-------|
| AUTH-P0-001 | Auth | Force Guest for New Signups | Automatically assign role=Guest on signup; elevated roles granted only via invitation | Auth 8 |
| AUTH-P0-002 | Auth | Block Guest Menu/API Access | Do not expose tool name, model name, internal infrastructure, cost, or structure to Guest. Only allow access to permitted menus/APIs | Auth 7 |
| AUTH-P0-003 | Auth | Server-side Final Auth Check | Server-side auth verification middleware required for all API requests. Client-side checks alone are insufficient | Auth 10 |
| SEC-P0-004 | Security | Prohibit Direct Firestore Access | Direct read/write to Firestore from client is forbidden. Only via Cloud Functions is allowed | Security 12 |
| SEC-P0-005 | Security | Enforce External API Gateway | Direct calls to external AI APIs (Gemini, OpenAI, etc.) are forbidden. Must route through internal Gateway (Cloud Functions) | Security 18 |
| SEC-P0-009 | Security | Server-side Sensitive Text Processing | Sensitive raw content (prompts, full responses) is processed server-side only. Only reference values (IDs) are sent to clients | Security 10 |
| COST-P0-006 | Cost | Model Call Cost Log | Must record model, inputTokens, outputTokens, estimatedCost for every AI model call | Cost 10 |
| COST-P0-007 | Cost | BQ Scan Cost Log | Must record bytesProcessed, estimatedCost when executing BigQuery queries | Cost 5 |
| COST-P0-011 | Cost | Cache-first Lookup | Cache lookup required before high-cost API calls. Actual call only on cache miss | Cost 5 |
| LOG-P0-008 | Logging | Mandatory Failed Request Logging | Must log all failed requests (4xx, 5xx, timeout). No omissions allowed | Logging 10 |
| LOG-P0-010 | Logging | Auth Change Audit Log | Record all auth-related events: role changes, permission grants/revocations, invitation sends | Logging 5 |

### Scoring System

| Domain | Max Score | Included Rules |
|--------|-----------|----------------|
| Security | 40 | SEC-P0-004, SEC-P0-005, SEC-P0-009 |
| Auth | 25 | AUTH-P0-001, AUTH-P0-002, AUTH-P0-003 |
| Cost | 20 | COST-P0-006, COST-P0-007, COST-P0-011 |
| Logging | 15 | LOG-P0-008, LOG-P0-010 |
| **Total** | **100** | **11 P0 rules** |

### Per-rule Automatic Verification Logic

Verification for each rule is performed based on the `check_pattern` defined in `rules/p0-catalog.yaml`. The core mechanism is Grep/Glob static analysis.

**Verdict Algorithm (per rule)**:

```
1. Glob(check_targets) → collect target files
2. grep_patterns matching → identify files using that feature
   - 0 matches → N/A (feature not used, no penalty)
3. must_not_contain check (excluding exclude_paths)
   - Match found → immediate FAIL + record evidence
4. must_contain check
   - All satisfied → PASS
   - Partially satisfied → WARNING
   - Not satisfied → FAIL
```

**Key Grep Patterns per Rule**:

| Rule ID | Feature Detection (grep_patterns) | Compliance Check (must_contain) | Violation Detection (must_not_contain) |
|---------|----------------------------------|--------------------------------|---------------------------------------|
| AUTH-P0-001 | `signup\|register\|createUser` | `role.*['"]guest['"]` | `role.*['"]admin['"]` (on signup) |
| AUTH-P0-002 | `guard\|middleware\|authorize` | `guest.*block\|guest.*deny` | -- |
| AUTH-P0-003 | `router\.(get\|post\|put\|delete)` | `auth\|verify\|authenticate` | -- |
| SEC-P0-004 | -- (all targets) | -- | `firebase/firestore\|getDocs\|setDoc` (client paths) |
| SEC-P0-005 | -- (all targets) | -- | `fetch\(['"]https?://(?!localhost)` (client paths) |
| SEC-P0-009 | -- (all targets) | -- | `res\.json\(.*password\|console\.log\(.*token` |
| COST-P0-006 | `openai\|vertexai\|gemini\|anthropic` | `cost\|token\|usage\|billing` | -- |
| COST-P0-007 | `bigquery\|BigQuery\|createQueryJob` | `totalBytesProcessed\|bytesProcessed\|cost` | -- |
| COST-P0-011 | `openai\|vertexai\|gemini\|anthropic` | `cache\|Cache\|redis\|memo` | -- |
| LOG-P0-008 | `catch\|errorHandler\|onError` | `logger\|log\.error\|winston\|pino` | -- |
| LOG-P0-010 | `updateRole\|changeRole\|setRole` | `audit\|auditLog\|eventLog` | -- |

**Detailed schema**: see `rules/p0-catalog.yaml` and the "Judgment Algorithm" section in `REFERENCE.md`

---

## Verification Scenarios (QA)

5 key verification scenarios run in Full Verify mode (`/compliance-verify`). Each scenario groups related P0 rules for end-to-end verification.

| ID | Scenario | Related Rules | Verification Method | Pass Criteria |
|----|---------|---------------|---------------------|---------------|
| SC-001 | **New Signup -> Guest Isolation** | AUTH-P0-001, AUTH-P0-002 | Verify role=guest assignment in signup code + confirm 403 return pattern when Guest calls protected API | PASS when role is guest and access-denied pattern exists for protected API |
| SC-002 | **AI Call -> Via Gateway + Cost Logged** | SEC-P0-005, COST-P0-006, COST-P0-011 | (1) Confirm absence of direct external API calls (2) Confirm routing via Gateway function (3) Confirm cost log fields (model, tokens, cost) recorded (4) Confirm cache lookup logic exists | PASS when Gateway routing + 4 cost log fields recorded + cache layer exists |
| SC-003 | **Firestore Access -> Functions-Only** | SEC-P0-004, AUTH-P0-003 | (1) Detect direct Firestore SDK import in client code (2) Confirm server-side auth verification middleware exists | PASS when 0 direct client access instances + server middleware exists |
| SC-004 | **Failed Requests -> No Log Gaps** | LOG-P0-008, LOG-P0-010 | (1) Confirm log call in error handler (2) Confirm no log gaps in catch blocks (3) Confirm audit log exists for auth change events | PASS when all error handlers call log + auth change audit log exists |
| SC-005 | **Sensitive Data -> Not Exposed to Client** | SEC-P0-009, AUTH-P0-002 | (1) Confirm API responses do not include raw prompts/responses, only reference IDs (2) Confirm Guest responses do not include model name/cost/infrastructure info | PASS when raw content not in response + Guest exposure control confirmed |

### Verification Flow by Scenario

```
SC-001: grep signup/register -> assert role='guest' -> grep guestBlock/guestDeny -> assert exists
SC-002: grep fetch(https://) in client -> assert 0 hits -> grep gateway log -> assert cost fields -> assert cache check
SC-003: grep firebase/firestore in client/ -> assert 0 hits -> grep authMiddleware in functions/ -> assert exists
SC-004: grep catch blocks -> assert logAction in each -> grep roleChange -> assert auditLog
SC-005: grep res.json for raw text -> assert 0 hits -> grep guest response -> assert no model/cost info
```

---

## Role-based Go/No-Go Checkpoints

After the deploy gate verdict, the role's Go/No-Go checkpoints must be cleared based on the grade. **4 roles × 5 items = 20 checkpoints total**.

### Service Stability (5 items)

| # | Checkpoint | Go Condition | No-Go Condition |
|---|-----------|-------------|-----------------|
| 1 | SLA Impact Analysis | Confirmed no impact on existing service availability/response-time SLA | SLA impact unanalyzed or degradation expected |
| 2 | Rollback Procedure | Rollback procedure documented + tested | Rollback procedure not established |
| 3 | Performance Test | Load/stress test completed + within threshold | Performance test not run |
| 4 | Incident Alerts | Incident detection alert channels (Slack/PagerDuty, etc.) configured | Alert channels not configured |
| 5 | Monitoring Dashboard | Dashboard for key metrics (error rate, response time, AI cost) exists | Monitoring absent |

### Engineer (5 items)

| # | Checkpoint | Go Condition | No-Go Condition |
|---|-----------|-------------|-----------------|
| 1 | FAIL Rule Root Cause Analysis | Root cause identified + documented for all FAIL rules | Unidentified items exist |
| 2 | Fix Code Verification | Fixed code accurately reflects the intent of the rule | Fix does not match rule intent |
| 3 | Re-verification Pass | Rule transitions to PASS in re-verification after fix | Re-verification not run or still FAIL |
| 4 | No Regression Impact | Fix confirmed to have no negative impact on other P0 rules | Another rule newly FAILs |
| 5 | Code Review Done | Code review approval completed for fixed code | Code review not completed |

### PM (5 items)

| # | Checkpoint | Go Condition | No-Go Condition |
|---|-----------|-------------|-----------------|
| 1 | User Impact Assessment | User impact of non-compliant items is acceptable | User impact not assessed |
| 2 | Schedule Risk | Fix timeline is within release schedule | Schedule overrun expected |
| 3 | Scope Agreement | Stakeholder agreement completed for scope changes | Agreement not reached |
| 4 | Cost Impact | AI usage cost within approved budget | Budget overrun expected |
| 5 | Communication | Changes shared with relevant teams | Not shared |

### CEO (5 items)

| # | Checkpoint | Go Condition | No-Go Condition |
|---|-----------|-------------|-----------------|
| 1 | Cost Cap | Monthly AI cost within pre-approved budget | Budget cap exceeded |
| 2 | Security Risk | All security P0 passed or exception reason is reasonable | P0 security FAIL + insufficient exception justification |
| 3 | Legal/Regulatory Risk | Data processing complies with applicable laws (privacy laws, etc.) | Legal risks not reviewed |
| 4 | Business Continuity | Business impact is limited if deployment fails | Business disruption risk exists |
| 5 | Final Approval | Final approval when all 4 above are Go | Deferred if even 1 is No-Go |

---

## Report Format

`compliance-report.md`, generated when `/compliance-verify` runs, consists of 6 sections.

### Report Section Structure (6 sections)

```markdown
# Compliance Report

## 1. Summary
- Project name, verification date/time, verification mode (quick-scan / full-verify)
- Total compliance score / 100
- Deploy gate grade (Green / Yellow / Red)
- P0 FAIL count
- Verification duration

## 2. Rule Results
| Rule ID | Category | Rule Name | Result | Score | Evidence |
|---------|----------|-----------|--------|-------|----------|
| AUTH-P0-001 | Auth | Force Guest for New Signups | PASS | 10/10 | signup.ts:45 |
| SEC-P0-005 | Security | Enforce External API Gateway | FAIL | 0/15 | client/api.ts:23 direct fetch |
| ...

## 3. Score Breakdown
| Domain | Score | Max | % |
|--------|-------|-----|---|
| Security | 20 | 40 | 50% |
| Auth | 25 | 25 | 100% |
| Cost | 17 | 20 | 85% |
| Logging | 12 | 15 | 80% |
| **Total** | **79** | **100** | **79%** |

## 4. Failures Detail
For each FAIL item:
- Violation code location (file:line)
- Description of the violation
- Recommended fix (remediation)
- Related verification scenario ID (SC-001–SC-005)

## 5. Gate Decision
- Verdict grade + basis for verdict
- List of required approval roles
- Role-based Go/No-Go checkpoint status (unmet items out of 20 shown)

## 6. Recommendations
- Immediate action: Fix P0 FAILs (file path + fix guide)
- Short-term improvement: Path from Yellow to Green
- Mid-term adoption: Order for introducing P1 recommended requirements
```

### Report Generation Rules

1. **Summary is always first**: Decision-makers must be able to immediately see the score and grade
2. **Evidence required**: Attach code evidence (file:line) to all PASS/FAIL items in Rule Results
3. **Failures Detail contains only FAILs**: PASS items appear only in the Rule Results table
4. **Role mapping in Gate Decision**: Auto-display required approval roles based on grade
5. **Recommendations priority**: Sorted as Immediate > Short-term > Mid-term

---

## Deploy Gate Policy

### Grade Verdict Criteria

| Grade | Score | Condition | Decision |
|-------|-------|-----------|----------|
| **Green** | 90–100 | All P0 PASS + total score ≥ 90 | Auto deploy approved |
| **Yellow** | 75–89 | All P0 PASS + total score 75–89 | Conditional approval (PM review required) |
| **Red** | 0–74 | Total score ≤ 74 **or** any P0 FAIL | Deploy blocked |

### Core Rules

1. **P0 Absolute Rule**: If even one P0 FAILs, the verdict is **Red** regardless of total score. Deploy automatically blocked
2. **Yellow conditional**: Total score passes but not perfect. PM reviews the risk and decides approve/reject
3. **Green auto-approve**: All P0 passed + score ≥ 90 allows deploy without additional approval

### Gate Execution Flow

```
/compliance-verify runs
       |
  Full verification of 11 P0 rules
       |
  Score computed (Security+Auth+Cost+Logging)
       |
  +----+----+----+
  |         |         |
Green     Yellow    Red
  |         |         |
Auto-Approve  PM-Approve  Deploy-Block
  |       Pending   |
  v         |      After Fix
Deploy       v      Re-verify
        PM Review     |
        |    |      v
      Approve  Reject  /compliance-improve
        |    |
        v    v
      Deploy  After Fix
            Re-verify
```

---

## Role-based Approval Process

Based on Section 14 of the internal AI tool mandatory implementation guide. The required approval roles vary by deploy grade.

### Service Stability

**Responsibility**: Verify incident impact, performance degradation, and rollback feasibility

Checklist:
- [ ] Does the new deployment not impact existing service SLAs?
- [ ] Is the rollback procedure documented?
- [ ] Has performance testing (load/stress) been completed?
- [ ] Are incident alert channels configured?

**Approval trigger**: Required for Yellow/Red grade

### Engineer

**Responsibility**: Root cause analysis of failed rules + code-level fix + re-verification

Checklist:
- [ ] Has the cause of all FAIL rules been identified?
- [ ] Does the fixed code accurately reflect the intent of the rule?
- [ ] Has the rule transitioned to PASS in re-verification?
- [ ] Does the fix have no negative impact on other rules?

**Approval trigger**: Required for Red grade (responsible for re-verification after fix)

### PM (Product Manager)

**Responsibility**: User impact, schedule risk, scope change approval

Checklist:
- [ ] Is the impact of non-compliant items on user experience acceptable?
- [ ] Is the schedule impact of fixes acceptable within the overall release timeline?
- [ ] If scope reduction/deferral is needed, has stakeholder agreement been reached?

**Approval trigger**: Required for Yellow grade

### CEO

**Responsibility**: Cost cap, business risk, final approval

Checklist:
- [ ] Is AI usage cost within the pre-approved budget?
- [ ] Is the security risk at an acceptable level for the business?
- [ ] Are legal/regulatory risks identified and managed?

**Approval trigger**: When cost cap is exceeded or when approving a security P0 exception

---

## Project Initialization (`/compliance-init`)

### Generated File Structure

```
project/
├── compliance/
│   ├── rbac-matrix.yaml          # 5-role × game/menu/feature permission matrix
│   ├── rules/
│   │   └── p0-rules.yaml         # 11 P0 rule definitions
│   ├── log-schema.yaml           # Behavior log schema (Firestore/BigQuery)
│   └── cost-tracking.yaml        # Cost tracking field definitions
├── compliance-config.yaml        # Project metadata + verification settings
└── compliance-report.md          # Verification result report (generated on verify run)
```

### Each YAML File Schema

**compliance-config.yaml** (project root):

```yaml
project:
  name: "my-ai-tool"
  type: "web-app"           # web-app | api | mobile-app | library
  tech_stack: ["typescript", "firebase", "next.js"]

verification:
  catalog_path: "compliance/rules/p0-rules.yaml"   # default
  exclude_paths:                                     # paths to exclude from verification
    - "node_modules/**"
    - "dist/**"
    - "**/*.test.ts"
    - "**/*.spec.ts"

scoring:
  domain_weights:            # total = 100
    security: 40
    auth: 25
    cost: 20
    logging: 15

gate:
  green_threshold: 90        # >= 90 = auto approve
  yellow_threshold: 75       # 75-89 = PM review required
  p0_fail_override: true     # Red verdict on P0 FAIL regardless of score
```

**compliance/log-schema.yaml** (behavior log schema):

```yaml
log_schema:
  version: "1.0.0"
  storage:
    primary: "firestore"           # for real-time access
    archive: "bigquery"            # for analytics/audit
    retention:
      hot: 90                      # days (Firestore)
      cold: 365                    # days (BigQuery)

  fields:
    - name: userId
      type: string
      required: true
    - name: action
      type: string
      required: true
      description: "action performed (ai_call, role_change, login, etc.)"
    - name: timestamp
      type: timestamp
      required: true
    - name: model
      type: string
      required: false
      description: "AI model name (gemini-1.5-flash, etc.)"
    - name: inputTokens
      type: number
      required: false
    - name: outputTokens
      type: number
      required: false
    - name: estimatedCost
      type: number
      required: false
      description: "estimated cost in USD"
    - name: status
      type: string
      required: true
      enum: [success, fail, timeout, error]
    - name: errorMessage
      type: string
      required: false
    - name: metadata
      type: map
      required: false
      description: "additional context (bytesProcessed, cacheHit, etc.)"
```

**compliance/cost-tracking.yaml** (cost tracking fields):

```yaml
cost_tracking:
  version: "1.0.0"

  ai_models:
    required_fields:
      - model              # model identifier
      - inputTokens        # input token count
      - outputTokens       # output token count
      - estimatedCost      # estimated cost in USD
    optional_fields:
      - cacheHit           # whether cache was hit
      - latencyMs          # response latency (ms)

  bigquery:
    required_fields:
      - queryId            # query identifier
      - bytesProcessed     # bytes scanned
      - estimatedCost      # estimated cost in USD
    optional_fields:
      - slotMs             # slot usage time
      - cacheHit           # BQ cache hit indicator

  cost_formula:
    gemini_flash: "$0.075 / 1M input tokens, $0.30 / 1M output tokens"
    gemini_pro: "$1.25 / 1M input tokens, $5.00 / 1M output tokens"
    bigquery: "$5.00 / TB scanned"
```

### RBAC Matrix Base Structure

```yaml
# compliance/rbac-matrix.yaml
roles:
  - id: super_admin
    name: Super Admin
    description: Full system administration + role assignment rights
  - id: admin
    name: Admin
    description: Service configuration + user management
  - id: manager
    name: Manager
    description: Team/game-level management
  - id: viewer
    name: Viewer
    description: Read-only access
  - id: guest
    name: Guest
    description: Minimum access (tool name/model name/cost/structure not exposed)

permissions:
  - resource: "dashboard"
    actions:
      super_admin: [read, write, delete, admin]
      admin: [read, write, delete]
      manager: [read, write]
      viewer: [read]
      guest: []  # no access
  # ... expand per game/menu/feature
```

### Gateway Pattern Example

```typescript
// functions/src/gateway/ai-gateway.ts
// Direct external API calls forbidden - must route through this Gateway

import { onCall, HttpsError } from "firebase-functions/v2/https";
import { verifyRole } from "../auth/rbac";
import { logAction } from "../logging/audit";
import { checkCache } from "../cache/cost-cache";

export const callAIModel = onCall(async (request) => {
  // 1. Server-side auth verification (AUTH-P0-003)
  const user = await verifyRole(request.auth, ["admin", "manager"]);

  // 2. Block Guest access (AUTH-P0-002)
  if (user.role === "guest") {
    throw new HttpsError("permission-denied", "Access denied");
  }

  // 3. Cache-first lookup (COST-P0-011)
  const cached = await checkCache(request.data.prompt);
  if (cached) {
    await logAction({
      userId: user.uid,
      action: "ai_call",
      source: "cache",
      cost: 0,
    });
    return { result: cached, fromCache: true };
  }

  // 4. AI call via Gateway (SEC-P0-005)
  const result = await callGeminiViaGateway(request.data.prompt);

  // 5. Record cost log (COST-P0-006)
  await logAction({
    userId: user.uid,
    action: "ai_call",
    model: result.model,
    inputTokens: result.usage.inputTokens,
    outputTokens: result.usage.outputTokens,
    estimatedCost: result.usage.estimatedCost,
  });

  // 6. Sensitive raw content processed server-side only; return reference ID to client (SEC-P0-009)
  const responseRef = await storeResponse(result.text);
  return { responseId: responseRef.id, summary: result.summary };
});
```

<!-- TODO: Designer output supplement pending - visual format and dashboard UI for compliance-report.md -->

---

## Relationship with Other Skills

### Integration with bmad-orchestrator

Where `bmad-orchestrator` manages the full project development phases (Analysis -> Planning -> Solutioning -> Implementation), `ai-tool-compliance` acts as a companion tool that verifies whether each phase's outputs meet compliance requirements.

**Recommended usage order**:
1. `/workflow-init` (bmad) -- establish project structure
2. `/compliance-init` (compliance) -- generate compliance foundation
3. After Phase 3 Architecture completes, `/compliance-scan` -- architecture-level compliance check
4. After Phase 4 Implementation completes, `/compliance-verify` -- full verification + deploy gate verdict

### Relationship with security-best-practices

`security-best-practices` provides general web security patterns (OWASP, HTTPS, XSS, CSRF). `ai-tool-compliance` assumes these as prerequisites and focuses on organization-specific requirements (5-role RBAC, Gateway enforcement, cost transparency, comprehensive behavior logging).

| Item | security-best-practices | ai-tool-compliance |
|------|------------------------|--------------------|
| RBAC | General mention | 5-role + game/menu/feature matrix |
| API Security | Rate Limiting, CORS | Gateway enforcement + cost log |
| Data Protection | XSS, CSRF, SQL Injection | Sensitive content server-side + Firestore policy |
| Logging | Security event logging | Comprehensive behavior log + schema/retention policy |
| Deploy Gate | None | Auto-block based on compliance score |

### Relationship with code-review

Where `code-review` subjectively reviews code quality/readability/security, `ai-tool-compliance` provides a quantitative verdict (pass/fail, out of 100) on "Does it pass the internal AI tool guide?" The `/compliance-scan` result can be used as reference material during code review.

### Relationship with workflow-automation

Where `workflow-automation` provides general CI/CD patterns (npm scripts, Makefile, GitHub Actions), `ai-tool-compliance` provides the domain-specific verification step inserted into that pipeline.

### scripts/ Directory — Detailed Implementation

#### install.sh -- Skill installation and initialization

```bash
bash scripts/install.sh [options]
  --dry-run        preview without making changes
  --skip-checks    skip dependency checks
```

What it does:
1. Dependency check (yq, jq -- optional; falls back to default parsing if absent)
2. Apply chmod +x to all scripts/*.sh
3. Validate YAML syntax of rules/p0-catalog.yaml
4. Print installation summary

#### verify.sh -- Full P0 rule verification

```bash
bash scripts/verify.sh [--rule RULE_ID] [--output JSON_PATH]
```

What it does:
1. Parse `rules/p0-catalog.yaml` (yq or grep-based)
2. For each rule:
   - Collect target files via `check_targets` Glob
   - Detect feature usage via `grep_patterns` (N/A if not used)
   - Detect `must_not_contain` violations (excluding exclude_paths)
   - Verify `must_contain` compliance
   - Determine Pass/Fail/Warning/N/A + collect evidence
3. Output results in `templates/verification-run.json` format
4. Print summary table to console

#### score.sh -- Compliance score computation

```bash
bash scripts/score.sh [--input VERIFY_JSON] [--verbose]
```

What it does:
1. Load verify.sh result JSON (or run verify.sh directly)
2. Calculate scores by domain:
   - Pass = 100% of score, Warning = 50%, Fail = 0%, N/A = excluded from denominator
   - Security: sum of SEC rule scores / Security max (35)
   - Auth: sum of AUTH rule scores / Auth max (30)
   - Cost: sum of COST rule scores / Cost max (20)
   - Logging: sum of LOG rule scores / Logging max (15)
3. Compute total score (out of 100)
4. Render `templates/risk-score-report.md`
5. Generate `templates/remediation-task.json` (per FAIL item)

#### gate.sh -- Deploy gate check

```bash
bash scripts/gate.sh
# exit 0 = Green (deploy approved)
# exit 1 = Red (deploy blocked)
# exit 2 = Yellow (conditional -- PM review required)
```

What it does:
1. Run verify.sh + score.sh sequentially
2. Check for P0 FAIL existence
   - If any exist → Red (exit 1)
3. Determine grade based on total score
   - 90+ → Green (exit 0)
   - 75–89 → Yellow (exit 2)
   - ≤ 74 → Red (exit 1)
4. Print grade + score + list of items requiring fixes to console

**CI/CD integration example (GitHub Actions)**:

```yaml
# .github/workflows/compliance-gate.yml
name: Compliance Gate
on: [pull_request]
jobs:
  compliance:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run compliance gate
        run: bash .agent-skills/ai-tool-compliance/scripts/gate.sh
```
<!-- TODO: System output supplement pending - GitHub Actions workflow integration YAML -->

---

## P1 Recommended Requirements (Gradual Adoption)

Items recommended for gradual adoption after passing all P0 rules:

| Domain | Requirement | Description |
|--------|-------------|-------------|
| Domain Management | Allowed domain whitelist | Restrict external domains callable by AI Gateway |
| Usage Statistics | Per-user/team usage aggregation | Daily/weekly/monthly usage dashboard |
| Cost Control | Budget cap alerts | Alert when cost threshold exceeded per team/project |
| Log Retention | Log retention policy | 90-day Hot / 365-day Cold / delete thereafter |

### P1 v1.1 Rule Catalog (Extended)

| Rule ID | Domain | Check Type | Key Criteria | Score |
|---------|--------|-----------|--------------|-------|
| P1-DOM-001 | Domain Management | static_analysis | Domain CRUD history + `createdAt/updatedAt/status/owner` metadata | 7 |
| P1-STAT-002 | Statistics | api_test | User/model/period/game filter statistics + cost aggregation freshness (<1h) | 6 |
| P1-COST-003 | Cost Control | config_check | 80% budget warning + 100% block (429/403) + reset cycle | 6 |
| P1-LOG-004 | Logging | config_check | Log schema validation + 6+ month retention + search/Export | 6 |

### Standard Columns for Notion Table Sorting (Additional)

| Column | Description | Source |
|--------|-------------|--------|
| Rule ID | Rule identifier | rules/p1-catalog.yaml |
| Category/Domain | Compliance domain | rules/p1-catalog.yaml |
| Check Type | Verification method (static/api/config/log) | rules/*-catalog.yaml |
| Pass/Fail Condition | Verdict criteria | rules/*-catalog.yaml |
| Score Impact | Weight | rules/*-catalog.yaml |
| Evidence | File:line or config reference | verify result JSON |
| Owner Role | Role responsible for action | compliance-report / role checklist |
| Action Queue | Improvement items within 1 week | remediation-task / report |

### Criteria Verification System Design (Additional)

| Component | Responsibility | Output |
|-----------|---------------|--------|
| Rule Registry | P0/P1 catalog version management and load policy | `rules/catalog.json`, `rules/catalog-p1.json`, `rules/catalog-all.json` |
| Evidence Collector | Code/config/API evidence collection and normalization | evidence/violations from `verify.sh` output |
| Verifier Engine | Per-rule PASS/FAIL/WARNING/NA verdict | `/tmp/compliance-verify.json` |
| Risk Scorer | Compute P0 Gate Score + P1 Maturity Score | `/tmp/compliance-score.json` |
| Gatekeeper | Separate deploy block (P0) and recommendation (P1) decisions | `gate.sh` exit code + gate summary |

### Operating Modes (Additional, preserving existing flow)

| Mode | Command | Behavior |
|------|---------|----------|
| P0 Default | `bash scripts/verify.sh .` | Verify P0 rules only (default, backward-compatible) |
| P0+P1 Extended | `bash scripts/verify.sh . --include-p1` | P0 verification + P1 recommended rules simultaneously |
| Gate Verdict | `bash scripts/gate.sh --score-file ...` | Deploy verdict based on P0; P1 tracks maturity/improvement |

---

## Constraints

### Mandatory Rules (MUST)

1. **P0 Absolute Principle**: All 11 P0 rules are verified without exception. Partial verification is not allowed
2. **Server final verification**: All auth decisions are made server-side. Client-side checks alone cannot result in PASS
3. **Gateway enforcement**: Any direct external AI API call discovered results in unconditional FAIL. No bypass allowed
4. **Guest default**: If a role other than Guest is assigned on signup, FAIL
5. **Evidence-based verdict**: All pass/fail verdicts must include code evidence (file path + line number)

### Prohibited Actions (MUST NOT)

1. **P0 exception abuse**: P0 exceptions are never allowed without CEO approval
2. **Score manipulation**: PASS verdict without Evidence is forbidden
3. **Gateway bypass**: Direct external API calls are not allowed for any reason including "testing purposes"
4. **Selective logging**: Logging only successful requests while omitting failed requests is not allowed

---

## Best practices

1. **Shift Left**: At project start, generate the foundation with `/compliance-init` before implementing business logic
2. **Gradual adoption**: Adopt in order: pass all P0 first -> then P1. Do not start with P1
3. **Re-verification loop**: After fixing violations, always re-run `/compliance-verify` to confirm score changes
4. **BMAD integration**: Adopt running compliance-verify after bmad-orchestrator Phase 4 as the standard workflow
5. **CI/CD integration**: Automate by adding a compliance-gate step to GitHub Actions

---

## References

- Internal AI Tool Mandatory Implementation Guide v1.1 (Notion)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Firebase Security Rules](https://firebase.google.com/docs/rules)
- [Cloud Functions for Firebase](https://firebase.google.com/docs/functions)

## Metadata

### Version
- **Current version**: 1.0.0
- **Last updated**: 2026-03-03
- **Compatible platforms**: Claude, Gemini, Codex, OpenCode

### Related Skills
- [bmad-orchestrator](../bmad-orchestrator/SKILL.md): Development phase orchestration
- [security-best-practices](../security-best-practices/SKILL.md): General web security patterns
- [code-review](../code-review/SKILL.md): Code quality/security review
- [workflow-automation](../workflow-automation/SKILL.md): CI/CD automation patterns
- [authentication-setup](../authentication-setup/SKILL.md): Authentication/authorization system setup
- [firebase-ai-logic](../firebase-ai-logic/SKILL.md): Firebase AI integration

### Tags
`#compliance` `#RBAC` `#security` `#cost-tracking` `#audit-log` `#gateway` `#firestore` `#deploy-gate` `#P0` `#AI-tool`
