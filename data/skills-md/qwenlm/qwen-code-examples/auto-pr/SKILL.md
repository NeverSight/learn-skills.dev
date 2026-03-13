---
name: auto-pr
description: Automated PR submission assistant, including code review, documentation generation, and PR creation
---

# Auto PR - Automated PR Submission Assistant

## Overview

This skill helps you automate the complete Pull Request process, including code review, documentation generation, and PR creation.

## Core Functions

1. **Update Base Branch** - Sync remote main/master branch
2. **Code Review Analysis** - Compare differences between current and base branch
3. **PR Template Discovery** - Automatically scan for PR templates in the project
4. **English Documentation Generation** - Generate English PR description, waiting for user confirmation
5. **Automatic PR Submission** - Create PR using English description after user approval
6. **Cleanup Process** - Offer to remove temporary PR description files after submission

## Usage

```
/auto-pr [base-branch]
```

- `base-branch`: Optional, defaults to `main`

## Workflow

Please execute the following workflows in sequence:

1. [Branch Preparation](./workflows/01-branch-preparation.md) ⭐⭐⭐
2. [Code Review](./workflows/02-code-review.md) ⭐⭐⭐
3. [Documentation Generation](./workflows/03-doc-generation.md) ⭐⭐⭐
4. [PR Submission](./workflows/04-pr-submission.md) ⭐⭐⭐

### Key Interaction Points

During the documentation generation phase, the process will pause to wait for user confirmation:

```
Branch Preparation → Code Review → Generate English Documentation → [Wait for User Confirmation] → Submit PR → [Clean Up Temporary Files]
```

**User Confirmation Points**:
- After English documentation is generated, wait for user review and confirmation
- After PR is submitted, confirm deletion of temporary description files (PR_DESCRIPTION.md, etc.)

## Prerequisites

### Environment Check

Before executing the skill, run the check script:

```bash
node ./scripts/check-prerequisites.js
```

### Dependency Requirements

| Dependency | Required | Installation Method |
|------------|----------|---------------------|
| Git | Yes | System built-in or `brew install git` |
| GitHub CLI | Yes | `brew install gh` |
| Node.js | Yes | `brew install node` |

### GitHub CLI Authentication

Complete authentication for first use:

```bash
gh auth login
```

Select as prompted:
1. GitHub.com
2. HTTPS
3. Use browser for authentication

After authentication, verify:

```bash
gh auth status
```

### Project Requirements

- [ ] Git repository initialized
- [ ] Remote repository configured
- [ ] Current branch is not main/master
- [ ] Unpushed commits exist

## Script Tools

This skill includes the following scripts:

| Script | Description |
|--------|-------------|
| `scripts/check-prerequisites.js` | Prerequisites check |
| `scripts/create-pr.js` | Automatic PR creation |

### Quick Start

```bash
node ./scripts/create-pr.js \
  --title "feat: feature description" \
  --body-file ./PR_DESCRIPTION.md
```

## Notes

- Ensure all changes are committed before execution
- PR descriptions will automatically search for templates in the project
- Supports GitHub (requires gh CLI installation)
- Temporary description files will be offered for deletion after PR submission
