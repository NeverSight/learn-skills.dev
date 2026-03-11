---
name: email-sender
description: 支持SMTP和API的邮件自动发送工具，内置Jinja2模板引擎，适用于自动化工作流、批量邮件发送、系统通知等场景。支持HTML邮件、多附件、模板变量、错误重试等企业级功能。
version: 1.0.0
author: "Claude Code Team"
category: automation
tags: [email, smtp, automation, template, notification]
requirements:
  - python >=3.8
  - pyyaml
  - jinja2
  - markupsafe
---

# Email Sender Skill

## 功能概述

email-sender是一个功能完整的邮件自动发送工具，支持:

- **多种发送方式**: SMTP协议和邮件服务API(SendGrid/MailGun/SES)
- **模板引擎**: 内置Jinja2模板系统,支持动态内容生成
- **附件支持**: 支持多附件上传,自动大小和类型检查
- **错误处理**: 自动重试机制,详细日志记录
- **安全保护**: 速率限制、证书验证、附件类型检查
- **配置灵活**: YAML配置文件,支持多环境切换

## 典型使用场景

1. **自动化通知**: CI/CD流水线状态通知、系统告警
2. **批量邮件**: 营销邮件、用户通知、报表分发
3. **工作流集成**: 作为自动化流程的一环发送邮件
4. **模板邮件**: 欢迎邮件、密码重置、订单确认

## 核心脚本

- `scripts/send_email.py`: 主发送脚本,处理邮件发送逻辑
- `scripts/template_manager.py`: Jinja2模板管理器
- `scripts/config_loader.py`: YAML配置加载器

## 模板资源

- `templates/default.html`: 通用邮件模板
- `templates/welcome.html`: 欢迎新用户邮件
- `templates/alert.html`: 系统警报邮件

## 配置文件

- `config/config.yaml`: 邮件服务器和功能配置
- `skill.yaml`: Skill元数据和接口定义

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置邮箱(编辑config/config.yaml)
# 3. 发送测试邮件
python scripts/send_email.py --to user@example.com --subject "测试" --body "测试内容"
```

详细文档请参考 [README.md](README.md)
