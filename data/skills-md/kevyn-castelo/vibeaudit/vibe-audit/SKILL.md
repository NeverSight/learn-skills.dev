---
name: vibe-audit
description: Audits a codebase for the five security failures that AI-generated code leaves behind most often — Supabase/Firebase tables without Row Level Security, authorization decided in the frontend, API routes that fetch by ID without checking ownership (IDOR/BOLA), API keys and secrets exposed in the bundle or Git history, and unvalidated user input (XSS, unrestricted upload, no rate limit). Use this skill whenever the user asks to review, audit, harden, or "check the security of" an application — and especially before any deploy, launch, or "is this safe to ship?" question. Also use it when the user mentions vibe coding, Supabase, RLS, leaked API keys, penetration testing their own app, or says a scanner flagged something. It produces a findings report with file, line, severity and evidence; it does not modify code — pair it with vibe-fix for remediation.
---

# vibe-audit

Find the five security holes that AI coding assistants reliably leave open.

They are not exotic. They are open because nobody prompted "and leave it locked" — security has no visual output, so it never makes it into the prompt. That means the failures are *predictable*, which is exactly what makes them auditable.

## Scope

| # | Failure | Reference |
|---|---------|-----------|
| 1 | Row Level Security disabled on Supabase/Firebase tables | `references/01-rls.md` |
| 2 | Authorization decided in the frontend | `references/02-broken-authz.md` |
| 3 | Routes that fetch by ID without checking the owner (IDOR/BOLA) | `references/03-idor.md` |
| 4 | Secrets exposed in the bundle, the repo, or Git history | `references/04-secrets.md` |
| 5a | Injection and XSS | `references/05a-injection-xss.md` |
| 5b | File upload without checks | `references/05b-uploads.md` |
| 5c | Missing rate limits | `references/05c-rate-limits.md` |

Audit only. Report findings, do not edit source files — a developer needs to see the shape of the problem before code starts moving. Remediation belongs to the `vibe-fix` skill.

## Not all five apply to every project

The five vary along different axes, and getting this wrong is the fastest way to produce a noisy report. Decide what is in scope *before* checking anything:

| Check | Applies when | Skip when |
|---|---|---|
| **1 — RLS** | The database is reachable from the client: Supabase, Firebase, Appwrite, Nhost, PocketBase, AWS Amplify/AppSync | There is a server between the client and the database. In a Django/Rails/Laravel/Express app with a private database, this category **does not exist** — say so in "Clean", do not invent an equivalent |
| **2 — Frontend authz** | Any app with a client and a server | A static site with no protected data behind it |
| **3 — IDOR** | Always, wherever a route takes an identifier | Never skip — this is the most portable of the five |
| **4a — Secrets in Git** | Always | Never skip |
| **4b — Secrets in the bundle** | A JavaScript frontend with a build step | Server-rendered apps with no client bundle. A Django template app cannot leak a key through `NEXT_PUBLIC_` because the mechanism isn't there |
| **5a — Injection/XSS** | Always, but the check inverts by template engine — see the reference | Never skip |
| **5b — Uploads** | The app accepts files | No upload path exists |
| **5c — Rate limits** | There are auth endpoints, paid-API proxies, or unbounded list endpoints | Purely static or read-only public content |

Run `scripts/detect_stack.sh` first precisely so this table can be applied from evidence rather than assumption. State the scoping decision at the top of the report — a reader needs to know whether "no RLS findings" means "checked and clean" or "not applicable here".

## Workflow

### 1. Map the stack before scanning

Run `scripts/detect_stack.sh` from the project root. It reports which languages, frameworks, database clients and secret-bearing files are present, and which scanners are installed locally.

Read the output before choosing checks. An audit that greps for `createClient` in a project with no Supabase client wastes the user's attention on noise, and noise is what makes people stop reading security reports.

### 2. Run whatever scanners exist

Run `scripts/run_scanners.sh`. It executes only the tools actually installed and writes results to `.vibeaudit/`:

- **gitleaks** — secrets in working tree *and* Git history (failure 4)
- **opengrep** / **semgrep** — SAST for injection, XSS, hardcoded secrets (failures 4, 5)
- **bandit** — Python-specific dangerous patterns (failure 5)
- **OWASP ZAP** — dynamic scan, only if the user supplies a running URL

If none are installed, say so plainly and continue with the manual checks — they cover ground scanners miss anyway. Do not block the audit on tool installation; offer install commands at the end.

### 3. Run the checks scanners cannot do

This is where most of the value is. Scanners find patterns; they do not find *missing* authorization, because absence has no signature. Work through the five references in order. Each one specifies what to grep for, what to read, what counts as evidence, and what the common false positives are.

Two deserve dedicated tooling:

- **RLS**: run `scripts/check_rls.py` against the migrations or schema directory. It parses `CREATE TABLE` statements and reports which tables never get `ENABLE ROW LEVEL SECURITY`, and which have RLS on but zero policies (which silently denies everything and usually gets "fixed" by turning RLS back off).
- **IDOR**: enumerate every route that takes an identifier and trace whether the handler compares that record's owner against the authenticated subject. `references/03-idor.md` describes the trace.

### 4. Triage before reporting

Rate each finding by what an attacker actually gets, not by how alarming the pattern looks:

- **Critical** — unauthenticated read or write of other users' data (RLS off on a table with user data; `service_role` key in the frontend bundle; route returning any record by ID with no ownership check)
- **High** — authenticated user reaching data or actions outside their scope; live secret committed anywhere in Git history
- **Medium** — defense-in-depth gaps: missing rate limit on auth endpoints, unvalidated input reaching a sink that is currently escaped by the framework, upload without type checking
- **Low** — hygiene: `.env` not in `.gitignore` while currently untracked, missing security headers

Verify before escalating. A hardcoded string matching a key pattern in a test fixture is not a critical finding, and reporting it as one costs you the reader's trust for the findings that are real.

### 5. Report

Always use this structure:

```markdown
# Security audit — <project name>
<date> · <commit sha> · <scanners that ran>

## Summary
<one paragraph: what an attacker can do today, in plain language>

| Failure | Status | Findings |
|---|---|---|
| 1. RLS | ❌ / ✅ / n/a | 3 |
| 2. Frontend authorization | ... | ... |
| 3. IDOR / ownership | ... | ... |
| 4. Exposed secrets | ... | ... |
| 5. Untrusted input | ... | ... |

## Findings

### [CRITICAL] <short title>
- **Where:** `path/to/file.ts:42`
- **Evidence:** <the actual line or query result — not a paraphrase>
- **Impact:** <what an attacker gets, concretely>
- **Fix:** <one line, then point at the vibe-fix reference>

## Clean
<what was checked and found sound — this matters, it tells the reader what the audit covered>

## Not covered
<what this audit could not check and why: no running instance for ZAP, no DB credentials to inspect live policies, etc.>
```

The "Not covered" section is not optional. An audit that implies completeness it does not have is worse than no audit, because it converts uncertainty into false confidence.

### 6. Hand off

Close with the exact next step: which finding to fix first, and that `vibe-fix` can apply the remediation. If secrets were found, say the rotation part out loud — a secret that appeared in a scan is compromised regardless of whether the commit was later deleted, and rotating it comes before any code change.

## Working against a live instance

If the user has a deployed URL and wants a dynamic scan, ZAP only runs against a target they own. Ask for explicit confirmation that they control the target before scanning, and keep the scan on the passive/baseline profile unless they ask otherwise — an active scan writes data and can knock over a small instance.

## Notes on false positives

Say "I could not verify this" rather than guessing. The three that burn the most time:

- Supabase tables in schemas other than `public` may be unreachable from the client anyway — check the exposed schemas setting before flagging.
- A frontend `isAdmin` check is not automatically a vulnerability. It is a vulnerability when the *server* does not repeat the check. Trace the corresponding endpoint before reporting.
- Anything under `test/`, `fixtures/`, `examples/` needs a look before it becomes a critical secrets finding — but a real key does not stop being real because it sits in a test file.
