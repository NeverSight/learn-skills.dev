---
name: project-discover-modules-contracts
description: Use when 你需要把选中的模块（优先 P0）做成 `.aisdlc/project/components/{module}.md` 的单页模块 SSOT，并在同一页内建立 API/Data 契约的权威入口、不变量摘要、证据入口与结构化缺口（Evidence Gaps），以满足 Discover 的 DoD 门禁。
---

# project-discover-modules-contracts（Step4：模块单页 SSOT + 契约段落 + 证据链）

## 概览

模块页是 Discover 的“权威入口”。它的目标不是写全细节，而是让 AI/人能在需要时 **快速判断边界与不变量，并且能沿着证据链定位到代码/契约/测试/CI/ops**。

**开始时宣布：**「我正在使用 project-discover-modules-contracts 技能为模块建立单页 SSOT（含契约段落与证据链）。」  

## 硬规则（P0 必须满足）

1. **模块页路径固定**
   - `.aisdlc/project/components/{module}.md`
2. **锚点标题必须存在（稳定跳转）**
   - `## TL;DR`
   - `## API Contract`
   - `## Data Contract`
   - `## Evidence（证据入口）`
   - `## Evidence Gaps（缺口清单）`
3. **契约不单独建目录**
   - 禁止 `.aisdlc/project/contracts/**`
4. **缺口必须结构化**
   - 所有缺口只写到 `## Evidence Gaps（缺口清单）`（不允许散落“待补/未发现/TODO”）
5. **禁止“占位句”冒充内容**
   - 在 `API Contract` / `Data Contract` / `Evidence` 等正文里，禁止写“待补齐后填写/待确认/未发现/以后再补”等占位句。
   - 如果缺证据或缺结论：只允许写入 `## Evidence Gaps（缺口清单）`，并保持正文段落简短、可追溯。

## 模块页 Frontmatter（必填）

```yaml
---
module: <module-short-name>
priority: P0|P1|P2
change_frequency: high|medium|low
last_verified_at: <YYYY-MM-DD>
source_files:
  - <path/to/key/file1>
  - <path/to/key/file2>
---
```

> **提示**：`change_frequency` 可用 git log 的经验判断或简单统计；`source_files` 只选“最能代表模块边界/契约/状态机”的关键源文件。

## 模块页推荐结构（最小可用）

```markdown
# <模块中文名>（<module>）

## TL;DR
<3–5 句话：做什么、边界、关键不变量、最关键的证据入口>

## 模块定位
- In：
- Out：

## Owner
- 团队/负责人/值班入口：

## 入口
- 代码入口：
- 运行入口（如有）：../ops/...

## 协作场景（1–2 个）
- 谁调用谁 + 关键边界（细节时序下沉到 spec）

## State Machines & Domain Events
- 状态机摘要：
- 领域事件摘要：

## API Contract
- 权威入口（必须可定位）：
- 不变量摘要（3–7 条）：
- 证据入口（最小粒度）：

## Data Contract
- 数据主责（Ownership）：
- 核心对象与主键：
- 权威入口（必须可定位）：
- 不变量摘要（3–7 条）：
- 证据入口（最小粒度）：

## Evidence（证据入口）
- Code：
- Tests：
- CI：
- Ops：

## Evidence Gaps（缺口清单）
- 缺口：
  - 期望补齐到的粒度：
  - 候选证据位置：
  - 影响：
```

## 契约段落写法（避免“字段大全”）

### `## API Contract` 最小要求（P0）

- **权威入口（必须可点击/可定位）**
  - OpenAPI/Proto/Schema 的源文件路径或生成物路径
  - 若有生成/校验命令或 CI job，写入口（不写长说明）
- **不变量摘要（3–7 条）**
  - 例如：鉴权方式、幂等语义、版本策略、错误码族、审计要求、超时/重试策略
- **证据入口（最小粒度）**
  - 至少 N 个关键 handler/router/controller 文件路径
  - 至少 1 个代表性测试入口（没有就进入 Evidence Gaps）
  - 至少 1 个 CI job/命令入口（能证明“有没有跑测试/有没有做契约校验”）

### `## Data Contract` 最小要求（P0）

- **数据主责（Ownership）**
  - 主写/只读/同步来源（边界明确）
- **核心对象与主键**
  - 对象名 + 主键/唯一标识 + 生命周期一句话
- **权威入口（必须可定位）**
  - migrations/DDL/Schema/ORM model 的证据入口
- **不变量摘要（3–7 条）**
  - 例如：唯一性约束、状态口径、关键枚举、不可变字段、对账口径入口
- **证据入口（最小粒度）**
  - 关键 repository/mapper/service 路径
  - 测试/CI 证据入口（无则进 Evidence Gaps）

## Evidence Gaps（缺口清单）模板（强制结构化）

> 任何“找不到/不确定/待补”都必须按这个结构写，避免缺口散落导致永远补不齐。
>
> **特别提醒：** 如果你暂时无法给出“3–7 条不变量摘要”，不要在正文里写“待补齐后填写”。
> 正确做法：在 Evidence Gaps 里新增缺口条目（例如“缺口：未提取 API 不变量摘要”），并写清候选证据位置与影响。
> 该模块此时不得在索引中打勾。

```markdown
## Evidence Gaps（缺口清单）

- 缺口：未发现 OpenAPI/Proto 权威入口（无法确认接口字段与错误码族）
  - 期望补齐到的粒度：定位到具体 schema 文件路径或生成 job 名
  - 候选证据位置：`docs/`、`api/`、`openapi/`、CI workflow 中的 build-docs job
  - 影响：需求设计与实现阶段会猜接口契约，容易破坏兼容性与回归成本高
```

## P1/P2 的降级规则（避免范围失控）

- **P1**：模块页必须存在；API 或 Data 允许缺失其一，但必须在 Evidence Gaps 写清缺口与影响
- **P2**：默认不创建模块页，只在索引占位；需要时再升级到 P1/P0

## 红旗清单

- 契约段落写成字段大全（应改为：权威入口 + 不变量摘要 + 证据入口）
- “缺口”用 TODO/待补散落在正文（必须集中到 Evidence Gaps）
- 在正文里写“待补齐后填写/未发现/以后再补”这种占位句（必须改为 Evidence Gaps）
- 在索引里重复模块页内容（索引只导航）

## 常见错误

- 把“证据入口”写成“你应该怎么做”（要写在哪里、而不是怎么操作）
- 把一次性交付细节写进项目级模块页（应下沉 spec 或外部 runbook）

