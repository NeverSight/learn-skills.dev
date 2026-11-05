---
name: uigraph
description: Plans and generates UIGraph artifacts, syncs them to the local viewer, UIGraph Cloud, or a self-hosted gateway, starts, opens, stops, kills, restarts, or checks the local UIGraph viewer, and launches Lens reviews. Use for any request about UIGraph, including `.uigraph.yaml` and `.uigraph/` artifacts, the local viewer, `uigraph` or `npx uigraph` commands, syncing, and Lens.
---

## Task

Pick the task from the user's request and read its reference before acting. When the request matches no task, ask what they want to do with UIGraph.

- **Create or update artifacts,** such as diagrams, APIs, database schemas, docs, test packs, and maps: [references/artifact-generation.md](references/artifact-generation.md).
- **Sync artifacts:** [references/sync.md](references/sync.md).
- **Start, stop, restart, or check the local viewer:** [references/local-viewer.md](references/local-viewer.md).
- **Run a Lens review:** [references/lens.md](references/lens.md).

## Questions

Ask the user every question through your agent's question tool, such as `AskUserQuestion` in Claude Code or `request_user_input` in Codex, whenever one is available. There is no exception. Write a question as plain text only when no such tool exists.
