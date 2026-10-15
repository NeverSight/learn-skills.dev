---
name: page-skeleton
description: 指导搭建 Vue3 YSS UI 列表、表单、详情和弹窗页面模块骨架，统一 index.vue、constant.ts、style.less、hooks 与私有组件职责；当新建页面或需要拆分超过 150 行的业务组件时使用。
---

# Page Skeleton Skill

## 触发条件

- 新建业务页面模块（列表、表单、详情、弹窗任意组合）。
- 需要快速搭建目录结构、类型文件、hooks、组件分层。
- 需要把页面代码控制在可维护结构，而不是单文件堆叠。

## 不适用场景

- 仅补一个局部交互逻辑，不涉及页面骨架重建。
- 仅改 API 请求细节：使用 `../api-integration/SKILL.md`。
- 仅做 Formily 细节：使用 `../formily-*` 系列 skill。

## 硬约束（禁止/必须）

- 开发前必须先执行组件选型：`../component-selection-imports/SKILL.md`。
- 页面目录默认拆分：`index.vue + constant.ts + style.less + hooks/`；存在多个私有视图或大量独立类型时再增加 `components/` 和 `type.ts`。
- `index.vue` 只做 hooks 组合和视图编排，原则上控制在 150 行以内；超过 150 行或包含多个独立职责时必须拆分。
- 表格列超过 10 行时放入 `constant.ts`；状态、API 调用、副作用和事件处理放入 `hooks/useXxx.ts`。
- 所有样式放入 `style.less`，SFC 只保留 `<style scoped lang="less">@import './style.less';</style>`。
- 所有导出函数、hooks、类型和静态配置必须有中文 JSDoc。
- 表单方案默认用 `YFormily`；分步场景默认用 `formily-step-flow`。
- 不得导入 `@formily/antdv` 作为业务 UI 方案。

## 标准代码骨架

```text
packages/src/views/{ModuleName}/
├── index.vue
├── constant.ts
├── style.less
├── hooks/
│   ├── use{Module}List.ts
│   └── use{Module}Form.ts
├── type.ts              # 独立类型较多时增加
└── components/          # 存在多个私有视图时增加
    ├── {Module}Table.vue
    └── {Module}Modal.vue
```

```vue
<script setup lang="ts">
import { useModuleList } from './hooks/useModuleList';
import { useModuleForm } from './hooks/useModuleForm';

const list = useModuleList();
const form = useModuleForm({ onSuccess: list.fetchData });
</script>
```

## 交付检查清单

- [ ] 目录拆分完整，职责清晰。
- [ ] `index.vue` 不超过 150 行，且仅负责组合和渲染。
- [ ] 类型定义与常量已抽离，不在页面内硬编码。
- [ ] hooks 可复用且命名清晰（`useXxx`）。
- [ ] 样式已抽离到 `style.less`，SFC 样式块已 scoped。
- [ ] 页面导入组件来源符合组件选型规则。
- [ ] 若包含表单，已选择对应 Formily skill。

## 失败兜底策略

- 当需求不清晰时，先落地最小骨架（列表区 + 操作区 + 弹窗占位），再增量填充。
- 当页面复杂度超预期时，优先继续拆 hooks 和私有组件，而不是在 `index.vue` 堆逻辑。
- 若组件是否封装存在歧义，回退到 `component-selection-imports` 先判定导入来源。

## 示例

- `./examples/StandardListPage/`
- `./examples/AdvancedFormPage/`
