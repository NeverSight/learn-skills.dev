---
name: spec-design-research
description: Use when 需要在 Spec 级设计阶段执行 D1 research（产出 `{FEATURE_DIR}/design/research.md`），或面对关键不确定性/高风险点需要先验证而不是直接进入 D2；常见症状包括缺少证据支撑取舍、未知项被写成 TODO/待确认问题、在压力下想猜 FEATURE_DIR 或把调研写成实现细节。
---

# spec-design-research

## 概览

本技能用于执行 Spec 级设计阶段的 **D1 research（可选）**：为 design 决策补足上下文与证据，并把未知收敛为**可执行的验证清单**，使 D2 可以直接引用结论而无需重复解释。  
本技能既可独立使用（只做 D1），也可作为 `spec-design` 的子技能被调用（当 D0 判定“不跳过”且命中 D1 触发信号时）。

**开始时宣布：**「我正在使用 spec-design-research 技能进行设计调研并落盘 research.md。」

## 何时使用 / 不使用

- **使用时机（命中任一）**
  - 方案正确性依赖未知事实（若 X 不成立，方案会推倒重来）
  - 存在多个可行方向，但缺少证据支撑取舍
  - 对外契约/迁移/安全/性能/一致性等存在高风险点，需要先验证
  - 你发现自己要写“待确认问题清单 / TODO”，但无法给出验证方式与下一步动作
- **不要用在**
  - 需求侧 SSOT 还没落盘（缺 `requirements/solution.md`）：先完成 R1（见 `spec-product-clarify`）
  - 不存在关键不确定性，且 `solution.md` 已经把关键约束与验收口径证据化：可跳过 D1 直接进入 D2

## 快速参考

- **唯一落盘位置**：`{FEATURE_DIR}/design/research.md`
- **最小化模板**：`skills/spec-design-research/research-template.md`（复制到上面路径再填写）
- **D1-DoD（缺一不可）**
  - 未知项不以“待确认问题”形式悬空：全部进入“风险与验证清单”
  - 研究结论可追溯，并能被 D2 直接引用（结论短、证据清、可复用）
- **禁止事项**
  - 禁止猜 `FEATURE_DIR` / 手写 `.aisdlc/specs/...` 路径
  - 禁止在 research.md 写实现规格（任务拆分/字段清单/DDL/脚本步骤）
  - 禁止输出“TODO 列表”替代验证清单
  - 禁止在 D1 擅自新建契约/ADR/实现规格文件或目录：D1 只产出 `design/research.md`；若需要更新 `project/contracts/` 或 `project/adr/`，在 research 里写“需要更新的入口 + 要点”，把实际落盘留给 D2（或用户明确要求的操作）

## 实施步骤（Agent 行为规范）

### 0) 门禁：定位 `{FEATURE_DIR}`（必须）

> 任何读写 `{FEATURE_DIR}/design/*.md` 之前，必须先执行 `spec-context`；失败立刻停止。

```powershell
$repoRoot = (git rev-parse --show-toplevel)
. (Join-Path $repoRoot "skills\spec-context\spec-common.ps1")
$context = Get-SpecContext
$FEATURE_DIR = $context.FEATURE_DIR
Write-Host "FEATURE_DIR=$FEATURE_DIR"
```

### 1) 读取最小必要输入（缺失则停止）

- **必读**：`{FEATURE_DIR}/requirements/solution.md`
- **按需**：`{FEATURE_DIR}/requirements/prd.md`、`{FEATURE_DIR}/requirements/prototype.md`
- **按需（项目级）**：`project/memory/*`、相关 `project/contracts/`、`project/adr/` 索引

**停止条件（不得脑补继续）：**

- 找不到或无法读取 `requirements/solution.md`
- `solution.md` 中的 In/Out、验收口径、关键约束不可追溯/不可测试（需要先回到 R1 补齐）

### 2) D1 是否需要执行（自检；避免“为调研而调研”）

若同时满足以下条件，可 **跳过 D1**（转入 D2）：

- 关键不确定性已在 `solution.md` 或既有 `design/research.md` 中被证据化
- 风险与验证清单已完整且可执行

否则进入步骤 3 编写/更新 `design/research.md`。

### 3) 把“未知项”转成“假设 + 验证清单”（核心机制）

> **硬规则**：research.md 不出现“待确认问题清单 / TODO”。未知一律转成验证清单条目。

转译模板（每条未知都必须落到表格里）：

- **风险/假设**：一句话描述不确定性（可含前提）
- **验证方式**：如何在最小成本下验证（调研/访谈/实验/压测/PoC/演练/数据回放）
- **成功/失败信号**：观测到什么算通过/不通过
- **Owner / 截止**：谁负责、何时前必须得到信号（避免无限期悬空）
- **下一步动作**：通过做什么/不通过做什么（分支动作）

### 4) 编写 `{FEATURE_DIR}/design/research.md`（最小结构）

**必须使用最小化模板**生成 research.md（避免结构漂移）：

1) 复制 `skills/spec-design-research/research-template.md` 的内容  
2) 粘贴到 `{FEATURE_DIR}/design/research.md`  
3) 按模板把占位符补齐（尤其是“验证清单”必须可执行）

> 写作约束：只保留支撑 D2 决策的最小信息；未知统一进入“验证清单”；不要新增“待确认问题/TODO”章节。

### 5) D1 输出后的衔接（给 D2 可直接引用的输入）

在 research.md 里确保以下内容可被 D2 直接引用：

- TL;DR 中的推荐方向是“机制级一句话”，而非实现步骤
- 每个关键结论都能追溯到：`solution.md`、contracts/ADR 索引或验证清单条目编号
- 验证清单可直接映射到 D2 的“风险与验证清单”（Owner/截止/动作不丢失）

## 红旗（出现任一即停止并纠偏）

- 没有 `FEATURE_DIR=...` 就开始写/改 `design/research.md`
- 缺 `requirements/solution.md` 仍继续写 research（=脑补）
- 出现“待确认问题清单 / TODO”，但没有验证方式/Owner/截止/动作
- research.md 变成实现文档：字段/DDL/迁移脚本/任务拆分
- TL;DR 超过 7 行或全是背景，没有“最大风险 + 推荐方向”

## 压力下的反合理化（常见借口 → 对应动作）

| 常见借口 | 对应规则 / 动作 |
|---|---|
| “先写到仓库根目录，回头再挪到 spec 里” | 禁止猜路径：先 `spec-context` 拿到 `FEATURE_DIR`，否则停止 |
| “没有 solution.md 也能先 research，缺的后补” | 禁止脑补：缺 `solution.md` 直接停止，先回到 R1 补齐 SSOT |
| “来不及写验证清单，先列 TODO” | TODO 违规：把每条 TODO 改写为验证清单（含 Owner/截止/信号/动作） |
| “PM 要求写细（字段/DDL/脚本）给开发” | 拒绝混层：research 只写结论/证据/验证；在 research 里写“需要更新的 `project/contracts/` / `project/adr/` 入口 + 要点”，不在 D1 写字段/DDL/脚本 |
| “我已经写了很多实现草稿，不想浪费” | 沉没成本无效：把草稿迁出 research；research 正文只保留可引用结论与取舍依据 |

## 常见错误（以及修复）

- **错误**：research 写成百科背景，缺少可执行验证。  
  **修复**：压缩背景到“决策所需最小信息”，把未知全部转为验证清单。
- **错误**：把未知留成“待确认问题清单”。  
  **修复**：用“风险/假设 → 验证方式 → 信号 → Owner/截止 → 动作”改写，并编号。
- **错误**：把接口字段/表结构写进 research，导致 D2 难以维护。  
  **修复**：research 仅写“对外承诺要点 + 追溯链接（`project/contracts/` / `project/adr/` 入口）”，字段/DDL/脚本留给 D2 或 implementation。

