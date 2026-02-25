---
name: new-issue
description: Create GitHub issues with duplicate detection and codebase analysis. Use when you discover a bug, improvement, or issue that wasn't in the original scope/spec during development. Triggers on phrases like "create an issue", "file a bug", "this should be tracked", "we should fix this later", "out of scope issue", "noticed a problem", "found a bug".
allowed-tools: Bash(gh:*), Grep, Glob, Read, WebSearch, Task, mcp__conductor__AskUserQuestion
---

# Smart GitHub Issue Creation

This skill helps create well-researched GitHub issues while preventing duplicates and wasted effort.

## When to Use This Skill

Activate this skill when:
- You discover a bug or issue that's **outside the current task's scope**
- You notice something that should be fixed but isn't part of the current spec
- The user mentions wanting to "track this for later" or "create an issue"
- You find an improvement opportunity while working on something else
- The user explicitly asks to create an issue or file a bug

## Workflow

### Step 1: Clarify the Issue

If the issue description is vague or missing, ask the user:
> "What issue would you like to create? Describe the bug, feature, or improvement."

### Step 2: Check if Already Fixed/Implemented

Before creating, verify this isn't already solved:

1. **Search codebase** for related keywords:
   ```bash
   # Use Grep/Glob to find relevant code
   ```

2. **Check recent commits** (filter by relevant keywords):
   ```bash
   # Generic recent commits
   gh api repos/{owner}/{repo}/commits --jq '.[0:20] | .[] | "\(.sha[0:7]) \(.commit.message | split("\n")[0])"'

   # Targeted search for specific keywords (more useful)
   gh api repos/{owner}/{repo}/commits --jq '[.[] | select(.commit.message | test("KEYWORD1|KEYWORD2"; "i"))] | .[0:10] | .[] | "\(.sha[0:7]) \(.commit.message | split("\n")[0])"'
   ```
   Replace `KEYWORD1|KEYWORD2` with terms relevant to the issue (e.g., "retweet|repost" for a retweet bug).

3. **If already fixed/implemented**, inform the user:
   > "It looks like this might already be addressed. I found [what you found]. Are you aware of this?"

   Options: "Show me the existing solution", "Create the issue anyway", "Cancel"

### Step 3: Check Existing GitHub Issues

Search for duplicates:

1. **Search open issues:**
   ```bash
   gh issue list --state open --limit 50 --json number,title,body,labels,url
   ```

2. **Search closed issues:**
   ```bash
   gh issue list --state closed --limit 30 --json number,title,body,labels,url,closedAt
   ```

3. **Keyword search:**
   ```bash
   gh search issues --repo {owner}/{repo} "keywords" --limit 20 --json number,title,body,url,state
   ```

4. **Fetch details with comments for promising matches:**
   ```bash
   gh issue view <number> --json number,title,body,comments,labels,state
   ```

5. **Based on findings:**

   **EXACT DUPLICATE:**
   > "I found an existing issue #[number] - [title] that matches this. What would you like to do?"
   - Options: "Add comment to existing", "View details", "Create anyway", "Cancel"

   **RELATED ISSUE:**
   > "I found related issue #[number]. Your issue could be a comment, sub-issue, or separate. Preference?"
   - Options: "Add as comment", "Create as sub-issue (I'll activate gh-subissues skill)", "Create separate issue"

   **CLOSED ISSUE:**
   > "This was previously reported as #[number] and [fixed/rejected]. Context: [summary]. Still want to proceed?"

### Step 4: Research Potential Solutions

If you have enough context:

1. **Explore codebase** for patterns and relevant files
2. **Use web search** via Task tool for best practices
3. **Formulate 1-3 approaches** with:
   - Brief description
   - Files that would need changes
   - Trade-offs (if applicable)

### Step 5: Draft Issue Content

Structure the issue:

```markdown
## Summary
[1-2 sentences]

## Context
[Background, how discovered, why it matters]

## Current Behavior (for bugs)
[What happens now]

## Expected Behavior
[What should happen]

## Potential Implementation (optional)
### Approach 1: [Name]
- Description
- Files: `path/to/file.ts`

## Additional Context
[Related issues, screenshots, etc.]
```

### Step 6: Confirm Before Creating

Present a **concise summary** (don't overwhelm with details upfront):

> "Ready to create issue:
>
> **Title:** [title]
> **Summary:** [1-2 sentences max]
>
> Does this look good?"

Options: "Create the issue", "Show more details", "Edit first", "Cancel"

**If user selects "Show more details"**, then display:
- Key findings from codebase exploration
- Proposed implementation approaches
- Files that would be affected

### Step 7: Create the Issue

```bash
gh issue create --title "type(area): description" --body "$(cat <<'EOF'
[structured content]
EOF
)"
```

Then display the URL and issue number.

## Sub-Issue Support

To create as a sub-issue, say:
> "I'll activate the gh-subissues skill to create this as a sub-issue of #[parent]."

Then use the Skill tool to invoke `gh-subissues`.

## During Development: Out-of-Scope Issues

When you notice an issue while working on something else:

1. **Briefly mention it** to the user:
   > "While working on [current task], I noticed [issue]. This seems out of scope for the current work. Would you like me to create an issue to track this for later?"

2. **If user agrees**, run through this workflow
3. **If user declines**, continue with the current task

This prevents scope creep while ensuring important issues aren't forgotten.

## Issue Title Conventions

Use conventional format:
- `fix(area): brief description` - Bug fixes
- `feat(area): brief description` - New features
- `refactor(area): brief description` - Code improvements
- `docs(area): brief description` - Documentation
- `chore(area): brief description` - Maintenance

## Handling Screenshots & Attachments

If the user provides screenshots or images for the issue:

1. **Check for attached files** in the conversation (e.g., `.context/attachments/`)
2. **Read and understand** the images before drafting the issue
3. **Create the issue first** (without images or with placeholder text) to get the issue number
4. **Upload images with issue-prefixed names** to a draft release:

```bash
# Create or reuse a draft release for issue assets
gh release view issue-assets 2>/dev/null || \
  gh release create issue-assets --draft --title "Issue Assets" --notes "Screenshots for issues"

# Copy and rename with issue prefix (e.g., 216-description.png)
cp "path/to/screenshot.png" /tmp/{issue#}-{description}.png

# Upload the renamed file
gh release upload issue-assets /tmp/{issue#}-{description}.png

# Get the URL
gh release view issue-assets --json assets --jq '.assets[] | select(.name | startswith("{issue#}")) | "\(.name): \(.url)"'
```

5. **Edit the issue** to add the image URLs (not as a separate comment):
```bash
gh issue edit {issue#} --body "$(cat <<'EOF'
[issue body with images]
![description](https://github.com/owner/repo/releases/download/issue-assets/{issue#}-description.png)
EOF
)"
```

**Naming convention:** `{issue#}-{description}.png` (e.g., `216-xfeed-display.png`, `216-xcom-expected.png`)

**Note:** The `gh` CLI cannot upload images directly to issues ([feature requested since 2020](https://github.com/cli/cli/issues/1895)). Release assets are the cleanest workaround that keeps images within the repo's GitHub ecosystem.

## Notes

- Always prioritize preventing duplicates - saves everyone time
- Be thorough but concise - don't overwhelm the user
- For simple, clearly new issues, streamline the process
- Keep the user informed at each decision point
- Check for user-provided debug URLs and include them in the issue
