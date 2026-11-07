---
name: make-bot-ui
description: Build a small operator UI over an agent/webhook backend. Use when buttons or controls should trigger an agent workflow.
---
# Make Bot UI

1. Define the operator actions, payload schema, authentication boundary, and observable completion state before UI code.
2. Keep secrets server-side. Treat webhook URLs/tokens as credentials.
3. Implement the thinnest UI that exposes state, errors, retries, and idempotent request IDs.
4. Make every action safe under duplicate delivery or refresh.
5. Verify one full round trip through the real backend when `observe`/network access exists. Otherwise ship a deterministic local mock plus an explicit integration gap.
