---
name: pdlc-retro
description: 迭代复盘——读状态机历史出趋势报告
argument-hint: "[--range 7d|30d|all] [--feature <feature-id>]"
allowed-tools: Read, Glob, Bash
layer: 2
stage: retro
produces:
  - docs/07_reviews/retro/<YYYY-MM>-retro.md
requires:
  - docs/.pdlc-state/
next_step: null
terminal_state: retro_done
---

# PDLC 迭代复盘

读取 `docs/.pdlc-state/` 下的状态机历史，按时间范围聚合，生成趋势复盘报告。

<!-- @include templates/prompts/iron-law-tool.md（已内联于下方，无需另读） -->
⛔ **IRON LAW · 不可违反的硬门禁（工具型命令）**

本命令不是主链路上的阶段：**不追加 `history`，不改 `current_stage` / `next_step` / `last_phase_result`**，也不为此分配功能ID。以下规则不可协商：

1. **文件必须落盘**：正文要求创建的文件必须作为实际文件写入磁盘，不可仅在对话中输出（只要求在对话里输出的，照正文办）。
2. **自检必须执行**：产出后按本命令的自检项逐项核对，不得以"已经很好了"为由跳过。
3. **防循环**：修复只做一次，不递归。修不了的问题记进报告，继续往下走。

**违反任一条 = 立即中止当前命令，输出违规详情，等待人工介入。**
<!-- @include-end templates/prompts/iron-law-tool.md -->

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

## 段一：聚合统计

### 1.1 参数解析

- `--range <N>d | all`：时间窗口（默认 `30d`）
- `--feature <feature-id>`：只看单个功能的时间线（输出 history 详情而非聚合）

### 1.2 读取与过滤

1. 列出 `docs/.pdlc-state/*.json`（跳过 `_` 前缀的索引文件与 `statusline.json`）
2. **跑契约体检**（见上方「读状态机之前：先做契约体检」），结果写进报告开头的「输入契约体检」节
3. 按 `created_at` 过滤到时间窗口内。缺 `created_at` 的文件改用 `history` 末条 `done_at`——**这是口径替换，必须计入体检块**，不得静默
4. 解析每份文件的 `history` 数组

### 1.3 计算指标

对时间窗口内的所有功能聚合：

**交付量**：
- 完成功能数：`current_stage` 以 `_done` 结尾——**判终态的唯一依据**，不看 `terminal_state`（它是目标不是事实）、不用封闭列表
- 修复缺陷数：`feature_id` 以 `B` 开头（契约口径）。体检报 `id-prefix-mismatch` 的文件在体检块点名，**不据此改口径**——两个口径打架时，报出来比悄悄挑一个更有用

**质量趋势**：
- 每阶段自检通过率（`passed / (passed + failed + manual)`）；某阶段一条自检记录都没有 → 写「无数据」，不写 0%
- 各阶段自检平均 `failed`、`manual` 数
- 行按阶段短名：`stage-alias` 按 `别名→短名` 归一化后计数（归一化了哪些写进体检块）；`stage-unknown` 单独成行，不并入任何阶段

**阶段耗时**：
- 相邻 history 条目的 `done_at` 差值作为阶段耗时，输出各阶段中位数
- 任一端时间戳没有时刻（体检报 `timestamp-no-time`）→ 该间隔**不可测**，不计入中位数；全部不可测 → 整节写「不可测：<原因>」。**不得输出 0.0h**——它会被读成「快到不耗时」，实际是精度不够

**卡点案例**：
- 自检 `failed > 2` 或 `manual > 1` 的阶段
- 同一阶段耗时 > 3 天的功能

### 1.4 自动推进的运行记录

状态机只记「走到了哪」，记不下「循环驱动推了几次、在哪被拦、为什么」——这些在驱动的运行记录里。用本 skill 自带的 `scripts/pdlc-loop.sh` 汇总（只读，不调用模型）：

```bash
bash scripts/pdlc-loop.sh --report --since <窗口起点 YYYY-MM-DD> --project <项目根>   # --range all 时不带 --since
```

- 输出**原样**放进报告的「自动推进（循环驱动）」节，表里的数字一个都不改、不重算
- 在原样输出下面写 1～3 句解读：哪个阶段被拦得最多、卡点原因里哪一类最多。只说输出里看得到的，不推测原因
- 输出是「没有循环运行记录」→ 该节只写这一句，不算异常
- 脚本跑不了（退出码非 0）→ 该节写「未汇总：<错误>」，不要自己去翻运行记录目录拼数字
- `--feature` 模式不跑这一步

## 段二：自检

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

**复盘报告自检清单：**
- [ ] 时间窗口正确（参数解析无误）
- [ ] 数值可加总（交付量、质量趋势）
- [ ] 列出了至少 1 个卡点案例或明确说明"无卡点"
- [ ] 体检有偏差时，报告**开头**有「输入契约体检」节，且后文计算没有再用已声明忽略的字段（如 `terminal_state`）
- [ ] 阶段耗时没有把「不可测」写成 0.0h
- [ ] 「自动推进」节是脚本的原样输出（或「没有循环运行记录」/「未汇总：<错误>」），解读没有超出输出里的数字

<!-- @include templates/prompts/loop-prevention.md（已内联于下方，无需另读） -->
## 防循环规则

本命令所有的自检-修复循环均受以下约束：

1. **单次检查**：同一个自检清单在本次命令执行中只跑一次（起始 + 修复后验证共两次读）
2. **单次修复**：发现的问题只尝试修复一轮
3. **不递归**：修复后不再重新触发自检的全量重跑
4. **失败降级**：无法自动修复的问题 → 记录到自审报告 → 流程继续 → 最终报告标注待人工处理

这是为了防止 agent 在"修完再查、查完再修"的往返中陷入死循环。
<!-- @include-end templates/prompts/loop-prevention.md -->

## 段三：生成报告文件

1. 确定输出路径：`docs/07_reviews/retro/<YYYY-MM>-retro.md`（按当月归档）
2. 写入模板：

```markdown
# <YYYY-MM> PDLC 迭代复盘

> 时间窗口：<起> ~ <止>
> 生成时间：<ISO 时间>

## 输入契约体检
（仅在体检有偏差或无法体检时出现；按「偏差类 × 份数 × 处理方式」汇总，放在全文最前面）

## 交付量
- 完成功能：<N> 个
- 修复缺陷：<M> 个

## 质量趋势
| 阶段 | 自检通过率 | 平均失败数 | 平均人工介入数 |
|------|----------|------------|--------------|
| requirements | XX% | N.N | N.N |
| design       | XX% | N.N | N.N |
| tdd          | XX% | N.N | N.N |
| impl         | XX% | N.N | N.N |
| review       | XX% | N.N | N.N |

## 阶段耗时中位数
- 需求: X.Xh  设计: X.Xh  TDD: X.Xh  实现: X.Xh  评审: X.Xh
  （时间戳缺时刻导致不可测时，写「不可测：<原因>」，不写 0.0h）

## 卡点案例
- <feature-id> 在 <stage> 阶段: <原因>

## 自动推进（循环驱动）
（`scripts/pdlc-loop.sh --report` 的原样输出，下面 1～3 句解读；没有运行记录时只写「没有循环运行记录」）

## 值得保留的做法
- <从高通过率/低耗时的功能中提炼>
```

3. **IRON LAW 落盘**：文件必须实际写入磁盘，不可仅在对话中输出

## 段四：交接

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

**本命令的 handoff 输出：**

```
✅ 复盘报告已生成：docs/07_reviews/retro/<YYYY-MM>-retro.md
📊 时间窗口：<起> ~ <止>，共 <N> 个功能
⚠️ 输入契约体检：<M> 处偏差（见报告开头；无偏差则省略本行）
👉 下一步：（本次流程结束，建议人工 review 报告）
```

---

**参数**：$ARGUMENTS
