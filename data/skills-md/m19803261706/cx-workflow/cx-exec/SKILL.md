---
name: cx-exec
description: >
  CX 工作流 — 任务执行与契约校验。当用户提到"执行任务"、"开始开发"、
  "实现功能"、"写代码"、"继续做"、"下一个任务"时触发。
  5 步流程：读任务 → 实现 → 契约校验 → 测试 → 提交。
  使用本地 task-{n}.md 和 status.json，自动校验实现是否与契约一致。
  完成所有任务后自动触发 cx-summary。
---

# cx-exec: 任务执行与契约校验

5 步精简流程实现功能代码，自动校验与 API 契约一致，全部完成后启动汇总。

## 使用方法

```
/cx-exec             # 执行下一个待执行任务
/cx-exec #1          # 执行指定任务编号
/cx-exec 1-5         # 批量执行任务 1 到 5
/cx-exec --phase 1   # 执行 Phase 1 的所有任务
/cx-exec --all       # 执行所有待执行任务（并行）
```

## 核心步骤

### Step 0: 初始化本地环境

```bash
PROJECT_ROOT=$(git rev-parse --show-toplevel)
DEVELOPER_ID=$(jq -r '.developer_id' "$PROJECT_ROOT/.claude/cx/config.json" 2>/dev/null || echo "cx")
CONFIG="$PROJECT_ROOT/.claude/cx/config.json"
FEATURE_DIR="$PROJECT_ROOT/.claude/cx/features/${DEVELOPER_ID}-{feature_slug}"
```

### Step 1: 读取任务

```bash
# 读取本地状态
STATUS_FILE="$FEATURE_DIR/status.json"
TASK_NUMBER=$(jq -r '.tasks[] | select(.status == "pending") | .number' "$STATUS_FILE" | head -1)

# 读取任务详情
TASK_FILE="$FEATURE_DIR/tasks/task-${TASK_NUMBER}.md"
```

**依赖检查**：
- 如果任务有 `depends_on`，检查依赖任务是否已完成
- 若未完成，提示用户先执行依赖任务，不强制执行

**更新任务状态**：标记为 `in_progress`。

### Step 2: 实现代码

根据 Task 文件中的任务描述和 **API 契约片段** 进行实现。

**关键原则**：
- **首先**阅读 Task 文件中的「📋 API 契约片段」
- 后端：Controller 路径、DTO 字段名、枚举值必须与契约一致
- 前端：API 路径、interface 字段名、枚举常量必须与契约一致
- 如果遇到阻塞（缺少依赖、需求不清），停下来告知用户

**技术栈自适应**：根据项目类型运行对应的测试和检查
```bash
[ -f pyproject.toml ] && uv run pytest
[ -f package.json ] && npm test
[ -f pom.xml ] && mvn test
```

### Step 3: 契约校验（核心新增）

实现完成后，**自动校验**代码是否与 Task 文件中的 API 契约一致。

**校验内容**：

```
1. 接口路径一致性
   比对：Controller @RequestMapping vs Task 中的契约路径
   不一致 → 自动修正

2. DTO/VO 字段一致性
   比对：DTO 类字段 vs Task 中的字段映射表
   不一致 → 自动修正

3. 状态枚举一致性
   比对：枚举类/常量 vs Task 中的状态枚举对照表
   不一致 → 自动修正

4. 请求/响应结构一致性
   比对：Controller 方法签名 vs Task 中的 Request/Response JSON
   不一致 → 自动修正
```

**校验结果处理**：

✅ **全部通过**：
```
契约校验通过
  接口路径: 3/3 一致
  字段映射: 12/12 一致
  状态枚举: 4/4 一致
  → 继续提交
```

⚠️ **发现不一致（自动修正）**：
```
契约校验发现不一致，自动修正中...

  ❌ 接口路径: POST /api/v1/certifications → 实际为 /certification
    → 已修正 @PostMapping 路径

  ❌ 字段名: rejectReason → 实际为 rejectMsg
    → 已修正 DTO 字段名和前端 interface

  ❌ 状态枚举: REJECTED → 实际为 REJECT
    → 已修正前端枚举常量

修正完成，重新运行测试...
```

❌ **修正后仍有问题（停止提交）**：
```
契约校验失败，无法自动修正

  问题: {具体问题}
  建议: {修复建议}

需要人工介入
```

### Step 4: 提交代码

```bash
git add {相关文件}
git commit -m "{type}({scope}): {description} (task #{task_number})"
```

commit message 遵循项目已有风格（或 conventional commits）。

### Step 5: 更新进度 & 解锁依赖任务

```bash
# 更新任务状态为 completed
jq ".tasks[] |= if .number == $TASK_NUMBER then .status = \"completed\" else . end" "$STATUS_FILE" > "$STATUS_FILE.tmp"
mv "$STATUS_FILE.tmp" "$STATUS_FILE"

# 解锁依赖该任务的 pending 任务
for dependent in $(jq -r ".tasks[] | select(.depends_on[]? == $TASK_NUMBER) | .number" "$STATUS_FILE"); do
  jq ".tasks[] |= if .number == $dependent then .status = \"pending\" else . end" "$STATUS_FILE" > "$STATUS_FILE.tmp"
  mv "$STATUS_FILE.tmp" "$STATUS_FILE"
done
```

### Step 6: Epic 闭环检测

检查所有任务是否完成：

```bash
TOTAL=$(jq '.tasks | length' "$STATUS_FILE")
COMPLETED=$(jq '[.tasks[] | select(.status == "completed")] | length' "$STATUS_FILE")

if [ "$COMPLETED" -eq "$TOTAL" ]; then
  # === 所有任务完成，触发闭环 ===
  echo "所有任务已完成，启动汇总..."

  # 自动触发 cx-summary
  # 如果 config.code_review = true，先启动代码审查流程
fi
```

## 批量执行模式

### 参数解析

```bash
case "$ARGUMENTS" in
  *-*)
    # 范围: 1-5
    RANGE=$(echo "$ARGUMENTS" | tr '-' ' ')
    TARGETS=$(jq -r ".execution_order[] | select(. >= $START and . <= $END)" "$STATUS_FILE")
    ;;
  --phase*)
    # Phase: --phase 1
    PHASE=$(echo "$ARGUMENTS" | grep -oE '[0-9]+')
    TARGETS=$(jq -r ".phases[] | select(.number == $PHASE) | .tasks[]" "$STATUS_FILE")
    ;;
  --all)
    # 所有 pending 任务
    TARGETS=$(jq -r '.tasks[] | select(.status == "pending") | .number' "$STATUS_FILE")
    ;;
esac
```

### 并行执行

根据 `parallel_group` 字段判断并行性：

**同一 `parallel_group` 的任务可并行，不同 group 串行。**

```bash
# 并行组 p1-a (task 1, 2 可并行)
Task agent: task-1.md → Step 1-5
Task agent: task-2.md → Step 1-5
            ↓ 全部完成后
# 并行组 p2-a (task 3, 4 可并行)
Task agent: task-3.md → Step 1-5
Task agent: task-4.md → Step 1-5
            ↓ 全部完成后
# 并行组 p3-a (task 5 串行)
Task agent: task-5.md → Step 1-5
```

### 子代理调用

每个任务通过 Task tool 启动独立子代理：

```
Task tool 参数:
  subagent_type: "task-executor"
  prompt: |
    项目根目录: $PROJECT_ROOT
    任务: $FEATURE_DIR/tasks/task-{n}.md

    请按 5 步流程完成:
    1. 读取 task-{n}.md 中的任务描述和 API 契约片段
    2. 按契约实现代码（路径、字段、枚举一致）
    3. 运行项目测试和检查
    4. 执行契约校验（对比实现 vs task-{n}.md 中的契约）
    5. 校验通过后 git add + commit

    commit message 格式: {type}({scope}): {desc} (task #{n})
```

**并行**：一条消息中发起多个 Task tool 调用
**串行**：等前一个完成后再启动下一个

## 错误处理

### 实现失败

```
任务执行遇到问题

错误: {具体错误}
已完成: {部分进度}

已恢复任务为 pending 状态，需要人工介入
```

任务状态重置为 `pending`，供后续重试。

### 契约校验失败（无法自动修正）

```
契约校验失败

不一致项:
{具体问题}

建议: 检查 Task 中的契约定义是否需要调整
或检查 Design Doc 中的相应章节
```

### 依赖未满足

```
任务 #103 依赖未满足

依赖: #101 (状态: pending)

建议: 先执行 /cx-exec #101
```

## 进度追踪

status.json 在 Step 5 实时更新，记录：
- 每个任务的状态（pending / in_progress / completed）
- Phase 的整体进度
- 下一个可执行任务

## 与 cx-plan 的衔接

- **输入**：status.json（任务列表）+ task-{n}.md（任务详情）
- **输出**：更新的 status.json + git commits
- cx-exec 读取 status.json 中的 `execution_order` 确定执行顺序

## 与 cx-summary 的衔接

- 当所有任务 completed 时，自动触发 cx-summary
- cx-summary 读取完整的 status.json 和 git log，生成汇总文档
- 可选启动代码审查（如 config.code_review = true）

## SubagentStop Hook

批量执行时，每个子代理完成后触发 SubagentStop hook 校验：
- 代码是否符合契约？
- 测试是否通过？
- 若有问题，标记任务为 failed，不自动重试

## 上下文持久化

SessionStart hook 自动加载当前 feature 的 status.json，输出：
```
当前进度:
  功能: cx-payment
  Phase 1: 2/2 completed
  Phase 2: 1/3 in_progress (Task #103)
  下一个: Task #104
```

使用户快速恢复中断的工作。
