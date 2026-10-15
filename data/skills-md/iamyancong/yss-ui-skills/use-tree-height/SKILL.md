---
name: use-tree-height
description: 指导 YTree、左树右表、组织树、分类树、树搜索和 Tab/抽屉内树区域使用 @yss-ui/hooks 的 useTreeHeight 实现自适应高度；当树区域需要独立滚动、容器切换后高度不正确或需要扣除 YTree 内置搜索高度时使用。
---

# useTreeHeight 使用

## 触发条件

- YTree 或左树右表需要独立滚动区和自适应高度。
- 树区域含内置搜索，或在 Tab/抽屉/折叠面板切换后高度不正确。

## 不适用场景

- 树节点很少、无需独立滚动，且父级布局已托管高度。
- 主要问题是树节点与右侧数据联动，而非布局高度。

## 文档检索

1. MCP 可用时，先用 `get_component_docs` 精确查询 `useTreeHeight`，需要示例时再调用 `get_demo`；不要仅凭 Skill 中的静态签名推断当前 API。
2. 精确查询无结果时，先用 `search_docs` 校正名称；仅在 MCP 不可用、调用失败或仍无结果时，回退读取最新 `llms-full.txt`。文档版本与当前依赖不一致时，再核对 Hook 源码、CodeGraph 和真实导出。

## 硬约束（禁止/必须）

- 把树区域的直接父容器 `ref` 传给 `useTreeHeight(treeAreaRef, options)`，并使用真实返回值 `treeHeight/recalculateHeight`。
- 最外层必须有可计算高度；树区域使用 `flex: 1; min-height: 0; overflow: hidden;`。
- 计算结果绑定到 `YTree` 的 `:height="treeHeight"`，不用固定魔法高度替代 Hook，也不为了触发虚拟滚动默认添加 `:virtual="true"`。
- 使用 YTree 内置搜索时配置 `extraOffset: YTREE_SEARCH_HEIGHT`；搜索区已放在 `treeAreaRef` 外部时不再扣除。
- `extraOffset` 只用于树区域内部实际占位的搜索、padding 或边框，禁止无依据叠加 `+16` 等偏移。
- Hook 仅在挂载时为当时存在的 `treeAreaRef` 建立 `ResizeObserver`。优先保持树区域外层容器挂载（如使用 `v-show`）；Tab/抽屉可见后在 `nextTick` 调用 `recalculateHeight()`。
- 隐藏态容器可能得到 `minHeight` 而不是真实可用高度；不把该值当成最终布局结果。

## 标准代码骨架

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { YTree } from '@yss-ui/components';
import { useTreeHeight, YTREE_SEARCH_HEIGHT } from '@yss-ui/hooks';

const treeAreaRef = ref<HTMLDivElement>();
const treeData = ref([]);
const { treeHeight, recalculateHeight } = useTreeHeight(treeAreaRef, {
  extraOffset: YTREE_SEARCH_HEIGHT,
});
</script>

<template>
  <div ref="treeAreaRef" class="tree-area">
    <YTree :height="treeHeight" :tree-data="treeData" filterable />
  </div>
</template>

<style scoped lang="less">
@import './style.less';
</style>
```

```less
/* style.less */
.tree-layout {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.tree-area {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}
```

## 容器切换时机

```typescript
import { nextTick } from 'vue';

/** 容器显示后补充一次高度计算。 */
const handleVisibleChange = async (visible: boolean) => {
  if (!visible) return;
  await nextTick();
  recalculateHeight();
};
```

## 交付检查清单

- [ ] `treeAreaRef` 在 Hook 挂载时可用，父级高度可计算。
- [ ] 内置搜索开关与 `YTREE_SEARCH_HEIGHT` 偏移一致，没有重复扣减。
- [ ] Tab/抽屉切换后使用真实的 `recalculateHeight()` 重算。
- [ ] 节点较少时未裁剪 DOM 被识别为正常虚拟滚动阈值行为。

## 失败兜底策略

- 树高度显示为 `minHeight` 且与容器不符时，检查是否在隐藏态完成首次计算，并在可见后重算。
- `treeAreaRef` 由 `v-if` 延迟创建且尺寸不再自动更新时，保持外层容器挂载后重新初始化 Hook，或使用 `v-show + recalculateHeight()`。
- 节点较少未触发 DOM 裁剪时，核对虚拟滚动阈值，不加 `virtual=true` 伪装修复。
