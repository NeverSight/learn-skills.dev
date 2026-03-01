---
name: create-issue
description: >-
  Create or update a GitHub issue with clarifying questions.
  TRIGGER when: user asks to create, update, edit, or refine a GitHub issue.
  Examples: "create an issue for...", "update issue 42", "improve the description on issue 137".
  DO NOT TRIGGER when: user just wants to view/list issues, comment on a PR, or implement a feature.
allowed-tools: Bash, Read, Glob, Grep, WebSearch, AskUserQuestion
---

Create or update a GitHub issue. **Do NOT implement — only create/update the issue.**

## Mode

- Argument is a **number or URL** → update mode
- Otherwise → create mode

## Create

1. Get feature/bug/task description from user (argument or ask)
2. Explore codebase for context
3. Ask 2-4 clarifying questions via `AskUserQuestion` (see guidelines below)
4. Draft the full issue (title + body) and present it to the user as a preview
5. Ask the user if it looks good or what to change — repeat 4-5 until approved
6. Only after explicit approval: create with `gh issue create`

## Update

1. Fetch with `gh issue view <number>`
2. Clarify what to change if not obvious
3. Draft the updated issue and present the full result to the user as a preview
4. Ask the user if it looks good or what to change — repeat 3-4 until approved
5. Only after explicit approval: apply with `gh issue edit` or `gh issue comment` (comment for additions, edit for rewrites)

## AskUserQuestion Guidelines

Call `AskUserQuestion` with **one single call** containing all your questions (max 4).
Each question **must** have:
- A short `header` (max 12 chars, e.g. "Type", "Scope", "Priority")
- A clear `question` ending with `?`
- Exactly 2-4 `options`, each with a short `label` and a `description`
- `multiSelect: false` unless the user can genuinely pick multiple

Use `AskUserQuestion` for **decisions with concrete options** (type of issue, priority, scope).
Use **plain text** for open-ended questions where the user needs to explain something freely — just output the question as regular text.

Example call structure:
```json
{
  "questions": [
    {
      "question": "What type of issue is this?",
      "header": "Type",
      "multiSelect": false,
      "options": [
        { "label": "Bug fix", "description": "Something is broken" },
        { "label": "Feature", "description": "New functionality" },
        { "label": "Improvement", "description": "Enhance existing behavior" }
      ]
    }
  ]
}
```

## Issue Body Structure

```markdown
## Summary
[1-2 sentences — what and why]

## Context
[What exists today, why this change is needed]

## Requirements
- [ ] [Specific, verifiable requirement]

## Affected Areas
- [File paths or modules]

## Out of Scope
[What this does NOT cover]

## Acceptance Criteria
- [ ] [Concrete, testable criterion]
```

Omit sections that aren't relevant. Keep it tight.

## Rules

- **Never call `gh issue create` or `gh issue edit` without explicit user approval of the previewed content**
- Title: imperative, under 70 chars
- Add labels if they exist (`gh label list`)
- Be specific: file paths, concrete criteria, no vague language
- Show the issue URL when done
