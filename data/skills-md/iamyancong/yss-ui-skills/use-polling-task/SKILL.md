---
name: use-polling-task
description: 指导使用 @yss-ui/hooks 的 usePollingTask 做页面级静默轮询、任务状态轮询和动态间隔调度；覆盖 start/stop/restart/runNow、pauseWhenHidden、generation/isCurrent、AbortSignal，禁止把它当成请求 loading/data/error Hook 或直接绑定页面主 loading。
---

# usePollingTask 使用

## 触发条件

- 页面需要静默轮询、任务状态轮询、动态切换间隔，或手动查询与轮询并存。
- 需要 `usePollingTask` 的 `start/stop/restart/runNow`、`pauseWhenHidden`、`isCurrent()` 或 `AbortSignal`。

## 不适用场景

- 只要给一次请求包 `loading`：使用 `useLoading`。
- 只要单请求的 `data/error/cache/重试`：用 `vue-hooks-plus/useRequest` 或项目现有请求 Hook，不要用轮询调度顶替。
- 表格高度、树高度问题：使用 `../use-table-height/SKILL.md` 或 `../use-tree-height/SKILL.md`。

## 实施流程

1. 当前会话可用 yss-ui MCP 时，先用 `get_component_docs` 查询 `usePollingTask`；需要启停、动态间隔、错误策略或可见性暂停时再 `get_demo`。
2. MCP 不可用或无结果时读取最新 `llms-full.txt`；仍不一致则以 `packages/hooks/src/usePollingTask` 为准。
3. 把“静默刷新”和“带 loading 的手动查询”拆成两个函数。轮询 task 只更新数据，不打页面主 loading。
4. 在 task 里写入结果前调用 `isCurrent()`；请求库支持时把 `signal` 传下去。

## 硬约束（禁止/必须）

- 从 `@yss-ui/hooks` 导入 `usePollingTask`。真实签名：`usePollingTask(task, options?)`。
- `task` 收到 `{ generation, signal?, isCurrent }`。Hook **不**返回 `data`，也**不**接管业务 loading。
- 返回值只有：`isActive`、`isRunning`、`currentInterval`、`generation`、`start`、`stop`、`restart`、`runNow`、`setInterval`。禁止臆造 `pause`/`resume`/`data`。
- 调度方式是“本轮 `await` 结束后再 `setTimeout`”，不是 `setInterval`。`isRunning === true` 时不会并发下一轮。`concurrent` 只允许 `false`。
- 默认 `interval: 0`（不轮询）、`autoStart: false`、`immediate: false`、`pauseWhenHidden: true`、`continueOnError: true`、`resumeMode: 'immediate'`。
- `interval <= 0` 时 `start()` 直接返回；`setInterval(0)` 会停止轮询。`interval` 支持 `number` 或 `Ref<number>`。
- **`isRunning` 不是页面 loading**。静默轮询不要把 `isRunning` 绑到表格/页面主 loading。
- 每次 `start/stop/restart` 都会推进 `generation`。写入数据前必须 `if (!isCurrent()) return;`，防止慢请求回写。
- `pauseWhenHidden: true` 时，隐藏标签页会停后续调度；已经开始的一轮若调用方不处理 `signal`，仍可能跑完。回到前台默认立即补一轮（`resumeMode: 'immediate'`），也可 `'next-interval'`。
- `start()`：启动新链（已在跑则 no-op）。`restart()`：先停再启。`runNow()`：立刻跑一轮，未启动则先启动。
- Orval/mutator 已经提示的 API 错误，不要在 `onError` 里再 `message.error`。`continueOnError: false` 会在 task throw 后停掉轮询链。
- 组件卸载会 `stop` 并移除 `visibilitychange` 监听，不必手写对称销毁，除非还有额外定时器。

## 标准代码骨架

```vue
<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { usePollingTask, type PollingContext } from '@yss-ui/hooks';

const rows = ref<unknown[]>([]);
const pollingInterval = ref(3000);

/** 静默刷新；写入前检查 isCurrent。 */
const refreshSilently = async ({ signal, isCurrent }: PollingContext) => {
  const response = await fetch('/api/list', { signal });
  const payload = await response.json();
  if (!isCurrent()) return;
  rows.value = payload;
};

const { start, stop, restart, runNow, isActive } = usePollingTask(refreshSilently, {
  interval: pollingInterval,
  pauseWhenHidden: true,
});

/** 手动查询可保留自己的 loading，不要复用 isRunning。 */
const handleSearch = async () => {
  stop();
  await refreshSilently({ generation: 0, isCurrent: () => true });
  await restart({ immediate: false });
};

onMounted(() => {
  void start();
});
</script>

<template>
  <div>{{ isActive ? 'polling' : 'idle' }}</div>
</template>
```

`fetch('/api/list')` 仅作调度示意；真实 Orval 方法按 `../api-integration/SKILL.md` 选择，并把 `signal` 放到请求库支持的位置。

## 交付检查清单

- [ ] task 写入前调用 `isCurrent()`；能传的请求都传了 `signal`。
- [ ] 页面主 loading 没有绑定 `isRunning`。
- [ ] 手动查询 `stop → 带 loading 的请求 → restart`，与静默 task 分离。
- [ ] `interval`、`pauseWhenHidden`、`continueOnError`、`resumeMode` 与产品行为一致；`0` 会停轮询。
- [ ] `onError` 没有重复 API `message.error`。

## 失败兜底策略

- 旧数据覆盖新数据：查是否漏了 `isCurrent()`，以及是否在 `restart` 后仍写闭包里的旧引用。
- 切走标签页回来连打多轮：确认只有一套 Hook，且隐藏时没有另写 `setInterval`。
- 请求失败后轮询消失：看是不是 `continueOnError: false` 或 `interval` 被设成 `0`。
- 想展示 loading：用 `useLoading` 包手动查询，不要把轮询 Hook 改造成请求状态机。
