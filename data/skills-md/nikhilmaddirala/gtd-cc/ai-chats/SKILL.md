---
name: ai-chats
description: Start or join an inter-agent chat session. Two Claude Code sessions communicate via a shared markdown file in tmp/. Use when the user says "ai-chat", "start a chat", "agent chat", or provides a chat slug to join.
---

# ai-chats

## Overview

Enables two Claude Code sessions to have a conversation with each other through a shared markdown file. One session starts the chat (creates the file), and the other joins (given the slug). Both agents then take turns writing messages and polling for replies.

## Sub-skills

CRITICAL: You MUST load the appropriate sub-skill based on whether the user is starting or joining a chat.

- **start.md**: Create a new chat session and return a slug for the other agent to join
  - Triggers: "start a chat", "new chat", "ai-chat" (with no slug argument)

- **join.md**: Join an existing chat session using a slug
  - Triggers: "ai-chat <slug>", "join chat", any argument that looks like a word-based slug

## Process

1. Parse user input to determine intent (start vs join)
2. If no slug provided → load `sub-skills/start.md`
3. If slug provided → load `sub-skills/join.md`
4. Execute the sub-skill process

## Guidelines

- Chat files live in `tmp/ai-chats/` (gitignored, ephemeral)
- Slugs use format: `adjective-noun-noun` random words (e.g., `brave-copper-fox`)
- File format is append-only markdown with clear speaker headers
- Each agent polls for new content by re-reading the file periodically
- Keep messages concise — this is agent-to-agent communication, not prose

## Interleaving with user conversation

The chat does NOT require your full attention. You can and should talk to your user between polls.

- If the user sends a message while you're in the poll loop, respond to them normally
- After responding, resume polling — don't abandon the chat
- You can do other work (read files, run commands, answer questions) between polls
- Think of the chat as a background activity, not a blocking foreground task
- Only pause polling if the user explicitly asks you to focus on something else

## Ending the chat

Do NOT end the chat prematurely. Only close when:

- The other agent writes `## END`
- The user explicitly asks you to stop the chat
- The conversation has genuinely reached a natural conclusion AND both agents have no pending questions
- Never end a chat just to "report back" to your user — you can talk to them while the chat stays open
