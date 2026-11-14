---
name: deliver-retro
description: Run a retrospective on one or more delivery runs (`deliver` or `flyingnobita-deliver`) and propose improvements to the delivery skill, its runtime checks and role profiles.
disable-model-invocation: true
---

# Delivery retrospective

The user has asked for a **retrospective** on delivery work. It combines a local
environment review adapted from Matt Pocock's `retro` with the layer a
multi-agent run adds: **coordination** (how the orchestrator ran its agents)
and **role split** (whether each piece of work landed with the right role). You
propose the smallest change to the delivery system that prevents each loss of
time, quality or authority next run, and track whether past fixes held.

The retro is read-only toward deliveries. It mutates no run record, pane,
worker, worktree or branch. It writes its own [ledger](references/ledger.md),
and, after the user's separate choice in step 9, TODO entries in the project's
chosen tracker. It edits skills or code only after the user picks candidates
for implementation; choosing to log a proposal is not that approval.

## Steps

1. Read and follow the local [environment review](references/environment.md)
   for the orchestrator's session and delivered repo. Hold its candidates for
   step 7 rather than presenting them now. Follow the [upstream comparison](references/upstream.md)
   to identify maintenance differences when an installed upstream copy is
   available; it is source material, not an instruction to execute `retro`.
   Done when every environment category has a candidate or an
   explicit clean or unavailable result, candidates are held for step 7, and the
   upstream comparison is recorded with its revision or its absence.

2. Resolve the runs. Default to the run this session orchestrated; otherwise
   the run ID, repo or branch the user names. "Recent runs" or a trend request
   means every run in the state root for the named repo, newest first. Read
   [evidence](references/evidence.md) and collect each run's primary sources,
   then read the [ledger](references/ledger.md) for past retros and their fixes.
   Done when each run's record, reports, branch history and orchestrator
   transcript are located, or each missing one is named with the reason.

3. Build a **timeline** per run: stages and user stops, then every task and
   attempt with its role, effective profile, start, settlement, report, verify
   result, follow-ups and recoveries. Done when every attempt in the run record
   appears on the timeline with an outcome.

4. Mark every **rework**: a plan revision, an attempt beyond a task's first, a
   review iteration beyond the first, a failed gate, a scope change, a worker
   report the independent run contradicted, and any correction the orchestrator
   or user made to a role's output. Trace each to its **origin**: the earliest
   stage and role that had the information to prevent it. Done when every rework
   has an origin, or is marked unattributable with the reason.

5. Run every check in [checks](references/checks.md) against the timeline and
   reworks. These complement the local environment review; a
   finding both cover is reported once, here. Done when every check ID has a
   finding or an explicit "clean, with evidence".

6. Turn environment and multi-agent findings into candidates, using the ledger's history:
   - A finding matching a past candidate (same check ID and owning file) is a
     **recurrence**. If that candidate was implemented, its fix did not hold:
     raise its severity one level and step its fix type up the ladder below.
   - An implemented past candidate whose measure the new runs satisfy has
     **held**; report it in one line.

   Choose the strongest **fix type** that removes the finding, in this order:
   1. **Runtime check**: a deterministic refusal in `deliver-runtime` or
      `deliver-orca-preflight` (the deliver skill's `scripts/`), with a test in
      the delivery repository's `tests/`. Use for a **mechanical** finding
      (a missing field, an unverified state passing a gate, a duplicate dispatch) that
      recurs, or whose first occurrence passed a gate. The candidate states the
      refusal condition, the command that refuses, a test case built from this
      run's evidence, and any legitimate run it could wrongly refuse.
   2. **Skill text**: a sharper step, completion criterion or role brief in the
      file that owns the behaviour (table below). The default for a first
      mechanical finding that passed no gate.
   3. **Profile**: a role's harness, model, effort or mode.
   4. **Project rule**: the delivered repo's `AGENTS.md` `## Delivery` section,
      `docs/agents/delivery.toml`, or a repo check from step 1.
   5. **Dependency**: an upstream `mattpocock-*` skill; record the contract
      change in [dependencies](../deliver/references/dependencies.md).

   | Behaviour | Owning file under `skills/deliver/` |
   |---|---|
   | Stops, stage order, orchestrator vs role edits, ticket split rule | `SKILL.md` |
   | Brief, grilling depth, size route | `references/intake.md` |
   | Role briefs, build and red-check gates, ticket graph merges | `references/pipeline.md` |
   | Review classification and repair loop | `references/review.md` |
   | Frontier, questions, human work, partial runs | `references/scheduling.md` |
   | QA guardrails and method | `references/qa.md` |
   | Landing and publication | `references/ship.md` |
   | Concurrency, landing and role settings | `references/configuration.md` |
   | Native operations, waits, permissions, recovery | `adapters/<host>.md` |
   | Herdr default profiles | `references/herdr-profiles.toml` |
   | Herdr project role profiles | the delivered repo's `docs/agents/delivery.toml` `[hosts.herdr.roles.<role>]`, changed through `deliver-setup` (or `flyingnobita-deliver-setup`) |
   | Paseo shared profiles | Paseo profile configuration (daemon / MCP) |
   | Orca default profiles | `references/orca-profiles.toml` |
   | Orca project role profiles | the delivered repo's `docs/agents/delivery.toml` `[hosts.orca.roles.<role>]`, changed through `deliver-setup` (or `flyingnobita-deliver-setup`) |

   Done when every candidate names one fix type, one owning file and a
   **measure**: the observable in the next run's evidence that shows it worked.

7. Present the candidates in severity order:
   1. **Authority**: a gate passed on unverified evidence, a role or the
      orchestrator acted beyond its approval, or a stop was skipped.
   2. **Correctness**: a defect shipped, or was caught only by QA, CI or the
      user.
   3. **Rework**: loops and revisions, ranked by elapsed time lost.
   4. **Waste**: idle time, duplicated legwork, oversized context.

   Give each candidate as: title; check ID; evidence (run ID, attempt or report
   path, timestamp or transcript line); origin; recurrence count; fix type and
   owning file with the proposed wording or check; measure. Merge the held
   environment candidates into the same order, labelled by their
   category. Then give the trends from the ledger: recurring findings, fixes
   that held, and the gate yield and profile fit tables from checks R7 and R9.
   Display duration columns as hours and minutes (`Hh Mm`), for example
   `337` minutes as `5h 37m` and `22` minutes as `0h 22m`. Round fractional
   minutes once to the nearest whole minute before splitting into hours and
   minutes. Preserve qualifiers such as `≥`; show unknown time as unknown,
   never zero. Keep numeric minutes in the ledger for calculations.
   End with the clean checks in one line.

8. Write this retro's ledger entry, with every candidate `proposed`. Done when
   the entry exists and the user has the candidate list.

9. End the retro with one offer to store its remaining TODOs in the project's
   chosen tracker. Name the destination and concrete candidate IDs/titles;
   offer all, selected IDs, or none. Include already accepted but unfinished
   work, and exclude completed, declined and duplicate items. If no TODOs
   remain, state that instead of offering empty work. If the destination is
   unknown, ask for it with the same offer; preserve an explicit `none` choice.
   The user may answer later. Until then keep the candidates in the ledger
   without writing external tracker entries or assuming consent from silence.

   On acceptance, use the shared [outstanding-work procedure](../deliver/references/outstanding.md):
   search for existing work, create/update the selected entries, read them back
   and return their links. Record each candidate's `tracker_refs` in the ledger.
   Logging proposed candidates keeps them `proposed`; implementation approval
   remains separate. If a write fails, retain the TODOs in the ledger and name
   the unsaved items. Done when the offer is presented and its pending,
   declined or verified-saved outcome is explicit.

When the user picks candidates, update their ledger status. Implement picked
candidates in the delivery repository under `skills/` or `tests/`,
or the delivered repo for project rules, with a CHANGELOG entry, commit
following repository commit rules (or a configured custom commit skill),
and record the commit in the ledger. Publication is a separate request.
