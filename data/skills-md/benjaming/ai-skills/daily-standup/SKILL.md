---
name: daily-standup
description: Daily standup assistant for Benjamin that compiles work priorities from Jira and Slack into a single prioritized task list. This skill should be used when Benjamin asks for morning standup, daily priorities, what to work on today, or needs to compile work items.
disable-model-invocation: true
---

# Morning Standup

Compile Benjamin's personal actionable todo list for today from Jira, Slack, and GitHub.

**Key principle:** Every item in the output must represent something Benjamin personally needs to act on today. If a ticket is assigned to someone else, already resolved, or doesn't require Benjamin's action — exclude it.

## Configuration

```yaml
jira:
  cloudId: "4a4bd20b-0645-4d11-9c98-8d0285630fd4"
  userId: "712020:30e7c6ae-4ea0-498a-b65d-c6107cba7e08"
  baseUrl: "https://hgdata.atlassian.net/browse/"
  projects:
    - key: RGI
      board: 1236
    - key: MITB
      board: 1036
      label: Engineering-Applications

slack:
  supportChannel: "C09E1666N78"  # eng-applications-support
  userId: "U09ATNQ9UV7"  # Benjamin Gelis
  priorityUsers:
    - Claire Renaud
    - Matthieu Courtin

github:
  username: "BenjaminG"
  orgs:
    - MadKudu
    - HGData

persistence:
  directory: "~/.claude/standups"
  format: "YYYY-MM-DD.md"
```

## Execution Steps

### 1. Gather Slack Data

Query #eng-applications-support channel:

```
mcp__slack__conversations_history channel_id: "C09E1666N78" limit: "15"
```

From the results:
- When priority recaps contain multiple team sections (Applications, Data, Core, etc.), only extract items under the **Applications** section — that is Benjamin's team. Ignore Data, Core, and other sections.
- Note any unresolved @mentions of Benjamin (U09ATNQ9UV7)
- Note any questions or requests directed at Benjamin or his team that need a response
- Collect all Jira issue keys mentioned in Slack messages for validation in step 3

### 2. Gather Jira Data

**RGI Project** — All non-Done issues assigned to Benjamin:

```bash
acli jira workitem search --jql 'project = RGI AND assignee = "712020:30e7c6ae-4ea0-498a-b65d-c6107cba7e08" AND status not in (Done)' --fields "key,summary,status,priority" --csv
```

**MITB Project** — Only issues with Engineering-Applications label assigned to Benjamin:

```bash
acli jira workitem search --jql 'project = MITB AND assignee = "712020:30e7c6ae-4ea0-498a-b65d-c6107cba7e08" AND status not in (Done) AND labels = "Engineering-Applications"' --fields "key,summary,status,priority" --csv
```

**For each issue returned**, fetch details, full comments, and attachments to build comprehensive context.

**Important:** Fetch all issue data in a **single Bash call using a loop** rather than individual parallel calls, to avoid cascading failures when one call errors:

```bash
mkdir -p /tmp/standup-attachments
for key in KEY1 KEY2 KEY3; do
  echo "=== $key ==="
  acli jira workitem view $key --json 2>&1 | jq '{key: .key, status: .fields.status.name, priority: .fields.priority.name, assignee: .fields.assignee.displayName, summary: .fields.summary}'
  echo "--- comments ---"
  acli jira workitem comment list --key $key --json 2>&1
  echo "--- attachments ---"
  acli jira workitem attachment list --key $key --json 2>&1
  echo
done
```

**Processing attachments:** For issues that have image attachments (png, jpg, gif, webp), download the most recent 2-3 images per issue:

```bash
# For each image attachment found in the JSON output above:
curl -L -u "$JIRA_EMAIL:$JIRA_API_TOKEN" \
  "$JIRA_BASE_URL/rest/api/3/attachment/content/$ATTACHMENT_ID" \
  --output "/tmp/standup-attachments/$KEY-$FILENAME"
```

Then use the **Read tool** to view each downloaded image (Claude is multimodal and can read images). Screenshots often contain the actual QA feedback, bug reproductions, or UI states that explain what needs to happen next.

**Env vars required for attachment download:** `JIRA_EMAIL`, `JIRA_API_TOKEN`, `JIRA_BASE_URL`. If not set, skip attachment download and note it in the output.

From the full comments, attachments, and details, extract for each issue:
- **Full comment thread context:** Read ALL comments (not just the latest), understand the conversation arc — who raised what, what was discussed, what was decided
- **Visual context from screenshots:** If images are attached, view them and describe what they show (e.g., "Screenshot shows missing chart legend in conversion volume view")
- **Next action:** What Benjamin specifically needs to do next (review, fix, respond, deploy, etc.)
- **Whether actionable now** or waiting on someone else

**Cleanup:** After generating the standup report, remove temp files:
```bash
rm -rf /tmp/standup-attachments
```

### 3. Check Jira Notifications (Watched Issues)

Fetch recently updated issues Benjamin is watching — these surface activity on issues he cares about but may not be assigned to:

```bash
acli jira workitem search \
  --jql 'watcher = currentUser() AND updated >= -3d ORDER BY updated DESC' \
  --fields "key,summary,status,assignee" --csv
```

For each watched issue returned:
- **Skip issues already fetched in step 2** (assigned to Benjamin) — avoid duplicate work
- Fetch the last 3 comments to understand what changed:

```bash
acli jira workitem comment list --key <KEY> --json 2>&1 | jq -r '.comments[-3:] | .[] | "[\(.author.displayName)] \(.body)"'
```

From the results, determine if Benjamin needs to act:
- Someone asked Benjamin a question or requested input in the comments
- A status change requires Benjamin's attention (e.g., moved to review, blocked)
- A teammate's work that Benjamin needs to unblock or approve

**Filtering:** Only include watched issues where Benjamin has a concrete action item. Exclude purely informational updates (e.g., someone else resolved it, automated status transitions).

### 4. Gather GitHub Data

**Benjamin's open PRs across all repos:**

```bash
gh search prs --author=@me --state=open --limit 20 --json title,number,repository,url,isDraft,updatedAt,createdAt
```

**PRs requesting Benjamin's review:**

```bash
gh search prs --review-requested=@me --state=open --limit 10 --json title,number,repository,url,author
```

**Enrich with review state** — for each non-draft PR from Benjamin's list, fetch the review decision:

```bash
for pr in $(echo "$PRS_JSON" | jq -r '.[] | select(.isDraft == false) | "\(.repository.nameWithOwner):\(.number)"'); do
  repo="${pr%%:*}"
  num="${pr##*:}"
  echo "=== $repo#$num ==="
  gh pr view "$num" --repo "$repo" --json reviewDecision,reviews --jq '{reviewDecision, reviewCount: (.reviews | length)}'
done
```

Possible `reviewDecision` values:
- `CHANGES_REQUESTED` — a reviewer requested changes; Benjamin is blocking their wait
- `APPROVED` — all reviewers approved; ready to merge
- `REVIEW_REQUIRED` or empty (0 reviews) — no one has reviewed yet; Benjamin is waiting on others

From the results:
- Match PR titles/branches to Jira issue keys (e.g., a PR title containing "RGI-265" or branch named "feat/MITB-599")
- Note which of Benjamin's PRs are drafts vs ready for review
- Note PRs from teammates that need Benjamin's review
- Flag stale PRs (open > 30 days) — these likely need rebase, cleanup, or closing
- Note PR age using `createdAt` field
- **Classify each non-draft PR by review state for tier routing:**
  - `CHANGES_REQUESTED` → UNBLOCK OTHERS (reviewers waiting on Benjamin)
  - `REVIEW_REQUIRED` with 0 reviews → MONITORING footer (Benjamin is waiting, no action needed)
  - `APPROVED` → IN PROGRESS (ready to merge — Benjamin needs to act)

### 5. Validate Slack Items Against Jira

For every Jira issue key found in Slack messages (step 1) that was NOT already fetched in step 2, fetch the issue details, full comments, and attachments:

```bash
acli jira workitem view <ISSUE-KEY> --json
acli jira workitem comment list --key <ISSUE-KEY> --json
acli jira workitem attachment list --key <ISSUE-KEY> --json
```

Download and view image attachments the same way as step 2.

For each Slack-mentioned issue, determine:
- **Is it assigned to Benjamin?** If assigned to someone else, it's not Benjamin's action item.
- **Is it still open?** If status is Done/Resolved/Closed, exclude it entirely.
- **Does it require a response from Benjamin?** (e.g., someone asked him a question, requested a review, or awaits his input)
- **What is the current actual status?** Use comments and status to get the real state, not just what Slack says.

**Filtering rules:**
- Exclude issues assigned to others unless Benjamin has a specific pending action (reply, review, unblock)
- Exclude resolved/closed issues entirely
- Exclude issues where the Slack message is informational only (no action needed from Benjamin)

### 6. Load Previous Standup

Check for the most recent standup file in `~/.claude/standups/`:

```bash
ls -1 ~/.claude/standups/*.md 2>/dev/null | sort -r | head -1
```

If a previous standup exists, read it and extract:
- All Jira issue keys and their statuses (parse from section headers and item lines)
- All PR entries

This data is used in step 7 to generate the diff section. If no previous standup exists (first run), skip the diff.

To detect **stale** items, also check the 2 standups before that:

```bash
ls -1 ~/.claude/standups/*.md 2>/dev/null | sort -r | head -3
```

An item is stale if it appears with the same status across 3+ consecutive standups.

### 7. Merge and Prioritize

Build a single **priority-ordered numbered list** of Benjamin's personal action items, grouped into urgency tiers. Items are numbered continuously across all tiers (1, 2, 3... N — no resets between tiers).

When a Jira issue has a matching open PR (matched by issue key in PR title or branch), annotate the item inline with `⌥ PR #N` and link.

**Tier assignment rules:**

| Tier | Emoji | Criteria |
|------|-------|----------|
| ⚡ DO NOW | 💬 🔴 | Unresponded Slack @mentions; items reopened/escalated by priority users (Claire, Matthieu); Blocker/Urgent priority; items explicitly requested same-day |
| 🔄 UNBLOCK OTHERS | 🟡 | Own PRs with `CHANGES_REQUESTED` review decision (reviewers waiting on Benjamin); teammate PRs requesting Benjamin's review; watched issues where someone asked for input |
| 🔨 IN PROGRESS | 🟠 | Items with Jira status "In Progress" where Benjamin is actively working (not blocked, not waiting on others). PRs with `APPROVED` review decision ready to merge. |
| 📋 UP NEXT | 🔴 ⬜ | Ready for Development, On Deck items. Use 🔴 for High priority, ⬜ for normal |
| ⏳ WAITING | ⏸ | Tasks with `status === "standby"` from today's or yesterday's task file (carried over). Sort by `paused_at` ascending (longest-waiting first). These tasks are NOT shown in any other tier. |

**Monitoring (not a tier — compact footer section):**

Items Benjamin has handed off. These are NOT numbered and appear as a single compact footer line.

| Jira Status | Routes to MONITORING when... | Escalates back when... |
|-------------|------------------------------|----------------------|
| In QA | No comments mentioning Benjamin in last 24h | QA comment mentions Benjamin, or test failure needs dev fix |
| Ready For QA | No pending questions directed at Benjamin | Priority user asks about status |
| In Review | No review comments directed at Benjamin | Reviewer requests changes or asks question |
| Blocked by X | Blocker is NOT assigned to Benjamin | Blocker assigned to Benjamin or resolved |

Own PRs with `REVIEW_REQUIRED` / 0 reviews also route to MONITORING (not IN PROGRESS).

**Escalation check:** During step 7, for each item that would route to MONITORING, scan the issue's comments (already fetched in step 2) for:
1. Comments from the last 24 hours that @mention Benjamin or ask a direct question
2. Subtasks assigned to Benjamin that are not Done
3. The issue being reassigned back to Benjamin after being with QA/reviewer

If any escalation trigger fires, route the item to the appropriate action tier instead (see table above).

**Within each tier**, sort by: Jira priority (Blocker > Critical > High > Medium > Low), then by most recent activity.

### 8. Generate Output

Construct links for every issue key as `[KEY](https://hgdata.atlassian.net/browse/KEY)`.

**Format — Priority Stack:**

```
┌─────────────────────────────────────────────────────────────┐
│  🌅  STANDUP — {date}                                       │
│  Last sync: {previous_date} · {N} action · {N} monitoring · {N} standby · {N} msg│
└─────────────────────────────────────────────────────────────┘

⚡ DO NOW
  1. 💬 [Brief description] — [who] [what]
     └─ #channel · date · What to respond
  2. 🔴 [KEY](url) — Summary
     └─ Context from comments/attachments → next action

🔄 UNBLOCK OTHERS
  3. 🟡 [KEY](url) — Summary                     ⌥ [PR #N](gh-url)
     └─ Feedback details / what to address
  4. 🟡 [repo#N](gh-url) — PR title — by [author]
     └─ Brief description of PR purpose

🔨 IN PROGRESS
  5. 🟠 [KEY](url) — Summary                     ⌥ [PR #N](gh-url)
     └─ Active work context / ready to merge

📋 UP NEXT
  6. 🔴 [KEY](url) — Summary                    High
     └─ Why it matters
  7. ⬜ [KEY](url) — Summary
     └─ Brief context

⏳ WAITING
  8. ⏸ [KEY](url) — Summary
     └─ Waiting on: {waiting_on} · standby Xh ago
  9. ⏸ [KEY](url) — Summary
     └─ Waiting on: {waiting_on} · standby 1d ago

╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌
🔔 Overnight: 🆕 KEY reason · ➡️ KEY old → new · ✅ KEY done · ⏸ KEY reason · ▶️ KEY
╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌

👀 Monitoring: KEY (brief) · KEY ⌥#N (brief) · KEY (brief) ...
🔍 Analysis: KEY (brief) · KEY (brief)
📦 Backlog: KEY (brief) · KEY (brief)
🧹 Stale PRs: #N(Nd) #N(Nd) ...
```

**Header box rules:**
- `{N} action` = count of items in DO NOW + UNBLOCK OTHERS + IN PROGRESS + UP NEXT (things requiring Benjamin's involvement)
- `{N} monitoring` = count of items in the MONITORING footer (handed off, no action needed)
- `{N} standby` = count of items in WAITING tier
- `{N} msg` = pending Slack messages
- `Last sync: {date}` uses the most recent previous standup date. Omit if first standup.
- Omit `{N} standby` from the header if zero standby tasks. Omit `{N} monitoring` if zero.

**Context line (`└─`) rules:**
- Every item MUST have a `└─` context line underneath
- The line should answer: "What do I need to do with this?"
- Derive context from the **full comment thread** + **attachments** + PR status + Slack messages — not from the issue title or a single comment
- Read ALL comments on each issue to understand the full conversation arc before summarizing
- If image attachments exist, view them and incorporate visual context (e.g., "Screenshot shows missing chart legend on conversion page")
- Keep to 1-2 lines, ~20 words max
- For Jira items: synthesize the full discussion + visual evidence into a clear next action for Benjamin
- For PRs: note age, review status, whether it needs rebase/cleanup
- For stale PRs (> 30 days): flag explicitly (e.g., "Open 45 days, likely needs rebase or closing")
- Use ⏸ prefix when an item is blocked/waiting on someone else

**PR annotation rules:**
- If a Jira item has a matching PR, append `⌥ [PR #N](gh-url)` inline on the same line
- Mark draft PRs explicitly with "(draft)"
- **Route Benjamin's PRs by review state:**
  - `CHANGES_REQUESTED` → 🔄 UNBLOCK OTHERS (reviewers waiting on Benjamin to address feedback)
  - `REVIEW_REQUIRED` / 0 reviews → 👀 MONITORING footer (Benjamin is waiting, no action needed)
  - `APPROVED` but not merged → 🔨 IN PROGRESS (ready to merge — Benjamin needs to act)
- Teammate PRs requesting Benjamin's review go in the 🔄 UNBLOCK OTHERS tier
- Benjamin's open PRs that don't match any Jira issue go in the 🧹 Stale PRs footer line

**Overnight diff rules:**
- Compact single-line format between `╌` dividers
- Use emoji prefixes: 🆕 (new items), ➡️ (status changes), ✅ (completed/resolved), ⚠️ (stale 3+ standups), ⏸ (newly on standby), ▶️ (unblocked since last standup)
- All changes on one line, separated by ` · `
- Compare by Jira issue key and status from previous standup file
- **Completed** = keys in previous standup but absent from today's data
- **New** = keys in today's data but absent from previous standup
- **Status Changes** = keys present in both with different status
- **Stale** = keys with identical status across 3+ consecutive standups
- **Newly standby** = keys that transitioned to `standby` since last standup — show as `⏸ KEY reason`
- **Unblocked** = keys that transitioned from `standby` to active since last standup — show as `▶️ KEY`
- Omit the entire overnight section if no previous standup exists

**Footer section rules:**
- 👀 Monitoring, 🔍 Analysis, 📦 Backlog, 🧹 Stale PRs are compact single-line lists
- Format: `emoji Label: KEY (brief) · KEY (brief)`
- **Monitoring line format:** `👀 Monitoring: KEY (brief status) · KEY ⌥#N (brief) · ...`
  - Each entry: issue key, optional `⌥#N` for linked PR, parenthetical status (~15 chars max)
  - Sort: In Review → In QA → Ready For QA (closest to done first)
  - If > 8 items: show first 6 + `+N more`
- Stale PRs use `#N(Nd)` format showing PR number and age in days
- Omit any footer line with no items

**Tier omission:** Omit any tier that has no items. Do not show empty tier headers.

### 9. Persist Report

After displaying the output, save the full standup report:

```bash
mkdir -p ~/.claude/standups
```

Write the complete output to `~/.claude/standups/YYYY-MM-DD.md` (using today's date).

If a file for today already exists (e.g., re-running standup), overwrite it with the latest data.

### 10. Generate Task File

After persisting the standup report, generate a structured task file for cross-session tracking.

**Create `~/.claude/daily-tasks/YYYY-MM-DD.json`** by extracting each numbered item from the standup output:

```bash
mkdir -p ~/.claude/daily-tasks
```

**Extraction rules — parse the standup output just generated:**

1. For each numbered item (1..N), extract:
   - Item number → `id`
   - Tier header above it → `tier` (map: `⚡ DO NOW` → `"do_now"`, `🔄 UNBLOCK OTHERS` → `"unblock_others"`, `🔨 IN PROGRESS` → `"in_progress"`, `📋 UP NEXT` → `"up_next"`, `👀 Monitoring` footer → `"monitoring"`)
   - Jira key from `[KEY](url)` pattern → `jira_key`, `jira_url`
   - Summary text after the em dash → `summary`
   - Context line (the `└─` line) → `context`
   - PR annotation `⌥ [PR #N](url)` → `pr_url`
   - Source: items with `jira_key` → `"jira"`, Slack-only items → `"slack"`, PR-only items → `"github"`

2. Items without a Jira key (e.g., Slack @mentions, PR review requests) should still be included with `jira_key: null`.

3. For monitoring items (from the `👀 Monitoring:` footer line): parse the line, split by ` · `, and create task entries with `tier: "monitoring"`. The `context` field gets the parenthetical text. The `summary` comes from the Jira data already fetched in step 2.

**JSON schema:**

```json
{
  "date": "YYYY-MM-DD",
  "standup_file": "~/.claude/standups/YYYY-MM-DD.md",
  "updated_at": "ISO-TIMESTAMP",
  "tasks": [
    {
      "id": 1,
      "tier": "do_now",
      "status": "pending",
      "jira_key": "RGI-265",
      "jira_url": "https://hgdata.atlassian.net/browse/RGI-265",
      "summary": "Migrate Evr Insights pages",
      "context": "In QA; Claire feedback on missing chart names",
      "pr_url": null,
      "source": "jira",
      "started_at": null,
      "completed_at": null,
      "carried_from": null,
      "waiting_on": null,
      "paused_at": null
    }
  ]
}
```

**Merge logic — if `~/.claude/daily-tasks/YYYY-MM-DD.json` already exists (re-run):**

1. Read the existing task file
2. Build a lookup map: `jira_key → {status, started_at, completed_at, waiting_on, paused_at}` for all existing tasks
3. For each new task being generated: if its `jira_key` matches an existing task, carry over `status`, `started_at`, `completed_at`, `waiting_on`, `paused_at` from the existing entry
4. Tasks with `status === "standby"` are routed to the `⏳ WAITING` tier regardless of what Jira reports for their status
5. This prevents losing in-progress/done/standby state when re-running standup mid-day

**Carry-over from previous day:**

Check if yesterday's task file exists:
```bash
cat ~/.claude/daily-tasks/$(date -v-1d +%Y-%m-%d).json 2>/dev/null
```

For tasks that appeared in yesterday's file and reappear today (matched by `jira_key`):
- Set `carried_from` to yesterday's date string
- If yesterday's task had `status === "standby"`, carry over `standby` status, `waiting_on`, and `paused_at` intact — the task is still blocked

Write the JSON file using the **Write tool** to `~/.claude/daily-tasks/YYYY-MM-DD.json`.

**Amend standup file:** After writing the task file, append an HTML comment reference to the standup markdown file:

```
<!-- task-file: ~/.claude/daily-tasks/YYYY-MM-DD.json -->
```

### 11. Empty State

If no tasks found across all sources:
```
No pending tasks - check backlog or ask PM for priorities.
```

Still persist the empty standup file so the diff tracks that it was a clean day. Also persist an empty task file with `"tasks": []`.

## Notes

- Both RGI (1236) and MITB (1036) boards are Kanban (no sprints). Use status to infer tier placement.
- Exclude Canceled and Done issues from output
- Omit any tier or footer line that has no items
- Use 🔴 emoji for High priority items (not bold text)
- Requirement Analysis and Backlog items go in the compact footer lines, not in the numbered tiers
- Blockers should be surfaced as 🔴 items in the ⚡ DO NOW tier with clear blocking context
