---
name: arco-design
description: "Arco Design React UI component library reference (@arco-design/web-react). Use this skill whenever the user asks to build a page, create a UI, write frontend code, develop a web application, design a dashboard, or implement any React interface — especially when they mention Arco, arco-design, @arco-design/web-react, or any Arco component name (Button, Table, Form, Modal, Select, Menu, etc.). Covers all 70 components with full API, code examples, import patterns, theming, i18n, layout, forms, tables, modals, navigation, data entry, data display, feedback, responsive design, and best practices."
---

# Arco Design React — Skills Reference

`@arco-design/web-react` — An enterprise-level React UI component library by ByteDance.

## Critical Conventions

**Always follow these rules when writing Arco Design code:**

- **Imports**: `import { Button, Table, Form } from '@arco-design/web-react'` — always from the package root, never from sub-paths like `@arco-design/web-react/es/Button`
- **Icons**: `import { IconSearch, IconPlus } from '@arco-design/web-react/icon'`
- **Types**: `import type { TableProps, FormInstance } from '@arco-design/web-react'`
- **Styles**: `import '@arco-design/web-react/dist/css/arco.css'` (full) or configure on-demand loading
- **Date library**: dayjs (NOT moment.js)
- **Controlled mode**: `value` + `onChange`; **Uncontrolled**: `defaultValue`
- **Sub-components**: accessed via `Component.Sub` pattern — `Form.Item`, `Select.Option`, `Menu.SubMenu`, `Input.Search`, `Input.TextArea`, `Grid.Row`, `Grid.Col`
- **Form.Item uses `field` prop** (not `name` like Ant Design)
- **Switch in Form** requires `triggerPropName="checked"`

## Skill Index

Load the relevant file below for full API reference, code examples, and best practices.

### Setup & Configuration

| Topic | File | When to use |
|-------|------|-------------|
| Installation | [getting-started.md](references/overview/getting-started.md) | Install `@arco-design/web-react`, import styles, configure tree-shaking or babel-plugin-import |
| Global Config | [config-provider.md](references/overview/config-provider.md) | Set global component size, theme, locale, default props via `<ConfigProvider>` |
| Theming | [theming.md](references/overview/theming.md) | Custom theme colors, CSS variable overrides, Less variables, dark mode toggle |
| Internationalization | [internationalization.md](references/overview/internationalization.md) | Switch languages, add locale packs, customize locale text |
| Architecture | [architecture.md](references/overview/architecture.md) | Understand controlled/uncontrolled patterns, props merging, ref forwarding, CSS naming |

### General Components

| Component | File | Use for |
|-----------|------|---------|
| Button | [button.md](references/components/general/button.md) | Buttons, button groups, icon buttons, loading state |
| Icon | [icon.md](references/components/general/icon.md) | Built-in icons (`IconXxx`), custom SVG icons, IconFont |
| Typography | [typography.md](references/components/general/typography.md) | Headings, paragraphs, text ellipsis, copyable/editable text |
| Link | [link.md](references/components/general/link.md) | Hyperlinks with icon, hover states |
| Divider | [divider.md](references/components/general/divider.md) | Horizontal/vertical dividers, dividers with text |

### Layout

| Component | File | Use for |
|-----------|------|---------|
| Grid | [grid.md](references/components/layout/grid.md) | 24-column `Row`/`Col` grid, responsive breakpoints (xs/sm/md/lg/xl/xxl), gutter |
| Layout | [layout.md](references/components/layout/layout.md) | Page skeleton: `Header`, `Sider`, `Content`, `Footer`, collapsible sidebar |
| Space | [space.md](references/components/layout/space.md) | Consistent spacing between elements, horizontal/vertical, wrap |

### Navigation

| Component | File | Use for |
|-----------|------|---------|
| Menu | [menu.md](references/components/navigation/menu.md) | Sidebar nav, top nav bar, sub-menus, menu groups, collapsible |
| Tabs | [tabs.md](references/components/navigation/tabs.md) | Tab switching, card tabs, editable/closable tabs, extra content |
| Dropdown | [dropdown.md](references/components/navigation/dropdown.md) | Dropdown menus, context menus, button dropdowns |
| Breadcrumb | [breadcrumb.md](references/components/navigation/breadcrumb.md) | Navigation hierarchy path, route breadcrumbs |
| Pagination | [pagination.md](references/components/navigation/pagination.md) | Page navigation, size changer, simple/mini mode |
| Steps | [steps.md](references/components/navigation/steps.md) | Step-by-step workflows, vertical/dot steps, error state |
| Affix | [affix.md](references/components/navigation/affix.md) | Pin element to viewport on scroll |
| Anchor | [anchor.md](references/components/navigation/anchor.md) | In-page anchor navigation, scroll-to-section |
| PageHeader | [page-header.md](references/components/navigation/page-header.md) | Page title + back button + breadcrumb + actions |

### Data Entry

| Component | File | Use for |
|-----------|------|---------|
| Form | [form.md](references/components/data-entry/form.md) | Form building, validation, `Form.Item` (uses `field` prop), `Form.List`, `useForm` hook |
| Input | [input.md](references/components/data-entry/input.md) | Text input, `Input.Password`, `Input.Search`, `Input.TextArea`, prefix/suffix |
| Select | [select.md](references/components/data-entry/select.md) | Dropdown select, multi-select, search, remote search, `Select.Option`, virtual scroll |
| DatePicker | [date-picker.md](references/components/data-entry/date-picker.md) | Date/range picker (`RangePicker`), week/month/quarter/year, disabled dates (dayjs) |
| TimePicker | [time-picker.md](references/components/data-entry/time-picker.md) | Time selection, range, 12h format, step intervals |
| InputNumber | [input-number.md](references/components/data-entry/input-number.md) | Numeric input, stepper, precision, min/max |
| Checkbox | [checkbox.md](references/components/data-entry/checkbox.md) | Multi-select, `Checkbox.Group`, select all / indeterminate |
| Radio | [radio.md](references/components/data-entry/radio.md) | Single select, `Radio.Group`, button-style radio |
| Switch | [switch.md](references/components/data-entry/switch.md) | Toggle switch, loading, text labels (use `triggerPropName="checked"` in Form) |
| Slider | [slider.md](references/components/data-entry/slider.md) | Range slider, marks, vertical, step, tooltip format |
| Rate | [rate.md](references/components/data-entry/rate.md) | Star rating, half-star, readonly, custom characters |
| Cascader | [cascader.md](references/components/data-entry/cascader.md) | Multi-level cascade (province/city), remote load, search |
| TreeSelect | [tree-select.md](references/components/data-entry/tree-select.md) | Select from tree structure, checkable, searchable, async load |
| Transfer | [transfer.md](references/components/data-entry/transfer.md) | Transfer items between two lists, search, simple mode |
| AutoComplete | [auto-complete.md](references/components/data-entry/auto-complete.md) | Input autocomplete, search suggestions |
| Mentions | [mentions.md](references/components/data-entry/mentions.md) | @mention users/topics in text input |
| InputTag | [input-tag.md](references/components/data-entry/input-tag.md) | Tag input, add/remove tags, drag sort |
| Upload | [upload.md](references/components/data-entry/upload.md) | File upload, drag-and-drop, image upload with preview |
| ColorPicker | [color-picker.md](references/components/data-entry/color-picker.md) | Color selection (hex/rgb/hsl) |
| VerificationCode | [verification-code.md](references/components/data-entry/verification-code.md) | OTP / verification code input |

### Data Display

| Component | File | Use for |
|-----------|------|---------|
| Table | [table.md](references/components/data-display/table.md) | Data tables, sort, filter, pagination, fixed columns/header, virtual scroll, row selection, expandable rows |
| List | [list.md](references/components/data-display/list.md) | Data lists, paginated, virtual scroll, grid layout |
| Card | [card.md](references/components/data-display/card.md) | Card containers, cover, `Card.Grid`, `Card.Meta`, actions |
| Tree | [tree.md](references/components/data-display/tree.md) | Tree structure, checkable, draggable, virtual scroll, async load |
| Tooltip | [tooltip.md](references/components/data-display/tooltip.md) | Hover text hints (for rich content use Popover) |
| Popover | [popover.md](references/components/data-display/popover.md) | Click/hover popup cards with rich content |
| Avatar | [avatar.md](references/components/data-display/avatar.md) | User avatars, avatar groups, image/text/icon avatars |
| Badge | [badge.md](references/components/data-display/badge.md) | Numeric badges, status dots, count indicators |
| Tag | [tag.md](references/components/data-display/tag.md) | Status tags, closable, `Tag.CheckableTag`, colored tags |
| Carousel | [carousel.md](references/components/data-display/carousel.md) | Image carousels, slideshows |
| Collapse | [collapse.md](references/components/data-display/collapse.md) | Collapsible panels, accordion mode, FAQ |
| Descriptions | [descriptions.md](references/components/data-display/descriptions.md) | Key-value detail display, bordered, responsive columns |
| Calendar | [calendar.md](references/components/data-display/calendar.md) | Calendar view, event marking |
| Comment | [comment.md](references/components/data-display/comment.md) | Comment display, nested replies, actions |
| Empty | [empty.md](references/components/data-display/empty.md) | Empty state placeholder |
| Image | [image.md](references/components/data-display/image.md) | Image display, preview, lazy load, `Image.PreviewGroup` |
| Statistic | [statistic.md](references/components/data-display/statistic.md) | Numeric display, countdown, trend indicators |
| Timeline | [timeline.md](references/components/data-display/timeline.md) | Timelines, activity feeds, changelog |

### Feedback

| Component | File | Use for |
|-----------|------|---------|
| Modal | [modal.md](references/components/feedback/modal.md) | Modal dialogs, `Modal.confirm()`, `useModal` hook, form-in-modal |
| Message | [message.md](references/components/feedback/message.md) | Global toast: `Message.success()`, `error()`, `warning()`, `loading()` |
| Notification | [notification.md](references/components/feedback/notification.md) | Rich notification toasts with title + content + actions |
| Drawer | [drawer.md](references/components/feedback/drawer.md) | Slide-out side panels, form editing, nested drawers |
| Alert | [alert.md](references/components/feedback/alert.md) | Inline alert banners (info/success/warning/error), banner mode |
| Progress | [progress.md](references/components/feedback/progress.md) | Linear/circular progress bars, step progress |
| Popconfirm | [popconfirm.md](references/components/feedback/popconfirm.md) | Lightweight confirmation popup before delete/submit |
| Result | [result.md](references/components/feedback/result.md) | Result pages (success/fail/403/404/500) |
| Skeleton | [skeleton.md](references/components/feedback/skeleton.md) | Loading skeleton placeholders with animation |
| Spin | [spin.md](references/components/feedback/spin.md) | Loading spinner wrapping content |

### Other

| Component | File | Use for |
|-----------|------|---------|
| BackTop | [back-top.md](references/components/other/back-top.md) | Scroll-to-top button |
| Portal | [portal.md](references/components/other/portal.md) | Render children into different DOM node |
| ResizeBox | [resize-box.md](references/components/other/resize-box.md) | Resizable containers, split panes |
| Trigger | [trigger.md](references/components/other/trigger.md) | Base popup positioning (underlies Tooltip/Popover/Dropdown) |
| Watermark | [watermark.md](references/components/other/watermark.md) | Text/image watermarks over page content |

### Patterns & Best Practices

| Topic | File | When to use |
|-------|------|-------------|
| Form Patterns | [form-patterns.md](references/patterns/form-patterns.md) | Dynamic forms, linked validation, nested forms, async submit, complex layouts |
| Table Patterns | [table-patterns.md](references/patterns/table-patterns.md) | Remote data, editable rows, virtual scroll large data, custom filters |
| Modal Patterns | [modal-patterns.md](references/patterns/modal-patterns.md) | Form-in-modal, confirmation flows, nested drawers, global messages |
| Controlled vs Uncontrolled | [controlled-uncontrolled.md](references/patterns/controlled-uncontrolled.md) | Choosing `value`+`onChange` vs `defaultValue` pattern |
| Responsive Design | [responsive-design.md](references/patterns/responsive-design.md) | Grid breakpoints, adaptive layout, mobile-friendly design |

### Hooks

Import from `@arco-design/web-react/hooks`. Use these headless hooks only when you need a fully custom UI — otherwise prefer the corresponding component.

| Hook | File | Use for |
|------|------|---------|
| useVerificationCode | [use-verification-code.md](references/hooks/use-verification-code.md) | Custom OTP input with focus, paste, keyboard navigation |
| useWatermark | [use-watermark.md](references/hooks/use-watermark.md) | Dynamic canvas watermark with tamper protection |
