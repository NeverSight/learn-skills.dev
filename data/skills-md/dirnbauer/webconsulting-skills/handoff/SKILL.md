---
name: "handoff"
description: "Compact the current conversation into a handoff document for another agent to pick up."
---

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save to the temporary directory of the user's OS - not the current workspace.

Include a "suggested skills" section in the document, which suggests skills that the agent should invoke.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

Redact any sensitive information, such as API keys, passwords, or personally identifiable information.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

---

## Credits & Attribution

This skill is based on the excellent work by
**[Matt Pocock](https://github.com/mattpocock)**.

Original repository: https://github.com/mattpocock/skills

**Copyright (c) Matt Pocock** - Agent skills for real engineering workflows (MIT License)

Special thanks to [Matt Pocock](https://github.com/mattpocock) for his generous open-source contributions, which helped shape this skill collection.
Adapted by webconsulting.at for this skill collection
