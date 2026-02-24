---
name: git-sync-checker
description: 智能检查本地代码与GitHub的同步状态,识别未提交、未推送、未拉取的更改,帮助在多台电脑之间无缝切换开发。触发词:"检查同步"、"切换电脑"、"准备下班"、"开始工作"。
allowed-tools: Bash, Read, Grep
---

# Git 同步状态检查器

## 目标

在多台电脑（公司、家里）之间切换开发时,自动检查代码同步状态,确保不会丢失代码或产生冲突。

## 快速开始

### 三步检查法

1. **说出触发词**：告诉 AI "检查同步"、"准备下班"或"开始工作"
2. **查看报告**：AI 自动检查并生成详细的同步状态报告
3. **执行建议**：根据报告中的命令提示，完成代码同步

### 典型使用示例

```
# 下班前
用户："准备下班，检查一下代码同步"
AI：运行 git 检查，发现有 3 个未推送的提交
AI：提供推送命令和验证步骤

# 上班时
用户："开始工作，拉取最新代码"
AI：检查远程更新，发现有 2 个新提交
AI：提供安全拉取命令
```

## 何时使用

### 📍 下班前（公司电脑）

- 准备离开公司,需要确保所有代码已推送到 GitHub
- 触发词: "准备下班"、"检查同步"、"推送代码"

### 🏠 到家后（家里电脑）

- 刚回到家,准备继续开发
- 触发词: "开始工作"、"拉取最新代码"、"检查同步"

### 🏢 上班前（公司电脑）

- 刚到公司,准备继续开发
- 触发词: "开始工作"、"检查同步"

### 🔄 任何时候

- 想知道当前代码与远程仓库的差异
- 触发词: "检查同步状态"、"git状态"

## 工作流程

### 完整检查流程图

```
用户触发
    ↓
1. 识别场景
   (下班/上班/日常检查)
    ↓
2. 执行 Git 检查
   ├─ git status (本地状态)
   ├─ git fetch (远程更新)
   └─ git log (提交对比)
    ↓
3. 分析结果
   ├─ 未提交的修改？
   ├─ 未推送的提交？
   ├─ 远程新提交？
   └─ 代码分叉？
    ↓
4. 生成报告
   ├─ 状态总结
   ├─ 问题清单
   └─ 操作建议
    ↓
5. 提供命令
   (可直接复制执行)
```

### 决策逻辑

- **场景识别**：根据触发词和当前状态判断用户意图
- **优先级**：先检查本地修改，再检查远程更新
- **安全原则**：提供可逆的操作建议，避免数据丢失
- **验证步骤**：每个操作都附带验证命令

## 检查流程

### 步骤 1: 检查基本 Git 状态

```bash
# 检查当前分支和状态
git status
git branch -vv
```

**识别问题**:

- ✅ 工作区干净: `nothing to commit, working tree clean`
- ⚠️ 有未暂存的修改: `Changes not staged for commit`
- ⚠️ 有未提交的修改: `Changes to be committed`
- ⚠️ 有未跟踪的文件: `Untracked files`

### 步骤 2: 检查与远程仓库的差异

```bash
# 获取远程仓库最新信息（不拉取代码）
git fetch origin

# 检查本地与远程的差异
git status -sb
git log --oneline origin/main..HEAD  # 本地领先的提交
git log --oneline HEAD..origin/main  # 远程领先的提交
```

**识别问题**:

- ✅ 本地领先: `Your branch is ahead of 'origin/main' by X commits`
- ⚠️ 远程领先: `Your branch is behind 'origin/main' by X commits`
- 🔴 分叉了: `Your branch and 'origin/main' have diverged`

### 步骤 3: 检查未推送的提交

```bash
# 查看未推送的提交详情
git log origin/main..HEAD --oneline
git diff origin/main..HEAD --stat
```

### 步骤 4: 检查潜在冲突

```bash
# 检查是否有潜在冲突（模拟合并）
git fetch origin
git merge-base HEAD origin/main
git diff --name-only $(git merge-base HEAD origin/main)..HEAD
git diff --name-only $(git merge-base HEAD origin/main)..origin/main
```

### 步骤 5: 生成同步报告

## 输出格式

### 场景 A: 准备下班（公司电脑）

````markdown
# 🏢 → 🏠 同步检查报告

## 📊 当前状态

- 分支: main
- 本地提交: 3 个未推送
- 工作区: 2 个文件有修改

## ⚠️ 需要处理的问题

### 1. 未提交的修改（2个文件）

\```
M src/components/dashboard-client.tsx
M src/hooks/use-smart-comparison.ts
\```

**建议操作**:
\```bash
git add .
git commit -m "feat: 完成XXX功能开发"
\```

### 2. 未推送的提交（3个）

\```
e18cf2e feat: 添加多图表标签页功能
a1b2c3d fix: 修复KPI计算精度问题
d4e5f6g docs: 更新开发文档
\```

**建议操作**:
\```bash
git push origin main
\```

## ✅ 推送清单

在离开公司前,请完成以下步骤:

- [ ] 提交所有未保存的修改
- [ ] 推送所有提交到 GitHub
- [ ] 验证 GitHub 上能看到最新代码
- [ ] 记录当前工作状态（可选）

## 🎯 推送后验证命令

\```bash
git status # 应显示 "nothing to commit, working tree clean"
git log --oneline origin/main..HEAD # 应无输出（表示已完全同步）
\```
````

### 场景 B: 开始工作（家里/公司电脑）

````markdown
# 🏠/🏢 开始工作 - 同步检查报告

## 📊 当前状态

- 分支: main
- 远程领先: 3 个提交
- 工作区: 干净

## 📥 需要拉取的更新

### 远程新增的提交（3个）

\```
e18cf2e feat: 添加多图表标签页功能
a1b2c3d fix: 修复KPI计算精度问题
d4e5f6g docs: 更新开发文档
\```

### 变更的文件

\```
src/components/features/multi-chart-tabs.tsx (新文件)
src/hooks/use-smart-comparison.ts (修改)
开发文档/01_features/F014_multi_chart_tabs/ (新增)
\```

## ✅ 拉取建议

**安全拉取命令**:
\```bash

# 1. 确认本地工作区干净

git status

# 2. 拉取最新代码

git pull origin main

# 3. 验证拉取成功

git status
pnpm dev # 启动项目验证
\```

## ⚠️ 注意事项

- ✅ 工作区干净,可以安全拉取
- 📝 拉取后建议运行 `pnpm dev` 验证项目正常
- 📚 查看更新的开发文档了解新功能
````

### 场景 C: 代码分叉警告

````markdown
# 🔴 代码分叉警告

## 问题描述

本地分支和远程分支已经分叉:

- 本地独有提交: 2 个
- 远程独有提交: 3 个

## 📊 分叉详情

### 本地独有的提交

\```
a1b2c3d feat: 添加XXX功能（在家里电脑上提交）
d4e5f6g fix: 修复YYY问题
\```

### 远程独有的提交

\```
e18cf2e feat: 添加ZZZ功能（在公司电脑上提交）
f7g8h9i fix: 修复AAA问题
j0k1l2m docs: 更新文档
\```

## 🔧 解决方案

### 方案 1: Rebase（推荐，保持线性历史）

\```bash

# 1. 备份当前分支

git branch backup-$(date +%Y%m%d-%H%M%S)

# 2. 获取最新远程代码

git fetch origin

# 3. Rebase 到远程分支

git rebase origin/main

# 4. 如果有冲突，解决后继续

git rebase --continue

# 5. 强制推送（仅当确定本地更改正确时）

git push origin main --force-with-lease
\```

### 方案 2: Merge（保留完整历史）

\```bash

# 1. 拉取并合并

git pull origin main

# 2. 解决冲突（如果有）

# 编辑有冲突的文件

# 3. 提交合并

git add .
git commit -m "merge: 合并远程更改"

# 4. 推送

git push origin main
\```

## ⚠️ 预防措施

1. **始终在下班前推送代码**
2. **始终在开始工作前拉取代码**
3. **避免在多台电脑同时开发同一功能**
4. **使用功能分支隔离不同的开发任务**
````

## 常见场景处理

### 场景 1: 忘记推送就下班了

**症状**: 在家里电脑上拉取时，发现没有公司的最新代码

**解决**:

1. 第二天到公司后，运行检查命令
2. 发现未推送的提交
3. 推送到 GitHub
4. 回家后重新拉取

### 场景 2: 两台电脑都有未推送的提交

**症状**: 代码分叉，本地和远程都有独有的提交

**解决**:

1. 运行检查命令，识别分叉
2. 选择 Rebase 或 Merge 方案
3. 解决冲突（如果有）
4. 推送合并后的代码

### 场景 3: 不确定当前在哪台电脑上工作过

**症状**: 混淆了工作进度

**解决**:

1. 运行检查命令
2. 查看未推送的提交信息
3. 查看提交时间和作者信息
4. 根据提交内容判断

## 最佳实践

### ✅ 推荐的工作流程

**下班前（公司电脑）**:

```bash
# 1. 运行同步检查
<使用此 skill>

# 2. 提交所有修改
git add .
git commit -m "feat: 完成XXX功能"

# 3. 推送到 GitHub
git push origin main

# 4. 验证推送成功
git log --oneline origin/main..HEAD  # 应无输出
```

**开始工作前（家里/公司电脑）**:

```bash
# 1. 运行同步检查
<使用此 skill>

# 2. 拉取最新代码
git pull origin main

# 3. 验证项目正常
pnpm dev

# 4. 开始开发
```

### 🔒 安全措施

1. **永远不要使用 `git push --force`**
   - 除非你 100% 确定远程代码是错误的
   - 使用 `--force-with-lease` 更安全

2. **提交前先拉取**

   ```bash
   git fetch origin
   git status  # 检查是否有冲突
   ```

3. **使用功能分支**

   ```bash
   # 在公司开发新功能
   git checkout -b feature/new-dashboard

   # 下班前推送
   git push origin feature/new-dashboard

   # 在家拉取并继续开发
   git fetch origin
   git checkout feature/new-dashboard
   git pull origin feature/new-dashboard
   ```

4. **定期同步**
   - 不要积累太多未推送的提交
   - 建议每完成一个小功能就推送一次

## 检查命令速查表

```bash
# 基础状态检查
git status                           # 工作区状态
git branch -vv                       # 分支与跟踪关系

# 与远程对比
git fetch origin                     # 获取远程更新（不合并）
git log origin/main..HEAD            # 本地独有的提交
git log HEAD..origin/main            # 远程独有的提交

# 差异对比
git diff origin/main                 # 与远程的详细差异
git diff --stat origin/main          # 差异文件统计

# 提交历史
git log --oneline -10                # 最近10个提交
git log --graph --oneline --all      # 分支图形化历史

# 远程仓库信息
git remote -v                        # 远程仓库地址
git remote show origin               # 远程仓库详细信息
```

## 工具限制

本 skill 只能**检查和建议**,不能自动执行 Git 操作。所有 Git 命令需要用户手动执行,以确保安全。

## 输出原则

1. **清晰的状态总结** - 用户一眼看懂当前情况
2. **具体的操作建议** - 提供可直接复制执行的命令
3. **风险提示** - 标注潜在的问题和注意事项
4. **验证步骤** - 告诉用户如何确认操作成功

## 高级功能

### 识别工作电脑

可以在 Git 配置中为不同电脑设置标识:

```bash
# 在公司电脑上
git config user.name "张三 (公司)"
git config user.email "zhangsan@company.com"

# 在家里电脑上
git config user.name "张三 (家)"
git config user.email "zhangsan@personal.com"
```

这样通过 `git log` 就能清楚看到哪些提交是在哪台电脑上完成的。

### 自动检查脚本（可选）

可以创建一个 pre-commit hook 自动检查:

```bash
# .git/hooks/pre-commit
#!/bin/bash
git fetch origin
LOCAL=$(git rev-parse @)
REMOTE=$(git rev-parse origin/main)

if [ $LOCAL != $REMOTE ]; then
    echo "⚠️  警告: 远程仓库有更新，请先拉取！"
    exit 1
fi
```
