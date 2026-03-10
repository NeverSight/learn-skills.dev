---
name: talk-to
description: Talk to an agent via Oracle threads. Use when user says "talk to", "message", "chat with", or wants to communicate with another agent.
---

# /talk-to - Agent Messaging

Send messages to agents via Oracle threads. Each agent has a persistent channel thread.

## Usage

```
/talk-to arthur "What's your status?"          # one-shot message
/talk-to arthur --new "Hey, starting fresh"    # skip lookup, create new thread
/talk-to arthur loop ask about their work      # autonomous conversation
/talk-to #42 "follow up on this"               # post to thread by ID
/talk-to --list                                # show channels
```

## Mode 0: No arguments

If ARGUMENTS is empty, show usage help then run --list.

## Routing

| Pattern | Use |
|---------|-----|
| `channel:{agent}` | Persistent per-agent channel |
| `topic:{agent}:{slug}` | Topic-specific thread (with `--topic`) |
| `#{id}` | Direct thread reference by ID |

## Mode 1: --list

1. `oracle_threads()` (no status filter)
2. Filter titles starting with `channel:` or `topic:`, exclude `closed`
3. Display: `channel:arthur (#42) pending — 12 msgs`

## Mode 2: --new (fast create)

Skip lookup. One MCP call.

1. Compose message from intent
2. `oracle_thread({ title: "channel:{agent}", message, role: "human" })`
3. Confirm: `Created channel:{agent} (thread #{id})`

## Mode 3: One-shot (default)

1. Compose message from intent
2. If first arg is `#{id}` → post directly to that thread ID
3. Otherwise: `oracle_threads()` → find `channel:{agent}`, create if missing
4. Post message to thread
5. `oracle_thread_read({ threadId })` → show any agent responses
6. Confirm: `Posted to channel:{agent} (thread #{id})`

## Mode 4: loop (autonomous conversation)

Like Ralph loop — AI drives the conversation autonomously. No user prompts between turns.

1. Find or create thread (`channel:{agent}`, or `--new` to skip lookup)
2. Compose opening message from user's intent and post it
3. **Autonomous loop** (max 10 iterations):
   a. `oracle_thread_read({ threadId })` — check for new messages
   b. If agent responded: read their response, compose a thoughtful follow-up, post it
   c. If no new response: compose a follow-up question or probe deeper, post it
   d. After each exchange, briefly note what you learned
   e. **Stop when**: enough insight gathered, conversation circling, or 10 iterations hit
4. Show summary:
   ```
   Conversation with {agent} (thread #{id}) — {n} messages, {iterations} turns

   Key insights:
   - [insight 1]
   - [insight 2]
   ```
5. Leave thread open for future use

**The goal is insight extraction.** You are having a conversation on behalf of the human to learn something useful.

## Parsing Rules

- First arg = agent name (lowercase), `#id` (thread ref), or `--list`
- `--new` = skip lookup, create fresh
- `loop` = autonomous conversation (AI drives, no user prompts)
- `--topic "slug"` = use `topic:{agent}:{slug}` instead of `channel:{agent}`
- Everything else = the message/intent

## Message Composition

**CRITICAL: You are the composer. The user gives intent, you write the message.**

- Compose a clear, natural message from the user's intent
- Post immediately — do NOT ask the user what to say
- Do NOT use AskUserQuestion for message content
- Show what you posted after sending

If the message already reads like a direct message (e.g. `"What's your status?"`), post as-is.

## Important Notes

- Agent names are always lowercase
- Thread titles are the routing key — never modify existing thread titles
- One channel thread per agent (reuse, don't recreate)
- `#{id}` lets users reference any thread directly — no lookup needed
- All messages attributed with `role: "human"`

ARGUMENTS: $ARGUMENTS
