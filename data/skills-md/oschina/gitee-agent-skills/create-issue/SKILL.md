---
name: create-issue
description: Use this skill when the user wants to create a new issue, report a bug, submit a feature request, or discuss a requirement before implementation. "create issue", "report bug", "create-issue", "submit issue", "新建 issue", "提需求", "提 bug". Requires Gitee MCP Server to be configured.
version: 1.0.0
requires:
  mcp-servers:
    - gitee
---

> **Note**: If you have `mcporter` installed locally, you should use `mcporter` to invoke the MCP tool instead of directly calling the MCP tool. The `mcporter` CLI provides a more convenient interface and better error handling.

# Create Issue via Gitee MCP

Create a well-structured Issue on Gitee after clarifying the requirements with the user. This skill is designed for discussions about new requirements, improvements, or bug reports before they are formally created as Issues.

## Prerequisites

- Gitee MCP Server configured (tools: `create_issue`, `list_repo_issues`, `list_user_repos`, `search_open_source_repositories`)
- User must provide: repository owner/name (or search/select from available repositories)
- Optional: issue type (feature/bug/enhancement), priority, labels

## Steps

### Step 1: Identify the Target Repository

If the user hasn't specified a repository, ask which scenario:

**Scenario A: User's own/private repository**
- Use `list_user_repos` to list repositories the user has access to
- Let user select from the list

**Scenario B: Open source/public repository**
- Use `search_open_source_repositories` to search for the repository
- Verify by checking the repository URL format (`owner/repo`)

If the user provides a repository directly (format: `owner/repo`), verify it exists by confirming with the user.

### Step 2: Clarify the Issue Content

Discuss with the user to gather the following information:

**For Bug Reports:**
- What is the expected behavior?
- What is the actual behavior?
- How to reproduce the issue (reproduction steps)?
- Environment details (OS, version, browser, etc.)
- Any error messages or logs?

**For Feature Requests:**
- What problem does this feature solve?
- What is the proposed solution?
- Are there any similar features in other projects for reference?
- Any design preferences or constraints?

**For Improvements:**
- What aspect needs improvement?
- What are the suggested improvements?
- What is the expected outcome?

Use the following template to structure the discussion:

```
## Issue Information

**Type:** [Bug / Feature / Enhancement / Question / Other]

**Title:** [Brief description - keep it under 50 characters]

**Description:**
[Detailed description of the issue]

**Reproduction Steps (for bugs):**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior:**
[What should happen]

**Actual Behavior:**
[What actually happens]

**Environment:**
- OS:
- Version:
- Browser (if applicable):

**Additional Context:**
[Any other relevant information, screenshots, logs, etc.]
```

### Step 3: Validate and Refine

Before creating the Issue:

1. Check if a similar Issue already exists using `list_repo_issues`
2. If duplicates are found, present them to the user
3. Refine the title and description based on discussion
4. Confirm with the user before creating

### Step 4: Create the Issue

Use `create_issue` to create the Issue with the following parameters:

- `owner`: repository owner
- `repo`: repository name
- `title`: Issue title (concise and descriptive)
- `body`: Issue description (detailed and well-structured)
- `labels`: (optional) comma-separated list of labels like `bug`, `feature`, `enhancement`

**Label recommendations:**
| Type | Labels |
|------|--------|
| Bug | `bug` |
| Feature | `feature` |
| Enhancement | `enhancement` |
| Question | `question` |
| Documentation | `docs` |

### Step 5: Confirm and Summary

After successful creation:
1. Display the Issue URL to the user
2. Summarize what was created
3. Ask if the user wants to:
   - Start implementing (use `implement-issue` skill)

## Example Conversations

**Example 1: Bug Report**
```
User: I found a bug in the login page - it doesn't show error message when password is wrong.

You: Let me help you create a bug report. Could you please clarify:
1. What is the expected behavior? (e.g., "Show 'Invalid credentials' message")
2. What is the actual behavior? (e.g., "Nothing happens, page just reloads")
3. How to reproduce? (e.g., "Enter wrong password and click login")
4. What browser and OS are you using?

User: [Provides details...]

You: Here's the Issue I've prepared:
Title: Login page doesn't show error message for invalid credentials
...
Should I create this Issue?
```

**Example 2: Feature Request**
```
User: I want to add dark mode to the app.

You: Great idea! Let me understand more about this feature:
1. What problem does dark mode solve? (e.g., "Reduce eye strain at night")
2. Should it follow system preference or be user-toggleable?
3. Any reference implementations you have in mind?

User: [Provides details...]

You: Here's the Issue I've prepared:
Title: Add dark mode support
...
Should I create this Issue?
```

## Notes

- Always confirm the Issue details with the user before creating it
- Search for existing Issues first to avoid duplicates
- Use clear, descriptive titles that summarize the issue in one line
- Include all necessary details in the description to help others understand and reproduce
- For complex features, consider creating a technical design document as a comment after the Issue is created
- If the user wants to immediately work on the Issue, suggest using the `implement-issue` skill afterwards
