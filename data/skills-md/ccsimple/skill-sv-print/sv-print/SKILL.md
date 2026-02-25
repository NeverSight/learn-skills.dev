---
name: sv-print
description: 可视化打印设计器组件。基于 Svelte 构建，支持 Vue、React、Angular、jQuery 等框架引入。提供拖拽式模板设计、预览、打印、导出 PDF/图片功能，支持插件扩展元素（ECharts、二维码、Fabric等）。
---

# sv-print

可视化打印设计器组件。基于 Svelte 构建，支持 Vue、React、Angular、jQuery 等框架引入。

## 快速开始

### 安装

```bash
# Svelte/Vanilla JS
npm i sv-print

# React
npm i @sv-print/react

# Vue2
npm i @sv-print/vue

# Vue3
npm i @sv-print/vue3

# 核心库
npm i @sv-print/hiprint
```

### 引入样式

在 main.ts 或 main.js 文件中引入组件样式

```js
import 'sv-print/dist/style.css';
```

### 引入打印样式

需要复制 `node_modules/@sv-print/hiprint/dist/print-lock.css` 到开发资源目录。<br/>
例如: Vue 项目的 `public` 目录。<br/>
假如你部署的网站是: `https://www.abcd.com/index.html` 那么确保 `https://www.abcd.com/print-lock.css` 能够正常访问。

在 `index.html` 中添加打印样式：

```html
<link rel="stylesheet" type="text/css" media="print" href="/print-lock.css" />
```

### 基本使用

```vue
<template>
  <div style="width:100vw; height:100vh">
    <Designer :template="template" @onDesigned="onDesigned" />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Designer } from '@sv-print/vue3';

const template = ref({});
const onDesigned = (e) => {
  const { hiprint, designerUtils } = e.detail;
  console.log(designerUtils.printTemplate);
};
</script>
```

## 核心概念

### 模板 JSON

模板数据格式包含 `panels` 数组，每个面板支持：

- `width/height`: 面板尺寸（单位 mm）
- `printElements`: 打印元素列表
- `paperHeader/paperFooter`: 页眉/页脚线
- `paperNumberLeft/paperNumberTop`: 页码位置
- `backgroundColor`: 背景颜色
- `watermarkOptions`: 水印配置

See [template.md](template.md) for details.

### 全局对象

| 对象             | 用途                              |
| ---------------- | --------------------------------- |
| `hiprint`        | 创建模板、打印预览、provider 管理 |
| `hiwebSocket`    | 连接打印客户端                    |
| `hinnn`          | 工具类（单位转换、事件等）        |
| `HIPRINT_CONFIG` | 全局配置对象                      |

See [api.md](api.md) for details.

### 设计器组件

Designer 组件支持丰富的参数：

- `template`: 模板 JSON 数据
- `printData`: 打印预览数据
- `config`: 配置参数
- `plugins`: 插件列表
- `events`: 事件回调
- `theme`: 主题配置

See [designer.md](designer.md) for details.

### 插件系统

官方插件：

- `@sv-print/plugin-ele-bwip-js` - 二维码/条形码
- `@sv-print/plugin-ele-echarts` - ECharts 图表
- `@sv-print/plugin-ele-fabric` - Fabric 绘制
- `@sv-print/plugin-ele-e2table` - Excel 表格
- `@sv-print/plugin-text-auto` - 文本自适应
- `@sv-print/plugin-formatter` - 数据格式化

See [plugins.md](plugins.md) for details.

## 常见场景

### 浏览器打印

```js
const printTemplate = new hiprint.PrintTemplate({ template: json });
const printData = { name: 'i不简' };
await printTemplate.print(printData);
// 批量打印
await printTemplate.print([printData, printData, printData]);
```

### 静默打印（需要打印客户端）

```js
const res = await printTemplate.print2(printData, {
  printer: '打印机名称',
  pageSize: { width: 210 * 1000, height: 297 * 1000 },
  copies: 2,
  landscape: false,
  color: true,
});
```

### 获取预览 HTML

```js
const html = (await printTemplate.getHtml(printData)).html();
```

## 导出

### 导出 PDF（需插件）

```js
import pluginApiPdf from '@sv-print/plugin-api-pdf3';
import { hiprint } from 'sv-print';

// 注册插件
hiprint.register({
  plugins: [pluginApiPdf({})],
});

// 导出 PDF
const printTemplate = new hiprint.PrintTemplate({ template: json });
const printData = { name: '测试数据' };

// 方式一：直接下载
await printTemplate.toPdf(printData, '文件名称');

// 方式二：获取 Blob 对象
const res = await printTemplate.toPdf(printData, {
  name: 'pdf名称',
  isDownload: false, // 不自动下载，返回结果对象
  type: 'blob', // 输出类型: blob | bloburl | dataurl | pdfobjectnewwindow
  onProgress: (cur, total) => {
    console.log('进度', Math.floor((cur / total) * 100) + '%');
  },
});
console.log('PDF Blob:', res);

// 方式三：小模板填充到指定纸张大小
// 适用于：模板中 panelLayoutOptions.layoutRowGap > 0 或 layoutColumnGap > 0
// 且 printData 为数组时，小模板会自动填充到指定纸张大小
await printTemplate.toPdf(printDataArray, '发货单', {
  paperWidth: 210, // 纸张宽度 (mm)
  paperHeight: 297, // 纸张高度 (mm)
});
```

**toPdf 参数说明：**

| 参数        | 类型     | 默认值  | 说明                                                 |
| ----------- | -------- | ------- | ---------------------------------------------------- |
| name        | string   | 'print' | 下载文件名                                           |
| isDownload  | boolean  | true    | 是否自动下载                                         |
| type        | string   | 'blob'  | 输出类型: blob, bloburl, dataurl, pdfobjectnewwindow |
| paperWidth  | number   | -       | 纸张宽度 (mm)，小模板填充时有效                      |
| paperHeight | number   | -       | 纸张高度 (mm)，小模板填充时有效                      |
| onProgress  | function | -       | 进度回调 (cur, total)                                |

### 导出图片（需插件）

```js
import pluginApiImage from '@sv-print/plugin-api-image';
import { hiprint } from 'sv-print';

// 注册插件
hiprint.register({
  plugins: [pluginApiImage({})],
});

// 导出图片
const printTemplate = new hiprint.PrintTemplate({ template: json });
const printData = { name: '测试数据' };

// 方式一：直接下载
await printTemplate.toImage(printData, '图片名称');

// 方式二：获取 URL 或 Blob
const res = await printTemplate.toImage(printData, {
  name: '图片名称',
  isDownload: false, // 不自动下载
  type: 'image/jpeg', // 图片类型: image/jpeg | image/png
  quality: 0.92, // 图片质量 0-1
  toType: 'url', // 返回类型: url | blob
  limit: 10, // 多少页为一个图片文件
  onProgress: (cur, total) => {
    console.log('进度', Math.floor((cur / total) * 100) + '%');
  },
});
console.log('图片URL:', res);

// 方式三：小模板填充到指定纸张大小
await printTemplate.toImage(printDataArray, '发货单', {
  paperWidth: 210, // 纸张宽度 (mm)
  paperHeight: 297, // 纸张高度 (mm)
});
```

**toImage 参数说明：**

| 参数        | 类型     | 默认值       | 说明                            |
| ----------- | -------- | ------------ | ------------------------------- |
| name        | string   | 'print'      | 下载文件名                      |
| isDownload  | boolean  | true         | 是否自动下载                    |
| type        | string   | 'image/jpeg' | 图片类型: image/jpeg, image/png |
| quality     | number   | 0.92         | 图片质量 0-1                    |
| toType      | string   | 'url'        | 返回类型: url, blob             |
| limit       | number   | 10           | 多少页为一个图片文件            |
| paperWidth  | number   | -            | 纸张宽度 (mm)，小模板填充时有效 |
| paperHeight | number   | -            | 纸张高度 (mm)，小模板填充时有效 |
| onProgress  | function | -            | 进度回调 (cur, total)           |

### 小模板填充说明

当需要将多个小模板（如名片、标签等）填充到一张大纸（如 A4）时使用：

```js
// 模板 JSON：配置行列间距
const templateJson = {
  panels: [
    {
      index: 0,
      name: '小模板',
      height: 50, // 小模板高度 (mm)
      width: 90, // 小模板宽度 (mm)
      panelLayoutOptions: {
        layoutType: 'row', // 行列布局类型: row, column
        layoutRowGap: 10, // 行间距 (mm)
        layoutColumnGap: 8, // 列间距 (mm)
      },
      printElements: [
        // 元素配置
      ],
    },
  ],
};

// 打印数据：数组格式
const printDataArray = [
  { name: '张三', phone: '13800138000' },
  { name: '李四', phone: '13900139000' },
  { name: '王五', phone: '13700137000' },
  // 更多数据...
];

// 导出到 A4 纸
await printTemplate.toPdf(printDataArray, '批量名片', {
  paperWidth: 210, // A4 宽度 (mm)
  paperHeight: 297, // A4 高度 (mm)
});
```

### 完整导出示例

```vue
<template>
  <div class="designer-container">
    <Designer :template="template" @onDesigned="onDesigned" />
    <div class="export-buttons">
      <button @click="exportPdf">导出 PDF</button>
      <button @click="exportImage">导出 图片</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Designer } from '@sv-print/vue3';
import pluginApiPdf from '@sv-print/plugin-api-pdf3';
import pluginApiImage from '@sv-print/plugin-api-image';
import { hiprint } from 'sv-print';

const printTemplate = ref(null);

// 注册导出插件
hiprint.register({
  plugins: [pluginApiPdf({}), pluginApiImage({})],
});

const onDesigned = (e) => {
  printTemplate.value = e.detail.designerUtils.printTemplate;
};

// 导出 PDF
const exportPdf = async () => {
  if (!printTemplate.value) return;

  const printData = { name: '测试数据' };

  try {
    // 显示下载进度
    await printTemplate.value.toPdf(printData, '发货单', {
      isDownload: true,
      paperWidth: 210,
      paperHeight: 297,
      onProgress: (cur, total) => {
        console.log('PDF 导出进度:', Math.floor((cur / total) * 100) + '%');
      },
    });
    console.log('PDF 导出完成');
  } catch (error) {
    console.error('PDF 导出失败', error);
  }
};

// 导出图片
const exportImage = async () => {
  if (!printTemplate.value) return;

  const printData = { name: '测试数据' };

  try {
    const res = await printTemplate.value.toImage(printData, '发货单', {
      isDownload: false,
      type: 'image/jpeg',
      quality: 0.92,
      toType: 'url',
      onProgress: (cur, total) => {
        console.log('图片导出进度:', Math.floor((cur / total) * 100) + '%');
      },
    });

    // 获取到 URL 后可以自定义处理
    console.log('图片 URL:', res);

    // 打开新窗口查看
    window.open(res, '_blank');
  } catch (error) {
    console.error('图片导出失败', error);
  }
};
</script>

<style>
.export-buttons {
  position: fixed;
  right: 20px;
  top: 20px;
  z-index: 1000;
}

.export-buttons button {
  margin-left: 10px;
  padding: 8px 16px;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.export-buttons button:hover {
  background: #66b1ff;
}
</style>
```

## 实际业务场景示例

### 场景一：自定义 Header 标题和菜单（保存到服务器）

```vue
<template>
  <div class="designer-container">
    <Designer
      headerTitle="发货单模板设计"
      :headerNewMenu="true"
      :headerMenuList="headerMenuList"
      :events="events"
      @onDesigned="onDesigned"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Designer } from '@sv-print/vue3';
import axios from 'axios';

const designerUtils = ref(null);

// 1. 自定义菜单列表
const headerMenuList = ref([
  {
    icon: 'sv-save',
    title: '保存模板',
    desc: 'Ctrl + S',
    click: (util) => util.save(), // 调用内置保存，会触发 events.onSave
  },
  {
    icon: 'sv-preview',
    title: '预览',
    desc: '',
    click: async (util) => {
      util.preview.show();
    },
  },
]);

// 2. 事件处理
const events = ref({
  // 保存模板 - 发送到服务器
  onSave: async (key, data) => {
    try {
      await axios.post('/api/template/save', {
        key: key || 'default-template',
        template: data,
        templateName: '发货单模板',
      });
      console.log('保存成功');
      return true; // 返回 true 阻止冒泡（不弹出内置保存提示）
    } catch (error) {
      console.error('保存失败', error);
      return false;
    }
  },
  // 编辑模板数据
  onEdit: (data) => {
    console.log('模板已编辑');
    return true;
  },
  // 编辑打印数据
  onEditData: (data) => {
    console.log('打印数据已编辑', data);
    return true;
  },
  // 快捷键
  onKeyDownEvent: (e, util) => {
    if (e.ctrlKey && e.key === 's') {
      e.preventDefault();
      util.save();
      return true;
    }
    return false;
  },
});

// 3. 初始化完成回调
const onDesigned = (e) => {
  const { designerUtils: utils } = e.detail;
  designerUtils.value = utils;

  // 可在此处加载已有模板
  loadTemplate();
};

// 加载模板
const loadTemplate = async () => {
  const res = await axios.get('/api/template/get?id=1');
  if (res.data.template) {
    designerUtils.value.printTemplate.update(res.data.template);
  }
};
</script>

<style>
.designer-container {
  width: 100vw;
  height: 90vh;
  overflow: hidden;
}
</style>
```

### 场景二：隐藏默认菜单，只保留自定义保存按钮

```vue
<template>
  <div class="designer-container">
    <Designer
      headerTitle="入库单设计"
      :headerNewMenu="true"
      :headerMenuList="headerMenuList"
      :showOption="{ showToolbar: true }"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Designer } from '@sv-print/vue3';

const headerMenuList = ref([
  {
    icon: 'sv-save',
    title: '保存',
    desc: 'Ctrl+S',
    click: async (util) => {
      const templateData = util.printTemplate.getJson();
      console.log('保存模板:', templateData);
      // 保存逻辑
    },
  },
  {
    icon: 'sv-preview',
    title: '预览',
    click: (util) => {
      util.preview.show();
    },
  },
  {
    gap: true, // 分割线
  },
  {
    icon: 'sv-print',
    title: '直接打印',
    click: async (util) => {
      await util.printTemplate.print2({ name: '测试数据' });
    },
  },
]);
</script>
```

### 场景三：根据 ID 从服务端加载模板并预览

```vue
<template>
  <!-- 设计器外层容器需要设置宽高 -->
  <div v-if="showDesigner" class="designer-container">
    <Designer
      :template="template"
      :printData="printData"
      :events="events"
      :onPreviewClick="onPreviewClick"
      @onDesigned="onDesigned"
    />
  </div>
  <!-- 加载中状态 -->
  <div v-else class="loading">
    <span>加载中...</span>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { Designer } from '@sv-print/vue3';
import axios from 'axios';

const route = useRoute();
const router = useRouter();

const showDesigner = ref(false); // 控制设计器显示
const template = ref({}); // 模板数据
const printData = ref({}); // 打印数据
const designerUtils = ref(null);

// 从路由获取模板 ID
const templateId = route.query.id as string;

// 事件处理
const events = ref({
  onSave: async (key, data) => {
    try {
      // 保存到服务器
      await axios.post('/api/template/save', {
        id: templateId,
        template: data,
      });
      console.log('保存成功');
      return true;
    } catch (error) {
      console.error('保存失败', error);
      return false;
    }
  },
});

// 预览点击事件
const onPreviewClick = () => {
  // 可自定义预览逻辑
  console.log('点击预览');
};

// 初始化完成回调
const onDesigned = (e) => {
  const { designerUtils: utils } = e.detail;
  designerUtils.value = utils;
};

// 从服务器加载模板和打印数据
const loadTemplate = async () => {
  try {
    if (!templateId) {
      // 没有 ID，跳转到新建页面或使用默认空模板
      template.value = {};
      showDesigner.value = true;
      return;
    }

    // 并行请求模板和打印数据
    const [templateRes, printDataRes] = await Promise.all([
      axios.get(`/api/template/${templateId}`),
      axios.get(`/api/template/${templateId}/printData`),
    ]);

    // 设置模板数据
    if (templateRes.data.template) {
      template.value = templateRes.data.template;
    }

    // 设置打印数据
    if (printDataRes.data.printData) {
      printData.value = printDataRes.data.printData;
    }

    // 数据加载完成后显示设计器
    showDesigner.value = true;
  } catch (error) {
    console.error('加载模板失败', error);
    showDesigner.value = true;
  }
};

onMounted(() => {
  loadTemplate();
});
</script>

<style scoped>
.designer-container {
  width: 100vw;
  height: 90vh;
  overflow: hidden;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 90vh;
  font-size: 16px;
  color: #666;
}
</style>
```

### 场景四：切换主题和语言

```vue
<template>
  <div class="designer-container">
    <Designer :theme="theme" :themeList="themeList" headerTitle="多主题模板设计" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Designer } from '@sv-print/vue3';

// 主题
const theme = ref('light');

// 可选主题列表
const themeList = ref([
  'light',
  'dark',
  'cupcake',
  'bumblebee',
  'emerald',
  'corporate',
  'synthwave',
  'retro',
  'cyberpunk',
  'dracula',
  'business',
  'winter',
]);

// 切换主题
const changeTheme = (newTheme: string) => {
  theme.value = newTheme;
};
</script>

<style>
.designer-container {
  width: 100vw;
  height: 90vh;
  overflow: hidden;
}
</style>
```

### 场景五：自定义可拖拽元素

```vue
<template>
  <div class="designer-container">
    <Designer :providers="providers" :providerMap="providerMap" :clearProviderContainer="true" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Designer } from '@sv-print/vue3';
import { hiprint } from 'sv-print';

// 定义 provider
const customProvider = (options) => {
  var addElementTypes = function (context) {
    context.removePrintElementTypes('customModule');

    context.addPrintElementTypes('customModule', [
      // 常规分组
      new hiprint.PrintElementTypeGroup('业务字段', [
        {
          tid: 'customModule.companyName',
          type: 'text',
          title: '公司名称',
          options: {
            title: '公司名称',
            field: 'companyName',
            testData: '不简科技',
            fontSize: 16,
            fontWeight: 'bolder',
          },
        },
        {
          tid: 'customModule.orderNo',
          type: 'text',
          title: '订单号',
          options: {
            title: '订单号',
            field: 'orderNo',
            testData: 'DD20240129001',
          },
        },
      ]),
      // 辅助分组
      new hiprint.PrintElementTypeGroup('辅助', [
        {
          tid: 'customModule.hline',
          type: 'hline',
          title: '横线',
        },
        {
          tid: 'customModule.rect',
          type: 'rect',
          title: '矩形',
        },
      ]),
    ]);
  };
  return { addElementTypes };
};

const providers = ref([customProvider({})]);

const providerMap = ref({
  container: '.hiprintEpContainer',
  value: 'customModule',
});
</script>

<style>
.designer-container {
  width: 100vw;
  height: 90vh;
  overflow: hidden;
}
</style>
```

### 场景六：表格元素使用

```js
// 表格元素模板
const tableTemplate = {
  panels: [
    {
      index: 0,
      name: '面板0',
      height: 297,
      width: 210,
      printElements: [
        {
          options: {
            left: 60,
            top: 60,
            height: 100,
            width: 500,
            field: 'table',
            columnFields: [
              { text: 'ID', field: 'id' },
              { text: '姓名', field: 'name' },
              { text: '数量', field: 'count' },
            ],
            columns: [
              [
                { width: 100, title: 'ID', field: 'id', checked: true },
                { width: 150, title: '姓名', field: 'name', checked: true },
                { width: 100, title: '数量', field: 'count', checked: true },
              ],
            ],
          },
          printElementType: {
            title: '表格',
            type: 'table',
            editable: true,
            columnResizable: true,
            isEnableInsertRow: true,
            isEnableDeleteRow: true,
          },
        },
      ],
    },
  ],
};

// 打印数据
const printData = {
  table: [
    { id: 1, name: '商品A', count: 100 },
    { id: 2, name: '商品B', count: 200 },
    { id: 3, name: '商品C', count: 300 },
  ],
};
```

### 场景七：二维码/条形码元素

**方式一：使用文本元素（无需插件）**

通过 `text` 元素设置 `textType` 属性实现二维码或条形码：

```js
// 二维码模板
const qrcodeTemplate = {
  panels: [
    {
      index: 0,
      name: '面板0',
      height: 297,
      width: 210,
      printElements: [
        {
          options: {
            left: 100,
            top: 60,
            height: 50,
            width: 50,
            title: '123456789', // 显示内容
            textType: 'qrcode', // 设置为二维码
            color: '#000000',
          },
          printElementType: {
            title: '文本',
            type: 'text',
          },
        },
      ],
    },
  ],
};

// 条形码模板
const barcodeTemplate = {
  panels: [
    {
      index: 0,
      name: '面板0',
      height: 297,
      width: 210,
      printElements: [
        {
          options: {
            left: 100,
            top: 60,
            height: 40,
            width: 150,
            title: '123456789',
            textType: 'barcode', // 设置为条形码
            color: '#000000',
          },
          printElementType: {
            title: '文本',
            type: 'text',
          },
        },
      ],
    },
  ],
};
```

**方式二：使用插件扩展的新元素类型（推荐）**

引入 `@sv-print/plugin-ele-bwip-js` 插件后，会新增 `barcode` 和 `qrcode` 元素类型：

```vue
<template>
  <div class="designer-container">
    <Designer :plugins="plugins" :template="template" headerTitle="发货单（含条码）" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Designer } from '@sv-print/vue3';
import pluginBwip from '@sv-print/plugin-ele-bwip-js';

const plugins = ref([
  pluginBwip({}), // 插件无配置参数，直接引入即可
]);

// 使用插件新增的 qrcode 元素类型
const template = ref({
  panels: [
    {
      index: 0,
      name: '面板0',
      height: 297,
      width: 210,
      printElements: [
        {
          options: {
            left: 100,
            top: 60,
            height: 60,
            width: 60,
            title: '二维码内容', // 显示内容
          },
          printElementType: {
            title: '二维码', // 插件新增的元素类型
            type: 'qrcode',
          },
        },
        {
          options: {
            left: 200,
            top: 60,
            height: 50,
            width: 150,
            title: '条形码内容',
          },
          printElementType: {
            title: '条形码', // 插件新增的元素类型
            type: 'barcode',
          },
        },
      ],
    },
  ],
});

// 打印数据
const printData = {
  name: '张三',
};
</script>

<style>
.designer-container {
  width: 100vw;
  height: 90vh;
  overflow: hidden;
}
</style>
```

### 场景八：接收外部保存信号触发设计器保存

```vue
<template>
  <div class="page-container">
    <div class="toolbar">
      <button @click="saveTemplate">外部保存按钮</button>
    </div>
    <div class="designer-container">
      <Designer :events="events" @onDesigned="onDesigned" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { Designer } from '@sv-print/vue3';
import { hinnn } from 'sv-print';

const designerUtils = ref(null);
const saveTrigger = ref(0); // 保存触发器

// 事件
const events = ref({
  onSave: (key, data) => {
    console.log('保存模板', key);
    // 发送到服务器或 localStorage
    return true;
  },
});

const onDesigned = (e) => {
  const { designerUtils: utils } = e.detail;
  designerUtils.value = utils;
};

// 外部保存
const saveTemplate = () => {
  if (designerUtils.value) {
    designerUtils.value.save();
  }
};

// 监听外部保存信号（可通过 pinia/vuex 或事件总线触发）
watch(saveTrigger, () => {
  saveTemplate();
});

// 模拟外部触发
// hinnn.event.trigger('saveTemplate');
</script>

<style>
.page-container {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.toolbar {
  height: 50px;
  padding: 0 20px;
  display: flex;
  align-items: center;
  background: #f5f5f5;
}

.designer-container {
  flex: 1;
  overflow: hidden;
}
</style>
```

### 场景九：设置默认纸张和尺寸

```vue
<template>
  <div class="designer-container">
    <Designer :paperList="paperList" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Designer } from '@sv-print/vue3';

const paperList = ref([
  { type: 'A4', width: 210, height: 297 },
  { type: 'A5', width: 148, height: 210 },
  { type: 'Custom', width: 100, height: 150 }, // 自定义尺寸
]);
</script>

<style>
.designer-container {
  width: 100vw;
  height: 90vh;
  overflow: hidden;
}
</style>
```

### 场景十：禁用/调整 UI 组件

通过 `styleOption`、`showOption`、`rulerStyle` 可以隐藏或调整各个小组件的位置：

```vue
<template>
  <div class="designer-container">
    <Designer
      :styleOption="styleOption"
      :showOption="showOption"
      :rulerStyle="rulerStyle"
      :showPanels="false"
      headerTitle="简化版设计器"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Designer } from '@sv-print/vue3';

// 控制各小组件的显示和位置
const styleOption = ref({
  draggableEls: {
    // 可拖拽元素区域
    mode: 'left', // 固定在左侧
    show: true, // 是否显示
    style: 'left:0;top:95px;width:200px;height:calc(100% - 340px);',
  },
  options: {
    // 属性面板 - 隐藏
    show: false,
  },
  pageStructure: {
    // 页面结构 - 隐藏
    show: false,
  },
  locationExchange: {
    // 位置交换 - 隐藏
    show: false,
  },
  miniMap: {
    // 小地图 - 隐藏
    show: false,
  },
  editableTools: {
    // 编辑工具 - 隐藏
    show: false,
  },
  zIndexTools: {
    // 层级工具 - 隐藏
    show: false,
  },
  fontTools: {
    // 字体工具 - 隐藏
    show: false,
  },
  zoomTools: {
    // 缩放工具 - 显示并调整位置
    mode: 'right',
    style: 'right:10px;top:100px;',
  },
  rotateTools: {
    // 旋转工具 - 隐藏
    show: false,
  },
});

// 控制主区域显示
const showOption = ref({
  showHeader: true, // 显示顶部 Header
  showToolbar: true, // 显示工具栏 Toolbar
  showFooter: true, // 显示底部 Footer
  showPower: false, // 隐藏 "powered by sv-print"
});

// 控制标尺
const rulerStyle = ref({
  show: false, // 隐藏标尺
});
</script>

<style>
.designer-container {
  width: 100vw;
  height: 90vh;
  overflow: hidden;
}
</style>
```

**styleOption 可配置项说明：**

| 组件             | 说明       | 可配置项                |
| ---------------- | ---------- | ----------------------- |
| panels           | 多面板区域 | mode                    |
| draggableEls     | 可拖拽元素 | show, mode, style, html |
| options          | 属性面板   | show, mode, style, html |
| pageStructure    | 页面结构   | show, mode, style, html |
| locationExchange | 位置交换   | show, mode, style, html |
| miniMap          | 小地图     | show, mode, style, html |
| history          | 历史记录   | show, mode, style, html |
| editableTools    | 编辑工具   | show, mode, style       |
| zIndexTools      | 层级工具   | show, mode, style       |
| fontTools        | 字体工具   | show, mode, style       |
| zoomTools        | 缩放工具   | show, mode, style       |
| rotateTools      | 旋转工具   | show, mode, style       |

**mode 取值说明：**

- `default` - 默认位置
- `top` - 固定在顶部
- `bottom` - 固定在底部
- `left` - 固定在左侧
- `right` - 固定在右侧
- `fixed` - 自由拖拽（需配合 style 设置初始位置）
