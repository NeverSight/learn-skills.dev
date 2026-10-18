---
name: smart-precompact
description: |
  Prepares a Claude Code session for compaction. Reads the session and prints
  ready-to-paste blocks: a /compact line with focus instructions tailored to this
  session, and a resume prompt for right after the compact or for a fresh session.
  Writes nothing to disk by default; `handoff` also saves the resume prompt to one
  file outside the project.
  Works in any language: everything the user sees comes back in the language of
  their messages.
  Use when the context is filling up or right before running /compact. Triggers:
  "prep me for compact", "prepare for compact", "before I compact",
  "ready to compact", "context is almost full", "the chat is getting long",
  "prompt to continue after compacting", "/smart-precompact",
  "תכין אותי לקומפאקט", "תכין לקומפאקט", "צריך לעשות קומפאקט", "לפני קומפאקט",
  "אחרי הקומפאקט", "הקונטקסט מתמלא", "השיחה ארוכה מדי".
  Also runs when the context hook (smart-precompact) adds a note that the context
  passed a threshold: answer the user first, then run with `handoff`.
  NOT for saving notes or memories when no compaction is in play, and NOT for
  shortening or compressing text, titles or files.
argument-hint: "[handoff | save | save notes]  empty = nothing written to disk"
allowed-tools: Read, Write, Edit, Bash(date *), Bash(mkdir -p *)
---

# smart-precompact

The task: pull out of the conversation what is worth surviving, and hand over prompts
that let the session continue after the compact without feeling like you are talking
to someone new.

**The success test**: after the compact, the session does not repeat a mistake that
was already made, does not ask a question the user already answered, and does not
suggest an approach that was already rejected.

**Speed contract**: the run is measured in seconds. No file search, no folder scan, no
`find`. The skill runs when the context is already full, and every unnecessary call
brings the automatic compact closer.

**Language**: these instructions are in English, but everything the user sees follows
the language of the user's messages: the receipt line, block 1, block 2 (translate its
labels naturally, for example "Building:" and "Failed, don't retry:"), and block 3.
Three things never change: the `/compact` command itself, exact strings copied from
the session (errors, paths, commands), and the handoff file's first line
`# Handoff . <root> . <date and time>`, which the hook uses to recognize its own files.

---

## Run modes

| Argument | What happens |
|---|---|
| *(empty)* | **Default.** Reads, filters, prints the blocks. **Zero writes to disk** |
| `handoff` | Also saves the resume prompt to one file outside the project, so a new session can continue from it |
| `save` | Also appends items to documentation files that already exist in the project |
| `save notes` | Like `save`, and also writes to the personal notes folder. **Only on explicit request**, and only if the path is set in `config.md` |

Modes combine, for example `handoff save`. The default touches nothing.

**Request in words**: "prep me for compact and save" or "so I can continue tomorrow" =
`handoff`. "and update the docs" = `save`. "also to my notes" or "also to Obsidian" =
`save notes`. The same request in any language means the same mode. When in doubt,
the default.

### Automatic trigger (hook, optional)
`scripts/compact_hook.py` is installed with `scripts/install_hook.py` (see `README.md`).
It does two things:
1. **Before a compact:** adds a note to the conversation when the context passes the
   first threshold (60%), and again at the second (80%). When the note appears:
   - **Answer what the user asked first.** Do not stop their work for the skill.
   - At the end of that same reply, run the skill in `handoff` mode, with the path
     from the note.
   - One line to the user, in the language of their message: the context passed X%,
     and the /compact line is ready. At the second threshold the wording is sharper:
     now is the time to compact (Smart compact in the band above the prompt, when it
     shows, or paste the line), before the automatic compact runs on its own.
   - The user already asked for the skill in that same message? Run once, and add
     `handoff`.
2. **After a compact:** puts the session's handoff file back into the conversation by
   itself. So when the hook is installed, the user only has to press Smart compact in the
   band, or paste the /compact line.

---

## Step 1: Context (one command)

```bash
date "+%Y-%m-%d %H:%M"; echo "root: $(git rev-parse --show-toplevel 2>/dev/null || pwd)"; echo "session: ${CLAUDE_CODE_SESSION_ID:-none}"; git status --short 2>/dev/null | head -10; grep -qs compact_hook.py ~/.claude/settings.json && echo "restore-hook: on"
```

That is all. No `ls` and no scan. `root` is the project root: every project path
(`docs/`, `CLAUDE.md`) is read from it, even if the conversation moved into a
subfolder. Branch and commit do not go into the prompt: Claude Code loads fresh git
state by itself, after a compact and in every new session.

**Was the conversation already compacted once?** (Part of it shows up for you as a
summary.) Read the session's handoff file if it exists (the path is in step 4b, so
this is a read and not a search). It is the record of what came before the
compaction. No file? Say in the receipt line that part of the conversation is
available to you only as a summary, and do not make things up about it.

---

## Step 2: Triage

Go through the conversation. For each item ask: **"If this disappears, what breaks in
the next session?"**

Five categories, in order of importance:

1. **Dead ends.** What we tried and failed, and why. **The most expensive category.**
   Without it the next session tries the same approach again.
2. **Decisions.** We chose X over Y, and there is a reason. Without the reason it is
   not a decision.
3. **User corrections.** "No, like this", "always do". Working rules, in the user's
   own words.
4. **Working state.** Which files we touched, what is half done, what is untested.
5. **Open items.** What is left, in order.

**Exact wording.** When an item depends on a string (a path, an error message, a field
name, a command), copy it word for word. A summary of an error message is already a
different error message.

**Never secrets.** An API key, token, password, connection string or card number is
replaced with `[REDACTED: what it is]`, even inside an exact string. The blocks get
saved to files and pasted into conversations, and a secret that gets into them has
already left.

### The omission test
Drop every item that:
- git, the code or CLAUDE.md already say (CLAUDE.md is reloaded after every compact)
- is true only for this moment in the conversation ("show me the file", intermediate
  wording)
- was replaced by a later conclusion

An average item is worth one line, not a paragraph. If more than 8 items came out,
you did not filter.

---

## Step 3: Writing the blocks

Read `reference/prompt-templates.md`, and write both blocks **before** any write to
disk. The handoff file is a copy of block 2, so block 2 must be final before it is
saved.

**The split:**
- **Block 2 (the resume prompt) stands on its own.** It is also the file a new session
  will read, and a new session has no summary. So it carries everything: dead ends
  with the reason, decisions with the reason, rules, state, pointers to files, and the
  next step.
- **Block 1 (the /compact line) protects the reasoning inside the summary.** It tells
  the summarizer what to keep and what to compress. **Never state.**
- **The only overlap allowed:** dead ends and user corrections, briefly. They are the
  most expensive to lose, and a duplicated line is cheaper than a session that repeats
  the same mistake. And from the other side: an area that holds a dead end never goes
  into "can compress".

**Length**: a compact line up to 60 words. A resume prompt up to 200 words, and up to
3 steps in "Next up".

---

## Step 4: Writing (only if requested)

**Without `save`, `save notes` or `handoff`, skip this step entirely.**

### 4a. save
Write **only to files that already exist**, relative to `root`. Never create a file or
folder in the project. No target at all? Say so in the receipt line, and the items
stay in block 2.

| What | Where | Cap per run |
|---|---|---|
| Decisions and dead ends | `docs/DECISIONS.md` | 2 |
| Open items, and `[x]` on what was completed | `docs/TASKS.md` | 5 |
| An explicit working rule | `CLAUDE.md` in the project root | **1, and almost always 0** |

Formats, edge cases and contradictions: `reference/routing-table.md`.

**The bar for CLAUDE.md.** The file is loaded into every session, forever, and a
redundant line there costs tokens in every future conversation. A line goes in only if
**all three** hold: (1) the user said it explicitly ("always", "never", "no, like
this"), and a rule is never inferred; (2) it is not already covered there in other
words (read before you write); (3) deleting it would change future behavior. When in
doubt, do not write, and note in the receipt that there was a candidate and why it was
rejected.

**Append-only.** No rewriting, no deleting, no "cleaning up". Only two exceptions:
marking `[x]` on a completed task, and correcting a line you wrote in this same run
when the user corrected its routing right away. Read before you write, and skip an
item that is already there.

### 4b. handoff
**The path:** does the hook note give a path? Use it. Otherwise
`~/.claude/handoffs/<first 8 characters of session>.md`. If session is `none`:
`~/.claude/handoffs/<name of the root folder>.md`.

**The content:** first line `# Handoff . <root> . <date and time from step 1>`, an
empty line, then block 2 as written in step 3, and as the very last line block 1 in a
hidden comment: `<!-- compact: <block 1 without the leading /compact, on one line> -->`.
The Smart PreCompact mod reads that line to run exactly this compact in one click; the
hook strips it before it puts the file back into the conversation. **One file per session, overwritten
on every run**, no archive: working state goes stale, and an old version of it
misleads. The hook deletes a file nobody touched for 14 days, and identifies it by the
first line: **do not change the header**, or the file will never be deleted. This is
the only file the skill creates outside the project. Folder missing?
`mkdir -p ~/.claude/handoffs`.

### 4c. save notes
The path and folder names come from `config.md` in the skill folder. **Do not search.**
No path, or it does not exist on disk? One line in the receipt, and skip. Formats:
`reference/routing-table.md`. In the notes folder you may create today's log if it
does not exist yet, and a new file for each decision
(`<decisions>/YYYY-MM-DD <short title>.md`).

---

## Step 5: The output

**One receipt line**, in the language of the conversation (even when the last message
is only a command): how many items, what was written and where, what was dropped and
why, contradictions found, and whether the conversation was compacted before. When run
from the hook, this line also includes the percentage, and there is no extra line.

**Then the blocks, of type `text` and not `bash`, with no text between them.** (In some
interfaces a bash block gets a Run button, and clicking it runs the text in the
terminal.)

| Mode | What is printed |
|---|---|
| Without `handoff` | Block 1, block 2 |
| `handoff`, without `restore-hook: on` | Block 1 (ends with the file path), block 2, block 3 |
| `handoff` and `restore-hook: on` | Block 1 (ends with the file path), block 3. The receipt line says the resume prompt was saved and will come back into the conversation by itself after the compact |

Block 3 is one sentence for a new session: `Read <path> and continue from there.`

**Is the next task unrelated to what we did?** Add a line: better to `/clear` and start
a clean session with block 2 or 3. A clean session costs less than a compact, and does
not carry a summary it does not need.

### Self-check before printing
- [ ] Every dead end and every decision has a reason
- [ ] Block 2 is understandable to a session that did not see the conversation
- [ ] The compact line does not describe state
- [ ] Up to 60 and 200 words, and up to 3 next steps
- [ ] Exact strings were copied word for word, and secrets were replaced with `[REDACTED]`
- [ ] No detail was invented about a part that was compacted

---

## Example

In another language, the blocks keep this shape with the labels and the prose in that
language.

```text
/compact Keep: why the checkouts/update webhook was rejected (it fired dozens of times
per cart and created duplicate emails), the exact wording of the 429 error from
Klaviyo, and the user's correction: "never send to real customers in tests". You can
compress the JSON debugging round and the log reading.
```

```text
Continue where we left off.

Building: an automatic abandoned cart email for a Shopify store.
State: the function in jobs/cart.ts is written and tested on a demo cart. Not tested against real Klaviyo, not deployed.
Decisions: Klaviyo and not Mailchimp, because Klaviyo has a built-in cart event.
Failed, don't retry: the checkouts/update webhook (it fired dozens of times per cart,
  created duplicate emails). Error: `429 Too Many Requests: rate limit 75/s exceeded`.
Rules set: never send to real customers in tests, only to the test address.
Read before touching: docs/DECISIONS.md
Next up: 1) deploy to staging  2) test on the test address  3) show me before turning it on.
```

---

## Accuracy contract

**Knows**: the content of the current conversation, tool output that ran in the
session, files you read in this run.

**Does not know (a tool is required)**:
- The date: `date` in step 1. Never from memory or from context.
- What is already written in a target file: `Read` before writing. Never assume.

**Asks when**: an item looks like a decision but has no stated reason. Do not invent
the reason. Ask in one line, or omit it.

**Refuses when**: asked to delete, compress or "clean up" existing content in the
documentation files, or when the conversation was already compacted, there is no
handoff file, and details are requested about what was compacted. Say so explicitly
instead of making it up.

---

## Boundaries

**Allowed**: read the conversation. The step 1 command. Read files at known paths
(target files, the handoff file, `config.md`). Print the blocks. Write only in the
modes that were requested, and only to the step 4 targets.

**Forbidden**: running `/compact` yourself (the user pastes it or presses Smart compact;
running it wipes their context). Searching for files or folders. Creating files or folders in the project.
Writing when no write mode was requested. Rewriting or deleting existing lines, except
the two exceptions in 4a. Copying a secret into a block or a file. Inventing a reason
for a decision that was not explained. The skill itself does not commit or push. A
separate user request to commit is handled as usual, after the blocks.
