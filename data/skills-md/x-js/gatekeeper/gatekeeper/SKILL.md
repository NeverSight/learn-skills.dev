---
name: gatekeeper
description: Gatekeeper 流水线【单一规则源 + 总控路由】。仅人工以 `/gatekeeper` 命令触发（禁止 Agent 自动使用）。先定位当前流程走到哪一步，再分派到对应子 skill 继续；若尚无流程则先发起 `/gatekeeper-init`。
version: "0.0.1"
author: X-JS
license: MIT
when-to-use: manual
metadata:
  tags: ["gatekeeper","router","manual-trigger"]
---

# Gatekeeper 总控路由与全局行为规则

> 本文件是迭代流水线的**单一规则源 + 总控路由**；所有子 skill 的职责见第八节，整体规则以下各节为准。
> 版本编号 = 当前 Git 分支名（只读 `git branch --show-current` 获取；失败/空 → 提示人工切换分支，禁止用空串/猜测值）。
> **路径约定（全局生效）**：`项目根/...` 一律指 Git 仓库根目录（`AGENTS.md` 所在目录，如 `项目根/.gatekeeper/`）；`gatekeeper` skill 的 `assets/` 指该 skill 自身资源目录，两者不可混淆。

## When to Use
1. **仅人工**以 `/gatekeeper` 命令触发（`agents/openai.yaml` 设 `allow_implicit_invocation: false`，禁止 Agent 隐式调用）；
2. 用于推进迭代、不确定当前进度、或从中断处继续。

## 一、固定迭代流水线（强制卡点 + 全留痕）

`人工需求确认` → `Agent概要设计`（小改动可跳过）→ `人工评审留痕+放行` → `Agent编码+单元测试` → `Agent dev环境测试（review.md 第三部分留痕）` → `人工代码评审留痕+放行` → `人工提交合并+部署staging` → `人工 staging测试验证（test.md留痕）` → `人工辅助部署prod收尾`。

- 需求确认判据：`requirement.md` 无 HTML 占位符，且「需求确认人/日期」已填。
- 聊天提及修改：需求/概要设计阶段 → 禁止直接改代码，要求人工补齐 requirement.md；编码阶段小改动（不涉及已评审接口/数据结构/设计）→ 可直接改码并走代码评审。
- 小改动迭代：progress.md 阶段2 可标「跳过」，跳过概要设计与设计评审，直接进入 T03。
- T07 问题归属：需求已有 → 回流阶段3/4 修复；需求未覆盖 → 人工补需求后重新开发，无需全流程重走。
- 历史归档：`项目根/.gatekeeper/history/` 保存已完结迭代，迭代中完全忽略。T08 完成或 `/gatekeeper-abort` 中止后，整体迁移至 `项目根/.gatekeeper/history/${版本编号}/`。

## 二、评审与测试留痕强制执行规则（核心）

1. 评审唯一依据 `review.md`；staging 测试唯一依据 `test.md`；dev 测试记录在 `review.md` 第三部分。忽略聊天临时评语。
2. 评审两轮（概要设计、代码）+ 测试一轮（staging）；均支持多轮整改复核，轮次记入同一表「轮次」列，不复制表头。
3. 工作逻辑：只读【状态=待整改】行针对性整改、不新增功能；整改后主动提示人工复核，不私自判定完成；必须人工标【复核通过】才结束本轮；误报置「无需整改」附理由，由人工裁决，不得硬改或私自清空。
4. 禁止无依据整改、超范围整改、私自清空问题记录。
5. 修复后输出修复清单，告知人工复核。
6. 问题全部【复核通过】+ 人工更新 progress.md 阶段 + 下发推进指令，方可进入下一阶段；AI 不主动轮询、不自行推进。
7. **代码评审最小要素（闸门2 强制）**：放行前①按 design.md「变更点清单」逐条核对 diff 范围，识别超范围改动；②对外接口契约变更须同步 `crmeb/apidoc/` 并在整改结果声明；③测试覆盖说明。空表/零问题不得直接通过；「零问题」须人工在放行备注写明核对范围与抽样项，人工至少抽样核对 1-2 个变更点。
8. **dev 测试与验收标准映射（T04 强制）**：review.md 第三部分每条测试项须填「对应验收§」（对应 requirement.md 七、验收标准）；存在未映射验收标准即视为 dev 测试不完整。
9. **staging 归属判定（test.md 强制）**：判「需求已有 / 需求未覆盖」前必须先 read requirement.md 原文引用条目；归属列仅允许该两枚举值，非法值主动提示人工修正；修复致接口契约变化须声明 apidoc 已同步。
10. **跨迭代回归（强制）**：design.md 变更点清单须声明「关联历史迭代回归项」；触及上期功能时 dev 测试必须回测并在 review.md ③ 留痕，否则 dev 测试不完整。

## 三、留痕与流程文件读写权限清单

> 本表仅约束 `.gatekeeper/` 留痕与全局流程文件；源码及 `crmeb/sql/`、`crmeb/apidoc/` 等属编码/测试阶段正常读写范围，不受本表限制。
> 表内未列出的 `.gatekeeper/` 文件一律只读：

| 文件 | 可读 | Agent 写入 | 说明 |
|------|:----:|:----------:|------|
| `项目根/.gatekeeper/${版本编号}/requirement.md` | ✅ | ❌ 禁止 | 人工编写，Agent 不得修改 |
| `项目根/.gatekeeper/${版本编号}/progress.md`（闸门+进度） | ✅ | ❌ 禁止 | 阶段总闸门，仅人工可改 |
| `项目根/.gatekeeper/${版本编号}/design.md` | ✅ | ✅ | Agent 概要设计输出 |
| `项目根/.gatekeeper/${版本编号}/review.md` | ✅ | ✅ 仅【状态】+【整改结果】两列 | 状态仅允许 待整改→已整改待复核 / 无需整改 |
| `项目根/.gatekeeper/${版本编号}/test.md` | ✅ | ✅ 仅【状态】+【整改结果】两列 | 同上 |
| `项目根/.gatekeeper/history/` | ✅ | ❌ 禁止 | 已完结归档，迭代中完全忽略 |
| `AGENTS.md`、`opencode.json`、`项目根/.gatekeeper/*.md`（全局规则） | ✅ | ❌ 禁止 | 全局配置，仅人工可改 |

## 四、模板与文件生成规则

模板统一存放于本 skill（`gatekeeper`）的 `assets/`；实例化 = 复制到 `项目根/.gatekeeper/${版本编号}/` + 替换 `${版本编号}` + 删除「使用说明」冗余文字：

| 模板 | 实例化目标 | 生成者 | 生成时机 |
|------|------------|--------|----------|
| `_template-requirement.md` | requirement.md | 人工 | 初始化（`gatekeeper-init`） |
| `_template-progress.md` | progress.md | 人工 | 初始化（`gatekeeper-init`） |
| `_template-design.md` | design.md | Agent | 阶段2（`gatekeeper-next`） |
| `_template-review.md` | review.md | Agent | 阶段2（`gatekeeper-next`） |
| `_template-test.md` | test.md | Agent | 阶段7（`gatekeeper-next`） |

## 五、单轮对话范围约束

1. 一轮对话只完成 1-2 个任务，禁止一次性完结全迭代。
2. 禁止跨阶段工作：未过概要设计评审（或未标跳过）前不得编码。
3. 进度、阶段、评审结果全部落盘，不依赖 AI 对话记忆。
4. Agent 回填整改结果后提示人工提交留痕文件；Git 提交由人工执行。

## 六、阶段流转识别

1. 设计评审：停止编码，待人工下发整改指令后读 review.md 问题清单。
2. 有人工录入【待整改】：逐条修复回填，状态置「已整改待复核」；误报置「无需整改」附理由。
3. 人工复核：通过标「复核通过」，驳回则问题进入下一轮。
4. 全部复核通过 + 人工更新 progress.md + 下发推进指令，方可进入下一环节。
5. 代码评审与设计评审逻辑一致。
6. staging 测试：人工录 test.md 问题 → Agent 判归属 → 修复回填 → 人工复验复核。
7. **进度定位**：progress.md 不维护「当前阶段」指针，依据各阶段【状态】定位首个未完成阶段行；归档前校验状态与留痕结论一致。

## 七、Token 消耗优化约束（强制）

1. **输出规范（P0）**：回复只输出 变更摘要+增量，禁止全表回显留痕文件；只展示与本次动作相关的行。
2. **模板头部精简（P0）**：留痕文件头部说明 1-2 行；实例化时删除「使用说明」冗余。
3. **增量读取（P1）**：按【状态=待整改】/最新轮次定位范围，只读待整改行与最新轮次；同轮已读不重复读。
4. **codegraph 收敛（P2）**：精确符号名 + maxFiles 限制；链路查询优先 trace/callers。
5. **单一规则源（P0）**：全局规则统一在本文件，避免重复注入。

## 八、指令与子 skill 一览

| 子 skill | 命令 | 职责 |
|----------|------|------|
| `gatekeeper-init` | `/gatekeeper-init` | 创建 `项目根/.gatekeeper/${版本编号}/`，实例化 requirement.md / progress.md 并校验占位符 |
| `gatekeeper-fix` | `/gatekeeper-fix` | 读取 review/test【待整改】问题，staging 先判归属，针对性修复回填，等人工复核 |
| `gatekeeper-next` | `/gatekeeper-next` | 确认复核通过后，执行当前阶段任务并实例化所需模板 |
| `gatekeeper-abort` | `/gatekeeper-abort` | 中止：核对留痕后标记并迁移至 history |
| `gatekeeper-finish` | `/gatekeeper-finish` | 归档校验四项齐备后迁移至 history |

## 九、总控路由分派（本 skill 核心动作）

### 1. 判断是否有流程
- `项目根/.gatekeeper/${版本编号}/` 不存在 → 尚无流程，发起 `/gatekeeper-init`，停止等人工填 requirement.md。
- 存在 → 继续。

### 2. 定位当前阶段
- 只读 `progress.md`，定位首个未完成阶段行（见六.7）；只读 `review.md` / `test.md` 检查【待整改】行。
- 存在 `.init-incomplete` 标记 → 回流 `gatekeeper-init`（补齐缺失文件）。

### 3. 分派子 skill（留痕状态优先，命中即停）
| 优先级 | 情形 | 分派 |
|:---:|------|------|
| 1 | review/test 存在【待整改】 | `/gatekeeper-fix` |
| 2 | 阶段1 需求确认未完成 | 无子 skill：提示人工填 requirement.md |
| 3 | 阶段2 概要设计未完成 | `/gatekeeper-next`（产出 design.md；小改动可标跳过） |
| 4 | 阶段3 编码+单测未完成 | `/gatekeeper-next` |
| 5 | 阶段4 dev 测试未完成 | `/gatekeeper-next` |
| 6 | 阶段5 代码评审未完成 | `/gatekeeper-next`（review.md 已在阶段2实例化）；待整改回流 fix |
| 7 | 阶段6 提交合并+部署 staging | 无子 skill：人工执行 git（Agent 不执行） |
| 8 | 阶段7 staging 测试未完成 | `/gatekeeper-next`（实例化 test.md）；待整改回流 fix |
| 9 | 阶段8 收尾且归档条件满足 | `/gatekeeper-finish` |
| 10 | 全部完成 | 提示人工可归档或开新迭代 |

### 4. 输出
- 只输出：版本编号、当前阶段、分派子 skill 及原因（一行）、后续人工动作；禁止全表回显留痕文件（见七.1）。

## Pitfalls
1. 本 skill 禁止 Agent 自动使用；检测到无流程目录只能发起 `/gatekeeper-init`，不得替人工推进需求。
2. 只做分派，不代行子 skill 动作。
3. requirement.md / progress.md 由人工维护，Agent 只读不写（见第三节）。
4. 版本编号目录已存在且无 `.init-incomplete` 时，不回流 init（避免覆盖人工内容）。
5. 一轮 `/gatekeeper` 只推进当前阶段（见第五节.1）。