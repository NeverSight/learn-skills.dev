---
name: perf-analyzer
description: 前端性能分析助手。分析组件渲染性能、Bundle 大小、网络请求效率，给出优化建议。适用于：(1) 页面加载慢排查，(2) 组件重渲染优化，(3) Bundle 体积优化，(4) 运行时性能瓶颈定位。
---

# 前端性能分析助手

分析性能问题并给出具体优化方案。

## 分析维度

### 1. 渲染性能

**自动检查项**：

| 检查项 | 检测方式 | 优化方案 |
|--------|---------|---------|
| 不必要的重渲染 | 搜索未 memo 化的组件、不稳定的 props 引用 | React.memo / useMemo / useCallback |
| 大列表无虚拟化 | 搜索 `.map()` 渲染超过 50 个元素 | react-virtualized / vue-virtual-scroller |
| 昂贵的计算 | 搜索 render/setup 中的复杂计算 | useMemo / computed |
| 状态更新过于频繁 | 搜索 setState/ref 在 scroll/resize 等高频事件中的调用 | 防抖/节流 |
| Context 滥用 | React: 检查 Context value 是否每次都是新引用 | 拆分 Context 或 useMemo value |

### 2. Bundle 分析

**自动检查项**：

| 检查项 | 检测方式 | 优化方案 |
|--------|---------|---------|
| 大型依赖全量导入 | `import lodash` vs `import { debounce } from 'lodash-es'` | 按需导入 / 替换为轻量替代 |
| 未使用的依赖 | package.json 中有但代码中未引用 | 移除 |
| 未代码分割 | 路由组件是否使用 lazy/defineAsyncComponent | 动态导入 |
| 重复依赖 | 检查 lock 文件中的版本重复 | 统一版本 |
| 图片资源未优化 | 搜索 .png/.jpg 直接引用 | WebP 格式 + 压缩 |

### 3. 网络请求

**自动检查项**：

| 检查项 | 检测方式 | 优化方案 |
|--------|---------|---------|
| 请求瀑布流 | 串行的 await API 调用 | Promise.all 并行 |
| 缺少缓存 | 相同 API 多次调用 | SWR / React Query / 手动缓存 |
| 缺少请求取消 | 组件卸载未取消进行中的请求 | AbortController |
| 未处理竞态 | 快速切换导致旧请求覆盖新数据 | 竞态保护 |

### 4. 内存泄漏

**自动检查项**：

| 检查项 | 检测方式 | 优化方案 |
|--------|---------|---------|
| 事件监听未移除 | addEventListener 无对应 removeEventListener | cleanup 函数 |
| 定时器未清理 | setInterval/setTimeout 无对应 clear | cleanup 函数 |
| 闭包持有大对象 | 事件回调/定时器中引用 state 或大数据 | WeakRef 或解绑 |

## 工作流程

1. **读取项目配置**：package.json、构建配置
2. **按维度扫描**：根据用户描述的问题选择扫描维度
3. **输出报告**：

```markdown
## 性能分析报告

### 概要
- 发现 N 个性能问题
- 预计优化后 [加载时间/渲染次数/bundle大小] 改善 XX%

### 🔴 高优先级
#### [问题描述]
- **位置**: `file.tsx` L42
- **影响**: [具体影响]
- **优化方案**: [具体方案 + 代码示例]

### 🟡 中优先级
...

### 🟢 低优先级
...
```

## 常用优化速查

详细的优化模式和代码示例，在分析时根据具体问题按需提供。

### React 优化关键词
- `React.memo`、`useMemo`、`useCallback` — 减少重渲染
- `React.lazy` + `Suspense` — 代码分割
- `useTransition` / `useDeferredValue` — 优先级调度

### Vue 3 优化关键词
- `v-once` / `v-memo` — 减少重渲染
- `defineAsyncComponent` — 代码分割
- `shallowRef` / `shallowReactive` — 减少深层响应式追踪
- `<KeepAlive>` — 缓存组件实例
