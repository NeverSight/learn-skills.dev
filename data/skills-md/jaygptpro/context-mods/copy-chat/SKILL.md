---
name: copy-chat
description: |
  Copies this whole Claude Code conversation to the clipboard as clean text: who said what,
  with times, a line where it was compacted, and no tool calls or their output. Ready to paste
  into another chat, a doc or an email. Also answers questions about the Copy chat button
  (the mod that comes with this skill). Use when the user asks to copy, export or move this
  conversation, or about the Copy chat button. Triggers: "copy this chat", "copy the
  conversation", "export this chat", "Copy chat button", "תעתיק את השיחה", "העתק שיחה",
  "להעביר את השיחה לצ'אט אחר".
  NOT for copying a single reply, a file or a code block.
---

# Copy chat

This folder holds a Claude Code mod (the `.claude-plugin` and `hooks` folders): a `Copy chat`
button above the prompt. Claude Code loads it by itself in every new conversation. The button is
the main way. This skill does the same copy when the user asks in words, or when their Claude
Code version does not run mods. Answer in the language of the user's messages.

## Copying the conversation

Run the script in this skill's folder (the base directory shown when this skill loaded), with
the Python the computer has (`python3`, else `python`):

```bash
python3 "<this skill's folder>/hooks/thread.py" "${CLAUDE_SESSION_ID}" "<the folder this conversation started in>"
```

- The first argument is this conversation's id. If it reached you unfilled (the literal text
  `${CLAUDE_SESSION_ID}`), use `--latest` in its place: the newest conversation of that folder.
  Say in one line that with several conversations open in the same folder, `--latest` may pick
  another one.
- The second is the working directory this conversation started in (from your environment
  info), not a folder you moved to since.

The script prints one JSON line:

- `{"ok": true, "mine": N, "claude": N, "compacts": N}`: copied. Tell the user it is on the
  clipboard and ready to paste, with the counts.
- `"why": "no clipboard tool"` or `"the clipboard refused it"`: run it again with `--print` at
  the end, and give the user the text after the first line in one code block to copy.
- `"why": "nothing to copy yet"` or `"the conversation file was not found"`: say so in one line.

Never paste the whole conversation into your reply unless the clipboard failed.

## What the copy holds

`Dana (Oct 6 12:01): ...` and `Claude (12:03): ...`. The name is the first word of the name on
the user's Claude account, else "Me". Times are this computer's time zone, with the date on the
first message and when the day changes. Images read as `[image]`. Subagents, tool output,
reminders and summaries are left out.

## The button

`Copy chat` above the prompt does the same in one press, and a notification says how many
messages went. Without Python it copies the messages without times. When other mods from this
collection, or Smart PreCompact, are installed, the button sits in the same row as theirs.

Off: `claude plugin disable copy-chat@skills-dir`. Remove: `npx skills remove copy-chat -g`.
No button in a new conversation: this Claude Code version does not run mods yet; asking in
words still works.
