---
name: slc
description: "Scope decisions using Simple, Lovable, Complete. Use when choosing an initial usable release, reducing or renegotiating scope, or judging whether a proposed release delivers its promised outcome. Also use for explicit SLC requests. For fixed-scope implementation, debugging, or experiments concerned only with learning, use the relevant workflow instead."
---

# SLC

Decide what a small release promises and what must work for someone to choose it as it is.

## Entry condition

Locate the unresolved scope decision. An initial release, an addition to an existing product, an internal tool, or a service can all qualify. A mention of "MVP" or "shipping" alone does not.

If the task already has an accepted scope and no new evidence threatens it, return to that task. Reopen only the affected decision when evidence changes feasibility or the promised outcome. An explicit request to explain SLC needs an explanation, not a scoping interview.

## Establish the promise

Use the available brief, current behavior, and user evidence to identify:

- Who will use this, in what situation, and what successful result they need.
- Their current alternative, including a manual process or doing nothing.
- Constraints that change the scope, such as time, budget, supported environments, existing commitments, and consequences of failure.

State the bounded promise in plain language. Separate known constraints from proposed restrictions; apply each constraint only to what it actually governs.

## Choose the next response

Check available context for missing facts whose absence prevents a defensible promise about correctness, safety, or authorization. A governing rule or supported use can be such a fact. An implementation choice within established obligations, such as a library, is not itself a blocker. Ordinary preference uncertainty can remain a labeled hypothesis.

### Clarification needed

When such a fact is unresolved, this turn's deliverable is a clarification, not a release scope. Return:

- The smallest question or set of questions that resolves the blocker, naming the responsible source or owner when relevant.
- Why the answer changes what can be promised.
- A provisional boundary using only established constraints, with the affected decision left pending.

End the response there and wait for the answer. Feature classifications, domain requirements, and acceptance checks belong to the resolved branch. A disclaimer or an assumed governing rule does not resolve the missing fact.

Example: "Scope a payroll tool for our staff: calculations, saved runs, and themes." The jurisdiction and supported employment arrangements are missing. Ask which payroll rules and arrangements the owner needs supported. The provisional boundary is payroll for that agreed group under those confirmed rules; calculation requirements and the feature decisions remain pending. If the brief already supplies those facts, use them instead of asking again.

### Enough context

When the promise has no unresolved correctness, safety, or authorization blocker, read [delivery.md](delivery.md) and continue the scope decision. Label assumptions that do not determine those obligations. Resolve other unknowns with a focused question only when their answers would materially change the recommendation; otherwise give a provisional recommendation.

After a clarification answer, check whether it resolves the blocker. Continue through this branch when it does; ask only about what remains unresolved when it does not.

## Source and adaptation

[Jason Cohen, "Your customers hate MVPs. Make a SLC instead."](https://longform.asmartbear.com/slc/) supplies Simple, Lovable, Complete and the test of a useful release without further feature development. Cohen presents SLC as an alternative to MVP. This skill deliberately pairs SLC's delivery standard with MVP-style learning; the process and examples are an adaptation, not claims from the article.
