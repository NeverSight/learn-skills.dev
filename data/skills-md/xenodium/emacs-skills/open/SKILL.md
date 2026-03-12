---
name: open
description: 'This skill should be used when the user invokes "/open" to open files from the latest interaction in Emacs buffers via emacsclient.'
tools: Bash
disable-model-invocation: true
---

# Open files in Emacs

Open files from the most recent interaction in Emacs buffers using `emacsclient --eval`. Only include files relevant to the latest interaction (files just generated, edited, listed, or produced by the most recent tool output), not all files mentioned throughout the conversation.

## How to open

First, locate `agent-skill-open.el` which lives alongside this skill file at `skills/open/agent-skill-open.el` in the emacs-skills plugin directory.

Each file spec in `:files` is either a string (file path) or a plist with `:file` and optional `:line`.

```sh
emacsclient --eval '
(progn
  (load "/path/to/skills/open/agent-skill-open.el" nil t)
  (agent-skill-open
    :files (quote ((:file "/path/to/file1.txt"
                    :line 42)
                   "/path/to/file2.txt"
                   "/path/to/file3.txt"))))'
```

## Rules

- Use absolute paths for files.
- Use `:line` when a specific line is relevant (e.g., an error location or a newly added function).
- Locate `agent-skill-open.el` relative to this skill file's directory.
- If no relevant files exist in the recent interaction, inform the user.
- Run the `emacsclient --eval` command via the Bash tool.
