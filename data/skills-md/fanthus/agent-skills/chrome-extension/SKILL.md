---
name: chrome-extension
description: Guides creation and modification of Chrome extensions using Manifest V3. Use when building browser extensions, Chrome plugins, or when the user mentions manifest.json, content scripts, background service worker, popup, or extension permissions.
---

# Chrome 插件开发

## 适用范围

本 Skill 用于在 Cursor 中制作或修改 Chrome 扩展（Manifest V3）。涉及 manifest 结构、content script、background、popup、权限与消息通信时按此执行。

## 扩展结构（Manifest V3）

必须使用 Manifest V3；V2 已弃用。

**最小 manifest.json 示例：**

```json
{
  "manifest_version": 3,
  "name": "扩展名称",
  "version": "1.0.0",
  "description": "扩展描述",
  "permissions": [],
  "optional_permissions": [],
  "host_permissions": []
}
```

常用入口与字段：

| 入口 | 用途 |
|-----|------|
| `background.service_worker` | 常驻逻辑（事件、定时、跨标签协调） |
| `action.default_popup` | 点击扩展图标时的弹窗 HTML |
| `content_scripts` | 注入到匹配网页的 JS/CSS |
| `options_page` | 设置页 |

## 权限

- **permissions**：声明即安装时请求（如 `storage`、`tabs`、`scripting`）。
- **host_permissions**：可访问的 URL（如 `https://*/*`、`<all_urls>`）。
- **optional_permissions**：运行时通过 `chrome.permissions.request()` 再请求。

仅声明实际需要的权限；敏感权限（如 `<all_urls>`）要能向用户解释用途。

## Background（Service Worker）

- 文件在 manifest 中通过 `background.service_worker` 指定，单文件，ES modules 需设 `"type": "module"`。
- 无 DOM、无 `window`；用 `chrome.*` API 与 `chrome.runtime` 消息。
- 空闲一段时间会被终止，不能依赖全局变量长期保存状态；持久化用 `chrome.storage`。

常用：监听 `chrome.runtime.onInstalled`、`chrome.tabs.onUpdated`、`chrome.alarms`，以及用 `chrome.runtime.sendMessage` / `chrome.tabs.sendMessage` 与 popup/content script 通信。

## Content Script

- 在 `content_scripts` 里指定 `matches`（URL 模式）、`js`、`css`。
- 运行在隔离的 JS 环境，与页面脚本不共享全局；可访问 DOM，不能直接访问页面的 `window` 变量。
- 与 background 通信：`chrome.runtime.sendMessage`；收：`chrome.runtime.onMessage`。
- 需操作页面脚本上下文时，通过注入 `<script>` 到页面再配合 `window.postMessage` 与 content script 交换数据。

## Popup

- 普通 HTML + JS 页面；生命周期短暂，关闭即销毁。
- 需要数据时从 `chrome.storage` 读，或向 background 发消息获取。
- 不要在此做长时间异步初始化；打开前在 background 准备好数据更稳妥。

## 消息通信

- **popup/content → background**：`chrome.runtime.sendMessage(message, response => {...})`。
- **background → content**：`chrome.tabs.sendMessage(tabId, message, response => {...})`；需先有 content script 注入到该 tab。
- 接收端：`chrome.runtime.onMessage.addListener((message, sender, sendResponse) => { ...; return true; })`。异步回复时必须 `return true` 并在回调里调用 `sendResponse`。

## 存储

- **chrome.storage.local**：本地，容量较大，适合扩展私有数据。
- **chrome.storage.sync**：跨设备同步，有配额限制。
- **chrome.storage.session**（MV3）：仅当前会话，关浏览器即清空。

读写均为异步：`chrome.storage.local.get/set(...)`。

## 常用清单片段

**带 background + popup + content script：**

```json
{
  "manifest_version": 3,
  "name": "示例扩展",
  "version": "1.0.0",
  "permissions": ["storage", "activeTab"],
  "host_permissions": ["https://*/*"],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup.html",
    "default_title": "打开面板"
  },
  "content_scripts": [
    {
      "matches": ["https://example.com/*"],
      "js": ["content.js"],
      "css": ["content.css"]
    }
  ]
}
```

## 开发与调试

- 代码修改后到 `chrome://extensions` 点击「重新加载」。
- Background：扩展页「Service Worker」链接打开 DevTools。
- Content script：在对应网页的 DevTools 里选该扩展的 context 查看。
- Popup：右键扩展图标 →「检查弹出内容」。

## 注意事项

- MV3 中不再有 persistent background page；长时间逻辑用 `chrome.alarms` 或由用户操作触发。
- 注入脚本优先用 `chrome.scripting.executeScript`（需 `scripting` 权限）做动态注入，必要时再配合 `content_scripts`。
- 上架 Chrome 商店需满足 [Chrome 网上应用店计划政策](https://developer.chrome.com/docs/webstore/program-policies/)；权限与隐私说明要清晰。