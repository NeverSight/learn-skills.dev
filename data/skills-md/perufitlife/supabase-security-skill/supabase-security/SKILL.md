---
name: supabase-security
description: "Use when auditing or hardening a Supabase project's security posture. Triggers: scan/audit Supabase, RLS verification, find leaky tables, check anon grants, review SECURITY DEFINER functions, prep for the May 30 / Oct 30, 2026 Data API exposure changes, generate remediation SQL. Works against any Supabase project (Cloud or self-hosted) given a Personal Access Token."
metadata:
  author: Perufitlife
  version: "0.1.0"
  homepage: https://github.com/Perufitlife/supabase-security-skill
---

# Supabase Security Skill

A pure-Node.js audit + remediation toolkit for Supabase projects. No dependencies, runs locally, your token never leaves your machine.

## What it checks

1. **Tables with RLS disabled** + grants to anon/authenticated → critical leak
2. **Tables with RLS enabled but zero policies** AND direct anon grants → defense-in-depth issue
3. **SECURITY DEFINER functions executable by anon** → privilege escalation surface
4. **Default privileges still grant CRUD on future tables** → Supabase enforces revoke by Oct 30, 2026
5. **Public storage buckets** → asset leakage
6. **Auth signups with autoconfirm enabled** → signup abuse risk

Each finding includes the exact SQL needed to fix it. The skill never applies fixes automatically — it generates, you review, you run.

## How to use

### Quick audit (JSON to stdout)

```bash
SUPABASE_ACCESS_TOKEN=sbp_xxx \
  node scripts/audit.js <project-ref>
```

### HTML report (recommended for sharing)

```bash
SUPABASE_ACCESS_TOKEN=sbp_xxx \
  node scripts/audit.js <project-ref> --html report.html
```

Open `report.html` in any browser. Self-contained (~25KB), Tailwind + Chart.js via CDN, copy-to-clipboard buttons on every fix.

### Get a token

`https://supabase.com/dashboard/account/tokens` → New token. Read-only is enough for the audit; remediation needs no extra scope (you run the SQL yourself).

## Remediation flow

1. Run the audit, get the HTML report.
2. Review each finding. **Don't blindly apply fixes.** Some "high" findings (e.g. `is_admin()` exposed to anon) are intentional API endpoints.
3. Click "Copy all SQL" at the bottom and paste into Dashboard → SQL Editor.
4. Run inside a transaction: `BEGIN; ... ROLLBACK;` first to verify, then `BEGIN; ... COMMIT;`.

## Scope and limits

- **Read-only by default.** No fix is ever applied without you running the SQL.
- **Cannot revoke `supabase_admin` default privileges** via the Management API (Postgres permission limit). The audit reports this and points to the Dashboard toggle (`Project Settings → Data API → "Automatically expose new tables" = OFF`).
- **No false-positive suppression for app APIs.** A `get_dashboard_stats()` function intentionally exposed to anon will still appear as a high finding — exposed code paths are the surface area; you decide if intentional.
- **Storage scan covers buckets only.** Per-object RLS is not audited (would require iterating every object).

## Why another Supabase scanner?

Most existing tools (SupaExplorer, AuditYourApp, Vibe App Scanner) are SaaS — your project ref + URL go to a third party. This skill runs locally with your own PAT. The only network calls are to `api.supabase.com`. Audit it: see `scripts/audit.js`, ~250 lines of plain Node.

## License

MIT — see LICENSE.
