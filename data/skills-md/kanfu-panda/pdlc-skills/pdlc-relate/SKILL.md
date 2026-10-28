---
name: pdlc-relate
description: 管理 feature 关系链（set/query/impact/orphans/rebuild/validate）
argument-hint: "<set|query|impact|orphans|rebuild|validate> [args]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
layer: 3
stage: ops
produces:
  - docs/.pdlc-state/_relations.json
  - docs/.pdlc-state/_graph.md
requires: []
next_step: null
terminal_state: null
---

# Feature 关系链管理

<!-- @include templates/prompts/iron-law-tool.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁（工具型命令）**

本命令不是主链路上的阶段：**不追加 `history`，不改 `current_stage` / `next_step` / `last_phase_result`**，也不为此分配功能ID。以下规则不可协商：

1. **文件必须落盘**：正文要求创建的文件必须作为实际文件写入磁盘，不可仅在对话中输出（只要求在对话里输出的，照正文办）。
2. **自检必须执行**：产出后按本命令的自检项逐项核对，不得以"已经很好了"为由跳过。
3. **防循环**：修复只做一次，不递归。修不了的问题记进报告，继续往下走。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law-tool.md -->

管理 PDLC feature 之间的关系链。维护反向索引 `docs/.pdlc-state/_relations.json` 和全局图 `docs/.pdlc-state/_graph.md`。

<!-- @include templates/prompts/relations.md（已内联于下方，无需另读） -->
## Feature 关系链（6 种类型）

PDLC 用扁平 feature ID 空间。关系链在 5 个位置冗余表达，本文件是类型与语法的**单一真相源**。

### 6 种关系类型

| 类型 | 语义 | 方向性 | 示例 |
|---|---|---|---|
| `extends` | A 是 B 的增量增强 | 有向（A→B） | `user-auth-otp` extends `user-auth-phone` |
| `depends_on` | A 需要 B 存在 | 有向（A→B） | `user-profile` depends_on `user-base` |
| `supersedes` | A 替代 B（B 进入废弃/待机） | 有向（A→B） | `auth-v2` supersedes `auth-v1` |
| `resolves` | A 修复缺陷 B | 有向（A→B） | `F20260603-090000` resolves `B20260520-110000` |
| `conflicts_with` | A 与 B 互斥 | 对称 | `payment-stripe` conflicts_with `payment-paypal` |
| `relates_to` | 弱耦合，应一起考虑 | 对称 | `password-policy` relates_to `otp-policy` |

**有向 vs 对称**：
- 有向类型（extends / depends_on / supersedes / resolves）只在源 feature 的关系块里存一条出边。
- 对称类型（conflicts_with / relates_to）写入时**两端都要镜像**（A.conflicts_with 含 B 时，B.conflicts_with 也必须含 A）。

### 表达位置 1：文档追溯头（pdlc-trace）

在 PDLC-TRACE 头加一行（无关系时整行省略）：

```
<!-- 关系: extends=F20260510-100000; depends_on=F20260501-090000,F20260415-110000; resolves=B20260520-110000 -->
```

语法：`type=id` 对，多 id 用 `,` 分隔，多对用 `; ` 分隔。

### 表达位置 2：状态机关系块（state JSON）

即状态机文件里的 `relations` 块（六键对象，每键一个 ID 数组）。存**出边**；入边由 `/pdlc-relate rebuild` 派生到 `_relations.json`。**只写本功能自己的状态文件**——不要为了「双向」去改对方功能的 `relations`，那是别的功能的状态，改了会让它看起来又被动过。

### 表达位置 3：反向索引 `_relations.json`（自动生成）

`/pdlc-relate rebuild` 扫描所有 `<id>.json` 关系块 + 文档头，生成正向 edges + 预计算 inbound/outbound index。

### 表达位置 4：全局图 `_graph.md`（自动生成）

mermaid 可视化。边样式按类型区分：`supersedes` 虚线、`conflicts_with` 粗线、其余实线。

### 表达位置 5：PRD §6.1 关系表

见 PRD 文档的 §6.1「关系」一节。

### 校验规则（`/pdlc-relate validate`）

- 悬空引用：关系指向的 ID 不存在
- 自引用：feature 关系到自己
- 循环：`extends` / `depends_on` 链不允许成环
- 矛盾对：同一目标同时 `supersedes` + `depends_on`
- 对称一致性：`conflicts_with` / `relates_to` 两端必须互含
<!-- @include-end templates/prompts/relations.md -->

<!-- @include templates/prompts/state-read.md（已内联于下方，无需另读） -->
## 读状态机之前：先做契约体检

`docs/.pdlc-state/*.json` 不一定都是 `/pdlc-*` 命令写出来的——手写的、旧版本写的、照着格式仿写的
都可能混在里面。字段对不上契约时，**不许边猜边算、再把猜出来的东西当结论**。先体检，再计算；
体检发现的每一处偏差，都必须出现在输出的**最前面**。

### 1. 跑体检

体检脚本随本 skill 一起分发，就在本 skill 目录下：`scripts/pdlc-state-lint.sh`（运行时会告知本 skill 的
所在目录）。它与正在运行的 skill 同一版本，体检规则——合法阶段名、偏差代码——与下方 §2 一致。

在项目根执行 `bash <本 skill 目录>/scripts/pdlc-state-lint.sh .`。stdout 每行一条偏差：`文件<TAB>代码<TAB>说明`。退出码三态：

- `0` 已体检、全部合契约 → 照常出结论，不输出体检块
- `1` 已体检、有偏差 → 照常计算，但输出最前面必须先放「输入契约体检」块（见 §3）
- `2` 无法体检（缺 jq / 无状态目录）→ 体检块写「无法体检：<原因>」，**不得当成合契约**

体检脚本不可用时（找不到，或当前平台没有随 skill 分发它），按 §2 的规则逐条人工核对，
体检块首行注明「体检脚本不可用，以下为人工核对」。

### 2. 体检规则（偏差代码）

读侧跳过 `_` 前缀的索引文件（如 `_relations.json`）与 `statusline.json`，它们不是功能状态机。

<!-- finding-codes:start -->
| 代码 | 判定 | 读侧怎么处理 |
|---|---|---|
| `json-invalid` | 文件不是合法 JSON | 跳过该文件，列入体检块 |
| `missing-field` | 缺 `feature_id` / `current_stage` / `history` / `next_step` / `created_at` 之一 | 用到该字段的指标，对这份文件记「不可判」 |
| `field-type-invalid` | 字段在、类型不对（如 `current_stage` 不是字符串、`history` 不是数组、`last_phase_result` 不是对象、history 条目不是对象） | **按缺失处理**：用到它的指标对这份文件记「不可判」。类型不对的时间戳不再另报 `timestamp-no-time` |
| `missing-last_phase_result` | 缺 `last_phase_result`（多为旧文件） | 不推断本阶段结果与 checks |
| `terminal_state-in-instance` | 实例里出现 `terminal_state` | **忽略该字段**，判终态只看 §4 |
| `non-contract-field` | 其它表外顶层字段（如 `title`） | 忽略 |
| `stage-alias` | `stage` 用了已知别名 | 可按说明里的 `别名→短名` 归一化计数，**但必须在体检块写明归一化了哪些** |
| `stage-unknown` | `stage` 既不是短名也不是已知别名 | 单独成行，不并入任何阶段 |
| `current_stage-unknown` | `current_stage` 既不是短名，也不以 `_done` 结尾 | 该功能归入「❓ 异常」 |
| `next_step-not-command` | `next_step` 不是纯命令名（如带散文后缀） | 按原文展示，不据此推断下一步 |
| `timestamp-no-time` | 时间戳只有日期、没有时刻 | 依赖它的**耗时类指标记「不可测」**，不得算成 0 |
| `relations-not-object` | `relations` 不是六键对象（如数组） | 这份文件的关系**不入图**，列入体检块 |
| `relations-unknown-type` | 关系键不在六类之内 | 该键下的关系不入图 |
| `relations-target-not-id` | 关系目标不是 feature ID（散文、模块路径等） | 该条不入图 |
| `relations-dangling` | 目标 ID 没有对应的状态文件 | 标「悬空」，不参与影响半径计算 |
| `id-prefix-mismatch` | 走的是修复流程（有 `fix` 阶段），ID 却不以 `B` 开头 | 缺陷计数按 ID 前缀的契约口径算，同时在体检块点名这份 |
| `checks-key-unknown` | `last_phase_result.checks` 里有状态机不认的键（如照抄 yml 的 `unit` / `lint`） | 该键当作不存在：对应维度记「无法判定」，**不**按键名猜它对应哪个 check |
| `checks-value-invalid` | check 的值不是布尔也不是 `null`（如 `"4 passed, 1 failed"`） | 该项记「无法判定」，不从字符串里解析结论 |
| `ok-checks-mismatch` | `ok=true`，但有 check 为 `false` | **以 checks 为准**：本阶段按未通过展示，在体检块点名这份 |
| `done-legacy` | `current_stage` 以 `_done` 结尾，但不是 `ship_done` / `deploy_done`（旧版写法） | 按「已走完」展示但标「是否已发布未知」；`/pdlc-ship` 会列出来请人确认 |
| `second-state-dir` | 仓库根另有一个 `.pdlc-state/` | 本命令只读 `docs/.pdlc-state/`，提示两处并存 |
<!-- finding-codes:end -->

**「不入图」不是丢弃**：关系目标是散文时，把它硬解读成某个 feature，等于把猜测升格成结构——
影响半径会因此多出一条本不存在的强依赖。宁可在体检块里原样列出，交给人判断。

#### 阶段短名全集

`history[].stage` 与 `last_phase_result.stage` 只能取下表的短名——每个短名由对应命令写入，
等于该命令 frontmatter 的 `stage:`。别名只为**读**旧数据时容忍，归一化必须披露；**写**的时候一律用短名。

<!-- stage-names:start -->
| 短名 | 由哪个命令写入 | 已知别名（读侧可归一化，须披露） |
|---|---|---|
| `requirements` | `pdlc-prd` | `prd` |
| `design` | `pdlc-design` | |
| `tdd` | `pdlc-tdd` | |
| `impl` | `pdlc-implement` | `implement, implementation` |
| `review` | `pdlc-review` | |
| `e2e` | `pdlc-e2e` | |
| `ship` | `pdlc-ship` | |
| `deploy` | `pdlc-deploy` | |
| `fix` | `pdlc-fix` | `bugfix` |
| `refactor` | `pdlc-refactor` | |
| `feature` | `pdlc-feature` | |
<!-- stage-names:end -->

> 旧版 `/pdlc-task` 曾写入 `task`，现已不写（任务看板不是阶段，写入会覆盖主链路的 `current_stage` / `next_step`）。
> 见到 `current_stage=task` 说明那次任务操作把功能的阶段盖掉了：体检报 `current_stage-unknown`，向用户说明后按 `history` 里最后一个主链路阶段理解进度。

### 3. 体检块的格式（放在输出最前面）

```
⚠️ 输入契约体检：<N> 份状态文件，<M> 处偏差——以下结论建立在这些处理之上
  · 3/5 份缺 created_at → 时间窗改用 history 末条 done_at
  · 阶段别名 prd→requirements ×1、implementation→impl ×2 → 已归一化计数
  · 5/5 份含 terminal_state → 已忽略（判终态只看 current_stage）
  · 2 份的 done_at 只有日期 → 阶段耗时记「不可测」
```

- **按「偏差类 × 份数 × 处理方式」汇总**，不要把脚本输出原样倒出来
- **放最前面，不放末尾**——结论会被单独引用，偏差得跟着结论走；写在报告末尾的偏差表，
  读者看到的时候已经信了前面的数字
- **计数照抄脚本输出，不要自己重数**：按代码计数用 `cut -f2 | sort | uniq -c`，份数按第一列去重。
  真机验证时脚本报 25 处无时刻的时间戳，报告正文却自己数成了 26——同一份报告里两个数字对不上，
  读者就不知道该信哪个
- 同一次输出里，前面披露了「已忽略 X」，后面的计算就不得再用 X

### 4. 判终态的唯一依据 ⛔

**已抵达终态 ⇔ `current_stage` 以 `_done` 结尾**（终态即「已发布」：`/pdlc-ship` 写 `ship_done`、`/pdlc-deploy` 写 `deploy_done`；旧版本留下的 `feature_done` / `fix_done` / `review_done` 也按终态读）。

- **不看 `terminal_state`**。状态机实例本就没有这个字段。skill frontmatter 里的 `terminal_state:`
  说的是「这个命令走完后**应当**到达的终态名」——是**目标**，不是**事实**。拿它判终态，
  等于把「打算完成」当成「已经完成」。
- **不用封闭列表**（如只认 `[feature_done, fix_done]`）。封闭列表会把合法的终态漏判成「进行中」，
  逼着读侧去别的字段里找答案——而最顺手的那个字段恰好就是 `terminal_state`。
- **`next_step` 为 `null` 也不等于终态**：`/pdlc-task` 写的 `next_step` 恒为 `null`，却未必完成；空的或残缺的状态文件也读得出 `null`。
<!-- @include-end templates/prompts/state-read.md -->

## 段一：执行子命令

从本命令的参数解析子命令。子命令分两类，**只读类绝不写任何文件**：

| 类别 | 子命令 | 写什么 |
|---|---|---|
| 写入类 | `set` / `rebuild` | `<fid>.json` 的 `relations` 块（仅 `set`）、`_relations.json`、`_graph.md` |
| 只读类 | `query` / `impact` / `orphans` / `validate` | 不写 |

只读类遇到 `_relations.json` **缺失或比任一状态文件旧**时：从各状态文件的 `relations` 块当场现算（只在内存里），
并在输出里注明「索引缺失 / 已过期，本次现算、未落盘；要持久化请跑 `/pdlc-relate rebuild`」。
**不要替用户顺手 rebuild**——查询命令悄悄改仓库，用户会在 `git status` 里看到两个来路不明的文件。

### `set <fid> <type> <target-fid> [target-fid...]`
为 feature `<fid>` 添加 `<type>` 关系，指向一或多个目标。
1. 读 `docs/.pdlc-state/<fid>.json`；**若无 `relations` 块**（旧状态文件 / Phase 1 关系块可选），先初始化六类空块（`extends`/`depends_on`/`supersedes`/`resolves`/`conflicts_with`/`relates_to`），再在 `relations.<type>` 数组追加目标（去重）
   - **`relations` 存在但不是六键对象**（体检报 `relations-not-object`，如数组形态）→ **停下，不写**。
     把现有条目原样列出，请人确认迁移方式后再动。直接初始化六类空块会把原有条目连同其中的说明文字
     一起覆盖掉——这是静默的数据丢失，比关系写不进去更坏
2. 若 `<type>` 是对称类型（conflicts_with / relates_to）→ 同时在每个目标的 `<fid>.json` 镜像写入
3. 写回后调用本命令 `rebuild` 流程刷新 `_relations.json` + `_graph.md`

### `query <fid>`
显示 `<fid>` 的全部关系（出边 + 从 `_relations.json` 读入边）。

### `impact <fid>` ⭐ 杀手锏
分析改动 `<fid>` 的影响半径。读 `_relations.json`（缺失或过期时按上文现算，不落盘）：
- 🔴 **直接影响**（depth 1 入边）：**只有** extends / depends_on 本 feature 的，必须协调
- 🟡 **间接影响**（depth ≥2 传递入边）：沿 extends / depends_on 传递的，应 review
- 🟢 **历史**（指向**已抵达终态**——`current_stage` 以 `_done` 结尾——的 feature 的边 / resolves 的缺陷）：仅审计
- `relates_to` / `conflicts_with` 是弱关系与互斥，**不进 🔴 / 🟡**，单列「相关 / 冲突」
- 体检中不入图的关系（数组形态、表外类型、散文目标）**不要解读成 feature 依赖**——原样列在体检块里，交给人判断
输出树状结构 + 建议（先 review 哪些 PRD / 是否该新建 supersedes feature 而非就地改）。

### `orphans`
列出 `_relations.json` 中 inbound + outbound 均为空的 feature（可能是孤立 / 死代码候选）。

### `rebuild`
扫描所有 `docs/.pdlc-state/<id>.json` 的 `relations` 块 + 文档追溯头的 `关系:` 行，重建：
- `_relations.json`：nodes（id→name/stage/terminal）+ edges（flat 有向列表）+ index（每节点预计算 inbound/outbound）
  - `terminal` = `current_stage` 以 `_done` 结尾（见上方「判终态的唯一依据」）。**不读 `terminal_state`**——
    它是目标不是事实，拿它算会把「停在 review、目标写着 review_done」的 feature 标成已完成
  - 只收**六键对象形态**、目标为合法 feature ID 的关系；体检报 `relations-not-object` / `relations-unknown-type` /
    `relations-target-not-id` 的不入图，列进输出的体检块
  - 目标 ID 没有状态文件（`relations-dangling`）的不入 edges，交给 `validate` 报告——不要为了过自检去造占位节点
- `_graph.md`：mermaid 图，边样式按类型区分（supersedes 虚线 / conflicts_with 粗线 / 其余实线），顶部加 `<!-- AUTO-GENERATED by /pdlc-relate · do not edit by hand -->`

### `validate`
按 `relations.md` 的校验规则检查：悬空引用 / 自引用 / extends·depends_on 成环 / 矛盾对 / 对称一致性。报告问题清单。

## 段二：自检（强制）

<!-- @include templates/prompts/self-audit.md（已内联于下方，无需另读） -->
## 段二：自检（强制）

重新阅读本次产出物，按质量关卡清单逐项检查。勾选已通过，标注未通过原因。

> **注意**：自检清单的具体内容由各命令自行定义，本片段只规定结构。

## 段三：修复（单次，不递归）

针对自检段标注为未通过的项：

- **可自动修复**：直接修复（如补缺字段、修正格式、补齐缺失段落）
- **修复后回验**：再次运行自检，确认被修复项现在通过
- **无法自动修复**：记录到自审报告，不再尝试，流程继续

⚠️ 单次修复原则：若一轮修复后仍有项未通过，**不再递归修复**，防止死循环。
<!-- @include-end templates/prompts/self-audit.md -->

### 关系链自检清单

- [ ] `_relations.json` 是合法 JSON（`jq . ` 通过）
- [ ] 所有 edge 的 from/to ID 在 nodes 中存在（无悬空）
- [ ] 对称类型（conflicts_with / relates_to）两端互含
- [ ] extends / depends_on 无环
- [ ] `_graph.md` 含 `AUTO-GENERATED` 头且 mermaid 语法成对闭合
- [ ] set 操作的目标 ID 格式合法（F/B 开头）
- [ ] 只读类子命令（query / impact / orphans / validate）没有写任何文件
- [ ] nodes 的 `terminal` 全部按 `current_stage` 后缀算，没有读 `terminal_state`

## 段三：修复（单次，不递归）

<!-- @include templates/prompts/loop-prevention.md（已内联于下方，无需另读） -->
## 防循环规则

本命令所有的自检-修复循环均受以下约束：

1. **单次检查**：同一个自检清单在本次命令执行中只跑一次（起始 + 修复后验证共两次读）
2. **单次修复**：发现的问题只尝试修复一轮
3. **不递归**：修复后不再重新触发自检的全量重跑
4. **失败降级**：无法自动修复的问题 → 记录到自审报告 → 流程继续 → 最终报告标注待人工处理

这是为了防止 agent 在"修完再查、查完再修"的往返中陷入死循环。
<!-- @include-end templates/prompts/loop-prevention.md -->

- 可自动修复（对称缺失补镜像 / index 不一致 → 重跑 rebuild）→ 直接修
- 无法自动修复（真实的循环依赖 / 用户意图矛盾）→ 记录到报告，提示人工介入

## 段四：交接

> **状态机豁免**：本命令非 feature-scoped（不推进单个 feature 的阶段），不更新 `<feature-id>.json` 的 history，只维护关系索引文件。同 `/pdlc-changelog`。

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

**本命令的 handoff 输出**（按子命令类别二选一）：

写入类（`set` / `rebuild`）：

```
✅ 关系操作完成：<子命令> <参数>
📦 已更新：docs/.pdlc-state/_relations.json + _graph.md
👉 下一步：/pdlc-relate impact <fid> 查影响 | /pdlc-status 看全景
```

只读类（`query` / `impact` / `orphans` / `validate`）：

```
✅ 关系查询完成：<子命令> <参数>（只读，未写任何文件）
👉 下一步：/pdlc-relate rebuild 持久化索引（若本次为现算） | /pdlc-status 看全景
```

体检有偏差时，两种都在最前面加一行 `⚠️ 输入契约体检：<M> 处偏差（见开头）`。

---

**关系操作**: $ARGUMENTS
