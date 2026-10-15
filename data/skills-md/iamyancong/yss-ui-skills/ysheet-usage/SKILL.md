---
name: ysheet-usage
description: 指导 YSS UI 协同表格、类 Excel 工作簿、Univer 电子表格使用 @yss-ui/components 的 YSheet；覆盖 optionalDependencies、@yss-ui/components/sheet 子路径、extraPresets/extraPlugins/extraLocales、IWorkbookData、只读与 Facade save/reload，避免把 Univer 运行时从主入口同步导入。
---

# YSheet 使用

## 触发条件

- 生成或修改协同表格、类 Excel 工作簿、Univer Sheet、筛选/数据校验 Preset 或只读电子表格。
- 需要配置 `YSheet` 的 `extraPresets`、`extraPlugins`、`extraLocales`、`config`、`IWorkbookData` 或 `save/reload`。

## 不适用场景

- 业务主列表、远程分页、操作列：使用 `../ytable-usage/SKILL.md`。
- 行内编辑明细表：使用 `../yedit-table-usage/SKILL.md`。
- 只要导出 Excel/CSV 文件流：使用 `../file-export-download/SKILL.md`。

## 实施流程

1. 当前会话可用 yss-ui MCP 时，先用 `get_component_docs` 查询 `YSheet` 的 Props、Events、Expose 与子路径导出；需要只读、筛选或数据校验时再用 `get_demo`。
2. MCP 不可用、调用失败或校正后仍无结果时，才读取最新 `llms-full.txt`；文档与当前依赖不一致时，以 `packages/components/src/sheet` 源码和 `package.json` 的 `exports`/`optionalDependencies` 为准。
3. 先确认只要核心表格还是要筛选/校验/绘图 Preset，再选择导入入口。
4. 给容器明确高度，用 `v-model` 绑定工作簿，需要持久化时调用 `save()`。

## 硬约束（禁止/必须）

- 基础用法从 `@yss-ui/components` 导入 `YSheet`（异步组件，未使用时不加载 Univer）。`LocaleType`、`IWorkbookData`、`YSheetProps`、`YSheetExpose` 也可从主入口导入。
- Univer Preset 运行时对象必须从 `@yss-ui/components/sheet` 导入，禁止业务代码直接 `import ... from '@univerjs/...'`，也禁止从主入口臆造 `UniverSheetsFilterPreset` 等符号。
- `@univerjs/*`、`react`、`react-dom`、`rxjs` 是 `@yss-ui/components` 的 **optionalDependencies**。安装组件库时会尝试拉取；未使用 YSheet 的项目缺包不应阻断安装。使用 YSheet 时保证私服能装到这些可选依赖，**不要**再让业务 `pnpm add` 一套 Univer 包，也**不要**把它们写进业务 `dependencies` 当普通必装项。
- Univer 扩展边界只有 `config`、`extraPresets`、`extraPlugins`、`extraLocales`。未声明的顶层属性不会透传给 Univer。
- `config` 是 `Partial<IUniverSheetsCorePresetConfig>`，与默认值合并且 `config` 优先。默认 `{ header: true, toolbar: true, footer: {}, contextMenu: true, formulaBar: true }`。`footer` 不能为 `true`，只能是 `false` 或对象。
- 必须给 YSheet 明确高度（数字会转成 `px`，字符串原样使用）；父级没有高度时不要只靠默认 `'100%'`。
- 没有公开插槽。禁止臆造 `#toolbar`、`#cell` 等插槽。
- 禁止直接改 `IWorkbookData` 对象来“刷新单元格”；运行时改数走 Univer Facade，持久化走 `save()`（会 `update:modelValue`）。
- `readonly` 会拦截键盘编辑、粘贴、拖拽、双击和右键入口；复制/撤销等修饰键组合仍允许。
- 语言缺省继承 `YConfigProvider`。核心包已注册简体/繁体/英文，切换调用 Facade `setLocale`，不重建工作簿。用户输入、工作表名、公式和数据不自动翻译。额外 Preset/插件必须经 `extraLocales` 提供对应词典。
- 组件卸载会自动 `dispose()`；不要在业务层再抄一套销毁逻辑，除非拿到了外部 `getUniverAPI()` 实例且自行创建了额外资源。

## 标准代码骨架

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { YSheet, type IWorkbookData } from '@yss-ui/components';

const sheetRef = ref<{ save: () => IWorkbookData | null } | null>(null);
const workbookData = ref<IWorkbookData | null>(null);

/** 把当前工作簿快照写回 v-model。 */
const handleSave = () => {
  const snapshot = sheetRef.value?.save();
  if (snapshot) {
    workbookData.value = snapshot;
  }
};
</script>

<template>
  <YSheet
    ref="sheetRef"
    v-model="workbookData"
    height="620px"
    locale="zh-CN"
    @error="() => undefined"
  />
</template>
```

启用筛选和数据校验时，改为从子路径导入 Preset 与语言包：

```typescript
import {
  LocaleType,
  UniverPresetSheetsDataValidationZhCN,
  UniverPresetSheetsFilterZhCN,
  UniverSheetsDataValidationPreset,
  UniverSheetsFilterPreset,
  YSheet,
} from '@yss-ui/components/sheet';

const extraPresets = [UniverSheetsFilterPreset(), UniverSheetsDataValidationPreset()];
const extraLocales = {
  [LocaleType.ZH_CN]: [UniverPresetSheetsFilterZhCN, UniverPresetSheetsDataValidationZhCN],
};
```

```vue
<YSheet
  v-model="workbookData"
  height="560px"
  :readonly="readonly"
  :config="{ header: false, toolbar: true, formulaBar: true, footer: { sheetBar: true } }"
  :extra-presets="extraPresets"
  :extra-locales="extraLocales"
/>
```

子路径当前还可导出 `UniverSheetsDrawingPreset` / `UniverPresetSheetsDrawingZhCN`。`extraPlugins` 接受插件类或 `[插件类, 配置]`。

## 交付检查清单

- [ ] 基础 `YSheet` 从 `@yss-ui/components` 导入；Preset/插件运行时从 `@yss-ui/components/sheet` 导入。
- [ ] 未从 `@univerjs/*` 直接导入，也未要求业务重复安装 optionalDependencies。
- [ ] 只使用 `config/extraPresets/extraPlugins/extraLocales` 扩展 Univer，没有虚构顶层 Props 或插槽。
- [ ] 容器有明确高度；持久化走 `save()`，没有原地改工作簿 JSON。
- [ ] 额外 Preset 已配套 `extraLocales`，`footer` 未写成 `true`。

## 失败兜底策略

- 页面能装组件库但 YSheet 白屏/加载失败：先确认 optionalDependencies 是否安装成功，而不是改成从主入口同步 import Univer。
- 需要筛选/校验却没有 UI：检查是否从 `@yss-ui/components/sheet` 引入对应 Preset，并传入 `extraPresets` + `extraLocales`。
- 高度为 0 或不渲染：给父容器或 `height` 明确像素/`%` 值。
- 改了 `workbookData` 字段但画布不变：改为 `reload(data)` 或 Facade API，不要假设深层对象变异会自动刷新。
