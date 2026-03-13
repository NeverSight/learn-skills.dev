---
name: browser-agent
description: AI 驱动的浏览器自动化工具集，包含 agent-browser（无障碍树提取）、actionbook（50+ 网站自动化食谱）、browser-use（Python 自动化库）。使用场景：(1) 抓取需要 JS 渲染的网页内容 (2) 从 X/Twitter、GitHub、Reddit 等平台获取数据 (3) 截图网页 (4) 自动化浏览器操作 (5) 获取网页的无障碍树结构。当用户需要访问动态网页、绕过反爬虫、或执行浏览器自动化时使用此技能。
---

# Browser Agent

AI Agent 浏览器自动化工具集，提供三种互补的工具用于网页数据获取和自动化操作。

## 工具选择指南

```
用户请求
    │
    ├── 简单抓取静态内容？
    │   └── 用 curl / WebFetch（更快）
    │
    ├── 需要 JS 渲染 / 绕过反爬？
    │   ├── agent-browser ── 提取无障碍树
    │   │
    │   ├── 截图？ ── agent-browser -s
    │   │
    │   └── 目标网站在 actionbook 列表？
    │       └── actionbook get <site> ── 获取专用食谱
    │
    └── 复杂多步骤自动化？
        └── browser-use (Python) ── AI 驱动自主操作
```

## agent-browser

CLI 工具，使用 Playwright 启动无头浏览器并提取页面的无障碍树（Accessibility Tree）。

**核心优势**：
- 无需登录即可访问大部分内容
- 获取结构化的可读文本
- 支持截图
- 自动处理 JS 渲染

### 基本用法

```bash
# 提取网页内容（无障碍树）
agent-browser <URL>

# 截图
agent-browser -s <URL>

# 指定输出格式
agent-browser -f markdown <URL>
agent-browser -f html <URL>
agent-browser -f text <URL>

# 交互模式（可点击、滚动）
agent-browser -i <URL>

# 指定浏览器
agent-browser --browser chromium <URL>
agent-browser --browser firefox <URL>
```

### 常见场景

```bash
# 获取 X/Twitter 帖子内容
agent-browser "https://x.com/username/status/123456"

# 获取 GitHub 仓库信息
agent-browser "https://github.com/owner/repo"

# 获取 Reddit 帖子
agent-browser "https://reddit.com/r/subreddit/comments/abc123"

# 获取新闻文章（JS 渲染）
agent-browser "https://example.com/article"
```

**详细命令参考**: [references/agent-browser-reference.md](references/agent-browser-reference.md)

## actionbook

50+ 网站的预计算自动化"食谱"，提供经过验证的自动化模板。

### 基本用法

```bash
# 列出所有支持的网站
actionbook list

# 获取特定网站的食谱
actionbook get <site>

# 示例
actionbook get github
actionbook get reddit
actionbook get amazon
```

### 工作流程

1. 运行 `actionbook list` 查看支持的网站
2. 运行 `actionbook get <site>` 获取该网站的自动化模板
3. 根据模板编写自动化脚本（使用 browser-use 或直接使用 agent-browser）

**详细命令参考**: [references/actionbook-reference.md](references/actionbook-reference.md)

## browser-use

Python 库，使用 AI 自主控制浏览器完成复杂任务。

### 安装

```bash
pip install browser-use
playwright install chromium
```

### 基本用法

```python
from browser_use import Agent
from langchain_openai import ChatOpenAI

async def main():
    agent = Agent(
        task="Go to GitHub and find the trending Python repositories",
        llm=ChatOpenAI(model="gpt-4"),
    )
    result = await agent.run()
    print(result)
```

### 常见场景

```python
# 表单填写
agent = Agent(
    task="Go to example.com and fill out the contact form with test data",
    llm=llm,
)

# 数据抓取
agent = Agent(
    task="Go to Amazon, search for 'wireless headphones', and extract the top 5 products with prices",
    llm=llm,
)

# 多步骤操作
agent = Agent(
    task="Log into Twitter, navigate to settings, and enable two-factor authentication",
    llm=llm,
)
```

**详细 API 参考**: [references/browser-use-reference.md](references/browser-use-reference.md)

## 决策流程

### 任务类型 → 工具选择

| 任务类型 | 推荐工具 | 原因 |
|---------|---------|------|
| 快速抓取单个页面 | agent-browser | 简单直接，无障碍树输出 |
| 需要页面截图 | agent-browser -s | 内置截图功能 |
| 目标网站在 actionbook 中 | actionbook + browser-use | 有现成的最佳实践 |
| 复杂多步骤操作 | browser-use | AI 自主决策和执行 |
| 需要登录的网站 | browser-use | 可以处理登录流程 |
| 批量数据采集 | browser-use | 支持循环和条件判断 |

### 示例工作流

**场景：获取 X/Twitter 帖子内容**

```bash
# 方法 1：直接使用 agent-browser（推荐）
agent-browser "https://x.com/username/status/123456"

# 方法 2：使用 browser-use 进行更复杂操作
# 编写 Python 脚本
```

**场景：GitHub Trending 分析**

```bash
# 方法 1：agent-browser
agent-browser "https://github.com/trending"

# 方法 2：使用 actionbook 获取 GitHub 食谱
actionbook get github
# 然后根据食谱编写脚本
```

## 注意事项

1. **速率限制**：频繁请求可能被目标网站封禁，建议添加延迟
2. **登录要求**：某些内容需要登录才能访问，使用 browser-use 处理
3. **动态内容**：agent-browser 会等待页面加载完成，但对于无限滚动页面需要交互模式
4. **法律合规**：确保抓取行为符合目标网站的服务条款

## 故障排除

| 问题 | 解决方案 |
|-----|---------|
| 页面加载超时 | 使用 `-t` 增加超时时间 |
| 内容未渲染 | 使用交互模式 `-i` 手动等待 |
| 反爬虫拦截 | 尝试不同的 user-agent 或使用 browser-use |
| 截图空白 | 确保页面完全加载后再截图 |
