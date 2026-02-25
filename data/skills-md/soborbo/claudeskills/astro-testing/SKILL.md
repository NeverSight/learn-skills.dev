---
name: astro-testing
description: Testing and QA gate for Astro lead gen sites. Manual + E2E + A11y + Performance. FAIL = no deploy.
---

# Astro Testing Skill

**No testing = No deploy. Period.**

## Purpose

QA gate before deployment. Blocking tests must pass.

## Output

```yaml
test_verdict: PASS | WARN | FAIL
blocking_issues: []
warnings: []
```

## Blocking vs Non-Blocking Tests

### Blocking (FAIL if any fails)

| Test | Category |
|------|----------|
| Form submits successfully | Critical |
| Thank you page displays | Critical |
| Email received (business) | Data |
| Confirmation email sent | Data |
| Lead saved in system | Data |
| Mobile menu works | UX |
| Phone link works | UX |
| Homepage loads | Core |
| 404 page exists | Core |
| Lighthouse ≥90 | Performance |

### Non-Blocking (WARN only)

| Test | Category |
|------|----------|
| Animation smoothness | Polish |
| Minor CLS (<0.1) | Performance |
| Desktop hover states | UX |
| Print stylesheet | Accessibility |

## Data Integrity Tests (Critical)

```yaml
data_integrity:
  - form_submitted: true
  - lead_saved: true
  - business_email_sent: true
  - customer_email_sent: true
  - analytics_event_fired: true
```

**Form shows success but data missing = FAIL.**

## Negative Tests (False Positive Guard)

| Test | Expected |
|------|----------|
| Submit empty form | Error, no submit |
| Invalid email format | Validation error |
| Honeypot filled | Silent reject |
| Missing privacy consent | Blocked |
| SQL injection attempt | Sanitized |

**Negative test passes incorrectly = FAIL.**

## Browser Coverage

```yaml
browser_matrix:
  required: [mobile_safari, mobile_chrome, desktop_chrome, desktop_safari]
  optional: [firefox, edge, samsung_internet]
```

**Missing required browser = FAIL.**

## Accessibility Thresholds

| Severity | Max Allowed | Result |
|----------|-------------|--------|
| Critical | 0 | FAIL |
| Serious | 0 | FAIL |
| Moderate | 2 | WARN |
| Minor | 5 | WARN |

## Performance Thresholds

| Metric | Threshold | Result |
|--------|-----------|--------|
| Lighthouse (all) | ≥90 | FAIL if below |
| LCP | <2.5s | WARN if above |
| CLS | <0.1 | WARN if above |
| Total JS | <100KB | WARN if above |

## Critical Path Tests (All 10 Required)

| # | Test |
|---|------|
| 1 | Homepage loads |
| 2 | Primary CTA works |
| 3 | Form visible |
| 4 | Form submits |
| 5 | Thank you displays |
| 6 | Business email received |
| 7 | Customer email sent |
| 8 | Phone link works |
| 9 | Mobile menu works |
| 10 | 404 page exists |

**Any fail = FAIL.**

## Manual Testing Summary

| Device | Key Checks |
|--------|------------|
| Mobile (375px) | Menu, form, keyboard, validation, 44px buttons, no h-scroll |
| Desktop (1440px) | Header, grid, hover, focus, tab order |

**Full checklists → [references/checklists.md](references/checklists.md)**

## Test Verdict

| Condition | Verdict |
|-----------|---------|
| Any blocking test fails | FAIL |
| Data integrity fail | FAIL |
| Required browser missing | FAIL |
| Lighthouse <90 | FAIL |
| Critical/serious a11y | FAIL |
| Negative test passes incorrectly | FAIL |
| Non-blocking issue | WARN |
| Moderate a11y (≤2) | WARN |
| All pass | PASS |

## Deployment Gate

```yaml
deployment_gate:
  block_on_fail: true
  require_manual_confirm: true
```

**FAIL → deploy blocked. No exceptions.**

## FAIL States

| Condition |
|-----------|
| Any critical path fails |
| Form success but no data |
| Email not received |
| Required browser not tested |
| Lighthouse <90 |
| Critical/serious a11y |

## WARN States

| Condition |
|-----------|
| Non-blocking test fails |
| Moderate a11y ≤2 |
| LCP >2.5s |
| CLS >0.1 |

## References

- [playwright-tests.md](references/playwright-tests.md) — E2E code
- [checklists.md](references/checklists.md) — Manual checklists

## Definition of Done

- [ ] 10 critical paths pass
- [ ] Data integrity verified
- [ ] Negative tests verified
- [ ] Required browsers tested
- [ ] Lighthouse ≥90 all
- [ ] A11y thresholds met
- [ ] Mobile manual test done
- [ ] Desktop manual test done
- [ ] test_verdict = PASS
