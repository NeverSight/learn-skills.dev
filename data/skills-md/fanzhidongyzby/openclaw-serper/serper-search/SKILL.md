---
name: serper-search
description: 使用 Google Serper Search API 进行网络搜索。当用户说"搜索"、"搜一下"、"查找"、"研究"、"调研"、"了解"、"查询"、"检索"时使用。
---

# Google Serper Search Tool

基于 Google Serper API 的网页搜索工具，提供实时、准确的搜索结果。

## When to Activate

当用户提到以下内容时自动激活：

### 搜索类关键词
- "搜索"、"搜一下"、"搜搜"、"查找"、"找一下"
- "研究"、"调研"、"了解"
- "查询"、"检索"
- "看看"、"查查"

### 特定场景
- 需要获取最新新闻、信息
- 需要验证事实或数据
- 需要研究某个技术或概念
- 需要查找文档、教程
- 需要比较不同产品或方案

### 示例问题
- "搜一下最新的 AI 发展趋势"
- "帮我搜索最新的 AI 发展趋势"
- "查找一下 Python 3.13 的新特性"
- "研究一下自动驾驶技术的现状"
- "查查最新的网络安全新闻"
- "找一些关于微服务的教程"

## Tools

### serper_search

**用途：** 执行网络搜索，返回结果列表

**参数：**
- `query` (必选，string)：搜索关键词
- `num` (可选，number)：返回结果数量，默认 5，最大 20
- `gl` (可选，string)：国家代码，默认 cn
- **推荐值：** cn（中国）、us（美国）、uk（英国）、jp（日本）
- `hl` (可选，string)：语言代码，默认 zh-CN
- **推荐值：** zh-CN（简体中文）、en（英文）、ja（日语）

## Best Practices

### 1. 搜索技巧

使用具体的关键词，避免过于宽泛：

**示例：**
- ✅ "Kimi AI 模型 参数 对比 2025"
- ✅ "Python 3.13 新特性 官方文档"
- ❌ "Python"（太宽泛，结果太多）

### 2. 添加时间限定

明确时间范围，获取最新信息：

**示例：**
- ✅ "LangChain 最新文档 2025"
- ✅ "Python 3.13 发布时间"
- ✅ "AI 人工智能 新闻 2025年2月"

### 3. 使用精确搜索

用引号搜索精确短语：

**示例：**
- ✅ "\"machine learning\" 最佳实践"
- ✅ "\"RAG 架构\" 实现"

### 4. 添加技术术语

提高搜索精度：

**示例：**
- ✅ "Spring Cloud 微服务 实现"
- ✅ "React Hooks useEffect 使用"

### 5. 结果数量选择

根据需求调整：
- **快速查询：** `num=3`（快速浏览核心信息）
- **深入研究：** `num=10`（全面了解主题）
- **综合调研：** `num=20`（最大深度，覆盖面广）

### 6. 多轮搜索策略

对于复杂主题，使用多轮搜索深入挖掘：

**场景：研究微服务架构**

```javascript
// 第一轮：基础概念
serper_search({ query: "微服务架构 概念 优势", num: 5 })

// 第二轮：技术实现
serper_search({ query: "微服务 Spring Cloud Kubernetes", num: 8 })

// 第三轮：最佳实践
serper_search({ query: "微服务 最佳实践 常见问题", num: 10 })
```

### 7. 结果处理原则

- **优先权威来源：** 官方文档、知名技术博客、学术论文
- **交叉验证：** 对比多个来源的信息
- **关注时效性：** 优先较新的内容（近1-2年）
- **快速筛选：** 通过 snippet 判断相关性

## Example Scenarios

### 场景 1：技术调研

**用户提问：** "研究一下 LangChain 的核心概念"

**AI 行为：**
```javascript
// 搜索核心概念
serper_search({
  query: "LangChain 核心概念 官方文档 2025",
  num: 5
})

// 如果需要更多细节，继续搜索
serper_search({
  query: "LangChain Agents Chains 使用示例",
  num: 8
})
```

**回复示例：**
```
根据搜索结果，LangChain 的核心概念包括：

1. **Chains（链）**：将多个组件串联成工作流
2. **Agents（智能体）**：自主决策的 AI 代理
3. **Tools（工具）**：LLM 可用的外部能力
4. **Memory（记忆）**：对话上下文管理

📖 详细文档：https://python.langchain.com/
```

### 场景 2：新闻获取

**用户提问：** "今天有什么 AI 新闻？"

**AI 行为：**
```javascript
serper_search({
  query: "AI 人工智能 新闻 2025年2月6日",
  num: 10
})
```

**回复示例：**
```
今日 AI 要闻：

1. **OpenAI 发布新模型**：能力提升 30%
2. **Google DeepMind**：突破蛋白质折叠新算法
3. **中国 AI 监管**：新规发布，促进行业健康发展

🔍 来源：各大科技媒体报道
```

### 场景 3：产品比较

**用户提问：** "Kimi 和 ChatGPT 哪个更好？"

**AI 行为：**
```javascript
// 搜索对比评测
serper_search({
  query: "Kimi ChatGPT 对比评测 2025",
  num: 5
})
```

**回复示例：**
```
根据评测对比：

| 特性 | Kimi | ChatGPT |
|------|------|---------|
| 中文理解 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 工具调用 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 响应速度 | 快 | 中等 |

💡 建议：中文任务用 Kimi，复杂工具调用用 ChatGPT
```

### 场景 4：事实验证

**用户提问：** "听说 Python 4 要发布了，是真的吗？"

**AI 行为：**
```javascript
serper_search({
  query: "Python 4 发布计划 官方声明",
  num: 5
})
```

**回复示例：**
```
经核实：

❌ Python 4 目前没有发布计划
✅ Python 3.13 是最新版本（2024年10月发布）
✅ Python 3.14 计划于 2025 年发布

📊 信息来源：Python 官方 GitHub、PSF 公告
```

### 场景 5：快速查找

**用户提问：** "帮我找一个 React Hooks 的教程"

**AI 行为：**
```javascript
serper_search({
  query: "React Hooks 官方教程 中文",
  num: 3
})
```

**回复示例：**
```
推荐教程：

1. 📚 **React 官方文档**（推荐）
   https://react.dev/learn

2. 🎓 **阮一峰 React Hooks 教程**
   https://www.ruanyifeng.com/blog/2019/09/react-hooks.html

3. 📺 **B站 React Hooks 视频教程**
   搜索"React Hooks 入门"
```

## Limitations

- **搜索结果来源：** Google，可能受地区和个性化影响
- **访问限制：** 某些网站可能被屏蔽或需要登录
- **结果数量：** 最多 20 条
- **速率限制：** API 有调用频率限制，避免短时间内大量请求
- **搜索质量：** 取决于关键词的准确性和时机

## Configuration

### 环境变量配置（推荐）

编辑 `~/.openclaw/.env`：

```bash
SERPER_API_KEY=your-api-key-here
```

### 插件配置

在 `openclaw.plugin.json` 的 `configSchema` 中配置 `apiKey`。

### 获取 API Key

访问 [https://serper.dev/](https://serper.dev/) 注册并获取 API Key。

免费额度：每月 2,500 次调用。

## Related Tools

- **web_search：** Brave Search API（备选方案）
- **web_fetch：** 获取单个网页的详细内容

## Version History

- **v1.0** (2026-02-06)：初始版本，基础搜索功能
  - 支持 Google Serper API
  - 提供中文、英文多语言搜索
  - 集成 OpenClaw Skill 系统

- **v1.1** (2026-02-11)：优化 description，添加触发关键词
  - 更新 description 包含触发关键词
  - 优化 skill 激活机制

## Future Plans

- 📚 **serper-scholar**：学术搜索支持
- 🔍 **高级筛选**：时间范围、域名过滤
- 📊 **结果缓存**：提升重复查询性能
- 🌍 **更多地区**：支持更多国家和语言

---

**Tips：** 使用搜索时，尽量用自然语言表达你的需求，AI 会自动帮你构建合适的搜索查询。