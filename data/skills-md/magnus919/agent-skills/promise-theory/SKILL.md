---
name: promise-theory
description: >-
  Teach promise vocabulary, fundamentals, and coordination diagnosis for promise-based
  systems. Do not use this skill for Semantic Spacetime models or SST CLI tooling; use
  `semantic-spacetime` for those model and tool workflows.
license: MIT
---

# Promise Theory

Promise theory (Mark Burgess; formalized with Jan Bergstra) is a method of
analysis for systems of autonomous agents — humans, LLM agents, APIs, and
deterministic automation. It supplies the vocabulary for designing and
diagnosing delegation: promises, acceptances, assessments, breaches, and
renegotiation. This skill is a thin router; load the dense material only when
a row in [Load By Need](#load-by-need) matches your task.

## Core model
A promise is an autonomous declaration of intended, but as yet unverified,
behaviour from a promiser to a promisee (body: label Λ, type τ, constraint χ).
Agents are autonomous: no agent can promise another's behaviour. Coordination
emerges from voluntary cooperation — an offer plus an acceptance (a
counter-promise) — never from imposed obligation. Obligations are derived,
non-autonomous impositions (imposition + penalty). Agents keep promises via an
evaluation loop: observe → assess → act, converging on the promised state. The
Downstream Principle: the most downstream party in a promise chain carries the greatest causal responsibility for the outcome.

## When to use

Load this skill when any of these triggers matches:

- **Modeling delegation between humans and agents** — decide who may promise what to whom, and who accepts, in a human + AI workforce.
- **Designing capability manifests or agent contracts** — declare capabilities and intent with acceptance criteria, verification, and withdrawal semantics.
- **Diagnosing coordination failures** — explain unkept promises, refused acceptances, or missing assessments in multi-agent work.
- **Calibrating trust and verification** — decide how much to verify an agent, at what rate, and at what cost.
- **Designing self-healing or convergent infrastructure** — evaluation loops that observe, assess, and act toward a desired state.
- **Converting obligation-based designs to promise-based ones** — replace push commands and mandates with voluntary offers and acceptance.

## When not to use

- **When enforceable centralized control is guaranteed** — if you can command and verify compliance directly, promise theory's machinery is overhead, not insight.
- **For simple single-agent prompting** — one model and one prompt, with no delegation graph to model, needs no promise vocabulary.
- **For imperative push-based orchestration scripts that need no consent modeling** — a cron job or CI pipeline that runs without acceptance semantics is not a promise system.
- **For legal contracts** — promise theory is not contract law; it models voluntary intent and assessment, not enforceable legal instruments. Draft real contracts with legal counsel.
- **When the user needs a specific tool manual** — route to the tool's own skill (for example, [cli-builder](../cli-builder/SKILL.md) for CLI conventions) instead of framing the tool with promise theory.

## Load By Need

| Need | Load |
|------|------|
| Re-derive a definition or the formal model (promise, imposition, obligation, bindings, trust, Downstream Principle) | [references/foundations.md](references/foundations.md) |
| Learn from CFEngine, IaC, or distributed-systems practice before designing convergent infrastructure | [references/applications-infrastructure.md](references/applications-infrastructure.md) |
| Design coordination between specific humans and agents (manifests, acceptance handshakes, oversight, authority) | [references/agent-coordination.md](references/agent-coordination.md) |
| Apply a named pattern — promise manifest, acceptance handshake, agent contract, evaluation loop, breach→renegotiation, redundancy, trust calibration | [references/patterns.md](references/patterns.md) |
| Decide how much to verify an agent, set a starting trust level, or wire assessment into evals and observability | [references/trust-and-verification.md](references/trust-and-verification.md) |
| Diagnose a coordination failure, run the breach taxonomy, or check the theory's limitations | [references/diagnosis-and-debugging.md](references/diagnosis-and-debugging.md) |
| Hit an unfamiliar term while applying this skill | [references/glossary.md](references/glossary.md) |

## Quick Start

Run these commands from the skill directory (`promise-theory/`); `python3 scripts/promise-contract.py --help` lists every command and flag.

1. **Draft a promise manifest.** Copy `templates/promise-manifest.yaml.tmpl` to a working file (for example `promise-manifest.yaml`) and fill the placeholders: agent ids and roles, at least one promise per agent (body, type, target), and at least one `expectations` entry whose `about` references a declared promise id.
2. **Lint it.** Run `python3 scripts/promise-contract.py lint promise-manifest.yaml`. Exit 0 with full expectation coverage means the manifest is valid; exit 1 names the violations to fix (coverage gaps, dangling acceptances, invalid enums) or reports a malformed file as a parse error — never a traceback. Re-run after each fix until clean.
3. **Add `--json` for machine-readable output.** Run `python3 scripts/promise-contract.py lint promise-manifest.yaml --json` to get a single JSON object on stdout (`valid`, `errors`, `warnings`, `coverage`, `bindings`) and nothing else.
4. **Add `--dry-run` to confirm no writes.** Run `python3 scripts/promise-contract.py lint promise-manifest.yaml --dry-run` to repeat the same check; lint is read-only, so nothing is written or modified.

## Available Scripts

This skill bundles one script; there are no others to discover. Both commands are read-only (`--dry-run` is accepted everywhere as a no-op guard).

| Script | Purpose | Invocation |
|---|---|---|
| `scripts/promise-contract.py` | Validates and renders promise-theory manifest contracts (restricted-YAML or JSON). `lint` checks a promise manifest against the promise-manifest v1 schema (exit 0 = valid with full expectation coverage; exit 1 = named lint errors or coverage gaps; exit 2 = usage/IO errors) and `render` prints a promise-graph summary of agents, promises, bindings, and uncovered expectations. Run `lint` after drafting or every edit of a manifest until it exits clean, and `render` when you need a human- or machine-readable view of the coordination model you just built. | `python3 scripts/promise-contract.py lint promise-manifest.yaml` |

Append `--json` for machine-readable output (a single JSON object on stdout); `render --json` gives the same treatment to the graph summary.

## Related Skills

| Skill | Route when... |
|-------|---------------|
| [agent-evals-and-observability](../agent-evals-and-observability/SKILL.md) | You need the assessment layer: evals, guardrails, and observability that verify promises are kept (also routed from `references/trust-and-verification.md`) |
| [agent-council](../agent-council/SKILL.md) | You need multi-agent debate as structured promise exchange and convergence (also routed from `references/agent-coordination.md`) |
| [workflow-architect](../workflow-architect/SKILL.md) | You need to design a workflow as a chain of promises (also routed from `references/patterns.md`) |
| [artifact-pyramids](../artifact-pyramids/SKILL.md) | You need to structure promise-keeping evidence as summaries → analysis → evidence dossiers (also routed from `references/trust-and-verification.md`) |
| [agent-skills](../agent-skills/SKILL.md) | You are authoring or editing an Agent Skills-format skill — the format this skill follows |
| [cli-builder](../cli-builder/SKILL.md) | You are building or refactoring the bundled CLI — `scripts/promise-contract.py` follows cli-builder conventions (non-interactive, `--json`, `--dry-run`) |

## Gotchas

1. **Provenance honesty.** The direct "promise theory + AI agents" literature is thin and recent (Burgess, "Cooperation in Human and Machine Agents," arXiv:2604.10505, 2026). In the references, claims not verified against a primary source carry `[UNVERIFIED]`, and the promise-theory → LLM-agent synthesis is labeled `EXTRAPOLATION`. Preserve those markers; they are what keep this skill honest.
2. **The theory is "semi-formal."** The authors themselves use that term: there is a notation, definitions, lemmas, and rules, but no complete axiomatisation or model theory. The famous ≤50% (impositions) vs ≤100% (promises) claim is an informal heuristic, not a derived result. Use the formalism as a reasoning aid, not a proof system.
3. **Autonomy is a modeling postulate, not an ideology.** It does not claim decentralization is morally right or always better; it is chosen because it forces complete documentation of intended behaviour and exposes failure modes.
4. **Promise-keeping must be stored as data.** CFEngine's documented gap: it reported whether a promise was kept right now, but promise-keeping was never stored as data, so the evaluation loop was incomplete. In a hybrid workforce, record assessments as versioned data (a promise ledger) or trust cannot accumulate.
5. **Verification loads are an attention/energy budget.** The rate at which you check (kinetic mistrust) is spent attention; Burgess & Dunbar model it as a bounded budget. Budget verification cost explicitly and start unknown agents at 50-50 rather than assuming trust or distrust.

## Prerequisites

- Python 3 with standard library only; `promise-contract.py` requires no third-party packages.
- A manifest to lint or render: copy `templates/promise-manifest.yaml.tmpl` and fill the placeholders (see Quick Start) before running either command.

## Limitations

- The CLI validates declaration structure, enum values, expectation coverage, and dangling acceptances — it cannot judge whether the promised behaviour is sensible, achievable, or actually kept; assessments live in your promise ledger, not in this tool.
- Promise theory is not contract law: nothing the script validates creates an enforceable legal instrument (see When not to use).
- Lint is a static check at a point in time; it does not observe agents or verify runtime promise-keeping.

## Exit Conditions

Stop when the delegation is modeled as a promise set, acceptances and assessments are recorded (or their absence explicitly deferred), and every breach has a renegotiation or escalation path. When diagnosing, stop after three non-converging passes and report the evidence instead of re-litigating the same promises.
