---
name: vite-starter
description: 使用 Vite 创建现代前端项目，支持 React、Vue、Svelte、Solid、Preact、Lit、Qwik 和 Vanilla JS，可选 TypeScript。当用户需要初始化新的前端项目、搭建 SPA、创建组件库、设置现代构建工具时使用此技能。触发场景：用户说"创建 vite 项目"、"新建 react/vue/svelte 应用"、"初始化前端项目"、"搭建 spa"、"用 vite 起一个项目"、"create vite project"、"new frontend app"，或明确提及 Vite、HMR、快速构建工具时。
license: MIT
metadata:
  category: frontend
  tags: vite, react, vue, svelte, typescript, frontend
---

# Vite 前端项目脚手架

使用 create-vite 快速创建现代前端项目，支持官方模板和社区模板，自动处理 TypeScript 配置验证。

## 工作流程

### 第 1 步：收集用户偏好

**必须询问以下信息（如果用户未提供）：**

| 偏好项 | 选项 | 说明 |
|--------|------|------|
| **框架** | React、Vue、Svelte、Solid、Preact、Lit、Qwik、Vanilla | 核心框架选择 |
| **语言** | TypeScript（推荐）、JavaScript | 是否启用 TypeScript |
| **包管理器** | pnpm（推荐）、npm、yarn、bun | 依赖管理工具 |
| **项目名称** | 字符串 | 目录名，可用 `.` 表示当前目录 |
| **构建器** | React 专属：Babel（默认）或 SWC（大型项目推荐） | 仅 React 项目需要选择 |

**偏好收集原则：**
- 如果用户已在请求中明确了某些偏好，无需重复询问
- 对于缺失的关键偏好，一次性列出所有问题，避免多轮对话
- 如果用户没有特殊要求，可直接提议推荐组合并请求确认

**推荐组合：**
```
React + TypeScript + pnpm + SWC → react-swc-ts 模板（性能最佳）
Vue + TypeScript + pnpm         → vue-ts 模板
Svelte + TypeScript + pnpm      → svelte-ts 模板
```

---

### 第 2 步：保存偏好到 assets 目录

将用户偏好保存为 JSON 文件，便于下次复用。

**存储位置：** `./assets/` 目录（相对于技能目录）

**文件命名规则：** `{描述性名称}.json`，例如 `react-ts-pnpm.json`

**文件格式：**
```json
{
  "name": "react-ts-pnpm",
  "description": "React + TypeScript + pnpm + SWC",
  "framework": "react",
  "language": "typescript",
  "packageManager": "pnpm",
  "template": "react-swc-ts",
  "createdAt": "2024-01-01"
}
```

**下次使用时：** 列出 `./assets/` 中已有的偏好文件，让用户选择直接复用或创建新的。

---

### 第 3 步：选择并执行安装命令

#### 官方模板（推荐，快速稳定）

**所有官方模板 ID：**

| 模板 ID | 框架 | 语言 | 备注 |
|---------|------|------|------|
| `vanilla` | Vanilla JS | JavaScript | |
| `vanilla-ts` | Vanilla JS | TypeScript | |
| `vue` | Vue 3 | JavaScript | |
| `vue-ts` | Vue 3 | TypeScript | |
| `react` | React | JavaScript | Babel |
| `react-ts` | React | TypeScript | Babel |
| `react-swc` | React | JavaScript | SWC（更快） |
| `react-swc-ts` | React | TypeScript | SWC（更快，推荐） |
| `react-compiler` | React | JavaScript | React Compiler（实验性） |
| `react-compiler-ts` | React | TypeScript | React Compiler（实验性） |
| `preact` | Preact | JavaScript | |
| `preact-ts` | Preact | TypeScript | |
| `lit` | Lit | JavaScript | Web Components |
| `lit-ts` | Lit | TypeScript | Web Components |
| `svelte` | Svelte | JavaScript | |
| `svelte-ts` | Svelte | TypeScript | |
| `solid` | Solid | JavaScript | |
| `solid-ts` | Solid | TypeScript | |
| `qwik` | Qwik | JavaScript | Resumability |
| `qwik-ts` | Qwik | TypeScript | Resumability |

**各包管理器命令：**

```bash
# pnpm（推荐）
pnpm create vite <项目名称> --template <模板ID>

# npm（注意：npm 7+ 需要 -- 分隔符）
npm create vite@latest <项目名称> -- --template <模板ID>

# yarn
yarn create vite <项目名称> --template <模板ID>

# bun
bun create vite <项目名称> --template <模板ID>
```

**在当前目录创建（使用 `.`）：**
```bash
pnpm create vite . --template react-swc-ts
```

**非交互式（CI/CD 或脚本环境）：**
```bash
pnpm create vite my-app --template react-swc-ts --no-interactive
```

#### 社区模板（功能更完整）

参考 [Awesome Vite 社区模板](https://github.com/vitejs/awesome-vite#templates) 获取完整列表。

使用 `tiged`（`degit` 的维护版本）克隆社区模板：
```bash
# 安装 tiged
npx tiged <用户名/仓库名> <项目名称>
cd <项目名称>
pnpm install
```

**热门社区模板：**
- [Vitesse](https://github.com/antfu/vitesse) — Vue 3 全功能模板（UnoCSS + i18n + 文件路由）
- [Vitamin](https://github.com/wtchnm/Vitamin) — React + TypeScript + Tailwind CSS + PWA
- [create-electron-vite](https://github.com/electron-vite/create-electron-vite) — Electron 桌面应用

---

### 第 4 步：安装依赖

```bash
cd <项目名称>   # 如果不是在当前目录创建
pnpm install    # 或对应包管理器的安装命令
```

---

### 第 5 步：TypeScript 编译验证（仅 TS 项目）

如果选择了 TypeScript 模板，**必须验证编译通过**：

```bash
# 执行类型检查（不生成文件）
pnpm exec tsc --noEmit

# 或运行构建验证
pnpm build
```

**预期输出：** 无错误输出，命令以退出码 0 完成。

如果出现类型错误，根据错误信息修复后再次验证，确认干净通过后再向用户报告完成。

---

### 第 6 步：向用户报告

报告内容包括：
1. 项目创建路径
2. 使用的模板和包管理器
3. TypeScript 编译验证结果（如适用）
4. 启动开发服务器的命令

```bash
# 启动开发服务器
pnpm dev
```

---

## 注意事项

- **SWC vs Babel**：对于 React 项目，SWC（`react-swc-ts`）比 Babel 快 20x+，推荐用于所有新项目
- **npm 7+ 特殊语法**：npm 传递参数给 create-vite 必须加 `--` 分隔符：`npm create vite@latest my-app -- --template react-ts`
- **在线预览**：可通过 `https://vite.new/{模板ID}` 在浏览器中快速预览任意官方模板（如 `https://vite.new/react-swc-ts`）

## 参考资源

- [Vite 官方文档](https://vitejs.dev/guide/)
- [create-vite 模板列表](https://github.com/vitejs/vite/tree/main/packages/create-vite)
- [Awesome Vite 社区模板](https://github.com/vitejs/awesome-vite#templates)
