---
name: coordinating
description: Conventions for running work across agents in Orca or T3 Code — sizing a task, picking model and effort, briefing helpers and workers, waiting without polling, handoffs, decision files, landing PRs. Load before spawning any helper, worker or delegated task, picking a model for one, coordinating a run, working a dispatched task, or handing off.
---

# Coordinating agents

The host app owns the mechanics: how agents are spawned, isolated, awaited and messaged.
This skill covers what to spawn, on which model, with what brief, and how to keep the
coordinator's context small. Commands live in the host map; load it now:

- `delegate_task` / `t3_*` tools available → T3 Code (even if `ORCA_*` env vars are set):
  [references/t3.md](references/t3.md)
- Otherwise `ORCA_WORKTREE_ID` set, or an Orca dispatch brief → Orca:
  [references/orca.md](references/orca.md)

| Situation | Section |
|---|---|
| About to spawn a helper, worker or delegated task | 1–3 |
| Coordinating a run of tickets | 4 |
| Working a task someone dispatched to you | 5 |
| Taking over, or rotating to a fresh session | 6 |
| A choice only the user can make | 7 |
| QA verify / fix on staging | 8 |

## 1. Size the task

Smaller is the default. When torn between two sizes, start smaller and step up on evidence:
the same check failing twice, or the task proving bigger.

| Size | Typical signal | Crew |
|---|---|---|
| **XS** | Typo, copy, config value, dependency bump, rename. | The agent alone, Light. |
| **S** | Clear task, one area, testable as written. | The agent alone, Mid; it checks its own work. |
| **M** | Several files, or a gap in the spec. | A planning pass first, a QA pass after. |
| **L** | Cross-cutting, new feature, schema change, new UI surface. | Planner to split it, builders for the parts, designer for UI, a reviewer per PR. |
| **Risky** (adds to any size) | Auth, payments, migrations, data deletion, secrets, public API. | An advisor before building, a second-family reviewer after. |
| **Unknown-cause bug** | Broken, cause unknown. | Diagnose first (`diagnosing-bugs`); build once the cause is reproduced. |

## 2. Pick model and effort

Name the model and effort on every launch: an unnamed child inherits its parent's, so a
heavy coordinator quietly spawns heavy children. The tiers live in
[models.yaml](models.yaml), with a Claude and a Codex model for each; read it now
(`~/.config/coordinating/models.yaml` replaces it when present: the user's own picks). With the
optional guard hooks installed ([SETUP.md](SETUP.md)), a delegate or Orca launch whose model
is not listed there, or that names no effort, is denied.

| Tier | Claude | Codex | For |
|---|---|---|---|
| **Light** | Haiku, low | `gpt-6-luna`, low | XS work, summarising logs or CI, mechanical sweeps, re-checks, re-reviews. |
| **Mid** (default) | Sonnet, medium | `gpt-6.1-sol`, medium | S/M building, QA, tests, design-system work, routine review. |
| **Heavy** | Opus, high | `gpt-6.1-sol`, high | Coordinating, planning, strategy, advice, diagnosis, L building, review of Risky changes. |

- **Your family first.** A helper runs on your own family's model for its tier. Your native
  subagent tool reaches only your family (Claude → Claude, Codex → Codex); the other family
  goes through `delegate_task` (T3) or `worker-start --agent` (Orca).
- **Second family** = the other family from yours (Claude coordinating → Codex; Codex
  coordinating → Claude), at Mid, or Heavy when Risky. It catches different things. Codex is
  also a good builder for backend or algorithmic S/M work.
- Heavy is the ceiling. When a Heavy advisor and a second-family reviewer disagree, put both
  verdicts to the user as a decision (section 7).
- Review rounds run on Mid (Heavy or second family when Risky). A re-review runs on Light
  and gets only the new commits plus the earlier findings.
- models.yaml wins over this table if they ever differ; ids not in it need an
  `extra_allowed` entry first.

## 3. Helpers and briefs

Most tasks need none. A helper is your own subagent by default; use a separate worker or
thread when it needs its own worktree, a different agent family, or must outlive the session.

| Role | Reach for it when | Tier | Gets back |
|---|---|---|---|
| **Builder** | Something needs building. | By size | The change (PR/diff) and a short summary. |
| **Planner** | M/L, or the path isn't obvious. Read-only. | Heavy | One-page plan: files, steps, tests, risks; for L, the split. |
| **Strategist** | Ordering a backlog, cutting scope. Product docs, not code. | Heavy | Order and cuts; open choices as a section 7 brief. |
| **Designer** | New or changed UI. | Mid; Heavy for a new pattern | UI spec covering empty/loading/error/success, or a throwaway prototype. |
| **QA** | Acceptance needs checking in a running app, device or suite. | Mid; Light for re-checks | Pass/fail per criterion with evidence paths. |
| **Advisor** | A Risky or ADR-level choice, or a builder stuck twice. Brief it without your preferred answer. | Heavy or second family | The pick, why, and the risk that would change it. |
| **Reviewer** | A PR worth a second look (always for L or Risky). Diff only (`code-review`); app checks belong to QA. | See section 2 | Findings by severity, then approve / changes-needed. |
| **Diagnoser** | Bug with unknown cause (`diagnosing-bugs`). | Heavy | Root cause, a failing test, suggested fix. |

Every brief is self-contained, because a child sees none of your history:

- **Target:** the issue number(s); tell it to read the issue, the issues it cites as "Decided
  in", the glossary and the relevant ADRs. The glossary is `GLOSSARY.md` (`GLOSSARY-MAP.md`
  points to one per context when there are several), or `CONTEXT.md` in repos on the older
  convention; read whichever exists.
- **Change:** what to build plus every acceptance criterion. Paste the triage "Agent brief"
  if there is one, never whole issue threads.
- **Constraints:** glossary vocabulary, ADRs, AGENTS.md language rules, the ticket's scope.
- **Ownership:** its own worktree and branch; one PR against `main` with `Closes #<n>`.
- **Observable acceptance:** the tests the change affects and the project's check commands
  pass; the full suite runs on the PR (section 5); report the PR link.
- **Answer shape:** a few lines back, detail in a file.

## 4. Coordinating

**Setup**
1. Read AGENTS.md, the glossary (`GLOSSARY.md`, `GLOSSARY-MAP.md` or `CONTEXT.md`), docs/adr/
   and docs/agents/. Source code is the workers' job.
2. Start the handoff file (section 6) and note the run or thread ids in it right away.
3. Work out the **frontier**: open `ready-for-agent` tickets with no open blockers (GitHub:
   `gh api repos/<owner>/<repo>/issues/<n>/dependencies/blocked_by`). Size each (section 1).
4. Raise anything that needs the user (`ready-for-human`, vendor/legal/hosting choices) at once
   as a section 7 brief, and keep it out of the wave.

**Waves**
- At most 5 workers at a time, each in its own worktree from `main`. Follow the brief's
  priority list (go-live critical path first).
- Before starting a worker, list existing worktrees, workers and threads (host map). One
  already on that ticket gets only the new instructions; send each brief once.
- Group closely related tickets touching the same code into one worker.

**Waiting**
- After dispatching, end the turn and idle. The host wakes you when something arrives (host
  map). Read messages once per wake, process all of them, and send every reply, release and
  ack in one chained call.
- Every check runs on a wake: no `sleep`, `until` or `for` loops, and no status check
  without one. CI: `gh pr checks <n> --watch` in a background shell call.
- A worker reporting the task is bigger than briefed gets a model step up or a helper, not
  another attempt on the same tier.
- Reviews come back as a reviewer's verdict; the coordinator keeps diffs and logs out of its
  own context.

**Device loops** never run in the coordinator or a builder. Every emulator, simulator or
browser tap → look → tap sequence goes to a QA helper (Mid; Light for re-checks) with the
acceptance criteria and the device id. The helper reads the accessibility tree before any
screenshot and runs each tap, settle and read as one shell call (host map).

**Landing**
- Merge only with the user's go-ahead: at a wave boundary, list each ready PR with a one-line
  summary and ask once.
- Wave-boundary report: done (tickets, PRs) · in flight · blocked, and on what · next wave.
- Release settled workers. Remove each worktree once its PR merges.
- Start each wave with a fresh coordinator from the handoff file (section 6).

## 5. Working a dispatched task

1. Do only the task. Read the issue and its "Decided in" issues, the glossary (`GLOSSARY.md`,
   `GLOSSARY-MAP.md` or `CONTEXT.md`), the relevant ADRs and AGENTS.md.
2. Bring in helpers only when the size calls for it (sections 1–3), naming their model.
3. Build it and add tests to the existing harness. While building, run only the tests the
   change affects: the touched files' tests, their package's suite, or the runner's own mode
   (`vitest related <files>`, `jest --findRelatedTests <files>`, `pytest <paths>`,
   `go test ./<pkg>/...`), plus the project's lint and type-check. The full suite is slow:
   leave it to CI on the PR, or run it once just before opening the PR when the project has
   no CI. UI verification goes to a QA helper; you get back the verdict.
4. If the task is bigger or harder than briefed, tell the coordinator what you learned. Two
   compactions on one ticket is that signal: write a short handoff note in the worktree and
   ask the coordinator to split the ticket or start a fresh worker from it.
5. Ask only what the issue, the glossary and ADRs leave open, batched into one question (Orca:
   `orca orchestration ask`; T3: end your result with it).
6. Open one PR (`pr` skill): `Closes #<n>`, acceptance criteria ticked. Merging is the user's.
7. Finish with a three-sentence summary plus the PR link, detail in a report file.

## 6. Handoff

Rotate, don't compact. At the first of these, write or update this file, then stop:
~250k tokens of context (Claude) or ~190k (Codex), any auto-compact warning, 25
orchestration rounds (`orca orchestration check` plus `delegate_task` calls), or a phase end
(plan → build → verify, a wave boundary). Numbers in your global instructions win. The
optional rotation hook ([SETUP.md](SETUP.md)) reminds you when you reach the token or round
limits.

- Path: `~/.<project>-coordinator/HANDOFF.md` for a coordinator,
  `~/.<project>-handoffs/<topic>.md` otherwise. Never the session scratchpad (it's deleted).
- Sections:
  1. The original brief, verbatim.
  2. Standing decisions and preferences, plus the decisions file path (section 7).
  3. Host state: run id, dispatches and terminals (Orca), or child thread links and task ids (T3).
  4. Repo state: branches, open PRs, uncommitted work.
  5. Environments: staging and prod URLs, credential *locations* (never values).
  6. Open items for the user.
  7. **START HERE**: the next 3–5 concrete steps.
- Coordinators append a dated notes section at every wave boundary.
- The new owner's prompt is a pointer: "You are taking over X. Read <file> in full first,
  especially START HERE. Preserve existing uncommitted work."
- Launch the new owner yourself (host map, "New owner"), reply with its link, then stop.
- A new owner, or any agent resuming after a usage-limit reset, reads this file and the
  decisions file before the next step.

## 7. Decisions for the user

- Write the questions to `~/.<project>-handoffs/decisions-<topic>.md` first: numbered
  `Q1…Qn`, lettered options `(a)/(b)/(c)`, your recommendation marked as the default on each.
  Send the user the same text plus the path.
- Record their answer in that file the moment it arrives, one line per Q with the chosen
  option and date. "Q1 a, Q2 b…" records those; "agree with all recommendations" (or
  "Aceito todas…") records every default. Then proceed through all of it without asking again.
- Cite `decisions-<topic>.md#Qn` when acting on a decision, and re-read the file after any
  compaction or rotation.
- Lasting decisions also go into an ADR (when the ticket asks) and the handoff file.

## 8. QA sweep

1. **Verify** on staging with `playwright-cli`. File one issue per defect with Area, Severity
   rationale, How established, Steps to reproduce, Expected, Actual, Evidence, Suggested
   direction and an "Agent brief"; label it `ready-for-agent`.
2. **Fix**: a coordinator dispatches builders (section 4).
3. **Re-verify**: a Light QA pass confirms each fix on staging and closes the issue, or
   reopens it with evidence.

## Standing preferences

- Do it yourself: run commands; use `computer-use` for GUI-only steps (router pages,
  dashboards, credentials from their browser).
- Fix dependencies properly (a release with the fix), never by patching `node_modules`.
- Clean up: release workers, remove merged worktrees, delete temp files.
