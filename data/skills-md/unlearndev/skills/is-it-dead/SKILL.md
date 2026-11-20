---
name: is-it-dead
description: Prove whether one file, function, endpoint, job, flag branch or package is really dead before deleting it. Runs the DEAD checks (Direct callers, Every other way in, Anyone outside, Data from production), checks the story in git history, has a fresh context argue that it's still used, then gives a verdict of DEAD, ALIVE or NOT PROVEN. Deletes only on a DEAD verdict and the user's yes, one item per commit. Use when the user asks "is this dead", "can I delete X", "is X still used", or wants to remove code safely.
argument-hint: "<file, symbol, route or package>"
disable-model-invocation: true
allowed-tools: "Bash(git log:*), Bash(git show:*), Bash(git blame:*), Bash(git status:*), Bash(git ls-files:*), Bash(git grep:*), Bash(git rev-parse:*), Bash(npx -y knip:*), Bash(npx knip:*), Bash(ls:*), Bash(cat:*), Bash(find:*), Bash(grep:*), Read, Grep, Glob"
---

# Is it dead?

## Arguments

Raw arguments: $ARGUMENTS

The arguments name **one candidate**: a file, a function or class, an export, a route, a job, a feature-flag branch, a config key or a package. If they're empty, ask which candidate to check (if a `/cruft-hunt` report is in the conversation, offer its "Start with" items) and stop.

## Goal

Decide, with evidence, whether the candidate is **DEAD**, **ALIVE** or **NOT PROVEN**, and only then, if the user agrees, delete it safely.

An agent's confidence is not evidence. Searching for the name and finding nothing is not proof: the name isn't the only way in. Every claim in the report must point at something the user can check.

DEAD is the checklist:

- **D · Direct callers**: real callers in the code. A test is not a caller.
- **E · Every other way in**: strings, folder scans and globs, config, scripts, CI, framework conventions.
- **A · Anyone outside**: email links, webhooks, public routes and files, embeds, other services, old app versions.
- **D · Data from production**: any sign it runs? The evidence has to cover the slowest cycle the code could run on.

Then two habits: **check the story** (why was it added?) and **one item per commit**.

## Instructions

### 1. Pin down the candidate

Work out exactly what it is and every name it could be reached by: file path, exported names, the route path (`/r/:code`), the job or template name as a string (`'order-shipped'`), the package name and what it's imported as, kebab/snake/camel variants. You'll search for all of them.

### 2. D · Direct callers

Search the whole repo for imports, calls and references to every name from step 1: all languages, templates and config included (`git grep -n`, `Grep`). For JS/TS also run `npx -y knip --no-progress` and `npx -y knip --production --no-progress` and note what they say about the candidate.

Classify every hit:

- **Real caller**: production code that uses it.
- **Its own test**: doesn't count. A test is not a caller.
- **Another candidate**: dead code calling dead code doesn't count. Say so.
- **Mention**: a comment or doc, not a use.

If there's a real caller, the candidate is ALIVE: skip to the report. **One exception: called, but for nothing.**

**Called, but for nothing?** For a shim, a guard, a fallback, an option or one side of a feature flag, being called isn't the question. The question is whether the **path** can still run: is there any input, stored data or flag value left that takes it? A shim for a data format that's been migrated, an option no caller passes, or the off side of a flag that's at 100% in production can be called on every request and still be dead. Judge the path, not the call: run the remaining checks against the path, and if nothing can take it, the verdict is DEAD. The deletion removes the path (plus the call, if the whole function is the path).

### 3. E · Every other way in

Look for ways in that don't use the name as an import:

- The name or path **as a string**, including built-up strings (template literals, `'jobs/' + name`) and other casings.
- **Folder scans and globs**: `readdir`, `glob`, `import.meta.glob`, `require.context`, auto-discovery by naming convention (jobs, commands, listeners, policies, migrations, plugins). If the candidate sits in a scanned folder, it's loaded.
- **Config and tooling**: config files, `package.json` / `composer.json` scripts, CI workflows, Dockerfiles, crontabs, infrastructure code.
- **Framework conventions**: file-based routes, service providers, DI containers, event subscribers, reflection.

### 4. A · Anyone outside

Could something outside this repo call it?

- Routes and endpoints, especially public or cross-origin ones.
- Webhooks from third parties.
- Links in emails and notifications (unsubscribe, magic links, "view in browser").
- Files served as-is (`public/`, embed scripts) that other sites load.
- A library's exported API, mobile apps, other services, old clients that never update.

Read `docs/`, `README*` and any API specs. If it's reachable from outside and you can't see every caller, you can't call it DEAD from code alone. You need production data.

### 5. D · Data from production

Look for runtime evidence in the repo: an `ops/` folder, exported logs, route-hit or analytics CSVs, job-run histories, feature-flag exports, coverage reports. Use it.

- **Check the window.** Find how often the code could run (cron schedule, billing cycle, seasonal or year-end logic). 30 days of logs say nothing about a job that runs once a year.
- **Feature flags:** use the production value, not the local default. A branch that's off locally may be at 100% in production, and the other branch may be the dead one.

If there's no runtime evidence, don't guess. Say exactly what would settle it (which log, which dashboard, which time window).

### 6. Check the story

- `git log --follow --format='%h %ad %s' --date=short -- <file>`
- `git log -S '<name>' --format='%h %ad %s' --date=short`
- `git blame -L <range> <file>` on the lines in question, then `git show <hash>` for the commit that added them.

Read the commit messages and any docs they point to (incidents, ADRs). Why was it added? Was it replaced by something else (a ghost)? Did the migration a shim waits for already run? Was it added to fix a real incident? Code that looks unnecessary but was added on purpose is ALIVE until the reason is gone.

### 7. The defence, in a fresh context

Have a context that hasn't seen your findings argue the other side.

- **In Claude Code**: spawn a subagent with only this brief (not your findings):

  > In the repository at `<repo root>`, find any evidence that `<candidate>` is still used or still needed. Look for imports and calls, the name or path as a string, folder scans and globs that would load it, config, package scripts, CI, framework conventions, routes or files that something outside the repo could call, links in emails, docs, git history (why was it added?), and any production evidence in the repo (logs, analytics, flag or job exports). Don't decide whether it's dead. Report each piece of evidence with `file:line`, a command and its output, or a commit hash. If you find none, say "No evidence found" and list where you looked.

- **Elsewhere**: print that brief in a code block for the user to paste into a new session, and mark the verdict *provisional* until they do.

Wait for the defence to report back before you write any of the report. Don't announce that you're waiting.

### 8. Verdict

- **DEAD**: no real callers, no other way in, nothing outside can reach it (or production data shows it unused across the full cycle), the story explains why it's left over, and the defence found nothing.
- **ALIVE**: any check found a real use or a live reason for it to exist. Say which.
- **NOT PROVEN**: you found no use, but a check couldn't be completed: outside callers you can't see, or no runtime evidence covering the cycle. Suggest a **tombstone**: a one- or two-line log in the repo's language that fires if the code runs, and how long to wait before deleting.

Never round NOT PROVEN up to DEAD.

### 9. Output the report

Use this format exactly:

```
## ⚰️ `src/billing/invoicePdfV1.ts`

**D · Direct callers:** none. `git grep -n renderInvoicePdf` finds the definition and `src/billing/invoicePdfV1.test.ts` only. A test is not a caller. knip --production lists it as unused.
**E · Every other way in:** none. Not in a scanned folder, no string references, not in scripts or config.
**A · Anyone outside:** none. An internal helper, not a route or public file.
**D · Data from production:** not needed. No route or job can reach it; `/invoices/:id.pdf` uses `renderInvoice.ts` (src/routes/invoices.ts:7).
**Story:** added in 91b07fe "Add PDF invoices" (3 Mar), replaced two days later by 4c2e9a1 "Render invoices in a worker so big orders don't time out", which switched the route and left this file behind.
**Defence (fresh context):** no evidence found. Looked at imports, strings, scripts, config, docs, logs.

**Verdict: DEAD.** An abandoned first approach, kept alive only by its own test.

Delete it? One commit: the file and its test. Afterwards I'll re-run knip to see what that frees up.
```

For ALIVE, end with the line that proves it:

```
**Verdict: ALIVE.** Called from outside the repo: the iOS app calls it (docs/mobile-api.md), and logs/requests-30d.csv shows 4,210 requests with an `iOS/` user agent.
```

For NOT PROVEN, end with the tombstone and the wait:

```
**Verdict: NOT PROVEN.** Nothing in the code calls it, but it's a public route and there's no production data for it.

Tombstone (server/routes/legacy.ts:12):
    console.warn('[tombstone 2026-11-09] GET /api/v1/feed still called', c.req.header('user-agent'))
Delete if it stays silent for 30 days.
```

### 10. Delete (only on DEAD, and only after the user says yes)

- Remove the candidate and **only its own** tests, fixtures and registrations (imports of it, a line in an index, its entry in a list). For a package, use the package manager (`npm uninstall`, `composer remove`, `uv remove`, …) so the lockfile updates.
- **Don't edit any other test.** Don't refactor, rename or tidy anything else.
- Run the project's checks: find them in `AGENTS.md`, `CLAUDE.md`, `README*`, or the manifest's scripts (typecheck, tests, build, lint).
- If anything fails, **stop**, put the files back (`git restore` / `git checkout --`), and report what failed. Never make a check pass by editing a test.
- Commit just this change: `Remove <candidate>` with a one-line body saying why it was dead.
- Re-run the dead-code tool and list anything that's **now also unused** because of this deletion (the cascade). Don't delete those; they each need their own check.

## Rules

- **One candidate per run.**
- **Evidence on every line**: a `file:line`, a command and what it returned, a commit hash, or a row from a production export.
- **A test is not a caller.** Neither is other dead code.
- **Never conclude DEAD from a name search alone.** Do all four checks, the story and the defence.
- **NOT PROVEN is a real answer.** Don't round it up.
- **Delete only on DEAD, after an explicit yes**, one item per commit, with no other changes.
- **Never edit or delete a test that isn't the candidate's own** to get the checks passing.
- **No preamble.** Start with the `## ⚰️` heading.
