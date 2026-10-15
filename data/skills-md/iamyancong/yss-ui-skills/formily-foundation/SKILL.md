---
name: formily-foundation
description: 指导基于 @yss-ui/components 的 YFormily 基础表单开发，覆盖字段校验规则、提交链路、查询表单栅格布局、scope 表达式与规范导入边界；当创建单页基础表单、配置普通校验或排查基础表单提交时使用。复杂动态联动请转至 formily-linkage-effects，分步向导请使用 formily-step-flow。
---

# Formily Foundation Skill

## 触发条件

- 创建或改造 `YFormily` 基础表单（字段、校验、提交）。
- 修复表单导入路径、schema 层级、提交不触发等问题。
- 实现普通单页表单，不含复杂联动或详情插槽。

## 不适用场景

- 复杂联动、副作用、跨字段逻辑：使用 `../formily-linkage-effects/SKILL.md`。
- 查看态 detail 插槽和 mode 切换：使用 `../formily-mode-slot-detail/SKILL.md`。
- 分步表单：使用 `../formily-step-flow/SKILL.md`。

## 文档检索

1. 当前会话可用 yss-ui MCP 时，先用 `get_component_docs` 查询 `YFormily` 的基础 Props、Methods 与 Schema 边界；实现字段布局、提交或校验失败时，再用 `get_demo` 获取 `formily/basic`、`formily/grid`、`formily/submit-failed` 等官方 Demo。
2. MCP 查询未命中时先用 `search_docs/list_components` 校正名称；MCP 不可用、调用失败或校正后仍无结果时，才读取最新 `llms-full.txt`。若文档与当前项目依赖版本不一致，用当前源码和导出核验。

## 硬约束（禁止/必须）

- 业务生成代码统一从 `@yss-ui/components` 导入 `YFormily` 与 `ISchema`；`YssFormily` 仅作为历史兼容别名说明。
- 禁止业务层导入 `@formily/antdv`、`@formily/antd*` UI 组件。
- 必须使用三层结构：`FormLayout -> FormGrid -> 字段`，禁止字段直接挂在根节点或单独以 `FormGrid` 作为顶层布局。
- `Submit` 必须传 `onSubmit`，否则不触发表单提交。
- 标准业务列表/CRUD 查询区默认让 `YFormily` 只渲染字段；查询/重置按钮用外部 `YButton` 放在 `.xxx__search-actions`，由 hook 的 `handleSearch/handleReset` 控制分页重置和请求。
- `AutoButtonGroup -> Submit/Reset` 仅用于纯 Formily 表单提交，不作为业务列表查询区默认方案。
- 查询区禁止横向放“表单 + 按钮”后用大 `gap`、`align-items: flex-start` 或 `padding-top` 硬调位置；字段换行时按钮必须在搜索卡片右下角。
- 横向表单必须显式设置 `FormLayout` 的 `labelWidth` 和 `labelAlign: 'right'`，抽屉/弹窗场景尤其不能让 label 宽度自适应。
- `FormGrid` 默认保持响应式：`minColumns: 1`，通过 `maxColumns` 和 `minWidth` 控制宽屏列数；不要写 `minColumns: maxColumns` 固定列数，除非用户明确要求不响应式。
- 查询表单常用 `labelWidth: 100~120`、`FormGrid { maxColumns: 3 或 4, minColumns: 1, minWidth: 260~360 }`，按钮行在表单外部右下角；抽屉/弹窗编辑表单常用 `labelWidth: 140`、`FormGrid { maxColumns: 2, minColumns: 1, minWidth: 320~360 }`。
- 备注、说明等长字段必须用 `x-decorator-props.gridSpan` 占满整行，例如两列布局用 `gridSpan: 2`。
- 下拉选择器（`Select`, `TreeSelect`, `Radio.Group` 等）异步数据源必须通过 `enum` 或 `x-reactions` / `field.dataSource` 注入，严禁写入 `x-component-props.options`（会导致 Formily 首次挂载空数组且后续不更新，产生首次打开弹窗显示“暂无数据”的 Bug）。
- 事件表达式必须字符串化（`'{{ ... }}'`），并按组件语义使用事件名。
- 只使用源码已公开的 Props 和实例方法；当前没有 `show-button-group`、`detail-as`、`validate`、`reset`、`clearValidate` 等 YFormily API。
- Orval API 的网络错误及 `success === false` 业务错误已由 `mutator.ts` 统一 `message.error` 并 reject；提交 hook 禁止在 `else` 或 `catch` 中重复提示。
- 客户端校验提示使用 `onFormSubmitValidateFailed`；禁止在 `onFormSubmitFailed` 或 `Submit.onSubmitFailed` 中调用 `message.error`，它们也会捕获 `onSubmit` 内的 API reject。
- **Formily 表单校验规则（x-validator）防坑规范**：
  - 必填文本字段必须声明 `whitespace: true`，即 `{ required: true, whitespace: true, message: '请输入xxx' }`，防止输入纯空格绕过前端校验。
  - 自定义长度、格式和跨字段校验不得重复承担必填职责；函数式校验必须在空值时返回通过（如 `validator: (val) => { const str = (val || '').trim(); if (!str) return true; return validateContentLength(val) || true; }`），空值统一交由 `required` 报错，非空时才校验具体规则。
  - 当前 YFormily 的 FormItem 适配层会在运行时归一化反馈：空值优先显示必填提示，非空值移除残留必填提示，多条相关消息只拼接一次。该兜底不替代正确的 Schema 校验职责拆分。
- **Schema 国际化工厂函数规范（Critical）**：
  - 在支持或预留国际化的微应用项目中，**严禁声明导出包含硬编码中文的静态 Schema 常量对象**；必须采用函数式工厂 `export const createSchema = (t: (key: string, ...args: any[]) => string): ISchema => ({ ... })` 导出。
  - 字段 `title`、`placeholder`、静态枚举 `enum`、校验规则 `message` 均调用 `t('...')` 生成。
  - 在 SFC 模板中通过 `const schema = computed(() => createSchema(t))` 传递给 `<YFormily :schema="schema" />`，确保语言切换时表单项与校验提示即时同步切换。
- 分步需求默认走 `formily-step-flow`，不在本 skill 内给 `FormStep` 方案。

## 标准代码骨架

```vue
<script setup lang="ts">
import { computed } from 'vue';
import { useI18n } from 'vue-i18n';
import { YFormily, type ISchema } from '@yss-ui/components';

/** 表单保存回调 Props。 */
interface SaveFormProps {
  onSave: (values: Record<string, any>) => Promise<void>;
}

/** 表单保存回调。 */
const props = defineProps<SaveFormProps>();
const { t } = useI18n();

/** 校验通过后提交表单数据。 */
const onSubmit = (values: Record<string, any>) => {
  return props.onSave(values);
};

/** 基础表单 Schema 工厂函数（支持国际化）。 */
export const createSchema = (t: (key: string, ...args: any[]) => string): ISchema => ({
  type: 'object',
  properties: {
    layout: {
      type: 'void',
      'x-component': 'FormLayout',
      'x-component-props': { layout: 'horizontal', labelWidth: 120, labelAlign: 'right' },
      properties: {
        grid: {
          type: 'void',
          'x-component': 'FormGrid',
          'x-component-props': { maxColumns: 3, minColumns: 1, minWidth: 260 },
          properties: {
            name: {
              type: 'string',
              title: t('common.name') || '名称',
              'x-decorator': 'FormItem',
              'x-component': 'Input',
              'x-component-props': { placeholder: t('common.placeholderInput') || '请输入' },
              required: true,
            },
            submit: {
              type: 'void',
              'x-component': 'Submit',
              'x-content': t('common.submit') || '提交',
              'x-component-props': { onSubmit: '{{ onSubmit }}' },
            },
          },
        },
      },
    },
  },
});

const schema = computed(() => createSchema(t));
</script>

<template>
  <YFormily :schema="schema" :scope="{ onSubmit }" />
</template>
```

## 业务查询区布局

```vue
<template>
  <YCard class="demo-page__search-card" :padding="16">
    <div class="demo-page__search-content">
      <div class="demo-page__search-form">
        <YFormily v-model="queryModel" :schema="searchSchema" />
      </div>
      <div class="demo-page__search-actions">
        <YButton type="primary" @click="handleSearch">查询</YButton>
        <YButton @click="handleReset">重置</YButton>
      </div>
    </div>
  </YCard>
</template>
```

```less
.demo-page {
  &__search-content {
    display: flex;
    flex-direction: column;
    align-items: stretch;
    gap: 16px;
  }

  &__search-form {
    width: 100%;
    min-width: 0;

    :deep(.ant-formily-form-item) {
      margin-bottom: 0;
    }

    :deep(.ant-formily-form-grid) {
      width: 100%;
    }
  }

  &__search-actions {
    display: flex;
    width: 100%;
    flex: 0 0 auto;
    align-items: center;
    justify-content: flex-end;
    gap: 12px;
  }
}
```

## 交付检查清单

- [ ] 导入来源和组件边界正确。
- [ ] schema 三层结构完整。
- [ ] 横向表单有固定 `labelWidth` 且 label 右对齐。
- [ ] `FormGrid` 使用响应式列配置，未把 `minColumns` 固定成宽屏列数。
- [ ] `Submit` 提交链路可用，校验可触发。
- [ ] 只使用公开 Props/实例方法，未出现 `show-button-group`、`detail-as` 等旧式或虚构 API。
- [ ] 业务列表查询/重置按钮在外部 `.xxx__search-actions`，按钮行独占下一行并右对齐；缩窄后不会贴在第一行字段旁。
- [ ] label 宽度和右对齐已显式配置。
- [ ] 包含可运行 `initial-values` 或 `v-model` 示例。
- [ ] 国际化多语言规范：在支持国际化的项目中，Schema 统一使用 `createSchema(t)` 工厂函数，字段标题、占位符、枚举与校验文案无硬编码中文。
- [ ] 未出现 `@formily/antdv` 业务层导入。
- [ ] API 失败仅由 `mutator.ts` 统一提示，业务 `else`/`catch` 未重复 `message.error`。

## 失败兜底策略

- 若提交不触发：先检查 `Submit.x-component-props.onSubmit`。
- 若字段不显示：先核对 `FormLayout/FormGrid/properties` 层级。
- 若 API 调用 reject：只恢复 loading 或回滚局部状态，不重复弹出错误提示。
- 若需求升级为联动/模式/分步：立即切换对应 skill，不在本 skill 内硬扩展。

## 参考

- 完整示例：`./references/examples.md`
