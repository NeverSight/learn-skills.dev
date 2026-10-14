---
name: format-storybook
description: Structure and organize Storybook files for scalability using battle-tested patterns. Based on "A Storybook format that scales with you" by Cassondra Roberts. Always use this skill when creating or editing any Storybook story file, writing template files, organizing a component library, setting up visual regression tests with Chromatic, or when the user asks anything about Storybook — even casual questions about file structure, controls, args, or how to document a component.
---

# Format Storybook

> Based on "[A Storybook format that scales with you](https://allons-y.llc/posts/2025-10-31/)" by Cassondra Roberts.

This skill provides patterns and conventions for building maintainable Storybook implementations that scale with your component library.

## Core Principles

1. **Compose, don't duplicate** - Import child component templates instead of copying markup
2. **Consistency over perfection** - Pick patterns and stick with them across your library
3. **Progressive disclosure** - Provide sensible defaults with optional controls for edge cases
4. **Self-documenting structure** - Organize files so the architecture is immediately clear

## File Structure

Keep Storybook assets close to component source files:

```
component/
├── component.js
├── component.css
└── stories/
    ├── component.stories.js    # Story definitions, controls, config
    ├── template.js              # Reusable render functions
    ├── component.docs.mdx       # [Optional] Documentation
    └── component.test.js        # [Optional] Visual regression grids
```

## Story File Structure

### Default Export

Every story file needs a default export with metadata:

```javascript
export default {
  title: "Components/Button",           // Sidebar hierarchy
  component: "Button",                  // Component name
  argTypes: { /* control definitions */ },
  args: { /* default values */ },
  parameters: { /* additional config */ },
  tags: [ /* organizational tags */ ]
};
```

### Organizing Controls

Group controls into logical categories for easy navigation:

- **State** - Interactive states (focused, open, disabled)
- **Variant** - Design variations (size, appearance)
- **Content** - Text, images, nested components
- **Advanced** - Edge cases and specialized configs

```javascript
argTypes: {
  size: {
    control: "select",
    options: ["sm", "md", "lg"],
    description: "The size of the button",
    table: { category: "Variant" }
  },
  isDisabled: {
    control: "boolean",
    description: "Whether the button is disabled",
    table: { category: "State" }
  }
}
```

**Tip**: Create shared control files in `.storybook/controls/` to reuse across components.

### Default Values

Always provide sensible defaults so the primary story renders in a useful state:

```javascript
args: {
  size: "md",
  isDisabled: false,
  label: "Click me"
}
```

Avoid meaningless "default" or "normal" options - use `undefined` instead.

### Creating Individual Stories

Use `.bind({})` to create stories that inherit from defaults:

```javascript
export const Default = Template.bind({});
Default.args = {};

export const Disabled = Template.bind({});
Disabled.args = {
  isDisabled: true
};

export const WithIcon = Template.bind({});
WithIcon.args = {
  icon: "settings",
  label: "Settings"
};
```

### Story Naming Conventions

Use concise, descriptive names:

- ✅ **Default** - Primary interactive example
- ✅ **With Icon** - Optional features
- ✅ **Loading State** - Specific states
- ✅ **Error Variant** - Edge cases
- ❌ **Button Default** - Don't repeat component name

### Useful Tags

- `!dev` - Hide stories from sidebar (documentation-only stories)
- `!autodocs` - Exclude from auto-generated docs
- Combine both for visual regression testing grids

## Template Files

The `template.js` file contains your rendering logic.

### Template Structure

Export a primary `Template(args, context)` function:

```javascript
import { html } from "lit";
import { classMap } from "lit/directives/class-map.js";
import { ifDefined } from "lit/directives/if-defined.js";

export const Template = (args, context) => {
  const {
    rootClass = "button",
    id,
    testId,
    customClasses = [],
    customStyles = {},
    size = "md",
    isDisabled = false,
    label = "Button"
  } = args;

  return html`
    <button
      class=${classMap({
        [rootClass]: true,
        [`${rootClass}--${size}`]: size,
        [`${rootClass}--disabled`]: isDisabled,
        ...customClasses.reduce((acc, c) => ({ ...acc, [c]: true }), {})
      })}
      style=${styleMap(customStyles)}
      id=${ifDefined(id)}
      data-testid=${ifDefined(testId)}
      ?disabled=${isDisabled}
    >
      ${label}
    </button>
  `;
};
```

### Standard Arguments

Accept these common arguments for flexibility:

- `rootClass` - Base CSS class
- `id` and `testId` - Identification and testing
- `customClasses` - Array of additional classes
- `customStyles` - Object of custom CSS properties

### Composition Pattern

Import and render nested component templates:

```javascript
import { Template as Popover } from "@design-system/popover/stories/template.js";
import { Template as Button } from "@design-system/button/stories/template.js";

export const Template = (args, context) => Popover({
  ...args,
  isOpen: true,
  trigger: (passthroughs, ctx) => Button({
    label: "Open Menu",
    ...passthroughs
  }, ctx),
  content: [/* child content */]
}, context);
```

### Lit Directives for Dynamic Behavior

- `classMap` - Conditional classes
- `styleMap` - Inline style objects
- `ifDefined` - Optional attributes (only render when defined)
- `when` - Conditional template regions

For interactive examples, use `context.updateArgs` to toggle state:

```javascript
onclick=${() => context.updateArgs({ isOpen: !args.isOpen })}
```

## Visual Regression Testing

For tools like Chromatic, create test grids in `component.test.js`:

```javascript
import { Template } from "./template.js";

export const TestGrid = {
  render: Template,
  parameters: {
    chromatic: { disableSnapshot: false }
  }
};

export const Default = TestGrid.bind({});
Default.tags = ["!autodocs", "!dev"];
Default.args = {
  // Test-specific args
};
```

**Strategy**: Group many states and variants into a single snapshot grid to optimize test runs.

## Accessibility

Always provide ARIA attributes through arguments:

```javascript
argTypes: {
  ariaHasPopup: {
    control: "select",
    options: ["true", "false", "menu", "dialog"],
    table: { category: "Advanced" }
  },
  ariaExpanded: {
    control: "boolean",
    table: { category: "State" }
  }
}
```

Use `ifDefined` so they only render when needed:

```javascript
aria-haspopup=${ifDefined(args.ariaHasPopup)}
aria-expanded=${ifDefined(args.ariaExpanded)}
```

## Documentation and Metadata

### Design Links

Connect stories to design files:

```javascript
parameters: {
  design: {
    type: "figma",
    url: "https://www.figma.com/..."
  }
}
```

### Package Information

Include metadata for documentation:

```javascript
import packageJson from "../package.json";

export default {
  parameters: {
    packageJson,
    status: { type: "stable" } // or "experimental", "deprecated"
  }
};
```

### Component Status

Use tags to communicate lifecycle:

```javascript
tags: ["stable", "migrated"]
```

## Setup Recommendations

### Path Aliasing

Configure package aliases in Storybook to avoid relative imports:

```javascript
// .storybook/main.js
export default {
  viteFinal: (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      "@design-system": path.resolve(__dirname, "../packages")
    };
    return config;
  }
};
```

Use in imports:

```javascript
// ✅ Good
import { Template } from "@design-system/button/stories/template.js";

// ❌ Avoid
import { Template } from "../../../button/stories/template.js";
```

### Rendering Library (Vanilla Projects)

For projects without a framework, use `lit` for templates:

```bash
npm install lit
```

Benefits:
- Lightweight and performant
- Conditional classes and styles
- Optional attributes
- Dynamic rendering utilities

### Auto-Generated Titles

Map folder structure to sidebar hierarchy:

```javascript
// .storybook/main.js
export default {
  stories: [
    {
      directory: '../packages/components',
      files: '*.stories.*',
      titlePrefix: 'Components',
    },
  ],
};
```

## Dos and Don'ts

### Do

- ✅ Import child component templates instead of duplicating markup
- ✅ Keep `template.js` focused on the component itself
- ✅ Categorize controls and set sensible defaults
- ✅ Hide VRT-only stories from sidebar using tags
- ✅ Reuse shared controls from a common location
- ✅ Include proper ARIA attributes
- ✅ Link to design files in parameters

### Don't

- ❌ Hardcode IDs - use a helper function to generate random IDs
- ❌ Duplicate markup from nested components
- ❌ Skip accessibility attributes
- ❌ Create stories for every possible variant (let users explore via controls)
- ❌ Use relative imports when aliases are available
- ❌ Add meaningless "default" or "normal" variant options

## Quick Reference

### Minimal Story File

```javascript
import { Template } from "./template.js";

export default {
  title: "Components/Button",
  component: "Button",
  argTypes: {
    size: {
      control: "select",
      options: ["sm", "md", "lg"],
      table: { category: "Variant" }
    }
  },
  args: {
    size: "md",
    label: "Click me"
  }
};

export const Default = Template.bind({});
```

### Minimal Template File

```javascript
import { html } from "lit";
import { classMap } from "lit/directives/class-map.js";

export const Template = (args) => {
  const { rootClass = "button", size = "md", label = "Button" } = args;
  
  return html`
    <button class=${classMap({
      [rootClass]: true,
      [`${rootClass}--${size}`]: size
    })}>
      ${label}
    </button>
  `;
};
```

## References

Read these when you need more detail than the guidelines above:

- [storybook-docs.md](references/storybook-docs.md) - Read when you need to look up specific Storybook APIs, addon configuration, or testing integrations (Chromatic, test runner)
- [lit-templates.md](references/lit-templates.md) - Read when you need details on Lit directives (`classMap`, `styleMap`, `ifDefined`, `when`) or template rendering patterns
- [article.md](references/article.md) - Read when you want the philosophy and reasoning behind these patterns, or need comprehensive end-to-end examples
