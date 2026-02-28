---
name: project-discover
description: Use when 需要对“已有代码的存量项目”做 Discover（逆向）并把仓库事实沉淀为 `.aisdlc/project/`，且你发现 AI/团队经常猜入口、猜边界、索引与细节双写、或缺证据链导致反复返工。
---

# project-discover（一次指令全量 Discover 总控：地图层 + 权威入口 + 证据链）

## 概览

本技能用于把“已有代码的存量项目”**在一次指令内尽可能完整地**逆向沉淀为 `.aisdlc/project/` 项目级 SSOT（长期资产），以支撑后续 Spec Pack 的 AI 辅助开发**尽量不再重复跑 Discover**。

Discover 的核心不是“把代码翻译成文档”，而是把以下三件事立起来（并且能被持续维护）：

- **地图层**：先有可导航的索引骨架（索引只导航）
- **权威入口**：每个 P0 模块有单页模块 SSOT（模块页是权威）
- **证据链**：每个关键结论都能指向仓库内可定位的证据入口（Evidence）或结构化缺口（Evidence Gaps）

**开始时宣布：**「我正在使用 project-discover 技能执行存量项目 Discover（逆向）并建立 `.aisdlc/project/` 项目级 SSOT。」  

## 目标（一次指令的交付物）

在**单次运行**结束时，默认应至少产出并自洽以下内容（允许“证据不足→结构化缺口”降级，但不允许脑补）：

- **Level-0 / Memory（北极星）**
  - `.aisdlc/project/memory/structure.md`
  - `.aisdlc/project/memory/tech.md`
  - `.aisdlc/project/memory/product.md`
  - `.aisdlc/project/memory/glossary.md`
- **Level-1 / 地图索引（只导航 + 进度面板）**
  - `.aisdlc/project/components/index.md`（含 direct-only 依赖图）
  - `.aisdlc/project/products/index.md`（建议；可按证据决定是否创建）
- **模块页（权威入口，优先 P0，尽可能多）**
  - `.aisdlc/project/components/{module}.md`：对每个识别到的 **P0 模块**尽可能创建并填充到 DoD；对 P1 模块尽可能创建（允许一段契约降级到 Evidence Gaps）；P2 默认仅索引占位
- **Ops（高 ROI；有证据则创建）**
  - `.aisdlc/project/ops/index.md`（以及 monitoring/rollback/runbook 等入口页，能链接到真实平台/配置/脚本时再加）
- **治理能力（可持续）**
  - DoD/勾选门禁规则能落地执行（“模块完成”只看模块页达标）
  - 增量 Discover（Delta Discover）与 stale（过期）机制在文档里有入口与写法约束（至少体现在模块页 frontmatter 与 products/ops/memory 的 Evidence Gaps）

## 何时使用 / 不使用

- **使用时机**
  - 你要为存量项目建立/补齐 `.aisdlc/project/`（memory / components / products / ops / nfr）
  - 你发现“入口在哪里、边界是什么、契约在哪”总是靠猜，导致 AI 或新人反复问同样的问题
  - 你担心索引与细节双写、字段大全、TODO 散落、契约不权威造成维护爆炸
  - 你要做增量 Discover（Delta Discover）来对抗知识过期（stale）
- **不要用在**
  - 你在做**需求级 Spec Pack** 的 `requirements/` / `design/` / `implementation/`（那是 spec-* 技能链路）
  - 你要写“字段级数据字典”作为合规/对账/KPI 口径治理的独立体系（这不是 Discover 的默认目标）

## 核心硬规则（出现任一条：停止并纠正）

1. **禁止产出 `.aisdlc/project/contracts/**`**
   - API/Data 契约必须合并进模块页：`.aisdlc/project/components/{module}.md` 的固定段落 `## API Contract` / `## Data Contract`
2. **索引只导航**
   - `.aisdlc/project/components/index.md` 与 `.aisdlc/project/products/index.md` 不得写不变量/字段/详细流程/“待补”
3. **模块页单页 SSOT（权威入口）**
   - P0 模块必须存在模块页，并包含固定标题（锚点稳定）：`## TL;DR`、`## API Contract`、`## Data Contract`、`## Evidence（证据入口）`、`## Evidence Gaps（缺口清单）`
4. **不脑补：缺证据就写 Evidence Gaps**
   - 不允许用“待补/未发现/TODO”散落正文；缺口必须进入 `## Evidence Gaps（缺口清单）`，结构化写清楚“缺什么/去哪找/影响”
5. **先 Scope 止损**
   - Discover 最大风险是覆盖面失控：必须先做 P0/P1/P2；P0 先做三件套（模块页 + 契约段落 + 证据链）再扩
6. **Products 收敛到 <= 6（默认）**
   - 业务模块地图是“业务语义锚点”，不是功能清单大全；过多会让地图失效

## 一次指令执行策略（总控编排，不反复运行）

本技能是“总控编排器”。执行时不要把工作拆成多轮让用户反复触发；而是在本次运行中完成：

- **先建地图骨架**（Memory + Index）
- **再并行补模块页**（P0 尽可能多，P1 尽可能覆盖，P2 只占位）
- **并行收敛 Products 与补 Ops**（有证据就落盘；缺证据写缺口）
- **最后做 DoD/一致性门禁回填**（哪些模块能打勾、哪些不行，原因在模块页 Evidence Gaps）

为确保输出可维护，Discover 拆成 4 个可交付域（对应现有子技能），但应在一次运行中完成并汇总：

| 你现在要做什么 | 用哪个子技能 | 主要输出位置 |
|---|---|---|
| 盘点“可作为证据的入口”，并做 P0/P1/P2 止损 | `project-discover-preflight-scope` | `.aisdlc/project/components/index.md`（priority/owner/code_entry 等）+ 证据入口清单落位到后续 memory/ops |
| 建立 Level-0 北极星与 Level-1 索引骨架（地图层） | `project-discover-memory-index` | `.aisdlc/project/memory/*` + `.aisdlc/project/components/index.md` + `.aisdlc/project/products/index.md` |
| 逐个把 P0 模块做成“单页模块 SSOT + 契约段落 + 证据链” | `project-discover-modules-contracts` | `.aisdlc/project/components/{module}.md` |
| 收敛 Products、补 Ops 入口、做 DoD 勾选门禁、建立增量维护 | `project-discover-products-ops-dod` | `.aisdlc/project/products/*` + `.aisdlc/project/ops/*` + DoD/Delta/过期规则 |

> **默认策略（尽可能丰富）**：不把 P0 限制在 1–3 个；在预算允许范围内，尽可能为所有识别到的 P0 都创建模块页并填充到可用门槛。若仓库过大导致无法全覆盖：仍然要完成 memory + index，并为未覆盖的 P0/P1 留下“可追溯的 Evidence Gaps 与候选证据位置”，而不是空白或脑补。

## 并行化建议（可选，但高 ROI）

当你面对 2+ 个互不依赖的任务域时，建议使用并行子代理（参考 `dispatching-parallel-agents`）。本技能的目标明确允许并鼓励把 **Modules** 与 **Products/Ops** 拆给独立子代理并行处理。

- **Preflight 并行**：分别扫描 run/test/ci/contract/ops 的证据入口
- **Modules 并行**：每个 P0 模块一个子代理（互不改同一模块页；不要让多个代理改同一个 `components/{module}.md`）
- **Products 并行**：1 个子代理负责 products 收敛与 `products/*`（只写入口级摘要，避免字段/流程大全）
- **Ops 并行**：1 个子代理负责 ops 入口与证据（监控/告警、日志入口、回滚入口），只要能给出真实入口就落盘，否则写 Evidence Gaps

### 并行分工硬约束（防冲突/防漂移）

- **总控（你）唯一可写范围**：
  - `.aisdlc/project/memory/*`
  - `.aisdlc/project/components/index.md`
  - `.aisdlc/project/products/index.md`
  - DoD 勾选回填与一致性校验（最终汇总）
- **模块子代理写入范围**：仅写自己负责的 `.aisdlc/project/components/{module}.md`
- **products 子代理写入范围**：仅写 `.aisdlc/project/products/*`（不改 components/index）
- **ops 子代理写入范围**：仅写 `.aisdlc/project/ops/*`

### 子代理输入（必须给清楚，避免“自创结构”）

给每个子代理的任务描述必须包含：

- 该代理**允许写入的路径白名单**
- 该页的**固定标题/锚点要求**（尤其模块页的 `## TL;DR / ## API Contract / ## Data Contract / ## Evidence / ## Evidence Gaps`）
- “**缺证据就写 Evidence Gaps，不许脑补**”的硬规则
- 要求输出“**权威入口链接 + 不变量摘要 + 证据入口**”的最小粒度（文件/类/job/命令）

## 常见借口与反制（来自基线压测）

> 这些借口来自“无技能约束”的基线压测原话。写入这里的目的，是为了在时间/权威/沉没成本压力下，仍能守住 Discover 的硬规则。

| 借口（原话风格） | 最常见违规 | 必须的反制动作 |
|---|---|---|
| “先把文档写全，结构搭满，细节后面再对代码补。” | 索引写细节；TODO 散落；脑补契约 | 先做 Scope + Index 骨架；所有细节下沉模块页；缺证据写 Evidence Gaps，不写推测 |
| “索引太干会没人看，写点说明不用点进去就懂。” | 索引变成细节堆（双写） | 索引只导航：只放链接/复选框/owner/code_entry；细节只在模块页 |
| “没有 Swagger/OpenAPI，先按经验写一版契约，标‘待核对’。” | 契约不权威；字段大全；错口径被放大 | 模块页契约段落只写：权威入口（文件/生成命令）+ 不变量摘要 + 证据入口；缺权威入口→Evidence Gaps |
| “时间紧，先把不确定的用‘待补/未发现’标出来，表示诚实。” | “待补”散落导致永远补不完 | 所有缺口集中到 `## Evidence Gaps`，并写：缺口/期望粒度/候选证据位置/影响 |
| “已经写了一半，再改成索引只导航要大改；先交差。” | 沉没成本驱动的结构性违规 | 删除/移动：把索引细节挪到模块页；索引回归导航；不能因为沉没成本违反结构规则 |
| “字段列全一点查起来方便。” | 字段大全（维护爆炸） | 字段级细节只通过权威入口链接（schema/DDL/model）；在 project 层只写不变量摘要 |
| “怎么跑/怎么部署是刚需，写在项目级入口最合适。” | 一次性交付细节污染项目级 | 项目级只写**入口链接**与最小护栏；详细操作手册归 ops 体系或外部平台链接 |

## 红旗清单（出现任一条：停止并纠正）

- 在 `.aisdlc/project/components/index.md` 或 `products/index.md` 里写了不变量/字段/详细流程
- 出现 `.aisdlc/project/contracts/**`
- 出现大量“TODO/待补/未发现”散落正文（未汇总到 `Evidence Gaps`）
- P0 模块打了 `- [x]`，但模块页缺少固定标题或缺少权威入口/不变量/证据入口
- 为了“写全”而把 Products 写成 20+ 个模块的功能清单

## 一致性与完成门禁（本次运行结束前必须做）

在一次指令的末尾，总控必须完成以下校验与回填，确保知识库“能用且不自相矛盾”：

- **索引只导航校验**：`components/index.md` / `products/index.md` 不出现不变量/字段/详细流程/“待补/未发现/TODO”
- **模块页达标校验（决定能否打勾）**：
  - P0：模块页存在；固定标题齐全；frontmatter 元数据齐全；API/Data 契约段落存在“权威入口 + 3–7 条不变量 + 证据入口”；若存在缺口必须写到 Evidence Gaps，且该模块不得勾选
  - P1：允许 API 或 Data 其一缺失，但必须 Evidence Gaps 结构化记录缺口与影响
  - P2：默认不勾选
- **SSOT 门禁**：索引中的勾选只是反映模块页是否达标；不得“先勾选再补内容”
- **依赖图维护**：`components/index.md` 的 Mermaid 依赖图只画 direct-only，并标注交互方式（API/Event/DB）
- **Products 收敛**：默认 <= 6；无法收敛必须给出原因与治理建议入口（不要把它写成大目录）

## Quick reference（高频速查）

### 最小可用交付（MVP）

- `.aisdlc/project/memory/structure.md`：怎么跑/怎么验/怎么发布的入口（可追溯）
- `.aisdlc/project/components/index.md`：模块地图（只导航）+ 复选框进度 + 依赖图
- 1–3 个 P0 模块页：`.aisdlc/project/components/{module}.md`（含 TL;DR + API/Data 契约段落 + Evidence/Evidence Gaps）

### DoD 的一句话

**模块是否“完成”，只由模块页内容是否达标决定；索引勾选只是反映这一事实。**

## 常见错误

- 把 Discover 做成“字段级字典工程”（维护爆炸）
- 先写细节再补地图（导致双写与断链）
- 看到缺口就脑补（下游会把猜测当事实）
- 把需求级一次性交付细节合并进项目级（项目级变成垃圾场）

