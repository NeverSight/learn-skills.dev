---
name: dby-publish
description: >-
  公众号图文流水线 · 终态是**排版好的公众号 HTML**或**文章进自己公众号草稿箱**时用它（只存草稿、绝不群发）。
  输入是**已写好的** Markdown/HTML，本流水线不代写正文，只做之后的确定性运维：渲染 → 图片预上传 → 封面 → 存草稿。
  ⚠️ 它会**写进用户自己的公众号后台**，用户只要成稿时别自作主张跑它。存草稿需绑号 + DOUBAOYA_API_KEY；
  只做本地渲染 / 换主题时不需要。
  Trigger words: 正文写好了怎么发 / 要排版好的公众号 HTML / 接着排版发草稿 / 写公众号 / 转公众号排版 /
  推公众号草稿 / 重新推草稿 / 带封面发布到草稿箱 / 把文章存进公众号草稿箱 / 公众号图文流水线 / dby-publish /
  存公众号草稿 / 公众号草稿箱 / 代发公众号草稿箱 / addDraft / draft/add / 图文推进公众号 / 稿子发到公众号后台。
version: 5.1.0
changelog: "封面 / 配图那一步改回指向 dby-image —— 服务端生图能力 2026-09 已恢复（换供应商 + gpt-image-2.5），此前那句「出图能力当前暂时下架」已成假信息；本包仍不出图，只消费落盘的本地文件。上一版（5.0.0）内容：BREAKING：删除 scripts/publish_draft.py（改用 `dby wechat publish`，默认停在确认态）；pipeline/preprocess-and-publish/account-verify 的 HTTP 全部改走 dby-api 共享请求层（lib/locate-dby.mjs 定位，缺 dby-api 退出码 3）；新增 scripts/dby.mjs 引导壳；文档路径改写 `$SKILL_DIR`；compatibility 不再需要 Python"
compatibility: >-
  需要 Node ≥ 18（脚本用全局 fetch 与 AbortSignal.timeout），不装任何 npm 包；
  接口调用经由 `dby-api` 包的共享 CLI（`scripts/lib/locate-dby.mjs` 定位），需与 dby-api 一起安装。
  存草稿这条路还需要环境变量 DOUBAOYA_API_KEY（形如 dyh_…，在 doubaoya.com 密钥中心生成）；需要能对 https://doubaoya.com 发 HTTPS 请求，并且用户已在 doubaoya.com 绑定自己的公众号；
  只做本地排版渲染 / 换主题时不需要密钥也不需要绑号。
  ⚠️ 正文里的本地图片若超过 1MB 需要压缩，靠可选的 sharp，缺它则回退 macOS 专有的 sips——
  所以在没装 sharp 的 Linux / 容器上，超过 1MB 的本地图会直接失败。
---

# 公众号图文流水线（都爆鸭）

把一篇**已经写好的**图文走一串确定性步骤，存进用户自己公众号的**草稿箱**，返回 `mediaId`。

正文归 `dby-write`（或用户自带）；取数、爆款样本、封面套路归 `dby-api`；合规检测归 `dby-banned-words`。
🔴 **终态纪律**：用户只要成稿就**不跑本包**——本包会写进他自己的公众号后台，是真实副作用。
终态未明先问一句，别默认往下推。

---

## 只想存草稿、不要排版

正文**已是公众号风格 HTML、无本地图也无本地封面**时直接打 CLI，不必走 `pipeline.mjs`。
`$SKILL_DIR` = 本包目录（宿主加载本 SKILL.md 时给出的目录）：

```bash
node "$SKILL_DIR/scripts/dby.mjs" wechat publish --appid <authorizerAppid> --title "标题" --html article.html --confirm
```

`--confirm` 前必须已有用户明确要发这一条的确认（见下面「防误发红线」）；不带 `--confirm`
会停在 confirmation_required，退出码 6，什么都不发生。参数细节见 `node "$SKILL_DIR/scripts/dby.mjs" wechat publish --help`。
带本地图 / 本地封面时改用 `scripts/preprocess-and-publish.mjs`，见 `references/draft-only.md`。

---

## 流程声明：`pipeline.json`

10 步 SOP 与全部硬规则声明在 [`pipeline.json`](./pipeline.json)（`steps[]` + `hardRules[]`）——它是**人读的约定文档**，
`pipeline.mjs` 不读取它，改流程要两边手工同步。**「封面 / 配图」这一步由 agent 执行**（本包不出图，见下节），其余步骤 `pipeline.mjs` 机械跑完。
本文只用步骤名不用序号；`pipeline.mjs` 日志里的「步骤 N」是脚本自己的机械步序，与 SOP 编号不对应。

→ 想逐步核对这 10 步分别做什么时读 `references/sop.md`，不需要就别读。

---

## 调用都爆鸭：本 Skill 用到的两条能力

只点名能力与详情端点；入参每次调用前现拉。

| operationKey | 详情端点 | 用在第几步 |
|---|---|---|
| `skill.wechat.render` ⚠️专用 | `GET /api/skills/wechat-render` | 「md→HTML」（服务端排版那条路） |
| `skill.wechat.draftPublish` ⚠️专用 | `GET /api/skills/wechat-draft-publish` | 「保存草稿」 |

生封面 / 生配图**不在本包**，出图能力当前暂时下架；未来是否恢复需重新评估，当前不承诺恢复时间。
本包只消费**用户自备或 agent 用自己工具生成**的本地文件，不调用已下架能力或旧包。

请求由 `scripts/pipeline.mjs`（及它调用的 `preprocess-and-publish.mjs`）代发；
绕开脚本自己拼请求时才读 `dby-gateway/references/protocol.md`（鉴权、密钥怎么拿、
先拉规格再拼参数、`execution.target`、信封格式）。
🔴 **报错码是例外，走脚本一样要读**：脚本原样抛错零解读，撞上就读该文件第 6 条
（429 按 IP 分桶，换 key、开新会话都没用，退避≤3 次且别加并发）。
🔴 两条**专用路由**的调用地址只在 `target` 里，从详情端点**推不出来**。

> **存草稿花钱、服务端排版渲染不花钱**；现价从详情响应现拉现说，花钱的那步动手前先问用户。

→ 用户要的东西**超出上面这两条**时，读 `dby-gateway/references/capability-index.md` 选路、
读 `routing-pitfalls.md` 看已知的坑；正常流程里这两份都不必读。

---

## 写正文之前

- 🔴 **正文不写标题，标题只走 `--title`**——公众号总是拿草稿 `title` 渲大标题，正文里再写就显示两次；
  `--html` 直发路径**原样**发出、没有去重，开头别放 `<h1>`。`--md` 路径兜了什么底见 `references/rendering.md`。
- 正文**不是走 `dby-write` 写的** → 先拉写作规范，读 `references/writing-spec.md`
  （`dby-write` 第 1 步已经拉过这一份，别再拉一次）。
- **计费只在存草稿成功时发生**，失败自动退回；具体扣多少以详情端点的实时点数字段为准，
  别照文档里的数字替用户算钱。`402 INSUFFICIENT_CREDITS` 时提示用户到账户页查看余额与获取方式（点数只赠不卖），不要重试。
- **不写 `--theme` 就是用你在排版工作室保存的默认排版**；md→HTML 只走平台
  `POST /api/wechat/render`（免费），**失败一律中止、绝不回退本机渲染器**。
  套哪套排版 / 老稿子重跑为什么长得不一样 / `> [!NOTE]` 提示块 → 读 `references/rendering.md`。

---

## 封面与配图（可选，本包不出图）

本包**不出图**。需要新图时交给 `dby-image`（2026-09 随服务端生图能力恢复而重建）；
图片也可以来自**用户自备**或**你自己 agent 的生图工具**：
拿到**本地文件路径**后接回流水线——
封面走 `--cover <路径>`；配图以 `<img src=本地路径>` 手工判断放进 Markdown 源对应 h2 小节末尾，
入源后重跑渲染，配图才会获得主题图样式。上传与排布仍归本包（流水线原样保留每个 `<img src>`
并预上传本地图）。用户已说「推」且**没提封面 / 配图**时不主动张罗：只提示一次
「不传封面就走兜底封面」，然后直接跑。

---

## CLI 用法

🔴 **防误发红线**（无论走哪个入口都成立）：**只存草稿、绝不群发**——没有任何群发路径，流水线**拒绝**任何
`--mass-send`/`--broadcast`/群发 参数；**需先绑号**（先在 doubaoya.com 把公众号授权绑定，本技能替不了你绑）；
**用户只要成稿时别自作主张跑它**。存完请用户去后台亲眼确认，群发的手永远在用户自己。

```bash
export DOUBAOYA_API_KEY="dyh_…"   # 或放 ~/.doubaoya/key、Keychain（account-verify 会找）

node scripts/pipeline.mjs --md article.md --title "标题"                 # 渲染 → 传图 → 存草稿
node scripts/pipeline.mjs --md a.md --title "标题" --render-only         # 只渲染，拿在线预览链接
node scripts/pipeline.mjs --md a.md --title "标题" --dry-run             # 发布前彩排，什么都不发
```

本机有多条 key 对应不同账号时，账号校验会停下要 `--account <账号>`，按报错列出的账号补上重跑。

正文来自**稿件面**（用户在网页审稿页审过的稿）时带 `--draft <稿件 id>`（可选 `--draft-version <n>`，
省略 = 最新版）——存草稿箱成功后服务端会把稿件自动关联到这条发布记录；不带就是普通发布。
带了但那条稿件不属于你 → 422 `VALIDATION_ERROR`，发布不执行、不扣点。

🔴 **跑完只认最终回报里的 `mediaId`**——它是「已存入草稿箱」的唯一凭据，没有它就不当已存入。
存草稿失败 / 中途 Ctrl-C / 不确定草稿箱里有没有 → 读 `references/recovery.md`（重跑不幂等，会多存一份）。

→ 要指定账号 / 公众号 / 本地封面 / 摘要，或用 `--html`、`--theme` 的完整写法时读
`references/cli.md`，不需要就别读。

---

## 冷门分支：需要时才读，不需要就别读

| 用户在说 / 你要干的事 | 读哪份 |
|---|---|
| **只看排版**（本机出稿看效果，不发） | 只读 `references/rendering.md`，其余都不读 |
| 哪个脚本干哪件事、想不走 `pipeline.mjs` 自己组合 | `references/modules.md` |
| **第一次用本包**（还没有 `config.json` / 身份卡） | `references/setup.md`（`config.json` 属于你个人、别提交） |
| **把某个公众号的排版复刻成 `theme.json`** | `references/clone-theme.md`（契约、校验器、现成主题怎么挑都在里面） |

---

## 前置条件

统一前置 **Node ≥ 18**，零外部依赖。本机渲染免密、无在线链接；平台渲染（`--render-only`）要密钥、有在线链接、不要绑号；
**`--dry-run` 与存草稿**要密钥且要绑号。
→ 逐层明细读 `references/prerequisites.md`，不需要就别读。

---

## 下一步（草稿存好之后）

草稿进箱即终点。还想往下走时：

| 用户接着想要什么 | 下一步 |
|---|---|
| 攒几天数据后看这个号的发文表现 / 做体检 | `dby-api`（打账号诊断能力 `skill.wechat.accountAnalyzer`） |
| 盯自己或竞品的发文节奏 | `dby-api`（打公众号发文列表端点） |
| 把已发布的文章拉正文归档 | `dby-api` |
| 用复盘信号挖下一轮选题 | `dby-api`（挖选题 / 追热点，也从这儿拉样本开写） |
| 说不清要到哪一步 | `dby`（公众号飞轮的逐跳导航） |

---

## 更新本技能

`npx skills update dby-publish`（全局安装的加 `-g`）。变更历史见 [`README.md`](./README.md)。
