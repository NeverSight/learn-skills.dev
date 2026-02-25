---
name: update-issue
description: Update a GitHub issue with new title, body, labels, or assignees
allowed-tools: Bash(gh issue view) Bash(gh issue edit) Bash(gh repo view)
metadata:
  model: sonnet
---

## Language Conventions

**Infer language style from the project:**
- Analyze existing issues, documentation, and commit messages to detect the project's language variant (US English, UK English, etc.)
- Match the spelling conventions found in the project (e.g., "initialize" vs "initialise", "behavior" vs "behaviour")
- Maintain consistency with the project's established language style throughout issue updates

---

Update a GitHub issue with the following workflow:

1. Check if we're in a GitHub repository
2. **Identify the issue to update:**
   - If issue number is provided (e.g., "issue 123", "#456", or "789"), use that issue
   - If not provided, ask the user for the issue number
3. **View current issue details:**
   - Use `gh issue view` to display current state
   - Show title, body, labels, assignees, and state
   - This helps understand what needs updating
4. **Check for ISSUE_TEMPLATE format:**
   - Look for issue templates in `.github/ISSUE_TEMPLATE/` or `.github/` directories
   - If the current issue follows a template, identify which template
   - Parse template structure to preserve required sections
5. **Determine what to update:**
   - Ask what fields the user wants to update (title, body, labels, assignees, state)
   - Accept input for new values
   - If updating body and template exists, maintain template structure
6. **Apply updates with validation:**
   - For title: Use natural, descriptive language
   - For body with template: Preserve template sections and formatting
   - For body without template: Use clear, structured format
   - For labels: Only use existing repository labels
   - For assignees: Only assign valid repository collaborators
   - Use `gh issue edit` to apply changes
7. **Confirm and display results:**
   - Show summary of all updates made
   - Display success message with link to updated issue

For the issue title:
- Use natural, descriptive language
- Keep it concise but informative
- Match the style of existing issue titles in the repository

For the issue body (when using ISSUE_TEMPLATE format):
- Follow the exact template structure
- Preserve required sections and formatting
- Update only the sections being changed
- Maintain template sections

For the issue body (custom format):
- Include clear problem statement or feature details
- Add relevant context from the update
- Keep it structured and actionable
- Maintain existing formatting style when possible

For labels and assignees:
- Only add labels that already exist in the repository
- Validate assignees are valid repository collaborators
- Show current labels and assignees before making changes
