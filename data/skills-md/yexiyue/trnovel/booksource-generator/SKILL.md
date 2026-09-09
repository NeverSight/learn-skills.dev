---
name: booksource-generator
description: >-
  从一个小说网站 URL 生成 TRNovel 书源(trnovel-booksource/v2 JSON)。当用户给出小说/阅读类网站并希望接入
  TRNovel、做书源、适配书源、逆向某站点目录/正文时使用——例如「给这个站做个书源 https://…」「generate a
  book source for X」「把这个小说网站接入 trnovel」「帮我解析这个站的章节/搜索」,即便没明说「书源」二字。
  本 skill 会探测真实站点、逆向 search/浏览/书详情/目录(含分卷)/正文 的 CSS/JSONPath 选择器,处理字符集与
  Cloudflare 反爬,写出 JSON,并用 `trn doctor` 全流程校验、按 ✓/✗ 迭代到通过。
---

# 书源生成器(TRNovel v2)

## 这是什么 · 书源的本质

书源是一份**声明式 JSON**,教 TRNovel 如何读一个小说站:去哪搜索、怎么浏览分类、从书详情页抽取书名/作者/封面、列出目录(章节 + 分卷)、抓取每章正文。你的任务:**给定站点 URL,逆向它的 HTML,产出一份能通过 `trn doctor` 的 `trnovel-booksource/v2` JSON。**

格式是**结构化**的(没有紧凑字符串 DSL):每个字段是一条「规则」——一次 CSS/JSONPath/正则抽取,或组合子(firstOf/concat/literal/template)。

- 精确字段与规则语法 → 读 `references/book-source.schema.json`
- 一份完整可运行的真实示例 → 读 `references/example-bilixs.v2.json`(MacCMS 系静态站,含 `fetch` 动态入口)
- 另一份真实示例(番茄小说网页版,SPA + 签名接口 + 渲染型取页) → 读 `references/example-fanqie.v2.json`
- 逐能力的探站/逆向战术、curl 探测配方、字符集与反爬细节 → 读 `references/reverse-engineering.md`

边做边查这三个文件,不要凭记忆硬编规则语法。

## 核心循环(照做)

1. **探站**:抓取代表性页面——首页、一本书的**详情页**、它的**目录页**、一个**搜索结果页**、一个**分类浏览页**。用 curl/WebFetch,保存 HTML,观察结构。
2. **逐能力逆向选择器**:search / explore / bookInfo / toc / content(见下「按能力逆向」)。
3. **判定字符集 + 反爬**(见下两节)。
4. **拼装 JSON**(`schema: "trnovel-booksource/v2"`,带 `samples` 黄金样例)。
5. **校验:`trn doctor <文件>`** → 看逐项 ✓/✗ → 只修那个 ✗ 对应的规则 → 重跑,直到全绿(或只剩已知难项,如被挑战的搜索)。
6. **导入:`trn import <文件>`** —— 把验证通过的书源写入 `~/.novel`,使其在网络小说里**立即可用**(闭环的最后一步,见下「导入」)。
7. 告知用户:doctor 各项结果 + 已导入,可在 `trn -n` 选用。

**绝不把未经 doctor 校验的书源交付,也别忘了最后一步导入。** 校验循环把「猜的选择器」变成「验证过的选择器」;导入让它真正能用。

## 用 doctor 做反馈引擎

在仓库根目录:

```bash
cargo run -- doctor /path/to/<站点>.v2.json
# 或已安装的二进制:trn doctor <文件>
```

它跑完整流程并对 **配置 / 浏览 / 书详情 / 目录 / 正文 / 搜索** 打 ✓/✗/○。读每个 ✗ 的 detail,**一次只修一条规则**,再跑。无样例时它会用浏览结果探一本书来测读取链路,所以**先把 `explore` 或 `samples` 做对**能解锁后面几项。

迭代提速:可先 `cargo build` 一次,然后反复跑 `./target/debug/trn doctor <文件>`(见 `scripts/validate.sh`)。

## 导入(闭环最后一步)

doctor 验证通过后,把书源装进 app 让它真正可用:

```bash
cargo run -- import /path/to/<站点>.v2.json
# 或已安装的二进制:trn import <文件>   (也支持 URL:trn import https://…/source.json)
```

它把书源写入 `~/.novel/book_sources.json`(按 `url`+`name` 去重,同名会被新的覆盖,便于反复迭代同一书源),之后在网络小说(`trn -n`)的书源列表里即可选用。**这是「AI 生成 → 验证 → 可用」闭环的收尾**:不导入,生成的书源只是个文件,用户用不上。

## 按能力逆向(关键启发式)

每条规则的 `select` 是 **self-or-descendant** 语义;HTML 默认 `via: "css"`。下面是从真实站点(MXCMS/MacCMS 系等)总结的高命中套路,细节见 `references/reverse-engineering.md`。

- **bookInfo(书详情)**:**先找 `og:` meta**——`<meta property="og:novel:book_name">`、`og:novel:author`、`og:novel:read_url`(常是 tocUrl)、`og:image`(封面)、`og:description`。用 `{"via":"css","select":"[property=\"og:novel:book_name\"]","extract":{"attr":"content"}}`。比靠页面可见元素稳得多。**`wordCount`**(字数)通常不在 `og:` meta 里,需从页面可见元素提取(如 `span.tag-link` 含 "878.7 万字");MacCMS 系站点的字数常在书详情页的辅助信息区。
- **toc(目录 + 分卷)**:目录页里**卷标题**(如 `第一卷`)和**章节链接**通常是兄弟节点。用一个 `list` 选择器**同时选中两者并保持文档顺序**(如 `.box > h2.module-title, .box a.module-row-text`);再用 `isVolume` 规则判定是否卷(对卷节点非空、对章节为空,例如选 `h2`);`name`/`url` 用 `firstOf` 兼容两种节点。引擎据 `isVolume` 切分「卷→章」。**常见坑**:目录开头常有 N 条「最新章节」预览(倒序、与正文区重复),用兄弟选择器(如 `#list dl dt:has(a[href*="txt_"]) ~ dd a`)只取「正文」标记之后的章节,避免重复/倒序。
- **content(正文)**:找正文容器(`.article-content`/`#content`/`.read-content` 等),`extract: "html"` 会把标签转成换行后清理;分页正文用 `nextPage` + `maxPages`。**若正文夹大量私有区/豆腐字符(`U+E000`–`U+F8FF`,显示为豆腐 □)→ 是字体反爬,见下「字体反爬」。**
- **search(搜索)**:从首页 `<form>` 找 action 与 input name(如 `searchkey`/`wd`)。`request.url` 用模板 `{{base}}/search.html?searchkey={{key}}`;`list` 选结果条目容器(**注意区分真正的结果区与推荐位**——它们可能用不同 class);`item` 里**必须含 `bookUrl`**(指向书详情)。POST 搜索用 `method:"POST"` + `body` 模板。
- **explore(浏览)**:两阶段结构——`entries` 生成可选入口,`page` 用选中入口的变量取书。
  - **`entries`**:入口源数组,两种变体:
    - `static`:硬编码入口列表 `[{title, vars?}]`。`vars` 是取页变量(字面量),与 `base`/`page`/`pageSize` 合并后驱动 `page`。
    - `fetch`:从远端页面动态抓取入口 `{request, list, item}`。`request` 取入口数据页,`list` 选数组,`item` 提取 `title`(Rule) + `vars`(`{name: Rule}`)。可选 `forEach` 按多组变量重复请求。
    - **优先用 `fetch` 动态提取分类入口**（从首页导航/API 获取），而非 `static` 硬编码。这样站点新增分类时不用手动更新书源。仅当站点无可用分类入口时才用 `static`。
    - 两种可混用,按声明顺序合并。
  - **`page`**:共享列表页规格 `{request, list, item}`——`request.url` 用入口变量 + `{{page}}` 模板生成取页 URL;`list`/`item` 同 search。
  - **`fetch` 入口的坑**:vars 里的 Rule 对「当前数据项」求值。`dom_query` 解析 HTML 片段时会包 `<html><body>`,**省略 `select` 时 `:root` 指向 `<html>` 而非目标元素**。提取 href 等属性时**必须显式写 `select`**(如 `"select": "a"`)匹配目标元素自身。
  - **过滤非目标入口**:`list` 选择器应尽量精确(如 `.nav-menu-items a[href*='lastupdate']` 而非 `a`),避免匹配到无关链接导致 `vars` 提取失败、拼出错误 URL。
  - SPA 书库站(分类列表由签名接口拉、无静态分类页):在 `page.request` 上加 `render:true` + `interceptApi`,`list`/`item` 改 `via:"json"` 对齐被拦截 API。取页**单页**:`{{page}}` 映射 URL(**从 1 起**、由 URL 模板对齐站点 API 页码基数,引擎不内置偏移),交互翻页由阅读器递增 `page` 驱动(列表不加 `nextPage`)。详见 references/reverse-engineering.md「渲染 explore」。

`{{base}}` = 站点根、`{{key}}` = 搜索词、`{{page}}`/`{{pageSize}}` = 分页。相对 URL 引擎会自动补全,**抽取 href 时保留相对路径即可**。

## 字符集

老站常是 GBK。若抓下的中文乱码,设 `http.charset: "gbk"`(或 `gb18030`)。不确定就用默认 `auto`(UTF-8 失败回退 GBK),doctor 正文/书名出现乱码即调。

## 反爬(Cloudflare 等)

若某端点(常是**搜索**)返回挑战页,doctor 会报「被反爬挑战拦截,需浏览器辅助或改用浏览」。处理顺序:

1. **先找未被挑战的等价入口**:很多站只锁伪静态搜索路径,底层路由(如 `/index.php/vod/search.html?...`)或 JSON 接口未被挡。换上去就不用反爬。**但要核实它真在按关键词过滤**(换两个词对比结果),别被「不管查啥都返回同一榜单」的假入口骗了。
2. **绕不开就标注取页模式**:站点整体能读、仅搜索被挑战 → `http.fetcher: "auto"`(默认,平时 reqwest、撞挑战才用系统浏览器解 `cf_clearance`);整站首请求即被挑战 / 正文靠 JS 渲染 → `"browser"`;想永不开浏览器 → `"reqwest"`(撞挑战即降级)。
3. **判「不可行」前先试低成本绕过**(很多站的拦截是浅的):
   - 章节页返回「加载中…」的 JS 跳转桩(HTTP 200,**不是** CF 挑战,`fetcher:browser` 救不了)?试**在 URL 后加个无害 query**(如 `?nocache=1`,用 `clean.append`)常能直接绕到真正文。
   - 正文/搜索是 **token 门控的 JSON 接口**?把发 token 的辅助端点(如 `/user/hm.html`)加进 `http.warmup` 拿 cookie,再用 `via:"json"` 解接口(cookie_store 会跨请求保留)。
4. **接受降级**:阅读链路通常开放,搜索被挑战不影响读书。doctor 把搜索标 ✗ 但 detail 精确,即视为「需浏览器/改用浏览」,不是规则 bug。

**架构边界**:若**整页正文由站点自身 JS 异步渲染 / 加密接口动态拉取**(没有任何静态路径返回正文文本),当前 reqwest + cookie 烤箱**拿不到**,`fetcher:browser` 也只解 CF 挑战、不跑站点内容 JS。此时如实告知用户「该站正文需能执行页面 JS 的渲染型取页(暂不支持)」,把能做的(浏览/书详情/目录)做好并保留正文选择器兜底。

详见 `references/reverse-engineering.md` 的「反爬」一节。

## 字体反爬(自定义字体 + PUA 占位)

有些站(典型:番茄小说网页版)正文里夹大量**私有区字符**(`U+E000–U+F8FF`,多显示为豆腐方块 □),靠页面一套自定义 `@font-face` 字体在浏览器里渲染回真字——你抓到的文本是 PUA 码点,直接读是乱码。**这不是选择器问题,是要「还原」。**

**识别**:抓到的正文/书名含大量私有区字符;页面 CSS 里有 `@font-face { … src:url(….woff2) }`。

**还原(两步)**:

1. 找到加密字体 URL(页面 CSS 的 `@font-face`),生成「码点 → 真字」映射表:
   ```bash
   trn gen-fontmap <字体URL或本地woff2> -o fontmap.json   # 基准字体缺省自动下载 Noto
   ```
   纯 Rust 字形匹配(woff2 解压 + 渲染字形 + 和常用汉字/数字/字母比长相),输出 `{码点:真字}`,并列出**低置信字**供人工核对。数字 0-9、英文字母也会被混淆进 PUA,候选集已覆盖、能正确还原(旧版工具只有汉字候选,会把「q」等解成形近汉字)。
2. 把表**内联进正文规则的 clean**:
   ```json
   "content": { "value": { "via": "css", "select": ".content", "extract": "html",
     "clean": [ { "fontMap": { "E4DE": "一", "E4F3": "的" } } ] } }
   ```

要点:同一站通常**全站一套字体**(映射固定,生成一次复用;站方换字体才重跑)。引擎只按表查、**不内置任何站点的表**(表是数据、跟着书源走)。详解见 `references/reverse-engineering.md` 的「字体反爬」与博客 `dev-notes/blog/font-anti-scraping-and-fontmap.md`。

## 登录与多步编排(host 桥,需 `js-host` 构建)

需要**登录/会员**才能读全本的站(典型:番茄网页版会员、JWT 鉴权书站),靠书源 JS 里的有状态 **host 对象**完成登录与跨请求传值。注入三个语义对象(**不是** Legado 的 `java`):

- `source` —— 书源状态/登录:`put/get`(跨请求 KV)、`getVariable/putVariable`、`putLoginHeader/getLoginHeader/getLoginHeaderMap/removeLoginHeader`、`getLoginInfo/getLoginInfoMap/putLoginInfo`(凭据 AES 加密存)。
- `net` —— 网络/cookie:`ajax(url)`→响应体、`connect(url, extraHeadersJson?)`/`post(url, body, extraHeadersJson?)`→`{body, code, headers}`、`getCookie(domain, key?)`。
- `crypto` —— 沿用(md5/sha/aes/base64/hex/t2s/s2t)。

**登录态统一**:`source.putLoginHeader(json)` 存任意 header map,引擎每请求自动并入——`Authorization: Bearer <jwt>`、自定义 token 头、`Cookie` **三者同一条路径**(无需 JWT 专门逻辑)。含 `Cookie` 字段会同步进 cookie 库(按注册域)。

**新增书源字段**:

| 字段 | 作用 |
|---|---|
| `loginUrl` | 普通 URL(走浏览器登录),或 `@js:…`/`<js>…</js>` 登录脚本(内含 `login()` 函数) |
| `loginUi` | 声明式登录表单 `[{name,type}]`,type ∈ text/password/select/toggle;收集值加密存 loginInfo |
| `loginCheckJs` | 每个网络方法响应后执行(`result`=响应),返回空/`false`/`0` 判失效 → 提示重登 |
| `enabledCookieJar` | 开启后响应 `Set-Cookie` 自动回灌 cookie 库 |
| `concurrentRate` | 限速 `"N/ms"` 或纯毫秒间隔 |
| `prelude`(各 op) | 结构化前置请求链 `[{url,method?,body?,headers?,capture,skipIfPresent?}]`,主请求/分页前按序执行;**默认构建即可用,不需 js-host** |

**脚本登录范式**(`loginUrl` 为脚本):约定导出全局 `login()`,内部取凭据→发请求→写回登录态:

```js
// loginUrl: "@js:function login(){ var r = net.post('/api/login', JSON.stringify(JSON.parse(source.getLoginInfo()))); var tok = JSON.parse(r.body).token; source.putLoginHeader(JSON.stringify({Authorization:'Bearer '+tok})); }"
```

**结构化多步(声明式,首选;不需 js-host)**:每个 op(search/explore/bookInfo/toc/content)可挂 `prelude` 前置请求链,每步对其响应做命名 `capture`,后续步骤/抽取规则用 `{{name}}` 引用——**不写字符串 DSL**(优于 host JS 的 `source.put/get` 命令式)。

```jsonc
"toc": {
  "prelude": [
    { "url": {"template":"{{base}}/api/prepare"},
      "capture": [{ "name":"csrf", "value": {"via":"json","select":"$.csrf"}, "scope":"chapter" }],
      "skipIfPresent": ["csrf"] }       // 已有则跳过,避免每章重抓
  ],
  "list": { "...": "主请求/规则用 {{csrf}} 引用" }
}
```

- `scope`:`chapter`(默认,本次调用消亡,一次性 csrf/sign/cursor 用它)/ `book`(随本书快照,详情→目录→正文复用)/ `source`(书源级,站级常量;同会话跨 op 共享)。
- 捕获**先于引用**由数组顺序保证;捕获产物是字符串;搜索主请求的 `request.vars`(`{name:Rule}`)等价对搜索响应的 chapter 级捕获,供 `list`/`item` 引用。
- 跨会话/历史续读是**全新引擎**:需 token 的 `toc`/`content` 应各自声明 `prelude` + `skipIfPresent` 幂等重取(search 阶段 token 用 `source`/`chapter`,**别用 `book`**——选书前无本书快照)。

**host JS 多步(需 `js-host`)**:JS 内 `net.ajax/connect` 复用取页管线(自动带 loginHeader + 按注册域的库 cookie);命令式跨请求传值用 `source.put/get`。**不引入** Legado 的 `@put:/@get:` 字符串 DSL。

要点:`prelude`/`capture` 结构化多步默认构建即可用;`loginUrl`/`net.*`/`source.*` 等登录与 host 网络能力仅 `js-host` 构建可用,纯净构建(默认)无网络/状态、行为不变。站点是否需登录用 AskUserQuestion 问用户,再决定 `loginUrl`/`loginUi` 形态。

## 拿不准就问(用 AskUserQuestion)

探站时遇到**你无法从页面自行判定**的事,别瞎猜——用 AskUserQuestion 问用户。典型:

- 站点需要登录/会员才能看正文或目录;
- 有多个候选区块,分不清哪个是「正文/书单」主体;
- 没有可用的样例书(`samples` 需要一个真实 book_url + 期望);
- 站点疑似需要浏览器才能拿到内容,问是否启用 `fetcher: "browser"`;
- 同一意图有多个搜索入口,问优先哪个。

把可推断的(默认 charset、相对 URL、auto fetcher)直接定下来,只把**真正需要用户拍板**的拿出来问。

## 产物

- `<站点>.v2.json`:`schema`/`name`/`url`/`http?`/`search?`/`explore?`/`bookInfo`/`toc`/`content`/`samples`。
- 至少一条 `samples`(一个真实 `bookUrl` + `expect`,如 `name`、`minChapters`、`volumes`、`minContentChars`)——既驱动 doctor 在无浏览时也能验,也供运行期自愈。
- 一句话交付小结:doctor 各项结果、哪些 ✓、哪些是已知降级项(如被挑战的搜索)。
