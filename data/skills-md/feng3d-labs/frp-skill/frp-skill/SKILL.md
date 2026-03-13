---
name: frp-skill
description: 部署 frp (fatedier/frp) 实现内网穿透，将本地服务暴露到公网。当用户需要配置 frp 反向代理、配置 frpc/frps、通过公网服务器暴露本地 HTTP/TCP 服务、或进行 NAT 穿透/内网穿透时使用此技能。覆盖 Windows 客户端和 Linux 服务端部署。
---

# frp 内网穿透部署

将本地服务（如 `http://127.0.0.1:端口`）通过公网服务器暴露，实现公网访问（如 `http://example.com:端口`）。

## 工作流程

1. 收集用户参数
2. 在公网 Linux 服务器上部署 frps（服务端）
3. 在本地 Windows 机器上部署 frpc（客户端）
4. 验证连通性

## 第一步：收集参数

需要的信息：
- `SERVER_ADDR` — 公网服务器域名或 IP（如 `li.feng3d.com`）
- `LOCAL_PORT` — 本地服务端口（如 `12345`）
- `REMOTE_PORT` — 公网暴露端口（通常与 LOCAL_PORT 相同）
- `LOCAL_IP` — 本地服务 IP（默认 `127.0.0.1`）

## 第二步：部署服务端（Linux）

在公网服务器上运行 `scripts/setup_frps.sh`，一键完成下载、配置、防火墙和 systemd 设置：

```bash
bash setup_frps.sh <版本号> <公网端口>
# 示例：bash setup_frps.sh 0.67.0 12345
```

脚本会自动：
- 下载 frps 到 `/usr/local/bin/`
- 创建 `/etc/frp/frps.toml`，设置 `bindPort = 7000`
- 开放防火墙端口（7000 + 公网端口）
- 创建并启动 `frps.service`（故障自动重启、开机自启）

如需手动配置，可参考 `assets/frps.toml` 模板。

## 第三步：部署客户端（Windows）

### 重要：杀毒软件处理

Windows Defender 及其他杀毒软件（如火绒）**会自动删除 frpc.exe**，必须在下载前将部署目录加入白名单。

以**管理员身份**运行 `scripts/setup_frpc.ps1`，脚本会自动处理 Defender 排除、下载和解压：

```powershell
powershell -ExecutionPolicy Bypass -File setup_frpc.ps1 -Version "0.67.0" -Dest "C:\部署目录"
```

如果脚本无法自动添加排除（如使用非 Defender 杀毒软件），需指导用户先手动将目录加入杀毒软件白名单/信任区。

### 创建 frpc.toml

用 `assets/frpc.toml` 作为模板，替换占位符：

```toml
serverAddr = "SERVER_ADDR"
serverPort = 7000

[[proxies]]
name = "PROXY_NAME"
type = "tcp"
localIP = "127.0.0.1"
localPort = LOCAL_PORT
remotePort = REMOTE_PORT
```

### 启动客户端

```cmd
.\frpc.exe -c frpc.toml
```

看到 `start proxy success` 表示连接成功。

## 第四步：验证

浏览器访问 `http://SERVER_ADDR:REMOTE_PORT`。

## 常见问题

| 现象 | 原因 | 解决方法 |
|------|------|----------|
| frpc.exe 下载后消失 | 杀毒软件拦截删除 | 先将目录加入白名单，再重新下载 |
| 连接服务器 7000 端口被拒绝 | 防火墙未开放 | 开放服务器防火墙 7000 端口，检查云厂商安全组 |
| 公网端口无响应 | 防火墙未开放 | 开放 REMOTE_PORT，检查云厂商安全组 |
| 连接本地服务失败 | 本地服务未运行 | 确认本地服务正在运行且 LOCAL_IP:LOCAL_PORT 正确 |
