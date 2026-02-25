---
name: vapor-ui
description: Vapor UI design system component and icon guide, UI mockup generator, and Figma design converter. Provides component catalog, icon lookup, usage patterns, props documentation, and converts Figma designs to production-ready vapor-ui code. Use when user asks "vapor-ui components", "vapor-ui icons", "아이콘 찾기", "vapor-ui 사용법", "vapor-ui를 사용해서 시안 구현", "convert figma", "figma to code", "implement design from figma", provides a Figma URL, or mentions specific components like "Button", "Input", "Modal".
---

# Vapor UI Design Skill

## Instructions

### Step 1: Identify User Intent & Detect Version

**Run these checks in parallel:**

1. **Determine user intent**:
    - **Component lookup**: User wants to know available components or specific component details
    - **Usage guidance**: User needs props, variants, or example code
    - **Mockup generation**: User wants to create a UI prototype
    - **Figma conversion**: User wants to convert Figma design to code

2. **Determine Vapor UI version** (in order of priority):
    1. **User-provided version**: If user specifies a version, use it directly
    2. **Auto-detect from codebase**:
        ```bash
        node scripts/detect-version.mjs [start-path]
        ```
        Output: `CORE: x.x.x` and `ICONS: x.x.x`

    Use `CORE` version for component scripts, `ICONS` version for icon scripts.

### Step 2: Component Information

**Get component list:**

```bash
node scripts/get-component-list.mjs <VERSION>
```

Example: `node scripts/get-component-list.mjs 1.0.0-beta.12`

**Get component details (props, description):**

```bash
node scripts/get-component-info.mjs <VERSION> <COMPONENT> [PART]
```

Example: `node scripts/get-component-info.mjs 1.0.0-beta.12 avatar`

For detailed component structure, refer to `references/component-structure.md`.

### Step 3: Component Examples

**Get example code:**

```bash
node scripts/get-component-examples.mjs <VERSION> <COMPONENT> [EXAMPLE_NAME]
```

Example: `node scripts/get-component-examples.mjs 1.0.0-beta.12 avatar default-avatar`

### Step 3.5: Icon Lookup

**Get icon list:**

```bash
node scripts/get-icon-list.mjs <ICONS_VERSION> [search-keyword]
```

Examples:

- `node scripts/get-icon-list.mjs 1.0.0-beta.12` - List all icons
- `node scripts/get-icon-list.mjs 1.0.0-beta.12 arrow` - Search icons containing "arrow"
- `node scripts/get-icon-list.mjs 1.0.0-beta.12 --outline` - List only outline icons
- `node scripts/get-icon-list.mjs 1.0.0-beta.12 --filled` - List only filled icons

**Note**: Use `ICONS` version from `detect-version.mjs` output for icon queries.

### Step 4: Mockup Generation

For mockup requests:

1. Run `get-component-list.mjs` to identify available components
2. Run `get-component-info.mjs` for each needed component's props
3. Run `get-component-examples.mjs` for usage patterns
4. Generate code using Vapor UI components only
5. Provide complete, copy-paste ready code

### Step 5: Figma Design Conversion

For Figma conversion requests:

1. **Parse Figma URL** to extract `file_key` and `node_id`:

    ```
    https://www.figma.com/design/{file_key}/...?node-id={node_id}
    ```

2. **Get design context** using MCP:

    ```
    mcp__figma-dev-mode-mcp-server__get_design_context
      - file_key: extracted from URL
      - node_id: extracted from URL (format: "X-Y" or "X:Y")
      - depth: 5 (or higher for complex designs)
    ```

3. **Analyze node tree**:
    - **💙 prefix nodes**: Design system components (see `references/design-system-recognition.md`)
    - **Auto-layout frames**: Convert to VStack/HStack/Box/Grid (see `references/figma-layout-mapping.md`)
    - **TEXT nodes**: Extract text content

4. **Convert layout properties**:
    - `layoutMode: VERTICAL` → VStack
    - `layoutMode: HORIZONTAL` → HStack
    - `itemSpacing` → gap token
    - `padding*` → padding tokens
    - See `references/token-mapping.md` for full mapping

5. **Recognize design system components**:
    - Nodes starting with **💙** are vapor-ui components
    - Extract `componentProperties` for variant → props mapping
    - Example: `💙Button` with `Size: md, ColorPalette: primary` → `<Button size="md" colorPalette="primary">`
    - **Important**: Layout props (`gap`, `padding`, `margin`, `backgroundColor`, etc.) must be inside `$css` prop

6. **Generate code**:
    - Build JSX from node tree (bottom-up)
    - Apply style utility props using design tokens
    - Output production-ready code

---

## Examples

**Example 1: Component Usage Query**

**User**: "How do I use the Button component?"

**Action**:

1. Run `node scripts/get-component-info.mjs 1.0.0-beta.12 button`
2. Run `node scripts/get-component-examples.mjs 1.0.0-beta.12 button`
3. Provide props, variants, and example code

**Result**: Complete Button usage guide with code examples

---

**Example 2: Mockup Generation**

**User**: "Create a login page mockup"

**Action**:

1. Run `get-component-list.mjs` to check available components
2. Run `get-component-info.mjs` for text-input, button, card, form
3. Run `get-component-examples.mjs` for form patterns
4. Generate responsive layout using Vapor UI

**Result**: Production-ready login page code

---

**Example 3: Component Discovery**

**User**: "What form components are available?"

**Action**:

1. Run `node scripts/get-component-list.mjs 1.0.0-beta.12`
2. Filter output for form-related components (text-input, textarea, checkbox, radio, select, etc.)

**Result**: Categorized list of form-related components

---

For Figma conversion examples, see `references/conversion-examples.md`.

---

## Troubleshooting

| Error                     | Cause                            | Solution                                        |
| ------------------------- | -------------------------------- | ----------------------------------------------- |
| Component not found       | Name mismatch or version error   | Run `get-component-list.mjs`, verify version    |
| Script fetch error        | Invalid version or network issue | Re-run `detect-version.mjs`, check network      |
| Figma node not recognized | No 💙 prefix                     | Treat as custom layout (Box/VStack/HStack/Grid) |
| Spacing mismatch          | Non-standard values              | Round to nearest token (see `token-mapping.md`) |

---

## References

### Component Documentation

- `references/url-patterns.md`: GitHub URL patterns for fetching component data
- `references/component-structure.md`: Component file structure and JSON schema

### Figma Conversion

- `references/figma-layout-mapping.md`: Auto-layout to component mapping
- `references/design-system-recognition.md`: 💙 prefix component recognition
- `references/token-mapping.md`: Figma values to vapor-ui tokens
- `references/conversion-examples.md`: Figma to code conversion examples

## Scripts

| Script                       | Purpose                                                              |
| ---------------------------- | -------------------------------------------------------------------- |
| `detect-version.mjs`         | Detect @vapor-ui/core and @vapor-ui/icons versions from package.json |
| `get-component-list.mjs`     | List all available components                                        |
| `get-component-info.mjs`     | Get component props and documentation                                |
| `get-component-examples.mjs` | Get component example code                                           |
| `get-icon-list.mjs`          | List and search icons (supports --outline, --filled, keyword search) |

## MCP Tools

| Tool                                                 | Purpose                      |
| ---------------------------------------------------- | ---------------------------- |
| `mcp__figma-dev-mode-mcp-server__get_design_context` | Fetch Figma design node tree |
| `mcp__figma-dev-mode-mcp-server__get_screenshot`     | Get visual reference image   |
| `mcp__figma-dev-mode-mcp-server__get_metadata`       | Get Figma file metadata      |
