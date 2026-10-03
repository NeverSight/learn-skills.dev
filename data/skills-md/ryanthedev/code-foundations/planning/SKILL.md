---
name: planning
description: "Implements the Standard/Full planning pipeline for Medium and Complex tasks: multi-step discovery, phase decomposition with skill matching, cross-cutting concerns, and plan emission with Gate fields."
user-invocable: false
disable-model-invocation: true
---

# Skill: planning

Standard/Full planning pipeline: **Discover -> Classify -> Explore -> Decompose -> Detail -> Cross-cut -> Save -> Check -> Confirm -> Handoff**

The plan is written in stages, not one shot: DECOMPOSE fixes the phase shape and seams, DETAIL fills one phase at a time with a reset between each, CROSS-CUT derives the whole-plan sections. Each stage writes to the file in place.

The plan is a contract between plan and build. It specifies WHAT and WHY at the strategic level, with explicit interfaces between phases.

**User-facing output stays terse.** Only three steps run a full checkpoint — a structured render that ends the turn and waits for a reply: EXPLORE's decision gate, the Skeleton Checkpoint, and CONFIRM. A brief one-sentence declaration (CLASSIFY's verdict, a demotion notice) can still surface inline, immediately followed by the next step's work in the same turn — but it stays one sentence, never a restated deliberation trail. Everything else — DISCOVER's gate, DETAIL's per-phase reset — is internal bookkeeping the user never sees. If a step's output reads like a transcript of the reasoning ("X confirmed... Y confirmed... this matches the prior call"), it's wrong regardless of which step produced it.

**Thinking effort:** Planning is where the reasoning lives — it benefits from **high** effort. If the session is running lower, suggest the user increase it before proceeding. (Build runs the other way: low for all-serial plans, default for wave plans — see `references/plan-integration.md`.)

### Create Progress Tasks

`TaskCreate` one task per pipeline step (the ten named in the header line above), `TaskUpdate` with `blockedBy` to enforce ordering:

```
DISCOVER | CLASSIFY | EXPLORE | DECOMPOSE | DETAIL | CROSS-CUT | SAVE | CHECK | CONFIRM | HANDOFF
```

During DETAIL, add one sub-task per phase under it (one `TaskCreate` each), worked in DAG order.

At user checkpoints (EXPLORE decision gate, Skeleton Checkpoint, CONFIRM) the rendered artifact is the turn's final message — complete the step's task at the **start of the next turn**, after the user answers, so the bookkeeping never trails the presentation.

**CHECK runs on all tracks** — never skip independent review.

---

## Step 1: DISCOVER

DISCOVER runs **after** the plan command's shared steps (code-standards scan, clarify, confirmed problem statement). Do NOT re-run them. This step is the *delta*: deepen codebase research, and re-confirm the problem statement only if discovery contradicts it.

### 1a: Deepen Codebase Research

The code-standards scan already ran in the plan command's shared step 1 — `docs/code-standards.md` exists. Do **not** reload the code-standards skill. Deepen the research instead: how similar problems are solved here, existing libraries/patterns to reuse, and patterns intentionally omitted (check git history).

**See also:** [pattern-reuse-gate.md](${CLAUDE_PLUGIN_ROOT}/references/pattern-reuse-gate.md)

### 1b: Re-confirm Problem Statement (only on contradiction)

A confirmed problem statement already arrives from the plan command's shared step — clarification ran there, under its 5-round cap. Do **not** reload the clarify skill or re-clarify from scratch. Only if deeper research contradicts or materially broadens the stated problem do you re-confirm (see Output below).

### Gate (internal check, not narrated to the user) — proceed to CLASSIFY only when all three hold

- [ ] Codebase research deepened (pattern reuse + prior art checked)
- [ ] Track received from dispatch (Medium/Complex)
- [ ] Problem statement holds, or was re-confirmed after a discovery contradiction

### Output: Problem Statement

A confirmed problem statement arrives from the shared steps in the plan command. DISCOVER refines it with deeper codebase context — don't redo clarification from scratch.

Review the existing problem statement against what deeper discovery found. If it holds, proceed. If discovery reveals the problem is different or broader than stated, update it, render the updated statement as markdown in conversation, and end the turn asking: "Discovery found [X]. Does the updated statement still capture what you want?" — `[X]` is a short phrase naming what changed, not a restatement of the discovery research; the updated statement itself carries the detail. Content confirmations happen in conversation, where the full statement is visible (see Channel Selection in [adaptive-questioning.md](${CLAUDE_PLUGIN_ROOT}/references/adaptive-questioning.md)).

---

## Step 2: CLASSIFY

Classify using signals: files touched (Medium 4-8, Complex 9+), patterns (Medium 2-3 some new, Complex multiple cross-cutting), cross-cutting concerns (Medium 1-2, Complex 3+), uncertainty (Medium approach unclear, Complex requirements uncertain), phase count (Medium 3-5, Complex 5-7).

State explicitly: "This is a **[Medium/Complex]** task. [1-sentence justification]." This sentence surfaces inline — it isn't its own checkpoint — and leads straight into EXPLORE's research in the same turn. **If uncertain between Medium and Complex, choose higher** (this tie-breaker refines Medium-vs-Complex only; the plan command's "Default to Quick" already routed the task here).

**Demotion path — discovery reveals the task is actually Simple:** if the signals now read Simple (one focused change, 1-2 phases, no approach comparison needed), stop the pipeline and hand back to the Quick track in `commands/plan.md`. Do not force a 3-phase plan onto a one-thing change. Say so explicitly: "Discovery shows this is a Simple task — switching to the Quick track."

| Track | Phases | Approach Comparison |
|-------|--------|---------------------|
| **Medium** | 3-5, ~100-150 words/phase | 2 approaches |
| **Complex** | 5-7, ~100-150 words/phase | 2-3 + pre-mortem |

**Hard cap: 7 phases.** More than 7 -> split into multiple plans.

---

## Step 3: EXPLORE

**Research BEFORE proposing** -- uninformed proposals waste the user's decision-making.

### Load Design Vocabulary

`Skill(code-foundations:ca-architecture-boundaries)` — system-level vocabulary (boundaries, dependency direction, SRP-by-actor) for generating structurally different approaches here and shaping phase seams at DECOMPOSE. Module-level design skills (e.g. aposd-designing-deep-modules) are NOT loaded here — they get matched per phase at DECOMPOSE and loaded during DETAIL.

### Research (Medium/Complex)

**Codebase:** How similar problems are solved, existing libraries/patterns, intentionally omitted patterns (check git history).

**Web (when technology choice is involved):** Compare libraries/frameworks, check current best practices. Search for "[tech A] vs [tech B] [year]", "[domain] best practices [year]".

### Generate Alternatives

Approaches must be **structurally different** (different technology, pattern, or architecture):
- Good: "JWT tokens" vs "Session cookies" vs "OAuth2"
- Bad: "JWT with refresh" vs "JWT without refresh" (same approach)

Everything about an approach lives in its row — no prose paragraph per approach before or after the table. One clause per cell; if a cell needs two sentences, the approach isn't simple enough yet. Source is a short tag (a file or pattern name), not a citation sentence.

| Approach | What | Trade-offs | Best When | Source |
|----------|------|-----------|-----------|--------|
| Option A | [one clause] | [one clause] | [one clause] | [codebase/web] |
| Option B | [one clause] | [one clause] | [one clause] | [codebase/web] |

### Pre-Mortem (Complex Only)

| Failure Mode | Probability | Impact | Which Approach Survives? |
|-------------|-------------|--------|-------------------------|
| [failure] | LOW/MED/HIGH | LOW/MED/HIGH | [approach] |

### Recommendation + Decision Gate

Open directly with the table — no restating CLASSIFY or DISCOVER's conclusions first; those already happened, and the user needs the fork, not the trail that led to it. End the turn with the approach comparison rendered as markdown in conversation — the full table (what, trade-offs, best-when, research source per approach; pre-mortem for Complex) — then **name a recommendation with 1-sentence rationale** (not neutral presentation; the user wants an opinion) and ask which approach to take. The comparison must be the turn's **final message, with no tool calls after it**: an approach comparison is a content review, and the conversation is the only surface that renders it in full (see Channel Selection in [adaptive-questioning.md](${CLAUDE_PLUGIN_ROOT}/references/adaptive-questioning.md)).

The user answers free-form — an approach name, "your recommendation", or a different direction entirely.

**Gate: DETAIL starts only after the user has picked.** Writing "Going with X" and moving on skips the decision that anchors every phase body — the user must answer. If they've been terse, apply confirmatory mode: lead with "I'll go with [X] unless you'd rather one of the others."

Record chosen approach, rationale, and fallback — held in conversation until DECOMPOSE writes them into the plan file's `## Chosen Approach` (the file doesn't exist yet).

---

## Step 4: DECOMPOSE

Get the *shape* right before investing in phase bodies. Write the skeleton only — no internals yet.

### The Plan Is a Contract

The plan specifies WHAT and WHY. Subagents determine HOW. Four readers: orchestrator (phase names, ordering, DW counts), build-agent (goal, scope, constraints, approach notes, file hints), post-gate-agent (goal, done-when), human (strategic intent, rationale).

**No implementation details in phases** -- the build-agent writes pseudocode after fresh discovery. Cross-phase seams are the one exception: the Produces contract pins the interface; internals stay the build agent's latitude. **Plans must be pipeline-compatible** -- deterministic rules, not interactive user prompts between sub-phases.

### Define the Phases as a DAG

For each phase, write only:

- **Name** + **one-line goal**
- **Depends on / Unlocks** — the edges
- **Produces:** what this phase hands the phase(s) that consume it — the explicit seam. This is the interface the contract promises; designing it now is exactly what one-shotting skips.
- **Skills:** matched now so DETAIL can load them (see below)
- **Difficulty:** LOW / MEDIUM / HIGH

### Match Skills per Phase

Skills are matched HERE so DETAIL can load them while writing phase bodies — a phase body written without domain knowledge is the planner guessing.

1. Match against your **available-skills register** — every skill whose description is in context. That includes the 18 matchable internal code-foundations skills (`user-invocable: false`: model-discoverable, hidden from the slash menu; `planning` itself is excluded — `disable-model-invocation` keeps it out of the register) AND skills from other installed plugins (e.g. skill-craft, mcp-builder, security-guidance). Each description carries its own when-to-match and sibling-disambiguation (the "not for X (use Y)" clauses) — match on the descriptions directly.
2. For each phase, compare the phase's goal against every candidate skill's when-to-match conditions (register descriptions for external skills; catalog entries plus their disambiguation notes for the internal sibling pairs)
3. Assign skills whose triggers match the phase work. Most phases match 1-3 skills.
4. Exclude workflow commands and pipeline skills (plan, build, debug, research, code-standards, clarify, planning)
5. Write `**Skills:**` on every skeleton header — `none -- [reason]` valid, omission NOT valid

**`none` is the exception, not the default.** If a phase writes code, designs an API, refactors, handles errors, touches control flow, or modifies existing untested code — there is almost certainly a matching skill. DETAIL may add skills it discovers while writing bodies; SAVE validates the final set.

### YAGNI Gate + Phase Sizing

Before accepting each phase: Is it needed for success criteria? Could we ship without it? If "not needed now" -> remove. **Granularity test:** each phase produces a deliverable meaningful to the orchestrator and verifiable by the post-gate-agent. If it's an internal component of another phase's deliverable, fold it in.

Phase counts: Medium 3-5, Complex 5-7. Prefer fewer. Express independent phases as DAG -- don't artificially linearize.

### Skeleton Checkpoint

Catching a wrong decomposition here is far cheaper than after the bodies are written. End the turn with the full skeleton rendered as markdown in conversation, asking "Does the N-phase decomposition look right?" — the user replies free-form. Two rules make this checkpoint structural rather than skippable:

1. **The skeleton is the turn's final message, with no tool calls after it.** Nothing is written to disk yet, so there is nothing to chain into — dialog previews truncate multi-phase content and collapsed Write output doesn't count as presentation, which is why the conversation is the channel.
2. **The plan file is written only after approval** (next section). A skeleton the user never saw cannot become a plan.

Skeleton content shape (markdown):

```markdown
## Skeleton: N phases
1. **[Name]** — [one-line goal] (LOW/MED/HIGH)
   produces: [seam] → Phase 2
2. ...
DAG: 1 → 2 → {3, 4} → 5
```

On "adjust"-type replies: revise, re-present the updated skeleton the same way.

### Write the Skeleton to the File

After "Looks right": `mkdir -p .code-foundations/plans` and create the plan file at `.code-foundations/plans/YYYY-MM-DD-<topic-slug>.md` (see Step 7 schema). The header carries `# Plan:`, `**Created:**`, `**Status:** draft`, `**Complexity:**`; then Context + Constraints + Chosen Approach, then one header per phase carrying name, goal, Depends on / Unlocks, Produces, Skills, Difficulty. The file is built **progressively** across DECOMPOSE -> DETAIL -> CROSS-CUT -> SAVE — recoverable if interrupted. Do not commit it.

---

## Step 5: DETAIL

Fill in one phase at a time. **Create a task per phase** (`TaskCreate`, ordered by the DAG) and work them in order — a deliberate stop-and-reset so each phase gets fresh attention instead of degrading across one long pass.

### Per-Phase Loop

For each phase task, in DAG order:

**1. Reframe** (the reset — write it before the body):

> Phase N: [name]. Consumes: [upstream Produces, or "nothing -- entry phase"]. Must produce: [this phase's Produces]. Difficulty: [X].

**2. Load the phase's skills** (matched at DECOMPOSE). For each skill not already loaded this conversation, invoke it with the Skill tool — `Skill(code-foundations:<name>)` for this plugin's own skills, `Skill(<plugin>:<name>)` for external ones; each self-loads its own checklists. Skills load once — later phases reuse them. Apply them while writing Constraints, Edge cases, and Done-when. If the work reveals a skill the skeleton missed, add it to the field.

**3. Write the body** using the phase template below.

**4. Complete the task**, then move to the next phase.

### Phase Template

```markdown
### Phase N: [Name]
**Model:** [assigned at SAVE]
**Skills:** [matched at DECOMPOSE, loaded during DETAIL -- skills or `none -- [reason]`]
**Gate:** [Full | Standard | Minimal -- assigned at SAVE]

**Goal:** [One sentence (Simple) | 1-2 sentences (Medium/Complex)]

**Scope:**
- IN: [covered]
- OUT: [excluded]

**Constraints:** [non-discoverable requirements -- omit if none]
**Edge cases:** [boundaries + error paths this phase must handle -- skill-informed; omit if none]
**Depends on:** [none | Phase X] | **Unlocks:** [Phase Y]
**File scope:** [globs this phase may touch, e.g. `src/auth/**, tests/auth/**` -- enables wave parallelism during build; omit if unknowable, and the phase then never runs in parallel]
**Produces:** [what downstream consumes -- carried from skeleton. If the seam is code, state the contract: signature / type / route / schema -- not prose]
**Security-sensitive:** [yes -- ONLY if the phase touches auth, crypto, secrets, deserialization, or untrusted input; omit otherwise. Triggers 3-sample majority-vote REVIEW during build.]
**Rollback:** [required if the phase performs destructive or irreversible actions (data deletion, prod deploy, migration): the compensating action, or "point of no return -- [mitigation]"; omit otherwise]

[Medium/Complex only]
**Approach notes:** [non-discoverable user decisions -- omit if none]
**File hints:** `path/` -- [why relevant]
[/Medium/Complex only]

**Done when:**
- [ ] DW-N.1: [verifiable criterion]

[Medium/Complex only]
**Difficulty:** LOW / MEDIUM / HIGH  [carried from skeleton]
**Uncertainty:** [what could change, or "None"]
[/Medium/Complex only]
```

**DW-ID format:** `DW-{phase}.{item}` -- every done-when item gets a stable ID. **250-word cap per phase body.**

### Approach Notes

Only non-discoverable user decisions. **Test:** could codebase search find it? If yes, it does NOT belong.
- Good: "Use JWT not sessions -- user chose stateless for horizontal scaling"
- Bad: "Create a UserService class with getUser(), createUser()" (implementation detail)

---

## Step 6: CROSS-CUT

Derive the whole-plan sections now that every phase body exists — they fall out of the full phase set.

### Test Coverage (ask first — the level gates how much you derive next)

`AskUserQuestion`: "How much test coverage?" Options (a decisive pick, so the dialog is the right channel): **100% (Recommended)**, **Targeted** (user names the layers, e.g. backend only), **Per-phase**, **None**. On **Targeted**, ask in conversation which layers before recording. Record under `## Test Coverage`.

### Test Plan

Load `Skill(code-foundations:cc-quality-practices)` (skip if already loaded; it self-loads its checklists). Apply its Test Case Generation to derive test items, to the chosen coverage level:

- **Per-DW:** one test item per done-when item across all phases (Unit + Integration + Manual)
- **Boundary:** below / at / above each boundary named in the phases' Edge cases
- **Dirty:** error paths, bad data, wrong size -- aim toward the 5:1 dirty:clean ratio; every code-touching phase contributes at least one dirty test

### Assumptions + Decision Log (Medium/Complex)

Fill from the choices made during EXPLORE and DETAIL:
- **Assumptions** table: assumption, confidence, verify-before-phase, fallback-if-wrong.
- **Decision Log:** decision, alternatives, rationale, phase.

### Notes

Gotchas and open questions surfaced while detailing. Per-phase edge cases live in the phase bodies, not here.

---

## Step 7: SAVE

The file already exists from DECOMPOSE, with bodies and cross-cut sections filled. SAVE annotates each phase with a model, validates the skill assignments made upstream, then validates the whole file against the schema.

### File Location

`.code-foundations/plans/YYYY-MM-DD-<topic-slug>.md`

### Model Detection + Gate Assignment + Skill Validation

**Model detection per phase — every phase carries `**Model:**`; build stops on a plan that omits it:**

Rules are evaluated **top-down, first match wins**, against the phase's name + Goal (keywords) and its DW list + File hints (counts); an "area" is a distinct top-level directory in File hints:

```
FABLE_KEYWORDS = [refactor, architect, migrate, redesign, rewrite, overhaul,
                  new abstraction, novel pattern, system design]
HAIKU_KEYWORDS = [config, rename, typo, bump, cleanup, delete, remove,
                  backfill, data fix, sql update, doc update]

1. **Security-sensitive:** yes OR any FABLE_KEYWORD
   OR (DW items >= 6 AND file hints >= 4 areas)                  -> fable
2. DW items <= 2 AND file hints <= 1 area AND any HAIKU_KEYWORD  -> haiku
3. Otherwise                                                     -> sonnet
```

(The fable rule sits first so a security-sensitive "auth config cleanup" can never fall through to haiku on its mechanical keywords.)

**Why Sonnet is the default, not omit:** Omit means inherit the user's session model — and the session may be running fable, which then propagates to every subagent. Most code-touching phases (test, fix, validate, implement, wire, helper, hook, integration) are well-specified translation work that Sonnet 5 runs faster and cheaper without measurable quality loss. Reserve Fable 5 for the keyword-flagged judgment-heavy phases, where its depth pays. (`opus` stays valid only as an explicit user-requested override — e.g. when fable is unavailable.)

**Gate assignment per phase — every phase carries `**Gate:**`; build stops on a plan that omits it:**

Build consumes the `**Gate:**` field verbatim — `Full`, `Standard`, or `Minimal` (see `commands/build.md` resolution order, rule 2). The planner sets it here with the risk context in hand. Mirror build.md's risk rules:

| Risk signal in the phase | Gate |
|---|---|
| Security / auth / payment work (matches `**Security-sensitive:**`) | Full |
| Multi-file change introducing new cross-phase seams | Full |
| Docs-only or config-only change | Minimal |
| (none of the above) | Standard |

**What the gate now decides is review *timing*, not review *existence*.** Every phase gets reviewed. Full-gate and security-sensitive phases block their commit on a passing REVIEW; Standard and Minimal phases commit on a green suite and are covered by a later batch REVIEW (build.md → Batch REVIEW). So the per-phase question is no longer "is this worth reviewing" — it is "would a defect here be cheaper to catch before the commit than three phases later." That is what pushes a phase to Full: cascading blast radius, a seam every later phase builds on, or security exposure.

Skill presence does NOT decide the gate — every phase carries skills, so skills cannot discriminate gate level. Gate is keyed off the risk of the work itself, exactly as build resolves it.

**Review cadence — one field in the plan header, not per phase:**

Set `**Review cadence:** N` — how many un-reviewed phases may accumulate before a batch REVIEW fires. **Default 3; write it explicitly even when you take the default**, so the choice is visible to the user at CONFIRM instead of buried in build's fallback.

| Signal in the plan | Cadence |
|---|---|
| Phases tightly coupled — a defect in one propagates fast through the others | 1–2 |
| Ordinary mixed plan | 3 (default) |
| Phases genuinely independent (disjoint `File scope`, few shared seams) | 4–5 |

Above 5 build clamps it: a batch reviewer must verify every DW item across every covered phase, and per-item recall degrades as that list grows. The cadence is the one knob that trades review latency against reviewer context, so pick it from the plan's coupling, not from how risky the feature feels overall — per-phase risk is what `**Gate:**` is for.

**Dependency + file-scope validation:**

1. Every phase has `**Depends on:**` (`none` or `Phase X` refs) — build derives its execution waves from these edges; a missing field stops the build.
2. Every referenced phase exists; a phase consuming another's `Produces` depends on it.
3. Phases with no dependency path between them and disjoint `**File scope:**` globs will run their BUILDs in parallel — verify the declared scopes are genuinely disjoint. A phase without `File scope` never runs in parallel (that's the opt-out, not an error). Note build adds its own co-scheduling conditions (only Standard/Minimal gates share a wave, width ≤ 3, no shared mutable test resources) — don't promise parallelism in the plan summary for Full-gate phases.

**Skill validation (every phase carries `**Skills:**`):**

Skills were matched at DECOMPOSE and refined during DETAIL. Validate the final set:

1. Every phase has `**Skills:**` populated — `none -- [reason]` valid, omission NOT valid
2. Every skill name matches a real available skill present in your available-skills register — internal (code-foundations) or external (another plugin) (reject typos/nonexistent names)
3. No workflow commands or pipeline skills (plan, build, debug, research, code-standards, clarify, planning)
4. Code-writing phases with `none` justify why no skill's triggers match — on any gap, re-run the DECOMPOSE matching procedure for that phase

### Plan File Schema

```markdown
# Plan: [Topic]
**Created:** YYYY-MM-DD
**Status:** draft   <- flipped to `ready` at CONFIRM; build refuses a draft plan
**Complexity:** [simple/medium/complex]
**Review cadence:** 3   <- un-reviewed phases allowed before a batch REVIEW fires; 1-5
---
## Context
[Problem statement from Step 1]
## Constraints
- [constraints]

[Medium/Complex only]
## Chosen Approach
**[Name]** -- [Rationale]. **Fallback:** [1 sentence]
## Rejected Approaches
- **[Name]:** [1 sentence why rejected]
[/Medium/Complex only]

---
## Implementation Phases
(Use phase template from Step 5)
---
## Test Coverage
**Level:** [100% / Targeted: <layers the user named> / Per-phase / None]
## Test Plan
- [ ] [tests] [Medium/Complex only] + Integration + Manual [/Medium/Complex only]

[Medium/Complex only]
## Assumptions
| Assumption | Confidence | Verify Before Phase | Fallback If Wrong |

## Decision Log
| Decision | Alternatives Considered | Rationale | Phase |
[/Medium/Complex only]

---
## Notes
- [edge cases, gotchas, open questions]
---
## Execution Log
_To be filled during /code-foundations:build_
```

### Save

The file was created at DECOMPOSE (`mkdir -p .code-foundations/plans` already done). Ensure every phase has `**Model:**`, `**Gate:**`, `**Skills:**`, and `**Depends on:**` populated, the header carries `**Status:** draft` and `**Review cadence:**`, and the schema is complete — build hard-requires these fields and stops with "re-run /code-foundations:plan" when any is missing. **Do not commit** — the plan is a working document, not a deliverable. Building handles worktree visibility by copying the plan file after worktree creation.

---

## Step 8: CHECK

**ALL tracks:** Dispatch subagent to review saved plan with fresh eyes. Never skip — independent review catches blind spots regardless of task size. The reviewer runs on **fable**: the plan is the highest-leverage artifact in the pipeline, and one fable pass here is cheap insurance.

```
Agent: fable, "Review plan"
Prompt: Review .code-foundations/plans/<plan>.md for structural issues.

Checklist:
- Structural: every constraint maps to a phase, done-when items cover problem statement,
  no scope overlap, union covers full feature, depends-on references exist, no orphan phases,
  every phase has a Produces (handoff) -- code seams stated as contracts (signature/type/
  route/schema, not prose), phases with destructive/irreversible actions carry Rollback,
  phases touching auth/crypto/secrets/deserialization/untrusted input are marked
  Security-sensitive, approach notes only non-discoverable, file hints present,
  done-when observable + has DW-ID, YAGNI
- Coherence: no contradictions, each phase's Produces matches what its dependents consume,
  user-observable output exists, high-uncertainty phases early
- Tests: test plan covers every DW item; boundary + dirty tests derived from phase Edge cases
- Skills: every phase has Skills field (not omitted), skills match work type,
  each skill name matches a real available skill in the available-skills register — internal or external (reject typos/nonexistent names),
  code-writing phases with `none` justify why no skill's triggers match
- Gates: every phase has a Gate field populated (Full/Standard/Minimal), matching its risk
  (Full for security/auth/payment or new cross-phase seams; Minimal for docs/config-only; Standard otherwise).
  Full is what makes a review block its commit — flag any phase whose defects would cascade
  into later phases but which is only Standard, and any Full phase whose risk doesn't justify
  serializing the build around it
- Review cadence: header carries **Review cadence:** with a value of 1-5, and it fits the plan's
  coupling (tightly coupled phases -> 1-2; independent phases -> 4-5)
- Models: every phase has Model field populated (fable/sonnet/haiku -- opus only as an
  explicit user-requested override; never omitted)
- Dependencies: every phase has Depends on populated and referenced phases exist; a phase
  consuming another's Produces depends on it; phases declared independent have disjoint
  File scope globs (File scope absent is valid -- it just opts the phase out of waves)
- Header: **Status:** is present and reads `draft` (CONFIRM flips it to `ready`)

Output: PASS or FINDINGS with specific fix recommendations.
```

After return: PASS -> proceed. FINDINGS -> fix; **structural fixes (phase boundaries, DW set, Produces seams, Gate/Model/Skills assignments) -> re-run CHECK**; minor fixes -> proceed (mirrors CONFIRM's rule).

---

## Step 9: CONFIRM

End the turn with the full plan summary rendered as markdown in conversation, closing with "Does this look right? Anything to add or change?" The user replies in their own words.

**Shape:** one table for the phases (goal, model, gate, dependencies, skills — this is the part the user scans first), then a short bullet list below it — constraint → phase mapping, test coverage level, review cadence, seams, CHECK results — one line per bullet, not a paragraph each. The review-cadence bullet states it in plain terms ("Review cadence 3 — phases 1-3 commit on green tests, then get reviewed together; phase 5 blocks on its own review"), because it is the line that tells the user how much unreviewed code will exist at any moment. Summarize CHECK's outcome ("PASS" or "N findings, fixed"), never the verbatim finding text. If a seam or guardrail needs more than one line to state, it belongs in the plan file, not the summary; point to the phase instead of re-explaining it there. A doctrine deviation (e.g., skipping a re-CHECK after a fix) gets one sentence on what and why, then the ask — not a justification paragraph.

Two rules make this checkpoint structural:

1. **The summary is the turn's final message, with no tool calls after it.** The conversation is the only surface that renders a multi-phase plan in full — the user won't open the saved file, Write/Edit results render collapsed, and dialog previews truncate (see Channel Selection in [adaptive-questioning.md](${CLAUDE_PLUGIN_ROOT}/references/adaptive-questioning.md)).
2. **On approval, flip `**Status:** draft` → `**Status:** ready` in the plan file.** Build refuses a draft plan, so a plan the user never confirmed cannot execute.

If the user has been terse during planning, present with assumptions stated ("Approving means X and Y ship as specced") rather than asking open-ended "thoughts?"

### Corrections

If changes requested: update plan (Status stays `draft`). Structural changes -> re-run CHECK. Minor changes -> update and re-present.

---

## Step 10: HANDOFF

`AskUserQuestion` (a decisive two-option pick — the dialog is the right channel): "Plan saved and ready. How would you like to proceed?"

1. **Build now** (Recommended) -- Suggest the effort level for the build run (low if the plan is all-serial, default if any phase carries `**File scope:**` and is therefore wave-eligible — the plan carries the reasoning), then run `/code-foundations:build .code-foundations/plans/<plan>.md`
2. **Tell me what to do** -- Numbered manual steps

**Question style:** See [adaptive-questioning.md](${CLAUDE_PLUGIN_ROOT}/references/adaptive-questioning.md). The "Recommended" tag on Build now is the confirmatory cue — keep it there.

---

## Chain

- **Receives from:** plan command (router dispatch)
- **Chains to:** build (via saved plan file)
