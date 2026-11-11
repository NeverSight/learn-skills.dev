---
name: setup-plain-writing
description: "Add a short block to your agents' global instructions so they open the plain-writing skill before the first reply. Run once, by hand."
disable-model-invocation: true
---

# Set up plain writing

Add [the block](block.md) to the global instructions of each agent the user has. The `plain-writing` skill must already be installed; if it is not, point to the README and stop.
This setup is a conversation: one question at a time, the recommended answer first, so the user can accept it in a word.

1. **Explore.** Find the global instructions files that exist:
   - Claude Code: `~/.claude/CLAUDE.md`, or a file in `~/.claude/rules/`;
   - Codex: `~/.codex/AGENTS.md`;
   - OpenCode: `~/.config/opencode/AGENTS.md`;
   - any other agent you know runs here.

   Apps that keep instructions in their settings, not in a file, get the block to paste. Note any file that already opens `plain-writing`: offer to update that block in place.
2. **Ask.** Ask which language to reply in; recommend the language the user writes to you. Then show the files and the block in that language, translated when it is not Russian, and ask to write it into each file.
3. **Write** only what the user accepted: add or update the block once in each chosen file, and keep everything else in it as it was.
4. **Report** the changed files and how to undo each change. Add one sentence: to change the style, add a line to the block, for example «Пиши без таблиц»; the block wins over the skill, and skill updates do not touch it.

Done when each chosen file holds the block once.
