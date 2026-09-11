---
name: think-contradiction-resolution
description: Converts a stuck trade-off into a contradiction to dissolve rather than a compromise to settle for. Names the two conflicting requirements, states an implementation-free Ideal Final Result, and applies the four separation principles (separate the requirements in time, space, scale, or condition) to satisfy both at once, then produces either a concrete resolution or an honest flag that the trade-off is genuine. Use when a decision has hardened into an either/or like speed versus quality, thorough versus fast, or generous versus profitable, when splitting the difference feels wrong and a win-win would be worth far more than the best compromise, or when a recurring design or product trade-off keeps forcing the same painful balance.
license: Apache-2.0
metadata:
  id: thinking-framework-skills.contradiction-resolution
  family: problem-framing
  evidence-tier: "M/P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Contradiction Resolution (Ideal Final Result)

Most problems arrive as a trade-off: to get more of A you must accept less of B (cheaper but flimsier, faster but riskier, generous but unprofitable). The reflex is to optimize - find the least-bad point on the curve. Contradiction resolution refuses that reflex first. It reframes the problem as a **contradiction to be dissolved** - a solution in which you stop trading A against B at all - and only settles for the compromise once a disciplined attempt to dissolve the trade-off has actually failed. The reframe is the durable move; it is the de-branded core of TRIZ (Genrich Altshuller, from 1946). The output is a **contradiction-resolution worksheet**, not a discussion.

## When to Use

- A problem is stated as, or has quietly collapsed into, an "A vs B" trade-off, and nobody has tested whether the trade-off is actually necessary.
- The obvious answer is "pick a point on the curve," and a genuine win-win would be worth far more than the best compromise.
- A design, process, or product tension keeps forcing the same painful balance ("thorough vs fast", "generous vs profitable", "secure vs convenient").
- The opposing requirements look like they might hold at different times, places, scales, or under different conditions.

## When NOT to Use

- **The trade-off is genuinely fundamental.** Some contradictions are imposed by physical law, conservation, regulation, or hard external limits and cannot be engineered away (you cannot separate "spend the money" from "keep the money"). Forcing the move there manufactures clever-sounding non-solutions and delays the real decision. When dissolution fails, the honest output is "this is a real trade-off" - route it to `think-decision-option-review` to choose under it, or treat it as a standing polarity to manage. This is the central wall.
- **You need idea volume, not a frame.** This skill is convergent on one tension and produces fewer ideas than open ideation. For breadth use `think-brainwriting` or `think-far-analogy-ideation`.
- **The tension is one you must manage, not eliminate.** An unresolvable polarity (centralize vs decentralize, structure vs flexibility) is to be navigated over time, not dissolved - that is tension/polarity mapping, not this.
- **No real opposition exists.** If the problem is vague or under-specified rather than genuinely two-sided, this tool will invent a contradiction that is not there. Frame it first with `think-problem-restatement`, then run this once a real trade-off is on the table.

## Instructions

When asked to resolve a trade-off or break a stuck compromise, follow these steps:

1. **Confirm a real trade-off and name the opposing pair.** State the problem as an explicit "to get more of A, we must accept less of B." If there is no genuine two-sided tension, stop and send it to framing (`think-problem-restatement`). Then classify the contradiction: a **technical** contradiction (improving parameter A degrades a *different* parameter B) or a **physical** contradiction (one *single* parameter must hold two opposite values at once). The form selects the resolution menu, so name it explicitly.
2. **State the Ideal Final Result (IFR).** Describe the end-state implementation-free: the required benefit delivered with no new cost, no new harm, and ideally no new mechanism - "the function happens by itself." Strip every "how." The IFR is not a goal restatement; stripping the apparatus exposes how much of it is actually necessary and counters the inertia that makes the trade-off feel inevitable.
3. **Attempt to dissolve the contradiction.** For a **physical** contradiction, run the four **separation principles** in turn and record each attempt: separate the opposing requirements in **time** (each holds at a different moment), in **space** (each holds in a different place or part), by **scale / system level** (move a requirement to a super- or sub-system), or by **condition** (each holds under a different case, segment, or trigger). For a **technical** contradiction, prompt with the **inventive principles** (segmentation, asymmetry, nesting, prior action, "the other way round", and so on). Treat any 39x39 contradiction matrix as a heuristic idea-prompt, never an authoritative lookup.
4. **Resolve or exit honestly.** If a separation or principle dissolves the contradiction, state the resolved solution concretely - what changes so you no longer trade A against B. If nothing dissolves it, declare the trade-off **genuine** and route it onward: to `think-decision-option-review` to choose under it, or to tension/polarity mapping to manage it. Do not manufacture a clever non-solution; the honest exit is part of the method, not a failure of it.
5. **Emit the contradiction-resolution worksheet.** Produce the artifact in `references/TEMPLATE.md`: the opposing pair, the contradiction type, the IFR, each dissolution attempt with the operator it used, and the outcome (a concrete resolution, or an honest "real trade-off, routed to ..."). The template's pre-printed evidence caveat is part of the artifact; carry it through verbatim.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the filled worksheet - opposing pair, IFR, dissolution attempts, and a resolution-or-honest-exit - not a prose essay.

## Quality Checklist

Before finalizing, verify:

- [ ] The trade-off is written as an explicit opposing pair, and classified as technical (two parameters) or physical (one parameter, two opposite values).
- [ ] The IFR is stated implementation-free (no "how"), not a reworded goal.
- [ ] Dissolution was attempted with named operators - the four separation principles for a physical contradiction, inventive-principle prompts for a technical one - and each attempt is recorded, not just the winner.
- [ ] Any contradiction matrix was used as a heuristic prompt, not an authoritative lookup.
- [ ] The outcome is either a concrete resolution OR an honest "this is a real trade-off" with an onward route - never a vague compromise dressed up as a dissolution.
- [ ] The output is the worksheet artifact, not prose.
- [ ] No overclaiming: the evidence is practitioner-grade and transferred, and the matrix is contested; claim "tests whether the trade-off is real and often dissolves it," not a measured gain in outcomes (see `evidence/dossier.md`).

## Evidence

Tier **P** (governing; honest read **M/P**, capped at P). Structured contradiction-based ideation has real controlled comparison behind it - quasi-experimental studies report TRIZ-style methods improve the novelty and variety of ideas while reducing their quantity (the M-leaning half) - but three deductions hold the grade at P: the studies measure the broad method, not this specific dissolve-plus-IFR move; the signature contradiction matrix is empirically contested (Spreafico and Russo, 2018, find it covers only ~10-15% of problems); and the one AI-context study (AI EDAM, n=32) found brainstorming higher on fluency and originality, with TRIZ ahead only on elaboration and flexibility. All of it is transferred from human practice, not validated on agents. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed contradiction-resolution worksheet on a real decision.
