---
name: openclaw-feishu-webhook
description: 为阿里云轻量服务器上的OpenClaw配置飞书Webhook通信方式。用于将OpenClaw从企业微信改为飞书webhook模式连接。
license: MIT
---

# OpenClaw 飞书 Webhook 配置指南

## 概述

本指南帮助你在阿里云轻量服务器上配置OpenClaw使用飞书Webhook方式进行通信。主要步骤包括：
1. 连接服务器并检查当前配置
2. 更新OpenClaw配置文件
3. 安装并配置Nginx反向代理
4. 在飞书开放平台配置Webhook地址

---

## 前置条件

- 阿里云轻量服务器（已安装OpenClaw）
- 飞书企业账号（管理员权限）
- 飞书开放平台应用凭证（App ID、App Secret、Verification Token）

---

## 步骤一：连接服务器

使用SSH连接到阿里云服务器：

```bash
# 需要安装sshpass
brew install sshpass

# 连接服务器
sshpass -p '服务器密码' ssh -o StrictHostKeyChecking=no root@服务器IP
```

---

## 步骤二：检查当前OpenClaw配置

```bash
# 查看当前配置文件
cat ~/.openclaw/openclaw.json
```

关键配置项：
- `channels.feishu.connectionMode`: 应为 "webhook"
- `channels.feishu.appId`: 飞书应用ID
- `channels.feishu.appSecret`: 飞书应用密钥
- `channels.feishu.verificationToken`: 飞书验证Token

---

## 步骤三：更新OpenClaw配置文件

编辑 `~/.openclaw/openclaw.json`，确保飞书配置包含以下字段：

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxxxx",
      "appSecret": "xxxxx",
      "connectionMode": "webhook",
      "verificationToken": "your-verification-token",
      "webhookPort": 3000,
      "webhookPath": "/feishu/events",
      "webhookHost": "127.0.0.1",
      "domain": "feishu",
      "groupPolicy": "open",
      "dmPolicy": "open",
      "allowFrom": ["*"]
    }
  }
}
```

**注意**：
- `connectionMode` 必须设为 "webhook"
- `webhookPort`、`webhookPath`、`webhookHost` 是关键配置，用于内部Webhook服务

---

## 步骤四：安装并配置Nginx反向代理

OpenClaw的Webhook服务监听在内网127.0.0.1:3000，需要通过Nginx反向代理暴露给外部。

### 4.1 安装Nginx

```bash
# Alibaba Cloud Linux / CentOS / RHEL
yum install nginx --disablerepo=docker-ce-stable

# Ubuntu / Debian
apt-get install nginx
```

### 4.2 配置Nginx反向代理

创建配置文件 `/etc/nginx/conf.d/feishu.conf`：

```nginx
server {
    listen 18790;
    server_name _;

    location /feishu/events {
        proxy_pass http://127.0.0.1:3000/feishu/events;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### 4.3 启动Nginx

```bash
nginx -t
systemctl enable nginx
systemctl start nginx

# 验证端口
netstat -tlnp | grep 18790
```

---

## 步骤五：重启OpenClaw服务

```bash
systemctl --user restart openclaw-gateway

# 查看日志
tail -50 /tmp/openclaw.log
```

确认日志显示：
```
[feishu] starting feishu[default] (mode: webhook)
[feishu] feishu[default]: Webhook server listening on 127.0.0.1:3000
```

---

## 步骤六：在飞书开放平台配置

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 进入你的应用 → 「机器人」
3. 在「Webhook事件」中添加：

```
http://你的服务器IP:18790/feishu/events
```

**注意**：端口是 **18790**（Nginx监听端口），不是18789

4. 订阅事件：
   - `im.message.message_created` - 接收消息

5. 发布应用版本

---

## 步骤七：测试连接

1. 在飞书群聊中添加机器人
2. @机器人发送消息测试

---

## 常见问题

### Q: 飞书配置显示"返回数据不是合法的JSON格式"

A: 检查Webhook地址是否正确，应为：
```
http://服务器IP:18790/feishu/events
```
端口是18790，不是18789

### Q: 无法收到消息

A: 检查以下几点：
1. 确认Nginx已启动：`systemctl status nginx`
2. 确认端口开放：`netstat -tlnp | grep 18790`
3. 测试本地：`curl http://localhost:18790/feishu/events`
4. 检查OpenClaw日志：`tail -50 /tmp/openclaw.log`

### Q: 如何更新配置

A: 编辑 `~/.openclaw/openclaw.json` 后，OpenClaw会自动热加载，或者执行：
```bash
systemctl --user restart openclaw-gateway
```

---

## 配置汇总

| 配置项 | 说明 | 示例值 |
|--------|------|--------|
| 服务器IP | 阿里云公网IP | 8.137.19.64 |
| Gateway端口 | OpenClaw网关端口 | 18789 |
| Nginx端口 | Webhook暴露端口 | 18790 |
| Webhook路径 | 飞书回调路径 | /feishu/events |
| 完整URL | 飞书配置地址 | http://8.137.19.64:18790/feishu/events |
