---
name: chrisai-chatting
description: Use for experimental chat-session experience work, including session caching and recall, turning agent intake prompts into HTML form artifacts, and converting agent responses into readable HTML preview links.
license: MIT
---

# ChrisAI Chatting

Use this skill for experimental workflows that improve the shape, continuity,
or artifact interface of chat sessions.

Do not use this skill for general conversation quality, prompt editing, broad
assistant behavior design, or production application implementation unless the
request is specifically about chat-session experience patterns.

## Internal Workflows

Use the narrowest workflow that owns the user's requested chat-session
experience artifact.

- `workflows/chat-session-caching-and-recall.md`: For preserving useful chat
  context, producing compact recall artifacts, deciding what should be cached,
  and rehydrating prior session state without overloading a new conversation.
- `workflows/html-form-intake.md`: For turning agent intake prompts into local
  HTML form artifacts that produce raw-text responses for the user to paste
  back into chat.
- `workflows/agent-response-to-html.md`: For mirroring agent responses into a
  readable HTML preview link while preserving the chat response as the
  canonical answer, or for saving/opening HTML when the user explicitly asks.

## General Rules

- Prefer artifact-oriented outputs when the user provides or asks for HTML.
- Preserve source meaning when transforming chat content into cache summaries,
  intake briefs, or HTML artifacts.
- Separate session-memory guidance from repository memory, application state,
  or long-term user profile storage unless the user explicitly asks to connect
  those systems.
- Do not invent persistence, storage, browser automation, or deployment
  behavior. Describe assumptions and ask for the missing target environment
  when those choices matter.

## Decision Rules

- If the task is about compacting, saving, recalling, or transferring useful
  chat-session context, use the chat-session caching and recall
  workflow.
- If the task starts from an agent intake prompt that should be answered as a
  form, an HTML form submission, exported form artifact, or submitted HTML
  payload, use the HTML form intake workflow.
- If the task asks for a response, summary, report, or handoff to become
  pretty, readable, previewed, or HTML-formatted, use the agent response to
  HTML workflow.
- If the request spans multiple workflows, choose the workflow that owns the
  first concrete artifact and keep any follow-up workflow explicit.
