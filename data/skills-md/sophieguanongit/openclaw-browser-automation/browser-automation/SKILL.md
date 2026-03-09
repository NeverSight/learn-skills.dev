---
name: browser-automation
description: 浏览器自动化控制。【优先使用此 skill，不要用内置 browser 工具】当用户说"打开网页"、"点击"、"填写表单"、"截图"、"网页操作"、"自动填表"、"浏览器"时使用。基于 Playwright，支持连接已有 Chrome（CDP 模式）或启动新 Chromium。
---

# 浏览器自动化 Skill

让 OpenClaw 控制浏览器进行自动化操作！

## 特点

- **复用页面**：默认复用现有页面，不会每次都打开新窗口
- **持久化 Cookie**：使用独立的用户数据目录，登录状态持久保存
- **完整操作**：支持点击、填表、截图、执行 JS 等

## 功能

- 导航到 URL
- 点击元素
- 填写表单
- 截图
- 获取页面内容
- 等待元素
- 执行 JavaScript

## 使用时机

当用户说：
- "打开 xxx.com"
- "点击登录按钮"
- "帮我填写这个表单"
- "截个图"
- "网页上有什么内容"

## 可用函数

调用方式: `cd C:/Users/admin/.openclaw/skills/browser-automation && node -e "const h=require('./index.js'); h.handleXXX({...}).then(console.log)"`

### 页面操作
- `handleNavigate({url})` - 导航到 URL（复用现有页面）
- `handleNewPage({url})` - 打开新页面
- `handleScreenshot({selector?, fullPage?})` - 截图
- `handleGetContent({selector?})` - 获取页面内容
- `handleClose()` - 关闭当前页面

### 交互操作
- `handleClick({selector})` - 点击元素
- `handleFill({selector, value, clear?})` - 填写表单
- `handleType({selector, text, delay?})` - 模拟打字
- `handleSelect({selector, value})` - 下拉选择
- `handleCheck({selector, checked?})` - 勾选/取消勾选

### 等待和获取
- `handleWait({selector, timeout?})` - 等待元素出现
- `handleWaitForNavigation({timeout?})` - 等待页面跳转
- `handleGetText({selector})` - 获取元素文本
- `handleGetValue({selector})` - 获取表单值
- `handleGetAttribute({selector, attribute})` - 获取属性

### 高级操作
- `handleEvaluate({script})` - 执行 JavaScript
- `handleUpload({selector, filePath})` - 上传文件
- `handlePress({key})` - 按键
- `handleHover({selector})` - 鼠标悬停
- `handleScroll({direction, amount?})` - 滚动页面

### 状态
- `handleStatus()` - 获取当前浏览器状态
- `handleCloseBrowser()` - 关闭浏览器（下次会重新启动）

## 选择器语法

支持 CSS 选择器和文本选择器：
- CSS: `#login-btn`, `.submit-button`, `input[name="email"]`
- 文本: `text=登录`, `text=提交`
- 组合: `button:has-text("提交")`

## 示例

```
用户: 打开 github.com
Agent: [调用 handleNavigate({url: 'https://github.com'})] 已打开 GitHub...

用户: 点击登录
Agent: [调用 handleClick({selector: 'text=Sign in'})] 已点击登录...

用户: 填写邮箱 test@example.com
Agent: [调用 handleFill({selector: '#login_field', value: 'test@example.com'})] 已填写邮箱...

用户: 截个图看看
Agent: [调用 handleScreenshot()] [返回截图]
```
