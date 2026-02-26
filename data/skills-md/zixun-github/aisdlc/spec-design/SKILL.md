---
name: spec-design
description: Use when 需要为某个 Spec Pack 产出 D2 决策文档（RFC/Decision Doc），并在压力下仍需自主决定是否执行 D0（分流跳过设计）与 D1（可选调研），避免猜 FEATURE_DIR、脑补输入、把设计写成实现细节或遗留 TODO/待确认清单。
---

# spec-design

## 概览

本技能用于执行 Spec 级“设计阶段”的 D2：产出可评审的 **决策文档（Decision Doc / RFC）**，并能在执行前**自主决策**是否需要先做 D0（分流：跳过/不跳过设计）与 D1（research：可选调研）。  
核心原则：**门禁优先（spec-context）→ 先分流（D0）→ 按需调研（D1）→ 决策落盘（D2）**。在任何压力下都禁止猜路径、禁止在缺少 SSOT 时脑补推进。

**开始时宣布：**「我正在使用 spec-design 技能产出设计决策文档（design/design.md / RFC）。」

## 何时使用 / 不使用

- **使用时机**
  - 用户要求产出 `design/design.md`（RFC/Decision Doc），或“做设计再进入 implementation”。
  - 你需要判断“是否可以跳过设计阶段”、以及“是否需要先 research”。
  - 你被要求把接口字段/表结构/任务拆分塞进设计文档，担心文档分层被破坏。
- **不要用在**
  - 需求尚未完成 R1（没有 `requirements/solution.md`）：先完成需求澄清与方案决策（见 `spec-product-clarify`）。
  - 用户明确只要 implementation 计划与任务：直接走 implementation（但仍需 `spec-context`）。

## 快速参考

- **硬门禁（第一优先级）**：任何读写 `{FEATURE_DIR}/design/*.md` 之前，必须先执行 `spec-context` 得到 `FEATURE_DIR=...`；失败立刻停止。
- **最短路径**
  - **跳过路径**：D0 判定跳过 → 不写 `design/*.md` → 进入 implementation（`plan.md` 补齐最小决策信息）。
  - **常规路径**：D0（不跳过）→（可选）D1 → D2（写 `design/design.md`）→ implementation。
- **输出位置**
  - D1（可选）：`{FEATURE_DIR}/design/research.md`
  - D2（必做，未跳过时）：`{FEATURE_DIR}/design/design.md`

- **最小化模板**
  - D1：`skills/spec-design-research/research-template.md`（复制到 `{FEATURE_DIR}/design/research.md` 再填写）
  - D2：`skills/spec-design/design-template.md`（复制到 `{FEATURE_DIR}/design/design.md` 再填写）

- **决策速查表**

| 你在判断什么 | 触发信号（任一命中） | 动作 |
|---|---|---|
| 是否能开始写任何 `design/*.md` | 没有 `FEATURE_DIR=...` 或 `solution.md` 缺失/不可追溯 | **停止**；先修上下文/补 SSOT |
| D0：是否跳过 design 阶段 | 范围单一、无对外承诺变化、无关键不确定性、验收口径已足够 | **可跳过**；改在 implementation `plan.md` 补齐最小决策信息 |
| D0：是否必须进入 D2 | 对外契约/权限/数据口径变更；数据迁移/回滚；关键不确定性；跨系统影响面大 | **不跳过**；进入 D1（按需）→ D2 |
| D1：是否需要 research.md | 方案正确性依赖未知事实；多方案缺证据；高风险点需先验证 | **执行 D1**，写 `design/research.md` 并给出验证清单 |
| D2：是否允许写实现细节/任务/DDL | 被要求“为了开发方便写进去” | **拒绝混层**；只写对外承诺要点 + 追溯链接，细节下沉 contracts/ADR/implementation |

## 实施步骤（Agent 行为规范）

### 0) 门禁：定位 `{FEATURE_DIR}`（必须）

> **红线**：不得猜 `.aisdlc/specs/...`，不得用当前工作目录拼相对路径。

```powershell
$repoRoot = (git rev-parse --show-toplevel)
. (Join-Path $repoRoot "skills\spec-context\spec-common.ps1")
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host "FEATURE_DIR=$FEATURE_DIR"
```

若上面报错 → **立刻停止**（不要生成/写任何 `design/*.md` 内容）。

### 1) 读取最小必要输入（缺失则停止）

- **必读（需求侧 SSOT）**：`{FEATURE_DIR}/requirements/solution.md`
- **按需**：`{FEATURE_DIR}/requirements/prd.md`、`{FEATURE_DIR}/requirements/prototype.md`
- **按需（项目级）**：`project/memory/*`、相关 `project/contracts/`、`project/adr/` 索引
- **若存在**：`{FEATURE_DIR}/design/research.md`、`{FEATURE_DIR}/design/design.md`

**停止条件（不得脑补继续）：**

- 找不到或无法读取 `requirements/solution.md`。
- 需求的 In/Out、验收口径、关键约束无法从输入追溯。

### 2) D0：分流（是否跳过设计阶段）

#### 2.1 何时可以“直接跳过 design 阶段”（满足其一即可考虑跳过）

- **范围单一、边界清晰**：几乎不涉及跨模块协作与系统性风险
- **无对外承诺变化**：无新增/变更对外契约（API/事件/权限/数据口径），且无数据迁移
- **无关键技术不确定性**：不需要先 research 验证
- **验收口径已足够**：验收在 `solution.md`（或 `prd.md`）已清晰、可测试、可追溯

#### 2.2 何时“不要跳过”（任一命中则默认不跳过）

- 新增/变更 **对外契约**（API/事件/权限/数据口径），或需要更新 `project/contracts/`
- 存在 **数据迁移/回滚** 风险，或需要新增/更新 ADR
- 有明确 **关键不确定性**（性能/安全/一致性/依赖/合规/网关能力/存储策略等）
- 涉及多个系统/团队/上下游，或影响面难以一句话界定

#### 2.3 覆写规则（防止“本可跳过但必须评审”）

即使满足跳过口径，若出现以下之一，仍 **不跳过**（进入 D2）：

- 用户/团队明确要求出 RFC 以便评审对齐
- 近期同类改动频繁返工/事故，需通过决策文档冻结口径

#### 2.4 D0 的最小输出（不落盘也可以）

输出一个可引用的结论段（3–7 条理由以内）：

- **结论**：跳过 / 不跳过
- **依据**：对应上面口径（可追溯到 `solution.md` / 合同/ADR 入口）
- **若跳过**：列出 implementation 的 `plan.md` 必补齐的最小决策信息：
  - 目标、范围与边界、关键约束、验收口径、验证清单（Owner/截止/信号/动作）

### 3) D1：research（可选调研；只在需要时做）

#### 3.1 触发 D1 的信号（命中任一则做）

- 方案正确性依赖未知事实（“如果 X 不成立，方案会推倒重来”）
- 存在多个可行方向，且缺少证据支撑取舍
- 对外契约/迁移/安全/性能/一致性存在高风险点，需要先验证

#### 3.2 何时跳过 D1

- 不确定性已在输入中被证据化（`solution.md`/已有 `research.md` 已覆盖关键风险与验证清单）
- 本次 D2 仅是低风险的小范围变更，且无关键未知

#### 3.3 `design/research.md` 最小结构（写结论，不写问题清单）

> **红线**：不要留下“待确认问题清单 / TODO 列表”。未知统一用“假设 + 验证清单”承接。

- **TL;DR（3–7 行）**：现状 + 最大风险 + 推荐方向
- **现状与问题域**
- **范围边界与不变量**
- **关键约束**
- **风险与验证清单（必填）**：风险/假设 → 验证方式 → 成功/失败信号 → Owner → 截止 → 下一步动作
- **备选与权衡（可选）**

### 4) D2：design（决策文档 / RFC；未跳过时必做）

#### 4.1 D2 的定位（写“决策”，不写“实现”）

- **只写**：为什么这样做、边界怎么裁切、方案与权衡、对外承诺要点、怎么验证、影响与迁移/回滚要点。
- **不写**：实现步骤、任务拆分、代码级细节、接口字段逐一罗列、DDL 细节。
  - 若必须对外承诺字段/兼容性：在本文写“要点 + 追溯链接”，细节下沉到 `project/contracts/` 或 ADR。

#### 4.2 `design/design.md` 建议最小结构（模板）

**必须使用最小化模板**生成 design.md（避免结构漂移）：

1) 复制 `skills/spec-design/design-template.md` 的内容  
2) 粘贴到 `{FEATURE_DIR}/design/design.md`  
3) 按模板把占位符补齐（尤其是 C4 L1–L3、备选方案、风险与验证清单、追溯链接）

> 写作约束：只保留支撑决策/验收/演进的最小信息；不要新增“待确认问题/TODO”章节；不要写实现细节/任务拆分/字段清单/DDL。

#### 4.3 D2-DoD（缺一不可）

- In/Out 明确，且能追溯到 `solution.md`
- 推荐方案用 C4 **L1+L2+L3** 说清楚，层次可追溯
- 关键决策说明“为什么选它/备选为何不选”
- 不确定性已收敛：未知全部进入“假设 + 验证清单”（Owner/截止/动作明确）

## 红旗（出现任一即停止并纠偏）

- 没有先拿到 `FEATURE_DIR=...` 就开始写 `design/*.md`
- 找不到 `requirements/solution.md` 还继续写设计（=脑补）
- 用“待确认问题清单 / TODO”悬空未知（应改为“假设 + 验证清单”）
- 把 D2 写成实现规格：任务拆分、实现步骤、字段/DDL 细节
- 缺少备选方案或缺少验证清单（导致无法评审/无法落地）

## 压力下的反合理化（常见借口 → 对应动作）

| 常见借口 | 对应规则 / 动作 |
|---|---|
| “先随便写到 `design/design.md`，回头再挪” | **禁止猜路径**：先 `spec-context` 拿到 `FEATURE_DIR`；否则停止 |
| “信息不全也能先出初稿，后面再补” | **禁止脑补**：缺 `solution.md` 或不可追溯就停止；把未知改写为“假设 + 验证清单” |
| “主管/PM 说不要门禁/不要查文档” | 门禁是硬规则：`Get-SpecContext` 失败就停止；不因权威压力破例 |
| “为了开发快，把任务/DDL/字段都写进设计” | **拒绝混层**：D2 只写决策与对外承诺要点 + 追溯链接；细节进 contracts/ADR/implementation |
| “没时间做备选/验证清单” | 备选与验证是 D2-DoD：缺失会导致无法评审/返工；宁可缩短正文也不删 DoD 项 |

## 常见错误（以及修复）

- **错误**：在压力下“先写了再说”，先生成文档再补输入。  
  **修复**：先过 `spec-context` 与 `solution.md` 门禁；缺失就停止，写清楚阻塞项。
- **错误**：把 research 当成“查资料”，写了很多背景但没有验证清单。  
  **修复**：把未知全部转成“风险/假设 → 验证方式 → 信号 → Owner/截止/动作”。
- **错误**：PM 要求把任务/接口/表结构写进设计，于是混层。  
  **修复**：设计文档只保留“对外承诺要点 + 追溯链接”；实现细节移入 implementation 或 contracts/ADR。

