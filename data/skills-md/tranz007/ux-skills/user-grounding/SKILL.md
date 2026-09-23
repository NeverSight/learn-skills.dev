---
name: user-grounding
description: Ground UX work in actual users and evidence when who the design is for, their goals or context, or the strength of user knowledge is materially uncertain. Use when a designer asks who this is for, whether personas are useful, what research is needed, what existing research says, or when a decision depends on unsupported assumptions about users. Do not activate merely because a UX task involves users when the audience and need are already clear.
license: MIT
metadata:
  author: Tranz007
  version: "0.2.1"
---

# User Grounding

Answer two questions: **who is this for, and what do we actually know about them?**

## Always

- **Context** — inspect what is already known before asking the user to repeat it. Use `.ux/INTENT.md` when product purpose or outcome can change the answer, and load only the additional project context the task needs.
- **User** — ground the work in the people affected, their goal, task, context, and available evidence. Do not invent user needs, behaviors, or personas.
- **Evidence** — keep known, inferred, assumed, unknown, and conflicted information distinct when the difference matters.
- **System** — prefer established product language, components, patterns, and rules before inventing new ones.
- **Clear** — lead with the useful point, use the minimum structure needed, and remove generic AI filler.
- **Trust** — never invent evidence, requirements, rationale, implementation status, or compliance.
- **Outcome** — for substantial multi-step work, keep intent active, use a small `.ux/STATE.md` only when continuity needs it, prioritize the highest-impact unresolved gap before polishing, and verify the actual experience against intent before declaring completion.

Do not recite these rules to the user unless one of them materially affects the answer.

Do not introduce research questions, personas, or discovery work when the user and task are already clear or the missing information would not materially change the work.

## Stay out of the way

Do not turn ordinary design work into a discovery exercise.

If the people affected, their task, and the relevant context are already clear enough to make the decision, proceed with the work. A small content, layout, state, or component change does not need a persona or research plan merely because one could be created.

Only dig deeper when uncertainty about the user could materially change the problem, design direction, priority, risk, or validation approach.

## Inspect evidence before asking

Look for the smallest relevant set of existing research, interview notes, usability findings, analytics, support or sales evidence, field observations, prior decisions, product documentation, and meaningful behavioral segments.

Do not ask the designer to summarize research the agent can inspect directly.

When useful, distinguish:

- **Observed** — behavior seen directly in research or use;
- **Reported** — what people said in interviews, surveys, support, or feedback;
- **Behavioral evidence** — analytics or other product-use evidence;
- **Assumed** — what the team currently believes without supporting evidence;
- **Unknown** — information that could change the design but is not established.

Use the existing UX Skills evidence language when a simpler Known / Inferred / Assumed / Unknown / Conflict distinction is sufficient.

## Build only the user picture the work needs

Focus on relevant differences, such as:

- the actor or user group;
- the goal or job they are trying to accomplish;
- the task and surrounding context;
- frequency, familiarity, urgency, interruption, environment, or device when they matter;
- roles, permissions, accessibility needs, language, or domain expertise when they affect behavior;
- meaningful differences between groups that require different design behavior;
- evidence supporting those differences.

Do not add demographic detail unless it is relevant and evidenced.

## Treat personas as optional

Never fabricate named personas, demographics, motivations, quotes, or pain points to make the work feel complete.

Use personas only when research supports durable differences in behavior, goals, context, or needs **and** the artifact would help the team make decisions. If a short user-group description, scenario, journey, or list of behavioral differences is enough, use that instead.

If existing personas are unsupported, say what is documented versus assumed rather than polishing them into credibility.

## Recommend research only when it reduces meaningful uncertainty

If an unknown could change the design, recommend the smallest appropriate way to learn enough. That might be reviewing existing evidence, inspecting analytics or support data, observing the task, conducting focused interviews, or testing the interaction.

Do not prescribe a research method because it is traditional UX practice. Match the method to the question.

If the available evidence is sufficient for the current decision, say so. More research is not automatically better UX.

## Output

Keep the result proportional to the question. Usually provide:

- who the work is for;
- what is known and what is assumed;
- the one or two unknowns that could actually change the work;
- the smallest next move, only if one is needed.

If no additional user work is needed, say that directly and continue.

## Contrast example

Bad:
> Before designing this settings change, let's create three personas, map their journeys, identify pain points, and run user interviews so we can fully understand their needs.

Good:
> The settings change applies to the same signed-in account owners already documented in this product, and it does not change their task or decision. I don't see a user-knowledge gap that would affect this change. No persona or new research is needed; proceed with the design-system and accessibility review.

Why: the good response uses user-centered judgment without making UX process the price of doing simple work.

## Examples

- "Who are we actually designing this for?"
- "Do we know enough about these users to make this decision?"
- "These personas feel made up. Are they useful?"
- "What research do we actually need before designing this?"
- "What does our existing research say about repeat bookers?"
