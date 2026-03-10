---
name: chrome-devtools-skill
description: 使用 Chrome DevTools MCP 获取和分析网页数据。当用户需要抓取网页内容、分析网页结构、提取数据、截图、监控网络请求或执行网页自动化任务时使用此 skill。
---

# Chrome DevTools Skill

使用 Chrome DevTools Protocol 进行网页数据获取和分析。

## 工作流程（AI 自动执行）

当用户使用此 skill 时，AI 应该**自动完成以下所有步骤**，而不是让用户手动执行：

### 1. 自动启动 Chrome 远程调试

AI 自动检测操作系统并启动 Chrome：

**Windows:**
```bash
start chrome --remote-debugging-port=9222 --user-data-dir="%TEMP%\chrome-devtools-profile" [URL]
```

> **重要提示**: 使用固定的 `--user-data-dir`（如 `chrome-devtools-profile`），不要每次使用不同的文件夹。这样 Chrome 会记住登录状态、Cookie 和缓存，下次启动更快。

**macOS:**
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="$TMPDIR/chrome-profile-stable" [URL]
```

**Linux:**
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-profile-stable" [URL]
```

### 2. 自动启动 MCP 服务器

AI 自动启动 MCP 服务器（在后台运行）：
```bash
npx -y chrome-devtools-mcp@latest --browser-url=http://127.0.0.1:9222
```

### 3. 执行用户请求的操作

使用以下 MCP 工具完成用户任务：
- `mcp__chrome-devtools__navigate_page` - 导航到页面
- `mcp__chrome-devtools__wait_for` - 等待页面加载
- `mcp__chrome-devtools__take_snapshot` - 获取页面快照
- `mcp__chrome-devtools__evaluate_script` - 执行 JavaScript 提取数据
- `mcp__chrome-devtools__screenshot` - 截取屏幕截图
- `mcp__chrome-devtools__list_network_requests` - 列出网络请求

## 标准操作流程（AI 使用）

当用户要求打开/分析/抓取某个网页时，AI 按以下顺序执行：

```
1. 启动 Chrome（调试模式）
2. 启动 MCP 服务器
3. 导航到目标 URL
4. 等待页面加载
5. 执行用户请求的操作（截图/提取数据/监控网络等）
6. 返回结果给用户
```

## 数据提取技巧

**提取列表数据**:

```javascript
() => {
  const items = document.querySelectorAll(".item");
  return Array.from(items).map((item) => ({
    title: item.querySelector(".title")?.innerText,
    link: item.querySelector("a")?.href,
  }));
};
```

**提取表格数据**:

```javascript
() => {
  const rows = document.querySelectorAll("table tr");
  return Array.from(rows).map((row) =>
    Array.from(row.querySelectorAll("td, th")).map((cell) => cell.innerText)
  );
};
```

## 常见用例

- **打开网页并截图**: 启动 Chrome → 导航 → 截图 → 返回结果
- **商品信息抓取**: 导航 → 滚动加载 → 提取列表
- **表单自动化**: 导航 → fill_form → click → wait_for
- **API 监控**: 导航 → list_network_requests → get_network_request
- **性能分析**: performance_start_trace → 操作 → performance_stop_trace

## 最佳实践

1. **自动处理所有前置步骤** - 不要要求用户手动启动 Chrome 或 MCP 服务器
2. **使用固定的用户数据目录** - 保持 `--user-data-dir` 一致，避免每次都重新加载
3. 先用 `take_snapshot` 了解页面结构
4. 复杂提取用 `evaluate_script` 执行 JavaScript
5. 确保返回 JSON 可序列化的数据
6. 处理动态内容时使用 `wait_for`

## 技术原理

### Chrome DevTools Protocol (CDP) 通信方式

| 方式 | 协议 | 用途 |
|-----|------|-----|
| **HTTP** | `http://127.0.0.1:9222/json/list` | 获取页面列表、基本信息 |
| **WebSocket** | `ws://127.0.0.1:9222/devtools/page/{pageId}` | 实时控制页面、执行脚本 |

### WebSocket 通信流程

```python
import asyncio
import websockets
import json

async def cdp_example():
    # 1. 连接到 Chrome DevTools WebSocket
    ws_url = "ws://127.0.0.1:9222/devtools/page/{pageId}"
    async with websockets.connect(ws_url) as ws:

        # 2. 启用 Runtime 域
        await ws.send(json.dumps({
            "id": 1,
            "method": "Runtime.enable"
        }))

        # 3. 执行 JavaScript
        await ws.send(json.dumps({
            "id": 2,
            "method": "Runtime.evaluate",
            "params": {
                "expression": "document.title",
                "returnByValue": True
            }
        }))

        # 4. 循环接收响应，匹配 id
        while True:
            msg = await ws.recv()
            data = json.loads(msg)
            if data.get('id') == 2:  # 匹配请求 id
                return data['result']['result']['value']
```

### 关键注意事项

1. **响应匹配**: WebSocket 会收到多种消息（`consoleAPICalled`、`executionContextCreated` 等），必须通过 `id` 匹配请求和响应
2. **等待页面加载**: 执行操作后使用 `await asyncio.sleep(2)` 或等待特定元素
3. **编码问题**: Windows 终端需要 `sys.stdout.reconfigure(encoding='utf-8')` 来正确显示中文

### 实战经验与踩坑记录

#### 问题 1: Windows 中文输出乱码
**现象**: 抓取的中文内容显示为乱码或抛出 `UnicodeEncodeError: 'gbk' codec can't encode character`
**原因**: Windows 终端默认使用 GBK 编码，而 Python 输出 UTF-8 中文时会冲突
**解决**: 在 Python 脚本开头添加编码配置：
```python
import sys
sys.stdout.reconfigure(encoding='utf-8')
```

**重要**: 所有示例脚本（`baidu_search_example.py`、`cdp_helper.py`）都已添加此编码配置，直接运行不会产生乱码。

#### 问题 2: HTML 字符实体转义
**现象**: JavaScript 代码中的 `=>` 箭头函数在通过 JSON 传输时被转义为 `=>`
**原因**: JSON 标准会对某些字符进行 Unicode 转义
**解决**: 这是正常现象，不影响实际执行。如果需要在 Python 中处理，可以使用：
```python
import codecs
decoded = codecs.decode(string, 'unicode_escape')
```

#### 问题 3: 页面 ID 获取
**现象**: 不知道当前页面的 WebSocket URL
**解决**: 通过 HTTP 接口获取页面列表：
```bash
curl -s http://127.0.0.1:9222/json/list
```
然后提取 `webSocketDebuggerUrl` 字段

**注意**: 页面 ID 是动态生成的，每次启动 Chrome 都会变化。应该在代码中动态获取而不是硬编码：
```python
import urllib.request
import json

def get_ws_url():
    req = urllib.request.Request('http://127.0.0.1:9222/json/list')
    with urllib.request.urlopen(req) as response:
        pages = json.loads(response.read().decode())
    return pages[0]['webSocketDebuggerUrl'] if pages else None
```

#### 问题 4: Windows 等待命令跨平台兼容性问题
**现象**: 在 Git Bash 中使用 `timeout /t 3 /nobreak` 报错 `invalid time interval`
**原因**: `timeout` 是 Windows CMD 命令，在 Bash 中语法不兼容
**解决**: 使用跨平台的等待方案：
```bash
# Windows CMD
timeout /t 3 /nobreak >nul

# Git Bash / Linux
sleep 3

# 跨平台通用（Windows）
ping -n 4 127.0.0.1 > nul
```

#### 问题 5: Claude Code 文件写入限制
**现象**: 直接使用 Write 工具创建新文件时提示 "File has not been read yet"
**原因**: Claude Code 要求必须先读取文件才能写入（安全机制）
**解决**:
1. 先使用 Read 工具读取文件（如果不存在会报错，需要用 Bash 创建空文件）
2. 或者使用 Bash 的 `echo` 或 `cat` 命令直接写入
3. 或者使用 Python 脚本动态生成并执行代码

#### 问题 6: 动态内容提取不完整
**现象**: 提取的搜索结果中某些字段（如摘要）为空
**原因**:
1. 页面使用了动态加载，需要滚动才能显示全部内容
2. 不同网站使用不同的 class 名称
3. 某些内容是异步加载的

**解决**:
1. 使用多个选择器匹配：
```javascript
const abstract = item.querySelector('.c-abstract, .abstract, [class*="abstract"]')?.innerText;
```
2. 滚动页面加载更多内容：
```javascript
window.scrollTo(0, document.body.scrollHeight);
```
3. 增加等待时间确保异步内容加载完成

#### 问题 7: 前台 vs 后台操作浏览器

CDP 支持两种操作模式，根据用户需求选择：

**后台操作（默认）**：
- 通过 WebSocket 发送 JavaScript 命令直接操作 DOM
- 浏览器界面不会显示操作过程（用户看不到输入、点击等动作）
- 适合数据抓取、自动化测试等不需要可视化反馈的场景
- 代码示例：
```python
# 直接设置输入框的值（用户看不到输入过程）
await ws.send(json.dumps({
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.querySelector('#kw').value = '美女';"
    }
}))
```

**前台操作（可视化）**：
- 使用 CDP 的 Input 域模拟真实用户输入
- 浏览器会显示完整的操作过程（键盘输入、鼠标点击等）
- 适合演示、教学、需要用户观察操作过程的场景
- 代码示例：
```python
# 1. 先聚焦输入框
await ws.send(json.dumps({
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.querySelector('#kw').focus();"
    }
}))

# 2. 模拟键盘输入（用户能看到逐字输入）
for char in "美女":
    await ws.send(json.dumps({
        "method": "Input.dispatchKeyEvent",
        "params": {
            "type": "char",
            "text": char
        }
    }))
    await asyncio.sleep(0.1)  # 模拟真实打字间隔

# 3. 模拟点击搜索按钮（用户能看到点击效果）
await ws.send(json.dumps({
    "method": "Input.dispatchMouseEvent",
    "params": {
        "type": "mousePressed",
        "x": 100,
        "y": 200,
        "button": "left"
    }
}))
```

**选择建议**：
| 场景 | 推荐模式 | 原因 |
|------|---------|------|
| 数据抓取 | 后台 | 速度快，不需要可视化 |
| 自动化测试 | 后台 | 稳定可靠，不受UI影响 |
| 搜索类任务 | 后台 | 直接构造URL更简单可靠 |
| 操作演示 | 前台 | 用户能看到完整过程 |
| 教学演示 | 前台 | 便于观察和理解 |
| 表单填写 | 两者皆可 | 后台更快，前台更直观 |

**搜索类任务推荐方案**：
- **后台方式**（推荐）：直接构造搜索URL，如 `https://www.baidu.com/s?wd=关键词`
- **前台方式**：仅当用户明确要求"可视化"、"能看到操作过程"时使用

#### 问题 8: 搜索类任务的最佳实践

**场景**: 用户要求"在百度/谷歌搜索某某关键词并抓取结果"

**方案对比**:

| 方案 | 实现方式 | 优点 | 缺点 | 推荐度 |
|------|---------|------|------|--------|
| **A** | 后台直接访问搜索URL | 简单、快速、稳定 | 用户看不到过程 | ⭐⭐⭐⭐⭐ |
| **B** | 前台模拟输入点击 | 可视化、有反馈 | 复杂、慢、需处理坐标 | ⭐⭐⭐ |

**推荐方案 A（后台方式）**：
```python
# 直接构造搜索URL，一步到位
url = f"https://www.baidu.com/s?wd={urllib.parse.quote(keyword)}"
await client.navigate(url)
await asyncio.sleep(3)  # 等待加载
results = await client.evaluate(extract_script)
```

**何时使用方案 B（前台方式）**：
- 用户明确要求"可视化操作"、"让我看到过程"
- 教学演示场景
- 需要展示自动化操作过程

**前台方式注意事项**：
1. 必须先 `focus()` 输入框
2. 打字间隔 0.1-0.15 秒最合适
3. 百度搜素按钮坐标约 x:650, y:230（1920x1080分辨率）
4. 需要启用 Input 域：`Input.enable`

**前台输入文字详细步骤**（以百度搜索框为例）：

```python
# 步骤 1: 启用 Input 域（必须先启用才能发送键盘事件）
await ws.send(json.dumps({
    "id": 1,
    "method": "Input.enable"
}))

# 步骤 2: 聚焦输入框（关键步骤，否则键盘事件可能无效）
await ws.send(json.dumps({
    "id": 2,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.querySelector('#kw').focus();",  # '#kw' 是百度搜索框ID
        "returnByValue": True
    }
}))
await asyncio.sleep(0.5)  # 等待聚焦完成

# 步骤 3: 清空输入框（可选，确保输入框为空）
await ws.send(json.dumps({
    "id": 3,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.querySelector('#kw').value = '';",
        "returnByValue": True
    }
}))

# 步骤 4: 逐字输入文字（用户能看到逐字输入动画）
text = "hello 你好呀"
for i, char in enumerate(text):
    await ws.send(json.dumps({
        "id": 10 + i,
        "method": "Input.dispatchKeyEvent",
        "params": {
            "type": "char",      # 输入字符
            "text": char          # 要输入的字符
        }
    }))
    await asyncio.sleep(0.15)  # 打字间隔，让用户能看到动画
```

**关键要点**：
- `type: "char"` 用于输入普通字符
- 必须先 `focus()` 输入框，否则输入可能无效
- 间隔时间建议 0.1-0.2 秒，太短可能漏字，太长用户等待久
- 支持中文输入，无需额外编码处理

#### 问题 9: 表单自动化执行顺序
**正确顺序**:
1. 启用 Runtime → 2. 填充输入框 → 3. 点击按钮 → 4. 等待页面加载 → 5. 提取数据

**示例代码**（百度搜索后台方式）：
```python
# 1. 填充搜索词
await ws.send(json.dumps({
    "id": 2,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.querySelector('#kw').value = '搜索词';",
        "returnByValue": True
    }
}))

# 2. 点击搜索按钮
await ws.send(json.dumps({
    "id": 3,
    "method": "Runtime.evaluate",
    "params": {
        "expression": "document.querySelector('#su').click();",
        "returnByValue": True
    }
}))

# 3. 等待加载
await asyncio.sleep(3)

# 4. 提取结果
await ws.send(json.dumps({
    "id": 4,
    "method": "Runtime.evaluate",
    "params": {
        "expression": """
            (() => {
                const items = document.querySelectorAll('.result');
                return Array.from(items).map(item => ({
                    title: item.querySelector('h3')?.innerText,
                    link: item.querySelector('a')?.href
                }));
            })()
        """,
        "returnByValue": True
    }
}))
```

## 用户使用指南

### 如何使用此 Skill

用户可以通过以下方式触发此 skill：

1. **直接说明需求** - 描述你想对网页做什么
2. **使用 `/chrome-devtools-skill` 命令** - 显式调用 skill
3. **提及网页操作** - 任何涉及"打开网页、抓取数据、截图"等关键词

### 提示词示例

以下是一些用户可以使用的提示词模板：

#### 基础操作
```
打开 https://www.example.com 并截图
```

```
抓取 https://www.example.com 的页面内容
```

```
分析一下这个网页：https://github.com/xxx/xxx
```

#### 数据提取
```
打开 https://www.jd.com，提取首页所有商品标题和价格
```

```
访问 https://www.zhihu.com/explore，获取热门问题列表
```

```
抓取 https://www.example.com 页面中的所有链接
```

#### 监控和分析
```
打开 https://www.example.com，监控页面加载的所有 API 请求
```

```
分析 https://www.example.com 的页面性能
```

```
访问 https://www.example.com，提取页面中的所有图片地址
```

#### 自动化操作
```
打开 https://www.example.com，在搜索框输入"关键词"并搜索
```

```
访问 https://www.example.com，点击"加载更多"按钮，抓取所有列表数据
```

### 提示词技巧

1. **明确 URL** - 提供完整的网页地址
2. **说明目标** - 清楚描述你想获取什么数据或执行什么操作
3. **指定格式** - 如果需要特定格式，可以说明（如"以表格形式返回"）
4. **复杂任务分步** - 对于多步骤任务，可以分步描述

### 示例对话

**用户**: 帮我打开百度，看看热搜榜有什么内容

**AI**: [自动启动 Chrome → 打开百度 → 提取热搜数据 → 返回结果]

---

**用户**: 抓取 https://news.ycombinator.com 的前 10 条新闻标题和链接

**AI**: [自动启动 Chrome → 打开 Hacker News → 提取新闻数据 → 返回表格]

---

**用户**: 分析一下淘宝首页都加载了哪些接口

**AI**: [自动启动 Chrome → 打开淘宝 → 监控网络请求 → 返回 API 列表]

## 参考资源

- **示例脚本**: 见 `scripts/` 目录
  - `baidu_search_example.py` - 百度搜索完整示例
  - `cdp_helper.py` - CDP 客户端封装类
  - `README.md` - 快速开始指南

## Chrome DevTools MCP 配置信息

如果用户询问`chrome-devtools MCP`怎么配置，提供以下 JSON 配置信息：

```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": [
        "chrome-devtools-mcp@latest",
        "--browser-url=http://127.0.0.1:9222"
      ]
    }
  }
}
```
// 测试修改
// 另一个测试修改
// 测试修改 pre-push 方案
