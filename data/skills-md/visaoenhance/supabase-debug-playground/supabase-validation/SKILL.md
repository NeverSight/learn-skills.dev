---
name: supabase-validation
description: "Supabase validation skill. Use when writing, deploying, or modifying any Supabase resource — edge functions, RPC functions, CRUD operations, RLS policies, or schema migrations. Adds mandatory pass/fail verification to every Supabase action before reporting completion."
license: MIT
compatibility: "Compatible with Cursor, Claude Code, and GitHub Copilot agent mode. Requires supabase CLI and Node >= 20 for local validation commands. Works with any project using Supabase (local or remote)."
metadata:
  author: visaoenhance
  version: "1.0.0"
---

> **This skill is safe for use in any project.**
> It never runs reset/break loops or destructive commands.
> Those exist only in the supabase-debug-playground teaching harness and are
> not part of this skill.

---

## Normative Principle

**No Evidence. Not done.**

Every action this skill governs — write, deploy, migrate, fix — is incomplete
until observable, raw output confirms it. This is not a style preference; it is
the contract this skill enforces.

**Two-tier action classification:**
- **Destructive actions** require environment classification (Rule A) + explicit
  confirmation before execution.
- **High-sensitivity file edits** (any file under `supabase/`) require showing
  a diff + confirmation before applying — even if the operation is not
  destructive by the definition below.

---

## Destructive Operations — Definition

Destructive operations are defined here so the term is not interpreted loosely.
Any rule that gates on "destructive" applies to all items in this list:

- Dropping tables or columns
- Resetting the database (`supabase db reset`)
- Replaying migrations against any live project (local, staging, or production —
  even local, unless explicitly confirmed disposable)
- Deleting rows or truncating tables
- Overwriting a deployed edge function
- Modifying or dropping RLS policies
- Any write using `service_role` key

If an operation is not on this list, it is still subject to Rules B and A
(evidence and environment classification) but does not require the full
destructive-operation confirmation protocol.

---

## Global Clause — Non-Interactive Mode

**Treat as non-interactive if any of the following are true:**
- No active chat session is available to receive a reply
- Running inside a CI job, automated workflow, or scheduled script
- Agent mode with `autoApprove`, `--yes`, or equivalent flag set
- The agent cannot determine whether a reply is possible

If uncertain, treat as non-interactive.

**Rule:** If user confirmation is required (by any rule below) but the agent is
running in a non-interactive context, the agent must:
1. Output the exact command, query, or SQL that would be executed
2. Explain what it does and why confirmation is required
3. Not execute it

A rule requiring confirmation does not become optional because the agent cannot
ask. It becomes a manual handoff.

---

## Global Clause — Never Disclose Secrets

**Never print, paste, log, or include in a diff:**
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY` (or any `service_role` key)
- JWTs or bearer tokens of any kind
- Any value that begins with `eyJ` (base64-encoded JWT)
- Any secret from `.env`, `.env.local`, or equivalent files

**If the agent needs to confirm a key is present:** state "I can see a value is
set for `SUPABASE_ANON_KEY`." If identity confirmation is needed, ask the user
to confirm the last 4 characters — do not print them.

**Showing `SUPABASE_URL` is permitted** — host portion only (e.g.,
`https://xyz.supabase.co`). Do not include query strings or path segments that
may carry tokens.

This rule applies even in local development.

---

## Rule A — Environment Classification Gate

Before any write, migration, RLS change, or function deploy, the agent must
classify the environment and surface evidence to the user. It must not proceed
until the environment type is confirmed.

**Classification levels:**
- `local` — `SUPABASE_URL` is `http://localhost:*`, or `supabase status` shows
  local instance
- `staging` — known non-production remote ref, explicitly confirmed by user
- `production` — any `*.supabase.co` URL or unrecognised project ref

**Evidence the agent must display before acting:**
- The value of `SUPABASE_URL` (host portion only — no keys)
- Output of `supabase status` or `supabase projects list` showing the project ref
- For production: the ref + any branch/context information available

**Enforcement:**
- `local` — agent may proceed with non-destructive validation commands
  autonomously. Non-destructive examples: `SELECT` schema inspection queries,
  `supabase functions logs`, `curl` / HTTP request replays, `git diff`,
  `supabase gen types typescript --local`.
- `staging` — agent must state the environment and confirm intent before writing
- `production` — agent must surface the full command for user review and require
  explicit "yes, proceed" before executing anything that writes or modifies schema
- If environment cannot be determined — treat as production; do not execute

**No Environment Assumptions (see also Rule G):** The agent must never infer
environment type from file presence alone — the existence of `.env`,
`supabase/config.toml`, or a `supabase/` directory does not confirm the
environment is local. Environment classification must be based only on runtime
evidence: the `SUPABASE_URL` value, output of `supabase status`, or an explicit
user statement. Rule G extends this constraint to all tasks, including read-only
inspection — not only pre-action gates.

---

## Rule B — No Silent Writes

An agent must never perform a write operation and report completion without
returning observable evidence that the write succeeded.

**Required evidence by operation type:**

| Operation | Required evidence |
|---|---|
| `INSERT` | Returned row with `id` from `.insert().select()` |
| `UPDATE` / `DELETE` | Row count or returned rows confirming the change |
| RLS policy change | Output of `SELECT policyname, cmd FROM pg_policies WHERE tablename = '...'` |
| Edge function deploy | HTTP response payload containing `request_id` and `ok: true` |
| Migration | `supabase db diff` or `information_schema.columns` query confirming column/table exists |
| Schema type regen | `git diff supabase/types.gen.ts` output (even if empty — show it) |

If the operation produces no returnable evidence (e.g., `Prefer: return=minimal`),
re-run the operation with `.select()` chained, or run a follow-up read query.

**Surface the raw output. Do not summarise before showing it.**
Return the actual payload — row object, JSON body, query result, diff — so the
user can verify directly. You may summarise after showing raw output.

```
// Bad
"Insert successful."

// Good
{ id: 42, created_at: "2026-02-28T20:14:22Z" }
// (then) "Insert confirmed — row id 42 returned."
```

---

## Rule C — `service_role` Restricted Use

`service_role` bypasses all RLS policies. Its use must be explicitly bounded.

**Permitted without user confirmation:**
- Read-only diagnostics only — `SELECT` queries to inspect schema, policies,
  or data for debugging purposes

**Require explicit user confirmation before use:**
- Any write, insert, update, or delete using `service_role`
- Any operation that modifies schema or policies using `service_role`

**Confirmation protocol:**
1. State clearly: "This operation requires `service_role` which bypasses RLS."
2. Display the environment classification (Rule A) as part of the request
3. Show the exact command or query that will be run
4. Wait for explicit "yes" — do not infer consent from prior approval of a
   related step
5. If non-interactive: output the command for manual review, do not execute

---

## Rule D — Safe Fallback When Tooling Is Unavailable

The agent must not hallucinate access it doesn't have.

**If a required tool is unavailable:**
1. State the missing capability explicitly
2. Propose a non-destructive alternative:
   - Instead of CLI logs → capture `error.code`, `error.message`, `error.hint`
     from the client SDK response
   - Instead of `supabase status` → ask user to run it and paste the output
   - Instead of DB introspection → provide the exact SQL for the user to run
     in the dashboard SQL editor
3. Never invent log output, query results, or command output
4. Never report a validation as passed unless the agent itself received and
   parsed the response

**Prohibited:**
- "I checked the logs and there are no errors" without having received log output
- "The migration ran successfully" without confirmed evidence
- "The policy is in place" without `pg_policies` output showing it

---

## Rule E — Minimal File Mutations

**Required behaviour:**
- Prefer the smallest diff that achieves the fix
- Before applying any file change, show a diff or describe line-level changes
- Never use a "replace entire file" pattern unless the user explicitly requests it
- For Supabase-specific files (`supabase/functions/**`, `supabase/migrations/**`,
  `supabase/types.gen.ts`): treat all changes as high-sensitivity and show the
  diff before applying

**Why Supabase files are high-sensitivity:**
- Overwriting a migration file that has already run creates drift — it does not
  undo the migration
- Overwriting `types.gen.ts` with stale content breaks TypeScript without a
  compile error
- Overwriting an edge function's `index.ts` with an earlier version silently
  reverts a fix

**Permitted without confirmation:** adding new files where no existing file is
displaced.
**Requires confirmation:** modifying or deleting any existing file under
`supabase/`.

---

## Rule G — No Hidden Context Assumption

The agent must not infer Supabase project configuration from local file presence
alone. The existence of `.env`, `supabase/config.toml`, or a `supabase/`
directory does not confirm which project is active, whether it is local or
remote, or whether the configuration applies to the current task.

**Environment classification must be based only on runtime evidence:**
- The resolved value of `SUPABASE_URL` (from the active shell environment — not
  a `.env` file the agent reads in isolation)
- Output of `supabase status` or `supabase projects list`
- An explicit user statement (e.g., "I'm working against our staging project")

**What this prevents:**
- A skill applied inside a monorepo where a `supabase/` folder exists but
  belongs to a different sub-project
- An agent assuming `local` because it sees `http://localhost` in a `.env` file
  that may be stale or inactive
- Hallucinated project context: "this looks like a local project" based on file
  presence alone

**Required agent phrasing:** "I can see a `supabase/` directory and a `.env`
file. To classify the environment I need to confirm the active `SUPABASE_URL`.
Running `supabase status`…" — not "This looks like a local project."

**Relationship to Rule A:** Rule G governs what the agent may *assume* at any
point, including read-only tasks. Rule A governs what the agent must *confirm
before acting*. Rule G is the precondition; Rule A is the gate.

---

## Activation Rule — When This Skill Applies

This skill MUST activate automatically whenever any of the following signals
appear in code, config, or commands:

- `supabase-js` is imported or used
- `supabase.rpc()` is called
- `.from(...).insert()`, `.update()`, or `.delete()` is used
- `CREATE FUNCTION`, `CREATE POLICY`, or `ALTER TABLE` appears in SQL
- `supabase functions deploy` is run
- `supabase gen types` is relevant to the task
- Any migration touches schema or RLS
- Any file under `supabase/functions/` is modified
- Any file under `supabase/migrations/` or `supabase/seed.sql` is modified
- Any `supabase db *` command is run (push/reset/diff)

**When activated:**
- Add a validation step to the task plan before execution begins
- Execute that validation step before reporting completion
- Do not ask the user whether to validate — validate automatically
- If execution is not possible, state that explicitly and provide the exact
  commands for the user to run

---

## Validation Contract

A Supabase task is not complete when code compiles or a command exits 0.
It is complete only when the validation step passes.

**Definition of done:**
1. Failure or baseline confirmed (run the current behaviour first)
2. Fix applied
3. Validation executed
4. Validation produces a binary pass result

**Required plan shape:**
1. Run current behaviour — confirm failure if fixing, baseline if building
2. Diagnose — read the actual error (code, message, hint)
3. Apply minimal fix
4. Verify — binary pass/fail, not eyeballing
5. Report completion

**Hard gates — none of these are optional:**
- "Looks correct" is not a valid success signal
- "Exit code 0" alone is not a valid success signal
- Never skip verification because the code looks right — run the check
- If a verify step fails, diagnose before retrying — do not loop without
  reading the error

---

## Pattern Index

| Pattern | Trigger | Passes when |
|---|---|---|
| 1 — Edge function (local) | Change to a function running via `supabase functions serve` | HTTP 200 + `body.ok === true` + `request_id` present |
| 2 — Edge function (production) | `supabase functions deploy <name>` to a real project | HTTP 200 + `body.ok === true` + `request_id` present |
| 3 — RPC | `CREATE OR REPLACE FUNCTION` or migration modifying an RPC | No error + response contains expected fields |
| 4 — CRUD / Insert | Any `.insert()`, `.update()`, `.delete()` via supabase-js | Non-null array with `id` present |
| 5 — RLS | `CREATE POLICY`, `DROP POLICY`, `ENABLE ROW LEVEL SECURITY` | All 3 roles pass: unauthed blocked + authed allowed + service_role allowed |
| 6 — Schema migration | Migration adding, removing, or renaming a column | `types.gen.ts` reflects live schema + file committed |

---

## Pattern 1 — Edge Function (Local)

**Trigger:** after any change to a Supabase edge function running locally via
`supabase functions serve`.

**Validation steps:**
1. POST to `http://localhost:54321/functions/v1/<name>`
2. Assert HTTP 200
3. Assert response body is valid JSON with `ok: true`
4. Assert `request_id` is present in the response body

**Fail signal:** HTTP 500, empty body, no `request_id`, or
`Deno.env.get(...)` returning `undefined`.

**Diagnostic:** errors stream to the `supabase functions serve` terminal —
read them directly. There is no `supabase functions logs` command for local dev.

**Docs:**
- [Environment Variables / Secrets](https://supabase.com/docs/guides/functions/secrets)
- [Error Handling](https://supabase.com/docs/guides/functions/error-handling)
- [Logging](https://supabase.com/docs/guides/functions/logging)
- [Troubleshooting](https://supabase.com/docs/guides/functions/troubleshooting)

**Do not report done until:** HTTP 200 + `ok: true` + `request_id` confirmed.

---

## Pattern 2 — Edge Function (Production)

**Trigger:** after `supabase functions deploy <name>` to a real Supabase project.

**Validation steps:**
1. POST to `$SUPABASE_URL/functions/v1/<name>` with
   `Authorization: Bearer $SUPABASE_ANON_KEY` (do not print the key value)
2. Assert HTTP 200
3. Assert response body is valid JSON with `ok: true`
4. Assert `request_id` is present in the response body

**Fail signal:** HTTP 500 or unstructured body.

**Diagnostic:** dashboard function logs:
`https://supabase.com/dashboard/project/<PROJECT_REF>/functions/<name>/logs`

**Docs:**
- [Deploy to Production](https://supabase.com/docs/guides/functions/deploy)
- [Environment Variables / Secrets](https://supabase.com/docs/guides/functions/secrets)
- [Logging](https://supabase.com/docs/guides/functions/logging)
- [Troubleshooting](https://supabase.com/docs/guides/functions/troubleshooting)

**Do not report done until:** HTTP 200 + `ok: true` + `request_id` confirmed
against the production URL.

---

## Pattern 3 — RPC

**Trigger:** after any `CREATE OR REPLACE FUNCTION` or migration that modifies
an RPC.

**Validation steps:**
1. Call via supabase-js: `supabase.rpc('<function_name>', { ...args })`
2. Assert `error` is null
3. Assert response data contains the expected fields

**Fail signal:** `error.code` is present — read `error.code`, `error.message`,
`error.hint` as a unit.

**Diagnostic:** if error code is `42703` (undefined column), run:
```sql
SELECT pg_get_functiondef('<schema>.<function_name>(<arg_types>)'::regprocedure);
```

**Docs:**
- [Database Functions](https://supabase.com/docs/guides/database/functions)
- [JavaScript RPC](https://supabase.com/docs/reference/javascript/rpc)
- [PostgREST Error Codes](https://supabase.com/docs/guides/api/rest/postgrest-error-codes)

**Do not report done until:** RPC returns no error + response shape is correct.

---

## Pattern 4 — CRUD / Insert

**Trigger:** after any insert, update, or delete via supabase-js.

**Validation steps:**
1. Always chain `.select().throwOnError()` onto the operation
2. Assert returned `data` is a non-null array
3. Assert the array contains a row with `id`

**Why this matters:** `.insert()` without `.select()` sends
`Prefer: return=minimal` — PostgREST returns 204 with empty body. supabase-js
translates this to `{ data: null, error: null }`. This is not confirmation the
row was saved.

**Correct pattern:**
```ts
const { data } = await supabase
  .from("table")
  .insert({ ...values })
  .select()
  .throwOnError();
// data is a non-null array if the insert succeeded
```

**Docs:**
- [Managing Tables](https://supabase.com/docs/guides/database/tables)
- [JavaScript Insert](https://supabase.com/docs/reference/javascript/insert)
- [PostgREST Error Codes](https://supabase.com/docs/guides/api/rest/postgrest-error-codes)

**Do not report done until:** insert returns a non-null array containing a row
with `id`.

---

## Pattern 5 — RLS

**Trigger:** after any `CREATE POLICY`, `DROP POLICY`,
`ALTER TABLE ... ENABLE ROW LEVEL SECURITY`, or migration touching RLS.

**Validation steps — all three must pass:**
1. **Unauthenticated anon** — attempt the restricted operation with a plain anon
   key and no auth session → assert blocked (error `42501`)
2. **Authenticated user** — same operation with anon key + valid JWT → assert
   allowed
3. **service_role** — same operation with service_role key → assert allowed
   (service_role always bypasses RLS)

**Diagnostic commands:**
```sql
-- See all policies on a table
SELECT policyname, cmd, qual, with_check
FROM pg_policies WHERE tablename = '<table>';

-- Confirm RLS is enabled
SELECT relname, relrowsecurity FROM pg_class WHERE relname = '<table>';
```

**Key insight:** if something works from the Supabase dashboard but fails in the
app, check whether an INSERT policy exists for the role your app uses.
`service_role` has `BYPASSRLS` — it skips policy evaluation entirely.

**Docs:**
- [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)
- [Debugging and Monitoring](https://supabase.com/docs/guides/database/inspect)
- [Hardening the Data API](https://supabase.com/docs/guides/database/hardening-data-api)

**Do not report done until:** all three scenarios produce the expected result.

---

## Pattern 6 — Schema Migration / Type Drift

**Trigger:** after any migration that adds, removes, or renames a column.

**Validation steps:**
1. Run: `supabase gen types typescript --local > supabase/types.gen.ts`
2. Run: `git diff supabase/types.gen.ts`
3. If diff is non-empty → expected (new column). Commit the updated file.
4. If diff is empty and you added a column → migration may not have run — check.

**Drift detection:**
```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = '<table>'
ORDER BY ordinal_position;
```

**Why this matters:** TypeScript compiles cleanly against stale types. A column
that exists in the DB but not in `types.gen.ts` is simply invisible to your code
— no compile error, silent bugs.

**CI:** run `supabase gen types typescript --local > supabase/types.gen.ts &&
git diff --exit-code supabase/types.gen.ts` after any migration deploy. Fail the
build if the diff is non-empty.

**Docs:**
- [Generating TypeScript Types](https://supabase.com/docs/guides/api/rest/generating-types)
- [Debugging and Monitoring](https://supabase.com/docs/guides/database/inspect)
- [Local Development](https://supabase.com/docs/guides/cli/local-development)

**Do not report done until:** `types.gen.ts` reflects the current live schema
and the file is committed.
