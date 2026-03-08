---
name: lazycat-dynamic-deploy
description: 处理懒猫微服(Lazycat MicroServer)应用的动态部署参数配置(lzc-deploy-params.yml)、清单文件 Go 模板渲染以及利用 application.injects 实现前端页面脚本注入的专业指南。
---

# 懒猫微服动态部署与注入指南

你是一个专业的懒猫微服应用架构师。当开发者需要向用户索要自定义配置（如密码、远程 IP 等），或者需要在不修改原应用代码的情况下，强行向应用的前端页面注入 JavaScript 脚本时，请遵循本指南。

## 1. 动态部署参数与模板渲染 (v1.3.8+)
懒猫微服支持在安装应用前，弹出一个 UI 界面让用户填写参数，然后利用这些参数动态渲染 `lzc-manifest.yml`。

### 步骤 A: 编写 `lzc-deploy-params.yml`
在项目根目录创建此文件，定义需要用户填写的字段。
```yaml
params:
  - id: target_ip
    type: string
    name: "目标服务器 IP"
    description: "你要代理的内网服务器 IP"
  - id: enable_debug
    type: bool
    name: "开启 Debug"
    default_value: "false"
    optional: true
```
*类型支持:* `string`, `bool`, `secret`, `lzc_uid`

### 步骤 B: 在 `lzc-manifest.yml` 中使用模板渲染
使用 Go 模板语法 (`{{ ... }}`) 读取参数。
- 用户参数使用 `.U.参数ID` (例如: `{{ .U.target_ip }}`)。如果 ID 包含 `.`，需使用 `index` (如 `{{ index .U "my.param" }}`)。
- 系统参数使用 `.S` (例如: `.S.BoxDomain`, `.S.IsMultiInstance`)。
- 随机密码生成函数: `{{ stable_secret "admin_password" | substr 0 8 }}` (同一个微服，相同的 seed 永远生成相同的字符串)。

**示例:**
```yaml
services:
  myapp:
    image: xxx
    environment:
      - REMOTE_IP={{ .U.target_ip }}
      - DB_PASS={{ stable_secret "db_root_pass" }}
```

## 2. 网页脚本注入 (`application.injects`) (v1.5.0+)
适用于在不修改第三方 Docker 镜像前端代码的情况下，向特定网页强行注入 JS 脚本（比如用来自动填充难以修改的默认密码）。

**核心逻辑：** 只有满足 `include`（白名单）且不命中 `exclude`（黑名单）的 HTML 页面才会被注入。

**示例：实现第三方系统的自动登录**
```yaml
application:
  injects:
    - id: auto-login
      mode: exact # 支持 exact(精确) 或 prefix(前缀)
      include:
        - "/login"      # 当访问 /login 时注入
        - "/#signin"    # 也能匹配 hash 路由
      scripts:
        # 使用懒猫内置的表单填充脚本
        - src: builtin://simple-inject-password
          params:
            user: "admin"
            password: "{{ stable_secret "app_admin_pass" }}"
            autoSubmit: true
```

**自定义注入脚本:**
如果你想注入自己写的脚本，可以将 JS 文件放在打包目录中，通过 `file:///lzcapp/pkg/content/myscript.js` 引用。在脚本内部，可以通过 `__LZC_INJECT_PARAMS__` 获取传入的 `params` 参数。

## 平台兼容性说明
如果需要查看详细的内置模板函数列表、系统参数列表（`SysParams`）或了解脚本注入的 `builtin://simple-inject-password` 的详细参数配置（如修改选择器），请主动读取本技能包 `references/` 目录下的相关 Markdown 文档。