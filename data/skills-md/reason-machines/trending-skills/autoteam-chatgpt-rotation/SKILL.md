---
name: autoteam-chatgpt-rotation
description: AutoTeam ChatGPT Team账号自动轮转管理工具，支持Codex额度监控、自动换号、CPA认证同步
triggers:
  - set up AutoTeam for ChatGPT account rotation
  - configure ChatGPT Team account manager
  - automate Codex quota monitoring and switching
  - sync CPA authentication files automatically
  - deploy AutoTeam with Docker
  - rotate ChatGPT Team accounts when quota is low
  - set up AutoTeam web dashboard
  - manage ChatGPT Team members with AutoTeam
---

# AutoTeam — ChatGPT Team账号自动轮转管理

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

AutoTeam 是一个自动化工具，用于管理 ChatGPT Team 账号的轮转：自动注册账号、获取 Codex OAuth 认证、监控额度余量、在额度低时智能切换账号，并将认证文件同步到 [CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)。

## 安装

### 前置条件

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) 包管理器
- Chromium（由 Playwright 管理）

### 一键安装

```bash
git clone https://github.com/cnitlrt/AutoTeam.git
cd AutoTeam
bash setup.sh
# 等价于: uv sync && uv run playwright install chromium
```

### 手动安装

```bash
uv sync
uv run playwright install chromium
cp .env.example data/.env
# 编辑 data/.env 填入必要配置
```

## 配置

### 环境变量（`data/.env`）

```env
# 临时邮箱服务（CloudMail）
CLOUDMAIL_API_KEY=$CLOUDMAIL_API_KEY
CLOUDMAIL_DOMAIN=example.com

# CPA（CLIProxyAPI）连接
CPA_BASE_URL=http://your-cpa-host:port
CPA_API_KEY=$CPA_API_KEY

# AutoTeam API 鉴权
AUTOTEAM_API_KEY=$AUTOTEAM_API_KEY

# ChatGPT Team 管理员账号
TEAM_ADMIN_EMAIL=admin@example.com
TEAM_ADMIN_PASSWORD=$TEAM_ADMIN_PASSWORD

# 额度阈值（低于此值触发轮转）
QUOTA_THRESHOLD=100

# Team 目标成员数
TEAM_SIZE=5

# Web 面板端口
PORT=8787
```

### 首次启动配置向导

```bash
uv run autoteam api
# 首次启动自动引导配置 CloudMail、CPA、API Key 并验证连通性
```

## CLI 命令

```bash
# 启动 Web 面板 + HTTP API（推荐，默认端口 8787）
uv run autoteam api

# 智能轮转，补满到 N 个账号（默认 5）
uv run autoteam rotate
uv run autoteam rotate 8

# 查看所有账号状态和额度
uv run autoteam status

# 检查所有账号额度
uv run autoteam check

# 手动添加一个新账号
uv run autoteam add

# 补满成员到目标数量
uv run autoteam fill
uv run autoteam fill 10

# 清理多余成员
uv run autoteam cleanup
uv run autoteam cleanup 5

# 同步认证文件到 CPA
uv run autoteam sync

# 管理员登录（刷新 admin session）
uv run autoteam admin-login
```

## Docker 部署

### 快速启动

```bash
git clone https://github.com/cnitlrt/AutoTeam.git && cd AutoTeam
mkdir -p data && cp .env.example data/.env
# 编辑 data/.env
docker compose up -d
```

### `docker-compose.yml` 结构

```yaml
services:
  autoteam:
    build: .
    ports:
      - "8787:8787"
    volumes:
      - ./data:/app/data   # 持久化配置、数据库、认证文件
    environment:
      - TZ=Asia/Shanghai
    restart: unless-stopped
```

### Docker 常用操作

```bash
# 查看实时日志
docker compose logs -f autoteam

# 重启服务
docker compose restart autoteam

# 进入容器执行 CLI
docker compose exec autoteam uv run autoteam status

# 停止服务
docker compose down
```

## HTTP API

所有 API 请求需携带鉴权头：

```
Authorization: Bearer $AUTOTEAM_API_KEY
```

### 核心端点

```bash
# 获取账号状态列表
GET /api/accounts

# 触发轮转任务
POST /api/rotate
Content-Type: application/json
{"target": 5}

# 检查额度
POST /api/check

# 补满成员
POST /api/fill
{"target": 5}

# 清理多余成员
POST /api/cleanup
{"keep": 5}

# 同步认证到 CPA
POST /api/sync

# 获取任务历史
GET /api/tasks

# 获取实时日志
GET /api/logs

# 获取/更新巡检配置
GET /api/patrol/config
PUT /api/patrol/config
Content-Type: application/json
{"enabled": true, "interval_minutes": 30, "threshold": 100}
```

### Python 调用示例

```python
import httpx
import os

BASE_URL = "http://localhost:8787"
HEADERS = {"Authorization": f"Bearer {os.environ['AUTOTEAM_API_KEY']}"}

# 获取账号状态
with httpx.Client() as client:
    resp = client.get(f"{BASE_URL}/api/accounts", headers=HEADERS)
    accounts = resp.json()
    for acc in accounts:
        print(f"{acc['email']}: quota={acc['quota']}, status={acc['status']}")

# 触发轮转
with httpx.Client(timeout=300) as client:
    resp = client.post(
        f"{BASE_URL}/api/rotate",
        headers=HEADERS,
        json={"target": 5}
    )
    task = resp.json()
    print(f"Task ID: {task['task_id']}, Status: {task['status']}")
```

## Web 管理面板

访问 `http://localhost:8787` 后查看以下页面：

| 页面 | 功能 |
|------|------|
| 📊 仪表盘 | 账号统计、状态表格、登录/移出/删除/同步操作 |
| 👥 Team 成员 | 全部 Team 成员（含外部成员）列表 |
| ⚡ 操作 & 任务 | 一键轮转/检查/补满/清理/同步 + 任务历史 |
| 📋 日志 | 实时日志查看器 |
| ⚙️ 设置 | 管理员登录 + 主号 Codex 同步 + 巡检配置 |

## 工作原理

### 轮转流程

```
检查额度
  └─ 低于阈值?
       ├─ 否 → 退出
       └─ 是 → 移出当前账号
                └─ 有备用账号?
                     ├─ 是 → 验证额度 → 加入 Team → 同步 CPA
                     └─ 否 → 注册新账号
                              └─ 临时邮箱 → ChatGPT 注册
                                   └─ 验证码 → Codex OAuth
                                        └─ 加入 Team → 同步 CPA
```

### 账号状态机

```
new → registering → registered → codex_auth → active → low_quota → removed
                        ↓                                              ↑
                      failed                                      (可复用)
```

## 常见模式

### 自动化巡检脚本

```python
import httpx
import os
import time

BASE_URL = os.environ.get("AUTOTEAM_BASE_URL", "http://localhost:8787")
HEADERS = {"Authorization": f"Bearer {os.environ['AUTOTEAM_API_KEY']}"}

def check_and_rotate():
    """检查额度，必要时触发轮转"""
    with httpx.Client(timeout=60) as client:
        # 先检查额度
        check_resp = client.post(f"{BASE_URL}/api/check", headers=HEADERS)
        check_resp.raise_for_status()
        
        # 获取账号状态
        accounts_resp = client.get(f"{BASE_URL}/api/accounts", headers=HEADERS)
        accounts = accounts_resp.json()
        
        low_quota = [a for a in accounts if a.get("quota", 999) < 100 and a["status"] == "active"]
        
        if low_quota:
            print(f"检测到 {len(low_quota)} 个低额度账号，触发轮转...")
            rotate_resp = client.post(
                f"{BASE_URL}/api/rotate",
                headers=HEADERS,
                json={"target": 5},
                timeout=300
            )
            print(f"轮转结果: {rotate_resp.json()}")
        else:
            print("所有账号额度正常")

if __name__ == "__main__":
    check_and_rotate()
```

### 配置巡检（通过 API）

```python
import httpx
import os

BASE_URL = "http://localhost:8787"
HEADERS = {"Authorization": f"Bearer {os.environ['AUTOTEAM_API_KEY']}"}

# 开启自动巡检，每 30 分钟检查一次，额度低于 100 触发轮转
with httpx.Client() as client:
    resp = client.put(
        f"{BASE_URL}/api/patrol/config",
        headers=HEADERS,
        json={
            "enabled": True,
            "interval_minutes": 30,
            "threshold": 100,
            "target_size": 5
        }
    )
    print(resp.json())
```

### 批量同步认证文件

```python
import httpx
import os

BASE_URL = "http://localhost:8787"
HEADERS = {"Authorization": f"Bearer {os.environ['AUTOTEAM_API_KEY']}"}

def sync_active_accounts():
    """只同步 active 账号的认证文件到 CPA"""
    with httpx.Client(timeout=120) as client:
        resp = client.post(f"{BASE_URL}/api/sync", headers=HEADERS)
        result = resp.json()
        print(f"同步结果: 成功={result.get('synced', 0)}, 失败={result.get('failed', 0)}")
        return result

sync_active_accounts()
```

## 故障排查

### 注册失败 / 验证码超时

```bash
# 问题：验证码有效期短，网络延迟导致失败
# 解决：使用延迟低的代理，或住宅代理
# 配置代理（在 .env 中）
HTTP_PROXY=http://user:pass@proxy-host:port
HTTPS_PROXY=http://user:pass@proxy-host:port
```

### Playwright 浏览器问题

```bash
# 重新安装 Chromium
uv run playwright install chromium

# Docker 中确认浏览器依赖
docker compose exec autoteam uv run playwright install-deps chromium
```

### CPA 同步失败

```bash
# 验证 CPA 连接
curl -H "Authorization: Bearer $CPA_API_KEY" $CPA_BASE_URL/health

# 检查 AutoTeam 日志
uv run autoteam api  # 查看 Web 面板日志页
# 或
docker compose logs -f autoteam | grep "sync"
```

### 账号被封 / IP 被标记

```bash
# 症状：注册成功率低，频繁出现 Cloudflare 挑战
# 解决方案：
# 1. 使用住宅代理（非 VPS IP）
# 2. 降低注册频率，在 .env 中增加延迟
REGISTER_DELAY_SECONDS=30

# 3. 减少并发（AutoTeam 同时只允许一个 Playwright 操作）
```

### 查看详细日志

```bash
# CLI 模式下增加详细输出
uv run autoteam rotate --verbose

# Docker 中查看完整日志
docker compose logs --tail=200 autoteam

# Web 面板实时日志
# 访问 http://localhost:8787 → 日志页面
```

### 数据库重置

```bash
# 清除本地数据（保留配置）
rm data/autoteam.db

# 重新启动后会自动初始化
uv run autoteam api
```

## 项目结构

```
AutoTeam/
├── data/               # 持久化数据（.env、数据库、认证文件）
│   ├── .env
│   └── autoteam.db
├── docs/               # 详细文档
│   ├── getting-started.md
│   ├── configuration.md
│   ├── docker.md
│   ├── api.md
│   ├── architecture.md
│   └── troubleshooting.md
├── src/autoteam/       # 源码
│   ├── cli.py          # CLI 入口
│   ├── api.py          # FastAPI 应用
│   ├── rotator.py      # 轮转核心逻辑
│   ├── browser.py      # Playwright 自动化
│   ├── quota.py        # 额度检查
│   └── sync.py         # CPA 同步
├── frontend/           # Vue 3 Web 面板
├── docker-compose.yml
├── setup.sh
└── pyproject.toml
```

## 重要限制

- **IP 风险**：VPS IP 容易被 OpenAI/Cloudflare 标记，强烈建议使用住宅代理
- **并发限制**：同一时间只允许一个 Playwright 操作，避免竞态
- **服务条款**：使用本工具可能违反 OpenAI 服务条款，风险自担
- **验证码时效**：OpenAI 验证码有效期极短，高延迟网络下成功率低
