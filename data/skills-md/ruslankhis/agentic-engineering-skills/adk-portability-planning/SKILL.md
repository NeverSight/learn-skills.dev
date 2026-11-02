---
name: adk-portability-planning
description: >-
  Assess how dependent an accepted Google ADK on GCP design is on Google Cloud
  and ADK, and write a separate, stakeholder-ready portability plan: provider
  dependencies, AWS and Azure alternatives, a small comparison of other agent
  frameworks, model portability, the replacement boundaries worth having,
  migration risks and a phased alternative outline with relative effort. Use
  when a portability goal or ticket names this skill, or when stakeholders ask
  about vendor lock-in, an exit plan or moving to another cloud or framework
  for an existing design. The GCP and ADK design stays the primary build; this
  skill writes docs/portability/<topic>.md and changes no code. Do not activate
  to choose hosting on Google Cloud (deploy-adk-on-google-cloud), to configure
  model failover (adk-model-and-output-contracts), to connect MCP or A2A peers
  (adk-agent-interoperability), or to build or migrate an application on
  another platform.
license: MIT
metadata:
  author: "Ruslan Khissamiyev"
  source-book: "Agentic Engineering"
  source-chapter: "cross-cutting"
  sources-reviewed: "2026-10-26"
  verified-against: "not applicable: writes portability plans; google-adk 2.13.0 source read 2026-10-26"
  version: "2026.10.28"
---

# ADK portability planning

## Purpose and boundaries

Answer one stakeholder question about an accepted GCP and ADK design: what
would it cost to move this later, and which parts are worth keeping
replaceable now? Write one document, `docs/portability/<topic>.md`, from the
[assessment template](assets/portability-assessment-template.md). It is an
**exit plan** (movable later at a known cost), planning only: GCP and Google
ADK stay the primary build, and the design, the plan's other goals, the
default framework and the code stay as they are. Describe alternatives as
responsibilities, options, differences and costs; implementation on a target
belongs to a later goal, if one is ever approved. Name the provider-specific
dependencies that remain and size them. Improvements to the current GCP build
go only under "Optional recommendations" and become tickets only after a
designer checkpoint approves them.

## When it runs

A `portability` goal or ticket names this skill, or a stakeholder asks about
lock-in, an exit plan or another cloud or framework for an existing design.
A design still marked draft is enough: assess it as it stands and carry its
open decisions that change a classification into "Open questions". Without
a design (`docs/architecture/<topic>.md`), say so and stop with this prompt
instead of designing:

```text
/adk-system-designer Design <application> on GCP and ADK. Record in the scope
gate that portability is a concern (raised by <who>, targets <named targets or
none named>), so the plan gains a portability goal.
```

## Read the record

Before writing anything, record the design's fingerprint in the ticket's
Evidence as `design before: <value>`, from `git hash-object
docs/architecture/<topic>.md` (it works whether or not the file is
committed). Read, noting the ID of every fact you will use: the ticket or plan goal
(acceptance items, `touches`, named targets); the design (requirements `R`,
contracts `C`, decisions `D`, and the scope-gate row "Portability or lock-in concern":
who raised it, what they fear, targets named); the plan (goals `G`,
measurement records `M`; in compact form the plan is the design file); and
the discovery brief, when it exists, for stakeholders and their calendar.
When code exists, inspect it for the provider dependencies it actually has:

```bash
grep -rnE "from google\.cloud|import vertexai|from vertexai|from google import genai|google\.genai|google\.adk\.tools\.(vertex|google_search)|VertexAi[A-Za-z]+|GcsArtifactService|google_search|bigquery|firestore|LiteLlm" --include='*.py' .
```

Mark each baseline fact `inspected` or `design-only`. A design that says
Postgres while the code imports Firestore is an open question, not a fix.

## Pin the concern

- Quote the stakeholder question, with who asked and when.
- Decide which question it is: **moving later at a known cost** (an exit
  plan: the default) or **running on several providers now** (multicloud:
  only on a stated need with a date or trigger). Write the answer in
  "Concern and scope".
- Take targets from the ticket or scope gate. When none are named, assess AWS
  and Azure plus the frameworks in the
  [framework reference](references/agent-frameworks.md) (LangGraph, OpenAI
  Agents SDK, Microsoft Agent Framework, Pydantic AI; Strands only as a short
  AWS row), and say in "Concern and scope" that the default was used.
- Keep **model swap** and **whole-system move** apart. A model behind the
  same ADK agent on GCP is a model change with a re-evaluation; a cloud or
  framework move is a system move. If the fear is model lock-in, the answer
  may be the model swap alone.

## Classify every component

Read [principles](references/principles.md) before classifying. Ask, in this
order, and stop at the first class that fits:

1. **shared logic**: no provider imports; moves with a test run.
2. **replaceable adapter**: a cheap port; no data conversion, same behaviour.
3. **provider-specific by choice**: kept for its value; a bounded rewrite.
4. **expensive dependency**: data to move or regenerate, changed semantics,
   re-evaluation or a repeated approval.

Use these exact class names; the checker accepts no others.
**Cheap seam, expensive switch:** an ADK seam (`BaseSessionService`,
`BaseMemoryService`, the model connectors) makes the code cheap to change
but leaves the model, Memory Bank or a RAG corpus an expensive dependency.
Put the seam in "Exit path" and the class from the switch. Every row cites
its design IDs and a Why; every expensive dependency names its exit path.

## Assess the five dimensions separately

Cloud, agent framework, model, service and deployment each get a row:
assessed, or `not a concern: <reason>`, the reason a fact ("one Cloud Run
container, no Agent Runtime features"). Their costs differ, but one strategy
usually answers all five: write one, not a solution per dimension.

## Boundaries worth having

Propose or keep a boundary only when one of the four rules in
[principles](references/principles.md#when-an-abstraction-pays) holds: (a) a
second implementation is needed now (a CI fake under a contract test
counts), (b) a stated switch requirement with a date or trigger, (c) the
framework already has the seam, (d) it cheaply isolates a volatile vendor
API. Under (c), name ADK's seam and use it; a wrapper around
`BaseSessionService` or the model registry is a shallow module. Otherwise
record an exit path instead. Never put a common interface over a managed
feature the design relies on (Memory Bank extraction, grounding, RAG Engine
ranking).

## Compare alternatives

- Clouds: read [AWS](references/aws.md) and [Azure](references/azure.md) for
  the targets in scope; one row per responsibility the design uses.
- Frameworks: read [agent frameworks](references/agent-frameworks.md); a small
  table, ADK first, limited to the features this design relies on. Cite
  vendor-authored pages (Pydantic AI's ADK comparison) as vendor-authored.
- Keep every `unverified` marker the references carry.
- Re-verify each volatile fact that drives a classification or risk (model
  availability, GA or preview status, hosted-agent support) at its source when
  web access exists, recording the URL and read date in "Sources". Without
  web access, cite the reference's URL and read date, and say so.

## Recommend the simplest strategy

Recommend the least work that answers the concern, usually: keep the build,
hold the exit plan, name the trigger that would reopen it. State the
trade-offs and why multicloud now is or is not justified. The checker rejects
"fully portable", "drop-in replacement", "cloud-agnostic" and similar phrases
unless a negation comes just before them; quote a stakeholder's own words in
quotation marks.

## Phased outline

A few high-level phases from
[principles](references/principles.md#phasing-patterns): a model candidate on
the frozen evaluation set first, a strangler façade or parallel run, data
backfill with change capture and checksums, evaluation sets re-run per
category, cutover with GCP kept as the rollback. No commands or schedules.

## Relative effort

One row per item: `small`, `medium`, `large`, `very large` or `unknown`
(write "unknown; needs a spike" rather than guess), the drivers and the
assumptions. Size by the largest driver, not the sum. Any item needing
re-evaluation (model, framework, retrieval) is at least medium. Show
contractual, compliance or client re-approval as a separate schedule risk.
Write durations, dates or money only when a plan record (`M2`) or the word
`assumption` sits in the same cell or sentence.

## Optional recommendations

`None.`, or one `###` block each with **What**, **Rationale**, **Acceptance
criteria**, **Specialist** (an installed sibling skill in backticks, such as
`adk-agent-evaluation`) and **Status:** proposed; needs a designer checkpoint.
Recommend only what cheaply lowers a switching cost in the current GCP build.

## Open questions

What only stakeholders or platform teams can answer: a move's date or
trigger, calling Gemini across clouds, approved models, design-code mismatches.

## Check and hand over

Run the checker from the project root, resolving `SKILL_DIR` to this skill's
directory:

```bash
python3 "$SKILL_DIR/scripts/check_portability.py" docs/portability/<topic>.md \
  --design docs/architecture/<topic>.md --plan docs/plans/<topic>.md
```

Its docstring lists every rule. Fix every error and review the warnings; a
pass checks form, not the architecture. Then confirm the design is
unchanged: this prints the value recorded as `design before`:

```bash
git hash-object docs/architecture/<topic>.md
```

Keep checker output in the ticket's Evidence rather than in `.adk-evidence/`:
the ticket touches only the assessment, so this session creates no other file.
Fill the ticket's Evidence per `adk-engineer` conventions: the assessment
path; the checker's result line; `design before` and `design after` values; targets and
frameworks assessed; the five dimensions with their outcome; each acceptance
item tagged `(deliverable)` with what showed it; the unverified claims the
recommendation rests on; the recommendations awaiting a checkpoint; an
`actual:` line with the human hours reported. Set the status to
`verified_local` when the checker passes and the two values match; the owner
sets `done` on acceptance.

End with the run prompt for the next ready goal, for example:

```text
/adk-engineer Carry out <next goal> from docs/plans/<topic>.md. Read
docs/architecture/<topic>.md, use the goal's primary and supporting skills,
verify its acceptance cases locally and record evidence in its ticket.
```

When an optional recommendation needs approval, end instead with this prompt,
in place of the next-goal prompt `plan_status.py` suggests:

```text
/adk-system-designer Checkpoint docs/plans/<topic>.md: decide the optional
recommendations in docs/portability/<topic>.md; turn each approved one into a
goal for its named specialist and record the rest as rejected.
```

## Never

- Change the design, another goal's scope, the default framework or code.
- Write application, Terraform, Bicep, IAM, Kubernetes or deployment code.
- Make the application multi-cloud by default.
- Promise full portability while provider-specific dependencies remain.
- Invent hours, prices or dates, or upgrade an `unverified` claim to fact.
- Create tickets or goals; propose them at a designer checkpoint instead.

Independent community project; not affiliated with or endorsed by Google.
