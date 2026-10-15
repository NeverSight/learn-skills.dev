---
name: vue3-best-practices
description: 在 Vue3 + TypeScript 业务页面、公共组件和 Composables 中规范响应式状态解构、组件跨级通信、异步竞态取消机制与长整型大数精度处理；当实现或重构复杂的 Vue3 业务逻辑与 Hooks 时使用。表单特定规范请结合 yss-formily，组件库维护参考 component-development。
---

# Vue3 Best Practices Skill

## 触发条件

- 业务页面出现响应式、组件通信、状态管理相关问题。
- 需要重构复杂组件逻辑到更稳的 Composition API 模式。
- 需要防止 `v-model`、`watch`、`reactive/ref` 常见误用。

## 不适用场景

- 纯样式调整，无状态逻辑修改。
- 仅写提交信息，不涉及代码实现。
- 仅做接口层封装，不涉及 Vue 组件行为。

## 硬约束（禁止/必须）

- 禁止直接修改 `props`，必须使用 `emit('update:xxx')`。
- 禁止在模板层写复杂业务逻辑，必须下沉到 `computed` 或 hook。
- 必须避免深层 watch 滥用，优先明确依赖源。
- 必须对异步请求做取消或竞态保护，避免旧请求覆盖新状态。
- 必须在复杂页面中拆 composable，禁止单文件耦合所有逻辑。
- 导出函数、composable、接口、类型与常量必须使用中文 JSDoc。
- 接口默认错误由 mutator 统一提示并 reject；业务逻辑只做状态恢复或错误转换，禁止在 `catch` 重复 `message.error`，除非请求显式设置了 `skipErrorHandler`。
- 在 hook/computed/watch 等业务逻辑里使用接口返回的 number 字段（id、主键、金额、数量等）时，禁止用 `Number()`/`parseInt`/`parseFloat`/`+x`/`*1`/`~~` 做任何数字转换，一律按字符串透传与比较；确需高精度数值计算时用 `decimal.js`/`big.js` 以字符串入参。底层 json-bigint 已存为字符串保精度，详见 `../api-integration/SKILL.md`「大数字与精度」。

## 标准代码骨架

```typescript
const props = defineProps<{ modelValue: string }>();
const emit = defineEmits<{ 'update:modelValue': [value: string] }>();

const localValue = computed({
  get: () => props.modelValue,
  set: value => emit('update:modelValue', value),
});

const loading = ref(false);

/** 请求数据并维护加载状态。 */
const fetchData = async () => {
  loading.value = true;
  try {
    await api();
  } finally {
    loading.value = false;
  }
};
```

## 交付检查清单

- [ ] `props` 单向数据流未被破坏。
- [ ] `v-model` 实现使用标准 `update:*` 事件。
- [ ] 异步逻辑具备 loading 与异常处理。
- [ ] 复杂逻辑已拆分到 composable。
- [ ] 接口返回的 number 字段在逻辑中保持字符串透传，未被 `Number()`/`parseInt`/`+x` 等转换。
- [ ] 模板表达式简洁，便于维护和测试。

## 失败兜底策略

- 响应式异常时，先定位是 `ref`/`reactive` 选型问题还是解构丢响应。
- 双向绑定异常时，先检查 `emit` 事件名和参数签名。
- 组件过重时，先抽离状态 hook，再处理视觉拆分。
