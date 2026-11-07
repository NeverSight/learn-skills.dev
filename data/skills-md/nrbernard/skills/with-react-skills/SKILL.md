---
name: with-react-skills
description: Route the React and UI skills through the /bake that follows.
disable-model-invocation: true
metadata:
  version: "0.2.0"
---

For the UI work that follows in this session, load each skill below through the Skill tool the first time its trigger holds:

| Trigger | Skill |
|---|---|
| A new screen, or a change to how one looks or reads | `frontend-design` |
| A component gains a prop, a variant, or shared state | `vercel-composition-patterns` |
| Data fetching, a server/client boundary, or a list that re-renders | `vercel-react-best-practices` |
| The build is done, before /code-review | `web-design-guidelines`, over every changed UI file |

The repo's CLAUDE.md, ADRs and test skills outrank a loaded skill; where one disagrees, follow the repo and name the conflict in the summary.

Done when every changed UI file has passed `web-design-guidelines`, and the summary names each skill loaded and the trigger that loaded it.
