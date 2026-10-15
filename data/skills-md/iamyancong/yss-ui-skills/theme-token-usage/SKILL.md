---
name: theme-token-usage
description: 指导 Vue3 YSS UI 微应用业务页面、公共组件、原型还原和主题修复使用可动态换肤的 CSS/Ant Design Token，覆盖主色、hover/active/selected/focus、状态色、中性色、透明色派生和暗色模式；当新增或修改 .vue、style.less、内联样式、TS 渲染配置、SVG 色值，或审查硬编码 #hex/rgb/渐变时使用。
---

# YSS UI 主题 Token 使用 Skill

## 触发条件

- 新增、重构或按原型实现 Vue3 业务页面、公共组件、布局、卡片、树、表格、表单、抽屉和详情页。
- 修改 `.vue`、`.less`、`.css`、`.scss`、TS/TSX 渲染配置或 SVG 中的颜色、背景、边框、阴影、渐变。
- 页面需要跟随主应用主题、JSP 预设主题、暗色模式或运行时主色切换。
- 评审或修复 `#1677ff`、`#3371ff`、`rgb/rgba/hsl` 等硬编码色值。

## 不适用场景

- 只维护主题源文件中的默认值或主题预设，例如 `variables.less`、`store/theme.ts`、`config/themes.ts`。
- 用户明确要求不可换肤的品牌插画、数据可视化固定色板或第三方资产原色；仍需在代码中注明固定色语义。
- 只修改与视觉无关的类型、接口或纯业务逻辑。

## 开发前检查

1. 读取当前微应用的 `packages/src/styles/variables.less`、主题 store/config 和相近页面，确认真实 Token 名称与运行时同步逻辑。
2. 确认主应用传入的 `colorPrimary` 最终是否同步到 Ant Design ConfigProvider、YSS CSS 变量和 VXE 变量。
3. 搜索本次改动涉及的硬编码色值，覆盖 SFC style、`style.less`、内联 `style`、`:style`、TS 配置、SVG `fill/stroke`。
4. 区分“主题消费代码”和“主题定义代码”；禁止机械替换主题源文件中的合法默认色板。

> 变量在 `:root` 中声明，不代表它会随运行时主题更新。必须同时检查主题同步代码是否写入该变量。

## Token 选择

按以下优先级选值：

| 语义 | 优先使用 | 兼容选择 |
| --- | --- | --- |
| 主色 | `var(--primary-color, #3371ff)` | `var(--yss-color-primary-6, #3371ff)` |
| hover | `var(--primary-color-hover, #4096ff)` | `var(--yss-color-primary-5, #4096ff)` |
| active | `var(--primary-color-active, #0958d9)` | `var(--yss-color-primary-7, #0958d9)` |
| 成功/警告/错误/信息 | `--success-color` / `--warning-color` / `--error-color` / `--info-color` | 对应 `--yss-color-*-6` |
| 正文/次要文字 | `--text-color` / `--text-color-secondary` | 使用项目已有语义 Token |
| 容器/页面背景 | `--bg-color-container` / `--bg-color` | 使用项目已有语义 Token |
| 边框/分割线 | `--border-color` / `--border-color-split` | 使用项目已有语义 Token |
| 反色文字 | `--text-color-inverse` | 不直接写 `#fff` |

需要主色透明背景、focus ring 或阴影时，从真实主色动态派生：

```less
background: color-mix(in srgb, var(--primary-color, #3371ff) 10%, transparent);
box-shadow: 0 0 0 3px color-mix(in srgb, var(--primary-color, #3371ff) 15%, transparent);
```

仅当主题同步逻辑明确维护 `--primary-1` 时才可使用 `var(--primary-1)`。禁止用带蓝色 fallback 的 `var(--primary-1, rgba(...))` 冒充动态主题；变量未同步时，红色等主题仍会回落为蓝色。

## 硬约束（禁止/必须）

- 必须优先让 `YButton`、`YTable`、`YTree`、`YFormily` 和 Ant Design Vue 组件消费 ConfigProvider 主题；非必要不覆盖其主色样式。
- 业务消费代码禁止直接写品牌蓝、主题红及其 hover/active/selected/focus 色阶，包括十六进制、`rgb/rgba/hsl`、渐变和阴影。
- 必须使用语义 Token；禁止仅按“颜色长得接近”替换，例如把错误态改成主色。
- `var()` fallback 必须与项目默认 Token 一致；fallback 只负责兼容，不得成为实际换肤来源。
- 禁止在页面局部随意发明 `--primary-light` 等新变量。确需新增时，必须在统一主题源声明，并在运行时主题同步链路中更新。
- 禁止对 CSS 变量使用 Less 编译期颜色函数，例如 `fade(@primary-color, 10%)`；`@primary-color` 指向 `var()` 时无法可靠计算。
- 禁止写 `rgba(var(--primary-color), 0.1)`；十六进制 CSS 变量不能直接作为 `rgba()` 通道参数。
- 固定数据可视化色板、品牌资产原色或遮罩色允许保留，但必须与换肤语义无关，并添加中文说明。
- 新增交互样式时必须覆盖 default、hover、active、selected、focus、disabled 中实际存在的状态。

## 标准代码骨架

```less
@import url('@/styles/variables.less');

.module-card {
  color: var(--text-color, rgba(0, 0, 0, 0.88));
  background: var(--bg-color-container, #fff);
  border: 1px solid var(--border-color-split, #f0f0f0);

  &__link {
    color: var(--primary-color, #3371ff);

    &:hover {
      color: var(--primary-color-hover, #4096ff);
    }
  }

  &.is-selected {
    color: var(--primary-color, #3371ff);
    background: color-mix(in srgb, var(--primary-color, #3371ff) 10%, transparent);
    border-color: var(--primary-color, #3371ff);
  }

  &:focus-visible {
    outline: none;
    box-shadow: 0 0 0 3px color-mix(in srgb, var(--primary-color, #3371ff) 15%, transparent);
  }
}
```

仅在 JS、图表或 Canvas 必须读取计算后色值时，优先使用 Ant Design Vue `theme.useToken()`；若消费微应用 CSS 变量，则通过 `getComputedStyle(document.documentElement)` 读取，不复制默认色板到业务常量。

## 验证流程

1. 扫描本次变更中的 `#hex`、`rgb/rgba`、`hsl/hsla`、渐变和 SVG 色值，逐项说明保留理由或替换为 Token。
2. 至少使用默认主色和一个明显不同的主色（例如红色）验证页面。
3. 检查文字、链接、图标、边框、背景、阴影以及 hover/active/selected/focus 状态是否同步变化。
4. 项目支持暗色模式时，再验证正文、次要文字、容器背景和边框；不得只验证主色。
5. 有原型截图时，主题适配与视觉还原必须同时通过，不能为像素接近而写死色值。

## 交付检查清单

- [ ] 已检查项目真实主题入口、Token 声明与运行时同步链路。
- [ ] 业务页面未硬编码品牌色及其交互态色阶。
- [ ] 主色透明态来自可动态更新的 Token，不依赖未同步的 `--primary-1` fallback。
- [ ] 状态色、中性色、容器背景和边框使用正确语义 Token。
- [ ] 已检查 SFC、Less、内联样式、TS 配置和 SVG，不只检查 `style.less`。
- [ ] 已用至少两种差异明显的主题色验证实际效果。
- [ ] 项目支持暗色模式时已完成暗色验收。
- [ ] 保留的固定色值均有明确、合理的非换肤语义。

## 失败兜底策略

- 找不到 Token 时，先查项目 `variables.less`、主题 store/config 和 `llms-full.txt`；禁止猜测变量名。
- 只有颜色值但没有语义 Token 时，先在统一主题源补充语义变量和运行时同步，再在页面消费。
- 第三方组件不跟随主题时，优先通过 ConfigProvider/component token 或其官方 CSS 变量桥接；最后才使用受控的深度样式覆盖。
- 浏览器目标不支持 `color-mix()` 时，在主题层生成并同步明确的透明态变量；不要在各页面散落固定透明色。
