---
name: page-list-module
description: 指导实现 YSS UI 标准列表模块、远程服务端分页、查询条件重置、YTable 顶部工具栏、行操作按钮权限、批量选择与左树右表联动；当实现具体的数据查询列表、表格交互与 CRUD 列表闭环时使用。整页全套架构编排请使用 yss-ui-business-page-generation，独立表单请使用 page-form-module。
---

# Page List Module Skill

## 触发条件

- 实现查询、表格、分页、行操作或批量操作组合的业务列表。
- 实现左树右表、远程分页、工具栏或列设置。

## 不适用场景

- 仅实现表单提交，没有列表或分页。
- 仅展示本地静态数据，不涉及业务查询与列表操作。

## 必读依赖

- 组件选型：`../component-selection-imports/SKILL.md`
- 表格 API：`../ytable-usage/SKILL.md`
- 查询表单：`../yss-formily/SKILL.md`
- 接口、错误链路和长整型：`../api-integration/SKILL.md`
- 左树右表高度：`../ytree-usage/SKILL.md`、`../use-tree-height/SKILL.md`、`../use-table-height/SKILL.md`

## 文档检索

1. MCP 可用时，按当前页面实际使用的能力调用 `get_component_docs` 查询 `YTable`、`YFormily`、`useTableHeight` 或 `useTreeHeight`，再用 `get_demo` 获取对应官方示例；不要只凭 Skill 内的静态片段推断 API。
2. 精确查询无结果时，先用 `search_docs` 或 `list_components` 校正名称；仅在 MCP 不可用、调用失败或校正后仍无结果时，回退读取最新 `llms-full.txt`。文档版本与当前依赖不一致时，再核对当前源码、CodeGraph 和真实导出。
3. 当前会话已经加载上述本地 Skill 时，不要再通过 MCP 重复查询同一 Skill；仅在依赖 Skill 缺失时使用 `list_skills`、`get_skill` 补齐规则。

## 硬约束（禁止/必须）

- 列表请求必须收敛在 `useXxxList`，模板不直接请求。
- 后端查询参数可用 `pageIndex/pageSize`；YTable 分页状态必须使用 `current/pageSize/total`。
- 远程分页必须配置 `pageable`、`pagination.remote = true`、`v-model:pagination` 和 `@page-change`；事件参数固定为 `{ current, pageSize }`，禁止读取 `currentPage`。
- 禁止臆造 `request`/`search-params` 等 Prop，也禁止把实例 `refresh()` 当成远程重新查询；该方法只调用 vxe `updateData()` 刷新当前表格数据，远程查询/重置/刷新必须调用业务 Hook。
- 查询区使用纵向 `search-content`：`YFormily` 仅渲染字段，查询/重置按钮在外部 `.xxx__search-actions` 独占下一行并右对齐。
- 新增、导入、批量操作等主操作直接放入 `#toolbar-right` 插槽即可自动渲染；**无需配置 `:toolbar-config="{ custom: true }"`**，避免无端展示列设置图标；**仅在业务明确需要列设置时才传入 `:toolbar-config="{ custom: true }"`**。
- 删除等危险操作默认使用 `actionConfig.buttons[].isConfirm` 按钮项气泡确认，禁止默认使用居中 `Modal.confirm`。
- 列定义、状态映射和筛选配置放入 `constant.ts`；超过 10 行的列不得内联在 `index.vue`。
- **国际化与多语言适配规范**：
  - 在支持国际化的项目中，严禁在 `constant.ts`、模板或 Hook 中硬编码中文；
  - 表格列定义采用 `createColumns(t)` 工厂函数，操作列采用 `createActionConfig(handlers, t)`，在 SFC 中通过 `computed` 响应式提供给 `YTable`；
  - 查询卡片中的查询与重置按钮必须绑定 `{{ $t('common.search') }}` 与 `{{ $t('common.reset') }}`；
  - 表格分页器必须声明 `showTotal: (total: number) => t('common.total', { total })`（或在 Hook/computed 中由当前语言派生），确保语言切换时中英文总数提示正常联动；
  - 表格工具栏主操作按钮必须通过 `{{ $t('common.create') }}`、`{{ $t('common.batchDelete') }}` 绑定多语言词条。
- 长整型 ID 保持字符串透传，禁止 `Number()`/`parseInt()` 等会丢失精度的转换；页码、状态值等普通 number 按真实生成类型使用。
- 禁止使用 `if (res?.success)` 包裹成功逻辑，也禁止在 `else`/`catch` 重复调用 `message.error`；mutator 已对 `success === false` 提示并 reject。

## 标准代码骨架

```typescript
import { reactive, ref } from 'vue';

/** 管理规则列表数据、查询条件和远程分页。 */
export const useRuleList = () => {
  const loading = ref(false);
  const dataList = ref<RuleItem[]>([]);
  const query = reactive<RuleQuery>({ pageIndex: 1, pageSize: 20, keyword: '' });
  const pagination = reactive({ current: 1, pageSize: 20, total: 0, remote: true });

  /** 请求规则列表；错误 Toast 由 mutator 处理。 */
  const fetchData = async (): Promise<void> => {
    loading.value = true;
    try {
      query.pageIndex = pagination.current;
      query.pageSize = pagination.pageSize;
      const res = await queryRuleList(query);
      dataList.value = res.data ?? [];
      pagination.total = res.totalCount ?? 0;
    } catch {
      dataList.value = [];
      pagination.total = 0;
    } finally {
      loading.value = false;
    }
  };

  /** 处理页码或每页数量变化。 */
  const handlePageChange = ({ current, pageSize }: { current: number; pageSize: number }): void => {
    pagination.current = current;
    pagination.pageSize = pageSize;
    void fetchData();
  };

  /** 从第一页执行查询。 */
  const handleSearch = (): void => {
    pagination.current = 1;
    void fetchData();
  };

  /** 重置查询条件并回到第一页。 */
  const handleReset = (): void => {
    Object.assign(query, { pageIndex: 1, pageSize: pagination.pageSize, keyword: '' });
    pagination.current = 1;
    void fetchData();
  };

  return { loading, dataList, query, pagination, fetchData, handlePageChange, handleSearch, handleReset };
};
```

`RuleItem`、`RuleQuery`、`queryRuleList` 必须替换为当前 Orval 生成类型和真实方法，禁止照抄占位名。

```vue
<YTable
  v-if="isReady"
  ref="tableRef"
  v-model:selected-row-keys="selectedRowKeys"
  :row-config="{ keyField: 'id', useKey: true }"
  :data="dataList"
  :columns="columns"
  :loading="loading"
  :height="tableHeight"
  pageable
  v-model:pagination="pagination"
  @page-change="handlePageChange"
>
  <template #toolbar-right>
    <YButton :disabled="selectedRowKeys.length === 0" @click="handleBatchDelete">{{ $t('common.batchDelete') }}</YButton>
    <YButton type="primary" @click="openCreate">{{ $t('common.create') }}</YButton>
  </template>
</YTable>
```

## 交付检查清单

- [ ] 已确认真实 Orval 导出、查询 DTO 和响应字段。
- [ ] 查询参数与 YTable 分页字段已映射，`page-change` 回调读取 `current/pageSize` 而非 `currentPage`。
- [ ] 若包含批量操作，首列已配置 `type: 'checkbox'`，设置了 `:row-config="{ keyField: 'xxx', useKey: true }"`，批量按钮配置了 `:disabled="selectedRowKeys.length === 0"`，操作成功后已清空选中态。
- [ ] 国际化多语言规范：在支持国际化的项目中，查询/重置按钮、表格列名、操作列标题、气泡确认、分页总数提示、工具栏主按钮均使用多语言词条，禁止硬编码中文。
- [ ] 查询/重置会回到第一页，远程分页配置完整。
- [ ] 主操作在 `#toolbar-right`，列设置已开启。
- [ ] 删除使用气泡确认，操作按钮的 loading/close 在成功与失败后都会恢复。
- [ ] 长整型 ID 未转 number，普通 number 仍符合真实类型。
- [ ] 没有 `if (res?.success)` 和重复错误 Toast。
- [ ] loading、空态和失败后数据状态可预期。

## 失败兜底策略

- 分页字段混乱时，在 Hook 中分离 YTable 状态和后端参数，不直接把 `pageIndex/totalCount` 绑到组件。
- 列表逻辑过大时，拆分 `useListData` 和 `useListActions`，不得回填到 `index.vue`。
- 响应字段不稳定时，在 Hook API 边界做最小映射，禁止在模板散落兼容分支。
