---
name: lazycat-advanced-routing
description: 处理懒猫微服(Lazycat MicroServer)应用的高级路由、多域名配置、TCP/UDP四层转发(ingress)、跨域处理以及使用 app-proxy 进行复杂代理规则配置的专业指南。
---

# 懒猫微服高级路由与网络配置指南

你是一个专业的懒猫微服网络配置专家。当用户在移植或开发应用时，遇到复杂的网络转发需求（如多域名、四层转发、去除 URL 前缀、自定义 Nginx 代理等）时，请严格遵循本指南。

## 核心路由机制 (Core Routing Mechanisms)

懒猫微服提供了三种层级的路由控制能力，请根据用户的需求选择最合适的方案：

### 1. 基础 HTTP/HTTPS 路由 (`application.routes`)
适用于绝大多数标准的 HTTP 代理场景。
**规则格式:** `URL_PATH=UPSTREAM`
**特点:** 默认会**去掉** `URL_PATH` 前缀。例如 `- /api/=http://backend:80`，访问 `/api/v1` 时，后端实际收到的是 `/v1`。

支持三种上游协议：
- `http(s)://$hostname/$path` (最常用，转发给容器。域名格式需为 `$service_name.$appid.lzcapp`)
- `file:///$dir_path` (直接托管静态文件)
- `exec://$port,$exec_file_path` (启动一个可执行文件并代理到本地端口)

### 2. 高级 HTTP 路由 (`application.upstreams`) (v1.3.8+)
适用于需要对 HTTP 请求进行精细控制的场景。
**能力包括:**
- **基于域名的分流:** 使用 `domain_prefix`。
- **保留 URL 前缀:** 设置 `disable_trim_location: true`。
- **解决 Host 校验报错:** 设置 `use_backend_host: true`。
- **跳过 SSL 验证:** 设置 `disable_backend_ssl_verify: true`。
- **清除特定 Header (解决跨域等):** 使用 `remove_this_request_headers: [Origin, Referer]`。

**示例:**
```yaml
upstreams:
  - location: /api
    backend: http://backend.cloud.lazycat.app.demo.lzcapp:80
    disable_trim_location: true # 保留 /api 前缀
```

### 3. TCP/UDP 四层转发 (`application.ingress`)
**绝对不要使用 routes 处理非 HTTP 流量！** 如果用户需要暴露 SSH、数据库、游戏私服等非 HTTP 端口，必须使用 `ingress`。
**警告:** 
- `ingress` 仅提供底层网络转发，**没有鉴权保护**，开发者需自行在应用内处理安全问题。
- 除非极特殊情况，**严禁**主动接管 80 和 443 端口。

**示例:**
```yaml
application:
  ingress:
    - protocol: tcp
      port: 3306
      service: mysql # 转发到 mysql 容器的 3306 端口
    - protocol: udp
      publish_port: 20000-30000 # 动态端口范围转发
      service: app
```

## 复杂反向代理最佳实践 (APP Proxy)

如果 `routes` 和 `upstreams` 仍然无法满足需求（比如需要极度复杂的 URL 重写、多域名分别指向不同后端，或者需要在微服中查看详细的请求日志），请使用官方提供的 `app-proxy` 镜像。

**镜像地址:** `registry.lazycat.cloud/app-proxy:v0.1.0` (本质是一个 OpenResty)

**使用方式：通过 `setup_script` 覆盖 Nginx 配置**
这是处理多域名 (配合 `application.secondary_domains`) 最强大的方式。

```yaml
application:
  subdomain: myapp
  secondary_domains:
    - myadmin
  routes:
    - /=http://app-proxy.cloud.lazycat.app.myapp.lzcapp:80
services:
  app-proxy:
    image: registry.lazycat.cloud/app-proxy:v0.1.0
    setup_script: |
      cat <<'EOF' > /etc/nginx/conf.d/default.conf
      server {
         server_name myapp.*; # 匹配默认域名
         location / { proxy_pass http://frontend:3000; }
      }
      server {
         server_name myadmin.*; # 匹配附加域名
         location / { proxy_pass http://backend:8080; }
      }
      EOF
```

## 平台兼容性说明
如果需要查看 `routes`, `upstreams`, `ingress` 的完整规范，或需要查看 APP Proxy 的更详细用法，请主动读取本技能包 `references/` 目录下的相关 Markdown 文档。