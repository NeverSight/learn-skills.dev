---
name: proposal-review
description: Review an agent's proposed approach for clear reasoning, supported assumptions, scope and decision readiness. Use maintainer-review for deep subsystem design and code-review for an existing patch; prose polishing alone is outside scope.
---

# Proposal Review

Review the supplied idea, including informal chat, without implementing or rewriting it.
Identify the intended outcome, constraints, mechanism, and decision to enable. Separate
verified facts, assumptions, and user choices; investigate discoverable factual gaps.

Read later corrections before reusing a prior conclusion.

Check:

- **Alignment:** does the mechanism solve the actual problem within the requested scope?
- **Reasoning:** trace consequential premises to code, contracts, measurements, or supplied
  evidence. Identify contradictions, causal jumps, and assumptions that could change the choice.
- **Necessity and cost:** compare applicable existing facilities or simpler approaches
  under the same requirements. Who owns new state and behavior, and what burden reaches
  callers or operators?
- **Readiness:** are material choices, failure behavior, and observable acceptance clear
  enough for the proposed next step? Distinguish unclear explanation, unsound design,
  and an untested hypothesis; avoid demanding implementation detail prematurely.

## When the route is uncertain

If the next step is an investigation, name the explanations the evidence still allows
and what distinguishes them; do not invent alternatives to a settled conclusion. Recommend
the feasible observation with the best discrimination for its total cost, including setup,
recovery and delay, and say how the relevant outcomes change the next step. Source inspection
may suffice. If all outcomes lead to the same action, the check is not resolving that choice;
judge its other purpose, such as acceptance, safety or establishing a baseline, separately.

Before scaling a test, assess whether it can reach and observe the condition. For rare
conditions, the run may itself be the search: state the detection method, stopping rule
and meaning of a null result. Distinguish a valid negative, an unreached trigger and an
invalid fixture; for a claimed fix, ask whether old behavior would pass the new acceptance.
Use unexpected results or controls to revise the next comparison instead of repeating an
unchanged non-discriminating setup. Repetition that adds useful statistical evidence is
not excluded. Review the test's decision value here; leave execution design to the pilot
or implementation plan.

Deep long-term design review belongs directly to
[maintainer-review](../maintainer-review/SKILL.md). A consequential interface, lifetime,
or migration question can deepen this review using that method within the same verdict.
Ordinary reasoning review needs neither a subsystem sweep nor an exhaustive interview.
For an existing patch, use [code-review](../code-review/SKILL.md).

Lead with ready for the stated next step, needs revision, or lacks decisive evidence.
For each material finding give the passage/location, evidence or unverified premise,
consequence, and smallest correction or resolving question. Separate optional suggestions;
only questions whose answers change the decision are blocking. Stop once these are resolved.

Recommend the next action: a user decision, feasibility experiment,
planning of settled choices, or already-authorized implementation. Keep findings with
the proposal and return in chat unless a durable review is required. Review acceptance
does not authorize execution or turn suggestions into tasks or Wayfinder entries.

## Lessons

- Judge readiness for the requested step: an RFC may expose a bounded support or
  policy question that would block merge. State what must be settled now and what
  the RFC asks maintainers to resolve; do not equate submission with release readiness.
- A successful workaround supports the observed result, not its proposed cause.
  Separate observation, hypothesis, and counterevidence; request a diagnostic experiment
  only when its result changes the next decision, and check available resources first.
