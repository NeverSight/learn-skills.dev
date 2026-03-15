---
name: git-commit-gen
description: 根据 git status 和 git diff 自动生成符合规范的中文 commit message，支持 Conventional Commits 格式，包含模块名称。当用户说"生成 commit"、"生成提交信息"、"commit message"、"帮我写 commit"、"提交信息"、"git commit"时触发。不适用于：查看 git log、切换分支、合并冲突等通用 git 操作。
version: 1.1.0
author: snailuu
allowed-tools: Bash, Read, Write
---

# Git Commit 信息生成技能

## Commit 信息规范

本项目使用中文 Conventional Commits 格式：

```
<type>(<scope>): <subject>

[可选的详细描述]
```

### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| feat | 新功能 | feat(聊天对话): 新增消息引用功能 |
| fix | Bug 修复 | fix(聊天对话): 修复消息流式渲染问题 |
| docs | 文档变更 | docs(README): 更新安装说明 |
| style | 代码格式调整（不影响功能） | style(按钮): 调整按钮边距 |
| refactor | 重构（既不是新功能也不是修复） | refactor(API): 优化请求处理逻辑 |
| perf | 性能优化 | perf(列表): 优化虚拟滚动性能 |
| test | 测试相关 | test(工具函数): 添加单元测试 |
| build | 构建系统或外部依赖变更 | build(deps): 升级 React 到 18.3 |
| ci | CI 配置文件和脚本变更 | ci(github): 添加自动化测试流程 |
| chore | 其他不修改源码的变更 | chore(配置): 更新 eslint 规则 |

### Scope 范围

根据修改的模块确定：
- 可以是文件名、功能模块名或组件名
- 如果影响多个模块，使用主要模块或使用 `*` 表示全局

### Subject 主题

- 使用中文简洁描述，不超过 50 个字符
- 使用动词开头：修复、新增、优化、调整、更新等
- 不使用句号结尾

## 执行步骤

### 1. 检查 Git 状态

```bash
git status --short
```

如果工作区干净（无修改），提示用户没有需要提交的更改。

### 2. 分析变更内容

```bash
git diff --stat
git diff --cached
git diff
```

### 3. 参考项目历史 Commit

```bash
git log --oneline -10
```

确保生成的格式与项目现有风格一致。

### 4. 智能分析并生成 Commit Message

1. **确定 Type**：新增文件/功能 → feat，修复问题 → fix，代码重构 → refactor，性能优化 → perf，样式调整 → style，其他 → chore
2. **确定 Scope**：根据修改的主要文件路径推断模块名（如 `src/pages/chat/` → 聊天对话）
3. **生成 Subject**：总结主要修改内容，使用简洁的中文描述

### 5. 输出格式

生成 2-3 个候选 commit message，按推荐度排序。每个候选项后提供简短说明。

如果变更较复杂，附带多行详细描述。

详细输出示例和执行提交流程见 `references/examples.md`。

## 注意事项

- 如果有大量文件修改，建议用户分多次提交
- 提交信息要准确反映实际修改内容，避免模糊描述
- 多个不相关的修改建议分开提交
