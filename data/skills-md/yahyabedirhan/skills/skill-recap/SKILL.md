---
name: skill-recap
description: Recap how a session used its skills, and end with findings and a verdict on whether any skill needs changing.
argument-hint: "Optional scope, such as \"all sessions from the last 5 hours\"; defaults to this session and its sub-agents"
disable-model-invocation: true
---

# Skill Recap

Look back over one or more sessions and work out how the agent and its sub-agents used their skills: where a skill helped the work, and where a skill, or a missing one, cost the session. End the **recap** with **findings**, each backed by **evidence** from the transcripts, and a **verdict**.

## Parameters

- `<skills-repo>`: the user's own skills repo on GitHub, as `owner/repo`.

## 1. Select the sessions

- **By default**, cover the current session and every sub-agent it spawned, at any depth. The session itself is in your context. Sub-agents ran in their own contexts, so read their transcripts from disk.
  - **When part of the session was compacted away:** read its transcript for the missing stretch.
- **When the user names a scope** such as a time window, a project or a list of sessions, use exactly that scope, sub-agents included.
  - **When the scope can be read more than one way,** such as which projects a time window covers: ask before reading.

### Where transcripts live

Claude Code keeps transcripts as files with one JSON object per line, laid out as below. The layout can change between versions, so when a path doesn't resolve, search `~/.claude/projects/` for the session id.

```text
~/.claude/projects/<project>/                 <project>: the session's working directory, with / and . turned into -
  <session-id>.jsonl                          the main session
  <session-id>/subagents/agent-<id>.jsonl     each sub-agent, nested ones included
  <session-id>/subagents/agent-<id>.meta.json its type, task description and spawn depth
```

The current session's id is in the `CLAUDE_CODE_SESSION_ID` environment variable. Skill loads appear as `tool_use` blocks named `Skill`, with the skill in `input.skill`, and as `<command-name>/<name></command-name>` in user messages.

- **For another harness:** find where it stores its sessions and how a skill load shows there. Codex keeps them under `~/.codex/sessions/` and loads a skill by reading its `skills/<name>/SKILL.md`, so a read of that file is the load. A session that edits the skill reads that file too, so tell an edit's read apart from a load.

## 2. Audit

Transcripts run long: search them for what the audit needs, such as skill loads, errors, retries, long runs of tool calls on one problem, and the user's corrections, and read around each hit rather than reading them whole.

Weigh every skill loaded in the scope, and every stretch where a skill was missing. Put in the recap anything where a skill helped or hurt the work, for example:

- tokens or time spent that a skill could have saved, or that a skill caused
- a rabbit hole a skill led into, or failed to prevent
- information in a skill that was wrong, or stale
- a surprise: something a skill assumed that turned out different in reality
- a skill that should have triggered and didn't, or triggered when it shouldn't have
- a rule the user stated in chat that no skill carries
- a workaround an agent invented for something a skill should cover

These are examples, not a checklist. Audit skills from other people's repos the same way as the user's own.

Each finding carries:

- **Skill**: its name and source repo, or "no skill" when one is missing
- **Evidence**: which session or sub-agent, and what happened there, quoted or closely paraphrased
- **Cost**: what it cost or risked, in tokens, time, wrong output or the user's attention
- **Opportunity**: the change to the skill that would fix it

Leave out anything that went wrong for reasons no skill could address, because a finding must point at a change to a skill.

## 3. Report

Give the findings, then the verdict:

- **"No skill changes needed."** when nothing qualifies. This is a good outcome, not a failed recap.
- Otherwise **"<n> opportunities"**, naming the skills they touch.

When there are opportunities, close with the next step: the user runs `/to-tickets` to file them as issues in `<skills-repo>`, unless they name another repo. `/to-tickets` works from the conversation, so the findings as written are its input.

When `<skills-repo>` is public, write each finding the way the user's instructions say public repositories are written: that rule lives in their agent instructions, so follow it from there.

- **For a finding about someone else's skill:** the user decides whether to file it in `<skills-repo>` anyway, fork the skill, or take it to the skill's own repo.

Stop after the report, and leave creating issues, commenting and editing skills to the user, since they choose which findings are worth acting on.
