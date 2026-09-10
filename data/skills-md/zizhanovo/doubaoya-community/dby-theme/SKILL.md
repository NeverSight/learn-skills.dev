---
name: dby-theme
description: >-
  公众号排版主题工作室 · 按你的口语改公众号文章的**默认排版样式**（配色 / 标题 / 引用 / 图注），本地即时预览，
  最后同时落到两处：存回服务端 + 存成本机 theme 文件。走 doubaoya.com，鉴权用你自己的 DOUBAOYA_API_KEY。
  触发方式：/dby-theme、改公众号排版、定制主题样式、换公众号配色、调排版主题、改默认排版。
  Trigger words: customize WeChat article theme, change layout / palette / heading style.
version: 1.4.4
changelog: 新增触发层盲测用例 evals/triggers.jsonl（10 正 / 8 负）；包行为零变化
  另主题契约指针指本包校验器 scripts/validate-theme.mjs
compatibility: >-
  需要 Node ≥ 18（校验脚本用全局 fetch）与 curl；正文示例用 jq 拼 JSON body，
  不想装 jq 也可以手写 JSON。不装任何 npm 包。
  需要环境变量 DOUBAOYA_API_KEY（形如 dyh_…，在 doubaoya.com 密钥中心生成）；需要能对 https://doubaoya.com 发 HTTPS 请求。
---

# 公众号排版主题工作室（都爆鸭）

排版是一份声明式的 **`themeJson`**（配色 palette + 每个标签的 inline-style 模板），渲染器按它把
Markdown 确定性地渲成公众号内联样式 HTML。按描述生成 / 修改合法的 themeJson，
本地自检 + 预览，再**存回服务端设为默认**；发文钉了 `--theme` / `config.mdTheme` 时再落一份本机文件。
渲染 / 存主题都**免费不扣点**。

---

## ⚠️ 四条硬红线（先读，全程守住）

### 红线 1 · 微信兼容:标题装饰只能挂在有文字的元素自身

公众号编辑器会 **strip 掉没有文字、纯靠 inline-block 宽高 + background 撑色块的空 `<section>`/`<span>`**。
标题引导条 / 强调竖条 / 下划线**必须作为 inline style 直接写在标题元素自身**，**绝不**用独立的空装饰块。

- ✅ 对:`elements.h2.style` 里直接写 `border-left:4px solid {{accent}};border-bottom:1px solid {{border}};padding:0 0 8px 11px;`
- ❌ 错:用 `wrapBefore` 注入一个空的 `<section style='width:32px;height:4px;background:…'>` 当色条（无文字 → 被 strip）。

### 红线 2 · 微信兼容:别给整篇套 `decorations.articleWrap` 外框

`decorations.articleWrap` 包整篇正文的浅底圆角卡片在公众号里会变成一道**突兀的边框**。
`articleWrap.before` / `after` 留空字符串；「呼吸感」用段间距（`margin` / `line-height`）和局部卡片（如 blockquote 圆角卡）实现。

### 红线 3 · 安全:themeJson 会内联进公众号草稿,服务端会拒收不合法主题

服务端 `POST`/`PUT`/`render` 都会 `validateTheme`，不过直接 **400**。生成后先跑
[`scripts/validate-theme.mjs`](./scripts/validate-theme.mjs) 自检——具体校验规则（顶层键、
palette/page 必填字段、style 禁写清单、体积上限）以它为准，不在这里另存一份会漂移的清单。

微信编辑器官方规范另有八条「不拒但走样」的写法（`position`、`text-align:start`、固定像素宽、自定义字体栈、文字底下铺渐变…），
清单与可读性基线见 `references/theme-schema.md` 末尾；校验器对其中四条打 warning。

### 红线 4 · 数据安全:动手改前必须落盘备份,没有备份不改

改主题是**就地覆写**（`PUT` / `POST + isDefault:true`），服务端不保留历史版本，改坏了没有第二处能找回。
第 1 步的 GET 命令已经把落盘备份写进命令本身——**照抄不删**；备份文件路径记下来，改坏了照
`references/deploy-scope.md`「回滚」一节把它 PUT 回去。

---

## 契约:服务端主题 CRUD + 渲染（以 doubaoya.com 主仓 render-routes.ts 为准）

⚠️ 先读 `dby-gateway/references/protocol.md` 再发请求（鉴权、密钥怎么拿、
信封与报错码全在那一份）。本 skill 自己的六条主题路由（`GET/POST /api/wechat/theme`、
`GET /api/wechat/themes`、`POST /api/wechat/render`、`PUT`/`DELETE /api/wechat/theme/:id`）
的请求体与返回 → 读 `references/crud.md`，不需要就别读。

```bash
export DOUBAOYA_API_KEY="dyh_你的密钥"
BASE="${DOUBAOYA_BASE_URL:-https://doubaoya.com}"
AUTH="Authorization: Bearer $DOUBAOYA_API_KEY"
```

**render 的主题解析优先级** `themeJson`（传了就用这份）> `themeId` >
我的默认主题 > 兜底 `benya-clean`，所以**预览编辑中的主题就传 `themeJson`**；
**一人一默认**，`isDefault:true` 时服务端在事务里把我其他主题的 `isDefault` 置反。

## 闭环步骤

### 1. 读起点主题并落盘备份（红线 4，照抄不删）

```bash
# a) 读我当前的默认主题(有就在它上面改)并强制落盘备份——主题体在 data.theme.themeJson
BACKUP="/tmp/dby-theme-backup-$(date +%s).json"
curl -s -H "$AUTH" "$BASE/api/wechat/theme" | tee "$BACKUP"
echo "已备份到 $BACKUP —— 改坏了见 references/deploy-scope.md「回滚」一节"

# b) 或列出内置主题,挑一个复制起步(推荐 benya-clean——已按红线 1 / 2 改造过)
curl -s -H "$AUTH" "$BASE/api/wechat/themes"
```

> 本 skill 也自带一个 WeChat-safe 起手模板 [`themes/theme.example.json`](./themes/theme.example.json)（暖橘编辑风,复制改配色即可）。

### 2. 按用户口语描述改 themeJson

把「换成暖橘色 / 标题要竖条 / 引用做成卡片 / 字再大一点 / 排版长得像某某号」翻译成合法 themeJson。
字段全貌见 `references/theme-schema.md`;守住上面四条红线。改配色最省事:**只动 `palette` 八个键**。

### 3. 本地先自检

把生成的主题写成本地文件,过本 skill 自带的零依赖校验器:

```bash
node scripts/validate-theme.mjs /tmp/my-theme.json   # 有硬错误按提示改;exit 0 = 合法
```

### 4. 预览（改一版看一版）

**API 渲染 → 存本地 .html 打开**:

```bash
# 用编辑中的 themeJson 渲染样例文章,拿回 HTML 存本地打开肉眼看
curl -s -H "$AUTH" -H 'Content-Type: application/json' \
  -d "$(jq -n --arg md "$(cat sample.md)" --slurpfile t /tmp/my-theme.json \
        '{markdown:$md, title:"预览", themeJson:$t[0]}')" \
  "$BASE/api/wechat/render" | jq -r '.data.html' > /tmp/preview.html
open /tmp/preview.html    # macOS;别的平台用浏览器打开
```

> `sample.md` 别带 `#` 一级标题：`title` 会被插成 h1，正文再有就显示两个大标题。
> render 返回的 HTML 与最终存进草稿的正文**逐字一致**。`data.warnings` 若有(如未知 `{{token}}`)一并看一眼。

→ 本机已装 `dby-publish` 且想在本机「改文件重跑即换肤」地预览，读 `references/live-preview.md`，
不需要就别读。改 themeJson 本身以上面 API 渲染那条路为准。

### 5. ⚠️ 落地生效范围（两条渲染路的主题源）

→ 主题调好、要存回去时读 `references/deploy-scope.md`——它回答「存了之后哪条路会变、
哪条不会」，并给出存回服务端 / 落本机文件 / 改坏了回滚的完整命令。

**存回服务端设为默认是主路**（`POST`/`PUT` + `isDefault:true`）：doubaoya.com 网页排版
工作室、`POST /api/wechat/render`、以及**未钉本机主题的 `dby-publish` 发文**都读它。
**仍需落一份本机 theme 文件**的只有三种情形：发文时钉着 `--theme` / `config.mdTheme`、
离线或拉取失败要兜底、用的是不带自动拉取的旧版 pipeline。
落完向用户汇报时**如实说清各自的生效范围，别混着说**。

## themeJson 结构（速查）

→ 真要动手写 / 改 themeJson 的字段时读 `references/theme-schema.md`（top-level 键、
`elements` 支持的标签、`{{token}}` 插值、`li.marker` / `img.figureStyle` / `hr.html` 这些位置），
不需要就别读。**只换配色的话改 `palette` 八个键就够**，其余用 `{{token}}` 自动跟随。

> 主题契约以本包 `scripts/validate-theme.mjs` 为准（跑它，别照文档记）；
> 本 skill 的 `references/theme-schema.md` + `themes/theme.example.json` 足够独立完成一次改主题。

---

## 下一步（先看用户要的终态是什么）

**别默认往下推**——用户要的终态停在哪一档，就在哪一档收手：

| 用户要的终态 | 到这一步够不够 | 下一步 |
|---|---|---|
| 只要把默认排版改成自己想要的样子 | ✅ 够了，**到这里就结束**（以后每次渲染自动生效） | — |
| 还要**用这套主题排版某篇正文、存进自己公众号草稿箱** | 不够 | `dby-publish`（存回服务端的默认排版它会自动拉；本机主题文件用 `--theme` 指过去） |
| 已有排好版的图文，只想让它进草稿箱 | 不够 | `dby-publish` |
| 正文还没写 | 不够 | `dby-api`（拉同主题爆文样本再写正文，走 api.gzh.hotArticle） |
| 正文没过违禁词 | 不够 | `dby-banned-words`（三平台一次比对，出安全改写版） |
| 说不清要到哪一步 | — | `dby`（公众号飞轮的逐跳导航） |
