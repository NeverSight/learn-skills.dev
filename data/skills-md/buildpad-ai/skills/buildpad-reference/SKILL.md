---
name: buildpad-reference
description: Buildpad UI component catalog and Buildpad-First rule reference. Lists all 40+ available components, hooks, services, and types. Enforces that raw Mantine form/input components must not be used when Buildpad provides equivalents. Automatically loaded as background context.
user-invokable: false
---

# Buildpad Component Reference

## Buildpad-First Rule (MANDATORY)

Before creating ANY custom component, check if Buildpad provides it. If available, use it via CLI.

| ❌ DO NOT Use Directly              | ✅ Use Buildpad Instead        |
| ----------------------------------- | ------------------------------ |
| `useForm` from @mantine/form        | `VForm`, `CollectionForm`      |
| `<DatePicker>` from @mantine/dates  | `DateTime` component           |
| `<Dropzone>` from @mantine/dropzone | `Files`, `Upload` components   |
| `<TextInput>` directly              | `Input` component              |
| `<Select>` directly                 | `SelectDropdown` component     |
| `<Checkbox>` directly               | `SelectMultipleCheckbox`       |
| `<Switch>` directly                 | `Toggle`, `Boolean` components |
| Custom `<Table>` for records        | `CollectionList` component     |
| Custom filter UI                    | `FilterPanel` component        |

Basic Mantine layout components (`Stack`, `Group`, `Button`, `Modal`, `Table`) are fine to use directly.

## Component Catalog (40+)

**Input**: Input, Textarea, InputCode, Tags, RichTextHtml, RichTextMarkdown, InputBlockEditor
**Selection**: SelectDropdown, SelectRadio, SelectMultipleCheckbox, SelectMultipleCheckboxTree, SelectMultipleDropdown, AutocompleteAPI, CollectionItemDropdown, SelectIcon
**Boolean**: Boolean, Toggle
**DateTime**: DateTime, Slider
**Files**: FileInterface, FileImage, Files, Upload
**Media**: Color, Map, MapWithRealMap
**Relations**: ListM2M, ListM2O, ListO2M, ListM2A (+ render-prop variants: ListM2MInterface, ListM2OInterface, ListO2MInterface)
**Layout**: Divider, Notice, GroupDetail
**System**: SystemPermissions
**Collections**: CollectionForm, CollectionList, CollectionListToolbar, CollectionListFooter, BulkActionsBar, DeleteConfirmModal, BottomPagination, FilterPanel
**Form**: VForm, FormField, FormFieldLabel, FormFieldInterface
**Table**: VTable (presentation table with sort, resize, reorder, header context menus)
**Workflow**: WorkflowButton

## Opt-in Modules (scaffolded whole via CLI)

These are ready-made, multi-screen experiences — installed with their own CLI command, not composed by hand. Use the dedicated skill for each.

| Module | Package | Screens / API | Skill |
| ------------- | ------------------- | -------------------------------------------------------------------------------- | -------------------------------------------------- |
| **Files**     | `@buildpad/ui-files` | `FileManager` (`/files` library) + `FileDetail` (`/files/[id]`); `useFiles`, `useFolders` hooks; `getAssetUrl` thumbnails | [add-files](../add-files/SKILL.md) |
| **Form Builder** | `@buildpad/ui-forms` | `FormBuilder` (visual author) + `DynamicForm` (runtime); `FormDefinition` model in `fb_definitions`; `useFormDefinitions` hook | [create-form-builder](../create-form-builder/SKILL.md) |
| **Workflows** | `@buildpad/ui-workflows` | `WorkflowsManager` (`/workflows`) + `WorkflowDetail` (state-diagram editor); `WorkflowAssignmentsManager`/`WorkflowAssignmentDetail`; `WorkflowInstancesManager`/`WorkflowInstanceDetail`; `useWorkflowDefinitions`, `useWorkflowAssignments`, `useWorkflowInstances` hooks with typed `DaaSRequestError` | [add-workflows](../add-workflows/SKILL.md) |
| **Cron Jobs** | `@buildpad/ui-cron` | `CronJobsManager` (`/cron`: jobs list + run History tab) + `CronJobDetail` (`/cron/[id]`: code editor slot, settings, per-job history); `CronRunsTable`, `CronRunLogModal`; `useCronJobs`, `useCronRuns` hooks with typed `DaaSRequestError` | [add-cron](../add-cron/SKILL.md) |
| **AI Chat** | `@buildpad/ui-chat` | `AiChatPanel` (docked right panel) or `AiChatWidget` (floating bubble), `AiChatButton` ("Ask AI", ⌘I) under `AiChatProvider`, `AiChat` for a custom shell, `AiChatContextChip`; backends `chocolateFactoryBackend` (browser-direct, CLI target `ai-chat-routes`, the default and the one that streams on Amplify) and `routeBackend` (server proxy, `ai-chat-proxy-routes`); talks to a Chocolate Factory agent, not to the data API | [add-ai-chat](../add-ai-chat/SKILL.md) |

`getAssetUrl` builds URLs for the app's `/api/assets/[id]` proxy. On a Supabase project that proxy serves file content. On an Engine project files are stored and served by the Engine: `/api/files`, `/api/folders`, `/api/files/signed-url`, and file content at `/api/files/assets/:id` (with a session or a signed token). A file shown in a browser, a public one included, is loaded through a signed URL from `/api/files/signed-url`, not by an anonymous read: an `<img>` element or a link sends no `X-Tenant-Id`. Set no storage bucket option: the Engine stores files on its own disk or in S3. The generated `/api/assets/[id]` proxy forwards to a path the Engine does not serve, so on an Engine project show a file through a signed URL from `/api/files/signed-url` rather than through `getAssetUrl`; see [add-files](../add-files/SKILL.md).

Note the naming: the field-level `Files`/`Upload` widgets and the `VForm`/`CollectionForm` runtime above are the *substrate*; `FileManager`/`FileDetail` and `FormBuilder`/`DynamicForm` are the full **modules** built on top of them.

## Available Hooks

```tsx
// Auth
import { useAuth, usePermissions } from "@/lib/buildpad/hooks";

// Relations
import { useRelationM2M, useRelationM2MItems } from "@/lib/buildpad/hooks";
import { useRelationM2O, useRelationM2OItem } from "@/lib/buildpad/hooks";
import { useRelationO2M, useRelationO2MItems } from "@/lib/buildpad/hooks";
import { useRelationM2A, useRelationM2AItems } from "@/lib/buildpad/hooks";

// Utilities
import {
  useFiles,
  useSelection,
  usePreset,
  useEditsGuard,
} from "@/lib/buildpad/hooks";

// Versioning & Workflow
import {
  useVersions,
  useWorkflowAssignment,
  useWorkflowVersioning,
} from "@/lib/buildpad/hooks";
```

## Utility Functions

```tsx
import { isNewItem, isExistingItem } from "@/lib/buildpad/utils";
```

| Function             | Description                                                                                                                       |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `isNewItem(id)`      | Returns `true` for `"+"`, `"%2B"`, `"new"`, `null`, `undefined`, `""`. Use this everywhere instead of inline `id === "+"` checks. |
| `isExistingItem(id)` | Inverse of `isNewItem()` with type guard — narrows to `string \| number`.                                                         |

**MANDATORY**: Always use `isNewItem()` in detail pages and any code that checks if an item is being created vs edited. Never write `id === "+"` or `id === "%2B"` inline — the utility handles all sentinel values including URL-encoded variants.

## CollectionForm Usage

```tsx
import { CollectionForm } from '@/components/ui/collection-form';

// Create mode
<CollectionForm collection="articles" onSuccess={(item) => router.push(`/articles/${item.id}`)} />

// Edit mode
<CollectionForm collection="articles" id={itemId} mode="edit" onSuccess={handleSave} />
```

CollectionForm automatically fetches schema, renders all 40+ field types, handles validation and submission.

## CollectionList Usage (MANDATORY for ALL Listing Views)

Every page or module that displays a list of collection records **MUST** use `CollectionList`.
Do NOT build custom tables with Mantine `<Table>` or raw `<table>` for collection data.

`CollectionList` provides a complete content-module-style layout:

- Action toolbar (CollectionListToolbar) with search, filter toggle, archive filter dropdown, refresh, bulk actions, and create button
- Integrated `FilterPanel` with active filter count badge
- Permission-gated create button and bulk actions (disabled with "Not allowed" tooltip when lacking permission)
- Built-in CRUD permission gating (auto-fetches `GET /permissions/me`, disables buttons when not allowed)
- Built-in delete workflow with confirmation modal, API call, and auto-refresh via `enableDelete`
- Pagination with configurable page sizes (10, 25, 50, 100) and item count display (CollectionListFooter)
- Field-type-aware cell rendering (booleans → ✓/✗, dates → formatted, numbers → localized, JSON → badge, UUID → truncated with tooltip)
- Column sorting, resizing, reordering via VTable composition
- Archive filtering (all/archived/unarchived) when `archiveField` is set

On an Engine project the Engine answers a delete with `204 No Content` and no body: code that reads a delete's answer must not expect a JSON body.

CRUD permissions are handled automatically — do not manually gate create/delete buttons or pass permission state. Use `bulkActions` only for custom operations beyond CRUD (e.g., Archive, Export).

### Full-Featured CollectionList (preferred pattern)

```tsx
import { CollectionList } from "@/components/ui";

<CollectionList
  collection="articles"
  enableSearch
  enableFilter
  enableSelection
  enableCreate
  enableDelete
  enableSort
  enableResize
  enableReorder
  enableHeaderMenu
  archiveField="status"
  archiveValue="archived"
  unarchiveValue="draft"
  limit={25}
  onCreate={() => router.push(`/content/articles/+`)}
  onItemClick={(item) => router.push(`/content/articles/${item.id}`)}
/>;
```

### BulkAction Interface (for custom operations beyond CRUD)

```tsx
interface BulkAction {
  label: string;
  icon?: React.ReactNode;
  color?: string;
  confirm?: boolean;
  /** When set, the action button is disabled if the user lacks this permission */
  requiredPermission?: "create" | "update" | "delete";
  action: (selectedIds: (string | number)[]) => void | Promise<void>;
}
```

### Permission-Aware Patterns

CollectionList and CollectionForm automatically resolve CRUD permissions from `GET /permissions/me`:

- **Admin bypass**: users whose policies grant `admin_access` (detected via `PermissionsService.isAdmin`) get full CRUD access and see all fields regardless of per-collection permissions
- **Create button**: disabled with tooltip when user lacks create permission
- **Bulk actions**: individually disabled based on `requiredPermission` field
- **Delete button**: built-in delete with confirmation when `enableDelete` is set (requires delete permission)
- **Field visibility**: columns filtered to only readable fields (admins see all fields)
- **Archive actions**: requires both update permission and archive field access

```tsx
// Permission state can be observed via callback
<CollectionList
  collection="articles"
  enableCreate
  onCreate={() => router.push("/content/articles/+")}
  onPermissionsLoaded={(perms) => {
    // perms: { createAllowed, readAllowed, updateAllowed, deleteAllowed, archiveAllowed }
    console.log("Can create:", perms.createAllowed);
  }}
/>
```

## Component Dependencies

| Component                              | Requires                                                                                                               |
| -------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| file-image, file, files                | upload                                                                                                                 |
| list-m2m, list-m2o, list-o2m, list-m2a | hooks, services, collection-form, collection-list                                                                      |
| vform                                  | ALL interface components (32+)                                                                                         |
| collection-form                        | vform + all interfaces                                                                                                 |
| collection-list                        | vtable (VTable), filter-panel, collection-list-toolbar, collection-list-footer, bulk-actions-bar, delete-confirm-modal |
| filter-panel                           | types                                                                                                                  |

## References

- [React component patterns](references/react-components.instructions.md)
