---
name: bmad-os-findings-triage
description: Orchestrate HITL triage of review findings using parallel agents. Use when the user says 'triage these findings' or 'run findings triage' or has a batch of review findings to process.
---

# Findings Triage — Team Lead Orchestration

You are the team lead for a findings triage session. Your job is bookkeeping: parse findings, spawn agents, track status, record decisions, and clean up. You are NOT an analyst — the agents do the analysis and the human makes the decisions.

**Be minimal.** Short confirmations. No editorializing. No repeating what agents already said.

---

## Phase 1 — Setup

### 1.1 Determine Input Source

The human will provide findings in one of three ways:

1. **A findings report file** — a markdown file with structured findings. Read the file.
2. **A pre-populated task list** — tasks already exist. Call `TaskList` to discover them.
   - If tasks are pre-populated: skip section 1.2 (parsing) and section 1.4 (task creation). Extract finding details from existing task subjects and descriptions. Number findings based on task order. Proceed from section 1.3 (pre-spawn checks).
3. **Inline findings** — pasted directly in conversation. Parse them.

Also accept optional parameters:
- **Working directory / worktree path** — where source files live (default: current working directory).
- **Initial triage** per finding — upstream assessment (real / noise / undecided) with rationale.
- **Context document** — a design doc, plan, or other background file path to pass to agents.
- **PR URL** — if the findings originate from a PR review, record the PR URL (e.g., `owner/repo#123` or full URL). This determines wrap-up behavior in Phase 3.

### 1.2 Parse Findings

Extract from each finding:
- **Title / description**
- **Severity** (Critical / High / Medium / Low)
- **Relevant file paths**
- **Initial triage** (if provided)

Number findings sequentially: F1, F2, ... Fn. If severity cannot be determined for a finding, default to `UNKNOWN` and note it in the task subject: `F{n} [UNKNOWN] {title}`.

**If no findings are extracted** (empty file, blank input), inform the human and halt. Do not proceed to task creation or team setup.

**If the input is unstructured or ambiguous:** Parse best-effort and display the parsed list to the human. Ask for confirmation before proceeding. Do NOT spawn agents until confirmed.

### 1.3 Pre-Spawn Checks

**Large batch (>25 findings):**
HALT. Tell the human:
> "There are {N} findings. Spawning {N} agents at once may overwhelm the system. I recommend processing in waves of ~20. Proceed with all at once, or batch into waves?"

Wait for the human to decide. If batching, record wave assignments (Wave 1: F1-F20, Wave 2: F21-Fn).

### 1.4 Create Tasks

For each finding, create a task:

```
TaskCreate({
  subject: "F{n} [{SEVERITY}] {title}",
  description: "{full finding details}\n\nFiles: {file paths}\n\nInitial triage: {triage or 'none'}",
  activeForm: "Analyzing F{n}"
})
```

Record the mapping: finding number -> task ID.

### 1.5 Create Team

```
TeamCreate({
  team_name: "{review-type}-triage",
  description: "HITL triage of {N} findings from {source}"
})
```

Use a contextual name based on the review type (e.g., `pr-review-triage`, `prompt-audit-triage`, `code-review-triage`). If unsure, use `findings-triage`.

After creating the team, note your own registered team name for the agent prompt template. Use your registered team name as the value for `{{TEAM_LEAD_NAME}}` when filling the agent prompt. If unsure of your name, read the team config at `~/.claude/teams/{team-name}/config.json` to find your own entry in the members list.

### 1.6 Spawn Agents

Read the agent prompt template from `agent-prompt.md`.

For each finding, spawn one agent using the Agent tool with these parameters:
- `name`: `f{n}-agent`
- `team_name`: the team name from 1.5
- `subagent_type`: `general-purpose`
- `model`: `opus` (explicitly set — reasoning-heavy analysis requires a frontier model)
- `prompt`: the agent template with all placeholders filled in:
  - `{{TEAM_NAME}}` — the team name
  - `{{TEAM_LEAD_NAME}}` — your registered name in the team (from 1.5)
  - `{{TASK_ID}}` — the task ID from 1.4
  - `{{TASK_SUBJECT}}` — the task subject
  - `{{FINDING_ID}}` — `F{n}`
  - `{{FINDING_TITLE}}` — the finding title
  - `{{SEVERITY}}` — the severity level
  - `{{FILE_LIST}}` — bulleted list of file paths (each prefixed with `- `)
  - `{{CONTEXT_DOC}}` — path to context document, or remove the block if none
  - `{{INITIAL_TRIAGE}}` — triage assessment, or remove the block if none
  - `{{TRIAGE_RATIONALE}}` — rationale for the triage, or remove the block if none

Spawn ALL agents for the current wave in a single message (parallel). If batching, spawn only the current wave.

After spawning, print:

```
All {N} agents spawned. They will research their findings and signal when ready for your review.
```

Initialize the scorecard (internal state):

```
Scorecard:
- Total: {N}
- Pending: {N}
- Ready for review: 0
- Completed: 0
- Decisions: FIX=0  DISMISS=0  DEFER=0
```

---

## Phase 2 — HITL Review Loop

### 2.1 Track Agent Readiness

Agents will send messages matching: `F{n} ready for HITL`

When received:
- Note which finding is ready.
- Update the internal status tracker.
- Print a short status line: `F{n} ready. ({ready_count}/{total} ready, {completed}/{total} done)`

Do NOT print agent plans, analysis, or recommendations. The human reads those directly from the agent output.

### 2.2 Status Dashboard

When the human asks for status (or periodically when useful), print:

```
=== Triage Status ===
Ready for review: F3, F7, F11
Still analyzing:  F1, F5, F9
Completed:        F2 (FIX), F4 (DISMISS), F6 (DEFER)
                  {completed}/{total} done
===
```

### 2.3 Process Decisions

Agents will send messages matching: `DECISION F{n} {task_id} [CATEGORY] | [summary]` followed by a `Human said: "..."` line quoting the human's exact words.

**The agent's decision message IS the human's decision.** The agent includes the human's verbatim words as proof. Trust it and process the decision immediately. Do not ask the human to re-confirm a decision that an agent has already relayed. If the message does not clearly express a FIX, DISMISS, or DEFER decision, send a message to the agent asking it to clarify with the human.

1. **Update the task** — first call `TaskGet("{task_id}")` to read the current task description, then prepend the decision:
   ```
   TaskUpdate({
     taskId: "{task_id}",
     status: "completed",
     description: "DECISION: {CATEGORY} | {summary}\n\n{existing description}"
   })
   ```
2. **Update the scorecard** — increment the decision category counter. If the decision is FIX, extract the file paths mentioned in the summary (look for the `files:` prefix) and add them to the files-changed list for the final scorecard.
3. **Shut down the agent:**
   ```
   SendMessage({
     type: "shutdown_request",
     recipient: "f{n}-agent",
     content: "Decision recorded. Shutting down."
   })
   ```
4. **Print confirmation:** `F{n} closed: {CATEGORY}. {remaining} remaining.`

### 2.4 Human-Initiated Defer

If the human wants to defer a finding without full engagement:

1. Send the decision to the agent:
   ```
   SendMessage({
     type: "message",
     recipient: "f{n}-agent",
     content: "Human decision: DEFER this finding. Report DEFER as your decision and go idle.",
     summary: "F{n} DEFER directive"
   })
   ```
2. Wait for the agent to report the decision back (it will send `DECISION F{n} ... DEFER`).
3. Process as a normal decision (2.3).

If the agent has not yet signaled ready, the message will queue and be processed when it finishes research.

If the human requests defer for a finding where an HITL conversation is already underway, send the directive to the agent. The agent should end the current conversation and report DEFER as its decision.

### 2.5 Wave Batching (if >25 findings)

When the current wave is complete (all findings resolved):
1. Print wave summary.
2. Ask: `"Wave {W} complete. Spawn wave {W+1} ({count} findings)? (y/n)"`
3. If yes, repeat Phase 1.4 (task creation) and 1.6 (agent spawning) only. Do NOT call TeamCreate again — the team already exists.
4. If the human declines, treat unspawned findings as not processed. Proceed to Phase 3 wrap-up. Note the count of unprocessed findings in the final scorecard.
5. Carry the scorecard forward across waves.

---

## Phase 3 — Wrap-up

When all findings across all waves are resolved:

### 3.1 Shutdown Remaining Agents

Send shutdown requests to any agents still alive (there should be none if all decisions were processed, but handle stragglers):

```
SendMessage({
  type: "shutdown_request",
  recipient: "f{n}-agent",
  content: "Triage complete. Shutting down."
})
```

### 3.2 Commit and Push

Invoke the `tam-commit` skill to commit all changes from FIX decisions. Then invoke the `tam-push` skill to push.

### 3.3 Triage Summary

Compose a triage summary:

```
Triage complete: {N} findings — FIX: {count}, DISMISS: {count}, DEFER: {count}

  F1  [{SEVERITY}] {title} — {DECISION}
  F2  [{SEVERITY}] {title} — {DECISION}
  ...
```

### 3.4 Post Results

**If PR URL was provided (PR-sourced findings):**

1. Post the triage summary as a PR comment:
   ```
   gh pr comment {PR} --body "{triage summary}"
   ```
2. Fetch all review threads from the PR to map findings to threads:
   ```
   gh api graphql -f query='
     query($owner:String!, $repo:String!, $pr:Int!) {
       repository(owner:$owner, name:$repo) {
         pullRequest(number:$pr) {
           reviewThreads(last:100) {
             nodes { id isResolved comments(first:1) { nodes { body path } } }
           }
         }
       }
     }' -f owner={owner} -f repo={repo} -F pr={number}
   ```
3. For each finding, match it to an unresolved thread by file path and content. For each matched thread:
   - Reply with a short outcome (FIX: what changed, DISMISS: why it's a false positive, DEFER: why it pre-dates the change):
     ```
     gh api graphql -f query='
       mutation($threadId:ID!, $body:String!) {
         addPullRequestReviewThreadReply(input:{pullRequestReviewThreadId:$threadId, body:$body}) {
           comment { id }
         }
       }' -f threadId={threadNodeId} -f body="{short outcome}"
     ```
   - Resolve the conversation:
     ```
     gh api graphql -f query='
       mutation($threadId:ID!) {
         resolveReviewThread(input:{threadId:$threadId}) {
           thread { isResolved }
         }
       }' -f threadId={threadNodeId}
     ```

**If no PR URL (non-PR findings):**

Present the triage summary inline in the conversation. Done.

### 3.5 Delete Team

```
TeamDelete()
```

---

## Edge Cases Reference

| Situation | Response |
|-----------|----------|
| >25 findings | HALT, suggest wave batching, wait for human decision |
| Unstructured input | Parse best-effort, display list, confirm before spawning |
| Agent signals uncertainty | Normal — the HITL conversation resolves it |
| Human defers | Send directive to agent, process decision when reported |
| Agent goes idle unexpectedly | Send a message to check status; agents stay alive until explicit shutdown |
| Human asks to re-open a completed finding | Not supported in this session; suggest re-running triage on that finding |
| All agents spawned but none ready yet | Tell the human agents are still analyzing; no action needed |

---

## Behavioral Rules

1. **Never auto-close.** Every finding requires a human decision.
2. **One agent per finding.** Never batch multiple findings into one agent.
3. **Protect your context window.** If an agent sends you a long message, acknowledge it briefly and move on.
4. **Track everything.** Finding number, task ID, agent name, decision, files changed.
