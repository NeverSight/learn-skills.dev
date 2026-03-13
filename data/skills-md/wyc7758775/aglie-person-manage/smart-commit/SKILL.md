---
name: smart-commit
description: 智能分析 git diff，根据相同业务逻辑将更改分为多个 commit，生成符合最佳实践的 commit message（带 Emoji 图标），并推送到远程分支。
voice:
  - 上传当前代码到远程仓库
  - 智能提交代码
  - 分批提交更改
  - smart commit
license: MIT
metadata:
  author: user
  version: "1.0.0"
---

# Smart Commit

此 skill 帮助代理智能地将代码更改分批提交，符合 Git 最佳实践。

## 工作流程

### 1. 获取当前更改
- 检查 git 状态：`git status`
- 获取完整差异：`git diff`（工作树）和 `git diff --staged`（已暂存）
- 如果有未暂存的更改，询问用户是否要先暂存

### 2. 分析更改内容

分析文件变更，识别业务逻辑分组。常见分组维度：
- **功能模块**：相同功能模块的文件分为一组
- **变更类型**：
  - ✨ 新功能 (feat)
  - 🐛 修复 bug (fix)
  - 📝 文档 (docs)
  - 🎨 样式 (style)
  - ♻️ 重构 (refactor)
  - ⚡ 性能 (perf)
  - ✅ 测试 (test)
  - 🔧 构建/工具 (chore)
  - 🚀 部署 (deploy)
- **文件关联**：具有依赖关系的文件应放在一起

### 3. 生成 Commit Messages

使用以下最佳实践格式：

```
<图标> <类型>(<范围>): <简短描述>

<详细描述（可选）>

<脚注（可选）>
```

常用图标与类型映射：
- ✨ `feat` - 新功能
- 🐛 `fix` - 修复 bug
- 📝 `docs` - 文档
- 🎨 `style` - 样式（不影响功能）
- ♻️ `refactor` - 重构（既不是新功能也不是修复）
- ⚡ `perf` - 性能优化
- ✅ `test` - 测试
- 🔧 `chore` - 构建过程或辅助工具变动
- 🚀 `deploy` - 部署
- 💄 `ui` - UI 样式更新

### 4. 执行分批提交

对于每个分组：
1. 添加相关文件：`git add <files>`
2. 创建提交：
   ```bash
   git commit -m "<图标> <类型>(<范围>): <描述>"
   ```
3. 提交后立即显示该 commit 的摘要

### 5. 推送到远程

所有 commit 创建完成后：
1. 获取当前分支名：`git branch --show-current`
2. 推送到远程：
   ```bash
   git push origin <branch-name>
   ```

## 重要约束

- **每次只处理一个分组**：先确认一个分组，再处理下一个
- **用户确认**：在提交每个分组前，简要说明该分组包含哪些文件的哪些更改，询问用户确认
- **不要合并不相关的更改**：如果某些更改不属于任何逻辑分组，单独处理
- **原子性提交**：每个 commit 应该只包含一个逻辑变更
- **清晰的描述**：描述应该是简洁的、行动导向的句子

## 示例

假设有以下更改：
- `src/app/page.tsx` - 添加新功能组件
- `src/app/lib/utils.ts` - 添加新工具函数
- `README.md` - 更新文档
- `src/styles/globals.css` - 样式调整

分析后分组：
1. **分组1**：feat - `src/app/page.tsx` + `src/app/lib/utils.ts`
2. **分组2**：docs - `README.md`
3. **分组3**：style - `src/styles/globals.css`

用户确认后依次提交并推送。
