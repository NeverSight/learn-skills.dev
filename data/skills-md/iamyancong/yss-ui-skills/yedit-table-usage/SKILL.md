---
name: yedit-table-usage
description: 指导 YSS UI 业务页面使用 @yss-ui/components 的 YEditTable 实现可编辑表格、行内编辑、添加/删除行、下拉多选与可创建 tags、行级候选联动、表头筛选、校验和查看态；当需求出现编辑表格、明细行、扩展属性、可编辑列或 YEditTableColumn 时使用。
---

# YEditTable 使用

## 触发条件

- 需求包含可编辑表格、行内编辑、明细行、扩展属性、行级候选联动或表格校验。
- 需要使用 `YEditTableColumn`、`validate()`、`addable`、`filterOptions` 或表头筛选。

## 不适用场景

- 主列表只展示和分页：使用 `../ytable-usage/SKILL.md`。
- 表单主体不是表格：使用 `../yss-formily/SKILL.md`。

## 实施流程

1. 当前会话可用 yss-ui MCP 时，先用 `get_component_docs` 查询 `YEditTable` 的 Props、Events、Methods、`YEditTableColumn` 和操作列配置；需要添加行、多选/可创建下拉、行级联动或校验时，再用 `get_demo` 获取对应官方 Demo。
2. MCP 工具不可用、调用失败或用 `search_docs/list_components` 校正后仍无结果时，才读取最新 `llms-full.txt`；若文档与当前项目依赖版本不一致，用当前源码和导出核验。
3. 区分列编辑器、行级候选、表头筛选三种职责，再设计行类型和校验。
4. 把行类型、列配置、新行工厂和纯操作配置放到 `constant.ts`；把数据状态、API、联动和事件放到 Hook。
5. 显式实现 `@add`、查看态、删除确认与 `validate()` 链路，再对照真实返回类型检查提交。

## 硬约束（禁止/必须）

- 业务可编辑表格必须优先使用 `YEditTable`，从 `@yss-ui/components` 导入 `YEditTable`、`YEditTableColumn`、`YTableActionConfig`；不用 `a-table` 手搭编辑态。
- 有 `component` 的列会由组件自动补齐 `edit-render`，业务列不需要重复写 `editRender: {}`。
- `component: 'form-item-select'` 的 `props.multiple: true` 表示从现有候选中多选；`props.allowCreate: true` 会进入 Ant Design Vue `tags` 模式，值必须按数组建模。
- 当前实现中 `multiple` 优先于 `allowCreate`，同时配置并不会得到“多选且可新建”。该需求必须明确说明当前能力缺口，使用自定义插槽或先增强组件，禁止继续生成错误 demo。
- 行级候选使用 `rowOptionsFieldName` 指定的行字段，或列级 `filterOptions({ field, optionsMap, row })`；不修改全局 `optionsMap` 影响其他行。
- `filterOptions` 只过滤编辑态候选；表头筛选使用 `filterable + filters + filterMethod`，文本面板优先使用 `filterRender: { name: 'VxeInput', props: {...} }`。
- `addable` 只渲染添加按钮并发出 `add`，不会自动创建行。必须监听 `@add` 并修改 `v-model:data`；业务插入位置要与 `addPosition` 一致。
- `disabled` 只禁用表格编辑，不会自动隐藏添加按钮和操作列。查看态必须同时设置 `:addable="false"` 并移除操作列/按钮。
- 删除使用 `type: 'action' + actionConfig.buttons[].isConfirm`；不默认使用 `Modal.confirm`。
- `validate()` 真实返回 `Promise<{ valid: boolean; errorMsg: Map<string, string> }>`。组件 ref 未就绪时不得误判为校验成功。
- 弹窗/抽屉内使用添加按钮时，高度 Hook 配置 `withAddButton: true`；如果同时分页或开启工具栏，一并开启对应偏移。
- API 失败由 `mutator.ts` 统一提示并 reject。Hook 中不写 `success === false` 分支，不在 `else/catch` 重复 `message.error`；清理状态放在 `finally`。
- **大表性能约束与反模式防护（Critical）**：
  - **固定行高**：大数据量（行数 > 50 或列数 > 20）必须显式通过 `tableConfig: { cellConfig: { height: 36 } }` 设置固定行高，避免虚拟滚动动态估算引发重排与滚动抖动。
  - **禁止每格嵌入 Formily**：严禁在单元格插槽中循环嵌套实例化 `<YFormily>` 或复杂双向响应式表单，必须使用组件内置轻量编辑器或行级激活。
  - **虚拟滚动合理阈值**：组件默认启用 `virtualXConfig: { enabled: true, gt: 50 }` 与 `virtualYConfig: { enabled: true, gt: 100 }`，不可随意关闭；宽表可主动调低 `gt` 阈值。
  - **分页优先**：超过 100 行且交互复杂时，优先采用 `pageable: true` 分页，而非全量挂载上千行可编辑 DOM。


### 统一消费与构建契约

- 默认单包安装，从 `@yss-ui/components` 具名导入并局部注册；不全局安装 YSSUI，不拆新的功能包。
- `@yss-ui/components/table`、`@yss-ui/components/formily` 自 1.6.7 起公开，是可选入口；旧版本先核对 exports，禁止批量改写根入口。
- 子路径与插件改善加载边界，不减少默认安装依赖；VXE/Formily 仍由组件库配套安装。
- 官方 `@yss-ui/components/vite` 插件自 1.7.0 起已发布，完整验收范围为 Vite 6。旧项目先读取实际安装版本、exports 和现有插件，禁止与旧隔离插件同时运行。
- 生成代码前用 MCP `get_consumption_contract` 核对版本；未知版本不得假设新插件可用。文档站 Demo 的样式导入不能直接复制为业务全局样式策略。

## 标准代码骨架

```typescript
import type { YEditTableColumn, YTableActionConfig } from '@yss-ui/components';

/** 扩展属性行。 */
export interface ExtRow {
  id?: string;
  _rowKey: string;
  extName?: string;
  extValues?: string[];
  memo?: string;
}

/** 可编辑表格列。 */
export const EDIT_COLUMNS: YEditTableColumn[] = [
  {
    field: 'extName',
    title: '扩展属性',
    minWidth: 220,
    component: 'form-item-select',
    props: { placeholder: '请选择扩展属性' },
    customRule: (value, _row, _field, all) => {
      if (!value) return { errMsg: '扩展属性不能为空' };
      if (all.filter(item => item.extName === value).length > 1) return { errMsg: '扩展属性不能重复' };
      return {};
    },
  },
  {
    field: 'extValues',
    title: '扩展值',
    minWidth: 240,
    component: 'form-item-select',
    props: { multiple: true, placeholder: '请选择扩展值' },
    customRule: value =>
      Array.isArray(value) && value.some(item => String(item).length > 100)
        ? { errMsg: '单个扩展值最多 100 个字符' }
        : {},
  },
  {
    field: 'memo',
    title: '备注',
    minWidth: 240,
    component: 'form-item-input',
    props: { placeholder: '请输入备注' },
    customRule: value => (String(value ?? '').length > 200 ? { errMsg: '最多 200 个字符' } : {}),
  },
  { type: 'action', title: '操作', width: 100, fixed: 'right' },
];

/** 表格字典数据；实际项目可由 Hook 响应式提供。 */
export const EDIT_OPTIONS_MAP = {
  extName: [
    { label: '类型', value: 'type' },
    { label: '级别', value: 'level' },
  ],
  extValues: [
    { label: '默认', value: 'default' },
    { label: '扩展', value: 'extended' },
  ],
};

/** 创建前端新行。 */
export const createEmptyRow = (): ExtRow => ({
  _rowKey: `temp-${Date.now()}-${Math.random().toString(36).slice(2)}`,
  extValues: [],
});

/** 创建带删除确认的操作配置。 */
export const createActionConfig = (onDelete: (row: ExtRow) => void): YTableActionConfig => ({
  buttons: [
    {
      value: 'delete',
      label: '删除',
      type: 'link',
      isConfirm: true,
      confirmProps: { title: '是否确认删除此条数据？', okText: '确定', cancelText: '取消' },
      click: ({ row }) => onDelete(row),
    },
  ],
});
```

```vue
<script setup lang="ts">
import { computed, ref } from 'vue';
import { YEditTable } from '@yss-ui/components';
import { createActionConfig, createEmptyRow, EDIT_COLUMNS, EDIT_OPTIONS_MAP, type ExtRow } from './constant';

/** 组件模式。0-新增，1-编辑，2-查看。 */
interface Props {
  mode: 0 | 1 | 2;
}

const props = defineProps<Props>();
const rows = ref<ExtRow[]>([]);
const tableRef = ref<InstanceType<typeof YEditTable>>();
const readonly = computed(() => props.mode === 2);
const columns = computed(() => (readonly.value ? EDIT_COLUMNS.filter(column => column.type !== 'action') : EDIT_COLUMNS));
const actionConfig = createActionConfig(row => {
  rows.value = rows.value.filter(item => item._rowKey !== row._rowKey);
});

/** 处理组件 add 事件，显式更新 v-model:data。 */
const handleAddRow = () => {
  rows.value = [...rows.value, createEmptyRow()];
};

/** 校验全部编辑行。 */
const validateRows = async (): Promise<boolean> => {
  if (!tableRef.value) return false;
  const { valid } = await tableRef.value.validate();
  return valid;
};
</script>

<template>
  <YEditTable
    ref="tableRef"
    v-model:data="rows"
    :columns="columns"
    :action-config="actionConfig"
    :options-map="EDIT_OPTIONS_MAP"
    :table-config="{ rowConfig: { keyField: '_rowKey', useKey: true }, editConfig: { trigger: 'click', mode: 'row', autoClear: false } }"
    :disabled="readonly"
    :addable="!readonly"
    add-btn-text="添加一行"
    add-position="bottom"
    @add="handleAddRow"
  />
</template>

<style scoped lang="less">
@import './style.less';
</style>
```

## Select 值类型边界

```typescript
/** allowCreate 对应 tags 模式，字段按数组存储。 */
interface CreatableRow {
  tags?: string[];
}

const creatableColumn: YEditTableColumn = {
  field: 'tags',
  title: '标签',
  component: 'form-item-select',
  props: { allowCreate: true, placeholder: '请选择或输入标签' },
};
```

## 表头筛选

```typescript
const textFilterColumn: YEditTableColumn = {
  field: 'columnName',
  title: '目标列名称',
  component: 'form-item-input',
  filterable: true,
  filters: [{ data: '' }],
  filterMethod: ({ option, cellValue }) =>
    String(cellValue ?? '').toLowerCase().includes(String(option?.data ?? '').trim().toLowerCase()),
  filterRender: { name: 'VxeInput', props: { clearable: true, placeholder: '请输入关键词' } },
};
```

- 远程筛选监听 `@filter-change`，并设置 `filterMethod: () => true` 禁用本地二次筛选。
- 切换数据源或新增行后，可调用 `tableRef.value?.getTableInstance()?.clearFilter()`。
- 只在面板高度定制时使用 `#<field>-filter`；修改 `option.data` 后调用 `updateFilterOptionStatus(option, !!option.data)` 同步状态。

## 交付检查清单

- [ ] `addable/@add/v-model:data/addPosition` 形成真实新增闭环。
- [ ] `allowCreate` 和 `multiple` 未被错误组合，行字段类型与 Select 模式匹配。
- [ ] 查看态同时禁用编辑、隐藏添加按钮和移除操作列。
- [ ] `validate()` 按 `{ valid, errorMsg }` 处理，组件 ref 未就绪时不提交。
- [ ] API Hook 没有重复 `message.error`，前端临时 key 不传给后端。

## 失败兜底策略

- 添加按钮无反应时，先确认已监听 `@add` 并更新 `v-model:data`，不继续调整 `addPosition`。
- 查看态仍能删除/添加时，移除操作列并将 `addable` 设为 `false`，不只依赖 `disabled`。
- 可创建多选与字段类型冲突时，回到 `allowCreate => tags 数组`、`multiple => 现有候选多选` 的真实实现；当前组合能力不足时明确报告。
- API 联动失败时在 `finally` 恢复行级 loading，不捕获后重复 `message.error` 或继续使用失败结果。
