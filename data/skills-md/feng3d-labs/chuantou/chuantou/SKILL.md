---
name: chuantou
description: Internal network tunneling system like ngrok or frp for exposing local services to the internet. Supports HTTP/WebSocket/TCP/UDP protocol forwarding with three-channel architecture.
---

# Chuantou / 穿透

内网穿透转发系统，类似 ngrok/frp，将局域网服务暴露到公网。

## 快速开始

启动服务端：
```bash
npx @feng3d/cts -p 9000 -t "my-token"
```

启动客户端：
```bash
npx @feng3d/ctc -s ws://server:9000 -t "my-token" -p "8080:3000:localhost"
```

## 系统架构

系统由服务端 (server) 和客户端 (client) 组成，采用三通道架构：

- **WebSocket 控制通道** — JSON 消息（认证/注册/心跳/连接通知）
- **TCP 数据通道** — 二进制帧（HTTP/WebSocket/TCP 数据高效转发）
- **UDP 数据通道** — UDP 数据帧（保留 UDP 语义的数据转发）

三个通道复用同一个控制端口。每个代理端口同时支持 HTTP/WebSocket/TCP/UDP 四种协议，自动识别协议类型。

通信流程：
```
外部请求 → [代理端口(TCP+UDP)] → 服务端 → (数据通道) → 客户端 → [本地服务]
```

## 命令

### 启动服务端

```bash
npx @feng3d/cts [选项]
```

选项：
- `-p, --port <端口>` - 控制端口（默认：9000）
- `-a, --host <地址>` - 监听地址（默认：0.0.0.0）
- `-t, --tokens <令牌>` - 认证令牌（逗号分隔）
- `--tls-key <路径>` - TLS 私钥文件（启用 HTTPS/WSS）
- `--tls-cert <路径>` - TLS 证书文件

### 启动客户端

```bash
npx @feng3d/ctc [选项]
```

选项：
- `-s, --server <URL>` - 服务器地址（默认：`ws://li.feng3d.com:9000`）
- `-t, --token <令牌>` - 认证令牌
- `-p, --proxies <配置>` - 代理配置（格式：`远程端口:本地端口:本地地址`）

### 代理配置格式

`远程端口:本地端口[:本地地址]`

- `远程端口`: 公网访问端口
- `本地端口`: 本地服务端口
- `本地地址`: 本地服务地址（可选，默认：localhost）

**推荐**：本地地址为 localhost 时推荐省略，使用 `8080:3000` 而非 `8080:3000:localhost`。

每个代理端口同时支持 HTTP/WebSocket/TCP/UDP 协议。

## TLS 支持

启用 TLS 加密隧道，在服务端配置：

```bash
npx @feng3d/cts --tls-key /path/to/key.pem --tls-cert /path/to/cert.pem
```

客户端需使用 `wss://` 协议：
```bash
npx @feng3d/ctc -s wss://server:9000 ...
```

## 使用示例

### 场景一：本地开发调试

将本地运行的 Vue/React 开发服务器暴露给外部访问：

```bash
# 服务端（有公网 IP 的机器）
npx @feng3d/cts -p 9000 -t "dev-token"

# 客户端（本地开发机器）
npx @feng3d/ctc -s ws://服务器IP:9000 -t "dev-token" -p "8080:5173:localhost"
```

访问 `http://服务器IP:8080` 即可访问本地开发服务器。

### 场景二：微信公众号开发

需要公网回调地址：

```bash
npx @feng3d/ctc -s ws://服务器IP:9000 -t "my-token" -p "8080:3000:localhost"
```

将 `http://服务器IP:8080` 配置为微信回调地址。

### 场景三：同时转发多个端口

```bash
npx @feng3d/ctc \
  -s ws://服务器IP:9000 \
  -t "my-token" \
  -p "8080:3000:localhost,8081:3001,8082:8000:localhost"
```

| 远程端口 | 本地端口 | 本地地址 | 用途 |
|---------|---------|---------|------|
| 8080 | 3000 | localhost | Web 服务（HTTP/WebSocket/TCP/UDP） |
| 8081 | 3001 | localhost | API 服务 |
| 8082 | 8000 | localhost | 其他服务 |

### 场景四：启用 TLS 加密

生产环境推荐启用 TLS：

```bash
# 服务端（需要域名和证书）
npx @feng3d/cts \
  --tls-key /etc/ssl/private/key.pem \
  --tls-cert /etc/ssl/certs/cert.pem \
  -t "prod-token"

# 客户端
npx @feng3d/ctc \
  -s wss://你的域名.com:9000 \
  -t "prod-token" \
  -p "8443:3000:localhost"
```

## 首次使用流程

1. **准备服务器**：需要一台有公网 IP 的机器

2. **启动服务端**：
```bash
npx @feng3d/cts -p 9000 -t "my-secret-token"
```

3. **启动客户端**（在本地机器）：
```bash
npx @feng3d/ctc \
  -s ws://服务器IP:9000 \
  -t "my-secret-token" \
  -p "8080:3000:localhost"
```

4. **访问服务**：打开浏览器访问 `http://服务器IP:8080`

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| 连接失败 | 检查服务端是否运行、令牌是否正确、地址是否正确、防火墙是否开放端口 |
| 端口被占用 | 使用 `-p` 选项指定其他端口 |
| TLS 错误 | 服务端启用 TLS 后，客户端必须使用 `wss://` 协议 |
| 隧道断开 | 客户端会自动重连，检查网络稳定性 |
| 无法访问本地服务 | 确认本地服务已启动，端口和地址配置正确 |
| UDP 穿透不可用 | UDP 通道建立失败不阻断启动，检查防火墙是否放行 UDP |
