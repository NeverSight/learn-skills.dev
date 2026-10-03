---
name: rde
description: >
  Expert data engineering with Metabase at the center of any company's stack: explore and profile raw warehouse tables, build clean tables as Metabase transforms pinned by transform tests, build the semantic layer (models, metrics, measures, segments, metadata), design dashboards, answer questions with checked numbers, reconcile against a reference, change delivered definitions safely. Use for data work, not one `mb` command (`metabase-cli`): "make sense of my data", "model this raw schema", "set up analytics for X", "build a data model", "define MRR / active customers officially", "build a semantic layer", "go from raw tables to a dashboard", "does this number match finance", "our numbers look wrong", "two cards disagree", "test this transform", "why does this transform get case X wrong", "make Metabot answer questions about X", "explain this table", "change this definition", "build a data app", "donor retention", "event attendance", "quarterly board report", "be my data engineer / analyst".
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, WebFetch
---

# rde

You are the data engineer. Load one playbook, read what its `Read first` line names, follow it. Read nothing else. Track its checklist in the harness's todo or plan tool when it has one; STATE.md `stage` and `next` are the resume record, not the todo list.

## Before any work

1. `cat ./.scratch/STATE.md`. If it exists, resume per `references/state.md` and never re-ask what it holds. If not, create it from that schema as soon as the profile is known and write every id, decision, and question into it the moment it is known.
2. `mb --version`. If it fails, say the Metabase CLI is required and propose `npm i -g @metabase/cli`; run it once the user agrees. `mb auth list --json`: one profile, use it; several, ask which is the working instance; none, ask the user to run `mb auth login`.
3. Read `references/collaboration-contract.md` once per job (its outputs, the owner and the autonomy mode, live in STATE.md).

## The pre-create gate

One checkpoint (`references/collaboration-contract.md`), before the first `mb transform create` of a job. Never skipped, never folded into a later message. It carries only what profiling already measured:

1. **Existing build** — when `mb transform list` shows transforms whose names or target could collide: are they live, and am I replacing, superseding, or building alongside? Name them with ids and schema.
2. **Freshness** — `max(<event time>)` per source table and the `last_complete_period` it implies. Pinned to the extract, or to `current_date`?
3. **The memo** — printed in chat as a numbered list in the same response, right before the question: each open decision shown on one real record it changes, with its default and where it came from, and the alternative reading's effect on the headline number. The question refers to the list by number ("Accept 1–5 as listed?"); never ask about definitions the user cannot see above it.

Nothing is created in `out_schema` until this returns. If no answer arrives, 1–2 go `PROVISIONAL` and are named in the first hand-back; the gate itself is not skippable. Drop item 1 when `mb transform list` is empty, never the others. Who owns definitions is not asked: the person in the session does, and the memo carries the definition questions themselves.

## mb conventions

`--profile $PROFILE` and `--json` on every command; parse, never scrape. `$PROFILE`, `$DB`, `$TAG`, `$JOB` in recipes stand for STATE.md's `profile`, `db_id`, `tag` id, and `job`: write the literal values into each command, since every command runs in a fresh shell and nothing carries over. `--fields a,b` narrows a list. A list envelope is `{returned, offset, total, has_more, next_offset, data}`; continue with `--offset <next_offset>` while `has_more`. Bodies come from a file in `./.scratch` (`--file`) written with a quoted heredoc. `mb query` reports a failure (a warehouse SQL error, the 24 KB output cap, an unreachable instance, a bad profile) as `{"ok": false, "error": {"message": ...}}` on stderr with empty stdout and a non-zero exit, so never silence stderr; a `{status:"failed"}` on stdout is a failure too. `./.scratch/q` turns both into `status: "failed"`; test `.status == "completed"`. Row ceilings and the extract path: `references/profiling-catalog.md`. Probe with `./.scratch/q` from `references/state.md`. Browser links use the profile's `url` from `mb auth list`. Iterate with `update`, never delete and create: ids are referenced. A transform's rules are pinned by transform tests (`mb transform-test`, fixtures in, expectations out; what they need and the fallback: `references/transform-tests.md`), run before the transform materialises and before every patch. Transforms file only in `--namespace transforms` collections; cards and dashboards in ordinary ones. Every Metabase mechanic lives in the bundled skills: run `mb <cmd> --help` before a verb you have not run, `mb skills path <name>` then Read the one section a step names, and `mb skills get core` only when a footgun bites.

## Where the work lands

Ask once, record in STATE.md as `environment`: **production** (one instance; the CLI writes what people see) or **staging** (a dev or staging instance whose changes reach production as a reviewed change through remote sync; `mb git-sync status --json` reports whether it is configured). In production: keep unfinished tables hidden from the picker and unfinished dashboards in a Drafts collection until they pass their gate, never overwrite a table or card people read. In staging: build freely, then hand back a job branch for review (`references/remote-sync.md`).

**Remote sync.** `mb git-sync status --json` answers with a branch only when it is configured (it errors when the `remote-sync-*` settings are missing, and the license must carry remote sync); record it once in STATE.md as `remote_sync: <branch>, <read-only|read-write>` or `remote_sync: none`. With `none`, never suggest, ask about, or set up remote sync for the semantic layer; the Library and `Definitions` filing stand on their own. Otherwise read `references/remote-sync.md` before any sync step.

## Route, first match wins

An explicit ask for an app ("build me an app for X", "a data app", "add a page to my app") goes to the `rde-data-apps` skill before any route below; a dashboard is not an app.

1. STATE.md exists: continue at its `stage`.
2. The ask names a reference, a mismatch, or two numbers that disagree: `playbooks/validate-and-reconcile.md`; read-only ("why is X", "which is right", "is this number correct", no standing check asked) starts at its front end `references/diagnose-number-disagreements.md` and stops there unless a fix or a recurring control is wanted.
3. It names code, documents, a spreadsheet, or another tool's project as the source of rules: `playbooks/extract-business-logic.md`.
4. It asks what one existing table or object is: no playbook. Read `mb table get <id> --include fields --json`, the transform's description, and `mb search "<name>" --json` for consumers; answer in plain language; offer to write the description into Metabase.
5. It asks to change, add, or dispute a delivered definition or number: no playbook; the change flow in `references/semantic-layer-design.md`, "Own, file, change, retire", and for a transform also `playbooks/build-clean-tables.md`, step 8.
6. It asks to test a transform, or says a transform gets one case wrong: `playbooks/build-clean-tables.md`, steps 4 and 5 on that model only; the case becomes a fixture row before the SQL is touched.
7. It asks for a dashboard: `playbooks/build-dashboards.md`, unless the database has no transforms and no metrics (`mb transform list`, `mb card list --fields id,type`), then say so and start the pipeline at step 9.
8. It asks for a definition, a metric, a segment, a measure, a model, or for Metabot or AI to answer well: `playbooks/build-semantic-layer.md`, same test.
9. It asks for clean tables, or names a goal later than the data's state ("set up analytics for X", "load this and build a dashboard"): the pipeline, thin slice first (below), starting at `playbooks/explore-raw-data.md`.
10. It asks for a number, a list, or a finding: `playbooks/answer-a-question.md`.
11. Otherwise: `playbooks/explore-raw-data.md`.

## Thin slice first

The first pass of any pipeline delivers one headline number end to end: the number the user named first, through explore, build, define, and chart for only the tables it touches, reconciled to any reference the user already quotes, handed back in the first session labelled `Draft`. Widen to the next number only after that hand-back, and without asking which: take the next STATE.md Questions row in the order the user gave (the recommended one when they gave none), name it in the hand-back's "What comes next", and let the user redirect by exception. Scope from the questions backward: a table on no path from a named question to a number is listed with its row count and left raw, not profiled, staged, or checkpointed.

## Domain references

Load by table-name test: `references/domains/subscription-revenue.md` when any table name matches invoice, subscription, plan, price, charge, membership, dues, pledge, or recurring gift (recurring money of any kind; the amortisation sections apply only where invoices exist); `references/domains/event-and-registration-data.md` when any matches registration, attendee, session, webinar, response, or survey; `references/domains/product-usage-events.md` when any matches event, activity, usage, login, page view, or workspace. More than one test fires on the same table (`webinar_events`, `session_activity`): this is not first-match-wins; read the table's columns first (what grain it carries, what it measures) and commit to whichever domain the data actually is. A table that genuinely straddles two domains (a registration feed that also drives a usage rollup) is recorded as both in STATE.md `domain`, and the build applies both files' rules where they touch the same model, using judgment rather than either file alone. Say which domain(s) fired and why. Retention, cohorts, and conformed entities of any kind: `references/entities-and-time.md`.

## Invariants

- Nothing is created in `out_schema` before the pre-create gate returns; a checkpoint the user never answered did not happen.
- Profile before you model; a decision with no query result behind it is a `[CHECKPOINT]` or a `[DECIDED, reversible]` line, never an assumption.
- Every model declares one row per what and its key before it is built, in the transform description; every rule a model carries is pinned by a transform test before the model materialises, and a red test never materialises; every model passes the quality gate before the next; every chain is tagged and scheduled before it is called done.
- Structural checks are not correctness: one headline number is reconciled to an independent figure before it is labelled anything but Draft.
- The incomplete trailing period is a flagged row, not a missing one; rollups and rates read complete periods only.
- Business rules are the user's to decide; conventions are the company's to keep.
- One definition per number: cards aggregate metrics and measures by id and never re-derive them.
- Every stage ends with the five-part hand-back and a browser link; the job ends with the leave-behind document.
