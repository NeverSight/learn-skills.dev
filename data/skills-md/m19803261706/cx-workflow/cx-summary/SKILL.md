---
name: cx-summary
description: >
  CX 工作流 — 汇总发布与闭环。手动触发或由 cx-exec 全部完成时自动调用。
  生成汇总文档，GitHub 同步（基于 config.github_sync），
  智能更新 CLAUDE.md 规范，触发完成通知。
  仅在用户明确调用 /cx-summary 或 cx-exec 全部完成时执行。不要自动触发。
---

# cx-summary: 汇总发布与闭环

手动或自动触发的最后一步：生成汇总文档，同步 GitHub，更新 CLAUDE.md，发送完成通知。

## 使用方法

```
/cx-summary              # 自动汇总当前功能
/cx-summary {功能名}     # 指定功能汇总
```

## 核心步骤

### Step 0: 初始化本地环境

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel)
DEVELOPER_ID=$(jq -r '.developer_id' "$PROJECT_ROOT/.claude/cx/config.json" 2>/dev/null || echo "cx")
CONFIG="$PROJECT_ROOT/.claude/cx/config.json"
FEATURE_DIR="$PROJECT_ROOT/.claude/cx/features/${DEVELOPER_ID}-{feature_slug}"
```

### Step 1: 代码审查（可选）

如果 `config.code_review = true`，启动代码审查流程：

```json
{
  "questions": [
    {
      "question": "所有任务已完成。是否在汇总前进行代码审查？",
      "header": "代码审查",
      "multiSelect": false,
      "options": [
        {"label": "全面审查 (推荐)", "description": "逻辑+安全+质量+清理"},
        {"label": "快速检查", "description": "仅逻辑和安全问题"},
        {"label": "跳过", "description": "直接进入汇总"}
      ]
    }
  ]
}
```

**全面审查**：
- 启动 code-reviewer 子代理审查 git diff（对照 design.md 契约）
- 发现 critical 问题 → 询问是否修复 → 修复后重新审查
- 发现 warning/info → 询问是否优化 → 启动 code-cleanup 子代理
- 完成后自动 commit（message: "refactor: code cleanup post-review"）

**快速检查**：
- 启动 code-reviewer 子代理（精简模式，仅检查逻辑 bug + 安全问题）
- 有问题展示，无问题继续

### Step 2: 生成汇总文档

生成 summary.md，包含：

```markdown
# 功能完成汇总: {功能名}

## 完成概览

| 项 | 内容 |
|---|---|
| 功能 | {feature_name} |
| 规模 | S/M/L |
| 完成时间 | {date} |
| 总任务数 | {N} |
| 提交数 | {M} |

## 相关文档

- PRD: {link_or_local_path}
- Design Doc: {link_or_local_path}
- ADR: {link_or_local_path}

## 功能描述

{从 prd.md 提取的功能概述}

## 实现清单

### Phase 1: {phase_name}
- [x] Task 1: {title}
  - 提交: {hash}
  - 变更文件: {count} 个

- [x] Task 2: {title}
  - 提交: {hash}
  - 变更文件: {count} 个

### Phase 2: {phase_name}
...

## 关键设计决策

{从 design.md 和 adr.md 提取的核心决策}

## API 接口清单

| 接口 | 方法 | 路径 | 状态 |
|------|------|------|------|
| {name} | POST | /api/v1/xxx | ✅ |
| {name} | GET | /api/v1/xxx | ✅ |

## 变更统计

- 新增文件: {count}
- 修改文件: {count}
- 删除文件: {count}
- 新增代码行: {count}
- 修改代码行: {count}

## 测试覆盖

- 单元测试: {count} 个，通过率 {%}
- 集成测试: {count} 个，通过率 {%}
- 代码审查: ✅ 通过

## 已知问题与后续改进

{如有 warning/info 级别的问题或建议的改进}

## 部署建议

{if L 规模: 包含部署步骤、数据迁移、兼容性说明}

---

> CX 工作流完成 | {date}
```

保存到 `.claude/cx/features/{dev_id}-{feature}/summary.md`。

### Step 3: GitHub 同步（基于模式）

根据 `config.github_sync`：

**off**：
- 仅保存本地 summary.md，不创建任何 GitHub Issue
- 本地闭环完成

**local**：
- 创建汇总 Issue（标签 `doc:summary`）
- Issue body 包含 summary.md 内容
- 不创建 PR

**collab**：
- 创建汇总 Issue（标签 `doc:summary`）
- 如果有代码审查，创建 PR（标签 `type:refactor`）
- PRD 和 Design Doc Issue 保持打开

**full**：
- 创建汇总 Issue（标签 `doc:summary`）
- 创建代码审查 PR（标签 `type:refactor`）
- **关闭所有相关 Issue**：PRD、Design Doc、ADR、Epic、所有子任务
- 标注 Scope Issue 该模块状态为已完成

### Step 4: 智能 CLAUDE.md 更新

检测是否有新的项目规范（如新 API 路径模式、新命名约定、新测试命令等）。

**Step 4a: 自动扫描**（无需询问）

```bash
# 检查是否有新规范
IS_NEW_CONVENTION=false

# 扫描 Design Doc：新 API 路径模式？
grep -E '/api/v[0-9]+/' design.md | sort -u > /tmp/design_paths.txt
if [ -f "$CLAUDE_MD" ]; then
  grep -E '/api/v[0-9]+/' "$CLAUDE_MD" | sort -u > /tmp/claude_paths.txt
  if ! diff -q /tmp/design_paths.txt /tmp/claude_paths.txt > /dev/null 2>&1; then
    IS_NEW_CONVENTION=true
  fi
fi

# 扫描 ADR：新架构决策？
if [ -f "adr.md" ] && grep -q "Accepted" adr.md; then
  if ! grep -q "$(head -1 adr.md | sed 's/# ADR: //')" "$CLAUDE_MD" 2>/dev/null; then
    IS_NEW_CONVENTION=true
  fi
fi

# 扫描 git diff：新测试命令、新依赖？
git log --oneline -p | grep -E '^\+\+\+.*test|^\+.*npm|^\+.*pytest' > /tmp/new_patterns.txt
if [ -s /tmp/new_patterns.txt ]; then
  IS_NEW_CONVENTION=true
fi
```

**Step 4b: 用户确认决策**（如有新规范）

```json
{
  "questions": [
    {
      "question": "这次开发产生了以下新的项目规范。要更新到 CLAUDE.md 吗？",
      "header": "规范更新",
      "multiSelect": false,
      "options": [
        {"label": "查看并更新", "description": "展示变更差异，用户确认后更新"},
        {"label": "不需要", "description": "跳过更新"},
        {"label": "我自己改", "description": "手动编辑 CLAUDE.md"}
      ]
    }
  ]
}
```

如果选择"查看并更新"：

```
新规范变更差异:

【API 路径规范】
  旧: /api/v1/{resource}
  新: /api/v2/{resource} (支持 v1 和 v2)

【数据库命名】
  旧: 未定义
  新: snake_case，含 created_at/updated_at 时间戳

【前端常量】
  新增: 状态枚举 (PENDING, PROCESSING, COMPLETED, FAILED)

【测试命令】
  新增: npm run test:e2e

这些更新会替换 CLAUDE.md 中【项目规范】段落。
总行数变化: 28 → 35 行（CX 段落）

是否确认更新？
```

**Step 4c: 执行更新**（用户确认后）

```bash
# 读取 CLAUDE.md
CLAUDE_MD="$PROJECT_ROOT/CLAUDE.md"

# 如果没有 CLAUDE.md，创建新文件
if [ ! -f "$CLAUDE_MD" ]; then
  cat > "$CLAUDE_MD" << 'EOF'
# Project Guidelines

<!-- CX-WORKFLOW-START -->
## CX 工作流 (v2.0)

### 命令
/cx-prd | /cx-exec | /cx-summary

### 活跃功能
(无)

### 项目规范
(待定义)

<!-- CX-WORKFLOW-END -->

## 其他项目信息

...
EOF
fi

# 如果没有 CX 段落，追加到末尾
if ! grep -q "CX-WORKFLOW-START" "$CLAUDE_MD"; then
  cat >> "$CLAUDE_MD" << 'EOF'

<!-- CX-WORKFLOW-START -->
## CX 工作流 (v2.0)

### 命令
/cx-prd | /cx-exec | /cx-summary

### 活跃功能
(无)

### 项目规范
(待定义)

<!-- CX-WORKFLOW-END -->
EOF
fi

# 替换标记之间的内容
# （脚本用 sed 或 awk 替换 CX-WORKFLOW-START 到 CX-WORKFLOW-END 之间的内容）

# 检查更新后的 CX 段落行数
NEW_LINES=$(grep -c "." <<< "$(sed -n '/CX-WORKFLOW-START/,/CX-WORKFLOW-END/p' "$CLAUDE_MD")")

if [ "$NEW_LINES" -gt 30 ]; then
  echo "⚠️ CX 段落已达 $NEW_LINES 行，建议精简。CLAUDE.md 每行都会消耗 token。"
  # 不强制阻止，给用户警告
fi
```

**Step 4d: 活跃功能更新**

无论是否有新规范，都要更新"活跃功能"行：

```markdown
### 活跃功能
- {feature_name}: 已完成 ✅

(如有其他活跃功能则列出，已完成的功能移到下方"已完成功能"）
```

### Step 5: 本地清理

```bash
# 归档当前功能的目录（可选）
# 移动到 .claude/cx/completed/{dev_id}-{feature}/
# 或在 .claude/cx/features/{dev_id}-{feature}/ 中创建 COMPLETED 标记文件

# 清空当前工作上下文
jq '.current_feature = null' "$CONFIG" > "$CONFIG.tmp"
mv "$CONFIG.tmp" "$CONFIG"
```

### Step 6: 发送完成通知

根据 `config.hooks.notification`（默认 true），使用 Notification hook：

```bash
# 桌面通知
NOTIFICATION_MSG="✅ CX 工作流完成
功能: {feature_name}
任务: {N} 个
时间: {duration}

汇总: .claude/cx/features/{dev_id}-{feature}/summary.md"
```

### Step 7: 输出结果

```
汇总发布完成

功能: {feature_name}
规模: S/M/L
完成任务: {N}
提交: {M}

本地汇总: .claude/cx/features/{dev_id}-{feature}/summary.md

GitHub 同步模式: {mode}
└─ (off: 本地仅    local: 创建 Issue    collab: Issue+PR    full: 关闭 Issue)

CLAUDE.md 更新: {是/否}
├─ 新规范检测: {有/无}
└─ 活跃功能更新: ✅

桌面通知: ✅ 已发送

下一步建议:
  运行 /cx-prd {下一个功能名} 开始下一个功能
  或运行 /cx-scope 查看项目蓝图
```

## 本地文件结构

```
.claude/cx/features/{dev_id}-{feature}/
├── summary.md              ← 汇总文档
├── summary.json            ← Issue 编号（可选）
├── status.json             ← 最终任务状态（已完成）
├── prd.md
├── design.md
├── adr.md
└── tasks/
    ├── task-1.md ... task-N.md
```

## 规范更新规则

CX 段落必须 ≤ 30 行。如更新导致超出，提示用户：
- 精简冗余内容
- 将详细规范移至项目文档（如 docs/ 目录）
- 在 CLAUDE.md 中仅保留精简版和关键链接

## Epic 和 Scope 闭环

- 如果在 collab/full 模式，关闭所有相关 GitHub Issue（PRD、Design、Epic、子任务）
- 更新 Scope Issue 中对应模块的状态为 ✅ 已完成
- 检查 Scope 中是否所有模块都完成，若是则关闭 Scope Issue

## 多功能场景

如果一个项目有多个功能（e.g., cx-payment, cx-refund）：
- 每个功能有独立的 .claude/cx/features/{dev_id}-{feature}/ 目录
- CLAUDE.md 中列出所有活跃功能和已完成功能
- Scope Issue 追踪整个项目的模块完成度

## 与 cx-exec 的衔接

- 当 cx-exec 检测到所有任务 completed 时，自动触发 cx-summary
- 如果 config.code_review = true，先启动代码审查，再进入汇总
- cx-summary 读取完整的 status.json 和 git log 生成汇总
