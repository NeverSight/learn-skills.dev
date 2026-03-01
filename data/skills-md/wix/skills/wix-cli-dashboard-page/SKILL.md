---
name: wix-cli-dashboard-page
description: Use when building admin interfaces, management pages, CRUD operations, or dashboard configuration UIs. Triggers include dashboard, admin panel, data management, settings pages.
compatibility: Requires Wix CLI development environment.
---

# Wix Dashboard Page Builder

Creates full-featured dashboard page extensions for Wix CLI applications. Dashboard pages appear in the Wix site owner's dashboard and enable site administrators to manage data, configure settings, and perform administrative tasks.

---

## Quick Start Checklist

Follow these steps in order when creating a dashboard page:

1. [ ] Create page folder: `src/dashboard/pages/<page-name>/`
2. [ ] Create `page.tsx` with WDS components wrapped in `WixDesignSystemProvider`
3. [ ] Create `extensions.ts` with `extensions.dashboardPage()` and unique UUID
4. [ ] Update `src/extensions.ts` to import and use the new extension

## Capabilities

### Data Operations (Wix Data SDK)

See [Wix Data Reference](references/WIX_DATA.md) for complete documentation.

**Summary:**

- Read: `items.query('Collection').filter/sort.limit.find()` → `{ items, totalCount, hasNext }`
- Write: `items.insert | update | remove`. Ensure collection permissions allow the action

**Query methods:** `eq`, `ne`, `gt`, `ge`, `lt`, `le`, `between`, `contains`, `startsWith`, `endsWith`, `hasSome`, `hasAll`, `isEmpty`, `isNotEmpty`, `and`, `or`, `not`, `ascending`, `descending`, `limit`, `skip`, `include`

### Dashboard APIs

See [Dashboard API Reference](references/DASHBOARD_API.md) for complete documentation including all methods, page IDs, and examples.

**Key methods:**

- `dashboard.navigate()` - Navigate between dashboard pages
- `dashboard.observeState()` - Receive contextual state and environmental information
- `dashboard.showToast()` - Display toast notifications
- `dashboard.openModal()` - Open dashboard modal extensions (see [wix-cli-dashboard-modal](../wix-cli-dashboard-modal/SKILL.md))
- `dashboard.navigateBack()` - Navigate back to previous page
- `dashboard.getPageUrl()` - Get full URL for a dashboard page
- `dashboard.openMediaManager()` - Open Wix Media Manager
- `dashboard.onBeforeUnload()` - Register beforeunload handler
- `dashboard.addSitePlugin()` - Add site plugin to slots
- `dashboard.setPageTitle()` - Set page title in browser tab
- `dashboard.onLayerStateChange()` - Handle foreground/background state changes

**CRITICAL: Using Modals in Dashboard Pages**

When you need to display popup forms, confirmations, detail views, or any dialog overlays from a dashboard page, you **MUST** use dashboard modals, not regular React modals or WDS Modal components.

- **Use dashboard modals** for: edit forms, delete confirmations, detail views, settings dialogs, any popup content
- **Do NOT use** WDS `Modal` component or custom React modal implementations
- **See [wix-cli-dashboard-modal](../wix-cli-dashboard-modal/SKILL.md)** for complete implementation guide

Dashboard modals are opened using `dashboard.openModal()` and provide proper integration with the dashboard lifecycle, state management, and navigation.

**Ecom Navigation:** See [Ecom Navigation Reference](references/ECOM_NAVIGATION.md) for ecom-specific navigation helpers.

### Embedded Script Configuration API

When building a dashboard page to configure an embedded script, see [Dynamic Parameters Reference](references/DYNAMIC_PARAMETERS.md) for complete implementation guide.

**Key points:**

- Use `embeddedScripts` from `@wix/app-management`
- Parameters are returned as strings - handle type conversions when loading
- All parameters must be saved as strings (convert booleans/numbers to strings)
- Use `withProviders` wrapper when dynamic parameters are present

## Files and Code Structure

Dashboard pages live under `src/dashboard/pages`. Each page has its own folder.

**File structure:**

- `src/dashboard/pages/<page>/page.tsx` — page component

**Key metadata fields:**

- `id` (string, GUID): Unique page ID used to register the page
- `title` (string): Used for browser tab and optional sidebar label
- `additionalRoutes` (string[], optional): Extra routes leading to this page
- `sidebar.disabled` (boolean, optional): Hide page from sidebar (default false)
- `sidebar.priority` (number, optional): Sidebar ordering; lower is higher priority
- `sidebar.whenActive.selectedPageId` (string, optional): Which page appears selected when this page is active
- `sidebar.whenActive.hideSidebar` (boolean, optional): Hide sidebar when this page is active

## WDS Provider Usage

Wrap your dashboard page component with `WixDesignSystemProvider` to enable WDS components and theming. You must also import the global CSS styles for WDS components to render correctly.

```typescript
import { WixDesignSystemProvider } from "@wix/design-system";
import '@wix/design-system/styles.global.css';

export default function () {
  return (
    <WixDesignSystemProvider>
      <Page>
        <Page.Header
          title="My Page"
          subtitle="This is a subtitle for your page"
        />
        <Page.Content>
          <EmptyState title="My Page" subtitle="Hello World!" theme="page" />
        </Page.Content>
      </Page>
    </WixDesignSystemProvider>
  );
}
```

**Note:** When using dynamic parameters, use the `withProviders` wrapper instead. See [Dynamic Parameters](references/DYNAMIC_PARAMETERS.md) for details.

## Hard Constraints

- Do NOT invent or assume new types, modules, functions, props, events, or imports.
- Use only entities explicitly present in the provided references or standard libraries already used in this project.
- If something is missing, call it out explicitly and provide a minimal TODO or clearly marked placeholder rather than creating it.
- Always verify component availability before using it in your generated code
- If you need a component not in the list, use a basic HTML element or create a simple custom component instead
- **Do NOT use WDS `Modal` component or custom React modal implementations** - Always use dashboard modals (see [wix-cli-dashboard-modal](../wix-cli-dashboard-modal/SKILL.md)) for any popup dialogs, forms, or overlays

## Examples

### Data Management Table

**Request:** "Create a dashboard page to manage blog posts"

**Output:** Page with table displaying posts, search toolbar, add/edit/delete actions, empty state.

### Settings Form

**Request:** "Build a settings page for notification preferences"

**Output:** Page with form fields, save button with toast confirmation, unsaved changes warning.

### Order Management

**Request:** "Create an admin panel for customer orders"

**Output:** Page with orders table, status badges, filters, detail dashboard modal (using [wix-cli-dashboard-modal](../wix-cli-dashboard-modal/SKILL.md)), status update actions.

### Embedded Script Configuration

**Request:** "Create a settings page for the coupon popup embedded script"

**Output:** Page with form fields for popup headline, coupon code, minimum cart value, and enable toggle. Uses `embeddedScripts` API to load/save parameters.

```typescript
// Key pattern for embedded script configuration pages
import { embeddedScripts } from "@wix/app-management";

// Load on mount
useEffect(() => {
  const load = async () => {
    const script = await embeddedScripts.getEmbeddedScript();
    const data = script.parameters || {};
    setOptions({
      headline: data.headline || "Default",
      enabled: data.enabled === "true",
      threshold: Number(data.threshold) || 0,
    });
  };
  load();
}, []);

// Save handler
const handleSave = async () => {
  await embeddedScripts.embedScript({
    parameters: {
      headline: options.headline,
      enabled: String(options.enabled),
      threshold: String(options.threshold),
    },
  });
  dashboard.showToast({ message: "Saved!", type: "success" });
};
```

## Extension Registration

**Extension registration is MANDATORY and has TWO required steps.**

### Step 1: Create Page-Specific Extension File

Each dashboard page requires an `extensions.ts` file in its folder:

**File:** `src/dashboard/pages/<page-name>/extensions.ts`

```typescript
import { extensions } from "@wix/astro/builders";

export const dashboardpageMyPage = extensions.dashboardPage({
  id: "{{GENERATE_UUID}}",
  title: "My Page",
  routePath: "my-page",
  component: "./dashboard/pages/my-page/page.tsx",
});
```

**CRITICAL: UUID Generation**

The `id` must be a unique, static UUID v4 string. Generate a fresh UUID for each extension - do NOT use `randomUUID()` or copy UUIDs from examples. Replace `{{GENERATE_UUID}}` with a freshly generated UUID like `"a1b2c3d4-e5f6-7890-abcd-ef1234567890"`.

| Property    | Type   | Description                                                                                          |
| ----------- | ------ | ---------------------------------------------------------------------------------------------------- |
| `id`        | string | Unique static UUID v4 (generate fresh - see note above)                                              |
| `title`     | string | Display title in dashboard sidebar                                                                   |
| `routePath` | string | URL path segment. Lowercase letters, numbers, dashes, and slashes only. Must NOT start with a slash. |
| `component` | string | Relative path to the page component (.tsx)                                                           |

### Step 2: Register in Main Extensions File

**CRITICAL:** After creating the page-specific extension file, you MUST read [wix-cli-extension-registration](../wix-cli-extension-registration/SKILL.md) and follow the "App Registration" section to update `src/extensions.ts`.

**Without completing Step 2, the dashboard page will not appear in the Wix dashboard.**

## Common Mistakes - Do NOT

**API confusion with other extension types:**

| WRONG (Embedded Script API) | CORRECT (Dashboard Page API) |
| --------------------------- | ---------------------------- |
| `name: "..."`               | `title: "..."`               |
| `source: "..."`             | `component: "..."`           |
| `route: "..."`              | `routePath: "..."`           |

Do NOT copy field names from embedded script or other extension registrations. Dashboard pages use `title`, `routePath`, and `component`.

## Code Quality Requirements

### TypeScript Quality Guidelines

- Generated code MUST compile with zero TypeScript errors under strict settings: strict, noImplicitAny, strictNullChecks, exactOptionalPropertyTypes, noUncheckedIndexedAccess
- Prefer type-narrowing and exhaustive logic over assertions; avoid non-null assertions (!) and unsafe casts (as any)
- Treat optional values, refs, and array indexing results as possibly undefined and handle them explicitly
- Use exhaustive checks for unions (e.g., switch with a never check) and return total values (no implicit undefined)
- Do NOT use // @ts-ignore or // @ts-expect-error; fix the types or add guards instead

### Core Principles

- Do NOT invent or assume new types, modules, functions, props, events, or imports
- NEVER use mocks, placeholders, or TODOs in any code
- ALWAYS implement complete, production-ready functionality
- Follow Wix dashboard page patterns and best practices precisely
- Handle all edge cases and error scenarios appropriately

### Code Quality Standards

- Prefer TypeScript with appropriate typing
- Use consistent naming conventions
- Include error handling where appropriate
- Add documentation for complex or non-obvious logic
- Prefer async/await for asynchronous operations
- Consider destructuring for cleaner code when beneficial
- Return well-structured response objects

### Error Handling

- Always implement proper error handling in dashboard pages
- Return appropriate error responses when data is invalid
- Log errors appropriately for debugging using console.error
- Handle network timeouts and external service failures

### Output Constraints

**Token limits:** Your max output is ~10,000 tokens. You MUST plan your response to stay well under this limit.

- If making a large file (>300 lines), split it into multiple smaller files with imports.
- If editing a large section (>100 lines), break it into multiple smaller edit operations.
- Count your output before responding - if it seems too long, reduce scope and prioritize.

**Brevity rules:** Minimize output tokens while maintaining quality and correctness.

- Do NOT add README.md, documentation files, or markdown files unless explicitly requested.
- Do NOT add excessive comments in code - only add comments where truly necessary for clarity.
- Do NOT re-output unchanged files or duplicate existing code.
- Do NOT generate placeholder code like "// TODO: implement" - provide working implementations.
- Only output files that are directly required for the task.

**Modular code strategy:** When generating substantial code, split into multiple smaller files with imports:

- Extract utilities/helpers into separate files
- Separate types/interfaces into dedicated type files
- Keep each component/function focused (~50-100 lines max)

## Verification

After implementation completes, the **wix-cli-orchestrator** will run validation using [wix-cli-app-validation](../wix-cli-app-validation/SKILL.md).

## API Spec Support

When an API specification is provided, you can make API calls to those endpoints. See [API Spec Reference](references/API_SPEC.md) for details on how to use API specs in dashboard pages.

---

## Layout Guidelines

Layout determines how users interact with your dashboard content. It establishes the structure, hierarchy, and rhythm of your dashboard page, contributing to the overall coherence and user experience. By making mindful and calculated choices in how you organize your content, users can move around more smoothly, saving time and frustration when completing tasks.

### Design Principles

To create dashboard pages optimized for user experience, follow these design principles:

1. **Consistent:** Maintain repetitive layouts and content patterns for intuitive and easy-to-read pages.
2. **Inclusive:** Create layouts and content that adapt well to various screen sizes.
3. **Balanced:** Emphasize the priority of regions and content elements through deliberate management of size and white space.
4. **Connected:** Minimize the distance between related regions or content elements to enhance cohesion and navigation.

---

### Screen Size

Dashboard pages are designed to accommodate various screen sizes rather than being tailored to one specific resolution. The primary content should be at the top of the page to ensure users immediately understand the purpose of the page.

> **Note:** Content displayed in the top 600 pixels of the page will be visible for the majority of users.

---

### Base Unit

The base unit establishes the increment by which all elements and measurements are multiplied. This practice ensures consistency in the spacing and sizing of design elements.

> **Note:** The design system is based on a 6px unit.

The layout grid, spacing tokens, and nearly all visual elements and sizes adhere to multiples of six (6, 12, 18, 24, etc.), with only occasional exceptions.

| TOKEN | SIZE | USE FOR |
|-------|------|---------|
| SP1 | 6px | Spacing between components |
| SP2 | 12px | Spacing between components |
| SP3 | 18px | Spacing between components |
| SP4 | 24px | Spacing between components, layout spacing |
| SP5 | 30px | Layout spacing |
| SP6 | 36px | Layout spacing |
| SP7 | 42px | Layout spacing |
| SP8 | 48px | Layout spacing |
| SP10 | 54px | Layout spacing |
| SP11 | 60px | Layout spacing |

---

### Layout Structure

To best design the layout for your app, understand:

1. The core frame of the app (Application frame)
2. The placement and alignment of each segment within the grid layout (Grid layout)
3. The content to appear in the grid (Common layouts)

#### Application Frame

The dashboard app frame is used by the majority of Wix applications settings. Dashboard pages consist of 4 areas:

| AREA | USAGE |
|------|-------|
| 1. Global navigation (top bar) | General navigation at the top of a page which allows users to navigate between different environments. Full width container with a fixed height of 48px. |
| 2. Sidebar navigation | Local navigation of an environment. Container with a fixed width of 228px. |
| 3. Content area | Page content area with a width that's adaptive to screen size. |
| 4. Side panel (optional) | An optional panel that shows additional actions or content associated with the content of a page. Fixed width of 420px. Can either overlay the main content area or push it from the right side. |

**Side Panel Guidelines:**
- Let the side panel overlay main content when it contains supplementary actions or settings, such as data filters
- Push main content with the side panel when users must see the full context to continue

---

#### Grid Layout

The system uses a fluid grid layout with a fixed maximum width. It uses columns that scale and resize the content accordingly.

The grid is constructed from 3 elements:
- **Columns** - The design system uses a 12-column grid. Column width is fluid and changes according to the page width.
- **Gutters** - The gaps between the columns. Gutter width has a fixed value of 24px.
- **Margins** - By default, a page's content area has 48px side margins and a 48px bottom margin.

**Grid Specifications:**
- Minimum content area width: 864 pixels (each grid column is 50px wide)
- Maximum content area width: 1248px (each column is 82px wide)
- Wider screens maintain 1248px content width with side margins stretching to center content
- Use 24px gap between cards both vertically and horizontally

---

### Common Layouts

Page layouts can be divided by intention into the following types:

#### 1. Form Layouts

Forms are pages that allow users to fill in data or edit existing data. Two variations:

- **2/3 layout with optional sidebar (8/4 column split)** - Provides flexibility to expose primary and secondary content at the same time
- **Full width (12 columns)** - Supports advanced product needs with complex structures

Both form page layouts include mandatory **Save** and **Cancel** actions in the header and footer areas.

**2/3 Layout Best Practices:**
- Use to expose primary and secondary content at the same time
- Keep the form easy to scan and comprehend
- Display a live content preview on the side (widget can be sticky)
- Use 8 columns for forms to keep text lines and input fields narrow for quicker reading
- Bring actions closer to related titles (e.g., toggle switches near settings)

**Full Width Layout Best Practices:**
- Use when a form includes complex structures such as tables
- Use for list items that contain many data columns

**Combining Layouts:**
- Avoid coast-to-coast inputs; keep inputs to 2/3 width of a card, or lay them out in two columns
- Use white space on the right side for content preview
- Use full width for tables with many columns and dividers that separate sections

> **Note:** A column is easy to read if it is wide enough to accommodate an average of 10 words per line.

#### 2. Display Layouts

Display pages showcase data or content without accepting input from users. They can contain minor actions such as data filtering.

**List (Table):**
- Tables display large data sets and provide users with a quick overview
- Use a 12-column layout for tables
- Enables users to manipulate and act on a data set

**List (Grid) Options:**
- 2 columns (6/6 split) - For items with lengthy descriptions
- 3 columns (4/4/4 split) - For visual items with multiple data types
- 4 columns (3/3/3/3 split) - For user-generated galleries and collections, reveals up to 50% more content above the fold than 4/4/4
- Custom - For mixed content needs

**Grid Selection Considerations:**
- Total amount of items to show
- Content to display in each list item
- What objects the list items reflect (match physical shapes when applicable)

**Dashboards:**
Display different types of data on a specific topic using a combination grid.

Column span recommendations:
- **3 or 4 columns** - For list items, previews, marketing, statistics, and charts
- **12 columns (full width)** - For tables and marketing content
- **8 columns** - For lists, tables with few data columns, setup wizards, and charts
- **6 columns** - For lists, tables with few data columns, and statistics

**Empty States:**
- Use full width layout for empty state of a page
- Indicates feature/product has no data yet, all data cleared, or not set up yet
- Include clear CTA indicating what to do to fill the page
- Can combine with other layout elements such as tabs, statistics widgets, or marketing cards

#### 3. Marketing Layouts

Marketing pages promote new products that site owners are not aware of yet. Built using the `<MarketingPageLayout/>` component split into 2 columns:

1. Promo messaging
2. Visual representation of product and features

Optional footer area can display features or testimonials list.

#### 4. Wizard Layouts

Wizard pages guide users through setting up a product or feature. They split complex forms into steps for easier completion.

**Entry Points:**
- A marketing page
- A marketing card
- The primary action of a page
- An empty state

> **Note:** Wizards must have a final destination. After completing all steps, users should end up on a relevant page: a dashboard, a details page, or any other relevant location.

---

### Related WDS Components

- `<Page />` - Main page wrapper
- `<Layout />` - Grid layout container
- `<MarketingPageLayout />` - Marketing page wrapper
- `<Card />` - Content container with 24px gaps between cards
