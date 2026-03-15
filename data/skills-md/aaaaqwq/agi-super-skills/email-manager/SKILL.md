---
name: email-manager
description: "多邮箱统一管理与智能助手。支持 Gmail、QQ邮箱等 IMAP 邮箱，定时查看邮件，AI 生成摘要和回复草稿，发送前需用户确认。"
license: MIT
metadata:
  version: 1.0.0
  domains: [email, automation, productivity]
  type: automation
---

# Email Manager - 邮箱智能管家

## 当使用此技能

- 管理多个邮箱账号（Gmail、QQ、Outlook 等）
- 定时查看邮件并生成摘要
- 智能生成回复草稿（需确认后发送）
- 重要邮件即时提醒

## 核心功能

### 1. 多账号管理
- 支持任意 IMAP 邮箱
- 使用 `pass` 安全存储凭据
- 配置文件：`config/accounts.json`

### 2. 定时任务
- 每日 8:00 和 17:00 自动检查
- 通过 OpenClaw cron 调度
- 发现重要邮件即时通知

### 3. 智能摘要
- 使用 AI 提取邮件要点
- 按优先级分类
- 推送到 WhatsApp/Telegram

### 4. 安全发送
- AI 生成回复草稿
- 发送前展示预览
- 用户确认后才发送

## 触发词

- "查看邮件"
- "邮件摘要"
- "回复邮件"
- "添加邮箱账号"
- "邮件设置"

## 配置步骤

### 1. 添加邮箱账号

```bash
# Gmail（需先开启 IMAP 并生成应用专用密码）
pass insert email/gmail/your-email@gmail.com
pass insert email/gmail/your-email@gmail.com-app-pass

# QQ 邮箱（需先开启 IMAP 服务并获取授权码）
pass insert email/qq/your-qq@qq.com
pass insert email/qq/your-qq@qq.com-auth-code
```

### 2. 更新账号配置

编辑 `config/accounts.json`：

```json
{
  "accounts": [
    {
      "name": "Gmail 主邮箱",
      "email": "your-email@gmail.com",
      "provider": "gmail",
      "imap_server": "imap.gmail.com",
      "imap_port": 993,
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "enabled": true
    },
    {
      "name": "QQ 邮箱",
      "email": "your-qq@qq.com",
      "provider": "qq",
      "imap_server": "imap.qq.com",
      "imap_port": 993,
      "smtp_server": "smtp.qq.com",
      "smtp_port": 587,
      "enabled": true
    }
  ]
}
```

### 3. 设置定时任务

使用 OpenClaw cron：

```bash
# 8:00 检查邮件
openclaw cron add --name "早间邮件检查" --schedule "0 8 * * *" --script "~/clawd/skills/email-manager/scripts/check_email.py"

# 17:00 检查邮件
openclaw cron add --name "晚间邮件检查" --schedule "0 17 * * *" --script "~/clawd/skills/email-manager/scripts/check_email.py"
```

## 安全策略

| 操作 | 权限级别 |
|------|----------|
| 读取邮件列表 | 🟢 自动 |
| 读取邮件内容 | 🟢 自动 |
| 生成摘要 | 🟢 自动 |
| 创建回复草稿 | 🟢 自动 |
| **发送邮件** | 🟡 **需确认** |
| 删除邮件 | 🔴 禁止 |

## 相关文件

- `scripts/check_email.py` - 邮件检查与摘要
- `scripts/send_email.py` - 发送邮件（需确认）
- `scripts/reply_draft.py` - 生成回复草稿
- `config/accounts.json` - 账号配置
- `config/providers.json` - 邮件服务商配置

## 常见邮箱 IMAP 配置

| 邮箱 | IMAP 服务器 | 端口 |
|------|-------------|------|
| Gmail | imap.gmail.com | 993 |
| QQ 邮箱 | imap.qq.com | 993 |
| Outlook | outlook.office365.com | 993 |
| 163 邮箱 | imap.163.com | 993 |
| 126 邮箱 | imap.126.com | 993 |

## 使用示例

### 查看邮件摘要
```
用户: 查看邮件
AI: [读取所有配置邮箱，生成摘要]
    
    📧 今日邮件摘要 (2026-02-19 08:00)
    
    Gmail 主邮箱 (3 封未读):
    1. [重要] 项目进度更新 - 张三
    2. 会议邀请：周五例会 - 李四
    3. 订单发货通知 - 淘宝
    
    QQ 邮箱 (1 封未读):
    1. 验证码通知 - 某服务
```

### 回复邮件
```
用户: 回复第1封邮件，告诉他项目进度正常
AI: [生成回复草稿]

    📝 回复草稿：
    
    收件人: 张三 <zhangsan@example.com>
    主题: Re: 项目进度更新
    
    内容:
    ---
    张三，你好！
    
    感谢你的关注。项目进度一切正常，目前按计划推进中。
    
    如有其他问题，随时联系。
    
    祝好，
    Daniel
    ---
    
    确认发送吗？（回复"确认"发送，"修改"调整，"取消"放弃）
```

---

## 故障排查

### SSL/连接问题
- **症状**: `Connection reset by peer`, `SSL: UNEXPECTED_EOF_WHILE_READING`
- **根因**: Mihomo/Clash TUN 模式劫持 IMAP 长连接不稳定
- **解决**:
  - Gmail 等海外邮箱：在 Mihomo `Merge.yaml` 添加 `DOMAIN-SUFFIX,imap.gmail.com,DIRECT`
  - QQ/163 等国内邮箱：需走国内代理出口，不可直连（海外 VPS）
  - 代码已内置 ssl_context + 3次重试 + 2s退避

### 编码问题
- **症状**: `LookupError: unknown encoding: unknown-8bit`
- **解决**: `_parse_email` 已添加 try/except 兜底用 utf-8 解码

### 超时问题
- **症状**: `check_email.py` 被 SIGKILL
- **解决**: 跳过 `test_connection`、limit 降到 10、使用 `headers_only=True`

*创建日期: 2026-02-19*
*更新日期: 2026-02-24*
*版本: 1.1.0*
