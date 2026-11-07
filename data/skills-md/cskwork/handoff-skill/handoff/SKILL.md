---
name: handoff
description: 'Handoff: saves state to pause, resume, or transfer work. Use when: "handoff", "pause here and continue later", "hand this over to QA or another agent".'
---

# Handoff

Create a handoff packet: a factual state snapshot plus an executable continuation plan. The packet is for the next agent, who starts with fresh context, so it must carry enough ground truth to resume without guessing.

## Workflow

1. **Fix the handoff target.**
   Infer whether the recipient is the same agent later, another coding agent, a reviewer, QA, or a human. If the user supplied arguments, treat them as the next session focus. Ask one question only when the recipient or purpose changes what must be captured.


2. **Inventory the current state.**
   Gather only durable facts:
   - Original goal and latest user request.
   - Current repository, branch, environment, and relevant paths.
   - Files created, edited, or intentionally left untouched.
   - Commands run, tests run, outputs observed, and commands still running.
   - Decisions made, options rejected, and why.
   - Known blockers, risks, assumptions, secrets, credentials, and external dependencies.

   Prefer artifact references over pasted bulk content. Use paths, URLs, issue IDs, commit hashes, command names, and short evidence quotes. If a command such as `git status` hangs or fails, record that exact fact instead of inventing state.


3. **Protect sensitive material.**
   Redact credentials, tokens, passwords, private personal data, and session cookies. Replace them with labels such as `[REDACTED_API_TOKEN]` and describe where the next agent should retrieve them safely.


4. **Write the continuation plan.**
   Convert remaining work into ordered steps. Include the details needed to execute and verify each step:
   - Why it exists.
   - Exact files or systems to inspect or edit.
   - Commands to run when known.
   - Completion criterion.
   - Side effects or rollback concerns.

   Keep tasks small enough that the next agent can complete or verify them one by one.


5. **Save the packet.**
   Use the most durable appropriate location:
   - If the current workspace has a docs convention, use it.
   - Else if a repository is active, save to `docs/handoffs/<YYYY-MM-DD-HHMM>-<topic>.md`.
   - Else save to the OS temp directory and name the file with the same timestamp and topic.

   Link to existing PRDs, plans, ADRs, tickets, diffs, and commits; summarize only what matters for restart.


6. **Run the resume check.**
   Read the packet as if you are the next agent, then check it against the `## Resume Check` checklist below.


## Handoff Packet Template

Use this structure unless a repository already has a stricter handoff format.

```markdown
# Handoff: <task or ticket>

Generated: <YYYY-MM-DD HH:MM timezone>
Recipient: <same agent later | another coding agent | reviewer | QA | human>
Focus: <what the next session should do first>
Status: <not started | in progress | blocked | ready for review | complete except verification>

## Goal
<Original goal and latest user request in one short paragraph.>

## Current State
- Workspace: `<absolute path or URL>`
- Branch or version: `<branch, commit, release, or unknown with reason>`
- Active services or sessions: `<name, pid, URL, or none>`
- Important artifacts: `<paths or URLs>`

## Completed Work
- <Fact with file path, command evidence, or artifact reference.>

## Decisions
- <Decision>: <reason>. Rejected: <alternative and reason>.

## Files And Changes
- `<path>`: <what changed and why>
- Untouched but relevant: `<path>`: <why it matters>

## Commands And Evidence
- `<command>`: <result, exit code, important output, or failure mode>

## Remaining Plan
1. <Action>
   - Why: <reason>
   - Where: `<file, service, or artifact>`
   - Command: `<command or none>`
   - Done when: <checkable condition>
   - Risk: <side effect or none>

## Verification Plan
- <Test, lint, type check, build, manual check, or external validation>

## Risks And Assumptions
- <Risk or assumption and how to verify it>

## Suggested Skills
- `<skill-name>`: <why it should be used>

## Resume Prompt
<A concise prompt the next agent can paste into a new session. Include this handoff path and the first step.>

## Redactions
- <What was redacted and where the next agent should retrieve it, or "none">
```

## Resume Check

Before finalizing, check:

- Goal and latest request are clear.
- Completed work and current state are evidence-backed, not guessed.
- Every modified file has a reason.
- Files and areas the next agent must not touch are named.
- Every running command, server, or external dependency is accounted for.
- Remaining plan is ordered, starts with the exact next action, and each step has a completion criterion.
- Verification plan names exact commands or concrete manual checks.
- Risks, assumptions, and redactions are explicit.
- Resume prompt is ready to paste.

If any item fails, revise the packet.

## Final Response

Respond with:

1. The saved packet path.
2. The first recommended next action.
3. What verification you performed on the packet.

Keep the response short. The packet is the durable artifact.
