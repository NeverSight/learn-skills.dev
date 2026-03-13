---
name: demand-mining
description: |
  需求挖掘助手，从社交平台（X/Twitter、Reddit、Hacker News 等）自动搜索和分析用户抱怨、痛点和未满足需求。
  用于发现产品机会、竞品分析、市场调研。

  触发场景：
  - 用户说"帮我挖掘 XX 领域/产品的用户需求"
  - 用户说"分析 XX 产品的用户抱怨"
  - 用户说"看看用户对 XX 有什么不满"
  - 用户说"找找 XX 领域的痛点"
  - 用户说"调研 XX 市场机会"
---

# Demand Mining - 需求挖掘

从社交平台挖掘用户真实声音，发现产品需求和市场机会。

## 工作流程

### Step 1: 明确挖掘目标

向用户确认：

1. **挖掘对象**: 特定产品（如 Notion、Figma）还是领域（如 AI 写作工具）
2. **竞品范围**: 是否分析竞品的用户反馈
3. **时间范围**: 近期（1个月）还是更长时间

### Step 2: 构建搜索策略

根据目标构建多维度搜索查询：

**抱怨类关键词（英文）:**

- `[product] sucks / hate / annoying / frustrating`
- `[product] problem / issue / bug`
- `switched from [product] / leaving [product]`
- `wish [product] could / [product] should`
- `[product] alternative / better than [product]`

**抱怨类关键词（中文）:**

- `[产品] 难用 / 垃圾 / 坑 / 吐槽`
- `[产品] 问题 / bug / 闪退`
- `弃用 [产品] / 从 [产品] 换到`
- `希望 [产品] 能 / [产品] 要是能`
- `[产品] 替代品 / 比 [产品] 好用`

**平台搜索策略:**

| 平台 | 搜索方式 | 特点 |
|------|----------|------|
| Reddit | `site:reddit.com [query]` | 深度讨论、真实反馈 |
| X/Twitter | `site:x.com [query]` 或 `site:twitter.com` | 即时吐槽、情绪强烈 |
| Hacker News | `site:news.ycombinator.com [query]` | 技术用户、专业观点 |
| V2EX | `site:v2ex.com [query]` | 中文技术社区 |
| 知乎 | `site:zhihu.com [query]` | 中文深度讨论 |
｜ 小红书 ｜ `site:xiaohongshu.com [query]` |  中文内容分享与电商平台 |

### Step 3: 执行搜索

使用 WebSearch 依次搜索各平台：

```
搜索示例：
1. site:reddit.com "notion" frustrating OR annoying OR sucks
2. site:x.com "notion" "switched to" OR "moving away"
3. site:reddit.com "notion" "wish it could" OR "should have"
```

对于有价值的帖子，使用 WebFetch 获取完整内容。

### Step 4: 分析与分类

将收集的用户声音按维度分类：

**分析框架（参见 [ANALYSIS_FRAMEWORK.md](references/ANALYSIS_FRAMEWORK.md)）:**

1. **功能缺失** - 用户想要但产品没有的功能
2. **体验问题** - 使用中的摩擦和痛点
3. **性能问题** - 速度、稳定性、兼容性
4. **定价问题** - 价格、性价比、付费模式
5. **竞品对比** - 用户为什么选择/离开

**分析维度:**

- 频次：多少人提到这个问题
- 情绪强度：轻微抱怨 vs 强烈不满
- 可操作性：能否转化为产品需求
- 市场机会：是否存在未被满足的市场

### Step 5: 生成报告

输出结构化 Markdown 报告（参见 [REPORT_TEMPLATE.md](references/REPORT_TEMPLATE.md)）。

## 输出格式

### 需求挖掘报告

```markdown
# [产品/领域] 需求挖掘报告

**生成时间**: YYYY-MM-DD
**数据来源**: Reddit, X, Hacker News, ...
**样本量**: 分析了 N 条用户反馈

## 核心发现

### Top 5 用户痛点

| 排名 | 痛点 | 频次 | 情绪强度 | 典型声音 |
|------|------|------|----------|----------|
| 1 | ... | 高 | 强烈 | "..." |

### 产品机会矩阵

| 机会点 | 用户需求 | 当前解决方案的不足 | 建议方向 |
|--------|----------|-------------------|----------|
| ... | ... | ... | ... |

## 详细分析

### 1. 功能缺失类

#### 1.1 [具体功能需求]
- **用户声音**: 原文引用
- **来源**: [平台链接]
- **分析**: 为什么用户需要这个
- **建议**: 可能的解决方案

### 2. 体验问题类
...

### 3. 定价问题类
...

### 4. 竞品洞察
...

## 行动建议

1. **立即可做**: ...
2. **中期规划**: ...
3. **需要调研**: ...

## 数据来源

| 平台 | 帖子数 | 链接汇总 |
|------|--------|----------|
| Reddit | N | [查看全部](...) |
```

## 最佳实践

1. **搜索多样性**: 使用多种关键词组合，避免遗漏
2. **原文引用**: 保留用户原话，避免过度解读
3. **注明来源**: 每条发现都标注出处链接
4. **量化呈现**: 用频次、比例说明问题普遍性
5. **可操作性**: 将痛点转化为具体产品建议

## 参考资料

- [ANALYSIS_FRAMEWORK.md](references/ANALYSIS_FRAMEWORK.md) - 完整分析框架和分类标准
- [REPORT_TEMPLATE.md](references/REPORT_TEMPLATE.md) - 报告模板详细说明
- [SEARCH_PATTERNS.md](references/SEARCH_PATTERNS.md) - 更多搜索关键词模式
