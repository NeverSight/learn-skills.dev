---
name: react-frontend-standards
description: React + TypeScript 前端编码规范:技术栈(共享组件库 @workspace/ui、Sonner、Tailwind CSS、Jotai、React Query/jotai-tanstack-query)、页面化项目结构、前后端统一响应格式、错误处理、状态管理。适用于构建、重构、评审 React 前端项目。
---

# React 前端编码规范

对所有代码应用 `typescript-standards`(TypeScript 通用编码规范)。

- 如果是 Next.js 项目,项目结构参考 `nextjs-standards`。
- 如果是 TanStack Start + Cloudflare Workers 项目,项目结构参考 `tanstack-cloudflare-standards`。

## 技术栈

- 使用 TypeScript 作为主要编程语言,确保类型安全和代码可维护性。
- 使用 React 作为核心 UI 库,构建可复用的组件。
  - 使用 Sonner 作为全局通知和提示的解决方案。
  - 全局只需在根组件引入一次 `Toaster` 组件。
  - 使用 React Hook 进行状态和副作用管理,遵循 React 的最佳实践。
- 使用 Tailwind CSS 进行样式设计,确保响应式和一致的用户界面。
- 使用 Jotai 进行状态管理。
- 使用 jotai-tanstack-query、@tanstack/query-core 进行数据获取和状态管理。

## 项目结构

- 代码应遵循清晰的页面化结构,确保每个页面职责单一,易于维护和扩展。
- 页面中组件化,确保组件可复用,提升开发效率。确保每个组件职责单一。
- 页面特有组件放在页面目录下的 `components/` 文件夹。
- 整站组件按职责分类放在 `components/` 目录下:站点特有自定义组件放在 `components/ui/`,通用复合组件放在 `components/common/`,布局组件放在 `components/layouts/`,全局 Providers 放在 `components/providers/`。
- 根布局只负责全局基础设施;不要默认在根布局中放置 Header、Footer 或页面级内容容器。
- Header、Footer、Sidebar 和页面级 Providers 应由对应的页面或路由布局组合,以支持不同页面使用不同布局。
- 优先使用页面级或路由级布局复用结构,不要在每个 page 组件中重复组合相同的布局 UI。
- Providers 通常使用 `components/providers/index.tsx`,主题等独立 provider 可以放在 `components/providers/theme-provider/index.tsx`。
- 跨站点通用的复合 UI 放在 `packages/ui/src/components/custom/` 统一承载。
- 如果是全栈应用,使用 `modules/<domain>/` 存放不同业务域的代码,并遵循 `typescript-standards` 中的目录职责与单向依赖规范。
- 文件和目录使用 kebab-case 命名。

通用目录结构可参考:

```
src/
├── components/
│   ├── ui/                   # 当前站点特有的自定义组件
│   ├── common/               # 通用复合组件
│   ├── layouts/              # 布局组件
│   └── providers/            # 全局 Providers
│       ├── index.tsx
│       └── theme-provider/
│           └── index.tsx
├── types/                    # 类型定义
├── utils/                    # 通用纯帮助函数
├── lib/                      # 三方库实例与协议封装
└── modules/                  # 业务域代码
    └── <domain>/
        └── index.ts
```

## UI 组件

- 优先使用 shadcn 组件,从 `@workspace/ui/components/shadcn/<name>` 导入。
- 使用 shadcn 等价组件替换原生表单控件:`<select>` → `select`,`<input type="checkbox">` → `checkbox`,其他 `<input>` → `input`,`<textarea>` → `textarea`,`<button>` → `button`。
- 如果 shadcn 没有直接覆盖某个需求,但可以通过组合 shadcn 组件满足,优先使用 shadcn 组合,而不是自研实现。
- 缺失且无法通过组合满足的需求才新增自定义组件;跨站点通用组件放到 `packages/ui/src/components/custom/`,当前站点特有组件放到项目的 `components/ui/`。

## 前后端约定

- 使用 RESTful 风格设计 API,确保资源的统一性和可预测性。
- API 请求和响应默认使用 JSON 格式进行数据交换;文件上传、下载等特殊场景应使用契约中明确的 `multipart/form-data`、文件流或其他适合的格式。
- 使用 `{ "code": string, "message": string, "data": any }` 作为统一的响应格式:
  - 其中 `code` 为字符串类型的错误码,`message` 为描述信息,`data` 为具体的响应数据。
  - 如果请求成功,`code` 应为 `"SUCCESS"`,`message` 可为空字符串,也可为业务所需的成功消息,`data` 包含实际数据。
  - 如果请求失败,`code` 应为具体的错误码字符串,`message` 包含错误描述,`data` 可为 `null` 或包含错误相关的数据。
- 所有敏感信息(如密码、令牌)在传输和存储时必须进行加密处理。
- 前端与后端约定使用 JWT(JSON Web Token)进行用户认证和授权。

## 错误处理

- 在前端应用中,异步操作可以使用 `try/catch` 块进行错误处理。
- 对于 API 请求错误,前端应根据后端返回的错误码和消息进行相应的处理和用户提示。需要有一个统一的错误处理机制,根据错误码进行分类处理。
- 错误 Toast 或提示信息应包含足够的上下文信息,以便于用户理解问题所在。
- 避免在前端暴露敏感的内部错误信息,确保安全性。
- 对于已知错误类型,提供明确的用户提示,帮助用户进行相应操作。
- 错误码应遵循统一的命名规范,便于识别和管理。

## TypeScript

- 类型定义文件应放置在 `types/` 目录下,确保类型定义的集中管理和易于维护,方便打包时自动包含。
- 使用接口(`interface`)和类型别名(`type`)定义复杂的数据结构,确保代码的可读性和可维护性。
- 避免使用 `any` 类型,尽量使用具体的类型定义,以确保类型安全。
- 使用枚举(`enum`)定义一组相关的常量值,确保代码的可读性和可维护性。
- 使用类型断言(`as`)时,应确保类型转换的正确性,避免潜在的类型错误。
- 定义通用类型时,使用泛型(`<T>`)以提高代码的灵活性和可重用性。
- 使用类型守卫(`typeof`、`instanceof`)进行类型检查,确保代码的类型安全。

## 状态管理

- 使用 React Query 进行服务器状态管理,确保数据获取和缓存的高效性。
- 使用 Jotai 进行客户端状态管理,确保状态的可预测性和易于维护。
- 避免在组件中直接操作全局状态,使用状态管理库提供的 API 进行状态更新。
- 使用原子(atom)和选择器(selector)进行状态的细粒度管理,确保状态的可复用性和可维护性。
- 页面级状态就近管理,全局状态谨慎使用;避免在状态管理中存储大量数据,确保状态的轻量级和高效性。
