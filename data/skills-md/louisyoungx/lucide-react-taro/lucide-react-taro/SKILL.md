---
name: lucide-react-taro
description: 在 Taro 微信小程序和 Web 项目中使用 Lucide 图标。当用户需要在 Taro 项目中添加图标、使用 lucide 图标库、生成 TabBar 图标时使用此技能。
---

# lucide-react-taro

`lucide-react-taro` 是 Lucide 图标库的 Taro 适配版本，专为 Taro 微信小程序和 Web 平台设计。

## 安装

```bash
npm install lucide-react-taro
# or
pnpm add lucide-react-taro
```

## 基础用法

```tsx
import { House, Settings, Camera, Zap } from 'lucide-react-taro';

function MyComponent() {
  return (
    <View>
      <House />
      <Settings size={32} />
      <Camera color="#ff0000" />
      <Zap strokeWidth={1} />
      <Zap size={48} color="#1890ff" strokeWidth={1.5} />
      <Zap size={48} strokeWidth={2} absoluteStrokeWidth />
      <House className="my-icon" style={{ marginRight: 8 }} />
    </View>
  );
}
```

## Props

| 属性                  | 类型               | 默认值           | 说明                                   |
| --------------------- | ------------------ | ---------------- | -------------------------------------- |
| `size`                | `number \| string` | `24`             | 图标尺寸                               |
| `color`               | `string`           | `'currentColor'` | 图标颜色                               |
| `strokeWidth`         | `number \| string` | `2`              | 描边宽度                               |
| `absoluteStrokeWidth` | `boolean`          | `false`          | 绝对描边宽度，启用后描边不随 size 缩放 |
| `className`           | `string`           | -                | CSS 类名                               |
| `style`               | `CSSProperties`    | -                | 内联样式                               |

同时支持 Taro `Image` 组件的其他属性。

## 按需导入

支持 tree shaking，只打包使用到的图标：

```tsx
import { House, Settings } from 'lucide-react-taro';
import { House } from 'lucide-react-taro/icons/house';
```

## 图标列表

所有图标名称与 [Lucide 官方](https://lucide.dev/icons/) 保持一致，使用 PascalCase 命名。

常用图标：`House`、`Settings`、`User`、`Search`、`Menu`、`ChevronRight`、`Check`、`X`、`Plus`、`Minus`、`Heart`、`Star`、`Camera`、`Image`、`Share`、`Download`、`Upload`

## CLI 工具：查找和验证图标

本库提供了 CLI 工具来查找和验证图标是否存在。这对 AI 助手非常有用，可以在生成代码前验证图标名称是否正确。

### 查找图标

```bash
# 模糊查找（默认）
npx taro-lucide-find arrow

# 精确查找
npx taro-lucide-find arrow-up --exact

# 列出所有图标
npx taro-lucide-find --list
```

### 验证图标

推荐在生成代码前，使用 `--json` 参数批量验证图标是否存在。

```bash
npx taro-lucide-find arrow-up user settings arw --json
```

**输出示例：**

```json
[
  {
    "query": "arrow-up",
    "exists": true,
    "name": "ArrowUp",
    "suggestions": []
  },
  {
    "query": "arw",
    "exists": false,
    "name": null,
    "suggestions": ["ArrowBigDownDash", "Archive", "..."]
  }
]
```

如果 `exists` 为 `false`，请使用 `suggestions` 中的推荐图标名称。

## CLI 工具：生成 TabBar 图标

微信小程序的 TabBar 不支持 base64 或 SVG 图片，只能使用本地 PNG 文件。本库提供了 CLI 工具来生成 TabBar 所需的 PNG 图标。

### 批量生成 TabBar 图标

支持一次性生成所有 TabBar 图标。

```bash
npx taro-lucide-tabbar House Settings User -c "#999999" -a "#1890ff"
```

### 指定输出目录和尺寸

```bash
npx taro-lucide-tabbar House Settings User -c "#999999" -a "#1890ff" -o ./src/assets/tabbar -s 81
```

### CLI 参数

| 参数             | 简写 | 默认值           | 说明         |
| ---------------- | ---- | ---------------- | ------------ |
| `--color`        | `-c` | `#000000`        | 图标颜色     |
| `--active-color` | `-a` | -                | 选中状态颜色 |
| `--size`         | `-s` | `81`             | 图标尺寸     |
| `--output`       | `-o` | `./tabbar-icons` | 输出目录     |
| `--stroke-width` | -    | `2`              | 描边宽度     |

### 在 app.config.ts 中使用

```ts
export default defineAppConfig({
  tabBar: {
    color: '#999999',
    selectedColor: '#1890ff',
    backgroundColor: '#ffffff',
    borderStyle: 'black',
    list: [
      {
        pagePath: 'pages/index/index',
        text: '首页',
        iconPath: './assets/tabbar/house.png',
        selectedIconPath: './assets/tabbar/house-active.png',
      },
      {
        pagePath: 'pages/settings/index',
        text: '设置',
        iconPath: './assets/tabbar/settings.png',
        selectedIconPath: './assets/tabbar/settings-active.png',
      },
    ],
  },
});
```

## 注意事项

1. **颜色默认值**：默认颜色为 `currentColor`，在小程序 Image 组件中可能不会继承父元素颜色，建议显式设置 `color` 属性。
2. **性能优化**：组件内部已实现 base64 缓存，相同参数组合只计算一次。
3. **兼容性**：已内置 base64 编码 polyfill，无需额外配置即可在微信小程序中使用。
4. **TabBar 图标**：小程序 TabBar 不支持 SVG/base64，请使用 CLI 工具生成 PNG 图标。
5. **TabBar 图标路径**：`iconPath` 和 `selectedIconPath` 必须添加 `./` 前缀（如 `./assets/tabbar/house.png`），否则图片无法正确加载。
