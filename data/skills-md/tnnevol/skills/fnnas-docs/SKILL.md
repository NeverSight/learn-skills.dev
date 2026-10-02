---
name: fnnas-docs
displayName: fnnas-docs
slug: fnnas-docs
description: 飞牛 fnOS 应用开发文档 - 快速开始、开发指南、开放 API、CLI 工具参考、应用案例和更新日志。当用户询问飞牛应用开发、开放 API、JS SDK、文件授权、Manifest 配置、应用权限或 Docker 构建等问题时使用此技能。
metadata:
  author: Tnnevol
  version: "1.1.2"
---

# SKILL: fnnas-docs (飞牛应用开发文档)

飞牛 fnOS 应用开发完整文档索引。基于飞牛应用开放平台的 [文档索引](https://developer.fnnas.com/llms.txt) 和 [完整文档](https://developer.fnnas.com/llms-full.txt) 整理。

## Quick Start

```bash
# 文档来源
https://developer.fnnas.com/llms.txt
https://developer.fnnas.com/llms-full.txt

# 技能目录
skills/fnnas-docs/

# 更新文档（如需同步最新内容）
 cd skills/fnnas-docs && python3 scripts/fetch-docs.py
```

## 使用场景

- 用户询问飞牛应用开发相关问题
- 需要查阅 fnOS 开发文档
- 了解应用打包、上架流程
- 配置 Manifest、环境变量、应用权限
- 构建 Native/Docker 应用
- 了解文档更新记录

## 创建与生命周期约束

- **创建应用模板**：用户要求创建原生应用时，使用 `fnpack create <app-name>`，不要添加 `--template` 参数；用户要求创建 Docker 应用时，必须使用 `fnpack create <app-name> --template docker`。
- **保护模板结构**：创建应用后，不允许删除模板提供的文件或目录，只能在基础模板上修改内容，或新增必要的文件和目录。
- **安装回调阶段**：只有执行 `cmd/install_callback` 阶段时，飞牛框架提供的环境变量目录才会生成；该阶段也是应用正式安装阶段。涉及安装目录、框架环境变量或安装后初始化的逻辑，应放在此阶段处理。
- **`cmd/main` 进程检测**：`cmd/main` 是框架用于管理应用运行状态的守护进程入口。应用可以使用非守护进程方式启动，框架会周期性探测进程的 PID 状态，具体实现可参考基础框架示例。若应用自身内置守护进程，可以不使用模板提供的 PID 文件进行探测，改为检测应用提供的 `status` 结果或实际 PID。
- **生命周期日志**：生命周期脚本不要单独维护日志文件，优先直接输出标准输出和标准错误；飞牛框架提供安装流程日志收集工具，直接输出便于统一收集和排查。

## Core References

| 分类     | 文档数 | 说明                               | 入口                                        |
| -------- | ------ | ---------------------------------- | ------------------------------------------- |
| 概览     | 1 篇   | 平台介绍与学习路径                 | [guide.md](references/guide.md)             |
| 快速开始 | 4 篇   | 环境准备、创建/测试/上架应用       | [quick-started/](references/quick-started/) |
| 开发指南 | 13 篇  | 架构、Manifest、权限、入口、网关等 | [core-concepts/](references/core-concepts/) |
| 应用案例 | 2 篇   | Native/Docker 应用实战案例         | [examples/](references/examples/)           |
| CLI 工具 | 2 篇   | fnpack、appcenter-cli              | [cli/](references/cli/)                     |
| 开放 API | 11 篇  | JS SDK、文件授权、页面能力和后端 API | [api/](references/api/)                     |
| 更新日志 | 5 篇   | 文档站点和开放 API 更新记录         | [update-log.md](references/update-log.md)   |

## 文档索引

### 📖 概览

| 文档     | 说明               | 链接                            |
| -------- | ------------------ | ------------------------------- |
| 欢迎加入 | 平台介绍、学习路径 | [guide.md](references/guide.md) |

### 🚀 快速开始

| 文档     | 说明                       | 链接                                                                      |
| -------- | -------------------------- | ------------------------------------------------------------------------- |
| 准备工作 | 环境要求、系统要求、技术栈 | [prerequisites.md](references/quick-started/prerequisites.md)             |
| 创建应用 | 应用创建流程               | [create-application.md](references/quick-started/create-application.md)   |
| 测试应用 | 应用测试与调试             | [test-application.md](references/quick-started/test-application.md)       |
| 上架应用 | 应用发布上架流程           | [publish-application.md](references/quick-started/publish-application.md) |

### 📘 开发指南

| 文档       | 说明                         | 链接                                                                          |
| ---------- | ---------------------------- | ----------------------------------------------------------------------------- |
| 应用框架   | fnOS 应用架构                | [framework.md](references/core-concepts/framework.md)                         |
| Manifest   | 应用配置清单                 | [manifest.md](references/core-concepts/manifest.md)                           |
| 环境变量   | 应用环境变量配置             | [environment-variables.md](references/core-concepts/environment-variables.md) |
| 应用权限   | 权限声明与管理               | [privilege.md](references/core-concepts/privilege.md)                         |
| 应用资源   | 资源配置与使用               | [resource.md](references/core-concepts/resource.md)                           |
| 应用入口   | 应用入口配置                 | [app-entry.md](references/core-concepts/app-entry.md)                         |
| index.cgi  | CGI 轻量入口                 | [index-cgi.md](references/core-concepts/index-cgi.md)                         |
| 统一网关   | 网关注册与鉴权               | [gateway-registration.md](references/core-concepts/gateway-registration.md)   |
| 用户向导   | 安装/升级/卸载向导           | [wizard.md](references/core-concepts/wizard.md)                               |
| 应用依赖   | 依赖管理                     | [dependency.md](references/core-concepts/dependency.md)                       |
| 中间件服务 | Redis、MinIO、RabbitMQ 等    | [middleware.md](references/core-concepts/middleware.md)                       |
| 运行时环境 | Python、Node.js、Java 运行时 | [runtime.md](references/core-concepts/runtime.md)                             |
| 图标       | 应用图标规范                 | [icon.md](references/core-concepts/icon.md)                                   |

### 💡 应用案例

| 文档            | 说明                 | 链接                                       |
| --------------- | -------------------- | ------------------------------------------ |
| Native 应用案例 | 从零创建 Native 应用 | [native.md](references/examples/native.md) |
| Docker 应用案例 | 从零创建 Docker 应用 | [docker.md](references/examples/docker.md) |

### 🔧 CLI 开发工具

| 文档          | 说明               | 链接                                              |
| ------------- | ------------------ | ------------------------------------------------- |
| fnpack        | 应用打包工具       | [fnpack.md](references/cli/fnpack.md)             |
| appcenter-cli | 应用中心命令行工具 | [appcentercli.md](references/cli/appcentercli.md) |

### 🔌 开放 API

| 文档             | 说明                                  | 链接                                             |
| ---------------- | ------------------------------------- | ------------------------------------------------ |
| 概述             | 开放能力范围和阅读顺序                | [overview.md](references/api/overview.md)        |
| 调用方式         | API Scope、JS SDK、后端 API 通用规则  | [calling.md](references/api/calling.md)          |
| 授权与文件       | 文件授权能力总览                      | [authorization/overview.md](references/api/authorization/overview.md) |
| 应用共享授权路径 | 管理员授权固定目录                    | [shared-access.md](references/api/authorization/shared-access.md) |
| 用户个人授权路径 | 当前用户授权目录或文件                | [user-access.md](references/api/authorization/user-access.md) |
| 文件权限检查     | 检查用户对文件或目录的 ACL             | [file-acl.md](references/api/authorization/file-acl.md) |
| 路径转换         | 转换内部路径为语义化展示路径           | [path-convert.md](references/api/authorization/path-convert.md) |
| 页面路由         | 打开文件、文件管理器和应用设置         | [routing.md](references/api/page/routing.md)     |
| 页面交互         | 页面标题、主题、语言和离开提示         | [ui.md](references/api/page/ui.md)               |
| 错误码           | JS SDK 和后端 API 错误码               | [error-codes.md](references/api/error-codes.md)  |
| 平台配置         | 读取语言、主题、系统版本和格式配置     | [platform-config.md](references/api/platform-config.md) |

### 📝 更新日志

| 文档       | 说明                          | 链接                                             |
| ---------- | ----------------------------- | ------------------------------------------------ |
| 2026-07-31 | 新增开放 API 和 API 文档索引   | [update-log.md](references/update-log.md)       |
| 2026-07-05 | 新增 llms.txt、fnpack V1.2.3  | [20260705.md](references/update-log/20260705.md) |
| 2026-05-09 | 统一网关文档补充              | [20260509.md](references/update-log/20260509.md) |
| 2025-12-31 | 文档组织调整、platform 字段等 | [20251231.md](references/update-log/20251231.md) |
| 2025-12-16 | 文档结构优化、入门示例调整    | [20251216.md](references/update-log/20251216.md) |

## 意图识别规则

### 入门相关
- "飞牛怎么开发" / "如何开发飞牛应用" / "fnOS 开发" → [prerequisites.md](references/quick-started/prerequisites.md)
- "环境要求" / "系统要求" / "准备工作" / "开发环境" → [prerequisites.md](references/quick-started/prerequisites.md)
- "系统架构" / "内核版本" / "支持的架构" → [prerequisites.md](references/quick-started/prerequisites.md)
- "技术栈" / "支持什么语言" / "用什么开发" → [prerequisites.md](references/quick-started/prerequisites.md)
- "平台介绍" / "学习路径" / "为什么开发" → [guide.md](references/guide.md)

### 应用创建相关
- "创建应用" / "新建应用" / "怎么创建应用" → [create-application.md](references/quick-started/create-application.md)
- "应用开发流程" / "开发步骤" → [create-application.md](references/quick-started/create-application.md)

### 测试相关
- "测试应用" / "调试应用" / "怎么测试" → [test-application.md](references/quick-started/test-application.md)
- "本地测试" / "实机测试" → [test-application.md](references/quick-started/test-application.md)

### 上架相关
- "上架应用" / "发布应用" / "提交审核" / "应用商店" → [publish-application.md](references/quick-started/publish-application.md)
- "怎么发布" / "如何上架" → [publish-application.md](references/quick-started/publish-application.md)

### 架构与配置相关
- "应用架构" / "fnOS 架构" / "框架" → [framework.md](references/core-concepts/framework.md)
- "Manifest" / "应用配置" / "manifest.json" / "配置文件" → [manifest.md](references/core-concepts/manifest.md)
- "环境变量" / "env" / "配置变量" / "ENV" → [environment-variables.md](references/core-concepts/environment-variables.md)
- "权限" / "应用权限" / "权限声明" / "privilege" → [privilege.md](references/core-concepts/privilege.md)
- "资源" / "应用资源" / "资源配置" / "resource" → [resource.md](references/core-concepts/resource.md)
- "入口" / "应用入口" / "入口配置" / "entry" → [app-entry.md](references/core-concepts/app-entry.md)
- "CGI" / "index.cgi" / "轻量入口" → [index-cgi.md](references/core-concepts/index-cgi.md)
- "向导" / "用户向导" / "引导页" / "wizard" → [wizard.md](references/core-concepts/wizard.md)

### 进阶功能相关
- "网关" / "网关注册" / "统一网关" / "gateway" → [gateway-registration.md](references/core-concepts/gateway-registration.md)
- "登录" / "认证" / "单点登录" / "SSO" / "authentication" → [gateway-registration.md](references/core-concepts/gateway-registration.md)
- "依赖" / "应用依赖" / "依赖关系" / "dependency" → [dependency.md](references/core-concepts/dependency.md)
- "中间件" / "中间件服务" / "middleware" → [middleware.md](references/core-concepts/middleware.md)
- "运行时" / "运行环境" / "runtime" → [runtime.md](references/core-concepts/runtime.md)
- "图标" / "Icon" / "应用图标" / "logo" → [icon.md](references/core-concepts/icon.md)

### 应用案例相关
- "Native" / "原生应用" / "本地构建" / "原生构建" → [native.md](references/examples/native.md)
- "Docker" / "容器应用" / "Docker 构建" / "容器化" → [docker.md](references/examples/docker.md)
- "案例" / "实战" / "示例" → [native.md](references/examples/native.md) 或 [docker.md](references/examples/docker.md)

### CLI 工具相关
- "fnpack" / "打包" / "应用打包" / "打包工具" → [fnpack.md](references/cli/fnpack.md)
- "appcenter-cli" / "appcenter" / "命令行工具" / "CLI" → [appcentercli.md](references/cli/appcentercli.md)
- "install-local" / "本地安装" / "快速安装" → [appcentercli.md](references/cli/appcentercli.md)

### 开放 API 相关
- "开放 API" / "Open API" / "API 概述" / "应用中心 API" → [overview.md](references/api/overview.md)
- "调用方式" / "api-scope" / "JS SDK" / "后端 API" → [calling.md](references/api/calling.md)
- "文件授权" / "授权与文件" / "授权目录" → [authorization/overview.md](references/api/authorization/overview.md)
- "共享授权" / "管理员授权" / "固定目录" → [shared-access.md](references/api/authorization/shared-access.md)
- "个人授权" / "用户授权" / "pickUserFile" → [user-access.md](references/api/authorization/user-access.md)
- "文件权限" / "ACL" / "checkUserACL" → [file-acl.md](references/api/authorization/file-acl.md)
- "路径转换" / "convertPath" → [path-convert.md](references/api/authorization/path-convert.md)
- "打开文件" / "文件管理器" / "页面路由" → [routing.md](references/api/page/routing.md)
- "页面交互" / "主题" / "语言变化" → [ui.md](references/api/page/ui.md)
- "平台配置" / "系统版本" / "getPlatformConfig" → [platform-config.md](references/api/platform-config.md)
- "错误码" / "API 报错" → [error-codes.md](references/api/error-codes.md)

### 更新日志相关
- "文档更新" / "更新记录" / "changelog" / "最近更新" → [update-log/](references/update-log/)

## 技术栈

fnOS 基于 Linux (Debian) 内核，支持：
- **服务端**：Node.js、Python、Java、Go 等
- **前端**：HTML/JavaScript/CSS 及现代框架
- **架构**：x86_64 (AMD64) 及 ARM
- **系统版本要求**：fnOS 0.9.27 及以上

## CLI 工具速查

| 工具            | 用途                       | 安装                                                                                                                                                                                                                    |
| --------------- | -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `fnpack`        | 应用打包                   | 下载对应平台二进制文件：[fnpack-1.2.3-darwin-amd64](https://static2.fnnas.com/fnpack/fnpack-1.2.3-darwin-amd64) / [fnpack-1.2.3-darwin-arm64](https://static2.fnnas.com/fnpack/fnpack-1.2.3-darwin-arm64)，放到 PATH 中 |
| `appcenter-cli` | 应用管理（安装/卸载/日志） | fnOS 设备预装                                                                                                                                                                                                           |

## References

| 文件                                                   | 说明                               |
| ------------------------------------------------------ | ---------------------------------- |
| [references/guide.md](references/guide.md)             | 平台概览                           |
| [references/quick-started/](references/quick-started/) | 快速开始文档（4 篇）               |
| [references/core-concepts/](references/core-concepts/) | 开发指南文档（13 篇）              |
| [references/examples/](references/examples/)           | 应用案例文档（2 篇）               |
| [references/cli/](references/cli/)                     | CLI 工具文档（2 篇）               |
| [references/api/](references/api/)                     | 开放 API 文档（11 篇）             |
| [references/update-log.md](references/update-log.md)   | 文档和开放 API 更新日志             |
| [scripts/fetch-docs.py](scripts/fetch-docs.py)         | 文档同步脚本（基于 llms.txt 和 llms-full.txt） |
