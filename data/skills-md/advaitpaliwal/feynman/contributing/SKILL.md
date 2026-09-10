---
name: contributing
description: Contribute changes to the Feynman repository itself. Use when the task is to add features, fix bugs, update prompts or skills, change install or release behavior, improve docs, or prepare a focused PR against this repo.
---

# Contributing

When working inside the Feynman repository, read the repo-root `CONTRIBUTING.md` and `AGENTS.md` files for project-specific conventions.

Use this skill when working on Feynman itself, especially for:

- CLI or runtime changes in `src/`
- prompt changes in `prompts/`
- bundled skill changes in `skills/`
- subagent behavior changes in `.feynman/agents/`
- install, packaging, or release changes in `scripts/`, `README.md`, or website docs

Minimum local checks before claiming the repo change is done:

```bash
npm test
npm run typecheck
npm run build
```

If the docs site changed, also validate `website/`.

When changing release-sensitive behavior, verify that `.nvmrc`, package `engines`, runtime guards, and install docs stay aligned.
