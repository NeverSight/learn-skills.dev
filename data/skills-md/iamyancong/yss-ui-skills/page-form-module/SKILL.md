---
name: page-form-module
description: 指导实现 YSS UI 新增、编辑和查看表单模块，覆盖 YFormily Schema、mode 0/1/2、详情渲染、数据回显与回填、表单值被意外清空排查、校验、提交 loading、弹窗销毁和列表刷新；当页面包含表单页、Modal 或 Drawer 表单，或编辑时回显丢失、提交后表单未重置时使用。
---

# Page Form Module Skill

## 触发条件

- 实现新增、编辑、查看表单页，或 Drawer/Modal 中的表单闭环。
- 需要处理 Schema、mode 0/1/2、回填、校验、提交和成功后列表刷新。

## 不适用场景

- 页面只包含列表查询，不包含任何表单编辑。
- 表单为分步流程：使用 `formily-step-flow`。
- 仅修复单个联动表达式：使用 `formily-linkage-effects`。

## 必读依赖

- 表单基础：`../formily-foundation/SKILL.md`
- 联动副作用：`../formily-linkage-effects/SKILL.md`
- 模式与详情：`../formily-mode-slot-detail/SKILL.md`
- 分步表单：`../formily-step-flow/SKILL.md`
- 接口与错误处理：`../api-integration/SKILL.md`

## 文档检索

1. MCP 可用时，先用 `get_component_docs` 查询 `YFormily` 的 `mode`、`detail-options`、实例提交与回填 API，再按场景用 `get_demo` 获取 `formily/modes`、`formily/group`、`formily/linkage` 或 `formily/steps` 示例。
2. 精确查询无结果时，先用 `search_docs` 或 `list_components` 校正名称；仅在 MCP 不可用、调用失败或校正后仍无结果时，回退读取最新 `llms-full.txt`。文档版本与当前依赖不一致时，再核对当前源码、CodeGraph 和真实导出。
3. 当前会话已经加载上述本地 Skill 时，不要再通过 MCP 重复查询同一 Skill；仅在依赖 Skill 缺失时使用 `list_skills`、`get_skill` 补齐规则。

## 硬约束（禁止/必须）

- 提交前必须调用 `formRef.submit()` 或 `Submit.onSubmit` 进入完整校验链路。
- `open/mode/currentId/formModel/submitting` 和回填、提交、关闭方法收敛在同一 Hook。
- **数据前置同步原则（必守）**：表单数据必须在 `openCreate`/`openEdit` 触发前**同步赋好 `formModel.value`**；**严禁**在弹窗/抽屉组件内部通过 `watch(visible) + await nextTick() + initForm()` 异步回填数据（会导致首次编辑正常，切换新增再编辑时因时序差读取到残留空对象导致回显变空白的经典 Bug）。
- **单一信任源**：使用 `v-model="formModel"` + `ref="formRef"` 调用 `submit()` 驱动；**严禁**在组件顶层写 `const form = createForm()` 与 `v-model`、`form.setValues`、`form.reset` 混用。
- **禁止滥用动态 `:key`**：**严禁**在 `YFormily`/`YssFormily` 上使用 `:key="isEdit ? 'edit' : 'create'"` 等强制 Remount，应直接通过 `:mode` 或响应式数据驱动。
- **弹窗生命周期隔离**：Modal/Drawer 必须配置 `:destroy-on-close="true"`，且内部 `YFormily` 必须使用 `v-if="open"` 随容器打开挂载、关闭销毁，避免宽度为 0 导致栅格退化，并彻底回收脏状态。
- 新增/编辑/查看使用 `YFormily :mode="mode"`，`mode=2` 不渲染保存按钮。
- Drawer 默认使用响应式宽度；基础表单设置 `FormLayout { labelWidth: 140, labelAlign: 'right' }`。
- Drawer/Modal 中的 `FormGrid` 默认使用 `maxColumns: 2`、`minColumns: 1`、`minWidth: 320~360`；禁止 `minColumns: 2` 锁死两列。
- 备注、说明和长文本通过 `x-decorator-props.gridSpan` 跨满整行。
- 下拉选择器异步数据源必须使用 `enum` 或 `x-reactions` / `field.dataSource` 注入，严禁写入 `x-component-props.options`；基础字典下拉优先在弹窗打开前 `await` 拉取完成或在页面初始化提前拉取。
- **表单校验规则规范**：必填文本字段声明 `whitespace: true`（如 `{ required: true, whitespace: true, message: '请输入xxx' }`）；自定义长度与格式校验必须使用条件式函数，空值放行交由 `required` 报错，非空才校验具体规则，禁止多个自定义校验重复承担必填职责。YFormily 适配层虽会归一化反馈展示，但不能代替正确的 Schema 语义。
- **弹窗/抽屉表单国际化规范（Critical）**：
  - 在支持国际化的项目中，弹窗/抽屉的标题必须接入多语言（如 `:title="mode === 0 ? t('common.create') : mode === 1 ? t('common.edit') : t('common.view')"`）；
  - 容器底部操作按钮文案（确认/取消/关闭）必须使用 `t('common.confirm')`、`t('common.cancel')`、`t('common.close')`；
  - 表单 Schema 采用 `createFormSchema(t)` 工厂函数结合 `computed` 驱动，字段标题、占位符、枚举选项及校验文案无硬编码中文。
- 长整型 ID 按字符串原样回填和提交，禁止 `Number()`/`parseInt()`；表单中的普通数值按生成 DTO 真实类型处理。
- 禁止使用 `if (res?.success)` 包裹保存成功逻辑，也禁止在 `catch` 重复 `message.error`。

## 标准代码骨架

```typescript
import { ref } from 'vue';

/** 默认表单模型 */
const createDefaultModel = () => ({
  name: '',
  code: '',
  description: '',
});

/** YFormily 业务侧仅需的实例方法。 */
interface FormilyFormRef {
  submit: () => Promise<Record<string, unknown>>;
}

/** 管理表单的模式、可见性、数据模型与提交链路。 */
export const useRuleForm = (onSuccess: () => void) => {
  const open = ref(false);
  const mode = ref<0 | 1 | 2>(0);
  const currentId = ref<string>();
  const formModel = ref(createDefaultModel());
  const submitting = ref(false);
  const formRef = ref<FormilyFormRef>();

  /** 打开新增：同步赋空值 */
  const openCreate = (): void => {
    mode.value = 0;
    currentId.value = undefined;
    formModel.value = createDefaultModel();
    open.value = true;
  };

  /** 打开编辑：同步赋目标行数据，前置完成回填 */
  const openEdit = (record: Record<string, any>): void => {
    mode.value = 1;
    currentId.value = record.id;
    formModel.value = {
      name: record.name ?? '',
      code: record.code ?? '',
      description: record.description ?? '',
    };
    open.value = true;
  };

  /** 关闭并清理 */
  const close = (): void => {
    open.value = false;
    formModel.value = createDefaultModel();
  };

  /** 校验并保存表单。 */
  const submit = async (): Promise<void> => {
    if (mode.value === 2 || submitting.value || !formRef.value) return;

    submitting.value = true;
    try {
      const values = await formRef.value.submit();
      await saveRule({ ...formModel.value, ...values, id: currentId.value });
      close();
      onSuccess();
    } catch {
      // Formily 校验反馈或 mutator 已展示错误，此处不重复 Toast。
    } finally {
      submitting.value = false;
    }
  };

  return { open, mode, currentId, formModel, submitting, formRef, openCreate, openEdit, close, submit };
};
```

`saveRule` 必须替换为当前 Orval 真实生成方法，不得照抄占位名。

```vue
<YFormily
  v-if="open"
  ref="formRef"
  v-model="formModel"
  :schema="schema"
  :mode="mode"
  :detail-options="{ bordered: true, maxColumns: 2, minColumns: 1, minWidth: 320 }"
/>
```

```typescript
/** Drawer 表单的基础布局 Schema。 */
export const drawerFormLayout = {
  type: 'void',
  'x-component': 'FormLayout',
  'x-component-props': { layout: 'horizontal', labelWidth: 140, labelAlign: 'right' },
  properties: {
    grid: {
      type: 'void',
      'x-component': 'FormGrid',
      'x-component-props': { maxColumns: 2, minColumns: 1, minWidth: 340, columnGap: 24, rowGap: 16 },
      properties: {},
    },
  },
};
```

## 交付检查清单

- [ ] `mode=0/1/2` 语义、回填和查看态渲染正确。
- [ ] 提交先校验，又防重入，loading 始终在 `finally` 恢复。
- [ ] Drawer/Modal 内 `YFormily` 按可见性条件挂载与销毁。
- [ ] label 宽度和右对齐一致，FormGrid 能从 2 列响应式收缩为 1 列。
- [ ] 长字段已跨行，长整型 ID 未转 number。
- [ ] 没有 `if (res?.success)` 和重复错误 Toast。
- [ ] 国际化多语言规范：在支持国际化的项目中，弹窗标题、确认/取消按钮、表单 Schema（字段标题、占位符、枚举选项、校验规则）无硬编码中文，均使用多语言工厂函数与词条。
- [ ] 成功后关闭表单并通知上层刷新。
- [ ] 业务层未导入 `@formily/antdv` UI 组件。

## 失败兜底策略

- 提交无响应时，先确认 `submit()` 是否实际调用并查看 Formily 校验反馈。
- 编辑回填异常时，核对真实 DTO、字段路径与 Schema path，不在模板散落转换。
- 表单过大时，拆分 Schema 生成函数、字典 Hook 和提交 Hook，保持 `index.vue` 不超过 150 行。
