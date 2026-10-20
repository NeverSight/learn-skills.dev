---
name: fable-skill-creator
description: "Author, evaluate, refine, optimize, and package autonomous AI agent skills across multi-agent ecosystems with BinEval scoring and description tuning. Use when creating a new skill from scratch, editing an existing skill that misfires or undertriggers, authoring test suites for skills, optimizing skill descriptions, or packaging skills for distribution — even if the user does not explicitly say \"fable-skill-creator\" (e.g. \"create a skill\", \"build a new skill\", \"optimize skill description\", \"package this skill\", \"teach the agent to do X\"). Do NOT use for general application code changes or non-skill tasks."
version: 1.3.0
pack: creator
inputs:
  - user_intent
  - workflow_trace
  - reference_sources
requires:
  - clear_capability_scope
produces:
  - structured_skill_package
  - eval_benchmark_suite
gates:
  - lack_of_surprise
  - objective_eval_criteria
fallback: fable-plan
mutatesWorkspace: true
parallelSafe: false
neural_links:
  precursors:
    - fable-discover
    - fable-research
  continuations:
    - fable-eval
    - fable-verify
    - fable-review
  lateral_peers:
    - fable-artifact
    - fable-config
  recovery: fable-recover
---

# Skill Creator

Create Skills that change agent behavior under pressure, not Skills that merely describe good practice.

## Mission
A production Skill is a compact operating manual for a recurring class of decisions. It should help an agent recognize the situation, choose among plausible actions, collect the right evidence, reject tempting shortcuts, and hand off cleanly when another specialist is better suited.

A schema-valid `SKILL.md` is not enough. A Skill that only says "inspect, plan, implement, verify" is documentation, not a behavioral capability.

## Activation Contract
Use this Skill when the requested work is to:
- create a new reusable Skill;
- strengthen or refactor an existing Skill;
- improve triggering accuracy or reduce overlap with neighboring Skills;
- add references, examples, templates, agents, or evals;
- convert a repeated workflow into a portable agent capability;
- prove that a Skill behaves correctly across more than a happy-path example.

Do not use it for ordinary application changes, bug fixes, or repository maintenance. Route those to the appropriate lifecycle Skill.

## Inputs
- **`user_intent`**: capability, behavior, or workflow to encode.
- **`workflow_trace`**: observed sequence of decisions/tools/failures, when available.
- **`reference_sources`**: primary docs, schemas, domain rules, or proven internal patterns.

## Skill Depth Classification
Before authoring, classify the capability:

| Class | Typical shape | Required depth |
| --- | --- | --- |
| Rule | One stable decision with few branches | concise Skill, strong boundaries |
| Procedure | Multi-step repeatable operation | staged protocol + evidence |
| Diagnostic | Symptoms map to competing causes | failure taxonomy + falsification |
| Orchestrator | Chooses/delegates among specialists | routing table + handoff contracts |
| Domain expert | Requires substantial specialist knowledge | deep references + examples + eval families |

If the capability is Diagnostic, Orchestrator, or Domain expert, a short checklist is presumptively insufficient.

## Skill Contract V2
Every non-trivial Skill must answer these questions explicitly.

### 1. When does it activate?
Define positive triggers, negative triggers, prerequisites, and escalation conditions. Include near-neighbor tasks that should *not* select this Skill.

### 2. What situation is the agent in?
Provide a small classification that changes behavior. Examples: bounded vs architectural, deterministic vs flaky, local vs external, reversible vs destructive, known vs uncertain.

### 3. What decisions must be made?
Use decision tables or branching rules for ambiguous cases. Do not hide judgment behind vague language such as "when appropriate" without defining the evidence that makes it appropriate.

### 4. What is the execution protocol?
For each stage specify:
- objective;
- allowed actions;
- required evidence;
- exit condition;
- stop/escalation condition.

### 5. How can it fail?
Name domain-specific failure classes and observable signals that distinguish them. Do not collapse every failure into "retry" or "use recover".

### 6. What must never become false?
List invariants that stay true throughout the Skill. Examples: no production mutation before valid RED, no release claim without registry confirmation, no review finding without a concrete failure mode.

### 7. Which shortcuts are tempting but invalid?
Document anti-patterns that capable models commonly choose under time pressure or ambiguous prompts.

### 8. What evidence leaves the Skill?
Define a handoff packet for the next specialist: facts learned, commands run, artifacts changed, residual risk, unresolved questions, and proof freshness where relevant.

### 9. What belongs in progressive resources?
`SKILL.md` should hold decision logic. References should add operational depth, not repeat the same checklist in different words.

Useful resources include:
- decision heuristics;
- failure diagnosis guides;
- legacy/edge-case playbooks;
- worked examples with trade-offs;
- tool-independent verification strategies;
- checklists only where the checklist encodes non-obvious domain knowledge.

### 10. How will we know the Skill actually works?
Create multiple semantically distinct eval families. Surface variations of one scenario do not count as breadth.

## Eval Depth Standard
For a non-trivial Skill, target at least **6 semantic scenario families** across its package before calling evaluation coverage mature. A family is a different decision problem, not the same prompt rewritten five ways.

Include a mix of:
- straightforward activation;
- boundary/non-trigger case;
- ambiguous situation requiring classification;
- adversarial pressure to take a shortcut;
- partial or contradictory evidence;
- failure/recovery handoff;
- legacy or constrained environment where the normal happy path is unavailable.

The enterprise behavior harness may still expand each family into known/negative/ambiguous/adversarial/holdout variants. That expansion does not replace semantic family breadth.

## Authoring Procedure
1. **Observe the real job**: identify decisions, artifacts, failure modes, and handoffs from real workflows or primary sources.
2. **Map neighboring Skills**: define what this Skill owns and what it deliberately refuses.
3. **Write eval scenarios first** for the most important failure-prone decisions. If the expected action cannot be stated clearly, the Skill contract is not ready.
4. **Design the decision model**: classification, branches, invariants, stop conditions.
5. **Write `SKILL.md`** in imperative, tool-independent language.
6. **Add progressive resources** for depth that would otherwise make the main Skill noisy.
7. **Add worked examples** including at least one case where the obvious first move is wrong.
8. **Create/refresh agent profiles** so host-facing prompts point to the full Skill contract rather than replacing it with a one-line summary.
9. **Validate packaging and registry metadata**.
10. **Run deterministic and behavioral evals**. Treat changed Skill/eval corpus hashes as requiring fresh proof.

## Invariants
- Never lower evaluation thresholds to preserve a maturity label after a Skill changes.
- Never copy private expected or forbidden oracle fields into provider-visible prompts.
- Canonical Skills must describe capabilities in provider-neutral language.
- Every non-trivial Skill package must include at least one substantial progressive reference (>=1000 bytes).
- Behavioral maturity claims require fresh verified holdout evaluation across semantic scenario families.

## Decision Rules
- Prefer one strong Skill with a clear domain over several overlapping micro-Skills.
- If two Skills can both reasonably trigger from the same ordinary request, sharpen their boundaries before adding more keywords.
- If the body contains only a linear happy-path procedure, add the branches that real work forces an expert to choose between.
- If a reference merely paraphrases the body, replace it with deeper material.
- If an eval can be passed by parroting the Skill description without understanding the situation, add ambiguity or conflicting evidence.
- Never lower eval thresholds to preserve a maturity label after the Skill changes.
- Never copy private expected/forbidden oracle fields into provider-visible prompts.
- Avoid provider-specific tool names in canonical behavior. Describe capabilities, then let host adapters map them.

## Failure Taxonomy
### Triggering failure
Skill activates too often or misses obvious requests. Fix boundaries and description before adding more procedure text.

### Behavioral shallowness
Skill selects the right broad action but cannot discriminate difficult subcases. Add classification, decision branches, and semantic eval families.

### Resource shallowness
References exist but contain only summaries. Replace with operational guides and worked trade-offs.

### Evaluation illusion
Pass rate is high because scenarios are near-duplicates or leak the answer. Increase semantic breadth and oracle isolation.

### Contract drift
`SKILL.md`, package metadata, agent profiles, registry entries, and evals describe different behavior. Reconcile before release.

## Anti-Patterns
Reject these patterns during Skill review:
- "Use best practices" without naming the decision or evidence.
- one generic procedure reused across unrelated Skills;
- references under ~one screen that only restate the main steps;
- one toy example presented as domain coverage;
- an eval suite made from one scenario plus wording variants;
- arbitrary retry counts with no diagnostic reason;
- completion criteria that can be satisfied without fresh evidence;
- `When NOT to Use` sections that omit the closest competing Skill;
- giant monolithic prompts that duplicate every reference and destroy progressive disclosure.

## Evidence Requirements
A strengthened Skill should provide:
- valid package/frontmatter structure;
- explicit activation and refusal boundaries;
- situation classification and decision rules;
- domain-specific failure taxonomy;
- at least one substantial progressive reference;
- worked example(s) covering a non-happy path;
- multiple semantic eval families;
- behavioral evidence re-run when the evaluated corpus changes.

## Handoff Contract
When finishing Skill authoring, report:
- Skill ID and owned capability;
- neighboring Skills and trigger boundaries;
- semantic eval families added;
- progressive resources added;
- known unsupported cases;
- deterministic validation status;
- whether behavioral evidence is fresh, stale, or not yet executed.

## Completion Criteria
Do not call the Skill mature merely because all expected folders exist.

Completion requires:
- package validation passes;
- contract sections above are materially present where relevant;
- resources add depth rather than duplication;
- eval breadth tests the major decisions and shortcuts;
- registry/host metadata remains consistent;
- any prior behavioral proof invalidated by corpus changes is explicitly marked stale until rerun.

## Progressive Resources
- Depth standard: `references/depth-standard-v2.md`
- Existing authoring references and templates remain useful for package mechanics.
