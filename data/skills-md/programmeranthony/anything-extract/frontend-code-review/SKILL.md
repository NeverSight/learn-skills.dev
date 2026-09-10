---
name: frontend-code-review
description: 指导在项目中对前端代码（Next.js/React/TypeScript/Tailwind 等）进行结构、可维护性、性能与一致性审查，基于既定规则清单。适用于用户请求审查 .tsx/.ts/.js/.jsx 等前端文件或前端目录下的页面与组件。不用于后端代码（如 .py）。
---

# Frontend Code Review（前端代码审查）

## 何时使用本 Skill

当用户要求**审查、分析或改进前端代码**（例如 `.tsx`、`.ts`、`.js` 文件）时使用本 skill。常见场景包括：

- **待提交变更审查**：在提交前检查当前变更中涉及的前端文件。
- **代码片段审查**：用户粘贴某个组件/页面/Hook 片段，请求审查。
- **按文件/模块审查**：用户点名一到数个前端文件或某个路由/组件目录。

以下情况**不要**使用本 skill：

- 审查目标是后端代码（如 `.py`、服务层、数据库访问等）——此时应使用后端 Code Review Skill。
- 仅讨论架构文档或后端接口设计，而非前端实现。

## 如何使用本 Skill

1. **明确审查范围与模式**：根据用户输入，限定在指定的组件、页面或目录内，不要「全仓库漫扫」。
2. 按 **Checklist** 中的规则执行审查；对每条命中的规则，找到**具体代码位置**并给出可执行建议。
3. 若某段代码未被 Checklist 覆盖，可参考 **General Review Rules** 做尽力审查。
4. 输出时**必须**严格遵循「Required Output」中的模板之一。

注意：

- 优先给出**具体、可落地**的改进建议（包括何处拆分组件、如何组织状态、如何统一样式等）。
- 若能提供简短代码示例，可帮助后续自动修复。

## 项目前端结构（审查范围参考）

以典型的 Next.js App Router + React + TypeScript + Tailwind 项目为例，常见分层与职责如下（实际路径以当前仓库为准，可根据项目实际结构类比到对应目录）：

- **路由与页面入口目录（例如 `app/` 或 `frontend/app/`）**：
  - 路由与页面入口（如 `app/xxx/page.tsx`、`app/[id]/page.tsx` 等）。
  - 顶层布局（如 `layout.tsx`），通常挂载全局布局组件（主框架、侧边栏、头部），不要在此堆积业务逻辑。
- **通用与领域组件目录（例如 `components/` 或 `frontend/components/`）**：
  - 复用的布局组件（如页面头部、布局容器）、表格/卡片/表单等 UI 组件。
  - 领域组件（如知识库列表、文档分段列表、业务向导步骤组件等），负责组合 UI 与轻量交互。
- **`lib/` 或 `services/`**：
  - HTTP 客户端与前端 API 封装（如 axios 实例、领域 API 模块）。
  - 通用工具函数与 Hook（如复用的数据加载 Hook、格式化工具等）。
-- **样式配置**：
  - 全局样式（如 `app/globals.css`）用于基础样式、滚动条、字体等。
  - Tailwind 配置（如 `tailwind.config.js`）可扩展主题颜色、间距、阴影等设计令牌，避免散落魔法值。

在进行前端 Code Review 时，优先检查：

- 页面是否复用了现有布局组件与上下文（例如统一的页面头部组件、侧边栏折叠状态的上下文），而不是各自实现一套布局。
- 新增页面是否放在合理的路由目录（与现有路由结构保持一致），新增组件是否放在组件目录下的合适子目录，而不是全部堆在页面文件中。
- 数据请求是否统一走封装好的 API 层或服务模块，而不是在组件内重复配置 axios/fetch。



## Checklist

根据审查范围，优先按以下规则文件进行检查：

- **代码质量与组件设计**：若涉及组件/Hook/页面结构、TypeScript 类型、可维护性，参考 [references/code-quality-rule.md](references/code-quality-rule.md)。
- **布局、样式与 UI 一致性**：若涉及布局框架、全局样式、颜色与风格统一、响应式表现，参考 [references/layout-style-rule.md](references/layout-style-rule.md)。
- **状态管理与数据流**：若涉及本地/全局状态、表单状态、异步数据加载、API 错误处理，参考 [references/state-data-rule.md](references/state-data-rule.md)。
- **性能与交互体验**：若涉及渲染性能、大列表、客户端/服务端边界、懒加载、交互反馈，参考 [references/performance-rule.md](references/performance-rule.md)。

若 Checklist 中的规则均不适用，可退回到下文的 General Review Rules 做尽力审查。

## General Review Rules

从以下四个维度给出审查意见：

1. **结构与可维护性**
   - 组件/页面是否职责单一，可读性良好，便于拆分与复用。
   - 是否存在重复代码（卡片、按钮、列表等模式），可以抽成复用组件。
   - 类型是否清晰（尽量避免 `any`），关键数据结构是否有统一的接口/类型定义。

2. **布局、样式与一致性**
   - 是否复用统一的布局组件（主布局、页面头部、侧边栏等）。
   - Tailwind 类名是否过度堆叠、包含大量魔法色值（如随意使用类似但不一致的灰色/紫色）。
   - 是否存在同一业务模块内风格不统一的问题（按钮样式、圆角、间距等）。

3. **状态与数据**
   - 异步请求是否有完整的 loading / error / empty 状态反馈。
   - 状态是否放在合适的层级（避免过度提升或不必要的全局状态）。
   - 是否存在可以用派生值计算的状态被重复存储的问题。

4. **性能与用户体验**
   - 是否有不必要的重新渲染（例如在 `.map` 中频繁创建匿名函数或对象、缺少 key 或 key 不稳定）。
   - 大列表/复杂视图是否考虑了懒加载、分页或虚拟列表。
   - 交互是否有明确反馈（按钮禁用/加载中的样式、错误提示等）。

## Required Output

当调用本 skill 时，输出**必须**严格遵循下列两种模板之一。

### Template A（存在问题或改进建议时）

```
# Code review
Found <N> urgent issues need to be fixed:

## 1 <brief description of bug>
FilePath: <path> line <line>
<relevant code snippet or pointer>


### Suggested fix
<brief description of suggested fix>

---
... (repeat for each urgent issue) ...

Found <M> suggestions for improvement:

## 1 <brief description of suggestion>
FilePath: <path> line <line>
<relevant code snippet or pointer>


### Suggested fix
<brief description of suggested fix>

---

... (repeat for each suggestion) ...
```

要求：

- 若没有「紧急问题」，可以省略 `urgent issues` 段落。
- 若没有「建议」，可以省略 `suggestions for improvement` 段落。
- 若问题数量超过 10 条，可汇总为 "10+ urgent issues" / "10+ suggestions"，并仅输出前 10 条。
- 保持模板中的空行与分隔线格式，以便后续自动解析。
- 若使用 Template A，且至少有一条需要改代码的项，最后追加一句简短追问，例如：
  - `Would you like me to use the Suggested fix section to address these issues?`

### Template B（未发现问题时）

```
## Code review
No issues found.
```

