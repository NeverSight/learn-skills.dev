---
name: highlight
description: 'This skill should be used when the user invokes "/highlight" to highlight relevant regions in one or more files in Emacs via emacsclient.'
tools: Bash
disable-model-invocation: true
---

# Highlight regions in Emacs

Highlight relevant regions in one or more files in Emacs using `emacsclient --eval`. Files are opened in a temporary read-only minor mode with highlighted overlays. The user presses `q` to exit the mode and remove all highlights in that buffer.

Determine the relevant files and line ranges from the most recent interaction context.

## How to highlight

First, determine the path to `agent-skill-highlight.el`. It lives alongside this skill file at `skills/highlight/agent-skill-highlight.el` in the emacs-skills plugin directory.

```sh
emacsclient --eval '
(progn
  (load "/path/to/skills/highlight/agent-skill-highlight.el" nil t)
  (agent-skill-highlight
    :files (quote (("/path/to/file1.el"
                    :regions ((:start 90 :lines 18)
                              (:start 114 :lines 49)))
                   ("/path/to/file2.el"
                    :regions ((:start 94 :lines 18)))))))'
```

- `:start` is the 1-indexed line number.
- `:lines` is the number of lines to highlight from that start line.
- Add as many files and regions as needed.

## Rules

- Use absolute paths for files.
- Locate `agent-skill-highlight.el` relative to this skill file's directory.
- If no relevant files or regions exist in the recent interaction, inform the user.
- Run the `emacsclient --eval` command via the Bash tool.
