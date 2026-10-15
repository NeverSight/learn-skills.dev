---
name: use-url-state
description: 指导使用 @yss-ui/hooks 的 useUrlState 管理当前路由 URL query 的读取、合并写入、按 key 清理和清空；覆盖 history 无感更新、replace/push、router 策略和分享链接恢复，不把 vue-router query 手写拼接或当成完整状态库。
---

# useUrlState 使用

## 触发条件

- 需要把筛选条件、Tab、关键字同步到地址栏 URL query，或从分享链接恢复这些参数。
- 需要 `useUrlState` 的 `setState`、`clearKeys`、`clearState`，或在 `history` / `router`、`replace` / `push` 之间选择。

## 不适用场景

- 只要标准列表查询重置、远程分页、YTable 工具栏，不涉及地址栏：使用 `../page-list-module/SKILL.md`。
- 跨页面全局状态、Pinia/provide 共享数据，而不是当前路由 query。
- 需要改 path/hash 或跳到另一条路由。本 Hook 只动当前 query。

## 实施流程

1. 当前会话可用 yss-ui MCP 时，先用 `get_component_docs` 查询 `useUrlState`；需要示例再 `get_demo`。
2. MCP 不可用或无结果时读取最新 `llms-full.txt`；仍不一致则以 `packages/hooks/src/useUrlState` 为准。
3. 默认 `history + replace` 无感写 URL。需要路由守卫/导航语义时再 `strategy: 'router'`；需要浏览器回退栈时再 `mode: 'push'`。
4. 用 `state` 读字符串视图，用 `setState` 合并补丁；重置用 `clearKeys` 或 `clearState`。

## 硬约束（禁止/必须）

- 从 `@yss-ui/hooks` 导入 `useUrlState`。真实签名：`useUrlState(options?)`，返回 `{ state, setState, clearKeys, clearState }`。
- 默认 `mode: 'replace'`、`strategy: 'history'`。`history` 走 `pushState/replaceState`，不触发 vue-router 导航重建；无 router 注入时也能工作。SSR/无 `window` 时会把 `history` 降为 `router`。
- `state` 是 `ComputedRef<Record<string, string>>`。重复 query key 取最后一个。`setState` 会把值 `String(...)`；读的时候不要当成 number/boolean 原样回来。
- `setState(patch)` 合并写入。`null`、`undefined`、`''` 会**删除**该 key，不是写成空字符串。
- `clearKeys(['a', 'b'])` 只删列出的 key；`clearState()` 清空当前路由全部 query。列表“重置”优先 `clearState({ mode: 'replace' })`，不要误删 path。
- 只改当前 `path + hash` 上的 query。禁止用它替换 `router.push({ path: '/other' })`。
- 需要触发守卫、滚动行为或依赖 `onBeforeRouteUpdate` 时传 `strategy: 'router'`；默认 `history` 不会走这些导航语义。
- 单次调用可覆盖 `mode`/`strategy`：`setState(patch, { mode: 'push', strategy: 'router' })`。
- 不要手写 `URLSearchParams` + `history.replaceState` 并行操作同一套 query，避免和 Hook 内部状态分叉。

## 标准代码骨架

```vue
<script setup lang="ts">
import { computed } from 'vue';
import { useUrlState } from '@yss-ui/hooks';

const { state, setState, clearKeys, clearState } = useUrlState();

const keyword = computed(() => state.value.keyword || '');
const tab = computed(() => state.value.tab || 'all');

/** 合并写入；空字符串会删除 key。 */
const handleKeywordChange = async (value: string) => {
  await setState({ keyword: value });
};

const handleTabChange = async (value: string) => {
  await setState({ tab: value });
};

const handleClearKeyword = async () => {
  await clearKeys(['keyword']);
};

const handleReset = async () => {
  await clearState({ mode: 'replace' });
};
</script>

<template>
  <div>
    <span>{{ keyword }} / {{ tab }}</span>
  </div>
</template>
```

需要回退栈时：`useUrlState({ mode: 'push' })`。需要 vue-router 导航语义时：`useUrlState({ strategy: 'router' })`。

## 交付检查清单

- [ ] 导入和返回值与真实签名一致，没有臆造 `getQuery`/`removeQuery`。
- [ ] 业务按字符串消费 `state`；空值删除 key 的行为符合预期。
- [ ] 重置用 `clearKeys`/`clearState`，没有改 path/hash。
- [ ] `history`/`router`、`replace`/`push` 的选择与是否需要守卫、回退栈一致。

## 失败兜底策略

- URL 变了但页面没反应：`history` 不走路由导航；依赖守卫时改 `strategy: 'router'`。
- 数字/布尔写进去读出来不对：先 `String` 再自己 parse，不要假设 Hook 保类型。
- 想清空某个筛选却变成 `?keyword=`：传 `'' | null | undefined` 让它删 key，不要写空字符串占位（空字符串同样删除；若看到残留，检查是否走了别的手写 query 代码）。
- 与 `router.replace({ query })` 抢状态：统一只通过 `useUrlState` 写 query。
