---
name: deliver
description: Deliver a change end to end by orchestrating agent profiles - grill, plan, test-first implementation, review, QA, then merge or open a PR. Use when the user's message starts with "deliver" or names `deliver` (or `flyingnobita-deliver`), whatever the size of the work.
---

# Deliver

You are the **orchestrator**. Every delivery runs this whole workflow, however small the change: size only chooses the route in step 1, never whether to skip a stage. Text after the word "deliver" is the input.

You turn the user's input into a confirmed **brief**, run role agents through a pipeline, check every stage's result yourself, and ship. Role agents write and commit the code and tests; the only project files you edit are the rules the user approved for `AGENTS.md`, tracker records, and the domain docs from the grilling stop. You coordinate, verify, and decide what goes to the user.

Keep independent verification bounded: reproduce each role claim once using its
retained command or driver. A failure goes back to the owning role with that
receipt for diagnosis and repair. The orchestrator inspects evidence and repeats
the corrected reproduction; successive replacement drivers and product debugging
belong to the role, not the orchestrator.

**Stops** are the only points where you end your turn to wait for the user:

1. the grilling round;
2. plan approval;
3. any **scope change**: a finding that changes what is being built or why;
4. the local preview, when the approved plan waits for the user to try it;
5. the PR draft, for an **upstream repo** only.

Work that needs steps only the user can perform (credentials, CI secrets, a third-party dashboard) is also a stop: load `wizard` (or `mattpocock-wizard`) to generate a guided script for those steps, and resume when the user reports them done.

Run everything else to completion without asking. Ending your turn is how the user is notified, so end it only at a stop, at a blocker you cannot resolve, or with the final report.

## Host adapter

Every host action below is an **operation**: start a role, send a role a follow-up, wait for an event, answer a permission, create a workspace, notify the user. Before step 1, read [host detection](references/host-detection.md), verify actual
caller/session membership, and select one adapter for the run:

- Confirmed Paseo session: [adapters/paseo.md](adapters/paseo.md).
- Confirmed Herdr session: [adapters/herdr.md](adapters/herdr.md).
- Confirmed Orca session: [adapters/orca.md](adapters/orca.md).
- Multiple confirmed hosts: ask the user to choose among them. Broken or ambiguous context: stop with the failed check.
- No adapter matches: tell the user which host you are in and stop.

The helpers `deliver-runtime` and `deliver-orca-preflight` ship with this skill as `scripts/deliver-runtime.py` and `scripts/deliver-orca-preflight.py`. Run each as `python3 <this skill's directory>/scripts/<name>.py`, wherever these references name the helper.

This skill builds on other skills and their file formats. When one is missing, or behaves differently from what [references/dependencies.md](references/dependencies.md) records, use that file's fallback and name the dependency in your report.

For configuration or legacy migration use `deliver-setup` (or
`flyingnobita-deliver-setup`); for a standalone branch review use `deliver-review`
(or `flyingnobita-deliver-review`); for agreed tickets without grilling or
planning use `deliver-implement` (or `flyingnobita-deliver-implement`). Questions about the
workflow use [references/workflow.md](references/workflow.md). Inspecting or
editing this skill does not start a delivery.

## 1. Intake

Read [references/intake.md](references/intake.md). Identify the input type, read it fully, and write the brief.

Done when the brief exists and its size route (single unit or ticket graph) is chosen.

## 2. Setup

1. Read [references/configuration.md](references/configuration.md) and resolve
   settings for this run. Legacy config triggers its migration path. Resolve the repository. With no local clone known, ask the user for a path and suggest any existing clones you find.
2. Resolve user identity and repository access: identify the executing user account (`gh api user -q .login` or configured git identity) and determine repository access (`gh repo view --json viewerPermission,isInOrganization,owner`). Organization repositories where the user has member/collaborator push access are direct repositories. If the user lacks write access (or repository policy requires fork contributions), fork the repository under the user's account and configure `upstream`. Fork only when the contribution route needs it.
3. Classify the repo route: **direct repo** (user has direct push access) or **upstream repo** (contributing through fork). Write access never grants merge authority; merging into the default branch requires explicit repository consent (`AGENTS.md` autonomous delivery rule) or explicit session approval, and branch protections must be respected.
4. Direct repo: read [references/project-rules.md](references/project-rules.md) and run its checks. Its questions join the grilling round.
5. Set up the work's workspace: an isolated worktree on its own branch, starting at the default branch (`origin/<default>` for a direct repo, `upstream/<default>` for an upstream repo). Every role works in it, one after another.
   - **Reuse** your own workspace when the host is Paseo, the work is a single unit, and the workspace is a worktree of this repo on a non-default branch with a clean tree and no commits beyond the base ref (`git rev-list --count <base>..HEAD` is 0). Fast-forward it to the base ref.
   - Otherwise **create** one through the adapter. Herdr and Orca create isolated workspaces; Herdr treats an existing worktree as a collision. A ticket graph adds one workspace per ticket at build time ([references/pipeline.md](references/pipeline.md#ticket-graph)).
6. Record the **baseline**: install dependencies and run the full test suite and linters as the repo's own docs and config define them. Inspect automated verification through [CI and local checks](references/ci.md); carry unresolved guardrail choices into grilling. A failing baseline is a blocker: report it at the grilling stop.

Done when the workspace is ready, recorded as reused or created, and the baseline result is recorded.

## 3. Grilling stop

Load `grilling` (or `mattpocock-grilling` if installed with the prefix) and grill the user on every open decision the brief leaves, at the depth intake set: for gaps-only depth, tell it to ask only what is missing or contradicted. For human steps or ticket graphs, read [references/scheduling.md](references/scheduling.md) and add its unresolved scheduling decisions. Add the setup questions, the local preview offer (what it would activate, the command, the state it replaces, and how that state is restored), and the QA offer (target host or environment, or skip) to its rounds.

Direct repo: also load `domain-modeling` (or `mattpocock-domain-modeling`), so glossary terms and ADRs are written as decisions settle. Upstream repo: write no domain docs.

Done when every open decision is settled and the user has confirmed the brief.

## 4. Plan stop

Start the planner role, read-only, with the brief and the decisions. Its plan must name:

- the vertical **slices** of the work, in order, marking each **destructive** slice: one that deletes, rolls back, prunes or overwrites durable state, together with the stronger implementer profile it runs on ([pipeline.md](references/pipeline.md#build));
- the **local preview** step when the user asked for one: what it activates, the activation command, the state it replaces, and how and when that state is restored, placed before the ship stage;
- the **seams**: the public interfaces the tests go through, each with a line on what it catches and what it misses (`tdd` tests only at seams the user confirmed);
- the commands for the tests, the full suite and the linters, and the plan's required test list by name, each group with exactly one kind from the contract, `behavioral`, `guard` or `bootstrap`; a group testing a new public surface is `bootstrap`, imports it at module scope, and states its plan-backed reason ([test evidence](references/test-evidence.md));
- when the product ships or fingerprints its own tree: the end-to-end command that prepares and validates the real artifact, and each gate it runs (freshness, fingerprint, leak checks), checked against every preparation step the plan requires so no required step is one a gate refuses;
- shared-file ownership, available extension hooks and test commands that mutate
  source fixtures, with serialization or isolated-copy boundaries for those commands.

When records or events can arrive delayed, replayed, batched or out of order, the
plan also names:

- the timestamp that defines chronological order: event time, never arrival or
  insertion time;
- when a record becomes visible to a reader, including any write-behind,
  batching or separate-read boundary;
- which operations depend on storage order.

It includes a separate-read counterexample with an ordering-sensitive retention
effect: a newer event was already persisted when an older one arrives, both are
read in separate operations, and a small retention ceiling that keeps the N
newest by event timestamp can drop or reorder the newer record. The proposed
tests go through approved public interfaces, with expected order and retained
records stated independently of the implementation. Example plan items: order by
`occurred_at`; a read may lag its write by one batch; retention scans in write
order; a test that inserts the older event second asserts the read order and
which record the ceiling keeps.

A task with no ordering-sensitive behaviour stays a small plan and gains no
event-order section.

For a single unit with **independent, substantial** parts (separate modules, no shared seams), the planner may propose them as a ticket graph with blocking edges, justifying the split against its cost: a worktree, an implementer and a merge per ticket, and a whole-branch review. The user approves the split with the plan; small or interdependent work stays one unit.

For a bug whose cause the input does not establish, the planner loads `diagnosing-bugs` (or `mattpocock-diagnosing-bugs`) and reproduces the bug before planning; a bug that does not reproduce is a scope change. The planner may also load `research` (or `mattpocock-research`) for external facts, `codebase-design` (or `mattpocock-codebase-design`) when the change moves a module interface, and `prototype` (or `mattpocock-prototype`) for a question code answers faster than discussion.

Read the plan yourself and check its claims against the code. Present the plan, its seams and what you verified.

Done when the user approves the plan and its seams, then `approve` records that approval with `approved` holding the `brief`, `plan` and `seams`, plus the actual request/approval as `evidence`. Record it before any build task or attempt exists, because `attempt` refuses without it. For a ticket graph, the plan is the ticket breakdown and its order. Then commit the approved `AGENTS.md` rules, tracker records and domain docs on the work branch following repository commit rules (or a configured custom commit skill), before the build starts. Delivery records (handoffs, plans, progress logs) stay in the run directory when the product ships or fingerprints its own tree, since their local paths would enter the artifact.

## 5. Build

Read [references/pipeline.md](references/pipeline.md) and run it: the implementer builds test-first at the approved seams and commits, your **red check** proves the new tests fail on the base, review loops until clean, the plan's local preview runs and restores before QA, and QA runs when offered. Answer role permission requests by the rule in the adapter. A scope change found here is a stop.

Done when every pipeline gate in `pipeline.md` has passed, each confirmed by your own run rather than a role's report.

## 6. Ship

Read [references/ship.md](references/ship.md) and follow the branch for the repo's route.

Done when the ship branch's final verification passes.

## 7. Report

Before the final response, collect outstanding items using
[outstanding work](references/outstanding.md). Recheck the brief, reports,
review mentions, QA gaps, deployment and cleanup receipts against current
evidence, and search the chosen tracker for existing entries.

Present the proposed tracker creates/updates with concrete item IDs/titles and
the destination. Ask whether to save all, selected items, or none. Write only
after the user's selection; a configured tracker or delivery approval is not
consent to these wrap-up writes. If the destination is unknown, resolve it in
the same offer. Keep pending or declined items in the private run artifact;
silence is not consent. If nothing remains to save, state that without an offer.

Done when the offer and its pending, declined or verified-saved outcome are
explicit. After acceptance, save only the selected items and verify their
tracker references. Include the central tracker link when configured, any
unsaved count and where those items are retained. A tracker entry does not
turn an unmet acceptance gate into completed work.

End with a short report: what changed, the evidence (tests, red check, review, QA), the commit, the PR, the merged commit for a direct repo, any dependency fallback used, and the outstanding-work references. After a run with scope changes, review loops beyond the first, or fallbacks, suggest `/deliver-retro` (or `/flyingnobita-deliver-retro`) in this session. This message is the user's notification that the work is done.
