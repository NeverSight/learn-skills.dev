---
name: create-docs
description: 使用 Movk Nuxt Docs 创建和编写文档站点。提供 MDC 组件用法、内容结构、配置指南和写作规范。
---

# Movk Nuxt Docs - 文档编写指南

使用 Movk Nuxt Docs 创建文档站点时，遵循本指南以确保内容结构规范、组件使用正确。

## 项目概述

Movk Nuxt Docs 是基于 Nuxt 4 的文档主题，采用 Layer 架构。核心技术栈：

- **Nuxt 4** + **Nuxt Content** - 框架和内容管理
- **Nuxt UI** - 组件库（Prose 组件用于 Markdown）
- **Tailwind CSS 4** - 样式系统
- **MDC 语法** - Markdown 中使用 Vue 组件

## 参考文档

根据当前任务按需加载，不要一次全部加载：

| 文件 | 内容 | 何时加载 |
|------|------|----------|
| `references/mdc-components.md` | MDC 组件用法和模板 | 编写 Markdown 内容时 |
| `references/configuration.md` | nuxt.config.ts 和 app.config.ts 配置 | 配置项目时 |
| `references/writing-guide.md` | 内容结构和写作规范 | 创建新页面或组织内容时 |

## 工作流程

### 第 1 步：分析项目

检查现有项目结构：

```bash
# 检查是否已安装 Movk Nuxt Docs
cat package.json | grep "@movk/nuxt-docs"

# 检查内容目录
ls content/
ls content/docs/
```

如果是新项目，使用模板创建：

```bash
# 完整模板（推荐）
npx nuxi init -t gh:mhaibaraai/movk-nuxt-docs/templates/default my-docs

# 模块文档模板（精简）
npx nuxi init -t gh:mhaibaraai/movk-nuxt-docs/templates/module my-module-docs
```

### 第 2 步：理解目录结构

标准项目结构：

```
my-docs/
├── app/
│   ├── app.config.ts            # 应用配置（主题、Header、Footer 等）
│   ├── components/              # 自定义组件（覆盖 Layer 默认组件）
│   └── composables/             # 自定义 Composables
├── content/
│   ├── index.md                 # 首页
│   ├── releases.yml             # 发布日志（可选，自动检测）
│   └── docs/                    # 文档页面
│       ├── 1.getting-started/
│       │   ├── 1.index.md
│       │   └── 2.installation.md
│       ├── 2.guide/
│       │   └── 1.usage.md
│       └── 3.api/
│           └── 1.reference.md
├── public/                      # 静态资源
├── nuxt.config.ts               # Nuxt 配置
└── package.json
```

**文件命名规则：**
- 需要控制排序时使用数字前缀：`1.index.md`、`2.installation.md`
- 无需排序的文件直接命名：`troubleshooting.md`、`ai-chat.md`
- 目录同理：需要排序用 `1.getting-started/`，否则直接命名
- 数字前缀不会出现在 URL 中

### 第 3 步：编写内容

加载 `references/mdc-components.md` 了解可用组件。

每个 Markdown 文件需要 Front-Matter：

```md
---
title: 页面标题
description: 页面描述，用于 SEO 和搜索。
---

## 第一个章节

正文内容...
```

**可选 Front-Matter 字段：**

| 字段 | 说明 |
|------|------|
| `title` | 页面标题 |
| `description` | 页面描述 |
| `navigation.title` | 导航中显示的标题（可与 title 不同） |
| `navigation.icon` | 导航图标（如 `i-lucide-book`） |
| `category` | 页面分类 |
| `seo.title` | SEO 标题（覆盖 title） |
| `seo.description` | SEO 描述（覆盖 description） |

### 第 4 步：配置项目

加载 `references/configuration.md` 了解详细配置选项。

基础 `nuxt.config.ts`：

```ts
export default defineNuxtConfig({
  extends: ['@movk/nuxt-docs'],

  // AI 聊天（可选）
  aiChat: {
    model: 'openai/gpt-5-nano',
    models: ['openai/gpt-5-nano'],
  },

  // MCP Server（可选）
  mcp: {
    name: 'My Docs'
  }
})
```

### 第 5 步：验证和预览

```bash
# 启动开发服务器
pnpm dev

# 构建检查
pnpm build
```

## 核心功能

### AI 聊天助手

内置 AI 聊天，支持多模型。在 `nuxt.config.ts` 配置 `aiChat` 选项。

### MCP Server

自动暴露文档为 MCP 工具，供 AI 助手查阅：
- `list-pages` - 列出所有页面
- `get-page` - 获取页面内容
- `list-examples` - 列出组件示例
- `get-example` - 获取组件示例

### LLM 优化

自动生成 `llms.txt` 和 `llms-full.txt`，优化 AI 对文档的理解。

### 组件文档自动生成

使用 `nuxt-component-meta` 自动提取 Vue 组件的 Props、Slots、Emits 信息。

### GitHub 集成

自动检测 Git 仓库信息，提供：
- 页面「在 GitHub 上编辑」链接
- 提交历史展示
- 最后更新时间

## 检查清单

创建文档页面时确认：

- [ ] Front-Matter 包含 `title` 和 `description`
- [ ] 标题层级从 `##` 开始（`#` 由系统渲染 title）
- [ ] MDC 组件语法正确（冒号数量匹配嵌套层级）
- [ ] 代码块标注了语言标识符和文件名
- [ ] 中英文之间有空格
- [ ] 使用中文全角标点
- [ ] 图片放在 `public/` 目录

配置项目时确认：

- [ ] `nuxt.config.ts` 包含 `extends: ['@movk/nuxt-docs']`
- [ ] 依赖包含 `@movk/nuxt-docs`、`better-sqlite3`、`tailwindcss`
- [ ] 需要排序的内容文件和目录使用数字前缀，无需排序的直接命名
