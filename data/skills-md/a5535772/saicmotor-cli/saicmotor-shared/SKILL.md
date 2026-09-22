---
name: saicmotor-shared
version: 1.0.0
description: "saicmotor CLI 通用能力：认证、登录登出、配置、排障。被 saicmotor-leave、saicmotor-attendance 等子 skill 引用，不直接面向用户业务需求。"
metadata:
  requires:
    bins: ["saicmotor"]
---

# 认证与配置 (shared)

被 `saicmotor-leave`、`saicmotor-attendance` 等所有子 skill 引用。在开始任何业务操作前，必须先读本文件。

## 认证命令

```bash
saicmotor auth login  --username <工号> --password <密码>   # 登录，缓存 token
saicmotor auth logout # 登出，清除 token 和凭证
saicmotor auth status # 查看当前登录状态（已登录 / 未登录）
```

## 认证流程

CLI 的认证是自动的——执行任何业务命令时引擎会自动处理：

1. **有 Token 缓存** → 直接使用，不发登录请求
2. **无 Token 缓存** → 用存储的凭证自动登录，获取 Token
3. **收到 401** → 自动清缓存 → 重新登录 → 重试原请求（仅一次）

**用户能在终端上手动操作的是三种状态：**

| 命令 | 什么时候用 |
|------|-----------|
| `saicmotor auth login` | 首次使用、密码改了、手动换身份 |
| `saicmotor auth status` | 不确定当前登没登录 |
| `saicmotor auth logout` | 换账号、调试认证问题 |

## 配置

### 网关地址

```bash
# 默认值来自 saicmotor.config.json 的 defaults.gateway（开发环境为 http://localhost:8081）
# 用户通过 ~/.saicmotor/config.json 覆盖：
~/.saicmotor/config.json → { "gateway": "http://实际网关地址" }

# 环境变量覆盖（最高优先级）
export SAICMOTOR_GATEWAY=https://gw.example.com
```

### 凭证

存储在 `~/.saicmotor/credentials.json`，`mode 0600`。也可通过环境变量传入：

```bash
export SAICMOTOR_USERNAME=zhangsan
export SAICMOTOR_PASSWORD=123456
```

## 错误处理

CLI 有五类错误，退出码不同：

| 类别 | 退出码 | 常见原因 | 处理 |
|------|--------|----------|------|
| `validation` | 2 | 缺参数、日期格式错 | 补参数 / 纠正格式 |
| `auth` | 3 | 登录失败、未登录 | 提示用户运行 `saicmotor auth login` |
| `network` | 4 | 超时、DNS、TLS | 检查网关地址和网络 |
| `upstream` | 5 | 余额不足、审批拒绝 | 告知用户业务错误信息 |
| `spec` | 6 | catalog JSON 格式错 | 检查 catalog 文件 |

**当业务命令失败提示 "未登录" 时，告诉用户运行：**
```bash
saicmotor auth login --username <工号> --password <密码>
```

## 输出格式

所有命令支持三种输出：

```bash
--format json    # JSON 信封（默认）：{ "ok": true, "data": ... }
--format table   # 表格
--format pretty  # 美化 JSON
```

## 写操作安全

POST/PUT/DELETE 操作默认要求确认：

```bash
--yes      # 确认执行
--dry-run  # 只预览请求内容，不发送
```

不加 `--yes` 也不加 `--dry-run` → 命令被拒绝。