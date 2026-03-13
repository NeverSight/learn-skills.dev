---
name: web-dev
description: Web 开发最佳实践和现代前端技术栈指导
---

# Web 开发技能

## 技术栈

### 前端框架
- **React** - 组件化 UI 库
- **Vue.js** - 渐进式框架
- **Next.js** - React 全栈框架
- **Vite** - 现代构建工具

### 样式
- **Tailwind CSS** - 实用优先的 CSS 框架
- **CSS Modules** - 模块化 CSS
- **styled-components** - CSS-in-JS

### 状态管理
- **Zustand** - 轻量级状态管理
- **Redux Toolkit** - Redux 官方工具集
- **React Query** - 服务端状态管理

## 最佳实践

### 组件设计
1. **单一职责** - 每个组件只做一件事
2. **可复用性** - 提取通用组件
3. **Props 接口** - 明确定义 TypeScript 接口
4. **错误边界** - 处理组件错误

### 性能优化
- 使用 `React.memo` 避免不必要的重渲染
- 懒加载路由和组件
- 图片优化（WebP、懒加载）
- 代码分割

### 代码规范
- ESLint + Prettier
- 统一的命名约定
- 组件文件结构一致
- 注释关键逻辑

## 项目结构

```
src/
├── components/      # 组件
│   ├── common/     # 通用组件
│   └── features/   # 功能组件
├── hooks/          # 自定义 Hooks
├── utils/          # 工具函数
├── services/       # API 服务
├── store/          # 状态管理
└── types/          # TypeScript 类型
```

## 常用命令

```bash
# 创建 React 项目
npm create vite@latest my-app -- --template react-ts

# 创建 Next.js 项目
npx create-next-app@latest

# 安装常用依赖
npm install zustand react-query axios

# 开发服务器
npm run dev

# 构建生产版本
npm run build
```

## 调试技巧

1. **React DevTools** - 检查组件树和 Props
2. **Chrome DevTools** - 性能分析
3. **console.log** - 基础调试
4. **debugger** - 断点调试

## 安全注意事项

- XSS 防护：永远不要使用 `dangerouslySetInnerHTML` 处理用户输入
- CSRF 防护：使用 CSRF token
- 敏感数据：不要在前端存储敏感信息
- 依赖审计：定期运行 `npm audit`
