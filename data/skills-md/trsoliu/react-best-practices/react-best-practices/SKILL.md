---
name: react-best-practices
version: 1.0.0
description: "React 项目开发全流程指南（中文）。涵盖技术栈选型、Monorepo 架构（pnpm + Turborepo）、开发规范、Git 提交约定、Changelog 管理、测试策略、代码审查、开发工作流与文档管理。适用于 React + TypeScript + Zustand + TanStack Query + Vitest + Playwright 技术栈。当用户创建 React 项目、编写/审查/重构 React 代码、配置测试或 CI/CD、创建需求/设计文档时自动激活。"
license: MIT
tags:
  - react
  - typescript
  - zustand
  - tanstack-query
  - monorepo
  - turborepo
  - pnpm
  - vitest
  - playwright
  - best-practices
  - chinese
  - architecture
  - testing
  - ci-cd
  - code-review
  - documentation
globs:
  - "**/*.tsx"
  - "**/*.ts"
  - "**/package.json"
  - "**/turbo.json"
  - "**/vite.config.*"
  - "**/vitest.config.*"
  - "**/playwright.config.*"
  - "**/.changeset/**"
compatibility: "适用于所有支持 Agent Skills 规范的 AI 编码助手，包括 Claude Code、Cursor、Cline、Windsurf、GitHub Copilot、Gemini CLI 等。"
---

# React 项目开发全流程指南

## 1. 技术栈选型指南

| 领域 | 选型 | 理由 |
|------|------|------|
| 语言 | TypeScript 5.x（strict mode） | 类型安全，减少运行时错误 |
| UI 框架 | React 18/19 | 生态成熟，社区活跃 |
| 包管理 | pnpm | workspace 原生支持，磁盘效率高，严格依赖隔离 |
| Monorepo | Turborepo | 增量构建、任务编排、远程缓存，与 pnpm 深度集成 |
| 客户端状态 | Zustand | 轻量（~1KB），API 简洁，无 Provider 嵌套 |
| 服务端状态 | TanStack Query | 缓存、重试、乐观更新、后台刷新一站式解决 |
| 路由 | React Router v7 | 通用 SPA 路由，类型安全，数据加载内置 |
| 样式 | Tailwind CSS + CSS Modules | 原子化 CSS 提效 + 模块化隔离 |
| 表单 | React Hook Form + Zod | 非受控高性能 + schema 验证复用 |
| HTTP | Axios / ky | 拦截器、取消请求，配合 TanStack Query |
| 构建 | Vite | 极速 HMR，ESM 原生支持 |
| 单元/组件测试 | Vitest + Testing Library | Vite 生态原生，API 兼容 Jest |
| E2E 测试 | Playwright | 多浏览器、自动等待、trace 调试 |
| 代码质量 | ESLint + Prettier + typescript-eslint | 统一风格，自动格式化 |
| Git Hooks | Husky + lint-staged + commitlint | 提交前自动检查，规范 commit message |
| 版本管理 | Changesets | 原生支持 monorepo 多包版本，自动生成 CHANGELOG |

## 2. Monorepo 项目架构规范

采用 pnpm workspace + Turborepo，推荐目录结构：

```
my-react-app/
├── pnpm-workspace.yaml       # workspace 配置
├── turbo.json                 # Turborepo 任务管道配置
├── package.json               # 根 package.json（scripts + devDeps）
├── .changeset/                # Changesets 配置
├── .husky/                    # Git hooks
├── apps/                      # 应用层
│   ├── web/                   # 主 Web 应用
│   │   ├── src/
│   │   │   ├── app/           # 入口、路由配置、全局 Provider
│   │   │   ├── features/      # 按功能模块组织（核心）
│   │   │   │   └── auth/
│   │   │   │       ├── components/
│   │   │   │       ├── hooks/
│   │   │   │       ├── api/
│   │   │   │       ├── stores/
│   │   │   │       ├── types/
│   │   │   │       └── index.ts
│   │   │   ├── components/    # 应用级通用组件
│   │   │   ├── hooks/         # 应用级通用 hooks
│   │   │   ├── lib/           # 工具函数、API 客户端、Query 配置
│   │   │   └── test/          # 测试工具、setup、mocks
│   │   ├── e2e/               # Playwright E2E 测试
│   │   ├── vite.config.ts
│   │   └── package.json
│   └── docs/                  # 文档站（可选）
├── packages/                  # 共享包
│   ├── ui/                    # 共享 UI 组件库
│   │   ├── src/
│   │   ├── package.json
│   │   └── tsconfig.json
│   ├── utils/                 # 共享工具函数
│   ├── tsconfig/              # 共享 TypeScript 配置
│   │   ├── base.json
│   │   ├── react.json
│   │   └── package.json
│   └── eslint-config/         # 共享 ESLint 配置
│       ├── index.js
│       └── package.json
├── docs/                      # 项目文档（需求/设计/ADR/指南）
└── tooling/                   # 工具配置（可选）
    └── prettier-config/
```

### 关键配置示例

**pnpm-workspace.yaml：**
```yaml
packages:
  - "apps/*"
  - "packages/*"
  - "tooling/*"
```

**turbo.json：**
```json
{
  "tasks": {
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**"] },
    "lint": { "dependsOn": ["^build"] },
    "typecheck": { "dependsOn": ["^build"] },
    "test": { "dependsOn": ["^build"] },
    "dev": { "cache": false, "persistent": true }
  }
}
```

**包间依赖（package.json）：**
```json
{
  "dependencies": {
    "@my-app/ui": "workspace:*",
    "@my-app/utils": "workspace:*"
  }
}
```

## 3. 应用内架构规范（feature-based）

每个 app 内部按功能模块组织，遵循以下命名规范：

| 类型 | 命名规则 | 示例 |
|------|---------|------|
| 组件 | PascalCase | `UserProfile.tsx` |
| Hooks | camelCase + `use` 前缀 | `useAuth.ts` |
| Stores | camelCase + `use` 前缀 + `Store` 后缀 | `useAuthStore.ts` |
| 工具函数 | camelCase | `formatDate.ts` |
| 类型文件 | PascalCase | `User.ts` |
| 常量 | UPPER_SNAKE_CASE | `API_BASE_URL` |
| 测试文件 | 与源文件同名 + `.test` | `useAuth.test.ts` |

### Import 排序规则
```typescript
// 1. 外部依赖
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'

// 2. 内部包（monorepo）
import { Button } from '@my-app/ui'

// 3. 相对路径
import { useAuthStore } from '../stores/useAuthStore'

// 4. 类型导入
import type { User } from '../types/User'
```

### Barrel file 策略
- 每个 feature 模块提供 `index.ts` 作为公共 API 出口
- 禁止跨 feature 直接引用内部文件，必须通过 `index.ts`
- `packages/` 下的共享包必须有 `index.ts` 导出
- 大型项目避免深层嵌套的 barrel re-export（影响 tree-shaking）

## 4. 开发约束与规范

### TypeScript 严格配置
```json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,
    "exactOptionalPropertyTypes": true
  }
}
```

### 编码规则
- 禁止使用 `any`，用 `unknown` + 类型守卫替代
- `interface` 用于组件 Props 和对象结构，`type` 用于联合类型和工具类型
- 优先使用命名导出（`export function`），避免默认导出
- 组件文件不超过 200 行，超出则拆分子组件或提取 Hook
- 超过 10 行的逻辑提取为自定义 Hook
- 使用判别联合（discriminated unions）管理复杂状态

### Zustand 规范
```typescript
// ✅ 推荐：单 store 单领域，actions 与 state 分离
interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
}

interface AuthActions {
  login: (user: User, token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState & AuthActions>()(
  devtools(
    persist(
      (set) => ({
        user: null,
        token: null,
        isAuthenticated: false,
        login: (user, token) => set({ user, token, isAuthenticated: true }),
        logout: () => set({ user: null, token: null, isAuthenticated: false }),
      }),
      { name: 'auth-storage' }
    )
  )
)

// ✅ 使用 selector 防止不必要的 re-render
const user = useAuthStore((s) => s.user)
```

### TanStack Query 规范
```typescript
// ✅ Query Key Factory 模式
export const userKeys = {
  all: ['users'] as const,
  lists: () => [...userKeys.all, 'list'] as const,
  list: (filters: UserFilters) => [...userKeys.lists(), filters] as const,
  details: () => [...userKeys.all, 'detail'] as const,
  detail: (id: string) => [...userKeys.details(), id] as const,
}

// ✅ 自定义 Hook 封装
export function useUser(id: string) {
  return useQuery({
    queryKey: userKeys.detail(id),
    queryFn: () => fetchUser(id),
    staleTime: 5 * 60 * 1000, // 5 分钟
  })
}
```

## 5. Git 提交约定

### Conventional Commits 格式
```
<type>(<scope>): <description>

[可选 body]

[可选 footer]
```

### Type 类型
| Type | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `refactor` | 重构（不改变功能） |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `docs` | 文档变更 |
| `style` | 代码格式（不影响逻辑） |
| `chore` | 构建/工具/依赖变更 |
| `ci` | CI/CD 配置变更 |

### Scope 定义（React 项目）
`auth`, `ui`, `api`, `store`, `test`, `config`, `deps`, `router`, `i18n`

### 中文示例
```
feat(auth): 添加用户登录功能
fix(cart): 修复购物车数量更新竞态条件
refactor(api): 将验证逻辑提取到中间件
test(user): 添加用户注册单元测试
chore(deps): 升级 React 至 v19
perf(list): 大列表添加虚拟滚动优化
```

### 分支命名
- `feature/<scope>-<description>` — 新功能
- `fix/<scope>-<description>` — Bug 修复
- `hotfix/<description>` — 紧急修复
- `refactor/<description>` — 重构
- `docs/<description>` — 文档
- `test/<description>` — 测试

### Husky + commitlint + lint-staged 配置
```json
// package.json（根目录）
{
  "scripts": {
    "prepare": "husky"
  },
  "lint-staged": {
    "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
    "*.{json,md,yaml}": ["prettier --write"]
  }
}
```

```javascript
// commitlint.config.js
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'scope-enum': [2, 'always', ['auth', 'ui', 'api', 'store', 'test', 'config', 'deps', 'router', 'i18n']],
  },
}
```

## 6. Changelog 管理规范

### 工具选型：Changesets
Changesets 原生支持 monorepo 多包版本管理，与 pnpm workspace 深度集成。

### 初始化
```bash
pnpm add -Dw @changesets/cli
pnpm changeset init
```

### 日常流程
```bash
# 1. 开发完成后，添加变更记录
pnpm changeset
# 交互式选择：影响的包 → 版本类型（patch/minor/major）→ 变更描述

# 2. 发版时，消费变更记录
pnpm changeset version
# 自动更新各包 package.json 版本号 + 生成 CHANGELOG.md

# 3. 发布
pnpm changeset publish
```

### 版本号规则（SemVer）
| 变更类型 | 版本号 | 示例 |
|---------|--------|------|
| Breaking Change | major | 1.0.0 → 2.0.0 |
| 新功能 | minor | 1.0.0 → 1.1.0 |
| Bug 修复 | patch | 1.0.0 → 1.0.1 |

### CI/CD 集成（GitHub Actions）
```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    branches: [main]
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
      - run: pnpm install --frozen-lockfile
      - uses: changesets/action@v1
        with:
          publish: pnpm changeset publish
          version: pnpm changeset version
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          NPM_TOKEN: ${{ secrets.NPM_TOKEN }}
```

## 7. 测试策略

### 测试金字塔
```
        ┌─────────┐
        │  E2E    │  Playwright — 关键用户流程
        ├─────────┤
        │ 组件测试 │  Vitest + Testing Library — 组件交互
        ├─────────┤
        │ 单元测试 │  Vitest — 工具函数、hooks、stores
        └─────────┘
```

### 覆盖率目标
- 单元测试：80%+
- 组件测试：70%+
- E2E：覆盖所有关键用户路径

### Vitest 配置
```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      exclude: ['node_modules/', 'src/test/', '**/*.d.ts'],
    },
  },
})
```

### Testing Library 规范
```typescript
// src/test/test-utils.tsx — 自定义 render（注入所有 Provider）
import { render } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { MemoryRouter } from 'react-router'

function createTestQueryClient() {
  return new QueryClient({ defaultOptions: { queries: { retry: false } } })
}

export function renderWithProviders(ui: React.ReactElement) {
  const queryClient = createTestQueryClient()
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter>{ui}</MemoryRouter>
    </QueryClientProvider>
  )
}
```

**查询优先级：** `getByRole` > `getByLabelText` > `getByText` > `getByTestId`
**事件：** 使用 `userEvent` 而非 `fireEvent`
**API Mock：** 使用 MSW（Mock Service Worker）

### Zustand Store 测试
```typescript
import { renderHook, act } from '@testing-library/react'
import { useAuthStore } from './useAuthStore'

beforeEach(() => {
  useAuthStore.setState({ user: null, token: null, isAuthenticated: false })
})

it('should login user', () => {
  const { result } = renderHook(() => useAuthStore())
  act(() => { result.current.login(mockUser, 'token-123') })
  expect(result.current.isAuthenticated).toBe(true)
})
```

### Playwright E2E 配置
```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  baseURL: 'http://localhost:5173',
  use: {
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'pnpm dev',
    port: 5173,
    reuseExistingServer: !process.env.CI,
  },
})
```

### Monorepo 测试编排
```bash
# Turborepo 增量测试（只测试受影响的包）
turbo run test --filter=...[HEAD~1]

# 全量测试
turbo run test

# 单包测试
turbo run test --filter=@my-app/web
```

## 8. 代码审查清单

### 功能
- [ ] 功能是否按需求正确实现
- [ ] 边界情况是否处理（空值、空数组、超长输入）
- [ ] 错误状态是否优雅处理（loading / error / empty）
- [ ] 是否有对应的需求文档或 issue 关联

### 代码质量
- [ ] 无 `any` 类型使用
- [ ] 组件职责单一，不超过 200 行
- [ ] 无不必要的 re-render（检查 selector、memo 使用）
- [ ] 复杂逻辑已提取为自定义 Hook
- [ ] 无硬编码的魔法数字/字符串（提取为常量）
- [ ] 命名清晰，符合命名规范

### 性能
- [ ] 大列表使用虚拟化（如 @tanstack/react-virtual）
- [ ] 图片使用懒加载
- [ ] 避免不必要的 useEffect
- [ ] useMemo/useCallback 用于昂贵计算和稳定引用
- [ ] 避免在 render 中创建新对象/数组

### 测试
- [ ] 新功能有对应测试
- [ ] 测试覆盖率未下降
- [ ] 测试命名描述行为而非实现
- [ ] Mock 范围最小化

### 无障碍
- [ ] 语义化 HTML 标签（button、nav、main、section）
- [ ] 键盘可导航（Tab、Enter、Escape）
- [ ] ARIA 标签完整（aria-label、role）
- [ ] 颜色对比度达标（WCAG AA 4.5:1）

## 9. 内置工作流

### 功能开发工作流（Feature Workflow）
```
需求确认 → 创建分支 → [编写 ADR] → 编码 → 测试 → 自查 → PR → CI → Review → 合并
```
1. 确认需求文档（PRD）已评审通过
2. 从 `main` 创建 `feature/<scope>-<desc>` 分支
3. 如涉及架构变更，先编写 ADR
4. 编码实现（遵循第 3、4 章规范）
5. 编写测试（遵循第 7 章策略）
6. 对照第 8 章代码审查清单自查
7. `pnpm changeset` 添加变更记录
8. 提交 PR，填写 PR 模板
9. CI 自动运行：lint → typecheck → test → build
10. Code Review 通过后合并

### Bug 修复工作流（Bugfix Workflow）
```
复现 → 创建分支 → 写失败测试 → 修复 → 回归 → PR → 合并
```
1. 复现问题，记录复现步骤
2. 从 `main` 创建 `fix/<scope>-<desc>` 分支
3. 先写一个能复现 bug 的失败测试用例
4. 修复代码使测试通过
5. 运行回归测试确认无副作用
6. `pnpm changeset`（patch 版本）
7. 提交 PR → 合并

### 发版工作流（Release Workflow）
```
changeset version → 更新版本 → CI → tag → 发布 → 通知
```
1. `pnpm changeset version` — 更新版本号和 CHANGELOG
2. 提交版本变更 commit
3. CI 自动构建 + 全量测试
4. 打 git tag
5. GitHub Release 发布（自动/手动）
6. 通知相关方（Slack/飞书/邮件）

### CI/CD Pipeline 工作流
```yaml
# PR 触发
lint → typecheck → unit test → build → preview deploy

# 合并 main 触发
full test → build → staging deploy

# tag 触发
build → production deploy
```

**GitHub Actions 模板（Monorepo 适配）：**
```yaml
# .github/workflows/ci.yml
name: CI
on:
  pull_request:
    branches: [main]
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo lint typecheck test build
```

## 10. 开发文档管理规范

### 文档目录结构
```
docs/
├── requirements/              # 需求文档
│   ├── 000-template.md        # 需求文档模板
│   ├── PRD-001-user-auth.md   # 产品需求文档
│   └── BRD-001-payment.md     # 业务需求文档
├── design/                    # 方案设计
│   ├── 000-template.md        # 设计文档模板
│   ├── HLD-001-system-arch.md # 概要设计
│   ├── LLD-001-auth-flow.md   # 详细设计
│   └── API-001-user.md        # API 接口设计
├── adr/                       # 架构决策记录
│   ├── 000-template.md        # ADR 模板
│   ├── 001-use-zustand.md
│   └── 002-monorepo-setup.md
├── guides/                    # 开发指南
│   ├── getting-started.md     # 快速上手
│   ├── development.md         # 开发环境搭建
│   ├── contributing.md        # 贡献指南
│   └── deployment.md          # 部署指南
├── specs/                     # 技术规格
│   └── api-design.md
└── decisions/                 # 技术选型记录
    └── tech-stack.md
```

### 需求文档规范（PRD/BRD）

**编号规则：** `<类型>-<序号>-<简述>` 如 `PRD-001-user-auth`

**PRD 模板：**
```markdown
# PRD-XXX: <功能名称>
- 状态：草稿 | 评审中 | 已确认 | 开发中 | 已完成
- 作者：
- 日期：

## 背景
为什么要做这个功能？

## 目标用户
谁会使用这个功能？

## 功能需求
### 核心功能
### 边界情况

## 非功能需求
性能、安全、兼容性要求

## 验收标准
- [ ] 标准 1
- [ ] 标准 2

## 优先级
P0/P1/P2/P3
```

**BRD 模板：**
```markdown
# BRD-XXX: <业务需求名称>
- 状态：草稿 | 评审中 | 已确认

## 业务背景
## 业务目标
## 业务流程
## 成功指标（KPI）
## 风险与依赖
```

### 方案设计文档规范

**概要设计（HLD）模板：**
```markdown
# HLD-XXX: <系统/模块名称>
- 状态：草稿 | 评审中 | 已批准
- 关联需求：PRD-XXX

## 系统架构图
## 模块划分
## 技术选型
## 数据流设计
## 部署方案
## 风险评估
```

**详细设计（LLD）模板：**
```markdown
# LLD-XXX: <功能名称>
- 关联 HLD：HLD-XXX

## 组件设计（组件图）
## 接口定义
## 状态管理设计
## 异常处理
## 性能考量
## 测试方案
```

**API 设计模板：**
```markdown
# API-XXX: <接口名称>

## 接口路径
`POST /api/v1/users/login`

## 请求格式
## 响应格式
## 错误码
## 鉴权方式
## 调用示例
```

**设计评审 Checklist：**
- [ ] 是否满足 PRD 中的所有需求
- [ ] 扩展性：未来需求变更是否容易适配
- [ ] 安全性：是否有 XSS/CSRF/注入风险
- [ ] 性能：是否考虑了大数据量场景
- [ ] 可测试性：是否方便编写测试

### ADR（架构决策记录）规范

**何时写 ADR：** 引入新依赖、变更架构模式、选择技术方案时

**ADR 模板：**
```markdown
# ADR-XXX: <决策标题>
- 状态：提议 | 已接受 | 已废弃 | 已替代
- 日期：
- 替代：ADR-YYY（如适用）

## 背景
什么问题需要决策？

## 决策
我们选择了什么方案？

## 备选方案
考虑过哪些其他方案？为什么没选？

## 后果
这个决策带来的正面和负面影响。
```

### 文档维护规则
- 新功能开发前必须有对应的需求文档（PRD）
- 涉及架构变更的功能必须有方案设计文档（HLD/LLD）
- 引入新技术/依赖必须有 ADR
- 新功能完成后必须更新相关开发指南
- README 保持最新的快速上手指引
- API 变更同步更新 specs 和 design 文档
- 每次发版检查文档是否需要更新
- 文档与代码同仓管理，PR 中同步提交
