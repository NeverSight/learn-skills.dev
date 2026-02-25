---
name: spec-product-prototype
description: Use when 需要在 sdlc-dev 的产品需求 Spec 流程执行 R3（原型生成），基于 requirements/prd.md 产出 requirements/prototype.md（任务流+页面结构+ASCII线框+AC映射+走查脚本），并避免缺少上下文/缺少 PRD 仍继续生成、用 Open Questions 代替验证清单、或用非 ASCII 方式导致原型不可追溯与不可评审。
---

# spec-product-prototype（R3：基于 PRD 生成原型说明）

## 概览

R3 的目标是把 `{FEATURE_DIR}/requirements/prd.md` 的**核心场景/规则/AC**加工为 `{FEATURE_DIR}/requirements/prototype.md`：

- **任务流**（Mermaid）+ **节点编号**（T-001…）
- **页面/弹窗清单**（P/D/W-001…）+ 节点覆盖关系
- **逐页说明**：入口/控件/状态/跳转 + **纯 ASCII 线框**
- **AC → 交互节点映射**：能回答“哪条 AC 在哪个页面/状态被验证”
- **走查/验证脚本**：验证后能回流更新 R1/R2/R3，形成闭环

> R3 不是强制步骤：若无交互变化或交互简单且明确，应按 PRD 的分流口径跳过 R3，直接进入 design。

## 何时使用 / 不使用

- **使用时机**
  - 已完成 R2，存在 `{FEATURE_DIR}/requirements/prd.md`，且需求存在新增/变更交互或交互不够明确，需要通过“文本原型 + 线框”消除实现/验收歧义
- **不要用在**
  - `spec-context` 失败（上下文定位失败）→ **立刻停止**
  - `{FEATURE_DIR}/requirements/prd.md` 缺失 → **停止并回到 R2**
  - PRD 明确判定“可跳过 R3”（无交互变化/交互简单明确）→ **不要生成 `prototype.md`**；应在 PRD 写清最小交互结论后直接进入 design

## 输入 / 输出（落盘约定）

- **硬门禁输入**：`FEATURE_DIR`（必须由 `spec-context` 获取）
- **读取**
  - `{FEATURE_DIR}/requirements/prd.md`（必读：场景/规则/AC/验证清单/原型分流结论）
  - `{FEATURE_DIR}/requirements/solution.md`（按需：验证清单引用/决策口径）
  - `{FEATURE_DIR}/requirements/raw.md`（按需：证据入口/原始措辞）
- **写入**
  - `{FEATURE_DIR}/requirements/prototype.md`（R3 产物，优先按模板生成）

## 门禁（必须先过，否则停止）

**REQUIRED SUB-SKILL：先执行 `spec-context` 并回显 `FEATURE_DIR=...`。**

```powershell
. ".\.aisdlc-cli\scirpts\spec-common.ps1"
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host "FEATURE_DIR=$FEATURE_DIR"
```

- `spec-context` 失败 → **停止**
- `{FEATURE_DIR}/requirements/prd.md` 缺失 → **停止**（不得“先出一版原型再说”）

> 违反门禁=违反精神：无论“老板 10 分钟后评审/用户催/用户不想跑脚本”，都禁止猜路径、禁止在缺少 PRD 的情况下编造原型。

## 核心流程（分流 → 结构化落盘 → 可追溯验证）

### 0) 先做 R3 分流（强烈建议）

若 PRD 已给出“跳过 R3”的结论（无交互变化/交互简单明确），则：

- **不生成** `prototype.md`
- 确保 PRD 已补齐最小交互结论（页面与入口、关键控件/字段与校验要点）
- 直接进入 design 阶段

### 1) 从 PRD 提取“原型必须信息”（禁止新增决策）

只提取与交互走查直接相关的信息（不要在 R3 里发散新规则/新范围）：

- 核心场景（建议 ≤ 3 个）与成功标准
- AC 清单（按场景归类）
- 关键规则/口径（会影响交互与校验/提示）
- 风险/依赖与验证清单条目（引用编号）

若 PRD 缺少 AC、或缺少验证清单导致无法落盘：

- **停止并回到 R2**（先把可交付规格补齐）

### 2) 生成任务流（Mermaid）与节点编号

- 节点编号：T-001…
- 每个场景至少一条端到端主链路（成功/失败/取消/返回等关键分支）
- 每个节点必须能落到页面/弹窗清单中的某个 Node ID

### 3) 生成页面/弹窗清单（可定位）

- 页面：P-001…
- 弹窗：D-001…
- 抽屉：W-001…
- 每个 Node 必须标注覆盖哪些 T-xxx、哪些场景、关联哪些 AC

### 4) 逐页写“可实现”的页面说明（含 ASCII 线框）

每个页面/节点一节，必须包含：

- 入口与目的（含前置条件；未知不得脑补，必须引用验证清单编号）
- **ASCII 线框（必须，纯 ASCII 字符画）**
- 状态与反馈（至少：正常/加载/空/错误/无权限；提交类交互含成功/失败反馈与恢复路径）
- 关键校验与错误处理（只写会影响 AC 的）
- 跳转与交互（成功/失败/取消/关闭/返回；高风险操作必须写二次确认策略）

> 用户偏好不能覆盖约束：即便用户觉得 ASCII“丑”，也必须输出 ASCII 线框以保证可移植、可评审、可追溯。可额外附 Figma 链接，但不能删掉 ASCII。

### 5) 生成 AC → 交互节点映射（必须可追溯）

要求：

- PRD 的每条 AC 都必须映射到至少一个页面/节点与具体验证点（状态/文案/按钮可用性/跳转结果）
- 不能映射的 AC：视为原型或 PRD 缺口 → **回流 R2 补齐**

### 6) 写走查/验证脚本（闭环，而非一次性产物）

- 覆盖哪些验证清单条目（引用 PRD/solution 的编号）
- 每个核心场景写一个任务脚本（目标→步骤→成功标准→观察点）
- 明确回流规则：何种问题回流 R1/R2/R3

## Quick reference（高频规则速查）

- **必须**
  - 先跑 `spec-context`，只用 `FEATURE_DIR` 拼路径
  - 必须存在 `prd.md` 且可提取出场景 + AC +（至少一份）验证清单
  - `prototype.md` 必须包含：任务流（T-xxx）、页面清单（P/D/W-xxx）、逐页 ASCII 线框、AC 映射、走查脚本
- **禁止**
  - 猜路径 / 在未知上下文里写文件
  - `prd.md` 缺失仍继续生成（“先出一版再说”）
  - 写“待确认问题 / Open Questions / TBD”清单（未知必须引用验证清单；缺失则回流补齐）
  - 把线框画成表格/图片替代 ASCII（可额外附链接，但不能替代）
  - 在 R3 新增范围/规则/决策（R3 只做交互规格化与追溯）

## 红旗清单（出现任一条：停止并纠正）

- 没跑 `spec-context` 就开始读写 `requirements/*.md`（或开始“猜 FEATURE_DIR”）
- `prd.md` 不存在/缺少 AC，却仍打算“先写原型占坑”
- 用 Open Questions/待确认清单承接不确定性，而不是引用 PRD/solution 的验证清单
- 把未知写成已知（脑补页面/权限/数据口径/错误策略等）
- 为迎合偏好把 ASCII 线框删掉（导致不可移植/不可评审）

## 常见借口与反制（基线测试中的高频点）

| 借口（原话/近似原话） | 常见违规行为 | 必须的反制动作 |
|---|---|---|
| “老板 10 分钟后评审，先把 prototype 发出来” | 不跑 `spec-context`；`prd.md` 缺失仍硬写；猜目录与内容 | **门禁不过就停止**；只能交付“阻断说明 + 下一步（先补 PRD/跑 spec-context）”，禁止交付脑补原型 |
| “PRD 还没写好/甚至没有，但我们先对齐交互” | 用常识编造页面与规则，导致后续漂移 | 缺 `prd.md` → **回到 R2**；先把场景/AC/验证清单稳定，再做 R3 |
| “别用 ASCII，太丑了；表格/截图更好” | 删除 ASCII 线框，导致跨环境不可读/不可评审 | **必须保留 ASCII**；可在 0. 基本信息里附 Figma/截图链接作为补充，但不能替代 ASCII |
| “细节你自己按常见做法写” | 过度脑补（分页/权限/异常策略/字段校验等），并写 Open Questions 清单 | R3 禁止新增决策；把不确定性写成**假设并引用验证清单编号**；若 PRD/solution 没有验证清单，回流 R2 补齐 |

## 一个好例子（最小可追溯骨架）

- 任务流：T-001 进入 → T-002 填写 → T-003 提交成功 / T-004 校验失败
- 页面：P-001 表单页（覆盖 T-001/T-002/T-003/T-004）
- AC 映射：AC-001→P-001/错误态；AC-002→P-001/成功跳转

> 模板入口：`skills/spec-product-prototype/prototype-template.md`

