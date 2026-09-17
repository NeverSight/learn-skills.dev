---
name: doudou-dev
description: 跨平台（Windows、macOS、Linux）管理 doudou-ai-coding 开发与构建流程。包含两大核心模式：(1) 开发调试模式（通过“调试/开发/启动/运行/本地跑起来/dev”等触发），启动 doudou-eggjs (npm run dev) 与 doudou-vue3 (pnpm dev)，提供端口与环境探测、依赖自动安装、并发日志与优雅退出；(2) 生产打包模式（通过“打包/构建/编译产物/生产打包/build/build:prod”等触发），执行 doudou-eggjs (npm run build，即 rec build -o dist) 与 doudou-vue3 (pnpm run build:prod，即 vite build) 生成发布产物。
compatibility: 跨平台兼容 Windows (PowerShell/CMD)、macOS (Zsh/Bash)、Linux (Bash)；需要 Node.js >= 20.0.0，前端强制要求 pnpm，后端调试需要 Redis 与数据库服务。
---

# 豆豆开发与构建技能 (doudou-dev)

本技能用于跨平台（Windows、macOS、Linux）管理 `doudou-ai-coding` 项目中的后端（`doudou-eggjs`）与管理端前端（`doudou-vue3`）的**开发调试**与**生产打包**。

---

## 模式分派与触发关键词

根据用户意图自动识别走 **开发调试** 或 **生产打包** 链路：

| 操作模式 | 触发关键词示例 | 后端执行命令 (`doudou-eggjs`) | 前端执行命令 (`doudou-vue3`) | 产物 / 监听端口 |
| :--- | :--- | :--- | :--- | :--- |
| 🚀 **开发调试模式** | “调试”、“启动”、“运行”、“开发环境”、“本地跑起来”、“dev”、“run” | `npm run dev`<br>*(执行 `npm-run-all -p mapper debug`)* | `pnpm dev`<br>*(执行 `vite`)* | 后端: `http://localhost:7001`<br>前端: `http://localhost:8001` |
| 📦 **生产打包模式** | “打包”、“构建”、“编译”、“发布产物”、“生产包”、“build”、“dist” | `npm run build`<br>*(执行 `rec build -o dist`)* | `pnpm run build:prod`<br>*(执行 `vite build`)* | 后端: `doudou-eggjs/dist/`<br>前端: `doudou-vue3/doudou-vue/` |

---

## 方式一：跨平台一键脚本（推荐）

技能内置了纯 Node.js ESM 脚本（兼容 Windows、macOS、Linux，免装额外全局依赖），自动处理环境检查、缺失依赖安装与子进程管理。

### 1. 开发调试 (Dev / Debug)

```bash
# 一键并行启动前后端开发调试服务（默认）
node skills/doudou-dev/scripts/dev.mjs

# 仅启动后端调试服务 (doudou-eggjs, npm run dev)
node skills/doudou-dev/scripts/dev.mjs --backend

# 仅启动前端开发服务 (doudou-vue3, pnpm dev)
node skills/doudou-dev/scripts/dev.mjs --frontend

# 启动前环境自检与端口探测
node skills/doudou-dev/scripts/check.mjs
```
> 特性：支持彩色日志标签（`[EggJS]` 青色、`[Vue3]` 绿色），按 `Ctrl+C` 跨平台安全清理所有子进程。

---

### 2. 生产打包 (Build)

```bash
# 一键打包前后端生产产物
node skills/doudou-dev/scripts/build.mjs

# 仅打包后端生产包 (doudou-eggjs: npm run build -> dist/)
node skills/doudou-dev/scripts/build.mjs --backend

# 仅打包前端生产包 (doudou-vue3: pnpm run build:prod -> doudou-vue/)
node skills/doudou-dev/scripts/build.mjs --frontend
```
> 特性：自动检测缺失依赖、统计各端打包耗时与产物目录大小。

---

## 方式二：各平台原生终端命令速查

### 1. Windows (PowerShell / Windows Terminal)

#### 🚀 启动调试
```powershell
# 窗口 1: 启动后端调试
cd doudou-eggjs
npm install
npm run dev

# 窗口 2: 启动前端开发
cd doudou-vue3
pnpm install
pnpm dev
```

#### 📦 生产打包
```powershell
# 打包后端
cd doudou-eggjs
npm run build

# 打包前端
cd doudou-vue3
pnpm run build:prod
```

---

### 2. Windows (CMD)

#### 🚀 启动调试
```cmd
:: 后端
cd doudou-eggjs && npm run dev

:: 前端
cd doudou-vue3 && pnpm dev
```

#### 📦 生产打包
```cmd
:: 后端
cd doudou-eggjs && npm run build

:: 前端
cd doudou-vue3 && pnpm run build:prod
```

---

### 3. macOS / Linux (Bash / Zsh)

#### 🚀 启动调试
```bash
# 后端
cd doudou-eggjs && npm install && npm run dev

# 前端
cd doudou-vue3 && pnpm install && pnpm dev
```

#### 📦 生产打包
```bash
# 后端打包
cd doudou-eggjs && npm run build

# 前端打包
cd doudou-vue3 && pnpm run build:prod
```

---

## 前置环境与依赖要求

| 依赖项 | 调试模式要求 | 打包模式要求 | 说明 |
| :--- | :--- | :--- | :--- |
| **Node.js** | `>= 20.0.0` (推荐 20 或 22 LTS) | `>= 20.0.0` | 跨端统一要求 |
| **npm** | 已安装 | 已安装 | 用于后端依赖安装与脚本执行 |
| **pnpm** | 已安装 | 已安装 | 前端 `doudou-vue3` **强制要求 pnpm**（`only-allow pnpm`） |
| **Redis** | 运行中 (默认 6379) | 可选 | 调试模式下 Egg.js 会连接 Redis 预热缓存与队列 |
| **数据库** | 已配置 (SQLite/MySQL/PgSQL) | 可选 | 数据库配置位于 `config.local.js` |

---

## 打包产物与部署说明

1. **后端产物 (`doudou-eggjs/dist`)**：
   - 由 `rec build -o dist` 打包生成；
   - 包含编译混淆后的服务端运行时文件，可直接用于 Node.js 生产部署。
2. **前端产物 (`doudou-vue3/doudou-vue`)**：
   - 由 `vite build` 生产构建；
   - 包含 HTML、CSS、JS 及 Gzip 压缩文件，可直接托管至 Nginx 或静态托管服务（生产 Base 路径可在 `.env.production` 中调整）。

---

## 常用端口与故障排查 (FAQ)

| 服务 | 端口 | 说明 |
| :--- | :--- | :--- |
| **Egg.js API** | `7001` | 后端 HTTP 接口服务 |
| **Vite Dev Server** | `8001` | 前端开发页面，开发模式自动代理 `/api` 至 7001 |
| **Egg 调试端口** | `9229` ~ `9239` | `start-debug.js` 自动寻找可用端口 |
| **Inspector Proxy** | `9999` ~ `10009` | Egg 调试代理端口 |
| **Redis** | `6379` | 缓存与 Bull 队列 |

### 常见问题

1. **前端报错 `Use 'pnpm install' for installation in this project`**：
   - 前端配置了强制包管理器，请严格使用 `pnpm install` / `pnpm dev` / `pnpm run build:prod`。
2. **后端调试启动报 `Redis connection failed`**：
   - 本地未启动 Redis 服务，请先启动 Redis（端口 6379）。
3. **端口冲突 `EADDRINUSE: 7001`**：
   - Windows: `netstat -ano | findstr :7001` 然后 `taskkill /PID <PID> /F`；
   - macOS/Linux: `lsof -i :7001` 然后 `kill -9 <PID>`。
4. **Mapper 编译报错 `rec: command not found` 或生成失败**：
   - 请在 `doudou-eggjs` 目录下执行 `npm install` 确保 `doudou-eggjs-cli` 正确安装。
