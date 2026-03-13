---
name: rebase2main
description: "将当前开发分支（通常是 dev）的提交通过 git rebase 同步到 main 分支，推送到远端，然后切回原分支。当用户提及「同步到 main」「rebase 到 main」「更新 main」「推送到主分支」「把 dev 合到 main」等关键词时使用此技能。即使用户没有明确说 rebase，只要意图是把开发分支内容同步到 main，就应触发此技能。"
user-invocable: true
metadata:
  version: "0.1.0"
---

# Rebase to Main

将当前开发分支的提交以 rebase 方式同步到 main 分支，推送远端，再切回原分支。

## 工作流程

1. **记录当前分支名称**

   ```bash
   git branch --show-current
   ```

   将结果保存，后续用于切回。如果当前已在 main 分支，提示用户并终止。

2. **确认工作树干净**

   ```bash
   git status
   ```

   如果存在未提交的变更，提示用户先处理（提交或暂存），不要继续。

3. **切换到 main 分支**

   ```bash
   git checkout main
   ```

4. **将 dev 的提交 rebase 到 main**

   ```bash
   git rebase <原分支名>
   ```

   如果出现冲突，停止并告知用户需要手动解决。

5. **推送 main 到远端**

   ```bash
   git push origin main
   ```

   使用普通 push，不使用 `--force`。如果 push 失败，告知用户原因。

6. **切回原分支**
   ```bash
   git checkout <原分支名>
   ```

## 注意事项

- 不使用 `--force` 推送，保证远端历史安全
- 如果 rebase 过程中出现冲突，立即停止并告知用户
- 执行前必须确认工作树干净（无未提交变更）
