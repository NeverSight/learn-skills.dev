---
name: subagent-team
description: Run multi-file, multi-phase coding work as a small software organisation in four layers. The main session is the director; in-house expert subagents design, review and accept; in-house execution subagents implement and test; external teams (other vendors' agents via CLI, plugin, ACP or MCP, such as agy, Codex CLI or OpenCode) take gated bulk work through a low-tier liaison; the human gets one batched question list at the end. Detects and confirms the host harness, keeps shared state on a team board in the repository, and keeps AGENTS.md and docs cross-referenced. Use this whenever a task spans several files or phases, and whenever you are about to split work or choose a task's flow, delegate to a subagent or an external agent, pick a model or effort for one, write a brief, choose, verify or track external teams, review or accept delegated work, set up a project's team policy, record a lesson or user adjustment, or decide whether to ask the user, even if the user never says "subagent".
license: MIT with Commons Clause v1.0 (see LICENSE)
compatibility: Built for Claude Code (primary) and Codex (secondary); other hosts are unverified. The method itself needs nothing but a harness that can spawn subagents. The optional helper scripts need Node.js 18+ (24 recommended) and git; run scripts/env-check.cjs at the start of a session.
metadata:
  version: "0.3.4"
---

# Subagent Team

Treat a large coding task like a small software organisation: a director, a team of in-house experts, an in-house execution team, external contractor teams, and a human owner who is asked as little as possible, all at once, at the end.

This skill is the method. Project facts (commands, sensitive modules, shared files, the host harness, which concrete model or external team fills which tier) belong in the project's `AGENTS.md` / `CLAUDE.md`, in a `## Subagent team` section created on first use. Project rules always win over this skill. Companion skills: `cli-agent-delegation` for calling external CLIs, `agent-handover` for progress records and mid-task handover.

This page holds the decisions you make on every task. Read a reference when you reach its step:

| When you... | Read |
|---|---|
| start a session, or something is missing | [references/environment-check.md](references/environment-check.md) |
| meet a new host, or need its mechanics | [references/host-harness.md](references/host-harness.md), [references/harness-claude-code.md](references/harness-claude-code.md), [references/harness-codex.md](references/harness-codex.md) |
| find no `## Subagent team` policy | [references/project-setup.md](references/project-setup.md) |
| split work, pick a flow, escalate, or decide who writes which document | [references/org-layers.md](references/org-layers.md) |
| pick a model and effort | [references/model-tiers.md](references/model-tiers.md) |
| write a brief | [references/brief-template.md](references/brief-template.md) |
| send work outside, choose or re-check teams, or brief a liaison | [references/external-teams.md](references/external-teams.md) |
| open or update the team board, or wire it into `AGENTS.md` | [references/team-board.md](references/team-board.md) |
| review or accept work | [references/verification.md](references/verification.md), [references/reviewer-prompt.md](references/reviewer-prompt.md) |
| dispatch, continue, stop or audit agents | [references/running-agents.md](references/running-agents.md) |
| run in Strict mode | [references/strict-mode.md](references/strict-mode.md) |
| want examples and lessons from real projects | [references/field-notes.md](references/field-notes.md) |

## 1. Start

Once per session, before the first dispatch, run `node <this skill's directory>/scripts/env-check.cjs --root <project root>`. It installs nothing; exit `0` is ready (maybe with warnings), `2` is blocked. Tell the user blockers and fixes in one short message, install only with consent, and re-run after changes. When external teams are found, ask the user once which may take work this session (unless the policy says `roster` or `none`). Fallbacks for anything missing, and what to record: [references/environment-check.md](references/environment-check.md).

**Host harness.** On first use, take the check's hint plus your own tool list and **confirm the host with the user**. Then establish its capabilities once: subagents, per-subagent model and effort, nested dispatch, background runs, a native task list, shell for subagents ([references/host-harness.md](references/host-harness.md)). Support levels: **Claude Code is the primary host**, **Codex the secondary**, and every other host is *unverified*. On another host, tell the user once that the skill was not tested there, and record each capability you check as *verified YYYY-MM-DD* or *unverified*.

**Team policy.** If `## Subagent team` exists in `AGENTS.md` (or `CLAUDE.md`), follow it without asking. If not, run the short setup questionnaire and write the section ([references/project-setup.md](references/project-setup.md)).

**Mode.** Say which one you picked in one line:

| Mode | Use when | Director edits files? |
|---|---|---|
| **Solo** | 1–2 files, obvious change, nothing to parallelize | Yes, just do it. Skip the rest of this skill. |
| **Standard** (default) | A feature across several files or phases | Writes contracts, wiring and shared files; delegates the rest |
| **Strict** | Several task lines, high-risk areas (money, auth, irreversible data), or many agents for days | Never. Every code task runs a `designed` flow with an L2 task lead and an independent reviewer; the board is mandatory ([references/strict-mode.md](references/strict-mode.md)) |

Escalate from Standard to Strict when you notice yourself losing track of who is editing what.

## 2. The organisation

```
L1  Director            the main session: intent, task breakdown, flows, contracts, integration, commit
L2  In-house experts    high / top-tier subagents: detail design, task leads, senior review, acceptance, expert calls
L3  In-house execution  mid / low-tier subagents: implement + test, independent review, runners, liaisons
L4  External teams      other vendors' agents via CLI / plugin / ACP / MCP: gated bulk work, second opinions
    Human               decides what nobody else may, once, at the end
```

The director's context is the most expensive in the system: push analysis, waiting and reviews down; keep only conclusions. Review and acceptance tasks get the code and the requirements, never the director's own conclusion. A layer is responsibility; a tier is model strength; they are chosen independently. Each layer's decisions and never-does list: [references/org-layers.md](references/org-layers.md).

Two principles run through everything:

1. **Delegate by default; decide by judgment.** The question is not "is this big?" but "does this need judgment?". Mechanical work goes out even when it is small enough to do yourself; judgment stays with L1 or L2.
2. **Verification must be executable.** Tests, commands with expected output, diffs, grep counts. Never "a model read it and thinks it is fine".

## 3. Tiers and effort

| Tier | Typical layer and role | Typical effort |
|---|---|---|
| top | L2 principal expert: hardest design calls, evaluating competing designs, senior review of the riskiest work | high |
| high | L1 director; L2 designers, task leads, senior reviewers; L3 implementers of risky work | medium–high |
| mid | L3 implementers of specified work, routine reviewers; L2 for routine splits | medium–high |
| low | L3 runners and liaisons | low |
| external-fast | L4: another vendor's cheap fast model for translations, bulk copy, mechanical edits | vendor's medium/high |
| external-strong | L4: another vendor's strong model for code-reading syncs, large homogeneous implementation, read-only second opinions | vendor's medium/high |

- **The director is the session's own model at high effort**; never switch it.
- **Pick before every dispatch and every rework round**, and state role, tier, effort and gate result in one line. Defaults drift.
- **Effort follows how much can only be settled by reasoning**, not the size of the change.
- **Implementation uses medium or high effort.** Start specified work at mid tier · medium; risky implementation at high tier · high. An unresolved question that seems to need effort above high goes to an L2 `consult` before implementation resumes.
- **Risk sets a floor**: a review of money, auth, migrations or irreversible data is high or top tier at high effort, on a model other than the author's.
- The project policy decides concrete models; under `auto` you choose and say so. Mapping, role table, dated roster and `scripts/model-roster.mjs`: [references/model-tiers.md](references/model-tiers.md).

## 4. Breakdown, flows and the outsourcing gate

**Break work down like an engineering manager**: program → task (`T3`) → sub-task or external job (`T3.a`). Split along ownership boundaries (one module, one contract owner, one lease); make every unit independently verifiable; peel the mechanical tail off judgement work and route it outward; isolate risky parts so they alone get the high tier and senior review; size each unit for one agent's context; start with contracts and the critical path.

**Choose a flow per task** and write it on the task's card:

| Flow | Path | Use when |
|---|---|---|
| `solo` | L1 | trivial; writing a brief costs more than the work |
| `direct` | L1 → L3 → L1 | the director's brief settles every decision |
| `outsource` | L1 → L3 liaison → L4 → L3 review → L1 | bulk, fully specified, passes the gate |
| `designed` | L1 → L2 → L3 → L2 accept → L1 | needs detail design, spans modules, or is sensitive |
| `designed+outsource` | L1 → L2 → L3 + (L3 liaison → L4) → L2 accept → L1 | as `designed`, with a mechanical tail L2 freezes and sends out |
| `consult` | L1 → L2 expert → L1 | a decision only, no code |

Outside `solo`, every code change gets an independent review, execution layers hand in real acceptance output, and the integration gate and commit stay with L1. Keep with the director: cross-task priorities, talking to the user, product decisions, contracts, final integration and commit.

**Outsourcing gate for implementation.** Send editing work to an external team only when *all four* hold:

1. **Fully specified**: what to do and which files are decided; no product or architecture decisions remain.
2. **No risk**: no business logic in billing, payment or auth, no data migrations, concurrency or data-loss paths; a mistake is easy to spot and roll back.
3. **Objective acceptance**: runnable commands or a checklist anyone can tick.
4. **Bulk or repetitive**: translations, homogeneous integrations, template fills, snapshot and exhaustive tests, doc syncs, mechanical refactors; or a small pure module with no billing or auth role, a frozen signature and hand-checkable cases.

**Run the gate on every task** and write the result on its card. In-house is an outcome of the gate, not the default; a long run with external teams on the roster and no external job usually means the gate was never run. Tests *for* a sensitive module may go out; its business code may not. Generated tests still need independent review of what they prove.

**Read-only second opinions have a separate route.** Sensitive code may be read by an authorized external reviewer even though it fails the implementation risk gate. Give another vendor's strong model at high effort the requirements, review scope and evidence to return, with no edit lease. Review sensitive designs before freezing them, and money, auth, schema or irreversible-data implementations alongside the in-house senior review. Keep the reviews independent; confirm findings by reproduction or decisive source evidence before fixing them. The verdict and acceptance stay in-house. If no authorized external reviewer is available, retain one independent in-house senior review and record the missing external opinion; stricter project review gates still apply. Do not widen the roster silently.

## 5. Workflow (Standard mode)

1. **Design doc and board.** Decision table, architecture, tasks with their flows, assignment table (layer, tier, effort, in-house or which external team), risks. When external teams are involved or the work may span sessions, open the team board with one card per task.
2. **Contracts first.** Types, state, interface signatures, component names and props, directory conventions; the type check passes. A shared computation has one named owner.
3. **Design** (flows with L2): sub-tasks, briefs, leases, acceptance commands; specs going to L4 are frozen. For money, auth and schema work, budget two review-and-fix rounds regardless of implementer tier; this is capacity planning, not a required number of rounds.
4. **Dispatch.** Every writer owns a lease; one writer per file at a time. Launch independent work, in-house and external, in one message.
5. **Execute and test** (L3, L4): code with tests and real acceptance output; independent reviewers audit, run and probe.
6. **Accept** (L2 where in the flow, otherwise L1), then the director integrates: wiring, shared files, dead code.
7. **Verify.** Type check, lint, tests, then a short targeted pass on the user's running dev server. Never start, stop or restart the user's services; ask them to.
8. **Review across phases** for what phase reviews cannot see: lifecycle ordering between subsystems, module-level caches, leftover dead code and keys.
9. **Record and commit.** Cards, progress record, lessons, `AGENTS.md`. Commit each verifiable unit where allowed; push, merge or deploy only as the project or the user allows.

## 6. External teams and the liaison

External teams are reached through a CLI, a plugin, ACP or an MCP server; the project's roster lists each team, its channel, which external tier each model fills, and whether it may edit or only review. Before trusting an untested team, run one tiny read-only job. When the user asks mid-run to add, drop or check a team, re-check without interrupting running jobs, report one capability table, and update the session choice, roster, queued cards and lessons.

Every external job gets a **liaison**: an L3, low-tier in-house subagent that dispatches exactly per the frozen brief, records job ids on the card, waits in bounded slices, checks the diff against the lease, runs the acceptance commands, answers only what the brief or repository already settles, and sends one mechanical rework round. Dispatch alone is never a final delivery: the liaison stays until collection and checks are complete, or explicitly escalates a blocker with the job's state and ids. The brief names where each acceptance check runs; a sandbox refusal leaves that check pending for an authorized in-house runner. It escalates every decision and any second failure, and never decides product or architecture, edits code, commits, talks to the user or starts a duplicate job. **External agents cannot run end-to-end checks** (no browser, device or full stack): their acceptance is static checks and unit tests, and the director arranges every end-to-end check for outsourced work, itself or through an in-house agent that has the tools. Without subagents, the director runs the job in the background instead. Roster, adjusting teams, fallbacks, the liaison's full duties and waiting per harness: [references/external-teams.md](references/external-teams.md). Calling Codex, agy, OpenCode and other ACP agents: skill `cli-agent-delegation`.

## 7. Shared state: the team board

Use the host's native mechanism (a shared task list, agent messaging) for live coordination. Use the **board in the repository** (`docs/agent-team/`: index, one card per task or job, progress, decisions, lessons) whenever an external team is involved, the work may span sessions or be handed over, in Strict mode, or when the host has nothing native; then the board is the source of truth. **One holder per card**, the only writer. Open questions are `[open]` items on the asking unit's card, answered in place, never deleted. `scripts/team-board.mjs` runs `init`, `new` and `status`. Layout and card template: [references/team-board.md](references/team-board.md).

## 8. Escalation and asking the human

Once the user authorizes continuous work, **do not stop mid-way to ask**. Questions go up to the next layer present in the flow: liaison or L3 (what the brief already settles) → L2 expert (technical calls inside the design) → L1 (cross-task priorities, contracts, leases; small reversible conventions) → principal expert in a `consult` (architecture trade-offs, bugs that resist reproduction, every option has a hard flaw) → human. Expert advice is data, not orders.

The human decides product and business calls, accounts, keys, payment, anything public, and always: reducing what users already have, irreversible data operations, prices and revenue, public commitments. Record each such question under *Open questions*, take the most conservative path (or skip), and keep going. At the end hand over one **grill-me list**: one question per item with one line of background, 2–3 options, your recommendation and why, the cost of choosing wrong, and what you did meanwhile. Order by impact, merge what can be merged, and ask only what only a human can answer. Escalation message format: [references/org-layers.md](references/org-layers.md).

## 9. Briefs, verification and review

- **A subagent knows only what you write.** Every brief is self-contained: goal; **verified facts** (with file:line, "do not re-check") kept apart from **things to verify** ("if it differs, stop and report"); the read-only contract; the lease; constraints *with reasons*; runnable acceptance commands; deliverables; report format; card path and escalation target. Standing prohibitions: no state-changing git, no dev-server restarts, no `.env*` or secrets (never print one; compare by hash), no repo-wide rewrites during parallel work, no edits to shared files. Templates and the pre-dispatch checklist: [references/brief-template.md](references/brief-template.md).
- **Implementers deliver tests with the code.** **Reviewers** audit the tests, then execute them and paste real output, and only then read code; test gaps mean NEEDS_CHANGES. Reviewers are read-only, never review their own work, and preferably run on another model or vendor.
- **"Done" is a claim.** Look at the diff, check the lease, run the acceptance commands, verify factual claims in docs. L2 accepts where the flow has it; L1 always runs the integration gate.
- **Rework** goes to the *same* agent with the concrete failure; a small fix may be done by the director outside Strict mode; L2 never edits, it sends the fix back. External work that fails twice comes back in-house.
- **Close review with evidence.** A finding needs a reproducible trigger or source evidence; its fixer confirms or rebuts it before editing. Re-review the fixes and affected invariants, then stop when confirmed blockers are closed and the gates pass. Rework on risky work alone is no reason to raise tier or effort.

Review procedure, fingerprints, mutation checks and command pitfalls: [references/verification.md](references/verification.md). Running agents (continue vs respawn, slots, worktrees, processes, dispatch audits): [references/running-agents.md](references/running-agents.md).

## 10. Keep the project's docs alive

Docs are how the next agent, session or tool runs this process well, so updating them is part of "done":

- `AGENTS.md` → `## Subagent team` holds the policy and links the board index, which links back. Each rule has **one** home; everything else links to it.
- When the user corrects the process or states a preference, write a dated row in `lessons.md` right away with their words verbatim; a project-wide rule also goes into `AGENTS.md`.
- At the end of each phase, note what was redone, which brief was unclear, which tool bit you, which outsourcing paid off. Promote rules into `AGENTS.md`, method improvements into [references/field-notes.md](references/field-notes.md) or your fork.
- Rules live in the repository, never only in an agent's local memory (skill `agent-handover`).

What to write where, and when: [references/team-board.md](references/team-board.md), "Keeping AGENTS.md and the docs cross-referenced".
