---
name: check-ci
description: This skill monitors PR CI checks by polling GitHub status until completion or timeout. Use when the user requests to check CI status, wait for CI to pass, monitor PR checks, or verify build status. Applicable for queries like "check my CI", "wait for CI to pass", "is my PR green", or "monitor CI checks".
disable-model-invocation: true
---

# Check CI

## Overview

This skill provides automated monitoring of GitHub Pull Request CI checks. It polls PR check status at regular intervals and reports when checks pass, fail, or timeout, enabling continuous integration workflow automation.

## When to Use This Skill

Trigger this skill when the user requests:
- Checking CI status for a PR
- Monitoring CI checks until completion
- Waiting for CI to pass before proceeding
- Verifying build status
- Polling GitHub PR checks with custom intervals or timeouts

## Core Workflow

### 1. Execute CI Polling

Run the `check_ci.sh` script to monitor PR checks:

```bash
bash scripts/check_ci.sh [PR_NUMBER] [INTERVAL] [TIMEOUT]
```

**Parameters:**
- `PR_NUMBER` (optional): PR number to monitor. Auto-detects from current branch if not provided
- `INTERVAL` (optional, default: 15): Seconds between polling attempts
- `TIMEOUT` (optional, default: 600): Maximum wait time in seconds

**Examples:**
```bash
# Auto-detect PR from current branch
bash scripts/check_ci.sh

# Monitor specific PR #123
bash scripts/check_ci.sh 123

# Custom interval (30s) and timeout (15 min)
bash scripts/check_ci.sh 123 30 900
```

### 2. Interpret Results

The script returns three possible outcomes:

**✅ Success (exit code 0):** All CI checks passed
- Indicate that the PR is green and ready for next steps
- Suggest proceeding with merge, review, or deployment

**❌ Failure (exit code 1):** One or more CI checks failed
- Parse the output to identify specific failing checks
- Analyze failure patterns (test failures, lint errors, build issues)
- Suggest concrete fixes based on the failure type:
  - Test failures: Review test output, fix failing tests
  - Lint errors: Run linter locally, apply fixes
  - Build failures: Check compilation errors, dependencies
  - Type errors: Review type definitions, fix type issues

**⏰ Timeout (exit code 2):** Polling exceeded timeout limit
- Suggest running with longer timeout: `check_ci.sh [PR] [interval] [longer_timeout]`
- Recommend checking GitHub directly for CI status
- Consider whether CI is actually running or stuck

### 3. Provide Actionable Summary

Structure the response as follows:

```markdown
## CI Polling Results for PR #[number]

### Final Status
[✅ All checks passed / ❌ Checks failed / ⏰ Polling timed out]

### Polling Summary
- Duration: [time]
- Final state: [description]
- Specific failures: [if applicable]

### Next Steps
[Specific actions based on results]
```

## Advanced Usage

### Auto-Detection Requirements

For PR auto-detection to work:
- Must be in a git repository
- Current branch must have an associated PR
- GitHub CLI (`gh`) must be authenticated

### Error Handling

**No PR found:**
- Verify current branch has an associated PR: `gh pr view`
- Suggest creating a PR if none exists
- Check if branch is pushed to remote

**GitHub CLI issues:**
- Verify `gh` is installed and authenticated
- Check repository access permissions
- Ensure network connectivity

### Integration with Other Workflows

This skill complements:
- PR creation workflows (check CI after pushing)
- Code review processes (verify CI before reviewing)
- Deployment pipelines (ensure CI passes before deploy)
- Automated testing workflows

## Resources

### scripts/check_ci.sh

Bash script that performs the actual CI polling. The script:
- Auto-detects PR number from current branch or accepts as argument
- Auto-detects repository owner/name from git remote
- Polls `gh pr checks` at configurable intervals
- Returns appropriate exit codes for success/failure/timeout
- Provides real-time status updates during polling

The script can be executed directly without loading into context, making it token-efficient for repeated CI monitoring operations.
