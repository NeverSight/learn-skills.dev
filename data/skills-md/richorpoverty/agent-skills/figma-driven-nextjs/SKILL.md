---
name: "figma-driven-nextjs"
description: "Figma设计驱动的Next.js开发技能。当用户提到'根据Figma'、'按照设计稿'、提供Figma链接或MCP数据时自动触发。"
---

# Figma-Driven Next.js 开发技能

基于 Figma 设计驱动的 Next.js 开发技能，结合 `vercel-react-best-practices` 和 `web-design-guidelines` 技能，以 Figma 设计文件为核心设计来源。

---

## 技术栈

| 类别 | 技术选型 |
|------|----------|
| **前端框架** | Next.js (App Router) |
| **后端服务** | Supabase |
| **样式方案** | Tailwind CSS |
| **图标库** | Lucide (https://lucide.dev/) |
| **动画库** | Motion (https://motion.dev/) |
| **工作流** | Figma MCP → Trae IDE |

---

## 核心原则

### Figma 优先
所有设计决策以 Figma 文件为准，`vercel-react-best-practices` 和 `web-design-guidelines` 作为代码质量和最佳实践的补充指导。

---

## 设计令牌系统

### 1. 颜色规范

**来源**: 严格遵循 Figma 文件中的颜色定义

**实现**: 创建统一的颜色令牌文件 `/styles/tokens/colors.ts`

**Dark 模式**:
- 自动推导 Dark 模式颜色（基于 Figma 原始颜色智能生成）
- 遵循 WCAG 对比度标准
- 仅支持 Light/Dark 双主题，不支持多主题

**颜色令牌结构**:
```typescript
// /styles/tokens/colors.ts
export const colors = {
  light: {
    primary: '#从Figma提取',
    secondary: '#从Figma提取',
    background: '#从Figma提取',
    foreground: '#从Figma提取',
    // ... 其他颜色
  },
  dark: {
    primary: '#自动推导',
    secondary: '#自动推导',
    background: '#自动推导',
    foreground: '#自动推导',
    // ... 自动生成
  }
}
```

**Dark 模式推导规则**:
- 背景色：降低亮度，保持色相
- 前景色：提高亮度，确保对比度 ≥ 4.5:1
- 强调色：微调亮度，保持品牌识别度
- 边框色：降低饱和度和亮度

### 2. 字体规范

**来源**: 使用 Figma 文件中的字体规范

**实现**: 创建字体令牌文件 `/styles/tokens/typography.ts`

**包含**: 字体族、字号、字重、行高、字间距

```typescript
// /styles/tokens/typography.ts
export const typography = {
  fontFamily: {
    sans: '从Figma提取',
    serif: '从Figma提取',
    mono: '从Figma提取',
  },
  fontSize: {
    xs: '从Figma提取',
    sm: '从Figma提取',
    base: '从Figma提取',
    lg: '从Figma提取',
    xl: '从Figma提取',
    '2xl': '从Figma提取',
    // ... 其他尺寸
  },
  fontWeight: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  lineHeight: {
    tight: '从Figma提取',
    normal: '从Figma提取',
    relaxed: '从Figma提取',
  },
  letterSpacing: {
    tight: '从Figma提取',
    normal: '从Figma提取',
    wide: '从Figma提取',
  },
}
```

### 3. 间距规范

**来源**: 遵循 Figma 文件中的间距定义

**实现**: 创建间距令牌文件 `/styles/tokens/spacing.ts`

**优化**: 可进行合理优化，但需明确告知用户优化了什么及原因

```typescript
// /styles/tokens/spacing.ts
export const spacing = {
  0: '0',
  1: '从Figma提取', // 如 4px
  2: '从Figma提取', // 如 8px
  3: '从Figma提取', // 如 12px
  4: '从Figma提取', // 如 16px
  // ... 其他间距
}
```

### 4. 阴影规范

**来源**: 从 Figma 提取阴影效果

**实现**: 创建阴影令牌文件 `/styles/tokens/shadows.ts`

```typescript
// /styles/tokens/shadows.ts
export const shadows = {
  sm: '从Figma提取',
  md: '从Figma提取',
  lg: '从Figma提取',
  xl: '从Figma提取',
}
```

---

## 布局规范

### 原则
响应式布局优先，自适应方法

### 断点策略
- **优先**: 根据 Figma 设计智能推荐断点
- **备选**: 使用行业标准断点（当 Figma 无明确断点时）

| 断点名称 | 最小宽度 | 用途 |
|---------|---------|------|
| `sm` | 640px | 手机横屏 |
| `md` | 768px | 平板竖屏 |
| `lg` | 1024px | 平板横屏/小笔记本 |
| `xl` | 1280px | 桌面显示器 |
| `2xl` | 1536px | 大屏显示器 |

### 自适应方法
- 使用 CSS Grid 和 Flexbox 实现自适应布局
- 使用 `clamp()` 函数实现流体字体和间距
- 使用容器查询（Container Queries）实现组件级响应式
- 使用相对单位（rem、em、vw、vh、%）替代固定像素值

### Figma 智能推荐规则
- 分析 Figma 中的 Auto Layout 设置
- 根据 Figma 组件的约束（Constraints）推断响应式行为
- 根据 Figma 变体（Variants）识别不同断点的设计

---

## 组件库架构

### 原子设计方法论
```
/components
  /atoms          # 原子组件（Button, Input, Icon...）
  /molecules      # 分子组件（SearchBar, Card...）
  /organisms      # 有机体组件（Header, Footer...）
  /templates      # 模板组件
  /pages          # 页面组件
```

### 组件文件结构
```
/components
  /atoms
    /Button
      Button.tsx        # 组件实现
      Button.types.ts   # 类型定义
      index.ts          # 导出
```

### 组件命名映射规则

**要求**: 创建 `/docs/component-mapping.md` 文件

**格式**:
```markdown
| Figma 组件名 | 代码组件名 | 文件路径 |
|-------------|-----------|---------|
| Button/Primary | Button | /components/atoms/Button |
| Button/Secondary | Button | /components/atoms/Button |
| Input/Text | Input | /components/atoms/Input |
```

---

## 图标处理

### 图标来源
1. **Figma 图标**: 从 Figma 导出的自定义图标
2. **Lucide 图标库**: https://lucide.dev/ 作为补充图标库

### 实现规范
- **Figma 图标**: SVG 组件化，存放于 `/components/icons/`
- **Lucide 图标**: 按需导入，Tree-shakable
- **自定义能力**: 支持尺寸、颜色、描边宽度自定义

### 命名规范
- Figma 导出: `Icon[Name].tsx`
- Lucide 使用: 直接导入 `import { IconName } from 'lucide-react'`

### 图标组件接口
```tsx
interface IconProps {
  size?: number
  color?: string
  strokeWidth?: number
  className?: string
}
```

---

## 动画规范

### 动画库
**Motion**: https://motion.dev/ - 生产级动画库

### 性能优化
- 使用 `willChange` 提示浏览器优化
- 优先使用 `transform` 属性
- 避免动画布局属性（width, height, top, left）

### 无障碍
支持 `prefers-reduced-motion` 媒体查询

### 动画类型
- 入场动画（Enter）
- 退出动画（Exit）
- 滚动动画（Scroll）
- 手势动画（Gesture）
- 布局动画（Layout）

### Motion 使用示例
```tsx
import { motion, AnimatePresence } from 'motion/react'

<AnimatePresence>
  {isVisible && (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      style={{ willChange: 'transform, opacity' }}
    />
  )}
</AnimatePresence>
```

---

## 主题切换机制

### 实现方式
- **CSS 变量**: 使用 CSS 自定义属性定义颜色
- **Tailwind Dark 模式**: `darkMode: 'class'` 配置
- **切换方式**: 系统偏好检测 + 手动切换
- **持久化**: localStorage 存储用户偏好

### 主题提供者
```tsx
// /components/ThemeProvider.tsx
'use client'
import { createContext, useContext, useEffect, useState } from 'react'

type Theme = 'light' | 'dark'
type ThemeContextType = {
  theme: Theme
  setTheme: (theme: Theme) => void
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined)

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>('light')
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
    const savedTheme = localStorage.getItem('theme') as Theme | null
    setTheme(savedTheme || (prefersDark ? 'dark' : 'light'))
  }, [])

  useEffect(() => {
    if (mounted) {
      document.documentElement.classList.toggle('dark', theme === 'dark')
      localStorage.setItem('theme', theme)
    }
  }, [theme, mounted])

  if (!mounted) return null

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (!context) throw new Error('useTheme must be used within ThemeProvider')
  return context
}
```

---

## 无障碍规范

遵循 `web-design-guidelines` 技能中的无障碍规则：

| 类别 | 要求 |
|------|------|
| **语义化 HTML** | 使用正确的 HTML 元素 |
| **ARIA 属性** | 必要时添加 aria-label、aria-describedby 等 |
| **键盘导航** | 所有交互元素可通过键盘访问 |
| **焦点管理** | 可见的焦点状态，使用 focus-visible |
| **颜色对比度** | 符合 WCAG AA 标准（4.5:1） |

---

## 图片处理

- **来源**: Figma 中的图片资源
- **实现**: 
  - 使用 Next.js `<Image>` 组件
  - 自动优化和懒加载
  - 响应式图片
  - 提供 alt 文本

---

## 代码风格

| 类别 | 规范 |
|------|------|
| **语言** | TypeScript（强类型定义） |
| **组件文件** | PascalCase（如 `Button.tsx`） |
| **工具函数** | camelCase（如 `formatDate.ts`） |
| **常量** | UPPER_SNAKE_CASE（如 `API_BASE_URL`） |

---

## 工作流程

```
Figma 文件 (MCP)
      ↓
  提取设计令牌
  (颜色、字体、间距、组件)
      ↓
  生成设计系统文件
  (tokens/*.ts)
      ↓
  创建组件映射文件
  (component-mapping.md)
      ↓
  创建基础组件
  (基于 Figma 组件)
      ↓
  应用最佳实践
  (vercel-react-best-practices)
      ↓
  无障碍与 UX 审查
  (web-design-guidelines)
      ↓
  完整页面实现
```

---

## 输出文件清单

每次从 Figma 创建项目时，应输出以下文件：

1. `/styles/tokens/colors.ts` - 颜色令牌（含 Light/Dark）
2. `/styles/tokens/typography.ts` - 字体令牌
3. `/styles/tokens/spacing.ts` - 间距令牌
4. `/styles/tokens/shadows.ts` - 阴影令牌
5. `/styles/tokens/index.ts` - 统一导出
6. `/styles/globals.css` - 全局样式
7. `/docs/component-mapping.md` - 组件命名映射规则
8. `/components/ThemeProvider.tsx` - 主题提供者
9. `/tailwind.config.ts` - Tailwind 配置（含设计令牌）

---

## 触发条件

当以下情况发生时，自动应用此技能：

- 用户请求从 Figma 设计创建页面/组件
- 用户提到 "根据 Figma..." 或 "按照设计稿..."
- 用户提供 Figma 文件链接或 MCP 数据
- 用户请求创建设计令牌

---

## 注意事项

1. **颜色来源**: 所有颜色必须从 Figma 提取，不使用技能内置颜色
2. **间距优化**: 如需优化间距，必须告知用户优化内容和原因
3. **Dark 模式**: 即使 Figma 没有 Dark 模式设计，也必须自动生成
4. **组件映射**: 必须创建组件命名映射文件，保持 Figma 与代码的一致性
5. **无障碍**: 所有组件必须符合 WCAG AA 标准

---

## 安装说明

### 安装命令
```bash
npx skills add https://github.com/Zekiwest/agent-skills --skill figma-driven-nextjs
```

### 重要：安装位置

**技能必须安装到当前工作区根目录下才能生效。**

Trae IDE 只会扫描"当前工作区根目录"下的 `.agents` 文件夹。

#### Monorepo 项目结构

如果你的项目是 Monorepo 结构（如 `project/web/app/page.tsx`），请确保：

1. **确认当前工作区根目录**：IDE 打开的文件夹是哪个？
2. **安装到正确位置**：技能必须安装到工作区根目录

```
# 正确示例：工作区是 web 子项目
project/
├── web/                    # ← 工作区根目录
│   ├── .agents/           # ← 技能安装位置
│   │   └── skills/
│   │       └── figma-driven-nextjs/
│   ├── app/
│   │   └── page.tsx       # ← 你打开的文件
│   └── skills-lock.json   # ← 锁文件
└── other-folder/

# 错误示例：技能装在上一级目录
project/
├── .agents/               # ❌ 错误位置！IDE 扫描不到
│   └── skills/
├── web/                   # ← 工作区根目录
│   ├── app/
│   │   └── page.tsx
│   └── (无 .agents)       # ❌ 这里没有技能
```

#### 验证安装

在项目根目录执行以下命令验证技能是否正确安装：

```bash
# 查看已安装的技能
npx skills list

# 应该能看到 figma-driven-nextjs
```

#### 重新安装到正确位置

如果技能安装位置错误，请在正确的工作区根目录重新执行安装命令：

```bash
cd /path/to/your/workspace/root
npx skills add https://github.com/Zekiwest/agent-skills --skill figma-driven-nextjs
```

### 安装作用域

- **Project（推荐）**: 仅当前项目可用
- **Global**: 所有项目可用（需要管理员权限）

### 依赖技能

此技能依赖以下技能，建议一并安装：

```bash
npx skills add https://github.com/vercel-labs/agent-skills --skill vercel-react-best-practices
npx skills add https://github.com/vercel-labs/agent-skills --skill web-design-guidelines
```
