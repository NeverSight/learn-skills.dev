---
name: yss-create-microapp
description: 离线脱机环境或网络受限时创建微应用的内置脚本后备，使用本地模板与离线脚本初始化微前端子应用工程；当无法访问外网、无 npm 连通性、网络受限或需直接执行本地脚本搭建子工程时使用。在线正常网络环境首选 create-yss-app，已有工程开发业务页面请使用 yss-frontend-dev。
---

# 创建本地微应用（离线后备）

> [!NOTE]
> 本 Skill 是微应用工程搭建的**离线底层后备**（内置脚本、离线可用）。
> 在线网络环境下，请**优先使用 `../create-yss-app/SKILL.md`**（基于官方 CLI 交互与预检生成）。仅在网络受限、无 npm 访问权限或离线调用时使用本工具。

## 触发条件

- 处于离线网络、局域网或无法直接访问 npm 仓库的环境。
- 用户明确要求使用内置脚本 `scripts/create.mjs` 初始化本地项目。
- 需要配置 qiankun 激活路由、Vite 端口、API Base 和本地代理。

## 不适用场景

- 在已有微应用中新建业务页面：使用 `../yss-ui-business-page-generation/SKILL.md`。
- 只创建单个 Vue 组件或只修改配置。
- 用户要求创建 GitLab 远程仓库、推送代码或触发 CI/CD；本 skill 与 CLI 只生成本地骨架，部署与远端请配合雨燕平台。

## 硬约束（禁止/必须）

- 必须收集并验证：应用英文名 `appName`、中文名 `appNameZh`、激活路由 `activeRule` 和最终目标父目录。
- `appName` 必须以小写字母开头，仅包含小写字母、数字和中划线，且不能以中划线结尾（例如 `order-center`、`crm`）。
- `activeRule` 统一对齐雨燕规范：必须是以 `/` 开头的单段路径，推荐小驼峰命名（如 `/orderCenter`），短横线兼容（如 `/order-center`）；默认由 `appName` 自动推导为小驼峰。
- 必须向用户展示最终绝对路径 `<targetDir>/<appName>`；目标已存在时必须停止，退出码 3，禁止覆盖。
- 优先推荐调用 CLI 方式：`npx @yss-ui/create --yes --json`；在完全离线或无 npm 环境下回退使用内置脚本 `node .agents/skills/yss-create-microapp/scripts/create.mjs`。
- 真正拉取模板前必须先使用相同参数追加 `--dry-run`，确认参数、缓存边界和最终路径。
- 模板缓存必须位于系统临时目录且名称以 `yss-frontend-template` 开头；脚本不得对任意用户目录执行 `reset --hard` 或 `clean -fd`。
- 默认模板为 GitHub 公开仓库 `https://github.com/iamyancong/microapp-template-vue3.git`（分支 `main`），无需凭据；非交互模式不会询问 git 凭据。用户指定内部模板仓库时，需确保本机已有对应 Git 凭据与访问权限，否则 dry-run 后真实拉取会失败；用户需要其他模板时用 `--template-url` 或环境变量 `YSS_FRONTEND_TEMPLATE_URL` 覆盖，不得自行猜测替代地址。
- 可选参数默认值：`port` 默认从 8081 起向上探测首个空闲端口；`activeRule` 默认由 `appName` 推导小驼峰（驼峰不合法时退回短横线，如 `app-1 → /app-1`、`crm2 → /crm-2`）；`apiBase` 默认为 `/api${activeRule}`；`proxyTarget` 优先级为 `--proxy-target` > `YSS_PROXY_TARGET` 环境变量 > 常量预设。
- CLI 的 `--json` 输出中 stdout 只有一行 JSON，日志在 stderr；解析结果时只读 stdout。拼错的参数（如 `--dryrun`）会直接退出码 2，不要靠猜测重试。
- 生成后默认会自动将 `@yss-ui/*` 依赖对齐至 registry 最新版本并处理 `pnpm-lock.yaml` 锁定；如需严格保留模板原写死版本可传入 `--no-sync-deps`。
- 生成后会自动同步最新官方 AI Skills（`npx -y @yss-ui/skills-cli@latest sync`），无需询问用户；同步失败只告警，不要因此重试创建。仅在无法联网时传 `--no-skills` 跳过。
- 没有用户明确授权时，不得擅自执行安装依赖、初始化 git、启动服务、创建远程仓库或推送代码。

## 标准代码骨架

### 推荐调用方式（CLI 优先）

```bash
npx @yss-ui/create "<appName>" \
  --name-zh "<appNameZh>" \
  --target-dir "<targetDir>" \
  --yes \
  --json
```

- 需指定非默认路由或端口时：追加 `--active-rule "</customRoute>"` 或 `--port <port>`。
- 需传递接口前缀或代理目标时：追加 `--api-base "</api/path>"` 或 `--proxy-target "<http://url>"`。
- 预检模式：追加 `--dry-run`。

### 离线后备脚本调用方式

当无法访问 npm 或需直接执行源码时，使用内置包装脚本：

```bash
node .agents/skills/yss-create-microapp/scripts/create.mjs \
  --name "<appName>" \
  --name-zh "<appNameZh>" \
  --target-dir "<targetDir>"
```

## 交付检查清单

- [ ] 必填参数、默认值推导与最终绝对路径已向用户确认。
- [ ] 目标项目原先不存在，未覆盖用户文件。
- [ ] 模板缓存路径通过安全校验，已有缓存的 remote 与请求模板一致。
- [ ] 脚手架进程退出码为 0，生成目录与 `package.json` / `micro-config.json` 存在。
- [ ] 中文名、描述、激活路由（符合驼峰规范）、端口、API Base 和代理配置正确。
- [ ] 未擅自执行安装、启动、推送或 CI 操作。

## 失败兜底策略

- 本地脚本缺失时：若执行 `scripts/create.mjs` 前发现对应文件在项目或全局不存在，必须提示用户运行 `npx -y @yss-ui/skills-cli sync` 安装官方 Skills（或使用 `npx @yss-ui/create`），并立即终止；**严禁自行编写临时替代脚本**。
- 参数不完整或不合法时，输出明确中文原因及示例（退出码 2），不带错误默认值继续。
- 目标目录已存在时立即中止（退出码 3），提示更换目录或应用名。
- 模板缓存不是期望的 Git 仓库或 remote 不一致时，报告冲突并换用新的安全缓存路径，不清理原目录。
- 模板拉取或脚手架失败时，保留完整错误和已生成路径，不在不明状态下反复覆盖重试。
- 模板拉取失败（退出码 5）时，把报错中的诊断原样转告用户：检查能否访问 GitHub，或由用户提供 `--template-url`；若使用内部模板仓库，确保本机已配置对应 Git 访问权限（凭据）。
