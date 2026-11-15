---
name: stario-tailwind-daisyui
description: Style a Stario app with Tailwind CSS v4 and DaisyUI through the standalone tailwindcss binary, with no Node, and a light and dark theme switch. Use when the user mentions Tailwind, DaisyUI, utility classes, themes, dark mode, or wants the app to look finished without writing CSS. The setup comes from `stario-create add tailwind`.
---

# Tailwind and DaisyUI without Node

Do not install Tailwind by hand, and never use `npm` or `npx`. Run the kit in the root of the app:

```bash
uvx stario-create@latest add tailwind
just css
```

The kit writes:

| File | What it holds |
| --- | --- |
| `justfile` | `tailwind` gets the pinned binary and the DaisyUI plugin once per machine. `css` builds; `css-watch` rebuilds next to `just dev`. |
| `frontend/src/input.css` | Tailwind scans `app/**/*.py`. DaisyUI with `light` and `dark`. `dark:` follows `data-theme`. |
| `app/assets.py` | `STYLE_CSS` is `css/output.css`. `SCRIPTS` loads `theme.js`. |
| `app/common/shell.py` | `data-theme` on `<html>`, kept through each morph. The theme restore before the first paint (the only inline script). A DaisyUI toast. |
| `static/js/theme.js` | `app.theme.toggle()`, kept in `localStorage`. |

A file that the app has changed is not replaced. The command prints `merge by hand: <file>` and the path of the kit version. Read it and merge its lines. Commit `static/css/output.css` after each `just css`. Yard serves the committed file.

## The theme switch

Put the button where the app wants it, often in a page header:

```python
h.Button(
    classes("btn", "btn-ghost", "btn-circle"),
    {"type": "button", "aria-label": "Switch theme"},
    data.on("click", "app.theme.toggle()"),
    h.Span(classes("dark:hidden"), "Dark"),
    h.Span(classes("hidden", "dark:inline"), "Light"),
)
```

The labels follow `dark:` utilities, so no script updates them. The server does not store the theme.

A custom theme replaces the `@plugin` block in `input.css`:

```css
@plugin "../daisyui.mjs" {
  themes: false;
}

@plugin "../daisyui-theme.mjs" {
  name: "app";
  default: true;
  color-scheme: light;
  --color-base-100: #f7f6f1;
  --color-base-content: #1a1f24;
  --color-primary: #3d4a6b;
  --color-primary-content: #f7f6f1;
}
```

## Classes in views

```python
h.Button(classes("btn", "btn-primary"), data.on("click", at.post(SAVE.href())), "Save")
h.Input(classes("input", "input-bordered", "w-full"), {"type": "text"}, data.bind("title"))
h.Div(classes("card", "bg-base-200", "shadow"), h.Div(classes("card-body"), ...))
```

- A class is generated only when its literal is in a `.py` file under `app/`. Use `classes("btn", "btn-primary")`, not string concatenation.
- DaisyUI component class first, Tailwind utilities after: `btn btn-primary w-full`.
- Theme colors only: `bg-base-100`, `bg-base-200`, `text-base-content`, `bg-primary`. No raw `bg-gray-100`, so the theme stays switchable.
- Layout with `flex`, `grid`, `gap-*`, `p-*`. No custom CSS for layout.
- Custom CSS goes into `input.css` under `@layer components` only when no DaisyUI class exists. Name it after the app: `.app-stage`.
- A class that only `static/js/` adds needs `@source "../../static/js/*.js";`. Better: the HTML holds the class, and `data.class_` toggles it.
- A modal is `<dialog class="modal">` with `data.preserve_attr("open")`. The server never renders it open.
- A drawer toggle is a checkbox the client owns: `data.preserve_attr("checked")`.

## Checks

- After a class change: `just css`, then commit `static/css/output.css`.
- A class that does not apply: check that its literal is in a `.py` file under `app/`, then `just css`. A test can assert it: `assert "btn-primary" in (ROOT / "static/css/output.css").read_text()`, with `ROOT` as in `tests/test_js.py`.
- Whether the page looks right is a question for the user, who watches the app. Do not open a browser or use computer use for a style.
