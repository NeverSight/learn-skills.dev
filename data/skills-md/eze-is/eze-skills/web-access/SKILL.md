---
name: web-access
license: MIT
github: https://github.com/eze-is/eze-skills
description: 
  所有联网操作必须通过此 skill 处理，包括：搜索、网页抓取、登录后操作、网络交互等。
  触发场景：用户要求搜索信息、查看网页内容、访问需要登录的网站、操作网页界面、抓取社交媒体内容（小红书、微博、推特等）、读取动态渲染页面、以及任何需要真实浏览器环境的网络任务。
metadata:
  author: 一泽Eze
  version: "1.3.0"
---

# web-access Skill

## 首次安装

用户首次使用时，执行以下流程：

**Step 1：运行环境探测**
```bash
bash ~/.claude/skills/web-access/scripts/check-deps.sh
```

**Step 2：AI 根据输出处理缺失依赖**

探测脚本只报告事实，安装决策由 AI 完成。缺什么装什么，Chrome 缺失时提示用户手动下载（无法自动安装）。

**Step 3：安装完成后，向用户说明以下内容**

> web-access 已就绪。凡是联网的需求直接说就行，我会自动选最合适的方式：
> - 只需要搜索结果 → 直接搜，最快
> - 需要看完整页面 → 抓取页面内容，不启动浏览器
> - 需要登录/动态页面/浏览器操作 → 自动启动浏览器，登录一次后持久保存。支持多 sub-agent 集群并行使用多个浏览器。
>
> Windows 用户需要 Git Bash 环境（安装 Git for Windows 即可）。

## 浏览哲学

**像人一样浏览，不像机器人一样执行程序。**

人类浏览网页时不会在开始前列出完整步骤，而是带着目标进入，边看边判断，遇到阻碍就解决，发现内容不够就深入——全程围绕「我要拿到什么」做决策。这个 skill 的所有行为都应遵循这个逻辑。

**三个核心判断：**

**① 我需要什么？** — 任务驱动，先想清楚目标信息的性质，再选最轻且能直达的方式。不要用重型工具做轻量任务，也不要用轻量工具面对它覆盖不到的内容。

**② 够了吗？** — 拿到的信息能完成任务，就是够了。不过度采集，不为了"完整"而浪费代价。大概了解一个视频，几帧就够；理解一篇文章，读文字就够；不需要全页截图去做能用 accessibility tree 完成的事。

**③ 遇到阻碍怎么办？** — 在层内解决，不退回，不打扰用户。弹窗、登录墙、广告、加载失败——像人一样判断这个阻碍是否真的挡住了目标内容：挡住了就处理，没挡住就绕过去继续。只有在确认无法自行解决时才告知用户。**UI 交互也是一种可绕过的间接层**：翻页、展开、点击不是获取内容的唯一路径——内容有可能已经在网站里，交互只是展示手段。

## 信息获取通道选择

- **先评估任务，再选通道**：根据「目标信息的性质、什么工具能直接拿到」决定起点，选最轻且能直达的方案。
- **确保信息的真实性，一手信息优于二手信息**：搜索引擎和聚合平台是信息发现入口。当多次搜索尝试后没有质的改进时，升级到更根本的获取方式：定位一手来源（官网、官方平台、原始页面）。

| 场景 | 通道 |
|------|------|
| 只需搜索摘要或关键词结果，或需要发现信息来源 | **WebSearch** |
| URL 已知，读取页面内容 | **Jina**（默认）；需要精确 meta / 统计数据时改用 **WebFetch** |
| URL 是 PDF | **Jina** |
| 非公开内容，或已知静态层无效的平台（小红书、微信公众号等公开内容也被反爬限制） | **浏览器 CDP**（直接，跳过静态层） |
| 需要动态内容、登录态、交互操作，或需要像人一样在浏览器内自由导航探索 | **浏览器 CDP** |

浏览器 CDP 不要求 URL 已知——可从任意入口出发，通过页面内搜索、点击、跳转等方式找到目标内容。

**Jina**：调用方式为 `r.jina.ai/example.com`（URL 前加前缀，不保留原网址 http 前缀）。免费限速 20 RPM，token 消耗很低。
底层用 Puppeteer 渲染页面（能处理 JS/SPA），再用 Readability 算法提取主文章内容转为 Markdown，会过滤导航、广告、侧边栏等噪声。适合文章、博客、文档、PDF 等以正文为核心的页面；对视频页、数据面板、商品页等非文章结构页面，可能提取到错误区块。拿到结果后判断内容是否符合任务预期，不符合则切换访问策略。

**WebFetch**：直接获取原始 HTML，不执行 JS。页面中嵌入的完整结构化数据（meta 标签、JSON-LD、data 属性等）完整保留，JS 渲染的内容拿不到。请求时加 header `Accept: text/markdown, text/html`，支持该协议的网站直接返回 Markdown。

**选择逻辑**：默认用 Jina。但如果任务明确需要精确的结构化字段（播放量、发布时间、OG 标签等藏在 HTML 源码而非页面正文的数据），直接用 WebFetch——这类数据 Jina 拿不到或不可靠。Jina 和 WebFetch 均无法处理时（空内容、403、需登录）→ 升级浏览器层。


**降级禁止**：进入更重的通道后，不得回头用轻量工具完成同一目标——等同于重走已知不通的路。浏览器层遇到阻碍应在层内解决（如处理登录），而不是绕回。唯一例外：浏览器操作中衍生的新子目标，可重新选择通道。

进入浏览器层后，区分任务性质：

- **操作型**（导航、填表、点击）：用 accessibility tree 感知界面，无法识别时才截图辅助
- **内容型**（读帖子、看资讯、分析页面）：accessibility tree 读文字结构，同时判断图片是否承载核心信息——是则提取图片 URL 定向读取

**图片判断**：社交媒体、图文博客、截图类内容，默认图片有价值，主动去取；工具类、导航类页面，默认 accessibility tree 够用。

## 浏览器 CDP 模式

### 启动

```bash
# 单 agent 任务（默认端口 9222）
bash ~/.claude/skills/web-access/scripts/ensure-browser.sh

# 并行任务（端口由主 agent 在 task prompt 中指定，见「并行调研」章节）
bash ~/.claude/skills/web-access/scripts/ensure-browser.sh $PORT
```

输出 `Browser ready on port XXXX`。启动后必须执行以下两步：

```bash
# 解析端口并设置 session（所有后续命令自动继承，无需重复传参）
PORT=<从输出解析的端口号>
export AGENT_BROWSER_SESSION="port-${PORT}"
```

输出状态说明：
- `Browser ready on port XXXX` → 可直接用，设置 PORT 和 SESSION 后继续（任务结束后关闭）
- `ERROR` → 执行 `bash ~/.claude/skills/web-access/scripts/close-browser.sh [端口]` 后重新运行

> **⚠️ 严禁降级**：只用 agent-browser CDP 模式，不切换到其他浏览器工具/MCP。

### 常用命令

将 `ensure-browser.sh` 输出中的端口号记为 `$PORT`，后续命令统一用该端口：

```bash
agent-browser --cdp $PORT open <url>           # 打开页面
agent-browser --cdp $PORT snapshot -i          # 可交互元素（操作用）
agent-browser --cdp $PORT snapshot             # 完整无障碍树（读文字用）
agent-browser --cdp $PORT click @ref-123       # 点击元素
agent-browser --cdp $PORT fill @ref-123 "内容" # 填写输入框
agent-browser --cdp $PORT wait load networkidle  # 仅用于 click/fill 触发导航后；open 已内置等待，勿在 open 后使用
agent-browser --cdp $PORT scroll down 3000     # 触发懒加载
agent-browser --cdp $PORT screenshot /tmp/x.png
agent-browser --cdp $PORT screenshot --annotate      # snapshot -i ref 失效时的升级方案，见 references/commands.md
agent-browser --cdp $PORT eval "<js>"          # 执行 JS，用于提取 DOM 信息
```

### 图片提取

判断内容在图片里时，用 `eval` 从 DOM 直接拿图片 URL，再定向打开截图读取——比全页截图精准得多。

技术事实：
- 页面中存在大量已加载但未展示的内容——轮播中非当前帧的图片、折叠区块的文字、懒加载占位元素等，它们存在于 DOM 中但对用户不可见。视觉层只是 DOM 数据的一个投影。以数据结构（容器、属性、节点关系）为单位思考，可以直接触达这些内容，而不依赖视觉层是否将其呈现出来。
- scroll 到底部会触发懒加载，使未进入视口的图片完成加载。用 `eval` 提取图片 URL 前若未滚动，部分图片可能尚未加载。

拿到图片 URL 后，Read 工具原生支持读取本地图片文件。对于无需 session 的公开图片 URL，可直接下载到本地后用 Read 读取，无需经过浏览器。需要 session/cookie 的图片才需要在浏览器内 open + screenshot。

### 视频内容获取

CDP headed 模式下浏览器真实渲染，截图可捕获当前视频帧。核心能力：**seek 到任意时间点截图**，可对视频内容进行离散采样分析。

```bash
# 获取总时长，制定采样计划
agent-browser --cdp $PORT eval "document.querySelector('video').duration"
# seek + 播放 + 截图
agent-browser --cdp $PORT eval "var v=document.querySelector('video'); v.currentTime=60; v.play()"
sleep 2
agent-browser --cdp $PORT screenshot /tmp/frame.png
# 全屏截图画面更清晰
agent-browser --cdp $PORT eval "document.querySelector('video').requestFullscreen()"
```

采帧粒度（仅供参考，具体视频具体分析：大概了解 → 30-60s 间隔；理解叙事 → 10s；精细分析 → 1-2s）由任务需求自行判断，无需用户指定。

### 登录判断

登录判断的核心问题只有一个：**目标内容拿到了吗？**

打开页面后，先尝试获取目标内容，持续执行。在此过程中，结合两方面信息做判断：

1. **领域知识**：对该网站的了解——X/Twitter 的最新时间线、小红书的私密内容、微博的完整评论等，这类内容通常需要登录才能获取完整数据
2. **页面实际反馈**：内容是否符合预期？是降级版（如热门帖代替最新帖）？是否有明显缺失？

即使页面显示了登录提示，只要目标内容已经拿到，就不需要打扰用户登录。

只有当确认**目标内容无法获取**时，才推断：登录是否能解决这个问题？若推断成立，告知用户：
> "当前页面在未登录状态下无法获取[具体内容]，请在已打开的 Chrome 窗口中登录 [网站名]，完成后告诉我继续。"

登录完成后无需重启浏览器，直接继续原任务。

### 任务结束

任务结束后关闭浏览器（**必须用此脚本，勿直接 kill，否则会留下崩溃窗口**）：
```bash
bash ~/.claude/skills/web-access/scripts/close-browser.sh [端口]   # 默认 9222
```

close-browser.sh 同时清理 Chrome 进程和 agent-browser session daemon，调用方无需额外操作。

## 并行调研：子 Agent 分治策略

任务包含多个**独立**调研目标时（如同时调研 N 个项目、N 个来源），鼓励合理分治给子 Agent 并行执行，而非主 Agent 串行处理。

**好处：**
- **速度**：多子 Agent 并行，总耗时约等于单个子任务时长
- **上下文保护**：抓取内容不进入主 Agent 上下文，主 Agent 只接收摘要，节省 token

**子 Agent 需继承 skill：**
在子 Agent prompt 中写 `遵循 web-access skill 的指引` 即可，子 Agent 会自动加载 skill，无需在 prompt 中复制 skill 内容或指定路径。

**子 Agent Prompt 写法：目标导向，而非步骤指令**

子 Agent 有完整的 skill 知识和自主判断能力。主 Agent 的职责是说清楚**要什么**，仅在必要与确信时限定**怎么做**。过度指定步骤会剥夺子 Agent 的判断空间，反而引入主 Agent 的假设错误。

错误：过度指定（预填了未验证的 URL/账号）：
```
打开 https://x.com/SomeAccount，抓取最新推文
```

正确：目标导向（子 Agent 自主发现路径）：
```
找到 XX 的官方 X 账号，获取最新推文内容
```

关键原则：不要预填未经验证的信息，信息来自用户直接提供或已确认时，才可直接传入。

**分治判断标准：**

| 适合分治 | 不适合分治 |
|----------|-----------|
| 目标相互独立，结果互不依赖 | 目标有依赖关系，下一个需要上一个的结果 |
| 每个子任务量足够大（多页抓取、多轮搜索） | 简单单页查询，分治开销大于收益 |
| 需要 CDP 浏览器或长时间运行的任务 | 几次 WebSearch / Jina 就能完成的轻量查询 |

**CDP 并发：每个端口启动独立 Chrome 实例，互不干扰。**
主 agent 在启动子 agent 时，在 task prompt 中为每个子 agent 明确指定一个独占端口，避免浏览器实例冲突（从 9222 起，在 9222–9299 范围内选择，每个子 agent 用不同端口）。子 agent 收到端口后调用 `ensure-browser.sh <PORT>` 启动。

## 特殊任务规则

### 核实任务

核实的目标是**一手来源**，而非更多的二手报道——多个媒体引用同一个错误会造成循环印证假象。

搜索用于**定位**来源，不用于**证明**真伪。找到来源后，直接访问读取原文。

| 信息类型 | 一手来源 |
|----------|---------|
| 政策/法规 | 发布机构官网 |
| 企业公告 | 公司官方新闻页 |
| 学术声明 | 原始论文/机构官网 |

**找不到官网时**：权威媒体的原创报道（非转载）可作为次级依据，但需向用户说明："未找到官方原文，以下核实来自[媒体名]报道，存在转述误差可能。"

### 工具能力边界理解

对任何工具（MCP、CLI、库）的能力有疑问时，**如果没有足够的知识把握，先查官方文档，如无足够文档介绍，可考虑查看源码，再作判断**，不猜测、不把不确定性转移给用户。

## References 索引

| 文件 | 何时加载 |
|------|---------|
| `references/commands.md` | 需要不常用命令时（drag、storage、pdf 等） |
| `references/login-flow.md` | 需要了解登录流程细节时 |
