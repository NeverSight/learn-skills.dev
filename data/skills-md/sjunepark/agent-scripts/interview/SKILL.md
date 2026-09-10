---
name: interview
description: "Brief consequential open decisions, interview the user where judgment matters, and act on confirmed choices. Explicit request only."
---

# Interview

Treat unresolved findings and questions from the relevant preceding conversation, plus any items named in the same prompt as `$interview`, as a decision agenda. Clear it at reviewer altitude, while leaving implementation details and strongly preferred answers to the implementer.

## Build and Triage the Agenda

1. Gather every item named or scoped by the invoking prompt. From the otherwise relevant preceding conversation, add only unresolved findings or questions that could materially affect direction, scope, user-visible behavior, an external contract, risk, or review policy. Then group tightly related items.
2. Inspect the relevant conversation, workspace, and other available evidence. Finding facts is the agent's job; ask the user only for judgment they need to own.
3. Classify every agenda item:
   - **Implementer-owned:** an implementation detail or an item with a strongly preferred answer. Choose the answer and state the intended handling briefly.
   - **User-owned:** multiple reasonable answers remain and the choice materially affects direction, scope, user-visible behavior, an external contract, risk, or review policy.
   - **Deferred:** the user intentionally leaves the item open. Record what remains unresolved and, when useful, what would unblock it.

Only user-owned items receive decision questions. Every agenda item receives a reviewer brief before its disposition. Classification determines who decides, not whether the user receives context.

## Brief Every Item, Then Ask

Work through a small group of tightly related agenda items at a time:

1. Infer the user's relevant knowledge from the conversation. Default to a reviewer who understands the goal but not the subsystem's mechanics.
2. Re-synthesize a self-contained reviewer brief for every item, including implementer-owned items, even when the evidence appeared earlier. The user should not need to scroll, inspect source files, or understand unexplained jargon.
3. Explain the minimum needed to understand or decide the item in plain language:
   - the decision-relevant concept, with unfamiliar terms defined on first use;
   - what is true now and why the issue exists;
   - why it matters to users, the product, risk, or future maintenance.
   Translate implementation facts into reviewer-level consequences. Include one concrete example when the choice changes an API, workflow, or other user-visible behavior. Use the shortest explanation that establishes the mental model.
4. Present the option set, then resolve according to ownership:
   - **Implementer-owned:** state the chosen answer and why it is strongly preferred. Briefly name the strongest credible alternatives, giving each one concise line for its main consequence and the condition that would make it appropriate. Then state the intended action without asking the user to choose.
   - **User-owned:** explain how the realistic options differ in outcomes and durable obligations, why the recommendation wins, and what condition would favor another option. Then ask a focused question. Use a structured question tool for genuinely enumerable choices when available; otherwise use numbered plain text.
   - **Deferred:** explain what remains unknown, why resolution is premature, and what would unblock it.
   Limit option sets to credible directions with meaningfully different outcomes. When constraints leave one viable direction, state the constraint and move on.
5. Follow an answer only when it conflicts with another decision, remains materially ambiguous, or exposes a consequential prerequisite. Resolve prerequisites before downstream decisions, and stop when the remaining choices belong to the implementer.

Place the brief before the first question or confirmation. Treat classification labels, recommendations, and the decision readback as summaries that follow the brief. Advance only when every resolvable item has enough context for a reviewer to explain the issue, its importance, the recommendation, and the credible outcome-distinct alternatives—or the constraint that leaves one viable direction—without reading the underlying implementation; for user-owned items, the reviewer must also understand the effect of each realistic option well enough to choose.

## Check Consequential Blind Spots

After clearing the agenda, make one bounded pass for consequential issues neither side raised. Admit an issue only if it could materially change direction, scope, user-visible behavior, an external contract, or risk exposure. Leave minor issues and ordinary implementation concerns with the implementer. If no issue meets the bar, move directly to the readback.

## Confirm, Then Act

Give one compact decision readback that accounts for every original item and any admitted blind spot as:

- a confirmed decision,
- an implementer-owned action, or
- an explicit deferral.

Include rationale only where it preserves an important tradeoff, and label
remaining assumptions. Treat unambiguous user answers as confirmation of their
items. Ask only about unresolved consequential assumptions, conflicts, or changes
introduced by the complete readback. A reply approving only some items settles
those items; a question, qualification, or correction leaves only the affected
items unresolved.

Carry settled decisions and implementer-owned actions into the original
authorized task. Hold only work dependent on an unresolved user-owned decision.
When the user requested only an interview, the settled readback is the deliverable.

The interview is complete when every agenda item is accounted for and no consequential user-owned decision remains unresolved; it does not need to visit every possible branch.
