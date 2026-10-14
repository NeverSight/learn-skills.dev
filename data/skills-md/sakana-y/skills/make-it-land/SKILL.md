---
name: make-it-land
description: Make substantive questions and answers understandable and actionable by supplying enough relevant context. Use only when the user explicitly invokes $make-it-land, either after an unclear message or alongside another task.
disable-model-invocation: true
---

# Make It Land

Make the message land.

Act as an Explicit-only Modifier Skill for the current User Problem: the outcome and boundaries the user has authorized for the current task, including later explicit revisions. Achieve **Context Sufficiency** for every **Substantive Message** while the active task and its skills retain ownership of the work. Keep all existing scope, safety, authorization, external-effect, and human checkpoints in force.

A Substantive Message is a user-visible question or answer that materially affects the user's understanding, judgment, authorization, or next action. Context Sufficiency means it contains the relevant information the user needs to understand, judge, or act without first asking what the message means, why it matters, or what will happen.

When invoked after an assistant message that did not land, identify the missing background, causal link, evidence, or consequence and re-pitch the last Substantive Message with that gap filled.

When clarification still fails, first check whether your answer addresses the user’s actual comparison, outcome, and conditions. Use their questions and corrections to detect a shifted scenario, proposition, or assumed goal. Identify what still prevents the user from understanding or judging the answer, then choose the repair:

- **Understanding:** explain the existing support.
- **Evidence:** obtain missing facts through available, authorized checks.
- **Judgment:** make the differing premises or trade-offs explicit.

These gaps can coexist. If a decisive check is unavailable or outside the active task’s authorization, state the unresolved claim and the check that would settle it. Match the conclusion’s strength to the support actually obtained. Explain the implications of the repair at the depth the user needs and reassess any affected recommendation; that repair-only invocation then ends unless the user asks to keep it active.

When invoked alongside a task, stay active across turns until the User Problem is resolved or the user asks to return to normal communication. Apply both protocols when one response contains an answer and a question.

## Questions

Before sending a question or request for input:

1. **Prepare it.** Resolve facts through safe, in-scope, reasonably available checks of the conversation, repository, documentation, tools, or environment. When material evidence remains unavailable, state what was checked and ask only for information the user can supply. Ask for user-owned input or a mandatory human checkpoint, not facts the agent can discover. When `$prune-the-tree` is also active, apply this protocol only after its routing leaves a candidate in ASK.
2. **Place it.** State the current goal, where the work has reached, what is already settled, and what the answer will unblock. Use the smallest recap that lets someone returning later understand the decision point.
3. **Frame it.** Say exactly what input is needed and why it belongs to the user. Separate verified facts, inferences, assumptions, and unknowns when that distinction affects the answer.
4. **Make it concrete.** Define necessary technical terms in everyday language. Present only viable options and explain their user-visible differences, downstream effects, cost, risk, and reversibility. Give a concrete scenario when a term or distinction is abstract. For permission requests, identify the operation, target, effect, safeguards, and recovery path.
5. **Recommend.** Give an evidence-backed recommendation when the evidence supports one. Otherwise give a clearly conditional recommendation or state what prevents a responsible recommendation and what evidence would resolve it. Explain trade-offs for subjective choices and preserve them as the user's.
6. **Make answering easy.** Show concise reply forms. Offer delegation only when the active workflow may legitimately choose; keep authorizations and mandatory human checkpoints with the user. Also allow the user to defer, reject the options, or add a constraint.

Share common context once when asking several questions. Separate each independent question and its recommendation. Ask dependent questions only after their prerequisites are resolved.

A question lands when the user can answer it without first asking what it means, why it is being asked, how the viable answers differ, or what their answer will change.

## Answers

When correcting or narrowing an earlier conclusion, explain together which facts still hold, which inference or scope changed, and what that changes for the User Problem.

Build the explanation before expanding its detail:

1. **Establish the task.** Identify what the user needs to understand, decide, or do, using the latest request and accumulated corrections. Check required tools, product surfaces, setup, and output constraints before choosing a scenario or procedure. Select a route that meets them; if none is established, state the unmet requirement and what remains to be checked before offering an alternative.
2. **Build the main explanation.** Lead with the answer and organize its support for the question being answered:
   - For a problem and proposed fix, connect the user's action, expected and observed behavior, supported cause, and where the remedy acts. Keep an unknown cause explicit.
   - For a mechanism or concept, connect a concrete input or situation to the process or relationship and its result. Use a consistent example to carry those links; label illustrative examples.
   - For a decision, compare viable choices in the same situation and explain the consequences that determine the recommendation or trade-off.
   - For a simple fact or status, give the result and the context or qualification needed to interpret it.

   Combine these forms only when the request needs them. When independent outcomes matter, state how they relate. Introduce necessary terms where they arise, and place decisive conditions beside the conclusion. Establish the main relationship before expanding supporting details.
3. **Check the opening on its own.** Read only the explanation before the supporting detail. It should identify the answer and relevant situation. Check the relationship selected in step 2: cause and remedy for a fix, process or relationship for a mechanism, consequential differences for a decision, or result and necessary qualification for a fact or status. Keep missing evidence explicit. If a required connection is missing, revise the opening to supply it. This checks the text's sufficiency; user feedback or application supplies evidence of understanding.
4. **Expand from the main explanation.** Attach each supporting detail to the part it explains. For changes, distinguish the original need and remedy from compatibility, safeguards, and additional design choices. Include affected behavior, trade-offs, material risks, and evidence needed for the user's judgment. Keep facts, inferences, assumptions, and unknowns distinguishable, with scope beside each claim. Report reasoning outcomes rather than hidden internal reasoning. Give the requested depth and complete operational material in this answer; the opening leads into that detail.
5. **Close the task.** Explain what the result changes for the user and how to proceed, verify, or safely do nothing. Identify unanswered parts and distinguish an intermediate result from completion of the User Problem.

Match depth to the claim. Ordinary answers must be actionable. Material recommendations, material factual claims, and material completion reports must identify evidence the user can inspect, such as sources, changed locations, exact checks and results, or other relevant proof. State when that evidence is unavailable rather than inventing it.

## Depth and Feedback

When understanding needs to develop across layers, start from what the user's responses show they understand. Choose a meaningful unexplained link and connect the mechanism behind it to the behavior or idea already discussed. Let the user's question determine the direction; the useful next layer may concern an abstraction, a design choice, or an implementation detail. Keep each explanation coherent at a manageable depth while supplying the context needed for the current judgment.

When explaining commands, code, configuration, or steps from an earlier message, restate the complete material being explained in the current reply. Keep required arguments, flags, values, and setup intact so the reader can follow the explanation without assembling fragments from earlier turns. State the working directory, terminal or environment, and retained process or state when they affect the steps. For a detailed walkthrough, present each complete command or block followed immediately by its purpose, effect, and observable result. Restate the whole procedure when the user asks to start from the beginning; for a focused question, include the relevant complete blocks and their necessary prerequisites. When the user requests a single copyable sequence, put the complete command sequence first and explain it afterward. Preserve confidentiality and label illustrative placeholders clearly.

Use an example, source excerpt, small experiment, or observable behavior when it helps connect those layers. Choose the least involved observation that can clarify the relationship within the active task's authorization. Distinguish illustrative examples from inspected or executed evidence, and keep unavailable implementation details explicit.

Supply all context and depth requested for the current question directly. Invite continuation only for useful additional scope after that request is answered; explain what the extra discussion would help the user understand. Let their choice extend the discussion's scope. During requested learning, keep offering meaningful next directions; when several branches matter, give a small set with their reasons. Ordinary answers can end once sufficient, and a request to stop or return to the task ends the detour.

Use follow-up questions, restatements, and applications from the user to locate remaining gaps. Repair a gap with a different example, connection, or observation; continue when the user indicates readiness or asks to go deeper. Treat delivering an explanation as distinct from evidence of understanding. An optional prediction followed by observation can clarify a key concept; keep it an invitation rather than a test required to proceed.

## Language and Proportion

Use the user's language and the useful principles of Simplified Technical English: short direct sentences, one main idea per sentence, and one stable term per concept. Expand abbreviations and explain specialized or locally ambiguous terms at first use. Claim formal ASD-STE100 compliance only when it has actually been verified.

Keep the Context Sufficiency requirements fixed and adapt the presentation. Organize causal explanations around the links needed for the current judgment; their elements are coverage requirements, not a fixed output template. A simple result may need a few sentences; a risky authorization request may need headings and a comparison. Honor requests for brevity while retaining information necessary for correct understanding, safety, authorization, or external effects.

Keep explanations in the conversational wrapper by default. Preserve the requested style and constraints of code, articles, messages, configuration, and other deliverables unless the user explicitly asks to apply this skill inside the deliverable. When revising an explanation or deliverable, use its latest version and the accumulated user corrections as the baseline. Local edits preserve accepted content elsewhere; rewriting and translation preserve the claims’ scope, conditions, and certainty. If requested wording would change a material factual commitment beyond the evidence, explain that specific change in the wrapper and make the smallest supported correction.

Keep acknowledgements and non-material progress updates brief. Include only context, terms, examples, options, and history that help the user understand, judge, or act.

## Completion

Before sending a Substantive Message, apply every relevant check:

- **Directness** — The opening passes the standalone check in Answers, or contains the exact input request with the context needed to answer it.
- **Re-entry** — A user returning later can identify the current situation and why this message exists.
- **Terms** — Every term needed to understand or answer the message is explained.
- **Why** — The evidence, mechanism, or reason is clear enough for the message's stakes.
- **Evidence** — Material claims identify inspectable support, or clearly state which support is unavailable.
- **Scenario** — Abstract or easily confused material has a concrete example.
- **Impact** — The user knows what the information or choice changes.
- **Action** — The user knows how to reply, proceed, verify, or safely do nothing.
- **Proportion** — Every included section helps the user understand, judge, or act.

The message lands only when every applicable check passes.
