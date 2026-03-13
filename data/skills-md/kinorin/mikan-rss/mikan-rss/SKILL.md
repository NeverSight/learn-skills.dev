---
name: mikan-rss
description: Fetch anime RSS subscription links and episode lists from mikanani.kas.pub based on year/season/title and subtitle group. Use when the user mentions 蜜柑计划, Mikan, mikanani, wants 番剧 RSS/订阅链接, or asks for某季度某番剧的种子/磁链订阅.
---

# Mikan RSS 番剧订阅 Skill

## When to use

Use this skill whenever the user:

- **提到蜜柑计划 / Mikan / mikanani.kas.pub** 并希望获取订阅链接或 RSS。
- **按“年份 + 季节”查询番剧**，例如“2025 年秋季番”“2026 冬季番”。
- **给出番剧名称，想要对应的 RSS**，如“帮我找《优雅贵族的休假指南。》的 RSS”。
- **指定或询问字幕组/翻译组的订阅**，如“只要 LoliHouse 的 RSS”“列出所有字幕组的链接”。

如果用户只是随便问“哪里可以看这个番”，不要使用本技能；只有当明确需要 **Mikan 上的番剧资源或订阅/RSS** 时才启用。

## Key concepts

- **季度（year, seasonStr）**  
  - 年份通过 URL 参数 `year=2025` 指定。  
  - 季度字符串通过 `seasonStr` 指定，对应：`冬`、`春`、`夏`、`秋`（UTF-8 URL 编码后直接用在请求中即可）。 
  - 冬（一月），春（四月），夏（七月），秋（十月），如果用户通过月份描述，通过这个关系一一对应。 
  - 可用季度列表存在主页 `#sk-data-nav > div > ul.navbar-nav.date-select` 中，用来验证年份/季度是否合法。

- **番剧列表接口（按季度）**  
  - 入口：`https://mikanani.kas.pub/Home/BangumiCoverFlowByDayOfWeek?year=<YEAR>&seasonStr=<SEASON>`  
  - 页面内容按照星期分组，内部每个番剧是指向 `https://mikanani.kas.pub/Home/Bangumi/<bangumiId>` 的链接。  
  - `bangumiId` 即番剧 ID，例如 `.../Home/Bangumi/3863` 中 `3863`。

- **番剧搜索结果页（按关键词）**  
  - 入口：`https://mikanani.kas.pub/Home/Search?searchstr=<ENCODED_KEYWORD>`，例如：  
    - `https://mikanani.kas.pub/Home/Search?searchstr=%E9%AD%94%E6%B3%95%E5%B0%91%E5%A5%B3%E5%B0%8F%E5%9C%86`（搜索“魔法少女小圆”）。  
  - 搜索结果主体位于 `#sk-container > div.central-container > ul` 下，每个 `<li>` 通常对应一个番剧或资源条目。  
  - 在本技能场景中，只需从该 `<ul>` 中提取与目标番剧直接相关的条目即可，**忽略页面上的“相关推荐”“搜索结果表格”等其他区域**。  
  - 解析策略示例：  
    - 在 `#sk-container > div.central-container > ul > li` 中查找标题文本或链接，匹配包含番剧名关键字的项；  
    - 一旦确认具体番剧，可继续通过内部链接（如果存在 `/Home/Bangumi/<bangumiId>`）或结合季度接口确定 `bangumiId`。

- **番剧详情页**  
  - 入口：`https://mikanani.kas.pub/Home/Bangumi/<bangumiId>`。  
  - 包含：番名、放送信息、简介，以及 **“字幕组列表”**。  
  - 每个字幕组通常显示为一个名称链接，形如 `https://mikanani.kas.pub/Home/PublishGroup/<subgroupId>`，`subgroupId` 即翻译组 ID（HTML 中常见形态为类似 `id="subgroup-370"`）。
  - 页面下方每个字幕组对应一个资源表格（番组名 / 大小 / 更新时间 / 下载链接 / 播放）。

- **RSS 订阅链接结构**  
  - 基本形态：`https://mikanani.kas.pub/RSS/Bangumi?bangumiId=<BANGUMI_ID>&subgroupid=<SUBGROUP_ID>`  
  - `bangumiId` 与 `subgroupid` 都来自上述页面结构。

## Workflow

当用户请求 Mikan 番剧订阅信息时，遵循以下流程。

### 1. 把用户需求规范化

1. **解析用户输入中的以下信息：**
   - 年份：例如 `2025`、`2026`。  
   - 季度：`冬`、`春`、`夏`、`秋`，或可以明确映射到上述之一的自然语言（例如“2025 秋番”“2025 秋季番组”→ `2025` + `秋`）。  
   - 番剧名称：优先使用用户给出的 **完整番名**；如只有部分关键字，准备做模糊匹配。  
   - 指定的字幕组（如果有）：例如 “只要 LoliHouse”“ANi 的订阅”。

2. **若用户未指定年份或季度：**
   - 默认使用当前或最近一季对用户最有可能含义的季度（例如当前日期落在哪个季度）。  
   - 在回复中明确标注你假定使用的 `year` 和 `seasonStr`，以便用户知道。

3. **若用户只给番名不提季度/年份：**
   - **优先使用关键词搜索页**：  
     - 构造 `https://mikanani.kas.pub/Home/Search?searchstr=<ENCODED_KEYWORD>`，其中 `<ENCODED_KEYWORD>` 为番剧名的 URL 编码（例如 “魔法少女小圆” → `%E9%AD%94%E6%B3%95%E5%B0%91%E5%A5%B3%E5%B0%8F%E5%9C%86`）。  
     - 在返回页面中，只解析 `#sk-container > div.central-container > ul` 下的 `<li>` 项，忽略其他区域（相关推荐、大资源表格等）。  
     - 从这些 `<li>` 中匹配番剧标题；若存在指向 `/Home/Bangumi/<bangumiId>` 的链接，可直接取得 `bangumiId` 并跳到后续流程。  
   - 如果搜索页无法可靠定位到唯一番剧（无结果或多个高度相似候选），则回退到 **按季度检索**：  
     - 先根据当前日期推断最可能的 `year + seasonStr`，在对应季度列表中搜索该番名；  
     - 若仍无法确定，明确说明需要用户补充具体 `年份 + 季节` 或更精确的番名。

### 2. 获取指定季度的番剧列表

1. 访问季度列表接口：
   - `https://mikanani.kas.pub/Home/BangumiCoverFlowByDayOfWeek?year=<YEAR>&seasonStr=<SEASON>`  
   - 例如：`year=2025&seasonStr=秋季`（URL 编码后使用）。

2. 解析返回页面：
   - 页面按“星期一～星期日/剧场版/OVA”等分区呈现。  
   - 在所有区块中，查找形如 `/Home/Bangumi/<bangumiId>` 的链接，并提取：  
     - `bangumiId`  
     - 显示的番剧标题（链接文字）  
     - 可选：最近更新时间等辅助信息。

3. 根据用户给定的番剧名进行匹配：
   - **优先精确匹配**：去除空格/全角符号差异，对比标题是否与用户名称一致或只多了英文标题。  
   - 若没有精确匹配，进行 **包含/模糊匹配**，找出包含用户给定关键字的番剧。  
   - 如果匹配结果为 0：  
     - 明确说明“在 `<YEAR> <SEASON>` 季度中未找到该番”，并给出该季度所有番剧列表供用户参考。  
   - 如果匹配结果多于 1：  
     - 将所有候选项列出（番名 + `bangumiId`），请用户选择其一，或在你认为最可能时选一个 **并说明选择依据**。

### 3. 解析番剧详情页，获取字幕组及资源

对于选定的 `bangumiId`：

1. 访问番剧详情页：  
   - `https://mikanani.kas.pub/Home/Bangumi/<bangumiId>`。

2. 在页面 **“字幕组列表”** 区域，提取每个字幕组信息：
   - 字幕组名称（例如 `LoliHouse`、`ANi`、`Kirara Fantasia` 等）。  
   - 字幕组 ID：通常出现在链接 `/Home/PublishGroup/<subgroupId>` 中，或元素 id 类似 `subgroup-<subgroupId>`。  
   - 最近更新时间（可从小节摘要或资源表格中获取）。

3. 为每个字幕组构造 RSS 订阅链接：
   - 模板：  
     - `https://mikanani.kas.pub/RSS/Bangumi?bangumiId=<BANGUMI_ID>&subgroupid=<SUBGROUP_ID>`  
   - 确保使用数字形式的 `bangumiId` 和 `subgroupid`（不带额外字符）。

4. 解析每个字幕组的资源列表（可选但推荐）：
   - 对应字幕组的小节中，存在一个表格；按行提取：  
     - **番组名 / 文件名**（通常带话数与分辨率信息）。  
     - **大小**。  
     - **更新时间**。  
     - **下载链接**（指向 `/Home/Episode/<episodeId>`，该页面包含磁链）。  
   - 出于篇幅考虑，不必在默认回答中列出所有条目；可：  
     - 默认给出 **最新几条** 资源。  
     - 若用户明确要求“全部列出来”，可以针对该字幕组完整列出。

### 4. 按用户偏好过滤字幕组

1. 如果用户指定了字幕组名称：
   - 在提取到的字幕组中按名称（或明显缩写/大小写变体）匹配。  
   - 若匹配不到，明确告知该番当前可用字幕组列表，让用户重新选择。

2. 如果用户没有指定字幕组：
   - 默认列出 **所有字幕组** 的 RSS 链接。  
   - 在输出中标记每个字幕组最近更新时间，以便用户自行判断活跃程度。

### 5. 输出格式

当返回结果时，使用结构化、易读的格式。例如：

- **番剧信息**
  - **番名**: `<番剧中文名 / 日文名 (如果存在)>`
  - **Bangumi ID**: `<bangumiId>`
  - **季度**: `<YEAR> 年 <SEASON>`（如“2025 年秋季”）

- **字幕组订阅列表（核心输出）**
  - **字幕组名称**: `<subgroupName>`
    - **Subgroup ID**: `<subgroupId>`
    - **RSS 链接**: `https://mikanani.kas.pub/RSS/Bangumi?bangumiId=<bangumiId>&subgroupid=<subgroupId>`
    - **最近更新时间**: `<最新资源更新时间，如果已解析到>`
    - **示例资源（可选，列出最近 3 条）**:
      - `<文件名 1>` · `<大小>` · `<更新时间>` · `Episode 链接`
      - `<文件名 2>` · ...

- **注意事项 / 限制（如有）**
  - 若季度或番名是你推断的而非用户明确指定，注明你的假设。  
  - 若存在多个同名或相似番剧，说明你选择的是哪一个，以及其他候选。

## Examples

### 示例 1：精确番名 + 季度

> 用户：给我 2026 年冬季《优雅贵族的休假指南。》在蜜柑上的所有字幕组 RSS 链接。

步骤（概略）：

1. 使用 `year=2026&seasonStr=冬` 请求季度列表，找到标题为“优雅贵族的休假指南。”的条目及其 `bangumiId`。  
2. 访问 `https://mikanani.kas.pub/Home/Bangumi/<bangumiId>`，解析字幕组 `LoliHouse`、`ANi`、`Kirara Fantasia`、`沸班亚马制作组` 等及各自 ID。  
3. 为每个字幕组构造 RSS 链接并输出：
   - `...?bangumiId=<bangumiId>&subgroupid=<LoliHouse 的 ID>`  
   - `...?bangumiId=<bangumiId>&subgroupid=<ANi 的 ID>`  
   - 等等。

### 示例 2：未给季度，只给番名

> 用户：帮我找《一拳超人 第三季》的 Mikan RSS。

处理方式：

1. 假定当前或最近一季为检索目标（例如 2025 年秋季），说明你使用的默认季度。  
2. 在该季度列表中搜索名称含 “一拳超人 第三季” 的条目。  
3. 按上文同样流程获取 `bangumiId`、字幕组列表与 RSS 链接，并在回答中确认：  
   - 该番所在季度  
   - 所使用的 `bangumiId`，以及是否有其他相近候选。

### 示例 3：只要特定字幕组

> 用户：只给我 LoliHouse 的 RSS 链接就行。

处理方式：

1. 首先同样确定番剧的 `bangumiId`。  
2. 在番剧详情页的字幕组列表中找到 **名称匹配 “LoliHouse”** 的字幕组，提取其 `subgroupId`。  
3. 仅输出这一条 RSS 链接，并标注该字幕组最近更新时间和可选的最新资源示例。
