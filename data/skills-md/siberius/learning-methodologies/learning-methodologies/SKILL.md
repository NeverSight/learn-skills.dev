---
name: learning-methodologies
description: Design or review educational applications by connecting learning goals, learner needs, activities, feedback and evidence of learning. Use for new learning tools or substantive changes to their teaching design. Do not apply to cosmetic changes or ordinary bug fixes without a learning-design issue.
metadata:
  version: "1.3.0"
  license: "MIT"
  repo: "https://github.com/siberius/learning-methodologies"
  author: "Luděk Sušický"
  format: "native bundle with generated standalone Markdown"
---

# Learning methodologies

Help design, implement or review educational applications whose learning activities, support and assessment serve the intended learners. Adapt the depth of work to the request, consequences and uncertainty. A small classroom activity does not need a full evaluation study or a new planning document.

## Didactic methods for applications built with AI

Use the methods to turn educational goals into learner actions, feedback rules and evidence in the generated application. For example, retrieval requires an attempt before revealing the answer, while scaffolding requires controllable help and a distinction between assisted and independent performance. AI can help implement these decisions; its output still needs subject and teaching review. This applies to offline applications as well as justified runtime AI.

Read [didactic rationale](references/didactic-rationale.md) when explaining why a method fits or tracing it into implementation. It connects methods to product decisions and the evidence needed to assess them.

## Working route

Use this route at the depth the task needs: establish the goal and constraints → choose a method for the learning obstacle → connect the learner's activity to evidence → implement within scope → check the result. For a review, inspect the existing design instead of implementing. Reuse known context; do not require a planning document for every step.

Read [decision examples](references/decision-examples.md) when help, alternative answers or uncertain curriculum alignment need clarification. They illustrate decisions, not scripts to copy into every lesson.

## Establish the learning context

Use information already present in the request, project and supplied materials. Ask only about missing information that materially changes the design. For minor uncertainties, state a reasonable assumption and proceed. Avoid a fixed questionnaire or repeated approval for ordinary choices already covered by the request.

Identify the relevant context: learners and prior knowledge, subject, intended outcomes, classroom or independent use, available time and devices, language, accessibility needs, and any supplied curriculum. Follow a curriculum when relevant to the setting; do not assume one national framework. Choose tone from the context and author preference. Do not infer attention, motivation, ability or preferred pedagogy from generation labels.

Include the surrounding teaching activity where useful: preparation, individual or group work, teacher intervention, discussion and follow-up. A teacher-led demonstration may need a good discussion prompt rather than accounts and individual scores.

## Connect goals to observable activity

For each important goal, connect the learner's action, evidence, success criteria, assistance conditions and next instructional decision. Keep this concise for small tasks. For open inquiry, the evidence may concern question quality, use of evidence or revision of an explanation rather than one predetermined answer.

Example: the learner predicts how changing resistance affects current, checks a model, explains any discrepancy, and solves a new case independently. Moving a slider or completing a screen alone does not establish understanding.

Use the observed learning obstacle to choose a suitable intervention. Treat an explanation of an error as a provisional hypothesis, not a diagnosis. Select a small coherent set of methods; do not add features merely because they appear in the catalog. Read [methods](references/methods.md) when selecting or implementing a method, support sequence or progression rule.

The method reference explicitly covers Socratic learning, the Feynman technique, the Zone of Proximal Development and scaffolding, worked examples, retrieval and spaced practice, error-based learning, metacognition, inquiry, role-play, peer and cooperative learning, projects, flipped teaching and optional gamification. These are selectable approaches, not required features of every application.

Bloom's taxonomy describes cognitive goals and knowledge types. Keep difficulty and prerequisites separate; do not require six locked levels. For practical, interpersonal or other outcomes, choose suitable evidence and acknowledge what an on-screen task cannot establish.

## Choose a proportionate realization

Distinguish AI used to build the application from AI used by learners in the finished product. Choose among reviewed static content, deterministic interactions or simulations, and runtime AI according to the goal and operating constraints. Hints, feedback and spaced practice can work without an AI service.

Before adding a substantial feature, consider its learning contribution, interaction burden, teacher workload, maintenance, data needs and running cost. Explain material tradeoffs. Do not add accounts, analytics, dashboards, a backend, paid services or external data flows merely to make the product appear complete. Confirm scope-changing decisions when not already authorized.

Read [simulations](references/simulations.md) when modeling a system, running an experiment or designing role-play. Clearly distinguish real observations, model calculations and fictional reconstruction. Never present invented AI output as a measurement or pretend an experiment ran.

Read [runtime AI](references/runtime-ai.md) only when the finished product calls an AI service. Define the teaching role, source boundaries, human oversight, data flows, cost limits and failure behavior. A prompt is not a substitute for application security.

Read [tutor modes and continuity](references/tutor-state.md) when implementing multi-step tutoring, practice/assessment transitions or resuming learning. Keep state and evidence in the application; these features do not require runtime AI.

## Make feedback and decisions trustworthy

Provide a useful next step after an error. In practice, allow help and a route to direct explanation or a worked solution when needed; avoid endless questioning. Reduce assistance based on independent performance, while keeping requested support available. An assessment may restrict assistance under explicit conditions.

Distinguish independent success, supported success, exposure to the answer and uncertainty. One correct guess, a confidence statement or two supported successes do not automatically establish mastery. Do not infer stable ability, motivation or a disorder from a short interaction.

Read [assessment](references/assessment.md) when designing scored tasks, rubrics, adaptivity or learning evaluation. Check subject correctness, plausible alternatives, numerical units and tolerances, and whether the task really requires the intended performance. Preserve valid alternative explanations and methods. Keep game rewards and speed separate from achievement unless they serve an explicit goal.

## Preserve access and teacher agency

Design for relevant WCAG 2.2 AA criteria and the learners' actual needs. Check keyboard operation, visible focus, understandable labels and feedback, alternatives to color or sound alone, and justified or adjustable timing. Choose appropriate ways to perceive information and express understanding; do not assign learners fixed learning styles. Seek specialist accessibility help when the implementation warrants it.

Collect only data needed for the activity and identify who sees it, where it goes and how it is retained. Check provider, school and local requirements for the actual deployment when relevant; do not invent universal legal rules. A local anonymous activity need not acquire accounts or persistent tracking.

Provide a proportionate way for the teacher or responsible author to review content, correct judgments and intervene in inappropriate adaptation. This can be an editable content file rather than a management system. Significant grading or placement decisions need accountable human review.

## Coordinate expertise without inflating the workflow

Use these perspectives as needed; one agent can cover them for a small task:

- Methodologist: intended outcomes, teaching context and instructional choices.
- Subject didactician: content accuracy, prerequisites, examples and misconceptions.
- Assessment designer: evidence, criteria, alternatives and limits of inference.
- Interaction designer: learner flow, help, accessibility and classroom use.
- Developer: data contracts, calculations, state, persistence and failure behavior.
- Reviewer: discrepancies between the goal, design and observed behavior.

Carry their decisions into implementation. Do not label a convenient technical choice pedagogically correct without evidence. Resolve material disagreements through source checking, a targeted check or an explicit unresolved question. Use independent review when complexity or consequences justify it; do not start a team for every task. Invoke other skills only for relevant work and when available.

## Verify and report at the right level

For implementation, check the affected learner path, meaningful errors, help and relevant failure states. For analysis-only requests, report findings and proposals without changing the product. Adapt checks to the application: a simulation needs model checks; runtime AI needs service-failure and output-handling checks; a simple static activity needs neither by default.

Keep three conclusions separate: functional correctness, didactic suitability and observed learning outcomes. Technical checks alone do not establish educational effectiveness. A small pilot can reveal problems without proving causal benefit. Report actual checks and unresolved assumptions; do not invent learner observations or efficacy results.

At handoff, summarize the learning goal, selected approach, important operating assumptions, checks actually completed and remaining limits. Include a goal-to-evidence table only when it makes the result easier to use. Keep the form appropriate to the user's request.

## Integration

When selecting a model, effort or speed, or adapting the loading mechanism, read [model and host profiles](references/model-profiles.md). This includes documentation-based guidance for OpenAI, Claude and Gemini. Keep one shared educational contract and report actual testing separately from intended compatibility. Do not load the profile for an ordinary educational task that does not need it.

Suitable for educational games, quizzes, tutorials, simulations, training and reviews of their teaching design. The core requires no packages, API, specific AI model or student data. References are conditional. The native bundle uses this file and its references; `learning-methodologies.md` is the generated standalone edition. Installation, deployment and other external changes require authorization for those actions. This skill does not replace project instructions or authorize additional scope.

Design references: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [CAST UDL Guidelines](https://udlguidelines.cast.org/). These guide design and review; citing them does not certify conformance or educational effectiveness.
