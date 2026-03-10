---
name: 1panel-api
description: 1Panel 开源面板 API Skill。提供网站管理、容器管理、数据库管理、文件管理等 23+ 个模块的完整 API 接口文档。
---

# 1Panel API Skills

🎯 **一键管理你的 1Panel 服务器**

## 快速开始

### 首次配置

首次使用本 Skill 时，请提供以下信息：

| 信息 | 说明 | 示例 |
|------|------|------|
| 1Panel 地址 | 服务器 IP 或域名 + 端口 | `http://192.168.1.100:8888` |
| API Key | 在面板「设置」→「API 密钥」中生成 | 你的密钥 |

### 获取 API Key

1. 登录 1Panel 面板
2. 进入「设置」→「API 密钥」
3. 点击「创建」生成新密钥
4. 复制生成的密钥

## 功能模块

| 模块 | 说明 |
|------|------|
| [Apps](./docs/SKILL-apps.md) | 应用商店、已安装应用管理 |
| [Websites](./docs/SKILL-websites.md) | 网站创建、配置、反向代理、SSL |
| [Containers](./docs/SKILL-containers.md) | Docker 容器管理 |
| [Databases](./docs/SKILL-databases.md) | MySQL、PostgreSQL、Redis、MongoDB |
| [Files](./docs/SKILL-files.md) | 文件上传、下载、压缩、解压 |
| [Backups](./docs/SKILL-backups.md) | 备份与恢复 |
| [Cronjobs](./docs/SKILL-cronjobs.md) | 定时任务 |
| [Runtimes](./docs/SKILL-runtimes.md) | PHP、Node、Python、Go、Java 运行环境 |
| [Hosts](./docs/SKILL-hosts.md) | 主机监控、防火墙、SSH、磁盘管理 |
| [Settings](./docs/SKILL-settings.md) | 系统配置、用户管理 |

## 认证方式

```bash
# Token 计算方式
api_key="你的API密钥"
timestamp=$(date +%s)
token=$(echo -n "1panel${api_key}${timestamp}" | openssl md5 | awk '{print $2}')

# 请求示例
curl -X GET "http://你的地址:8888/api/v2/containers/list" \
  -H "1Panel-Token: $token" \
  -H "1Panel-Timestamp: $timestamp" \
  -H "Content-Type: application/json"
```

## 了解更多

- 📖 完整 API 文档：见 [docs](./docs/) 目录
- ❓ 常见问题：见 [README.md](./README.md)
- 🔧 1Panel 官网：https://1panel.cn/
