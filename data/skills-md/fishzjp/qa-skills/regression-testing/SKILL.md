---
name: regression-testing
slug: regression-testing
displayName: 回归测试
version: 0.8.1
description: "After a code change (diff/fix/requirement change), decide what to regression-test: changed files → functions → features → cases traceability; outputs a ranked list. Not for: editing case files (test-case-writing), long-term strategy (test-strategy). 代码变更后判断回归哪些测试：沿改动分析链产出分级回归清单。不用于：用例增量修改、长期策略。"
---

# 回归测试（regression-testing）

代码变更 → 自动判断应该回归哪些测试。

- **输入**：Code Diff（`git diff <base>...<head>`）、Bug 修复说明、需求变更说明、已有用例（markmap + `测试用例.schema.yaml`）、（可选）需求模型
- **输出（落盘）**：`{项目}/回归清单_{日期}.md`——必须回归（P0）/ 建议回归（P1）/ 可选回归（P2）三级，逐条给依据。**档名沿用 P 系记号，但归档规则是影响直接程度，与用例自身优先级是两套口径**：直连改动 → 必须回归，同模块间接受影响 → 建议回归；一条 [P2] 用例因 code_refs 直连改动同样进「必须回归」档（流水线分层消费按本档位执行，见 `../core/pipeline-integration.md`）
- **前置依赖**：持久的"用例 ↔ 代码 ↔ 功能"追溯映射，v0 三层全部来自落盘产物，不依赖会话记忆：
  1. **代码级锚点**：用例附录「代码证据清单（TC ↔ 文件:行）」，由 Schema 的 `code_refs` 结构化
  2. **功能层**：需求模型 + Schema 的 `module` / `risk_ref`
  3. **per-run 增量**：改动文件映射附录（针对本次 diff 生成）

> 没有这个数据结构，影响面分析就只是"让模型读一遍 diff 猜"。**启动前三档资产盘点**（决定走哪条路，防止零资产硬编清单）：
> - **全套齐**（markmap + Schema 追溯映射都在）：走工作流完整分析链
> - **只有 markmap 无 Schema**：先由 `test-case-writing` 对存量 markmap 抽取补建（不需要人工重写），再进工作流
> - **零用例资产**：不凭 diff 编造清单——向用户给降级选项：P0 冒烟建议（逐条标「无追溯依据，覆盖不保真」），或先由 `test-case-writing` 补建最小用例集再回来跑本流程
>
> **知识库输入（另查，不改变上述分流）**：项目存在 `.qa/` 知识库时，启动先读其 `INDEX.md`——`flaky-tests.md` 的 active 条目直接作为「历史噪声 vs 真实回归」判定与回归分级的输入（写入与治理由 `qa-memory` 承担）。

## When to Use

- 代码变更（feature/Bug 修复/重构）合入后，需要选择回归范围
- Bug 修复后需要确定"修复验证 + 关联回归"的用例集
- 需要一份逐条给依据、可裁剪的分级回归清单

## When NOT to Use

- 用例文件的增量修改本身（标记/新增/废弃用例）→ `test-case-writing` 增量更新流程
- 长期回归策略（锚点用例、回归节奏）→ `test-strategy` 的 regression_plan
- 单条失败的分辨与定性 → 执行类 skill 单条流程（`automated-e2e-testing` 工作流二 / `api-testing` §4）；一轮失败 ≥3 条先走 `../core/triage.md` 分流；Bug 经用户定性裁决后才进 `bug-analysis`（其输入必须是已确认 Bug）
- 端到端流水线 → `qa` 编排

## 分析链

```text
Changed Files（git diff）
    ↓
Changed Functions（diff 中被修改的函数/类/组件）
    ↓
Affected Features（函数 → 所属功能：经 Schema code_refs / module / 需求模型映射）
    ↓
Affected Test Cases（功能 → 用例：risk_ref / module / 附录改动文件映射）
    ↓
Regression Scope（三级回归清单 + 依据）
```

## 工作流

### 1. 盘点变更

```bash
git diff <base>...<head> --stat          # 改动文件清单
git diff <base>...<head> -U3             # 逐文件读改动内容，定位改动函数
```

变更类型分类（基础四类，与 `test-case-writing` 阶段一「改动盘点」的枚举一致）：🆕 新建 / ✏️ 修改（可按需细分标注：行为修改、🐛 Bug 修复（关联 Bug 单）、🔧 重构（行为应不变））/ 🗑️ 删除 / 💀 死代码。类型不同，回归侧重不同（重构 → 全量行为锚点；Bug 修复 → 修复验证 + 该 Bug 历史关联用例；死代码 → 不产生回归用例）。

### 2. 影响面分析（沿分析链逐层映射）

- **代码层**：Schema 中 `code_refs` 命中改动文件（或同文件邻近行）的用例 → 直接受影响。`code_refs` 是**用例编写时的快照而非实时索引**——命中处与本次 diff 内容明显对不上（函数已消失 / 行号整体偏移出邻近带 / 文件已改名）即判锚点陈旧，**整批降级为参考信号**改走功能层 / 风险层映射，并在清单头部注明口径
- **功能层**：改动函数所属功能（module / 需求模型）下的全部用例 → 间接受影响；共享工具/公共组件改动 → **消费方全查**（grep 引用方，逐个判断）
- **风险层**：Risk Map 中挂在受影响功能上的风险（`risk_ref` 反查）→ 其锚点用例（Critical 风险必进"必须回归"）
- **历史层**（有 Bug 单时）：该 Bug 涉及功能的历史回归用例

> 分析过程对每个映射给依据（"TC-03-02 code_refs 命中 `coupon_service.py:124`"），**映射不上的不硬编**——列入"影响不明，建议人工判断"。

### 3. 生成分级回归清单

有关联 Bug 时，**修复验证用例并入「必须回归」档**：取 bug-analysis「回归建议」给出的修复验证用例（无既有用例则给新增 TC 编号建议，落文件归 `test-case-writing`），并与该 Bug 条目「回归建议」双向互链。

```markdown
# 回归清单 — {日期}

- 变更基线：{base}...{head}（{commit 数} commits，{文件数} 文件）
- 变更类型：{新增/修改/修复/重构/删除}
- 关联 Bug：{Bug 编号列表，非修复类变更省略此行；有则与对应 Bug 条目的回归建议双向互链}

## 必须回归（P0）
| 用例 | 依据 |
|------|------|
| TC-01-01（SMOKE-1） | 改动文件 code_refs 直连 + Critical 风险 R1 锚点 |
| TC-03-01（修复验证） | Bug-001 修复验证，来源 bug-analysis「回归建议」（新增编号归 test-case-writing） |

## 建议回归（P1）
| 用例 | 依据 |
|------|------|
| TC-02-03 | 同功能模块间接受影响（module=发放流程） |

## 可选回归（P2）
| 用例 | 依据 |
|------|------|
| TC-06-02 | 公共组件改动，消费关系间接 |

## 影响不明（建议人工判断）
- {文件/功能}：{为什么映射不上}

## 无影响确认（显式排除）
- {模块}：{排除依据，如"改动仅涉日志文案，无行为变更"}
```

> 与 `test-strategy` 的 regression_plan 对齐：锚点用例（Critical 风险 P0）默认进"必须回归"；执行方式按 automation_plan（e2e / api / 手动）标注。

### 4. 交付与执行衔接

- 清单落盘后交执行：自动化部分 → `automated-e2e-testing` / `api-testing`；手动部分 → 测试工程师
- **流水线分层消费**：本清单的三级分级同时是流水线触发分层的依据——PR 冒烟跑 P0、夜间任务跑 P1 全量 + P2 抽样、发布卡点全量；headless 非交互运行时检查点降级/产物落盘/退出码语义见 `../core/pipeline-integration.md`（此时加载），回流后的批量失败进 `../core/triage.md`
- 回归结果汇总进测试报告（`../core/report-template.md` §5 回归摘要）
- **多失败先分流**：一轮回归失败 ≥3 条时，先按 `../core/triage.md` 四分类预归类——C 环境 / D 不稳定剔出本轮 Bug 同步口径（C 修复后受影响批次强制原样重跑），B 资产问题单列待办，剩余 A 类才进入下行状态同步
- **回归结果同步 Bug 状态**：修复验证对应的 Bug 条目按结果更新——通过 → 已验证关闭；失败 → 已修复待验证（附失败证据；条目已处于该状态则**复验轮次 +1**，达 3 向用户提示升级裁决——换修复方向 / 转不予修复评审），字段口径见 `../core/report-template.md` §3（使用约定 6）

## Common Mistakes

| 错误 | 后果 | 正确做法 |
|------|------|---------|
| 只按改动文件名匹配用例 | 同名不同层、公共组件消费方漏检 | 沿分析链走到底，公共组件 grep 引用方 |
| 无 Schema 时靠"读 diff 猜" | 影响面分析退化为猜 | 先对存量 markmap 抽取 Schema（`test-case-writing`） |
| 清单不给依据 | 不可复核，无法裁剪 | 每条用例给映射依据 |
| 全量回归一刀切 | 回归成本爆炸、关键用例被稀释 | 三级分级 + 显式排除清单 |
| 映射不上的硬编进清单 | 虚假置信 | "影响不明"单独列出，人工判断 |
| 用例文件修改与回归范围混为一谈 | 职责越界 | 用例修改归 `test-case-writing`，本 skill 只选回归范围 |
| 零用例资产仍照常产出三级清单 | 凭 diff 编造用例名，清单表面专业实则不可执行 | 先做三档资产盘点；零资产走冒烟建议降级路径并标「无追溯依据」 |
| 锚点陈旧的 code_refs 仍当直连依据 | 重构后影响面错漏（漏掉真受影响的、误报已消亡的） | 命中处与 diff 对不上即整批降级，改走功能层/风险层映射 |
