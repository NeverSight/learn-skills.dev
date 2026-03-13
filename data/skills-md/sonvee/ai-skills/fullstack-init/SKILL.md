---
name: fullstack-init
description: 初始化前后端分离全栈项目的脚手架和配置，并在日常开发中遵守用户固定的技术栈选型。当用户提到"初始化项目"、"新建全栈项目"、"搭建前后端分离项目"、"创建一个新项目"、"帮我建个项目"等意图时，主动触发此 skill。即使用户没有明确说"全栈"，只要上下文涉及同时需要前端和后端的新项目，也应触发。日常讨论技术方案、写代码时也应遵守本 skill 中的技术栈约定。
---

# 全栈项目初始化 Skill

## 技术栈约定

- 这是用户固定的技术选型，在给建议、生成代码、初始化项目时，**始终遵循以下栈，不推荐替代方案**，除非用户主动提出更换
- 在运行本 Skill 的过程中，明确指定不使用 brainstorming 的 Skill，以防止干扰项目初始化的流程步骤

---

## 项目结构约定

- 前后端**分离开发**，但放在**同一个 Git 仓库**（Monorepo）
- 目录结构如下：

```
project-root/
├── frontend/          # Vue3 前端项目（含自己的 .env）
├── backend/           # NestJS 后端项目（含自己的 .env）
├── docs/              # 项目文档
│   ├── requirements/  # 项目需求文档
│   ├── design/        # 详细设计文档（接口设计、数据库设计等）
│   ├── ui-ux/         # UI/UX 设计文档、原型说明
│   └── misc/          # 其他文档
├── CONFIG.md          # 项目配置说明（给 AI 和开发者看，提交到 Git）
├── .gitignore
└── README.md
```

> 各子项目的环境变量由各自目录内的 `.env` 管理，根目录不创建 `.env`，避免混淆。

---

## 命名规范

- **所有文件名、目录名只使用英文字母、数字、连字符（-）或下划线（\_）**，严禁中文命名，防止编码问题
- 文件内容（注释、文档、README）推荐使用中文，方便理解

---

## 初始化流程

当用户要求初始化项目时，严格按照以下步骤执行：

### 第一步：确认基本信息

询问以下内容（用户已提供的跳过）：

1. 项目名称（用于根目录文件夹命名）
2. 前端目标平台（web / uniapp / 全都要），默认 web

### 第二步：创建根目录结构

```bash
mkdir <project-name>
cd <project-name>
mkdir frontend backend
mkdir -p docs/requirements docs/design docs/ui-ux docs/misc
```

### 第三步：初始化前端项目

严格遵守 `frontend-init` skill 中的步骤，进行前端项目初始化。

| Topic         | Description | Reference                                    |
| ------------- | ----------- | -------------------------------------------- |
| frontend-init | 初始化前端  | [frontend-init](references/frontend-init.md) |

**等用户确认前端初始化完成后，再继续后续步骤**

### 第四步：初始化后端项目

严格遵守 `backend-init` skill 中的步骤，进行后端项目初始化。

| Topic        | Description | Reference                                  |
| ------------ | ----------- | ------------------------------------------ |
| backend-init | 初始化后端  | [backend-init](references/backend-init.md) |

**等用户确认后端初始化完成后，再继续后续步骤**

### 第五步：生成根目录 CONFIG.md

根目录创建 `CONFIG.md`，用中文编写。它的作用是给 AI 和开发者快速了解项目的配置全貌，不涉及敏感值，内容如下：

```markdown
# 项目配置说明

## 技术栈

- 前端：Vue3 + Vite + Vue Router + Pinia + Element Plus + UnoCSS + Sass + Axios + VueUse + Lodash。（JavaScript）
- 后端：NestJS + Prisma。（TypeScript）
- 数据库：PostgreSQL
- 缓存：Redis（本地，无密码）
- 包管理：pnpm

## 环境变量说明

### 前端

`frontend/.env.development` 开发环境变量

| 变量名               | 说明                     | 示例                         |
| -------------------- | ------------------------ | ---------------------------- |
| VITE_APP_ENV         | 环境名                   | development                  |
| VITE_APP_BASE        | 基础路径                 | ./                           |
| VITE_APP_ROUTER_MODE | 路由模式：hash / history | hash                         |
| VITE_APP_PORT        | 服务端口                 | 3028                         |
| VITE_APP_API         | API 基础地址             | /api-dev                     |
| VITE_APP_API_PROXY   | API 跨域代理地址         | http://127.0.0.1:3068/api/v1 |

`frontend/.env.production` 生产环境变量

| 变量名               | 说明                                    | 示例       |
| -------------------- | --------------------------------------- | ---------- |
| VITE_APP_ENV         | 环境名                                  | production |
| VITE_APP_BASE        | 基础路径，如 /app/                      | /          |
| VITE_APP_ROUTER_MODE | 路由模式：hash / history                | history    |
| VITE_APP_PORT        | 服务端口                                | 80         |
| VITE_APP_API         | API 基础地址，需调整为生产环境 API 地址 | /api-prod  |

### 后端

`backend/.env.development` 开发环境变量

| 变量名         | 说明         | 示例        |
| -------------- | ------------ | ----------- |
| ENV_NAME       | 环境名       | development |
| NODE_PORT      | 服务端口     | 3068        |
| API_PREFIX     | API 前缀     | /api/v1     |
| DB_HOST        | 数据库地址   | 127.0.0.1   |
| DB_PORT        | 数据库端口   | 5432        |
| DB_USER        | 数据库用户名 | sove        |
| DB_PASSWORD    | 数据库密码   |             |
| DB_NAME        | 数据库名     | pg_demo     |
| REDIS_HOST     | Redis 地址   | 127.0.0.1   |
| REDIS_PORT     | Redis 端口   | 6379        |
| REDIS_PASSWORD | Redis 密码   |             |
| REDIS_DB       | Redis 库     | 0           |

`backend/.env.production` 生产环境变量

| 变量名         | 说明         | 示例          |
| -------------- | ------------ | ------------- |
| ENV_NAME       | 环境名       | production    |
| NODE_PORT      | 服务端口     | 3068          |
| API_PREFIX     | API 前缀     | /api/v1       |
| DB_HOST        | 数据库地址   | 101.34.89.199 |
| DB_PORT        | 数据库端口   | 5432          |
| DB_USER        | 数据库用户名 | sove          |
| DB_PASSWORD    | 数据库密码   |               |
| DB_NAME        | 数据库名     | pg_demo       |
| REDIS_HOST     | Redis 地址   | 127.0.0.1     |
| REDIS_PORT     | Redis 端口   | 6379          |
| REDIS_PASSWORD | Redis 密码   |               |
| REDIS_DB       | Redis 库     | 0             |
```

### 第六步：生成根目录 README.md

用中文编写，包含以下内容：

- 项目简介
- 技术栈说明
- 环境要求（Node.js 版本、pnpm）
- 快速开始：
  1. 参考 `CONFIG.md` 中的环境变量说明，在各子项目目录下创建 `.env` 并填写配置（或对 AI 说"初始化配置参数"自动生成）
  2. 前端启动命令
  3. 后端启动命令
- 目录结构说明

### 注意事项

全栈项目初始化完成后：

- 无需创建 Git 仓库，由用户自行创建并提交
- 提示用户需要在 CONFIG.md 中填写配置参数，用户配置完成后对 AI 说 "初始化配置参数"，AI 需要将参数同步到各子项目的 .env.\* 文件中

---

## 技术选型背景（理解用户，更好地给出帮助）

用户是 Vue3 前端工程师，NestJS 和 Prisma 是正在学习中的技术。因此：

- **前端写 JavaScript**，在组件、函数、props、重要逻辑处遵守 JSDoc 规范写好注释
- **后端写 TypeScript**，在模块、Service、Controller、配置项等关键位置写好 TSDoc 注释
- 注释目的是让用户随时能看懂自己的代码，不需要靠记忆回想逻辑
- 给出 NestJS / Prisma 相关代码时，适当加上中文注释，帮助理解
- 遇到 Prisma 或 NestJS 的用法问题，优先给出完整可运行的示例代码

---

## 日常开发中的技术栈遵守

即使不是在初始化新项目，只要用户在讨论技术方案、写代码、解决问题，也默认遵循上述技术栈。例如：

- 问"怎么做状态管理" → 推荐 Pinia，不推荐 Vuex
- 问"怎么连接数据库" → 用 Prisma ORM v7，不推荐 TypeORM
- 问"怎么做缓存" → 用 Redis（ioredis），不推荐其他方案
- 问"用什么包管理器" → pnpm
- 问"怎么发请求" → 用 axios，不用原生 fetch
- 需要操作 DOM、监听事件、处理响应式工具函数等 Hook 时 → 优先用 VueUse，不自己手写
- 需要数组/对象/字符串处理等工具函数方法时 → 优先用 Lodash，不重复造轮子

---

## 同步配置参数

当用户说"初始化配置参数"、"同步配置"、"把配置写入环境变量"等语句时，执行以下操作：

1. 读取项目根目录的 `CONFIG.md`，从表格中提取各参数的实际填写值
2. 将参数写入对应的 `.env.*` 文件
3. 写入完成后，告知用户哪些文件已更新
