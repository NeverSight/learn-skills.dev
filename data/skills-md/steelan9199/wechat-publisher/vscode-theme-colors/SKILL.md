---
name: vscode-theme-colors
description: 供 AI 查阅 VSCode 主题颜色设置。当用户询问 VSCode 主题颜色、颜色自定义、主题配置、workbench.colorCustomizations 等相关问题时触发。
---

# VSCode 主题颜色设置

## 概述

此 skill 提供 VSCode 主题颜色设置的完整参考资料，包括：
- 颜色主题的基本概念和使用方法
- 可自定义的颜色标识符列表
- 如何创建和发布自定义主题

## 快速参考

### 设置颜色主题

```json
{
  "workbench.colorTheme": "Solarized Dark"
}
```

### 自定义主题颜色

```json
{
  "workbench.colorCustomizations": {
    "activityBar.background": "#00AA00",
    "sideBar.background": "#347890"
  }
}
```

### 为特定主题设置自定义颜色

```json
{
  "workbench.colorCustomizations": {
    "[Monokai]": {
      "sideBar.background": "#347890"
    }
  }
}
```

### 编辑器语法高亮自定义

```json
{
  "editor.tokenColorCustomizations": {
    "comments": "#229977",
    "strings": "#FF0000"
  }
}
```

## 颜色格式

支持以下十六进制格式：
- `#RGB` (简写，如 `#e35`)
- `#RGBA` (简写带透明度，如 `#e35f`)
- `#RRGGBB` (完整，如 `#ee3355`)
- `#RRGGBBAA` (完整带透明度，如 `#ee3355ff`)

透明度 `00` = 完全透明，`ff` = 完全不透明（默认）

## 完整颜色参考

详见 [references/theme-color-reference.md](references/theme-color-reference.md) 获取所有可自定义的颜色标识符完整列表。

## 创建新主题

1. 使用 `Developer: Generate Color Theme from Current Settings` 命令生成主题文件
2. 或使用 Yeoman 生成器创建主题扩展：
   ```bash
   npm install -g yo generator-code
   yo code
   ```

## 常用颜色分类

### 基础颜色
- `focusBorder` - 聚焦元素边框
- `foreground` - 整体前景色
- `selection.background` - 文本选择背景

### 窗口边框
- `window.activeBorder` - 活动窗口边框
- `window.inactiveBorder` - 非活动窗口边框

### 按钮
- `button.background` - 按钮背景
- `button.foreground` - 按钮前景
- `button.hoverBackground` - 悬停背景

### 编辑器
- `editor.background` - 编辑器背景
- `editor.foreground` - 编辑器前景
- `editor.lineHighlightBackground` - 当前行高亮

### 侧边栏
- `sideBar.background` - 侧边栏背景
- `sideBar.foreground` - 侧边栏前景

### 活动栏
- `activityBar.background` - 活动栏背景
- `activityBar.foreground` - 活动栏前景

### 状态栏
- `statusBar.background` - 状态栏背景
- `statusBar.foreground` - 状态栏前景
