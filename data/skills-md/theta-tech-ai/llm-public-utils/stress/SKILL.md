---
name: stress
description: "Stress-test apps (especially webapps) — confirm reliability, comb happy paths, cause mischief, run a panel of distinct first-time users, and hunt bugs in code — via agent browser, API scripts, or both. Use whenever the user wants to find bugs, edge cases, knots, break an app, harden UX or APIs, QA a flow, run launch or onboarding QA, test what confuses real users, simulate different users or personas, or catch issues before users do — even if they only say try the app, test this, hit the API, or see what breaks."
---

# Stress: Unearth Bugs Before Users Do

A stress run is **sequential**, not a pick-list: prove the happy path works, groom it, attack it, then hunt the code. All of it hardens an app's *functionality* (not load/scale — that can be a future `load.md`):

| # | Phase | Temper | Question it answers |
|---|-------|--------|---------------------|
| 1 | **Reliability** (gate) | Patient happy-path repetition until it earns trust | Does the happy path *consistently* complete? |
| 2 | **Comb** | Gentle, repeated happy-path grooming | Where are the knots on and around the path? |
| 3 | **Mischief** | Hostile, out-of-order chaos | What breaks under abuse the system doesn't expect? |
| 4 | **Bug hunt** | Code-first, multi-angle review | What do layers, workflows, and data models hide? |

Run the phases **in order, 1-3 passes each** for the app-driving phases — the full shape lives in [process.md](references/process.md). A failed reliability gate *ends the run early*: there is no point combing or attacking a system that can't reliably do its one job.

Phase 4 is **code review, not app driving** — it never touches the running app, so it may run **in parallel** (a subagent reading code while you drive phases 1-3) instead of strictly last. Run any single phase standalone only when the user asks for exactly that (e.g. "just cause mischief"); otherwise the sequence is the default, and reliability is the entrance fee for everything downstream.

> **If the product is a webapp, start at the front door.** The user only ever touches the UI — every backend route, worker, and DB invariant exists to serve what renders in the browser. A pass that only probes the API or reads code is testing a surface no user sees; it will over-report backend defects and miss the UX, state, timing, and copy bugs that are what actually reach people. Default your *hands* to the agent browser for any webapp, and drive it like a real user, not a quick screenshot check. The frontend driving playbook in [driving.md](references/driving.md) is the core of doing this well.
>
> This is a **rebalancing, not a replacement.** The code-first ([bug-hunter.md](references/bug-hunter.md)) and API hunts find a different and equally real class — data loss, authz holes, races, audit/compliance gaps, silent corruption — that never shows up on screen until it bites a user. Keep doing that hunt; it's essential. The correction is only that it had been *crowding out* the front door: lead with the browser, then go deep on the backend too. Do both.

## Shared references (read these)

| File | When |
|------|------|
| [references/process.md](references/process.md) | **The standard run** — deployment lay of the land, then 1-3 reliability → 1-3 comb → 1-3 mischief passes |
| [references/driving.md](references/driving.md) | Choosing **browser vs API vs hybrid** — different surfaces catch different bugs |
| [references/findings.md](references/findings.md) | **What to do with bugs** (GitHub issues by default, artifacts, auto-fix) |

## Mode references (read the ones you will use)

- [references/reliability.md](references/reliability.md)
- [references/comb.md](references/comb.md)
- [references/mischief.md](references/mischief.md)
- [references/bug-hunter.md](references/bug-hunter.md)
- [references/personas.md](references/personas.md) — **the first-time-user panel** (5 independent persona agents, findings ranked by how many hit them, rerun to prove the fix)

## Before you start

1. Read **driving** + **findings** (+ **process** for a full run), then the mode file(s) for this pass.
2. **Get set up** — auth may live in env vars, docs, a local-dev skill, token scripts, or a bypass.
3. Pick a **drive surface** (browser, API, or hybrid) from [driving.md](references/driving.md). Webapp UX work → browser-heavy; contracts/concurrency/repetition → API-heavy; best results usually hybrid.
4. Confirm reporting only if the user contradicted [findings.md](references/findings.md).

## How to choose a mode

- **"Does it work?" / sanity check / pre-release confidence** → reliability
- **"Walk through the happy path" / "comb" / polish** → comb
- **"Break it" / "try to mess it up" / chaos** → mischief (optionally after one comb pass so you know the happy path)
- **"Review the code for bugs"** → bug hunter
- **"Test it as a real user" / launch QA / onboarding / "what confuses people" / "simulate N different users"** → the [persona panel](references/personas.md): independent first-time-user agents in parallel, merged into one list ranked by how many personas each defect hits, then a rerun of the identical panel to prove the fixes
- **"Hit the API" / contract / concurrency stress** → comb or mischief with an **API-first** drive plan
- **"Stress test this" / vague** → the standard run in [process.md](references/process.md): reliability first, then comb, then mischief; bug-hunt ugly code along the way

## Your job

Stress the system. Unearth bugs. Record them per [findings.md](references/findings.md) (or fix if asked). Summarize with links. Leave the app harder to break than you found it.
