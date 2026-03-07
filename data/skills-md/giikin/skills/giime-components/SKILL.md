---
name: giime-components
description: 【必读·强制】Giime 组件库强制使用规范。编写或修改任何涉及 UI 组件的前端代码前必须先阅读本技能。涵盖 gm-* 组件增强特性、GmConfirmBox/GmMessage/GmCopy 等插件用法、常用代码模式及 MCP 文档获取方式。
---

# Giime 组件库使用规范

Giime 是基于 Element Plus 扩展和增强的内部组件库，所有 `el-` 组件都有对应的 `gm-` 版本。未列出的 `gm-*` 组件与 `el-*` 行为一致，可直接替换使用。

## 使用原则

1. **优先 Giime**：`el-button` → `gm-button`，`el-table` → `gm-table`，以此类推。Giime 在 Element Plus 基础上统一了默认行为（如自动 loading、默认 filterable），直接使用可以减少重复配置。
2. **特殊需求**：Giime 无法满足时可用 Element Plus 原生组件。
3. **旧代码兼容**：旧代码保持原样，新代码按本规范编写。
4. **二次确认用 `GmConfirmBox`**：删除等危险操作使用 `GmConfirmBox`，它会自动处理确认按钮的 loading 和禁用状态，避免重复提交。
5. **复制用 `GmCopy`**：`GmCopy` 自动处理剪切板 API 兼容性并提示成功/失败，无需手写 try-catch。
6. **消息提示用 `GmMessage`**：`GmMessage` 默认合并相同消息（`grouping: true`），避免短时间内弹出大量重复提示，体验优于 `ElMessage`。

## 核心增强特性（gm-\* vs el-\*）

以下组件相对于 Element Plus 有**增强行为**，使用时需了解差异：

| 组件              | 增强内容                                                                           |
| ----------------- | ---------------------------------------------------------------------------------- |
| `gm-button`       | 异步 `@click` 自动处理 loading；disabled 时自动 type='info'；自动 Clarity 事件追踪 |
| `gm-select`       | 默认 `filterable: true`；推荐使用 `:options` 传入选项                              |
| `gm-cascader`     | 默认 `filterable: true`                                                            |
| `gm-table`        | 新增 `tableId` 属性（注入 TableCtx）；默认 `scrollbarAlwaysOn: true`               |
| `gm-upload`       | 支持 `v-model:fileList` 双向绑定                                                   |
| `gm-image`        | 新增下载进度、默认工具栏（缩放/旋转/下载）、`download()` 方法                      |
| `gm-image-viewer` | 同 `gm-image`，新增下载进度和默认工具栏                                            |
| `gm-popover`      | 新增 `before-enter`/`before-leave`/`after-enter`/`after-leave` 事件                |
| `GmMessage`       | 默认 `grouping: true`（相同消息合并）；支持全局 `plain` 配置                       |
| `GmMessageBox`    | alert 默认禁止 Esc 和遮罩关闭；confirm/prompt 默认显示取消按钮                     |
| `GmConfirmBox`    | 二次确认弹窗，自动处理确认按钮 loading 和禁用                                      |
| `GmCopy`          | 复制到剪切板，自动提示成功/失败                                                    |

> **注意**：`gm-select-v2` 未默认开启 `filterable`，与 `gm-select` 不同。

## 常用代码模式

### 二次确认删除

```ts
const handleDelete = () => {
  GmConfirmBox({ message: '是否确认删除？' }, async () => {
    await deleteItem();
    GmMessage.success('删除成功');
  });
};
```

### 异步按钮（自动 loading）

绑定异步函数即可，无需手动管理 loading 状态。当按钮仅执行 `emit` 而不返回 Promise 时，不会触发自动 loading：

```vue
<gm-button @click="handleSubmit">提交</gm-button>
```

```ts
const handleSubmit = async () => {
  await submitForm();
  GmMessage.success('提交成功');
};
```

### 选择器（:options 写法）

```vue
<gm-select v-model="form.status" clearable :options="statusOptions" />
```

### 复制到剪切板

```ts
GmCopy(text);
```

## 获取详细文档

使用具体组件、Hook 或工具函数时，通过 `giime-docs` MCP 获取详细用法：

1. 调用 `get-giime-docs-sidebar` 获取完整目录（包含所有组件/Hook/工具函数的链接）
2. 调用 `get-giime-component-doc({ link })` 获取对应的 Markdown 文档

如果 `giime-docs` MCP 未配置，参考 [mcp-setup.md](references/mcp-setup.md) 进行安装。
