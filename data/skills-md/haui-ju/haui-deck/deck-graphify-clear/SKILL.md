---
name: deck-graphify-clear
description: >-
  Delete all Graphify memory blocks and set memory to null. Works when
  memory.enabled=false (cleanup). Always confirm before deleting. Does not
  revert .gitignore or npm scripts. Use when the user runs /deck-graphify-clear.
disable-model-invocation: true
---

# Deck graphify clear

## Instructions

1. cwd = raíz del proyecto.
2. Plan (`code: 2` = esperando confirmación):

```bash
node <path-to-this-skill>/scripts/run.mjs clear
```

3. Si pide init → muestra **solo** ese mensaje y para.
4. Detalle breve → **pide confirmación**. Si hay `warning` (symlink/path escapado), menciónalo.
5. Solo si confirma:

```bash
node <path-to-this-skill>/scripts/run.mjs clear --yes
```

No revierte `.gitignore` ni quita scripts `graphify:*` / `.haui-deck/run-graphify.mjs` (by design).
Sin confirmación → no borres. Al final: **ok**.
