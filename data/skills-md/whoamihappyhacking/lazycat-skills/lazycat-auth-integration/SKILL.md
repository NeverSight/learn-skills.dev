---
name: lazycat-auth-integration
description: 用于处理懒猫微服(Lazycat MicroServer)应用接入官方认证体系（OIDC单点登录）、HTTP Header用户身份识别、API Auth Token 以及配置独立鉴权(public_path)的专业指南。
---

# 懒猫微服认证体系接入指南

你是一个专业的懒猫微服认证与权限配置专家。当开发者需要让应用实现免密登录（接入 OIDC）、识别当前请求用户信息、或放行部分公共 API 时，请遵循本指南。

## 1. 接入 OIDC 单点登录 (SSO)
懒猫微服 (v1.3.5+) 提供了统一的 OIDC 支持，允许应用自动获取用户信息和权限组（`ADMIN` 或 `NORMAL`），实现免密登录。

**配置方法 (`lzc-manifest.yml`):**
1. 声明 OIDC 回调路径 (`application.oidc_redirect_path`)。系统只要检测到这个字段，就会在部署时自动注入相关的环境变量。
2. 将系统生成的 OIDC 环境变量传递给应用。

**示例:**
```yaml
application:
  subdomain: myapp
  oidc_redirect_path: /auth/oidc.callback # 必须填写！系统据此生成环境变量。请查阅应用的 OIDC 文档获取准确路径。
services:
  myapp:
    image: xxx
    environment:
      - OIDC_CLIENT_ID=${LAZYCAT_AUTH_OIDC_CLIENT_ID}
      - OIDC_CLIENT_SECRET=${LAZYCAT_AUTH_OIDC_CLIENT_SECRET}
      - OIDC_ISSUER_URI=${LAZYCAT_AUTH_OIDC_ISSUER_URI}
      - OIDC_AUTH_URI=${LAZYCAT_AUTH_OIDC_AUTH_URI}
      - OIDC_TOKEN_URI=${LAZYCAT_AUTH_OIDC_TOKEN_URI}
      - OIDC_USERINFO_URI=${LAZYCAT_AUTH_OIDC_USERINFO_URI}
```

## 2. HTTP Headers 身份识别 (自定义后端)
如果用户是在自己开发后端代码，`lzc-ingress` 会在所有经过认证的请求到达应用容器前，自动注入以下 HTTP Headers。开发者可直接信任这些 Header。

- `X-HC-User-ID`: 登录的用户名 (UID)
- `X-HC-User-Role`: 用户角色 (`NORMAL` 或 `ADMIN`)
- `X-HC-Device-ID`: 客户端在当前微服内的唯一设备 ID
- `X-HC-Login-Time`: 登录时间的 Unix 时间戳

**注意：** 应用后端可直接根据 `X-HC-User-ID` 认为该用户已登录，无需再次验证密码。

## 3. 独立鉴权与免登录访问 (`public_path`)
默认情况下，所有 HTTP 请求都必须经过懒猫微服的强制登录认证。如果应用有自己的鉴权机制（如 Token），或者这是一个公开页面（如分享链接），可以通过 `public_path` 放行。

**配置方法 (`lzc-manifest.yml`):**
```yaml
application:
  public_path:
    - /api/public/  # 放行 /api/public/ 开头的路径
    - /share/       # 放行 /share/ 开头的路径
```
**注意：** 放行的路径，系统依然会尝试获取登录状态。如果已登录，`X-HC-User-ID` 等 Header 依旧会存在；如果未登录，则清空相关 Header 但**不拦截请求**。

## 4. 脚本与自动化调用 (API Auth Token)
当需要编写脚本（如 Python, bash）调用微服系统 API 或应用接口时，不能依赖浏览器的 Cookie。懒猫 (v1.4.3+) 提供了 `API Auth Token` 机制。

**获取方式：** 只能通过 SSH 进入微服命令行生成。
```bash
hc api_auth_token gen --uid admin
```
**调用方式：** 在 HTTP 请求头中带上 `Lzc-Api-Auth-Token: <token>`。

## 平台兼容性说明
如果遇到更复杂的 OIDC 配置问题、Header 拦截问题，请主动读取本技能包 `references/` 目录下的相关 Markdown 文档（`oidc.md`, `http-request-headers.md`, `public-api.md`, `api-auth-token.md`）。