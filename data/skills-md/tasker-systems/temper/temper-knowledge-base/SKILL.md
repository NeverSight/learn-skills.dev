---
name: temper-knowledge-base
description: Work with a Temper knowledge base over MCP — goals, tasks, sessions,
  research, decisions, search and contexts. Use when the user mentions their knowledge
  base, contexts, session notes, or a goal.
---

# Temper — Knowledge Base Workflow (MCP)

This is the **MCP packaging** of the temper workflow skill. Everything here happens through tool
calls against a Temper server. There is no vault to find, no `temper.toml` to read, and no local
directory that holds the truth — **the server is authoritative**, and it is the only thing you are
talking to.

> If you are working inside a checkout of the temper source repository with the `temper` CLI on
> PATH, you want the CLI packaging of this skill instead. This one speaks tools.

## What lives in a knowledge base

**Contexts** are workspaces that home resources. A context is addressed by **ref** — `@me/<slug>`
for your own, `+<team>/<slug>` for a team's, or a bare UUID. **Bare names are rejected**: pass
`"@me/temper"`, never `"temper"`. Every write and list input spells this field `context_ref`.

**Resources** are the documents themselves, each with a **doc type**. `references/frontmatter.md`
lists the recognized types and their schemas — read it rather than guessing: a name outside it is
accepted with no type schema, so a typo silently becomes a new type. The ones you will use are
`goal`, `task`, `session`, `research`, `decision`, `concept`, and `evidence` (a goal's evidence
record).

**Cognitive maps** are a different home: a telos-governed graph of *distilled* nodes rather than
resources as they are. See *Declared gaps* below before working in one.

## How this skill works

This file is the router. Read a supporting file when the work calls for it, not upfront.

| File | Read it when |
|------|--------------|
| `knowledge-base.md` | **The tool reference.** Which tool for which intent, reads vs writes, orientation, block-grain ingest |
| `references/frontmatter.md` | Before any write — the doc types, the two metadata tiers, what you may and may not send |
| `session-lifecycle.md` | Starting or ending a working session; mid-session drift; checkpoints |
| `session-wrap.md` | **Ending one** — what the note must hold, and the handoff preamble the next session starts from |
| `memories.md` | What a `memory`-typed resource is — how to read one, and how to author, correct and supersede one |
| `subagent-guidance.md` | Before dispatching any subagent |
| `plan-verification.md` | Before acting on a written plan's claims about code |
| `implementation-grounding.md` | Writing a plan, or writing code from one — including yourself |
| `review-gates.md` | **Before opening a PR** — when the change owes a code review and/or a security review pass, who counts as a reviewer, what a pass must return |
| `data-artifacts.md` | **Before storing structured data** — when to commit a data artifact vs. writing into a resource body, and the selection vocabulary |
| `outcome-registers.md` | **Authoring or amending a goal**, or deciding whether a criterion belongs on one |
| `working-a-goal.md` | **Working a goal** — uptake, resume, advance, record, decompose, close |

> **Read these as principles, not checklists**: a worked example is evidence *for* its principle,
> never the scope of it.

## Outcome Discipline — applies to every task, whether or not you author a goal

Four rules. They are short because they are always in force; the reasoning, the eight register
elements, and the worked failures are in `outcome-registers.md`, which you read **only** when
authoring or amending a goal or sub-goal.

- **A clause states what must be true, or must never be true, and names no mechanism still open at
  its altitude.** The *how* is the part that mutates, and a clause naming an open one propagates that
  commitment to every reader — most damagingly to an implementing agent, which builds the mechanism
  the clause named rather than the outcome it meant. A mechanism the frame owner chose in a cited
  `decision` is a prior: be precise about it, never vague to avoid it.
- **A witness is authored during the build, never in a preamble.** A witness must fail against the
  state its clause claims to change. When the mechanism does not exist yet, "fails against current
  state" is satisfied by the *absence of the feature* — vacuously, by anything. A clause whose
  mechanism is unbuilt carries a **declared hole, not a filed task** — until taken up; then the work
  answers to a clause it can be judged against, and if none exists, that clause is the missing goal.
- **Coverage is never inferred from absence.** A criterion with no evidence says so explicitly. A
  retired check leaves a named remainder, not a gap that reads as clean.
- **The discipline detects; it does not decide.** Reporting that something never ran, or that a
  criterion is uncovered, never concludes that the work should be dropped. Cost, churn and whether a
  goal is worth pursuing belong to the user, not to a criterion inside it.

## Starting a session

**The purpose comes first.** Before running `session-lifecycle.md`'s standing-state checklist —
or any listing — know what the session is for. If the user's ask is ambiguous, **ask before
doing anything else**; a ritual performed before the purpose is known is effort spent on the
wrong question. Then load the heavy context lazily: the checklist's reads are warranted when
the session will touch goals or tasks, not as an opening flourish.

## Starting work on a task

There is no `task start` tool. A task is a resource, and starting one is three calls:

```
Tool: list_resources   Input: { "doc_type_name": "task", "context_ref": "@me/<ctx>",
                                "stage": "backlog" }
Tool: get_resource     Input: { "id": "<task uuid>", "include_content": true }
Tool: update_resource_meta
Input: { "id": "<task uuid>",
         "managed_meta": { "temper-stage": "in-progress" },
         "open_meta": {} }
```

Stages are `backlog`, `in-progress`, `done`, `cancelled` — there is no "active".

**`update_resource_meta` takes both tiers, each a per-key patch** — a key you omit is untouched, a
key you send is replaced whole; `"open_meta": {}` touches nothing.

A task's `temper-mode` (`plan` / `build`) and `temper-effort` (`small` / `medium` / `large`) say how
much process the work deserves. If either is missing, ask. If the work drifts away from what they
say, `session-lifecycle.md` has the drift table.

## Creating a task

```
Tool: create_resource
Input: {
  "context_ref": "@me/<ctx>",
  "doc_type_name": "task",
  "title": "<title>",
  "content": "# <title>\n\n<problem statement>\n\n## Acceptance Criteria\n\n<criteria>",
  "managed_meta": { "temper-stage": "backlog", "temper-mode": "build",
                    "temper-effort": "medium" },
  "goal": "<goal ref>"
}
```

`goal` is a first-class field, not metadata: it projects a live `advances`→goal edge, which is the
only thing `list_resources`' `goal` filter reads. `update_resource` carries `goal` to re-point it and
`clear_goal: true` to retract it.

## Listing is capped — enumerate before asserting

**Never claim a goal, task, or session is absent — or that a set is complete — from one
`list_resources` call.** The response is a **page**: default 50 rows, `limit` maxes at 200. It
carries `total` alongside `rows`, and `rows.len() < total` means there is more you have not seen.

Before asserting absence or completeness, either **narrow** (`doc_type_name`, `stage`, `status`,
`tags`, `goal`) or **page** (`limit` + `offset`) until you have the whole set. An agent that reads a
short page as the full backlog reports the wrong state confidently, which is worse than reporting
nothing.

## Referencing other resources — full UUIDv7, and link it

**A UUID is not a SHA. Never abbreviate one.** A UUIDv7's leading bits are a **timestamp**, so
resources created near each other share a prefix *by construction* — a goal and the task written a
minute later routinely agree on their first seven characters, and the prefix resolves to nothing a
reader can follow. Write the full 36 characters everywhere — prose, tables, `open_meta`, commit
messages.

**When a document refers to another resource, write it as a markdown link:**

```markdown
[<the resource's exact title>](./<full-uuidv7>)
```

Resources are addressed **flatly** — there is no directory tree to be relative to, so `./<uuid>` is
the entire path and resolves wherever the body renders. Take the title from `list_resources` /
`get_resource`, not from memory (an approximate title is a citation that looks precise and is
not), and escape any `[`, `]`, `(` or `)` it contains, or the link will not render.

## Writing bodies

`create_resource` takes the whole markdown body in `content` and returns the finished resource — the
server chunks and embeds inline, so there is no second step and nothing to poll.

`update_resource`'s `content` **replaces** the body. Send the whole amended document, never a
fragment: a partial body is a silent truncation, not an append. To change only frontmatter, use
`update_resource_meta` and send no body at all.

**Because it replaces, verify what you are about to send.** `get_resource` hands you a *snapshot*,
and the gap between reading it and writing it back is where content disappears.

- **Re-read immediately before writing**, not once at the start of the work — `get_resource` again
  and re-apply to what is actually stored now
- **Assert at BOTH ends of a splice** — confirming your new text landed says nothing about what it
  displaced; prefer counting sections or naming markers over trusting a length
- **Prefer the narrowest write** — `update_resource_meta` when only frontmatter changes

This is operating discipline, not a lock. Writes are **not** mutexed, and deliberately so.

For a body too large for one call, for a resumable build, or for citation-grade per-block
attribution, use the `segmented_ingest` lifecycle and `annotate_resource` — `knowledge-base.md`
has both.

## Subagent dispatch

Before dispatching any subagent:

1. Read `subagent-guidance.md`.
2. Include the applicable principles in the prompt **verbatim, not summarized** — paraphrase is the
   loss that guidance exists to prevent.
3. If the subagent will write a plan, or write code from one, inject `implementation-grounding.md`
   verbatim. That is what it is for, and it is the one most often skipped.

> **This applies to you, too.** Nobody dispatches you in the main loop — load
> `implementation-grounding.md` yourself before writing a plan.

**Skills and plugins are looked up on request, not on arrival.** If the client exposes skills or
plugins, discover what exists when a dispatch is imminent — or when the user asks about quality
gates — then present the list and ask what subagents should use. Do not scan as an opening flourish.

## Declared gaps — what this packaging does not carry

Stated rather than left to be discovered, because coverage is never inferred from absence.

- **Cognitive maps.** The tool surface exists (`cogmap_*`, and `knowledge-base.md` covers the
  orientation trio), but the *authoring discipline* — the authored-4 under an invocation envelope,
  provenance, fold-then-recreate supersession, cross-map linking — ships only in the CLI packaging.
  Read from a map freely; before **authoring** into one, say so and ask.
- **Teams.** Creating teams, roles and offboarding have no guide here. Invitations and leaving
  a team do: see `invitation_read` / `invitation_manage` / `team_manage` in `knowledge-base.md`.
- **Project setup.** `/temper init` — fundamentals authoring and the onboarding flow — ships
  only in the CLI packaging; this surface has no slash command, skill directory, or wizard.
- **Per-cell workflow files.** The CLI packaging carries a file per `mode × effort` cell. They are
  written against CLI commands, so they are not shipped here rather than shipped wrong.
