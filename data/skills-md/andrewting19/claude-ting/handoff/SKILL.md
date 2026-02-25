---
name: handoff
description: Hand off work to a fresh dev session when context is running long. Creates a briefing and spawns a new session the user can attach to.
---

# Handoff Skill

Use this skill when context is running long and you need to hand off work to a fresh session. Instead of compacting and losing nuance, create a comprehensive briefing and spawn a new dev session that can continue with full context.

## When to Use

- User explicitly requests a handoff
- Context is getting long and quality may degrade
- You've accumulated significant context that would be lost in compaction
- The remaining work is substantial enough to warrant a fresh session

## The Handoff Flow

1. **Synthesize your knowledge** - You have all the context. Distill it into what the next agent actually needs.

2. **Spawn dev session** - Use `create_dev_session` from the dev-sessions MCP.

3. **Send the briefing** - Use `send_dev_message` to deliver a comprehensive briefing (see structure below). Write it directly into the tool call - don't duplicate it in chat.

4. **Inform the user** - Tell them the session ID and how to attach.

## Briefing Structure

This is a recommended structure. Adapt it based on what's actually important for your specific situation.

```markdown
## Handoff Briefing

### Goal
What we're ultimately trying to accomplish. Be as thorough as needed - if the goal requires detailed explanation, provide it.

### Current State
- What's been completed
- What's in progress
- Key decisions made and the reasoning behind them

### Relevant Code
Files and areas of the codebase that matter for this task. Not an exhaustive list -
just what the next agent should start with. They can explore from there.

- `path/to/important/file.py` - why it matters
- `path/to/another/` - what's in this directory

### What's Next
The concrete next steps. Be specific but not overly prescriptive.

1. First thing to do
2. Second thing to do
3. etc.

### Context and Gotchas
Things you learned that aren't obvious from the code:
- Gotchas and pitfalls
- Why certain approaches were chosen
- What didn't work and why
- Anything non-obvious

---

## Instructions for You

1. Read the relevant code listed above. Explore further as needed to build understanding.

2. Once you understand the codebase and the task, summarize your understanding and
   proposed approach.

3. **Wait for the user** - Do not start implementation until the user explicitly
   says to continue. They will attach to this session and review your understanding first.
```

## Guidelines for Writing Briefings

**Be thorough where it matters** - Complex business logic, non-obvious constraints, nuanced requirements - explain these fully. Don't omit critical details just to be concise.

**Be concise where you can** - Don't waste tokens on things the receiving agent can figure out. They're intelligent. Give them files and they can explore the code themselves.

**Stay focused** - Include what's relevant to the task. Skip tangential context that won't help them succeed.

**Include the "why"** - Decisions without reasoning are hard to build on. If you chose approach A over B, say why.

**Mention what didn't work** - Failed approaches are valuable context. The next agent shouldn't repeat your mistakes.

## After Sending

Tell the user:
```
Handoff complete. I've created session [session-id] with a full briefing.

To continue:
  tmux attach -t dev-[session-id]

The new agent will read the code and present its understanding.
It's waiting for you to say "continue" before taking any action.
```
