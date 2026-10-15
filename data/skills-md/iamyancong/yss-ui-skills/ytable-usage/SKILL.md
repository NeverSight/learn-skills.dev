---
name: ytable-usage
description: 指导 YSS UI 业务列表页、CRUD 表格、远程分页、操作列、气泡确认、列筛选、字典翻译、行拖拽、工具栏和自定义插槽正确使用 @yss-ui/components 的 YTable；当需要配置 YTableColumn、YTableActionConfig、pagination、filter-change 或表格实例方法时使用。
---

# YTable 使用

## 触发条件

- 生成或修改业务列表、CRUD 表格、远程分页、操作列、列筛选、工具栏或行拖拽。
- 需要配置 `YTableColumn`、`YTableActionConfig`、分页状态或表格实例方法。

## 不适用场景

- 可编辑表格是核心需求：使用 `../yedit-table-usage/SKILL.md`。
- 页面只有短小静态数据且不需要表格交互。

## 实施流程

1. 当前会话可用 yss-ui MCP 时，先用 `get_component_docs` 查询 `YTable` 的 Props、Events、Slots、Types 与实例方法；需要远程分页、筛选、操作列、拖拽或工具栏时，再用 `get_demo` 获取对应官方 Demo。
2. MCP 工具不可用、调用失败或用 `search_docs/list_components` 校正后仍无结果时，才读取最新 `llms-full.txt`；若文档与当前项目依赖版本不一致，用当前源码和导出核验。
3. 把远程数据、`loading`、分页映射、API 调用和事件处理放入 Hook；把列定义和纯配置放入 `constant.ts`。
4. 在模板中组合 `data/columns/loading/pagination`，并根据真实开启的工具栏和分页配置高度 Hook。
5. 完成后核对删除确认、远程筛选、分页字段映射和 API 错误处理边界。

## 硬约束（禁止/必须）

- 默认从 `@yss-ui/components` 导入 `YTable`、`YTableColumn`、`YTableActionConfig` 等真实导出，不使用 `a-table` 实现业务主表格。
- 远程分页状态使用 `current/pageSize/total/remote`，显式设置 `remote: true`；后端 `pageIndex/pageSize/totalCount` 只在 Hook 中映射。
- 开启内置分页时传 `pageable`，受控更新使用 `v-model:pagination`，请求时机使用 `@page-change="handlePageChange"`。
- `page-change` 事件参数固定为 `{ current: number, pageSize: number }`；回调必须读取 `current`，禁止写成组件不会派发的 `currentPage`。
- YTable 没有 `request` 或 `searchParams` Props；远程查询由业务 Hook 管理。`refresh()` 是真实实例方法，内部调用 vxe-table `updateData()` 刷新当前表格数据，不等于重新调用后端接口。
- 行键使用 `:row-config="{ keyField: 'id', useKey: true }"`，不臆造 `row-key` Prop。**在轮询或频繁刷新运行态的表格中，强烈建议显式配置 `keyField` 为真实业务主键**，以确保操作列“更多”与 Popconfirm 确认弹层按稳定行身份保持，避免行对象浅拷贝或重建时误关弹层。
- 新增、导入、批量操作等主按钮直接放入 `#toolbar-right` 或 `#toolbar-left` 插槽即可自动渲染工具栏；**无需配置 `:toolbar-config="{ custom: true }"`**，避免无端展示列设置图标；**仅在业务明确需要列设置时才传入 `:toolbar-config="{ custom: true }"`**。
- 删除、启停、发布等危险操作使用 `actionConfig.buttons[].isConfirm = true`，不默认使用 `Modal.confirm`；配合 `needLoading: true` 时，异步回调自然 resolve 视为成功自动关闭并清理 loading，也可显式调用 `helpers.close()` 立即关闭；异常或 reject 时自动停止 loading 并保持弹层供重试，或配置 `manualClose: true` 开启严格受控关闭模式。
- 列配置超过 10 行时放入 `constant.ts`；需要调用组件 Hook 的操作配置使用工厂函数注入回调，禁止在 `constant.ts` 直接引用组件局部的 `openEdit/deleteItem`。
- **表格国际化多语言规范（Critical）**：
  - 在支持或预留国际化的项目中，**严禁在表格列配置、操作列配置和工具栏按钮中硬编码中文**。
  - **列定义多语言工厂函数**：列定义推荐采用工厂函数 `export const createColumns = (t: (key: string, ...args: any[]) => string): YTableColumn[] => [...]`，在组件中通过 `const columns = computed(() => createColumns(t))` 动态响应语言切换。
  - **操作列配置多语言工厂函数**：`createActionConfig` 必须支持注入 `t` 函数，配置 `title: t('common.operation')`，按钮项配置 `label: t('common.edit')` / `label: t('common.delete')`，气泡确认配置 `confirmProps: { title: t('common.confirmDelete'), okText: t('common.confirm'), cancelText: t('common.cancel') }`。
  - **操作列列宽多语言自适应**：`YTable` 与 `YEditTable` 底层已支持根据按钮文本长度及语言环境智能自适应计算安全列宽，并具备安全下限纠偏（Safety Clamp）机制。业务新模块在 `createActionConfig` 中**推荐无需硬编码 `width`**，交由组件库全自动托管；存量模块即使显式配置了 `width`，在英文环境下组件库也会自动将其纠偏至安全宽度，彻底杜绝英文文本被裁剪。
  - **分页总数多语言配置**：分页 `pagination` 配置项推荐声明 `showTotal: (total: number) => t('common.total', { total })`（或在 Hook/computed 中动态传入），确保语言切换时中英文总数提示即时响应，禁止写死 `"共 ${total} 条"`。
  - **工具栏按钮**：插槽中的操作按钮文案统一使用 `{{ t('common.create') }}` 等国际化词条，禁止直接写死 `<YButton>新增</YButton>`。
- 远程筛选必须提供稳定 `filters`，设置 `filterMethod: () => true` 禁用本地二次过滤，并监听 `filter-change`。
- 自适应滚动列表绑定 `:height="tableHeight"`；`pageable`、工具栏分别对应 `withPagination: true`、`withToolbar: true`。纯短表不强制引入高度 Hook。
- `mutator.ts` 已对网络错误和 `success === false` 统一 `message.error` 并 reject。API Hook 不再检查 `success === false`，不在 `else/catch` 重复 `message.error`；用 `finally` 恢复 loading，让异常继续中断流程。


### 统一消费与构建契约

- 默认单包安装，从 `@yss-ui/components` 具名导入并局部注册；不全局安装 YSSUI，不拆新的功能包。
- `@yss-ui/components/table`、`@yss-ui/components/formily` 自 1.6.7 起公开，是可选入口；旧版本先核对 exports，禁止批量改写根入口。
- 子路径与插件改善加载边界，不减少默认安装依赖；VXE/Formily 仍由组件库配套安装。
- 官方 `@yss-ui/components/vite` 插件自 1.7.0 起已发布，完整验收范围为 Vite 6。旧项目先读取实际安装版本、exports 和现有插件，禁止与旧隔离插件同时运行。
- 生成代码前用 MCP `get_consumption_contract` 核对版本；未知版本不得假设新插件可用。文档站 Demo 的样式导入不能直接复制为业务全局样式策略。

## 标准代码骨架

```typescript
import type { YTableActionConfig, YTableColumn } from '@yss-ui/components';

/** 列表行数据。 */
export interface ItemRow {
  id: string;
  name: string;
  status: string;
}

/** 状态字典。 */
export const STATUS_OPTIONS = [
  { label: '启用', value: '1' },
  { label: '停用', value: '0' },
];

/** 列表列配置工厂函数（支持国际化） */
export const createColumns = (t: (key: string, ...args: any[]) => string): YTableColumn[] => [
  { type: 'seq', title: t('common.seq') || '序号', width: 70 },
  { field: 'name', title: t('demo.name') || '名称', minWidth: 180 },
  { field: 'status', title: t('demo.status') || '状态', width: 120, isTransform: true },
  { type: 'action', title: t('common.operation') || '操作', width: 180 },
];

/** 按组件 Hook 提供的回调创建操作列配置（支持国际化） */
export const createActionConfig = (
  handlers: {
    onEdit: (row: ItemRow) => void;
    onDelete: (row: ItemRow) => Promise<void>;
  },
  t: (key: string, ...args: any[]) => string
): YTableActionConfig => ({
  title: t('common.operation') || '操作',
  width: 180,
  fixed: 'right',
  buttons: [
    { value: 'edit', label: t('common.edit') || '编辑', type: 'link', click: ({ row }) => handlers.onEdit(row) },
    {
      value: 'delete',
      label: t('common.delete') || '删除',
      type: 'link',
      isConfirm: true,
      confirmProps: {
        title: t('common.confirmDelete') || '确认删除该数据吗？',
        okText: t('common.confirm') || '确定',
        cancelText: t('common.cancel') || '取消',
      },
      click: ({ row }) => handlers.onDelete(row),
    },
  ],
});
```

## 远程分页 Hook 关键模式

```typescript
import { ref } from 'vue';
import type { YTablePagination } from '@yss-ui/components';
import type { ItemRow } from '../constant';

/** 列表 API 依赖，由当前项目的 Orval 函数适配。 */
export interface ItemListApi {
  queryPage: (params: { pageIndex: number; pageSize: number }) => Promise<{
    list?: ItemRow[];
    totalCount?: number;
  }>;
  deleteItem: (params: { id: string }) => Promise<unknown>;
}

/** 管理 YTable 远程分页和删除刷新。 */
export const useItemList = (api: ItemListApi) => {
  const dataList = ref<ItemRow[]>([]);
  const loading = ref(false);
  const pagination = ref<YTablePagination>({ current: 1, pageSize: 20, total: 0, remote: true });

  /** 查询当前页；错误提示由 mutator 统一处理。 */
  const loadList = async () => {
    loading.value = true;
    try {
      const result = await api.queryPage({
        pageIndex: pagination.value.current,
        pageSize: pagination.value.pageSize,
      });
      dataList.value = result.list ?? [];
      pagination.value = { ...pagination.value, total: result.totalCount ?? 0 };
    } finally {
      loading.value = false;
    }
  };

  /** 同步 YTable 分页状态并重新查询。 */
  const handlePageChange = async ({ current, pageSize }: { current: number; pageSize: number }) => {
    pagination.value = { ...pagination.value, current, pageSize };
    await loadList();
  };

  /** 删除后刷新列表；不重复弹出 API 错误。 */
  const handleDelete = async (row: ItemRow) => {
    await api.deleteItem({ id: row.id });
    await loadList();
  };

  return { dataList, loading, pagination, loadList, handlePageChange, handleDelete };
};
```

```vue
<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useI18n } from 'vue-i18n';
import { YButton, YTable } from '@yss-ui/components';
import { useTableHeight } from '@yss-ui/hooks';
import { createActionConfig, createColumns, STATUS_OPTIONS, type ItemRow } from './constant';
import { useItemList, type ItemListApi } from './hooks/useItemList';

/** 列表实例的 API 依赖。 */
interface Props {
  api: ItemListApi;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  create: [];
  edit: [row: ItemRow];
}>();

const { t } = useI18n();
const tableAreaRef = ref<HTMLDivElement>();
const { tableHeight } = useTableHeight(tableAreaRef, { withPagination: true, withToolbar: true });
const { dataList, loading, pagination, loadList, handlePageChange, handleDelete } = useItemList(props.api);

/** 响应式列配置（随语言切换即时更新） */
const columns = computed(() => createColumns(t));

/** 响应式操作列配置（随语言切换即时更新） */
const actionConfig = computed(() =>
  createActionConfig(
    {
      onEdit: row => emit('edit', row),
      onDelete: handleDelete,
    },
    t
  )
);

onMounted(loadList);
</script>

<template>
  <div ref="tableAreaRef" class="table-area">
    <YTable
      :data="dataList"
      :columns="columns"
      :action-config="actionConfig"
      :loading="loading"
      :options-map="{ status: STATUS_OPTIONS }"
      :row-config="{ keyField: 'id', useKey: true }"
      :height="tableHeight"
      pageable
      v-model:pagination="pagination"
      @page-change="handlePageChange"
    >
      <template #toolbar-right>
        <YButton type="primary" @click="emit('create')">{{ t('common.create') }}</YButton>
      </template>
    </YTable>
  </div>
</template>

<style scoped lang="less">
@import './style.less';
</style>
```

```less
/* style.less */
.table-area {
  height: 100%;
  min-height: 0;
  overflow: hidden;
}
```

## 表格多选与批量操作标准模式

当业务需要 Checkbox 多选与批量操作（如批量删除、批量导出、批量启用）时，遵循以下规范：

1. **列配置**：首列必须声明 `{ type: 'checkbox', width: 50, fixed: 'left', align: 'center' }`。
2. **行唯一键**：必须显式指定 `:row-config="{ keyField: 'id', useKey: true }"`（`keyField` 与业务主键如 `userCode` 对齐）。
3. **受控双向绑定**：推荐优先使用 `v-model:selected-row-keys="selectedRowKeys"` 或 `v-model:selected-rows="selectedRows"`，或者统一监听 `@selection-change`。
4. **批量操作按钮**：放在 `#toolbar-right`，并配置 `:disabled="selectedRowKeys.length === 0"`。
5. **清空选中态**：批量操作成功后，直接重置 `selectedRowKeys.value = []` 或调用 `tableRef.value.clearSelection()`。

```vue
<YTable
  ref="tableRef"
  v-model:selected-row-keys="selectedRowKeys"
  :row-config="{ keyField: 'id', useKey: true }"
  :data="dataList"
  :columns="columns"
  pageable
  v-model:pagination="pagination"
  @page-change="handlePageChange"
>
  <template #toolbar-right>
    <YButton :disabled="selectedRowKeys.length === 0" @click="handleBatchDelete">{{ t('common.batchDelete') }}</YButton>
  </template>
</YTable>
```

## 插槽与实例边界

- 优先使用 kebab-case：单元格 `#<field>`、表头 `#<field>-header`、筛选 `#<field>-filter`、工具栏 `#toolbar-left/#toolbar-right`、展开行 `#expand-row`、分组表头 `#group-header`、更多图标 `#action-more-icon`。
- `getTableInstance()`、`refresh()`、`recalculate()`、`clearSelection()`、`getSelectedRows()`、`getSelectedRowKeys()`、`setSelection()`、`getPaginationInstance()` 是真实暴露方法；只在对应语义下使用。

## 交付检查清单

- [ ] 分页状态和 `page-change` 参数均使用 `current/pageSize`，未使用 `currentPage`；`filter-change` 与 YTable 真实 API 一致。
- [ ] 国际化多语言规范：在多语言项目中，列配置使用 `createColumns(t)`、操作列使用 `createActionConfig(handlers, t)`、分页总数 `showTotal` 绑定国际化模板函数、工具栏按钮使用 `$t`，禁止硬编码中文。
- [ ] 多选列已配置 `type: 'checkbox'`，已设置 `:row-config="{ keyField: 'xxx', useKey: true }"`，批量按钮绑定了 `selectedRowKeys.length === 0` 禁用。
- [ ] 批量操作成功后已重置 `selectedRowKeys` 并调用 `tableRef.clearSelection()`。
- [ ] 未使用虚构 `request/searchParams/row-key` Props，也未把 `refresh()` 当成远程请求。
- [ ] 工具栏、字典翻译、操作确认与高度偏移均与实际开关一致。
- [ ] API Hook 没有 `success === false` 分支或重复 `message.error`。

## 失败兜底策略

- 分页字段混乱时，在 Hook 中分离 YTable 状态和后端参数，不直接把 `pageIndex/totalCount` 绑到组件。
- 操作过多时使用 `displayLimit` 和更多菜单；远程刷新失效时回到业务 `loadList()`，不把实例 `refresh()` 当成接口请求。
- API 失败后只在 `finally` 恢复本地 loading，让 mutator 的 reject 继续中断删除后刷新等后续流程。
