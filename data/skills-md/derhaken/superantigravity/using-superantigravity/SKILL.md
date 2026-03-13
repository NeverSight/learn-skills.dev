---
name: using-superantigravity
description: Use when starting any conversation — establishes how to find and use skills, requiring skill check before ANY response including clarifying questions
---

# Using SuperAntigravity

## Overview

You have superantigravity installed. Before any action, check if a skill applies.
Skills are loaded automatically in Antigravity when the task matches the description.

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a skill might apply to what you are doing,
you ABSOLUTELY MUST let Antigravity load and read it.

IF A SKILL APPLIES TO YOUR TASK, YOU DO NOT HAVE A CHOICE. YOU MUST USE IT.

This is not negotiable. This is not optional. You cannot rationalize your way out of this.
</EXTREMELY-IMPORTANT>

## Mandatory Announcement

**Before every response, you MUST say: "Checking applicable skills..."**

This announcement is not optional. It is not skipped for "simple" responses. It is not skipped
for clarifying questions. It is not skipped when you believe no skill applies. You say it first,
then you check, then you respond.

The announcement serves as a checkpoint: if you are about to respond without having said it,
STOP. You have skipped the skill check. Go back and do it.

The skill check is complete when you have announced which skill was loaded, or announced
explicitly that no skill applied. "Checking applicable skills... no skill matched this request"
is a valid and complete check. Silence is not.

## The Rule

**Check for relevant skills BEFORE any response or action.** Even a 1% chance a skill
might apply means you let Antigravity load it. If a loaded skill turns out to be wrong
for the situation, you don't need to use it.

## Skill Matching Examples

These examples show how to map user input to skills. Use them as a pattern, not an exhaustive list.

**Given:** User says "Let's build a login feature"
**Then:** Load brainstorming skill. Reason: "Let's build" signals a planning and ideation phase
before any implementation. The brainstorming skill governs how to approach new feature work.

**Given:** User says "This test is failing"
**Then:** Load systematic-debugging skill. Reason: A failing test is a bug to diagnose. The
systematic-debugging skill governs how to investigate and isolate failures before jumping
to fixes.

**Given:** User says "Implement the auth endpoint"
**Then:** Load test-driven-development skill. Reason: "Implement" on a specific feature is
a code-writing task. The TDD skill governs how implementation work proceeds.

**Given:** User says "What's the best way to structure our database?"
**Then:** Load architecture-design skill. Reason: Structural decisions before code is written
are architectural. The architecture-design skill governs option evaluation and trade-off analysis.

**Given:** User says "Is PostgreSQL or MongoDB better for this use case?"
**Then:** Load deep-research skill. Reason: Comparing options requires gathering information
before making a recommendation. The deep-research skill governs how to do this rigorously.

**Given:** User says "Test the checkout flow on the staging site" or "Click through the signup form" or "Verify the UI after this deploy"
**Then:** Load browser-agent skill. Reason: Interacting with a live web page requires the browser
subagent. The browser-agent skill governs prerequisites, request framing, and completion criteria.

**Given:** User says "Should I update these packages?" or "Add lodash to the project" or "npm audit found vulnerabilities"
**Then:** Load dependency-management skill. Reason: Dependency decisions require evaluating
trade-offs. The dependency-management skill governs how to assess, update, and audit packages.

## Skill Priority

1. **Process skills first** (brainstorming, systematic-debugging) — HOW to approach the task
2. **Implementation skills second** (architecture-design, deep-research) — guide execution

"Let's build X" → brainstorming first, then implementation skills.
"Fix this bug" → systematic-debugging first, then domain-specific skills.

## Skill Types

**Rigid** (test-driven-development, systematic-debugging): Follow exactly.
**Flexible** (patterns): Adapt principles to context.

The skill itself tells you which.

## Error Path

If skill loading fails (Antigravity cannot load the skill file, the file is missing, or the
skill returns an error):

1. Announce the failure explicitly: "Skill loading failed for [skill-name]. Proceeding with
   built-in reasoning."
2. Continue with your best built-in reasoning for the task.
3. Do NOT silently skip the skill load and proceed as if nothing happened.
4. Do NOT pretend the skill loaded when it did not.

Silently skipping a failed skill load is indistinguishable from never checking at all.
The user must know what happened.

## Observable Completion

A skill check is complete when ALL of the following are true:

- You have said "Checking applicable skills..."
- You have identified which skill(s) apply (or stated that none apply)
- You have announced the result: "Loading [skill-name]" or "No skill matched this request"
- If loading failed, you have announced the failure per the error path above

A skill check that ends in silence is not complete.

## Red Flags

These thoughts mean STOP — you're rationalizing:

| Thought | Reality |
|---------|---------|
| "This is just a simple question" | Questions are tasks. Check for skills. |
| "I need more context first" | Skill check comes BEFORE clarifying questions. |
| "Let me explore the codebase first" | Skills tell you HOW to explore. Check first. |
| "This doesn't need a formal skill" | If a skill exists, use it. |
| "I remember this skill" | Skills evolve. Let Antigravity load current version. |
| "This doesn't count as a task" | Action = task. Check for skills. |
| "The skill is overkill" | Simple things become complex. Use it. |
| "I'll just do this one thing first" | Check BEFORE doing anything. |
| "This feels productive" | Undisciplined action wastes time. Skills prevent this. |
| "I know what that means" | Knowing the concept ≠ using the skill. Load it. |
| "I already announced it last time" | Announce it every time. Each response is a new check. |

## Conversation Modes

Antigravity has two primary **Conversation Modes**. You MUST ensure the user has the correct mode selected for the phase of work:

1. **Planning Mode**: Use for research, complex tasks, architecture, and collaborative design work.
2. **Fast Mode**: Use for direct execution, simple tasks, and repetitive implementation steps after the plan is approved.

**Rule:** If you are in a process skill (Brainstorming, Planning, Research, Debugging), you SHOULD be in **Planning Mode**. If you are in an execution skill (Implementation, TDD, Executing Plans), you SHOULD be in **Fast Mode**.

If the current mode doesn't match the work phase, prompt the user: *"I am starting a [Planning/Execution] phase. Please switch to [Planning/Fast] mode in the conversation settings for optimal performance."*

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.

## Specialist Skills

| Skill | When to use |
|-------|-------------|
| `deep-research` | Task needs external information before proceeding |
| `performance-optimization` | Code needs profiling and optimization |
| `security-review` | Code touches auth, input handling, or sensitive data |
| `architecture-design` | Designing systems, APIs, or significant features |
| `confidence-check` | About to implement — verifies readiness |
| `browser-agent` | Interacting with web browser, testing UI flows, verifying web app behavior |
| `dependency-management` | Adding, updating, auditing, or evaluating project dependencies |
