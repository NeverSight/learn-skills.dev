---
name: supabase-splinter-review
description: Run Supabase Splinter on local DB and triage findings into fix-now vs defer with a remediation plan. Inputs focus and threshold.
metadata:
  short-description: Inputs focus threshold. Run Splinter locally then plan worthy fixes
---

# Supabase Splinter Review

## Goal

Run `splinter.sql` against a local Supabase instance, assess each recommendation, identify which are worth resolving now, and propose an actionable plan for those selected items.

## Invocation syntax

Preferred:

```text
$supabase-splinter-review <focus> <threshold>
```

Examples:

```text
$supabase-splinter-review all warn
$supabase-splinter-review security error
$supabase-splinter-review performance warn
$supabase-splinter-review
```

Normalization:

- `focus`: `all | security | performance`
- `threshold`: `error | warn | info`
- If omitted, default to `all warn`.

## Preconditions

- Local Supabase instance is running.
- `supabase` CLI is installed.
- `psql` is installed.

## Run Splinter

From the skill directory:

```bash
bash scripts/run_splinter.sh
```

Artifacts produced (default):

- `.splinter/splinter.sql`
- `.splinter/splinter_results.csv`
- `.splinter/run_metadata.txt`

## Assessment workflow

1. Execute Splinter and load findings
- Run the helper script.
- Parse the CSV findings.
- Normalize severity labels and categories.

2. Filter by invocation args
- Apply `threshold` first:
  - `error`: only high-severity findings
  - `warn`: include error + warning
  - `info`: include all findings
- Apply `focus` next:
  - `security`: auth/permissions/data exposure findings
  - `performance`: indexing/query/planner findings
  - `all`: no focus filtering

3. Score each finding
- Score dimensions:
  - production impact
  - confidence/false-positive risk
  - implementation effort
  - validation effort
- Mark each finding as:
  - `fix-now`
  - `defer-with-rationale`
  - `ignore-with-rationale`

4. Decide what is worthy
- Worthy items are those marked `fix-now`.
- Include `defer-with-rationale` only when risk is non-trivial but blocked by missing evidence.

5. Build remediation plan
- Order by risk reduction and dependency.
- For each worthy finding include:
  - proposed change
  - migration/test/docs impact
  - validation command(s)
  - rollback note if migration-affecting

## Worthiness rubric

Prefer `fix-now` when:

- finding indicates likely security boundary weakness
- finding indicates high-probability production performance issue
- effort is low/medium and validation is straightforward
- issue affects critical paths (auth, hot queries, write-heavy tables)

Prefer `defer-with-rationale` when:

- recommendation is likely workload-dependent and evidence is missing
- recommendation conflicts with known intentional architecture
- effort/risk is high and impact is uncertain

Prefer `ignore-with-rationale` when:

- recommendation is clearly not applicable to this project shape
- recommendation is a duplicate or superseded by existing controls

## Output format

Use this exact structure:

```markdown
Scope:
- focus: <all|security|performance>
- threshold: <error|warn|info>

Splinter summary:
- total findings: <n>
- after filtering: <n>
- fix-now: <n>
- defer: <n>
- ignore: <n>

Finding triage:
1. `<finding title or id>` — `<fix-now|defer-with-rationale|ignore-with-rationale>`
   Reason: <why>
   Evidence: <CSV row summary or SQL context>

Worthy items to resolve now:
1. `<finding>`
   Change: <what to change>
   Impacted files: <paths>
   Validation: <commands>
   Rollback: <note if needed>

Suggested implementation plan:
1. <step 1>
1. <step 2>
1. <step 3>

Deferred items:
1. `<finding>` — <why deferred and what evidence would unblock>
```

## Guardrails

- Do not auto-apply DB changes unless user explicitly asks to implement.
- Do not label an item `fix-now` without a concrete validation path.
- Call out assumptions (for example unknown workload or missing query stats).
- Keep recommendations tied to project context, not generic best-practice-only advice.

## References

- Splinter repository: [https://github.com/supabase/splinter/tree/main](https://github.com/supabase/splinter/tree/main)
- Splinter SQL: [https://raw.githubusercontent.com/supabase/splinter/refs/heads/main/splinter.sql](https://raw.githubusercontent.com/supabase/splinter/refs/heads/main/splinter.sql)
- Supabase CLI status output formats: [https://supabase.com/docs/reference/cli/supabase-status](https://supabase.com/docs/reference/cli/supabase-status)
