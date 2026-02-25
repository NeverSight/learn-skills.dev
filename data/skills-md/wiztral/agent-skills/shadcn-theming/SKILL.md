---
name: shadcn-theming
description: Customize the Shadcn design system (Tailwind v4 supported). Update design tokens, safe refactoring, and color management.
---

# Shadcn Theming

Use this skill to modify the look and feel of the application (`globals.css` / `index.css`), add new colors, and manage design tokens.

## Documentation
- [Shadcn Theming](https://ui.shadcn.com/docs/theming)

## Workflow

### 1. File Identification & Validation
-   **Locate CSS**: `app/globals.css` (Next.js) or `src/index.css` (Vite).
    -   *If missing*: Ask user for the main global stylesheet location.
-   **Check Version**: Look for `tailwind.config.js` (v3) or `@import "tailwindcss"; / @theme { ... }` (v4).
    -   *If both missing*: The project might not be set up correctly. Use `shadcn-setup` or verify Tailwind installation.

### 2. Token Management & Evolution

#### Adding New Colors (OKLCH Preferred)
1.  **Generate Value**: Use the `convert_colors.js` script to get the OKLCH value for your color.
    ```bash
    node scripts/convert_colors.js "#ff0000"
    ```
2.  **Add to CSS**:
    -   **v4**: Add to `@theme` or `@layer base`.
    -   **v3**: Add to `:root` and `.dark` variables, then reference in `tailwind.config.js` `extend`.

#### Adaptive Design Strategy
When the user asks for high-level changes (e.g., "Make it softer"):
-   **Radius**: Increase `--radius` (e.g., `0.5rem` -> `1rem`).
-   **Colors**: Lower contrast or saturation using OKLCH chroma (C) values.
-   **Density**: Adjust spacing tokens if present.

#### Safe Refactoring
**Evolution over Destruction**:
-   **Do not** reuse a semantic token for a significantly different purpose (e.g., don't turn `destructive` blue).
-   **Create New**: If a new semantic meaning emerges (e.g., "Success State"), create `--success` / `--success-foreground`.
-   **Search First**: Before renaming `--primary`, search the entire codebase to understand impact.

### 3. Contrast & Accessibility
-   **Check Pairs**: When changing a background color (e.g., `--primary`), **IMMEDIATELY** check its pair (`--primary-foreground`) for contrast.
-   **Rule**: Ensure at least 4.5:1 contrast ratio for text.

### 4. Implementation Details (Tailwind v4)
In Tailwind v4, prefer CSS-first configuration:

```css
@theme {
  --color-primary: oklch(0.6 0.1 240);
  --color-primary-foreground: oklch(0.98 0 0);
  /* ... */
}
```

If the project uses `:root` variables (standard Shadcn), keep them:

```css
@layer base {
  :root {
    --primary: 0.6 0.1 240; /* Note: Shadcn often uses space-separated values for HSL/legacy. Adapt as needed. */
  }
}
```
*Note: If Shadcn is set up with CSS variables, respect the project's existing format (HSL vs OKLCH).*

## References
-   [Advanced Theming (Dark Mode & Typography)](references/advanced-theming.md)
