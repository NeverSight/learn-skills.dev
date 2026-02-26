---
name: refine-dev
description: 协助开发基于 Refine 框架的 React 应用。提供项目初始化、核心配置、数据提供者（Data Providers）、认证（Auth Provider）以及 UI 库集成的指导。专注于使用 shadcn/ui 构建现代化的后台管理系统。
---

# Refine Dev Skill

Refine 是一个基于 React 的框架，用于快速构建数据密集型应用。它通过解耦业务逻辑与 UI 层，提供了极高的开发效率。

## 何时使用此技能
- **构建后台管理系统**: 当你需要快速搭建功能完善的 Admin 面板或仪表盘时。
- **数据密集型应用**: 应用涉及大量的表格、表单、CRUD 操作以及复杂的数据流管理。

## 初始化项目 (开始之前)

在执行任何初始化命令之前，你**必须**先询问并收集用户的偏好。不要假设默认值，请确认以下参数：

1. **项目名称与元数据**:
   - 项目名称 (Project Name)
   - 作者名称 (`--init-author-name`)
   - 作者 URL (`--init-author-url`)
   - 许可证 (`--init-license`, 例如 MIT)
   - 是否为私有项目 (`--init-private`)

2. **前端框架选择**:
   - **Vite** (推荐，极致的开发体验)
   - **Next.js** (适合需要 SSR 或更复杂路由的项目)

3. **Refine 架构配置**:
   - **Data Provider**: (例如 Simple REST, Supabase, Appwrite 等)
   - **Auth Provider**: 是否需要集成身份验证。

## 快速开始

根据用户在初始化阶段提供的偏好，运行对应的初始化命令。

### 使用预设初始化 (推荐)
```bash
# 示例：使用 Vite + shadcn/ui 预设
npm create refine-app@latest [项目名] -- --preset vite-shadcn
```

## 核心工作流

### 1. 配置 Refine 组件
在 `App.tsx` (或 Next.js 的布局文件) 中配置组件：
```tsx
import { Refine } from "@refinedev/core";

function App() {
  return (
    <Refine
      dataProvider={dataProvider}
      authProvider={authProvider}
      resources={[
        {
          name: "posts",
          list: "/posts",
          create: "/posts/create",
          edit: "/posts/edit/:id",
          show: "/posts/show/:id",
        },
      ]}
    >
      {/* 页面组件 */}
    </Refine>
  );
}
```

### 2. 查阅详细文档
- **数据提供者**: [data-provider.md](references/data-provider.md)
- **认证提供者**: [auth-provider.md](references/auth-provider.md)
