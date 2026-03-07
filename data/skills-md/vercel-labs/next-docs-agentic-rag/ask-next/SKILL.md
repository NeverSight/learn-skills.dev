---
name: ask-next
description: >-
  Look up Next.js documentation for a topic. Use before implementing any
  Next.js feature to get accurate, up-to-date framework knowledge.
argument-hint: "[topic - e.g. cache components, routing, server actions]"
disable-model-invocation: true
user-invocable: true
allowed-tools: Bash
---

Query the Next.js documentation RAG API for the topic: $ARGUMENTS

Steps:

1. Call the RAG API:

```bash
curl -s -X POST "https://next-docs-agentic-rag.labs.vercel.dev/api/rag" \
  -H "Content-Type: application/json" \
  -d "$(jq -n --arg q "$ARGUMENTS" '{query: $q}')"
```

2. Read the returned documentation carefully.

3. Present a concise summary of the relevant Next.js documentation, citing specific doc file paths where applicable.
