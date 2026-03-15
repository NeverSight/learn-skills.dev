---
name: ai-code-stats
description: "统计代码的 AI 生成比例，并生成个人报告。支持最新 commit、暂存区、指定 commit 和 commit 范围多种模式"
version: "1.2.0"
author: "Lingma"
tags: ["ai-code", "statistics", "git", "pre-commit", "post-commit", "report"]
trigger: manual
---

## 技能描述

这是一个用于统计代码中 AI 生成比例的 skill。它支持多种统计模式（最新 commit、暂存区、指定 commit、commit 范围），能够识别 AI 生成的代码标记，并生成详细的个人报告。

**触发命令**: `/ai-stats [command] [options]` 或 `/aistats [command] [options]`

## 命令用法

### 子命令模式（推荐）

```
/ai-stats                              # 默认：统计最新 commit
/ai-stats staged                       # 统计暂存区内容
/ai-stats commit <hash>                # 统计指定 commit
/ai-stats range <hash1>..<hash2>       # 统计 commit 范围
```

**完整参数格式**：
```
/ai-stats [command] [commit-hash|range] [task-name] [git-username]
```

### 兼容模式（旧用法）

```
/ai-stats                              # 使用默认 commit message 和 Git 用户名
/ai-stats "用户管理模块"                # 指定需求名，使用默认 Git 用户名
/ai-stats "用户管理模块" aurorayang     # 指定需求名和用户名
```

## 子命令详解

### 1. 最新 Commit 统计（默认）

统计最近一次 commit 的代码变更。

```bash
# 基本用法
/ai-stats

# 指定需求名
/ai-stats "用户管理模块"

# 指定需求名和用户名
/ai-stats "用户管理模块" aurorayang
```

### 2. 暂存区统计

统计当前暂存区（staged）的代码变更。

```bash
# 基本用法
/ai-stats staged

# 指定需求名
/ai-stats staged "用户管理模块"

# 指定需求名和用户名
/ai-stats staged "用户管理模块" aurorayang
```

### 3. 指定 Commit 统计

统计特定 commit hash 的代码变更。

```bash
# 基本用法
/ai-stats commit abc1234

# 指定需求名
/ai-stats commit abc1234 "用户管理模块"

# 指定需求名和用户名
/ai-stats commit abc1234 "用户管理模块" aurorayang
```

### 4. Commit 范围统计

统计两个 commit 之间的所有代码变更。

```bash
# 基本用法
/ai-stats range abc1234..def5678

# 指定需求名
/ai-stats range abc1234..def5678 "用户管理模块"

# 指定需求名和用户名
/ai-stats range abc1234..def5678 "用户管理模块" aurorayang
```

## 参数说明

| 参数 | 位置 | 说明 | 默认值 |
|------|------|------|--------|
| `command` | 第1个 | 子命令：`staged`、`commit`、`range` 或省略 | 省略=最新 commit |
| `commit-hash` | 第2个 | 当 command 为 `commit` 时的目标 hash | - |
| `range` | 第2个 | 当 command 为 `range` 时的范围，格式 `hash1..hash2` | - |
| `task-name` | 倒数第2个 | 需求/任务名称 | 当前 commit message |
| `git-username` | 最后1个 | Git 用户名 | `git config user.name` |

**报告命名规则**：
- 有需求名：`ai-code-report-YYYY-MM-DD-需求名.md`
- 无需求名：`ai-code-report-YYYY-MM-DD-HHmmss.md`

**重复需求处理**：
- 相同需求名的报告会自动更新，而不是创建新文件
- 更新时会保留原文件，更新内容和统计信息

## 功能特性

- **多模式支持**：最新 commit、暂存区、指定 commit、commit 范围
- 自动检测代码变更
- 识别 AI 生成代码标记（`@ai-generated`、`@ai-generated-start/end`）
- 统计 AI 生成代码与人工编写代码的比例
- 生成个人专属报告（按登录用户名分类存储）
- 支持多种文件类型（.ts, .tsx, .js, .jsx, .mpx, .vue 等）

## 执行流程

### 1. 解析命令参数
- 识别子命令（staged/commit/range）
- 提取 commit hash 或范围
- 获取需求名和用户名

### 2. 获取用户信息
- 通过 `git config user.name` 获取当前 Git 用户名
- 作为报告存储目录名称

### 3. 收集代码变更
根据模式选择不同的 Git 命令：
- **最新 commit**: `git show --numstat HEAD`
- **暂存区**: `git diff --cached --numstat`
- **指定 commit**: `git show --numstat <hash>`
- **Commit 范围**: `git diff --numstat <range>`

### 4. 识别 AI 生成代码
- 扫描文件头部的 `@ai-generated` 标记
- 扫描文件中的 `@ai-generated-start` 和 `@ai-generated-end` 标记
- 统计 AI 生成的代码行数

### 5. 计算统计数据
- 总变更文件数
- 总新增行数 / 总删除行数
- AI 生成文件数 / AI 生成行数
- AI 代码占比（按文件数和行数分别计算）

### 6. 生成个人报告
- **报告路径**: `{project-root}/AI-Generate/{username}/`
- **文件名格式**: `ai-code-report-{YYYY-MM-DD-需求名}.md`
- **内容包含**:
  - 本次提交统计摘要
  - AI 生成代码详细清单
  - 文件级别统计
  - 历史累计统计（如存在历史报告）

## 报告内容结构

```
# AI 代码生成统计报告

**生成时间**: YYYY-MM-DD HH:mm:ss
**统计人**: {username}
**提交哈希**: {commit-hash}
**提交信息**: {commit-message}

---

## 统计摘要

| 指标 | 数值 |
|------|------|
| 变更文件总数 | {n} |
| 新增代码行数 | {n} |
| 删除代码行数 | {n} |
| AI 生成文件数 | {n} |
| AI 生成代码行数 | {n} |
| **AI 代码占比** | **{x}%** |

---

## AI 生成文件清单

### 新增文件（AI 生成）

| 序号 | 文件路径 | 类型 | AI 生成行数 |
|------|----------|------|-------------|
| 1 | `src/...` | TypeScript | 150 |

### 修改文件（含 AI 生成部分）

| 序号 | 文件路径 | AI 生成行数 | 修改说明 |
|------|----------|-------------|----------|
| 1 | `src/...` | 45 | 新增函数 |

---

## 文件详细统计

### {文件路径}
- 文件类型: {type}
- 新增行数: {n}
- 删除行数: {n}
- AI 生成行数: {n}
- AI 占比: {x}%

---

## 历史累计统计

| 指标 | 本次 | 累计 | 总计 |
|------|------|------|------|
| 提交次数 | 1 | {n} | {n} |
| AI 生成文件数 | {n} | {n} | {n} |
| AI 生成代码行数 | {n} | {n} | {n} |

---

*报告由 AI Code Stats Skill 自动生成*
```

## 使用方法

### 手动触发

```bash
# 默认：统计最新 commit
/ai-stats

# 统计暂存区
/ai-stats staged

# 统计指定 commit
/ai-stats commit abc1234

# 统计 commit 范围
/ai-stats range abc1234..def5678

# 指定需求名和用户名
/ai-stats commit abc1234 "用户管理模块" aurorayang
```

### 作为 pre-commit hook

可以在 `.git/hooks/pre-commit` 中添加：
```bash
#!/bin/bash
# 调用 AI 代码统计
echo "正在统计 AI 生成代码..."
node .lingma/skills/ai-code-stats/ai-code-stats.js staged
```

### 直接运行脚本

```bash
# 最新 commit
node .lingma/skills/ai-code-stats/ai-code-stats.js

# 暂存区
node .lingma/skills/ai-code-stats/ai-code-stats.js staged

# 指定 commit
node .lingma/skills/ai-code-stats/ai-code-stats.js commit abc1234

# commit 范围
node .lingma/skills/ai-code-stats/ai-code-stats.js range abc1234..def5678

# 完整参数示例
node .lingma/skills/ai-code-stats/ai-code-stats.js commit abc1234 "用户管理模块" aurorayang
```

## AI 代码标记识别规则

### 1. 完整 AI 生成文件标记
```
/**
 * @ai-generated
 * @date 2024-01-15
 * @description 用户管理模块
 */
```

### 2. 部分 AI 生成代码标记
```
// @ai-generated-start
// 这部分代码由 AI 生成
function autoGenerated() {
  // ...
}
// @ai-generated-end
```

## 输出示例

### 控制台输出
```
🔍 AI 代码统计
================
统计人: zhangsan
需求名称: 用户管理模块 (命令行指定)

📋 模式: 指定 Commit 检查 (abc1234)
变更文件: 5 个
新增行数: 320 行
删除行数: 45 行

🤖 AI 生成统计
================
AI 生成文件: 2 个
AI 生成行数: 180 行
AI 代码占比: 56.3%

📄 报告已生成
================
模式: 新建报告
路径: AI-Generate/zhangsan/ai-code-report-2024-01-15-用户管理模块.md
```

## 报告存储结构

```
{project-root}/
└── AI-Generate/
    ├── zhangsan/
    │   ├── ai-code-report-2024-01-15-143022.md
    │   ├── ai-code-report-2024-01-16-092145.md
    │   └── summary.md (累计统计)
    ├── lisi/
    │   └── ai-code-report-2024-01-15-161530.md
    └── ...
```

## 技术实现

### 使用的 Git 命令

#### 最新 Commit 模式
```bash
git show --numstat --format= HEAD
git show HEAD -- "{file}"
```

#### 暂存区模式
```bash
git diff --cached --numstat
git diff --cached -- "{file}"
```

#### 指定 Commit 模式
```bash
git show --numstat --format= {hash}
git show {hash} -- "{file}"
```

#### Commit 范围模式
```bash
git diff --numstat {hash1}..{hash2}
git diff {hash1}..{hash2} -- "{file}"
```

### 通用命令
```bash
# 获取当前用户名
git config user.name

# 获取即将提交的 commit 信息
git log -1 --pretty=format:%s HEAD

# 获取暂存区 tree hash
git write-tree
```

### 文件检测逻辑
1. 根据模式选择对应的 Git 命令获取变更
2. 读取每个变更文件的内容
3. 检查文件头部是否包含 `@ai-generated` 标记
4. 扫描文件内容中的 `@ai-generated-start` 和 `@ai-generated-end` 标记对
5. 计算标记范围内的代码行数
6. 累加得到 AI 生成代码总行数

## 配置选项

### 支持的文件类型
- `.ts` - TypeScript
- `.tsx` - TypeScript React
- `.js` - JavaScript
- `.jsx` - JavaScript React
- `.mpx` - MPX 小程序框架
- `.vue` - Vue 单文件组件
- `.less` / `.scss` / `.css` - 样式文件
- `.json` - JSON 文件
- `.md` - Markdown 文件

### 排除路径
以下路径的文件会被自动排除：
- `node_modules/`
- `dist/`
- `build/`
- `.git/`
- `.lingma/`
- `AI-Generate/`（避免自引用）

## 注意事项

1. **模式选择**：
   - `staged` 模式检查暂存区内容，适合 pre-commit 场景
   - `commit` 模式检查已提交的特定 commit
   - `range` 模式适合统计一个功能分支的所有变更

2. **确保 Git 配置正确**：需要正确设置 `user.name` 才能生成个人报告

3. **标记必须规范**：AI 生成代码需要按照规范添加标记才能被正确识别

4. **报告不会自动提交**：生成的报告文件需要手动添加到暂存区

5. **重复统计防护**：
   - 相同 commit hash 不会重复生成报告
   - 相同文件内容（blob hash）不会重复统计

## 版本历史

### v1.2.0
- 新增子命令支持：`staged`、`commit`、`range`
- 支持统计指定 commit 的代码
- 支持统计 commit 范围的代码
- 优化参数解析逻辑，兼容旧用法

### v1.1.0
- 新增用户名参数支持
- 支持 `/ai-stats [task-name] [username]` 格式
- 不传参数时默认使用 Git 用户名

### v1.0.0
- 初始版本
- 支持暂存区 AI 代码统计
- 生成个人专属报告
- 支持历史累计统计
