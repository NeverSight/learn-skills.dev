---
name: check-svg
description: 检查项目中 SVG 的使用是否符合最佳实践：SVG 需作为独立组件（非内联），并通过 import 使用。
---

# SVG 组件检查 Skill

## 目标

- 确保项目中没有内联的 `<svg>` 出现在业务组件文件中。
- 确保所有 SVG 被封装为独立的 React/TS 组件并从组件中导入使用。

## 检查项（必须全部满足）

1. 禁止在业务组件（例如 `.tsx`, `.jsx` 文件）内直接写 `<svg>` 标签。
2. 所有 SVG 必须封装为组件（按项目约定放置，例如 `src/components/icons/` 或 `components/icons/`）。
3. 使用图标时应通过 `import IconName from '.../icons/IconName'` 引入并以 `<IconName />` 使用。

## 检查方法（审查者/工具参考）

- 手动审查：在变更的文件中查找 `<svg` 标签，确认是否为内联；若是内联则要求迁移。
- 推荐查找正则（示例，供人工或工具使用）：
  - 内联 SVG 检测：`<svg[^>]*>[\s\S]*?<\/svg>`

- 替换建议：将内联 `<svg>` 内容提取为 `IconName.tsx`（PascalCase），放入 `components/icons/`，并在原处用 `import` + `<IconName />` 替换，同时把原有的 `width/height/fill/className` 等迁移为 props。

## 示例

不合格（示例）

```tsx
// Button.tsx
export const Button = () => (
  <button>
    <svg viewBox="0 0 24 24">
      <path d="..." />
    </svg>
  </button>
);
```

## 复核准则

- 检查是否存在内联 `<svg>`；若存在，请要求将其抽离为组件并更新使用处。
- 检查导入路径与图标目录是否符合团队约定。

## 参考

- 项目已有最佳实践：[skills/svg-icon-best-practice/SKILL.md](../svg-icon-best-practice/SKILL.md)
