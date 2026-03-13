---
name: karpathy-rss-daily-briefing
description: Fetches Andrej Karpathy's curated RSS feed, reads ALL original articles, and generates a themed daily briefing document with citation links. This skill should be used when the user asks to generate a Karpathy RSS daily report, fetch Karpathy's curated RSS updates, or create an AI/tech daily briefing based on Karpathy's sources. Trigger phrases include "Karpathy 日报", "Karpathy RSS", "生成日报", "RSS briefing", "Karpathy daily".
---

# Karpathy 精选 RSS 日报生成

基于 Andrej Karpathy 精选的 RSS 信源，自动抓取**全部**条目、阅读原文、按主题合并排序，生成结构化中文日报。

## Language
**Match user's language**: Respond in the same language the user uses.

## 数据源

RSS Pack 地址：`https://youmind.com/rss/pack/andrej-karpathy-curated-rss`

## How It Works / 工作流程

按以下步骤顺序执行，完成每步后勾选对应项，再进入下一步。

Progress:
- [ ] Step 1: 获取 RSS 内容
- [ ] Step 2: 创建素材组
- [ ] Step 3: 全量深度阅读
- [ ] Step 4: 主题合并、排序与日报生成

### Step 1：获取 RSS 内容

使用 WebFetch 工具抓取 RSS feed：

```
URL: https://youmind.com/rss/pack/andrej-karpathy-curated-rss
```

解析返回的 RSS XML/JSON，提取过去 24 小时内的**全部**条目。记录每条的：
- 标题（title）
- 链接（link）
- 发布时间（pubDate）
- 信源名称（source/feed name）
- 摘要（description/summary）

### Step 2：创建素材组

创建素材组文件，命名格式：

```
YYYY-MM-DD - Karpathy 精选 RSS 日报素材
```

将 Step 1 获取的**全部** RSS 条目按信源分组归入此素材组，不做筛选。

### Step 3：全量深度阅读

对**每一条** RSS 条目，使用 WebFetch 工具阅读原文链接，获取文章全文或核心段落。不做筛选，全部阅读。记录：
- 文章核心观点
- 关键数据/发现
- 引用链接

若原文链接 404 或无法访问，使用 RSS 摘要作为替代并标注。

可并行发起多个 WebFetch 请求以提升效率。

### Step 4：主题合并、排序与日报生成

将**全部**条目按主题进行聚合：
1. **合并**：相同或强相关主题的多篇文章合并到同一 section
2. **排序**：按相关性和重要性排列，核心 AI/技术话题在前，低相关话题（书评、历史回顾、非技术内容等）放在后面
3. **生成**：输出日报 document，命名格式：

```
YYYY-MM-DD - Karpathy 精选 RSS 日报
```

## 日报模板

严格遵循以下模板结构生成日报内容：

```markdown
> Andrej Karpathy 精选的信源资讯汇总 | 共 [N] 条更新

---

## 🔥 核心主题：【主题标题】

【基于原文阅读的合并描述，包含关键观点、数据和发现】

- 来源：[文章标题1](原文链接1)
- 来源：[文章标题2](原文链接2)

## {emoji}【主题 2】：【副标题】

【合并描述】

- 来源：[文章标题](原文链接)

...（更多主题，按相关性降序排列）

---

## 📊 今日数据

- **XX** 条 RSS 更新
- **XX** 篇深度阅读
- **XX** 个主题：AA、BB、CC

## 💡 编者观察

【对今日整体趋势的简要评论，2-3 句话】

---

*本日报由 AI 自动生成 | 数据源：*[Andrej Karpathy curated RSS](https://youmind.com/rss/pack/andrej-karpathy-curated-rss)
```

### 模板规则

- **全量覆盖**：每一条 RSS 更新都必须出现在日报中，不遗漏
- 相同主题的多篇文章合并到同一 section，分别列出引用链接
- 按**相关性排序**：AI/ML/技术核心话题靠前，泛科技话题居中，非技术内容（书评、历史、文化等）靠后
- 每个主题用合适的 emoji 开头（🔥 用于最核心主题，其余自选）
- "今日数据"中的数字必须与实际内容一致
- 所有引用必须附带原文链接
- 日报语言为中文，专有名词保留英文

## 完成报告

日报生成完毕后，输出以下结构化报告：

```
[Karpathy RSS 日报] 完成！
日期：YYYY-MM-DD
RSS 条目：XX 条
深度阅读：XX 篇
合并主题：XX 个
输出文档：YYYY-MM-DD - Karpathy 精选 RSS 日报
```
