---
name: code-review
description: Review C#/.NET code changes (.NET 8–10, ASP.NET Core and class libraries) for correctness, async/threading, EF Core, security, resource-lifetime, and API-contract defects, and present the findings as a visual HTML report with severity badges and before/after code. Use this skill whenever the user asks to review code, review a diff/PR/branch/commit, check changes before commit or merge, find bugs in recent changes, or asks "does this look right / anything wrong with this" about C# or .NET code — even if they never say the words "code review".
metadata:
  origin: dotnet-skills
  targets: .NET 8, 9, and 10 (ASP.NET Core and class libraries)
---

# Code Review (.NET)

Review a set of C#/.NET code changes for defects and present the findings as a self-contained HTML report. The goal is to catch bugs that would ship — not to enforce style.

This is a **read-only review**. Do not modify any source file. The output is the report plus a verdict in chat; fixing only starts if the user asks.

## Severity Rubric — Use These Levels Exactly

Every finding gets exactly one severity. Assign it by answering the decision question — not by gut feel.

| Severity | Decision question | Examples |
|----------|-------------------|----------|
| **Blocker** | Will this fail, corrupt data, or be exploitable in production under realistic conditions? | SQL injection, missing `[Authorize]`, `async void` handler, data race, saving unvalidated user input over an entity |
| **Warning** | Is there a realistic condition under which this misbehaves — or a resource/performance risk that grows with load? | N+1 query, `.Result` on the request path, `HttpClient` per call, swallowed exception, missing `CancellationToken` |
| **Suggestion** | Is there a strictly better idiom the author would almost certainly accept? | `Any()` over `Count() > 0`, `AsNoTracking` on a read path, `TimeProvider` over `DateTime.UtcNow` |

The verdict is mechanical: any Blocker → **Request changes**; no Blockers but ≥1 Warning → **Approve with reservations**; otherwise → **Approve**.

## Process

### 1. Determine the scope

Work down this list and stop at the first match:

1. **User named the target** (a PR number, branch, commit, or files) — review exactly that. For a PR use `gh pr diff <N>` and `gh pr view <N>`; for a branch use `git diff main...<branch>`.
2. **Uncommitted work exists** (`git status --porcelain` is non-empty) — review it with `git diff HEAD` (plus `git status` for untracked files, which you read in full).
3. **The branch is ahead of the default branch** — review `git diff <default>...HEAD` (three dots: only this branch's changes).
4. **Nothing above applies** — ask the user what to review. Do not review the whole repository unprompted.

Record for the report header: repo/solution name, branch, scope description (e.g. "uncommitted changes, 6 files"), and the diff stat (`git diff --stat`).

If the scope is not a diff (user pointed at files or a folder), review those files in full; everything in them counts as "changed" for the rules below.

### 2. Read the code — not just the diff

A diff hunk out of context is where false positives come from. For every changed file:

1. Read the **whole file** (or at minimum the full member containing each hunk plus the class's fields and constructor — that's where lifetime and threading bugs hide).
2. If a **signature, contract, or behavior changed**, grep for the callers and read enough of them to know whether they're now broken.
3. Note the file's role (endpoint, handler, entity, EF configuration, test, DI setup) — the checklist keys off roles.
4. Skim `Program.cs` / DI registration once per review: service lifetimes there decide whether many findings are real (e.g. a `DbContext` in a singleton).

If `dotnet` is available and the solution builds quickly, `dotnet build` is cheap evidence — a compile error outranks any reading. Skip it if the build is slow or the environment can't run it; never let it replace reading.

### 3. Hunt for defects

Read [references/review-checklist.md](references/review-checklist.md) **before** hunting — it contains the defect catalog with detection patterns, the reason each one is a bug, and correct-code replacements. Do not improvise checks from memory; the catalog's "when it's NOT a finding" notes matter as much as the detections.

Make one pass per category, in this order (highest payoff first):

| # | Category | One-line focus |
|---|----------|----------------|
| 1 | Async & threading | `async void`, sync-over-async, fire-and-forget, shared `DbContext` across tasks |
| 2 | Data access (EF Core) | N+1, injection via raw SQL, client-side evaluation, `SaveChanges` in a loop |
| 3 | Security | Missing auth, over-posting, path traversal, secrets, weak hashing, IDOR |
| 4 | Correctness | Null handling, culture/comparison traps, `decimal` for money, swallowed exceptions |
| 5 | Resources & lifetimes | Captive dependencies, `HttpClient` per call, undisposed `IDisposable`, static mutable state |
| 6 | API contract (ASP.NET Core) | Entities on the wire, wrong status codes, missing validation, middleware order |
| 7 | Performance | Sync I/O on the request path, allocation in hot loops, per-call `JsonSerializerOptions` |
| 8 | Tests | Behavior changed with no test touched, assertions that can't fail |

For every hit, record **evidence**: the file path, line number, and the exact offending line(s) quoted verbatim. A finding you cannot quote does not exist.

### 4. Verify and grade

Run every candidate finding through this gate before it reaches the report:

1. **Quote check** — re-open the file; the quoted code appears at the cited line.
2. **Handled-elsewhere check** — search for the guard you'd expect (caller validation, middleware, filter, `try/catch`, DI configuration). Only report if it's genuinely absent.
3. **Scope check** — the defect is in changed code. Pre-existing code is only reportable when the change makes it worse, or it's a security Blocker you can't responsibly omit (then label it "pre-existing" in the card).
4. **Scenario check** — you can state the concrete failure: *this input/state → this wrong outcome*. If you can't, downgrade one level or drop it.

Then apply the rubric, and cap the report: **at most 12 findings, at most 3 of them Suggestions.** If you have more, keep the highest severities and strongest evidence. Three verified Blockers beat twelve maybes — never pad, and never report style/naming/formatting at all.

### 5. Render the HTML report

Read [references/html-report.md](references/html-report.md) for the full scaffold, the finding-card template, code-snippet styling, and the escaping rules. Follow it closely — the scaffold is complete and tested; do not redesign it.

Mechanics:

- Write one self-contained HTML file to the OS temp directory — never into the repo. Resolve the temp dir from `$env:TEMP` (Windows) or `$TMPDIR`/`/tmp` (macOS/Linux); name the file `code-review-<yyyyMMdd-HHmmss>.html`.
- Open it for the user: `Start-Process <path>` on Windows, `open <path>` on macOS, `xdg-open <path>` on Linux.
- Tell the user the absolute path in your reply, in case auto-open fails.

Each finding card must contain: title, severity badge, category chip, `file:line` reference, the offending code (escaped, offending line highlighted), the fixed code, and a one-or-two-sentence "why" naming the failure scenario. The report ends with the verdict and a short ordered fix-first list.

### 6. Verdict in chat, then stop

After the report is written and opened, state in chat: the verdict, the severity counts, and the single most important finding in one sentence. Then ask:

> "Want me to fix any of these?"

Do not start fixing, do not stage or commit anything. If the user disputes a finding and their reason holds, concede it plainly — do not defend a finding the evidence doesn't support.

## Rules

- **Read-only until asked.** The review changes nothing in the repo.
- **Evidence or it doesn't ship.** Every finding quotes the actual code at a real `file:line`.
- **Bugs, not taste.** Style, naming, formatting, and "I'd have structured this differently" never appear — not even as Suggestions.
- **The diff is the subject.** Don't drift into reviewing the whole codebase; pre-existing issues follow step-4 scope rules.
- **Calibrated severity.** When torn between two levels, pick the lower one — an inflated Blocker costs more credibility than a missed Warning.
- **Empty is a valid result.** If nothing survives verification, say so, render the report with zero findings and an **Approve** verdict, and don't invent something to look useful.
