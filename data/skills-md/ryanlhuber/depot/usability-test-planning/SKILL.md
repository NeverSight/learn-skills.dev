---
name: usability-test-planning
description: "Plans a usability test with representative users (goals, participants, tasks, measures, session guide) and summarizes results. Use when a design needs validation with real users or session results need analysis."
---

# Usability Test Planning

## Purpose
Plan a usability test with representative users, covering goals, participants, tasks, measures, and questions, and summarize results in a way that supports decisions.

## When to use
- Use when: a design needs validation with real users, or heuristic findings need confirming.
- Use when: test sessions have been run and results must be analyzed and summarized.
- Do not use when: the aim is to measure market demand or preference at scale; other research methods fit better.

## Inputs
- Required: the design or prototype to test, the questions the test must answer, and the primary user tasks.
- Optional: target users and screening criteria, constraints (time, budget, access, remote or in person), accessibility needs to include, prior findings.
- Assumptions: unspecified participant criteria are stated as assumed.
- For results analysis, required: the tasks with their success definitions (the test plan) and session notes recorded per participant per task. If notes are missing, or do not cover a task, say so and ask for them; report no findings, counts, success rates, or quotes for that task.

## Process
1. State the research questions and the decisions the results will inform.
2. Define participant criteria based on behaviors and needs that matter to the questions, including users of assistive technology where relevant, and the number of sessions with a rationale.
3. Write realistic tasks as scenarios with a goal and starting context, without naming the interface elements or steps to use. Give each a success definition.
4. Define measures: task success, errors, time, effort or confusion signals, and post-task or post-test ratings where useful.
5. Prepare the session guide: introduction, consent and recording permissions, task order and counterbalancing, neutral prompts, and a closing set of questions.
6. Run a pilot and fix unclear tasks or materials before the main sessions.
7. After sessions, and only from supplied session notes, record observations per participant per task, then identify patterns across participants. Judge each task against its success definition: success, errors, effort, and confusion.
8. Report findings with severity, evidence (counts, observations), and confidence, and recommend changes or further validation.

## Rules and heuristics
- Required: tasks and prompts do not lead participants or reveal the answer.
- Required: obtain informed consent and handle participant data per applicable policy.
- Required: report sample size and limits; do not generalize small samples into statistics.
- Required: report findings only for tasks the session notes cover, and list the tasks they do not cover as untested.
- Recommended: separate observations from interpretation in notes.
- Recommended: report what worked as well as what failed.

## Checks
- Each research question maps to at least one task or question.
- Each task has a success definition.
- Participant criteria match the target users and the questions.
- Reported findings cite the evidence and the number of participants affected.
- Findings follow the [repository finding structure](../../../docs/contribution-evidence-and-quality-standards.md#review-finding-structure) where applicable.

## Output
Return a test plan (questions, participants, tasks with success definitions, measures, session guide, logistics) and, after sessions, a results summary with prioritized findings, evidence, confidence, limitations, and recommended next steps. Use the [test plan](templates/test-plan.md).

## Completion criteria
- The plan lets another researcher run the test consistently.
- Results, when reported, trace to observed evidence and state their limits.
