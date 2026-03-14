---
name: playwright-browser
description: 浏览器自动化技能，支持101个工具：页面导航、元素交互、内容提取、截图、网络控制、性能监控等
version: 2.1.0
mcp:
  command: node
  args:
    - dist/mcp-server.js
---

# Playwright Browser Skill - 浏览器自动化技能

## ⚡ AI 调用指南（OpenClaw 必读）

### 如何调用 MCP 工具

当用户请求浏览器操作时，你需要通过 MCP 协议调用相应的工具。以下是调用方法：

#### 基本调用流程

1. **启动浏览器** → 调用 `browser_launch`
2. **访问网页** → 调用 `browser_goto`
3. **执行操作** → 调用相应工具（点击、填写、提取等）
4. **关闭浏览器** → 调用 `browser_close`

#### 常用工具快速参考

| 用户需求 | 调用工具 | 参数示例 |
|---------|---------|---------|
| "访问网站" | `browser_goto` | `{ "url": "https://example.com" }` |
| "点击按钮" | `browser_click` | `{ "selector": "button.submit" }` |
| "填写表单" | `browser_fill` | `{ "selector": "#username", "value": "admin" }` |
| "获取标题" | `browser_get_title` | `{}` |
| "截图" | `browser_screenshot` | `{ "path": "screenshot.png", "fullPage": true }` |
| "获取文本" | `browser_get_text` | `{ "selector": "h1" }` |
| "等待元素" | `browser_wait_for_selector` | `{ "selector": ".content" }` |

#### 完整示例：访问网页并获取标题

```
用户："访问 example.com 并获取页面标题"

你应该调用：
1. browser_launch({ "headless": false })
2. browser_goto({ "url": "https://example.com" })
3. browser_get_title({})
4. browser_close({})
```

#### 完整示例：搜索操作

```
用户："在百度搜索 OpenClaw"

你应该调用：
1. browser_launch({})
2. browser_goto({ "url": "https://www.baidu.com" })
3. browser_fill({ "selector": "#kw", "value": "OpenClaw" })
4. browser_click({ "selector": "#su" })
5. browser_wait_for_selector({ "selector": ".result" })
6. browser_close({})
```

#### 重要提示

- ✅ **必须先调用 browser_launch** - 任何操作前都要先启动浏览器
- ✅ **使用完毕调用 browser_close** - 释放资源
- ✅ **等待元素加载** - 使用 browser_wait_for_selector 确保元素存在
- ✅ **选择器语法** - 使用 CSS 选择器（#id, .class, button[type="submit"]）

---

## 🚀 用户使用指南

这是一个强大的浏览器自动化技能，可以帮助你控制浏览器、访问网页、提取内容、截图等。通过 MCP 协议提供 101 个完整的浏览器操作工具。

### 如何使用这个技能

**基本用法：**
当你需要访问网页、提取信息或控制浏览器时，直接告诉我你的需求即可。我会自动选择合适的工具来完成任务。

**示例对话：**
- "帮我访问 example.com 并获取页面标题"
- "打开百度搜索 'OpenClaw'"
- "访问 github.com 并截图"
- "帮我从这个网页提取所有链接"
- "启动浏览器并访问 https://www.google.com"

### 主要功能

1. **网页访问** - 访问任何网站，获取页面内容
2. **内容提取** - 提取文本、链接、图片等信息
3. **页面交互** - 点击按钮、填写表单、滚动页面
4. **截图保存** - 对整个页面或特定元素截图
5. **数据抓取** - 批量提取网页数据
6. **自动化测试** - 模拟用户操作，测试网站功能

### 常见使用场景

**场景 1：快速查看网页**
```
你：帮我看看 example.com 上有什么内容
我：会自动启动浏览器，访问网页，提取并总结内容
```

**场景 2：提取信息**
```
你：从 news.ycombinator.com 提取今天的热门文章标题
我：会访问网页，提取所有文章标题并整理给你
```

**场景 3：网页截图**
```
你：帮我截取 github.com 首页的截图
我：会访问网页并保存截图
```

**场景 4：表单填写**
```
你：帮我在这个网站的搜索框输入 "OpenClaw" 并搜索
我：会找到搜索框，输入内容，点击搜索按钮
```

## 💡 使用提示

- **无需指定工具名称** - 直接说你的需求，我会自动选择合适的工具
- **支持中英文** - 可以用中文或英文描述你的需求
- **支持复杂任务** - 可以组合多个操作完成复杂任务
- **自动处理错误** - 如果遇到问题，我会自动重试或调整策略

---

## 🔧 工具调用指南（给 OpenClaw 看的）

### 基本调用流程

**步骤 1：启动浏览器**
```json
工具名称: browser_launch
参数: {
  "browserType": "chromium",
  "headless": false
}
```

**步骤 2：访问网页**
```json
工具名称: browser_goto
参数: {
  "url": "https://example.com",
  "waitUntil": "networkidle"
}
```

**步骤 3：提取内容**
```json
工具名称: browser_get_title
参数: {}
```

**步骤 4：关闭浏览器**
```json
工具名称: browser_close
参数: {}
```

### 常用工具快速参考

#### 1. 启动浏览器
```json
{
  "tool": "browser_launch",
  "arguments": {
    "browserType": "chromium",
    "headless": false
  }
}
```

#### 2. 访问网页
```json
{
  "tool": "browser_goto",
  "arguments": {
    "url": "https://example.com"
  }
}
```

#### 3. 获取页面标题
```json
{
  "tool": "browser_get_title",
  "arguments": {}
}
```

#### 4. 获取页面文本
```json
{
  "tool": "browser_get_text",
  "arguments": {
    "selector": "body"
  }
}
```

#### 5. 点击元素
```json
{
  "tool": "browser_click",
  "arguments": {
    "selector": "button.submit"
  }
}
```

#### 6. 填写表单
```json
{
  "tool": "browser_fill",
  "arguments": {
    "selector": "#username",
    "value": "user@example.com"
  }
}
```

#### 7. 截图
```json
{
  "tool": "browser_screenshot",
  "arguments": {
    "path": "screenshot.png",
    "fullPage": true
  }
}
```

#### 8. 获取所有链接
```json
{
  "tool": "browser_get_links",
  "arguments": {}
}
```

#### 9. 等待元素
```json
{
  "tool": "browser_wait_for_selector",
  "arguments": {
    "selector": ".content",
    "timeout": 10000
  }
}
```

#### 10. 关闭浏览器
```json
{
  "tool": "browser_close",
  "arguments": {}
}
```

### 完整任务示例

#### 示例 1：访问网页并提取标题
```
步骤 1: browser_launch
  参数: { "headless": false }

步骤 2: browser_goto
  参数: { "url": "https://example.com" }

步骤 3: browser_get_title
  参数: {}

步骤 4: browser_close
  参数: {}
```

#### 示例 2：搜索并提取结果
```
步骤 1: browser_launch
  参数: { "headless": false }

步骤 2: browser_goto
  参数: { "url": "https://www.baidu.com" }

步骤 3: browser_fill
  参数: { "selector": "#kw", "value": "OpenClaw" }

步骤 4: browser_click
  参数: { "selector": "#su" }

步骤 5: browser_wait_for_selector
  参数: { "selector": ".result", "timeout": 5000 }

步骤 6: browser_get_text
  参数: { "selector": ".result" }

步骤 7: browser_close
  参数: {}
```

#### 示例 3：提取网页数据
```
步骤 1: browser_launch
  参数: {}

步骤 2: browser_goto
  参数: { "url": "https://news.ycombinator.com" }

步骤 3: browser_wait_for_selector
  参数: { "selector": ".itemlist" }

步骤 4: browser_evaluate
  参数: { 
    "script": "Array.from(document.querySelectorAll('.titleline > a')).map(a => ({ title: a.textContent, url: a.href }))"
  }

步骤 5: browser_close
  参数: {}
```

### 重要提示

1. **必须先启动浏览器** - 使用任何其他工具前，必须先调用 `browser_launch`
2. **使用完毕要关闭** - 任务完成后，调用 `browser_close` 释放资源
3. **等待页面加载** - 访问网页后，使用 `browser_wait_for_selector` 等待内容加载
4. **选择器要准确** - 使用正确的 CSS 选择器来定位元素
5. **处理错误** - 如果工具调用失败，检查参数是否正确

---

## 📚 技术文档

以下是完整的工具列表和技术文档，供高级用户参考。

## 目录

1. [浏览器管理](#浏览器管理) (8个工具)
2. [页面导航](#页面导航) (4个工具)
3. [元素交互](#元素交互) (12个工具)
4. [键盘鼠标操作](#键盘鼠标操作) (8个工具)
5. [内容提取](#内容提取) (11个工具)
6. [高级选择器](#高级选择器) (7个工具)
7. [等待操作](#等待操作) (7个工具)
8. [截图和PDF](#截图和pdf) (3个工具)
9. [JavaScript执行](#javascript执行) (3个工具)
10. [Cookie和存储](#cookie和存储) (8个工具)
11. [网络控制](#网络控制) (7个工具)
12. [文件操作](#文件操作) (2个工具)
13. [视口和设备](#视口和设备) (6个工具)
14. [滚动操作](#滚动操作) (2个工具)
15. [性能指标](#性能指标) (3个工具)
16. [无障碍功能](#无障碍功能) (1个工具)
17. [时间控制](#时间控制) (5个工具)
18. [权限管理](#权限管理) (2个工具)
19. [对话框处理](#对话框处理) (1个工具)
20. [Frame操作](#frame操作) (1个工具)

---

## 浏览器管理

### browser_launch
启动浏览器实例（支持设备模拟、视频录制、追踪等高级功能）

**参数：**
- `browserType`: 'chromium' | 'firefox' | 'webkit' (默认: 'chromium')
- `headless`: boolean - 是否无头模式 (默认: true)
- `viewport`: { width: number, height: number } - 视口大小
- `deviceName`: string - 设备名称，如 'iPhone 13', 'Pixel 5'
- `recordVideo`: boolean - 是否录制视频
- `recordTrace`: boolean - 是否记录追踪
- `slowMo`: number - 慢动作延迟（毫秒）

**调用示例：**
```json
{
  "browserType": "chromium",
  "headless": false,
  "viewport": { "width": 1920, "height": 1080 },
  "deviceName": "iPhone 13"
}
```

### browser_close
关闭浏览器并释放所有资源

**参数：** 无

**调用示例：**
```json
{}
```

### browser_new_page
创建新的浏览器页面（标签页）

**参数：** 无

**调用示例：**
```json
{}
```

### browser_switch_page
切换到指定索引的页面

**参数：**
- `index`: number - 页面索引（从0开始）

**调用示例：**
```json
{ "index": 1 }
```

### browser_close_page
关闭指定索引的页面

**参数：**
- `index`: number - 页面索引（可选，默认关闭当前页面）

**调用示例：**
```json
{ "index": 0 }
```

### browser_get_all_pages
获取所有打开的页面列表

**参数：** 无

**调用示例：**
```json
{}
```

### browser_get_version
获取浏览器版本信息

**参数：** 无

**调用示例：**
```json
{}
```

### browser_is_connected
检查浏览器连接状态

**参数：** 无

**调用示例：**
```json
{}
```

---

## 页面导航

### browser_goto
导航到指定URL

**参数：**
- `url`: string - 目标URL（必需）
- `waitUntil`: 'load' | 'domcontentloaded' | 'networkidle' - 等待条件
- `timeout`: number - 超时时间（毫秒）

**调用示例：**
```json
{
  "url": "https://www.example.com",
  "waitUntil": "networkidle",
  "timeout": 30000
}
```

### browser_go_back
返回上一页

**参数：** 无

**调用示例：**
```json
{}
```

### browser_go_forward
前进到下一页

**参数：** 无

**调用示例：**
```json
{}
```

### browser_reload
刷新当前页面

**参数：** 无

**调用示例：**
```json
{}
```

---

## 元素交互

### browser_click
点击页面元素

**参数：**
- `selector`: string - CSS选择器（必需）
- `timeout`: number - 超时时间（毫秒）
- `button`: 'left' | 'right' | 'middle' - 鼠标按钮
- `clickCount`: number - 点击次数

**调用示例：**
```json
{
  "selector": "button.submit",
  "button": "left",
  "clickCount": 1
}
```

### browser_dblclick
双击元素

**参数：**
- `selector`: string - CSS选择器（必需）

**调用示例：**
```json
{ "selector": ".item" }
```

### browser_hover
鼠标悬停在元素上

**参数：**
- `selector`: string - CSS选择器（必需）

**调用示例：**
```json
{ "selector": ".menu-item" }
```

### browser_fill
填写表单字段（清空后填入）

**参数：**
- `selector`: string - CSS选择器（必需）
- `value`: string - 要填写的值（必需）

**调用示例：**
```json
{
  "selector": "#username",
  "value": "user@example.com"
}
```

### browser_type
逐字符输入文本（模拟真实键盘输入）

**参数：**
- `selector`: string - CSS选择器（必需）
- `text`: string - 要输入的文本（必需）
- `delay`: number - 每个字符间的延迟（毫秒）

**调用示例：**
```json
{
  "selector": "#search",
  "text": "playwright",
  "delay": 100
}
```

### browser_press
按下键盘按键

**参数：**
- `selector`: string - CSS选择器（必需）
- `key`: string - 按键名称（如 'Enter', 'Tab', 'Escape'）

**调用示例：**
```json
{
  "selector": "#search",
  "key": "Enter"
}
```

### browser_select
选择下拉框选项

**参数：**
- `selector`: string - CSS选择器（必需）
- `value`: string | string[] - 选项值（必需）

**调用示例：**
```json
{
  "selector": "select#country",
  "value": "US"
}
```

### browser_check
勾选复选框

**参数：**
- `selector`: string - CSS选择器（必需）

**调用示例：**
```json
{ "selector": "#agree-terms" }
```

### browser_uncheck
取消勾选复选框

**参数：**
- `selector`: string - CSS选择器（必需）

**调用示例：**
```json
{ "selector": "#newsletter" }
```

### browser_focus
聚焦到元素

**参数：**
- `selector`: string - CSS选择器（必需）

**调用示例：**
```json
{ "selector": "#email" }
```

### browser_drag
拖拽元素到目标位置

**参数：**
- `sourceSelector`: string - 源元素选择器（必需）
- `targetSelector`: string - 目标元素选择器（必需）

**调用示例：**
```json
{
  "sourceSelector": ".draggable",
  "targetSelector": ".drop-zone"
}
```

### browser_tap
触摸点击（移动端）

**参数：**
- `selector`: string - CSS选择器（必需）

**调用示例：**
```json
{ "selector": ".mobile-button" }
```

---

## 键盘鼠标操作

### browser_keyboard_down
按下键盘按键（不释放）

**参数：**
- `key`: string - 按键名称（必需）

**调用示例：**
```json
{ "key": "Shift" }
```

### browser_keyboard_up
释放键盘按键

**参数：**
- `key`: string - 按键名称（必需）

**调用示例：**
```json
{ "key": "Shift" }
```

### browser_mouse_move
移动鼠标到指定坐标

**参数：**
- `x`: number - X坐标（必需）
- `y`: number - Y坐标（必需）
- `steps`: number - 移动步数（平滑移动）

**调用示例：**
```json
{
  "x": 100,
  "y": 200,
  "steps": 10
}
```

### browser_mouse_click
在指定坐标点击鼠标

**参数：**
- `x`: number - X坐标（必需）
- `y`: number - Y坐标（必需）

**调用示例：**
```json
{
  "x": 150,
  "y": 250
}
```

### browser_mouse_wheel
鼠标滚轮滚动

**参数：**
- `deltaX`: number - 水平滚动量（必需）
- `deltaY`: number - 垂直滚动量（必需）

**调用示例：**
```json
{
  "deltaX": 0,
  "deltaY": 100
}
```

### browser_mouse_down
按下鼠标按键（不释放）

**参数：**
- `button`: 'left' | 'right' | 'middle' - 鼠标按键
- `clickCount`: number - 点击次数

**调用示例：**
```json
{
  "button": "left",
  "clickCount": 1
}
```

### browser_mouse_up
释放鼠标按键

**参数：**
- `button`: 'left' | 'right' | 'middle' - 鼠标按键
- `clickCount`: number - 点击次数

**调用示例：**
```json
{
  "button": "left",
  "clickCount": 1
}
```

### browser_keyboard_insert_text
插入文本（不触发键盘事件，直接设置值）

**参数：**
- `text`: string - 要插入的文本（必需）

**调用示例：**
```json
{
  "text": "Hello World"
}
```

---

## 内容提取

### browser_get_text
获取元素的文本内容

**参数：**
- `selector`: string - CSS选择器（必需）

**调用示例：**
```json
{ "selector": "h1.title" }
```

### browser_get_title
获取页面标题

**参数：** 无

**调用示例：**
```json
{}
```

### browser_get_html
获取整个页面的HTML内容

**参数：** 无

**调用示例：**
```json
{}
```

### browser_get_links
获取页面中所有链接

**参数：** 无

**调用示例：**
```json
{}
```

### browser_get_attribute
获取元素的属性值

**参数：**
- `selector`: string - CSS选择器（必需）
- `attribute`: string - 属性名称（必需）

**调用示例：**
```json
{
  "selector": "img.logo",
  "attribute": "src"
}
```

### browser_get_input_value
获取输入框的值

**参数：**
- `selector`: string - CSS选择器（必需）

**调用示例：**
```json
{ "selector": "#email" }
```

### browser_is_visible
检查元素是否可见

**参数：**
- `selector`: string - CSS选择器（必需）

**调用示例：**
```json
{ "selector": ".modal" }
```

### browser_is_enabled
检查元素是否启用

**参数：**
- `selector`: string - CSS选择器（必需）

**调用示例：**
```json
{ "selector": "button.submit" }
```

### browser_is_checked
检查复选框/单选框是否选中

**参数：**
- `selector`: string - CSS选择器（必需）

**调用示例：**
```json
{ "selector": "#agree" }
```

### browser_count
统计匹配选择器的元素数量

**参数：**
- `selector`: string - CSS选择器（必需）

**调用示例：**
```json
{ "selector": ".product-item" }
```

### browser_get_current_url
获取当前页面URL

**参数：** 无

**调用示例：**
```json
{}
```

---

## 高级选择器

### browser_get_by_role
通过ARIA角色查找元素

**参数：**
- `role`: string - ARIA角色（必需）
- `name`: string - 可访问名称

**调用示例：**
```json
{
  "role": "button",
  "name": "Submit"
}
```

### browser_get_by_text
通过文本内容查找元素

**参数：**
- `text`: string - 文本内容（必需）
- `exact`: boolean - 是否精确匹配

**调用示例：**
```json
{
  "text": "Sign In",
  "exact": true
}
```

### browser_get_by_label
通过标签文本查找表单元素

**参数：**
- `text`: string - 标签文本（必需）
- `exact`: boolean - 是否精确匹配

**调用示例：**
```json
{
  "text": "Email Address",
  "exact": false
}
```

### browser_get_by_placeholder
通过占位符文本查找输入框

**参数：**
- `text`: string - 占位符文本（必需）
- `exact`: boolean - 是否精确匹配

**调用示例：**
```json
{
  "text": "Enter your email",
  "exact": false
}
```

### browser_get_by_test_id
通过测试ID查找元素

**参数：**
- `testId`: string - 测试ID（必需）

**调用示例：**
```json
{ "testId": "submit-button" }
```

### browser_get_by_alt_text
通过alt属性文本查找图片元素

**参数：**
- `text`: string - alt文本（必需）
- `exact`: boolean - 是否精确匹配

**调用示例：**
```json
{
  "text": "Company Logo",
  "exact": false
}
```

### browser_get_by_title
通过title属性查找元素

**参数：**
- `text`: string - title文本（必需）
- `exact`: boolean - 是否精确匹配

**调用示例：**
```json
{
  "text": "Click to expand",
  "exact": false
}
```

---

## 等待操作

### browser_wait_for_selector
等待元素出现在DOM中

**参数：**
- `selector`: string - CSS选择器（必需）
- `timeout`: number - 超时时间（毫秒）
- `state`: 'attached' | 'visible' | 'hidden' - 等待状态

**调用示例：**
```json
{
  "selector": ".loading-complete",
  "timeout": 10000,
  "state": "visible"
}
```

### browser_wait_for_timeout
等待指定时间

**参数：**
- `timeout`: number - 等待时间（毫秒，必需）

**调用示例：**
```json
{ "timeout": 3000 }
```

### browser_wait_for_url
等待URL匹配指定模式

**参数：**
- `url`: string - URL模式（必需）
- `timeout`: number - 超时时间（毫秒）

**调用示例：**
```json
{
  "url": "https://example.com/dashboard",
  "timeout": 5000
}
```

### browser_wait_for_request
等待网络请求

**参数：**
- `urlPattern`: string - URL模式（必需）
- `timeout`: number - 超时时间（毫秒）

**调用示例：**
```json
{
  "urlPattern": "**/api/users",
  "timeout": 10000
}
```

### browser_wait_for_response
等待网络响应

**参数：**
- `urlPattern`: string - URL模式（必需）
- `timeout`: number - 超时时间（毫秒）

**调用示例：**
```json
{
  "urlPattern": "**/api/data",
  "timeout": 10000
}
```

### browser_wait_for_function
等待JavaScript函数返回true

**参数：**
- `fn`: string - JavaScript函数代码（必需）
- `arg`: any - 传递给函数的参数
- `timeout`: number - 超时时间（毫秒）
- `polling`: number - 轮询间隔（毫秒）

**调用示例：**
```json
{
  "fn": "() => document.readyState === 'complete'",
  "timeout": 5000,
  "polling": 100
}
```

### browser_wait_for_load_state
等待页面加载到指定状态

**参数：**
- `state`: 'load' | 'domcontentloaded' | 'networkidle' - 加载状态（必需）
- `timeout`: number - 超时时间（毫秒）

**调用示例：**
```json
{
  "state": "networkidle",
  "timeout": 30000
}
```

---

## 截图和PDF

### browser_screenshot
截取页面截图

**参数：**
- `path`: string - 保存路径
- `fullPage`: boolean - 是否截取整页
- `type`: 'png' | 'jpeg' - 图片格式
- `quality`: number - 图片质量（0-100，仅JPEG）

**调用示例：**
```json
{
  "path": "screenshot.png",
  "fullPage": true,
  "type": "png"
}
```

### browser_screenshot_element
截取指定元素的截图

**参数：**
- `selector`: string - CSS选择器（必需）
- `path`: string - 保存路径

**调用示例：**
```json
{
  "selector": ".chart",
  "path": "chart.png"
}
```

### browser_pdf
生成页面PDF

**参数：**
- `path`: string - 保存路径
- `format`: string - 纸张格式（如 'A4', 'Letter'）
- `printBackground`: boolean - 是否打印背景

**调用示例：**
```json
{
  "path": "page.pdf",
  "format": "A4",
  "printBackground": true
}
```

---

## JavaScript执行

### browser_evaluate
在页面上下文中执行JavaScript代码

**参数：**
- `script`: string - JavaScript代码（必需）
- `arg`: any - 传递给脚本的参数

**调用示例：**
```json
{
  "script": "document.querySelectorAll('h2').length"
}
```

### browser_add_script_tag
向页面添加脚本标签

**参数：**
- `url`: string - 脚本URL
- `content`: string - 脚本内容

**调用示例：**
```json
{
  "url": "https://cdn.example.com/library.js"
}
```

### browser_add_style_tag
向页面添加样式标签

**参数：**
- `url`: string - 样式URL
- `content`: string - 样式内容

**调用示例：**
```json
{
  "content": "body { background: red; }"
}
```

---

## Cookie和存储

### browser_set_cookies
设置一个或多个Cookie

**参数：**
- `cookies`: array - Cookie数组（必需）
  - `name`: string - Cookie名称
  - `value`: string - Cookie值
  - `domain`: string - 域名
  - `path`: string - 路径

**调用示例：**
```json
{
  "cookies": [
    {
      "name": "session",
      "value": "abc123",
      "domain": "example.com",
      "path": "/"
    }
  ]
}
```

### browser_get_cookies
获取当前页面的所有Cookie

**参数：** 无

**调用示例：**
```json
{}
```

### browser_clear_cookies
清除所有Cookie

**参数：** 无

**调用示例：**
```json
{}
```

### browser_set_local_storage
设置LocalStorage项

**参数：**
- `key`: string - 键名（必需）
- `value`: string - 值（必需）

**调用示例：**
```json
{
  "key": "theme",
  "value": "dark"
}
```

### browser_get_local_storage
获取LocalStorage项

**参数：**
- `key`: string - 键名（可选，不提供则返回所有）

**调用示例：**
```json
{ "key": "theme" }
```

### browser_clear_local_storage
清除LocalStorage

**参数：** 无

**调用示例：**
```json
{}
```

### browser_storage_state
保存存储状态（Cookie和LocalStorage）

**参数：**
- `path`: string - 保存路径

**调用示例：**
```json
{ "path": "storage.json" }
```

### browser_restore_storage_state
恢复存储状态

**参数：**
- `state`: object - 存储状态对象（必需）

**调用示例：**
```json
{
  "state": { "cookies": [], "origins": [] }
}
```

---

## 网络控制

### browser_set_offline
设置离线模式

**参数：**
- `offline`: boolean - 是否离线（必需）

**调用示例：**
```json
{ "offline": true }
```

### browser_block_requests
拦截匹配模式的请求

**参数：**
- `patterns`: array - URL模式数组（必需）

**调用示例：**
```json
{
  "patterns": ["*.jpg", "*.png", "*/ads/*"]
}
```

### browser_mock_response
模拟网络响应

**参数：**
- `urlPattern`: string - URL模式（必需）
- `response`: object - 响应对象（必需）
  - `status`: number - 状态码
  - `body`: string - 响应体
  - `contentType`: string - 内容类型

**调用示例：**
```json
{
  "urlPattern": "**/api/users",
  "response": {
    "status": 200,
    "body": "{\"users\": []}",
    "contentType": "application/json"
  }
}
```

### browser_get_request_logs
获取请求日志

**参数：**
- `limit`: number - 限制数量

**调用示例：**
```json
{ "limit": 50 }
```

### browser_get_response_logs
获取响应日志

**参数：**
- `limit`: number - 限制数量

**调用示例：**
```json
{ "limit": 50 }
```

### browser_get_console_logs
获取控制台日志

**参数：**
- `limit`: number - 限制数量

**调用示例：**
```json
{ "limit": 100 }
```

### browser_clear_logs
清除所有日志（请求、响应、控制台）

**参数：** 无

**调用示例：**
```json
{}
```

---

## 文件操作

### browser_upload_file
上传文件到文件输入框

**参数：**
- `selector`: string - 文件输入框选择器（必需）
- `filePath`: string | array - 文件路径（必需）

**调用示例：**
```json
{
  "selector": "input[type='file']",
  "filePath": "C:\\Users\\Admin\\document.pdf"
}
```

### browser_download_file
触发文件下载

**参数：**
- `triggerSelector`: string - 触发下载的元素选择器（必需）

**调用示例：**
```json
{ "triggerSelector": "a.download-link" }
```

---

## 视口和设备

### browser_set_viewport_size
设置视口大小

**参数：**
- `width`: number - 宽度（必需）
- `height`: number - 高度（必需）

**调用示例：**
```json
{
  "width": 1920,
  "height": 1080
}
```

### browser_get_viewport_size
获取当前视口大小

**参数：** 无

**调用示例：**
```json
{}
```

### browser_emulate_media
模拟媒体类型和配色方案

**参数：**
- `colorScheme`: 'light' | 'dark' | 'no-preference' - 配色方案
- `media`: 'screen' | 'print' - 媒体类型

**调用示例：**
```json
{
  "colorScheme": "dark",
  "media": "screen"
}
```

### browser_set_geolocation
设置地理位置

**参数：**
- `latitude`: number - 纬度（必需）
- `longitude`: number - 经度（必需）
- `accuracy`: number - 精度

**调用示例：**
```json
{
  "latitude": 37.7749,
  "longitude": -122.4194,
  "accuracy": 100
}
```

### browser_clear_geolocation
清除地理位置设置

**参数：** 无

**调用示例：**
```json
{}
```

### browser_touchscreen_tap
触摸屏点击指定坐标（移动端）

**参数：**
- `x`: number - X坐标（必需）
- `y`: number - Y坐标（必需）

**调用示例：**
```json
{
  "x": 100,
  "y": 200
}
```

---

## 滚动操作

### browser_scroll_to
滚动到指定坐标

**参数：**
- `x`: number - X坐标（必需）
- `y`: number - Y坐标（必需）

**调用示例：**
```json
{
  "x": 0,
  "y": 1000
}
```

### browser_scroll_into_view
滚动元素到可见区域

**参数：**
- `selector`: string - CSS选择器（必需）

**调用示例：**
```json
{ "selector": "#footer" }
```

---

## 性能指标

### browser_get_metrics
获取页面性能指标

**参数：** 无

**调用示例：**
```json
{}
```

**返回数据包括：**
- domContentLoaded: DOM内容加载时间
- loadComplete: 页面完全加载时间
- firstPaint: 首次绘制时间
- firstContentfulPaint: 首次内容绘制时间

### browser_get_coverage
开始收集JavaScript和CSS代码覆盖率

**参数：** 无

**调用示例：**
```json
{}
```

### browser_stop_coverage
停止收集代码覆盖率并返回结果

**参数：** 无

**调用示例：**
```json
{}
```

---

## 无障碍功能

### browser_get_accessibility_snapshot
获取页面无障碍树快照

**参数：**
- `selector`: string - 限定范围的选择器（可选）

**调用示例：**
```json
{ "selector": "main" }
```

---

## 时间控制

### browser_install_clock
安装时钟控制（用于测试时间相关功能）

**参数：**
- `time`: number | string - 初始时间

**调用示例：**
```json
{ "time": 1609459200000 }
```

### browser_set_system_time
设置系统时间

**参数：**
- `time`: number | string - 时间戳或日期字符串（必需）

**调用示例：**
```json
{ "time": "2024-01-01T00:00:00Z" }
```

### browser_fast_forward
快进时间

**参数：**
- `time`: number - 快进的毫秒数（必需）

**调用示例：**
```json
{ "time": 60000 }
```

### browser_pause_clock
暂停时钟（冻结时间）

**参数：** 无

**调用示例：**
```json
{}
```

### browser_resume_clock
恢复时钟运行

**参数：** 无

**调用示例：**
```json
{}
```

---

## 权限管理

### browser_grant_permissions
授予浏览器权限

**参数：**
- `permissions`: array - 权限列表（必需）
  - 可选值: 'geolocation', 'notifications', 'camera', 'microphone', 'clipboard-read', 'clipboard-write'
- `origin`: string - 限定域名

**调用示例：**
```json
{
  "permissions": ["geolocation", "notifications"],
  "origin": "https://example.com"
}
```

### browser_clear_permissions
清除所有权限

**参数：** 无

**调用示例：**
```json
{}
```

---

## 对话框处理

### browser_handle_dialog
处理JavaScript对话框（alert, confirm, prompt）

**参数：**
- `action`: 'accept' | 'dismiss' - 操作类型（必需）
- `promptText`: string - prompt对话框的输入文本

**调用示例：**
```json
{
  "action": "accept",
  "promptText": "My Input"
}
```

---

## Frame操作

### browser_get_frames
获取页面中所有frame

**参数：** 无

**调用示例：**
```json
{}
```

---

---

## 🎯 实际使用场景示例

以下是一些实际的使用场景，展示如何用自然语言与我交互来完成任务。

### 场景 1：查看网页内容
**你说：** "帮我看看 example.com 上有什么"

**我会做：**
1. 启动浏览器
2. 访问 example.com
3. 提取页面标题和主要内容
4. 总结并告诉你

### 场景 2：搜索信息
**你说：** "在百度搜索 'OpenClaw 使用教程'"

**我会做：**
1. 启动浏览器
2. 访问百度
3. 在搜索框输入关键词
4. 点击搜索按钮
5. 提取搜索结果

### 场景 3：提取数据
**你说：** "从 news.ycombinator.com 提取前10条新闻标题"

**我会做：**
1. 访问 Hacker News
2. 定位新闻列表
3. 提取标题和链接
4. 整理成列表返回给你

### 场景 4：网页截图
**你说：** "帮我截取 github.com 首页的截图"

**我会做：**
1. 访问 GitHub
2. 等待页面加载完成
3. 截取整页截图
4. 保存并告诉你文件位置

### 场景 5：表单操作
**你说：** "帮我在这个登录页面输入用户名和密码"

**我会做：**
1. 找到用户名输入框
2. 填写用户名
3. 找到密码输入框
4. 填写密码
5. 询问是否需要点击登录按钮

### 场景 6：监控网页变化
**你说：** "每隔5分钟检查一次这个网页的价格"

**我会做：**
1. 定期访问网页
2. 提取价格信息
3. 与上次对比
4. 如有变化立即通知你

---

## 📖 技术文档：工具列表

以下是完整的 101 个工具的详细文档，供高级用户和开发者参考。

**注意：** 作为普通用户，你不需要了解这些技术细节。直接用自然语言告诉我你的需求即可。

---

## 使用示例

### 示例1：基础网页访问和截图
```
1. browser_launch({ "headless": false })
2. browser_goto({ "url": "https://www.example.com" })
3. browser_get_title()
4. browser_screenshot({ "path": "screenshot.png", "fullPage": true })
5. browser_close()
```

### 示例2：表单填写和提交
```
1. browser_launch()
2. browser_goto({ "url": "https://example.com/login" })
3. browser_fill({ "selector": "#username", "value": "user@example.com" })
4. browser_fill({ "selector": "#password", "value": "password123" })
5. browser_click({ "selector": "button[type='submit']" })
6. browser_wait_for_selector({ "selector": ".dashboard", "timeout": 10000 })
7. browser_close()
```

### 示例3：数据抓取
```
1. browser_launch()
2. browser_goto({ "url": "https://example.com/products" })
3. browser_wait_for_selector({ "selector": ".product-list" })
4. browser_count({ "selector": ".product-item" })
5. browser_get_links()
6. browser_evaluate({ "script": "Array.from(document.querySelectorAll('.price')).map(e => e.textContent)" })
7. browser_close()
```

### 示例4：网络拦截和模拟
```
1. browser_launch()
2. browser_block_requests({ "patterns": ["*.jpg", "*.png", "*/ads/*"] })
3. browser_mock_response({ 
     "urlPattern": "**/api/users", 
     "response": { "status": 200, "body": "{\"users\": []}" }
   })
4. browser_goto({ "url": "https://example.com" })
5. browser_get_request_logs({ "limit": 50 })
6. browser_close()
```

### 示例5：移动设备模拟
```
1. browser_launch({ 
     "deviceName": "iPhone 13", 
     "headless": false 
   })
2. browser_goto({ "url": "https://example.com" })
3. browser_tap({ "selector": ".mobile-menu" })
4. browser_screenshot({ "path": "mobile.png" })
5. browser_close()
```

### 示例6：性能监控
```
1. browser_launch()
2. browser_goto({ "url": "https://example.com" })
3. browser_get_metrics()
4. browser_get_console_logs({ "limit": 100 })
5. browser_get_response_logs({ "limit": 50 })
6. browser_close()
```

---

## 选择器语法参考

### CSS选择器
```css
/* ID选择器 */
#element-id

/* 类选择器 */
.class-name

/* 属性选择器 */
[data-testid="submit"]
[name="username"]
[type="text"]

/* 组合选择器 */
div.container > button.primary
form input[type="text"]
ul li:first-child

/* 伪类选择器 */
button:hover
input:focus
div:nth-child(2)
```

### 高级选择器
```javascript
// 通过文本内容
browser_get_by_text({ "text": "Sign In" })

// 通过ARIA角色
browser_get_by_role({ "role": "button", "name": "Submit" })

// 通过标签
browser_get_by_label({ "text": "Email Address" })

// 通过占位符
browser_get_by_placeholder({ "text": "Enter your email" })

// 通过测试ID
browser_get_by_test_id({ "testId": "submit-button" })
```

---

## 常用键盘按键

- `Enter` - 回车键
- `Tab` - Tab键
- `Escape` - Esc键
- `Backspace` - 退格键
- `Delete` - 删除键
- `ArrowUp`, `ArrowDown`, `ArrowLeft`, `ArrowRight` - 方向键
- `Home`, `End` - Home/End键
- `PageUp`, `PageDown` - 翻页键
- `Control`, `Shift`, `Alt`, `Meta` - 修饰键
- `F1`-`F12` - 功能键

---

## 错误处理和最佳实践

### 1. 浏览器生命周期管理
- 使用前必须先调用 `browser_launch` 启动浏览器
- 使用完毕后应调用 `browser_close` 释放资源
- 浏览器未启动时调用其他方法会抛出错误

### 2. 等待策略
- 使用 `browser_wait_for_selector` 确保元素加载完成
- 设置合理的超时时间（默认30秒）
- 使用 `waitUntil: 'networkidle'` 等待网络请求完成

### 3. 选择器最佳实践
- 优先使用稳定的选择器（ID、data-testid）
- 避免使用易变的选择器（nth-child、复杂的CSS路径）
- 使用语义化选择器（getByRole、getByLabel）提高可维护性

### 4. 性能优化
- 使用 `headless: true` 提高执行速度
- 使用 `browser_block_requests` 拦截不必要的资源（图片、广告）
- 合理设置视口大小，避免过大的截图

### 5. 调试技巧
- 使用 `headless: false` 查看浏览器操作过程
- 使用 `slowMo` 参数减慢操作速度
- 使用 `browser_get_console_logs` 查看页面错误
- 使用 `recordVideo` 和 `recordTrace` 记录操作过程

### 6. 错误处理
```javascript
// 所有工具调用失败时会返回错误信息
// 建议在使用时：
1. 先检查浏览器是否已启动
2. 使用 wait_for_selector 确保元素加载完成
3. 设置合理的超时时间
4. 使用 try-catch 处理异常情况
```

---

## 注意事项

1. **路径格式**：Windows系统使用双反斜杠 `\\` 或正斜杠 `/`
   - 正确：`C:\\Users\\Admin\\file.pdf` 或 `C:/Users/Admin/file.pdf`
   - 错误：`C:\Users\Admin\file.pdf`

2. **超时设置**：默认超时为30秒，可根据需要调整
   - 网络慢时增加超时时间
   - 快速操作可减少超时时间

3. **截图返回**：截图返回base64编码的图片数据
   - 可保存到文件或直接使用

4. **Cookie域名**：设置Cookie时必须指定正确的域名
   - 域名必须与当前页面匹配

5. **JavaScript执行**：evaluate中的代码在页面上下文执行
   - 可访问页面的DOM和全局变量
   - 返回值必须是可序列化的

6. **设备模拟**：支持的设备名称参考Playwright设备列表
   - 常用：'iPhone 13', 'Pixel 5', 'iPad Pro'

7. **权限授予**：某些功能需要先授予权限
   - 地理位置需要 'geolocation' 权限
   - 通知需要 'notifications' 权限

---

## 工具总数统计

- **浏览器管理**: 8个工具
- **页面导航**: 4个工具
- **元素交互**: 12个工具
- **键盘鼠标操作**: 5个工具
- **内容提取**: 11个工具
- **高级选择器**: 5个工具
- **等待操作**: 5个工具
- **截图和PDF**: 3个工具
- **JavaScript执行**: 3个工具
- **Cookie和存储**: 8个工具
- **网络控制**: 7个工具
- **文件操作**: 2个工具
- **视口和设备**: 4个工具
- **滚动操作**: 2个工具
- **性能指标**: 1个工具
- **无障碍功能**: 1个工具
- **时间控制**: 3个工具
- **权限管理**: 2个工具
- **对话框处理**: 1个工具
- **Frame操作**: 1个工具

**总计：101个核心工具**

---

## 版本信息

- **版本**: 2.0.0
- **更新日期**: 2024
- **Playwright版本**: 最新稳定版
- **支持平台**: Windows, macOS, Linux

---

## 技术支持

如遇到问题，请检查：
1. Playwright是否正确安装
2. 浏览器驱动是否已下载
3. 选择器是否正确
4. 超时时间是否足够
5. 网络连接是否正常

更多信息请参考：
- Playwright官方文档：https://playwright.dev
- 项目README文档
- Windows兼容性指南
