---
name: cmd-gh-issue
description: Create structured GitHub issues from conversation context using gh CLI
disable-model-invocation: true
---

# Create GitHub Issue from Conversation

Create a well-structured GitHub issue using `gh` CLI, populated with context from the current conversation.

## Instructions

1. **Determine the repo** -- confirm you're inside a git repo with a GitHub remote:

   ```bash
   gh repo view --json nameWithOwner -q '.nameWithOwner'
   ```

   If this fails, ask the user which repo to file against.

2. **Synthesize the conversation** into a GitHub issue body following the structure below.

3. **Create the issue** using `gh`:

   ```bash
   gh issue create --title "<concise title>" --body "$(cat <<'ISSUE_EOF'
   <issue body here>
   ISSUE_EOF
   )"
   ```

4. **Report back** with the issue URL.

## Issue Body Structure

Build the issue body in this exact order:

### Section 1: What & Why

Open with a short (2-4 bullet) summary answering:

- **What** needs to happen?
- **Why** does it matter? (user pain, system constraint, business goal)

This section should stand alone -- a reader who stops here should understand the ask.

### Section 2: Context & Discussion

This is the bulk of the issue. Capture everything relevant from our conversation:

- **Background** -- what led to this discussion
- **Current behavior** -- how things work today (or don't)
- **Desired behavior** -- what success looks like
- **Constraints & decisions** -- trade-offs we discussed, options we rejected and why
- **Technical details** -- relevant code paths, configs, schemas, API shapes, error messages
- **Related work** -- links to PRs, issues, docs, or external references mentioned

**Formatting rules for this section:**

- Use `## Headings` and `### Subheadings` to organize by topic
- Use bullet points over paragraphs
- Use markdown tables for comparisons, option matrices, or structured data
- Embed images/screenshots if any were shared (use `![alt](url)` syntax)
- Wrap code snippets, commands, file paths, and config in fenced code blocks with language tags
- Use `<details><summary>...</summary>...</details>` to collapse verbose content (logs, full configs, large code blocks) so the issue stays scannable
- Do NOT strip context -- preserve the substance of our discussion, but reorganize it logically

### Section 3: Implementation Plan

End with the plan we've aligned on (even if rough). Frame it for a future agent or developer picking this up cold:

- Number the steps
- Call out key files to create or modify
- Note any open questions or decisions still TBD (prefix with `[ ]`)
- If there are dependencies between steps, make the order explicit
- If we haven't aligned on a plan yet, write `## Implementation Plan\n\n_TBD -- no plan agreed on yet._`

## Labels & Assignment (optional)

- If the conversation implies a category (bug, feature, enhancement, tech-debt), add `--label` flags
- Do NOT assign unless the user explicitly asks

## Style Rules

- **Title**: imperative mood, under 70 chars (e.g., "Add retry logic to webhook delivery")
- **No fluff**: skip filler phrases like "It would be great if..." -- be direct
- **Bias to structure**: headers > paragraphs, bullets > prose, tables > lists-of-pairs
- **Preserve signal**: don't summarize away details that a future implementer would need
- **Mark uncertainty**: if something was discussed but not decided, say so explicitly with "TBD" or an open checkbox `[ ]`
