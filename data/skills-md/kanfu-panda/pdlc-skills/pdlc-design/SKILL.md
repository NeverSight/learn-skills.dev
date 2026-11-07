---
name: pdlc-design
description: 创建技术设计文档（自动生成 + 自检 + handoff）
argument-hint: "<功能ID | 功能描述> [--autonomous]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 2
stage: design
produces:
  - docs/02_design/<subsystem>/<feature-id>-design.md
requires:
  - docs/01_requirements/prd/
next_step: pdlc-tdd
terminal_state: design_done
---

# 创建设计文档

<!-- @include templates/prompts/iron-law.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁**

以下规则为**不可协商**的执行约束：

1. **文件必须落盘**：所有带编号（功能ID / 缺陷ID）的文档，必须作为实际文件写入磁盘，不可仅在对话中输出。
2. **阶段必须落章**：每个阶段完成后必须在状态机 `docs/.pdlc-state/<feature-id>.json` 追加 history，不可跳过。
3. **测试必须存在**：进入 `/pdlc-implement` 前，对应测试必须存在且处于红灯状态。违反则中止。
4. **自检必须执行**：段二自检为强制步骤，不得以"已经很好了"为由跳过。
5. **防循环**：段三修复为单次，不递归。无法自动修复的问题记录到报告，继续往下走。
6. **状态必推进**：成功执行某 phase 后 `current_stage` 必须变更。收尾时若发现 `current_stage` 未推进，视为失败并报错，**不得静默返回**（防止外层循环拿滞后的状态空转烧额度）。唯一例外：命中人工点主动 block 时，`current_stage` 保持不变但必须写 `last_phase_result.ok=false` + `blocked_reason`。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law.md -->

根据已有的需求文档，在 `docs/02_design/` 对应子目录下创建技术设计文档。

## 输入解析

从本命令的参数中判断输入类型：
- **文件路径**（以 `/`、`./` 开头，或以 `.md`、`.txt`、`.pdf` 结尾，或实际存在的文件）：直接读取该文件作为需求来源，跳过 PRD 搜索
- **功能ID**（`F<日期>-<时分秒>`，`/pdlc-prd` 交接时给的就是它）或**功能名关键词**：按下方守卫找 PRD

<!-- @include templates/prompts/artifact-lookup.md（已内联于下方，无需另读） -->
## 定位上游产物：先查状态机，再按关键词搜

守卫要找的上游文档（PRD、设计文档、评审记录等），按下面的顺序定位，**命中即停**：

1. **输入是功能ID / 缺陷ID**（`F…` / `B…`）且 `docs/.pdlc-state/<ID>.json` 存在 → 读它 `history[].produced` 里记下的路径，取所需类型的文档。这是上游阶段亲手记的，最可靠
2. **没有状态机、或 `produced` 里没有所需文档** → 在对应目录下搜：文件名含该 ID 或功能名关键词，或文件顶部 PDLC 追溯头的 `功能ID` 等于该 ID
3. **命中多份** → 不要随手挑一份：交互模式下列出来请人选；`--autonomous` 下优先取文件名含该 ID 的，仍不止一份则按「真需人判断」阻塞（写 `blocked_reason`，列出候选）

找到后从文件名或追溯头取功能ID，后续产出一律沿用它，**不另分配新 ID**。
<!-- @include-end templates/prompts/artifact-lookup.md -->

## PDLC 前置检查（必须执行，不可跳过）

1. 若输入为文件路径，直接读取文件内容作为需求，提取功能名和功能ID（如有），跳到步骤 4
2. 按上面的顺序在 `docs/01_requirements/prd/` 下找本功能的 PRD
3. **未找到** → 输出以下信息后**立即停止，不继续执行**：
   ```
   ⛔ PDLC 守卫：未找到与「<功能名>」相关的 PRD 文档。
   设计文档必须基于已有的 PRD。请先运行：
   👉 /pdlc-prd <需求描述>
   ```
4. **找到** → 提取功能ID（如 `F20260326-090000`），读取该 PRD 内容，继续执行

<!-- @include templates/prompts/design-options.md（已内联于下方，无需另读） -->
## 方案比较（写设计文档之前）

先判断这次设计有没有**值得比较的技术取舍**——存储怎么选、同步还是异步、新建服务还是扩展现有模块、接口怎么切、数据模型拆不拆等。

- **没有**（沿用项目里已有的做法、PRD 也没留可争的点）→ 不比较，在设计文档开头写一句「沿用 <既有做法>，没有值得比较的取舍」，直接写设计。**不要为了凑数编出几个明显不会选的方案**
- **有** → 列 2～3 个候选，用一张表比较，然后给出推荐：

  | 方案 | 做法（一句话） | 改动面 | 主要风险 | 对 PRD 验收标准 / 非功能需求 | 与现有代码和规范的契合 |
  |---|---|---|---|---|---|

  推荐写明理由，理由要落到 PRD 条目或项目规范上，不写「更优雅」「更灵活」这类说不出依据的话。

**谁来选**：

- **交互模式**：把表和推荐给人看，问一次选哪个（只问这一轮），人选定后再写设计
- **问不了人**（参数带 `--autonomous`，或在 `/pdlc-feature` 里——开工后不再提问，阶段二还可能跑在子代理里）→ 选推荐的方案，推进状态时传
  `--decision "设计方案=<方案名>（<一句理由>）"`；候选之间的差别取决于 PRD 没交代的业务取舍（比如成本和一致性二选一）时，也照推荐选，
  但把这个假设写进设计文档的「方案比较」节，让人在评审时看得到

**落盘**：设计文档开头加「方案比较」一节——比较表、选定的方案、怎么选的（人选 / 按推荐自动选）；没比较的就是上面那一句。
后面的接口、表结构、架构都按选定的方案写，不要在正文里又混进落选方案的做法。
<!-- @include-end templates/prompts/design-options.md -->

## 输出位置

- API 设计 → `docs/02_design/api/`
- 架构设计 → `docs/02_design/architecture/`
- 数据库设计 → `docs/02_design/database/`

## 要求

1. 先阅读找到的 PRD 文档，全面理解需求
2. 参考 本 skill 目录下的 `assets/api-design-template.md` 获取 API 设计模板格式
3. 参考 `docs/00_standards/` 目录了解项目规范（未命中 → 提示 `consider /pdlc-standard add <category>/<topic>`）
4. **文件名格式**: `<功能ID>-<功能名>-<类型>.md`（如 `F20260326-090000-user-auth-api.md`），类型可以是 api / arch / db
   - 若 PRD 为旧格式无功能ID，则使用旧格式 `YYYYMMDD-<功能名>-<类型>.md`
5. **文档顶部必须包含 PDLC 追溯头**：
   ```
   <!-- PDLC-TRACE -->
   <!-- 功能ID: F20260326-090000 -->
   <!-- 功能名称: user-auth -->
   <!-- 阶段: 设计 -->
   <!-- 前置文档: docs/01_requirements/prd/F20260326-090000-user-auth-prd.md -->
   ```
<!-- @include templates/prompts/output-language.md（已内联于下方，无需另读） -->
🌐 **Output language for generated artifacts**

All generated artifacts (PRDs, design docs, code comments, review reports,
test plans, deployment manuals, changelog entries, etc.) follow this policy:

1. **Default — match the conversation language exactly**:
   - 用户用中文与 Claude 对话 → 产中文文档、中文代码注释、中文报告
   - User talks to Claude in English → produce English artifacts
   - User talks in another language → produce artifacts in that language
   - **Never silently default to a fixed language regardless of the user's input.**

2. **Explicit override always wins**: when the user specifies a language for
   an artifact (e.g. "write the PRD in English", "用英文写 API 设计文档",
   "output the deploy doc in Japanese"), use that language for that artifact,
   regardless of conversation language.

3. **Mixed-language requirements**: if the user wants some artifacts in one
   language and others in a different language (common: Chinese PRD + English
   API docs for partners), honour each per-artifact instruction.

4. **Uncertain**: if you cannot reliably detect the conversation language,
   ask once before producing the first artifact.

This policy applies to **content** (prose, comments, headings). It does
**not** override technical conventions like English variable names, English
git commit subjects, or English error codes when the project's conventions
require them.
<!-- @include-end templates/prompts/output-language.md -->
7. 必须包含：概述、接口/架构/表结构定义、错误码/异常处理、数据模型
8. API 设计需遵循 RESTful 规范，统一响应格式 `{ code, message, data }`
9. **设计文档自审与自动修复**（每份设计文档创建后立即执行，不可跳过）：
   - 重新阅读刚创建的设计文档，对照 PRD 逐项检查以下质量门禁：

   **方案比较检查**：
   - [ ] 文档开头有「方案比较」节：比较表 + 选定方案 + 怎么选的；或一句「沿用 <既有做法>，没有值得比较的取舍」
   - [ ] 正文按选定方案写，没有混进落选方案的做法

   **PRD 一致性检查**：
   - [ ] PRD 中每条 P0/P1 功能是否都有对应的设计覆盖（接口/表结构/架构组件）
   - [ ] 接口的入参/出参是否与 PRD 描述的功能行为一致
   - [ ] 错误码是否覆盖了 PRD 中列出的异常场景

   **API 设计检查**（如有 API 文档）：
   - [ ] 接口 URL 命名是否遵循 RESTful 规范（名词复数、层级清晰）
   - [ ] 请求/响应结构是否完整（无缺失字段）
   - [ ] 统一响应格式 `{ code, message, data }` 是否一致执行
   - [ ] 分页接口是否有 page/pageSize/total 参数
   - [ ] 鉴权方式是否明确说明

   **数据库设计检查**（如有 DB 文档）：
   - [ ] 每张表是否有主键定义
   - [ ] 外键关系是否与 ER 图一致
   - [ ] 常用查询字段是否有索引设计
   - [ ] 是否有 `created_at`、`updated_at` 等审计字段
   - [ ] 迁移 DDL 是否完整可执行

   **跨文档一致性检查**（如同时有 API + DB 文档）：
   - [ ] API 响应字段是否与数据库字段对应（字段名、类型）
   - [ ] API 的查询/筛选参数是否有对应的数据库索引支撑

   **自动修复**：
   - PRD 功能遗漏：自动补充对应的接口/表设计
   - 缺失的错误码：根据接口行为自动补充常见错误码（400/401/403/404/409/500）
   - 缺失的索引：根据查询模式自动补充索引设计
   - 缺失的审计字段：自动添加 `created_at`、`updated_at`
   - 缺失的分页参数：自动补充列表接口的分页设计
   - 修复后在文档末尾追加审查记录：
     ```
     ## 自审记录
     - 审查时间：<ISO 8601>
     - 对照 PRD：<PRD 文件路径>
     - 发现问题：X 项
     - 自动修复：X 项
     - 修复明细：
       - [已修复] <问题描述>
     ```

10. 创建完成后，提示用户下一步是编写测试用例（`/pdlc-tdd <功能名>`）

设计目标: $ARGUMENTS

<!-- pdlc:meta 由 frontmatter 生成（adapters/sync_skills.py），勿手改 -->
> **本命令的状态机取值**：阶段短名 `design`（写进 `history[].stage` 与 `last_phase_result.stage`）；下一跳 `pdlc-tdd`（写进 `next_step`，交接时提示）。
<!-- pdlc:meta-end -->
<!-- @include templates/prompts/state-update.md（已内联于下方，无需另读） -->
## 状态机更新（段四必须执行）

本命令完成主产出后，必须推进状态机文件 `docs/.pdlc-state/<feature-id>.json`。

### 用脚本推进，不要手写状态 JSON

```bash
bash scripts/pdlc-advance.sh <功能ID> --stage <本阶段短名> --next <下一跳命令名|null> \
  [--produced <产物路径，逗号分隔>] [--autonomous] [--decision "<确认点>=<所选默认>"]... \
  [--name <kebab-case>（状态文件还不存在时）] <项目根>
```

- 脚本是本 skill 自带的 `scripts/pdlc-advance.sh`。阶段短名与下一跳就是本命令正文里「本命令的状态机取值」那两个值；带了 `--autonomous` 就照传
- **检查由脚本自己跑**：它按阶段调用同目录的 `scripts/pdlc-checks.sh`（tdd 验红灯；impl / fix / refactor 跑 unit、coverage、lint；
  review 再加 e2e；e2e 只跑 e2e；文档类阶段不跑），据此判 `ok`、整段写入 history 与 `last_phase_result`，
  写完调用 `scripts/pdlc-state-lint.sh` 体检。**不要**自己先写 `checks`，也不要挑检查项
- tdd 阶段的 `--produced` 必须列出写的测试文件：脚本记下它们的指纹，之后 impl / refactor / review 推进时比对
- 主动交还人类（命中人工点、评审有阻塞项、测试本身有矛盾等）→ 加 `--blocked "<原因>"`：脚本照跑检查、如实记录，但不推进，原因写进 `blocked_reason`
- `/pdlc-ship` 写 `ship_done`、`/pdlc-deploy` 写 `deploy_done` → 加 `--done`（只有这两个命令能用）

脚本的退出码决定怎么收尾：

| 退出码 | 含义 | 你要做的 |
|---|---|---|
| `0` | 已推进 | 交接里引用 stdout 那行 JSON（`checks`、`current_stage`、`next_step`） |
| `3` | 未推进：检查没过 / 红灯没验证 / 主动 block / tdd 写的测试被改 | 把 stdout 里的 `blocked_reason` 原样写进报告，按阻塞收尾。**不要为了让它推进去改测试或改检查命令** |
| `2` | 脚本跑不了（参数错、缺 jq、状态文件损坏） | 参数错就改正重跑；缺 jq 才按下面的格式手写，并在报告里写明「状态机未经脚本写入」 |

> 退出码 `3` 且原因是「tdd 阶段写的测试被改动」：实现阶段不改测试。测试是否真的写错了（与设计 / PRD 矛盾），**只有人能判断**：
> - 交互模式：先把矛盾讲清楚、问人；人同意后再带 `--tests-changed "<理由>"` 重跑，理由记进 `auto_decisions`
> - `--autonomous`：没有人可问，**不要改测试**，带 `--blocked "<矛盾在哪>"` 收尾。自主模式下带 `--tests-changed` 脚本也不推进
>
> 项目开了 PDLC 护栏（`docs/00_standards/pdlc-hooks.yml`）时，用 Write / Edit 直接写状态文件会被拦下。

### 状态文件格式（读状态时参考；只有脚本跑不了时才照它手写）

```json
{
  "feature_id": "<F/B ID>",
  "feature_name": "<kebab-case>",
  "created_at": "<首次创建时间 ISO 8601>",
  "current_stage": "<当前阶段名>",
  "run_mode": "interactive | autonomous",
  "history": [
    {
      "stage": "<阶段名>",
      "done_at": "<ISO 8601>",
      "produced": ["<相对路径 1>", "<相对路径 2>"],
      "self_audit": { "passed": <N>, "failed": <N>, "manual": <N> },
      "auto_decisions": [
        { "point": "<autonomous 下自动前进的确认点>", "chose": "<所选默认>", "at": "<ISO 8601>" }
      ]
    }
  ],
  "last_phase_result": {
    "stage": "<本次阶段名>",
    "ok": true,
    "advanced_to": "<推进到的下一阶段 | null>",
    "checks": {},
    "self_audit": { "failed": 0 },
    "blocked_reason": null,
    "run_mode": "interactive | autonomous",
    "at": "<ISO 8601>"
  },
  "relations": {
    "extends": [],
    "depends_on": [],
    "supersedes": [],
    "resolves": [],
    "conflicts_with": [],
    "relates_to": [],
    "_updated_at": "<ISO 8601 | 省略>"
  },
  "next_step": "<下一跳命令名，如 pdlc-design；若流程结束则为 null>"
}
```

> ⛔ 示例里的 `"checks": {}` 是「本阶段没有命令可跑」的样子，**不是键名示范**——键名与取值见下方 §1。

> **`relations` 块（RFC#6，Phase 1 可选，Phase 2 推荐）**：6 个 key 对应 6 种关系类型，各为 ID 数组，存**出边**。其中 `conflicts_with` / `relates_to` 是对称类型，两端都要写；其余四种有向，只写在源 feature 上。拿不准时用 `/pdlc-relate set` 写入，它会按规则校验。旧状态文件无此块时视为全空，向后兼容。入边由 `/pdlc-relate rebuild` 派生到 `_relations.json`，不在此块手维护。

> ⛔ **写状态机的四条硬约束**——读侧（`/pdlc-status`、`/pdlc-retro`、`/pdlc-relate`）会逐条体检，
> 违反的每一处都会出现在它们输出的最前面：
>
> 1. **实例里不写 `terminal_state`**。skill frontmatter 的 `terminal_state:` 是「这个命令走完后应到达的终态名」，
>    不是状态字段。判终态只看 `current_stage` 是否以 `_done` 结尾。
> 2. **`history[].stage` 写本命令的阶段短名**（见本命令正文里「本命令的状态机取值」）——`pdlc-implement` 写 `impl`，
>    不写 `implement` / `implementation`；`pdlc-prd` 写 `requirements`，不写 `prd`。
> 3. **时间戳必须带时刻**：`created_at` / `done_at` / `at` 一律写完整 ISO 8601（如 `2026-07-28T10:40:00+08:00`）。
>    只写日期，同一天内的阶段耗时就全部算成 0——读侧只能记「不可测」。
> 4. **`next_step` 只写命令名或 `null`**，不附说明文字（如「pdlc-ship（等评审通过）」）。
>    要说明原因，阻塞时写进 `last_phase_result.blocked_reason`。

> ⛔ **`_done` 的含义是「已发布」，只由 `/pdlc-ship`（写 `ship_done`）与 `/pdlc-deploy`（写 `deploy_done`）写入。**
> 其它命令的 `current_stage` 一律写本命令的阶段短名，走完整条链路的编排命令（`/pdlc-feature`）也一样——
> 它收尾时 `current_stage` 是最后一个阶段的短名，`next_step` 是 `pdlc-ship`。
>
> - 「评审通过、等待发布」就是 `current_stage` 为 `review` 且 `next_step` 为 `pdlc-ship`（`/pdlc-e2e` 在评审之前，它的下一跳是 `pdlc-review`）。
>   循环相关文档里说的 `review_done` 指的就是这个状态，**不是**要写进 `current_stage` 的值。
> - 为什么：读侧判「已抵达终态」只看 `current_stage` 是否以 `_done` 结尾。评审通过就写 `_done`，
>   `/pdlc-ship` 就分不清哪些功能已经发布过，发布说明会重复或漏收。
> - 旧版本写入的 `feature_done` / `fix_done` / `review_done` 分不清是否已发布，`/pdlc-ship` 会列出来请人确认。

### 手写回退（仅脚本退出码 2 且无法修正时）

1. **文件不存在** → 创建文件，写入初始结构（`history` 为含当前阶段的数组）
2. **文件存在** → 读取 JSON，追加当前阶段到 `history`，更新 `current_stage` 和 `next_step`
3. **写回文件**：用 `jq` 或等效工具保持格式化
4. **写完体检**：运行 `bash scripts/pdlc-state-lint.sh <项目根>`，属于本功能状态文件的偏差当场改正。退出码 `2`（缺 jq 等）= 没体检，报告里写明「未体检」，不得当作通过。

⚠️ 若更新失败（文件损坏/权限问题），必须中止命令并在最终报告中报错。状态机不可跳过。

### `last_phase_result`（机器可读阶段结果；脚本按下面的规则写，手写回退时照做）

顶层 `last_phase_result` 是循环判停的**唯一真源**，外层只需 `jq '.last_phase_result.ok'` 即可决定 继续 / 停止 / 交还人类。规则：

1. **`checks` 只放真跑命令的退出码结果**（`scripts/pdlc-checks.sh` 的 stdout 原样），键名只能是 `tests_pass` / `coverage_pass` /
   `lint_clean` / `e2e_pass`（tdd 段 `red_verified`），值只能是布尔或 `null`（无法判定）。不照抄 `test-commands.yml` 的 `unit` / `lint`，
   不写 `"4 passed, 1 failed"` 这类摘要。没有检查可跑的阶段（文档类阶段、项目无 `test-commands.yml`）→ `checks: {}`，
   绝不因为「本阶段成功」就填 `true`——schema 示例里 `checks` 是空的，正是这个意思。
2. **`self_audit` 单列**：只放自检未通过数，**仅供参考，不作循环判停依据**。
3. **`ok` 的定义**：没有命中 `blocked_reason`，且 tdd 段 `red_verified` 为 `true`、其它阶段没有任何检查为 `false`（`null` 不拦）→ `true`；否则 `false`。
4. **命名空间**：`advanced_to` = **下一阶段的短名**，**不是命令名、也不是本阶段的 `current_stage`**。三者关系：`stage`=本阶段短名、`current_stage`=本阶段完成后的当前短名、`advanced_to`=下一阶段短名、`next_step`=下一跳命令名。

   ⛔ **短名不是「命令名去掉 `pdlc-` 前缀」**——`pdlc-implement` 的短名是 **`impl`**，不是 `implement`。别推导，查下表：

<!-- stage-map:start -->
   | `next_step`（下一跳命令名） | `advanced_to`（下一阶段短名） |
   |---|---|
   | `pdlc-tdd` | `tdd` |
   | `pdlc-implement` | `impl` |
   | `pdlc-review` | `review` |
   | `pdlc-design` | `design` |
   | `pdlc-ship` | `ship` |
   | `pdlc-deploy` | `deploy` |
<!-- stage-map:end -->

   `next_step` 为 `null`（终态或无后续）时 `advanced_to` 也是 `null`。

   > 📌 **本表是唯一真源，且是被断言钉住的**：每行的短名必须等于该 skill 自己 frontmatter
   > 里声明的 `stage:`，且任何 skill 的非 `null` `next_step` 都必须在表里有行——两个方向
   > 都由 `tests/frontmatter-check.sh` 检查，所以表不会和实现各自漂移。
   >
   > 写错短名的后果与键名写错同类：消费方按契约名匹配，认不出就当没这个阶段。
5. **推进一致**：`ok=true` 时本阶段必须真的推进了 `current_stage`（与第 6 条 IRON LAW 呼应）；到达终态或无后续时 `advanced_to=null`。`ok=false`（含 blocked）时 `current_stage` 不变、`advanced_to=null`、`blocked_reason` 写明原因。
6. **`run_mode`**：镜像本次调用是否带 `--autonomous`（带了写 `autonomous`，没带写 `interactive`）。
<!-- @include-end templates/prompts/state-update.md -->
<!-- @include templates/prompts/handoff.md（已内联于下方，无需另读） -->
## 段四：交接（Handoff）

命令完成后必须输出以下格式的最终消息：

```
✅ <阶段名> 完成：<主要产出物路径>
📊 自检：<通过数>/<总数> 通过（若有未通过，附要点）
📦 状态快照：docs/.pdlc-state/<feature-id>.json
👉 下一步：/pdlc-<next_step>
   （如果有分叉）或 /pdlc-<alt>（条件：<选择依据>）
```

**规则：**
- 主流程命令（写状态机的命令；下一跳见正文里「本命令的状态机取值」）必须显式输出"下一步"，不可省略
- 工具型命令（Layer 3）可以没有 `next_step`，此时输出 `👉 下一步：（本次流程结束，无后续）`
- 分叉场景必须说明**选择条件**，例如"若需补充测试用例 → `/pdlc-tdd`；若测试已齐 → `/pdlc-review`"
<!-- @include-end templates/prompts/handoff.md -->
