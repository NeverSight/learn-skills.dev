---
name: dired
description: 'This skill should be used when the user invokes "/dired" to open files from the latest interaction in an Emacs dired buffer via emacsclient.'
tools: Bash
disable-model-invocation: true
---

# Open files in Emacs dired

Open files from the most recent interaction in an Emacs dired buffer using `emacsclient --eval`. Only include files relevant to the latest interaction (files just generated, edited, listed, or produced by the most recent tool output), not all files mentioned throughout the conversation.

## Strategy

Determine whether the relevant files all reside in the same directory or span multiple directories, then call `agent-skill-dired` accordingly.

- **Same directory**: `:dir` is the directory, `:files` are basenames. Opens dired at that directory with the files marked in context.
- **Multiple directories**: `:dir` is the common ancestor, `:files` are relative paths. Creates a curated `*agent-files*` buffer with all files marked.

First, locate `agent-skill-dired.el` which lives alongside this skill file at `skills/dired/agent-skill-dired.el` in the emacs-skills plugin directory.

```sh
emacsclient --eval '
(progn
  (load "/path/to/skills/dired/agent-skill-dired.el" nil t)
  (agent-skill-dired
    :dir "/path/to/directory"
    :files (quote ("file1.txt"
                   "file2.txt"
                   "file3.txt"))))'
```

## Rules

- Use relative paths in `:files` relative to `:dir`.
- Locate `agent-skill-dired.el` relative to this skill file's directory.
- If no relevant files exist in the recent interaction, inform the user.
- Run the `emacsclient --eval` command via the Bash tool.
