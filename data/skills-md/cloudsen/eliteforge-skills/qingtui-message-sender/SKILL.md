---
name: qingtui-message-sender
description: 在 macOS 上通过轻推桌面版向指定联系人发送文本消息。用户提供联系人名称和消息内容时使用，例如“打开轻推，给张三发送：xxx”“用轻推给某人发一句话”。运行前必须已安装轻推桌面版，并给当前终端或 Codex 授予辅助功能权限；脚本会用截图 + OCR 做发送前校验，因此通常还需要屏幕录制权限。执行时只做精确匹配：先搜索联系人，再校验当前会话标题与目标完全一致；匹配失败就停止，避免误发。
---

# QingTui Message Sender

## 目标
调用 `scripts/send_qingtui_message.swift`，在 macOS 轻推桌面版里给指定联系人发送一段纯文本。

## 必填参数
- `contact`：联系人显示名，必须与轻推会话标题精确一致。
- `message`：要发送的纯文本内容。

## 前置条件
- 已安装轻推桌面版。
- 当前终端或 Codex 已授予 macOS 辅助功能权限。
- 建议同时授予屏幕录制权限，因为脚本会截屏并用 OCR 校验联系人和消息。
- 只支持文本消息，不支持图片、文件、卡片。

## 工作流
1. 校验 `contact` 和 `message` 非空。
2. 运行脚本：
   - `swift scripts/send_qingtui_message.swift --contact "<contact>" --message "<message>"`
3. 脚本会自动：
   - 打开或激活轻推。
   - 聚焦左上角搜索框并搜索联系人。
   - 用 OCR 在搜索结果里查找精确匹配项。
   - 打开会话后再次校验标题完全等于 `contact`。
   - 校验通过后把文本写入输入区并回车发送。

## 调试
- 只验证定位，不真正发送：
  - `swift scripts/send_qingtui_message.swift --contact "<contact>" --message "<message>" --dry-run`

## 安全规则
- 只接受精确标题匹配，不做模糊猜测。
- 找不到联系人、权限不足、截图失败、OCR 校验失败、界面结构异常时，直接报错并停止。
- 轻推当前是 Chrome App 包装界面，脚本依赖当前桌面布局；如果轻推大版本改版，需要同步更新脚本。
