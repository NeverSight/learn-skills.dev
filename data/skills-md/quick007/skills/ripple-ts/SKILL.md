---
name: ripple-ts
description: Skill that helps agents work with the framework RippleTS. Links back to the llms.txt, and provides info that might be helpful to the LLM.
---

# RippleTS Skill

This skill helps you work with RippleTS, a TypeScript UI framework that combines the best parts of React, Solid, and Svelte.

## Documentation Links

- **AI/LLM Documentation**: https://www.ripple-ts.com/llms.txt (comprehensive reference, read this)
- **Official Docs**: https://www.ripple-ts.com/docs
- **GitHub**: https://github.com/Ripple-TS/ripple

## Key Concepts for LLMs

### File Extension
RippleTS uses `.ripple` files with TypeScript-first JSX-like syntax.

### Component Definition
Components use the `component` keyword, NOT functions returning JSX:

```ripple
component Button(props: { text: string, onClick: () => void }) {
  <button onClick={props.onClick}>
    {props.text}
  </button>
}
```

### CRITICAL RULES

1. **Text Must Be in Expressions**: Unlike HTML/JSX, raw text is NOT allowed. Always wrap text in curly braces:
   - ❌ `<div>Hello</div>`
   - ✅ `<div>{"Hello"}</div>`

2. **Templates Only Inside Components**: JSX-like elements can ONLY exist inside `component` function bodies, not in regular functions or variables.

### Reactivity

Use `track()` to create reactive values and `@` to access them:

```ripple
import { track } from 'ripple';

export component Counter() {
  let count = track(0);
  
  <div>
    <p>{"Count: "}{@count}</p>
    <button onClick={() => @count++}>{"Increment"}</button>
  </div>
}
```

### Reactive Collections

Use special syntax for fully reactive collections:
- Arrays: `#[1, 2, 3]` or `new TrackedArray(1, 2, 3)`
- Objects: `#{a: 1, b: 2}` or `new TrackedObject({a: 1})`

### Control Flow

Templates support inline control flow:

```ripple
component App(props: { items: string[] }) {
  <div>
    if (props.items.length > 0) {
      <ul>
        for (const item of props.items; index i) {
          <li>{item}</li>
        }
      </ul>
    } else {
      <p>{"No items"}</p>
    }
  </div>
}
```

### Scoped CSS

Add `<style>` elements directly in components for scoped styles:

```ripple
component StyledComponent() {
  <div class="container">
    <h1>{"Styled Content"}</h1>
  </div>
  <style>
    .container {
      background: blue;
      padding: 1rem;
    }
  </style>
}
```

### Dynamic Classes

Use object/array syntax for conditional classes (powered by clsx):

```ripple
let includeBaz = track(true);
<div class={{ foo: true, bar: false, baz: @includeBaz }}></div>
```

## Installation & Setup

```bash
# Create new project from template
npx degit Ripple-TS/ripple/templates/basic my-app
cd my-app
npm i && npm run dev

# Or install in existing project
npm install ripple
npm install --save-dev '@ripple-ts/vite-plugin'
```

## VSCode Extension

- **Name**: "Ripple for VS Code"
- **ID**: `Ripple-TS.ripple-ts-vscode-plugin`

## React Compatibility

Ripple supports embedding React components using `<tsx:react>` blocks. Requires `@ripple-ts/compat-react` package and configuration in `mount()`.

## Best Practices

1. Use `track()` for reactive state
2. Wrap all text content in expressions `{}`
3. Use scoped `<style>` elements for component styling
4. Use `effect()` for side effects, not direct reactive access
5. Keep components focused with TypeScript interfaces for props

## Limitations

- Currently SPA-only (SSR coming soon)
- No hydration support yet
- Tracked objects cannot be created at module/global scope
