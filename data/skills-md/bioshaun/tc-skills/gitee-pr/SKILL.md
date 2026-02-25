---
name: gitee-pr
description: Create and submit Gitee pull requests with team convention enforcement. Use when the user asks to open/submit a Gitee PR on gitee.com and needs an automated flow that validates branch naming, commit prefixes, clean working tree, optional auto-commit, branch push, and PR creation.
---

# Gitee PR

Use `scripts/create_gitee_pr.py` to execute a rules-first PR workflow.
Apply team rules from `gitee-pr-rules.md` before creating PR.

## Rule Files

- Main rules: `gitee-pr-rules.md`

## Required Inputs

- Set Gitee token: `GITEE_TOKEN` or `--token`.
- Ensure remote is a Gitee repo or provide `--repo owner/repo`.
- Run command inside a Git repository.

## Workflow

1. Resolve `head` and `base` branches.
2. Enforce branch naming format: `member/verb-description`.
3. Ensure working tree is clean before PR (or auto-commit when `--auto-commit` is enabled).
4. Validate all commit subjects in `remote/base..head` with allowed prefixes:
   - `feat:`
   - `fix:`
   - `docs:`
   - `refactor:`
   - `style:`
   - `test:`
   - `chore:`
5. Warn (non-blocking) when multiple core files are changed.
6. Enforce Chinese PR content: title and body must include Chinese text.
7. Enforce PR body template sections and order:
   - `## 改动了什么？`
   - `## 为什么改动？`
   - `## 测试结果？`
   - `## 注意事项`
8. Push branch unless `--no-push`.
9. Create PR via Gitee API and print PR URL.

## Recommended Commands

```bash
export GITEE_TOKEN="<token>"
python3 scripts/create_gitee_pr.py \
  --base main \
  --title "修复：优化过滤逻辑"
```

```bash
# Auto-commit local changes before PR checks
python3 scripts/create_gitee_pr.py \
  --auto-commit \
  --commit-message "chore: prepare gitee pr changes" \
  --base main
```

```bash
# Validate checks and preview generated PR body without API call
python3 scripts/create_gitee_pr.py --base main --dry-run --no-push
```

```bash
# Keep custom body (must follow required template sections)
python3 scripts/create_gitee_pr.py \
  --base main \
  --body "$(cat pr-body.md)"
```

## Default PR Body Template

When `--body` is not provided, script generates:

```markdown
## 改动了什么？
- <commit summaries>

## 为什么改动？
- 请补充本次改动的业务背景和目标。

## 测试结果？
- 已检查提交前工作区为干净状态。
- 请补充本地测试命令与结果。

## 注意事项
- 无
```

## Merge Cleanup

After PR merge, clean branch:

```bash
git branch -d <branch-name>
git push origin --delete <branch-name>
```
