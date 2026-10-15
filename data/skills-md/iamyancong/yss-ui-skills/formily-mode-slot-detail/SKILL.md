---
name: formily-mode-slot-detail
description: 指导 YFormily 新增、编辑、查看三态与插槽渲染；当配置 mode 0/1/2、查看态只读、详情页 Descriptions 展示、detail-options、Schema Slot 或详情字段插槽时使用。
---

# Formily Mode Slot Detail Skill

## 触发条件

- 需要 `mode: 0/1/2` 的新增、编辑、查看三态切换。
- 查看态需要 Descriptions 响应式渲染或 `detail-*` 字段插槽。
- 同一字段在编辑态使用 Schema Slot、查看态使用 detail slot。

## 不适用场景

- 基础表单骨架：使用 `../formily-foundation/SKILL.md`。
- 复杂联动与副作用：使用 `../formily-linkage-effects/SKILL.md`。
- 分步流程：使用 `../formily-step-flow/SKILL.md`。

## 文档检索

1. 当前会话可用 yss-ui MCP 时，先用 `get_component_docs` 查询 `YFormily` 的 `mode`、`detail-options`、Slots 和 Methods；实现三态、详情插槽或 Schema Slot 时，再用 `get_demo` 获取 `formily/modes`、`formily/group`、`formily/slot` 等官方 Demo。
2. MCP 查询未命中时先用 `search_docs/list_components` 校正名称；MCP 不可用、调用失败或校正后仍无结果时，才读取最新 `llms-full.txt`。若文档与当前项目依赖版本不一致，用当前源码和导出核验。

## 硬约束（禁止/必须）

- mode 语义固定：`0=新增`、`1=编辑`、`2=查看`；默认值为 `0`。
- `mode=2` 直接进入 Descriptions 查看态并强制 readPretty；源码没有 `detail-as` 等额外详情开关，禁止生成旧式 prop。
- 描述列表配置使用 `:detail-options`。默认 `responsive=true`，此时 `columns` 被忽略；响应式列数使用 `maxColumns`、`minColumns`、`minWidth`，固定列数才组合 `responsive: false` 与 `columns`。
- 查看态插槽命名固定为 `#detail-<path>`，字段路径中的 `.` 替换为 `-`；作用域为 `{ value, item, values }`。
- 编辑态插槽使用 `x-component: 'Slot'` 与 `x-component-props.name`；`value/onChange` 默认提供，仅在需要 `field` 或整表数据时配置 `params`。
- 运行时切换 mode 时加 `:key="mode"`，确保当前实现重新创建 form/schema 上下文并避免状态残留。
- 查看态不会发送 `update:modelValue`；回填优先在渲染前准备好 `v-model`/`initial-values`，或通过已公开的 `setValues` 更新。
- 只使用公开实例方法：`getValues`、`setValues`、`submit`、`setFieldState`、`toggle/expand/collapse`；禁止编造 `validate/reset/clearValidate`。
- 加载详情的 Orval API 错误已由 `mutator.ts` 统一 `message.error` 并 reject，业务 `else`/`catch` 禁止重复提示。
- 分步需求默认走 `formily-step-flow`，不在本 skill 中给 `FormStep` 默认方案。

## 标准代码骨架

```vue
<script setup lang="ts">
import { YMonaco, YFormily, type ISchema } from '@yss-ui/components';
import { ref } from 'vue';

/** YFormily 业务模式。 */
type FormMode = 0 | 1 | 2;

/** 当前表单模式。 */
const mode = ref<FormMode>(0);

/** 编辑和查看回填值。 */
const initialValues = {
  user: { email: 'user@example.com' },
  sql: 'select * from users',
};

/** 编辑与详情共用的 Schema。 */
const schema: ISchema = {
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
          'x-component-props': { maxColumns: 2, minColumns: 1, minWidth: 320 },
          properties: {
            user: {
              type: 'object',
              properties: {
                email: {
                  type: 'string',
                  title: '邮箱',
                  'x-decorator': 'FormItem',
                  'x-component': 'Input',
                },
              },
            },
            sql: {
              type: 'string',
              title: 'SQL',
              'x-decorator': 'FormItem',
              'x-decorator-props': { gridSpan: 2 },
              'x-component': 'Slot',
              'x-component-props': { name: 'sql' },
            },
          },
        },
      },
    },
  },
};
</script>

<template>
  <YFormily
    :key="mode"
    :schema="schema"
    :initial-values="initialValues"
    :mode="mode"
    :detail-options="{ bordered: true, maxColumns: 3, minColumns: 1, minWidth: 260 }"
  >
    <template #sql="{ value, onChange }">
      <YMonaco :model-value="value" language="sql" @change="onChange" />
    </template>

    <template #detail-user-email="{ value }">
      <a :href="`mailto:${value}`">{{ value }}</a>
    </template>

    <template #detail-sql="{ value }">
      <YMonaco :model-value="value" language="sql" readonly />
    </template>
  </YFormily>
</template>
```

## 交付检查清单

- [ ] mode 语义和默认值正确，运行时切换配置了 `:key="mode"`。
- [ ] 未生成 `detail-as`、旧式详情开关或虚构实例方法。
- [ ] `detail-options` 已区分响应式 `maxColumns` 与固定列 `columns`。
- [ ] 查看态插槽路径映射正确，作用域只使用 `{ value, item, values }`。
- [ ] 编辑 Slot 名称与模板插槽一致，只在需要时声明 `params`。
- [ ] 查看回填在进入 `mode=2` 前准备完毕，未依赖查看态 v-model 回写。
- [ ] API 失败只由 `mutator.ts` 统一提示，业务 `else`/`catch` 未重复 `message.error`。
- [ ] 无分步 `FormStep` 默认实现。

## 失败兜底策略

- 查看态插槽不生效时，先按详情收集后的数据路径核对 `detail-<path>`，不要把 `FormLayout/FormGrid` 容器名拼入路径。
- 编辑态插槽不生效时，核对 `x-component-props.name` 与模板名；需要整表值时再加入 `params: ['$values']`。
- 模式切换错乱时先确认 `:key="mode"`，再检查回填数据是否在新实例挂载前准备好。
- API 调用 reject 时只恢复 loading 或保留原数据，不重复弹出错误提示。
