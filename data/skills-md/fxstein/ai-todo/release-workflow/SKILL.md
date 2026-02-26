---
name: release-workflow
description: Guides release preparation and execution for ai-todo. Use when the user asks to 'prepare release', 'execute release', 'release', or mentions creating a new version.
---

# Release Workflow for ai-todo

## Quick Reference

- **Prepare:** `./release/release.sh --prepare [--beta] [--set-version X.Y.Z] --summary release/AI_RELEASE_SUMMARY.md`
- **Dry Run:** `./release/release.sh --prepare --dry-run` (preview without committing)
- **Execute:** `./release/release.sh --execute`
- **Abort:** `./release/release.sh --abort [version]` (cleanup failed release)
- **Linear Tracking:** Release workflow integrated with Linear issues (auto-updates status)
- **Detailed docs:** [release/RELEASE_PROCESS.md](../../../release/RELEASE_PROCESS.md)

## Prepare a Release

When user asks to "prepare release" or "prepare beta release":

1. **Check Linear for release issue:**
   - Search Linear for release-related issues: `user-linear.list_issues` with filters for release keywords
   - **If no issue found:** ⚠️ Warn "No Linear release issue found. Do you want to proceed anyway?"
   - **If one issue found:** Show issue details and confirm
   - **If multiple issues found:** Present list and ask user to select one
   - **Once confirmed:** Mark issue as "In Progress" using `user-linear.update_issue`
   - **Store issue ID** for later updates
2. **Pre-flight checks:** Verify repository is ready for release:
   - **Check branch:** `git branch --show-current` (must be `main`)
   - **Check sync:** `git fetch origin && git status` (must be in sync with origin/main)
   - **Check clean:** `git status --porcelain` (must be empty - no uncommitted changes)
   - **If any check fails:** ⚠️ Warn user with specific issue and ask "Do you want to proceed anyway?"
   - **If user declines:** Stop and let them fix the issue first.
3. **Wait for CI:** `./scripts/wait-for-ci.sh`
4. **Generate summary:** Create 2-4 paragraphs highlighting user-facing changes. Save to `release/AI_RELEASE_SUMMARY.md`.
   - **For beta-to-beta releases:** Analyze commits since the last beta tag.
   - **For stable releases (graduating from beta):** Analyze ALL commits since the last **stable** release (not the last beta). This ensures the summary covers the entire beta cycle.
   - See "Generating Release Summary" section below for detailed guidance.
5. **Commit and push summary:** The release script requires a clean repository.
   - `git add release/AI_RELEASE_SUMMARY.md`
   - `git commit -m "release: Add AI-generated summary for v[version]"`
   - `git push`
6. **Run prepare:** `./release/release.sh --prepare [--beta] --summary release/AI_RELEASE_SUMMARY.md`
7. **Show preview to user:** Display the proposed release notes with clickable link.
   - Show `release/RELEASE_NOTES.md` summary/preview (first ~20 lines)
   - Provide clickable markdown link: `[release/RELEASE_NOTES.md](release/RELEASE_NOTES.md)` (not inline code)
8. **Update Linear issue:**
   - Read `release/RELEASE_NOTES.md` content
   - Post content to Linear issue as comment using `user-linear.create_comment`
   - **Include clickable link:** Add link to full notes at top of comment: `📋 Full Release Notes: [release/RELEASE_NOTES.md](https://github.com/fxstein/ai-todo/blob/main/release/RELEASE_NOTES.md)`
   - Mark issue as "In Review" using `user-linear.update_issue`
9. **STOP.** Wait for user approval before proceeding.

## Generating Release Summary

**Role:** You are a Technical Release Manager for a professional Open Source project.

**Task:** Draft a release summary based on commit messages for **end-users** (not developers).

**Commit Range:**
- **For beta-to-beta releases:** Analyze commits since the last beta tag (e.g., `v4.0.0b2..HEAD`)
- **For stable releases (graduating from beta):** Analyze ALL commits since the last stable release (e.g., `v3.0.2..HEAD`)

**Constraints & Formatting:**
1. **Format:** Write exactly 2-4 paragraphs of narrative text. Do not use bulleted lists or markdown headers (e.g., no `#` or `##`).
2. **Content:** Focus only on the most significant features, user-facing changes, and critical fixes. Filter out minor chores, typo fixes, or internal refactors unless they directly impact end users.
3. **Documentation:** If commits added new documentation files (`.md`, `.pdf`), mention them with direct GitHub links:
   - Get repo URL: `git remote get-url origin` (convert SSH to HTTPS if needed)
   - Format: `[filename](https://github.com/user/repo/blob/main/path/to/file.md)`
4. **Tone:** Professional, concise, and encouraging. Write for users who want to understand what's new and why they should upgrade.
5. **Output:** Save to `release/AI_RELEASE_SUMMARY.md`

**Example Structure:**
```
This release focuses on [theme/primary improvement]. [Key feature 1] provides [user benefit]. [Key feature 2] enhances [capability].

[Second major area of improvement]. [Specific change] now allows users to [benefit]. [Another change] improves [aspect] by [improvement].

Additional improvements include [grouped minor features]. Several bug fixes improve robustness including [specific fixes that matter to users].
```

**Generate Commits:**
```bash
# For beta-to-beta:
git log v4.0.0b2..HEAD --pretty=format:"%h %s" --no-merges

# For stable (graduating from beta):
git log v3.0.2..HEAD --pretty=format:"%h %s" --no-merges
```

## Execute a Release

When user asks to "execute release":

1. **Run execute:** `./release/release.sh --execute`
2. **Monitor CI:** Watch GitHub Actions until successful deployment:
   - Poll `gh run list` for latest workflow run
   - Wait for "completed" status with "success" conclusion
   - If CI fails, report error and STOP (see Error Handling section)
3. **Update Linear issue:**
   - Read `release/RELEASE_SUMMARY.md` content
   - Post release summary to Linear issue using `user-linear.create_comment`
   - Include PyPI link: `https://pypi.org/project/ai-todo/[version]/`
   - Include GitHub release link from workflow output
   - Mark issue as "Done" using `user-linear.update_issue`

## Abort a Release

When user asks to "abort release":

1. **Run abort:** `./release/release.sh --abort [version]`
2. **Update Linear issue (if exists):**
   - Post abort summary to Linear issue using `user-linear.create_comment`
   - Include: reason for abort, version that was aborted, current state
   - Mark issue as "Todo" using `user-linear.update_issue` (reset for retry)

## Error Handling

**If ANY error occurs:**
1. **STOP IMMEDIATELY.**
2. Report the error.
3. **If Linear issue exists:** Post error details to issue
4. **WAIT FOR USER.** Do not attempt auto-recovery.

## Forbidden Actions

- ❌ Never auto-execute after prepare.
- ❌ Never bypass CI/CD failures.
- ❌ **NEVER use `--no-verify` on git commits.**

## Additional Resources

- **Detailed Process:** [release/RELEASE_PROCESS.md](../../../release/RELEASE_PROCESS.md)
- **Version Strategy:** Beta vs Stable release guidelines in RELEASE_PROCESS.md
- **Migration Handling:** See RELEASE_PROCESS.md for adding migrations to releases
- **Release Scripts:** All scripts are in `release/` directory
