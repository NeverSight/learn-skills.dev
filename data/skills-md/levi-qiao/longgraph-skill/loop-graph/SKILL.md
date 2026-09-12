---
name: loop-graph
description: Compile one durable loop-graph run into executor, ledger, directives, ops, and supervisor artifacts under a dated `.longgraph` directory, then present copy-ready host prompts. Use directly for a custom multi-round shape with gated milestones, independent audit, cross-host execution, or durable state; focused sibling packs handle code convergence, requirement delivery, and evidence-led research. Existing runtime nodes are self-contained.
---

# loop-graph — a graph of agent nodes, not a drifting loop

## Module boundary

This is the **shared compiler**, not a goal-specific workflow. It owns the graph
shape, the five runtime artifact schemas, generic interview mechanics, and host
handoff. A focused preset owns only its North Star, proof, interview questions,
recommended work shape, method guards, knobs, and slug; it never forks templates
or adds a runtime node.

Use [`../loop-converge/SKILL.md`](../loop-converge/SKILL.md) for code cleanup,
[`../loop-deliver/SKILL.md`](../loop-deliver/SKILL.md) for requirement delivery,
and [`../loop-research/SKILL.md`](../loop-research/SKILL.md) for evidence-led
solution selection. Use this skill directly only when a custom pack is genuinely
needed. The exact contract is in [`docs/preset-contract.md`](docs/preset-contract.md).

## What it does & why

Turns a vague long-horizon request ("make it production-ready", "accuracy above baseline", "finish the migration") into a small **graph of agent nodes** that stays on-spec across many rounds:

- an **executor node** — drives the work round by round against a single scoreboard;
- a **supervisor node** — audits the work from *outside* the executor's context (re-verifying claimed-done against the shared standards) and corrects course before drift compounds.

Why a graph, not a loop: an agent grinding a long task **is inside the context that drifted**, so it rationalizes scope creep and calls half-done work "done". The nodes talk only through durable, inspectable state (ledger, git tree, directives file) — never a shared, polluted context.

**Each node runs on its own timer, and no node ever wakes another.** The executor fires, closes several verified rounds on warm context, and ends. The supervisor fires on a slower cadence, audits, appends corrections, and ends. A correction is picked up on the executor's next fire. Two independent clocks and one file edge — no dispatch, no resume prompt, no liveness protocol, and therefore nothing that can leave the run waiting for a wake that never comes.

## The graph it builds

```
        ┌─────────────┐   reads / rewrites   ┌──────────────┐
        │  EXECUTOR    │ ───────────────────▶ │              │
        │  node        │ ◀─────────────────── │  ledger.md   │  ← single scoreboard
        │ (own timer)  │                      │ (shared state)│
        └─────────────┘                      └──────────────┘
              ▲                                      ▲
              │ reads each round                     │ reads only (never writes it)
              │                                      │
        ┌───────────────┐   appends corrections ┌──────────────────┐
        │ directives.md │ ◀──────────────────── │   SUPERVISOR     │  ← separate context,
        └───────────────┘                       │ node (own timer) │     slower cadence
                                                 └──────────────────┘
                                                     │ checkpoint-commits clean work
                                                     │ escalates human-only calls
                                                     ▼
                                                   git / you
```

Five live artifacts from a short interview:

1. **`executor.md`** — executor prompt: one task book, one cadence, anti-bloat rules, stop conditions, red lines.
2. **`ledger.md`** — the single scoreboard both nodes read; the executor rewrites it every round.
3. **`directives.md`** — the bounded one-way corrections queue: current STANDING locks + not-yet-folded numbered corrections; folded ones rotate into a cold archive.
4. **`ops.md`** — the exact context index and gates every cold node follows,
   plus current environment/data/host lifecycle facts when applicable; update
   facts in place, never as a timeline.
5. **`supervisor.md`** *(optional)* — supervisor prompt, scheduled; independently re-verifies claimed-done work, checkpoint-commits what passes, decides pending items, and corrects drift / steers the plan via the directives file.

**Run directory — fixed, one per run.** Everything above goes in `.longgraph/<YYYY-MM-DD-slug>/` at the repo root (workspace root for multi-repo runs), plus an `archive/` subdir for in-run rotations. **A new run always creates `.longgraph/…` from the templates — never retarget or edit a previous run's files**: patching stale prompts wastes tokens and leaves leftover text steering toward the old goal. The old directory stays untouched (it *is* the archive); distill what still holds into the new ledger's starting snapshot and copy still-in-force STANDING directives forward. Commit the run directory unless data policy forbids — it's the durable state the graph depends on.

Runtime contract ids are `longgraph.loop-graph.*`.

Invariants: **ledger = the only scoreboard**; **one independently verifiable work item
(which may be one coherent workset) per round → verify → update ledger**; **the
supervisor steers only through `directives.md` (a one-way edge) — it never edits the
ledger or shares the executor's context**.

## When to use it

- Task spans many rounds; the user won't babysit each one.
- "Done" is verifiable (tests, gates, metrics) — the graph needs a definition of done it can check itself.
- Real risk of scope creep, "looks done" work, or quietly changing contracts / lowering the bar.

**Not** for a one-shot edit, or when success needs a human to judge every time — say so, suggest a plain task.

## Language

Interview in the user's language and mirror it in the prose inside the artifacts (goals, notes, red lines). Keep structural keywords, headings, and field names as in the templates so files stay tool-friendly.

## When called from a preset skill

A sibling authoring skill (for example [`loop-converge`](../loop-converge/SKILL.md))
may bind a **preset pack** and then hand off here. The pack follows the
[`preset contract`](docs/preset-contract.md); treat it as already
answered for:

- **North Star and proof** — skip that interview question unless the pack is
  silent on a checkable outcome.
- **Supervisor** — required when the pack says so; do not ask to omit it.
- **Method guards** — append the pack's guards as `PROJECT_SPECIFIC_METHOD_GUARDS`.
- **Knob overrides** — use the pack's numbers instead of the defaults.
- **Recommended shape** — present the pack's decomposition (milestones, or a
  rotation for a sweeping run) as A unless inspection shows a materially
  different one.
- **Artifact emphasis** — compile the pack's required facts into the shared
  `ledger.md`, `ops.md`, `directives.md`, executor, and supervisor sections;
  do not create a second runtime template or scoreboard.

Still discover the workspace. Still ask at most three owner questions; with a
bound pack those are typically scope, authority, and launch mode. Still
generate from this skill's [`templates/`](templates/) — never a second template
set, never a third runtime node. The preset skill does not execute the generated
nodes.

## How to run it

**Step 1 — Discover, then interview.** Before asking anything, inspect the workspace and current system/tool context. Infer the current authoring host, project root, repos, branches, dirty state, repo instructions, likely gates, and any explicit goal/constraints. **Never ask the user which client or host this is when the system context already identifies it.** Capture the dirty-state baseline before this session changes anything — whatever you go on to move, archive, generate, or delete becomes indistinguishable from the owner's uncommitted work unless your own paths are enumerated in the ledger's starting snapshot. Keep authoring probes side-effect-free: direct scratch output into the new run's evidence directory, suppress tool caches when possible, and remove a known artifact this session created before handing off. An authoring run must not leave a product-path cache masquerading as owner work.

Ask one short batch of at most three questions containing only unresolved owner
decisions. Propose the answer; do not ask the owner to design it. If more than three
details remain, prioritize goal/proof, safety authority, and launch mode; infer or
defer the rest. Ask a follow-up only when the run would otherwise be unsafe or
unverifiable:

1. **North Star and proof**, only when the request does not already imply a checkable outcome. Offer one concise recommended wording.
2. **Authority**, only where not already stated. Recommended default: local edits and verification allowed; no push, destructive git, production/remote mutation, secret or real-data exposure, unbounded spend, or lowering an acceptance bar. Ask whether commits are allowed only when the run needs them. When the run performs metered or expensive work, put the actual numbers in `ops.md` — "spend beyond budget" is an owner-only tripwire, and an undeclared budget makes it unenforceable. Say what each gate actually costs: money, wall-clock, or risk. A gate that costs only time is batched, not rationed — a cap that puts a whole area of the work out of reach is a scope decision wearing a budget's clothes, and it belongs in the scope answer instead.
3. **Milestones**, only when two materially different decompositions exist. Present the recommended phase split and exit checks as A; offer B only when it changes the outcome or risk. Single goal means no milestone question. Sequence so the smallest slice that unblocks the main line comes first: a large enabling refactor placed ahead of the delivery milestone concentrates risk and delays every proof behind it. Split such a milestone into the narrow unblocking part and a remainder that runs alongside the main line instead of in front of it.
4. **Launch mode**, unless the user already chose it: **A (Recommended) — create both runtime nodes here on the detected Codex or Claude Code host**; **B — print copy-ready prompts only**. Ask target hosts only for B or when the user explicitly requests a cross-host run.

Do not ask for repo paths, branches, host, test commands, red lines, or cadences when they are discoverable. If a gate is missing or ambiguous after inspection, propose the narrowest credible command and ask one A/B choice. Long-horizon loop-graph runs include the supervisor by default; ask whether to omit it only when its value is genuinely doubtful.

For each supervised milestone boundary, name its exact promotion audit surface and exit checks. Expect the run to block often — owner decisions, missing inputs, unmet dependencies, a milestone under audit: seed the Debt & gap register with enough real, independent work that the executor always has a legal next item instead of ending the fire early.

**When the work has to be found, seed the method — not the list.** For runs whose items are discovered (dead code, duplication, coverage holes, stale config), you see one context window of a tree the run will cross many times, so a hand-written candidate list becomes the run's ceiling: the executor works it, then reports done. Compile detectors, a refill quota (close N → discover at least N), and a rotation across the whole surface into `ops.md` and the ledger, and seed the register with the *method* plus measured baselines. Make termination a yield check — two consecutive full sweeps whose fresh detector pass yields under a threshold — never an empty queue. Pair it with an output floor per fire so productivity, not a round count, decides when a fire ends. Fix the **owner-only decision list** (typical: DDL/schema, credentials / remote env / real-data exposure, spend beyond budget, lowering a metric bar, frozen contracts, push) — everything off that list the supervisor decides itself.

- **Pre-adjudicate critical-path calls now.** Research the project and draft the evidence bar yourself; do not ask the owner to design it. Present: **A (Recommended)** accept the drafted standing authorization, **B** keep the action owner-blocked, and only when real, **C** a clearly different safe alternative. Explain each outcome in plain language and accept a one-letter reply. Write accepted bars as STANDING directives. Only a decision that genuinely needs case-by-case human judgment stays blocking.
- **Owner decision UX is a runtime contract.** Every later owner escalation must use the decision-card format below. The owner should not need to understand internal symbols, reconstruct history, or propose the solution.

```text
Decision needed: <one plain-language sentence>
Why now: <what is blocked and what happens if we wait>
Recommendation: A — <choice> (<one-sentence reason>)
A (Recommended) — <outcome and main tradeoff>
B — <outcome and main tradeoff>
C — <only when genuinely distinct; otherwise omit>
Reply with: A / B / C
```

Use at most three mutually exclusive options. Put the safest reversible option first unless evidence clearly favors another. Translate technical evidence into consequences; place paths, commands, and jargon in an optional `Technical note` after the choices. Never end with "what do you think?" or make the owner invent option D. If no answer arrives, the run holds at the safe no-change state.

**Host and cadence.** Infer the current authoring host from system context and callable tools. Codex and Claude Code are the supported direct-launch planners. When A is chosen, place both runtime nodes on that detected host and read only its reference; do not ask about or print other-host syntax. When B or an explicit cross-host request is chosen, read one reference per selected node:

- [Claude Code](references/claude-code.md)
- [Codex](references/codex.md)
- [Grok Build](references/grok.md)
- [Cursor](references/cursor.md)
- [shell / cron](references/shell-cron.md)

Do not load unrelated host references. The selected reference owns capability checks, node creation, and how each node arms and stops its own timer. Other hosts may execute prepared prompts, but direct creation is supported only from Codex and Claude Code.

Set two cadences. The timer guarantees a node comes back; it does not pace it. `EXEC_INTERVAL` is how soon the executor returns after a fire ends — short, because the fire, not the interval, decides how much work happens. `SUP_INTERVAL` is 3–4× that, phase-offset, so the supervisor audits several times across a long fire.

**Size the milestone to the fire, not the fire to a round count.** A round stays one
independently verifiable work item; that item may be the largest related workset that
shares a behavior claim, write set, and gate. Every fire boundary pays a cold
re-derivation, so one fire should carry a whole milestone and end at a seam — the
milestone exit, or a closed convergence round. That makes milestone granularity the
real context-cost lever: a milestone the executor cannot plausibly finish in one warm
fire should be split, and `FIRE_ROUND_CAP` ends only that fire, never the run.

**Compile context, do not narrate it.** Host prompts are one-line pointers to the runtime Markdown. At authoring time, build an `ops.md` Context index with exact files, symbols/headings, evidence paths, and narrow gates. Every Current slice and correction points to those IDs. Runtime nodes read the hot state plus referenced rows only; they do not scan the workspace, reopen whole authority documents, or restate source text. The supervisor audits deltas since its durable watermark and runs full gates only at promotion/checkpoint or when a narrow gate is insufficient.

Decide from context what you reasonably can and state the assumption; anything genuinely the user's call (data policy, DB access, lowering a bar) becomes a red line, a **standing authorization** (offer your drafted recommendation as a choice), or an `owner-blocked` item (only if it truly can't be pre-decided). Never hand the owner an unstructured problem.

**Step 2 — Generate** a fresh `.longgraph/<YYYY-MM-DD-slug>/` from `templates/`:

- Always: `executor.md`, `ledger.md`, `directives.md`, `ops.md`, and `archive/`.
  Add `supervisor.md` only when chosen.
- Replace every placeholder and delete guidance comments. Keep paths inside the run directory.
- Keep host launch prompts to a pointer plus the host primitive. Put behavior in `executor.md`/`supervisor.md`, never duplicate it in the handoff prompt. Two things matter in every launch prompt: **read-and-follow, never an authoring verb** ("set up", "create", "author", "plan" read as permission to build something, and a fresh node answers by creating a second run) — and **"do not load any skill"**, because a host that matches skills by name or path can inject the authoring skill before the node opens its own file.
- **Owner-facing paste is a `/loop` line on every host that has `/loop`.** Shape:
  `/loop {{INTERVAL}} Execute the existing runtime node at {{PATH}}. Do not load any skill.`
  Cadence, timer-ID recording, self-stop, and freshness belong in `TIMER_STEP` or the
  node file — never as extra owner steps ("write this ID into `ops.md`", "then create
  a scheduled task"). Codex has no `/loop`: the owner paste is the thin read-and-follow
  line. Mention creating a scheduled task or automation only when the owner explicitly
  asked; the compiled `TIMER_STEP` is what arms Codex.
- Compile the `ops.md` Context index before writing the first ledger slice. Each row names when to read it, exact source pointers, and exact verification. Make the ledger Current slice and every directive cite those rows.
- Tune the knobs; otherwise use `FIRE_ROUND_CAP=8`, `CONVERGE_EVERY=5`, `NET_LINE_CAP=400`, `KEEP_ROUNDS=5`, `OPEN_DIRECTIVE_CAP=8`, `STANDING_CAP=12`, `GAP_CAP=12`, and `FILE_LINE_CAP=200`. Open-ended runs add `FIRE_OUTPUT_FLOOR` (the closed items or net lines a fire must land before it may end) and `YIELD_FLOOR` (the per-sweep discovery count under which the run may go terminal).
- **Every durable section is bounded and rotates on a rule that actually fires.** Rotate by count against a cap — rounds past `KEEP_ROUNDS` and corrections at or below the folded watermark move to `archive/`; STANDING and the gap register are capped and rewritten in place; no live file exceeds `FILE_LINE_CAP` lines. A rule keyed to a boundary that may never be reached (a fixed shard size, a milestone that slips) is the same as no rule: the file grows until a node truncates its read and silently misses the newest entry. Anything re-read every round that can only grow is a defect, not a style choice.
- Fill `TIMER_STEP` from the selected reference. Delete it only when the node has
  nothing to arm, record, or stop. A `/loop` interval on the launch line is not a
  reason to delete `TIMER_STEP` if the node must still write its own timer ID or
  delete its own task. Never ask the owner to type a task, session, or automation
  ID into `ops.md`. Host-specific facts belong in references, not in the generic
  templates.
- Name the host's cheap model tier as `FANOUT_TIER` in `ops.md` when the executor may spawn read-only sub-tasks; delete the section when the host has no cheap concurrent tier. Read-only investigators run cheap; the executor itself does not.
- Render [`templates/handoff.md`](templates/handoff.md) only as the chat response. It is a presentation template, not a runtime artifact: never save `handoff.md` in the run directory. Delete its supervisor section and the `To steer` line when no supervisor was selected.
- Keep hot files lean: current state, unresolved rows, recent rounds, and unconsumed directives only.

**Step 3 — Deliver without making the owner discover the workflow.** Offer only when the user has not already chosen:

- **A (Recommended) — create both nodes here** when the detected host is Codex or Claude Code.
- **B — prompts only** when the owner will launch elsewhere.

Never end at "files generated." End with the exact next action and copy-ready prompt(s).

- **Create both nodes here:** treat the user's A choice as authorization to create the two in-scope runtime sessions. Follow the selected reference's ordered capability check and creation protocol. Use the current project/checkout; do not create a cross-host prompt or silently switch to worktrees. Verify both nodes started, and report their IDs, both cadences, and how to stop them. Do not ask for a second confirmation.
- **Prompts only:** render the completed [`templates/handoff.md`](templates/handoff.md) in chat without persisting it. It must say how many sessions/tasks/processes to open, where each prompt goes, what continues automatically, how it stops, and how to steer. Never ask the owner to write host IDs or create a timer the compiled node already owns.
- Never leave `{{PLACEHOLDER}}` text or tell the owner merely to "start the loop." Keep executor and supervisor in separate contexts; use a cheap/fast executor and a strong supervisor when available.

## The rules that make it work (encoded in the templates)

- `ledger.md` is the single, bounded scoreboard; executor writes it, supervisor never does.
- One independently verifiable work item per round: implement, verify, record.
  A related workset shares one behavior claim, write set, and gate; unrelated work
  stays separate. Register side-gaps for later.
- Each node owns one timer and wakes only itself; blocked work moves to the registered lane instead of ending the fire.
- Force convergence off durable state the supervisor audits; pilot expensive batches; require a real consumer before new surface area.
- Count only reproducible evidence on the declared real set.
- Pre-authorize checkable owner calls; present genuine exceptions as recommended A/B/C choices.
- Keep the supervisor's context separate; it re-verifies, steers only through directives, and stops its own timer at terminal state.

## Files in this skill

- [`templates/`](templates/) — host-neutral runtime artifacts plus a chat-only launch-prompt template.
- [`references/`](references/) — one small, independently loaded file per host.
- [`methodology.md`](../../lib/methodology.md) — the deep dive (why each rule exists, failure modes it prevents).
- [`examples/add-tests-to-cli/`](examples/add-tests-to-cli/) — a fully worked, generic example.
- [`examples/migrate-blob-storage/`](examples/migrate-blob-storage/) — a longer worked example: milestones, a cohort pilot, a supervisor directive in action, and the non-skippable milestone gate blocking until the supervisor audits and releases.
