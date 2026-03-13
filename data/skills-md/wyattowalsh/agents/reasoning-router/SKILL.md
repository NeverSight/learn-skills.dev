---
name: reasoning-router
description: >-
  Classify problems and route to optimal thinking MCP (11 available). Monitor
  confidence, re-route on stall. Use for complex reasoning. NOT for simple
  questions (answer directly) or code review (honest-review).
license: MIT
argument-hint: "[problem or question]"
model: opus
metadata:
  author: wyattowalsh
  version: "0.1.0"
---

# Reasoning Router

Meta-reasoning layer: classify problems, dispatch to the optimal thinking MCP,
monitor progress, re-route on stall. Minimize total tokens to a high-confidence
conclusion.

Always uses the most advanced model (currently Opus 4.6). Meta-reasoning about
*how to think* is the highest-leverage reasoning task.

## Dispatch

| `$ARGUMENTS` | Action |
|---|---|
| Problem or question text | **Route** — classify and dispatch to optimal thinking method |
| `compare <problem>` | **Compare** — run 2-3 strategies on the same problem, pick best |
| `status` | **Status** — show current thinking session state |
| `switch <method>` | **Switch** — re-route to specified method mid-session |
| `recap` | **Recap** — summarize reasoning so far across all methods used |
| `methods` | **Methods** — show available methods with when-to-use cheatsheet |
| Empty | **Guide** — show routing cheatsheet and token tier table |

---

## Classification

Run `!uv run python skills/reasoning-router/scripts/problem-classifier.py "$ARGUMENTS"`
for deterministic pre-scan, then refine with LLM judgment.

### Axis 1 — Structure (what shape is the reasoning?)

| Structure | Signals | Primary Method |
|-----------|---------|----------------|
| **Decomposable** | "break down", multi-hop, sub-questions | `atom-of-thoughts` |
| **Sequential** | "step by step", ordered process, debugging | `sequential-thinking` |
| **Branching** | "explore options", "what if", alternatives | `cascade-thinking` |
| **Constrained** | "given that", requirements, formal specs | `shannon-thinking` |
| **Interconnected** | dependencies, circular, complex system | `atom-of-thoughts` (full) |
| **Creative** | "brainstorm", "novel", "stuck", "reframe" | `creative-thinking` |
| **Contradictory** | paradox, "both true", tension, dilemma | `lotus-wisdom` |
| **Investigative** | "why did", root cause, debug, diagnose | `crash` |

### Axis 2 — Complexity (how deep?)

| Complexity | Signals | Depth Control |
|------------|---------|---------------|
| **Simple** (1-3 steps) | Short input, single concept, "quick" | Tier 1 ONLY: `aot-light` or `sequential` |
| **Moderate** (4-8 steps) | Multiple factors, some uncertainty | Default depth, structure-matched method |
| **Complex** (9+ steps) | Cross-domain, high uncertainty | Full depth, extended steps |
| **Wicked** (open-ended) | No clear solution, values conflict | Composition patterns allowed |

### Axis 3 — Domain (what kind?)

| Domain | Method | Why |
|--------|--------|-----|
| **Engineering/architecture** | `shannon-thinking` | Constraints → model → proof |
| **Debugging** | `crash` | Tool-aware investigation |
| **Research** | `cascade-thinking` | Parallel perspectives |
| **Math/logic** | `atom-of-thoughts` | Dependency DAG |
| **Strategy** | `think-strategies` | Strategy comparison |
| **Creative/design** | `creative-thinking` | Lateral techniques |
| **Philosophy/ethics** | `lotus-wisdom` | Non-dual integration |
| **Planning** | `sequential-thinking` | Linear progression |
| **Pattern tracking** | `structured-thinking` | Persistent memory |

---

## Routing Algorithm

Optimize for **minimum total tokens to reach a high-confidence conclusion**.

```
1. Run problem-classifier.py for deterministic signals
2. Score each axis (structure × complexity × domain)
3. Apply efficiency gate:
   - Simple: ALWAYS Tier 1 (aot-light or sequential-thinking)
   - Moderate: structure-matched method at default depth
   - Complex: full method with extended depth
   - Wicked: composition patterns allowed
4. Resolve conflicts:
   - Structure > domain (HOW > WHAT)
   - Complexity modulates depth AND tier
   - Ties: ALWAYS prefer lower token cost
5. Select primary + fallback
6. Present: "Using [method] — [why]. Fallback: [method]." (1 line)
7. Invoke with minimum viable totalThoughts
8. Monitor for stalls — escalate only on evidence
```

### Token Cost Tiers

```
Tier 1 (lightest): aot-light, sequential-thinking
Tier 2 (moderate): structured-thinking, cascade-thinking, crash
Tier 3 (heavy):    shannon-thinking, atom-of-thoughts (full), think-strategies
Tier 4 (heaviest): creative-thinking, deep-lucid-3d, lotus-wisdom
```

### Efficiency Rules

- Never Tier 3-4 for a problem Tier 1-2 can handle
- Start with lowest viable `totalThoughts`; expand only on `needsMoreThoughts`
- `cascade-thinking`: start 2 branches max; add only if coverage insufficient
- `creative-thinking`: use `timeframe: "quick"` unless wicked
- `think-strategies`: start with `linear` or `chain_of_thought` before heavier strategies

---

## Stall Detection

Read `references/stall-detection.md` when any stall signal fires.

**4 stall signals:**
1. **Confidence plateau** — no increase >0.05 in 3+ steps
2. **Circular reasoning** — same claim restated
3. **Step overrun** — exceeds 2× initial estimate
4. **User signal** — "try something else" or `/think switch`

**Re-routing by block type:**

| Block | New Method | Why |
|-------|-----------|-----|
| Stuck in depth | `cascade-thinking` | Broaden |
| Too broad | `atom-of-thoughts` | Decompose |
| Too formal | `creative-thinking` | Reframe |
| Too abstract | `crash` | Ground in evidence |
| Contradictions | `lotus-wisdom` | Integrate |
| Wrong method | Reclassify | Start routing over |

**Hard limits:** Max 3 re-routes per session. Max 3× step estimate. No ping-pong
(can't return to a method already re-routed from). After 3 re-routes → recovery
protocol: present findings, ask user to guide.

---

## Composition Patterns

Read `references/composition-patterns.md` for full protocols.

| Pattern | Sequence | When |
|---------|----------|------|
| **Sketch→Detail** | `aot-light` → `aot` (full) | Quick outline then deep dive |
| **Diverge→Converge** | `creative-thinking` → `sequential` | Generate options then evaluate |
| **Explore→Formalize** | `cascade-thinking` → `shannon` | Survey landscape then prove |
| **Decompose→Investigate** | `aot` → `crash` (per atom) | Break down then debug each |
| **Analyze→Integrate** | `cascade-thinking` → `lotus-wisdom` | Surface contradictions then synthesize |
| **Strategize→Plan** | `think-strategies` → `sequential` | Step back then plan forward |

**Context transfer:** At every method transition, produce ≤100 word summary of key
findings with confidence scores. Carry claims, drop scaffolding.

**When NOT to compose:** Simple/moderate complexity, first method is converging, time
pressure is high.

---

## Compare Mode

When invoked with `compare <problem>`:

1. Classify the problem normally
2. Select 2-3 candidate methods (primary + 1-2 plausible alternatives)
3. Run each for 3-5 steps on the same problem
4. Compare: which produced higher-confidence findings with fewer tokens?
5. Present comparison table and recommend the winner
6. Continue with the winning method if user agrees

---

## Methods Quick Reference

When invoked with `methods` or for the routing cheatsheet:

| Method | MCP Tool | Tier | Sweet Spot |
|--------|----------|------|-----------|
| sequential-thinking | `sequentialthinking` | 1 | Linear, ordered reasoning |
| aot-light | `aot-light` | 1 | Quick atomic sketches |
| structured-thinking | `capture_thought` | 2 | Cross-session memory |
| cascade-thinking | `cascade_thinking` | 2 | Multi-perspective exploration |
| crash | `crash` | 2 | Debugging with tool integration |
| shannon-thinking | `shannonthinking` | 3 | Formal proof under constraints |
| atom-of-thoughts | `aot` + `atomcommands` | 3 | Deep decomposition with DAG |
| think-strategies | `think-strategies` | 3 | Named strategy frameworks |
| creative-thinking | `discover_techniques` → `plan` → `execute` | 4 | Lateral thinking (3-step required) |
| deep-lucid-3d | `analyze_problem` | 4 | Holistic UCPF analysis |
| lotus-wisdom | `lotuswisdom` (start: `tag: begin`) | 4 | Paradox and contradiction |

Read `references/capability-map.md` for full tool parameters and workflows.

---

## Reference File Index

| File | Read When |
|------|-----------|
| `references/capability-map.md` | First invocation or unfamiliar with a tool's parameters |
| `references/routing-matrix.md` | Resolving routing conflicts, ties, or edge cases |
| `references/composition-patterns.md` | Problem needs a multi-tool sequence |
| `references/stall-detection.md` | Stall signal fires or session exceeds expected steps |

Load ONE reference at a time. Do not preload.

---

## Scope Boundaries

**In scope:** Problem classification, thinking MCP dispatch, stall detection,
re-routing, composition pattern selection, method comparison.

**Out of scope:** Actually performing the reasoning (the thinking MCP does that),
running tools or writing code (use appropriate skills), code review (honest-review),
research (research), debugging implementation (use crash MCP directly).

---

## Canonical Vocabulary

| Term | Meaning |
|------|---------|
| method | A specific thinking MCP tool (e.g., cascade-thinking) |
| tier | Token cost classification (1=lightest, 4=heaviest) |
| structure | The shape of reasoning a problem requires |
| routing | Selecting the best method for a classified problem |
| stall | When a method stops making progress (confidence plateau, circular reasoning) |
| re-route | Switching to a different method mid-session |
| composition | Chaining 2+ methods sequentially for complex problems |
| efficiency gate | Override that forces Tier 1 methods for simple problems |
| context transfer | Summarizing findings when switching between methods |

---

## Critical Rules

1. **Always use the most advanced model** — `model: opus`. Never downgrade.
2. **Minimize total tokens to conclusion** — pick the lightest method that handles
   the problem. Escalate only on evidence of stall.
3. **Present routing decision before invoking** — 1 line: method, why, fallback.
4. **Never invoke without classification** — even if user names a method, validate fit.
5. **Carry forward on re-route** — summarize findings ≤100 words, don't restart.
6. **Simple gets simple** — Tier 1 for simple problems, always. No exceptions.
7. **Token cost breaks ties** — equal fit → lower tier wins.
8. **Start minimal, expand on evidence** — lowest `totalThoughts`, expand only when
   the tool requests more or stall detected.
9. **One method at a time** — no simultaneous thinking MCPs. Composition is sequential.
10. **Router ≠ thinker** — classify, dispatch, monitor. Don't duplicate reasoning.
11. **Respect tool workflows** — creative-thinking: discover→plan→execute.
    lotus-wisdom: start with `tag: begin`. aot: use `atomcommands` for control.
12. **Track token spend** — note approximate tokens per session to refine routing.
