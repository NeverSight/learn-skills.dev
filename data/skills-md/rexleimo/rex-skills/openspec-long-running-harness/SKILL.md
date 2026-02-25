---
name: openspec-long-running-harness
description: Use when implementing long-running agent workflows that need cross-session state persistence, incremental progress tracking, and gate enforcement. Combines OpenSpec spec-driven development with Anthropic's effective harnesses pattern for multi-context-window projects.
---

# OpenSpec Long-Running Agent Harness

## 概述

整合 OpenSpec 规范与 Anthropic "Effective Harnesses for Long-Running Agents" 最佳实践，为跨多个 context window 的 Agent 任务提供：

1. **状态持久化** - 通过 `feature_list.json` 和 `session_state.json` 跨会话保持进度
2. **增量进展** - 每个 session 只处理一个 feature，明确记录进展
3. **Gate Enforcement** - 会话结束前必须验证：工作区干净、新 commit、E2E 通过
4. **并行执行** - 支持 3-6 个独立子任务并发，依赖链串行

## 触发条件（必须命中）

满足任一条件就必须调用本技能：

1. 用户使用 `/opsx:apply` 或 `/openspec:apply` 且项目存在 `openspec/harness/` 目录
2. 用户明确要求 "long-running" 或 "harness" 模式
3. 用户提到 "跨会话"、"持久化状态"、"增量进展" 并涉及 OpenSpec 工作流
4. 项目已初始化 OpenSpec 结构，需要实现多个 feature

## 核心文件结构

```
openspec/harness/
├── feature_list.json     # 功能清单（Feature 定义 + 状态）
├── progress.log.md       # 进度日志（结构化会话记录）
├── session_state.json    # 当前会话状态
└── init.sh               # 环境检查脚本
```

## 状态机

```
                    ┌─────────────────────────────────────┐
                    │                                     │
                    ▼                                     │
┌──────────┐   ┌───────────────┐   ┌──────────┐   ┌─────────────┐
│ pending  │──▶│ in_progress   │──▶│ verifying│──▶│  passing    │
└──────────┘   └───────────────┘   └──────────┘   └─────────────┘
     │                │                   │              │
     │                │                   │              │
     │                ▼                   ▼              │
     │          ┌───────────┐       ┌──────────┐        │
     └─────────▶│ blocked   │◀──────│  failed  │◀───────┘
                └───────────┘       └──────────┘
```

## 执行规则

### 会话开始例行（必须按序执行）

1. **确认目录** - `pwd` 确认当前工作目录
2. **读取进度** - 读取 `progress.log.md` 了解最近工作
3. **选择任务** - 读取 `feature_list.json` 选择下一个任务
4. **环境检查** - 运行 `init.sh` 验证环境
5. **更新状态** - 更新 `session_state.json`

### 会话执行规则

1. **单一 Feature** - 每个 session 只处理一个 feature
2. **并行粒度** - 支持 3-6 个独立子任务并发
3. **依赖串行** - 有依赖关系的任务必须串行执行
4. **只改状态** - 禁止修改 `feature_list.json` 的 feature 定义，只能修改 status
5. **写冲突避免** - 并行任务不得修改同一文件重叠区域

### 会话结束例行（Gate Enforcement）

1. **工作区检查** - `git status` 确认工作区干净
2. **Commit 验证** - 确认存在新 commit（相对 session 开始）
3. **E2E 验证** - 运行 E2E 测试，必须通过
4. **状态更新** - 标记 feature 为 `passing`（如果 E2E 通过）
5. **摘要写入** - 写会话摘要到 `progress.log.md`

## 标准流程

### Phase 1: 初始化 Harness

```bash
# 如果项目没有 harness 结构，先初始化
./scripts/harness-init.sh <project-name>
```

创建：
- `openspec/harness/feature_list.json`
- `openspec/harness/progress.log.md`
- `openspec/harness/session_state.json`
- `openspec/harness/init.sh`

### Phase 2: 启动会话

```bash
./scripts/harness-start.sh
```

执行：
1. 运行 `init.sh` 检查环境
2. 读取 `progress.log.md` 最近进度
3. 调用 `harness-pick-next.sh` 选择任务
4. 更新 `session_state.json`

### Phase 3: 实现任务

按以下模式工作：

**并行模式**（3-6 个子任务）：
- 适用于：无依赖关系的独立任务
- 执行：同时启动多个 Sub Agent
- 汇总：统一收集结果，检查一致性

**串行模式**：
- 适用于：强依赖链 A → B → C
- 执行：按序完成，每步验证后再下一步

### Phase 4: 结束会话

```bash
./scripts/harness-end.sh
```

执行：
1. 运行 `harness-verify-e2e.sh` E2E 验证
2. 检查 gate conditions
3. 更新 feature 状态
4. 写会话摘要

## 任务选择策略

`harness-pick-next.sh` 按以下优先级选择：

1. **Priority**: P1 > P2 > P3
2. **Status**: `failed` > `in_progress` > `blocked` > `pending`
3. **依赖**: 无阻塞的 feature 优先

## 输出模板

### 会话开始输出

```markdown
## Session {N} Started - {date}

### Environment
- Directory: {pwd}
- Git Branch: {branch}
- Start Commit: {hash}

### Selected Task
- ID: {feature-id}
- Priority: {P1|P2|P3}
- Description: {description}
- Steps: {step count}

### Parallel Plan (3-6 tasks)
1. {Task A}: {goal} → {output}
2. {Task B}: {goal} → {output}
3. {Task C}: {goal} → {output}
...
```

### 会话结束输出

```markdown
## Session {N} Ended - {date}

### Completed
- Feature: {id} - {description}
- Commits: {hash list}
- Duration: {time}

### Gate Results
- [x] Working tree clean
- [x] New commit created: {hash}
- [x] E2E verification passed

### Progress Log Updated
- Status: passing
- Files modified: {count}

### Next Steps
- Next feature: {id}
- Remaining: {count} features
```

## 并发执行指南

### 可并行的场景

- 不同文件的修改
- 不同模块的功能
- 独立的测试用例
- 并行的调研任务

### 必须串行的场景

- 同一文件的修改
- 有依赖关系（A 的输出是 B 的输入）
- 共享状态更新
- 最终合并提交

### 冲突处理

1. **检测** - 分析任务文件边界
2. **重排** - 按文件/模块边界重新划分任务
3. **降级** - 无法避免冲突时改为串行

## 错误处理

### E2E 验证失败

1. 标记 feature 为 `failed`
2. 记录失败原因到 `progress.log.md`
3. 不提交 code，保持工作区状态供调试
4. 下次 session 优先处理 failed feature

### 环境检查失败

1. 记录问题到 `progress.log.md`
2. 标记 feature 为 `blocked`
3. 记录 `blocked_reason`
4. 提示用户手动修复

### 依赖阻塞

1. 标记为 `blocked`
2. 记录依赖的 feature id
3. 在依赖 feature 完成后自动解除

## 与 OpenSpec 命令集成

| OpenSpec 命令 | Harness 集成 |
|---------------|--------------|
| `/opsx:new` | 初始化 harness + 创建 `feature_list.json` |
| `/opsx:apply` | 选择下一个 failing feature，启动实现 |
| `/opsx:verify` | 运行 E2E 验证，更新状态 |
| `/opsx:archive` | 验证所有 features passing，归档 |

## 最佳实践

1. **小步提交** - 每个 feature 拆分为多个小 commit
2. **频繁验证** - 每个 subtask 完成后局部验证
3. **清晰记录** - `progress.log.md` 记录关键决策和问题
4. **环境隔离** - `init.sh` 确保环境一致性
5. **增量进展** - 宁可小步前进，不要大步跳跃

## 参考资源

- Anthropic Article: https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- OpenSpec Parallel Agents: `../openspec-parallel-agents/SKILL.md`
- Spec Kit Orchestrator: `../spec-kit-parallel-orchestrator/SKILL.md`
