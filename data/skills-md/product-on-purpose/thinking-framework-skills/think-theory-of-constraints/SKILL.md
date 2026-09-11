---
name: think-theory-of-constraints
description: Produces a constraint-intervention plan that names the single binding constraint capping a system's throughput and attaches its exploit, subordinate, and elevate decisions, after testing capacity versus demand at each step to confirm that step is genuinely the rate-limiter rather than the loudest one. Use when a system has a clear flow (a pipeline, a funnel, a queue, an approval chain, a production line) whose output is capped by one step and improvement effort is being spread evenly across all steps instead of aimed at the bottleneck. Not for coverage questions (route to think-issue-tree), recurring deep-cause questions (route to think-iceberg-model), or accumulation-trajectory questions (route to think-stocks-and-flows-reasoning).
license: Apache-2.0
metadata:
  id: thinking-framework-skills.theory-of-constraints
  family: systems-and-consequences
  evidence-tier: "P"
  version: 0.1.0
  standard: "0.8"
---
<!-- thinking-framework-skills | https://github.com/product-on-purpose/thinking-framework-skills | Apache-2.0 -->
# Theory of Constraints

The throughput of a whole system is governed by **one binding constraint** - its rate-limiting step - so improving anything other than that constraint does almost nothing for the system as a whole. The default improvement instinct is the opposite: make every part faster, cheaper, more utilized. This skill refuses that reflex. It treats local efficiency at a non-constraint as waste, because a non-bottleneck working harder just piles inventory in front of the bottleneck, and it concentrates effort on the one step that caps the flow while **subordinating** (not optimizing) everything else. The single question it forces is whether one step limits the throughput of the whole, and whether effort is aimed there or scattered. The output is a **constraint-intervention plan** - the named binding step plus its exploit, subordinate, and elevate decisions - not a discussion. This is the Five Focusing Steps reduced to its working core; it is deliberately scoped to the bare bottleneck move, not the full Goldratt operational systems (Drum-Buffer-Rope, Critical Chain, Throughput Accounting).

## When to Use

- A system has a clear **flow** - a pipeline, a funnel, a queue, an approval chain, a production line - that work items pass through, and its output is capped by one step.
- Improvement effort is being spread evenly across all steps, or aimed at the loudest, most-complained-about step, instead of at the step that actually caps throughput.
- Adding resources is not lifting output ("we keep adding salespeople but revenue is flat"), which suggests the constraint is elsewhere.
- There is appetite to wring more from the limiting step before spending to add capacity.

## When NOT to Use

- **No single binding constraint, or an unstable or non-flow problem.** This method assumes one dominant, reasonably stable bottleneck governs the system. With several co-equal limiters, a constraint that shifts faster than you can act on it, or no flow at all (a one-off decision, a design question, a values trade-off), forcing a single-constraint frame manufactures a rate-limiter that is not really binding and aims effort at the wrong place. Say so and stop.
- **Coverage or "have we considered every part?" questions go to `think-issue-tree`.** Exhaustive decomposition (every category of cause or option, nothing left out) is the inverse move; coverage is this method's failure mode, not its goal.
- **Recurring or deep-structural-cause questions go to `think-iceberg-model`.** "Why does this keep recurring, and where structurally do we intervene?" is leverage by causal depth (event to pattern to structure to mental model), which a bottleneck analysis does not provide.
- **Accumulation-trajectory ("is the stock rising or falling?") questions go to `think-stocks-and-flows-reasoning`.** Whether a quantity is accumulating up or down is a net-flow reading, a different error from locating a rate-limiter.
- **Treat the identified constraint as a hypothesis to test, never as found.** A wrongly named bottleneck - the loudest step rather than the binding one - sends the whole exploit / subordinate / elevate sequence at the wrong target. The method does not itself prove which step is binding; the capacity-versus-demand test does.
- **Do not subordinate healthy parts to a step that was never the true limiter.** "Subordinate everything to the constraint" is correct only when one constraint really governs. Applied where it does not, it starves working parts of the system to feed a step that was never the rate-limiter.

## Instructions

When asked where to unblock throughput in a system with a flow, follow these steps:

1. **Confirm there is a flow with a plausible single rate-limiter.** State the system as a sequence of steps that something passes through (work items, candidates, tickets, units). If there is no flow, or several co-equal limiters, or an unstable, shifting constraint, stop and route out (see "When NOT to Use"); do not manufacture a bottleneck.
2. **Identify the candidate binding constraint as a hypothesis.** Name the one step that appears to cap downstream output. Resist naming the loudest, most-complained-about, or most-visible step by reflex.
3. **Test it with capacity versus demand, per step.** For each step, state its capacity (how much it can process per unit time) against the demand placed on it. The binding constraint is the step where demand meets or exceeds capacity and the steps after it sit starved or idle. If the data does not single out one step, say the constraint is unproven and stop short of the exploit sequence.
4. **Exploit the constraint.** List how to get maximum useful throughput from that step with resources already on hand, before any spend (remove idle time, stop it doing work that is not throughput, feed it only good inputs, offload non-essential tasks).
5. **Subordinate everything else.** State how each non-constraint should run at the pace the constraint can absorb, not at its own local maximum. Name the local-efficiency habits that must be deliberately given up (a non-bottleneck running flat-out just builds queue in front of the constraint).
6. **Elevate the constraint, only if still binding after exploit.** State what added capacity would raise the constraint (hire, buy, parallelize, redesign the step), explicitly gated behind exploitation being exhausted.
7. **Re-check.** Note that elevating or exploiting can move the constraint to a new step; record the trigger to return to step 2, and the warning not to keep optimizing the old bottleneck out of inertia.
8. **Emit the constraint-intervention plan** per `references/TEMPLATE.md`. The deliverable is the plan, not prose.

## Output Format

Use the template in `references/TEMPLATE.md`. The deliverable is the constraint-intervention plan - the named binding constraint, the capacity-versus-demand test, and the exploit / subordinate / elevate decisions with a re-check trigger - not a prose essay.

## Quality Checklist

Before finalizing, verify:

- [ ] The system is stated as a flow (a sequence of steps work passes through), and if there is no flow or no single binding constraint, the skill said so and stopped.
- [ ] The binding constraint is named as a **hypothesis**, not asserted as found, and is not just the loudest or most-visible step.
- [ ] Capacity versus demand was tested **per step**, and the named constraint is the step where demand meets or exceeds capacity while downstream starves.
- [ ] Exploit (wring throughput with current resources) precedes elevate (add capacity); elevate is gated behind exploitation being exhausted.
- [ ] Non-constraints are **subordinated** to the constraint's pace, not optimized to their own local maximum, and the local-efficiency habits to give up are named.
- [ ] The re-check trigger is recorded (what would move the constraint, and the warning not to keep optimizing the old one).
- [ ] No overclaiming: the bottleneck principle is operationally backed but has no controlled trial of this move and is transferred from human practice (see `evidence/dossier.md`).
- [ ] The output is the constraint-intervention plan artifact, not prose.

## Evidence

Tier **P** (governing; honest floor and ceiling). The bottleneck principle is durable, broadly taught, and endorsed even by its critics (Mukherjee and Chatterjee, 2007, separate criticism of Goldratt's rigour from criticism of the bottleneck approach), with a large, consistently positive operational record (Mabin and Balderstone's review of 80-plus reported applications; Bacelar-Silva, Cox and Rodrigues, 2020, a systematic review of 42 healthcare implementations). But none of it is controlled comparative evidence for the cognitive move, and two cautions cap the grade: selection bias (Mabin and Balderstone report finding no documented failures - a literature of self-reported winners), and the move under test is not the move shipped (most evidence measures the full apparatus of Drum-Buffer-Rope, Critical Chain, and Throughput Accounting, not the bare identify-and-exploit step; the part closest to a standalone thinking method, the Thinking Processes, has the weakest evidence). Evidence is transferred from human teams in manufacturing, projects, and healthcare, not AI-validated. The impression that "the method always works" is an artifact of the no-failures-reported literature and is excluded from any claim. Full grading, sources, and caveats: `evidence/dossier.md`.

## Examples

See `references/EXAMPLE.md` for a completed constraint-intervention plan on a real decision.
