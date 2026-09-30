---
name: novel-integration-merge
description: 用 Novel 的 fix/niudieyi-merge-issue 过渡分支处理开发或功能分支合入 dev/test 的冲突。用于“走过渡分支合 dev/test”“重置到 origin/dev 或 origin/test 后合源分支并强推”等完整集成请求，也支持只报告冲突范围。不用于直接发布 dev/test/master 或普通功能分支同步。
---

# Novel 集成冲突过渡分支

目的：在 `fix/niudieyi-merge-issue` 上制作可合入 dev/test 的结果，保留源分支本身的历史。

```text
origin/dev 或 origin/test
    ↓ reset 当前过渡分支
合并指定源分支 → 解决冲突 → 验证 → 合并提交
    ↓ force-with-lease
origin/fix/niudieyi-merge-issue
```

## 输入与授权

- **目标基线**：`origin/dev` 或 `origin/test`，由用户本次请求或明确的当前上下文决定。缺失就问，不沿用上次任务的目标。
- **源分支**：用户指定的开发/功能分支，常见 `niudieyi-dev`。本地分支名就合本地版本；只有用户明确给出远端 ref 才合远端版本。缺失且上下文不明确时问。
- **过渡分支**：固定 `fix/niudieyi-merge-issue`，远端固定为 `origin` 的同名分支。

用户明确调用本 skill 执行完整流程（例如“用 novel-integration-merge 把 niudieyi-dev 合到 dev”），就是对本次过渡分支 **reset、merge、冲突解决、commit 和强推** 的授权。开始时简述目标、源和推送位置，随后连续完成，不逐步重复确认。自动发现本 skill、询问用法或要求创建/修改 skill，本身不授权这些 Git 操作。

用户的局部要求优先：
- “先看冲突、别解决”：只完成重置和试合并，报告范围后保留现场。
- “只重置”“只解决”“不提交”“不推送”：严格停在指定边界。
- 普通“提交并推送”不能自动升级成完整重建和强推；已有的明确授权在本次流程内持续有效。

本流程不直接推送 dev/test/master，不建立 PR、不合入目标分支、不部署，也不把过渡分支反向合回源分支。

## 1. 检查与固定版本

在当前目录操作，遵守当前 AGENTS.md 和 `docs/rules/branching.md`；不另开 worktree。

1. 检查 `git status --porcelain`、`git branch --show-current`、`git remote -v`，确认仓库是 Novel、当前分支恰为 `fix/niudieyi-merge-issue`。分支不符时说明实际位置并让用户确定，不在开发分支上执行 reset。
2. 工作区必须干净且没有进行中的 merge/rebase。若是本次流程的续做，直接继续既有现场，不再 reset；若来源不明，先报告。未提交内容需用户决定如何保留，不能自动清理、覆盖或 stash。
3. `git fetch origin` 更新远端引用；失败就停。验证目标和源均存在且指向 commit，源不能是当前过渡分支。
4. **在 reset 前**记录：原 HEAD、目标 SHA、源 SHA，以及 `git ls-remote --heads origin refs/heads/fix/niudieyi-merge-issue` 返回的远端过渡分支 SHA，后者作为本次固定 lease。远端不存在则期望值为空；命令失败不等于分支不存在。

后续操作使用这次记录的 SHA，避免其他任务移动源分支或后台 fetch 改变推送保护依据。保存原 HEAD 供必要时恢复，不自动创建备份分支。

## 2. 重置与试合并

以下变量由上一节的检查赋值，不直接粘贴未校验的用户文本：

```bash
git reset --hard "$target_sha"
git merge --no-commit --no-ff "$source_sha"
```

重置只影响当前过渡分支；不执行 `git clean`。确认 reset 成功才执行 merge。

- 有冲突：用 `git diff --name-only --diff-filter=U` 和 `git diff --cc` 列出文件、冲突块和功能范围。
- 退出码非零但没有未合并文件：按实际错误处理，不能当成普通冲突继续提交。
- 已包含源提交：不制造空提交；完整流程仍需将重建后的分支按授权推到远端。
- 用户只要求看冲突：报告源/目标 SHA、文件及冲突含义，停在现场，连无冲突合并也不自动提交。

## 3. 解决与验证

默认逐块理解双方意图，结合调用点、提交历史和测试保留兼容功能，不整仓使用 ours/theirs。用户明确要求某块“以源分支为准”时按该范围处理；不要把上次的选择或对某位作者的判断泛化到本次。

关注冲突附近的自动合并：删掉 import、参数或辅助函数时，确认对应调用、权限和行为是否一起变化。Git 没报文本冲突不代表行为没有退化。不借解决冲突重做无关业务。

修改对应模块前读取项目要求的 ref 文档。验证遵守 `docs/rules/ai-self-verify.md` 和用户当前目录优先约定，优先运行受影响的测试/类型检查，不为简单合并启动整套服务。

验收：
- 无未解决的 index 条目或残留冲突标记。
- 定向测试通过；若存在基线失败，用同范围证据区分，不能把新失败说成旧问题。
- `git diff --check` 以及暂存后的 `git diff --cached --check` 通过。

新引入的失败先修复；无法解释的失败或两边行为无法兼容时，报告具体证据和待决定项，保留现场。

## 4. 提交

暂存全部本次合并内容，排除测试生成物；意外出现的外部改动先调查，不能混进合并。按 `git-commit` skill 使用英文 Conventional Commit 消息，例如：

```text
chore: merge niudieyi-dev into dev-based integration branch
```

只完成本次合并的一个提交，不 amend，不跳过 hooks。提交失败就停，不推送。检查源 SHA 和目标 SHA 均为最终 HEAD 的祖先，且工作区干净。

## 5. 强推过渡分支

完整流程已明确授权强推，不先试一个注定可能 non-fast-forward 的普通 push，也不 pull/rebase 旧过渡分支历史。使用精确 lease 实现用户的 `push -f` 意图：

```bash
git push -u \
  --force-with-lease="refs/heads/fix/niudieyi-merge-issue:$expected_remote_sha" \
  origin HEAD:refs/heads/fix/niudieyi-merge-issue
```

执行前再次确认当前分支名、HEAD 和目标。检查远端目标基线是否仍等于本次 `target_sha`；若已推进，报告需要重新基于新目标合并，不悄悄发布旧基线结果。

`expected_remote_sha` 使用步骤 1 记录的值；空值表示只允许创建尚不存在的分支。lease 拒绝说明远端已变化，立即停止并展示差异，不更新 lease 后自动重试，也不降级成裸 `--force`。

成功后用 `git ls-remote` 核对远端同名分支 SHA 等于本地 HEAD。报告目标基线、源分支、解决了什么、验证结果、最终提交和推送位置；不要把“推送过渡分支”说成“已合入 dev/test”。
