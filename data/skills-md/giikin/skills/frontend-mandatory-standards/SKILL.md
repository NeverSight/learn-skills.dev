---
name: frontend-mandatory-standards
description: 【必读·强制】公司前端开发强制规范。编写或修改任何前端代码前必须先阅读本技能。涵盖 Composition API 强制规范、命名约定、接口调用规则、Pinia 状态管理、组件拆分等全部开发约束。
---

# 前端开发规范

## 技术栈

- **语言**：TypeScript
- **框架**：Vue 3 Composition API (`<script setup>`)
- **CSS**：Tailwind CSS（避免使用 `<style>` 标签，Tailwind class 覆盖不了的场景除外）
- **状态管理**：Pinia
- **UI 框架**：Giime（基于 Element Plus 增强，`el-*` → `gm-*`）

## 命名规范

| 场景             | 风格         | 示例                                 |
| ---------------- | ------------ | ------------------------------------ |
| 类型/接口        | PascalCase   | `UserInfo`, `ApiResponse`            |
| 变量/函数/文件夹 | camelCase    | `userName`, `handleSubmit()`         |
| 环境常量         | UPPER_CASE   | `VITE_BASE_URL`                      |
| 组件文件         | PascalCase   | `UserProfile.vue`                    |
| Composables      | use 前缀     | `useUserInfo`, `useFormValidation`   |
| 布尔值           | 辅助动词前缀 | `isLoading`, `hasError`, `canSubmit` |
| 事件处理         | handle 前缀  | `handleClick`, `handleSubmit`        |

**变量命名**：避免 `data`/`info`/`list`/`result`/`status` 等通用名称，使用 `formData`/`userInfo`/`taskList` 等具体业务名称。

## 通用编码规则

- **注释**：每个方法和变量添加 JSDoc 注释，使用中文；函数内部添加适量单行中文注释
- **函数声明**：优先使用 `const` 箭头函数而非 `function`，除非需要重载
- **异步**：优先 `async/await`，不用 Promise 链式调用
- **现代 ES**：优先使用 `?.`、`??`、`Promise.allSettled`、`replaceAll`、`Object.groupBy` 等
- **守卫语句**：条件提前退出，减少嵌套深度
- **函数参数**：1-2 个主参数 + options 对象，避免参数超长

```ts
// ✅ 函数参数设计示例
const urlToFile: (url: string, options?: FileConversionOptions) => Promise<File>;
```

- **工具库优先**：减少造轮子
  - **日期**：`dayjs`
  - **Vue 工具**：`vueuse`（`tryOnMounted`、`useEventListener`、`useLocalStorage` 等）
  - **数据处理**：`lodash-es`（`compact`、`cloneDeep`、`uniqBy` 等 ES 未提供的方法）
- **Git 操作**：不要操作 git 命令，除非用户明确要求
- **格式化**：修改后执行 `npx eslint --fix <文件路径>`
- **类型检查**：执行 `npx vue-tsc --noEmit -p tsconfig.app.json`

更多示例见 [coding-conventions.md](references/coding-conventions.md)

## Composition API 规范

### 1. 减少 watch，优先事件绑定

watch 是隐式依赖，难以追踪变更来源。优先在事件回调中直接处理逻辑，数据流更清晰：

```ts
// ❌ 隐式监听，难以定位谁触发了变更
watch(count, () => {
  console.log('changed');
});

// ✅ 在事件中直接处理，数据流清晰
const handleCountChange = () => {
  console.log('changed');
};
// <gm-input v-model="count" @change="handleCountChange" />
```

### 2. 使用 defineModel

Vue 3.4+ 引入的 `defineModel` 将 props + emit + computed 三件套简化为一行，减少样板代码：

```ts
// ❌ 三件套写法，样板代码多
const props = defineProps<{ modelValue: string }>();
const emit = defineEmits<{ 'update:modelValue': [value: string] }>();

// ✅ defineModel 一行搞定
const value = defineModel<string>({ required: true });
```

### 3. 使用 useTemplateRef

Vue 3.5+ 推荐使用 `useTemplateRef` 获取模板引用，类型安全且避免 ref 变量名与模板 ref 属性名耦合：

```ts
// ❌ 变量名必须与 template 中的 ref="inputRef" 完全一致
const inputRef = ref<FormInstance | null>(null);
```

```ts
// ✅ 类型安全，解耦变量名和模板 ref
const inputRef = useTemplateRef('inputRef');
```

### 4. 优先 ref，避免无理由 reactive

`reactive` 在解构时会丢失响应性，整体替换时需要逐字段赋值。`ref` 行为更可预测，通过 `.value` 可以直接整体替换：

```ts
// ❌ reactive 解构丢失响应性，整体替换需 Object.assign
const profileData = reactive({ name: '', age: 0 });
```

```ts
// ✅ ref 行为统一，profileData.value = newData 即可整体替换
const profileData = ref({ name: '', age: 0 });
```

### 5. Props 直接解构

Vue 3.5+ 支持 `defineProps` 解构时保持响应性并设置默认值，`withDefaults` 已不再需要：

```ts
// ❌ withDefaults 在 Vue 3.5+ 已不必要
const props = withDefaults(defineProps<{ size?: number }>(), { size: 10 });

// ✅ 直接解构，简洁且响应式
const { size = 10 } = defineProps<{ size?: number }>();
```

### 6. Dialog 暴露 openDialog

弹窗组件通过 `defineExpose` 暴露 `openDialog` 方法，父组件通过 ref 调用，避免通过 props 控制 visible 导致的状态同步问题：

```ts
const dialogVisible = ref(false);

const openDialog = (data?: SomeType) => {
  dialogVisible.value = true;
};

defineExpose({ openDialog });
```

### 7. 自动导入，不要显式 import Vue API

`ref`、`computed`、`watch`、`onMounted` 等已通过 `unplugin-auto-import` 自动导入。显式 `import { ref } from 'vue'` 会产生冗余代码，且与项目配置不一致。

### 8. 样式用 Tailwind CSS

所有样式通过 Tailwind 的 class 实现。只有 Tailwind 无法覆盖的场景（如深度选择器 `:deep()`、复杂动画）才使用 `<style>`。

### 9. 配置数据抽离

选项列表、表单规则、tableId 等与页面逻辑无关的配置数据，在 `modules/**/composables/useXxxOptions.ts` 中抽离，保持组件专注于交互逻辑：

```ts
export const useXxxOptions = () => {
  const tableId = 'xxx-xxx-xxx-xxx-xxx';
  const xxxOptions = [{ label: '选项1', value: 1, tagType: 'primary' as const }];
  const rules = {
    xxx: [{ required: true, message: 'xxx不能为空', trigger: 'blur' }],
  };

  return { tableId, xxxOptions, rules };
};
```

### 10. 组件代码结构

统一使用 `template` → `script` → `style` 顺序。

## 代码拆分规范

每次向已有 `.vue` 文件添加新功能、或创建新模块时，都应首先阅读 [directory-structure.md](references/directory-structure.md) 了解拆分原则。

### 何时触发拆分

| 触发场景                                   | 操作                                                                                                     |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| **新建增删改查模块**                       | **先阅读** [crud.md](references/crud/crud.md) 学习完整的 CRUD 代码模板和文件拆分方式，按模板生成所有文件 |
| **向已有页面添加功能**（新增表单、弹窗等） | 先检查当前文件行数，超过 300 行应拆分；评估新增内容是否应作为独立子组件                                  |
| **新建模块/页面**                          | 先规划目录结构（`components/`、`composables/`、`stores/`），按功能区域预拆分                             |
| **修改迭代已有功能**                       | 如果发现当前文件已臃肿（>300 行），在完成需求的同时顺带拆分，不要让文件继续膨胀                          |

### 核心原则

- **一般 `.vue` 文件不超过 300 行**：除入口级别文件（如 `index.vue`）外，子组件、弹窗等文件应控制在 300 行以内
- **入口文件可适当放宽**：`index.vue` 作为模块入口承担编排职责，行数可适当超出，但也应尽量精简
- **按功能区域拆分 UI 组件**：每个独立的功能区域（搜索栏、表格、弹窗、表单区等）应作为独立子组件
- **核心业务逻辑保留在 `index.vue`**：主页面负责数据获取、状态管理、子组件编排
- **UI 展示逻辑下沉到子组件**：子组件只负责渲染和用户交互
- **避免过度传参**：当 props 层级超过 2 层时，使用 Pinia 替代深层 props 传递

### 标准模块目录结构

```
modules/xxx/
├── index.vue                    # 主页面（编排子组件、管理数据）
├── components/                  # UI 子组件
│   ├── Search.vue
│   ├── Table.vue
│   └── EditDialog.vue
├── composables/                 # 逻辑复用
│   └── useXxxOptions.ts
└── stores/                      # 状态管理（需要时）
    └── useXxxStore.ts
```

详细的拆分策略、示例代码和 Props 传递原则见 [directory-structure.md](references/directory-structure.md)

## 接口调用规范

### 文件限制

`/src/api` 下的文件由代码生成工具自动生成，可以简单修改但**不能新建和删除**。

### 文件结构

每个接口生成两个文件：

- `postXxxYyyZzz.ts` — 原始 axios 方法
- `usePostXxxYyyZzz.ts` — useAxios 响应式封装

文件名通过 "请求方法+路由地址" 生成：`post /open/v1/system/list` → `postOpenV1SystemList.ts` + `usePostOpenV1SystemList.ts`

### 选择规则

| 场景          | 使用版本                  | 原因                                                  |
| ------------- | ------------------------- | ----------------------------------------------------- |
| 默认          | `useXxx` 封装版本         | 提供响应式数据（`data`、`isLoading`）和自动取消竞态   |
| 循环/批量请求 | 原始版本（无 `use` 前缀） | `useAxios` 会取消前次请求，循环调用时只有最后一个生效 |

```ts
// ✅ 默认：useAxios 封装
const { exec: getListExec } = usePostXxxV1ListPage();

await getListExec();
```

```ts
// ✅ 批量：原始接口 + Promise.all
await Promise.all(ids.map(id => deleteXxxV1Item({ id })));
```

### API 导入规则

所有接口和类型统一从 `controller/index.ts` 或 `interface/index.ts` 导入，降低耦合度，方便后期重构：

```ts
// ✅ 从 controller 统一导入
import type { PostGmpV1CrowdListInput } from '@/api/gmp/controller';
import { postGmpV1CrowdList } from '@/api/gmp/controller';
```

```ts
// ✅ 公共类型从 interface 导入
import type { CrowdItemVo } from '@/api/gmp/interface';
```

```ts
// ❌ 不要从具体文件导入
import { postGmpV1CrowdDetail } from '@/api/gmp/controller/RenQunGuanLi/postGmpV1CrowdList';
```

### 错误处理

- **无需 try/catch**：`createAxios` 拦截器自动弹出错误提示，业务代码不需要手动 catch
- **无需判断 code**：非正常响应码会被拦截器自动 reject，不需要 `if (code !== 200)`
- **需要 finally 时**：使用 try/finally（不写 catch），用于清理副作用

### 使用流程

1. 如果提供了接口地址，第一步找到 `@/api/xxx/controller` 中定义的请求方法
2. 仔细阅读接口文件中的类型定义，不要自己编参数
3. 根据场景选择 `useXxx` 版本或原始版本
4. 下拉框、单选框等数据源可从接口文档注释获取，获取后在 `useXxxOptions` 中抽离复用

更多用法示例见 [api-conventions.md](references/api-conventions.md)

## Pinia 状态管理

### Store 文件组织

```
modules/xxx/
├── stores/
│   └── useXxxStore.ts    # 模块专用 store
└── index.vue
```

### 何时使用

Pinia 适合跨多层组件共享状态、异步任务轮询等场景。不要过度使用——只在父子组件间传递的数据用 props/emits，局部状态用 ref，简单表单数据用 v-model。

### 使用规范

```ts
// 命名体现业务含义，不要用 const store = useXxxStore
const xxxStore = useXxxStore();

xxxStore.resetStore(); // 进入页面时重置，确保干净状态
```

### 跨组件共享状态

当组件嵌套超过 2 层且需要共享状态时，用 Pinia 替代 props 层层传递：

```
index.vue → Result.vue → ResultSuccess.vue → ImageSection.vue
                    ↓
              各组件直接访问 store，不需要 props 逐层传递
```

Store 标准写法、轮询任务模式等见 [pinia-patterns.md](references/pinia-patterns.md)

## 参考文档

| 主题              | 说明                                                 | 参考                                                        |
| ----------------- | ---------------------------------------------------- | ----------------------------------------------------------- |
| **CRUD 代码模板** | **新建增删改查页面时必读**，完整的文件拆分和代码模板 | [crud.md](references/crud/crud.md)                          |
| 编码约定详解      | 守卫语句、函数参数设计、工具库用法等完整示例         | [coding-conventions.md](references/coding-conventions.md)   |
| 接口调用指南      | useAxios 用法、类型定义、导入规则完整说明            | [api-conventions.md](references/api-conventions.md)         |
| Pinia 使用模式    | Store 创建、重置、跨组件共享等模式                   | [pinia-patterns.md](references/pinia-patterns.md)           |
| 组件拆分规范      | 何时拆分、目录结构、Props 传递原则                   | [directory-structure.md](references/directory-structure.md) |
| 字典模块规范      | useDictionary、Store 创建、命名规范                  | [dictionary.md](references/dictionary.md)                   |
| 环境变量配置      | .env 分层原则、域名规则、多环境构建                  | [env.md](references/env.md)                                 |
