---
name: check-refine-trpc
description: 检查组件是否直接使用 trpc，组件必须使用 refine。
---

# 组件级强制规则：禁止直接使用 trpc

- 目的：在代码库中识别前端组件/页面中**直接导入或调用 `trpc` 客户端** 或 `@tanstack/react-query` 的 hook 的情况。
- 规则：组件层必须使用 `refine` 的 hooks（例如 `useList`、`useOne`、`useCreate`、`useUpdate`）或通过已实现的 `DataProvider` 封装后再在组件中使用。**禁止在组件或页面中直接使用 `trpc` 客户端或其 hooks。**

## 检测方法

- 静态扫描组件/页面文件，查找直接导入或使用以下模式（任意匹配即为违规）：
  - 导入 `trpc` 客户端（如 `import { trpc } from` / `import trpcClient from`）
  - 直接使用 `trpc.*.useQuery` / `trpc.*.useMutation` 或 `useQuery`/`useMutation` 来自 `@tanstack/react-query` 并用于组件渲染
  - 直接在组件中调用 `trpcClient` 的方法（如 `trpcClient.query(...)`）

## 示例（禁止 / 允许）

- 禁止：在组件中直接使用 trpc hook

- 禁止示例：见 [bad-example.ts](references/bad-example.ts)
- 允许示例：见 [good-example.ts](references/good-example.ts)

## 核查清单（强制）

- 目标：定位并列出需要从 `trpc`/`react-query` 迁移到 `refine` 的组件使用点，提供最小可执行修复建议。
- 违规判断（任一成立即违规）：
  - 文件包含 `import .*\btrpc\b` / `import trpcClient` 等直接导入
  - 使用 `trpc\.[A-Za-z0-9_]+\.(useQuery|useMutation)`
  - 在组件中直接使用 `useQuery(` 或 `useMutation(` 来自 `@tanstack/react-query`
  - 在组件中直接调用 `trpcClient.*` RPC 方法
- 推荐自动化检测正则（示例）：
  - 导入检测：`import\s+.*\btrpc\b|import\s+trpcClient`
  - hook 检测：`trpc\.[a-zA-Z0-9_]+\.(useQuery|useMutation)`
  - react-query 检测：`from\s+['\"]@tanstack/react-query['\"]|\buseQuery\s*\(`

## 修复建议

- 优先：用 `refine` 的 `useList`/`useOne`/`useCreate`/`useUpdate` 替换组件内数据调用。
- 可选：在 `DataProvider` 中封装 trpc 调用并在组件中通过 `resource` + `refine` hooks 使用。
- 复杂查询：在 `DataProvider` 增加 `custom`，并通过 refine 的自定义 hook 使用，保持行为等价（分页/筛选映射）。
