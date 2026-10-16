---
name: frontend-ui-engineering
description: 构建生产级、可访问、响应式的面向用户 UI。当构建或修改界面和页面、创建组件、实现布局、满足 WCAG 可访问性要求、管理状态，或输出需要看起来和感觉上都是生产级而不是 AI 生成时使用。
---

# 前端 UI 工程

## 概述

构建可访问、高性能、视觉打磨到位的生产级用户界面。目标是让 UI 看起来像由顶级公司里有设计意识的工程师构建的，而不是 AI 生成的。这意味着真正遵循设计系统、正确的可访问性、周到的交互模式，以及没有那种泛泛的 "AI aesthetic"。

## 何时使用

- 构建新的 UI 组件或页面
- 修改现有面向用户的界面
- 实现响应式布局
- 添加交互或状态管理
- 修复视觉或 UX 问题

## 组件架构

### 文件结构

把所有与组件相关的东西放在一起（colocate）：

```
src/components/
  TaskList/
    TaskList.tsx          # Component implementation
    TaskList.test.tsx     # Tests
    TaskList.stories.tsx  # Storybook stories (if using)
    use-task-list.ts      # Custom hook (if complex state)
    types.ts              # Component-specific types (if needed)
```

### 组件模式

**优先组合而非配置：**

```tsx
// Good: Composable
<Card>
  <CardHeader>
    <CardTitle>Tasks</CardTitle>
  </CardHeader>
  <CardBody>
    <TaskList tasks={tasks} />
  </CardBody>
</Card>

// Avoid: Over-configured
<Card
  title="Tasks"
  headerVariant="large"
  bodyPadding="md"
  content={<TaskList tasks={tasks} />}
/>
```

**保持组件职责聚焦：**

```tsx
// Good: Does one thing
export function TaskItem({ task, onToggle, onDelete }: TaskItemProps) {
  return (
    <li className="flex items-center gap-3 p-3">
      <Checkbox checked={task.done} onChange={() => onToggle(task.id)} />
      <span className={task.done ? 'line-through text-muted' : ''}>{task.title}</span>
      <Button variant="ghost" size="sm" onClick={() => onDelete(task.id)}>
        <TrashIcon />
      </Button>
    </li>
  );
}
```

**数据获取与展示分离：**

```tsx
// Container: handles data
export function TaskListContainer() {
  const { tasks, isLoading, error } = useTasks();

  if (isLoading) return <TaskListSkeleton />;
  if (error) return <ErrorState message="Failed to load tasks" retry={refetch} />;
  if (tasks.length === 0) return <EmptyState message="No tasks yet" />;

  return <TaskList tasks={tasks} />;
}

// Presentation: handles rendering
export function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <ul role="list" className="divide-y">
      {tasks.map(task => <TaskItem key={task.id} task={task} />)}
    </ul>
  );
}
```

## 状态管理

**选择能工作的最简单方案：**

```
Local state (useState)           → Component-specific UI state
Lifted state                     → Shared between 2-3 sibling components
Context                          → Theme, auth, locale (read-heavy, write-rare)
URL state (searchParams)         → Filters, pagination, shareable UI state
Server state (React Query, SWR)  → Remote data with caching
Global store (Zustand, Redux)    → Complex client state shared app-wide
```

**不要让 props 穿透超过 3 层。** 如果你在不使用这些 props 的组件之间层层传递，就引入 context 或重构组件树。

## 遵循设计系统

### 避开 AI 审美

AI 生成的 UI 有可辨识的套路。把它们全部避开：

| AI 默认做法 | 为什么是问题 | 生产级水准 |
|---|---|---|
| 满屏紫色/靛蓝 | 模型默认选用视觉上"安全"的配色，让每个 app 看起来都一样 | 使用项目实际的调色板 |
| 滥用渐变 | 渐变增加视觉噪音，且与多数设计系统冲突 | 与设计系统匹配的扁平或克制的渐变 |
| 万物圆角（rounded-2xl） | 最大圆角传达"友好"，但无视了真实设计中圆角半径的层级 | 遵循设计系统中一致的 border-radius |
| 千篇一律的 hero 区块 | 模板驱动的布局，与实际内容和用户需求毫无关联 | 内容优先的布局 |
| Lorem ipsum 式文案 | 占位文本掩盖了真实内容才会暴露的布局问题（长度、换行、溢出） | 贴近真实的占位内容 |
| 到处都是过大的 padding | 均等的宽松 padding 会摧毁视觉层级并浪费屏幕空间 | 一致的间距刻度 |
| 库存式的卡片网格 | 均质网格是布局上的捷径，无视信息优先级和扫描模式 | 目标驱动的布局 |
| 重阴影设计 | 层层阴影增加的深度会与内容争抢注意力，并拖慢低端设备渲染 | 除非设计系统明确规定，否则用克制或无阴影 |

### 间距与布局

使用一致的间距刻度，不要凭空发明数值：

```css
/* Use the scale: 0.25rem increments (or whatever the project uses) */
/* Good */  padding: 1rem;      /* 16px */
/* Good */  gap: 0.75rem;       /* 12px */
/* Bad */   padding: 13px;      /* Not on any scale */
/* Bad */   margin-top: 2.3rem; /* Not on any scale */
```

### 排版

尊重标题层级：

```
h1 → Page title (one per page)
h2 → Section title
h3 → Subsection title
body → Default text
small → Secondary/helper text
```

不要跳过标题层级。不要给非标题内容使用标题样式。

### 颜色

- 使用语义化颜色 token：`text-primary`、`bg-surface`、`border-default`，而不是原始 hex 值
- 确保足够对比度（正文 4.5:1，大字号文本 3:1）
- 不要只靠颜色传达信息（同时使用图标、文本或图案）

## 可访问性（WCAG 2.1 AA）

每个组件都必须达到这些标准：

### 键盘导航

```tsx
// Every interactive element must be keyboard accessible
<button onClick={handleClick}>Click me</button>        // ✓ Focusable by default
<div onClick={handleClick}>Click me</div>               // ✗ Not focusable
<div role="button" tabIndex={0} onClick={handleClick}    // ✓ But prefer <button>
     onKeyDown={e => {
       if (e.key === 'Enter') handleClick();
       if (e.key === ' ') e.preventDefault();
     }}
     onKeyUp={e => {
       if (e.key === ' ') handleClick();
     }}>
  Click me
</div>
```

### ARIA 标签

```tsx
// Label interactive elements that lack visible text
<button aria-label="Close dialog"><XIcon /></button>

// Label form inputs
<label htmlFor="email">Email</label>
<input id="email" type="email" />

// Or use aria-label when no visible label exists
<input aria-label="Search tasks" type="search" />
```

### 焦点管理

```tsx
// Move focus when content changes
function Dialog({ isOpen, onClose }: DialogProps) {
  const closeRef = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (isOpen) closeRef.current?.focus();
  }, [isOpen]);

  // Trap focus inside dialog when open
  return (
    <dialog open={isOpen}>
      <button ref={closeRef} onClick={onClose}>Close</button>
      {/* dialog content */}
    </dialog>
  );
}
```

### 有意义的空状态和错误状态

```tsx
// Don't show blank screens
function TaskList({ tasks }: { tasks: Task[] }) {
  if (tasks.length === 0) {
    return (
      <div role="status" className="text-center py-12">
        <TasksEmptyIcon className="mx-auto h-12 w-12 text-muted" />
        <h3 className="mt-2 text-sm font-medium">No tasks</h3>
        <p className="mt-1 text-sm text-muted">Get started by creating a new task.</p>
        <Button className="mt-4" onClick={onCreateTask}>Create Task</Button>
      </div>
    );
  }

  return <ul role="list">...</ul>;
}
```

## 响应式设计

移动优先设计，再向大屏扩展：

```tsx
// Tailwind: mobile-first responsive
<div className="
  grid grid-cols-1      /* Mobile: single column */
  sm:grid-cols-2        /* Small: 2 columns */
  lg:grid-cols-3        /* Large: 3 columns */
  gap-4
">
```

在这些断点测试：320px、768px、1024px、1440px。

## 加载与过渡

```tsx
// Skeleton loading (not spinners for content)
function TaskListSkeleton() {
  return (
    <div className="space-y-3" aria-busy="true" aria-label="Loading tasks">
      {Array.from({ length: 3 }).map((_, i) => (
        <div key={i} className="h-12 bg-muted animate-pulse rounded" />
      ))}
    </div>
  );
}

// Optimistic updates for perceived speed
function useToggleTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: toggleTask,
    onMutate: async (taskId) => {
      await queryClient.cancelQueries({ queryKey: ['tasks'] });
      const previous = queryClient.getQueryData(['tasks']);

      queryClient.setQueryData(['tasks'], (old: Task[]) =>
        old.map(t => t.id === taskId ? { ...t, done: !t.done } : t)
      );

      return { previous };
    },
    onError: (_err, _taskId, context) => {
      queryClient.setQueryData(['tasks'], context?.previous);
    },
  });
}
```

## 另见

详细的可访问性要求和测试工具见 `../../references/accessibility-checklist.md`。

## 常见合理化借口

| 借口 | 现实 |
|---|---|
| "可访问性是锦上添花" | 在许多司法辖区它是法律要求，也是工程质量标准。 |
| "我们以后再做成响应式的" | 事后补响应式设计的难度是从一开始就做好的 3 倍。 |
| "设计还没定稿，先跳过样式" | 使用设计系统的默认值。无样式的 UI 会给审阅者留下破碎的第一印象。 |
| "这只是个原型" | 原型会变成生产代码。把地基打对。 |
| "AI 审美暂时没问题" | 它传递的是低质量信号。从一开始就使用项目真正的设计系统。 |

## 危险信号

- 超过 200 行的组件（拆分它们）
- 内联样式或任意的像素值
- 缺少错误状态、加载状态或空状态
- 没有做键盘导航测试
- 把颜色作为状态的唯一指示（红/绿，没有文本或图标）
- 泛泛的 "AI look"（紫色渐变、过大的卡片、库存式布局）

## 验证

构建完 UI 后：

- [ ] 组件渲染时 console 无报错
- [ ] 所有可交互元素都支持键盘访问（用 Tab 键遍历页面）
- [ ] 屏幕阅读器能传达页面的内容和结构
- [ ] 响应式：在 320px、768px、1024px、1440px 均正常
- [ ] 加载、错误和空状态全部处理
- [ ] 遵循项目的设计系统（间距、颜色、排版）
- [ ] dev tools 或 axe-core 中没有可访问性告警
