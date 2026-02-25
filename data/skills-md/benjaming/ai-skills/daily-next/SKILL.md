---
name: daily-next
description: Pick up the next task from today's daily task list and gather full context for working on it. This skill should be used when Benjamin says "next", "next task", "what's next", "pick up task", "start task", or wants context for a specific task ID or Jira key.
argument-hint: "[task-id or JIRA-KEY]"
disable-model-invocation: true
---

# Next — Pick Up Next Task

Load today's task list, select a task, gather deep context, mark it as in-progress, and present a structured briefing.

## Configuration

```yaml
jira:
  cloudId: "4a4bd20b-0645-4d11-9c98-8d0285630fd4"
  userId: "712020:30e7c6ae-4ea0-498a-b65d-c6107cba7e08"
  baseUrl: "https://hgdata.atlassian.net"

slack:
  supportChannel: "C09E1666N78"
  userId: "U09ATNQ9UV7"

persistence:
  tasksDir: "~/.claude/daily-tasks"
  standupsDir: "~/.claude/standups"
```

## Execution Steps

### 1. Load Task File

Read today's task file:

```bash
cat ~/.claude/daily-tasks/$(date +%Y-%m-%d).json 2>/dev/null
```

**If no file exists for today:**
- Check if a standup exists: `ls ~/.claude/standups/$(date +%Y-%m-%d).md 2>/dev/null`
- If standup exists but no task file: "Task file missing. Run `/daily-standup` to regenerate."
- If no standup either: "No standup for today. Run `/daily-standup` first."
- **Stop here.**

Parse the JSON. Display a compact status summary:

```
📋 Today's tasks: N total · N pending · N in_progress · N standby · N done
```

### 2. Select Task

**If `$ARGUMENTS` is a number:** select that task ID directly.

**If `$ARGUMENTS` matches a Jira key pattern** (e.g., `RGI-265`, `MITB-599`): find the task with matching `jira_key`.

**If `$ARGUMENTS` is empty:** select the first task with `status: "pending"`, scanning from id=1 upward. This respects tier priority since IDs are continuous across tiers (DO NOW items have lowest IDs). **Skip tasks with `status: "standby"` during auto-selection.**

**If the selected task has `status: "standby"`:** Warn and stop — do not allow picking up a standby task directly:
```
⏸️ Task #N ($KEY) is on standby. Waiting on: {waiting_on}
   Run /daily-unblock $N first to activate it, then /daily-next $N to pick it up.
```

**If a task is already `in_progress`:**
- Warn: "⚠️ Task #N (KEY) is already in progress."
- Ask whether to continue with the in-progress task, or switch to the requested one.

**If no pending tasks remain:** "All tasks done, in progress, or on standby. Run `/daily-done` to complete current task, `/daily-unblock` to activate a standby task, or `/daily-standup` to refresh."

### 3. Gather Deep Context

For the selected task, fetch comprehensive context based on its source type.

**3a. Jira context** (if task has a `jira_key`):

Fetch issue details, full comment history, and attachments in a single bash call:

```bash
mkdir -p /tmp/next-attachments
key="$JIRA_KEY"
echo "=== $key ==="
acli jira workitem view $key --json 2>&1 | jq '{key: .key, status: .fields.status.name, priority: .fields.priority.name, assignee: .fields.assignee.displayName, summary: .fields.summary, description: .fields.description, labels: .fields.labels, created: .fields.created, updated: .fields.updated}'
echo "--- comments ---"
acli jira workitem comment list --key $key --json 2>&1
echo "--- attachments ---"
acli jira workitem attachment list --key $key --json 2>&1
echo "--- links ---"
acli jira workitem view $key --json 2>&1 | jq '.fields.issuelinks'
```

**Download recent image attachments** (max 3, most recent first):
- For each image attachment (png, jpg, gif, webp) from the attachment list:

```bash
curl -L -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "https://hgdata.atlassian.net/rest/api/3/attachment/content/$ATTACHMENT_ID" \
  --output "/tmp/next-attachments/$KEY-$FILENAME"
```

- Use the **Read tool** to view each downloaded image (multimodal)
- If `$JIRA_EMAIL` or `$JIRA_API_TOKEN` are not set, skip attachment download and note: "Jira auth env vars not set — skipping attachment download."

**3b. Confluence context** (if Jira description or comments contain Confluence links):

Scan the issue description and comment bodies for Confluence page URLs matching `atlassian.net/wiki/spaces/*/pages/*`.

For each Confluence page found, extract the page ID from the URL and fetch it:

```
mcp__claude_ai_Atlassian__getConfluencePage with the page ID
```

Summarize relevant sections of each Confluence page in the briefing. Focus on information that helps understand or complete the task.

If the Atlassian MCP is not available, note: "Confluence content unavailable — MCP not connected."

**3c. Slack context** (search for related threads):

```
mcp__claude_ai_Slack__slack_search_public_and_private query: "$JIRA_KEY" limit: 5
```

If threads found mentioning this Jira key, summarize the most relevant discussion points. Focus on action items, decisions, and context not already captured in Jira comments.

If Slack MCP is not available, skip silently.

**3d. GitHub PR context** (if task has a `pr_url`):

Extract the repo and PR number from the `pr_url`, then:

```bash
gh pr view $PR_NUMBER --repo $REPO --json title,body,state,reviews,comments,reviewDecision,mergeable,statusCheckRollup,headRefName
```

Note: the PR URL format is typically `https://github.com/ORG/REPO/pull/NUMBER`.

### 4. Mark In-Progress

Read the current task file, update the selected task:
- Set `status` to `"in_progress"`
- Set `started_at` to current ISO timestamp (use `date -u +%Y-%m-%dT%H:%M:%SZ`)
- Update `updated_at` on the root object

Write the updated JSON back to the same file using the **Write tool**.

### 5. Present Briefing

Display a structured briefing:

```
┌─────────────────────────────────────────────────────────────┐
│  🎯 TASK #N — $JIRA_KEY                                     │
│  $SUMMARY                                                    │
│  Tier: $TIER · Priority: $PRIORITY · Jira Status: $STATUS    │
└─────────────────────────────────────────────────────────────┘

## Description
[Issue description from Jira, formatted for readability]

## Conversation Thread
[Chronological summary of ALL Jira comments — author, date, key points]
[Read the full thread to understand the conversation arc]

## Visual Evidence
[Description of screenshots/images viewed — what they show, what's relevant]

## Related
- PR: [#N](url) — review state, checks status
- Confluence: [Page Title](url) — brief summary of relevant content
- Slack: thread summary if found
- Linked Issues: [KEY](url) — relationship type, status

## Suggested Next Action
[Clear, actionable statement of what to do first — derived from the full context above]
```

Adapt the briefing based on available data. Omit sections with no content. The "Suggested Next Action" is the most important section — it should synthesize all context into a clear starting point.

### 6. Cleanup

```bash
rm -rf /tmp/next-attachments
```

## Edge Cases

- **Task file exists but is empty** (no tasks array): "Task list is empty. Re-run `/daily-standup`."
- **Selected task already `done`**: "Task #N is already done. Pick another or run `/daily-next` for the next pending task."
- **Selected task `skipped`**: Allow picking it up — set status back to `in_progress`.
- **Selected task `standby`**: Warn and stop. Tell user to `/daily-unblock N` first.
- **Jira API errors**: Show whatever context is available from the task file itself (`summary`, `context` fields), note that live data is unavailable.
- **Multiple tasks `in_progress`**: List all in-progress tasks, ask which to continue or whether to start a new one.
