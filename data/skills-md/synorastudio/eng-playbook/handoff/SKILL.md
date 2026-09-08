---
name: handoff
description: Write a compact Handoff for a fresh agent. Use when nearing a context limit, session boundary, agent switch, or pause in multi-session work.
argument-hint: "What should the next session focus on?"
---

# Handoff

Write for a fresh agent with no access to the conversation.

Save it outside the workspace unless the user asks for a repo artifact. Use the operating system temp directory by default.

## Include

- Current goal.
- Current state.
- Decisions made.
- Open questions.
- Relevant files, issues, ADRs, and docs by path or URL.
- Suggested skills for the next session.
- Recommended next action.

## Leave out

- Secrets, credentials, tokens, or sensitive personal information.
- Full copies of artifacts already stored elsewhere.
- Long transcripts.
- Unverified speculation unless clearly labeled.

## Template

```md
# Handoff

## Goal

## Current state

## Decisions

## Open questions

## Important artifacts

## Suggested skills

## Next action
```

If the user provides a focus argument, tailor the handoff to that next session.

Before finishing, verify that the next agent can identify the goal, the exact stopping point, and one concrete next action without consulting the conversation.
