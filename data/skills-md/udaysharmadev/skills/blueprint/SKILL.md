---
name: blueprint
description: Documents observed or proposed software architecture with evidence-backed context, container, component, dynamic, data-flow, and deployment views. Use when the user needs architecture diagrams, onboarding material, trust boundaries, or a design view before a major change.
---

# blueprint: architecture you can actually read

Diagrams exist to answer questions. You pick the few diagrams this system
actually needs, ground every node in real code, and ship them as an
artifacts set a team can navigate: markdown for the repo, HTML for humans.

## When to use

- "document the architecture of this system"
- "draw the request flow for checkout"
- "diagram how the system should look after the refactor, marked as proposed"

## When NOT to use

- "Where does X live?" → `spelunk` quick mode.
- "Will this scale? What should the architecture become?" → `headroom`
  decides; you can document the outcome.
- A single small diagram inside a README → just write inline Mermaid,
  skip the full deliverable.

## Prerequisites

Repository access. Analysis reuses `spelunk` deep mode when a fresh
`docs/repo-map.md` exists (verify it's recent); otherwise run a deep pass
first: you cannot diagram what you haven't mapped.

Identify the reader, decision, scope, and time boundary before drawing. A
runtime map, a future proposal, a deployment view, and an incident timeline
answer different questions and must not be blended. Capture the current commit,
environment, and source of any infrastructure information.

## Authority, provenance, and change boundaries

- Architecture documentation may inspect code, configuration, manifests, and
  supplied infrastructure records. It must not query production, change cloud
  state, or reveal secrets without explicit authority.
- Mark each element **observed**, **inferred**, **proposed**, or **unknown**.
  A diagram's visual confidence must not make an inference look deployed.
- Do not expose internal addresses, credentials, customer identifiers, private
  topology, or sensitive trust-boundary detail in a public artifact. Produce a
  redacted view when audience requires it.
- Preserve useful existing diagrams, ADRs, terminology, and links. Reconcile or
  date them; do not erase a historical view to make a proposed design look
  current.
- A diagram does not approve an architecture change. Hand a proposed decision
  to the appropriate owner with alternatives and consequences.

## Operating modes

| Mode | Question | Minimum output |
| --- | --- | --- |
| Current-state map | What is deployed or implemented now? | evidence map, context/container view, provenance |
| Change design | What could change and why? | current/proposed separation, sequence, ADRs, acceptance evidence |
| Onboarding | Where do I begin and how does work flow? | reader-focused context, containers, one dynamic path |
| Security boundary | Where does identity/data cross trust zones? | redacted boundary/data-flow view and open assumptions |
| Reliability review | How does failure propagate and recover? | dependency/failure/deployment view and operational gaps |
| Documentation recovery | Which existing diagrams are stale? | freshness audit, retained/updated/retired decision list |

Use the smallest mode that answers the request. A small repository may deserve
one source-backed diagram rather than a ceremonial C4 set.

## Evidence inventory and abstraction rules

Build an evidence table before creating nodes:

| Item | Evidence source | State | Confidence | Reader-safe label |
| --- | --- | --- | --- | --- |
| Component/store/dependency | file, manifest, trace, or supplied record | observed/inferred/proposed/unknown | high/medium/low | diagram label |
| Relationship | call site, config, network rule, or contract | same | same | edge label |
| Ownership/decision | ADR, code owner, user statement | same | same | prose/ADR |

Use C4 terminology precisely: a container is an application or data store, not
a Docker container by default; a component is a major internal responsibility,
not every class or folder. Keep code-level detail in links or a targeted
component diagram only when it answers the reader's question. Label data,
protocol, direction, and synchronous/asynchronous semantics where ambiguity
would affect a decision.

## Diagram and ADR decision framework

Choose every artifact by reader question, not coverage. A context view explains
people and external systems; a container view explains runtime applications and
stores; a component view explains a bounded internal area; a sequence explains
one temporal path; a data-flow explains ownership/lifecycle; a deployment view
explains runtime placement; a failure view explains propagation and recovery.
Read the conditional menu in `references/diagram-guide.md`. For HTML or
untrusted diagram input, read [renderer boundaries](references/rendering.md).

Create an ADR only for a load-bearing decision with alternatives and meaningful
consequences. One ADR addresses one decision: status, context, decision,
alternatives, consequences, evidence, owner, and supersession link. Do not
write an ADR to describe a diagram or manufacture consensus. If decision
authority is unknown, record an open decision rather than choosing.

## Workflow

### 1. Analyze

From the repo map and targeted reads, identify components, data stores,
external dependencies, and request paths. Every observed node must trace to
code, configuration, deployment manifests, infrastructure state, or explicit
evidence supplied by the user. Proposed nodes belong in a clearly marked
proposed view; unsupported boxes do not belong in either.

### 2. Choose the diagrams that help (C4 Abstraction)

Avoid monolithic documentation. Pick only diagrams that answer named questions
for their audiences. Context and container views are the default; component,
dynamic, data-flow, and deployment views are conditional.
The menu in `references/diagram-guide.md` maps the question to the diagram type.
For each major component on a diagram, the README notes its reasoning in
one line: responsibility, boundary, dependency direction, data it owns,
failure mode, and **explicit trust boundaries** (where security contexts change).
A box without a reason is decoration. Common picks:

- new team onboarding → system context + container view + one request
  sequence;
- before refactor → component view + the two flows being touched;
- design doc for a feature → proposed sequence + data model delta;
- reliability review → failure path + deployment.

### 3. Write the Mermaid sources

Use one `.mmd` file per diagram in `docs/architecture/`. Split a diagram
when labels or relationships stop being legible. Labels name real things (`api/index.ts`,
`Postgres`, `Stripe webhook`): no "Service Layer Abstraction". Validate
each with the bundled checker: `scripts/validate-mermaid docs/architecture/*.mmd`
(a limited heuristic for diagram types, delimiters, and labels; it is not
a Mermaid parser and may reject valid syntax). Static checks don't prove
rendering: render once via mermaid-cli when available and say whether
you did.

### 4. Assemble the deliverable

- `docs/architecture/README.md`: index: one paragraph per diagram (what
  question it answers, when to read it), mermaid blocks inline (GitHub
  renders them natively), plus **Assumptions** and **Risk callouts**
  sections, plus a **Decisions** section that links the plan's AgDRs when
  they exist (or states the 2–3 load-bearing decisions inline for small
  docs: a diagram without its decisions is a picture, not architecture).
  Opens with a provenance header (`<!-- generated by blueprint on
  YYYY-MM-DD @ <short-sha>, map <fresh|re-run-date> -->`) so readers can
  tell whether the diagrams describe current code.
- `docs/architecture/architecture.html`: from `assets/template.html`:
  same content, navigable sidebar, zoomable diagrams, print-friendly.
  Fill every template placeholder; delete unused sections rather than
  shipping empty ones.

### 5. Verify and report

Spot-check rule: pick the two most load-bearing nodes across your
diagrams and re-verify them in code (the module exists, the connection is
real). Report what was verified vs. inferred.

### 6. Review for reader and change safety

Render every changed diagram in the same environment that readers use when
possible. Check legibility at normal reading size, node/edge label clarity,
diagram source validity, and links to evidence. Confirm a reader can tell:
what is current, what is proposed, what crosses a trust boundary, what data is
owned where, what fails first, and which claims remain uncertain.

For a changed architecture, review both directions: what new behavior enters
the system and what existing contract, data, deployment, observability, or
rollback path changes. Add an ADR or an explicit open decision when a diagram
reveals a choice that future maintainers would otherwise rediscover.

## Tool selection and fallbacks

- Use repository search, manifests, deployment files, tests, traces, and user
  supplied infrastructure evidence before a generic diagram template.
- Use Mermaid source as the portable default and the bundled validator for
  static checks. A static pass detects only limited syntax problems.
- Render through a project-approved renderer when available. Without it, check
  syntax, inspect source carefully, and mark visual rendering unverified.
- Use a diagram editor only when it can export a source-controlled artifact or
  the user explicitly wants an image deliverable. Do not leave the only source
  of truth in an opaque tool.
- For large systems, start with a context/container map and select one
  high-value flow. Split diagrams rather than shrinking type until unreadable.
- For uncertainty, use a labeled inferred edge, source link, or open question.
  Do not add a speculative service as a neutral placeholder.

## Failure handling and edge cases

- **Stale docs versus code:** preserve the old view with provenance, create the
  corrected current view, and list the discrepancy. Do not silently overwrite
  history.
- **Conflicting evidence:** record sources and scope, then ask the owner or run
  the narrowest safe observation. Config and code can legitimately describe
  different environments.
- **Missing infrastructure access:** map the repository-observed boundary and
  name the unknown external pieces. Do not infer cloud resources from a library.
- **Sensitive topology:** publish a redacted audience-safe view plus a private
  evidence list only when the user authorizes both audiences.
- **Diagram too dense:** split by question, not by visual region; add a linking
  sentence and avoid duplicate ambiguous nodes.
- **Proposed change without authority:** document alternatives and consequences,
  then stop at a decision request. Do not turn a diagram into implementation.

## Quality gates

In addition to the diagram-specific gates below, verify:

- Every node and non-obvious edge has evidence or a visible state label.
- Current, inferred, proposed, and unknown are visually/textually distinct.
- Diagram type, abstraction level, and scope match a named reader question.
- Trust, data ownership, failure semantics, and deployment claims appear only
  where evidence supports them or are called out as assumptions.
- Mermaid source validates; visual render status, source commit, and spot-check
  results are reported.
- ADRs contain a decision, alternatives, consequences, authority/status, and
  link to their relevant diagram rather than duplicating it.

## Honesty rules

- **Never fabricate infrastructure**: no invented queues, replicas,
  CDNs, or "future" components drawn as if they exist. Proposed things go
  in a clearly-marked *Proposed* diagram or dashed nodes.
- Uncertain edges get labeled `(inferred)` in the README, not silently
  drawn.
- If the architecture is genuinely one app + one database, say that in
  one honest diagram instead of decorating it into a microservices saga.

## Stop conditions

- Deliverable written + spot-checks reported → done.
- Repo too small to warrant the full set (single-file scripts) → say so,
  produce the one honest diagram, stop.
- Repo map conflicts with current evidence or is too old for the task's risk:
  refresh the relevant evidence before drawing.

## Output contract

```text
docs/architecture/
  README.md             ← provenance header + index + inline diagrams + decisions + assumptions + risks
  architecture.html     ← navigable, print-friendly deliverable
  context.mmd           ← one file per diagram (kebab-case names)
  containers.mmd
  request-flow.mmd
```

Chat summary: the diagram list with each one's question, the 1–2 risk
callouts that matter most, and the spot-check results.

## Research basis

Read [references/research.md](references/research.md) when a decision depends on
an external standard, a numerical claim, or a fast-moving practice. The ledger
records what the source supports, what it does not support, and when to reverify.
