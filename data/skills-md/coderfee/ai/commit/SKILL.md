---
name: commit
description: Git 提交工作流，当用户需要提交代码、生成规范提交消息、拆分多模块改动时使用。
---

# commit

执行标准化的 Git 提交流程，确保提交历史符合 Conventional Commit Messages。

## 工作流程

1. **分析更改**: 运行 `git status` 和 `git diff` 识别改动逻辑。
2. **逻辑分组**: 将不同功能或模块的更改拆分为独立的提交，严禁一次性提交不相关的改动。
3. **生成消息**: 为每组更改生成**全英文**的规范消息。
4. **自动执行**: 按顺序执行 `git add .` (或特定文件) 和 `git commit -m "<message>"`。
5. **安全推送**: 完成所有本地提交后，执行 `git push`。
6. **异常处理**: 提交失败时自动回滚暂存区，推送前需用户确认。
7. **钩子处理**: 自动识别并处理 pre-commit 钩子修改的文件。

## 消息规范

- **语言**: 必须使用**英文 (English)**。
- **格式**: `<type>(<scope>): <subject>`
  - **Type**: 必须从以下范围选择：
    - `feat`: New feature
    - `fix`: Bug fix
    - `docs`: Documentation only changes
    - `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
    - `refactor`: A code change that neither fixes a bug nor adds a feature
    - `perf`: A code change that improves performance
    - `test`: Adding missing tests or correcting existing tests
    - `chore`: Changes to the build process or auxiliary tools and libraries
  - **Scope**: 可选，小写英文，指出改动范围（如：auth, parser, user-api）。
  - **Subject**: 
    - 使用祈使句（Imperative mood），首字母不要大写。
    - 结尾不要加句号 `.`。
    - 简洁明了，控制在 50 字符以内。

## 约束规则

- **严禁使用 Emoji**: 保持纯文本格式。
- **严禁 Force Push**: 确保远程分支安全。
- **单行模式**: 消息必须是单行，严禁换行或正文描述。
- **提交修改规则**: 远程已推送的提交禁止使用 --amend 修改。
- **文件暂存规则**: 优先按分组添加特定文件，避免使用 git add . 包含无关内容。

## 示例

- `feat(auth): add google oauth2 support`
- `fix(db): resolve connection leak in production`
- `refactor(utils): simplify date format logic`
