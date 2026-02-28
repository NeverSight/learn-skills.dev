---
name: smart-debugger
description: 前端智能调试助手。从错误信息、控制台日志、异常行为描述快速定位问题代码并给出修复建议。适用于：(1) 运行时错误（TypeError、ReferenceError 等），(2) 控制台警告分析，(3) 页面白屏/卡顿排查，(4) 网络请求异常，(5) 组件渲染异常。与 BugHunter 区别：smart-debugger 聚焦快速定位，BugHunter 做完整闭环修复。
---

# 智能调试助手

从错误信息快速定位问题根因，给出修复建议。

## 输入方式

接受以下任一形式：
- 错误信息文本（如 `TypeError: Cannot read properties of undefined`）
- 控制台日志片段
- 异常行为描述（如"组件反复渲染，页面卡顿"）
- 指定文件路径 + 问题描述

## 调试流程

### 1. 错误分类

根据输入信息归类：

| 类别 | 信号 | 优先排查 |
|------|------|---------|
| **运行时类型错误** | TypeError, ReferenceError | 变量未定义、属性访问链、类型断言 |
| **渲染异常** | 白屏、组件不显示、闪烁 | 条件渲染逻辑、数据初始状态、Suspense/ErrorBoundary |
| **性能问题** | 卡顿、频繁重渲染 | useEffect 依赖、状态更新循环、大列表未虚拟化 |
| **网络请求** | 4xx/5xx、CORS、超时 | API 地址、请求头、代理配置 |
| **样式异常** | 布局错乱、样式不生效 | CSS 优先级、动态 class、主题覆盖 |
| **构建错误** | 编译失败、类型错误 | 导入路径、类型定义、tsconfig |
| **控制台警告** | React/Vue 警告 | Key 重复、PropTypes、响应式丢失 |

### 2. 上下文收集

根据分类，自动执行对应的上下文收集：

**通用步骤**（所有类别都执行）：
1. 读取 `package.json` 识别技术栈和框架版本
2. 如果提供了文件路径，读取相关文件

**按类别额外收集**：

| 类别 | 自动收集 |
|------|---------|
| 运行时错误 | 从堆栈信息定位源文件 → 读取文件 → 检查上下文 |
| 渲染异常 | 检查组件 props/state 定义 → 数据流追踪 |
| 性能问题 | 搜索 useEffect/watch 使用 → 检查依赖数组 |
| 网络请求 | 检查 API 配置、代理配置、环境变量 |
| 构建错误 | 检查 tsconfig.json、webpack/vite 配置 |

### 3. 模式匹配

将错误信息与常见前端错误模式进行匹配，快速给出方向。

#### 高频错误速查

**TypeError: Cannot read properties of undefined (reading 'xxx')**
- 排查：可选链缺失 `obj?.prop`、API 返回结构变化、异步数据初始状态为 undefined
- 修复：添加空值保护、设置默认值、检查数据流

**TypeError: xxx is not a function**
- 排查：导入错误（default vs named export）、版本升级 API 变更、异步加载未完成
- 修复：检查 import 语句、查阅库的 changelog

**Maximum update depth exceeded / Too many re-renders**
- 排查：useEffect 依赖数组缺失/错误、setState 在 render 中调用、对象/数组引用不稳定
- 修复：修正依赖数组、使用 useMemo/useCallback 稳定引用

**Cannot update a component while rendering another**
- 排查：在渲染阶段调用了 setState（来自子组件的回调、context 更新）
- 修复：将更新移至 useEffect 或事件处理函数中

**Objects are not valid as a React child**
- 排查：渲染了原始对象 `{obj}`、日期对象未转字符串、Promise 未解析
- 修复：JSON.stringify 或提取具体字段

**Vue: [Warn] Invalid prop type / Missing required prop**
- 排查：PropTypes 定义与传入不匹配、组件 API 变更
- 修复：检查组件文档、修正 prop 传入

**Vue: [Warn] Avoid using non-primitive value as key**
- 排查：v-for 的 key 使用了对象而非原始值
- 修复：使用唯一 ID 字段作为 key

### 4. 输出格式

```markdown
## 🔍 诊断结果

**错误类型**：[分类]
**根因**：[一句话说明]

### 问题定位
- 文件：`path/to/file.tsx`
- 行号：约 L42（基于堆栈 / 代码分析）
- 代码片段：
  ```tsx
  // 问题代码
  ```

### 修复建议
```tsx
// 修复后的代码
```

### 预防措施
- [如何避免同类问题]
```

## 与 BugHunter 的分工

| 场景 | 使用工具 |
|------|---------|
| 拿到一个错误信息，想快速定位修复 | **smart-debugger**（本 skill） |
| 收到 Redmine Bug 工单，需要完整修复闭环 | **BugHunter**（subagent） |
| 难以定位的复杂 Bug，需要深度分析 | 先用 smart-debugger 初诊 → 转 BugHunter |
