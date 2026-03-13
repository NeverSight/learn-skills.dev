---
name: memory-search
description: Search persistent memory for relevant information from past coding sessions. Use when user asks about previous work, past bugs, architectural decisions, or anything that may have been worked on before.
---

1. Call `supermemory_search` with a focused query based on what the user is asking about
2. If results found, surface relevant memories in your response with context
3. If no results found, note that no prior memory exists for this topic
4. For broad questions, try both project scope and user scope
