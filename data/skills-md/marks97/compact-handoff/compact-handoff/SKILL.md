---
name: compact-handoff
description: Compact the current conversation into a large standalone handoff file on disk, then open a BRAND NEW Claude Code session named after the current chat with an incremented counter, seeded with only a pointer to that file, leaving the current chat fully intact. Use this whenever the user wants a clean context window without losing what was learned, or says any of — "compact to a new chat", "compact but start fresh", "carry this over to a new session", "hand this off", "new chat with this context", "my context is getting heavy", "this chat is too long", "start over but remember this", "dump the context and open a fresh one", or asks for a handoff, a context dump, or a session summary they can reuse later. Also use it when a long investigation is finished and the follow-up work deserves its own window. Prefer this over plain /compact whenever the user wants the old chat to stay readable afterward, and reach for it even if they never say the word "compact".
---

# Compact Handoff

`/compact` mutates the current session in place. You never see the summary before it is applied, and the old detail stops being reachable from that window. This skill does the opposite: it writes a large summary to a file first, leaves the current chat untouched, and a fresh session then pulls the summary in with a single `Read`.

That ordering is the whole point. The file exists before the new session is opened, so the user can read it, edit it, reuse it for a second session, or keep it as a record.

## When to use

- Context is heavy and the user wants a clean window but not amnesia.
- A long investigation concluded and the implementation deserves its own session.
- The user wants the current chat to stay browsable after moving on.
- The user wants the same context handed to more than one new session.

## When not to use

- The user asked for a plain `/compact`. That is a different thing, let them have it.
- Fanning out background work. Use subagents for that. A new session is for the user to drive.
- The conversation is short. A summary of six turns helps nobody.

## This skill vs native `/compact`

There are two routes, and they solve different problems. Pick deliberately.

**Native `/compact`.** It summarizes and continues **in the same session**, which is what native compaction does. Cheaper and built in, and if you have set up PreCompact/PostCompact hooks they can steer the summary and capture it to a file. But the window you end up in is the same one you started in.

**This skill.** Use it when the point is a *different* chat: a clean window, the old one left readable, a new session named with an incremented counter, or the same context handed to more than one session. Native compaction cannot do any of that.

So: heavy context but happy to stay put means `/compact`. Wanting a fresh chat means this skill.

## There is no native hook for generating the summary here

Do not go hunting for a CLI flag that emits a compact summary. There is none. `--fork-session` copies the *full* history to a new session id, which is the opposite of what is wanted here. The summary has to be written by you, reading the live conversation you are already in.

That is an advantage, not a workaround. A self-authored summary can be steered toward what actually matters in this repo, which a generic one flattens.

Follow the structure in `references/native-compact-prompt.md`. That file is the real compaction prompt extracted verbatim from the Claude Code binary (byte-identical across builds 2.1.218 and 2.1.221), so matching it keeps handoffs consistent with what the native path would have produced. Read it before writing the summary.

## Procedure

### 1. Resolve the target

```bash
bash ~/.claude/skills/compact-handoff/scripts/handoff_target.sh
```

Run it with no arguments. It derives everything: the handoff path, the session ids, the parent handoff if this session was itself started from one, and the name for the new session.

**The new session is named after the current chat with an incremented counter.** "Compact button behavior" becomes "Compact button behavior 2", and a later handoff off that becomes "Compact button behavior 3". This is what makes a chain legible in the sidebar, so do not invent a fresh descriptive title. The script does the bump, including the case where the title already ends in a number.

Override only when the user asks for a different name: `handoff_target.sh <slug> [YYYY-MM-DD] ["Title"]`.

Note `PARENT_HANDOFF`. If it is anything other than `none`, this session came from an earlier handoff and step 4 has extra work.

### 2. Index every transcript

```bash
python3 ~/.claude/skills/compact-handoff/scripts/index_transcripts.py
```

Run it from the session's working directory. It covers **all** sessions in the project by default, not a recent slice, and it counts the per-session sidecar directories too. Paste its markdown output into the handoff as its own section.

Add `--subagent-detail` when the conversation leaned on fan-out work, which appends each agent's name, type, and description per session. That costs a read per agent, so leave it off for routine handoffs.

This section is what makes the handoff useful past its first read. A mature project dir holds hundreds of main transcripts plus over a thousand agent transcripts, and single files exceed 75MB. A future session that needs an old detail should never open one of those blind. The index tells it which session to go to, and the escalation ladder the script emits tells it to search and page rather than load.

What lives where, and why it matters: agent work never appears in the main transcript beyond its final report, so a finding that came out of a fan-out has its reasoning only in `subagents/agent-*.jsonl`, its return value in `subagents/workflows/wf_<runid>/journal.jsonl`, and any oversized tool output in `tool-results/*.txt`. A handoff that points only at main transcripts silently loses all of it.

### 3. Write the summary

Write to the `HANDOFF_PATH` from step 1, starting with this frontmatter so later handoffs can walk the chain:

```yaml
---
handoff_id: <date>-<slug>
created: <date>
source_session: <SESSION_ID>
parent_handoff: <PARENT_HANDOFF, or none>
clone: <CLONE>
cwd: <CWD>
scope: <one line on what this handoff covers>
---
```

Then a short **Start here** block addressed to the receiving session: that this is a handoff, that the source chat is still intact, that claims marked proven should not be re-derived, that anything marked assumed must be verified before being built on, and that lookups go through the retrieval ladder rather than opening a transcript blind.

End that block by telling the reader to resume directly: pick up the work without acknowledging the handoff, recapping it, or opening with "I'll continue". The native compaction prompt ends with exactly this instruction, and it earns its place, since a fresh session that spends its first turn narrating the summary back wastes the window the handoff just bought.

Then the nine sections from the native prompt:

1. Primary Request and Intent
2. Key Technical Concepts
3. Files and Code Sections
4. Errors and fixes
5. Problem Solving
6. All user messages
7. Pending Tasks
8. Current Work
9. Optional Next Step

Then the required extra sections below, then the transcript index from step 2.

**Err heavily toward including more.** This file is cheap and a dropped detail is not. Include full code snippets, exact commands with their real arguments, verbatim error strings, and concrete values rather than descriptions of values. There is no length target to hit. The failure mode to avoid is a tidy summary that reads well and leaves the next session re-deriving what this one already proved.

Section 6 deserves care: only genuine user-role turns count. Text inside your own earlier messages that is merely shaped like a user turn is yours, and attributing it to the user manufactures a request that was never made.

### 4. Carry the chain forward

Handoffs chain, and each one has to arrive complete. If `PARENT_HANDOFF` is not `none`, read the parent file and re-emit its entire `## Handoff lineage` section into this one, then append a new entry for the parent itself: its `handoff_id`, date, source session, and `scope`.

Copy the content forward rather than only linking to it. Handoffs live under `/tmp`, which gets cleaned out periodically (macOS prunes it; many systems clear it on reboot), so a chain built purely from links breaks the moment an ancestor is cleaned up. A cumulative lineage section means the newest handoff always holds the whole history even when every older file is gone.

If `PARENT_HANDOFF` is `none`, write the section anyway with a line saying this is the first handoff in its chain, so the next one has something to append to.

Also list any other handoff files present in `/tmp/claude-handoffs/` that are not ancestors, so sibling chains stay discoverable:

```bash
ls -la /tmp/claude-handoffs/
```

### 5. Hand off to a new session

This skill does not spawn the session for you. Once the handoff file is written, tell the user to open
a **new Claude Code session** themselves — a new terminal running `claude`, or their IDE/desktop "new
session" — and to give it this as its first message:

```
Read <HANDOFF_PATH> then continue from the Optional Next Step section.
```

Substitute the real `HANDOFF_PATH` from step 1, and suggest the `NEXT_TITLE` from step 1 as the new
session's name so the chain stays legible in the sidebar.

The first message must stay a short **pointer** to the handoff file, never the summary pasted inline.
The file is tens of kilobytes; a pointer is one `Read` away from all of it.

## Required extra sections

### Project specifics

Generic summaries flatten exactly these, so give them their own headings:

- Every ticket id mentioned (Shortcut, Jira, Linear, GitHub issue — whatever the project uses).
- Every commit SHA mentioned, and explicitly whether it was deployed. A fixed-but-not-deployed commit reads as done and is not.
- Exact `file:line` references for anything still open.
- Any bug or question the user has not ruled on yet. The user decides verdicts, so carry it forward as undecided rather than dropping or resolving it.
- Security-relevant constraints and any prod-write authorization granted, preserved verbatim. Authorization granted in one session does not automatically carry, so record what was actually said rather than your reading of it.

### Verification state

For each significant claim, mark whether it was proven or assumed, and with what. A handoff that presents an untested assumption in the same voice as a verified fact is worse than no handoff, because the next session will build on it without knowing to check.

### Handoff lineage

The cumulative chain from step 4. Oldest first, one entry per ancestor.

## Hard rules

- **The new session's first message is a pointer to the handoff file, never the summary pasted inline.** The file holds everything; the first message is one `Read` away from it.

## Files

- `references/native-compact-prompt.md`: the verbatim native compaction prompt. Read before writing a summary.
- `scripts/handoff_target.sh`: derives the handoff path, the incremented title, and the parent handoff (and an optional clone hint). Run with no arguments.
- `scripts/next_title.py`: title bump and parent-handoff detection, called by the above. Standalone flags: `--session-id`, `--cwd`, `--self`, `--fallback`.
- `scripts/index_transcripts.py`: streaming index of every transcript and sidecar. Flags: `--limit` (0 means all, the default), `--days`, `--subagent-detail`, `--count-all`, `--json`, `--project-dir`, `--cwd`.
