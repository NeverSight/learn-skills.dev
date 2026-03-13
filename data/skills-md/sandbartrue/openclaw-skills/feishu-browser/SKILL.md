---
name: feishu-browser
description: 通过浏览器模拟真人操作飞书网页版。包括发送/读取群聊消息、@人、创建文档、设置文档权限。当需要用瓦力账号在飞书网页上执行操作时使用此skill。
---

# Feishu Browser Skill

通过 OpenClaw browser tool (profile=openclaw) 操控飞书网页版，模拟真人操作。

## 前置条件

**本 skill 不需要飞书 API 权限。** 它通过浏览器模拟真人操作飞书网页版，只需要：
1. OpenClaw browser 已启动（`browser action=start profile=openclaw`）
2. 一个**已登录飞书的浏览器 session**（手动扫码登录一次即可）

> 💡 适合场景：外部群（API 机器人进不去）、需要以个人账号身份操作

## 环境信息

| 项目 | 值 |
|------|-----|
| 租户域名 | `ja484frx8z.feishu.cn` |
| 消息页 | `https://ja484frx8z.feishu.cn/next/messenger/` |
| Browser Profile | `openclaw` |
| Viewport | 1280×800（最低要求，聊天列表需要 ≥1280 宽度） |

## 前置条件

1. 浏览器已启动：`browser action=start profile=openclaw`
2. 飞书账号已登录（瓦力账号）
3. Viewport 设为 1280×800

## 核心操作

### 1. 发送消息

导航到消息页 → 点击目标群聊 → 清空输入框 → 写入内容 → 点击发送按钮。

**关键点：**
- 必须用 `document.execCommand('insertText')` 写入内容（innerHTML/innerText 不触发飞书框架）✅ 已验证
- 必须点击发送按钮（Enter 键无法发送）✅ 已验证
- 发送按钮位置：viewport 1280×800 下 x>1210, y>730 ✅ 已验证

👉 详细流程见 [references/send-message.md](references/send-message.md)

### 2. 读取消息

通过 `browser action=snapshot` 获取当前聊天窗口的消息列表，解析文本内容。

**快速读取（已验证）：**
```javascript
// ✅ 已验证 - 获取聊天窗口可见消息
(function(){
  var msgs = document.querySelectorAll('[class*="message"]');
  var result = [];
  msgs.forEach(function(m){ if(m.textContent.trim()) result.push(m.textContent.trim()); });
  return JSON.stringify(result.slice(-10));
})()
```

也可以直接用 `browser action=snapshot` 拿 aria tree，搜索消息内容。

### 3. @人

在输入框中输入 `@` 字符，等待选人下拉列表出现，然后点击目标人名。

👉 详细流程见 [references/send-message.md](references/send-message.md#at人)

### 4. 创建文档

通过飞书文档页面创建新文档，使用富文本编辑器输入内容。

👉 详细流程见 [references/create-doc.md](references/create-doc.md)

### 5. 设置文档权限

通过文档右上角「分享」按钮设置权限。

👉 详细流程见 [references/doc-permissions.md](references/doc-permissions.md)

### 6. 群消息监控

定期截图 + snapshot 对比检测新消息，判断是否需要回复。

👉 详细流程见 [references/monitor-chat.md](references/monitor-chat.md)

## 常用 Browser 调用模式

```
# 启动浏览器
browser action=start profile=openclaw

# 导航
browser action=navigate profile=openclaw targetUrl="https://ja484frx8z.feishu.cn/next/messenger/"

# 截图查看当前状态
browser action=screenshot profile=openclaw

# 获取页面结构
browser action=snapshot profile=openclaw

# 执行 JS
browser action=act profile=openclaw request={kind:"evaluate", fn:"..."}

# 点击元素（通过 snapshot 拿到的 ref）
browser action=act profile=openclaw request={kind:"click", ref:"e42"}
```

## 常见问题

### Q: 输入框写入内容后飞书没检测到？
A: 必须用 `execCommand('insertText')`，不能用 innerHTML 或 innerText。

### Q: 发送按钮找不到？
A: 检查 viewport 是否 ≥1280×800。发送按钮在右下角，坐标约 x>1210, y>730。

### Q: 聊天列表不显示？
A: viewport 宽度必须 ≥1280px。

### Q: 页面加载后操作失败？
A: 导航后等待 2-3 秒再操作。可用 screenshot 确认页面状态。

### Q: @人列表不出现？
A: 确保输入框已 focus，然后用 execCommand 插入 `@` 字符，等待 1-2 秒。

### Q: 聊天区域无法滚动？
A: 飞书使用虚拟列表，`scrollTop` 和 `scrollBy` 不生效。必须用键盘 PageUp/PageDown：
```
# 先 hover 到聊天区域（main ref），再按 PageUp/PageDown
browser action=act request={kind:"hover", ref:"<main_area_ref>"}
browser action=act request={kind:"press", key:"PageUp"}   # 向上滚
browser action=act request={kind:"press", key:"PageDown"}  # 向下滚
```
**⚠️ 已验证：JS 的 scrollTop/scrollBy/WheelEvent 对飞书虚拟列表无效，只有 PageUp/PageDown 有效。**
