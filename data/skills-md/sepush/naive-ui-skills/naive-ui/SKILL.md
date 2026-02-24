---
name: naive-ui
description: Use when working with naive-ui components, or troubleshooting naive-ui usage issues.
license: MIT
metadata:
  author: Sepush
  version: "2026.2.23"
---

# Naive UI Practices

Usage guide for Naive UI and Vue 3 applications. Contains 33 rules across 8 categories, prioritized by impact to guide automated refactoring, component creation, and troubleshooting.

## When to Apply

Reference these guidelines when:
- Writing new Vue 3 components using Naive UI
- Implementing forms and data validation
- Handling large datasets with virtual scrolling (DataTable, Tree, Select)
- Customizing application themes and dark mode
- Troubleshooting Naive UI usage issues and styling conflicts

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Core Configuration | CRITICAL | `core-` |
| 2 | Form & Data Input | CRITICAL | `component-` |
| 3 | Complex Data Display | HIGH | `component-` |
| 4 | Feedback & Overlay | HIGH | `component-` |
| 5 | Layout & Navigation | MEDIUM | `component-` |
| 6 | Basic Data Display | MEDIUM | `component-` |
| 7 | Advanced Customization | LOW-MEDIUM | `core-` |
| 8 | Ecosystem & Troubleshooting | LOW | `core-` |

## Quick Reference

### 1. Core Configuration (CRITICAL)

- `core-setup` - Auto-import setup, global config, providers
- `core-theme` - Theme overrides, dark mode, CSS variables, useThemeVars
- `core-import-on-demand` - Import on demand and tree shaking
- `core-nuxtjs` - Nuxt.js integration best practices
- `core-ssr` - Server-Side Rendering guidelines
- `core-style-conflict` - Potential style conflict resolution

### 2. Form & Data Input (CRITICAL)

- `component-form-validation` - Validation rules, dynamic forms, array fields
- `component-form` - Layout, validation, dynamic fields, nested forms
- `component-input` - Formatted input, precision, validation triggers
- `component-select` - Filterable, multiple, tags, async search, custom render
- `component-datepicker` - Date ranges, shortcuts, formatting, timezone
- `component-upload` - Custom request, file handling, drag drop

### 3. Complex Data Display (HIGH)

- `component-datatable` - Virtual scroll, remote data, sorting, filtering, fixed columns
- `component-tree` - Async loading, checkable, controlled state, large dataset handling
- `component-virtual-list` - Virtual scrolling patterns

### 4. Feedback & Overlay (HIGH)

- `component-modal` - Form modals, draggable, focus management, async close
- `component-feedback` - Programmatic API, global methods (Message, Notification)
- `component-feedback-alert` - Alert, Skeleton, Spin, LoadingBar, Popconfirm

### 5. Layout & Navigation (MEDIUM)

- `component-layout` - Layout, Grid, Flex, Space, Card, Divider
- `component-menu` - Menu, Dropdown, Breadcrumb, Tabs
- `component-navigation-steps` - Steps, Timeline, Pagination, Anchor, BackTop

### 6. Basic Data Display (MEDIUM)

- `component-data-display` - Image, List, Descriptions, Calendar, Time, Countdown
- `component-display` - Badge, Tag, Avatar, Progress, Statistic, Result, Empty
- `component-button` - Button variants, loading, icons
- `component-selection` - Radio, Checkbox, Switch, Slider, Rate, ColorPicker

### 7. Advanced Customization (LOW-MEDIUM)

- `core-customize-theme` - Customizing theme extensively
- `core-fonts` - Configuring fonts
- `core-i18n` - Internationalization
- `core-controlled-uncontrolled` - Controlled manner & uncontrolled manner

### 8. Ecosystem & Troubleshooting (LOW)

- `core-troubleshooting` - Common issues and quick fixes
- `core-installation` - Installation guidelines
- `core-jsx` - JSX & TSX usage
- `core-umd` - Using UMD build
- `core-usage-sfc` - Usage in SFC
- `core-vite-ssge` - Vite SSG/SSE integration
- `core-vitepress` - Vitepress integration
- `core-experimental-features` - Experimental features

## How to Use

Read individual rule files for detailed explanations and code examples:

```
references/core-setup.md
references/component-datatable.md
```

Each rule file contains:
- Specific implementation details
- Code examples for Vue 3 setup script
- Warning notes and prerequisites
- Relevant TypeScript interfaces

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
