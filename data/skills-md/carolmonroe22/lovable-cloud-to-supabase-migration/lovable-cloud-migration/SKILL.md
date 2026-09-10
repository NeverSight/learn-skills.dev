---
name: lovable-cloud-migration
description: Guide for migrating from Lovable Cloud to your own Supabase project. Use when users ask about exporting data from Lovable Cloud, removing or disconnecting Lovable Cloud, pausing Lovable Cloud, restoring a Lovable Cloud .backup export, migrating to their own Supabase, getting data out of managed Lovable database, switching from Lovable Cloud to external Supabase, connecting their own Supabase to a Lovable project, or Lovable Cloud limitations (no SQL editor access, no custom auth emails, no direct Supabase dashboard access, no service role key).
license: MIT
metadata:
  author: Carol Monroe - Lovable Champion and Supabase SupaSquad Member
  author_url: https://carolmonroe.com
  author_github: CarolMonroe22
  version: "4.1.2"
  tested: "2026-08-31"
  tags:
    - supabase
    - lovable
    - migration
    - database
    - lovable-cloud
    - mcp
    - export
---

# Lovable Cloud to Own Supabase Migration

> Created by **Carol Monroe** - Lovable Champion and Supabase SupaSquad Member
> The full migration was verified on a real end-to-end migration (12 tables,
> 237 rows, 23 users, 40 storage files, 5 edge functions, 2 cron jobs) on
> 2026-07-06. Password-hash access through Lovable MCP was rechecked on
> 2026-08-31 without exposing any hash values.

## What Changed in v4.1.2 (August 2026)

Lovable's official documentation says that user passwords are not exported in a
usable form and recommends a password-reset flow for migrated users. This skill
therefore treats password reset as the default path.

The native export is still the primary source for the database, but it must never
be presented as a password-preserving export.

An optional advanced route remains available when Lovable MCP `query_database`
can read
`auth.users.encrypted_password` on supported Cloud projects. A boolean-only
capability check succeeded on 2026-08-31, and the complete hash-preserving flow
was previously verified in March and July 2026. This route is optional,
sensitive, and subject to change because Lovable MCP is a research preview.

## What Changed in v4 (July 2026)

Lovable shipped official **Export**, **Pause**, and **Remove** buttons for Cloud
(Cloud tab > Overview > Advanced settings). **Lovable Cloud is no longer permanent.**
This rewrites the migration playbook:

- The old "Cloud can never be disconnected" fact is obsolete. You can now export
  your database, remove Cloud from the SAME project, and connect your own Supabase.
- The native export file (a `pg_dump` custom-format backup) is now the PRIMARY
  database source. Do not assume it preserves usable passwords. Follow the
  official reset path by default, or explicitly opt into the advanced MCP hash
  route after a capability check and security confirmation.
- The old 68-step MCP migration into a fresh Lovable project is now the FALLBACK
  path, kept for the cases the native export cannot serve.

Naming note: this skill keeps the name `lovable-cloud-migration` on purpose so v4
REPLACES any earlier install of the same skill (whose "Cloud is permanent" guidance
is now obsolete) instead of coexisting with it. If both this and an older copy are
somehow present, this one wins - delete the older one.

## What This Skill Does

Migrates an entire Lovable Cloud project to your own Supabase: database schema,
data, RLS policies, functions, triggers, sequences, auth users and identities,
storage buckets and files, edge functions with correct per-function verify_jwt,
cron jobs, and secrets inventory. Then removes Cloud and connects the user's own
Supabase to the same Lovable project. Passwords use the official reset path by
default; the advanced MCP route can preserve existing hashes when available and
explicitly approved.

## Decision Point (ALWAYS start here)

Ask what the user actually needs, then pick the path:

| User's situation | Path |
|---|---|
| "My app burns credits while I'm not working on it" | No migration. **Pause Cloud** (Cloud tab > Overview > Advanced settings). Done. |
| "I want backups of my Cloud data" | No migration. **Export project data** works standalone, once per 24h, keep building on Cloud. |
| Ready to run on own Supabase, database ≤ 5 GB | **SAME-PROJECT PATH** (primary, below): Export + auth decision + Remove + Connect on the existing Lovable project. |
| Database > 5 GB, export unavailable/failing, or user wants the original Cloud project kept untouched | **FRESH-PROJECT PATH** (legacy fallback): full MCP migration into a new Lovable project. See [references/fresh-project-path.md](references/fresh-project-path.md). |

Remind the user: Export/Pause/Remove buttons cost no credits. Only agent prompts do.

## Why Migrate at All (the right reasons)

Lovable Cloud is a solid managed backend. Migration makes sense when the project
needs things only a full Supabase setup provides:

| You want to... | Why it needs your own Supabase |
|---|---|
| Customize auth emails (sender, design, content) | Cloud sends from `no-reply@auth.lovable.cloud` |
| Access the full Supabase dashboard | SQL editor, extensions, logs, monitoring |
| Use the service role key | Admin operations and some edge functions |
| Have staging + production environments | Cloud is one database per project |
| Own your infrastructure long-term | Your project, your org, your billing |

If none of these apply and the user is happy on Cloud, say so: there is no need
to migrate, and Export-as-backup + Pause cover most worries now.

## Prerequisites

| Requirement | Needed for | How to set up |
|---|---|---|
| Lovable account with Cloud enabled | Everything | - |
| Supabase account | Everything | https://supabase.com |
| GitHub connected to the project | Everything (function code travels via the repo) | Editor > + menu > GitHub > Connect |
| **Lovable MCP** | Strongly recommended for inventory and source-side checks; required for the optional password-hash preservation route | `/mcp` in Claude Code, or claude.ai Settings > Connectors - https://docs.lovable.dev/integrations/mcp-servers |
| Supabase MCP | Destination-side automation (create project, run every verification) | Built into Claude Code - https://supabase.com/docs/guides/getting-started/mcp |
| pg_restore 16+ with zstd | Same-project path Step 14 | macOS: `brew install postgresql@18` |
| GitHub CLI (`gh`) | Fresh-project path only | `brew install gh` + `gh auth login` |
| Supabase CLI | Optional - faster function deploys and storage uploads | https://supabase.com/docs/guides/getting-started |

Works in Claude Code and claude.ai, and also in other MCP-compatible agents like
Cursor. Without any MCP, the same-project path still works - the user reads the
counts off the Cloud panel by hand and Claude guides the terminal steps.

## Choose Migration Level

Ask the user which level they want before starting:

| Level | Audience | Behavior |
|---|---|---|
| **Guided** | First migration, not technical | Explain each phase, confirm before proceeding, show what is happening |
| **Standard** | Knows Supabase/Lovable | Confirm key decisions, run phases with minimal pauses |
| **Express** | Advanced, done it before | Ask for source + destination, run everything, report at the gate |

Every level stops at the same hard checkpoints: cost confirmation, the Phase 7
gate, and the Remove click.

## Key Facts

### The native export
- Format: `pg_dump` v18 **custom format** with **zstd compression** (source Postgres 17).
- Restoring requires `pg_restore` v16+ **built with zstd**. The libpq build from
  Homebrew does NOT include zstd and fails with "does not support compression with
  zstd" even when the version number looks fine. Use `postgresql@18` (Trap 18).
- Lovable's documentation says password material is not exported in a usable
  form. Treat the export as carrying users, not usable passwords, and plan resets
  unless the optional MCP route is completed and verified.
- INCLUDED for the supported database flow: schema and data, RLS policies,
  triggers, custom functions, sequences, cron and storage metadata. Verify every
  component against the baseline because the export contract can change.
- NOT included: storage FILES (actual bytes), edge function CODE (lives in the
  repo), edge function SECRET values, vault secret VALUES (rows restore but are
  encrypted with the old project's key, unrecoverable cross-project).
- The export saves INTO the project's own Cloud storage as a bucket named like
  `database_export_06_07_26`. **Download it before removing Cloud** - it dies with
  Cloud (Trap 17). Limits: 5 GB, one export per 24 hours.
- The "we'll email you" toast is unreliable. Don't wait for the email: check
  Storage for the export bucket (~1 minute for a small database).

### Passwords: official default vs advanced MCP route
- **Official default:** Lovable says passwords are not exported in a usable form.
  Build and test a password-reset flow before removing Cloud.
- **Advanced option:** Run a capability check that returns only counts, never
  hashes. If non-empty hashes are accessible, explain that the values will pass
  through MCP/agent execution, obtain explicit approval, then migrate only the
  minimum required auth fields.
- Never paste hashes into chat, print them, commit them, or store them in a normal
  project folder. Delete protected temporary artifacts after the login test.
- If the capability check fails, the agent cannot guarantee secret-safe handling,
  or any expected password user lacks a hash, use the reset path for that user.
  OAuth and passwordless users may correctly have no hash. Do not improvise
  passwords.

### The Lovable side
- After connecting an own Supabase, the Lovable agent CAN deploy edge functions to
  it (confirmed directly with the agent, config.toml respected). It CANNOT set
  edge function secrets - only the user can, in the Supabase dashboard.
- `LOVABLE_API_KEY` is a managed WORKSPACE secret, independent of Cloud. It
  SURVIVES Cloud removal. AI features keep working after re-wiring (Trap 25).
- Connecting the Supabase integration auto-rewrites `.env` (correct URL + key, no
  manual editing). But it may also overwrite `src/integrations/supabase/client.ts`
  with a template that breaks SSR on modern (TanStack) stack projects (Trap 23).
- GitHub sync is two-way. Temporary helper functions you delete in Supabase come
  BACK if they still live in the repo - delete them everywhere (Trap 24).
- Remix still does NOT work for migration - it inherits Lovable Cloud.

### Security
- The `.backup` file contains personal and authentication data and may contain
  sensitive credential material. Treat it like a password: keep it local, never
  commit it, delete it after the migration.
- If the database password touched a chat, a script, or an AI session during the
  migration, rotate it at the end (Dashboard > Settings > Database).
- Before pushing any migration artifacts to a public repo, scan them for project
  refs, keys, emails, and personal data.

## THE SACRED ORDER

```
1. EXPORT      the database (button)
2. DOWNLOAD    the export + the storage files    ← they live inside Cloud
3. BUILD       the new Supabase (restore, fix, upload, deploy)
4. AUTH        test password reset, or explicitly run the MCP hash route
5. VERIFY      the 12-count gate — ALL GREEN or stop
6. REMOVE      Lovable Cloud                     ← only now, nothing before this is destructive
7. CONNECT     your own Supabase to the same project
```

Nothing is removed until its replacement is alive and verified. At every step
before 6, the app still runs on Cloud, untouched. If any step fails, stop and fix -
Cloud is the safety net until the gate is green.

## SAME-PROJECT PATH (primary)

The full 33-step playbook lives in
[references/same-project-path.md](references/same-project-path.md).
Read it when actually running the migration. The shape:

| Phase | Steps | What happens | Human moments |
|---|---|---|---|
| 1. Baseline + GitHub | 1-4 | 12-count inventory, repo connected, verify_jwt + secrets map | Connect GitHub if missing |
| 2. Export + Download | 5-8 | Official export triggered, found in Storage, downloaded, storage files downloaded | Export click, downloads |
| 3. Create destination | 9-12 | Supabase project, session pooler connection string | Confirm cost |
| 4. Restore | 13-16 | zstd-capable pg_restore, identities fix pass, auth decision, snapshot check | Approve advanced hash route or use reset |
| 5. Post-restore fixups | 17-21 | Cron recreate + zombie hunt, ghost rows cleared, files uploaded, URLs rewritten, sequences | - |
| 6. Functions + secrets | 22-25 | Deploy (CLI/MCP/agent), secrets re-entered, AI re-wired, temp helpers deleted everywhere | Enter secrets |
| 7. THE GATE | 26-28 | 12-category audit vs baseline + tested auth path + image opens | Gate decision |
| 8. Remove + Connect | 29-33 | Remove Cloud, connect own Supabase, fix integration overwrite, final tidy | Remove + Connect clicks |

### Hard stops (never skip, at any migration level)

1. **Cost confirmation** before creating the Supabase project (Step 9).
2. **The gate** (Step 28): every count green + one tested login through the chosen
   auth path (original password after MCP preservation, or completed reset), or
   DO NOT proceed. Cloud stays as the safety net.
3. **Remove is the only destructive click** (Step 29) and it is always the user's
   hand, never automated, never before the gate.

## When to read what

| Situation | Read |
|---|---|
| Running the primary migration | [references/same-project-path.md](references/same-project-path.md) |
| Export unavailable, DB > 5 GB, or original project must stay untouched | [references/fresh-project-path.md](references/fresh-project-path.md) |
| Choosing/comparing export methods | [references/export-methods.md](references/export-methods.md) |
| Storage helper function (fresh-project path) | [references/migrate-storage-function.md](references/migrate-storage-function.md) |
| A symptom needs a fix | Symptoms table in [references/same-project-path.md](references/same-project-path.md), then [references/troubleshooting.md](references/troubleshooting.md) |

## FRESH-PROJECT PATH (legacy fallback)

The complete v3.1 flow - 68 deterministic steps, 9 phases, MCP-driven scan and
rebuild into a NEW Lovable project - lives in
[references/fresh-project-path.md](references/fresh-project-path.md).

Use it when:
- The database exceeds the 5 GB export cap (also: email support@lovable.dev with
  the project ID for a manual export).
- The export feature is unavailable or failing for the project.
- The user wants the original Cloud project kept running/untouched (staging-style
  migration with zero risk to the original).

That reference keeps its own trap table (Traps 1-16) and troubleshooting rows.

## Traps Added in v4 (17-26, all hit and verified live)

| Trap | Severity | Description | Prevention |
|---|---|---|---|
| 17 | Critical | Export saves INTO Cloud storage - Remove deletes it | Sacred order: Export -> DOWNLOAD -> Remove last (Steps 5-7, 29) |
| 18 | Blocker | brew libpq pg_restore lacks zstd, fails on the .backup | Test with pg_restore --list first; postgresql@18 (Step 13) |
| 19 | Critical | auth.identities dropped by restore FK ordering | Count check + second data-only pass (Step 15) |
| 20 | Silent bug | cron.job restore = permission denied; restored/recreated commands point at OLD project URL and run against a dead endpoint | cron.schedule + zombie hunt + cron.alter_job (Step 17) |
| 21 | Silent bug | storage.objects ghost rows block uploads ("resource already exists"); protect_delete blocks SQL DELETE | Clear via Storage API/CLI before upload, never SQL (Step 18) |
| 22 | Silent bug | Signed URLs (?token=) die with the old project; text-replace makes them LOOK migrated | Regenerate or NULL, never rewrite (Step 20) |
| 23 | Breaker | Supabase integration overwrites client.ts, breaks SSR on modern stack | Post-connect fix prompt with explicit Do NOTs (Step 31) |
| 24 | Zombie | Temp helper functions replicate back via two-way GitHub sync | Delete in Supabase AND in the repo (Step 25) |
| 25 | Surprise (good) | LOVABLE_API_KEY survives Cloud removal (workspace secret) | Re-wire: server functions (recommended) or copy the key (Step 24) |
| 26 | Data loss | Restore is a snapshot at EXPORT time; later writes are missing | Ask when writes stopped; re-export or re-apply deltas (Step 16) |

## Trap Added in v4.1

| Trap | Severity | Description | Prevention |
|---|---|---|---|
| 27 | Account lockout | Current Lovable docs say official exports do not contain usable passwords | Default to reset; use the MCP hash route only after capability check, explicit approval, and secure handling |

## Human Assistance Points (same-project path)

| Step | What the user must do | Why not automated |
|---|---|---|
| 1 | Connect GitHub in the editor | Dashboard-only flow |
| 5 | Click Export project data | Dashboard-only button |
| 7 | Download the export zip | Browser download |
| 8 | Download storage files (small projects) | Browser download (scriptable for large) |
| 23 | Enter edge function secrets | No MCP/agent can set secrets |
| 29 | Click Remove Lovable Cloud | Destructive, deliberately manual |
| 30 | Connect own Supabase | Dashboard OAuth flow |
| 33 | OAuth providers, JWT secret | Dashboard-only settings |
| Cost | Confirm Supabase project cost | MCP requires explicit confirmation |


## Plan Requirements

| Tool | Plan needed | Cost |
|---|---|---|
| Lovable | Any plan with Cloud | Varies |
| Supabase | Free works if slot available | $0-$10/mo |
| Claude Code (optional, automates everything) | Pro or Max | $20/mo+ |
| claude.ai (optional, no-CLI route) | Free/Pro | $0+ |
| GitHub | Free | $0 |

## Documentation Links

| Resource | URL |
|---|---|
| Lovable Cloud advanced settings (export, pause, remove) | https://docs.lovable.dev/features/advanced-settings |
| Lovable GitHub integration | https://docs.lovable.dev/integrations/github |
| Lovable MCP | https://docs.lovable.dev/integrations/mcp-servers |
| Supabase: restore a backup | https://supabase.com/docs/guides/platform/migrating-within-supabase/dashboard-restore |
| Supabase: database backups | https://supabase.com/docs/guides/platform/backups |
| Supabase MCP | https://supabase.com/docs/guides/getting-started/mcp |
| Supabase Edge Functions | https://supabase.com/docs/guides/functions |
| Supabase Storage | https://supabase.com/docs/guides/storage |
| Supabase Auth | https://supabase.com/docs/guides/auth |

## Resources by Carol Monroe

- The manual walkthrough this skill automates:
  https://carolmonroe.com/blog/export-remove-lovable-cloud
- Migrate with AI guide (claude.ai route + Claude Code route):
  https://carolmonroe.com/blog/migrate-lovable-cloud-with-ai
- Legacy MCP migration guide (fresh-project path):
  https://carolmonroe.com/blog/lovable-cloud-mcp-migration
- MCP setup for claude.ai chat:
  https://carolmonroe.com/blog/connect-lovable-supabase-mcp-to-claude
