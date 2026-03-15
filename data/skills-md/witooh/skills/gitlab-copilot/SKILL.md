---
name: gitlab-copilot
description: Interact with GitLab via the glab CLI. Supports five MR workflows — Read (summarize), Review (full code/security/QA review), Fix (review + implement), CI Fix (fix pipeline failures), and Feedback (address review comments). Trigger whenever the user provides a GitLab MR URL or says anything like "อ่าน MR", "ดู MR", "check MR", "review MR", "ช่วย review MR นี้", "ตรวจ MR", "แก้ตาม MR", "fix MR", "fix CI", "fix pipeline", "แก้ pipeline", "แก้ตาม comment", "แก้ตาม feedback", "address feedback", or just pastes a GitLab MR URL. Also supports listing MRs, viewing MR status, checking CI/CD pipelines, approving MRs, and other glab operations. Trigger on "check pipeline", "list open MRs", "pipeline failed", or any GitLab-related task.
compatibility:
  environment: copilot-cli
  tools:
    - task
    - view
    - bash
    - skill
    - write_agent
    - read_agent
---

# GitLab Skill (Copilot CLI)

Use the `glab` CLI to interact with GitLab. Supports five MR workflows (Read → Review → Fix → CI Fix → Feedback) plus general glab operations.

## URL Parsing

When given a GitLab MR URL like `https://gitlab.com/group/subgroup/project/-/merge_requests/42`:

- **repo_ref**: strip `https://` and everything from `/-/` onward → `gitlab.com/group/subgroup/project`
- **mr_id**: extract the number after `merge_requests/` → `42`

These two values power most glab commands: `glab mr <cmd> <mr_id> --repo <repo_ref>`

## Intent Detection

When given a GitLab MR URL, determine the user's intent before selecting a workflow. There are five distinct workflows — **Read** is the lightest (just summarize), **Review** runs full specialist agents, **Fix** reviews then implements, **CI Fix** targets pipeline failures, and **Feedback** addresses reviewer comments. Default to Read when no strong signal indicates the user wants more.

| Signal in User Request | Workflow |
|------------------------|----------|
| "อ่าน", "ดู", "check", "สรุป", "summary", bare URL with no action verb | **MR Read** — fetch MR info + diff, then summarize. No specialist agents. |
| "review", "ตรวจ", "ช่วย review", "review ให้หน่อย" | **MR Review** — full code/security/QA review via 3 parallel specialist agents, post findings as comment |
| "แก้", "fix", "แก้ตาม", "แก้ issue", "implement", "ทำตาม" | **MR Fix** — review first, then auto-chain to /neo-team-copilot to implement fixes |
| "fix CI", "fix pipeline", "แก้ pipeline", "pipeline fail", "CI fail", "build fail" | **MR CI Fix** — fetch failed job logs, analyze, chain to /neo-team-copilot to fix |
| "address feedback", "แก้ตาม comment", "แก้ตาม feedback", "resolve threads", "ตอบ review" | **MR Feedback** — parse unresolved review threads, implement fixes, resolve |

**Decision rule:**
1. If the user's message mentions CI/pipeline failure → **MR CI Fix**
2. If the user's message mentions feedback/comments to address → **MR Feedback**
3. If the user's message contains a fix/แก้ keyword (not CI/feedback-specific) → **MR Fix**
4. If the user's message explicitly says "review" or "ตรวจ" → **MR Review**
5. Everything else (bare URL, "อ่าน", "ดู", "check", "สรุป", or ambiguous) → **MR Read** (lightest option, no side effects)

---

## Specialist Reference Files

This skill delegates review work to three specialist agents. Their detailed instructions live in the neo-team-copilot skill's reference files. Before spawning review agents, read these files with `view`:

| Specialist | Reference File |
|------------|---------------|
| Code Reviewer | `.agents/skills/neo-team-copilot/references/code-reviewer.md` |
| Security | `.agents/skills/neo-team-copilot/references/security.md` |
| QA | `.agents/skills/neo-team-copilot/references/qa.md` |

---

## MR Read Workflow

The lightest workflow — no specialist agents, no comments posted. Just fetch MR data and present a concise summary to the user in the conversation.

```
1. Fetch MR info (JSON) and diff
2. Summarize in conversation
```

### Step 1: Fetch

```bash
glab mr view <mr_id> --repo <repo_ref> --output json
glab mr diff <mr_id> --repo <repo_ref>
```

### Step 2: Summarize

Present a concise Thai summary covering:

- **MR metadata** — title, author, status, source → target branch, pipeline status
- **What changed** — brief description of the changes (group by area: features, refactoring, CI, docs, tests)
- **Files changed** — count and key files
- **Existing comments** — if there are review comments, briefly note them

Keep it terminal-friendly and scannable. Do NOT spawn specialist agents or post any comments on the MR.

---

## MR Review Workflow

When the user asks to review a MR (or intent is detected as "review"), run this pipeline:

```
1. Fetch MR info, diff, and existing comments
2. Read & summarize existing comments (understand what's already discussed)
3. code-reviewer + security + qa → review in PARALLEL (with comment context)
4. Compose Thai comment from template
5. Post comment to the MR
```

### Step 1: Fetch

```bash
glab mr view <mr_id> --repo <repo_ref> --output json
glab mr diff <mr_id> --repo <repo_ref>
glab mr note list <mr_id> --repo <repo_ref>
```

Extract from the view output: MR title, source branch, target branch, author.

### Step 2: Read Existing Comments

Before diving into the review, read through all existing MR comments/notes fetched in Step 1. This gives crucial context — other reviewers may have already flagged issues, the author may have explained design decisions, or there may be ongoing discussions that affect how you should review. Summarize the key points:

- Issues already raised by other reviewers
- Author's explanations or decisions
- Unresolved discussions that need attention
- Resolved items (avoid duplicating feedback)

This prevents the review from repeating what's already been said and helps focus on gaps that haven't been addressed yet.

### Step 3: Parallel Review

Read the project's `CLAUDE.md` if available (for conventions). Then read the three specialist reference files listed above, and spawn all three agents at the same time — including a summary of existing comments so reviewers have full context:

```
task(
  description: "Code review MR diff",
  agent_type: "general-purpose",
  model: "claude-opus-4.6",
  prompt: """
# Role: Code Reviewer
[paste full code-reviewer instructions from .agents/skills/neo-team-copilot/references/code-reviewer.md]

---
## Project Conventions
[relevant sections from CLAUDE.md if available, else omit]

---
## Existing MR Comments
[summary of existing comments from Step 2 — issues raised, author explanations, unresolved discussions]
Do NOT repeat issues that other reviewers have already flagged unless you have additional insight to add.

---
## Task
Review the following MR diff for convention compliance.

MR: !<mr_id> — <mr_title>
Branch: <source> → <target>

## Diff
<full diff output>
"""
)

task(
  description: "Security review MR diff",
  agent_type: "general-purpose",
  model: "claude-sonnet-4.6",
  prompt: """
# Role: Security Reviewer
[paste full security instructions from .agents/skills/neo-team-copilot/references/security.md]

---
## Existing MR Comments
[summary of existing comments from Step 2 — issues raised, author explanations, unresolved discussions]
Do NOT repeat security concerns that have already been raised unless you have additional findings.

---
## Task
Security review the following MR diff.

MR: !<mr_id> — <mr_title>
Branch: <source> → <target>

## Diff
<full diff output>
"""
)

task(
  description: "QA review MR diff",
  agent_type: "general-purpose",
  model: "claude-sonnet-4.6",
  prompt: """
# Role: QA Reviewer
[paste full QA instructions from .agents/skills/neo-team-copilot/references/qa.md]

---
## Project Conventions
[relevant sections from CLAUDE.md if available, else omit]

---
## Existing MR Comments
[summary of existing comments from Step 2 — issues raised, author explanations, unresolved discussions]
Do NOT repeat QA concerns that have already been raised unless you have additional findings.

---
## Task
QA review the following MR diff. Focus on:
- Test coverage gaps (are new code paths tested?)
- Missing edge case tests
- Regression risks
- Acceptance criteria validation (if available)

MR: !<mr_id> — <mr_title>
Branch: <source> → <target>

## Diff
<full diff output>
"""
)
```

> **💡 Multi-turn enhancement (v1.0.5+):** Spawn review agents with `mode: "background"` instead of default sync. If any agent's output needs clarification or deeper analysis, use `write_agent` to send follow-up messages — the agent retains full context from its initial review. Use `read_agent` to retrieve updated results.

### Step 4: Compose Thai comment

Read [references/mr-review-template.md](references/mr-review-template.md) and fill in findings from all three agents (code-reviewer, security, qa).

### Step 5: Post

```bash
glab mr note <mr_id> --repo <repo_ref> -m "<thai_comment>"
```

If `glab` is not authenticated or fails, output the review in the conversation instead and tell the user.

---

## MR Fix Workflow

When intent is detected as "fix" (user wants to fix issues from a MR), run review first then auto-chain to /neo-team-copilot for implementation.

```
1. Fetch MR info, diff, and existing comments          (same as MR Review Step 1)
2. Read & summarize existing comments                   (same as MR Review Step 2)
3. code-reviewer + security + qa → review in PARALLEL   (same as MR Review Step 3)
4. Compile findings into structured handoff context
5. Invoke /neo-team-copilot via skill tool with findings
6. Post summary comment on MR (after fix is done)
```

### Steps 1-3: Same as MR Review

Run the exact same fetch → read comments → parallel review pipeline. The only difference is what happens after.

**Important for MR Fix:** When composing the agent prompts in Step 3, add this instruction to each agent:

> Categorize every finding with a severity level: **Blocker**, **Critical**, **Warning**, or **Info**. Format each finding as: `[Severity] file:line — description`. This structured output is required for the handoff to the fix pipeline.

### Step 4: Compile Findings for Handoff

After all three review agents return, compile their findings into a structured context for /neo-team-copilot:

```
## MR Fix Context

**MR:** !<mr_id> — <mr_title>
**Branch:** <source_branch> → <target_branch>
**Repository:** <repo_ref>

### Review Findings

#### Code Review Findings
<code_reviewer_output — full findings with severity levels>

#### Security Findings
<security_output — full findings with severity levels>

#### QA Findings
<qa_output — full findings with severity levels>

### Severity Summary
| Level | Count |
|-------|-------|
| Blocker | X |
| Critical | X |
| Warning | X |
| Info | X |

### MR Diff
<full diff for reference>
```

Only proceed to Step 5 if there are **Blocker or Critical** findings. If all findings are Warning/Info only:
1. Post the review comment on the MR (using the MR Review template from Step 4-5 of the Review workflow)
2. Inform the user in the conversation: "ไม่พบ Blocker/Critical — findings ทั้งหมดเป็น Warning/Info เท่านั้น ไม่จำเป็นต้องแก้ไขเร่งด่วน"
3. **End the workflow here.** Do NOT invoke /neo-team-copilot. The user can manually request fixes if desired.

### Step 5: Invoke /neo-team-copilot

Use the `skill` tool to invoke /neo-team-copilot with the compiled findings:

```
skill(skill: "neo-team-copilot")

Then in the conversation, provide the task:

แก้ไขโค้ดตาม review findings จาก MR

<compiled findings from Step 4>

## Instructions
- Fix all Blocker and Critical findings
- Address Warning findings where practical
- Info findings are optional improvements
- The MR diff is provided for context — the code is already in the working directory
- After fixing, run existing tests to verify nothing is broken
```

/neo-team-copilot will classify this as a **Bug Fix** workflow internally and run:
1. system-analyzer → understand the codebase + findings
2. developer + qa + code-reviewer → implement fixes + test + verify (3-WAY PARALLEL)
3. Remediation if needed

### Step 6: Post Summary Comment

After /neo-team-copilot completes, post a summary comment on the MR:

```bash
glab mr note <mr_id> --repo <repo_ref> -m "<summary_comment>"
```

The comment should follow this format:

```
## 🤖 MR Fix Summary

**MR:** !<mr_id> — <mr_title>

### สิ่งที่แก้ไข
<list of fixes applied, mapped to original findings>

### สถานะ
- Blocker: X/Y แก้แล้ว
- Critical: X/Y แก้แล้ว
- Warning: X/Y แก้แล้ว

**ผลลัพธ์:** ✅ แก้ไขเสร็จ / ⚠️ แก้ไขบางส่วน (ดูรายละเอียดด้านบน)

---
*Fix โดย GitLab Skill + Neo Team · Copilot CLI*
```

---

## MR CI Fix Workflow

When the user wants to fix CI/pipeline failures for a MR, run this pipeline:

```
1. Fetch MR info and pipeline status
2. Identify failed jobs and fetch logs
3. Analyze failures and categorize
4. Chain to /neo-team-copilot to implement fixes
5. Push fix and optionally retry pipeline
```

### Step 1: Fetch MR + Pipeline Status

```bash
glab mr view <mr_id> --repo <repo_ref> --output json
glab ci list --repo <repo_ref> --branch <source_branch>
```

Extract MR metadata and identify the latest pipeline. If the MR URL wasn't provided but the user mentions a branch or "fix pipeline", use `glab ci status` to find the current pipeline.

### Step 2: Get Failed Job Logs

```bash
# List jobs in the failed pipeline:
glab ci view <pipeline_id> --repo <repo_ref>

# Fetch logs for each failed job:
glab ci trace <job_id> --repo <repo_ref>
```

Collect the last ~100 lines of each failed job's log output. These contain the actual error messages.

### Step 3: Analyze Failures

Categorize each failure:

| Category | Examples | Typical Fix |
|----------|----------|-------------|
| Build failure | Compilation errors, missing imports, type errors | Fix source code |
| Test failure | Unit/integration/E2E test failures | Fix code or update tests |
| Lint failure | Style violations, formatting issues | Run formatter, fix violations |
| Config failure | Docker build, missing env vars, bad CI config | Fix config files |

Present a summary to the user before proceeding:

```
## CI Failure Analysis

**Pipeline:** #<pipeline_id> — <status>
**Branch:** <source_branch>

### Failed Jobs
1. [Build] job-name — CompilationError: missing import "pkg/util"
2. [Test] test-unit — FAIL TestUserCreate: expected 200, got 500

Proceed to fix?
```

### Step 4: Invoke /neo-team-copilot

Use the `skill` tool to invoke /neo-team-copilot with failure context:

```
skill(skill: "neo-team-copilot")

Then in the conversation, provide the task:

แก้ไข CI/pipeline failures จาก MR

## CI Failure Context
**MR:** !<mr_id> — <mr_title>
**Branch:** <source_branch>
**Pipeline:** #<pipeline_id>

### Failed Jobs
<for each failed job:>
- **Job:** <job_name> (stage: <stage>)
- **Category:** <Build|Test|Lint|Config>
- **Error:** <relevant error excerpt from logs>
- **Log excerpt:**
  ```
  <last 30-50 lines of relevant log output>
  ```

## Instructions
- Fix all failing jobs
- Run the failing commands locally to verify fixes before pushing
- Do NOT change CI configuration unless the config itself is the problem
- If a test failure reveals a genuine bug, fix the code (not the test)
```

/neo-team-copilot will classify this as a **Bug Fix** workflow and route through system-analyzer → developer → verification agents.

### Step 5: Push and Retry

After /neo-team-copilot completes the fix:

```bash
# Push the fix to the MR branch
git push origin <source_branch>

# Optionally retry the pipeline
glab ci retry <pipeline_id> --repo <repo_ref>
```

Post a summary comment on the MR:

```bash
glab mr note <mr_id> --repo <repo_ref> -m "<summary>"
```

Summary format:

```
## 🤖 CI Fix Summary

**MR:** !<mr_id> — <mr_title>
**Pipeline:** #<pipeline_id>

### สิ่งที่แก้ไข
- ✅ [Build] job-name — fixed missing import
- ✅ [Test] test-unit — fixed handler returning wrong status code

### Pipeline
🔄 Retry triggered — pipeline #<new_pipeline_id>

---
*CI Fix โดย GitLab Skill + Neo Team · Copilot CLI*
```

---

## MR Feedback Workflow

When the user wants to address review feedback/comments on a MR, parse unresolved threads and implement fixes.

```
1. Fetch MR info, diff, and all comments/discussions
2. Filter and group unresolved feedback
3. Chain to /neo-team-copilot with structured feedback
4. Push fix, post summary, and resolve threads
```

### Step 1: Fetch

```bash
glab mr view <mr_id> --repo <repo_ref> --output json
glab mr diff <mr_id> --repo <repo_ref>
glab mr note list <mr_id> --repo <repo_ref>
```

### Step 2: Parse Unresolved Feedback

From the notes/comments, identify:
- **Actionable feedback** — explicit change requests ("fix this", "add error handling", "rename to X")
- **Suggestions** — optional improvements ("consider using...", "might be better to...")
- **Questions** — need user input before acting ("why did you choose X?", "should this handle Y?")

Group by file and classify:

```
### Unresolved Feedback

#### file: src/handler.go
1. @reviewer1: "Missing error handling on line 42" — Actionable
2. @reviewer2: "Consider using context.WithTimeout" — Suggestion

#### file: src/service.go
1. @reviewer1: "N+1 query in GetUsers" — Actionable

#### Questions (need user input)
1. @reviewer1: "Should this endpoint support pagination?"
```

**If there are questions**, present them to the user via `ask_user` before proceeding. The user's answers become part of the context for /neo-team-copilot.

### Step 3: Invoke /neo-team-copilot

```
skill(skill: "neo-team-copilot")

Then in the conversation, provide the task:

แก้ไขโค้ดตาม review feedback จาก MR

## Feedback Context
**MR:** !<mr_id> — <mr_title>
**Branch:** <source_branch> → <target_branch>

### Actionable Feedback
<list of actionable items with file, line, reviewer, and description>

### Suggestions
<list of suggestions — implement where practical>

### User Answers to Questions
<answers from Step 2, if any>

### MR Diff
<current diff for context>

## Instructions
- Address ALL actionable feedback items
- Implement suggestions where practical; explain in summary if skipped
- Run existing tests after changes
- Do not modify code unrelated to the feedback
```

### Step 4: Push, Post Summary, and Resolve

After fixes are applied:

```bash
git push origin <source_branch>
glab mr note <mr_id> --repo <repo_ref> -m "<summary>"
```

Summary format:

```
## 🤖 Feedback Addressed

**MR:** !<mr_id> — <mr_title>

### สิ่งที่แก้ไข
- ✅ src/handler.go:42 — เพิ่ม error handling ตาม @reviewer1
- ✅ src/service.go:15 — แก้ N+1 query ตาม @reviewer1
- ✅ src/handler.go:58 — ใช้ context.WithTimeout ตาม @reviewer2
- ⏭️ src/config.go:10 — skipped: ไม่เกี่ยวกับ scope ของ MR นี้

### ผลลัพธ์
- Actionable: X/Y แก้แล้ว
- Suggestions: X/Y implemented

---
*Feedback addressed โดย GitLab Skill + Neo Team · Copilot CLI*
```

---

## Common glab Operations

Use these directly via `bash` when the user asks for something other than a full review:

| Task | Command |
|------|---------|
| List open MRs | `glab mr list --repo <repo_ref>` |
| View MR details | `glab mr view <mr_id> --repo <repo_ref>` |
| Approve MR | `glab mr approve <mr_id> --repo <repo_ref>` |
| Check pipeline status | `glab ci status --repo <repo_ref>` |
| List pipelines | `glab ci list --repo <repo_ref>` |
| Retry a job | `glab ci retry <job_id> --repo <repo_ref>` |
| Add a note/comment | `glab mr note <mr_id> --repo <repo_ref> -m "<text>"` |

For `--repo`, you can omit it if you're already inside the project directory (glab detects the remote automatically).

## Error Handling

- **glab not authenticated**: tell the user to run `glab auth login`
- **glab command fails**: output the review as conversation text instead of posting, explain what failed
- **Empty diff**: note that the MR has no file changes and skip the review agents
- **Large diff (>500 lines)**: warn the user, proceed but note the review may miss details
- **Large single-line files** (minified JS, large JSON): the view tool now shows partial content — note this in the review if such files are part of the diff
