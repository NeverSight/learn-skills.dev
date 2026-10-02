---
name: agent-harness
description: >
  Designs a harness for a project — a team of specialist agents plus the
  skills each agent follows — from a one-sentence domain description. Use
  when the user asks to "build a harness for this project", "design an
  agent team", "set up an automation system for <domain>", or wants to
  restructure/extend an existing harness. Also use for maintenance
  requests on an existing harness: "audit the harness", "check harness
  status", "sync agents and skills". Use the `agent-harness-evolve`
  skill for retrospectives and feedback-driven improvement of a harness
  that is already running. Works with any coding agent that can delegate
  work to a subagent — it does not assume any single vendor's
  orchestration API.
---

# Agent Harness — designing agent teams and the skills they use

Design a harness for a project. Define each agent's role, and write the
skills each agent follows while working.

## Core principles

1. Agent definitions and skills always live at the **project level**,
   never under a home-level directory (`~/.claude/`, `~/.codex/`,
   `~/.copilot/`, etc.) — those are per-user personal config, not
   something the rest of the project's contributors or CI share. Reuse
   this project's existing agent/skill convention if one is already
   present (e.g. `.claude/agents/` + `.claude/skills/`,
   `.github/agents/` + `.github/skills/`). If no convention exists yet,
   don't guess from a memorized table — host tools change which
   project-level directories they auto-load across versions. Instead,
   check the current host tool's own authoritative self-documentation
   (a built-in docs/help tool if one is available, otherwise its
   `--help`/`/help` output or README) for the directories it reads at
   session start, and ask the user to confirm if that check is
   inconclusive. Record whatever convention you land on in the change
   log (step 4) so later sessions reuse it instead of re-detecting. If
   detection is inconclusive and nothing exists yet, fall back to
   `AGENTS/` for agent personas and `skills/` for skills. Agents say
   *who* does the work; skills say *how*.
2. Choose an execution primitive based on the shape of the work. If a
   sequence of steps and its repeat conditions can be fixed in advance,
   use **checklist-driven delegation**. If the same specialist needs to
   go back and forth on feedback, use **file-mediated coordination**. If
   a result is only needed once, use **one-shot delegation**. Full
   selection criteria are in step 2.
3. Choose a model tier per agent based on the task's complexity,
   duration, autonomy, and latency needs. Use **high-capability** for the
   hardest work that must plan and run autonomously over many steps;
   **general-purpose** for design, code generation, deep analysis, and
   cross-verification; **fast** for routine work like log parsing, format
   conversion, and simple collection. Full criteria are in step 3.
4. Record only the trigger condition and a change log for the harness in
   this project's top-level agent-instructions file. Don't assume a
   single fixed filename — multiple host tools each read their own
   file at the start of every session (`CLAUDE.md` for Claude Code,
   `GEMINI.md` for Gemini CLI, and `AGENTS.md` recognized by several
   tools including Codex and Copilot CLI), and which files a given tool
   reads can change across versions. Check the current host tool's own
   self-documentation for the filename(s) it reads, same as Core
   principle 1. If the project already has one of these files, append
   to it. If none exists and detection is inconclusive, default to
   `AGENTS.md` since it's the convention the most tools recognize
   today. Either way, a new session must be able to find the
   orchestrator skill from that file alone.
5. Keep feeding what you learn from running the harness back into the
   agents, skills, and that change log. Retrospectives and change-finding
   are `agent-harness-evolve`'s job.
6. Write every generated agent definition, skill, orchestrator, and
   change-log entry in the language the user is conversing in. Writing
   this skill document and its `references/` templates in English is not
   a reason to produce English output by default — translate template
   headings and example text into the user's language too. If the user
   sets a language explicitly, follow it; if they don't and you're
   extending an existing harness, follow that harness's existing
   language.

## Procedure

### Step 0: Check current state

When this skill loads, check the existing setup first.

1. Determine this project's agent directory and skill directory using
   Core principle 1 (reuse an existing convention, or detect the
   current host tool's recognized project-level directories via its
   own self-documentation rather than a hardcoded table), then read
   those directories plus the top-level agent-instructions file.
2. Pick a path based on what you find:
   - **Building from scratch**: if the agent or skill directory is
     missing or empty, run every step starting at step 1.
   - **Extending an existing harness**: if you need to add agents or
     skills to an existing harness, run only the steps the table below
     marks required.
   - **Operating or maintaining**: if you need to audit, fix, or
     resynchronize an existing harness, go to step 7's maintenance
     procedure.

   | Change | Step 1 | Step 2 | Step 3 | Step 4 | Step 5 | Step 6 |
   | --- | --- | --- | --- | --- | --- | --- |
   | Add an agent | Skip, reuse step 0's findings | Decide only which execution primitive and which team/stage | Required | When a dedicated skill is needed | Update the orchestrator | Required |
   | Add/modify a skill | Skip | Skip | Skip | Required | When wiring changes | Required |
   | Change structure/execution primitive | Skip | Required | Only affected agents | Only affected skills | Required | Required |

3. If an existing orchestrator references a proprietary multi-agent API
   this skill's host tool doesn't support (most commonly leftover
   references to another tool's workflow DSL or persistent-agent
   messaging API), treat it as ported from a different tool and offer to
   rewrite it using this skill's three portable primitives — see "Porting
   an existing tool-specific harness" in `references/execution-modes.md`.
4. Cross-check the actual agent/skill list against the change log and
   find any mismatches.
5. Report your findings and plan to the user and get confirmation.

### Step 1: Analyze the domain and the work

1. Identify the project's domain and goal from the user's request.
2. Break the required work into kinds: generation, verification,
   editing, analysis.
3. Check the shape of the workflow so you can choose an execution
   primitive:
   - Can the list of items to process be enumerated up front? (e.g. N
     files to move, M perspectives to review)
   - Does it need a verify-and-revise loop?
   - Does quality depend on agents exchanging opinions?
   - Does the same specialist need to stay in a single ongoing
     conversation?
4. Find overlaps or conflicts with the agents/skills discovered in step
   0.
5. Look at the codebase to learn the tech stack, data model, and major
   modules.
6. Match your explanations to the user's vocabulary and question level.
   Don't use terms like "assertion" or "JSON Schema" unassisted with a
   user who has little coding experience.

### Step 2: Design the execution primitive and team structure

#### 2-1. Choosing an execution primitive

Agent-harness recognizes three portable execution primitives. Every
coding agent capable of delegating work to at least one subagent can
execute all three; none of them require a specific vendor's API.

| Primitive | What it is | Suited to |
| --- | --- | --- |
| **Checklist-driven delegation** | The orchestrating session itself follows a plain-language procedure: dispatch step N, collect its result, feed it into step N+1; run independent steps as parallel one-shot delegations in a single turn. | Work where the item list, verification criteria, and repeat conditions can be fixed in code or in a written checklist ahead of time; large fan-outs; the result needs a consistent, reproducible structure across runs |
| **File-mediated coordination** | One or more delegated agents read a shared coordination file on entry and write to it on exit — a task list or structured hand-off note the orchestrating session maintains — instead of exchanging live messages. | A named specialist needs to keep context across several rounds of feedback, negotiation, or joint editing |
| **One-shot delegation** | A single call to a subagent/background-task tool. Only the result comes back; delegated agents don't talk to each other. | Work that doesn't need agents to converse and only needs a result once |

Decide in this order:

1. If the item list, verification criteria, and repeat conditions can be
   fixed ahead of time, use checklist-driven delegation. Fixing the
   control flow ahead of time, instead of leaving it to the model's
   in-the-moment judgment, is what makes a run reproducible.
2. If that's hard to fix ahead of time, and agents need to converse or
   remember earlier context, use file-mediated coordination.
3. If neither applies and you only need a result, use one-shot
   delegation.
4. If different stages need different primitives, mix them. Note each
   stage's primitive in the orchestrator.

Advanced multi-agent features (an explicit workflow-scripting tool, a
persistent-named-agent messaging tool) are an optimization some host
tools expose for primitives 1 and 2 — use them where available, since
they're more efficient, but every pattern in this skill must also work
with plain delegation and a shared file when they aren't. Keep the
default scale small — a handful of agents — and only scale up to a large
fan-out when the user explicitly asks for thorough/exhaustive coverage.

> For a detailed comparison, concurrency limits, and notes on porting an
> existing tool-specific harness, see `references/execution-modes.md`.

#### 2-2. Choosing a team pattern

1. Split the work by area of expertise.
2. Choose one of the six patterns below. Full criteria are in
   `references/team-patterns.md`.
   - **Pipeline**: stages process in a fixed order, each consuming the
     previous stage's output. Suited to checklist-driven delegation.
   - **Fan-out/fan-in**: independent work runs in parallel, then results
     are merged. Checklist-driven delegation; use the parallel-step
     variant only when you need all results before merging.
   - **Expert pool**: only the specialist matching the input is called.
     Suited to one-shot delegation (or file-mediated coordination if the
     same specialist needs a follow-up conversation).
   - **Producer-reviewer**: one agent produces, another reviews. Use
     checklist-driven delegation with adversarial reverification, or a
     file-mediated producer/reviewer pair.
   - **Supervisor**: a central agent tracks progress and reassigns work.
     File-mediated coordination with a shared task list.
   - **Hierarchical delegation**: an agent delegates to sub-agents, who
     may delegate further. Keep this within two levels; nest
     checklist-driven delegation at most one level deep.
3. If output accuracy matters, combine verification approaches:
   - **Adversarial verification**: attach N independent adversarial
     verifiers to each finding; only findings a majority mark
     `confirmed` with sufficient evidence pass. `refuted`/`uncertain`
     don't count as passing.
   - **Judge panel**: build N drafts independently, judge them in
     parallel, and base the final version on the strongest draft.
   - **Loop-until-dry**: keep searching until K consecutive rounds turn
     up nothing new.
   - **Multi-angle sweep**: search in parallel using different criteria
     (container, content, entity, time, ...).
   - **Gap reviewer**: have a final agent look only for what's missing.

#### 2-3. Criteria for splitting agents

Split agents by the expertise required, whether work can run in
parallel, how much conversational context must persist, and how likely
the agent is to be reused. Full table in "Criteria for splitting agents"
in `references/team-patterns.md`.

### Step 3: Write agent definitions

Define specialist agents you'll reuse across sessions as files under this
project's agent-definition convention (`{name}.md`). Don't put a role
you'll reuse only directly into a one-shot delegation's prompt.

- Defining it as a file is what makes it reusable in later sessions —
  reference it by name from whatever mechanism the host tool uses to
  select a custom agent/persona type.
- Fixing what agents exchange ahead of time is what makes collaboration
  results stable.
- Agents say who does the work; skills say how — keep them separate.

Put a specialist role you'll reuse into a file as a custom type, and
reference that file's name when you invoke it. Don't create a definition
file for a one-shot task that fits a built-in type (a generic
full-access type, a read-only exploration type, a read-only
planning type).

#### Check for overlap with existing agents

Before creating a new agent file, check whether its role overlaps an
existing agent in this project's agent directory. Do this even when
you've skipped step 1 to only add an agent — building or extending a
harness repeatedly is exactly how same-role agents pile up under
different names. If it overlaps, don't create a new name — reuse or
extend the existing agent. Criteria and the exception (deliberately
specialized domains) are in "Designing for agent reuse" in
`references/team-patterns.md`.

#### Model selection criteria

Choose a model tier per agent based on complexity, duration, autonomy,
and latency. Set it wherever this project's agent-definition format
exposes a model field, and record the reason as a comment in the agent
definition or orchestrator.

| Tier | Selection criteria | Representative work |
| --- | --- | --- |
| **high-capability** | The hardest work: planning and running autonomously over many linked steps | Agent orchestration, long-horizon planning and execution, synthesizing large amounts of material, turning a vague idea into something concrete |
| **general-purpose** | Scope is clear but needs deep reasoning and analysis | Design/architecture, code generation, complex analysis, cross-verification, critiquing research methodology, creative work |
| **fast** | Procedure is clear and speed matters more than depth | Log analysis, format conversion, static file checks, running deploy scripts, simple collection |

- Use high-capability when the plan for the next step depends on the
  previous step's result and must run autonomously over a long horizon.
  Use general-purpose to go deep on one bounded problem. For example,
  deeply critiquing a single paper calls for general-purpose; reviewing
  dozens of papers to build a strategy and final report calls for
  high-capability.
- Default to fast for ordinary work when the call is close.
- Don't mark every agent high-capability or general-purpose just because
  it feels important — choose the tier the actual work demands, not the
  agent's perceived status.
- Even when the coordinating top-level agent uses high-capability, pick
  each worker's tier independently based on its own task.

> Full tier guidance is in `references/model-selection-guide.md`.

#### What goes in a definition file

The definition's frontmatter must have `name` and `description`. Add
whatever this project's format uses to restrict available tools and to
set the model tier. For read-only review/analysis agents, remove
edit/write access so they can't change files.

Conversely, give agents that fix output both write and edit-in-place
access. Without edit-in-place, even a one-line fix requires rewriting
the whole file, and on large output an agent will give up on fixing it
and work around it elsewhere instead. Some lazily-loaded tools (shared
task-list operations, messaging) have been observed missing at call
time even when listed as available — have agents in file-mediated
coordination report, on their first update, which tools are actually
usable.

The body must cover the core role, working principles, input/output
rules, error handling, and how to collaborate. For agents using
file-mediated coordination, add a "## Coordination notes" section
specifying who else reads/writes the shared file and how.

> The definition template, full examples, and tool-restriction caveats
> are in "Agent definition structure" in `references/team-patterns.md`.

#### When including a QA agent

- Give the QA agent a type with full tool access. A read-only
  exploration type can't run verification scripts.
- Don't just check that files exist — cross-check the API response
  shape against what the frontend hook expects.
- Don't check only once at the end — check each module as soon as it's
  complete.
- Full method in `references/qa-agent-guide.md`.

### Step 4: Write skills

Write the skill each agent follows at `{skill-dir}/{name}/SKILL.md`.
Full guidance in `references/skill-writing-guide.md`.

#### 4-0. Check for overlap with existing skills

Before creating a new skill, check whether it overlaps an existing one
in this project's skill directory. If it overlaps, don't create a new
name — wire the existing skill to the agent, or extend it. Criteria and
the exception (deliberately specialized domains), and how far to
generalize, are in "Designing for skill reuse" in
`references/skill-writing-guide.md`.

#### 4-1. Directory structure

```
skill-name/
├── SKILL.md              # required
│   ├── YAML frontmatter  # name and description required
│   └── Markdown body
├── scripts/              # optional: code for repeated or
│                            must-be-deterministic work
├── references/           # optional: reference docs read only when needed
└── assets/               # optional: templates, images used in output
```

#### 4-2. Writing trigger conditions into `description`

The host agent decides which skill to load from its `name` and
`description`. In `description`, write concretely what the skill does
and the situations it must be used in, and distinguish similar-looking
situations where it should *not* be used.

**Bad example:** `"A skill for processing PDF documents"`

**Good example:** `"Reads PDF files, extracts text and tables, merges,
splits, rotates, watermarks, encrypts/decrypts, and OCRs. Always use
this when the user mentions a .pdf file or asks for a PDF deliverable.
Especially useful for conversion/editing/analysis beyond a plain
'read this PDF' request."`

#### 4-3. Body-writing principles

| Principle | How to apply it |
| --- | --- |
| **Explain why first** | Don't just list `ALWAYS`/`NEVER` — say why the rule exists. Knowing the reason lets the agent judge correctly in edge cases too. |
| **Keep it concise** | Keep `SKILL.md` under 500 lines. Delete or move to `references/` anything that doesn't help with judgment. |
| **Generalize to principles** | Don't write rules that only fit one example. Write judgment criteria that apply across inputs. |
| **Pre-bundle repeated code** | If multiple agents would rewrite the same script during testing, put it in `scripts/`. |
| **Write as directives** | Pick one consistent imperative register for the whole document. What must happen should be unambiguous. |

#### 4-4. Progressive disclosure

A skill loads information and executable code at these points:

| Information | Loaded | Recommended size |
| --- | --- | --- |
| **Metadata** (`name`, `description`) | Always | ~100 words |
| **`SKILL.md` body** | When the skill loads | Under 500 lines |
| **`references/`** | When that material is needed | No limit |
| **`scripts/`** | When running repeated or must-be-deterministic work | No limit; can run without being read first |

- As `SKILL.md` nears 500 lines, move detail to `references/` and note
  in the body when to read which file.
- Reference docs over 300 lines get a table of contents near the top.
- If guidance differs by domain or framework, split reference docs so
  only the needed file gets read.

#### 4-5. Linking agents and skills

- One agent can use more than one skill.
- Multiple agents can share the same skill.
- Skills say how to do the work; agents say who's doing it.

### Step 5: Wire it together and set execution order

The orchestrator is a skill too. It ties individual agents and skills
into one workflow and decides who collaborates when and in what order.
Full templates per primitive are in
`references/orchestrator-template.md`; delegation-procedure examples are
in `references/workflow-recipes.md`.

When extending an existing harness, edit the existing orchestrator
instead of creating a new one. When you add an agent, reflect it in the
composition, work assignment, and data-passing order, and add its new
trigger condition to the `description`.

#### 5-0. Orchestrator per execution primitive

- **Checklist-driven delegation**: the orchestrator skill writes out the
  procedure as a plain checklist (or a workflow script, if the host tool
  exposes one) — gather the fixed item list, dispatch one delegation per
  item, collect results, hand off to the next stage.
- **File-mediated coordination**: dispatch named delegations and
  coordinate through a shared coordination file (a task list or hand-off
  note) instead of a live messaging API. Delegations that need to keep
  context across rounds get re-invoked with the prior context plus the
  coordination file's current state.
- **One-shot delegation**: call the delegation tool N times in parallel
  in a single turn and collect results as they complete.

Mix primitives per stage when different stages have different needs —
for example, gather material with checklist-driven delegation, then have
a file-mediated pair reconcile it; or have a file-mediated pair draft
something, then run checklist-driven adversarial verification over it.
Mark each stage with `**Execution primitive:**`.

> Full per-primitive templates (with worked procedures and ASCII flow
> diagrams) are in `references/orchestrator-template.md`.

#### 5-1. Data-passing methods

| Method | How | Fits which primitive | Use when |
| --- | --- | --- | --- |
| **Structured return value** | A delegation call returns a schema-validated structured result (if the host tool supports it) | Checklist-driven delegation | The next stage needs to process the result programmatically |
| **Plain return value** | The delegation tool's own return message | One-shot delegation | The main session collects a summary directly |
| **Message** | Delivered directly between delegations | File-mediated coordination | Real-time coordination and feedback is needed, via whatever live-messaging tool the host provides |
| **Shared coordination file** | A task list or hand-off note that delegations read and update | File-mediated coordination | Managing progress, dependencies, and dynamic assignment |
| **File** | Write to and read from a fixed path | Any primitive | Data is large, or the process needs to be inspected later |

When passing data by file:

- Store intermediate output under `_workspace/` beneath the working
  directory.
- Name files `{stage}_{agent}_{artifact}.{ext}`, e.g.
  `01_analyst_requirements.md`.
- Only the final deliverable goes to the path the user specified;
  `_workspace/` stays for later verification.

#### 5-2. Error handling

Give the orchestrator an explicit error-handling policy: retry once,
then proceed without that result and note the gap in the final report
rather than deleting conflicting data; never retry failures that will
fail the same way again (quota exhaustion, expired auth, denied
permission); and when the orchestrator fills a gap itself, use only
facts it verified directly — don't guess at a stalled delegation's
judgment calls.

> Per-primitive mechanics (null-filtering a failed fan-out step,
> recovering a stalled file-mediated delegation, etc.) are in "Error
> handling" in the matching template in
> `references/orchestrator-template.md`.

#### 5-3. Scale

| Scale | Named delegations (file-mediated) | Delegation calls (checklist-driven) |
| --- | --- | --- |
| Small: under 10 tasks | 2-3 | 2-5 |
| Medium: 10-20 tasks | 3-5 | ~10; beyond the per-session concurrency limit, excess queues automatically |
| Large: over 20 tasks | Supervisor + 3-5 workers | Tens to hundreds; keep an overall cap (e.g. 1,000) |

- More agents cost more to manage. Keep the default scale small.
- If the user specifies a token budget (e.g. "+500k"), check remaining
  budget in the checklist/workflow logic and scale execution down
  accordingly.

#### 5-4. Recording the harness in the project's top-level instructions file

Once set up, record that a harness exists and its trigger condition in
this project's top-level agent-instructions file (per Core principle 4
— `AGENTS.md` by default, or whatever filename detection turned up).
That file is read every new session, so don't repeat detailed
execution rules there.

````markdown
## Harness: {domain name}

**Goal:** {the harness's core goal, one line}

**Trigger condition:** use the `{orchestrator-skill-name}` skill for
{domain}-related requests. Simple questions can be answered directly.

**Change log:**
| Date | Change | Target | Reason |
| --- | --- | --- | --- |
| {YYYY-MM-DD} | First built as agent-harness | Everything | - |
````

Don't put the agent/skill list, directory structure, or detailed
execution rules there — the orchestrator skill and the agent/skill
directories own that. The top-level file keeps only the trigger
condition and the change log.

#### 5-5. Handling follow-up requests

The orchestrator must work on a re-run or revision request, not just on
first execution: add follow-up phrasing (rerun, update, fix, redo just
one part, based on the previous result) to the `description`, check
prior work in the orchestrator's step 0 (rerun only the affected stage
if `_workspace/` has a partial match, start fresh into a timestamped
directory if there's new input, resume from a prior run identifier if
the host tool supports it), and document the re-invocation method in the
agent definition.

> Full `description`-phrasing guidance is in "Follow-up-request phrasing"
> in `references/orchestrator-template.md`.

### Step 6: Verify and test

Verify the harness you built. Full method in
`references/skill-testing-guide.md`.

#### 6-1. Verify files and references

- Confirm every agent file is in the right place.
- Confirm every skill's YAML frontmatter has `name` and `description`.
- Confirm agents that reference each other by name use matching names.
- Confirm you haven't created command/slash-command files unless this
  project's convention calls for them.

#### 6-2. Verify per execution primitive

- **Checklist-driven delegation**: confirm any fixed metadata is a
  literal (no non-deterministic values baked into cached state), that
  you only wait on a full parallel-fan-out step when you actually need
  every result, that null/failed results get filtered, and that stage
  names/titles match the plan's own stage list.
- **File-mediated coordination**: confirm who sends/reads what in the
  coordination file, task dependencies, and the delegation count.
- **One-shot delegation**: confirm each delegation's input/output chains
  correctly, parallel calls are batched into one turn, and no result is
  dropped while collecting.
- **Mixed primitives**: confirm each stage states its primitive and that
  data doesn't get lost across a primitive switch.

#### 6-3. Run-test each skill

1. Write 2-3 concrete test requests per skill, phrased the way a real
   user would.
2. Run with-skill and baseline side by side to measure how much the
   skill improves the result. If this needs repeating, turn the A/B
   comparison itself into a checklist-driven run.
3. Combine a qualitative pass (user review) with a quantitative pass
   (assertions). Fall back to user judgment where you can't write an
   objective check.
4. When you find a problem, fix it as a generalizable principle, not a
   rule that only blocks one example. Retest, and keep iterating until
   further fixes buy little.
5. If multiple agents keep producing the same code, move it into
   `scripts/`.

#### 6-4. Verify trigger conditions

1. Write 10 requests that should trigger the skill, in varied phrasing
   and explicitness.
2. Write 10 near-miss cases that sound similar but need a different
   skill or tool.

A clearly unrelated request doesn't test the boundary. For an
image-generation skill, "extract this spreadsheet's chart as a PNG" is a
better near-miss than "write a Fibonacci function" — the output is an
image, but a spreadsheet tool is actually the right fit. Also check for
trigger overlap with existing skills.

#### 6-5. Dry run

- Confirm the orchestrator's stage order is logical.
- Confirm the data-passing path isn't broken partway through.
- Confirm every agent's input matches the prior stage's output.
- Confirm the fallback procedure actually runs when something fails.

#### 6-6. Record test scenarios

Add a `## Test scenarios` section to the orchestrator skill with one
happy path and at least one failure path.

### Step 7: Operate, maintain, and improve

A harness isn't a one-and-done deliverable.

Retrospectives and feedback-driven improvement are `agent-harness-evolve`'s
job. Use it when the user asks to "retrospect on the harness", "evolve
the harness", or "apply this feedback". That skill analyzes the delta
between the initial setup and the current state, generalizes feedback so
it applies across situations, and updates agents, skills, the
orchestrator, and the change log.

This skill (`agent-harness`) handles operating and maintaining an
existing harness directly:

1. **Check current state**: compare the agent directory, skill
   directory, and orchestrator configuration, build a list of mismatches,
   and tell the user.
2. **Add/fix incrementally**: change one thing at a time and verify
   immediately after.
3. **Record the change**: log date, change, target, and reason in the
   top-level agent-instructions file.
4. **Verify the change**: check file structure. If it affects trigger
   conditions, test triggering too. If the change is large, also run the
   execution test and dry run, then do a final check that the
   top-level file matches the actual files.

Propose improving via `agent-harness-evolve` when:

- The same kind of feedback has come up twice or more.
- An agent keeps failing for the same root cause.
- The user keeps doing the same work manually, bypassing the
  orchestrator.

## Deliverable checklist

- [ ] Created a file for every reusable custom agent type under this
      project's agent directory, excluding one-off work that reuses a
      built-in type.
- [ ] Created the needed `SKILL.md` files and reference docs under this
      project's skill directory.
- [ ] One orchestrator skill covers data-passing method, error handling,
      and test scenarios.
- [ ] Documented which execution primitive(s) are in use — checklist-driven
      delegation, file-mediated coordination, one-shot delegation — and
      marked each stage's primitive if mixed.
- [ ] Chose each agent's model tier by complexity, duration, autonomy,
      and latency, with the reason in a comment. Didn't blanket-assign
      the same high-end tier to every agent.
- [ ] Didn't create unwanted command/slash-command files.
- [ ] Checked new agents/skills against existing ones for overlap before
      creating them. Where they overlapped and the domain wasn't
      deliberately specialized, reused or extended the existing one
      instead, with no name/role collisions.
- [ ] Wrote agent definitions, skills, the orchestrator, and the
      top-level change log in the language the user converses in. Used
      the user's explicit language choice, or the existing harness's
      language, where applicable.
- [ ] The skill `description` specifically states what it does, its
      trigger conditions, and follow-up-request phrasing.
- [ ] `SKILL.md` bodies are under 500 lines; moved detail to
      `references/` past that.
- [ ] Ran 2-3 test requests resembling real usage.
- [ ] Verified trigger conditions with both should-trigger requests and
      near-miss boundary cases.
- [ ] The top-level agent-instructions file records only the trigger
      condition and the change log.
- [ ] The orchestrator's step 0 distinguishes first run, follow-up run,
      and partial rerun, and covers resume options if the host tool
      supports them.

## Attribution

This skill is a derivative work of
[revfactory/harness](https://github.com/revfactory/harness), licensed
under the Apache License, Version 2.0. See `LICENSE` and `NOTICE` in
this directory for the full license text and a summary of what was
changed.

## Reference docs

- **Execution primitives in detail**: `references/execution-modes.md`
- **Model selection guide**: `references/model-selection-guide.md`
- **Team patterns and agent definitions**: `references/team-patterns.md`
- **Worked team-composition examples**: `references/team-examples.md`
- **Delegation-procedure recipes and caveats**: `references/workflow-recipes.md`
- **Orchestrator templates**: `references/orchestrator-template.md`
- **Skill-writing guide**: `references/skill-writing-guide.md`
- **Skill-testing guide**: `references/skill-testing-guide.md`
- **QA agent guide**: `references/qa-agent-guide.md`
