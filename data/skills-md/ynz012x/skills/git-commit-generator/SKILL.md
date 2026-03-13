---
name: git-commit-generator
description: 分析 git 暂存区变更内容，自动推断提交类型（type）和作用域（scope），生成符合 Conventional Commits v1.0.0 规范的中文提交消息，并执行 git commit。
disable-model-invocation: true
---

# Git Commit Generator

分析暂存区变更，生成 Conventional Commits 规范的中文提交消息并自动提交。

## 流程概述

1. 检查前置条件 - 确认暂存区有内容可提交
2. 收集变更信息 - 获取暂存区 diff 和文件列表
3. 推断 type 和 scope - 根据变更内容智能推断
4. 生成并提交 - 生成中文消息后直接执行 git commit

完整规范参考：[references/conventional-commits-spec.md](references/conventional-commits-spec.md)

---

## Step 1: 检查前置条件

运行 `git status --porcelain` 检查暂存区状态。

- 存在暂存文件（行首为 `M `、`A `、`D `、`R ` 等）时继续
- 无暂存文件时提示用户先 `git add`，**终止流程**
- 检测到 `.git/MERGE_HEAD` 存在时提示这是 merge commit，**终止流程**（用户应使用 git 默认消息）
- 检测到 `.git/REBASE_HEAD` 存在时提示当前处于 rebase 状态，**终止流程**

## Step 2: 收集变更信息

### 基础信息（始终读取）

```bash
git diff --cached --name-status    # 变更文件列表和状态（M/A/D/R）
git diff --cached --stat           # 变更统计摘要
git log --oneline -5               # 近期提交风格参考
```

### 详细 diff（按条件读取）

根据变更规模决定是否读取详细 diff：

| 变更规模 | 判定条件 | 读取策略 |
|----------|----------|----------|
| 小型 | 文件数 ≤ 10 且 stat 显示总行数 ≤ 300 | 完整读取 `git diff --cached` |
| 中型 | 文件数 ≤ 20 或总行数 ≤ 500 | 仅读取前 10 个文件的 diff |
| 大型 | 文件数 > 20 或总行数 > 500 | 不读取详细 diff，仅基于 name-status 和 stat 推断 |

## Step 3: 推断 type 和 scope

### Type 推断

按优先级从高到低判断：

| 优先级 | 条件 | Type |
|--------|------|------|
| 1 | 所有变更文件在 `test/` 或 `tests/` 目录 | `test` |
| 2 | 所有变更文件为文档格式（.md/.rst/.txt） | `docs` |
| 3 | 所有变更文件为 CI/构建配置（Dockerfile, .github/, Makefile, *.yaml 等） | `ci` 或 `build` |
| 4 | 新增文件占比 > 80% | `feat` |
| 5 | diff 语义分析：修复缺陷、解决异常 | `fix` |
| 6 | diff 语义分析：代码重组但功能不变 | `refactor` |
| 7 | diff 语义分析：性能相关优化 | `perf` |
| 8 | 仅格式/样式变更，无逻辑改动 | `style` |
| 9 | 以上均不匹配 | `chore` |

### Scope 推断

1. 提取所有变更文件路径（排除测试文件，除非全部为测试文件）
2. 计算共同父目录，取最后一级目录名作为 scope
3. 特殊处理：
   - monorepo（`packages/`、`apps/`）：取包名
   - `src/` 前缀：去除前缀后重新计算
   - 根目录配置文件：用文件名作 scope（如 `docker`、`deps`）
   - 跨 3 个以上不同模块：省略 scope
4. scope 使用 kebab-case，长度不超过 30 字符

### Breaking Change 检测

分析 diff 是否包含：删除公共函数/方法、修改 API 签名、移除导出接口。检测到时**自动添加** `!` 后缀和 `BREAKING CHANGE:` footer。

## Step 4: 生成并提交

### 消息格式

```
<type>[(scope)][!]: <中文描述>

[中文 body]

[BREAKING CHANGE: <说明>]
```

### 生成规则

- **type**：英文，从 Step 3 推断
- **scope**：英文，可选，从 Step 3 推断
- **description**：中文，动宾结构，简洁概括变更目的
- **body**：中文，复杂变更（文件数 > 5）时用列表列举关键变更点
- **footer**：Breaking Change 时添加 `BREAKING CHANGE: <说明>`

### 执行提交

生成消息后直接执行提交：

```bash
git commit -m "$(cat <<'EOF'
<完整 commit message>
EOF
)"
```

- 提交成功：显示 commit hash，流程结束
- 提交失败（如 pre-commit hook 失败）：显示错误信息，**终止流程**（用户自行处理后重新调用）
