---
name: zhihu-html
description: "将 Markdown 转换为知乎编辑器兼容的 HTML。脚本处理确定性格式转换，AI 处理引用标记的 data-text 描述。Use this skill when: 用户要求生成知乎格式/知乎 HTML、将 Markdown 转为可粘贴到知乎编辑器的 HTML、提到知乎发文/排版/专栏、需要将带链接的文章转换为知乎 sup 引用格式。"
---

# Zhihu HTML Converter

将 Markdown 转换为知乎编辑器兼容的 HTML。

## ⚠️ 路径解析（重要）

本 skill 的脚本位于 SKILL.md 所在目录下。执行任何脚本之前，**必须**先确定本文件的实际路径，并以此推导脚本目录。

**规则：** 以下文档中所有 `$SKILL_DIR` 占位符应替换为本 SKILL.md 文件所在的目录路径。

例如：如果本文件位于 `/Users/xxx/Desktop/AI/skills/zhihu-html/SKILL.md`，则 `$SKILL_DIR` = `/Users/xxx/Desktop/AI/skills/zhihu-html`。

```bash
SKILL_DIR="<本 SKILL.md 文件所在目录的绝对路径>"
```

---

## Quick Start

### 从 Markdown 文件转换

```bash
node "$SKILL_DIR/scripts/convert.mjs" --input article.md --output article.html
```

### 从 stdin 读取

```bash
echo "# 标题\n\n段落内容" | node "$SKILL_DIR/scripts/convert.mjs" --output article.html
```

### 输出到 stdout

```bash
node "$SKILL_DIR/scripts/convert.mjs" --input article.md
```

---

## 链接处理配置

支持区分站内链接和站外链接的处理方式：

- **站内链接**：转换为普通 `<a>` 标签
- **站外链接**：转换为知乎 `<sup>` 引用格式（需要 AI 生成 data-text）

### 配置方式

在 `scripts/extract-refs.mjs` 文件中修改 `LINK_CONFIG` 对象：

```javascript
const LINK_CONFIG = {
  enabled: true,
  internalDomains: [
    'zhihu.com'  // 会匹配 zhihu.com 及其所有子域名
  ],
  internalPatterns: [
    // 可选：添加正则表达式模式进行更精确的匹配
    // '^https://www\\.zhihu\\.com/question/\\d+',
    // '^https://zhuanlan\\.zhihu\\.com/p/\\d+'
  ]
};
```

### 配置说明

- `enabled`: 是否启用链接区分功能（默认 `true`）
- `internalDomains`: 站内域名列表，支持子域名匹配
  - 例如 `"zhihu.com"` 会匹配 `zhihu.com`、`www.zhihu.com`、`zhuanlan.zhihu.com` 等
- `internalPatterns`: 站内链接的正则表达式模式列表
  - 用于更精确的 URL 匹配

### 默认行为

默认配置将 `zhihu.com` 域名下的所有链接视为站内链接，其他链接视为站外链接。

---

## Workflow

本 skill 分三步流水线工作，AI 只需处理精简的引用 JSON，无需阅读完整 HTML：

**Step 1: 转换 Markdown → 知乎 HTML（含占位标记）**

```bash
node "$SKILL_DIR/scripts/convert.mjs" -i article.md -o article.html
```

脚本处理所有确定性的格式转换。所有链接输出为 `<!-- REF:N ... -->` 占位标记。

**Step 2: 提取引用列表（给 AI 看的精简 JSON）**

```bash
node "$SKILL_DIR/scripts/extract-refs.mjs" -i article.md -o refs.json
```

提取所有链接，并根据内置配置标记类型（internal/external）。输出示例：
```json
[
  {
    "numero": 1,
    "url": "https://www.zhihu.com/question/12345",
    "originalText": "知乎问题",
    "context": "这里有一个知乎问题的链接。",
    "type": "internal",
    "dataText": ""
  },
  {
    "numero": 2,
    "url": "https://www.langchain.com/report",
    "originalText": "报告",
    "context": "LangChain 的调查报告显示，超过 50% 的开发者已经在使用 Agent。",
    "type": "external",
    "dataText": ""
  }
]
```

AI 根据 `url`、`originalText`、`context` 信息（也可访问 URL 获取页面标题），
为 `type: "external"` 的引用填写 `dataText` 字段。站内链接（`type: "internal"`）不需要填写 `dataText`。

**AI 生成 data-text 的规则：**
- 优先使用中文描述，如"阿里云：AI Agent的工程化被低估了"
- 学术论文保持英文原名，如"Why Do Multi-Agent LLM Systems Fail?"
- 官方文档可用"XXX 官方文档"格式
- 简洁明了，让读者看到标题就知道引用了什么

**Step 3: 应用引用 → 生成最终 HTML**

```bash
node "$SKILL_DIR/scripts/apply-refs.mjs" -i article.html -r refs.json -o final.html
```

脚本将 HTML 中的 `<!-- REF:N ... -->` 占位标记替换为：
- `type: "internal"` → `<a href="...">文字</a>`
- `type: "external"` → `文字<sup ...>[N]</sup>`

不指定 `-o` 时默认覆盖输入文件。

---

## 知乎 HTML 规范

### 允许的标签
- `<h1>` — 文章标题（仅一个）
- `<h2>` — 章节标题
- `<p>` — 段落
- `<b>` — 加粗
- `<code>` — 行内代码
- `<a>` — 站内超链接（需配置）
- `<sup data-text="..." data-url="..." ...>` — 站外引用/超链接

### 保留的标签
- `<ul>` `<ol>` `<li>` — 列表
- `<table>` `<thead>` `<tbody>` `<tr>` `<th>` `<td>` — 表格
- `<pre><code>` — 代码块
- `<img>` — 图片

### 禁用的标签
- 不使用 `<h3>` 及以下层级标题（降级为 `<p><b>...</b></p>`）
- 不使用 `<blockquote>` 引用标签（降级为 `<p>`）
- 不使用 `<hr>` 分割线
- 站外链接不使用 `<a>` 标签（使用 `<sup>` 引用格式）

### 超链接格式

知乎对超链接有两种处理方式：

1. **站内链接**（需配置）：保留为普通 `<a>` 标签
```html
<a href="https://zhuanlan.zhihu.com/p/123456">文章标题</a>
```

2. **站外链接**（默认）：转换为 `<sup>` 引用格式
```html
<sup data-text="描述标题" data-url="链接地址" data-draft-node="inline" data-draft-type="reference" data-numero="序号">[序号]</sup>
```

- `data-text` 由 AI 根据上下文和 URL 内容生成（见 Workflow Step 2）
- 编号按首次出现顺序从 1 递增
- 同一链接多次出现时保持首次编号

### 段落规范
- 每段用 `<p>` 包裹
- 不使用 `<br>` 换行，拆成多个 `<p>`
- `<sup>` 紧跟被引用内容，不加空格

---

## Options

### convert.mjs

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input` | 输入 Markdown 文件 | stdin |
| `-o, --output` | 输出 HTML 文件 | stdout |
| `--wrap` | 用完整 HTML 文档包裹（含 meta charset） | off |

### extract-refs.mjs

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input` | 输入 Markdown 文件 | required |
| `-o, --output` | 输出 JSON 文件 | stdout |

### apply-refs.mjs

| Option | Description | Default |
|--------|-------------|---------|
| `-i, --input` | 含占位标记的 HTML 文件 | required |
| `-r, --refs` | AI 填写后的引用 JSON 文件 | required |
| `-o, --output` | 输出最终 HTML 文件 | 覆盖 input |

---

## Markdown 到知乎 HTML 对照

| Markdown | 知乎 HTML |
|----------|-----------|
| `# 标题` | `<h1>标题</h1>` |
| `## 标题` | `<h2>标题</h2>` |
| `**加粗**` | `<b>加粗</b>` |
| `` `代码` `` | `<code>代码</code>` |
| `[文字](站内链接)` | `<a href="站内链接">文字</a>`（需配置） |
| `[文字](站外链接)` | 脚本输出 `文字<!-- REF:N url="站外链接" text="文字" -->`，AI 替换为 `文字<sup ...>[N]</sup>` |
| 段落 | `<p>段落</p>` |
| `### 三级标题` | 转为 `<p><b>三级标题</b></p>` |
| 列表 | 保留 `<ul>/<ol>/<li>` |
| 表格 | 保留 `<table>` |
| 代码块 | 保留 `<pre><code>` |
| 图片 | 保留 `<img>` |
| `---` | 忽略 |
| `> 引用` | 转为 `<p>` 段落 |

---

## 示例

### 输入 (Markdown)

```markdown
# AI Agent 的未来

**AI Agent** 正在改变软件开发的方式。

## 背景

LangChain 的调查 [报告](https://www.langchain.com/report) 显示，
超过 50% 的开发者已经在使用 Agent。

另一项研究 [论文](https://arxiv.org/paper) 也证实了这一趋势。

在[知乎上的讨论](https://www.zhihu.com/question/123456)中，
很多开发者分享了他们的实践经验。

## 技术实现

关于具体的实现方式，可以参考 [OpenAI 的官方文档](https://platform.openai.com/docs)。

同时，[这篇知乎专栏文章](https://zhuanlan.zhihu.com/p/654321) 也提供了很好的中文教程。

## 结论

前面提到的 [报告](https://www.langchain.com/report) 还发现了更多有趣的数据。
```

### 输出 (知乎 HTML)

Phase 1 脚本输出（含占位标记）：

```html
<h1>AI Agent 的未来</h1>
<p><b>AI Agent</b> 正在改变软件开发的方式。</p>
<h2>背景</h2>
<p>LangChain 的调查 <!-- REF:1 url="https://www.langchain.com/report" text="报告" --> 显示，超过 50% 的开发者已经在使用 Agent。</p>
<p>另一项研究 <!-- REF:2 url="https://arxiv.org/paper" text="论文" --> 也证实了这一趋势。</p>
<p>在<!-- REF:3 url="https://www.zhihu.com/question/123456" text="知乎上的讨论" -->中，很多开发者分享了他们的实践经验。</p>
<h2>技术实现</h2>
<p>关于具体的实现方式，可以参考 <!-- REF:4 url="https://platform.openai.com/docs" text="OpenAI 的官方文档" -->。</p>
<p>同时，<!-- REF:5 url="https://zhuanlan.zhihu.com/p/654321" text="这篇知乎专栏文章" --> 也提供了很好的中文教程。</p>
<h2>结论</h2>
<p>前面提到的 <!-- REF:1 url="https://www.langchain.com/report" text="报告" --> 还发现了更多有趣的数据。</p>
```

Phase 2 提取的引用 JSON（AI 需要填写 external 类型的 dataText）：

```json
[
  {
    "numero": 1,
    "url": "https://www.langchain.com/report",
    "originalText": "报告",
    "context": "LangChain 的调查 [报告]...",
    "type": "external",
    "dataText": ""  // AI 填写
  },
  {
    "numero": 3,
    "url": "https://www.zhihu.com/question/123456",
    "originalText": "知乎上的讨论",
    "context": "在[知乎上的讨论]...",
    "type": "internal",
    "dataText": ""  // 站内链接不需要填写
  }
]
```

Phase 3 AI 处理后的最终输出：

```html
<h1>AI Agent 的未来</h1>
<p><b>AI Agent</b> 正在改变软件开发的方式。</p>
<h2>背景</h2>
<p>LangChain 的调查 报告<sup data-text="LangChain：Agent 工程现状调查报告" data-url="https://www.langchain.com/report" data-draft-node="inline" data-draft-type="reference" data-numero="1">[1]</sup> 显示，超过 50% 的开发者已经在使用 Agent。</p>
<p>另一项研究 论文<sup data-text="Why Do Multi-Agent LLM Systems Fail?" data-url="https://arxiv.org/paper" data-draft-node="inline" data-draft-type="reference" data-numero="2">[2]</sup> 也证实了这一趋势。</p>
<p>在<a href="https://www.zhihu.com/question/123456">知乎上的讨论</a>中，很多开发者分享了他们的实践经验。</p>
<h2>技术实现</h2>
<p>关于具体的实现方式，可以参考 OpenAI 的官方文档<sup data-text="OpenAI Platform Documentation" data-url="https://platform.openai.com/docs" data-draft-node="inline" data-draft-type="reference" data-numero="4">[4]</sup>。</p>
<p>同时，<a href="https://zhuanlan.zhihu.com/p/654321">这篇知乎专栏文章</a> 也提供了很好的中文教程。</p>
<h2>结论</h2>
<p>前面提到的 报告<sup data-text="LangChain：Agent 工程现状调查报告" data-url="https://www.langchain.com/report" data-draft-node="inline" data-draft-type="reference" data-numero="1">[1]</sup> 还发现了更多有趣的数据。</p>
```

---

## File structure

### scripts/
- `convert.mjs` — Markdown → 知乎 HTML（含占位标记）
- `extract-refs.mjs` — 从 Markdown 提取引用列表 + 上下文，输出 JSON
- `apply-refs.mjs` — 用 AI 填写的 JSON 替换 HTML 中的占位标记，生成最终 HTML

### assets/
- `example.md` — 示例 Markdown 输入
- `example.html` — 对应的知乎 HTML 输出（含占位标记）
