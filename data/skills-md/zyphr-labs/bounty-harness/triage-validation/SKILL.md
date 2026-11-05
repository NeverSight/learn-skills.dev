---
name: triage-validation
description: Finding validation before writing any report — 7-Question Gate (all 7 questions), 4 pre-submission gates, always-rejected list, conditionally-valid chain table, CVSS 3.1 quick reference, severity decision guide, report title formula, 60-second pre-submit checklist. Use BEFORE writing any report. One wrong answer = kill the finding and move on. Saves N/A ratio.
---

# TRIAGE & VALIDATION

## Overview

One wrong answer = STOP. Kill it. Move on.

> "N/A hurts your validity ratio. Informative is neutral. Only submit what passes all 7 questions."

This skill is a pre-report quality gate. Run it on every candidate finding before
spending time on a report: the 7-Question Gate disqualifies weak leads in minutes,
the 4 pre-submission gates catch everything else, and the never-submit list stops
known-invalid bug classes from ever reaching a report. The conditionally-valid
table tells you which findings are only reportable with a proven chain.

- Workflow `run-gate` walks the 7-Question Gate and the 4 pre-submission gates.
- Workflow `check-never-submit` matches a finding description against the
  always-rejected list and the common N/A kill signals.
- Script `scripts/chain_validity.py` checks a candidate finding against the
  conditionally-valid chain-required table.

## Quick Reference

### The 7-Question Gate

Ask IN ORDER. One wrong answer = STOP immediately.

**Q1: Can an attacker use this RIGHT NOW, step by step?**
Complete this template:
```
1. Setup:   I need [own account / another user's ID / no account]
2. Request: [exact HTTP method, URL, headers, body — copy-paste ready]
3. Result:  I can [read / modify / delete] [exact data shown in response]
4. Impact:  The real-world consequence is [account takeover / PII read / money stolen]
5. Cost:    Time: [X minutes], Capital: [$0 / $X subscription required]
```
**If you CANNOT write step 2 as a real HTTP request → KILL IT.**

**Q2: Is the impact on the program's accepted impact list?**
Go to the program page. Find "Vulnerability Types" or "Out of Scope."
- **Critical**: Any-user ATO without interaction, RCE, SQLi with data exfil, admin auth bypass
- **High**: Mass PII exfil, privilege escalation, internal SSRF with data, stored XSS all users
- **Medium**: IDOR on specific user non-critical data, XSS on sensitive page requiring click
- **Low**: Non-sensitive info disclosure, clickjacking with PoC
**If your bug maps to a listed exclusion → KILL IT.**

**Q3: Is the root cause in an in-scope asset?**
- Vulnerable domain is on the in-scope list (not `*.internal.target.com`)
- It's a production asset (not staging/dev unless explicitly in scope)
- It's not a third-party service the company just uses (Stripe, Salesforce, Google Auth)
**If out-of-scope → KILL IT.**

**Q4: Does it require privileged access that an attacker can't realistically get?**
- "Admin can do X" = centralization risk = **KILL IT** (on 99% of programs)
- "Non-admin can do X that only admin should do" = valid
- "Requires physical access / MFA device" = usually invalid
- "Requires compromised victim account to work" = questionable, low severity at best

**Q5: Is this already known or accepted behavior?**
1. Program's disclosed reports: Ctrl+F endpoint name + bug class
2. GitHub issues on target repo: `is:issue label:security ENDPOINT_NAME`
3. Changelog — does it mention this behavior?
4. API docs / design docs — is it documented as intended?
**If acknowledged/design decision → KILL IT.**

**Q6: Can you prove impact beyond "technically possible"?**
- XSS → show actual cookie theft or session hijack, not just `alert(1)`
- SSRF → hit an internal endpoint that returns data, not just DNS ping
- SQLi → show actual data exfil from a real table, not just error message
- IDOR → show actual other-user's data in response, not just a 200 status code
**If you can only show "technically possible" → DOWNGRADE severity, not kill.**

**Q7: Is this a known-invalid bug class?**
Check the NEVER SUBMIT list below. If it's on this list without a chain → **KILL IT.**

### Q8: Identity check — which session found this, and does it survive?

For any finding made under an authenticated hunt, record the answer to each:
```
1. Session ID:        [12-char BBHUNT_SESSION_ID hash from audit.jsonl]
2. Identity:          [low-priv user A / high-priv user B / API key / etc.]
3. Anonymous repro:   Does the same request work with NO auth header?
4. Cross-identity:    Does it work under session B with the same data scope?
5. Stale-cred repro:  Does a logged-out / expired session still get the data?
```
- **IDOR / BOLA**: must work with session A reading session B's data — if it only
  works with no auth, that's "missing auth" not IDOR (different bug, different severity).
- **Priv-esc**: must work with low-priv session reading high-priv data — if both
  sessions can already see it, no bug.
- **Auth bypass**: must work *without* a valid session — if it stops working when
  you log out, you've found a permissions issue, not a bypass.
- If you cannot answer the identity questions, treat the finding as unproven.
  Blank answers auto-fail on auth-related findings.

### 4 Pre-Submission Gates

Run in sequence. ALL 4 must PASS.

**Gate 0: Reality Check (30 seconds)**
```
[ ] Bug is REAL — confirmed with actual HTTP requests, not code reading alone
[ ] Bug is IN SCOPE — checked program scope page explicitly
[ ] Reproducible from scratch — can reproduce starting from fresh session
[ ] Evidence ready — screenshot, response body, or video
```

**Gate 1: Impact Validation (2 minutes)**
```
[ ] Can answer: "What can attacker DO that they couldn't before?"
[ ] Answer is more than "see non-sensitive data" (unless program pays for info disclosure)
[ ] Real victim: another user's data, company's data, financial loss
[ ] Not relying on victim doing something unlikely
```

**Gate 2: Deduplication Check (5 minutes)**
```
[ ] Searched HackerOne Hacktivity for this program + similar bug title/endpoint
[ ] Searched GitHub issues for target repo
[ ] Read most recent 5 disclosed reports for this program
[ ] Not a "known issue" in their changelog or public docs
[ ] Google: "TARGET_NAME ENDPOINT_NAME bug bounty"
```

**Gate 3: Report Quality (10 minutes)**
```
[ ] Title: [Bug Class] in [Endpoint] allows [actor] to [impact]
[ ] Steps to Reproduce: copy-pasteable HTTP request
[ ] Evidence: screenshot/video of actual impact (not just 200 status)
[ ] Severity: matches CVSS 3.1 score AND program's severity definitions
[ ] Remediation: 1-2 sentences of concrete fix
[ ] NEVER used "could potentially" or "may allow"
```

## Workflow Selection

| Situation | Workflow |
|---|---|
| New candidate finding before any report work | `run-gate` |
| Finding description drafted, check against always-rejected list | `check-never-submit` |
| Finding matches a "chain required" class | `check-never-submit` output + `scripts/chain_validity.py` |
| All gates passed, time to write the report | hand off to `reporting` skill |

## Available Workflows

### run-gate
Runs the 7-Question Gate and the 4 pre-submission gates against a finding
directory (`FINDING_DIR` must contain at least `description.txt` and ideally
`request.txt` / `response.txt`). Writes a gate result markdown report.

Command (via `bin/bb-run triage-validation run-gate`):
```
mkdir -p $OUTDIR/triage && \
python3 .claude/skills/triage-validation/scripts/triage_gate.py --finding-dir "${FINDING_DIR:?Set FINDING_DIR}" --output $OUTDIR/triage/gate_result.md
```
Outputs: `$OUTDIR/triage/gate_result.md`. Safety tier: passive.

### check-never-submit
Matches the finding description and evidence filenames against the NEVER SUBMIT
list and the common N/A kill signals, and prints which rules the finding
violates (each hit = kill the finding or build the required chain).

Command (via `bin/bb-run triage-validation check-never-submit`):
```
mkdir -p $OUTDIR/triage && \
python3 .claude/skills/triage-validation/scripts/never_submit_check.py --finding-dir "${FINDING_DIR:?Set FINDING_DIR}" --output $OUTDIR/triage/never_submit.md
```
Outputs: `$OUTDIR/triage/never_submit.md`. Safety tier: passive.

## Evidence Required

| Artifact | File |
|---|---|
| Raw HTTP request used to reproduce | `evidence/<finding>/request.txt` |
| Response showing impact | `evidence/<finding>/response.txt` |
| Identity/session answers (auth findings) | gate result markdown |
| Chain PoC (conditionally-valid classes) | `evidence/<finding>/poc.sh` |
| Gate result + never-submit verdict | `$OUTDIR/triage/*.md` |

## References

- Full rules: `references/shuvonsec-rules/hunting.md` and `references/shuvonsec-rules/reporting.md`
- CVSS 3.1 scoring workflow: `reporting` skill (`cvss-score`)
- Never-submit source list: `scripts/never_submit_check.py` + runbook `runbooks/04-never-submit.md`
- Conditionally-valid chain table: `scripts/chain_validity.py`
- Redaction policy: gate reports may quote requests with cookies/tokens —
  keep them local-only under `$OUTDIR` and redact before committing.
