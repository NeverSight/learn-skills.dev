---
name: vcs-branch
description: Git branch naming convention format and strategy.
---

# VCS Branching

## Format
`<type>/<issue-number>-<short-description>`

### Types
- `feat/` - New feature
- `fix/` - Bug fix  
- `refactor/` - Code refactoring
- `docs/` - Documentation
- `test/` - Tests
- `chore/` - Maintenance

## Workflow
1. **Identify**: Find the related issue number and platform (GitHub/GitLab).
2. **Drafting**:
   - Use lowercase and kebab-case.
   - 3-6 words for description.
3. **MITM Confirmation**: ALWAYS present the drafted branch name to the USER for approval before creation.
4. **Execution**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b <branch-name>
   ```

## Guidelines
- **English Only**: Branch descriptions must be in English.
- **Sync**: Always pull the latest changes from the base branch before creating a new one.
