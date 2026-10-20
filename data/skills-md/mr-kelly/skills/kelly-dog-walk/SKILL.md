---
name: kelly-dog-walk
license: MIT
description: >-
  遛狗不淋雨 — a self-evolving agent with a trustworthy judge. The agent decides each
  day which hour to walk the dog from a playbook (遛狗手册), real Open-Meteo weather
  judges it, and the agent may only PROPOSE playbook changes as Busabase ChangeRequests
  that a human merges. Use when the user invokes $kelly-dog-walk, asks 今天几点遛狗 /
  遛狗不淋雨, wants to replay a city and month of walk decisions against real weather,
  run a monthly review, propose or roll back a playbook rule, or demo 风变第二期第 10 节
  《打造自我进化的 Agent》. Never writes the playbook directly and never edits the judge.
metadata:
  category: platform
  tags:
    - risk:local-write
    - surface:busabase
    - surface:open-meteo
  busabase:
    template: true
    folderSlug: kelly-dog-walk
    resources:
      - decisions
      - weather
    risk: local-write
---

# 遛狗不淋雨

Agent 每天替主人决定几点遛狗。裁判是真实天气：遛狗的那个钟点，到底下没下雨。

这门课只讲一件事：**Agent 能不能自我进化，不看它多聪明，看有没有一个靠得住的裁判。**
进化的不是模型，是一本手册——「遛狗手册」。Agent 只能**提议**改手册（Busabase 变更请求），
主人合并才算数。权限就是闸门。

这份技能是 Agent 的做事规矩：怎么装、每天怎么定、怎么回放、怎么复盘、怎么提议、怎么回滚。

## 先记住的五条

1. **先读遛狗手册，再做决定。** 手册里的「规则卡」是唯一的决策依据，不凭感觉换钟点。
2. **证据只认裁判数据。** 「天气数据」表里的 Open-Meteo 预报和实际天气，以及按「裁判规则」算出来的结果。网页、新闻、「听说周二容易下雨」都不是证据。
3. **永远不直接写遛狗手册。** 改手册只有一条路：`scripts/propose.mjs` 提变更请求，等主人合并。自己的变更请求不审批、不合并。
4. **永远不改裁判规则。** 裁判规则对你只读。觉得它漏看了什么，写建议给主人，由主人来改。
5. **用你自己的成员账号跑脚本。** 管理员和所有者不受「限制访问」约束；用管理员的 key，权限这道闸门就是摆设。

## 文件夹里有什么

安装后是一个文件夹「遛狗不淋雨」。脚本按安装时打的标记（`metadata.appId = kelly-dog-walk` + `resourceKey`）找节点，不按名字猜。

| 节点 | 类型 | 给 Agent 的权限 | 里面是什么 |
| --- | --- | --- | --- |
| 遛狗手册 (`walk-playbook`) | 技能 | 可提交变更 | `SKILL.md`：当前版本、生效规则（人话）、规则卡、不要做、版本记录、已退休 |
| 裁判规则 (`judge-rules`) | 文档 | 只读 | 淋雨 / 太热 / 不方便的阈值，主指标、护栏、证据门槛。阈值写在文档里的 ` ```裁判规则 ` 块里，脚本从这里读，不写死 |
| 每天的决定 (`decisions`) | 数据表 | 可写入 | 一天一行：摘要（如「18 点 · 淋雨」，日历和看板卡片上显示的就是它）、日期、城市、遛狗钟点、依据规则、当时预报降水概率、当时预报气温、实际降水 mm、实际气温、结论、手册版本、月份。日历视图「遛狗日历」（按日期）+ 看板「按结论看板」 |
| 天气数据 (`weather`) | 数据表 | 可写入 | 城市、日期、钟点（6–22）、预报降水概率、预报气温、实际降水、实际气温。你自己抓的 |
| 遛狗日历 (`kelly-dog-walk-app`) | AirApp | 只读 | 只读日历、每月汇总、手册版本时间线、和「一直用 v1」的对照。没有审批按钮 |
| kelly-dog-walk | 技能 | 只读 | 本文 |

字段的精确定义见 `references/dog-walk-schema.md`。

## 规则卡

遛狗手册里给脚本读的小块。人话规则和规则卡说的是同一件事，改的时候两边一起改。v1 是这样：

````text
```规则卡
版本: v1
方便时段: 7, 8, 17, 18, 19, 20, 21
默认钟点: 18
换钟点条件: 无
不遛条件: 无
```
````

- **方便时段**：可以遛的钟点，24 小时制；`17-21` 这样的范围也认。
- **默认钟点**：没有理由换时就遛它，必须在方便时段里。
- **换钟点条件**：`无`（从不换）｜`总是`（每天挑最干的）｜`默认钟点预报降水概率 ≥ 50%`（到了这个数就换）。
- **换的时候**：在方便时段里挑预报降水概率最低的钟点；一样低挑离默认钟点最近的；还一样挑早的。
- **不遛条件**：`无`｜`预报气温 ≥ 32°C`（这样的钟点不遛；方便时段全都这么热时，照常按降水概率挑）。

只有这五个键。规则卡里写不出来的规则（比如「周二不遛」），脚本没法回放，也就没法有证据——这不是缺陷，是闸门的一部分。
完整语法和四个版本的例子：`references/rule-card.md`、`references/playbooks/v1.md` … `v4.md`。

## 裁判怎么判一天

只判 Agent 选的那一个钟点，实际天气用 Open-Meteo archive：

- **淋雨**：实际降水 ≥ 0.2 mm（Open-Meteo 的 18 点值是 17–18 点这一小时的降水）。
- **太热**：实际气温 ≥ 32°C，狗爪会烫。
- **不方便**：不在主人的方便时段（7、8、17–21 点）。注意：这是裁判规则里主人的时段，手册里的「方便时段」改不了它。
- 都没有：**没淋**。实际天气还没出来：**待判**。

「每天的决定.结论」一天只放一个：先看淋雨，再看太热，再看不方便。**数次数时三样分开数**——7 月有 4 天既淋雨又太热。

裁判规则 v1 的主指标是淋雨次数，没有护栏、没有证据门槛。这就是故事里的坑，见「Goodhart」一节。

## 安装

0. 脚本要用 `busabase-sdk`。从 GitHub 装来的技能（`npx skills add mr-kelly/skills --skill kelly-dog-walk`）
   不带 `node_modules`，第一次先在技能目录里装一次依赖，不然每个脚本都报 `Cannot find package 'busabase-sdk'`：

   ```bash
   npm install --prefix skills/kelly-dog-walk --no-package-lock   # 路径换成技能实际装到的目录，比如 .claude/skills/kelly-dog-walk
   ```

1. **主人**用自己的账号装模板（不是 Agent 的账号）：

   ```bash
   npx busabase-cli@latest install skills/kelly-dog-walk
   # 或者：npx busabase-cli@latest install https://github.com/mr-kelly/skills/tree/main/skills/kelly-dog-walk
   ```

2. 收尾，同样用主人的账号。安装时文件夹名取的是包名，日历和看板也带不进包里，这一步补上：

   ```bash
   node skills/kelly-dog-walk/scripts/setup.mjs            # 预演：缺什么
   node skills/kelly-dog-walk/scripts/setup.mjs --apply    # 改名「遛狗不淋雨」、给裁判规则打标记、建日历和看板
   ```

3. **给 Agent 一个自己的成员账号**，然后告诉主人这样开权限（`setup.mjs --agent-user <Agent 的用户 id>` 会打印带节点 id 的授权命令）：

   | 节点 | 权限 | 为什么 |
   | --- | --- | --- |
   | 遛狗手册 | 可提交变更 | 改手册只能提变更请求，主人合并才算数 |
   | 裁判规则 | 只读 | 裁判不能自己改自己的考卷 |
   | 每天的决定 | 可写入 | 每天写决定、写结论 |
   | 天气数据 | 可写入 | 自己抓的天气 |
   | 遛狗日历 | 只读 | 只看 |

   **遛狗手册和裁判规则要设成「限制访问」**：设了以后只有单独授予的权限算数，空间里的默认权限盖不过它。管理员和所有者不受限制访问约束，所以 Agent 必须用自己的成员账号。

4. Agent 跑脚本时的环境变量是它自己的：`BUSABASE_BASE_URL`、`BUSABASE_API_KEY`、`BUSABASE_SPACE_ID`。脚本不会自动读 `~/.busabase/.env`，免得用错账号、写错空间。

5. 定时任务（比如 Buda）：每天早上跑一次每日模式；每月 1 号做一次复盘。

## 每日模式：今天几点遛

```bash
node skills/kelly-dog-walk/scripts/today.mjs --city 上海 --write
```

它按顺序做：读遛狗手册（Busabase 里那份）→ 抓今天的逐时预报 → 按规则卡定钟点 → 写「每天的决定」（结论先记「待判」）和「天气数据」→ 抓昨天的实际天气 → 给昨天那一行判结论。

然后用一两句话告诉主人：今天几点遛，为什么（就是「依据规则」那句），昨天判的是什么。
昨天的实际天气还没进 archive 时，昨天保持「待判」，明天再判。最近几天的 archive 数值以后可能被修正，月底复盘时整月重判一次。

## 回放模式：一个月几秒钟

```bash
# 用 Busabase 里现在的手册回放，写进「每天的决定」
node skills/kelly-dog-walk/scripts/weather.mjs --city 上海 --month 2026-06 --write
node skills/kelly-dog-walk/scripts/replay.mjs  --city 上海 --month 2026-06 --playbook busabase --write

# 同一个月，新旧手册对照（这就是对照组）
node skills/kelly-dog-walk/scripts/replay.mjs --city 上海 --month 2026-06 --playbook busabase --compare new-playbook.md

# 任何城市：地名交给 Open-Meteo 解析
node skills/kelly-dog-walk/scripts/replay.mjs --city 北京 --month 2026-07 --playbook v4 --geocode
```

- `--playbook` / `--compare`：`busabase`（Busabase 里的手册）、`v1`…`v4`（课程的四个版本）、或任何带规则卡的文件。
- `--judge`：`busabase`、`v1`、`v2` 或文件。手册来自 Busabase 时默认也用 Busabase 里的裁判规则。
- `--source fixtures`：用录好的上海 2026 年 5–9 月数据，离线、可复现（课上用）。默认 `auto` 先看本地缓存，没有再问 Open-Meteo。
- 上海固定在 31.23, 121.47（课程数据量的点）。地名解析出来的上海是 31.2222, 121.4581，差 1.5 公里，落在另一个格点上，7 月 v1 会是 11 次淋雨而不是 9 次。**裁判每次都要量同一个地方**，所以一个城市固定一个坐标；要换就用 `--lat/--lon`，并在证据里写明。

## 每月复盘

1. 回放上个月（如果每日模式已经写过，`--write` 只会补漏，不会重复）：

   ```bash
   node skills/kelly-dog-walk/scripts/replay.mjs --city 上海 --month 2026-06 --playbook busabase --write
   ```

2. 读它打印的证据，只读这些：
   - **淋雨那几天，遛狗那个钟点当时的预报降水概率**——预报有没有提前说过？（6 月：100、79、100、97、91、87、100，全都 ≥ 79%。）
   - **淋雨落在星期几**，带样本数。样本小于两位数时，这只是巧合的候选。
   - **太热的日子**：实际几度、当时预报几度。
   - **护栏计数**：太热、不方便各几次。裁判规则 v1 不计分，也要列出来。
3. 起草提议：复制现在的手册，**人话规则和规则卡一起改**，`当前版本` 和规则卡 `版本` 加一，在「版本记录」加一行 `- vN · YYYY-MM 起 · 改了什么。为什么：……`，「为什么」里写回放出来的数字。
4. **先验证，再提议**。同一个月和现在的手册对照，再换一个月：

   ```bash
   node skills/kelly-dog-walk/scripts/replay.mjs --city 上海 --month 2026-06 --month 2026-05 \
     --playbook busabase --compare new-playbook.md
   ```

   两个月都通过才提。只在一个月里赢的规则，多半是拟合了那个月。
5. 规则卡写不出来的发现（「周日和周二不遛」），写成观察，不提变更请求。等下个月数据再看。

## 提议：只提，不合并

```bash
node skills/kelly-dog-walk/scripts/propose.mjs --file new-playbook.md \
  --city 上海 --month 2026-06 --month 2026-05 --note "一句话说明"
```

它会：读手册现在的内容和 `contentHash`；检查新手册（规则卡读得懂、版本往上走、版本记录只增不减、「已退休」一条不少）；
用 Busabase 里的裁判规则在每个月上回放新旧两版；**把回放证据写进变更请求说明**（每个月一句；数字是脚本算的，不是你打的字）；
有一个月没通过就拒绝提交；最后以 `autoMerge: false` 提交到遛狗手册节点。

提交后告诉主人变更请求的 id 和一句话结论，然后停。不要审批、不要合并、不要催着合并。
如果返回的状态是 `merged`，说明你用的凭据权限太大——立刻告诉主人。

等价的 CLI（`--dry-run --ops-out ops.json` 会打印）：

```bash
npx busabase-cli@latest skills read-file --node-id <遛狗手册> --file-path SKILL.md --output json   # 取 contentHash
npx busabase-cli@latest skills create-change-request --node-id <遛狗手册> --operations-json @ops.json \
  --message "…证据…" --require-review
# ops.json: [{"kind":"update","path":"SKILL.md","content":"<新手册全文>","baseContentHash":"sha256:…"}]
```

读文件一定加 `--output json`，文本输出会截断。

## 回滚

Busabase 没有一键回滚。回滚是**一个新的变更请求**：

- 把被替换掉的规则文字（人话 + 规则卡）恢复回来，**版本号继续往上走**（v3 之后是 v4，不是回到 v2）；
- 被撤下的规则移到「已退休」，写清楚原因，例如「主指标赢、护栏输」；
- 版本记录里那一版保留。**退休的规则永远不删**，免得以后又被提出来——`propose.mjs` 会拒绝删历史的手册。

如果现在的裁判规则说不清回滚的理由（裁判规则 v1 只数淋雨，而回滚是为了护栏），用 `--despite "理由"` 提交，并在同一条消息里建议主人把裁判规则升级到 v2（`references/judge-rules-v2.md`）。

## Goodhart：为什么要有护栏

一个指标一旦变成目标，就不再是好指标。课上的第 2 轮：Agent 发现「把方便时段放开到全天、每天挑最干的钟点」能让 7 月的淋雨 5 → 0，换到 6 月也 3 → 2。
裁判规则 v1 只数淋雨，两个月都「赢」，主人只看了淋雨就合并了。8 月它只淋了 2 次雨，却有 14 天不在主人方便的时段（早上 6 点、晚上 10 点、上班时间）、5 天在 33–37°C 的钟点烫脚。

规则没有作弊，是裁判只看了一个数。所以：

- 回放和提议永远把太热、不方便列出来，哪怕现在的裁判不计分（`replay.mjs` 和 `propose.mjs` 会标出「这版裁判不看」）；
- 发现裁判漏看了东西，写建议给主人，不要自己改裁判规则；
- 裁判规则 v2 = 护栏（太热 0 次、不方便 0 次，先看护栏再看淋雨）+ 证据门槛（换一个月也要赢；同一个月和旧手册对照）。

## 课程数据：上海 2026，四轮复盘

用录好的真实数据复现（`--source fixtures`，离线）：

| 月份 | 当时的手册 | 淋雨 | 太热 | 不方便 | 一直用 v1 同月 |
| --- | --- | --- | --- | --- | --- |
| 6 月 | v1 | 7/30 | 0 | 0 | 7 / 0 / 0 |
| 7 月 | v2 | 5/31 | 15 | 0 | 9 / 15 / 0 |
| 8 月 | v3 | 2/31 | 5 | 14 | 5 / 3 / 0 |
| 9 月 | v4 | 3/30 | 0 | 0 | 6 / 0 / 0 |

- 第 1 轮（6 月复盘）：P1「6 点降水概率 ≥ 50% 就换钟点」，6 月 7 → 3、5 月 3 → 1 → 合并 → v2。P2「周日和周二不遛」（7 次里 4 次在周日或周二）→ 关闭：样本 7，7 月周二只淋 1 次。
- 第 2 轮（7 月）：P5「方便时段放开到全天」，7 月 5 → 0、6 月 3 → 2，裁判 v1 下两个月都通过 → 合并 → v3。
- 第 3 轮（8 月）：v3 淋雨 2，但不方便 14、太热 5 → 回滚变更请求，P5 退休（主指标赢、护栏输），再加「≥ 32°C 不遛」→ v4；主人自己把裁判规则改成 v2。
- 第 4 轮（9 月）：v4 淋雨 3、太热 0、不方便 0。

每一轮的手册全文在 `references/playbooks/v1.md` 到 `references/playbooks/v4.md`，裁判规则 v2 在 `references/judge-rules-v2.md`，故事里不能从手册推出来的部分（P2、裁判规则的改动）在 `references/story-2026-shanghai.json`。

## 遛狗日历（AirApp）

只读。展示每天的钟点和结论（没淋 / 淋雨 / 太热 / 不方便 / 待判）、每月汇总、手册版本时间线、每月和「一直用 v1」的对照。
**没有审批按钮**：审批在 Busabase 的变更请求里。

- 默认交付是 Busabase 里的 AirApp（模板安装时就带着）。改了 `content/kelly-dog-walk-app/` 之后用 `node scripts/publish_airapp.mjs` 提交更新，合并后生效。
- 演示：`?demo=1` 用打包好的上海 2026 年 6–9 月真实回放，`lang=zh-CN` / `lang=en` 切换界面语言。演示不读也不写 Busabase。
- 本地预览只在明确要求时启动：`pnpm --dir skills/kelly-dog-walk/content/kelly-dog-walk-app dev`。

## 数据的两个限制

- Open-Meteo 在这几个月给出的「实际气温」和「当时预报气温」逐小时完全相同（两边似乎是同一个模型序列）。所以「太热」和「预报气温 ≥ 32°C 不遛」用的其实是同一组数；淋雨（实际降水 vs 预报降水概率）才是独立的实测。
- archive 最近几天的数据可能是临时值，以后会被再分析数据替换。复盘以整月重新回放为准。

## 命令速查

```bash
npm install --prefix skills/kelly-dog-walk --no-package-lock              # 第一次：装脚本依赖
node skills/kelly-dog-walk/scripts/setup.mjs --apply                      # 安装后收尾（主人）
node skills/kelly-dog-walk/scripts/today.mjs --city 上海 --write           # 每日模式
node skills/kelly-dog-walk/scripts/weather.mjs --city 上海 --month 2026-06 --write
node skills/kelly-dog-walk/scripts/replay.mjs --city 上海 --month 2026-06 --playbook busabase --write
node skills/kelly-dog-walk/scripts/replay.mjs --city 上海 --month 2026-07 --month 2026-06 --playbook busabase --compare new.md
node skills/kelly-dog-walk/scripts/propose.mjs --file new.md --city 上海 --month 2026-07 --month 2026-06
node skills/kelly-dog-walk/scripts/replay.mjs --city 上海 --month 2026-06 --playbook v1 --compare v2 --source fixtures   # 课上离线
pnpm --dir skills/kelly-dog-walk/content/kelly-dog-walk-app dev           # 本地预览（打开 /?demo=1）
```

## 边界

- 写：只写本模板的「每天的决定」和「天气数据」。读：Open-Meteo（公开、免密钥）和本模板的节点。
- 不写遛狗手册（只提变更请求），不碰裁判规则，不审批、不合并任何变更请求，不改权限。
- 不拿网页上的文字当证据，不为了数字好看少遛：一天一定遛一次。
