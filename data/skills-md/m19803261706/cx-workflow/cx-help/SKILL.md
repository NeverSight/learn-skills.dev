---
name: cx-help
description: >
  CX 工作流 — 帮助与使用指南。展示可用命令、当前工作流状态、完整工作流概览。
  触发词：帮助、help、怎么用、工作流、命令、怎么开始、指南。
  自动触发当用户询问工作流相关问题。
---

# cx-help — CX 工作流使用指南

## 快速开始

CX 工作流是一套完整的开发管线，从需求到交付、从 Bug 修复到代码审查，覆盖整个开发周期。

```
新功能开发流：PRD → Design → Plan → Exec → Review → Summary
Bug 修复流：Fix → Investigate → Test → Commit
```

## 命令速查表

### 系统命令

| 命令 | 说明 |
|------|------|
| `/cx-init` | 项目初始化（仅运行一次）|
| `/cx-help` | 显示此帮助文档 |
| `/cx-status` | 查看当前进度和状态 |
| `/cx-config` | 查看或修改工作流配置 |

### 开发命令

| 命令 | 说明 | 触发条件 |
|------|------|---------|
| `/cx-prd <功能名>` | 需求收集与规模评估 | 想做新功能时 |
| `/cx-design <功能名>` | 技术设计与 API 契约定义 | PRD 规模为 M 或 L |
| `/cx-adr <决策>` | 架构决策记录 | PRD 规模为 L 或遇到架构问题 |
| `/cx-plan <功能名>` | 任务分解与计划 | Design Doc 完成后 |
| `/cx-exec` | 执行下一个任务 | 有 cx-ready 任务待执行 |
| `/cx-summary` | 功能汇总与发布 | 所有任务完成后 |

### 轻量路径

| 命令 | 说明 |
|------|------|
| `/cx-fix <bug描述>` | Bug 修复（调查→定位→修复→测试→提交） |

## 工作流程详解

### 新功能开发路径

```
第一步：/cx-prd <功能名>
├─ 多轮对话收集需求
├─ 自动评估规模 S/M/L
└─ 生成 PRD 文档

    ↓

第二步：规模检查
├─ S（小）→ 跳过 Design Doc，直接进入第四步
├─ M（中）→ 需要 Design Doc（第三步）
└─ L（大）→ 需要 Design Doc + ADR（第三步 + 补充）

    ↓

第三步：/cx-design <功能名>
├─ 读取 PRD 内容
├─ 定义 API 契约（路径、请求/响应）
├─ 锁定枚举值和字段映射
└─ 生成 Design Doc

    ↓ (仅 L 规模)

第三步-B：/cx-adr <决策点>
├─ 记录架构关键决策
├─ 说明取舍理由
└─ 生成 ADR 文档

    ↓

第四步：/cx-plan <功能名>
├─ 分解 Design Doc 为具体任务
├─ 标注 API 契约下沉到各任务
├─ 标记并行分组（可同时执行的任务）
└─ 生成任务清单

    ↓

第五步：/cx-exec（循环）
├─ 执行下一个 cx-ready 任务
├─ 实现代码
├─ 自动校验是否符合 API 契约
├─ commit 并标记完成
└─ 重复直到全部任务完成

    ↓

第六步：智能代码审查（可选）
├─ 如果 code_review=true（默认），询问审查方式
├─ 选项：全面审查 / 快速检查 / 跳过
├─ 全面审查包括：逻辑 bug + 安全隐患 + 代码质量
└─ 可自动修复 critical 问题或清理 dead code

    ↓

第七步：/cx-summary
├─ 生成功能汇总文档
├─ 按 GitHub 同步模式（off/local/collab/full）创建 Issue/PR
├─ 智能检测是否有新项目规范，询问是否更新 CLAUDE.md
├─ 完成桌面通知
└─ 功能闭环完成 ✅
```

### Bug 修复路径

```
/cx-fix <bug描述>

Step 1: 理解问题
├─ 如果在 collab/full 模式，查看 GitHub Issue 详情
└─ 收集问题背景

    ↓

Step 2: 调查和定位
├─ 使用 Explore subagent 扫描相关代码
├─ 定位错误根因
└─ 评估影响范围

    ↓

Step 3: 修复实现
├─ 编写修复代码
└─ 按项目规范提交

    ↓

Step 4: 测试验证
├─ 运行现有测试用例
├─ 验证 fix 是否有效
└─ 检查是否引入新 bug

    ↓

Step 5: 提交并闭环
├─ commit 修复
├─ 如果在 collab/full 模式，关闭对应 GitHub Issue
└─ Bug 修复完成 ✅
```

## 规模评估详解

PRD 完成后，系统自动评估功能规模，决定后续流程：

### S（小规模）
- 影响: 单个模块或页面
- 新增 API: 0 个或仅修改现有
- 数据库: 无变更
- 架构: 无变更
- **决策**: 跳过 Design Doc，直接 /cx-plan

### M（中规模）
- 影响: 前后端联动
- 新增 API: 1-3 个
- 数据库: 1-2 个表改动
- 架构: 小调整（新中间件、新库）
- **决策**: 需要 /cx-design 定义 API 契约

### L（大规模）
- 影响: 全栈变更
- 新增 API: 4+ 个
- 数据库: 3+ 个表，核心表变更
- 架构: 新技术栈或重大调整
- **决策**: 需要 /cx-design + /cx-adr

## API 契约机制（核心特性）

Design Doc 中定义三大强制章节，锁死前后端对齐规范：

### 1. API 契约
完整的接口定义：

```
POST /api/v1/merchant/certification
Request:  { realName, idCardNumber, businessLicense? }
Response: { code: 0, data: { certificationId, status: "PENDING" } }
Error:    { code: -1, message: "..." }
```

### 2. 状态枚举对照表
统一前后端的枚举值和显示文本：

```
| 后端常量 | API 值 | 前端常量 | 显示文本 |
| PENDING  | "PENDING" | 'PENDING'  | "审核中" |
| APPROVED | "APPROVED" | 'APPROVED' | "已批准" |
```

### 3. VO/DTO 字段映射表
从数据库到前端的完整字段映射链：

```
| DB: real_name | DTO: realName | API: realName | TS: realName |
| DB: id_card   | DTO: idCard   | API: idCard   | TS: idCard   |
```

**契约生命周期**：
1. Design Doc 中定义 → 锁定规范
2. Plan 阶段下沉到各子任务 Issue body → 任务团队可见
3. Exec 执行时自动校验 → 实现必须一致

## GitHub 同步模式

选择适合你的团队规模和协作模式：

### off（纯本地）
- 开发完全在本地
- /cx-summary 仅生成本地 summary.md
- 适合: 单人项目、内部测试

### local（轻量协作）
- 开发在本地，完成时记录
- /cx-summary 创建一个汇总 Issue（供回顾）
- 适合: 单人或小团队回顾

### collab（团队协作推荐）
- PRD / Design Doc 创建为 Issue（供团队 review）
- 任务执行在本地
- /cx-summary 创建汇总 Issue + PR（供最终审查）
- 适合: 2-5 人团队

### full（完整追踪）
- 所有文档和任务都创建 Issue
- CX 1.0 完整行为，本地缓存加速
- /cx-summary 创建汇总 Issue，关闭所有任务 Issue
- 适合: 大团队、严格流程管理

### 在 /cx-config 中切换：
```
/cx-config
→ 修改 github_sync: off / local / collab / full
```

## 当前工作流状态查询

```
/cx-status
```

显示：
- 当前活跃功能（如果有）
- 各功能的进度（已完成/进行中/待处理）
- 最近的 Bug 修复记录
- 下一个待执行任务

## 配置管理

```
/cx-config
```

可以查看或修改：
- `developer_id` — 开发者标识
- `github_sync` — GitHub 同步模式
- `code_review` — 是否启用代码审查
- `agent_teams` — 是否启用前后端 agent 协作
- `background_agents` — 是否允许后台 agent
- `auto_format` — 代码自动格式化开关

## CLAUDE.md 规范守卫

工作流会自动维护项目 CLAUDE.md 中的 CX 段落（通过标记 `<!-- CX-WORKFLOW-START/END -->`）：

- 初始化时创建或更新
- 每次 /cx-exec 更新进度数字
- /cx-summary 完成时智能检测新规范，询问是否更新

**重要**: CX 段落始终保持 ≤30 行（保护 token 效率）。过长的规范放入 references/ 目录。

## 常见问题

**Q: 我想修改规模评估结果？**
A: /cx-prd 阶段重新运行，或手动编辑 `features/{feature_name}/prd.md`。

**Q: 如何中断任务并恢复？**
A: 直接 /cx-exec，会自动从中断点继续。下次会话启动时自动加载上下文。

**Q: API 契约定义了但实现有改动？**
A: Design Doc 更新后重新 /cx-plan，新的契约会下沉到任务。已执行的任务不回溯，在下一个功能 Design Doc 时更新。

**Q: 能否并行执行多个任务？**
A: 可以。/cx-plan 会标注 `parallel_group`，/cx-exec 自动判断可并行的任务，用 Task tool 并行。

**Q: 代码审查不想每次都做？**
A: /cx-config 中设置 `code_review: false`。

**Q: 没有 GitHub 账户或公开仓库？**
A: 使用 `github_sync: off` 或 `local`，完全本地开发。

## 完整工作流手册

更详细的技术细节请参考：
- `.claude/cx/references/workflow-guide.md` — 完整工作流说明
- `.claude/cx/references/contract-spec.md` — API 契约规范说明
- `.claude/cx/references/templates/` — 各阶段模板

## 获取帮助

- `/cx-help` — 显示此文档
- `/cx-status` — 查看当前进度
- 功能执行时遇到问题，直接提问，CX 会诊断并恢复
