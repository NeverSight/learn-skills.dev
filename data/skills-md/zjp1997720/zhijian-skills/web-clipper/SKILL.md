---
name: web-clipper
description: 从单篇文章 URL 或文章索引页/归档页中抓取正文并保存到本地 Markdown。用户提到“收藏文章”“保存网页”“批量抓取页面里的文章”“把这个 archive 页前 N 篇拉下来”“保存到 Obsidian / Clippings / 本地”时必须优先使用。尤其适合公开网页、Substack、博客文章页、文章归档页。遇到懒加载列表、动态页面、静态抓取不全时，先用 browser 收集文章 URL，再调用脚本批量落地，以成功率优先。
---

# Web Clipper

目标：把「网页文章收藏」做成稳定工作流，而不是一次性手工操作。

## 和 Obsidian / 本地知识库的关系

本 Skill 是文章进入本地知识系统的入口。它不把网页直接冒充成已经整理好的知识，而是先保存为带来源信息的 `source_candidate`，供后续人工筛选、知识编译或写作流程继续处理。

默认分工：

- Obsidian Web Clipper：浏览器里手动剪藏，模板负责生成最小 OKF frontmatter。
- 本 skill：Agent 批量抓取、补抓失败页面、检查文章正文质量。
- 后续知识流程：把高价值候选资料编译成来源卡、概念、方法、案例、练习或写作素材。

新增或抓取的文章默认不是“已整理知识”，而是“待判断资料”。状态字段使用：

```text
unprocessed -> queued -> source_carded -> compiled -> used
ignored / needs_human
```

保存的 Markdown 应尽量包含以下字段，方便 Obsidian、检测脚本和后续 Agent 读取：

```yaml
---
type: source_candidate
title: "..."
summary: "..."
source: "https://..."
resource: "https://..."
source_kind: web_article
platform: web
author: "..."
published: "YYYY-MM-DD"
clipped: "ISO时间"
clipper: agent_web_clipper
okf_version: local-okf-v0.2
compile_status: queued
status: unprocessed
training_relevance: medium
topics:
  - Agent
candidate_outputs:
  - source_card
  - writing_fuel
reuse_note: ""
tags:
  - clipping
---
```

字段含义：

- `type: source_candidate`：表示这是候选来源，不是正式 Wiki 页。
- `source_kind`：来源类型，例如 `wechat_article`、`x_status`、`web_article`。
- `training_relevance`：内容复用相关度。Agent 抓取默认 `medium`，可用 `--training-relevance high|medium|low|unknown` 覆盖。
- `topics`：OKF 主题标签。脚本会从标题、URL、描述和 tags 粗推，也可用 `--topic Agent --topic AI培训` 显式指定。
- `candidate_outputs`：后续可能拆成的知识资产类型。脚本默认 `source_card` + `writing_fuel`，可用 `--candidate-output method` 等重复追加。
- `compile_status`：后续自动检测和编译流程读取的主状态字段。Agent 抓取默认 `queued`，表示进入候选队列但不自动写正式 Wiki。

## 这个 skill 解决什么问题

它覆盖两类任务：

1. **单篇收藏**
   - 输入一个文章 URL
   - 提取标题、摘要、发布日期、正文
   - 保存为 Markdown 到用户指定目录

2. **批量收藏**
   - 输入一个索引页、归档页、专题页、作者主页
   - 按用户要求抓前 N 篇、热门文章、最新文章，或指定的一组文章
   - 批量保存到本地

## 成功率优先的执行策略

按下面顺序走，不要反过来：

## 首次使用与依赖自检

这个 skill 在分享 zip 给别人后，统一走 wrapper，不要直接打主脚本。

首次运行时，先执行：

```bash
bash <web-clipper-root>/scripts/run_web_clipper.sh --help
```

注意：这条命令有副作用。

它会先运行 bootstrap，可能创建默认 clipping 目录和当前项目下的 `.web-clipper/EXTEND.md`。

wrapper 会先调用 `scripts/bootstrap.sh`，自动做这些事：

1. 检查 Python 3 是否可用
2. Python 3 缺失时尝试自动安装
3. 检查主脚本是否完整
4. 自动创建默认 clipping 目录
5. 首次运行时写入当前项目下的 `.web-clipper/EXTEND.md`

默认把“当前命令所在目录”当成目标项目根目录。

所以要从目标 vault 根目录执行 wrapper，不要在子目录里随手运行。

如果自动安装失败，要明确告诉用户：

- 卡在 Python 运行时，而不是网页抓取逻辑
- 当前平台推荐的安装命令
- 安装完成后重新运行 wrapper 即可

如果用户没给保存目录，优先顺序如下：

1. 当前项目 `.web-clipper/EXTEND.md` 里的 `default_output_dir`
2. 当前仓库下的 `00_收件箱/Clippings/`
3. 当前工作目录下的 `Clippings/`

### 路径 A：脚本直抓（最短成功路径）

适用：

- 公开网页
- 不需要登录
- 文章页 HTML 里直接带正文或结构化 JSON
- Substack / 常规博客 / 简单 CMS
- X/Twitter 长文、老式博客、结构不标准但公开可读的文章页

做法：

- 优先调用 `scripts/run_web_clipper.sh`
- 单篇：直接抓 URL
- 批量：先让脚本尝试从索引页静态提取文章链接

脚本内部会自动按站点和失败情况选择 extractor：

1. X/Twitter 长文和微信公众号文章优先 `defuddle@0.19.2`，这是当前最短成功路径
2. 普通网页先静态解析 HTML / JSON-LD / `<article>` / `<main>`
3. 静态失败后 fallback 到 `defuddle`
4. `defuddle` 失败后 fallback 到 Jina Reader (`r.jina.ai`)
5. 微信公众号等页面如果 `defuddle` 失败，再走 Metaso Reader API；Jina 常会拿到微信“环境异常”页，不作为公众号优先路径

输出 frontmatter 会包含 `extractor` 字段，方便排查是哪一路成功。

### 路径 A2：Jina Reader fallback

适用：

- 静态直抓失败
- 页面结构老、正文不在 `<article>` / `<main>` 中
- `defuddle` 没拿到正文，但 Jina Reader 能清洗出 Markdown

做法：

- 脚本会自动调用 `https://r.jina.ai/<原始URL>`
- 不需要 API Key
- 输出会继续保存成统一的本地 Markdown

### 路径 A3：Metaso Reader API fallback

适用：

- 静态直抓失败（微信公众号、有反爬的站点等）
- 脚本报 `article body not found`
- 不需要额外安装，只需要配置 API Key

做法：

- 脚本会自动 fallback 到 Metaso Reader API
- 需要设置环境变量 `METASO_API_KEY`
- API 返回结构化 Markdown，包含图片链接
- 对微信公众号、163 等反爬站点效果很好

如果没有配置 `METASO_API_KEY`，这层会被跳过，继续走路径 B/C。

### 路径 B：浏览器补链路

适用：

- 索引页懒加载
- 静态 HTML 里只露出部分文章链接
- 需要滚动页面才能拿全前 N 篇
- 页面结构怪，脚本无法可靠收集链接

做法：

1. 用 `browser` 打开索引页
2. 滚动页面，直到收集到足够数量的文章 URL
3. 在页面里执行 JS，返回去重后的文章 URL 列表
4. 把 URL 列表写到临时 txt 文件
5. 再调用 `scripts/run_web_clipper.sh --url-file ...` 批量落地

这个模式很重要：**浏览器负责拿链接，脚本负责落地正文**。

### 路径 C：浏览器直接抽正文

适用：

- 单篇页面静态抓取被封
- `web_fetch` 被拦
- 脚本抓正文失败，但浏览器能正常打开渲染后的页面

做法：

- 用 `browser` 进入文章页
- 用 evaluate 从 DOM 或页面内嵌 JSON 里抽正文
- 组装 Markdown
- 用 `write` 落地文件

只有在 A、B 都不稳时再用 C，因为 C 更重，但成功率高。

### 路径 C2：CDP Proxy 兜底

适用：

- 脚本已经确认正文提取失败
- 浏览器页面本身能正常打开
- 宿主的 Browser 运行时在初始化、选 tab 或 evaluate 阶段报错，继续重试同一运行时没有收益

如果当前环境提供 `web-access` 或等价的浏览器控制 Skill，先完整读取并遵守它，再使用 CDP Proxy。依赖检查、风险提示和 tab 清理都属于执行合同，不能跳过。

执行顺序：

1. 运行 `web-access` 的依赖检查，确认 Chrome remote debugging 和 Proxy 可用。
2. 在回复中展示该 Skill 要求的自动化风险提示。
3. 通过 Proxy 新建后台 tab，不复用或关闭用户已有 tab。
4. 打开目标文章，用 `/eval` 读取标题、作者、发布日期、摘要和正文容器。微信公众号优先检查 `#js_content`，同时检查页面标题和正文长度，排除验证页、环境异常页和空壳页面。
5. 正文达到完整文章量级后，再组装统一 frontmatter 和 Markdown；搜索摘要、正文片段和验证页文本都不能冒充原文。
6. 保存成功后关闭自己创建的 tab，并在 frontmatter 记录 `extractor: browser_cdp`，方便追溯兜底路径。

CDP Proxy 是 Browser 运行时故障后的替代执行面，不改变本 Skill 的输出：最终仍是一份结构完整、可进入 OKF / Wiki 流程的本地 Markdown。

## 输入澄清规则

如果用户没说明，优先补齐这 4 件事：

1. **单篇还是批量**
2. **抓多少篇**
3. **保存到哪里**
4. **是否只抓正文，还是顺带保留 frontmatter 元数据**

默认值：

- 单篇：抓 1 篇
- 批量：如果用户说“前几篇/前 20 篇/热门文章”就按用户要求；没说数量时，先问
- 输出格式：Markdown + YAML frontmatter
- 默认保存目录：如果用户没指定，就放用户已有的 clipping 目录；没有既有目录时优先使用 `00_收件箱/Clippings/`

## 推荐命令

### 单篇

```bash
WEB_CLIPPER_ROOT="<web-clipper-root>"
bash "$WEB_CLIPPER_ROOT/scripts/run_web_clipper.sh" \
  --url "<文章URL>" \
  --mode single \
  --output-dir "<输出目录>" \
  --training-relevance medium \
  --candidate-output source_card \
  --candidate-output writing_fuel
```

### 批量，静态收集链接

```bash
WEB_CLIPPER_ROOT="<web-clipper-root>"
bash "$WEB_CLIPPER_ROOT/scripts/run_web_clipper.sh" \
  --url "<索引页URL>" \
  --mode batch \
  --count 20 \
  --output-dir "<输出目录>"
```

### 批量，浏览器先收集链接再落地

```bash
WEB_CLIPPER_ROOT="<web-clipper-root>"
bash "$WEB_CLIPPER_ROOT/scripts/run_web_clipper.sh" \
  --url-file /tmp/article_urls.txt \
  --mode batch \
  --count 20 \
  --output-dir "<输出目录>"
```

如果用户没有显式传 `--output-dir`，wrapper 会优先读取 `.web-clipper/EXTEND.md` 的默认目录；如果没有配置，再自动回退到 `00_收件箱/Clippings/` 或 `Clippings/`。

## 浏览器收集 URL 的建议 JS

当静态页面拿不全链接时，用 `browser.act(kind="evaluate")` 执行类似逻辑：

```js
async () => {
  const collect = () => [
    ...new Set(
      Array.from(document.querySelectorAll('a[href*="/p/"]'))
        .map((a) => a.href)
        .filter((h) => !h.includes("/comments")),
    ),
  ];

  let urls = collect();
  for (let i = 0; i < 8 && urls.length < 20; i++) {
    window.scrollTo(0, document.body.scrollHeight);
    await new Promise((r) => setTimeout(r, 1500));
    urls = collect();
  }
  return urls;
};
```

然后把结果写到 `/tmp/article_urls.txt`，每行一个 URL。

## 输出要求

每篇文章输出一个 Markdown 文件，推荐结构：

```markdown
---
type: source_candidate
title: "..."
author: "..."
source: "..."
resource: "..."
archive: "..."
source_kind: web_article
platform: web
published: "YYYY-MM-DD"
clipped: "ISO时间"
clipper: agent_web_clipper
okf_version: local-okf-v0.2
compile_status: queued
status: unprocessed
training_relevance: medium
topics:
  - Agent
candidate_outputs:
  - source_card
  - writing_fuel
reuse_note: ""
tags:
  - clipping
---

# 标题

> 摘要

正文...
```

## 文件命名

默认格式：

```text
YYYY-MM-DD 标题.md
```

如果日期缺失，就用：

```text
unknown-date 标题.md
```

## 失败处理

如果批量任务失败，不要一句“失败了”就结束。按这个顺序排查：

1. 索引页是否懒加载，导致静态只拿到部分链接
2. 文章页是否是公开页
3. 文章正文是否藏在结构化 JSON，例如 `body_html`
4. 是否需要浏览器渲染后再抽正文

要明确告诉用户卡在哪一层：

- 链接收集失败
- 正文提取失败
- 文件写入失败

## 当前已验证成功的站点模式

### Substack

已验证：

- 可从 archive 页收集文章 URL
- 可从文章页内嵌 JSON 字段 `body_html` 提取正文
- 适合保存到 Obsidian Clippings

这类站点优先用脚本批量处理；当 archive 页是懒加载时，用浏览器补 URL 收集。

### 微信公众号

已验证：

- 静态直抓会被反爬拦截（验证页）
- `defuddle` 对可公开访问的公众号文章可直接抓到正文、标题和作者，是当前优先路径
- Jina Reader 常会抓到微信“环境异常”验证页，不作为公众号优先路径
- 通过 Metaso Reader API（路径 A3）可作为 `defuddle` 失败后的兜底，返回完整 Markdown + 图片链接
- 需要配置 `METASO_API_KEY` 环境变量

## 交付回执

完成后，用简短结果回执，不要啰嗦：

```markdown
已保存到: <目录或文件路径>
类型: clipping / Markdown
理由: 已按要求完成单篇或批量文章收藏
```

如果是批量任务，再补一行：

- 成功 X 篇
- 失败 Y 篇

## 不该触发这个 skill 的情况

这些情况不要硬用本 skill：

- 用户要的是摘要、改写、翻译，而不是收藏落地
- 用户要抓登录后内容，且没有可用登录态
- 用户要抓整站所有页面做爬虫归档
- 用户要的是浏览器自动化测试，而不是文章收藏

## 安全边界

- 只处理用户有权访问的公开 HTTP(S) 页面；不绕过登录、付费墙、验证码或访问控制。
- 文章正文可能受版权保护。默认用途是个人研究、内部归档和知识整理；保留作者、日期与原链接，不擅自公开转载全文。
- `defuddle` 通过 `npx` 运行固定版本；Jina Reader 与可选 Metaso fallback 会把目标 URL 发送给第三方服务。
- 设置 `METASO_API_KEY` 即表示启用可选的 Metaso fallback；使用前应确认账号费用与数据传输边界。
- wrapper 会把输出限制在当前项目内。首次 bootstrap 可能安装 Python、创建 clipping 目录并写入 `.web-clipper/EXTEND.md`，执行前应向用户说明这些副作用。
