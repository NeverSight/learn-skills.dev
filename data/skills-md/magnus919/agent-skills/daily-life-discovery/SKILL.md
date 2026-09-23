---
name: daily-life-discovery
description: >-
  Guide a consent-based conversation that helps a person discover how an AI
  agent could improve their day-to-day life: routines, friction, attention,
  decisions, relationships, learning, and small experiments. Use when someone
  asks for a daily check-in, wants the agent to learn how they work, says
  "grill me," wants a conversational journal, or asks what an AI could help
  with. Do not use for therapy, diagnosis, crisis support, covert monitoring,
  or product requirements interviews.
license: MIT
compatibility: Agent-agnostic. Requires only a conversational interface; memory, calendar, and other tools are optional.
---

# Daily Life Discovery

Help the person discover useful forms of partnership with an AI agent through a guided conversation. The goal is not to collect a biography or manufacture tasks. The goal is to surface recurring needs, constraints, preferences, and opportunities that the person may not have thought to ask for.

## Operating contract

1. Ask permission to begin and offer a mode:
   - **Day debrief:** reconstruct and reflect on a recent day.
   - **Pattern discovery:** understand routines, friction, energy, and recurring decisions.
   - **Agent design:** identify what the agent should notice, remember, suggest, or do.
   - **Small experiment:** choose one low-risk change to try this week.
   If the user's request already clearly names the mode, do not repeat the mode menu. A mode choice and a substantive discovery question are separate interaction steps; do not ask both in the same turn unless the user explicitly asks for options.
2. Ask one substantial question at a time. Follow the answer instead of running a fixed questionnaire.
   One question means one information target. Combine context in the wording if needed, but do not append independent questions about platform, workflow, preferences, and boundaries in the same turn.
3. Reflect what you heard before changing topics. Mark interpretations as hypotheses and invite correction.
4. Prefer concrete episodes over abstract self-descriptions: "Tell me about the last time..." beats "What are you like?"
5. Do not turn every answer into advice. First understand; then offer at most two relevant possibilities and ask which, if any, is useful.
6. Preserve agency. Suggestions, reminders, memory writes, and external actions require the person's stated preference or confirmation.
7. Keep the conversation bounded. Ask whether to continue, pause, switch modes, or stop after roughly 8 to 15 questions, or sooner if the person has enough signal.
   When the person gives a time, attention, or energy budget, select the smallest useful mode and ask one high-signal question. Do not present the full mode menu unless they ask for options.

## Capability matchmaking

Before proposing that the agent should help, inspect the capabilities the host actually exposes: tools, installed skills, memory, scheduled jobs, connected services, platform CLIs, and any relevant documentation. Use the host's discovery mechanisms rather than guessing from the skill catalog or the model's training data.

Classify each proposed match:

- **Available:** the host exposes the capability and the agent knows how to use it.
- **Available but unverified:** the host appears to expose it, but the agent has not checked the live integration or current command.
- **Buildable:** the need is clear, but it requires a new skill, a small script, or a platform CLI integration.
- **Not a fit:** the agent cannot safely or reliably provide it.

Say which category applies. Do not claim a platform integration exists until it has been checked, and do not invent commands, APIs, or permissions. If the same need recurs and the missing piece is reusable, offer to make one of these artifacts:

1. a portable skill that teaches any compatible agent the workflow;
2. a focused CLI tool for a platform the person depends on; or
3. both, with the skill orchestrating the CLI.

Ask which platform, account, or data source matters before designing an integration. Until that answer and a live capability check exist, label the match Available but unverified and do not suggest a prototype, command, or integration path as if it were ready. Keep the first version narrow, inspectable, and reversible. A proposal is not an implementation: only report an artifact as built after creating and testing it.

## Conversation loop

For each turn:

1. Identify the user's latest concrete signal: event, feeling, friction, goal, preference, uncertainty, or repeated pattern.
2. Choose the next question that most reduces uncertainty or reveals an actionable opportunity.
3. Ask an open, specific question with a single center of gravity.
4. Reflect the answer in one or two sentences. Separate observation from inference.
5. Match the need against the host's capabilities. Inspect before claiming.
6. Offer a branch: deepen this, explore a neighboring area, summarize what has emerged, or design a reusable skill/CLI.

Load [the question bank](references/question-bank.md) when you need prompts for a particular domain or when the conversation is becoming repetitive. Load [the research basis](references/research-basis.md) when explaining why the interaction uses these patterns or when designing a substantial extension.

## Discovery dimensions

Cover only the dimensions that fit the person's life. Do not force a checklist.

- **Rhythm:** What starts, ends, or interrupts a typical day?
- **Friction:** Where does effort, avoidance, confusion, or context switching recur?
- **Attention and energy:** When is focus available or depleted? What changes it?
- **Commitments:** Which obligations are visible, invisible, recurring, or easy to forget?
- **Decisions:** What choices recur, and what information arrives too late?
- **Relationships:** Which conversations, people, or coordination tasks matter?
- **Learning and curiosity:** What does the person keep returning to, and what would help them go deeper?
- **Environment:** What tools, spaces, devices, or physical constraints shape the day?
- **Delight:** What would make the day more interesting, playful, calm, or meaningful?
- **Boundaries:** What should the agent never notice, remember, suggest, or do?

## Turning discovery into opportunities

Treat the person's report as evidence of a perceived need, not proof of frequency, cost, or causal pattern. Label what is volunteered, observed, and still unknown; do not assign confidence or call something a recurring pattern until the conversation has gathered supporting examples.

Classify each candidate opportunity before presenting it:

- **Notice:** detect or summarize something already available to the agent.
- **Remember:** retain a durable preference, fact, or ongoing thread.
- **Prompt:** ask a timely question or offer a gentle check-in.
- **Prepare:** gather context before a decision, meeting, or transition.
- **Act:** perform a user-authorized task.
- **Explore:** suggest a connection, resource, or experiment.

For every opportunity, state the evidence, the proposed benefit, the uncertainty, and the agency boundary. Prefer small reversible experiments over broad automation.

## Memory and privacy gate

Treat the conversation as private exploration, not automatic consent to store everything.

- Ask before saving a new durable memory unless the user has already established an explicit memory policy.
- Distinguish **said**, **observed**, and **inferred**. Never store an inference as a fact.
- Avoid storing sensitive health, financial, legal, relationship, location, or identity details unless the person explicitly asks and the agent has a safe memory mechanism.
- Offer a reviewable memory summary: "I could remember X, Y, and Z. Should I save any of those?"
- Explain what a memory would change in future behavior. Support correction, deletion, and forgetting when the host supports them.
- Never infer a diagnosis, personality disorder, addiction, or clinical risk from ordinary conversation.

## Session close

When the person wants to stop, or enough signal has emerged, produce a short review:

Ground every closeout line in the conversation. If the available context contains no concrete findings, say so explicitly and do not populate memory candidates, opportunities, or open threads with generic placeholders.

```text
What I heard:
- [recurring situation or need]

Possible ways I could help:
1. [small, concrete opportunity]
2. [optional opportunity]

One experiment:
- [reversible next step, if wanted]

Possible memories:
- [only explicit, durable candidates; none if there are none]

Open question:
- [what remains uncertain]
```

Ask which opportunities, if any, they want to pursue. Do not claim that a memory was saved, a reminder was created, or an action was completed unless the host actually performed and verified it.

## Safety and boundaries

This skill supports reflection and practical coordination, not mental-health treatment. If the person expresses imminent danger, self-harm, abuse, or a medical emergency, stop the discovery flow and follow the host's safety protocol. Do not use this skill to monitor another person without their knowledge, profile a household, or make consequential decisions on someone's behalf.

For sensitive health or diagnostic requests, state the boundary briefly, then ask one non-clinical question or offer one focused next-step branch. Do not respond with a full menu of modes or broad support options before the person chooses to continue.

## When not to use

- Use a product or stakeholder discovery skill for requirements interviews.
- Use a daily-note or journaling skill when the person already knows what they want recorded.
- Use a task-management skill when the request is already a specific action.
- Use a therapy or crisis resource when the person needs clinical or emergency support.

## Completion criteria

The session is complete when the person has either stopped, selected a next step, or received a concise summary with explicit uncertainty and memory choices. Do not continue asking questions merely to fill a quota.
