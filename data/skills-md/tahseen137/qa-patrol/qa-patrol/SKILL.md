---
name: qa-patrol
description: >
  Automated QA testing for web apps using local browser automation. Runs entirely on your machine —
  no data leaves, no cloud services, no external servers. Level 1 (smoke tests) needs only a URL.
  Level 2 (auth/payment testing) uses optional env vars for test credentials. Level 3 (static analysis,
  DB checks) optionally reads local files and connects to a user-provided database.
  Supports Supabase/Firebase auth, Stripe payments, React Native Web, Next.js, and SPAs.
---

# QA Patrol

Automated QA testing skill for web applications. Catches bugs that unit tests miss: cross-platform issues, auth state problems, data integrity failures, and integration breakages.

## Security & Privacy

**All tests run locally on your machine. Nothing is sent to external servers. The browser automation uses OpenClaw's built-in browser control — no cloud services involved.**

### Permissions by Level

| Level | What it does | Permissions needed | Env vars needed |
|-------|-------------|-------------------|-----------------|
| **1 — Smoke** | Loads pages, checks for errors | `browser` only | `APP_URL` (or pass `--url`) |
| **2 — Auth/Payments** | Tests sign-in, checkout flows | `browser` only | Test account credentials (see below) |
| **3 — Static Analysis** | Scans local source code for bug patterns | `browser` + `read` | None (uses local `repo_path`) |
| **3 — DB Integrity** | Compares DB values to UI display | `browser` | `DATABASE_URL` |

**The `read` permission is ONLY needed for Level 3 static analysis.** Level 1 and Level 2 tests use browser automation exclusively. If you only run Level 1/2 tests, the skill never accesses local files.

### Environment Variables (all optional)

| Variable | Required | Used by | Purpose |
|----------|----------|---------|---------|
| `APP_URL` | No | Level 1+ | Target app URL (can also use `--url` flag) |
| `ADMIN_EMAIL` | No | Level 2 | Admin test account email |
| `ADMIN_PASSWORD` | No | Level 2 | Admin test account password |
| `FREE_EMAIL` | No | Level 2 | Free-tier test account email |
| `FREE_PASSWORD` | No | Level 2 | Free-tier test account password |
| `PRO_EMAIL` | No | Level 2 | Pro test account email |
| `PRO_PASSWORD` | No | Level 2 | Pro test account password |
| `DATABASE_URL` | No | Level 3 | DB connection for data integrity checks |

**⚠️ Use test credentials only — never supply production passwords or production DATABASE_URL.**

### Secrets Handling
- **NEVER hardcode secrets** in test plans — always use environment variable interpolation: `${env.ADMIN_PASSWORD}`
- Credentials are read from your local environment at runtime
- Test plans in this skill's examples use only `${env.VAR}` placeholders
- The skill does not persist, log, or transmit credentials

### Security Pattern Detection (Not Exploitation)
The `references/bug-patterns.md` file contains regex patterns for **detecting exposed secrets** in codebases (e.g., `sk_live_`, `api_key=`). These are **detection patterns** used to help developers find and fix security issues — they are NOT exploitation tools. This is standard practice in security linters like ESLint, Semgrep, and GitHub's secret scanning.

### No Install Scripts, No Code Files
This is an **instruction-only skill** — it contains no executable code, no install scripts, and no third-party dependencies. The entire security surface is the SKILL.md instructions and OpenClaw's built-in browser/read capabilities.

## Quick Start

### Level 1: Zero-Config Smoke Test
```bash
# Just provide a URL
qa-patrol https://example.com
```

### Level 2: With Auth/Payments
```bash
# Use a test plan template
qa-patrol --plan auth-supabase.yaml --url https://example.com
```

### Level 3: Full Config
```bash
# Custom test plan with data integrity checks
qa-patrol --plan my-app.yaml
```

## Workflow

### 1. Load or Generate Test Plan

If a YAML test plan is provided, load it. Otherwise, generate a basic plan:

```yaml
app:
  url: <provided URL>
  name: <extracted from page title>

tests:
  smoke:
    - name: Homepage loads
      navigate: /
      assert:
        - element_exists: main
        - no_console_errors: true
```

See `assets/templates/` for test plan templates:
- `basic.yaml` - Zero-config smoke test
- `auth-supabase.yaml` - Supabase auth flows
- `payments-stripe.yaml` - Stripe checkout testing
- `full-saas.yaml` - Complete SaaS test plan

### 2. Execute Tests

Run tests in order: smoke → auth → payments → data_integrity → static_analysis.

For each test:
1. Navigate to the target URL
2. Execute steps (click, type, wait)
3. Capture snapshot and console logs
4. Evaluate assertions
5. Record PASS/FAIL/SKIP with evidence

#### Browser Automation Patterns

```python
# Navigate and snapshot
browser(action="navigate", targetUrl="https://example.com/page")
browser(action="snapshot")

# Form interaction
browser(action="act", request={"kind": "click", "ref": "email_input"})
browser(action="act", request={"kind": "type", "ref": "email_input", "text": "user@test.com"})
browser(action="act", request={"kind": "click", "ref": "submit_button"})

# Check console for errors
browser(action="console", level="error")
```

See `references/test-patterns.md` for complete automation patterns.

### 3. Check for Known Bug Patterns

Scan codebase (if accessible) for anti-patterns across **10 categories**:

| Category | Example Patterns | Severity |
|----------|-----------------|----------|
| **Cross-Platform** | `Alert.alert` without `Platform.OS` guard, `Linking.openURL` in Modal | High-Critical |
| **Auth State** | RLS policies blocking authenticated users, session persistence failures | High-Critical |
| **Data Integrity** | UI/DB mismatches, duplicate records, calculation errors | Medium-High |
| **Integration** | Stripe JWT failures, edge function auth issues, webhook errors | Critical |
| **Cache** | Stale cache masking failures, service worker issues | Medium |
| **Environment** | Missing ENV vars, API keys exposed in client code | Critical |
| **Performance** | Poor Core Web Vitals (LCP/CLS/FID), large bundle size, memory leaks | Medium-High |
| **Accessibility** | Missing ARIA labels, poor keyboard nav, low contrast, missing alt text | High |
| **Mobile** | Fixed desktop width, small touch targets, missing viewport meta | High |
| **SEO** | Missing meta tags, broken links, slow TTFB, no structured data | Low-Medium |

See `references/bug-patterns.md` for the full catalog of **39+ patterns**.

### 4. Data Integrity Checks (Level 3)

When `data_integrity` tests are defined:

1. Execute the DB query (requires DB access)
2. Navigate to the UI path
3. Extract the displayed value
4. Compare against query result
5. Flag mismatches with severity based on % difference

### 5. Generate Report

Output a structured report:

```markdown
# QA Report: [App Name]
**Date**: YYYY-MM-DD HH:MM
**URL**: https://example.com
**Confidence**: 87%

## Summary
| Category | Pass | Fail | Skip |
|----------|------|------|------|
| Smoke    | 5    | 0    | 0    |
| Auth     | 3    | 1    | 0    |
| Payments | 0    | 0    | 2    |

## Failures

### [FAIL] Auth: Session persistence after refresh
**Steps**: Sign in → Refresh page → Check auth state
**Expected**: User remains signed in
**Actual**: Redirected to login page
**Evidence**: [screenshot]
**Severity**: High

## Recommendations
1. Fix session persistence (likely cookie/localStorage issue)
2. Add Platform.OS guards to Alert.alert calls
```

See `references/report-format.md` for the complete template.

## Test Plan Reference

### App Configuration

```yaml
app:
  url: https://example.com      # Required: base URL
  name: My App                  # Optional: display name
  stack: expo-web               # expo-web | nextjs | spa | static
```

### Auth Configuration

```yaml
auth:
  provider: supabase            # supabase | firebase | auth0 | custom
  login_path: /auth             # Path to login page
  accounts:
    admin:
      email: admin@test.com
      password: ${ADMIN_PASSWORD}  # Use env vars for secrets
    free:
      email: free@test.com
      password: ${FREE_PASSWORD}
    guest: true                 # Test anonymous/guest mode
```

### Test Types

#### Smoke Tests
```yaml
tests:
  smoke:
    - name: Homepage loads
      navigate: /
      assert:
        - element_exists: main
        - no_console_errors: true
        - no_network_errors: true
    
    - name: Navigation works
      navigate: /
      steps:
        - click: { ref: nav_link }
        - assert: { url_contains: "/target" }
```

#### Auth Tests
```yaml
tests:
  auth:
    - name: Sign in flow
      steps:
        - navigate: /auth
        - type: { ref: email_input, text: "${auth.accounts.free.email}" }
        - type: { ref: password_input, text: "${auth.accounts.free.password}" }
        - click: { ref: sign_in_button }
        - wait: { url_contains: "/home", timeout: 5000 }
        - assert: { element_exists: "user_avatar" }
    
    - name: Sign out flow
      requires: signed_in
      steps:
        - click: { ref: user_menu }
        - click: { ref: sign_out_button }
        - assert: { url_contains: "/auth" }
    
    - name: Session persistence
      requires: signed_in
      steps:
        - navigate: /home
        - refresh: true
        - assert: { element_exists: "user_avatar" }
```

#### Payment Tests
```yaml
tests:
  payments:
    provider: stripe
    tests:
      - name: Checkout creation
        steps:
          - navigate: /pricing
          - click: { ref: pro_plan_button }
          - wait: { url_contains: "checkout.stripe.com", timeout: 10000 }
          - assert: { element_exists: "cardNumber" }
```

#### Data Integrity Tests
```yaml
tests:
  data_integrity:
    - name: Card count matches
      query: "SELECT count(*) FROM cards WHERE country='CA'"
      ui_path: /settings
      ui_selector: "[data-testid='card-count']"
      tolerance: 0  # Exact match required
    
    - name: Points calculation
      query: "SELECT points_rate FROM tiers WHERE name='Gold'"
      ui_path: /calculator
      ui_selector: ".points-display"
      tolerance: 0.01  # 1% tolerance
```

#### Static Analysis
```yaml
tests:
  static_analysis:
    scan_path: ./src
    patterns:
      - name: Alert.alert without Platform guard
        grep: "Alert\\.alert"
        exclude_grep: "Platform\\.OS"
        severity: high
        fix_hint: "Wrap in Platform.OS check or use cross-platform alert"
      
      - name: Hardcoded API keys
        grep: "(sk_live_|pk_live_|api_key.*=.*['\"][a-zA-Z0-9]{20,})"
        severity: critical
```

### Assertions Reference

| Assertion | Description |
|-----------|-------------|
| `element_exists: "ref"` | Element with ref is in DOM |
| `element_visible: "ref"` | Element is visible |
| `text_contains: "string"` | Page contains text |
| `url_contains: "/path"` | URL includes path |
| `no_console_errors: true` | No console.error calls |
| `no_network_errors: true` | No failed network requests |
| `value_equals: { ref, value }` | Input value matches |
| `count_equals: { ref, count }` | Number of matching elements |

### Variable Interpolation

Use `${...}` for dynamic values:
- `${auth.accounts.free.email}` - From test plan
- `${env.API_KEY}` - From environment
- `${captured.user_id}` - From previous step capture

## Confidence Scoring

Calculate confidence based on test coverage and results:

```
base_confidence = 50
per_smoke_pass = +5 (max 20)
per_auth_pass = +8 (max 24)
per_payment_pass = +10 (max 20)
per_data_check_pass = +6 (max 18)
static_analysis_clean = +8
no_critical_failures = +10

final_confidence = min(base + bonuses - penalties, 100)
```

Penalties:
- Critical failure: -20
- High severity failure: -10
- Medium severity failure: -5
- Skipped critical test: -5

## Files

### References
- `references/test-patterns.md` - Browser automation patterns and examples
- `references/bug-patterns.md` - Known bug patterns to detect
- `references/report-format.md` - QA report template

### Templates
- `assets/templates/basic.yaml` - Zero-config smoke test
- `assets/templates/auth-supabase.yaml` - Supabase auth testing
- `assets/templates/payments-stripe.yaml` - Stripe payment testing
- `assets/templates/full-saas.yaml` - Complete SaaS test plan

### Examples
- `assets/examples/rewardly.yaml` - Real-world React Native Web app test plan

## Tips

1. **Start with smoke tests** - Verify basic functionality before auth/payments
2. **Use guest mode first** - Test without auth to establish baseline
3. **Check console early** - Console errors often reveal root causes
4. **Screenshot failures** - Always capture evidence for debugging
5. **Test cache states** - Sign out and clear cache to expose hidden issues
6. **Verify cross-platform** - If React Native Web, test alert/linking patterns
