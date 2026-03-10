---
name: eliteforge-git-specification
description: 统一执行璀璨工坊 Git 治理规范，覆盖分支模型、提交信息、MR 流程、发布与热修策略。用户提到 Git 规范、分支命名、rebase/merge 选择、MR 提交流程、squash 要求、commit message 校验、release 合并、hotfix 命名或冲突规避时使用。
---

# EliteForge Git Governance

## 目标

在 Git 操作任务中，优先调用内置脚本完成标准化操作；无法脚本化时再输出原生命令。始终保证分支策略、提交规范和 MR 门禁与团队规则一致。
任何“需要修改代码”的任务，必须先满足分支门禁，再允许编辑文件。

## 执行原则

1. 分支前置门禁（必做）  
先执行分支检查，未通过门禁时禁止改代码、禁止提交。

- 若任务包含代码修改，当前分支必须为：
  - 正常迭代：`feature/<version>/<developer>/<taskId>/<taskDesc>` 或 `bugfix/<version>/...`
  - 热修场景：`hotfix/<major.minor.x>-<MMDD>`
- 当前分支若是 `master`、`main`、`nightly`、`qa/<version>`、`release/<version>`，必须先新建并切换到合规分支。
- 仅在“只读查询/统计分析”任务中可跳过此门禁。

建议命令模板（正常迭代）：

```bash
git fetch -v -f -t --prune
base_ref="origin/master"
git show-ref --verify --quiet refs/remotes/origin/master || base_ref="origin/main"
git switch -c feature/<version>/<developer>/<taskId>/<taskDesc> "$base_ref"
```

2. 识别场景  
先判断是 `正常迭代`、`热修`、`分支整理`、`提交/MR 合规` 还是 `统计分析`。

3. 定位脚本目录（必做）  
不要假设当前仓库存在 `scripts/`。先定位 skill 自身目录下的脚本，再调用。

```bash
ELITEFORGE_GIT_SCRIPTS=""
for root in "$PWD" "${SKILLS_HOME:-}" "$HOME"; do
  [ -n "$root" ] || continue
  found="$(find "$root" -type d -path '*/eliteforge-git-specification/scripts' 2>/dev/null | head -n 1)"
  if [ -n "$found" ]; then
    ELITEFORGE_GIT_SCRIPTS="$found"
    break
  fi
done
[ -n "$ELITEFORGE_GIT_SCRIPTS" ] || { echo "Cannot locate eliteforge-git-specification/scripts." >&2; exit 1; }
```

4. 优先脚本  
若脚本已覆盖对应能力，优先调用脚本，不重复手写长命令流。

5. 严格门禁  
始终检查分支前置条件、是否需要 squash、MR/pipeline 状态与发布路径。

6. 结构化输出  
输出内容固定为：`结论`、`分支门禁检查`、`命令序列`、`风险与门禁`、`提交/MR 文案`。

## 脚本映射（优先使用）

1. 自动拉取与合并版本分支  
`bash "$ELITEFORGE_GIT_SCRIPTS/auto_merge" [--ff-only | --merge | --rebase]`  
适用：在 `qa/<version>` 或 `release/<version>` 分支上，批量合并对应 `feature/<version>/`、`bugfix/<version>/` 变更。

2. 检查指定版本分支合并状态  
`bash "$ELITEFORGE_GIT_SCRIPTS/check_merge" <version> <branch>`  
适用：核对 `feature/<version>` 和 `bugfix/<version>` 是否已合入目标分支（如 `release` 或 `qa`）。

3. 清理本地分支  
`bash "$ELITEFORGE_GIT_SCRIPTS/delete_local_branches"`  
适用：删除除 `master/main` 外的本地分支。

4. 清理已合并远程分支  
`bash "$ELITEFORGE_GIT_SCRIPTS/delete_merged_branches" <version>`  
适用：在 `release/<version>` 上识别并删除已合并 `feature/<version>` 分支。  
注意：该脚本包含交互确认。

5. 重命名分支  
`bash "$ELITEFORGE_GIT_SCRIPTS/rename_git_branch" <old-branch> <new-branch>`  
适用：本地分支重命名并同步远程。

6. 生成变更摘要  
`bash "$ELITEFORGE_GIT_SCRIPTS/git_change_summary.sh"`  
适用：输出相对 `master..HEAD` 的变更摘要（排除 `style/build/test`）。

7. 统计作者代码量  
`bash "$ELITEFORGE_GIT_SCRIPTS/user_code.sh" <base_dir> '<author1|author2|...>' <YYYY-MM-DD>`  
适用：按作者与起始日期统计多个仓库的增删改行数。

## 流程基线

- 一个需求一个 `feature/<version>/<developer>/<taskId>/<taskDesc>`。
- 任何代码改动前，先确认已在合规开发分支；禁止在 `master/main/nightly/qa/release` 直接开发。
- `feature` 提测到 `qa/<version>` 使用 MR；联调用 `nightly`。
- `feature` 合入 `release/<version>` 前先 squash 为单提交。
- `release/<version>` 合回 `master` 使用 `git merge --ff-only`。
- `hotfix/<major.minor.x>-<MMDD>` 仅用于现场阻塞问题。

## 提交与 MR 约束

- 提交格式：`<type>(<scope>): <subject>`。
- 当 `type` 为 `feat` 或 `fix`，`scope` 必须为 `#<ID>`。
- 最终 MR 前必须 squash；MR title 与 squash 后提交一致。
- 使用 `.gitlab/merge_request_templates/default.md` 并完成自检。
- pipeline 全绿后再通知 reviewer。

## 参考资料

- 需要完整规范与示例时读取 `references/git-governance-reference.md`。
