---
name: deck-graphify-refresh
description: >-
  Re-index an existing Graphify memory block. Without an id, refreshes
  memory.default. If config/memory missing, prints /deck-init or
  /deck-graphify-init. Use when the user runs /deck-graphify-refresh.
disable-model-invocation: true
---

# Deck graphify refresh

## Instructions

1. cwd = raíz del proyecto.
2. Ejecuta:

```bash
node <path-to-this-skill>/scripts/run.mjs refresh [id]
```

3. Si pide init → muestra **solo** ese mensaje y para.
4. Si `noop: true` / `message: memory.enabled=false` → **solo** `ok, memoria deshabilitada`. No digas que refrescaste. (exit 0 + noop = pausa.)
5. Sin id → `memory.default`. Si ok real → **ok**.
