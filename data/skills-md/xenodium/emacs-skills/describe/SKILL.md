---
name: describe
description: 'This skill should be used when the user invokes "/describe" to look up Emacs documentation via emacsclient.'
tools: Bash
disable-model-invocation: true
---

# Look up Emacs documentation

Look up Emacs documentation using `emacsclient --eval` and summarize the findings. The query is searched across multiple mechanisms (function, variable, face, key binding, and apropos) in one call, returning all findings as a single string.

First, locate `agent-skill-describe.el` which lives alongside this skill file at `skills/describe/agent-skill-describe.el` in the emacs-skills plugin directory.

```sh
emacsclient --eval '
(progn
  (load "/path/to/skills/describe/agent-skill-describe.el" nil t)
  (agent-skill-describe :query "dired-mark"))'
```

## Rules

- Summarize the returned documentation for the user in the conversation.
- Locate `agent-skill-describe.el` relative to this skill file's directory.
- Run the `emacsclient --eval` command via the Bash tool.
