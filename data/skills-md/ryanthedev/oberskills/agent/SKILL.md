---
name: agent
description: >-
  Subagent dispatch guidance for the Agent tool — whether to delegate or work
  inline, the four-part delegation contract, model and effort selection,
  parallel fan-out sizing, fork vs fresh subagent, and dispatching independent
  verifier agents. Use before any Agent tool call: spawning subagents, fanning
  out work across files or research angles, delegating exploration or review,
  briefing a verifier, or deciding whether delegation is worth it at all.
  Not for: wording a prompt that isn't an agent dispatch (use oberskills:prompt)
  or authoring reusable skill and agent definition files — structure,
  frontmatter, and evals (use oberskills:skill-craft); their prompt bodies
  (use oberskills:prompt).
when_to_use: >-
  Before calling the Agent tool. Trigger phrases: dispatch an agent, spawn a
  subagent, use subagents, fan out, parallelize with agents, delegate this
  search, research, or review, have an agent verify, run agents in parallel.
---

# Dispatching subagents

Guidance for writing `Agent` tool calls (the Task tool was renamed Agent in v2.1.63; `Task(...)` still works as an alias). A subagent is a context-isolation tool: it spends tokens in its own window and returns a distilled summary, so your window stays clean. That isolation is also the failure surface — the delegation prompt is the only channel in, and the return summary is the only channel out. Keep both channels precise.

Platform mechanics: `references/mechanics.md` in this skill directory · Orchestration patterns: `references/patterns.md` in this skill directory · Verifier dispatch: `references/verifier-dispatch.md` in this skill directory

## Host Mapping

Use the host's available subagent or delegation tool when present. If no such tool is available, work inline and state that the host has no subagent surface.

| Concept | Claude Code | Codex/other hosts |
|---|---|---|
| Spawn work | `Agent(...)` / Task tool | Host-provided subagent/delegation tool, when available |
| Wait or follow up | Agent return / resume | Host-provided wait or message operation, when available |
| No delegation surface | Work inline | Work inline |

## 1. The dispatch gate

Agents cost roughly 4x the tokens of working inline; multi-agent fan-outs cost roughly 15x (Anthropic multi-agent research system). Delegation pays for itself only when isolation or parallelism buys something — multi-agent beat single-agent Opus by 90.2% on breadth-first research precisely because the task decomposed into independent directions. Deciding how to dispatch is itself the first dispatch decision.

| Situation | Route | Why |
|---|---|---|
| Needs back-and-forth, or phases share heavy context (plan → implement → test on one artifact) | Inline | State dies at each subagent boundary; coupled work loses it |
| Quick targeted change; latency matters | Inline | Subagents start cold and re-gather context |
| Task needs mid-task user input | Inline | A subagent has no user channel — the harness strips `AskUserQuestion` from every subagent |
| Side question about content already in this conversation | `/btw` | Sees the full conversation but has no tool access — for what the session already knows, not for finding out something new |
| Side task that needs your full conversation context | Fork | Inherits the whole conversation and reuses the parent prompt cache — cheaper than re-briefing a fresh subagent. Always runs on your model |
| Self-contained task producing verbose output you won't reference again (test runs, log digs, doc fetches, codebase searches) | One subagent | The single most valuable use: tens of thousands of tokens explored, only the distilled summary returned |
| Independent items to process the same way (many files, many candidates, research angles) | Parallel fan-out, same turn | Independence is the requirement; see §4 for sizing |
| Output needs checking | Separate verifier subagent | Producers can't grade their own work; see §5 |

Once you've decided to delegate, pick the dispatch mode. Background versus foreground is set by the harness, not by a call parameter (Claude Code mechanics; details in the mechanics reference §7):

| Mode | Use when |
|---|---|
| Background (interactive sessions — every dispatch) | Always, interactively: you're notified on completion in a later turn, and a permission prompt from the subagent surfaces in your session rather than being denied. When the result gates your next step, the gate is waiting for that notification — keep to work that doesn't depend on it, and never predict the result |
| Foreground (fork mode off — headless `-p`/SDK; always for in-process teammates) | The harness blocks on a subagent when the result is needed before continuing; otherwise it still backgrounds |
| `subagent_type: "fork"` | The task needs your conversation, not a briefing (§1 gate row). A `model` override is ignored |
| `isolation: "worktree"` | Parallel agents writing to the same repo. Costs a temp worktree per agent; skip it for read-only work |
| `isolation: "remote"` | Long detached work in a cloud environment. Always background; availability is gated |

Where prompts *can't* surface — `dontAsk` mode, or a headless run with no permission handler configured (mechanics reference §7) — pre-grant every permission the task needs; otherwise a delegated edit fails while the subagent reports success.

Spawn-bias drifts across model generations — state trigger conditions in both directions: when a task fans out across independent items, delegate rather than iterating serially; AND when a single read or a sequential edit means just doing it.

## 2. The delegation contract

The delegation prompt is the only thing the subagent knows about your task. It does not see this conversation, your invoked skills, or files you've read. Thin prompts cause cold-start thrash: the agent re-discovers context you already had. Every dispatch contains four parts (Anthropic's orchestrator finding: without an objective, an output format, tool guidance, and clear boundaries, agents duplicate work and leave gaps):

```
OBJECTIVE   — the outcome, plus how you will use the result.
              "Find where user auth is implemented; I need the pattern to
              add OAuth" not "search for auth files".
OUTPUT      — the exact deliverable shape AND a size bound.
              "Return only the failing tests with their error messages" not
              "report the test run". Default bound: a distilled summary,
              roughly 1,000–2,000 tokens, no transcripts or file dumps.
TOOLS       — which tools/sources to use and which to skip; rate-limit notes
              (e.g. "arXiv calls sequential; S2/OpenAlex parallel").
BOUNDARIES  — what's in scope vs out; exact paths, branches, identifiers;
              write scope if any.
```

Add a CONTEXT block when the agent needs state from this conversation:

- Decisions already made (so it doesn't relitigate them).
- What was already tried and failed (so it doesn't repeat it).
- For multi-dispatch chains, the goal anchor: `ORIGINAL GOAL / COMPLETED SO FAR / CURRENT SUBTASK / REMAINING PLAN` — agents drift off-goal within 10–15 steps without it (ReCAP).
- Any CLAUDE.md rule the task depends on (e.g. "ignore vendor/") when dispatching Explore or Plan — those two built-ins skip CLAUDE.md and git status.

**Subagents don't inherit your skills.** A fresh subagent has zero awareness of skills you've used. Load them explicitly, as flat lines at the top of the prompt — agents execute flat `Skill(...)` / `Read(...)` lines but skip nested directives like "follow every instruction in that file". Resolve all paths yourself before dispatch:

```
Skill(oberskills:write)
Read(/abs/path/to/reference.md)
```

For a reusable agent definition (a file in `agents/`), prefer the `skills:` frontmatter field, which preloads full skill content at startup.

Write the objective as an outcome, not actions:

| Question | Bad | Good |
|---|---|---|
| What outcome do I need? | "Search for files" | "Find where user auth is implemented" |
| What will I do with the result? | "Look at it" | "Understand the pattern to add OAuth" |
| How will I know it succeeded? | "It returns something" | "File paths + the approach, in ≤1 page" |

If the objective can't be stated as an outcome because the user's own intent is ambiguous, run `oberskills:clarify` before dispatching. Length is fine; vagueness is not. For a long or novel brief — a new reusable agent definition, or instructions beyond a screen — invoke `Skill(oberskills:prompt)` for wording-level craft first.

## 3. Model and effort

Two levers, in order: drop effort before dropping a model tier. Lower effort on the same model is the cheap knob — Anthropic's effort table names subagents as the typical `low` use — and a weaker model running longer is not a substitute for a stronger one (a model upgrade beat doubling the token budget in Anthropic's testing). Don't compensate for a too-weak subagent by letting it run more.

**Where each lever binds (Claude Code).** The Agent call takes `model` but has no effort parameter: a subagent's effort comes from its definition's `effort` frontmatter, otherwise from your session. For an ad-hoc dispatch to a built-in type, tier and the scope of the brief are the only per-call levers, and the subagent runs at your session's effort. A worker role you dispatch repeatedly earns a definition file with `effort` pinned (field table: mechanics reference §3); in an API harness you own, set effort per request.

Effort semantics: `low` buys terse, direct execution with fewer tool calls; `medium` buys deliberation over alternatives; `high`+ buys extended reasoning on ambiguity. Defaults by role: low for bounded workers, medium for analysis and synthesis, high or above only for deciders. Effort steers thinking and tool-call volume, not prose length — a return that runs long needs a size bound in OUTPUT (§2), not lower effort. Level names don't buy the same amount of thinking on different models, and Anthropic's guidance on every recent release is to re-run an effort sweep rather than port settings, so treat these role defaults as starting points, not constants. At `xhigh`/`max`, leave room in `max_tokens`: thinking and response text share that cap (number in the snapshot). Behavioral deltas that follow from effort choices: the prompt skill's claude-models.md §5.

| Tier alias | Dispatch role |
|---|---|
| `haiku` | Read-only discovery: file search, classification, log/screenshot triage. Smallest context window of the lineup — don't hand it huge inputs |
| `sonnet` | Workhorse workers: extract, analyze, synthesize; parallel research fan-outs; code analysis |
| `opus` | Subagents that write code, make decisions, or carry tricky reasoning — and the default orchestrator (below) |
| `fable` | Escalation tier: work the tier below has failed at raised effort, or hours-long long-horizon runs. Rarely a subagent |
| omit `model` (inherit) | Default for writers and deciders, and the safe choice during capacity incidents, when an explicit `model: "opus"` can hang at "Initializing…" (mechanics reference §8). On a top-tier session this bills at the top tier — forks always do |

**Orchestrator default: start one tier below the top, escalate on measured failure.** Anthropic's model-selection guidance starts most work one tier below the top and moves to the top model for demanding long-horizon work, or when evals at raised effort still fall short. That is this section's ladder — effort first, then tier — applied to the orchestrator. Ratios price tokens, not tasks: a model can write longer responses, longer files, and more narration for the same job (the snapshot names which), so a flat per-token price can still mean a higher bill. The lever is a length bound in the contract and a conciseness instruction (the prompt skill's snippets.md #22), not effort.

Routing defaults: research/lookup → general-purpose with `model: "haiku"` (built-in Explore now inherits your model, so it is no longer cheap by construction — mechanics reference §2); extract/analyze worker → `sonnet`, from a definition with `effort: low|medium` when the role recurs; write/decide → inherit. When several sources set a subagent's model, the per-call `model` wins — except on a fork, which ignores it and always runs on your model. Full resolution order: mechanics reference §1.

### Lineup snapshot — verified 2026-09-21

The guidance above reads correctly without this block; at the next model release, edit here. Aliases resolve to the latest model in each tier (`claude --help`: "an alias for the latest model"), so a dispatch written today follows the next upgrade. Sources, all fetched on that date: Anthropic's pricing page, models overview, choosing-a-model guide, effort page, and the Opus 5 and Fable 5.1 prompting pages.

| Alias | Model (ID) | Input / output per MTok | vs Haiku | Context / max output |
|---|---|---|---|---|
| `haiku` | Haiku 4.5 (`claude-haiku-4-5-20251001`) | $1 / $5 | 1x | 200K / 64K |
| `sonnet` | Sonnet 5 (`claude-sonnet-5`) | $2 / $10 | 2x | 1M / 128K |
| `opus` | Opus 5 (`claude-opus-5`) | $5 / $25 | 5x | 1M / 128K |
| `fable` | Fable 5.1 (`claude-fable-5-1`) | $10 / $50 | 10x | 1M / 128K |

- **Pricing.** Sonnet 5's $2/$10 launched as introductory and is now the standard price; the scheduled rise to $3/$15 was cancelled. Fable 5.1 cache reads bill at 0.025x input ($0.25/MTok) against 0.1x on every other model — under Opus 5's $0.50 — which softens the top-tier premium for forks and long-lived subagents on a warm cache. Models from the Opus 4.7 generation on use a tokenizer that produces roughly 30% more tokens for the same text; Haiku 4.5 predates it, so the ratios understate the per-text gap. Check the claude-api skill for live pricing before cost-sensitive choices.
- **Orchestrator.** "If you're unsure which model to use, start with Claude Opus 5 for most workloads. Use Claude Fable 5.1 for demanding reasoning and long-horizon agentic work, or when your evals on Claude Opus 5 at higher effort still fall short" (models overview; the choosing-a-model guide puts the trigger at `xhigh` or `max`). Fable 5.1 sits a tier above Opus 5 rather than level with it: Anthropic's launch benchmarks put it ahead, most on long-horizon agentic work and least on contained coding. That evidence is vendor-reported and third-party scores were only seen secondhand in this sweep, so none is carried here — the start-on-Opus default rests on cost and Anthropic's recommendation, not on parity. Fable 5.1 also requires 30-day data retention (no ZDR without Anthropic's authorization); Opus 5 does not.
- **Effort.** Opus 5 and Fable 5.1 take all five levels and default to `high`. Opus 5: "use `low` and `medium` liberally" where evals hold, `xhigh` for demanding coding and agentic work, and at `xhigh`/`max` start `max_tokens` at 64K and tune from there. Fable 5.1: `medium` roughly matches Fable 5 at lower cost, `low` is often competitive with smaller models on cost per task, and at `high` and above it asks for a large `max_tokens` without naming a figure. Haiku 4.5 does not take the effort parameter — tier is the only lever there — and its retirement floor is 2026-10-15, so expect the `haiku` alias to move.
- **Behavior.** Opus 5 delegates to subagents more readily than earlier models (§4 caps it), verifies its own work unprompted (§5), and writes longer responses and files; on Opus 5 "changing effort does not reliably shorten responses," so prompt for length.

## 4. Parallel fan-out

Size the fan-out to the task — overinvestment is the classic failure (Anthropic's early orchestrators spawned 50 subagents for simple queries):

| Task shape | Agents | Tool calls each |
|---|---|---|
| Simple fact-finding / lookup | 1 | 3–10 |
| Direct comparison | 2–4 | 10–15 |
| Complex decomposable research | up to 10, clearly divided | — |

Default ceiling 3–5 parallel agents; coordination overhead beats returns past about 3 when agents interact or refine each other's work — fully independent, non-overlapping fan-outs tolerate up to ~10 (distinction and sizing evidence in `references/patterns.md` in this skill directory).

**Current models reach for subagents readily — cap it.** Anthropic's Opus 5 guidance is that delegation "multiplies cost and time when applied to small tasks" and that harnesses should "give explicit guidance on which scenarios warrant delegation, or set deterministic caps on how many agents can be launched" (in Claude Code, the depth and concurrency variables in the mechanics reference §1). Older models under-delegated, so any "delegate more" instruction written for one should be deleted rather than kept alongside a cap. Verbatim cap block: "Delegate to a subagent only for large tasks that are genuinely independent and parallelizable, such as a wide multi-file investigation. Do not delegate work you can finish yourself in a handful of tool calls, and do not use subagents to verify or double-check your own work. If one subagent can complete the task, use one rather than several, and keep spawn counts low."

- Spawn all independent agents in the same turn; request parallelism concretely ("use three subagents, one per module") — the model is conservative about parallelism unless told.
- Agents must be independent. If outputs feed each other, run them sequentially from here.
- Never give parallel agents overlapping write scopes.
- Group fan-out by rate-limited resource (parallel agents hammering one API produce 429s).
- Each returned summary lands in your window — five verbose reports refill the context you were protecting. The OUTPUT bound in every contract is what keeps fan-in cheap.

## 5. Verification dispatch

Never have the producing agent validate its own output — models catch fewer than half of their own errors (evidence in the verifier reference). Verification is a separate dispatch with three rules:

1. **Deterministic checks first.** Tests, typecheck, lint, and builds run before any LLM judgment, and their results go to the verifier as raw output.
2. **No intent framing.** The verifier dispatch carries no plan context, no "this implements X", no progress narrative — conclusion framing can collapse defect detection almost entirely. Hand it the artifact, the checks, and the acceptance criteria. Nothing else.
3. **Verifier may be a weaker model.** Checking is easier than producing; downgrade one tier (opus producer → sonnet verifier). How good any one model is as the *sole* reviewer of correctness-critical code is contested — the vendor's claim and the one third-party benchmark disagree for the current lineup (verifier reference, rule 5) — so on concurrency-heavy diffs let deterministic checks carry correctness rather than a single LLM pass.

**Reconciling this with the delegation cap (§4).** Anthropic's cap block says "do not use subagents to verify or double-check your own work," which reads like it contradicts this section. It doesn't: the target is *reflexive* verification scaffolding inside a working loop — an agent spawning a checker because the prompt told it to always verify, which is redundant with what Opus 5 already does unprompted. This section is about the orchestrator commissioning an independent verification dispatch for a high-stakes artifact, with no intent framing and deterministic checks first. Delete the standing "always add a verification step" instruction; keep the deliberate verify dispatch.

Ask for coverage, not pre-filtered findings: report every issue including low-severity or uncertain ones, with confidence and severity per finding — a separate step filters (a "high-severity only" instruction is followed literally and reports less — Opus 5 prompting page). Cap verify→revise at two rounds, then escalate to the user.

Template and evidence: `references/verifier-dispatch.md` in this skill directory.

## 6. Failure modes

When a dispatch goes wrong, fix the prompt before the model — prompt engineering on the orchestrator was the primary lever in every failure class Anthropic observed.

| Failure | Mechanism | Fix |
|---|---|---|
| Cold-start thrash | Thin delegation prompt; agent rediscovers known context | Front-load paths, decisions, failures into CONTEXT (§2) |
| Results too narrow | Over-constrained prompt | Remove constraints first; don't add more |
| Results too broad / wrong focus | Vague objective or misleading context | State the outcome plus how you'll use it |
| Return bloat | No output bound | Size-bound every OUTPUT ("only the failing tests…") |
| Duplicate / gapped fan-out | Missing boundaries between agents | Explicit non-overlapping scopes per agent |
| Goal drift in chains | No anchor; drift sets in within 10–15 steps | Goal-anchor block in every chained dispatch (§2) |
| Lost state at handoff | 42% of multi-agent failures are handoff context loss (VulnBot) | Summarize state + original goal + tried-and-failed at every handoff |
| Retry loop | No failure memory | List failed approaches; after 2 failures force a categorically different strategy, then escalate |
| Silent edit failure | Permission prompt auto-denied where nobody can answer it (`dontAsk`, or a headless run with no permission handler) | Pre-grant the permissions, or keep approval-gated edits in the parent |
| Quit-early / fabricated done | Agent reports completion without evidence | Require evidence per claim in OUTPUT; verify via §5. Don't bolt on forced-continuation scaffolds — they help o-series models and hurt Claude (numbers in the prompt skill's porting reference) |
| Shallow results on hard task | Model or effort too low | Raise effort first, then tier (§3); if raised single attempts still fail, dispatch 3–5 short scoped attempts and majority-vote (patterns reference §2) |
| Subagent context overflow | Oversized delegated job | Scope to fit; split the task, not the window |

## 7. Going deeper

- `references/mechanics.md` in this skill directory — Agent tool parameters, model resolution, nesting and caps, built-ins, the canonical subagent frontmatter field table, schema-level boundaries, forks and `/btw`, background and resume, gotchas.
- `references/patterns.md` in this skill directory — orchestration pattern catalog, multi-agent sizing evidence, topology selection, long-run harness patterns, defect diagnosis.
- `references/verifier-dispatch.md` in this skill directory — debiased verification rules, evidence, and a copyable verifier dispatch template.

Authoring a reusable subagent `.md` definition — file structure, frontmatter, and evals → `Skill(oberskills:skill-craft)`; its prompt body → `Skill(oberskills:prompt)`.
