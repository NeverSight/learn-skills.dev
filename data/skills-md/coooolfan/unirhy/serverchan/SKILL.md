---
name: serverchan
description: 通过 Server酱³ 发送推送通知。在无人值守开发时，需要向用户发送消息、通知、提醒时使用此 skill。从环境变量 FT07_KEY 获取密钥。
---

# Server酱 推送

## 使用方法

执行脚本发送推送：

```bash
python3 scripts/send.py "标题" "简短描述"
```

## 参数说明

- `title`: 必填，推送标题
- `desp`: 可选，简短描述（保持简洁）
- 不使用 `tags` 参数

## 示例

```bash
# 仅标题
python3 scripts/send.py "任务完成"

# 带描述
python3 scripts/send.py "构建成功" "项目已部署"
```
