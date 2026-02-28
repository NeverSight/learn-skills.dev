---
name: cogover-fe
description: Cogover Frontend UI Kit (components, forms, hooks, design tokens), commit convention, i18n. Use when writing/reviewing UI code, creating commits, or translating text.
license: MIT
metadata:
  author: cogover
  version: "3.1.0"
---

# Cogover Frontend Skill

## Quy trình bắt buộc

Mô hình **routing table + on-demand reference**. File này = index. Chi tiết nằm trong `reference/`.

### Khi nhận task:

1. Đọc file này (đã load) → xác định reference files liên quan
2. Dùng **Read tool** đọc từ `{skill_base_dir}/reference/<name>.md`
3. Áp dụng quy tắc khi implement. Tuân theo DO/DON'T chính xác
4. Commit/i18n → đọc `{skill_base_dir}/reference/commit-convention.md` hoặc `i18n-translation.md`

### Quy tắc:
- **CHỈ đọc reference liên quan** task hiện tại, KHÔNG đọc hết
- Task phức tạp → đọc song song nhiều Read calls
- Delegate subagent → truyền nội dung reference vào prompt (subagent không đọc được skill files)
- Import component/hook → luôn từ `@stringeecom/ui-kit`
- Text mới → viết tiếng Việt trước, dịch i18n khi được yêu cầu
- Date/Time → luôn dùng `dayjs`
- Không tự tạo git commit trừ khi user yêu cầu
- Tách task độc lập → sub agent song song

### Styling Foundations (BẮT BUỘC khi viết UI):
- **Colors** → dùng configured tokens (`text-primary-main`, `bg-surface-default`), KHÔNG raw hex/rgb/Tailwind default (`bg-blue-500`)
- **Spacing** → dùng `rem` (`p-[1rem]`, `gap-[0.5rem]`), KHÔNG `px` (`p-[16px]`). Quy đổi: 1rem = 16px
- **Typography** → dùng `prose-*` classes (`prose-body2`, `prose-h2`), KHÔNG `text-[14px] font-semibold`
- **className** → dùng `cx()` với grouped args theo concern, KHÔNG string concat/template literals
- **Tokens** → kiểm tra `tailwind.config.js` trước, KHÔNG hardcode values

## Reference Files

### Foundation & Workflow
`color-palette-usage` · `cx-class-grouping` · `spacing-rem-only` · `tokens-tailwind-config` · `typography-prose-classes` · `no-auto-markdown` · `no-typescript-any` · `prettier-and-lint-check` · `uikit-import-source` · `uikit-text-vietnamese-first` · `uikit-no-auto-commit` · `uikit-parallel-sub-agents` · `commit-convention` · `i18n-translation`

### Data & Query
`uikit-object-field-record` · `uikit-tanstack-query-hooks` · `dayjs-date-time`

### Form System
`uikit-form-react-hook-form` · `uikit-form-builder` · `uikit-form-item` · `uikit-form-control-label`

### Page Pattern
`page-list-resource` — 10 rules (RULE-LIST-PAGE-01→10): directory structure, types, options, FormProvider+URL sync, table+debounce, helpers, columns hook, FilterMenu, ActionMenu, data flow

### Common Components
`uikit-alert` · `uikit-avatar` · `uikit-avatar-field` · `uikit-breadcrumbs` · `uikit-button` · `uikit-button-group` · `uikit-icon-button` · `uikit-tooltip` · `uikit-smart-tooltip` · `uikit-checkbox` · `uikit-checkbox-group` · `uikit-ckeditor` · `uikit-collapsible-container` · `uikit-confirm-modal` · `uikit-copy-link-button` · `uikit-created-by-info` · `uikit-date-picker` · `uikit-date-range-calendar` · `uikit-date-range-picker` · `uikit-draggable-wrapper` · `uikit-draggable-item` · `uikit-drawer` · `uikit-file-preview` · `uikit-filter-generator` · `uikit-filter-generator-base` · `uikit-help-button` · `uikit-horizontal-steps` · `uikit-insert-field-object-v2` · `uikit-insert-field-object-button-v2` · `uikit-insert-field-object-button-wrapper2` · `uikit-layout-select-button` · `uikit-limitable-list` · `uikit-list-view-table` · `uikit-modal` · `uikit-popper` · `uikit-reaction` · `uikit-resize-bar` · `uikit-skeleton` · `uikit-step-progress-bar` · `uikit-steps` · `uikit-stringee-dnd-context` · `uikit-table` · `uikit-table-settings` · `uikit-tabs` · `uikit-tag` · `uikit-text-link` · `uikit-vertical-steps` · `uikit-usage-help-button`

### Form Inputs
`uikit-duration-input` · `uikit-duration-range-input` · `uikit-email-input` · `uikit-emoji-control-picker` · `uikit-emoji-picker` · `uikit-file-input` · `uikit-input-group` · `uikit-input-number` · `uikit-markdown-editor` · `uikit-monaco-editor` · `uikit-multiple-select` · `uikit-phone-input` · `uikit-radio` · `uikit-radio-group` · `uikit-rating` · `uikit-search-input` · `uikit-select` · `uikit-slider` · `uikit-switch` · `uikit-tags-input` · `uikit-text-field` · `uikit-time-picker` · `uikit-time-range-picker` · `uikit-time-select` · `uikit-tree-select` · `uikit-url-input`

### Hooks
`uikit-use-force-update` · `uikit-use-get-data-field-by-slug` · `uikit-use-get-data-field-option-label` · `uikit-use-get-field-label` · `uikit-use-get-layout` · `uikit-use-get-record-page-link` · `uikit-use-get-state-from-search-params` · `uikit-use-histories-state` · `uikit-use-merge-record-filters` · `uikit-use-merged-refs` · `uikit-use-replace-record-value` · `uikit-use-save-to-search-params` · `uikit-use-sync-state`

### Notifications & Toast
`showToastMessage` → xem trong bất kỳ reference file component nào

> Path: `{skill_base_dir}/reference/<name>.md`
