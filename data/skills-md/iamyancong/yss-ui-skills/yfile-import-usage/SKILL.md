---
name: yfile-import-usage
description: 指导 YSS UI 文件导入弹窗、两步导入流程使用 @yss-ui/components 的 YFileImport；覆盖选择文件、nextStep.onSuccess、importResult、loadings、downloadTemplate 事件和结果插槽，避免与导出下载或普通 Upload 混淆。
---

# YFileImport 使用

## 触发条件

- 生成或修改文件导入弹窗、Excel/CSV 导入向导、两步导入（选择文件 → 结果确认）。
- 需要配置 `YFileImport` 的 `nextStep`、`finalImport`、`importResult`、`loadings`、`fileTypeList` 或 `#result` 插槽。

## 不适用场景

- 导出报表、下载 Blob、解析 `Content-Disposition`：使用 `../file-export-download/SKILL.md`。
- 只要一个普通附件 Upload 字段、没有导入向导弹窗。
- 浏览器预览远程文件，不走导入确认流程。

## 实施流程

1. 当前会话可用 yss-ui MCP 时，先用 `get_component_docs` 查询 `YFileImport` 的 Props、Events、Slots、Expose；需要两步流程、失败数据或 Formily 按钮打开时再 `get_demo`。
2. MCP 不可用或无结果时读取最新 `llms-full.txt`；仍不一致则以 `packages/components/src/file-import` 源码为准。
3. 用 `v-model` 控制弹窗可见性；在 `nextStep` 里做预检，成功后调用 `onSuccess()` 进入结果步。
4. 模板下载、失败数据下载走 `../file-export-download/SKILL.md` 的 Blob 链路，不要在导入组件里手写 `createObjectURL`。

## 硬约束（禁止/必须）

- 从 `@yss-ui/components` 导入 `YFileImport`；类型可导入 `YFileImportProps`、`FileImportTexts`、`ImportResult`。`FILE_IMPORT_LOADING_NAME`、`YFileImportEmit` **不是**公开运行时导出，loading 名用字符串字面量。
- 组件内部 `beforeUpload` 恒为 `false`，不会按 `action` 自动上传。文件留在 `fileList` 里，由业务在 `nextStep` / `finalImport` 提交。
- `drag`、`autoUpload` 只是历史兼容字段：上传区固定 `Upload.Dragger`，也不会自动上传。直传请用 `uploadProps.customRequest`。
- 两步流程：`nextStep` 通过本地校验后才会 emit。载荷含 `fileList`、`close`、`loadingName: 'nextStep'` 和 **`onSuccess`**。必须在业务预检成功后调用 `onSuccess()`，否则不会进入结果步。文档事件表若漏了 `onSuccess`，以源码为准。
- `loadings` 是字符串数组。合法标识：`'downloadTemplate'`、`'nextStep'`、`'finalImport'`、`'exportErrorData'`。往数组里加减这些名字来控制按钮 loading。
- `importResult.successkey` 为真时结果步显示“确认导入”；`failkey` 为真时显示“下载失败数据”。数字字段 `success/fail/total` 只用于展示。打开弹窗会 `reset()` 回到选文件步，因此结果要在 `onSuccess` 之后再展示，不要指望默认 demo 值当真实导入结果。
- `fileTypeList` 用来拼 `accept` 和扩展名校验（如 `xls` → `.xls`）。一旦传入 `accept`，组件不再做扩展名校验。
- 浮层 `getContainer` 固定 `document.body`。Modal 扩展只走 `modalProps`，Upload 扩展只走 `uploadProps`。
- 插槽：`#uploader`（`{ fileList, accept, multiple }`）、`#result`（`{ result }`）、`#footer-left`、`#footer-right`。文档与 Demo 用 kebab-case。
- Expose：`open()` / `close()` / `reset()`。受控场景优先 `v-model`。
- Formily 已注册 `YFileImport`，但导入弹窗应作为页面兄弟组件，用 Schema 按钮通过 scope 打开；不要把它当成普通表单项。
- `downloadTemplate` / `exportErrorData` 只负责发出事件；真正落盘必须按导出 Skill 处理 Blob。Orval 错误由 mutator 提示，不要在这些 handler 里重复 `message.error`。

## 标准代码骨架

```vue
<script setup lang="ts">
import { ref } from 'vue';
import { YButton, YFileImport, type ImportResult } from '@yss-ui/components';

const visible = ref(false);
const loadings = ref<string[]>([]);
const importResult = ref<ImportResult>({
  successkey: '',
  failkey: '',
  success: 0,
  fail: 0,
  total: 0,
});

const setLoading = (name: string, on: boolean) => {
  loadings.value = on ? [...loadings.value, name] : loadings.value.filter(item => item !== name);
};

/** 预检通过后必须调用 onSuccess 才能进入结果步。 */
const handleNextStep = async (payload: {
  loadingName: string;
  fileList: Array<{ originFileObj?: File }>;
  onSuccess: () => void;
}) => {
  setLoading(payload.loadingName, true);
  importResult.value = { successkey: 'ok', failkey: '', success: 2, fail: 0, total: 2 };
  payload.onSuccess();
  setLoading(payload.loadingName, false);
};

/** 确认导入；接口错误交给 mutator。 */
const handleFinalImport = async (payload: { loadingName: string; close: () => void }) => {
  setLoading(payload.loadingName, true);
  payload.close();
  setLoading(payload.loadingName, false);
};

/** 下载导入模板：实际 Blob 处理见 file-export-download。 */
const handleDownloadTemplate = async (payload: { loadingName: string }) => {
  setLoading(payload.loadingName, true);
  setLoading(payload.loadingName, false);
};
</script>

<template>
  <YButton type="primary" @click="visible = true">导入</YButton>
  <YFileImport
    v-model="visible"
    :file-type-list="['xls', 'xlsx', 'csv']"
    :loadings="loadings"
    :import-result="importResult"
    @next-step="handleNextStep"
    @final-import="handleFinalImport"
    @download-template="handleDownloadTemplate"
  />
</template>
```

## 交付检查清单

- [ ] `nextStep` 成功路径调用了 `onSuccess()`。
- [ ] `loadings` 使用真实字符串标识；`importResult` 的 `successkey`/`failkey` 与按钮显隐一致。
- [ ] 没有依赖 `autoUpload`/`action` 自动上传，也没有从包里导入内部常量。
- [ ] 模板/失败数据下载走 Blob 工具，没有重复 `message.error`。
- [ ] 插槽使用 kebab-case；Formily 场景是兄弟弹窗而不是表单字段。

## 失败兜底策略

- 点了下一步还停在选文件：检查是否调用 `onSuccess()`，以及 `fileTypeList`/`accept` 校验是否拦截。
- 结果步没有确认按钮：给 `importResult.successkey` 非空值。
- 选择文件后浏览器直接上传：不要传会触发默认上传的 `uploadProps`；保持组件拦截，自己在事件里提交。
- 打开弹窗仍显示上次结果：这是 `modelValue` 变 `true` 时 `reset()` 的预期行为，先走完 `nextStep` 再展示结果。
