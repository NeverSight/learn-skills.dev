---
name: select
description: 'This skill should be used when the user invokes "/select" to open one or more files in Emacs and select a region relevant to the current discussion via emacsclient.'
tools: Bash
disable-model-invocation: true
---

# Select region in Emacs

Open one or more files in Emacs and select (activate the region around) the code or text most relevant to the current discussion using `emacsclient --eval`. This allows the user to immediately act on the selection: narrow, copy, refactor, comment, etc.

Determine the relevant files and line ranges from the most recent interaction context.

## How to select

First, locate `agent-skill-select.el` which lives alongside this skill file at `skills/select/agent-skill-select.el` in the emacs-skills plugin directory.

```sh
emacsclient --eval '
(progn
  (load "/path/to/skills/select/agent-skill-select.el" nil t)
  (agent-skill-select
    :selections (quote (("/path/to/file1.el"
                         :start 10
                         :end 25)
                        ("/path/to/file2.el"
                         :start 5
                         :end 12)))))'
```

- `:start` is the 1-indexed start line.
- `:end` is the 1-indexed end line.
- The last file visited will have the visually active region. Other files have mark and point set (use `C-x C-x` to reactivate when switching to them).

## Rules

- Use absolute paths for files.
- Choose the region most relevant to the current discussion (e.g., a function just modified, a block with an error, code just generated).
- If no specific region is apparent, select the entire relevant function or block.
- Locate `agent-skill-select.el` relative to this skill file's directory.
- If no relevant files or regions exist in the recent interaction, inform the user.
- Run the `emacsclient --eval` command via the Bash tool.
