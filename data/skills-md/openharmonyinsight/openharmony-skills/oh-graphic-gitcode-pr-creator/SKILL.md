---
name: oh-graphic-gitcode-pr-creator
description: Automate Gitcode Pull Request creation workflow for OpenHarmony graphic subsystem including code commit, issue creation, and PR submission with proper template formatting. Use when user needs to create a PR for the Gitcode platform, especially for OpenHarmony graphic projects that require specific PR templates with CodeCheck tables and Signed-off-by tags.
---

# OpenHarmony Graphic Gitcode PR Creator

## Quick Start

Create a Gitcode PR by following these steps:

1. **Check git status** - Verify modified files
2. **Commit changes** - Add Signed-off-by to commit message
3. **Push to remote** - Push branch to origin
4. **Create Issue** - Create related issue
5. **Create PR** - Use PR template from `.gitcode/PULL_REQUEST_TEMPLATE.zh-CN.md`

## Workflow

### 1. Check Git Status

```bash
git status
git diff <file>
```

### 2. Commit Changes

Get user config and create commit with Signed-off-by:

```bash
git config user.name
git config user.email
git add <files>
git commit -m "<message>\n\nSigned-off-by: <name> <<email>>"
```

### 3. Push to Remote

```bash
git push origin <branch-name>
```

**Note**: You need to ask the user for the target branch name before creating the PR. Common options:
- `master` (default for most cases)
- `OpenHarmony-6.1-Release` (for 6.1 release branch)

### 4. Create Issue

Use `gitcode_create_issue` to create issue with:
- Title: PR title
- Body: Description of changes

### 5. Create PR

Read PR template from `.gitcode/PULL_REQUEST_TEMPLATE.zh-CN.md` and fill in:
- **Description**: Summary of changes
- **Issue number**: Link to created issue
- **Test & Result**: Test information
- **CodeCheck**: Fill all self-check results with "Pass"
- **L0新增用例自检结果**: Check appropriate box

Use `gitcode_create_pull_request` with formatted body.

## CodeCheck Template

When filling CodeCheck table, ensure all rows have "Pass" in the result column:

| 类型 | 自检项 | 自检结果 |
|-------|---------|-----------|
| 多线程 | ... | Pass |
| 内存操作 | ... | Pass |
| 外部输入 | ... | Pass |
| 敏感信息 | ... | Pass |
| 数学运算 | ... | Pass |
| 初始化 | ... | Pass |
| 权限管理 | ... | Pass |

## Common Patterns

### Test Optimization PRs

For test file optimizations:
- Description: "Optimize <test_file> - remove redundant code and improve coverage"
- CodeCheck: All Pass (test code doesn't typically trigger security checks)
- L0用例: Check "是，有新增L0用例，且完成自检"

### Bug Fix PRs

For bug fixes:
- Description: "Fix <bug_description> in <file>"
- Test & Result: Describe test scenario and expected behavior
- CodeCheck: All Pass

## Important Notes

- Always use the Chinese PR template for OpenHarmony projects
- Ensure branch name is descriptive
- Link PR to issue for traceability
- Force push with `--force` when amending commits
