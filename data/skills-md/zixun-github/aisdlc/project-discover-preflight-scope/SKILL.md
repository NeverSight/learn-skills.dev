---
name: project-discover-preflight-scope
description: Use when 你要开始存量项目 Discover，但你还不清楚“哪些入口可作为证据（run/test/ci/contract/ops）”以及“应该先做哪些模块（P0/P1/P2）”，并且担心范围失控导致不可维护。
---

# project-discover-preflight-scope（Step0+1：证据入口盘点 + 范围止损）

## 概览

Preflight 的目标不是“把信息都写出来”，而是先把 **可执行/可定位的证据入口** 盘清楚；Scope 的目标是先把 **覆盖面止损**（P0/P1/P2），避免逆向工程变成“写全但不可维护”。

**开始时宣布：**「我正在使用 project-discover-preflight-scope 技能执行 Discover 的 Preflight 与 Scope 止损。」  

## 输入 / 输出

- **输入**
  - 仓库根目录（代码、配置、依赖、CI/CD 配置）
  - 已有文档入口（README/Makefile/package.json/脚本等）
  - 可观测/运维入口（若存在：dashboard、告警、runbook、回滚）
- **输出（落盘）**
  - `.aisdlc/project/components/index.md`：模块清单 + P0/P1/P2 + code_entry + 复选框（此时不打勾）
  - `.aisdlc/project/memory/structure.md`：将“如何跑/如何验/如何发布”的入口以链接形式固定（下一步子技能会正式写）
  - **注意**：Preflight 的“证据入口清单”不需要单独建新文件，建议以“入口链接 + Evidence Gaps”逐步分散落位到 `memory/*`、模块页与 `ops/*`

## 核心原则（Preflight）

1. **优先可执行证据**
   - 优先级：脚本/CI job/契约文件/迁移/生成命令 > 描述性文档 > 口述经验
2. **只记录“入口”，不写推断**
   - 你要写的是“从哪里进入、如何定位、证据在哪个文件/哪个 job”，不是“它应该怎么工作”
3. **缺证据 = 结构化缺口**
   - 写进后续文档的 `## Evidence Gaps`：缺口/期望粒度/候选位置/影响

## Preflight 最小清单（找证据入口）

> 只要能定位到具体文件或 job 名，就算有效入口；不要为了“写完整说明”而脑补。

- **运行入口**
  - 本地启动脚本/命令入口（例如：`package.json scripts`、`Makefile`、`*.ps1/*.sh`、docker-compose、k8s manifest）
  - 环境变量入口（例如：`.env.example`、配置模板、helm values）
- **测试入口**
  - 单测/集成测/E2E 的命令入口与目录入口
  - 覆盖率/门禁入口（例如：CI job、测试阈值配置）
- **CI/CD 入口**
  - workflow/pipeline 文件位置 + 关键 job 名
  - 是否有 docs/link-check 等门禁（如果没有，后续可作为建议）
- **契约/结构化事实入口**
  - OpenAPI/Proto/GraphQL schema
  - DB migrations/DDL/ORM models
- **可观测/运维入口（如有）**
  - dashboard、告警、日志查询入口、runbook、回滚入口

## Scope（P0/P1/P2）规则

### 分级建议（与 Discover DoD 对齐）

- **P0（必须）**：高频变更、跨团队交界、对外集成多、事故/故障热点、合规风险高
- **P1（建议）**：稳定但经常被引用/被问到/被依赖的基础能力
- **P2（按需）**：低风险、低协作、生命周期短；先做索引占位，必要时再升级

### 逆向深度止损（强约束）

- **P0**：必须最终具备模块页 `.aisdlc/project/components/{module}.md`，且页内同时包含 `## API Contract` + `## Data Contract` + `## Evidence`（缺口只能写到 `Evidence Gaps`，且此模块不得打勾）
- **P1**：必须最终具备模块页；允许 API 或 Data 其中一段降级为 Evidence Gaps（记录缺口与影响）
- **P2**：只在索引占位导航（默认不创建模块页）

## `components/index.md`（Scope 落盘）最小模板

> **索引只导航**：此表格不写不变量、不写字段，不写“待补/未发现”。缺口统一留给模块页的 `Evidence Gaps`。

```markdown
# Components Index（地图层：只导航）

| module | priority | owner | code_entry | api_contract | data_contract | ops_entry | status |
|--------|----------|-------|------------|--------------|---------------|-----------|--------|
| auth | P0 | team-x | `src/auth/` | [api](./auth.md#api-contract) | [data](./auth.md#data-contract) | [ops](../ops/index.md) | - [ ] |
| order | P1 | team-y | `src/order/` | [api](./order.md#api-contract) | [data](./order.md#data-contract) |  | - [ ] |
| legacy-tooling | P2 |  | `tools/legacy/` |  |  |  | - [ ] |
```

## 并行化建议

当入口盘点任务互不依赖时，建议并行：

- Agent A：运行入口 + 环境变量入口
- Agent B：测试入口 + 质量门禁入口
- Agent C：CI/CD 入口
- Agent D：契约/Schema/DDL 入口 + Ops 入口

## 红旗清单

- Scope 还没做，就开始为一堆模块写细节（范围必失控）
- 用“我猜应该是……”来填运行/测试/契约（必须写 Evidence Gaps）
- 在索引里写“主要类/核心表/错误码/字段列表”（索引只导航）

## 常见错误

- 把 Preflight 变成“写 README 教程”（应只固定入口与证据链）
- 试图一次覆盖全部模块（应先 P0 三件套）

