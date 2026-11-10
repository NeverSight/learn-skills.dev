---
name: "wot-ui-unocss-preset-guide"
description: "指导安装、配置并使用 @wot-ui/unocss-preset。Invoke when 用户询问该预设的接入、配置、使用示例或常见问题排查。"
---

# Wot UnoCSS Preset 使用指南

## 适用场景

当用户询问以下内容时，优先使用本 Skill：

- 如何安装 `@wot-ui/unocss-preset`
- 如何在 `unocss.config.ts` 配置 `presetWot`
- `prefix`、`preflight`、`baseTokens` 怎么用
- 为什么类名不生效、自动补全不出现、CI 与本地结果不一致

目标是给出可直接复制的最佳实践，帮助用户快速完成接入并稳定运行。

## 最小安装步骤

```bash
pnpm add -D unocss
pnpm add @wot-ui/unocss-preset
```

## 推荐配置（完整示例）

```ts
import { presetWot } from '@wot-ui/unocss-preset'
import { defineConfig } from 'unocss'

export default defineConfig({
  presets: [
    presetWot({
      prefix: 'wot',
      preflight: true,
      baseTokens: false,
    }),
  ],
})
```

## 配置项说明

- `prefix`：工具类前缀，默认 `wot`。示例：`wot-text-primary`、`wot-m-main`。
- `preflight`：是否注入 wot-ui CSS 变量，默认 `true`。
- `baseTokens`：是否开放基础色板和原始 token 类名，默认 `false`。

## 常用类名示例

- 颜色：`wot-text-primary`、`wot-bg-danger-surface`、`wot-border-border-main`
- 间距：`wot-m-main`、`wot-gap-tight`、`wot-gap-x-loose`
- 内边距：`wot-p-main`、`wot-px-tight`、`wot-pb-loose`
- 圆角：`wot-rounded-md`、`wot-rounded-full`
- 字重：`wot-font-medium`、`wot-font-semibold`
- 排版：`wot-text-body-main`、`wot-text-title-large`
- 透明度：`wot-opacity-disabled`
- 描边：`wot-border-stroke-main`

## 上手示例（可复制）

### 1) 一个“卡片”示例（uni-app / Vue）

```vue
<template>
  <view class="wot-bg-filled-oppo wot-rounded-2xl wot-p-super-loose wot-border-border-main wot-border-stroke-main">
    <text class="wot-text-title-large wot-text-text-main wot-font-semibold">
      Wot UnoCSS Preset
    </text>

    <view class="wot-mt-tight">
      <text class="wot-text-body-main wot-text-text-secondary">
        wot-text-body-main + wot-text-text-secondary
      </text>
    </view>

    <view class="wot-mt-loose wot-bg-primary wot-rounded-full wot-px-main wot-py-extra-tight">
      <text class="wot-text-label-large wot-text-text-white wot-font-semibold">
        wot-bg-primary
      </text>
    </view>
  </view>
</template>
```

### 2) 间距/布局示例（常见组合）

- 外边距：`wot-mt-tight`、`wot-mt-main`、`wot-mt-super-loose`
- 内边距：`wot-p-loose`、`wot-px-main`、`wot-py-extra-tight`
- 横向/纵向组合：`wot-mx-main`、`wot-my-loose`
- gap：`wot-gap-tight`、`wot-gap-x-main`、`wot-gap-y-loose`

### 3) 语义色示例（背景/文字/边框）

- 背景：`wot-bg-primary`、`wot-bg-success-surface`、`wot-bg-warning-surface`、`wot-bg-danger-surface`
- 文字：`wot-text-text-main`、`wot-text-text-secondary`、`wot-text-primary`、`wot-text-success-main`
- 边框：`wot-border-border-main`、`wot-border-success-main`、`wot-border-warning-main`、`wot-border-danger-main`

### 4) 暗黑模式示例

预设会输出暗色变量选择器 `.wot-theme-dark ...`，你只需要在根节点加 class：

```vue
<template>
  <view :class="dark ? 'wot-theme-dark' : ''">
    <view class="wot-bg-filled-oppo wot-p-main wot-rounded-lg">
      <text class="wot-text-text-main">当前主题：{{ dark ? 'Dark' : 'Light' }}</text>
    </view>
  </view>
</template>
```

### 5) 打开 baseTokens（可选）

当你希望使用基础色板/原始 token 时启用：

```ts
presetWot({
  baseTokens: true,
})
```

启用后会额外提供类似 `wot-base-black` 这类 token（用于 `theme.colors` 与颜色规则匹配）。

## 轻量提醒

- 历史项目若仍使用 `w-` 前缀，可通过 `prefix: 'w'` 兼容。
- 若 playground/子包构建异常，优先检查是否：
  - 使用包名导入（如 `@wot-ui/unocss-preset`）
  - 在依赖主包产物的场景下先执行主包构建
- 若需要同步上游 wot-ui 变量，可使用：
  - `pnpm generate:css-vars:clone`

## 常见问题排查

1. 类名不生效
- 确认项目已启用 UnoCSS 且 `presetWot()` 已加入 `presets`。
- 确认类名前缀与配置一致（默认 `wot-`）。

2. VS Code 没有自动补全
- 确认安装 UnoCSS 官方扩展。
- 确认编辑器能定位到项目 `unocss.config.ts`。
- 确认类名写在扩展可扫描的文件类型内。

3. CI 能复现但本地不复现（或反过来）
- 对齐 Node/pnpm 版本与锁文件。
- 对齐执行顺序（例如先构建主包，再构建依赖主包产物的 playground）。

## 响应风格要求

- 输出简洁、可执行，优先给“可复制配置 + 最短排查路径”。
- 当用户目标明确时，先给结论和配置，再补充原因说明。
- 不擅自引入本项目未使用的额外工具链或复杂抽象。
