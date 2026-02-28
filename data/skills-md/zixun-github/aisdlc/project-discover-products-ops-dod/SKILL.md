---
name: project-discover-products-ops-dod
description: Use when 你已经有了 components 地图与若干模块页，现在需要收敛业务模块（products<=6）、固定运行/排障/回滚入口（ops）、并执行 DoD 门禁与增量 Discover（Delta Discover、stale 过期检测）来保证知识库可用且可维护。
---

# project-discover-products-ops-dod（Step5+6+7+11：Products + Ops + DoD + 增量维护）

## 概览

这一阶段把 Discover 从“能写出来”升级到“能治理、能持续可用”：

- **Products**：把业务模块地图收敛到可治理数量（默认 <= 6），为需求阶段提供稳定语义锚点
- **Ops**：固定“能跑、能验、能回滚、能排障”的入口（高 ROI）
- **DoD**：用门禁规则决定是否允许索引打勾（索引勾选只是反映事实）
- **Delta Discover / stale**：让知识库能随代码变化增量更新，不快速过期

**开始时宣布：**「我正在使用 project-discover-products-ops-dod 技能收敛 Products、建立 Ops 入口并执行 DoD 与增量维护门禁。」  

## Products（业务模块聚合与收敛 <= 6）

### 核心原则

- Products 是**业务地图**，不是功能清单大全
- 优先用“数据主责 + 对外能力 + 组织边界”来聚类
- 默认目标：<= 6；如果无法收敛，必须写明原因与治理建议入口

### 从代码反推 Products 的高信号线索（建议顺序）

1. **数据主责**：哪个组件主写哪些核心对象（来自模块页 `## Data Contract`）
2. **对外能力边界**：哪些 API 是稳定承诺（来自模块页 `## API Contract`）
3. **组织边界**：owner/team 划分（来自 `components/index.md`）
4. **运行边界**：独立部署/SLO 的单元（如果证据存在）

### `products/index.md` 最小模板（只导航）

```markdown
# Products Index（业务地图：只导航）

> 建议收敛到 <= 6 个业务模块。这里不是功能清单。

| product | owner | entry | related_components | status |
|---|---|---|---|---|
| commerce | team-a | ./commerce.md | auth, order, payment | - [ ] |
```

### `products/{product}.md` 建议只写“入口级摘要”

- TL;DR（业务边界一句话）
- Capability Catalog（CAP-001 粒度：能力名 + 一句话 + 证据入口）
- Business Rules Index（规则名 + 一句话 + 代码证据入口）
- Domain Events（事件名 + 语义一句话 + 证据入口）

> **禁止**：把产品页写成字段大全/接口大全/详细时序；细节通过证据入口指向代码或模块页。

## Ops（运行入口与证据链）

### 目标

把“能跑、能验、能回滚、能排障”的入口固定下来。Ops 页**只做入口与要点**，不重复长操作手册。

### 推荐落盘结构

```
.aisdlc/project/ops/
  index.md
  runbook.md
  monitoring.md
  rollback.md
```

### `ops/index.md` 最小模板

```markdown
# Ops Index（入口页）

## 运行入口
- 本地启动：../memory/structure.md#入口
- 环境变量/配置：<权威入口>

## 可观测入口
- Dashboard：
- Alerts：
- Logs：

## 回滚入口
- Rollback：

## Evidence Gaps（缺口清单）
- 缺口：
  - 期望补齐到的粒度：
  - 候选证据位置：
  - 影响：
```

## DoD（完成标准）与门禁

### 项目级 DoD（最小自检）

- [ ] Level-0 四份 Memory 具备“入口清晰/边界清晰/可导航”
- [ ] Level-1 索引骨架已生成（components/products），且索引只导航
- [ ] `components/index.md` 含跨模块依赖关系图（Mermaid，direct only）
- [ ] 每个 P0 模块页满足：存在模块页 + 固定标题齐全（含 `## Evidence` 与 `## Evidence Gaps`）+ frontmatter 元数据齐全 + 契约段落具备权威入口/不变量/证据入口
- [ ] Products 收敛到 <= 6；或已记录不可收敛原因与治理建议入口

### 状态一致性门禁（SSOT，必须遵守）

> **唯一事实来源**：模块是否允许在 `components/index.md` 打勾，只由该模块页是否达标决定。

- **P0 模块允许 `- [x]` 的前置条件**
  - 模块页存在且可导航：`.aisdlc/project/components/{module}.md`
  - 模块页包含固定标题：`## TL;DR`、`## API Contract`、`## Data Contract`、`## Evidence（证据入口）`、`## Evidence Gaps（缺口清单）`
  - 模块页 frontmatter 包含：`change_frequency`、`last_verified_at`、`source_files`
  - `## API Contract` 与 `## Data Contract` 都包含：
    - 权威入口（可定位）
    - 3–7 条不变量摘要
    - 证据入口（文件/类/job/命令级最小粒度）
  - 模块页正文不得散落“待补/未发现/待…后填写/以后再补”等占位句；缺口只能写入 `## Evidence Gaps（缺口清单）`
  - 若存在缺口，必须写入 `## Evidence Gaps（缺口清单）`，且**不得**打勾
- **P1 模块允许 `- [x]` 的降级条件**
  - 模块页存在；API 或 Data 允许缺失其一，但缺口必须结构化写入 `Evidence Gaps`
- **P2 模块**
  - 默认不打勾；只占位导航即可

## 增量 Discover（Delta Discover）与过期检测（stale）

### 何时触发 Delta Discover

- Merge-back 完成时（引入新 ADR/契约/能力）
- PR 涉及 P0/P1 模块的关键源文件变更时
- 模块被标记为 stale（过期）时

### Delta Discover 的最小执行范围（止损）

1. 识别受影响模块（根据变更文件列表与模块页 `source_files`）
2. 只更新这些模块的：
   - `.aisdlc/project/components/{module}.md`（TL;DR、契约段落、不变量、Evidence/Evidence Gaps）
   - `.aisdlc/project/components/index.md`（导航链接、依赖图、勾选状态）
3. 更新模块页元数据：
   - `last_verified_at`
   - `source_files`（如果边界变化）

### stale 的写法建议（不强制落盘形态）

- 模块页通过 `last_verified_at` 体现“新鲜度”
- 当模块 stale：
  - 不要用“忽略过期”继续写需求/设计
  - 先做 Delta Discover（最小范围）把关键不变量与证据入口更新到可用

## 红旗清单

- Products 写成几十个模块的功能清单（地图失效）
- Ops 写成长操作手册（应只做入口与要点）
- 打勾不看模块页内容（违反 SSOT 门禁）
- 模块 stale 仍继续把它当权威输入（应先 Delta Discover）

## 常见错误

- 用“待补/未发现”占位替代 Evidence Gaps（缺口会永远散落）
- 只做一次全量 Discover，不做增量维护（知识很快过期）

