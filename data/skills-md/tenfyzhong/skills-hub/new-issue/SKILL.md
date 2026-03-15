---
name: new-issue
description: Use when the user asks to create a GitHub issue from the current conversation context (e.g., "new issue", "create issue", "file an issue", bug/feature request) with a target repo given or auto-detected, and gh CLI is available/authenticated.
---

# New Issue Skill

Create a GitHub issue based on the current conversation context.

## Prerequisites Check (MUST verify first)

**Mode Detection**: Check if user specified a target repository.

| User Input | Mode | Git Repo Required |
|------------|------|-------------------|
| `https://github.com/owner/repo` | Explicit | No |
| `owner/repo` | Explicit | No |
| No repo specified | Auto-detect | Yes |

### Always Required:

```bash
# Check if gh CLI is available and authenticated
gh auth status
```

If gh not authenticated → "Please run `gh auth login` first."

### Only for Auto-detect Mode (no repo specified):

```bash
# Check if in a git repository
git rev-parse --is-inside-work-tree

# Get repository info
gh repo view --json owner,name,url
```

If not in git repo and no target specified → "Please specify a target repository (e.g., `owner/repo` or GitHub URL), or navigate to a git project."

## Input

The user triggers this skill with phrases like:
- "new issue"
- "create issue"
- "file an issue"
- "report this bug"
- "submit feature request"

**Optional**: User may specify target repository:
- Full URL: `https://github.com/owner/repo`
- Short form: `owner/repo`

Context for the issue comes from:
- Current conversation history
- User's description of the problem/feature
- Code snippets or error messages discussed
- Any relevant file paths mentioned

## Workflow

### Step 1: Determine Target Repository

**Case A: User specified a repository**

Parse the user input to extract owner/repo:

```bash
# From URL: https://github.com/owner/repo or https://github.com/owner/repo/...
# Extract: owner/repo

# From short form: owner/repo
# Use directly

# Validate the repository exists and is accessible
gh repo view "$TARGET_REPO" --json owner,name,url
```

If repo not found or inaccessible → "Repository '$TARGET_REPO' not found or you don't have access."

**Case B: Auto-detect from current git repo**

```bash
# Get repository info and check if it's a fork
gh repo view --json owner,name,isFork,parent,url

# If it's a fork, get parent (upstream) info
IS_FORK=$(gh repo view --json isFork -q '.isFork')
if [ "$IS_FORK" = "true" ]; then
  UPSTREAM_OWNER=$(gh repo view --json parent -q '.parent.owner.login')
  UPSTREAM_NAME=$(gh repo view --json parent -q '.parent.name')
  TARGET_REPO="$UPSTREAM_OWNER/$UPSTREAM_NAME"
else
  # Use current repo as target
  TARGET_REPO=$(gh repo view --json owner,name -q '.owner.login + "/" + .name')
fi
```

### Step 2: Analyze Context and Generate Issue Content

Based on the conversation context, generate:

**Language Requirement**:
- The issue title and all description content MUST be in English.
- If the conversation is in another language, translate/summarize into English.

**Title Generation Rules**:
1. Keep concise (under 80 characters)
2. Start with issue type prefix if clear: `[Bug]`, `[Feature]`, `[Enhancement]`, `[Question]`
3. Describe the core problem/request clearly
4. Use imperative mood when appropriate
5. Use English only

**Description Generation**:

Structure the description with these sections as applicable:

```markdown
## Description

[Clear explanation of the issue/feature request]

## Context

[Relevant background information from the conversation]

## Steps to Reproduce (for bugs)

1. [Step 1]
2. [Step 2]
3. [Expected vs Actual behavior]

## Proposed Solution (if discussed)

[Any solutions discussed in the conversation]

## Additional Information

- [Relevant code snippets]
- [Error messages]
- [Environment details if relevant]
```

### Step 3: Present Draft for User Review (CRITICAL)

**MUST use the `question` tool to present the draft and get user confirmation.**

Present the generated issue to the user:

```
## Issue Draft

**Target Repository**: [TARGET_REPO]

**Title**: [Generated Title]

**Description**:
[Generated Description]

---

Please review the above issue draft.
```

Use the `question` tool to ask:

```
Options:
1. "Submit as-is" - Create the issue with current content
2. "Modify title" - Change the issue title
3. "Modify description" - Change the issue description
4. "Cancel" - Do not create the issue
```

### Step 4: Handle User Modifications

If user chooses to modify:

**For title modification**:
- Ask user for the new title
- Update and show the revised draft
- Return to Step 3 for confirmation

**For description modification**:
- Ask user what changes they want
- User can provide:
  - Specific text to add/remove/change
  - General instructions like "make it shorter" or "add more detail about X"
- Update and show the revised draft
- Return to Step 3 for confirmation

**Loop until user confirms or cancels.**

### Step 5: Create the Issue

Once user confirms, create the issue:

```bash
# Create issue on the target repository
gh issue create \
  --repo "$TARGET_REPO" \
  --title "$ISSUE_TITLE" \
  --body "$ISSUE_BODY"
```

**Use HEREDOC for body to preserve formatting**:

```bash
gh issue create --repo "$TARGET_REPO" --title "$ISSUE_TITLE" --body "$(cat <<'EOF'
## Description

[Description content here]

## Context

[Context content here]

EOF
)"
```

### Step 6: Report Results

After issue creation, provide:

```bash
# Get the created issue details
gh issue view --repo "$TARGET_REPO" <ISSUE_NUMBER> --json number,title,url,state
```

## Output Format

---

### Issue Created Successfully

**Issue**: #[NUMBER] - [TITLE]
**Repository**: [TARGET_REPO]
**URL**: [ISSUE_URL]

#### Summary

[Brief confirmation of what was submitted]

---

## Error Handling

| Situation | Action |
|-----------|--------|
| No context provided | Ask user to describe the issue they want to create |
| User cancels | "Issue creation cancelled. No issue was created." |
| API error | Report the error and suggest checking permissions |
| Rate limited | Inform user and suggest waiting |
| No write access | "You don't have permission to create issues on [REPO]. Consider forking first." |
| Repo not specified + not in git repo | Ask user to specify target repo or navigate to a git project |
| Invalid repo format | "Invalid repository format. Use 'owner/repo' or full GitHub URL." |

## Common Mistakes

- Generating a title or description in a non-English language
- Skipping explicit user confirmation before issue creation
- Including secrets or sensitive data in the issue body

## Important Notes

1. **Always Confirm**: NEVER create an issue without explicit user confirmation
2. **Preserve Context**: Include relevant conversation context in the issue
3. **Flexible Targeting**: Accept explicit repo (URL or owner/repo) OR auto-detect from git
4. **Fork Awareness**: When auto-detecting, target upstream repository for forks
5. **Formatting**: Use proper Markdown formatting in issue body
6. **Privacy**: Do not include sensitive information (API keys, passwords, etc.) in issues
7. **Iteration**: Allow multiple rounds of modification before submission
