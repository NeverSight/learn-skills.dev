---
name: route-work
description: Use only when the user explicitly asks to route a work kickoff to its first workflow owner or decide whether a proven in-flight owner should continue.
license: MIT
---

# Route Work

Read [references/routing.md](references/routing.md) through its
`route-work-contract-end` marker before assessing the request. It is the
single source of truth for every routing decision and output; do not recreate
its tables here.

## Assess, render, stop

1. Assess the request under the reference.
2. Render exactly one of its response templates without changing its
   bold first line or section labels.
3. Stop immediately after the card.
