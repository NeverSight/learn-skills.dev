---
name: create-pr
description: Push branch and create GitHub pull request (auto-assigned)
allowed-tools: Bash(git status) Bash(git push) Bash(git log) Bash(git diff) Bash(gh pr create) Bash(gh pr list) Bash(git branch)
metadata:
  model: sonnet
---

## Language Conventions

**Infer language style from the project:**
- Analyze existing pull requests, commit messages, and documentation to detect the project's language variant (US English, UK English, etc.)
- Match the spelling conventions found in the project (e.g., "optimize" vs "optimise", "favor" vs "favour")
- Maintain consistency with the project's established language style throughout PR titles and descriptions

---

Create a pull request with the following workflow:

1. Check current git status and branch
2. Push the current branch to remote (with -u flag if needed)
3. Analyse recent commits to generate PR title and description
4. Create GitHub PR and auto-assign to current user:
   - Use `gh pr create --assignee @me` to self-assign the pull request
   - If assignment fails (user not a collaborator), GitHub CLI will create the PR without assignment
   - This provides convenience for repository collaborators while remaining safe for contributors
5. Optional: Additional assignees can be added using `--assignee` flag (comma-separated for multiple)
   - Note: PR is already auto-assigned to the current user via `--assignee @me` in step 4

**CONCISE PR RULE: Keep everything brief and focused**

Generate a title based on the commit history and user's request context.

For the PR title:
- Use natural, descriptive language (NOT conventional commits format like "feat:", "fix:", "chore:")
- Make it clear and specific to the changes
- Keep it concise but informative

For the PR description:
- **Maximum 1-2 bullet points** summarizing the key changes
- **No verbose explanations** - be direct and specific
- **No test plan, acceptance criteria, or additional sections**
- Focus only on what changed and why
