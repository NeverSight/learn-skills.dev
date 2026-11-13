---
name: svelte-styling
license: Apache-2.0
description: "Svelte 5 样式技能。当用户需要使用作用域样式、:global、CSS 自定义属性、class 指令、style: 指令、嵌套 style、或理解 Svelte 的样式隔离机制时使用。"
---

# Svelte Styling Reference (Svelte 5)

本技能覆盖 Svelte 组件的样式系统，包括作用域样式、全局样式、CSS 自定义属性、class 处理、`style:` 指令、嵌套 `<style>` 和 scoped keyframes。

## When to use this skill

当用户需要编写 Svelte 组件的样式、处理样式隔离、CSS 变量传递、`style:` 指令、动画 keyframes、或理解 Svelte 编译器如何处理样式时使用本技能。

## Critical: Scoped Styles

`<style>` 块中的 CSS 默认**作用域化**——仅影响当前组件内的元素：

```svelte
<style>
  p { color: burlywood; }
  .container { padding: 1em; }
</style>
```

编译时 Svelte 为作用域内的选择器自动添加哈希类（如 `svelte-123xyz`）。

### 特异性（Specificity）

Scoped 选择器额外增加 **+0-1-0** 特异性（来自作用域类），可能覆盖全局相同选择器：

```css
/* 全局 */
p { color: blue; }

/* 组件内（scoped，优先级更高） */
p { color: red; }
```

### `:where()` 包装

当同一作用域类需要出现在选择器中多次时，**只有第一次**实际贡献特异性；后续出现被包裹在 `:where(.svelte-xyz123)` 中，贡献零特异性。这避免了深层选择器（如 `.a .b .c`）的特异性爆炸。

### Scoped Keyframes

`@keyframes` 名称也会自动作用域化，同一组件内 `animation: name` 引用会被重写以匹配：

```svelte
<style>
  @keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-20px); }
  }
  .animated { animation: bounce 1s; }  /* 编译为 bounce-svelte-abc123 */
</style>
```

### 何时样式不生效

- 元素由子组件渲染（scoped 不会穿透组件边界）
- `{@html}` 内容（没有作用域类）
- 类名是动态/程序化添加的，且选择器未使用 `:global(...)`
- 选择器不匹配模板中实际存在的元素
- 在 `style=""` 属性或 JS 中使用 scoped keyframe 名称（用 `-global-` 解决）

## Critical: Global Styles

### `:global(...)` 单选择器

```svelte
<style>
  :global(body) { margin: 0; }          /* 全局 body */
  div :global(strong) { color: goldenrod; } /* 嵌套全局 */
  p:global(.big.red) { font-weight: bold; } /* 带条件 */
</style>
```

- `:global(selector)` — 整个选择器退出作用域。
- `parent :global(child)` — 父级保留作用域，子级不保留（最常用形式）。
- `tag:global(.class.class)` — 元素仍带作用域类，但触发类不需出现在模板中（适用于第三方库运行时添加的类）。

### `:global { ... }` 块（多选择器）

```svelte
<style>
  :global {
    p { margin: 1em; }
    .theme-dark { --bg: #111; }
  }

  .parent :global {
    .foo .bar { color: red; }  /* .parent 是 scoped，.foo .bar 是全局 */
  }
</style>
```

`:global` 块中的选择器按原样发出，**不**降低特异性——只有 `.foo .bar` 自身的特异性。

### 全局 Keyframes

在 keyframe 名称前加 `-global-`：

```svelte
<style>
  @keyframes -global-my-animation-name {
    0% { opacity: 0; }
    100% { opacity: 1; }
  }
</style>
```

编译后 `-global-` 前缀被移除，成为 `my-animation-name`，可被其他组件、`<style>` 属性、JS 引用。

> 编译器**只**重写同一 `<style>` 块内的 `animation` 引用。`style="..."` 属性、`{@html}` 内容、JS、`style:color` 指令中的 keyframe 名称**不会**被重写——这些地方需要 `-global-` 名称。

## Critical: CSS Custom Properties

### 传入自定义属性

```svelte
<Slider bind:value --track-color="black" --thumb-color="rgb(255 0 0)" />
```

编译时 Svelte 包裹一层 `svelte-css-wrapper`（或 SVG 中的 `<g>`）承载内联 style：

```svelte
<svelte-css-wrapper style="display: contents; --track-color: black; --thumb-color: rgb(255 0 0)">
  <Slider ... />
</svelte-css-wrapper>
```

> 包装元素有 `display: contents` 但**仍**会出现在 `>` 子选择器匹配中——必要时改用后代选择器。

### 组件内读取

```svelte
<style>
  .track { background: var(--track-color, #aaa); }
  .thumb { background: var(--thumb-color, blue); }
</style>
```

### CSS 自定义属性可级联

无需直接传值，只要父元素定义了 CSS 变量，子组件即可读取：

```css
/* 全局 */
:root { --primary: #ff3e00; }
```

## Critical: `style:` Directive

`style:` 指令是 `style="..."` 属性的简写，每个属性一个指令。

```svelte
<div style:color="red">A</div>           <!-- 字符串字面量 -->
<div style:color={myColor}>B</div>        <!-- 表达式 -->
<div style:color>C</div>                  <!-- 简写：变量名与属性名相同 -->
```

### 多个样式

```svelte
<div style:color style:width="12rem" style:--columns={columns}>...</div>
```

### CSS 自定义属性

`style:--var` 设置 CSS 变量：

```svelte
<div style:--columns={columns} style:--gap="1rem">...</div>
```

### `!important` 修饰符

`style:color|important="red"` → 编译为 `style="color: red !important"`。

### 优先级

`style:` 指令**胜出**于同元素上的 `style=""` 属性——即使 `style=""` 中使用了 `!important`：

```svelte
<div style:color="red" style="color: blue !important">This will be red</div>
```

### 数值单位

数字不会自动加单位：

```svelte
<div style:width={10}>...</div>          <!-- 错误：width: 10 -->
<div style:width="{10}px">...</div>      <!-- 正确 -->
```

## Critical: class Attribute

Svelte 5.16+ 的 `class` 属性支持对象和数组（用 `clsx` 处理）。

### 对象形式

```svelte
<div class={{ cool: isCool, large: isLarge }}>...</div>
```

### 数组形式

```svelte
<div class={[faded && 'saturate-0 opacity-50', large && 'scale-200']}>...</div>
```

### 混合

```svelte
<Button class={['btn', props.class]} />
```

### 类型安全

```svelte
<script lang="ts">
  import type { ClassValue } from 'svelte/elements';
  let { class: cls }: { class: ClassValue } = $props();
</script>
<div class={['original', cls]}>...</div>
```

### 5.16 之前的 falsy 行为

历史原因：`class={false}` 会被序列化为 `class="false"`，但 `class={undefined}` / `class={null}` 会让属性消失。Svelte 未来版本会让所有 falsy 值省略 class。

## Critical: `class:` Directive（已不推荐）

Svelte 5.16+ 推荐用 `class={}` 对象/数组形式替代 `class:` 指令：

```svelte
<!-- 等价 -->
<div class={{ cool, lame: !cool }}></div>
<div class:cool class:lame={!cool}></div>
```

## Critical: Nested `<style>` Elements

一个组件只能有**一个顶层** `<style>` 块，但可以嵌套 `<style>` 标签（不经过作用域处理，直接插入 DOM）：

```svelte
<div>
  <style>
    /* 原生 style 标签，无作用域，规则全局生效 */
    div { color: red; }
  </style>
</div>
```

**使用场景：**
- 主题 token 的 `{#if}` 切换（变量随切换增删）
- 第三方组件自带的 CSS
- 动态主题变量
- 邮件 / SVG 模板

**注意：** 嵌套 `<style>` 中的 `@keyframes` 名称是**全局**的，**不会**被重写。多个组件中同名 keyframe 会冲突。

## Critical: `{@html}` and Scoped Styles

`{@html}` 注入的内容**没有**作用域类，scoped 选择器不会匹配。用 `:global(...)` 解决：

```svelte
<style>
  :global(.highlight) { color: red; }
</style>
```

**警告：** 永远不要用 `:global(...)` 来样式化你无法完全控制的 HTML——XSS 风险。

## Quick Fixes

| 问题 | 解决方案 |
|------|----------|
| 样式不生效 | 检查 scoped 哈希是否覆盖；用 `:global` |
| 组件样式传不进去 | 用 CSS 自定义属性（`--var`）而非 scoped 选择器 |
| 父组件不能覆盖子组件的样式 | 用 `--var` 传值，或用 `:global`（不推荐） |
| 全局样式被组件 scoped 覆盖 | scoped 提升 +0-1-0 特异性；用 `:where()` 或增加全局选择器特异性 |
| Tailwind 类不生效 | JIT 找不到动态拼接的类名；用 `class={[...]}` 数组映射或 `safelist` |
| 动态 `style="animation: x"` 找不到 keyframe | keyframe 是 scoped 的；用 `@keyframes -global-x` |
| `style:` 不生效 | 检查表达式语法；数值需要单位 |
| `> .child` 不匹配 | 父传 `--var` 时包了 `svelte-css-wrapper`；改用后代选择器 |
| slot 内容样式不到 | 用 `::slotted(selector)` 从父组件样式化 |

## Gotchas

1. **Scoped 样式隔离** — 通过哈希类实现，不会真正"隐藏"样式（查看页面源码可见）
2. **Scoped 选择器 +0-1-0 特异性** — 总是高于相同形状的全局选择器
3. **`@keyframes` 名称也 scoped** — `style="animation: name"` 找不到 scoped 名称（用 `-global-`）
4. **`{@html}` 内容不受 scoped 影响** — 插入的 HTML 无作用域类
5. **CSS 变量不需要 scoped** — `var(--custom)` 天然跨作用域和级联
6. **`svelte-css-wrapper` 元素** — 父传 `--var` 时插入，破坏 `>` 子选择器
7. **`:global` 不降低特异性** — 它退出作用域，但不退出 specificity
8. **嵌套 `<style>` 是全局** — 不走 Svelte 编译器，原样插入 DOM
9. **编译器只在同 `<style>` 块内重写 `animation`** — 其他地方需 `-global-`
10. **`<style>` 属性和 JS 中的 scoped keyframe 名称** — 不被重写

## FAQ

**Q: 如何让样式影响子组件内部？**
A: 两种方式：① 父组件传入 CSS 自定义属性（推荐）；② 用 `:global`（影响全局，会破坏封装）。

**Q: Svelte 编译后 class 名称是什么？**
A: 形如 `svelte-123xyz` 的哈希，组件级唯一。

**Q: scoped 样式会赢过全局样式吗？**
A: 是。scoped 提升 +0-1-0 特异性。同形状的全局 `p` 输给 scoped `p`。

**Q: 何时用 `:global` 而不是 CSS 变量？**
A: 当你必须控制选择器本身（位置、选择什么），而不是传入值时，用 `:global`。大多数"传值"的场景用 CSS 变量更好。

**Q: 为什么 `class:[...]` 数组中的 falsy 值不会变成字符串？**
A: Svelte 用 clsx 规则过滤掉 `false`/`null`/`undefined`/`""`/`0`。`class={false}` 才会变成 `class="false"`（历史行为，5.16+ 已改变数组形式）。

**Q: 嵌套 `<style>` 中的规则为什么是全局的？**
A: 嵌套 `<style>` 不经过 Svelte 编译器的 scoping 处理，按原样插入 DOM。浏览器会像处理普通 `<style>` 一样解析它。

**Q: scoped keyframe 可以从外部触发吗？**
A: 不行。scoped keyframe 名称在编译时被改写，外部无法用裸名引用。用 `@keyframes -global-name`。

**Q: `style:` 指令和 `style="..."` 属性同时用会怎样？**
A: `style:` 胜出，即使 `style=""` 用了 `!important`。这是 Svelte 5 的设计。

**Q: 我能用 `bg-${color}-500` 这样的模板字符串做动态 Tailwind 类吗？**
A: 不能可靠工作——JIT 看不到完整类名。用查找表（`{ red: 'bg-red-500', ... }`）或 `safelist`。

## Examples

| File | Description |
|------|-------------|
| [examples/README.md](./examples/README.md) | Entry point listing all example files with descriptions |
| [examples/scoped-styles.md](./examples/scoped-styles.md) | Scoped styles, specificity, `:where()` trick, when styles don't apply, compiled output, svelte-css-wrapper |
| [examples/scoped-keyframes.md](./examples/scoped-keyframes.md) | `@keyframes` scoping, the `-global-` prefix, sharing animations, triggering from JS, prefers-reduced-motion |
| [examples/global-patterns.md](./examples/global-patterns.md) | `:global(...)` single, compound, nested, block, and when to use vs CSS custom properties |
| [examples/style-directive.md](./examples/style-directive.md) | `style:property`, `style:--var`, `\|important`, expressions, multiple styles, value coercion |
| [examples/nested-style.md](./examples/nested-style.md) | Raw `<style>` tags inside templates, `{#if}`/`{#each}` style fragments, lifecycle, gotchas |
| [examples/tailwind.md](./examples/tailwind.md) | Tailwind CSS, arbitrary values, dynamic theming with custom properties, safelist, twMerge |

## References

| File | Description |
|------|-------------|
| [references/README.md](./references/README.md) | Entry point listing all reference files with descriptions |
| [references/scoped-deep.md](./references/scoped-deep.md) | Deep dive into scoping mechanism, hash generation, `:where()` wrapping, nested `<style>`, edge cases |
| [references/scoped-keyframes.md](./references/scoped-keyframes.md) | Scoped keyframes, the `-global-` prefix, sharing across components, rewriter rules |
| [references/global-reference.md](./references/global-reference.md) | Full reference for `:global(...)` single, nested, block, compound, with cascade and transform examples |
| [references/specificity.md](./references/specificity.md) | Specificity interactions, `:where()` / `:is()` / `:not()`, override strategies, cascade order |
| [references/style-directive.md](./references/style-directive.md) | All `style:` forms, `style:--var` serialization, `\|important`, value coercion, precedence |
| [references/css-custom-properties.md](./references/css-custom-properties.md) | CSS Custom Properties: passing, reading, cascading, dynamic updates |
| [references/class-directive.md](./references/class-directive.md) | class vs class: directive, ClassValue types, clsx patterns |
