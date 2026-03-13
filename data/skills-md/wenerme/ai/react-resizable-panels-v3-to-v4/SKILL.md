---
name: react-resizable-panels-v3-to-v4
description: Use when upgrading react-resizable-panels from v3 to v4, fixing v4 type/runtime errors (PanelGroup not exported, direction prop invalid, layout broken), adapting to the new Group/Separator API and percentage string syntax, or updating CSS selectors for renamed data attributes. Triggers on "react-resizable-panels v4", "PanelGroup not found", "PanelResizeHandle not found", "panel layout broken after upgrade".
---

# react-resizable-panels v3 → v4 迁移指南

## 概述

react-resizable-panels v4 是一次重大版本升级。核心变化：组件重命名（ARIA 对齐）、尺寸单位系统重构（数字从百分比变为像素）、移除 `order` prop、移除 `onCollapse`/`onExpand`。本技能覆盖迁移的所有关键路径。

## 迁移步骤总览

### Step 1: 安装

```bash
pnpm add react-resizable-panels@4
# 或
npm install react-resizable-panels@4
```

### Step 2: 组件重命名

| v3 | v4 | 说明 |
|----|-----|------|
| `PanelGroup` | `Group` | 容器组件重命名 |
| `PanelResizeHandle` | `Separator` | 分隔条重命名，对齐 ARIA `separator` role |
| `Panel` | `Panel` | **不变** |

```diff
- import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
+ import { Panel, Group, Separator } from 'react-resizable-panels';

- <PanelGroup direction='horizontal'>
+ <Group orientation='horizontal'>
    <Panel />
-   <PanelResizeHandle />
+   <Separator />
    <Panel />
- </PanelGroup>
+ </Group>
```

### Step 3: 类型重命名

| v3 类型 | v4 类型 | 说明 |
|---------|---------|------|
| `PanelResizeHandleProps` | `SeparatorProps` | 随组件重命名 |
| `PanelOnCollapse` | **已移除** | 用 `onResize` 替代 |
| `PanelOnExpand` | **已移除** | 用 `onResize` 替代 |
| `ImperativePanelGroupHandle` | `GroupImperativeHandle` | 重命名 |
| `ImperativePanelHandle` | `PanelImperativeHandle` | 重命名 |
| (新增) `PanelSize` | `{ asPercentage: number; inPixels: number }` | 新类型 |

```diff
- import type { PanelResizeHandleProps } from 'react-resizable-panels';
+ import type { SeparatorProps } from 'react-resizable-panels';

- import type { PanelOnCollapse, PanelOnExpand } from 'react-resizable-panels';
+ // 已移除，改用 Panel 的 onResize 回调
```

### Step 4: Props 变更

#### Group (原 PanelGroup)

| v3 Prop | v4 Prop | 说明 |
|---------|---------|------|
| `direction` | `orientation` | 重命名，对齐 ARIA 标准 |
| `autoSaveId` | **已移除** | 用 `useDefaultLayout` hook 替代 |
| `ref={groupRef}` | `groupRef={groupRef}` | ref 改为命名 prop |
| `onLayout` | `onLayoutChange` / `onLayoutChanged` | 重命名并拆分 |

```diff
- <PanelGroup direction='horizontal' autoSaveId='my-layout' ref={groupRef}>
+ <Group orientation='horizontal' groupRef={groupRef}>
```

#### Panel

| v3 Prop | v4 Prop | 说明 |
|---------|---------|------|
| `order` | **已移除** | 条件渲染不再需要 order |
| `onCollapse` | **已移除** | 用 `onResize` 替代 |
| `onExpand` | **已移除** | 用 `onResize` 替代 |
| `ref={panelRef}` | `panelRef={panelRef}` | ref 改为命名 prop |

```diff
- <Panel id='left' order={1} onCollapse={handleCollapse} onExpand={handleExpand}>
+ <Panel id='left' onResize={(nextSize, id, prevSize) => {
+   if (prevSize) {
+     const wasCollapsed = prevSize.asPercentage === 0;
+     const isCollapsed = nextSize.asPercentage === 0;
+     if (isCollapsed && !wasCollapsed) handleCollapse();
+     if (!isCollapsed && wasCollapsed) handleExpand();
+   }
+ }}>
```

### Step 5: 尺寸单位转换（关键！）

**v3**: 所有 size 值为数字，隐式表示百分比。
**v4**: 数字表示像素，百分比需要显式字符串。

支持的单位：`px`、`%`、`em`、`rem`、`vh`、`vw`

```diff
- <Panel defaultSize={30} minSize={20} maxSize={60}>
+ <Panel defaultSize='30%' minSize='20%' maxSize='60%'>

- <Panel collapsedSize={5} collapsible>
+ <Panel collapsedSize='5%' collapsible>
```

**警告**: 如果直接升级不改 size 值，所有数字都会从"百分比"变成"像素"，布局会完全错乱！

**快速迁移规则**: 在所有 `defaultSize`、`minSize`、`maxSize`、`collapsedSize` 的数值后加 `%` 并转为字符串。

### Step 6: CSS Data 属性更新

v4 简化了 data 属性体系：

| v3 属性 | v4 属性 | 说明 |
|---------|---------|------|
| `data-panel-group-direction="horizontal"` | `aria-orientation="vertical"` | **语义翻转！** v3=组方向，v4=分隔条方向 |
| `data-panel-group-direction="vertical"` | `aria-orientation="horizontal"` | **语义翻转！** 水平分隔条在垂直组中 |
| `data-resize-handle-state="hover"` | `data-separator="hover"` | 简化 |
| `data-resize-handle-state="drag"` | `data-separator="active"` | `drag` → `active` |
| `data-resize-handle-state="inactive"` | `data-separator="inactive"` | 简化 |
| `data-resize-handle-active` | `data-separator="active"` | 合并 |

**Separator 的 `data-separator` 属性值**: `inactive`、`hover`、`active`、`disabled`

**关键陷阱**: v3 的 `data-panel-group-direction` 是**组的方向**，v4 的 `aria-orientation` 是**分隔条自身的方向**。语义完全翻转！

- 水平组 (`orientation="horizontal"`)：分隔条是**垂直**的 → `aria-orientation="vertical"` → 需要 `width`
- 垂直组 (`orientation="vertical"`)：分隔条是**水平**的 → `aria-orientation="horizontal"` → 需要 `height`

```diff
  /* CSS 选择器更新 — 注意语义翻转！ */
- [data-panel-group-direction="horizontal"] { width: 1px; cursor: col-resize; }
+ [aria-orientation="vertical"] { width: 1px; cursor: col-resize; }

- [data-panel-group-direction="vertical"] { height: 1px; cursor: row-resize; }
+ [aria-orientation="horizontal"] { height: 1px; cursor: row-resize; }

- [data-resize-handle-state="hover"] { ... }
+ [data-separator="hover"] { ... }

- [data-resize-handle-state="drag"] { ... }
+ [data-separator="active"] { ... }

- [data-resize-handle-active] { ... }
+ [data-separator="active"] { ... }

  /* Tailwind / 内联 data 属性 */
- className='data-[resize-handle-state=inactive]:opacity-20'
+ className='data-[separator=inactive]:opacity-20'
```

### Step 7: Hook 变更

```diff
- import { useRef } from 'react';
- const panelRef = useRef<ImperativePanelHandle>(null);
- const groupRef = useRef<ImperativePanelGroupHandle>(null);
+ import { usePanelRef, useGroupRef } from 'react-resizable-panels';
+ const panelRef = usePanelRef();
+ const groupRef = useGroupRef();

  // autoSaveId 替代方案
+ import { useDefaultLayout } from 'react-resizable-panels';
+ const defaultLayout = useDefaultLayout({ groupId: 'my-layout', storage: localStorage });
```

### Step 8: 其他移除

```diff
  // disableGlobalCursorStyles() 全局函数已移除
- import { disableGlobalCursorStyles } from 'react-resizable-panels';
- disableGlobalCursorStyles();
+ // 改为 Group 上的 prop
+ <Group disableCursor orientation='horizontal'>
```

## 常见错误快速定位

| 症状 | 原因 | 修复 |
|------|------|------|
| `PanelGroup is not exported` | 组件重命名 | 替换为 `Group` |
| `PanelResizeHandle is not exported` | 组件重命名 | 替换为 `Separator` |
| `direction is not a valid prop` | prop 重命名 | 替换为 `orientation` |
| 布局完全错乱（面板极小/极大） | 尺寸单位变更 | 数字加 `%` 后缀转字符串 |
| CSS hover/drag 样式失效 | data 属性变更 | 更新 CSS 选择器 |
| `order is not a valid prop` | prop 已移除 | 直接删除 `order` |
| `onCollapse is not a valid prop` | prop 已移除 | 改用 `onResize` |
| `autoSaveId is not a valid prop` | prop 已移除 | 改用 `useDefaultLayout` |
| `PanelResizeHandleProps not found` | 类型重命名 | 替换为 `SeparatorProps` |

## 迁移检查清单

- [ ] 安装 v4: `react-resizable-panels@4`
- [ ] `PanelGroup` → `Group`
- [ ] `PanelResizeHandle` → `Separator`
- [ ] `direction` → `orientation`
- [ ] 所有 size 数值加 `%` 后缀转字符串
- [ ] 移除所有 `order` prop
- [ ] `onCollapse`/`onExpand` → `onResize` 回调
- [ ] `ref` → `panelRef`/`groupRef` 命名 prop
- [ ] `autoSaveId` → `useDefaultLayout` hook
- [ ] 更新 CSS: `data-panel-group-direction` → `aria-orientation`
- [ ] 更新 CSS: `data-resize-handle-state` → `data-separator`
- [ ] 更新类型 import: `PanelResizeHandleProps` → `SeparatorProps`
- [ ] 运行 typecheck 验证
- [ ] 视觉验证布局和拖拽交互

## 完整迁移示例

### Before (v3)

```tsx
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';

function MyLayout() {
  return (
    <PanelGroup direction='horizontal'>
      <Panel defaultSize={30} minSize={10} order={1}>
        <Sidebar />
      </Panel>
      <PanelResizeHandle className='w-1 bg-gray-300 hover:bg-blue-400' />
      <Panel defaultSize={70} minSize={30} order={2}>
        <Content />
      </Panel>
    </PanelGroup>
  );
}
```

### After (v4)

```tsx
import { Panel, Group, Separator } from 'react-resizable-panels';

function MyLayout() {
  return (
    <Group orientation='horizontal'>
      <Panel defaultSize='30%' minSize='10%'>
        <Sidebar />
      </Panel>
      <Separator className='w-1 bg-gray-300 hover:bg-blue-400' />
      <Panel defaultSize='70%' minSize='30%'>
        <Content />
      </Panel>
    </Group>
  );
}
```
