---
name: semantic-spacetime
description: >-
  Model and analyze Semantic Spacetime (SST) graphs, distances, trajectories, drift, and
  model files. Do not use this skill for promise-theory vocabulary and fundamentals
  without SST modeling; use `promise-theory` for the substrate concepts.
license: MIT
---

# Semantic Spacetime

Semantic Spacetime (SST) is Mark Burgess's discrete, graph-theoretic model of
meaning over time. A *semantic element* is one autonomous agent plus its scalar
promises; a *semantic spacetime* is a collection of such elements in which a
local change in state, promises, or configuration is a local unit of time. Time
is proper time — there is no global clock (the precedence view Burgess credits
to Lamport). Causality is cooperative: every adjacency requires an offer (+) and
an acceptance (−) promise on both ends, so space is made of cooperating nodes
and edges. The 2025 γ(3,4) formalism types the graph: three node meta-types
(events, things, concepts) connected by four link types (0 = NEAR, ±1 = LEADS
TO, ±2 = CONTAINS, ±3 = EXPRESSES). Absorbing states in partial graphs leak
information, and intentionality enters at the boundary. SST is built on Promise
Theory — for the promise vocabulary, load [promise-theory](../promise-theory/SKILL.md)
instead of re-deriving it here. This skill is a thin router: load the dense
material only when a row in [Load By Need](#load-by-need) matches your task.

## When to use

- **When you need to design or analyze shared semantic ground between agents**
  — model what "meaning" means in this system (what does a concept, term, or
  promise mean to whom), producing a γ(3,4) map of the shared semantic ground
  as the artifact.
- **When you need to model intent or meaning over time** — trajectories,
  drift, and convergence of understanding between agents, agents and humans,
  or agents and their instructions; the artifact is a semantic trajectory with
  recorded observations.
- **When you need to design convergent, self-healing coordination** — a loop
  in which state is continuously measured against a desired meaning and
  repaired toward it; model the loop as semantic elements whose local change
  is time.
- **When you need to diagnose semantic drift, divergence, or dead-ends** —
  absorbing states, meaning gaps, and non-converging agents; the artifact is a
  drift finding with the leaking boundary identified.
- **When you need to map promises onto spacetime** — trajectories, promise
  propagation, and causality between agents; model each promise as an edge and
  trace how intent propagates through the graph.
- **When you need to analyze temporal blindness in agents** — state tracking,
  event ordering, and causality failures where an agent cannot tell what
  happened before what; model event order via proper time instead of a shared
  clock.

## When not to use

- **Physics or relativity** — SST is not a theory of quantum gravity or
  spacetime physics; it assumes no manifold structure and no momentum. Do not
  use it for physics problems; those belong to a physics domain.
- **Pure vector embeddings, RAG, or semantic search without temporal-causal
  structure** — a static embedding index has no proper time, no causality, and
  no trajectories to model; route to the embedding or semantic-search tool's
  own skill instead.
- **Enforceable centralized control** — if you can command and verify
  compliance directly, SST's cooperative-promise machinery is overhead, not
  insight (the same boundary promise-theory draws); route to
  [promise-theory](../promise-theory/SKILL.md) when you need the control-vs-
  cooperation discussion.
- **Simple single-agent prompting** — one model and one prompt with no
  delegation or meaning space to model needs no spacetime vocabulary.
- **Tool manuals or framework documentation** — routing to the tool's own
  skill is always better than framing the tool with SST.

## Load By Need

| Need | Load |
|------|------|
| Re-derive the formal model: semantic element, semantic spacetime, proper time, γ(3,4) typing rules, learning/knowledge formalism, promise substrate | [references/foundations.md](references/foundations.md) |
| Learn from the CFEngine and infrastructure lineage before designing convergent systems (convergence semantics, IaC/Kubernetes/GitOps/IBN lessons, promise-keeping-as-data, SLOs, the record axis) | [references/applications-infrastructure.md](references/applications-infrastructure.md) |
| Model an agent team in SST terms or design agent coordination (Burgess's agent papers, drift/temporal-blindness literature, MCP/A2A substrate, synthesis patterns) | [references/agent-coordination.md](references/agent-coordination.md) |
| Apply a named pattern — semantic anchor, trajectory, convergence loop, promise propagation, drift detection, absorbing-state detection, shared semantic manifold, γ(3,4) modeling, distance metrics, reconciliation | [references/patterns.md](references/patterns.md) |
| Diagnose semantic drift, divergence, dead-ends (absorbing states), or meaning gaps with a bounded procedure | [references/diagnosis-and-debugging.md](references/diagnosis-and-debugging.md) |
| Hit an unfamiliar term while modeling or diagnosing | [references/glossary.md](references/glossary.md) |
| Find or verify a primary source — the papers, project pages, and adjacent work behind a claim | [references/bibliography.md](references/bibliography.md) |

## Quick Start

The bundled CLI (`scripts/semantic-spacetime.py`) is stdlib-only — any
`python3` runs it, nothing to install — and every command is read-only. Run
the commands below from the repository root; the CLI resolves no files
relative to its own location, so the same commands work from any directory
with absolute paths.

1. **Draft an SST model.** Copy `templates/sst-model.yaml.tmpl` to a working
   file (for example `sst-model.yaml`) and replace the example values: declare
   agents (id, role, promises), semantic nodes (id, type in
   {event, thing, concept}), edges (from, to, link in -3..3), acceptances,
   trajectories, and observations. The machine-delimited block between
   `# --- example ---` and `# --- end example ---` shows a complete, valid
   model to imitate; the same model is committed, fully filled, at
   `tests/fixtures/sample-model.yaml`.
2. **Lint it** against the sst-model-v1 format — exit 0 prints a coverage
   summary, exit 1 prints named violations:
   `python3 semantic-spacetime/scripts/semantic-spacetime.py model lint semantic-spacetime/tests/fixtures/sample-model.yaml`
3. **Map the γ(3,4) graph** (`--format` is one of text | mermaid | json):
   `python3 semantic-spacetime/scripts/semantic-spacetime.py model map semantic-spacetime/tests/fixtures/sample-model.yaml --format mermaid`
4. **Measure semantic distance** — weighted hop count (each hop weighs
   |link| + 1):
   `python3 semantic-spacetime/scripts/semantic-spacetime.py model distance semantic-spacetime/tests/fixtures/sample-model.yaml --from report-event --to drift-concept`
5. **Trace trajectories** — every simple path with link types annotated;
   cycles are noted and the enumeration terminates on any finite model:
   `python3 semantic-spacetime/scripts/semantic-spacetime.py model trajectory semantic-spacetime/tests/fixtures/sample-model.yaml --from report-event --to drift-concept`
6. **Diff two snapshots** — added/removed/changed semantic regions; identical
   snapshots report `no drift`. Point the command at your two snapshot files
   (running it on the same file twice demonstrates the no-drift case):
   `python3 semantic-spacetime/scripts/semantic-spacetime.py model drift semantic-spacetime/tests/fixtures/sample-model.yaml semantic-spacetime/tests/fixtures/sample-model.yaml`
7. **Machine-readable output.** Append `--json` to any command for a single
   JSON object on stdout. `--dry-run` is accepted everywhere as a no-op guard.
8. **Draft the analysis report.** Copy `templates/sst-analysis.md.tmpl` to a
   working file (for example `sst-analysis.md`) and fill the skeleton: system
   description → semantic spacetime map → drift/divergence/absorbing-state
   findings → interventions → verification/measurement plan.
9. **Diagnose drift when agents disagree.** If agents diverge, treat the
   disagreement as an observation, measure the semantic distance between their
   interpretations, and locate the absorbing state or leaking boundary where
   information stops flowing.

## Available Scripts

This skill bundles one script; there are no others to discover. Every command
is read-only (`--dry-run` is accepted everywhere as a no-op guard), and
`--json` on any command produces a single JSON object on stdout.

| Script | Purpose | Invocation |
|---|---|---|
| `scripts/semantic-spacetime.py` | Lints, maps, and analyzes SST models in the sst-model-v1 format. Subcommands: `model lint` (validate against the schema), `model map --format text\|mermaid\|json` (render the γ(3,4) graph), `model distance --from X --to Y` (weighted hop count, each hop weighs \|link\| + 1), `model trajectory --from X --to Y` (enumerate simple paths with link types), and `model drift file-a file-b` (diff two snapshots into added/removed/changed regions). Run `lint` after drafting or every edit of a model until it exits clean, then use the analysis subcommands when mapping shared semantic ground, measuring distance between interpretations, tracing intent propagation, or diagnosing drift between snapshots. | `python3 semantic-spacetime/scripts/semantic-spacetime.py model lint <model.yaml>` |

Exit codes: 0 = valid/covered, 1 = named violations or missing/unreachable ids, 2 = usage or IO errors.

## Related Skills

| Skill | Route when... |
|-------|---------------|
| [promise-theory](../promise-theory/SKILL.md) | You need the substrate vocabulary SST builds on: promises, offers and acceptances, convergence, the Downstream Principle, and coordination diagnosis (also routed from `references/foundations.md`) |
| [agent-evals-and-observability](../agent-evals-and-observability/SKILL.md) | You need to turn measurement and verification of semantic claims into evals, traces, and release gates (also routed from `references/foundations.md`) |
| [agent-council](../agent-council/SKILL.md) | You want structured multi-agent debate as a mechanism for negotiating shared meaning between agents |
| [workflow-architect](../workflow-architect/SKILL.md) | You want to encode a semantic-spacetime-informed workflow as a reusable skill bundle |
| [artifact-pyramids](../artifact-pyramids/SKILL.md) | You need to structure SST evidence — models, maps, observations — as summaries → analysis → evidence dossiers |
| [agent-skills](../agent-skills/SKILL.md) | You are authoring or editing an Agent Skills-format skill — the format this skill follows |
| [cli-builder](../cli-builder/SKILL.md) | You are building or refactoring the bundled CLI for SST models (it will follow cli-builder conventions: non-interactive, `--json`, `--dry-run`) |

## Gotchas

1. **Provenance honesty.** The theory files tag every factual claim
   `[VERIFIED]` (confirmed in a primary source fetched during research) or
   `[UNVERIFIED]` (secondary or inferred), and label original synthesis
   `EXTRAPOLATION`. Preserve those markers when you reuse the material;
   dropping a marker silently upgrades a claim. See the provenance block in
   [references/foundations.md](references/foundations.md).
2. **The theory is semi-formal and unrefereed.** Burgess published the series
   as self-published notes with no intention of seeking refereed publication,
   and "some proofs [are] left to the reader." Use SST as a reasoning aid, not
   a proof system. See the status section in
   [references/foundations.md](references/foundations.md).
3. **Local time ≠ global clock.** Proper time is per semantic element: a local
   change is that element's unit of time. There is no shared clock ordering all
   events; global order is an observer-relative artifact. See the proper-time
   section in [references/foundations.md](references/foundations.md).
4. **Semantics requires measurement.** Meaning cannot be asserted before it is
   measured at the right scale — "dynamics always trumps semantics" (the
   CFEngine-lineage lesson in
   [references/applications-infrastructure.md](references/applications-infrastructure.md)).
   SST's spacelike (repeated trials, constant state) and timelike (continuously
   adapting) measurements are the two ways to stabilize observation; see the
   measurement-duality section of [references/foundations.md](references/foundations.md).
5. **Promise-keeping must be stored as data.** The gap documented in the
   CFEngine lineage — reporting whether a promise is kept right now without
   ever storing promise-keeping as queryable data — is exactly the gap SST's
   semantic-time record axis addresses (see the promise-keeping-as-data gap in
   [references/applications-infrastructure.md](references/applications-infrastructure.md)).
   Record observations as versioned data or trust cannot accumulate.

## Prerequisites

- Python 3 with standard library only; the CLI has nothing to install.
- A model file to analyze: copy `templates/sst-model.yaml.tmpl` and replace the example values (a complete, valid example lives at `tests/fixtures/sample-model.yaml`).
- The CLI resolves no files relative to its own location, so commands work from any directory — use paths relative to where you run them.

## Limitations

- The theory is semi-formal and unrefereed; the CLI is a reasoning aid for models you author, not a proof system (see Gotchas).
- `distance` and `trajectory` exit 1 when an id is missing or no path connects two nodes; trajectory enumeration covers simple paths only (no repeated nodes) and terminates on any finite model.
- The CLI reads and analyzes model files only: it does not observe running agents, measure live systems, or store observations — recording measurements as versioned data stays your responsibility.

## Exit Conditions

Stop when the system is modeled as a semantic spacetime — semantic elements,
γ(3,4) edges, trajectories, and acceptances recorded — drift/divergence/
absorbing-state findings are written down, and a verification/measurement plan
is stated. When diagnosing drift, stop after three non-converging passes and
report the evidence instead of re-litigating the same model.
