---
name: model-killing-line
description: "Draws the 模型斩杀线 - Pareto-frontier scatters (Vibe Code Bench Score vs Cost/Test + Artificial Analysis Intelligence Index vs Cost per Task + Vals AI Terminal-Bench 4.0 Score vs Cost/Test + CommandCode Max 10× 智力 vs 每月可跑请求数 + OpenCode Go 智力 vs 每月估算请求数) as a single-page HTML with hover tooltips, efficient-zone shades, separate charts/tables per source, and one joint 解读. Use when the user asks for a 斩杀线, Vibe Code / 编码能力 chart, AA chart, TBench/Terminal-Bench chart, CommandCode chart, OpenCode Go / OpenCode 套餐 chart, or Pareto frontier of coding models. Takes no arguments - data always comes from https://www.vals.ai/benchmarks/vibe-code, https://www.vals.ai/benchmarks/terminal-bench-4, https://artificialanalysis.ai/leaderboards/models, https://commandcode.ai/docs/plans/max and https://opencode.ai/console/go."
---

# model-killing-line

Zero-argument skill. Fetches the two Vals AI leaderboards (Vibe Code Bench +
Terminal-Bench 4.0), the Artificial Analysis model leaderboard,
加上两个订阅套餐页（CommandCode Max 10× / OpenCode Go），computes each Pareto
frontier, and emits a
single-page `index.html` with switchable sections (tab 切换，默认通用智力，
解读常驻) — chart + table per board 由脚本生成，解读由 LLM 每次实时撰写（脚本不写解读文案）；

- ① 通用智力斩杀线（数据源 Artificial Analysis）: X = Cost per Task USD (log axis),
  Y = Intelligence Index, efficient zone = Index > 35 & cost < $1
  (表格只收 Index > 20 且 Cost 有效的行；2026-11 起 AA 表格只有 7 列，
  Creator 从模型 logo 的 alt 抓，效率维用榜单自带的 Time per Task（分钟，越短越快），
  tok/s 已拿不到——详见下面 fetch-aa.mjs 一节).
- ② 编码能力斩杀线（数据源 Vals AI Vibe Code Bench，tab 文案「编码能力」）:
  X = Cost / Test USD (log axis，跑完一个完整建站任务的成本)，Y = Vibe Code Bench Score (%)，
  efficient zone = Score ≥ 80% & cost ≤ $5。**这张榜取代了原来的 DeepSWE**
  （DeepSWE 2026-09 之后停止更新，Vibe Code Bench 2026-11-05 仍在跑）。**一行一个模型，
  ~121 行全部进表格**：页面原始 ~124 行里 3 个模型被不同 harness 重复跑过（Claude Opus 4.8
  的 OpenHands/Claude Code、GPT 5.5 的 OpenHands/Factory/Codex、Claude Sonnet 4.6 的
  Claude Code/OpenHands），fetch 时折叠成「最高分那次 run」。**harness 不进任何展示面**
  （绝大多数行都是 OpenHands，没有信息量，露出来只会让同一模型出现三行像 bug）——
  身份键就是 model，图上圈/表格徽标/tooltip 三态按它判定。页面没给 Cost 的 7 行
  （Beam 1.0 / Muse Spark / Grok Build 0.1 / Laguna M.1 / Laguna XS.2 / Nemotron 3 Ultra /
  SWE-1.6 Fast）没有 X 坐标，只进表格不进图。**效率维用榜单自带的 Duration / Test**
  （跑完一个任务要多久，越短越好；tokens÷duration 那种自算速度不用——它会奖励话痨模型，
  跟"跑得快"不是一回事）。前沿大圆半径按最近邻自适应（R = minDist/2 − 2，夹在 [8,18]），
  因为 DeepSeek 三代挤在 $0.36/$0.41/$0.58 会把固定 R=18 叠成一坨。
- ③ 终端智能斩杀线（数据源 Vals AI Terminal-Bench 4.0 榜, 可选）: URL
  https://www.vals.ai/benchmarks/terminal-bench-4，X = Cost / Test USD (log axis，页面直接给，
  不再用 total_cost_usd ÷ n_trials 折算)、Y = Score %（Terminal-Bench 4.0 解决率），
  efficient zone = Score ≥ 40% & cost ≤ $10。**这张榜取代了原来的 tbench.ai 官方榜**
  （旧榜只给整次 run 的总成本、混着 agent × reasoning_effort 多档变体，X 轴要折算、表格 8 列；
  Vals 榜与同站 Vibe Code Bench 完全同构，2026-11-05 更新，61 行，一行一个模型，
  harness 全是 Mini-SWE-agent）。**身份键 = model**：harness / agent / effort 都不进任何
  展示面，图上圈 / 表格徽标 / tooltip 三态都按它判定。页面没给 Cost 的 1 行（Beam 1.0）
  没有 X 坐标，只进表格不进图。**效率维用榜单自带的 Duration / Test**（越短越好，与编码榜
  同口径），不再用 run 平均 tok/s。带 tb-data.json + tb-chart.svg 时 gen-html 自动启用
  第三个 tab；缺这两个文件则保持双榜页面不报错。表格 6 列：
  `# / Model / Score / Cost/Test / Tokens/Test / Duration`，按 score 降序，全部 61 行进表
  （Cost 缺失行显示 —）。前沿大圆半径按最近邻自适应（同编码榜）。
- ④ CommandCode 斩杀线（数据源 CommandCode 官方文档，可选）: X = Max 10× 官方
  `Requests / month`（log 轴，向右＝更能跑），Y = 智力指数。右上方高性价比区 =
  智力 ≥ 35 且 ≥ 100K 次/月。**只做 Max 10×**——OpenCode / Pro plan 的请求数、
  Max 20× 的额度都不能混进来（口径不同，混了图就没意义）。详见下面
  「CommandCode tab 的口径与过滤规则」一节，那一节是本 tab 的行为契约，改动前先读。
- ⑤ OpenCode Go 斩杀线（数据源 OpenCode 官方文档，可选）: X = **基础 Go（$10/月）**
  官方估算的 `Requests per month`（log 轴，向右＝更能跑），Y = 智力指数（**AA 单源**）。
  右上方高性价比区 = 智力 ≥ 27 且 ≥ 100K 次/月。**只做 Go 一档**：Go Plus（$40，3× 额度）/
  Go Teams（$20/member）都是同一批模型的三套额度，混进来会让同一模型在图上出现三个 X 位置，
  而图上没有价格轴。详见下面「OpenCode Go tab 的口径与过滤规则」一节。
- 解读只有一块: 由 LLM 每次实时根据最新数据自由撰写，脚本不生成解读文案，只提供数据。

Frontier models render as logo circles with callout labels, everyone else
as small dots, efficient zone shaded top-left. Every dot shows a hover
tooltip with its model name.

All artifacts go to the OS temp dir (`os.tmpdir()/model-killing-line/`,
overridable via `MKL_DIR` env var) — never the repo. The final `index.html`
is auto-opened in the system default browser via `open.mjs`.

## The core loop (run from anywhere; outputs go to the OS temp dir)

```bash
node .agents/skills/model-killing-line/scripts/fetch-vc.mjs            # → $TMPDIR/model-killing-line/vc-data.json (~121 rows, Vals AI Vibe Code Bench)
node .agents/skills/model-killing-line/scripts/fetch-aa.mjs           # → $TMPDIR/model-killing-line/aa-data.json (~32 rows, AA)
node .agents/skills/model-killing-line/scripts/fetch-tb.mjs            # → $TMPDIR/model-killing-line/tb-data.json (61 rows, Vals AI Terminal-Bench 4.0) — 可选
node .agents/skills/model-killing-line/scripts/fetch-openrouter.mjs   # → $TMPDIR/model-killing-line/or-data.json (Top 30 from OpenRouter Top Weekly, text modality) — 可选
node .agents/skills/model-killing-line/scripts/fetch-plans.mjs         # → $TMPDIR/model-killing-line/plans-data.json (CommandCode Max 10×) — 可选
node .agents/skills/model-killing-line/scripts/fetch-go.mjs            # → $TMPDIR/model-killing-line/go-data.json (OpenCode Go $10/月) — 可选
node .agents/skills/model-killing-line/scripts/find-top-missing.mjs   # → $TMPDIR/model-killing-line/top-missing.json (OR Top 20 里没上双榜的模型) — 可选
node .agents/skills/model-killing-line/scripts/render-vc.mjs          # → $TMPDIR/model-killing-line/vc-chart.svg (logos inlined as data URIs)
node .agents/skills/model-killing-line/scripts/render-aa.mjs          # → $TMPDIR/model-killing-line/aa-chart.svg
node .agents/skills/model-killing-line/scripts/render-tb.mjs          # → $TMPDIR/model-killing-line/tb-chart.svg — 可选（和 fetch-tb 成对，结构与 render-vc 同构）
node .agents/skills/model-killing-line/scripts/render-plans.mjs       # → $TMPDIR/model-killing-line/plans-chart.svg — 可选（和 fetch-plans 成对）
node .agents/skills/model-killing-line/scripts/render-go.mjs          # → $TMPDIR/model-killing-line/go-chart.svg — 可选（和 fetch-go 成对）
node .agents/skills/model-killing-line/scripts/gen-html.mjs [--with-top-missing]  # → $TMPDIR/model-killing-line/index.html (单文件 HTML；存在 tb-data.json + tb-chart.svg 时自动加「终端智能」tab，存在 plans-data.json + plans-chart.svg 时再自动加「CommandCode」tab，存在 go-data.json + go-chart.svg 时再自动加「OpenCode Go」tab；带 --with-top-missing 才注入 OR Top 缺失行；解读区只留 #llm-obs 空位)
# LLM 看完本轮数据后自由撰写解读 HTML 片段，存文件后注入：
node .agents/skills/model-killing-line/scripts/gen-html.mjs [--with-top-missing] --obs /tmp/mkl-obs.html  # --obs <html文件|->（- 从 stdin 读；MKL_OBS 传路径亦可）
node .agents/skills/model-killing-line/scripts/open.mjs               # auto-open index.html in default browser
```

`$TMPDIR/model-killing-line` = `os.tmpdir()/model-killing-line` (i.e.
`/tmp/model-killing-line` on Linux/macOS). Set `MKL_DIR` env var to override.
`open.mjs` uses `open` (macOS) / `cmd start` (Windows) / `xdg-open` (Linux)
and falls back to printing the `file://` path when no GUI browser exists.
Optionally verify headlessly before calling it done:

```bash
agent-browser open file://"$(node -e "console.log(require('os').tmpdir())")"/model-killing-line/index.html
```

No parameters on any step. Thresholds live in the scripts, not in arguments —
see below. The scripts read/write via cwd and need only node stdlib.

## What each script does

- `fetch-vc.mjs`: GETs https://www.vals.ai/benchmarks/vibe-code 的 SSR HTML，在
  `<table aria-labelledby="benchmark-leaderboard-title">` 里逐 `<tr>` 抓 7 列
  （Rank / Model+详情页 href / Harness / Score / Cost / Test / Tokens / Test / Duration / Test）。
  原始行先按 model 折叠（同模型多 harness 只留 score 最高、同分更便宜的那次），
  每行输出 `{rank, model, harness(仅留档，不展示), runs, score, cost(缺失 null), tokens,
  tokens_disp, duration_sec, duration_disp, org, slug, url}`。
  org 与 slug 来自详情页路径 `/models/<org>_<slug>`（如 `anthropic_claude-sonnet-5-5`），
  用来拼 OpenRouter 链接，比按名字前缀猜准。Throws when zero rows parse — 页面改版
  （列顺序/表格容器变更）时看文件头的列约定。页面顶部还有 `Updated MM/DD/YYYY` 文案，
  脚本会打印出来（当前 10/29/2026）。
- `render-vc.mjs`: 结构同 `render-aa.mjs`（自适应 log x 轴、碰撞感知 callout、透明 hit-area、
  `data-*` 驱动 tooltip），但：
  · 身份键 = model（一行一个模型；harness 在 fetch 阶段已折叠掉，不画不显示）；
  · 效率维 = `duration_sec`（越短越高效，`pareto3` 的第三维按「越大越好」所以传负值）；
    输出只有 `data-tokens` / `data-dur`，没有 tok/s 这个字段；
  · 只画 cost 有效的行（7 行无 cost 的只进表格）；
  · **前沿大圆半径自适应**：R = 最近邻距离/2 − 2，夹在 [8,18]（DeepSeek 三代挤在
    $0.36/$0.41/$0.58，固定 R=18 会重叠 50%+ 把一个点完全盖住）。圆仍画在真实坐标上，
    **不推开**（斩杀线的语义就是真实位置），只缩半径 + 多裁一个 clipPath 尺寸；
  · 画布顶部留 72px（而不是 50px）抬头空间：80~92% 那段太密，气泡只能往点上方放；
  · callout 盒子比 AA 小一号（10px 字 / 18px 高）+ 两轮布局（先严格不压小圆点，
    再放宽允许盖背景点，但永不得压其他前沿大圆/已放盒子/标题）。标签按 `labeled:`
    日志核对：未放下的会列出来（圆点仍在，hover 看名字）。
- `fetch-aa.mjs`: GETs the Artificial Analysis leaderboard SSR HTML and
  parses the `<tbody>` rows. **2026-11 站点改版：表格从 9 列变成 7 列**
  （`Model | Intelligence Index | Cost per Task USD | Time per Task (min) |
  First Answer Token (s) | Context Window | Further Analysis`）：
  · Creator 列没了 → 从模型名 cell 里的 lab logo `<img alt="Anthropic">` 抓 creator
    （比按名字猜准）；
  · Speed 列默认展示 **Time per Task Minutes**（跑完一个任务要几分钟，越短越快）；
    tok/s（`outputSpeed`）只作为页面里可切换的列存在，SSR 不渲染 → 拿不到
    （旧的 `/api/v2/data/*` 已下线，新的 `/api/v2/language/models*` 要 API key）。
    所以 **AA 的效率维 = Time per Task（分钟，越短越好）**，与 Vals 两张榜的
    Duration / Test 同口径；`time_per_task` 缺失的行按 -Inf 处理；
  · 模型名拆成「主名 + effort 变体」（主名在 div、变体在灰色 span：
    `Claude Fable 5.2` + `Max, Default Fallback`）。输出 `model` = `主名 (变体)`，
    另存 `base` / `variant`；`normalizeSlug` 剥括号后仍是主名，OR 链接照旧命中。
  Keeps only Intelligence Index > 20 with cost > 0（log 轴画不了 $0.00 免费档）。
  No public JSON API — SSR HTML is the only source.
- `render-aa.mjs`: same structure as `render-vc.mjs` but for AA data
  (log x 基础域 0.01~10、y 基础域 20~55——**数据超界 / 大量空白时坐标轴自适应**：
  x 按 log 刻度阶梯 `[0.01,0.02,0.05,0.1,0.2,0.5,1,2,5,10,15,20,50,100]` 取
  「比数据最小成本更低一档的刻度」为左边界（数据 0.07 起时轴不再从 $0.01 起，
  否则左侧 1/4 画布是空的）、「覆盖最大成本的下一档刻度」为右边界
  （基础域 $10 封顶会把 $10~13 的模型画到右边框外）；y 上界 = `数据 max + 2`
  再扩到 5 的整数倍（留出前沿大圆 R18+外圈的位置，避免 59 分的点露出画布顶部），
  下界 = `min(20, 数据 min 向下扩到 5 的整数倍)`；x tick 由同一阶梯按域内筛选生成，
  y 刻度随之生成到新上界；
  zone Index > 35 & < $1, `data-creator` / `data-index` 属性,
  same-base-name single label + collision-aware callouts, efficient 高效点描蓝圈同上）。
- `fetch-tb.mjs`: GETs https://www.vals.ai/benchmarks/terminal-bench-4 的 Astro SSR
  HTML，解析 `<table aria-labelledby="benchmark-leaderboard-title">`（与 fetch-vc 完全同构，
  列：Rank / Model+详情页 href / Harness / Score / Cost / Test / Tokens / Test / Duration / Test；
  页面无公开 JSON API，表格是唯一稳定来源）。每行 =
  `{rank, model, harness(仅留档不展示), runs, score, cost(缺失 null), tokens, tokens_disp,
  duration_sec, duration_disp, org, slug, url}`；同模型多 harness 折叠为最高分那次
  （当前 61 行全是 Mini-SWE-agent，这一步是空操作）。页面顶部 `Updated MM/DD/YYYY`
  打印到控制台。Throws when zero rows parse（页面改版时先看文件头的列约定）。
- `render-tb.mjs`: 与 `render-vc.mjs` 同构（log x 轴 `X_LADDER` 阶梯自适应、y 上界按
  数据扩到 5 的倍数、碰撞感知 callout、透明 hit-area、前沿大圆半径按最近邻自适应），
  但标题 / 轴文案是 Terminal-Bench 4.0，zone = Score ≥ 40 & Cost ≤ $10，
  y 轴**不设 100 下限**（当前数据最高 65.15 → 上界 70，否则上半张图全空）。
  `data-model`/`data-score`/`data-cost`/`data-tokens`/`data-dur` 属性 +
  Duration / Test 效率维；3D 差集 + 次级 2D 前沿 → 高效蓝圈同 VC。
  身份键 = model（图上 / 表格 / tooltip 三态一致）。logo 按模型名前缀选
  （Vals 名字带品牌前缀，见 logos.mjs 的 `logoFileOf`），链接用
  `tbLink(model, org)`（= `vcLink` 别名）。
- `fetch-plans.mjs`: GETs `https://commandcode.ai/docs/plans/max`（官方
  `Requests / 5 hours / week / month` 请求表 + 价格表）和
  `https://commandcode.ai/docs/plans/pro`（CommandCode 自家的 `Intelligence` 列，
  以及**只存在于 Pro 页**的 peak 时段价）。输出的 `requests_*` 全部直接引用官方值，
  **不做二次推算**（自算 token 口径值只留作 `est_requests_month` / `est_vs_official`
  做 QA 校验，不参与坐标 / zone / Pareto）。Pro 页的脏模型名（`MiMo V2.5 -98%`、
  `Grok 4.7-40%Ends September 27, 2026`、`DeepSeek V4.1 FlashOff-peak shown …`、
  `JevDecision model …`、`Pixel CanaryFree`）由 `cleanCcName()` 清洗。
- `render-plans.mjs`: 结构同前三个，但**前沿大圆不做 de-clutter**（见下），
  `data-tier` / `data-contributor` / `data-peakwin` 属性，peak 孪生点用虚线环 +
  从 off-peak 拉细连线，Contributor 用橙色虚线大圈 + 两行标注。
- `fetch-go.mjs`: GETs `https://opencode.ai/console/go`（Console 页，唯一剩下的表格
  Model | Relative request allowances | Est. requests / 5 hr | Monthly limit，每行同时给
  Go / Go Plus 两档，只取 `data-plan="go"`）+ 官方 models API
  `https://opencode.ai/inference/go/v1/models`（per-1M 单价 / 月额度 / peak 倍率 / 隐私，
  id 与 Console 页 `data-model` slug 一一对应作 join 键）。旧文档页的三个套餐表 + token 画像
  段落已下线（2026-11 改版）。**X = 官方 Est. requests / 5 hr × 5 = 每月请求数**：新页只给 5h，
  周 = 2.5×5h、月 = 5×5h（旧官方估算表的恒等式，逐模型精确成立），`requests_source` 标
  `official-5h-derived`。自检三条：JSON-LD 里 Go 价格必须是 $10；Console 页与 API 的模型集合
  必须一致；Go 数值必须小于 Go Plus。`Unlimited` 的请求数存 `null` + `free: true`
  （log 轴画不了无限）。Y 轴智力**只用 AA**（见下节），AA 无分的行标 `index_pending`、不上图。
  peak 孪生：仅 `multipliers.when.any`（每日时段窗口，如 DeepSeek 两款 factor=2）才拆；
  `when.date.gte` 型（如 Gemini 4 Argon "2026-12-01 起全天 2×"）只记 notes 不拆行。
- `render-go.mjs`: 与 `render-plans.mjs` 同构（右上高性价比区、按 requests 降序扫 index
  record-high 的右上包络、`MIN_STEP=0.5`、固定 R=15 不做 de-clutter、碰撞感知 callout），
  三处不同：① X 轴用 `X_LADDER` 阶梯自适应（数据 ~735~217k 次/月 → 轴域 500~500k；沿用
  "10 的整数次幂"写法左右会各空掉 1/5 画布）；② Y 轴不设 60 分母，取 `ceil((max+2)/5)*5`
  （当前 50 → 55），只留大圆 + callout 的抬头空间；③ peak 孪生点用灰色虚线环 + 一条从 off-peak
  指过来的细虚线（表示"同一款模型的另一个时段"，不是另一款模型）。`data-req` / `data-req5h` /
  `data-reqweek` / `data-tier` / `data-peakwin` 属性，三态与表格一致。

三维语义（能力 × 成本 × 效率）：2D 前沿（绿，🔪高性价比）只看能力+成本；
效率维三张散点榜各自用自家的时间口径（Vibe Code Bench = **Duration / Test**，
Vals Terminal-Bench 4.0 = **Duration / Test**，AA = **Time per Task（分钟，2026-11 起
AA 的 Speed 列默认就是它；tok/s 只存在于可切换列、SSR 拿不到）**；
CommandCode / OpenCode Go 两张订阅榜无效率维），
**不再做跟 AA 融合的复合效率**（DeepSWE 的 steps 与旧 TBench 的 run 平均 tok/s 都随换源下线了）。
叠加效率后仍无人能全包围的，再在内部按能力×成本取一次次级 2D 前沿
（不画线只判断）：线上才算高效（蓝，⚡），次级线下
（被另一个蓝色全包围）降级真被斩。剩下才是真被斩（无色）。
表格行/图上圈/tooltip/解读全部三态一致；`worst` 只从真被斩里取。
编码表 / 终端表同宽 6 列：`# / Model / Score / Cost/Test / Tokens/Test / Duration`
（Cost 缺失行显示 —，但仍然列在表里；两张 Vals 榜都不设 Harness 列，也不设 Tokens/s 列——
效率看 Duration，token 吞吐对"跑完一个任务要多久"没有解释力）。跨榜重合用 `normalizeSlug` 作归一键直接比
（不再经过 fuse.mjs）。
- `openrouter.mjs`: 模型名归一化 + OpenRouter 详情页链接（`normalizeSlug` 去括号
  effort 后缀 → 小写 hyphen slug；`aaLink(model, creator)` 按 AA 的 creator（2026-11 起从
模型 logo 的 alt 抓，不再有 Creator 列）定 org，
  `vcLink(model, org)` 按 Vals 详情页路径里的 org 前缀定 org（`VALS_ORG_TO_OR`），
  `tbLink` = `vcLink`（两张 Vals 榜同站同源，都按详情页 `/models/<org>_<slug>` 定 org；
  旧 tbench.ai 榜用的是 Creator 列 + `aaLink`，已随换源下线），`dsLink` 现在被 CommandCode 与
  OpenCode Go 两张表共用——它会把名字里的空格先压成 `-` 再匹配前缀（OpenCode 写 `GPT 6 Luna` /
  `MiMo-V2.6-Flash`，不归一化会漏掉 `gpt-` 这一整批，表现为「同一模型在 AA tab 有详情页、
  在 OpenCode tab 只有搜索页」），并新增 `longcat → meituan` / `hy3|hy4 → tencent` /
  `step- → stepfun` 三条前缀；个例进 `SLUG_OVERRIDE`，
  OR 无详情页的进 `SEARCH_ONLY` 回退搜索页）。新增模型先 curl 验 title 非软 404
  再进映射（Vibe Code Bench 那批是用 https://openrouter.ai/api/v1/models 的
  id 清单逐个核对的，19 个已下架/未上 OR 的老模型会走搜索页）。
- `gen-html.mjs`: inlines the SVGs (`chart-code` ← vc-chart.svg + `chart-gen` ← aa-chart.svg,
  以及存在 tb-chart.svg
  时第三个 `chart-tb`、存在 plans-chart.svg 时第四个 `chart-plans`、存在 go-chart.svg 时
  第五个 `chart-go`) + all JSONs + shared
  `LOGO_MAP` into `index.html`: two (带 TB 数据则 three, 再带 CommandCode 数据则 four,
  再带 OpenCode Go 数据则 five) independent chart+table sections + tabs, one joint 解读卡片
  （见下「解读：LLM 实时撰写」——
  脚本只在卡片里留 `<div id="llm-obs">` 空位 + 把数据以 JSON 形式内联进页面供
  LLM 读取，不生成任何解读文案，不硬编码模型名）。页头有小字生成日期
  （构建时写入）+ JS 过期判断：打开时间距生成日期超过 15 天则显示数据过期提示。Tooltips
  bound per-card via `bindTip()`. 所有模型名均可点（表格整行可点 +
  解读 + 图上气泡统一链到 OpenRouter 详情页，无详情页的回退
  搜索页；表格行 hover 加深背景、键盘回车/空格亦可打开）。
  `index.html` is fully self-contained —
  copy it anywhere, no `logos/` folder needed.
  **可选 `--with-top-missing`**（或 `MKL_INCLUDE_TOP_MISSING=1`）：若
  存在 `top-missing.json`，会把 OR Top 20 里「用了但还没上双榜」的模型
  嵌进表格——「上一代」型（hy4-preview / deepseek-v4-flash-0423 /
  muse-spark-1.3-contributor / ...）黄底（🆕 待更新）行挂在
  编码榜/AA 对应上一代行正上方；纯免费型（Laguna S 2.1 (free) 等）青底
  （🆓 免费）行置顶两张表。其它无上一代又非免费的会进 skipped
  名单（控制台报告，不渲染到表）。
- `fetch-openrouter.mjs`: GETs `/api/frontend/v1/models/find?order=top-weekly
  &input_modalities=text`（不需要 agent-browser），response 已是服务端按
  "近 7 天处理 token 数"排序好的结果。analytics 块按 `model_permaslug`
  给每天 prompt/completion tokens，累加即得到页面显示的周 tokens
  （页面数字 ≈ 累加和，差 1 天的忽略）。输出 `or-data.json`，每行
  `{rank, name, short_name, provider, slug, input_price, output_price,
  context_length, is_free, weekly_tokens, created_at}`。
- `find-top-missing.mjs`: 读 `or-data.json` + `vc-data.json` + `aa-data.json`，
  从 OR Top 20 里挑出"用了但还没上双榜"的模型，**双榜分开判断**：
  - OR slug 同时命中 VC + AA（按各自命名规则，VC 用 `normalizeSlug(vcLink().slug)`
    即品牌全名归一化 + `SLUG_OVERRIDE` 兜底、AA 用 `normalizeSlug` 剥
    `(max)/(xhigh)/...` effort 后缀匹配）→ 双榜都已 benchmark，跳过
  - OR slug 只命中 VC：VC 已 benchmark，AA 落后 → 走 `findPredecessor(k, 'aa')` 找 AA successor
  - OR slug 只命中 AA：AA 已 benchmark，VC 落后 → 走 `findPredecessor(k, 'vc')` 找 VC successor
    （例：`DeepSeek V4.1 Flash` slug=`deepseek-v4.1-flash`，AA 有 `(max)` 变体视为同 benchmark，
    编码榜没这个 slug → strip `.1` 后命中 `deepseek-v4-flash`，挂编码表此行上方）
  - 双榜都没直接命中：走 strip 启发式找 predecessor，命中哪 board 就挂哪 board
  - 还找不到：is_free → free 桶；否则 skipped
  - **额外入口（AA highlight → 编码榜缺失）**：复用 render-aa 的 2D+3D 前沿逻辑
    算出 AA 的高性价比 + 高效集合（`frontNames ∪ fastNames`），**两条独立路径**：
    - OR 上有的：OR `normalizeSlug(short_name)` 直接命中 AA highlight canon（不做
      额外后缀剥除，避免把 `ling-3.0-flash-fin` 和 `ling-3.0-flash` 误判为同一个）
      且编码榜里没这个 slug → 作为 VC successor 注入，锚点 key = AA 规范键。
      例：`Ling 3.0 Flash Fin (free)` 的 canon 是 `ling-3.0-flash-fin`，与
      `ling-3.0-flash` 不匹配，不进这里。
    - OR 上没有的：AA highlight 集合里某条不在编码榜里、不在 OR 里、但 AA 本身有
      记录（这是 AA 独立信号，如 `Claude Fable 5.1 (xhigh with fallback)`
      不在 OR Top 30）→ 作为 VC successor 注入，via 标 `'aa-highlight-no-or'`。
      gen-html `tmSubLine` 会用"AA highlight"代替"OR Top #"，`tmUrl` 用
      `aaLink(model, creator)` 拼详情页 URL。
  Strip 启发式：末位日期（`-MMDD`/`-YYYYMMDD`）、嵌入的 `.N`、常见后缀
  （contributor/preview/free/exp/vision/lite/next/plus/flash/fast/pro/...）逐个剥，
  每个候选再 `末位数字 -1`（hy4 → hy3）。输出 `top-missing.json`，
  提供 `successors[] / free[] / skipped[]`，`predecessor: {board, key, via?}` 记录锚点。
  strip 规则增例：新增模型名映射进 `TRAILING_TOKENS` 数组。
  AA-highlight 启发式增例：`AA_HIGHLIGHT_TAIL_TOKENS` 数组（fin/instant/edge/...）。
- `open.mjs`: opens `index.html` in the system default browser (platform
  `open` / `start` / `xdg-open`); never throws — prints the `file://` path
  when auto-open fails.

## 解读：LLM 实时撰写（脚本不生成解读文案）

- `gen-html.mjs` 只负责：页面结构 + 图表/表格 + 把原始数据内联进页面
  （`VC_ROWS` / `AA_ROWS` / `TM_SUCCESSORS` / `TM_FREE` 四个 JSON 常量 + 控制台
  打印的前沿/高效区/最惨名单）。解读卡片里只留一个空位
  `<div id="llm-obs">`（或等价占位），不写任何分析文字。
- 每次跑完管线后，由 LLM（调用本 skill 的 agent）在本轮对话里实时自由撰写解读：
  打开 `index.html`（或直接读 `$TMPDIR/model-killing-line/` 下的
  `vc-data.json` / `tb-data.json` / `aa-data.json` / `top-missing.json` + 终端输出的前沿名单），
  看完本轮数据后自由发挥，写成 HTML 片段（可用 `<ul class="obs">` + `<li>`，
  模型名想链 OpenRouter 可用页面内联的链接，样式类 `.obs a` 已就绪），存文件后用
  `gen-html.mjs --obs <文件>` 注入 `#llm-obs`，再展示/截图给用户。
- 唯一要求：基于本轮实际数据现看现写，不得复用上一轮的解读内容；
  开头第一条固定为 📌 太长不看，用非常精简的一句话按成本优先 / 效率优先 / 能力优先各给一个选择；**三个选择都从 AA 榜取**（详见下面「解读撰写原则」第 1 条），之后条数句式自由发挥。

### 解读撰写原则（Agent 必读的视角提示词）

每次撰写解读前必须把以下五条原则作为强制上下文阅读，不能跳过：

1. **推荐一律从 AA 榜选，📌 太长不看也不例外**。四榜数据时效不一致：AA Intelligence
   Index 每日更新，是唯一有"最新信号"的源；Vals 的两张榜（Vibe Code Bench /
   Terminal-Bench 4.0，数周一次重测）虽然现在同频更新，仍是快照，不适合给新代模型定档。
   **📌 太长不看的三个选择（成本优先 / 效率优先 / 能力优先）必须全部取自 AA 榜**
   （AA 的 Index + Cost per Task + Time per Task 三个字段就够定档），并在括号里标注
   编码榜 / TB 的实测档作为佐证（"编码榜实测 88.9%"），而不是用编码榜 / TB 的数字当
   推荐依据。例如成本优先给 `GPT-6.1 Sol (medium)`（AA 46 分 / $0.36）而不是
   `DeepSeek V4.1 Flash`（编码榜 84.74% / $0.41 的唯一前沿便宜档）——后者在 AA 上只有
   `DeepSeek V4.1 Flash 1017 (max)` 的 32 分，拿它定档就是拿慢榜压快榜。
2. **缺测 ≠ 短板**。编码榜 / TB 暂未实测的"新一代"模型（即页面里挂 `📊 仅 AA 实测`
   徽标的 `unbench-succ` 行）应理解为 "按 AA 实测 + 代际推测的候选"，而不是
   "不推荐" / "待更新" / "缺测 = 短板"。新一代模型通常强于上一代，所以这些候选
   应该被放进选型池而不是排除。解读里必须明确点出"对应的上一代"
   （如 GPT-6 Luna → GPT-5.6 Luna、Claude Opus 5.5 → Claude Opus 5、
   MiMo-V2.6-Pro → DeepSeek V4 Pro），并给出推测涨幅（如"编码榜推测 ≥ 67%"）。
3. **避免暗示短板的措辞**。禁用 "暂缺" / "待更新" / "短板" / "缺测 = 不推荐"
   等暗示模型不行的措辞；改用 "未实测（按代际推测 ≥ 前代 X）"。📌 太长不看
   一行也要按这个视角写：被推荐的应该是"AA Index X + 推测 ≥ 上一代编码榜/TB 数据"
   的组合，而不是"编码榜/TB 缺测所以搁置"。
4. **OR Top Weekly 流量信号独立成段**。OpenRouter Top Weekly 的周用量是 production
   data 的代理信号 — 流量大但 AA 上还没有 Index 的模型（典型是 `Hy4 preview`，
   以及每轮都要重新看的一批新模型；具体量级一律读本轮 `or-data.json` 的
   `weekly_tokens`，**不要引用上一轮的旧数字**）是"benchmark 滞后于生产采用"的典型
   案例，解读里要单独成段提及（与"仅 AA 实测"段区分开）。
5. **引用徽标 / 集合状态前先核对 render 输出**。`render-*.mjs` 每次会打印
   `frontier points` / `efficient` / `zone` 名单，解读里的 🔪 / ⚡ / 📊 说法必须与那
   三个名单一致。已踩过的坑：**AA 榜的 2D 前沿与 ⚡ 高效圈交集常常为空**（前沿只看
   能力×成本，⚡ 是 3D 差集），所以"某点在前沿上又套着 ⚡"这种话要先把两个名字
   都在两份名单里查到才能写；查不到就只写其中一个。同理编码榜 / 终端榜的 ⚡ 都是
   **榜单自带的 Duration / Test 更短**（不是 AA 的 Time per Task，不是 token 吞吐，也不是
   「单位成本产出」），拿 AA 的时间口径解释它们的 ⚡ 也会错位（两榜的任务集不同）：
   跑得快 ≠ 输出得多，话痨模型 tok/s 高但更慢。AA 自己的 ⚡ 则按 AA 的 Time per Task 判定。

不允许出现：把 `unbench-succ` 行说成"短板" / "候选但暂不可用"；把"新一代模型
缺测"说成"不推荐"；用编码榜/TB 的缺测率来评价 AA 上的高 Index 模型；**用编码榜 / TB 的
数字给 📌 太长不看 定档**（推荐理由的 X / Y 必须是 AA 的 Index 与 Cost per Task）；
**把 OpenCode Go 的"次/月"和 CommandCode 的"次/月"直接比大小**（两家 token 画像、月额度、
套餐结构都不同，OpenCode 那个还是估算值——跨站比会得到"哪家更划算"的假结论）。

## CommandCode tab 的口径与过滤规则

这一节是 ④ tab 的**行为契约**。前三 tab 的规则大多可以照搬，这里不行——CommandCode
的官方数据有它自己的坑，绕过下面任一条会得到一张好看但错的图。

### 口径（绘图数据必须来自官方值）
- **X 轴 = 官方 `Requests / month`**（log 轴，向右＝更能跑）。`requests_5h` / `requests_week`
  也直接引用官方值。**不要用自算 token 公式反推主数据**——自算会引入 1%~11% 的偏差
  （实测比官方低）。自算值只留作 `est_requests_month` / `est_vs_official` 做 QA。
- **只做 Max 10×**。OpenCode / Pro plan 的请求数、Max 20× 的额度是另一套口径。
- **Y 轴 = 智力，CC 优先 / AA 兜底**：`index = cc_intel ?? aa_index`。CommandCode 的
  Intelligence 表有分模型 60 个，AA 规范模型只有 35 个；单用 AA 会把一批有分的模型
  挡在图外。保留 `index_source` / `cc_intel` / `aa_index` / `aa_model` 字段备查。
  CC 保留 1 位小数，AA 取整。⚠️ `null >= -Infinity` 在 JS 里是 `true`（null→0），所以
  前沿扫描必须先 `if (r.index == null) continue`，否则待更新模型会被当成「智力 0 的新纪录」。
- **高性价比区在右上**（请求数越多越好，智力越高越好）：`index ≥ 35 && requests_month ≥ 100000`。

### 过滤（按顺序，缺一不可）
1. **AA 变体去重**：同一模型的多个 AA 变体只留一个（官方请求数最多的那个）。
2. **族内弱支配过滤**（`kept` / `superseded`）：同族里新一代 `index >=` 且
   `requests >=` 上一代、至少一项严格更高，就删旧代。**不能简单「每族只留最高版本」**——
   会误删真实的取舍档位（Pro / Mini / Lite / Flash）。典型保留点：MiniMax M2.5、
   Gemini 3.1 Flash Lite、Step 3.7 Flash、Kimi K2.5、GPT-5.6 Terra。
   `index == null` 的行两边都不参与（没有 Y 值可比），既不会被删也不会删别人。
3. **同请求数去重**：同族里官方月请求数**完全相同**（= 官方给了同一个价）的多代只留最新。
   典型：Claude Opus 4.6/4.7/4.8/5 全是 2,990 次/月（同价 $5/$25/$0.5），只留 Opus 5。
   这条**对 `index == null` 的模型也生效**（支配判定对它们无效），也是它与第 2 条
   必须分开写的原因。同代（`gen` 相同）撞数不动。
4. **peak / off-peak 孪生拆分**：Pro 页 Model 列内嵌 `· peak $in / $out 01–04 & 06–10 UTC,
   Mon–Fri`。Max 页价格表**只给 off-peak 价**。有 peak 价的模型拆成两行，
   `model` 分别加 ` (off-peak)` / ` (peak)` 后缀，`requests_*` 全部 **÷ ratio**
   （ratio = peak_in ÷ off_peak_in，官方只给 in/out 两个价，cache 按同一倍率缩放）。
   **用倍率缩放而不是重算成本**——重算会带进 token 口径误差，倍率缩放是精确的。
   peak 行标 `tier: 'peak'`，支配判定与同请求数去重都必须**按 tier 隔离**
   （off-peak 会把 peak 当成「被支配的旧代」删掉）。

### Pareto 与分层
- `MIN_STEP = 0.5`：相对上一个**真正入选**的阶梯点，智力至少提升 0.5。被跳过的点
  不能抬高 `best`（否则噪声会抬高后续所有门槛）。`gen-html` 侧表格的 🔪 扫描用同一常量
  `PLANS_MIN_STEP`，保证图上阶梯数与表格 🔪 数一致。
- **Contributor 不进主 Pareto**，单独用橙色虚线圈 + 两行标注（图上文字「数据换折扣」/
  「不计入阶梯」，图例 `数据换折扣 · 不计入阶梯`）。原因：Muse Spark 1.3 Contributor
  智力 48.1 / 682K 次·月，计入会吃掉除 Claude Opus 5.5 外的所有阶梯点，5 步压成 2 步。
  机制写「数据换折扣」**不要写「5 折」**——官方价格表显示 input ≈ 常规版 1/12.5、
  output ≈ 1/21.25、cache ≈ 1/75。
- **前沿大圆不做 de-clutter**：固定画在真实坐标上，R = 15。理由：原来沿径向推开 +
  细线连回真实坐标，peak 孪生点把 `DeepSeek V4.1 Flash (off-peak)` 顶开 34px，
  一条这么长的引线会让人误读成「点其实在那儿」——而斩杀线的语义就是真实位置。
  缩小图标和去掉 de-clutter**必须一起做**：Flash(487k,38) 与 DeepSeek(385k,39.5)
  圆心距 32.7px，R=18 时两圆相交，R=15 时（2R=30）刚好不相交。callout 标签另有
  自己的碰撞布局，会自动避开真实位置的大圆。

### 表格与 UI 约束
- 表格**只有 4 列**：`#` / `Model` / `智力` / `次/月`。
- 徽标：`🔪 高性价比`（在 Pareto 阶梯上）+ `🆕 待更新`（`index == null`）；
  Contributor 例外，给 `🔪 高性价比` + `贡献数据` 两个（它两轴都是全场最好，只因不计入
  主阶梯而拿不到 front；不标会让表里性价比最高的行看起来平平无奇）。
  **不要**加「⚡ 高效」（本表没有 Tokens/s，快慢无从谈起）、**不要**露出
  「映射存疑」/「合并了 …」/ 额度池·premium 任何字样。
- `index == null` 的模型**不丢弃**，智力列显示 `—` + `🆕 待更新`。
  同族按 `family` 分块、块间按族内最高智力排、块内先放有智力的再按代际倒序
  （新一代在上一代的上一行），同代 tiebreak 放 off-peak 在 peak 前。
- **tooltip 只留 2 行硬数据**（规格对齐 AA tab 的 `chart-gen`）：head + 智力/次月 +
  次周/次5h。不要加口径解释、自算对照、AA 兜底详情。

## OpenCode Go tab 的口径与过滤规则

这一节是 ⑤ tab 的**行为契约**。它 90% 照搬 CommandCode tab（同一套"右上角才是好"的语义、
同一套 4 列表格与 🔪 徽标），但下面四条是它自己的硬规则。

### 口径
- **只做基础 Go（$10/月）一档**。Go Plus（$40，约 3× 额度）/ Go Teams（$20/member）都是
  同一批模型的三套额度：混进一张图会让同一个模型出现三个 X 位置，而图上没有价格轴，
  读者只会看到"同名点散成三处"。单档也才谈得上"月费固定 → X 轴纯比能跑多少次"。
  选 Go 而不是 Plus/Teams：它是文档页的标题档、最便宜、且**每美元额度最高**
  （Plus = 3× 请求 / 4× 月费；Teams ≈ 1.08× 请求 / 2× 月费）。
- **X 轴 = 官方 `Est. requests / 5 hr` × 5（每月请求数）**。Console 页只印 5h 值，
  月 = 5×5h、周 = 2.5×5h（旧官方估算表的恒等式，逐模型精确成立）——解读里不要把周/月
  换算值说成"官网直接印的数"。单价与月额度取官方 models API。
  token 画像段落已下线，不再有自算 QA。
- **Y 轴 = AA Intelligence Index，单源**。OpenCode 自己不发布分数。另一条候选是 CommandCode
  的 Intelligence 列，但 2026-11 实测两家**已经不是同一把尺子**：Claude / GPT / Gemini 差 1~4 分，
  国产开放权重模型系统性差 +10~16 分（GLM-5.3 44.8 vs AA 32、MiMo V2.6 Pro 46.3 vs 30、
  Step 5 Preview 43.7 vs 29）。两根尺子混在一根 Y 轴上，点的高低就有一半来自尺子差异，
  所以这里**不混**——与 CC tab 的 "CC 优先 / AA 兜底" 是相反的取值顺序，改动时别照抄。
  AA 同一模型的多个 effort 变体（`Grok 4.7 (xhigh)/(high)/(low)`、`Claude Haiku 5.5 (max)/…`）
  取 **index 最高**的那个（与 AA tab 的 table 口径一致），`aa_model` 字段记录实际取到哪一行。
- **高性价比区在右上**：`index ≥ 27 && requests_month ≥ 100000`（阈值按本榜实际分布定：
  100K 次/月以上只有 3 个点，27 分就是这一簇里最低的那个）。

### 折叠 / 过滤（按顺序）
1. ~~上下文档位折叠~~（旧文档页已下线）：现在一行一个模型，无需折叠。
2. **peak / off-peak 孪生拆分**：仅 API `multipliers.when.any`（每日时段窗口）才拆——
   DeepSeek V4.1 Flash / V4 Pro（factor=2，01–04 & 06–10 UTC，周一至周五）拆成
   `(off-peak)` / `(peak)` 两个点，peak 的请求数按 factor 倍率缩放（倍率精确；
   用成本重算会带进误差）。`when.date.gte` 型（Gemini 4 Argon 2026-12-01 起全天 2×）
   只记 notes 不拆行。支配判定与同请求数去重必须**按 tier 隔离**。
3. **族内弱支配过滤**（`superseded`）：同族里新一代 `index >=` 且 `requests >=` 上一代、
   至少一项严格更高，就删旧代。**不能"每族只留最高版本"**——会误删真实的取舍档位。
   OpenCode 上典型：DeepSeek V4 Pro 被 V4.1 Flash 支配（同族、两轴都不差）。
4. **同请求数去重**（`same_req_dropped`）：同族同 tier 且官方估算月请求数**完全相同**
   （= 同一额度同一价）的多代只留最新。典型：MiMo-V2.6-Flash = MiMo-V2.5 = 150,400、
   MiMo-V2.6-Pro = MiMo-V2.5-Pro = 16,300、Muse Spark 1.3/1.2 Contributor = 226,600。
5. **免费档**（`Unlimited` 请求数 + `Free` 价格：Beam Free / Iceman Contributor Free）：
   `requests_month = null`，表格置顶 + 🆓 免费 + 「不限量」，不进图（log 轴画不了无限）。
6. **AA 无分的行不丢弃**：表格里 `—` + 🆕 待更新（当前 14 个，占全表一半），不上图。
   Contributor（数据换折扣档，当前 Muse Spark 1.3/1.2）在**没有智力分**时**不给** 🔪/贡献数据
   徽标——那是拿未证实的性价比做推荐；只标一个灰色「数据换折扣」（"这价是拿数据换的"是可核对的
   事实，与"值不值"无关）。CC tab 相反：它有官方实测值，所以照旧给 🔪+贡献数据。因此
   `renderCallTable` 的 `dealBadgeAlways` 只有 CC 表传 `true`。

### 表格 / tooltip
- 表格 4 列：`# / Model / 智力 / 次/月`，与 CC 表**共用同一个渲染函数** `renderCallTable()`
  （族分块、免费置顶、待更新排序、🔪 徽标全部一套代码）。改一边等于同时改两个 tab。
- tooltip 与 CC tab 同规格：head + 智力/次月 + 次周/次5h；peak 孪生只多一段时段窗口，
  靠模型名的「（peak）」后缀 + 灰色 `peak 时段` 标签区分。

## Thresholds (edit in the render script, never ask the user)

- render-vc.mjs: `ZONE_COST` / `ZONE_SCORE` (`5` / `80`): Vibe Code Bench 高性价比区
  （x 上限 $5、y 下限 80%）。x 轴按 `X_LADDER` 阶梯自适应（当前数据 $0.07~$57.92 →
  轴域 $0.05~$100），y 轴 `0 ~ max(100, 数据 max+2 扩到 5 的倍数)`。
- render-aa.mjs: `ZONE_COST` / `ZONE_INDEX` (`1` / `35`).
- render-go.mjs: `ZONE_REQ` / `ZONE_INDEX` (`100000` / `27`): OpenCode Go 高性价比区
  （x 下限 10 万次/月、y 下限 27 分，右上）。x 轴按 `X_LADDER` 阶梯自适应（当前数据
  735~216,670 → 轴域 500~500k），y 轴 `min(20, 数据 min 向下扩到 5 的倍数)` ~
  `ceil((数据 max+2)/5)*5`（当前 20~55，不设 60 分母，否则上半张图全空）。
- render-tb.mjs: `ZONE_COST` / `ZONE_SCORE` (`10` / `40`): Vals Terminal-Bench 4.0
  高性价比区（x 上限 $10、y 下限 40%）。x 轴同 render-vc 的 `X_LADDER` 阶梯自适应
  （当前数据 $0.21~$30.34 → 轴域 $0.1~$50），y 轴 `0 ~ max(70, 数据 max+2 扩到 5 的倍数)`
  （不设 100 下限，分数带上沿只有 65%，否则上半张图全空）。
- `LOGO_RING` (`#487265`): uniform green ring around all logo badges
  (frontier + dots + tooltip); effort colors are no longer used anywhere
  （换源后 TB 不再有 effort 变体，旧 `effortColor()` 已删除）。

## Completion criteria

- `fetch-vc.mjs` prints `rows: ~121 (cost 缺失 ~7 行…)` + `updated: MM/DD/YYYY`，多 harness 折叠
  只在有折叠时多打一行 `多 harness 折叠（保留最高分 run）: …`（当前 3 个模型）。
  行数或 cost 缺失数的量级变了 = Vals 页面改版（列顺序 / 表格容器），先看文件头
  的列约定再改。`updated` 太久没动说明这个榜也开始停更了，要在解读里说清楚。
- `fetch-aa.mjs` prints `trs: ~202, kept: ~32`（2026-11 改版后：7 列表格、Index>20 且
  cost>0；老模型那一栏多半是 `'--'`，所以 kept 比改版前少了一大截，属正常）。
  `kept` 骤降/骤升都要先看是不是页面又改版（脚本在列数 ≠ 7 时会直接抛错），
  再确认过滤条件没变。
- `fetch-tb.mjs` prints `rows: ~61 (cost 缺失 1 行…)` + `updated: MM/DD/YYYY`
  （Vals Terminal-Bench 4.0）。行数或 cost 缺失数的量级变了 = Vals 页面改版
  （列顺序 / 表格容器）— 重新检查文件头的列约定。
- `render-tb.mjs` prints frontier points + `labeled:` + `efficient:`；前沿数按 model 计
  一行一个模型，`efficient:` 里的名字必须能在 TB 表格里找到对应行（三态一致）。
- `fetch-go.mjs` prints `Console 页: 32 个模型`、`models API: 32 个模型`、
  `智力（AA 单源）: 有分 ~16 / 待更新 ~16`、`peak 孪生: 2 个`。
  任何一条量级变了 = OpenCode Console 页或 models API 改版，先看脚本头注释里的数据源约定。
- `render-go.mjs` prints x/y domain + 高性价比区个数 + pareto 名单 + `labeled:` + 待更新/免费名单；
  pareto 名单必须与 `gen-html.mjs` 打印的 `go frontier:` 一致（两边同一个 `MIN_STEP=0.5`），
  `labeled:` 里的「未放下 …」说明气泡位不够（圆点仍在，hover 可看名字）。
- `render-vc.mjs` prints frontier points + `labeled:` + `efficient:`；前沿数必须等于
  Pareto-optimal 行数（按 model 计，一行一个模型），`labeled:` 里若出现「未放下 …」说明
  气泡位置不够，圆点仍在（hover 可看名字），可考虑再加大 padT 或补候选位。
- Hovering any dot in `index.html` shows a card with that dot's lab logo,
  model name, score, cost and tokens/duration（编码 / 终端两张 Vals 榜都没有 harness、
  agent、effort、tok/s；终端榜的 tooltip 标题写 Terminal-Bench 4.0 Score）。
  AA 榜的 tooltip 两行硬数据 = Index + Cost/Task 与 Time/Task（分钟）+ 首 token 秒数。
  CommandCode / OpenCode Go 两张订阅榜只有两行硬数据（智力 + 官方次/月 + 次周/次5h），
  没有 tokens/s —— 它们的 X 轴是"能跑多少次"，快慢无从谈起。
- `logos/` (27 files, ~464KB, designarena `model-logos`, resized to 128px)
  ships with the skill and is inlined at build time; nothing is copied to
  the output dir. Logo mapping lives in `logoFileOf()` in
  `scripts/logos.mjs` (case-insensitive prefix match on a **separator-normalized**
  name, e.g. `gpt-` → OpenAI logo); add a line there when new labs appear.
  归一化不是洁癖：三家写同一个模型的方式不同（`MiMo V2.6 Flash` in CommandCode vs
  `MiMo-V2.6` in AA；`Tencent Hy3` vs `hy3`），不先把空格/下划线压成 `-` 就会表现为
  「同一模型在 A tab 有 logo、在 B tab 退化成小圆点」。改完跑一遍 14 条老前缀的回归。
  `logos/` 里没有对应文件的（LongCat / Fugu / Jev）会回退到字母 logo。
