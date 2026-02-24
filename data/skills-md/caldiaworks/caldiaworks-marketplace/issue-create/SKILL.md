---
name: issue-create
version: 0.3.0
description: "Create GitHub Issues from user input or USDM requirements documents. Standalone mode guides through title, body, and labels. USDM mode creates a hierarchy of issues from requirements with specifications in the issue body. Use when: create issue, new issue, GitHub issue, open issue, file issue, create issues from requirements, USDM to issues, issue-create, /issue-create."
---

# GitHub Issue Creation

Create GitHub Issues in two modes: standalone (interactive) or USDM (batch from requirements document). Works in any Git repository with GitHub as the remote.

## Prerequisites

Before creating issues, verify the environment:

1. The current directory is a Git repository. If not, inform the user and stop.
2. The GitHub CLI (`gh`) is authenticated. If not, instruct the user to run `gh auth login`.

## Mode 1: Standalone Issue

Create a single issue through dialogue with the user.

### Step 1: Collect Details

1. Ask the user for an issue title (required).
2. Accept an optional issue body describing the issue in detail.
3. Accept optional labels for the issue.

If the user provides all details upfront (e.g., "create an issue titled X about Y"), skip the interactive prompts and proceed to creation.

### Step 2: Create Issue

1. Create the issue immediately after collecting details:
   ```bash
   gh issue create --title "<title>" --label "<labels>" --body "<body>"
   ```
2. Display the created issue number and URL.

### Error Handling

If issue creation fails, display the error message returned by `gh issue create`.

## Mode 2: USDM Document Input

Create a hierarchy of issues from a USDM requirements document. This mode is triggered when the user provides a USDM document path and a parent issue number.

### Input

- **USDM document path**: Path to a Markdown file following USDM format (REQ/SPEC hierarchy).
- **Parent issue number**: The GitHub Issue under which top-level requirements are created as sub-issues.

### Step 1: Parse Requirements

1. Read the USDM document.
2. Extract all requirements (both top-level `REQ-NNN` and sub-requirements `REQ-NNN-N`).
3. For each requirement, collect:
   - ID and title
   - Reason
   - Description
   - Child specifications (SPEC) belonging to that requirement
   - Parent requirement (if it is a sub-requirement)
4. Display a summary of the extraction: total number of requirements and the list of REQ IDs. Proceed to creation unless the user explicitly aborts.

### Step 2: Create Issues Top-Down

Process the hierarchy top-down (parents before children) because `gh sub-issue add` requires the parent issue number.

For each requirement:

1. Create a GitHub Issue with label `usdm:req`.
2. The issue title follows the convention: `REQ-NNN: Title` or `REQ-NNN-N: Title`.
3. The issue body uses this template:

```markdown
## Reason

{Reason text from USDM document}

## Description

{Description text from USDM document}

## Specifications

| SPEC ID | Specification |
|---------|--------------|
| SPEC-NNN | {Specification text} |

## Source

- Document: [{document-id}]({link-to-document}) § {REQ-ID}
- Ticket: #{parent-issue-number}
```

4. Link the issue as a sub-issue:
   - Top-level REQs become sub-issues of the parent issue.
   - Sub-requirements become sub-issues of their parent requirement's issue.

```bash
gh issue create --title "REQ-001: Title" --label "usdm:req" --body "..."
gh sub-issue add <parent-issue-number> <new-issue-number>
```

5. Display the created issue number and URL after each creation.

### Step 3: Verify Hierarchy

After all issues are created, verify the hierarchy with `gh sub-issue list` on the parent issue and report the result to the user.

### Important Rules

- **Do not create separate issues for specifications (SPEC)**. Specifications are included in the parent requirement's issue body as a table.
- **Create `usdm:req` label** if it does not exist: `gh label create "usdm:req" --color 0075ca --description "USDM Requirement"`
- **Each issue is self-contained**: readable and understandable on its own, with a source reference link back to the USDM document.
- **Process top-down**: always create parent issues before children.

See `references/usdm-issue-mapping.md` for the full mapping guide.

## Before Finishing

After creating issues, review each one from a reader's perspective:

- **Self-contained?** Can someone understand this issue without access to the conversation or source document? If the issue body lacks context (reason, scope, acceptance criteria), add it before moving on.
- **Source traceable?** Does every issue link back to its origin (USDM document, idea document, or conversation context)? A reader should be able to find the full context if they need it.

## Constraints

- Do not create issues outside the current repository.
- Do not modify existing issues unless explicitly part of the USDM hierarchy creation.
- In USDM mode, display the count and REQ IDs before batch creation. Proceed unless the user aborts.
