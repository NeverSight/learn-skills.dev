---
name: nextjs-standards
description: Next.js App Router 项目结构规范:目录结构、路由组、布局与动态路由、proxy.ts/middleware 鉴权、API Routes、Jotai 状态管理、Server/Client Components、Providers、命名与导入约定。适用于开发、重构、评审 Next.js 应用(如 app/layout.tsx、page.tsx、proxy.ts、route.ts)。
---

# Next.js 项目结构规范

编辑前先确认仓库确实使用 Next.js。同时应用 `typescript-standards`(TypeScript 通用编码规范)与 `react-frontend-standards`(React 前端编码规范)。

## 核心原则

- 代码应遵循清晰的页面化结构,确保每个页面职责单一,易于维护和扩展
- 页面中组件化,确保组件可复用,提升开发效率。确保每个组件职责单一
- 遵循命名约定,文件和目录名称应使用 kebab-case 命名法
- `src/types` 目录下存放所有类型定义文件
- 保留仓库既定的 App Router 或 Pages Router 约定,没有明确要求时不要在两者之间迁移

## 目录结构

```
src/
├── app/                       # 页面和布局组件（App Router）
│   ├── layout.tsx            # 根布局组件
│   ├── page.tsx              # 首页
│   ├── (auth)/               # 需要认证的路由组
│   │   ├── layout.tsx        # 认证布局
│   │   ├── dashboard/
│   │   │   ├── page.tsx
│   │   │   ├── components/   # 页面特有组件
│   │   │   │   └── stats-card.tsx
│   │   │   └── stores/       # 页面特有状态
│   │   │       └── dashboard-store.ts
│   │   └── settings/
│   │       └── page.tsx
│   ├── (public)/             # 公共访问路由组
│   │   ├── layout.tsx        # 公共页面布局
│   │   ├── about/
│   │   │   └── page.tsx
│   │   └── auth/
│   │       ├── login/
│   │       │   └── page.tsx
│   │       └── components/
│   │           └── login-form.tsx
│   ├── api/                  # API 路由
│       ├── users/
│       │   └── route.ts
│       └── products/
│           └── route.ts
│   ├── [some-page]/
│   │   ├── layout.tsx        # 页面级布局
│   │   └── page.tsx
│
├── components/               # 整站可复用的 UI 组件
│   ├── ui/                   # 当前站点特有的自定义组件
│   │   └── user-avatar.tsx
│   ├── common/               # 通用复合组件
│   │   ├── header.tsx
│   │   └── footer.tsx
│   ├── layouts/              # 布局组件
│   │   ├── auth-layout.tsx
│   │   └── public-layout.tsx
│   └── providers/            # 全局 Providers
│       ├── index.tsx
│       └── theme-provider/
│           └── index.tsx
│
├── stores/                   # 整站公共状态管理（Jotai）
│   ├── user-store.ts        # 用户认证状态
│   └── theme-store.ts       # 主题状态
│
├── types/                    # 类型定义
│   ├── user.ts
│   └── api.ts
│
├── utils/                    # 公共工具函数
│   ├── auth.ts
│   └── formatters.ts
│
├── hooks/                    # 公共自定义 Hooks
│   └── use-auth.ts
│
├── lib/                      # 第三方库封装
│   └── db.ts
│
├── modules/                  # 全栈 Next.js 的业务域代码
│   └── <domain>/
│       └── index.ts
│
└── proxy.ts                  # 中间件
```

## 路由规范

### 根布局 (layout.tsx)

```tsx
// src/app/layout.tsx
import type { Metadata } from 'next'
import { Providers } from '@/components/providers'

export const metadata: Metadata = {
  title: 'My App',
  description: 'My Next.js App',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body>
        <Providers>
          {children}
        </Providers>
      </body>
    </html>
  )
}
```

RootLayout 只负责全局基础设施,例如 `<html>`、`<body>`、全局 Providers、全局样式和必要的全局通知容器。不要在 RootLayout 中默认放置 `Header`、`Footer` 或页面级 `<main>`;不同页面可能需要不同的布局。

### 页面级布局 ([some-page]/layout.tsx)

```tsx
// src/app/[some-page]/layout.tsx
import { Header } from '@/components/common/header'
import { Footer } from '@/components/common/footer'

export default function SomePageLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <>
      <Header />
      <main>{children}</main>
      <Footer />
    </>
  )
}
```

Header、Footer、Sidebar 和页面级 Providers 应放在对应的路由组或页面目录的 `layout.tsx` 中。使用嵌套路由布局复用同一页面区域的结构,使用不同的 `layout.tsx` 支持不同页面的布局差异。

### 认证路由组 ((auth))

```tsx
// src/app/(auth)/layout.tsx
import { redirect } from 'next/navigation'
import { getUser } from '@/utils/auth'

export default async function AuthLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const user = await getUser()

  if (!user) {
    redirect('/auth/login')
  }

  return (
    <div className="auth-layout">
      <Sidebar />
      <main className="content-area">{children}</main>
    </div>
  )
}
```

### 公共路由组 ((public))

```tsx
// src/app/(public)/auth/login/page.tsx
import { LoginForm } from './components/login-form'

export default function LoginPage() {
  return (
    <div className="login-page">
      <LoginForm />
    </div>
  )
}
```

### 动态路由

```tsx
// src/app/products/[id]/page.tsx
interface ProductPageProps {
  params: { id: string }
}

export default async function ProductPage({ params }: ProductPageProps) {
  const product = await getProduct(params.id)
  return <ProductDetail product={product} />
}
```

## 中间件（Proxy.ts）

### 使用 Proxy.ts 进行鉴权

```tsx
// src/proxy.ts
import { getSessionCookie } from "better-auth/cookies";
import { type NextRequest, NextResponse } from "next/server";

export function proxy(request: NextRequest) {
  const sessionCookie = getSessionCookie(request);

  // Optimistic redirect only. The authoritative auth check remains in page/layout server code.
  if (!sessionCookie) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard"], // Specify the routes the middleware applies to
};
```

中间件/代理检查只是优化手段,权威的认证与授权仍应保留在页面/布局的服务端代码中。

## API Routes

```tsx
// src/app/api/users/route.ts
import { NextResponse } from 'next/server'
import { db } from '@/lib/db'

export async function GET() {
  const users = await db.users.findMany()
  return NextResponse.json(users)
}

export async function POST(request: Request) {
  const data = await request.json()
  const user = await db.users.create({ data })
  return NextResponse.json(user, { status: 201 })
}
```

API 路由保持薄层:校验输入、调用领域逻辑、返回契约约定的状态码与响应结构;使用 RESTful 路由和 JSON,除非契约明确要求其他格式。

## 组件规范

### 页面特有组件

- 放在页面目录下的 `components/` 文件夹
- 使用 kebab-case 命名:`stats-card.tsx`
- 使用 `'use client'` 指令（如需客户端交互）

### 全局复用组件

- 放在 `src/components/` 目录下
- `components/ui/`:当前站点特有的自定义组件
- `components/common/`:跨页面通用的复合组件
- `components/layouts/`:布局组件
- `components/providers/`:全局 Providers;根 Providers 通常为 `components/providers/index.tsx`,主题等独立 provider 可以为 `components/providers/theme-provider/index.tsx`
- 使用 kebab-case 命名

### UI 组件优先使用 shadcn

- 优先使用 shadcn 组件,从 `@workspace/ui/components/shadcn/<name>` 导入。
- 使用 shadcn 等价组件替换原生表单控件:`<select>` → `select`,`<input type="checkbox">` → `checkbox`,其他 `<input>` → `input`,`<textarea>` → `textarea`,`<button>` → `button`。
- 如果 shadcn 没有直接覆盖某个需求,但该需求可以通过组合 shadcn 组件满足,优先使用 shadcn 组合,而非自研实现。

### 自定义组件归属

- 缺失且无法通过组合满足的需求才新增自定义组件。
- 跨站点通用组件放到 `packages/ui/src/components/custom/`,统一承载当前通用复合 UI。
- 当前站点特有的组件放到项目的 `components/ui/` 目录下。

## 全栈 Next.js 的业务模块

- 如果是全栈 Next.js,建议使用 `modules/<domain>/` 存放不同业务域的代码,例如常量/标签、selections、query keys、GraphQL query options 和纯业务函数。
- 按业务使用 kebab-case 创建 domain 目录。
- 模块内文件名省略域名前缀,以 `index.ts` 桶导出作为对外入口。
- 目录依赖遵循 `typescript-standards` 中的单向依赖规范;业务模块可以依赖 `lib/` 和 `utils/`,不得反向依赖业务模块。

## 状态管理（Jotai）

### 全局 Store

```tsx
// src/stores/user-store.ts
import { atom } from 'jotai'

export interface User {
  id: string
  email: string
  name: string
  role: 'admin' | 'user'
}

// 基础 atom
export const userAtom = atom<User | null>(null)

// 派生 atom
export const isAuthenticatedAtom = atom(
  (get) => get(userAtom) !== null
)

// 派生 atom - 用户角色
export const userRoleAtom = atom(
  (get) => get(userAtom)?.role || 'guest'
)

// 写入 atom - 更新用户
export const updateUserAtom = atom(
  null,
  (get, set, user: User | null) => {
    set(userAtom, user)
    // 可选：同步到 localStorage
    if (user) {
      localStorage.setItem('user', JSON.stringify(user))
    } else {
      localStorage.removeItem('user')
    }
  }
)

// 异步 atom - 获取用户信息
export const fetchUserAtom = atom(
  async (get) => {
    const response = await fetch('/api/user')
    const user = await response.json()
    return user as User
  }
)
```

### 主题 Store

```tsx
// src/stores/theme-store.ts
import { atom } from 'jotai'

type Theme = 'light' | 'dark'

export const themeAtom = atom<Theme>('light')

export const toggleThemeAtom = atom(
  null,
  (get, set) => {
    const current = get(themeAtom)
    const next = current === 'light' ? 'dark' : 'light'
    set(themeAtom, next)
    localStorage.setItem('theme', next)
  }
)
```

### 页面级 Store

```tsx
// src/app/(auth)/dashboard/stores/dashboard-store.ts
import { atom } from 'jotai'

export interface DashboardStats {
  totalUsers: number
  activeUsers: number
  revenue: number
}

export const statsAtom = atom<DashboardStats | null>(null)
export const isLoadingAtom = atom(false)

export const fetchStatsAtom = atom(
  async (get) => {
    const response = await fetch('/api/dashboard/stats')
    const stats = await response.json()
    return stats as DashboardStats
  }
)
```

### 使用示例

```tsx
'use client'

import { useAtom, useAtomValue, useSetAtom } from 'jotai'
import { userAtom, isAuthenticatedAtom, updateUserAtom } from '@/stores/user-store'

export function UserProfile() {
  const [user] = useAtom(userAtom)
  const isAuthenticated = useAtomValue(isAuthenticatedAtom)
  const updateUser = useSetAtom(updateUserAtom)

  const handleLogout = () => {
    updateUser(null)
    // 登出逻辑
  }

  return (
    <div>
      {isAuthenticated ? (
        <div>
          <p>{user?.name}</p>
          <button onClick={handleLogout}>登出</button>
        </div>
      ) : (
        <p>请登录</p>
      )}
    </div>
  )
}
```

## Server Components vs Client Components

### Server Components（默认）

```tsx
// 服务端组件 - 可直接使用 async/await
import { getData } from '@/lib/data'

export default async function ServerPage() {
  const data = await getData()
  return <div>{data}</div>
}
```

### Client Components

```tsx
'use client'

import { useState } from 'react'
import { useAtom } from 'jotai'
import { themeAtom } from '@/stores/theme-store'

export default function ClientComponent() {
  const [theme, setTheme] = useAtom(themeAtom)
  const [count, setCount] = useState(0)

  return (
    <button onClick={() => setCount(count + 1)}>
      {count} - Theme: {theme}
    </button>
  )
}
```

仅在组件需要浏览器 API、状态、副作用或事件处理器时才添加 `'use client'`;服务端专用依赖和密钥不得出现在客户端模块中。

## Providers 配置

Providers 放在 `src/components/providers/` 目录下。根 Providers 使用 `index.tsx`,例如 Jotai 与 Query Client;主题等独立 provider 使用 `theme-provider/index.tsx` 等子目录入口,便于按职责拆分。

```tsx
// src/components/providers/index.tsx
'use client'

import { Provider as JotaiProvider } from 'jotai'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

export function Providers({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(() => new QueryClient())

  return (
    <JotaiProvider>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </JotaiProvider>
  )
}
```

## 命名约定

- 文件和目录:`kebab-case` (如:`user-profile.tsx`)
- 组件函数:`PascalCase` (如:`UserProfile`)
- 变量和函数:`camelCase` (如:`getUserData`)
- 类型和接口:`PascalCase` (如:`UserProfileProps`)
- Jotai atoms:`camelCase` 以 `Atom` 结尾 (如:`userAtom`)

## 导入规范

```tsx
// shadcn 组件从共享 UI 包导入
import { Button } from '@workspace/ui/components/shadcn/button'
import { useAtom } from 'jotai'
import { userAtom } from '@/stores/user-store'
import type { User } from '@/types/user'
```

项目内部模块使用已配置的 `@/` 别名引用 `src` 目录;站点特有自定义组件从 `@/components/ui/...` 导入。

## 元数据配置

```tsx
// src/app/dashboard/page.tsx
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Dashboard',
  description: 'User dashboard page',
}
```

## 中间件配置（旧版本兼容）

Next.js 新项目使用 `src/proxy.ts` 作为请求代理入口;不要同时创建 `proxy.ts` 和 `middleware.ts`。仅在项目仍使用旧版 Next.js 时,才使用下面的 `middleware.ts` 形式。

```tsx
// src/middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { AuthProxy } from '@/lib/proxy'

export async function middleware(request: NextRequest) {
  const authProxy = AuthProxy.getInstance()

  // 使用 Proxy 处理认证
  const result = await authProxy.handle(request)
  if (result) return result

  // 继续其他逻辑
  return NextResponse.next()
}

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/settings/:path*',
    '/auth/:path*',
  ],
}
```

## 最佳实践

- 页面职责单一,避免臃肿
- 组件保持小而专注,职责单一
- 优先使用 Server Components,仅在必要时使用 Client Components
- 类型定义集中管理,保持类型安全
- 页面级状态（Jotai atoms）就近管理,全局状态谨慎使用
- 使用路由组 `(folder)` 组织相关页面
- API 路由遵循 RESTful 规范
- 使用中间件 + Proxy.ts 处理鉴权逻辑
- Jotai atoms 分为基础 atom、派生 atom、写入 atom 和异步 atom
- 环境变量管理配置信息

## 校验

- 修改路由、布局、proxy、元数据、配置或 Server/Client 边界后,运行仓库的类型检查与构建检查
- 涉及认证、未认证、not-found、loading、error 路径变更时,逐一验证这些路径
