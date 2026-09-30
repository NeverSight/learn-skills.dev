---
name: ticket-generator
description: Generates a ticket (title + description, markdown only) from an engineering tripack, a raw report/finding doc, or directly from actual code changes (diff/branch compare) when no docs exist. Use this at the END of implementation work, right before pushing to a branch, or retroactively when work was already committed/pushed but no ticket was ever written. Always use when the user asks to "buat tiket", "generate ticket", "write a ticket for this change", or wants a ticket/task description derived from a tripack, a finding (e.g. dependency upgrade, SonarQube finding), or a diff/branch comparison. Do NOT use this for pre-work planning tickets (that's engineering-tripack-generator's task-plan) — this skill documents what was actually done or is actually changing.
---

# Ticket Generator

Produces a single ticket — **title + description, in markdown only** — that accurately reflects what was actually changed, not just what was planned. It runs post-implementation (or retroactively after a commit/push), so the source of truth is the real diff, with docs (tripack/finding) as supporting context.

## Step 0 — Required Input Gate (validate before doing anything else)

Do NOT ask the user interactively mid-run. Instead, inspect what was given in the invocation prompt, determine the scenario below, and if a required input for that scenario is missing, STOP immediately and tell the user exactly what's missing. Never guess a default (e.g. never assume `main` as base_branch).

**Inputs Claude looks for in the prompt:**
- `doc_path` — path to a tripack (technical-design/tactical-strategy/task-plan) or a raw report/finding doc. Optional depending on scenario.
- `base_branch` — a branch name to diff against (e.g. `main`, `develop`). If present, it is the **dominant signal** — see Scenario Detection.
- `output_language` — **REQUIRED, always.** Must be either `en` (English) or `id` (Indonesian/Bahasa Indonesia). If not specified anywhere in the prompt, STOP and ask the user which language they want before generating anything. This determines the language of the generated title + description (this SKILL.md itself always stays in English — only the *output* changes).

## Step 1 — Scenario Detection

Check in this priority order:

1. **`base_branch` given explicitly?** → **Scenario 3 (Retroactive / Branch Compare)**, regardless of whether `doc_path` is also given. If `doc_path` is present, treat it as *additional context only* — not the authoritative source of Goal/Scope. Diff source: `git diff base_branch...HEAD` (or the equivalent comparison against the current branch).
2. **No `base_branch`, but `doc_path` given AND the working tree has uncommitted/staged changes?** → **Scenario 2 (Docs + Diff)**. Diff source: working tree / staged diff. Implementation is done but not yet pushed.
3. **No `base_branch`, `doc_path` given, working tree is clean (no diff)?** → **Scenario 1 (Docs-only)**. No diff exists yet — ticket is generated purely from the doc. (Note: this is the pre-work case; confirm with the user this is intentional, since the skill's main use case is post-implementation.)
4. **None of the above clearly holds** → STOP. Ask the user to clarify which scenario applies (they've likely forgotten to pass `doc_path` or `base_branch`).

| Scenario | Required | Optional | Diff source |
|---|---|---|---|
| 1 — Docs-only | `doc_path`, `output_language` | — | none |
| 2 — Docs + Diff | `doc_path`, `output_language` | — | working tree / staged |
| 3 — Retroactive | `base_branch`, `output_language` | `doc_path` (context only) | `git diff base_branch...HEAD` |

## Step 2 — Gather the Real Change

- For Scenario 2/3: read the actual diff. Identify every file/function touched.
- Cross-reference touched files/functions against flow docs (from `flow-scanner`, if available in the repo) to determine which business flow(s) are impacted. Don't rely on file paths alone if a flow doc exists — it gives the authoritative file→flow mapping.
- If `doc_path` is also present, compare the *planned* scope (In Scope/Out of Scope from tripack) against what the diff *actually* touches. If there's a mismatch (diff touches something tripack marked Out of Scope, or vice versa), surface this explicitly in the description rather than silently trusting the doc.

## Step 3 — QA Impact Gate (conditional, not automatic)

QA Impact is **optional in every scenario** — including Scenario 1/2 with a tripack. Do not force it in and do not force it out; decide per case:

- Does the diff touch anything with **observable behavior** (API response, UI, user-facing flow, business logic)? → Include the QA Impact table.
- Is the diff purely internal (refactor with no contract change, comment/formatting, dependency bump with no breaking API change, internal renames)? → Skip the QA Impact section entirely. Add one line in the Description instead: *"No QA impact — internal change, no observable behavior change."*
- If genuinely ambiguous, default to **including** QA Impact rather than skipping it — a table that turns out to be light-touch costs less than a missed regression.

**QA Impact table format (always this table, never bullets):**

| No | Area | Yang dicek | Expected | Dikerjakan oleh |
|----|------|-----------|----------|-----------------|
| 1  | ...  | ...       | ...      | QA Engineer |

When `output_language` is `en`, translate the headers (`Yang dicek` → `What to check`, `Dikerjakan oleh` → `Owner`, `Expected` stays `Expected`). Role values stay the fixed tokens `QA Engineer` and `QA` in both languages — they are team roles, not prose.

- **Area**: the module/flow/endpoint actually touched (from Step 2's flow mapping).
- **Yang dicek**: the specific scenario to verify — prioritize edge cases exposed by the change (new-user path, old-data path, empty/zero cases), not just the happy path.
- **Expected**: the expected outcome per Acceptance Criteria — each AC can usually be split into 1+ regression rows.
- **Dikerjakan oleh**: exactly one owner per row. Assign it from the rules below. Do not ask the user, and do not leave the cell blank or write both roles in one cell. If one scenario needs both a product-surface check and a data/contract check, split it into two rows.
- If the diff is something like a dependency upgrade with no direct behavior change but still warrants a smoke check, one row is enough (e.g. Area = service name, Yang dicek = "smoke test after upgrade", Expected = "no errors, behavior unchanged", Dikerjakan oleh = `QA`).

**Who owns the row**

`QA Engineer` when the check cannot be closed from the product surface alone. Use this when verification needs data, contract, or runtime inspection:

- persisted data, migration, backfill, schema, or consistency across stores/services
- API contract, payload fields, status codes, or error codes
- technical data edges: empty, zero, null, legacy/old records, partial records
- idempotency, retry, concurrency, or ordering

`QA` when the check is product behavior a functional tester can verify without inspecting data stores, payloads, or logs:

- user-facing flow, UI, copy, or navigation
- business acceptance stated in user language
- smoke that behavior is unchanged, with no data inspection

If a row still does not fit cleanly, assign `QA Engineer` whenever any data or contract inspection is required; otherwise assign `QA`.

## Step 4 — Generate the Ticket

Output format — **markdown only**, title + description, written entirely in `output_language`:

```markdown
# [TYPE] Title

## Description
2–3 sentences: what changed and why. TYPE is one of FEATURE / BUGFIX / REFACTOR / CHORE.

## Goal
One outcome-oriented sentence.

## In Scope
- ...

## Out of Scope
- ...
(If Step 2 found a mismatch between planned and actual scope, note it here explicitly.)

## QA Impact
(Omit this whole section if Step 3 determined there's no QA impact — replace with the one-line note in Description instead.)

| No | Area | Yang dicek | Expected | Dikerjakan oleh |
|----|------|-----------|----------|-----------------|
| 1  | ...  | ...       | ...      | QA Engineer |

## Acceptance Criteria
- ...

## Related
- Links/paths to doc_path, flow doc, delta report, task-plan, or the compared branch — whatever was actually used as input.
```

Notes on generation:
- **Title**: concise, action-oriented, prefixed with the TYPE tag.
- Do not include a "Progress" / done-vs-todo checklist section — this skill runs after work is finished (or retroactively), so there's no pending-work state to report. If the user explicitly says some planned tasks were deferred/skipped, mention that under Out of Scope, not as a separate section.
- For Scenario 3 with no `doc_path`, Goal/In Scope/Out of Scope are **reconstructed from the diff and commit history**, not verified against an original intent. Say so plainly, e.g. (in the output language): *"Goal & scope reconstructed from commit history — not verified against original intent, please review."*

## Related
- Upstream in the chain: `flow-scanner`, `spec-delta-analyzer`, `engineering-tripack-generator`, `sonar-report-generator`, `go-task-executor`.
- This skill is meant to run right before push — it does not modify code, branches, or commits. It only reads and reports.