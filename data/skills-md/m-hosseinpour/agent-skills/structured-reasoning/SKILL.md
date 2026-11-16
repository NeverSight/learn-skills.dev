---
name: structured-reasoning
description: Use when a request requires substantial reasoning, synthesizing evidence, resolving uncertainty, planning, or weighing meaningful alternatives, regardless of domain or whether the result is an answer, recommendation, artifact, or action. Also use for explicit brainstorming, stress-testing an idea or decision, or a guided interview to clarify a plan. Skip simple factual lookups and obvious mechanical tasks.
---

# Structured Reasoning

Help the user get a useful result from a nontrivial request. Understand what matters, investigate what is uncertain, and connect the response or chosen approach to the user's goal. This skill is domain-independent and self-contained.

**Loading is a thinking checkpoint, not an automatic interview or approval gate.** A clear but complex request still benefits from analysis. If context already settles the important decisions, proceed with the requested work without repeated questions, a separate approval turn, or a visible process preamble.

## When to Use

Use for any nontrivial request, even with clear instructions or when only an answer is wanted. Judge the reasoning required, not the subject, output format, presence of code, or size of the deliverable. Work is nontrivial when reaching a useful result requires substantial analysis, connecting evidence, understanding interacting constraints, resolving uncertainty, or weighing meaningful consequences. Repeating many obvious operations does not alone make a task nontrivial.

Also use for an explicit request to brainstorm or explore possibilities, even when small. Scale the discussion accordingly; a bounded request for ideas may need only the ideas, not clarifying questions.

Use the deeper interview method below when the user asks to challenge their assumptions or examine a plan through questions. Keep that method within the requested scope; it is not the default response to every uncertainty.

- Skip simple questions with a direct, well-established answer and routine mechanical tasks with no meaningful uncertainty or trade-off. Do not exclude a substantial explanation or investigation merely because it changes nothing.
- Use relevant specialized methods or skills alongside this checkpoint. They supply domain technique; structured reasoning does not replace them. When investigating a failure, establish the cause before proposing a remedy; use `systematic-debugging` if available.
- Check prior decisions against relevant current evidence only where circumstances could have changed. Do not reopen them merely because this skill loaded.

## Investigate Before Proposing

1. **Understand the request.** Identify the desired result, relevant context, constraints, and what would make the result useful or unacceptable. Distinguish a request for information or support from permission to act. Read supplied material and relevant available evidence before asking about facts they can answer. Keep user priorities, reported experiences, verified facts, proposals, and assumptions distinct.
2. **Close gaps that could change the result.** Separate factual uncertainty, which calls for investigation, from goals, preferences, or boundaries that need the user's input. Use appropriate sources or a focused check; assess relevance, credibility, recency, and conflicting evidence where they matter. Do not turn an inference into a fact or ask the user to guess what can be investigated. Not every request needs files, tools, or a web search.
3. **Find the choices that remain.** Consider viable alternatives, dependencies, resources, risks, reversibility, privacy, and effects on affected people where relevant. Scale depth to what could change the conclusion, scope, approach, or confidence, not every imaginable concern. Respect the user's values rather than substituting your own; acknowledge limits of evidence and expertise when they matter.

If evidence is unavailable, name the uncertainty and its consequence. Do not rely on an unresolved material gap as if settled; give a bounded or conditional answer when useful, or ask for the missing input if it is needed. A low-risk, reversible assumption can be stated without blocking the work. If no material user decisions remain, proceed with investigation or the requested result; gathering evidence does not need another approval by default.

## Conversation

1. **Ask only result-changing questions.** Start with the most important unresolved goal or constraint when its answer is needed. Ask one focused question at a time; batch only genuinely independent questions. Explain why the answer matters when that is not obvious. Do not repeat answered questions or run a fixed questionnaire. Respond to the user's expressed concern before turning it into a decision exercise.
2. **Make choices easy to compare.** Prefer the environment's question tool with selectable options when available; otherwise give concise choices in chat. Explain each option's benefit and cost, mark a recommendation when justified, and leave room for an alternative answer. Word questions neutrally; do not make agreement with your recommendation the easiest answer. Use an open question when meaningful choices cannot yet be offered.
3. **Compare alternatives when they help.** For meaningful trade-offs, present viable options, usually two or three, and explain which best fits the user's priorities and the evidence. Include a smaller step or keeping the current situation when viable. Do not invent alternatives to meet a quota or manufacture a decision in a request for explanation. When the user wants possibilities rather than a verdict, do not force convergence.
4. **Keep consequential choices with the user.** Resolve comparable alternatives before taking actions that commit the user to materially different outcomes, risks, costs, or obligations. A recommendation is not the user's decision. If one approach is clearly better under the agreed constraints, explain why and proceed within authorization; routine execution choices do not need permission. When only advice is requested, offer reasoned or conditional guidance without treating agreement as permission to act.

Stop asking when the goal and constraints are clear enough to provide a useful result and remaining user input cannot reasonably change it. Summarize settled choices and bounded assumptions only when that helps. Do not delay a useful answer until every uncertainty disappears or impose a decision on a user who wants exploration or support.

When feasibility is the only question, answer from sufficient evidence or use the smallest useful check within scope and authorization. Report findings and limitations, not an unsolicited implementation. A proposed experiment is not permission to spend money, contact people, expose information, or change shared state; retaining a disposable prototype is a separate decision.

## Dependent Decisions and Deeper Interviews

Use this method when several decisions depend on one another, answers can change the direction of the work, or the user requests a deeper interview or stress test. A single ambiguity needs only a direct question. This method is part of this skill; no separate interview skill is required.

1. **Map the relevant dependencies.** Identify settled choices, unresolved decisions, and facts still needed. Track which answers would change later questions or options; a small branching outline is enough, and a diagram or document is optional. For example, whether a tool is personal or shared comes before questions about team roles and permissions. Follow branches that could affect the requested result, not every imaginable branch.
2. **Ask what is ready now.** Start with the highest-impact unresolved decision whose prerequisites are known. Batch a few genuinely independent questions when that reduces turns without overwhelming the user, respecting the environment's question-tool limits. If one answer could change another question's wording, relevance, or options, defer that question to a later round. Use the conversation's question format above, not a mandatory interview template.
3. **Investigate missing facts separately.** Look up discoverable facts within the authorized scope rather than asking the user to guess. Delegate only when allowed and worthwhile, not for every lookup. If evidence is pending or unavailable, mark dependent decisions as unresolved; continue with independent questions or useful work instead of assuming the missing answer.
4. **Test the important assumptions.** When depth is warranted, probe unsupported premises, conflicts between goals, plausible failure conditions, simpler alternatives, and evidence that would change a conclusion. Challenge the idea constructively, not the person; do not invent objections, treat preferences as factual errors, or push past a user who declines further probing.
5. **Update the next round.** Use each answer to settle decisions, prune irrelevant branches, and identify newly answerable questions. If new evidence or answers conflict with a settled choice, explain the conflict and revisit only affected decisions. An unanswered material question remains open, not tacitly approved.

Finish using the stopping rule above: the important decisions are settled enough for a useful result, and remaining uncertainty is either immaterial or explicitly bounded. For an interview, briefly summarize the resulting understanding and any material open issues so the user can correct it; do not impose an extra confirmation turn when nothing consequential remains undecided. Completing an interview does not itself authorize implementation or external action.

## Result and Next Step

Provide the kind of result the user requested. Their stated priorities and prior approvals already count as decisions; do not require a separate approval turn that adds nothing. A request to analyze, explain, or discuss authorizes that work, not external action or implementation of the conclusion.

Include what is relevant, not a fixed report template:

- The answer, synthesis, possibilities, recommendation, or agreed approach, connected to the user's goal.
- The important evidence, reasoning, trade-offs, and limits of confidence; distinguish established findings from judgment.
- How to assess usefulness or success where applicable. Match the check to the claim; not every outcome has a test or a measurable guarantee.
- Any meaningful unresolved assumption and an optional or authorized next step, without implying the user must take one.

Use only the detail the work needs. Record decisions or an approach durably when continuity or a handoff warrants it, following existing conventions and the user's request; do not introduce a document workflow by default. A plan can help substantial execution, but neither a plan nor a separate design is mandatory after discussion. Use `writing-implementation-plans` if available when an implementation plan is actually needed, not for every nontrivial answer. Do not duplicate decisions across artifacts.

## Visual Decisions

When a visual would genuinely help understanding or comparison, offer the simplest useful diagram, image, or mockup. Text is sufficient when seeing it adds little; a visual preview is optional.

Read `references/visual-decisions.md` when preparing visual explanations, mockups, or comparisons; it covers representation, preview, feedback, and privacy. Use an existing preview tool or a static artifact rather than adding a custom server. Get the user's decision in the conversation when one is needed, not through assumed browser click capture. If previewing is unavailable, offer a simpler representation. No companion scripts or service are required.

## Scope and Simplicity

- Start with the smallest useful result; exclude work that does not serve the stated goal.
- If a broad request contains independent strands, identify them and clarify priorities only when needed; do not fragment a result the user requested as a whole.
- If new information changes an agreed choice, explain why and resolve only the affected consequential decision, not unchanged details again.
- If investigation contradicts an assumption or approach, reassess rather than forcing the evidence to fit it.
- Do not turn a settled request into an interview, a document, or a plan merely because this skill was loaded.

## Evaluating This Skill

When maintaining the skill's selection or conversation behavior, use [evaluation scenarios](references/evaluation-scenarios.md) to check dependent questions, assumption testing, and nearby cases that should stay simple. These are reusable inputs and expected outcomes, not evidence of completed tests or a required workflow for ordinary requests.
