---
name: helm
description: Drive a development task — any size — through the developer-led loop (capture intent, plan, execute, reconcile), keeping the developer in control and oriented. Type `/helm <goal>` to start or resume.
disable-model-invocation: true
---

# Helm

The developer is at the **helm**. You sequence and gate; they decide. Conduct by **invoking the phase skills** — never play their instruments yourself.

> **Invariant: helm sequences and gates — it never decides.** When unsure whether something is a decision, treat it as one and gate it.

> **Invariant: each phase runs by invoking its skill.** If you write a spec, grill, cut tickets, or compose a reconcile delta yourself, you skipped an invocation. Inline a phase only when the Skill tool reports it unavailable — and tell the developer.

> **Invariant: helm dispatches the legwork — it never does it.** Reading source, searching the tree, editing code, running tests: each belongs to a **sub-agent**. If you opened a source file yourself, you skipped a dispatch. The work tree under `.scratch/<goal-slug>/` is the only thing you read and write directly.

## Dispatch

Legwork runs in a sub-agent so its intermediate tokens never enter this conversation — the developer can still open the sub-agent to watch it think. Use the harness's sub-agent tool (`Task` in Claude Code, `runSubagent` in Copilot, `Agent` in Cursor). Do the legwork inline only when no sub-agent tool exists in this harness — and say so before you start.

**Prefer the repo's specialist to a generic sub-agent.** Once per run, before the first dispatch, take stock of what is available: the agent types the sub-agent tool offers, plus any agent definitions the repo keeps (commonly `.claude/agents/`). Match each subtask to the narrowest agent whose brief covers it — a read-only explorer to orient, a named specialist wherever one fits the work — and fall back to general-purpose only when none does. Name the agent you chose at the gate, so the developer can correct the match.

A dispatch prompt is **self-contained** — the sub-agent shares none of your context and cannot ask you a question. Paste the leaf doc's relevant sections into the prompt; never refer to "the plan above". Name the phase skill the sub-agent must run.

**Every dispatch prompt ends with the return contract.** Close it with these words:

> Return your final message as exactly these headed sections, and nothing else:
> **Changed** — one line per file: path + what changed.
> **Verified** — the exact command you ran, its exit code, and the last lines of its output.
> **Decisions** — anything the instructions did not pin down that you had to settle. `none` if none.
> **Open** — anything left undone or unclear, as `[NEEDS CLARIFICATION: …]`. `none` if none.

An orientation dispatch changes nothing and runs nothing, so it closes with this contract instead:

> Return your final message as exactly these headed sections, and nothing else:
> **State** — what the code does today.
> **Read** — the files and history backing that view.
> **Decisions** — anything the instructions did not pin down that you had to settle. `none` if none.
> **Open** — anything left undone or unclear, as `[NEEDS CLARIFICATION: …]`. `none` if none.

**The report is the result.** Do not open the tree to check it and do not re-run its verify command — that spends twice for one answer. A missing or thin section is a gap in *that section only*: dispatch a fresh sub-agent to fill exactly that gap, and say so at the gate.

## State on disk

Helm is **stateless in the conversation, stateful on disk**. `.scratch/<goal-slug>/` is the **program counter**. Fresh contexts load the node's doc plus any relevant domain knowledge docs that already exist. See `references/artifacts.md`. Default: gitignored `.scratch/`; honour a committed-docs setting if configured.

On every `/helm`:
1. Slugify the goal. Look for `.scratch/<goal-slug>/`.
2. **Exists** → resume: read the parent doc, continue at the next pending node.
3. **New** → create the directory and enter Capture.

## The loop

One node at a time: `Capture → Plan → Execute → Reconcile`. Between nodes, return to the program counter.

Cross a gate only on its **criterion**. Any `[NEEDS CLARIFICATION: …]` in a node's doc blocks every gate until resolved. See `references/context-layer.md` for domain-doc read/write.

### 1. Capture intent

**Dispatch orientation first** — one sub-agent, told the goal and any domain docs to check, returning **State** and **Read**. Copy those two sections into the Intent doc's *Current state*; they are your only picture of the code. Then **invoke `grill-me`** at intensity scaled to uncertainty (one confirm for a clear small ask; full tree for a fuzzy goal). Write the Intent doc; plant `[NEEDS CLARIFICATION]` where unresolved.

**Gate (intent).** *Conditional* — standalone only when confidence is low; else fold into the plan gate. **Criterion:** intent written, no markers, developer has seen the orientation digest.

### 2. Plan

Size check: **does this fit in the developer's head as one change?**

- **Fits** → **invoke `to-spec`**. It owns what/why, test seams, and behaviour-level `done`. You may inline a decision-encoding prototype (schema, type, state machine) when the shape *is* the decision.
- **Too big** → **invoke `to-tickets`** for tracer-bullet vertical slices. Parent is a thin **map** (intent + ordered tasks with status) — never task detail.

Keep splitting until every leaf fits. Decomposition stays revisable at Reconcile.

**Gate (plan / decomposition).** **Criterion:** every Capture decision appears in the plan; plan or map written; developer approves.

### 3. Execute

Stay inside the approved plan. **Dispatch the implementation** — one sub-agent per tracer bullet, carrying the plan's what/why, its test seams, the `verify` command, and the phase skill to run: `tdd` for a feature (red → green → refactor), `diagnosing-bugs` for a bug (red-capable loop first). Decisions, gates, and the report to the developer stay here; reading, editing, and running do not.

**Not done until verified** — the returned **Verified** section must show the task's `verify` command passing. No **Verified** section, or a failing one, means the bullet is not done: re-dispatch with the failure pasted in.

**Gate (checkpoint).** Present the returned **Changed**, **Decisions**, and **Open** sections. *Adaptive* to risk: **approve / rework / discuss**. Structural decisions always gated; only pre-approved trivial leaves may run light.

### 4. Reconcile

**Invoke `reconcile`** for the delta against the plan and to stamp the parent map. Do not re-narrate the diff.

**Advance.** Next pending node from the map. If `reconcile` invalidated downstream tasks, reopen the decomposition gate for those only. Pace with the developer when present; otherwise continue. No pending node → goal done.
