---
name: iconfont-downloader
description: |
  Iconfont图标下载器 Skill 可以帮助用户从 iconfont.cn 搜索并下载最匹配的 SVG 图标。
---

# Iconfont图标下载器 Skill

从 iconfont.cn 搜索并下载最匹配的 SVG 图标。支持多种浏览器自动化方式（MCP > Playwright > Puppeteer），搜索后展示结果让用户选择。

## 功能特性

- 🔐 **多种登录方式**：支持账号密码登录、二维码登录
- 🌐 **多种浏览器自动化**：优先使用 MCP，其次 Playwright，最后 Puppeteer
- 🔍 **关键词搜索**：中英文关键词搜索图标
- 📋 **结果展示**：搜索后以表格形式展示，让用户选择
- 💾 **单个下载**：根据用户选择下载指定图标
- 📦 **批量下载**：支持批量下载多个图标
- 🔄 **结果缓存**：搜索结果缓存，方便批量选择

## 安装方法

### 方法1：通过 Skill 市场安装（推荐）

待 Skill 市场上线后，可以直接在应用内搜索 "iconfont-downloader" 安装。

### 方法2：手动安装

1. 将整个 `iconfont-downloader` 目录复制到应用的 skills 目录：
   - Windows: `%APPDATA%/SuperClientR/skills/`
   - macOS: `~/Library/Application Support/SuperClientR/skills/`
   - Linux: `~/.config/SuperClientR/skills/`

2. 重启应用，在设置中启用该 skill

### 方法3：开发模式安装

```bash
# 在项目根目录执行
pnpm skill:install ./skills/iconfont-downloader
```

## 依赖安装

### 优先级说明

此 skill 会自动检测并使用以下工具（按优先级排序）：

1. **MCP 浏览器工具**（如果可用）- 无需额外安装
2. **Playwright** - `pnpm add playwright`
3. **Puppeteer** - `pnpm add puppeteer`

如果检测到 MCP 浏览器工具，无需安装其他依赖。

### 安装 Playwright（推荐）

```bash
cd skills/iconfont-downloader
npm install playwright
# 或者
pnpm add playwright
```

### 安装 Puppeteer（备选）

```bash
cd skills/iconfont-downloader
npm install puppeteer
# 或者
pnpm add puppeteer
```

## 使用方法

### 1. 登录

登录是必须的，其他工具都需要登录后才能使用。

**方式一：账号密码登录**

```json
{
  "tool": "iconfont-downloader.login",
  "input": {
    "username": "your_username",
    "password": "your_password"
  }
}
```

**方式二：二维码登录**

```json
{
  "tool": "iconfont-downloader.login",
  "input": {
    "useQRCode": true
  }
}
```

登录时会打开浏览器窗口，二维码登录需要在 60 秒内完成扫码。

### 2. 搜索图标

```json
{
  "tool": "iconfont-downloader.search",
  "input": {
    "keyword": "home",
    "limit": 10,
    "page": 1
  }
}
```

返回结果示例：

```json
{
  "success": true,
  "output": {
    "total": 10,
    "keyword": "home",
    "icons": [
      {
        "序号": 1,
        "图标ID": "1234567",
        "名称": "home-line",
        "作者": "设计师A",
        "预览": "https://example.com/preview1.png"
      },
      {
        "序号": 2,
        "图标ID": "1234568",
        "名称": "home-fill",
        "作者": "设计师B",
        "预览": "https://example.com/preview2.png"
      }
    ],
    "message": "找到 10 个与 \"home\" 相关的图标",
    "instructions": "请查看上方图标列表，告诉我你想下载哪个..."
  }
}
```

### 3. 选择并下载图标

搜索完成后，用户可以看到图标列表，然后选择要下载的图标：

**方式一：按序号下载**

用户说："下载第2个"

```json
{
  "tool": "iconfont-downloader.download",
  "input": {
    "iconId": "1234568",
    "iconName": "home-fill",
    "rename": "HomeIcon"
  }
}
```

**方式二：批量下载**

用户说："下载1,3,5" 或 "下载前5个" 或 "全部下载"

```json
{
  "tool": "iconfont-downloader.downloadBatch",
  "input": {
    "selections": "1,3,5",
    "keyword": "home",
    "outputPath": "./src/renderer/src/components/icons"
  }
}
```

支持的选择格式：
- `"1,2,3"` - 下载第1、2、3个
- `"1-5"` - 下载第1到5个
- `"前5个"` - 下载前5个
- `"all"` 或 `"全部"` - 下载全部

### 4. 检查登录状态

```json
{
  "tool": "iconfont-downloader.checkLoginStatus",
  "input": {}
}
```

### 5. 退出登录

```json
{
  "tool": "iconfont-downloader.logout",
  "input": {}
}
```

## 完整使用流程示例

```
用户: 帮我下载一个首页图标

AI: 我需要先登录 iconfont.cn。请选择登录方式：
1. 账号密码登录 - 请提供用户名和密码
2. 二维码登录 - 我会打开浏览器让您扫码

用户: 用二维码登录

AI: [调用 login 工具，useQRCode: true]
     已打开浏览器，请使用淘宝/支付宝/微博扫码登录...

AI: 登录成功！现在搜索首页图标...

AI: [调用 search 工具，keyword="首页"]

AI: 找到 10 个相关图标：

| 序号 | 图标ID   | 名称        | 作者     |
|------|----------|-------------|----------|
| 1    | 1234567  | 首页-line   | 设计师A  |
| 2    | 1234568  | 首页-fill   | 设计师B  |
| 3    | 1234569  | home-icon   | 设计师C  |
...

请问你想下载哪个？可以告诉我：
- 序号（如"下载第2个"）
- 多个序号（如"下载1,3,5"）
- 范围（如"下载前5个"）
- 全部（如"全部下载"）

用户: 下载第2个

AI: [调用 download 工具，iconId="1234568", iconName="首页-fill"]

AI: 图标下载成功！已保存到 src/renderer/src/components/icons/首页-fill.svg
```

## 批量下载示例

```
用户: 把这些图标的前5个都下载了

AI: [调用 downloadBatch 工具]

AI: 批量下载完成：5 成功，0 失败
- 图标1.svg ✓
- 图标2.svg ✓
- 图标3.svg ✓
- 图标4.svg ✓
- 图标5.svg ✓
```

## 目录结构

```
iconfont-downloader/
├── scripts/
│   ├── manifest.json      # Skill 配置
│   ├── index.ts          # 主实现文件
│   ├── index.js          # 编译后的 JS 文件
│   └── package.json      # 依赖配置
├── SKILL.md              # 本说明文档
└── IMPLEMENTATION_GUIDE.md # 实现指南
```

## 技术实现

### 浏览器自动化优先级

1. **MCP 浏览器工具**
   - 检查 `globalThis.mcp` 是否可用
   - 无需额外依赖
   - 由 host 应用统一管理浏览器实例

2. **Playwright**
   - 动态导入 `playwright`
   - 支持 Chromium/Firefox/WebKit
   - 更好的现代 Web 支持

3. **Puppeteer**
   - 动态导入 `puppeteer`
   - Chrome DevTools Protocol
   - 成熟稳定

### 搜索实现

优先使用 iconfont API (`/api/icon/search.json`)，失败时回退到页面爬取。

### 登录实现

- 打开浏览器访问 `https://www.iconfont.cn/login`
- 支持账号密码自动填充
- 支持验证码检测（提示用户手动处理）
- 登录成功后提取 cookies 用于后续 API 调用

## 注意事项

1. **登录安全**：
   - 密码仅在登录过程中使用，不会保存到磁盘
   - 登录 session 以 cookies 形式保存在内存中
   - 建议定期调用 `checkLoginStatus` 检查 session 有效性

2. **Session 有效期**：
   - iconfont 的 session 可能会过期
   - 如遇到登录失效错误，需要重新调用 `login`

3. **反爬虫**：
   - 请合理使用，避免频繁请求
   - 搜索间隔建议保持合理时间

4. **版权问题**：
   - 下载的图标请遵守原作者的版权声明
   - 商用请注意图标授权协议

5. **浏览器依赖**：
   - 首次使用 Playwright/Puppeteer 可能需要下载浏览器
   - 下载可能需要一些时间，请耐心等待

## 故障排除

### 登录失败

- 检查用户名和密码是否正确
- 检查是否需要验证码（当前需要手动在浏览器中完成验证）
- 检查网络连接
- 尝试使用二维码登录

### 搜索无结果

- 尝试使用英文关键词
- 检查是否已登录
- 检查登录状态是否过期（调用 checkLoginStatus）

### 下载失败

- 检查目标目录是否有写入权限
- 检查磁盘空间
- 检查是否已登录

### 浏览器工具未检测到

```
错误：未检测到浏览器自动化工具
```

解决方案：
```bash
cd skills/iconfont-downloader
pnpm add playwright
# 或
pnpm add puppeteer
```

## 更新日志

### v2.0.0

- ✨ 新增批量下载功能 (`downloadBatch`)
- ✨ 支持多种浏览器自动化方式（MCP > Playwright > Puppeteer）
- ✨ 搜索结果缓存机制
- ✨ 智能选择解析（支持序号、范围、自然语言）
- ♻️ 重构登录流程，支持二维码登录
- ♻️ 优化搜索结果展示格式

### v1.0.0

- 初始版本
- 基础登录、搜索、下载功能

## 许可证

MIT
