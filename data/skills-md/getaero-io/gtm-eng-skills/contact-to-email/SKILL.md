---
name: contact-to-email
description: "Find and verify email addresses for contacts. Handles name+company, LinkedIn URL, or name+domain starting points."
---

# Contact → Email

This is a recipe shortcut. It pre-selects the contact-to-email recipe but the **gtm-meta-skill governs the entire session**.

## Execution order

1. **Invoke `gtm-meta-skill`** using the Skill tool.
2. **Follow the meta-skill's full routing instructions** — analyze the user's complete prompt and load every sub-doc the meta-skill tells you to. Do not skip docs just because a recipe is pre-selected.
3. **Additionally read** the contact-to-email recipe at `../gtm-meta-skill/recipes/contact-to-email.md` (relative to this file) for the specific workflow.

The recipe only covers one part of the task. The meta-skill handles everything else the user asked for.
