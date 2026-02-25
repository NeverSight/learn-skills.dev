---
name: playwright_browser
description: 基于Playwright的高级浏览器自动化技能。支持动态网页抓取、点击/输入模拟、百度搜索、页面快照、数据提取和批量图片下载。当需要处理JavaScript渲染的页面、模拟用户交互或自动化网页操作时使用此技能。
---

# Playwright 浏览器自动化技能

此技能提供基于 Playwright 的完整浏览器自动化能力，支持在无头模式下执行复杂的网页交互任务。

## 核心功能

### 1. 基础浏览 (browser_tool.py)
访问网页、截图、读取 HTML 内容。
- 支持等待特定元素加载完成
- 支持全页截图和 HTML 内容预览
- 自动处理容器环境的 sandbox 限制

### 2. 数据抓取 (scraper.py)
使用 CSS 选择器精确提取网页数据。
- 支持单个和多个元素提取
- 支持提取文本或属性值
- JSON 格式输出，便于后续处理

### 3. 搜索功能 (search.py)
使用百度搜索引擎并返回结构化结果。
- 自动填充关键词并提交搜索
- 提取标题、链接、描述
- 支持自定义结果数量

### 4. 自动化交互 (automator.py)
执行复杂的操作链，模拟真实用户行为。
- 点击、输入、下拉选择
- 滚动、等待、执行 JavaScript
- 支持在关键步骤截图

### 5. 页面快照 (snapshot.py)
高质量页面截图和 PDF 导出。
- 全页或可视区域截图
- PDF 格式导出
- 自动生成缩略图

### 6. 图片批量下载 (download_images.py)
自动提取并下载网页中的所有图片。
- 智能提取所有 img 标签
- 根据 alt 或 title 生成文件名
- 支持自定义下载数量和输出目录
- 高质量原始图片下载

## 使用方法

### 基础浏览

访问网页并截图：
\`\`\`bash
python skills/playwright_browser/browser_tool.py --url https://example.com --screenshot --output example.png
\`\`\`

读取页面 HTML 内容：
\`\`\`bash
python skills/playwright_browser/browser_tool.py --url https://example.com --read
\`\`\`

等待特定元素加载：
\`\`\`bash
python skills/playwright_browser/browser_tool.py --url https://example.com --screenshot --wait .main-content
\`\`\`

### 数据抓取

提取单个元素文本：
\`\`\`bash
python skills/playwright_browser/scraper.py https://example.com --selector title:h1:text
\`\`\`

提取多个元素（如所有链接）：
\`\`\`bash
python skills/playwright_browser/scraper.py https://example.com --selector links:a:href:multiple --json
\`\`\`

提取特定属性：
\`\`\`bash
python skills/playwright_browser/scraper.py https://example.com --selector img_url:img:src
\`\`\`

### 百度搜索

搜索关键词：
\`\`\`bash
python skills/playwright_browser/search.py "搜索关键词" --max 10
\`\`\`

JSON 格式输出：
\`\`\`bash
python skills/playwright_browser/search.py "搜索关键词" --json > results.json
\`\`\`

### 自动化交互

使用 JSON 配置文件：
\`\`\`bash
python skills/playwright_browser/automator.py https://example.com --file actions.json
\`\`\`

直接传入操作链：
\`\`\`bash
python skills/playwright_browser/automator.py https://example.com --actions '[{"type":"fill","selector":"#input","value":"test"},{"type":"click","selector":"#submit"}]'
\`\`\`

actions.json 示例：
\`\`\`json
[
  {"type": "wait", "delay": 2000},
  {"type": "fill", "selector": "#username", "value": "alice"},
  {"type": "fill", "selector": "#password", "value": "password"},
  {"type": "click", "selector": "#login"},
  {"type": "wait_for", "selector": ".dashboard"},
  {"type": "screenshot", "filename": "dashboard.png"}
]
\`\`\`

### 页面快照

全页截图：
\`\`\`bash
python skills/playwright_browser/snapshot.py https://example.com --output fullpage --full-page
\`\`\`

导出为 PDF：
\`\`\`bash
python skills/playwright_browser/snapshot.py https://example.com --output report --format pdf
\`\`\`

### 批量下载图片

下载网页中的所有图片：
\`\`\`bash
python skills/playwright_browser/download_images.py https://example.com --output-dir downloaded_images --max 10
\`\`\`

参数说明：
- `--output-dir`: 输出目录（相对于 alice_output/），默认为 "images"
- `--max`: 最大下载数量，默认为 20

示例：
\`\`\`bash
# 从 NVIDIA 官网下载最多 5 张图片
python skills/playwright_browser/download_images.py https://www.nvidia.cn --output-dir nvidia_images --max 5
\`\`\`

## 技术细节

- **浏览器引擎**: Chromium (无头模式)
- **视口设置**: 默认 1280x800 (可根据需要调整)
- **容器优化**: 自动添加 `--no-sandbox` 和 `--disable-setuid-sandbox` 参数
- **异步执行**: 使用 asyncio 实现高效并发
- **输出目录**: 所有文件默认保存至 `alice_output/`

## 支持的操作类型 (automator.py)

| 类型 | 参数 | 说明 |
|------|------|------|
| `click` | selector | 点击指定元素 |
| `fill` | selector, value | 输入文本 |
| `select` | selector, value | 下拉选择 |
| `wait` | delay | 等待指定毫秒数 |
| `scroll` | selector 或 position | 滚动到元素或页面顶部/底部 |
| `screenshot` | filename | 保存截图 |
| `evaluate` | script | 执行 JavaScript |
| `wait_for` | selector | 等待元素出现 |

## 选择器配置格式 (scraper.py)

选择器参数格式：`name:css_selector:attribute[:multiple]`

- `name`: 提取结果的键名
- `css_selector`: CSS 选择器
- `attribute`: 要提取的属性，默认 `text`（文本内容）
- `multiple`: 可选，设为 `true` 时提取所有匹配项

示例：
- `title:h1:text` - 提取 h1 标签的文本
- `images:img:src:multiple` - 提取所有 img 的 src 属性
- `links:a:href` - 提取第一个 a 标签的 href

## 注意事项

- **容器限制**: 在容器环境中运行时，必须使用 `--no-sandbox` 参数（已自动处理）
- **超时设置**: 默认超时时间为 30 秒，可根据任务复杂度调整
- **动态内容**: 如需等待 JavaScript 渲染，使用 `--wait` 参数或 `wait_for` 操作
- **反爬策略**: 某些网站可能有反爬虫机制，建议适当添加延迟
- **内存使用**: 处理大量页面时注意内存占用，可分批处理
- **依赖要求**: 需要已安装 `playwright` 包及浏览器二进制文件
- **图片下载**: 某些网站可能有防盗链机制，导致部分图片无法下载

## 依赖安装

\`\`\`bash
pip install playwright
playwright install chromium
\`\`\`

## 常见问题

**Q: 如何处理需要登录的页面？**
A: 使用 automator.py 的操作链，按顺序执行 fill (用户名) → fill (密码) → click (登录按钮) → wait_for (登录后元素)

**Q: 如何提取 JavaScript 动态生成的内容？**
A: 使用 browser_tool.py 的 `--wait` 参数或 scraper.py 的 `--wait` 参数等待元素加载

**Q: 如何处理弹出框？**
A: 使用 automator.py 的 `evaluate` 操作执行 JavaScript 关闭，或在页面上下文中提前禁用

**Q: 为什么某些网站无法访问？**
A: 可能是反爬虫限制，可以尝试设置 user-agent 或使用代理（需修改代码添加 context 配置）

**Q: 为什么只下载了部分图片？**
A: 某些图片可能有加载延迟、防盗链或 base64 编码。脚本会自动跳过无法访问的图片

**Q: 下载的图片文件名如何确定？**
A: 脚本会优先使用 img 标签的 alt 属性，其次是 title 属性。如果没有则使用 "image_N" 格式
