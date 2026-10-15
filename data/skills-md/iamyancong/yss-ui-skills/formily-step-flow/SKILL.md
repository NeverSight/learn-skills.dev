---
name: formily-step-flow
description: 指导基于 Ant Design Vue Steps 与多 YFormily 实例的分步表单与向导流程录入，覆盖各步骤独立校验、跨步数据持久保留、最终确认预览与聚合提交闭环；当业务需要分步录入、分阶段流程或多步骤向导时使用。单页普通表单请使用 formily-foundation，单纯字段联动请使用 formily-linkage-effects。
---

# Formily Step Flow Skill

## 触发条件

- 需求是分步表单（Step Form）或流程化录入。
- 每一步需要独立校验与前进/后退控制。
- 需要跨步数据聚合、确认预览和最终提交编排。

## 不适用场景

- 普通单页表单：使用 `../formily-foundation/SKILL.md`。
- 仅字段联动：使用 `../formily-linkage-effects/SKILL.md`。
- 仅查看态插槽：使用 `../formily-mode-slot-detail/SKILL.md`。

## 文档检索

1. 当前会话可用 yss-ui MCP 时，先用 `get_component_docs` 查询 `YFormily` 的 `submit()`、`mode`、`v-model` 和回填边界，再用 `get_demo` 获取 `formily/steps` 官方 Demo；`Steps` 的属性以当前 `ant-design-vue` 依赖和类型为准。
2. MCP 查询未命中时先用 `search_docs/list_components` 校正名称；MCP 不可用、调用失败或校正后仍无结果时，才读取最新 `llms-full.txt`。若文档与当前项目依赖版本不一致，用当前源码和导出核验。

## 硬约束（禁止/必须）

- 默认方案使用 `ant-design-vue` 的 `Steps` + 多 schema / 多 `YFormily`；组件库没有 `YSteps`，禁止编造。
- 业务层禁止把 `@formily/antdv FormStep` 作为默认方案；只有维护旧代码或用户明确指定时才可使用。
- 每次前进前对当前 YFormily 实例执行 `submit()`；该方法校验成功后 resolve，失败时 reject，不返回布尔值，禁止写 `ok !== false`。
- 每步使用独立 `v-model` 数据，并以单一 `reactive` 对象聚合；`v-if` 卸载实例后仍由该数据源保留回填值。
- 确认步骤用前面步骤的聚合数据作为 `initial-values`/`v-model`，禁止绑定一个空的第三步对象导致详情无数据。
- 最终 API 提交只聚合业务步骤，禁止把纯确认步骤当作新数据源。
- Orval API 的网络错误及 `success === false` 业务错误已由 `mutator.ts` 统一 `message.error` 并 reject；最终提交的 `else`/`catch` 禁止重复提示，loading 放在 `finally` 恢复。

## 标准代码骨架

```vue
<script setup lang="ts">
import { YButton, YFormily, type ISchema } from '@yss-ui/components';
import { Steps as ASteps } from 'ant-design-vue';
import { computed, reactive, ref } from 'vue';

/** YFormily 对外提交能力。 */
interface YssFormilyExpose {
  submit: () => Promise<Record<string, any>>;
}

/** 分步表单数据。 */
interface StepFormData {
  step1: { name: string };
  step2: { level: string };
}

/** 分步表单提交回调 Props。 */
interface StepFlowProps {
  onSubmit: (values: StepFormData) => Promise<void>;
}

/** 分步表单提交回调。 */
const props = defineProps<StepFlowProps>();
/** 当前步骤，从 0 开始。 */
const currentStep = ref(0);
/** 最终提交状态。 */
const submitting = ref(false);
/** 第一步表单实例。 */
const step1Ref = ref<YssFormilyExpose>();
/** 第二步表单实例。 */
const step2Ref = ref<YssFormilyExpose>();
/** 步骤导航配置。 */
const stepItems = [{ title: '基础信息' }, { title: '策略配置' }, { title: '确认提交' }];
/** 跨步唯一数据源。 */
const formData = reactive<StepFormData>({
  step1: { name: '' },
  step2: { level: 'normal' },
});

/** 创建符合业务三层布局约定的步骤 Schema。 */
const createStepSchema = (properties: Record<string, ISchema>): ISchema => ({
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
          properties,
        },
      },
    },
  },
});

/** 第一步 Schema。 */
const step1Schema = createStepSchema({
  name: {
    type: 'string',
    title: '任务名称',
    required: true,
    'x-decorator': 'FormItem',
    'x-component': 'Input',
  },
});
/** 第二步 Schema。 */
const step2Schema = createStepSchema({
  level: {
    type: 'string',
    title: '策略等级',
    required: true,
    enum: [
      { label: '普通', value: 'normal' },
      { label: '严格', value: 'strict' },
    ],
    'x-decorator': 'FormItem',
    'x-component': 'Select',
  },
});
/** 确认步骤 Schema。 */
const confirmSchema = createStepSchema({
  name: { type: 'string', title: '任务名称', 'x-decorator': 'FormItem', 'x-component': 'Input' },
  level: { type: 'string', title: '策略等级', 'x-decorator': 'FormItem', 'x-component': 'Input' },
});
/** 确认步骤展示数据。 */
const confirmValues = computed(() => ({ name: formData.step1.name, level: formData.step2.level }));

/** 校验当前步骤，成功后前进。 */
const next = async () => {
  const currentRef = currentStep.value === 0 ? step1Ref.value : step2Ref.value;
  if (!currentRef) return;
  try {
    await currentRef.submit();
    currentStep.value += 1;
  } catch {
    return;
  }
};

/** 返回上一步。 */
const back = () => {
  currentStep.value = Math.max(0, currentStep.value - 1);
};

/** 提交全部步骤数据。 */
const submitAll = async () => {
  submitting.value = true;
  try {
    await props.onSubmit({ step1: { ...formData.step1 }, step2: { ...formData.step2 } });
  } finally {
    submitting.value = false;
  }
};
</script>

<template>
  <ASteps :current="currentStep" :items="stepItems" />

  <YFormily v-if="currentStep === 0" ref="step1Ref" v-model="formData.step1" :schema="step1Schema" />
  <YFormily v-else-if="currentStep === 1" ref="step2Ref" v-model="formData.step2" :schema="step2Schema" />
  <YFormily
    v-else
    :schema="confirmSchema"
    :initial-values="confirmValues"
    :mode="2"
    :detail-options="{ bordered: true, maxColumns: 2, minColumns: 1, minWidth: 320 }"
  />

  <YButton :disabled="currentStep === 0" @click="back">上一步</YButton>
  <YButton v-if="currentStep < 2" type="primary" @click="next">下一步</YButton>
  <YButton v-else type="primary" :loading="submitting" @click="submitAll">提交</YButton>
</template>
```

复杂页面把 schema、类型与步骤 hook 分别拆到 `constant.ts`、`hooks/useStepFlow.ts`，保持 `index.vue` 在 150 行以内。

## 交付检查清单

- [ ] 使用 `ASteps + 多 YFormily`，组件来源明确且未编造 `YSteps`。
- [ ] 每步前进前 await 当前实例 `submit()`，校验 reject 时不会前进。
- [ ] 未使用 `ok !== false` 判断 `submit()` 结果。
- [ ] 步骤切换后数据可保留和回显，确认页直接读取前序聚合数据。
- [ ] 最终提交只聚合真实业务步骤，未把确认页空对象混入 payload。
- [ ] API 失败只由 `mutator.ts` 统一提示，业务 `else`/`catch` 未重复 `message.error`。
- [ ] 业务层未使用 `@formily/antdv FormStep` 作为默认实现。

## 失败兜底策略

- 下一步无校验时确认 ref 指向当前已挂载实例，并直接观察 `submit()` 是否 reject。
- 状态串联错误时先收敛为单一 `reactive` 数据源，再检查每步 `v-model` 路径。
- 确认页为空时检查是否错误绑定了独立 `step3`，应改为前序数据的 `computed` 聚合。
- API 调用 reject 时只在 `finally` 恢复 loading，不重复弹出错误提示。
- 步骤过多或主组件超过 150 行时，按阶段拆子组件和 `useStepXxx` hook。
