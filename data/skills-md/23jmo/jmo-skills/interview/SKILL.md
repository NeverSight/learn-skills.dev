---
name: interview
description: Interview user in-depth to create a detailed spec
allowed-tools: AskUserQuestion, Write, Agent
---

Follow the user instructions and interview me in detail using the AskUserQuestionTool about literally anything: technical implementation, UI & UX, concerns, tradeoffs, etc. but make sure the questions are not obvious. be very in-depth and continue interviewing me continually until it's complete. then, write the spec to a file.

**Save location:** `<cwd>/.plans/<relevant-name>.md`

- `<cwd>` = the current working directory — the project you are actually working in. Specs live with the code they describe so they are easy to find, open in an editor, and commit alongside the work.
- `<relevant-name>` = a short kebab-case slug describing the spec topic, ending in `-spec.md` (e.g. `friends-tab-redesign-spec.md`).
- Create the `.plans/` directory if it does not exist — the Write tool creates parent directories automatically.
- Always resolve and write the absolute path, and state the path you wrote to in your reply.
- Do not save specs under `~/.claude/` — they become impossible to find there.

<instructions>$ARGUMENTS</instructions>
