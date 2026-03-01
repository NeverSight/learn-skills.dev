---
name: wix-cli-site-component
description: "Use when building React site components with editor manifests for Wix CLI applications."
---

# Wix Site Component Builder

Creates production-quality React site components with editor manifests for Wix CLI applications. Site components are React components that integrate with the Wix Editor, allowing site owners to customize content, styling, and behavior through a visual interface.

## Architecture

Site components consist of **four required files**:

### 1. Component Manifest (`manifest.json`)

Defines the contract between the React component and Wix ecosystem:

- **editorElement**: Root element configuration (selector, displayName, archetype, layout)
- **cssProperties**: CSS API for styling customization
- **data**: Data API for content configuration
- **elements**: Nested element definitions for granular editing
- **behaviors**: Editor interaction behaviors

### 2. React Component (`component.tsx`)

Production-ready React functional component:

- Implements props interface matching manifest data structure
- Applies className and id to root element
- Handles element removal state via `wix.elementsRemovalState`
- Uses sub-component pattern for nested elements
- Includes proper TypeScript typing and error handling

### 3. CSS Styles (`style.css`)

Modern CSS with responsive design:

- Synced selectors with manifest and React classNames
- CSS variables for dynamic styling
- Responsive design without media queries (flexbox, grid, clamp)
- Pointer events enabled for editor elements
- No inline styles for static values
- Each selector once only, `box-sizing: border-box` all elements
- NO `transition: all`, NO media queries (except `prefers-reduced-motion`)
- Root display: Declare `--display: [value]` CSS variable, then use `display: var(--display)` on root

### 4. TypeScript Types (`types.ts`)

Strict type definitions:

- Props interfaces for all components
- Data type mappings (text → string, image → Image object)
- Element props structure with optional chaining
- Wix system types (Wix interface, REMOVED type)

## Component Manifest Structure

**You MUST read [MANIFEST_GUIDELINES.md](references/MANIFEST_GUIDELINES.md) before implementing a site component.** It contains the complete manifest structure, all data types, element configurations, and required patterns.

The manifest defines the editor contract using these key sections:

### installation (Initial Placement)

```json
{
  "installation": {
    "staticContainer": "HOMEPAGE",
    "initialSize": {
      "width": { "sizingType": "pixels", "pixels": 400 },
      "height": { "sizingType": "pixels", "pixels": 300 }
    }
  }
}
```

- **staticContainer**: Use `"HOMEPAGE"` for automatic installation on Harmony editor
- **initialSize**: Defines initial dimensions with `sizingType` options:
  - `"content"` - Auto-size based on content
  - `"stretched"` - Fill available space
  - `"pixels"` - Fixed pixel dimension (requires `pixels` property)

### editorElement (Root Configuration)

```json
{
  "selector": ".component-name",
  "displayName": "Component Name",
  "archetype": "Container",
  "layout": {
    "resizeDirection": "horizontalAndVertical",
    "contentResizeDirection": "horizontal"
  },
  "cssProperties": {
    "backgroundColor": {
      "displayName": "Background Color",
      "defaultValue": "#ffffff"
    }
  },
  "data": {
    "columns": {
      "dataType": "number",
      "displayName": "Number of Columns",
      "number": { "minimum": 1, "maximum": 4 }
    }
  },
  "elements": {
    "title": {
      "elementType": "inlineElement",
      "inlineElement": {
        "selector": ".component-name__title",
        "displayName": "Title",
        "data": {
          "titleText": {
            "dataType": "text",
            "displayName": "Title Text"
          }
        },
        "behaviors": {
          "selectable": true,
          "removable": true
        }
      }
    }
  }
}
```

### Data Types Reference

| Type | Runtime Value | Use Case |
|------|---------------|----------|
| `text` | string | Names, titles, descriptions |
| `textEnum` | string | Predefined options |
| `number` | number | Quantities, dimensions |
| `booleanValue` | boolean | Toggles, flags |
| `a11y` | Object | Accessibility attributes |
| `link` | `{ href, target, rel }` | Navigation links |
| `image` | `{ uri, url, alt, width, height }` | Images |
| `video` | Video object | Media content |
| `vectorArt` | Sanitized SVG object | Icons, graphics |
| `localDate` | string (YYYY-MM-DD) | Date values |
| `localTime` | string (hh:mm) | Time values |
| `webUrl` | string | External URLs |
| `richText` | string (HTML) | Formatted content |
| `arrayItems` | Array | Collections, lists |
| `direction` | string | HTML dir attribute |
| `menuItems` | Array of menu items | Navigation menus |

### CSS Properties Reference

Common CSS properties for styling customization:

- **Layout**: `display`, `gap`, `padding`, `margin`, `width`, `height`
- **Typography**: `font`, `fontSize`, `fontWeight`, `textAlign`, `color`
- **Background**: `backgroundColor`, `backgroundImage`
- **Border**: `border`, `borderRadius`, `boxShadow`
- **Positioning**: `alignItems`, `justifyContent`, `flexDirection`

**Complete CSS properties reference:** See [CSS_GUIDELINES.md](references/CSS_GUIDELINES.md) for all CSS properties, variable patterns, and styling best practices.

## React Component Patterns

**Complete reference:** See [REACT_PATTERNS.md](references/REACT_PATTERNS.md) for detailed component architecture, all coding patterns, and implementation examples.

### Props Structure

```typescript
interface ComponentProps {
  // Standard props (always present)
  className: string;
  id: string;
  wix?: Wix;

  // Component-level data (from editorElement.data)
  columns?: number;
  layout?: string;

  // Element props (from elements definitions)
  elementProps?: {
    title?: {
      titleText?: string;
      wix?: Wix;
    };
    button?: {
      buttonText?: string;
      buttonLink?: Link;
      wix?: Wix;
    };
  };
}
```

### Sub-Component Pattern

Extract every distinct UI element into named sub-components:

```typescript
// Title sub-component
interface TitleProps {
  titleText?: string;
  className: string;
}

const Title: FC<TitleProps> = ({ titleText = "Default Title", className }) => (
  <h2 className={className}>{titleText}</h2>
);

// Main component
const ProductCard: FC<ProductCardProps> = ({
  className,
  id,
  elementProps,
  wix
}) => {
  const removalState = wix?.elementsRemovalState || {};

  return (
    <div className={`product-card ${className}`} id={id}>
      {!removalState['title'] && (
        <Title
          className="product-card__title"
          {...elementProps?.title}
        />
      )}
      {!removalState['button'] && (
        <Button
          className="product-card__button"
          {...elementProps?.button}
        />
      )}
    </div>
  );
};
```

### Conditional Rendering

All elements must be conditionally rendered based on removal state:

```typescript
const removalState = wix?.elementsRemovalState || {};

return (
  <div className={`component ${className}`} id={id}>
    {!removalState['elementKey'] && <Element />}
  </div>
);
```

## CSS Guidelines

### Responsive Design Strategy

Components live in user-resizable containers (300-1200px) within varying viewports:

- **Root element**: `width: 100%; height: 100%`
- **Layout structure**: Use CSS Grid and Flexbox for fluid responsiveness
- **Typography**: Use `clamp()` for fluid scaling
- **Spacing**: Fixed or tight clamp spacing (≤50% variation)

### CSS Variables for Dynamic Styling

```css
.component {
  --display: block;
  --background-color: #ffffff;
  --text-color: #333333;

  display: var(--display);
  background-color: var(--background-color);
  color: var(--text-color);
  pointer-events: auto;
}
```

### Selector Synchronization

**CRITICAL**: CSS selectors must match manifest selectors and React classNames exactly:

- React: `className="product-card__title"`
- CSS: `.product-card__title { ... }`
- Manifest: `"selector": ".product-card__title"`

## Design Guidelines

**Complete reference:** See [DESIGN_SYSTEM.md](references/DESIGN_SYSTEM.md) for visual design principles, creative guidelines, and aesthetic best practices.

### Spacing as Communication

| Relationship | Value | Use Case |
|---|---|---|
| Tight (icon + label) | 0.25-0.5rem (4-8px) | Clustering related items |
| Same category | 1-1.5rem (16-24px) | Card sections, form fields |
| Different sections | 2-3rem (32-48px) | Major content blocks |
| Emphasis/Drama | 4rem+ (64px+) | Hero content, luxury feel |

### Visual Consistency

- **Corner Radius**: All similar elements share same radius (0-4px sharp, 6-12px rounded)
- **Shadow Levels**: Max 3 levels (rest, hover, floating)
- **Element Heights**: Consistent heights for similar elements
- **Color Strategy**: Use full palette purposefully for hierarchy and zones

### Creative Exploration

Push beyond obvious solutions:

- **Cards**: Asymmetric grids, overlapping elements, thick accent borders
- **Lists**: Alternating styles, spotlight patterns, color rhythm
- **Interactive Elements**: Split buttons, colored icon circles, smooth transitions
- **Content Hierarchy**: Large numbers for stats, quote callouts, whitespace dividers

## Component Elements Guidelines

### One Element = One Manifest Entry

Each distinct visual part requires a separate manifest element:

- ✅ 3 buttons → 3 separate elements
- ✅ Image + text → 2 separate elements
- ❌ Multiple items grouped as one element

### Data Scoping Rules

**editorElement.data** - Component-wide configuration only:
- ✅ Layout enums, numbers (columns: 3, speed: 500)
- ❌ Text, links, images (belongs to elements)
- ❌ show/hide booleans (use removable: true instead)

**elements[key].data** - Content for that specific element:
- ✅ Element-specific content (title text, button link, image)

## Asset Requirements

When components need default images, use this format:

```typescript
// Import in component
import { heroImage } from './assets/defaultImages';

// Usage
<img src={heroImage} alt="Hero" />
```

Asset specification format:
```
<imageUrlName>
{ "description": "Modern cityscape at sunset", "width": 1920, "height": 1088 }
</imageUrlName>
```

**Rules:**
- Import as named export from `'./assets/defaultImages'`
- Width/height: multiples of 64, between 128-2048px
- NEVER use external URLs

## Output Structure

```
src/site/components/
└── {component-name}/
    ├── manifest.json        # Component manifest
    ├── component.tsx        # React component
    ├── style.css           # CSS styles
    ├── types.ts            # TypeScript types
    └── assets/             # Optional assets
        └── defaultImages.ts
```

## Examples

**Complete working example:** See [EXAMPLE.md](references/EXAMPLE.md) for a full production-ready site component with all patterns, including manifest, React component, CSS, and types.

### Product Card Component

**Request:** "Create a product card component with image, title, price, and buy button"

**Output:**
- Manifest with 4 elements (image, title, price, button)
- React component with sub-components for each element
- CSS with responsive grid layout and hover effects
- TypeScript types for all props and data structures

### Hero Section Component

**Request:** "Build a hero section with background image, headline, subtitle, and CTA button"

**Output:**
- Manifest with background image CSS property and 3 text elements
- React component with overlay design and typography hierarchy
- CSS with responsive text scaling and dramatic spacing
- Asset specifications for default hero images

### Feature List Component

**Request:** "Create a features component with configurable number of items"

**Output:**
- Manifest with arrayItems data type for feature collection
- React component mapping over features array with safety checks
- CSS with flexible grid layout adapting to item count
- Sub-components for feature icons, titles, and descriptions

## Extension Registration

**Extension registration is MANDATORY and has TWO required steps.**

### Step 1: Create Component-Specific Extension File

Each site component requires an `extensions.ts` file in its folder:

```typescript
import { extensions } from "@wix/astro/builders";
import manifest from "./manifest.json";

export const sitecomponentMyComponent = extensions.siteComponent({
  ...manifest,
  id: "{{GENERATE_UUID}}",
  description: "My Component",
  type: "platform.MyComponent",
  resources: {
    client: {
      component: "./site/components/my-component/component.tsx",
      componentUrl: "./site/components/my-component/component.tsx",
    },
  },
});
```

**CRITICAL: Type Naming Convention**

The `type` field uses the format `platform.{PascalCaseFolderName}`:
- Folder `my-component` → `type: "platform.MyComponent"`
- Folder `product-card` → `type: "platform.ProductCard"`
- Folder `hero-section` → `type: "platform.HeroSection"`

The folder name is converted to PascalCase (hyphens removed, each word capitalized).

**CRITICAL: UUID Generation**

The `id` must be a unique, static UUID v4 string. Generate a fresh UUID for each extension - do NOT use `randomUUID()` or copy UUIDs from examples.

### Step 2: Register in Main Extensions File

**CRITICAL:** After creating the component-specific extension file, you MUST read [wix-cli-extension-registration](../wix-cli-extension-registration/SKILL.md) and follow the "App Registration" section to update `src/extensions.ts`.

**Without completing Step 2, the site component will not be available in the Wix Editor.**

## Code Quality Requirements

**Complete reference:** See [TYPESCRIPT_QUALITY.md](references/TYPESCRIPT_QUALITY.md) for comprehensive type safety guidelines and code quality standards.

### TypeScript Standards

- Strict TypeScript with no `any` types
- Explicit return types for all functions
- Proper null/undefined handling with optional chaining
- No `@ts-ignore` or `@ts-expect-error` comments

### React Best Practices

- Functional components with hooks
- Proper dependency arrays in useEffect
- Component must react to prop changes
- SSR-safe code (no browser APIs at module scope)

### ESLint Compliance

1. No unused vars/params/imports (`@typescript-eslint/no-unused-vars`)
2. No external images: `img` `src` not `https://...` (allowed: local imports, `wixstatic.com`, variables)
3. SSR-safe: No `window`/`document` at module scope/constructor, guard browser APIs in `useEffect`/handlers
4. No `dangerouslySetInnerHTML` or inline `<style>` tags - use CSS variables or inline `style` prop for dynamic values
5. No `window.fetch` (`no-restricted-properties`)
6. Hooks `exhaustive-deps`: ALL values from component scope used inside `useEffect`/`useCallback` MUST be in dependency array
7. Use `const`/`let` (no `var`), no unknown JSX properties

## Hard Constraints

- Do NOT invent or assume new types, modules, functions, props, events, or imports
- Use only entities explicitly present in the provided references or standard libraries already used in this project
- Do NOT add dependencies; do NOT use `@wix/design-system` or `@wix/wix-ui-icons-common`
- All user-facing content must come from props (no hardcoded text)
- Links/media from manifest only, never hardcode URLs
- NEVER use mocks, placeholders, or TODOs in any code
- ALWAYS implement complete, production-ready functionality

## Verification

After implementation, use [wix-cli-app-validation](../wix-cli-app-validation/SKILL.md) to validate TypeScript compilation, build, preview, and runtime behavior.

## Reference Documentation

- [Complete Example](references/EXAMPLE.md) - Full production-ready site component example with all patterns
- [Component Manifest Guidelines](references/MANIFEST_GUIDELINES.md) - Detailed manifest structure and best practices
- [React Patterns](references/REACT_PATTERNS.md) - Component architecture and coding patterns
- [CSS Guidelines](references/CSS_GUIDELINES.md) - Styling conventions and responsive design
- [Design System](references/DESIGN_SYSTEM.md) - Visual design principles and creative guidelines
- [TypeScript Quality](references/TYPESCRIPT_QUALITY.md) - Type safety and code quality standards
