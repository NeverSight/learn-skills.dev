---
name: ytree-usage
description: 指导 YSS UI 左树右表、组织树、分类树、目录树和节点管理页使用 @yss-ui/components 的 YTree，覆盖 fieldNames 字段映射、搜索过滤、受控选中、节点动作、删除确认、虚拟滚动和自适应高度；当生成或修改树形筛选、左树右表、树搜索或树节点操作时使用。
---

# YTree 使用

## 触发条件

- 生成或修改左树右表、组织树、分类树、目录树、树搜索或树节点操作。
- 需要配置 `fieldNames`、受控选中、`YTreeActionItem` 或树区域自适应高度。

## 不适用场景

- 树数据只用于表单 TreeSelect 字段：使用 `YFormily` 或对应表单规范。
- 页面只有普通列表而没有层级筛选：使用 `../ytable-usage/SKILL.md`。

## 实施流程

1. 当前会话可用 yss-ui MCP 时，先用 `get_component_docs` 查询 `YTree` 的 Props、Slots、Events 和 `YTreeActionItem`；需要搜索、节点动作、受控选中或左树右表时，再用 `get_demo` 获取对应官方 Demo。
2. MCP 工具不可用、调用失败或用 `search_docs/list_components` 校正后仍无结果时，才读取最新 `llms-full.txt`；若文档与当前项目依赖版本不一致，用当前源码和导出核验。
3. 确定树数据的 title/key/children 字段、受控状态和选中后的业务联动。
4. 按容器布局配置 `useTreeHeight`，再添加搜索和节点动作。
5. 若包含删除，单独完成气泡确认链路；不把 `danger` 颜色当成二次确认。

## 硬约束（禁止/必须）

- 从 `@yss-ui/components` 导入 `YTree`、`YTreeActionItem` 等真实导出；高度使用 `@yss-ui/hooks` 的 `useTreeHeight`。
- 数据字段不一致时配置 `fieldNames`，不为了改名重复递归复制树数据。
- 搜索使用 `filterable + v-model:searchValue`；受控选中使用 `v-model:selectedKeys`。
- 普通节点菜单使用 `showActions + getNodeActions`，并监听 `@action`。`YTreeActionItem` 只支持 `key/label/icon/disabled/danger`，禁止臆造 `isConfirm/click` 等字段。
- `danger: true` 只改变危险项视觉，不会弹出确认框。删除必须放在节点附近的 `#node-suffix` 或当前选中节点操作区，用 Ant Design Vue `Popconfirm` 的 `@confirm` 调用接口；不使用居中 `Modal.confirm`。
- 树区域需要滚动时绑定 `:height="treeHeight"`，不默认添加 `:virtual="true"`。只有展开后可见扁平节点数 `* itemHeight > height` 时才会实际裁剪 DOM。
- 使用 YTree 内置搜索时，高度 Hook 通过 `extraOffset: YTREE_SEARCH_HEIGHT` 扣除 48px；不再叠加无依据的魔法数。
- 左树右表优先组合 `YSplitPane + YCard + YTree + YTable`；切换节点时同步查询条件并把右表分页重置为第 1 页。
- 节点删除 API 的错误由 `mutator.ts` 统一提示并 reject；不在 `else/catch` 重复 `message.error`。

## 标准代码骨架

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { YTree, type YTreeActionItem } from '@yss-ui/components';
import { useTreeHeight, YTREE_SEARCH_HEIGHT } from '@yss-ui/hooks';

/** 树节点数据。 */
interface TreeNode {
  id: string;
  name: string;
  children?: TreeNode[];
}

const emit = defineEmits<{
  create: [node: TreeNode];
  edit: [node: TreeNode];
}>();
const treeAreaRef = ref<HTMLDivElement>();
const treeData = ref<TreeNode[]>([]);
const searchValue = ref('');
const selectedKeys = ref<Array<string | number>>([]);
const { treeHeight } = useTreeHeight(treeAreaRef, {
  extraOffset: YTREE_SEARCH_HEIGHT,
});

/** 生成当前节点的非危险操作。 */
const getNodeActions = (): YTreeActionItem[] => [
  { key: 'add', label: '新增子节点' },
  { key: 'edit', label: '编辑' },
];

/** 处理 YTree 动作事件。 */
const handleTreeAction = ({ key, node }: { key: string; node: TreeNode }) => {
  if (key === 'add') emit('create', node);
  if (key === 'edit') emit('edit', node);
};
</script>

<template>
  <div ref="treeAreaRef" class="tree-area">
    <YTree
      :height="treeHeight"
      :tree-data="treeData"
      :field-names="{ title: 'name', key: 'id', children: 'children' }"
      filterable
      show-actions
      v-model:searchValue="searchValue"
      v-model:selectedKeys="selectedKeys"
      :get-node-actions="getNodeActions"
      @action="handleTreeAction"
    />
  </div>
</template>

<style scoped lang="less">
@import './style.less';
</style>
```

```less
/* style.less */
.tree-area {
  flex: 1;
  min-height: 0;
  overflow: hidden;
}
```

## 删除确认边界

```vue
<template #node-suffix="{ node }">
  <Popconfirm title="确认删除该节点吗？" ok-text="确定" cancel-text="取消" @confirm="handleDelete(node)">
    <YButton type="link" @click.stop>删除</YButton>
  </Popconfirm>
</template>
```

`Popconfirm` 从 `ant-design-vue` 导入，`YButton` 从 `@yss-ui/components` 导入。如果每个节点都展示删除会过密，把同样的 `Popconfirm` 放到选中节点的页面工具栏。

## 交付检查清单

- [ ] `fieldNames`、`searchValue`、`selectedKeys`、`action` 与真实 API 一致。
- [ ] 节点动作项未出现虚构字段，删除不会点菜单后立即执行。
- [ ] 高度偏移与内置搜索实际开关一致，没有多扣魔法数。
- [ ] 左树选中后，右表查询条件和分页重置闭环清晰。

## 失败兜底策略

- 节点字段不统一时先修正 `fieldNames`，不复制整棵树换键。
- 点击删除立即调用 API 时，移出节点动作菜单，改为节点附近或页面操作区 `Popconfirm`。
- 传入 `height` 但节点未裁剪时，先核对展开后可见节点数、`itemHeight` 和阈值，不盲目强制 `virtual=true`。
- 节点 API 失败后让 mutator reject 中断右表刷新等后续流程，不重复错误提示。
