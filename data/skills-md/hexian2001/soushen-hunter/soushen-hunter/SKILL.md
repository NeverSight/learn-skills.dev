---
name: soushen-hunter
description: |
  高性能 Bing/Google 搜索引擎 Skill - "搜神猎手"
  使用 Playwright 底层 API 进行深度网页搜索和元素提取

  功能：
  1. Bing/Google 搜索执行 - 返回结构化搜索结果（标题、链接、摘要、来源）
  2. 深度页面分析 - 提取页面的所有关键元素（链接、表单、按钮、脚本、元数据）
  3. 可配置搜索引擎 - 支持 Bing 和 Google 切换

  触发条件：
  - 用户需要进行网络搜索时
  - 需要提取网页结构信息（链接、表单等）时
  - 需要无 API 成本的搜索解决方案时

  使用方法：
  - 基础搜索：./soushen "搜索关键词" [--num N] [--engine ENGINE]
  - 深度分析：./soushen --deep <目标 URL>
  - 配置引擎：./soushen --set-default-engine bing|google
---

# 搜神猎手 (SouShen Hunter) - 搜索引擎 Skill

高性能 Bing/Google 搜索引擎，基于 Playwright 实现深度网页信息提取。

## 核心功能

### 1. Bing/Google 搜索
执行搜索并返回结构化结果：
- 标题、URL、摘要、来源网站
- 支持 Bing 和 Google 双引擎
- 可配置结果数量
- 支持中文和英文搜索

### 2. 深度页面分析
对指定 URL 进行深度扫描，提取：
- **所有链接**：文本、href、类型
- **表单信息**：action、method、输入字段
- **按钮元素**：文本、类型、动作
- **外部脚本**：JS 文件 URL 列表
- **页面元数据**：meta tags、Open Graph 等

## 使用方法

### 基础搜索（推荐）
```bash
# 使用默认搜索引擎
./soushen "OpenClaw AI Agent"

# 指定结果数量
./soushen "AI 人工智能" --num 20

# 指定搜索引擎
./soushen "AI" --engine google
```

### 深度页面分析
```bash
./soushen --deep https://example.com
```

### 配置
```bash
# 设置默认搜索引擎
./soushen --set-default-engine bing
./soushen --set-default-engine google

# 查看当前配置
./soushen --config
```

### Python API
```python
# Bing 搜索
from bing_search import BingSearchAgent

async with BingSearchAgent(headless=True) as agent:
    results = await agent.search("关键词", num_results=10)

# Google 搜索
from google_search import GoogleSearchAgent

async with GoogleSearchAgent(headless=True) as agent:
    results = await agent.search("关键词", num_results=10)

# 深度分析
elements = await agent.extract_page_elements("https://example.com")
```

## 依赖要求

- Python 3.8+
- playwright (`pip install playwright`)
- Chrome/Chromium 浏览器

## 配置说明

脚本默认查找以下 Chrome 路径：
- `/root/ezisall/chrome-linux64/chrome`（项目自带）
- `~/.local/bin/chrome-for-testing-dir/chrome`
- `/usr/bin/google-chrome`
- `/usr/bin/chromium`

可通过环境变量自定义：
```bash
export CHROME_PATH=/usr/bin/google-chrome
```

## 反检测特性

### Bing
- 禁用自动化控制标记
- 模拟真实用户代理
- 设置合理视口大小

### Google（高级）
- 用户数据目录复用（保留 Cookie 和会话）
- 浏览器指纹伪装（隐藏 webdriver 特征）
- 行为模拟（随机延迟、鼠标移动）
- 多用户代理轮换
- 地理位置模拟

## 注意事项

- Google 搜索可能遇到人机验证，建议：
  - 使用有登录状态的 Chrome 配置
  - 控制搜索频率（每分钟不超过 5-10 次）
  - 遇到验证时切换到 Bing
