---
name: ship
description: "Ship changes through the full PR lifecycle. Use after completing feature work to commit, push, create PR, wait for checks, and merge. Handles the entire workflow: syncs with main, creates feature branch if needed, groups commits logically with semantic messages, creates detailed PR, monitors CI, fixes issues, squash merges, and cleans up. Invoke when work is ready to ship."
argument-hint: --pr-only, --no-squash, --keep-branch (optional flags)
allowed-tools: Bash, Read, Glob, Grep, Agent, Skill
---

# Ship - Full PR Lifecycle

When this skill is invoked, IMMEDIATELY output the banner below before doing anything else.
Pick ONE tagline at random — vary your choice each time.
CRITICAL: Reproduce the banner EXACTLY character-for-character. The first line of the art has 4 leading spaces — you MUST preserve them.

```
{tagline}

⠀   ██╗███████╗██╗  ██╗██╗██████╗
   ██╔╝██╔════╝██║  ██║██║██╔══██╗
  ██╔╝ ███████╗███████║██║██████╔╝
 ██╔╝  ╚════██║██╔══██║██║██╔═══╝
██╔╝   ███████║██║  ██║██║██║
╚═╝    ╚══════╝╚═╝  ╚═╝╚═╝╚═╝
```

Taglines:
- 🚚 Special delivery!!!
- 📦 If it compiles, it ships!
- 🚢 Anchors aweigh!
- 🙏 git push and pray!
- ⚡ Shipping faster than Amazon Prime!
- 🏀 Yeet the code into production!
- 📬 Another one for the merge queue!
- 🟢 LGTM — Let's Get This Merged!

---

## Output Formatting

After the banner, display parsed input:
```
┌─ Input ────────────────────────────────────────
│  {Field}:  {value}
│  Flags:    {parsed flags or "none"}
└────────────────────────────────────────────────
```

Pre-flight results:
```
── Pre-flight ───────────────────────────────────
  ✅ {dep}           {version or "found"}
  ⚠️ {dep}           not found → {fallback detail}
  ❌ {dep}           missing → stopping
──────────────────────────────────────────────────
```

Stage/phase headers: `━━ {N} · {Name} ━━━━━━━━━━━━━━━━━━━━━━━━━`

Status icons: ✅ done · ❌ failed · ⚠️ degraded · ⏳ working · ⏭️ skipped

---

Ship changes through the complete PR lifecycle. Every stage runs in a subagent
to isolate context from the primary conversation. Prompts for each stage are
in `references/stage-prompts.md`.

## Flags

Parse optional flags from the request:
- `--pr-only`: Stop after creating the PR
- `--no-squash`: Use regular merge instead of squash
- `--keep-branch`: Don't delete the source branch after merge

---

## Pre-flight

Before starting, check all dependencies in this table:

| Dependency | Type | Check | Required | Resolution | Detail |
|-----------|------|-------|----------|------------|--------|
| git | cli | `git --version` | yes | stop | Install from https://git-scm.com |
| gh | cli | `gh --version` | yes | url | https://cli.github.com |
| ship-analyzer | agent | `~/.claude/agents/ship-analyzer.md` | no | fallback | Uses general-purpose agent |

For each row, in order:
1. Run the Check command (for cli/npm) or test file existence (for agent/skill)
2. If found: continue silently
3. If missing: apply Resolution strategy
   - **stop**: notify user with Detail, halt execution
   - **url**: notify user with Detail (install link), halt execution
   - **install**: notify user, run the command in Detail, continue if successful
   - **ask**: notify user, offer to run command in Detail, continue either way (or halt if required)
   - **fallback**: notify user with Detail, continue with degraded behavior
4. After all checks: summarize what's available and what's degraded

Read `default_branch` and `remote` from Stage 1's SYNC_REPORT. These are
substituted into all stage prompts as `{REMOTE}` and `{DEFAULT_BRANCH}`.

### Platform Detection

After sync, detect the hosting platform from the remote URL:

```bash
REMOTE_URL=$(git remote get-url {REMOTE} 2>/dev/null)
if echo "$REMOTE_URL" | grep -qiE 'dev\.azure\.com|visualstudio\.com'; then
  PLATFORM="azdo"
elif echo "$REMOTE_URL" | grep -qi 'github\.com'; then
  PLATFORM="github"
else
  PLATFORM="github"   # default fallback
fi
```

Pass `{PLATFORM}` into all stage prompts. Each stage uses the appropriate
CLI tool: `gh` for GitHub, `az repos`/`az pipelines` for Azure DevOps.

> **Azure DevOps prerequisite:** The `az devops` extension must be installed
> and configured (`az devops configure --defaults organization=... project=...`).
> If `az repos` commands fail, report the setup requirement to the user.

---

## Stage 1: Sync

Launch **Bash subagent** (haiku — simple git commands):

```
Task(
  subagent_type: "Bash",
  model: "haiku",
  description: "Sync with default branch",
  prompt: "Follow ~/.claude/skills/sync/SKILL.md subagent prompt. Return SYNC_REPORT."
)
```

Parse SYNC_REPORT. Extract `remote` and `default_branch`. Abort if sync failed.

---

## Stage 2: Commit, Push & Create PR

This stage needs to **read and understand code** to write good commit messages
and PR descriptions. Use a code-aware subagent.

Launch **ship-analyzer subagent** (reads diffs + source files):

```
Task(
  subagent_type: "ship-analyzer",
  description: "Analyze, commit, push, and create PR",
  prompt: <read from references/stage-prompts.md#stage-2>
)
```

> **Fallback:** If `ship-analyzer` is not available, use `subagent_type: "general-purpose"`.

Substitute `{USER_INTENT}`, `{FILES_TO_INCLUDE}`, `{FILES_TO_EXCLUDE}`,
`{REMOTE}`, `{DEFAULT_BRANCH}`, `{PLATFORM}` into the prompt.

Parse SHIP_REPORT. Abort if failed.

**Rollback:** If push succeeds but PR creation fails, report the error and
suggest the manual PR creation command. Do NOT revert the push.
- GitHub: `gh pr create --head {branch}`
- Azure DevOps: `az repos pr create --source-branch {branch} --target-branch {DEFAULT_BRANCH}`

**If `--pr-only` flag: Stop here and report PR URL to user.**

---

## Stage 3: Wait for CI

Launch **Bash subagent** in the **background** (haiku — just polling):

```
Task(
  subagent_type: "Bash",
  model: "haiku",
  run_in_background: true,
  description: "Monitor CI checks",
  prompt: <read from references/stage-prompts.md#stage-3>
)
```

Substitute `{PR_NUMBER}` into the prompt.

While CI runs in the background, briefly inform the user:
```
CI running for PR #{pr_number}... waiting for checks.
```

When the background task completes, read the output file and parse CHECKS_REPORT.

---

## Stage 4: Fix Failing Checks (if needed)

If CHECKS_REPORT shows failures, launch **general-purpose subagent**:

```
Task(
  subagent_type: "general-purpose",
  description: "Fix CI failures",
  prompt: <read from references/stage-prompts.md#stage-4>
)
```

Substitute `{PR_NUMBER}`, `{BRANCH}`, `{FAILING_CHECKS}` into the prompt.

If fixed, return to Stage 3 (run CI watch again).
If unable to fix after 2 attempts, report to user and stop.

---

## Stage 5: Merge & Final Sync

Launch **Bash subagent** (haiku — simple git + platform CLI commands):

```
Task(
  subagent_type: "Bash",
  model: "haiku",
  description: "Merge PR and sync",
  prompt: <read from references/stage-prompts.md#stage-5>
)
```

Substitute `{PR_NUMBER}`, `{REMOTE}`, `{DEFAULT_BRANCH}`, merge/branch flags.

Parse LAND_REPORT.

---

## Final Report to User

Compile all stage reports into a summary:

```
┌─ Ship · Report ────────────────────────────────
│
│  ✅ Ship complete
│
│  🌿 Branch:  {branch}
│  🔗 PR:      {pr_url}
│  🔀 Merged:  {merge_commit} ({merge_type})
│
│  📝 Commits
│     • {commit message 1}
│     • {commit message 2}
│
│  📊 {count} files changed ({diff_summary})
│
└─────────────────────────────────────────────────
```

If any stage failed, add:
```
│  ❌ Failed at: {stage name}
│     {error description}
│     {suggested resolution}
```
