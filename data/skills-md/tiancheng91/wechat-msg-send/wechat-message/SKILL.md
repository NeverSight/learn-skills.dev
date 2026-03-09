---
name: wechat-message
description: 此技能用于在 macOS 上通过 AppleScript 自动化发送微信消息。当用户需要"发送微信消息"、"给微信好友发消息"、"微信自动发送"、"微信群里发消息"、或提到"wechat message"、"微信自动化"时使用此技能。
version: 1.0.0
---

# 微信消息发送技能

此技能通过 AppleScript 脚本实现 macOS 上微信消息的自动化发送。

## 功能概述

- 自动激活微信应用
- 搜索指定联系人或群组
- 发送指定消息内容
- 支持中文和特殊字符

## 使用方法

### 调用方式

```bash
osascript scripts/wechat_automation_script.applescript "<用户名>" "<消息内容>"
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| 用户名 | 是 | 微信联系人名称或群名称，需完全匹配 |
| 消息内容 | 是 | 要发送的消息文本 |

### 使用示例

```bash
# 发送消息给好友
osascript scripts/wechat_automation_script.applescript "张三" "你好，今天有空吗？"

# 发送消息到群组
osascript scripts/wechat_automation_script.applescript "工作群" "大家好！"

# 发送包含中文的消息
osascript scripts/wechat_automation_script.applescript "Yatocala" "hello你好"
```

## 工作流程

1. **激活微信** - 将微信窗口置于最前
2. **打开搜索** - 使用 `Cmd+F` 打开联系人搜索框
3. **搜索联系人** - 粘贴用户名并选择第一个匹配结果
4. **定位输入框** - 通过 Tab 键和点击确保焦点在输入框
5. **发送消息** - 粘贴消息内容并按回车发送
6. **隐藏窗口** - 发送完成后隐藏微信窗口

## 注意事项

- **微信必须已登录** - 执行前确保微信应用已登录
- **联系人名称需精确匹配** - 搜索时会选择第一个匹配结果
- **执行时间约 15 秒** - 脚本包含多个延时以确保稳定性
- **需要辅助功能权限** - 首次使用需授予 System Events 辅助功能权限

## 权限配置

如果脚本执行失败，请检查以下权限：

1. **系统偏好设置** → **安全性与隐私** → **隐私**
2. 选择 **辅助功能**
3. 确保以下应用已添加并勾选：
   - Terminal（或你使用的终端应用）
   - System Events

## 故障排除

| 问题 | 可能原因 | 解决方案 |
|------|----------|----------|
| 消息未发送 | 焦点未在输入框 | 检查 Tab 键次数是否足够 |
| 搜索不到联系人 | 名称不匹配 | 确认联系人名称完全一致 |
| 脚本执行中断 | 权限不足 | 检查辅助功能权限 |
| 发送中文乱码 | 编码问题 | 确保终端使用 UTF-8 编码 |

## 文件结构

```
wechat-message/
├── SKILL.md                              # 主说明文档
├── template.md                           # 消息模板
├── examples/
│   └── sample.md                         # 使用示例
└── scripts/
    └── wechat_automation_script.applescript  # AppleScript 脚本
```
