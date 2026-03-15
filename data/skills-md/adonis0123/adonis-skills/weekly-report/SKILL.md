---
name: weekly-report
description: Generate structured weekly reports from Git commit history across one or multiple repositories. Use when you need concise, project-grouped progress summaries for status reporting.
allowed-tools: Read, Write, Bash(git:*), Bash(python:*)
metadata:
  author: adonis
  version: "1.0.0"
---

# 周报生成技能

自动读取 Git 提交记录，按项目分组生成结构化周报。

## 功能特性

- 自动读取 Git 提交记录
- 支持多仓库汇总
- 自动识别当前用户 (`git config user.name`)
- 按项目分组，生成结构化周报
- 过滤琐碎提交（typo、merge、format 等）
- 支持添加补充说明
- 周报统一存储在 `~/.weekly-reports/` 目录

## 使用方式

### 基本用法

在任意 Git 项目目录中执行：

```
/weekly-report
```

### 执行流程

1. **选择时间范围**
   - 本周 (显示具体日期，如 2026-01-06 ~ 2026-01-12)
   - 上周 (显示具体日期，如 2025-12-30 ~ 2026-01-05)
   - 前半年 (显示具体日期，如 2025-07-13 ~ 2026-01-13)
   - 自定义周报（输入周一日期）
   - 自定义时间段（输入起始日期，截止到今天）

   **重要**：选择时必须显示具体的日期范围，让用户确认是否正确

2. **选择仓库**（如已配置多仓库）
   - 显示已配置的仓库列表
   - 可多选要包含的仓库
   - 可添加当前目录为新仓库

3. **添加补充内容**（可选）
   - 输入额外的工作内容
   - 如：参与会议、技术分享等

4. **生成周报**
   - 读取选定仓库的 Git 提交（必须覆盖所有分支/远端跟踪分支，避免漏提交）
   - 按项目分组
   - 过滤琐碎提交
   - 生成 Markdown 格式周报
   - 在周报正文末尾自动追加"下周计划"模板（详见输出格式）
   - 周报保存到 `~/.weekly-reports/{year}/week-{week}.md`
   - 时间段报告保存到 `~/.weekly-reports/periods/{start_date}_to_{end_date}.md`

## Git 提交读取（重要）

为避免“只读取当前分支而漏掉其它分支（例如 `credits-lite*`）”的问题，读取提交时必须使用 `--all`（覆盖本地分支 + 远端跟踪分支），并确保截止时间包含结束日当天：

```bash
# 关键点：
# - 用 --all 覆盖所有本地 refs（包含 remotes/origin/*）
# - --until 用 “结束日 23:59:59” 避免漏掉结束日当天提交
# - --author 建议用 name + email 联合匹配，避免不同身份写法漏掉本人提交

AUTHOR_PATTERN="(your-name|your@email.com)"  # 或仅用你的 name/email
git log --all \
  --author="$AUTHOR_PATTERN" \
  --since="$START_DATE 00:00:00" \
  --until="$END_DATE 23:59:59" \
  --pretty=format:"%H|%s|%an|%ad" \
  --date=short
```

如果 `git branch -a` 看不到目标远端分支（说明本地没有对应的远端跟踪引用），需要先 `git fetch --all --prune`（在用户同意且网络可用时执行），否则无法读取到“本地不存在的分支”的提交。

## 输出格式

周报采用层级列表结构，**必须包含日期范围标题**，按项目分组：

### 周报格式

```markdown
# 周报 (2026-01-06 ~ 2026-01-12)

项目名称
  - 主要工作点（10字以内）
    - 补充说明（可选）
  - 另一个工作点

其他
  - 不属于特定项目的工作内容

下周计划
项目名称
-
```

### 时间段报告格式

时间段报告**不追加**"下周计划"模板（因为不是周维度）。

```markdown
# 工作总结 (2025-07-13 ~ 2026-01-13)

项目名称
  - 主要工作点（10字以内）
    - 补充说明（可选）
  - 另一个工作点

其他
  - 不属于特定项目的工作内容
```

### "下周计划"模板规则

周报正文生成完毕后，在末尾追加"下周计划"区块：

1. 标题行固定为 `下周计划`（无 `#` 前缀，与项目名同级）
2. 从本周周报正文中提取所有出现过的项目名（不含"其他"），按原顺序列出
3. 每个项目名下放一行 `-` 作为占位符，方便用户后续填写
4. 如果用户在交互中主动提供了下周计划内容，直接填入对应项目下，不再使用占位符

### 示例输出

```markdown
# 周报 (2026-01-06 ~ 2026-01-12)

project-frontend
  - 构建工具升级改造
  - 核心功能开发流程跟进
    - 方案合理性优化
  - 脚本国际化优化

project-backend
  - 自定义类型化消息渲染
  - 断线重连流程梳理

其他
  - 新版国际化方案讨论

下周计划
project-frontend
-
project-backend
-
```

## 配置文件

配置文件位于 `~/.weekly-reports/config.json`：

```json
{
  "repos": [
    {
      "name": "project-a",
      "path": "/home/user/projects/project-a"
    },
    {
      "name": "project-b",
      "path": "/home/user/projects/project-b"
    }
  ],
  "default_author": "auto",
  "output_format": "markdown"
}
```

## 总结原则

### 必须遵守

- **事实导向**：只总结实际完成的工作
- **简洁精炼**：主要工作点控制在 10 字以内
- **重点突出**：过滤琐碎修改
- **按项目分组**：相同项目的工作归类
- **层级清晰**：用缩进表示从属关系

### 过滤规则

以下提交不会单独列出：
- 纯格式化/代码风格调整
- 简单的 typo 修复
- 依赖版本小幅更新
- Merge 提交
- 重复性的相似提交

详细格式规范见 [周报格式规范](references/WEEKLY_REPORT_FORMAT.md)
