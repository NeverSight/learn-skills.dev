---
name: "element-plus-skills"
description: "Element Plus Skills Library - A comprehensive skill library for AI agents to understand and utilize Element Plus UI components. Invoke when user needs to work with Element Plus components, theming, i18n, dark mode, or design specifications."
metadata:
  author: jiaiyan
  version: "1.0.0"
---

# Element Plus Skills Library

A comprehensive skill library for Element Plus UI framework, designed for AI agents to understand and utilize Element Plus components effectively.

## When to Invoke

Invoke this skill when:
- User needs to implement any Element Plus component
- User asks about Element Plus configuration or setup
- User wants to customize themes or use dark mode
- User needs internationalization (i18n) support
- User asks about design specifications (colors, borders, typography)
- User encounters issues with Element Plus components

## Skill Library Overview

This library contains **88 skills** organized into the following categories:

| Category | Count | Description | Path Pattern |
|----------|-------|-------------|--------------|
| Component Skills | 77 | Individual component documentation | `./components/el-{name}/SKILL.md` |
| Design Specifications | 5 | Border, Color, Layout, Typography, Overview | `./element-plus-design-{name}/SKILL.md` |
| Foundation Skills | 6 | Quickstart, Theming, i18n, Dark Mode, SSR, Components | `./element-plus-{name}/SKILL.md` |

## How to Locate Skills

### 1. Component Skills (77 skills)

All component skills follow the naming convention `el-{component-name}` and are located in the `components/` directory.

**Path Pattern:**
```
./components/el-{component-name}/SKILL.md
```

**Examples:**
- Button: `./components/el-button/SKILL.md`
- Form: `./components/el-form/SKILL.md`
- Table: `./components/el-table/SKILL.md`
- Dialog: `./components/el-dialog/SKILL.md`

### 2. Design Specification Skills (5 skills)

Design skills provide guidance on Element Plus design system.

| Skill Name | Path | Description |
|------------|------|-------------|
| Border | `./element-plus-design-border/SKILL.md` | Border styles, radius, shadows |
| Color | `./element-plus-design-color/SKILL.md` | Color palette and semantics |
| Layout | `./element-plus-design-layout/SKILL.md` | 24-column grid system |
| Typography | `./element-plus-design-typography/SKILL.md` | Font conventions |
| Overview | `./element-plus-design-overview/SKILL.md` | Design system overview |

### 3. Foundation Skills (6 skills)

Foundation skills cover core setup and configuration.

| Skill Name | Path | Description |
|------------|------|-------------|
| Quickstart | `./element-plus-quickstart/SKILL.md` | Installation and setup |
| Theming | `./element-plus-theming/SKILL.md` | Theme customization |
| i18n | `./element-plus-i18n/SKILL.md` | Internationalization |
| Dark Mode | `./element-plus-dark-mode/SKILL.md` | Dark mode implementation |
| SSR | `./element-plus-ssr/SKILL.md` | Server-side rendering |
| Components | `./element-plus-components/SKILL.md` | Component overview index |

## Skill Invocation Guide

### Step 1: Identify User Intent

Analyze the user's request to determine which skill category is needed:

| User Request Pattern | Skill Category | Example Skill |
|---------------------|----------------|---------------|
| "Create a button/form/table..." | Component | `el-button`, `el-form`, `el-table` |
| "How to set up Element Plus" | Foundation | `element-plus-quickstart` |
| "Customize theme colors" | Foundation | `element-plus-theming` |
| "Add multi-language support" | Foundation | `element-plus-i18n` |
| "Implement dark mode" | Foundation | `element-plus-dark-mode` |
| "What colors are available?" | Design | `element-plus-design-color` |
| "How does the grid work?" | Design | `element-plus-design-layout` |

### Step 2: Locate the Skill File

Use the path patterns above to locate the appropriate skill file:

```markdown
# For component skills
./components/el-{component-name}/SKILL.md

# For design skills
./element-plus-design-{name}/SKILL.md

# For foundation skills
./element-plus-{name}/SKILL.md
```

### Step 3: Read and Apply Skill Content

Each skill file contains:
- **When to Invoke**: Specific conditions for using the skill
- **Features**: Component capabilities and options
- **API Reference**: Attributes, events, slots, exposes
- **Usage Examples**: Code snippets for common patterns
- **Best Practices**: Recommended implementation guidelines

## Component Skill Index

### Basic Components (14)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Affix | `./components/el-affix/SKILL.md` | Sticky positioning |
| Alert | `./components/el-alert/SKILL.md` | Alert messages |
| Anchor | `./components/el-anchor/SKILL.md` | Anchor navigation |
| Avatar | `./components/el-avatar/SKILL.md` | User avatars |
| Backtop | `./components/el-backtop/SKILL.md` | Back to top button |
| Badge | `./components/el-badge/SKILL.md` | Badges and marks |
| Breadcrumb | `./components/el-breadcrumb/SKILL.md` | Breadcrumb navigation |
| Button | `./components/el-button/SKILL.md` | Buttons |
| Card | `./components/el-card/SKILL.md` | Card containers |
| Carousel | `./components/el-carousel/SKILL.md` | Image carousels |
| Collapse | `./components/el-collapse/SKILL.md` | Collapsible panels |
| Divider | `./components/el-divider/SKILL.md` | Dividing lines |
| Icon | `./components/el-icon/SKILL.md` | SVG icons |
| Link | `./components/el-link/SKILL.md` | Text links |
| Text | `./components/el-text/SKILL.md` | Styled text |

### Form Components (24)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Autocomplete | `./components/el-autocomplete/SKILL.md` | Input with suggestions |
| Cascader | `./components/el-cascader/SKILL.md` | Cascading selection |
| Checkbox | `./components/el-checkbox/SKILL.md` | Checkboxes |
| ColorPicker | `./components/el-color-picker/SKILL.md` | Color picker |
| ColorPicker Panel | `./components/el-color-picker-panel/SKILL.md` | Color picker panel |
| DatePicker | `./components/el-date-picker/SKILL.md` | Date picker |
| DatePicker Panel | `./components/el-date-picker-panel/SKILL.md` | Date picker panel |
| DateTimePicker | `./components/el-datetime-picker/SKILL.md` | Date time picker |
| Form | `./components/el-form/SKILL.md` | Form management |
| Input | `./components/el-input/SKILL.md` | Text input |
| InputNumber | `./components/el-input-number/SKILL.md` | Number input |
| InputTag | `./components/el-input-tag/SKILL.md` | Tag input |
| Mention | `./components/el-mention/SKILL.md` | Mention input |
| Radio | `./components/el-radio/SKILL.md` | Radio buttons |
| Rate | `./components/el-rate/SKILL.md` | Star rating |
| Select | `./components/el-select/SKILL.md` | Dropdown select |
| Select V2 | `./components/el-select-v2/SKILL.md` | Virtualized select |
| Slider | `./components/el-slider/SKILL.md` | Slider input |
| Switch | `./components/el-switch/SKILL.md` | Toggle switch |
| TimePicker | `./components/el-time-picker/SKILL.md` | Time picker |
| TimeSelect | `./components/el-time-select/SKILL.md` | Time select |
| Transfer | `./components/el-transfer/SKILL.md` | Transfer panels |
| TreeSelect | `./components/el-tree-select/SKILL.md` | Tree select |
| Upload | `./components/el-upload/SKILL.md` | File upload |

### Data Display Components (17)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Calendar | `./components/el-calendar/SKILL.md` | Calendar view |
| Descriptions | `./components/el-descriptions/SKILL.md` | Description list |
| Empty | `./components/el-empty/SKILL.md` | Empty state |
| Image | `./components/el-image/SKILL.md` | Image with preview |
| Pagination | `./components/el-pagination/SKILL.md` | Pagination |
| Progress | `./components/el-progress/SKILL.md` | Progress bar |
| Result | `./components/el-result/SKILL.md` | Result page |
| Skeleton | `./components/el-skeleton/SKILL.md` | Loading skeleton |
| Table | `./components/el-table/SKILL.md` | Data table |
| Table V2 | `./components/el-table-v2/SKILL.md` | Virtualized table |
| Tag | `./components/el-tag/SKILL.md` | Tags |
| Timeline | `./components/el-timeline/SKILL.md` | Timeline |
| Tree | `./components/el-tree/SKILL.md` | Tree view |
| Tree V2 | `./components/el-tree-v2/SKILL.md` | Virtualized tree |
| Statistic | `./components/el-statistic/SKILL.md` | Statistics display |
| Segmented | `./components/el-segmented/SKILL.md` | Segmented control |

### Navigation Components (8)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Dropdown | `./components/el-dropdown/SKILL.md` | Dropdown menu |
| Menu | `./components/el-menu/SKILL.md` | Navigation menu |
| PageHeader | `./components/el-page-header/SKILL.md` | Page header |
| Steps | `./components/el-steps/SKILL.md` | Steps guide |
| Tabs | `./components/el-tabs/SKILL.md` | Tabs |

### Feedback Components (12)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Dialog | `./components/el-dialog/SKILL.md` | Modal dialog |
| Drawer | `./components/el-drawer/SKILL.md` | Drawer panel |
| Loading | `./components/el-loading/SKILL.md` | Loading overlay |
| Message | `./components/el-message/SKILL.md` | Toast message |
| MessageBox | `./components/el-message-box/SKILL.md` | Message box |
| Notification | `./components/el-notification/SKILL.md` | Notification |
| Popconfirm | `./components/el-popconfirm/SKILL.md` | Popconfirm |
| Popover | `./components/el-popover/SKILL.md` | Popover |
| Tooltip | `./components/el-tooltip/SKILL.md` | Tooltip |
| Tour | `./components/el-tour/SKILL.md` | Product tour |

### Layout Components (4)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| Container | `./components/el-container/SKILL.md` | Layout container |
| Space | `./components/el-space/SKILL.md` | Spacing |
| Splitter | `./components/el-splitter/SKILL.md` | Split panels |

### Utility Components (5)

| Component | Skill Path | Description |
|-----------|------------|-------------|
| ConfigProvider | `./components/el-config-provider/SKILL.md` | Global config |
| InfiniteScroll | `./components/el-infinite-scroll/SKILL.md` | Infinite scroll |
| Scrollbar | `./components/el-scrollbar/SKILL.md` | Custom scrollbar |
| Watermark | `./components/el-watermark/SKILL.md` | Watermark |

## Usage Examples

### Example 1: User asks about button implementation

**User Request:** "How do I create a primary button with loading state?"

**Agent Action:**
1. Identify intent: Component skill - Button
2. Locate skill: `./components/el-button/SKILL.md`
3. Read skill content
4. Provide response with API reference and code example

**Response:**
```vue
<template>
  <el-button type="primary" :loading="loading" @click="handleClick">
    {{ loading ? 'Loading...' : 'Submit' }}
  </el-button>
</template>

<script setup>
import { ref } from 'vue'

const loading = ref(false)

const handleClick = async () => {
  loading.value = true
  try {
    await submitData()
  } finally {
    loading.value = false
  }
}
</script>
```

### Example 2: User asks about form validation

**User Request:** "How do I create a form with validation?"

**Agent Action:**
1. Identify intent: Component skill - Form
2. Locate skill: `./components/el-form/SKILL.md`
3. Read skill content
4. Provide response with validation example

**Response:**
```vue
<template>
  <el-form :model="form" :rules="rules" ref="formRef">
    <el-form-item label="Name" prop="name">
      <el-input v-model="form.name" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm">Submit</el-button>
    </el-form-item>
  </el-form>
</template>

<script setup>
import { ref, reactive } from 'vue'

const formRef = ref()
const form = reactive({
  name: ''
})

const rules = {
  name: [
    { required: true, message: 'Please input name', trigger: 'blur' }
  ]
}

const submitForm = async () => {
  await formRef.value.validate()
  // Submit logic
}
</script>
```

### Example 3: User asks about theme customization

**User Request:** "How do I customize Element Plus theme colors?"

**Agent Action:**
1. Identify intent: Foundation skill - Theming
2. Locate skill: `./element-plus-theming/SKILL.md`
3. Read skill content
4. Provide response with CSS variables example

**Response:**
```css
:root {
  --el-color-primary: #409eff;
  --el-color-success: #67c23a;
  --el-color-warning: #e6a23c;
  --el-color-danger: #f56c6c;
  --el-color-info: #909399;
}
```

### Example 4: User asks about dark mode

**User Request:** "How do I implement dark mode in Element Plus?"

**Agent Action:**
1. Identify intent: Foundation skill - Dark Mode
2. Locate skill: `./element-plus-dark-mode/SKILL.md`
3. Read skill content
4. Provide response with implementation example

**Response:**
```vue
<template>
  <el-config-provider :locale="locale" :size="size">
    <div :class="{ 'dark': isDark }">
      <App />
    </div>
  </el-config-provider>
</template>

<style>
.dark {
  color-scheme: dark;
}
</style>
```

## Configuration Requirements

### Prerequisites

Before using this skill library, ensure:

1. **Vue 3.3+** is installed
2. **Element Plus 2.4+** is installed
3. **Node.js 18+** for development

### Installation

```bash
npm install element-plus
npm install @element-plus/icons-vue
```

### TypeScript Support

Add to `tsconfig.json`:

```json
{
  "compilerOptions": {
    "types": ["element-plus/global"]
  }
}
```

## Input Parameters

When invoking skills, consider these parameters:

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| component | string | Component name (e.g., "button", "form") | Yes |
| feature | string | Specific feature needed (e.g., "validation", "loading") | No |
| context | object | Additional context (framework, TypeScript usage) | No |

## Output Format

Each skill provides:

1. **API Reference**: Complete attributes, events, slots, exposes
2. **Code Examples**: Working code snippets
3. **Best Practices**: Recommended implementation patterns
4. **Common Issues**: Troubleshooting tips
5. **Component Interactions**: How to use with other components

## Important Notes

### 1. Skill Priority

When multiple skills could apply, prioritize in this order:
1. Component-specific skills (most specific)
2. Foundation skills (configuration)
3. Design specification skills (guidelines)

### 2. Cross-References

Many skills reference related skills. Always check:
- Related components in the same category
- Foundation skills for configuration
- Design skills for styling guidelines

### 3. Version Compatibility

This skill library is based on Element Plus 2.4+. Some features may not be available in earlier versions.

### 4. Naming Conventions

- Component skills use `el-{name}` format (matches Vue component tags)
- Foundation skills use `element-plus-{name}` format
- Design skills use `element-plus-design-{name}` format

### 5. File Structure

```
element-plus-skills/
├── SKILL.md                          # This file (main entry)
├── README.md                         # English documentation
├── README_CN.md                      # Chinese documentation
├── AGENTS.md                         # Agents documentation
├── components/                       # 77 component skills
│   ├── el-button/
│   │   └── SKILL.md
│   ├── el-form/
│   │   └── SKILL.md
│   └── ...
├── element-plus-quickstart/          # Foundation skills
├── element-plus-theming/
├── element-plus-i18n/
├── element-plus-dark-mode/
├── element-plus-ssr/
├── element-plus-components/
├── element-plus-design-border/       # Design skills
├── element-plus-design-color/
├── element-plus-design-layout/
├── element-plus-design-typography/
└── element-plus-design-overview/
```

## Best Practices for Agents

1. **Always start with this file** when user mentions Element Plus
2. **Locate the specific skill** based on user intent
3. **Read the complete skill file** before responding
4. **Provide code examples** from the skill documentation
5. **Reference related skills** when applicable
6. **Include best practices** from the skill content
7. **Mention common issues** if relevant to user's context

## Related Resources

- [Element Plus Documentation](https://element-plus.org/)
- [Vue 3 Documentation](https://vuejs.org/)
- [Element Plus GitHub](https://github.com/element-plus/element-plus)
- [Element Plus Icons](https://element-plus.org/en-US/component/icon.html)
