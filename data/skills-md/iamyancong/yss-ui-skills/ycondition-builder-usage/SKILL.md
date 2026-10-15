---
name: ycondition-builder-usage
description: 指导规则配置、数据质量条件、嵌套 AND/OR 条件树使用 @yss-ui/components 的 YConditionBuilder；覆盖 ConditionGroup/ConditionLeaf、loadFields/loadValues、getOperators、BETWEEN/IN、strictMode 校验和 disabled，禁止把 readonly 或未消费的 segments 当成可用 API。
---

# YConditionBuilder 使用

## 触发条件

- 生成或修改条件构建器、规则表达式、数据质量筛选条件、嵌套 AND/OR 条件树。
- 需要配置 `YConditionBuilder` 的 `loadFields`、`loadValues`、`getOperators`、`operatorOptions`、`BETWEEN`/`IN` 或 `validate()`。

## 不适用场景

- 普通查询表单字段、级联 Select：使用 `../yss-formily/SKILL.md` 或 `../formily-foundation/SKILL.md`。
- YTable 列头筛选、字典翻译：使用 `../ytable-usage/SKILL.md`。
- YConditionBuilder 不是 Formily 内置 `x-component`，不要写进 Schema 组件表。

## 实施流程

1. 当前会话可用 yss-ui MCP 时，先用 `get_component_docs` 查询 `YConditionBuilder` 的 Props、Events、Expose 与 `ConditionGroup`；需要远程字段、联动操作符、BETWEEN 或校验时再 `get_demo`。
2. MCP 不可用或无结果时，读取最新 `llms-full.txt`；仍不一致则以 `packages/components/src/condition-builder` 源码为准。
3. 先定义根 `ConditionGroup`，再提供字段/操作符/值加载函数。
4. 提交前调用 `validate()` 或监听 `@validate`；只读展示用 `disabled`。

## 硬约束（禁止/必须）

- 从 `@yss-ui/components` 导入 `YConditionBuilder` 和类型 `ConditionGroup`、`ConditionLeaf`、`OperatorOption`、`OptionItem`、`YConditionExpose`。
- 根数据必须是 `type: 'GROUP'` 的 `ConditionGroup`（`logicalOp: 'AND' | 'OR'` + `children`），叶子是 `type: 'LEAF'`（`field/operator/value`）。禁止改成扁平 `{ field, op, val }[]` 还绑到 `v-model`。
- `createEmptyGroup`、`DEFAULT_OPERATOR_OPTIONS` **不是**包的运行时导出；业务侧自己构造初始组和操作符列表，或省略 `operator-options` 使用组件内置项。
- 字段和值候选必须走 `load-fields(q)`、`load-values({ q, field, operator, node })`。组件会显示 label、写入 value。
- 静态操作符用 `operator-options`；按字段变化时用 `get-operators(field)`。每项必须带 `kind: 'none' | 'single' | 'between' | 'multiple'`，否则输入形态会落到 `single`。
- `kind: 'between'` 时 `value` 是 `[start, end]`；`multiple` 是数组；`none`（如 `IS NULL`）不展示值输入。
- `readonly` 已废弃且**当前不生效**。只读/禁用必须用 `disabled`。
- `segments` / `SegmentSchema.render` 存在于类型，但运行时**不消费**。禁止按自定义分段、自定义控件去生成 UI。
- `getValue('legacy')` 不会转换成另一套旧结构，与 `getValue()` 返回同一棵 `ConditionGroup`。新代码不要传 `legacy`。
- `is-root`、`depth`、`remove` 事件只给内部递归节点用；业务入口保持默认，不要监听 `remove`。
- 默认 `strict-mode` 为 `true`：字段、操作符、值（`kind !== 'none'`）都必填，`0` 视为有效值。允许空条件时显式 `:strict-mode="false"`。
- `and-text` / `or-text` 可覆盖“且/或”展示；不传则走组件语言包。国际化项目不要在业务里写死中文操作符 label，用 `t()` 生成 `operator-options`。

## 标准代码骨架

```vue
<script setup lang="ts">
import { ref } from 'vue';
import {
  YConditionBuilder,
  type ConditionGroup,
  type OperatorOption,
  type OptionItem,
  type YConditionExpose,
} from '@yss-ui/components';

const conditionRef = ref<YConditionExpose | null>(null);
const model = ref<ConditionGroup>({
  id: 'root',
  type: 'GROUP',
  logicalOp: 'AND',
  children: [],
});

const operatorOptions: OperatorOption[] = [
  { label: '等于', value: 'EQ', kind: 'single' },
  { label: '区间', value: 'BETWEEN', kind: 'between' },
  { label: '包含', value: 'IN', kind: 'multiple' },
  { label: '为空', value: 'IS NULL', kind: 'none' },
];

const fieldOptions: OptionItem[] = [
  { label: '年龄', value: 'age' },
  { label: '城市', value: 'city' },
];

/** 按关键字过滤字段。 */
const loadFields = async (q: string): Promise<OptionItem[]> => {
  const keyword = q.toLowerCase();
  return fieldOptions.filter(
    item => item.label.toLowerCase().includes(keyword) || item.value.toLowerCase().includes(keyword)
  );
};

/** 按当前字段加载值候选。 */
const loadValues = async (args: {
  q: string;
  field: unknown;
  operator: string | undefined;
}): Promise<OptionItem[]> => {
  if (String(args.field) !== 'city') return [];
  return [
    { label: '北京', value: 'beijing' },
    { label: '上海', value: 'shanghai' },
  ];
};

/** 提交前校验整棵条件树。 */
const handleSubmit = () => {
  const valid = conditionRef.value?.validate() ?? false;
  if (!valid) return;
  const payload = conditionRef.value?.getValue();
  return payload;
};
</script>

<template>
  <YConditionBuilder
    ref="conditionRef"
    v-model="model"
    :max-depth="3"
    :operator-options="operatorOptions"
    :load-fields="loadFields"
    :load-values="loadValues"
    @validate="() => undefined"
  />
</template>
```

按字段动态操作符时传入 `:get-operators="getOperators"`，并在函数内返回带 `kind` 的 `OperatorOption[]`。

## 交付检查清单

- [ ] `v-model` 绑定的是 `ConditionGroup`，叶子含 `field/operator/value`。
- [ ] `loadFields` / `loadValues` / `kind` 与真实输入形态一致；BETWEEN 未当成单值。
- [ ] 只读用 `disabled`，没有依赖 `readonly` 或自定义 `segments`。
- [ ] 提交走 `validate()` / `@validate`；`getValue()` 未假设 legacy 转换。
- [ ] 没有把 YConditionBuilder 写进 Formily `x-component`。

## 失败兜底策略

- 下拉里没有字段：补 `load-fields`，不要把选项写进不存在的 `options` Prop。
- 选了“区间”仍只有一个输入框：检查操作符 `kind` 是否为 `'between'`。
- 点了只读仍能编辑：把 `readonly` 换成 `disabled`。
- `validate()` 一直 false：先看 `strict-mode` 和空叶子；允许空值时关闭严格模式，而不是改数据结构。
