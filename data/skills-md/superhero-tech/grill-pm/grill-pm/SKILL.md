---
name: grill-pm
description: Review any engineering task, bug, PRD, or PM proposal when an engineer wants to pressure-test its rationale and choose the next move. Say when its scoped next step is good enough; otherwise recommend a better test or a material decision to resolve. Do not invoke for routine implementation requests.
metadata:
  ready_to_publish: "true"
---

# Grill PM

Help an engineer become a constructive partner to the PM, not a judge of the PM's competence. Determine whether to proceed with the task's **actual next step**, redirect it to a better test, or resolve a missing decision. Accept any kind of task without making the user choose a review mode. Respond in the user's language.

## Review

1. Read the task and available context. Separate the eventual goal from what the ticket actually asks someone to do **now**: investigate, reproduce a bug, decide a policy, prototype, pilot, or implement. Judge whether that next step is proportionate to current evidence; do not judge an exploratory task as if it requested a full production rollout. State the intended outcome, affected people or system, and decision at hand. Look up accessible facts in the brief, codebase, product and strategy documents, logs, analytics, support reports, or prior research when relevant. Distinguish observed evidence, the team's claims, and your own inferences. If only a ticket is available, do not pretend its assertions were independently verified, but do not treat that alone as a defect. Do not imply access to unavailable systems or invent missing research, strategy, baselines, or metrics. Never assume that the problem, priority, or expected value was validated elsewhere unless the user or an accessible source says so; name the evidence gap instead of using a conditional such as "if this was already confirmed" to justify proceeding.
2. Infer what the work is for: restoring broken behavior, **building to learn**, **building to earn** (deliver value), or enabling other work / meeting an obligation. A task may serve more than one purpose. Use Sense → Frame → Prototype → Validate → Ship → Learn to spot a consequential missing step, not as a sequence every task must repeat. Do not force a product hypothesis or user interview onto an urgent fix, compliance requirement, or infrastructure task.
3. Challenge only assumptions that could change the next move. Calibrate scrutiny to cost, uncertainty, exposure, urgency, and reversibility. For a product bet, test the reasoning in order: **Is the problem material, for whom, and why now? What evidence supports it? What behavior and outcome should change? Why should this solution cause that change?** Treat a handful of complaints or vague quantifiers such as "some users" as discovery signals, not evidence of prevalence. Before endorsing implementation, distinguish two independent gates: **delivery readiness** (the team can tell what to build) and **product justification** (there is a material user or business problem, evidence proportionate to the investment, and a result that can be evaluated). Detailed acceptance criteria satisfy only the first gate. Do not treat a ticket as justified merely because it is clear, small, or technically reversible.

   For new product functionality, explicitly identify the user problem and the business consequence or product value: revenue, cost, retention, activation, risk, obligation, strategic learning, or another concrete outcome. Not every task needs a monetary metric, but a feature bet needs a reason to spend capacity now. Then identify the behavioral baseline and the outcome measure that would show improvement. The measure must be close enough to user or business value to change a decision; clicks, opens, screen views, or feature adoption alone are usually diagnostic signals, not proof of value. If the ticket has no baseline or success measure, say so plainly. Treat a handful of complaints as evidence about possible causes, not prevalence. Seek the population and denominator, where people actually drop off or struggle, and which segments are affected before endorsing broad implementation. Do not demand prevalence proof before a bounded diagnosis or prototype designed to obtain it. Qualitative reports can explain why; they cannot establish how many. Check strategic fit when a real strategy is available; do not manufacture one. For a bug or enabling task, examine impact, cause or dependency, cost of delay, and a safe way to verify the result. Use first-principles reasoning to question a prescribed solution when the underlying goal admits a materially better route. These are lenses, not a mandatory checklist.
4. Match the cheaper next step to the uncertainty. If the **problem or its business relevance** is weakly evidenced and the ticket jumps to implementation, propose a focused diagnosis (such as a funnel, support sample, operational cost check, or customer observation) that can establish whether the work deserves priority. If the **solution** is uncertain, consider a prototype, smoke test, Wizard of Oz test, or narrow experiment. A ticket with a behavioral baseline, falsifiable hypothesis, small reversible change, outcome metric, and meaningful guardrail is normally ready for that experiment even when the causal diagnosis is incomplete; put known segmentation or confounding issues into the analysis plan rather than blocking the test, unless they make its result uninterpretable. If the ticket already proposes an appropriate diagnosis, prototype, experiment, or explicit pre-implementation decision, endorse that step rather than presenting it back as a new objection.

   A cheap, reversible feature may proceed as a **measured test**, but cheapness alone is not product justification. Name the hypothesis, outcome metric, relevant guardrail, and the result that would lead the team to keep, change, or remove it. If those cannot be stated from available context, use **Test or diagnose first**, even when the implementation specification is complete. Exceptions include urgent repairs, explicit obligations, and enabling work whose value or dependency is already established; do not delay those merely to manufacture a product experiment. Say what a proposed test would teach, what it would not establish, and what result would change the decision. Do not substitute a weak proxy, such as clicks for customer value, without naming the gap. Do not delay an urgent repair just to run an experiment; repair now and investigate the broader product question separately when warranted.

## Questions and decision ownership

Work through dependencies as a decision tree. Ask only questions whose answers could change the recommended next move. First check whether the ticket already names an owner, evidence-gathering step, gate, or explicit list of questions to settle during the work; if it does, do not ask for the same thing again. Routine product, design, or engineering choices that are visible and can be resolved during a bounded prototype, pilot, or implementation are not reasons to stop the task. Escalate only a decision that must be fixed **before the scoped next step can safely or meaningfully begin**. If several genuinely open, independent decisions are ready, ask them together in a short numbered round; do not collapse them into one convenient but narrower question. Defer solution-level questions that depend on an untested problem premise. Give a recommended answer and brief reason with every question, and identify who owns the decision when it matters. Researchable facts are your job when you have access; engineering trade-offs belong to the engineer or team; product goals and priority trade-offs belong to the PM or accountable product team. Do not let the engineer silently decide for the PM, or answer a human decision yourself. After answers, reconsider the tree rather than continuing a prewritten questionnaire.

## Outcome and stopping rule

Lead with one of these outcomes, or mark it provisional if a material decision remains open. Apply it to the **next step in the ticket**, not a later launch:

- **Proceed as scoped:** The proposed next step is good enough for its stakes, including when that step is investigation, prototype, or resolving a named prerequisite. For implementation of new product functionality, use this outcome only when both delivery readiness and product justification are present, or when the scoped implementation is explicitly a measured test with a decision rule. A complete solution specification without a material problem, expected outcome, or way to judge improvement is not enough. Say so plainly, mention any existing gate without relabeling it as your discovery, and stop looking for objections. This does not endorse a later rollout.
- **Test or diagnose first:** The ticket prematurely commits to a solution or priority while a cheaper observation or experiment could change the decision. Identify the pivotal assumption, test, and decision it will unlock. Do not use this label when investigation or testing is already the ticket's next step.
- **Clarify a missing decision:** A consequential choice has no owner or resolution path in the ticket and the scoped next step cannot safely or meaningfully begin without it. Name the decision, its owner, your recommendation, and why it matters. Do not use this label for an explicit pre-implementation gate already in the ticket, a visible question meant to be answered during the work, or a routine design/engineering choice.

For every new-feature review, make the conclusion expose four things even if briefly: **the problem worth solving, the evidence and baseline, the outcome measure, and why the proposed next step is the cheapest credible way to learn or deliver value**. If one is missing, name it and explain whether it blocks implementation or can be obtained inside the proposed test. Do not silently downgrade a missing business problem or success measure to a documentation nicety.

Give the engineer a concise, evidence-based way to raise a real concern with the PM: what is known, what is assumed, why it matters, and the proposed next move. Do not manufacture criticism to fill a template. Preserve the engineer's agency: if the task is sufficiently grounded for its stakes, recommend proceeding rather than creating a handoff. Stop when no unresolved assumption could materially change the next step, even if the task is not perfectly documented. The review itself does not authorize implementation, scope changes, messages to the PM, or edits to the task; present those actions for the user to choose.

## Response contract

Use the following order for a single-task review. Translate the headings and verdict label into the user's language when appropriate, but preserve their meaning and order.

```markdown
## Verdict
[Proceed as scoped | Test or diagnose first | Clarify a missing decision]

[One-sentence reason for the verdict.]

## Product case

- Problem: [...]
- Evidence and baseline: [...]
- Business or user outcome: [...]
- Why this next step: [...]

## Critical gap

[The one missing fact or decision that changes the next move.]

## Recommended next move

[A concrete action, what it will teach or deliver, and which decision depends on the result.]

## Question or message to PM

[A concise, ready-to-use message stating what is known, what is assumed, why it matters, and the proposed move.]
```

Apply these rules without turning the response into an empty form:

- Omit **Critical gap** when there is no material gap. Do not write “None.”
- Omit **Question or message to PM** when the task can proceed and there is no real concern to raise.
- For bugs, obligations, and enabling work, replace **Product case** with **Delivery case** using: impact, evidence, risk or dependency, and verification.
- For several tasks, repeat a compact version of the same order for each task. A summary table may precede the reviews when it materially improves comparison, but it does not replace the per-task reasoning.
- Keep a normal single-task review concise, usually 150–300 words. Use more only when the stakes or genuinely independent decisions require it.
- Do not add extra generic sections, restate the ticket, or fill omitted information with invented content merely to complete the structure.

## Calibration

When creating, updating, or regression-testing this skill, read [references/gold-set.md](references/gold-set.md). It contains a complete product-task example and controlled cases for missing problem evidence, business relevance, outcome, causal rationale, baseline, value metric, guardrail, and decision ownership, plus boundary cases that should proceed. Do not load it for ordinary task reviews.
