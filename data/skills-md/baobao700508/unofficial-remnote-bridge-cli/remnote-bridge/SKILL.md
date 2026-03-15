---
name: remnote-bridge
description: "RemNote 知识库操作指南。通过 remnote-bridge 命令行工具读取、编辑、搜索 RemNote 知识库中的内容。当用户需要操作 RemNote 知识库时使用此 skill——包括读取笔记、编辑内容、搜索、浏览知识库结构、创建闪卡、修改文档属性等。触发关键词包括：RemNote、知识库、笔记、Rem、闪卡、文档、read-rem、edit-rem、read-tree、edit-tree、search、read-globe、read-context。即使用户没有明确提到 CLI 命令，只要意图是操作 RemNote 中的数据，都应触发此 skill。"
---

# RemNote CLI 操作指南

本 skill 指导 AI Agent 通过 remnote-bridge 操作 RemNote 知识库。

**详细命令文档**位于 `instructions/` 目录下，执行具体命令前务必先读取对应文件：

| 命令 | 文档路径 |
|:-----|:---------|
| setup | `instructions/setup.md` |
| connect | `instructions/connect.md` |
| disconnect | `instructions/disconnect.md` |
| health | `instructions/health.md` |
| read-rem | `instructions/read-rem.md` |
| edit-rem | `instructions/edit-rem.md` |
| read-tree | `instructions/read-tree.md` |
| edit-tree | `instructions/edit-tree.md` |
| read-globe | `instructions/read-globe.md` |
| read-context | `instructions/read-context.md` |
| search | `instructions/search.md` |
| addon | `instructions/addon.md` |
| clean | `instructions/clean.md` |
| install-skill | `instructions/install-skill.md` |
| 全局概览 | `instructions/overall.md` |

---

## 1. 核心概念

### 一切皆 Rem

RemNote 中所有内容的基本单元都是 **Rem**。文档、文件夹、闪卡、标签——本质上都是 Rem 的不同形态。

| 用户说的 | 实际上是 |
|:---------|:---------|
| 笔记 / 条目 | Rem |
| 文档 / 页面 | Rem（`isDocument=true`） |
| 文件夹 | Rem（Document 且子节点全是 Document） |
| 闪卡 / 卡片 | Card——由 RemNote 根据 Rem 属性自动生成，**不可直接操控** |

### Rem 类型系统

两个独立维度：

- **type**（闪卡语义）：`concept`（加粗）、`descriptor`（正常字重）、`default`（普通）、`portal`（嵌入引用容器）
- **isDocument**（页面语义）：与 type 完全独立

### CDF 框架（Concept-Descriptor Framework）

RemNote 推荐的知识结构化方法：

```
线性回归 :: 最基本的回归模型        ← Concept（type:concept，加粗）
  假设 ;; 因变量与自变量呈线性关系   ← Descriptor（type:descriptor，斜体）
  损失函数 ;; 均方误差 (MSE)        ← Descriptor
```

### 闪卡的 CLI 操作方式

闪卡由 `type`、`backText`、`practiceDirection` 三个字段控制。通过 CLI 操作闪卡，修改的是这些**字段**。

**禁止**：在文本中插入分隔符（`::`、`;;`、`>>`、`<<` 等）来创建闪卡。分隔符是 RemNote 编辑器的输入语法，CLI 无法识别。

| 闪卡操作 | CLI 方法 |
|:---------|:---------|
| 创建概念定义 | `edit-tree` 新增行 `概念 ↔ 定义`，再 `edit-rem` 设 `type: "concept"` |
| 创建正向问答 | `edit-tree` 新增行 `问题 → 答案` |
| 创建多行答案 | `edit-tree` 新增行 `问题 ↓`（子行自动成为答案） |
| 改变闪卡类型 | `edit-rem` 修改 `type`、`backText`、`practiceDirection` |

### 理解用户意图：分隔符映射

用户在 RemNote 编辑器中通过分隔符创建闪卡。当用户提到这些分隔符时，理解其意图并映射到上述 CLI 操作：

| 用户说 / 编辑器分隔符 | 对应 type | 对应 practiceDirection |
|:----------------------|:----------|:----------------------|
| `::` | concept | both |
| `;;` | descriptor | forward |
| `>>` / `<<` / `<>` | default | forward / backward / both |
| `>>>` / `::>` / `;;>` | default / concept / descriptor | 多行（子 Rem 为答案） |
| `{{}}` | default | forward（完形填空） |

### 三种链接机制

| 机制 | 用户操作 | 本质 | CLI 可见性 |
|:-----|:---------|:-----|:-----------|
| **Reference** | `[[` | RichText 中的 `{"i":"q","_id":"remId"}` | read-rem 的 text 数组 |
| **Tag** | `##` | Rem 的 tags 数组 | read-rem 的 `tags` 字段 |
| **Portal** | `((` | 嵌入实时视图（**编辑同步**） | read-tree 标记 `type:portal refs:id1,id2` |

Portal 的编辑同步意味着修改一处会影响另一处。Portal 引用的 Rem 不会被 read-tree 自动展开，需要对 refs 中的 ID 单独 read-tree。Portal 引用列表可通过 `edit-rem` 修改（str_replace 简化 JSON 中的 `portalDirectlyIncludedRem` 数组）。

#### Portal 操作速查

| 操作 | 命令 | 方式 |
|:-----|:-----|:-----|
| 创建 Portal | `edit-tree` | 新增行 `<!--portal refs:id1,id2-->` |
| 删除 Portal | `edit-tree` | 从大纲中移除 Portal 行（与删除普通行相同） |
| 修改引用列表（增删引用的 Rem） | `edit-rem` | str_replace 简化 JSON 中的 `portalDirectlyIncludedRem` 数组 |
| 移动 Portal（换父节点/位置） | `edit-tree` | 与移动普通行相同 |
| 读取 Portal | `read-rem` | 自动输出 8 字段简化 JSON |

### RichText 格式

`text` 和 `backText` 字段是 JSON 数组，元素为纯字符串或格式化对象：

```json
["纯文本", {"i":"m","b":true,"text":"粗体"}, {"i":"q","_id":"remId"}]
```

#### 元素类型

| `i` 值 | 类型 | 必填字段 | 可选字段 |
|:-------|:-----|:---------|:---------|
| 纯 string | 纯文本 | — | — |
| `"m"` | 带格式文本 | `text` | 格式标记（见下表） |
| `"q"` | Rem 引用 | `_id` | `content`, `showFullName`, `aliasId` |
| `"i"` | 图片 | `url` | `width`, `height`, `percent`(25/50/100) |
| `"x"` | LaTeX | `text` | `block`(true=块级公式) |
| `"a"` | 音频/视频 | `url`, `onlyAudio` | `width`, `height` |
| `"s"` | 卡片分隔符 | — | `delimiterCharacterForSerialization` |

**注意**：`i:"a"` 的 `onlyAudio` 是**必填**字段（`true`=音频，`false`=视频），缺少会导致 SDK 拒绝写入。

#### 格式标记（主要用于 `i:"m"`，但 `i:"q"` 等也支持）

| 字段 | 类型 | 含义 |
|:-----|:-----|:-----|
| `b` | `true` | 加粗 |
| `l` | `true` | 斜体（小写字母 L，不是 I） |
| `u` | `true` | 下划线 |
| `h` | `number` | 高亮颜色（见 RemColor 枚举） |
| `tc` | `number` | 文字颜色（见 RemColor 枚举） |
| `q` | `true` | 行内代码（红色等宽样式） |
| `code` | `true` | 代码块（带语言标签和复制按钮） |
| `language` | `string` | 代码块语言（如 `"javascript"`、`"python"`） |
| `cId` | `string` | 完形填空 ID |
| `hiddenCloze` | `true` | 完形填空隐藏状态 |
| `revealedCloze` | `true` | 完形填空已揭示状态 |
| `iUrl` | `string` | 外部超链接 URL |
| `qId` | `string` | 行内引用链接的 Rem ID |

**注意**：`url` 字段已废弃无效，超链接必须用 `iUrl`。

#### RemColor 颜色枚举（`h` 和 `tc` 共用）

| 值 | 颜色 | 值 | 颜色 | 值 | 颜色 |
|:---|:-----|:---|:-----|:---|:-----|
| 0 | 无颜色/默认 | 4 | Green | 7 | Gray |
| 1 | Red | 5 | Purple | 8 | Brown |
| 2 | Orange | 6 | Blue | 9 | Pink |
| 3 | Yellow | — | — | — | — |

#### 常用构造示例

以下为 `JSON.stringify(null, 2)` 格式化后的实际样式（key 按字母序）：

```jsonc
// 粗体（注意 key 顺序：b < i < text）
{ "b": true, "i": "m", "text": "粗体" }
// 行内代码
{ "i": "m", "q": true, "text": "console.log()" }
// 超链接（iUrl 不是 url！）
{ "i": "m", "iUrl": "https://example.com", "text": "点击访问" }
// 红色高亮 + 粗体（h 是数字，不是字符串）
{ "b": true, "h": 1, "i": "m", "text": "重点" }
// 完形填空
{ "cId": "cloze1", "i": "m", "text": "答案内容" }
// Rem 引用（_id 排在所有小写 key 之前）
{ "_id": "remId", "i": "q" }
// Rem 引用加粗
{ "_id": "remId", "b": true, "i": "q" }
// LaTeX 公式
{ "i": "x", "text": "E = mc^2" }
// 图片
{ "i": "i", "url": "https://...", "width": 200, "height": 100 }
// 视频（onlyAudio 必填！）
{ "i": "a", "onlyAudio": false, "url": "https://youtube.com/watch?v=xxx" }
// 音频
{ "i": "a", "onlyAudio": true, "url": "https://example.com/audio.mp3" }
```

> **注意**：在 RemObject 的格式化 JSON 中，数组内的对象会展开为多行（每个 key 一行，缩进 4+2 空格）。以上为简写——构造 edit-rem 的 oldStr/newStr 时必须使用实际的多行格式。

#### highlightColor（Rem 级别）vs h（RichText 行内）

- `highlightColor`：RemObject 顶层字段，值为字符串（`"Red"`, `"Blue"` 等）或 `null`，作用于整行背景
- `h`：RichText 元素内格式标记，值为数字 0-9（RemColor 枚举），作用于行内文字片段

两者完全独立，互不影响。

#### 序列化确定性

RichText 对象内部按 **key 字母序排列**（`sortRichTextKeys()`），确保 JSON 始终一致。`_id` 中的 `_`（U+005F）排在所有小写字母（`a`=U+0061）之前。构造 edit-rem 的 oldStr 时必须保持相同的 key 顺序，否则匹配失败。

### Powerup 机制与噪音过滤

RemNote 格式设置（fontSize、highlightColor 等）底层通过 Powerup 机制实现，会注入隐藏 Tag 和子 Rem。默认自动过滤（`includePowerup=false`）。read-tree 支持 `--includePowerup` 恢复完整数据，read-globe 和 read-context 硬编码过滤无选项。

---

## 2. 命令决策

### ⚠️ 用户正在看的页面对你不可见

用户在跟你沟通时，往往默认你也能看到他正在浏览的 RemNote 页面，但实际上你们的信息是不对等的。当你发现以下情况时，**必须主动执行 `read-context` 来对齐信息**：
- 用户提到了你没有上下文的内容（如"这个"、"当前页面"、"这里"）
- 用户的描述与你已知的信息对不上
- 你搜索不到用户提到的某些内容
- 用户似乎在引用他正在查看的界面

先用 `read-context` 看到用户所看到的，再做决策，沟通才能顺畅。

### 读取：用户想了解什么？

```
知识库整体结构（"有哪些文档"）       → read-globe
用户当前在看什么（"当前页面"）        → read-context
某个 Rem 的子树（"展开这个主题"）     → read-tree <remId>
某个 Rem 的详细属性（"详细信息"）     → read-rem <remId>
按关键词搜索（"搜索 X"）            → search <query>（中文搜索有限制，见下方说明）
```

#### read-globe vs read-context vs read-tree

| 场景 | 命令 | 特点 |
|:-----|:-----|:-----|
| 知识库有什么 | `read-globe` | 仅 Document 层级，**无缓存**，最小序列化（无 backText/箭头） |
| 我在编辑什么 | `read-context --mode focus` | 鱼眼视图（焦点 depth=3，siblings depth=1，叔伯 depth=0），**无缓存** |
| 当前页面内容 | `read-context --mode page` | 均匀展开，**无缓存** |
| 展开某主题细节 | `read-tree <id>` | 完整子树，**有缓存**供 edit-tree |

**重要**：read-globe、read-context、search 都**不写入缓存**，不能替代 read-tree/read-rem 作为 edit 的前置条件。read-context 需要用户在 RemNote 中有焦点（focus 模式）或打开页面（page 模式）。

### 修改：用户想改什么？

```
Rem 的属性（文本、类型、格式、标签）  → edit-rem   （前置：先 read-rem）
树的结构（新增、删除、移动、重排）    → edit-tree  （前置：先 read-tree）
某行的文字内容                       → edit-rem   （不是 edit-tree！）
```

**关键区分**：`edit-rem` 修改 Rem 的**属性**，`edit-tree` 修改 Rem 之间的**结构关系**。`edit-tree` **禁止修改行内容**。

---

## 3. 标准工作流

### ⚠️ 标准模式：connect 后需要用户配合

`connect` 成功只意味着 daemon 和 Plugin 服务已启动，**Plugin 并未自动连接**。用户必须在 RemNote 中完成操作，Plugin 才能连接到 daemon：

**首次使用**（RemNote 从未加载过此插件）：
1. 打开 RemNote 桌面端或网页端
2. 点击左侧边栏底部的插件图标（拼图形状）
3. 点击「开发你的插件」（Develop Your Plugin）
4. 在输入框中填入 connect 输出的 Plugin 服务地址（如 `http://localhost:29101`）
5. 等待插件加载完成

**非首次使用**（之前已加载过此插件）：
- 只需**刷新 RemNote 页面**即可（浏览器 F5 或 Cmd+R），插件会自动重新连接

**你必须**：执行 `connect` 后，**立即告知用户需要完成上述操作**，不要直接调用业务命令。引导用户完成后，用 `health` 确认三层就绪再继续。

### Headless 模式：自动连接

标准模式每次 connect 后都需要用户手动操作 RemNote。Headless 模式通过 setup（一次性）+ headless Chrome 实现自动连接，后续 connect 无需用户介入。

**⚠️ 模式选择建议**：日常使用推荐**标准模式**。Headless 模式下 Chrome 在后台运行，**无法感知用户正在 RemNote 中浏览和操作的界面**（`read-context` 返回的是 headless Chrome 的上下文，而非用户的浏览器）。只有在全自动化场景（CI/CD、定时任务、批量操作等无需与用户界面交互的场景）才建议使用 Headless 模式。

#### 首次使用（setup）

setup 会弹出 Chrome 窗口，用户需要完成两件事：
1. **登录 RemNote**
2. **配置 dev plugin**：插件图标 → 开发你的插件 → 填入 connect 输出的 Plugin 服务地址（如 `http://localhost:29101`）

完成后**彻底退出 Chrome**（macOS 必须 Cmd+Q，仅关窗口不够）。

**Agent 交互方式**：
```
1. 调用 setup
2. 立即告知用户：
   "已打开 Chrome 浏览器。请完成以下操作：
    1. 登录 RemNote
    2. 在 RemNote 中配置开发插件：点击左下角插件图标 → 开发你的插件 → 输入 connect 输出的 Plugin 服务地址
    3. 完成后彻底退出 Chrome（macOS 请按 Cmd+Q）"
3. 等待 setup 返回（阻塞，最长 10 分钟）
4. 成功 → 进入下一步 connect --headless
```

setup 只需执行一次。之后每次连接直接用 `connect --headless`。

#### 后续使用（connect --headless）

```
1. connect --headless   -- 启动 daemon + headless Chrome 自动加载 RemNote 和 Plugin
2. health               -- 等待三层就绪（Plugin 需要 10-30 秒连接，可多次轮询）
3. 业务操作
4. disconnect           -- 结束会话
```

**无需任何用户操作**——headless Chrome 在后台自动完成登录和 Plugin 加载。

#### 排查

- `health --diagnose`：截图 + Chrome 状态 + console 错误（确认页面是否正常加载）
- `health --reload`：重载 headless Chrome 页面（Plugin 未连接时尝试）
- 如果 Plugin 始终不连接，可能是 RemNote 登录 session 过期，需重新 setup

### 完整流程（标准模式）

```
1. connect              -- 启动会话（幂等，重复调用安全）
2. ⚠️ 引导用户在 RemNote 中加载插件（首次填端口，非首次刷新页面）
3. health               -- 确认三层就绪：daemon → Plugin → SDK（链式依赖）
4. read-globe           -- 了解知识库结构（首次探索）
   或 read-context      -- 了解用户当前上下文
5. search "关键词"       -- 定位目标 Rem（结果不进缓存！）
6. read-tree <id>       -- 展开子树 → 写入缓存（edit-tree 的前置）
7. read-rem <id>        -- 读取属性 → 写入缓存（edit-rem 的前置）
8. edit-rem / edit-tree -- 执行修改
9. disconnect           -- 结束会话（缓存全部清空，幂等）
```

**超时**：daemon 默认 30 分钟无 CLI 交互自动关闭，每次请求重置计时器。长时间操作间可用 health 保活。

---

## 4. 双模式 I/O（`--json`）

Agent 应始终使用 JSON 模式调用命令。

```bash
# 正确：位置参数 = JSON 字符串
remnote-bridge read-rem --json '{"remId":"kLrIOHJLyMd8Y2lyA","fields":["text","type"]}'
remnote-bridge search --json '{"query":"机器学习","numResults":10}'

# 错误：禁止混用裸 remId + --json
remnote-bridge read-rem kLrIOHJLyMd8Y2lyA --json   # 会失败！
```

注意：search 的 JSON 参数名是 `numResults`（不是 `limit`）。

### 中文搜索限制（重要）

search 调用 RemNote SDK 官方搜索方法，其分词基于空格分割。**中文、日文、韩文等无空格分词的语言搜索效果差**——SDK 将多字词拆为单字符 token 匹配，导致返回 0 结果或不相关结果。RemNote 本地桌面版已优化此问题，Web 版未优化。

**应对策略**：
1. 先用完整关键词搜索
2. 若返回 0 结果且关键词为中文等非空格语言：用**单个最具区分度的字**重试（如搜 "键" 而非 "共价键"）
3. 若仍无结果：改用 `read-globe` → `read-tree` 浏览定位
4. 搜索持续不佳时，询问用户："您使用的是 RemNote Web 版还是本地桌面版？Web 版中文搜索存在已知限制。"

### JSON 输出结构

```jsonc
{ "ok": true,  "command": "read-rem", ... }   // 成功
{ "ok": false, "command": "read-rem", "error": "..." }  // 失败
```

---

## 5. 安全机制：三道防线

### 防线 1：缓存存在性

必须先 read 再 edit。未缓存的 Rem 不允许编辑。

### 防线 2：乐观并发检测

edit 时从 SDK 重新读取最新数据，与缓存严格比较。被外部修改则拒绝编辑且**不更新缓存**——迫使 Agent 重新 read。

### 防线 3：str_replace 精确匹配

`oldStr` 必须在目标文本中恰好匹配 1 次。

### 缓存更新规则

| 场景 | 缓存行为 | Agent 操作 |
|:-----|:---------|:-----------|
| 写入成功 | 从 SDK 重新读取 → 更新缓存 | 可继续编辑 |
| 防线 2 拒绝 / 部分写入失败 | **不更新缓存** | 必须重新 read |
| 防线 3 拒绝 / JSON 语法错误 | 缓存保持不变 | 调整 oldStr/newStr 后**直接重试** |
| 操作执行中异常（edit-tree） | 已执行的操作保留（**无回滚**），不更新缓存 | 必须重新 read-tree |

---

## 6. Markdown 大纲格式

read-tree / read-globe / read-context 输出 Markdown 大纲，edit-tree 基于此大纲编辑。

### 缩进规则

**每级缩进 2 个空格**。根节点 0 空格，直接子节点 2 空格，孙节点 4 空格。缩进不可跳级（如从 0 直跳 4 空格会报 `indent_skip` 错误）。

### 行结构

```
{缩进}{前缀}{内容}{箭头}{backText} <!-- {remId} {元数据} -->
```

### 前缀

| 前缀 | 含义 |
|:-----|:-----|
| `# ` / `## ` / `### ` | H1/H2/H3 标题 |
| `- [ ] ` / `- [x] ` | 未完成/已完成待办 |
| `` `...` `` | 代码块 |
| `---` | 分隔线 |

### 箭头（编码 practiceDirection）

| 箭头 | 方向 | 格式 |
|:-----|:-----|:-----|
| ` → ` | forward | `text → backText` |
| ` ← ` | backward | `text ← backText` |
| ` ↔ ` | both | `text ↔ backText` |
| ` ↓ ` / ` ↓` | forward 多行 | 有 backText: `text ↓ backText`；无: `text ↓` |
| ` ↑ ` / ` ↑` | backward 多行 | 同上 |
| ` ↕ ` / ` ↕` | both 多行 | 同上 |

### 元数据标记

| 标记 | 含义 |
|:-----|:-----|
| `type:concept` / `type:descriptor` / `type:portal` | Rem 类型 |
| `doc` | isDocument = true |
| `top` | 知识库顶层 Rem |
| `children:N` | 折叠的子节点数（深度超限） |
| `role:card-item` | 多行闪卡答案行 |
| `tag:Name(id)` | 标签 |
| `refs:id1,id2` | Portal 引用 |

### 省略占位符（两种类型）

```
<!--...elided 3 siblings (parent:id range:2-4 total:5)-->     精确省略：maxSiblings 超限，调大 maxSiblings
<!--...elided >=10 nodes (parent:id range:5-14 total:20)-->   非精确省略：maxNodes 耗尽，调大 maxNodes
```

精确省略保留前 70% + 后 30%，中间插入省略行。**省略占位符不可删除或修改**，否则报 `elided_modified` 错误。

---

## 7. edit-tree 结构编辑

### 支持的操作

| 操作 | 方式 | 执行顺序 |
|:-----|:-----|:---------|
| 新增 | 在 newStr 中添加无 remId 的新行 | 1（从浅到深） |
| 移动 | 改变行的缩进/位置 | 2 |
| 重排 | 调换同级行顺序 | 3 |
| 删除 | 从 newStr 中移除带 remId 的行 | 4（从深到浅） |

一次 edit-tree 可组合多种操作。

### 禁止的操作

| 操作 | 错误类型 | 替代方案 |
|:-----|:---------|:---------|
| 修改已有行内容 | `content_modified` | 使用 `edit-rem` |
| 删除/修改/移动根节点 | `root_modified` | — |
| 删除有隐藏子节点的行 | `folded_delete` | 用更大 depth 重新 read-tree |
| 删除行但保留子节点 | `orphan_detected` | 必须同时删除所有子行 |
| 删除/修改省略占位符 | `elided_modified` | 用更大参数重新 read-tree |
| 缩进跳级 | `indent_skip` | 每级 2 空格，不可跳级 |

### 新增行格式

新增行可用 Markdown 前缀和箭头：

```markdown
  # 新标题
  新闪卡 → 答案
  问题 ↔ 回答
  - [ ] 新待办
  `代码块`
```

### 新增行指定类型/属性（metadata-only 注释）

新增行可在行尾添加 HTML 注释来指定 type、isDocument、tag，格式中不含 remId：

```markdown
  新概念 <!--type:concept-->
  新文档页 <!--type:concept doc-->
  带标签的描述 <!--type:descriptor tag:数学(tag01)-->
  多标记组合 <!--type:concept doc tag:基础(tag02) tag:数学(tag01)-->
```

支持的标记：`type:concept`、`type:descriptor`、`doc`、`tag:Name(id)`（可多个，空格分隔）。

### 新增 Portal

在 newStr 中用特殊格式创建 Portal：

```markdown
  <!--portal refs:id1,id2-->      创建 Portal 并引用 id1、id2
  <!--portal-->                   创建空 Portal
```

注意：与已有 Portal 行（`<!--remId type:portal refs:id1,id2-->`）不同，新增 Portal 以 `<!--portal` 开头，无 remId。Portal 不能通过 `edit-rem` 设 `type: "portal"` 创建，只能用此格式或 SDK `createPortal()`。

### 嵌套新增（一次创建父+子结构）

新增行下面可以再嵌套新增行，缩进表示父子关系：

```
newStr:
  父节点 ↓
    答案行 1
    答案行 2
  子节点 A <!--idA-->
```

创建顺序从浅到深，嵌套的子行会自动成为新创建父节点的 children。

### practiceDirection 保护

SDK bug 自动修复：移动行进入多行闪卡父节点时自动设 `isCardItem=true` 并修正 practiceDirection；移出时自动清除。Rem 自身的合法 practiceDirection 会被保留。

### str_replace 构造示例

```bash
# 在 idA 前插入新行
--old-str '  子节点 A <!--idA-->'
--new-str '  新增行\n  子节点 A <!--idA-->'

# 删除叶子节点（注意尾部换行）
--old-str '    叶子节点 <!--leaf-->\n'
--new-str ''

# 调换两个兄弟顺序
--old-str '  节点 A <!--idA-->\n  节点 B <!--idB-->'
--new-str '  节点 B <!--idB-->\n  节点 A <!--idA-->'
```

---

## 8. edit-rem str_replace 要点

操作对象是 `JSON.stringify(remObject, null, 2)` 的文本（缩进 2 空格的 JSON）。

### 使用技巧

1. **包含字段名**避免模糊匹配：`"\"type\": \"concept\""` 而非 `"concept"`
2. 替换后必须是合法 JSON
3. 修改 RichText 时注意 key 字母序：

```
oldStr: "\"text\": [\n    \"Hello\"\n  ]"
newStr: "\"text\": [\n    \"World\"\n  ]"
```

### 21 个可编辑字段

```
text, backText, type, isDocument, parent,
fontSize, highlightColor,
isTodo, todoStatus, isCode, isQuote, isListItem, isCardItem, isSlot, isProperty,
enablePractice, practiceDirection,
tags, sources, positionAmongstSiblings, portalDirectlyIncludedRem
```

### 特殊字段处理规则

| 字段 | 特殊行为 |
|:-----|:---------|
| `backText` | `null` → 调用 `setBackText([])`（清除背面）；裸字符串自动包装为 `[string]` |
| `highlightColor` | `null` → 调用 `removePowerup('h')`（SDK 不接受 null） |
| `fontSize` | `null` → 调用 `setFontSize(undefined)`（恢复普通大小） |
| `todoStatus` | 依赖 `isTodo=true` 才生效；`null` 被跳过（清除 todo 应设 `isTodo=false`） |
| `type` | 不可设为 `portal`（只能通过 SDK `createPortal()` 创建） |
| `parent` + `positionAmongstSiblings` | 共享同一 SDK 调用 `setParent(parentId, position)`，**应在同一次 str_replace 中同时修改** |
| `tags` / `sources` | **Diff 机制**：对比当前 vs 目标数组，逐项 add/remove。必须列出完整目标数组，缺少的会被删除 |
| `portalDirectlyIncludedRem` | Portal 专用可写。**Diff 机制**：对比当前 vs 目标数组，逐项 addToPortal/removeFromPortal。仅 type=portal 时可修改。edit-rem 对 Portal 使用 8 字段简化 JSON |

### 常用只读字段（修改只产生警告，不生效）

```
id, children, createdAt, updatedAt, remsReferencingThis, remsBeingReferenced,
aliases, descendants, siblingRem, isTable, portalType, propertyType
```

### read-rem 输出模式

| 模式 | 字段数 | 用法 |
|:-----|:-------|:-----|
| 默认 | 33（RW + R） | 常用场景 |
| Portal 简化 | 8（id, type, portalType, portalDirectlyIncludedRem, parent, positionAmongstSiblings, createdAt, updatedAt） | type=portal 时自动切换，`--full` 和 `--fields` 可覆盖 |
| `--full` | 51（含低频 R-F） | 需要 Powerup 标识、时间戳等 |
| `--fields` | 自选 + id | 精确获取特定字段 |

缓存始终存储完整 51 字段 RemObject，字段过滤仅影响输出。

---

## 9. 错误诊断速查

| 错误 | 原因 | 恢复 |
|:-----|:-----|:-----|
| 守护进程未运行 | 未 connect 或已超时 | `connect` |
| Plugin 未连接 | RemNote 未打开 | 打开 RemNote（health 三层：daemon→Plugin→SDK 链式依赖） |
| has not been read yet | 未先 read | 执行对应 read 命令（search 结果不算 read！） |
| has been modified since last read | 被外部修改 | 重新 read（必须，不可直接重试） |
| old_str not found | oldStr 不精确 | 检查引号、空格、换行、RichText key 顺序 |
| old_str matches N locations | oldStr 不够具体 | 扩大 oldStr 范围，包含更多上下文 |
| invalid JSON | newStr 破坏了 JSON 结构 | 检查引号、逗号、括号完整性（可直接重试） |
| content_modified | edit-tree 中改了行内容 | 用 edit-rem |
| orphan_detected | 删了父但留了子 | 同时删除所有子行 |
| folded_delete | 删了有隐藏子节点的行 | 用更大 depth 重新 read-tree |
| elided_modified | 删/改了省略占位符 | 用更大 depth/maxSiblings 重新 read-tree |
| indent_skip | 缩进跳级（如 0→4 空格） | 每级 2 空格，不可跳级 |
| children_captured | 新行劫持已有子节点 | 把新行插到兄弟末尾 |
| old_str not found in simplified Portal JSON | Portal 编辑时 oldStr 不匹配简化 JSON | 检查 Portal 简化 JSON 格式 |
| Rem not found | remId 无效或已删除 | 用 search 重新定位 |

---

## 10. 配置

配置文件：`~/.remnote-bridge/config.json`（全局目录，所有实例共享）

端口由槽位自动分配（槽位 0: 29100/29101/29102，槽位 1: 29110/29111/29112，以此类推），最多 4 个并发实例。

关键默认值：超时 30 分钟、maxNodes 200、maxSiblings 20、readTreeDepth 3、readGlobeDepth -1（无限）、缓存上限 200 条。
