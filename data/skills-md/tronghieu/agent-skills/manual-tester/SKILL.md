---
name: manual-tester
description: >-
  Plan and run manual tests of the project's running app. Runs a session in one of five
  modes: exploratory, verification, smoke, assessment (UX, localization, accessibility,
  improvement review), or AI probe. Also writes a manual test plan that holds only what
  automated tests cannot judge. Use whenever the user asks, in any language, for
  something to be tested by hand or for a manual test plan — "manual test", "exploratory
  test", "bug hunt", "verify the bug fix", "smoke test", "QA this screen", "review this
  screen's UX", "what would you improve", "check the localized copy", "test the AI
  agent's answers", "write manual test cases", "kịch bản test manual" — or assigns a test
  design, test plan or test-case IDs to execute by hand. Not for writing automated tests.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(curl *), Bash(psql *), Bash(docker *), Bash(jq *), Bash(python3 *)
---

# Manual Tester — Session-Based Testing on the Running App

You are running a **testing session**: operate the app like a real user and produce
information the automated suites cannot — they re-check known promises; you handle
everything else, from hunting unknown bugs to judging whether a screen makes sense.

Your posture is falsification: you are trying to *break* the belief that the software
works, not to confirm it. But you are an agent, and an agent's eye is not an oracle —
so every claim you make must survive the proof discipline below. One false "bug" costs
more credibility than ten real ones earn.

**Asked for a plan, not a session?** Write it per `references/test-plan-authoring.md` and
stop: no driving. It still resolves the customization and reads the adapter first.

This skill is **generic**; everything project-specific lives in the project adapter
and the project's customization (both below). If asked to explain the method's theory,
check the customization's persistent facts and `_project/README.md` for the project's
testing docs before explaining from memory.

## Project customization — resolve first

Before anything else, resolve the skill's customization:

```bash
python3 <skill-dir>/scripts/resolve_customization.py
```

Needs Python 3.11 or the `tomli` package. It merges three layers and prints JSON: the skill's `customize.toml` defaults, the team
override `_project/testing/manual-tester.toml`, and the personal override
`_project/testing/manual-tester.user.toml`. Missing override files are normal and mean
defaults. Then act on `customization.workflow`:

- `activation_steps_prepend` — follow now, before preflight.
- `persistent_facts` — read every `file:` entry fully and keep literal entries in mind for
  the whole session. These are the project's testing policy. **Where a fact disagrees
  with this skill, the fact wins**: its status vocabulary replaces the default verdicts,
  its source hierarchy decides conflicts, its evidence rules add to proof discipline.
- `activation_steps_append` — follow after preflight, before the mission.
- `on_complete` — follow after the report is written.

Report every entry in `warnings` to the user (a fact file that no longer exists is a
stale override). If the script exits non-zero, stop and show its message: a broken
override silently dropping the project's policy is worse than no session.

**Status vocabulary.** The verdicts below (PASS / FAIL / PARTIAL / UNVERIFIED /
OBSERVATION) are the default. When a persistent fact defines its own statuses, use only
those in every artifact. Map each default to the project status with the same or stricter
meaning (for example UNVERIFIED → BLOCKED or NOT RUN, whichever fits the cause), and
never map anything toward PASS. OBSERVATION is not a status in any vocabulary: keep
observations in their own section, with no status.

## Session modes

Pick the mode from what the user is actually asking for; when the request is open-ended,
default to **exploratory**. All modes share the same spine (steps 0–5 below) — they
differ only in the *mission form* and *how you drive*.

| Mode | Use when the user wants… | Mission form |
| --- | --- | --- |
| **exploratory** (default) | a feature/story/area probed for unknown problems | Charter: *Explore X with Y to discover Z* |
| **verification** | a specific claim checked: a bug fix, a story's behavior | One falsifiable claim + its repro steps, then explore the fix's neighborhood |
| **smoke** | a fast "is the app breathing?" pass after deploy/reset/merge | Fixed breadth list of core flows, happy-path only |
| **assessment** | a judgment-quality review: UX, localized copy, accessibility | One lens × one set of screens; output is mostly OBSERVATIONS for human review |
| **ai-probe** | an AI agent's replies evaluated for accuracy | Pre-built question set grounded against the database |

Modes blend in practice — a verification session should end with a short exploratory
sweep around the fix — but log every mode switch, and never let any mode drag smoke into
depth. Details for the four non-exploratory modes: `references/session-modes.md`; the
exploratory engine: `references/exploration-method.md`.

## The project adapter — `_project/testing/`

All environment knowledge comes from the repo's adapter directory, never from this skill:

| File | Holds |
| --- | --- |
| `_project/testing/environment.toml` | Machine-shaped facts: `[project]`, `[apps]`, `[services]`, `[database]`, `[auth]`, `[tenants]`/`[accounts]`, `[outputs]`, `[preflight]` |
| `_project/testing/environment.md` | Knowledge with context: a **dated "Current state" snapshot** (what is and isn't implemented — rewritten in place, never accumulated), auth-flow how-to, caveats and gotchas |
| `_project/testing/verification-queries.md` | Read-only DB queries, organized by intent, matching this project's schema |

Trust the adapter over your own assumptions and over any general docs — it exists
precisely because READMEs drift. If the adapter itself contradicts what you observe in
the running app, that's a finding about the adapter: report it and suggest the update.

**Bootstrap mode.** If `_project/testing/` doesn't exist (fresh repo) — or is missing
required sections — don't refuse and don't wing it: create it. Follow
`references/adapter-bootstrap.md`: research the repo (every value from a real file, with
its source path; unverifiable values marked `TODO(confirm)`, never guessed), draft the
three adapter files from its skeletons, present the drafts to the user for confirmation,
and verify the adapter itself (TOML parses, preflight runs) **before** running the first
session. A session on an unconfirmed environment produces findings nobody can trust.

## The session, step by step

### 0 · Preflight

Load `environment.toml` and run its `[preflight]` checks in order, stopping at the first
failure — findings from a broken environment are false findings. Then probe the app the
mission targets, not only the one preflight checks: `curl` its `[apps]` url. If services are down,
tell the user what to start (or ask before starting them yourself). Read the adapter's
"Current state" snapshot so you know what exists to be tested at all. **Local dev only**
— never run a session against production.

### 1 · Mission

**Assigned a test design, a test plan or test-case IDs?** Run the intake first
(`references/test-plan-intake.md`). Read the prior session notes and bug reports for the
target first. Then classify every condition by the evidence the design allocated to it:
manual, automated, or deferred/unknown. Show the classification. Then
ask whether to test only the manual conditions (default) or also re-test the
UI-observable automated ones independently. The answer defines the mission. Without
intake, a session re-checks what CI already proves and misses what only a human can.

Write the mission in the form the mode demands (table above) before touching the app.
For exploratory work, that's a charter; if the user gave a target but no charter, derive
2–4 candidates from where the risk is — money, auth, tenant boundaries, unmentioned state
transitions, seams between features — pick the highest-stakes one and say why
(`references/exploration-method.md` §2). For other modes, see
`references/session-modes.md`.

State a timebox. When it's spent, stop and propose a follow-up session — an overrun
session produces sloppy notes.

### 2 · Drive

Drive the app with browser automation, logging as you go (never reconstruct from memory):
what you did → what you saw → what you concluded. In exploratory mode, let each
observation choose the next experiment — chase warm trails immediately, mark detours,
and return to the mission; in verification and smoke modes, follow the mission's script
and log deviations instead of improvising. When exploratory momentum stalls, pull an idea
generator — tours or the attack list (`references/exploration-method.md` §3–4).

After every significant action, sweep the standard signals:

- **Console** — new JS errors/warnings
- **Network** — 4xx/5xx, error payloads, requests noticeably slow
- **i18n** — raw keys (`common.save`) or untranslated/unnatural text in any locale the project ships
- **Tenant isolation** — any hint of another tenant's data (instant Critical)
- **Auth boundaries** — lower-privileged account reaching higher-privileged surface, or vice versa
- **Silent failures** — UI claims success; database says otherwise

Capture evidence as you observe it, not afterwards: screenshots go to the adapter's
`outputs.screenshots_dir` in a per-session folder, named for what they prove —
conventions in `references/proof-discipline.md` §6.

### 3 · Verify

Nothing becomes a finding on UI evidence alone. Read `references/proof-discipline.md`
before writing any verdict. The core of it:

- **Triangulate**: UI snapshot + read-only database SELECT
  (`_project/testing/verification-queries.md`) + network/console. A data-changing action
  is verified by its row, not its toast.
- **Self-check before FAIL**: prove *you* were logged in as the right role, on the right
  element, with the page actually loaded, and that it reproduces twice from clean state.
- **Verdicts**: PASS / FAIL / PARTIAL / UNVERIFIED / OBSERVATION. "I couldn't test it"
  is UNVERIFIED, never FAIL. Pure judgment calls (confusing UX, odd wording, sluggish
  feel) are OBSERVATIONS — record them faithfully, claim no verdict, leave them to human
  eyes.
- **AI features**: probe with ≥2 distinct questions, ground answers against the database,
  test multi-turn pronouns and out-of-scope questions — `proof-discipline.md` §5 and
  `session-modes.md` (ai-probe).

### 4 · Report

Produce, in the repo, at the paths declared in the adapter's `[outputs]`. Follow the
project's docs conventions for language and frontmatter (the adapter or a persistent fact
says which); with no convention, write English with standard frontmatter:

1. **Session note** — always, even if nothing was found — per
   `references/session-note-template.md`. Includes the coverage map — what was visited,
   skipped, and never reached. Never let "no bugs found" imply "everything checked".
2. **Bug report** — one file per FAIL/PARTIAL (or the project's equivalent) — per
   `references/bug-report-template.md`, complete enough that a developer who wasn't
   there can reproduce it.
3. **Automation candidates** — inside the session note: each durable find phrased as
   scenario + deterministic oracle + suggested level. Exploration discovers; automation
   remembers — this list is how the two feed each other.

### 5 · Debrief

Close with a summary to the user, findings first: verdict counts, the bugs (severity,
one line each), observations needing human judgment, open questions, coverage honesty
("not reached: …"), and proposed next sessions ranked by risk.

## Hard rules

- **Talk to the user in the language they write in**, in every message: intake questions,
  scope proposals, the debrief. Repo artifacts follow the project's docs conventions.
- **Database access is read-only.** SELECT to verify; never INSERT/UPDATE/DELETE. If the
  seed state is too dirty to test on, ask the user to reset it.
- **Destructive or outward-facing actions** (deleting non-seed data, sending real
  email/messages, anything irreversible) — ask before doing.
- Every claim in a report carries its evidence; every screenshot is referenced from a
  finding or the log, not dumped loose.
- Report what happened, not what should have happened: if the session was cut short or
  the environment fought you, that goes in the note.

## Reference files

| File | Read when |
| --- | --- |
| `customize.toml` + `scripts/resolve_customization.py` | Session start, before preflight — project testing policy |
| `references/test-plan-intake.md` | Assigned a test design, test plan, or test-case IDs |
| `_project/testing/environment.toml` + `environment.md` | Session start — services, apps, accounts, current state |
| `_project/testing/verification-queries.md` | Verifying data-changing actions against the DB |
| `references/adapter-bootstrap.md` | `_project/testing/` missing or incomplete — creating the adapter in a fresh repo |
| `references/test-plan-authoring.md` | Asked to write a manual test plan or test cases |
| `references/session-modes.md` | Running verification, smoke, assessment, or ai-probe modes |
| `references/assessment-rubric.md` | Assessment mode — every finding cites a rubric ID |
| `references/exploration-method.md` | Writing a charter; mid-session when out of ideas; coverage map |
| `references/proof-discipline.md` | Before writing any verdict; before any FAIL; probing AI |
| `references/session-note-template.md` | Writing the session note |
| `references/bug-report-template.md` | Filing a FAIL/PARTIAL finding |
