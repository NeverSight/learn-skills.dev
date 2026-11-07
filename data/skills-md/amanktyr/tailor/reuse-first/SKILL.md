---
name: reuse-first
description: Enforces reuse-first software engineering. Prevents duplicate components, utilities, hooks, functions, CSS classes, and abstractions by searching existing workspace code first.
---

# Reuse-First Engineering Skill

Activate this skill before creating any new component, utility function, hook, service, database helper, or CSS class.

> **Operational Directive:** *Never build from scratch what already exists in the codebase.*

---

## 1. Automated AST Catalog Search

Before writing new code, query the workspace symbol catalog or execute the duplicate finder:

```bash
# Search for matching components, hooks, or functions in workspace
node skills/reuse-first/scripts/find-duplicates.js modal
node skills/reuse-first/scripts/find-duplicates.js user
node skills/reuse-first/scripts/find-duplicates.js fetch
```

---

## 2. Semantic Synonym Lookup Matrix

Inspect concept synonyms rather than searching for exact names only:

| Requested Concept | Potential Matches & Synonyms to Inspect First |
| :--- | :--- |
| **Modal / Dialog** | `Dialog`, `Popup`, `Sheet`, `Drawer`, `Modal`, `AlertModal`, `ConfirmBox` |
| **Toast / Notification** | `Notification`, `Snackbar`, `Banner`, `Toast`, `Message`, `Alert` |
| **Data Fetcher / API** | `getUser`, `fetchUser`, `loadUser`, `findUser`, `queryUser`, `userService`, `apiClient` |
| **Date Formatting** | `formatDate`, `formatTimestamp`, `parseDate`, `dateUtils`, `timeAgo`, `Intl.DateTimeFormat` |
| **Button / CTA** | `Button`, `IconButton`, `ActionButton`, `SubmitBtn`, `LinkButton` |
| **Dropdown / Picker** | `Select`, `Combobox`, `MenuSelect`, `DropdownMenu`, `Autocomplete` |
| **Form Inputs** | `Input`, `TextField`, `FormField`, `Checkbox`, `RadioGroup`, `Switch` |
| **Table / Grid** | `DataTable`, `Table`, `DataGrid`, `VirtualList`, `Pagination` |

---

## 3. Decision Framework: Parameterize vs Create New

When a matching component or utility is identified:

```
┌────────────────────────────────────────────────────────┐
│ Is semantic similarity >= 70%?                         │
└───────────────────────────┬────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
           YES                              NO
            │                               │
┌───────────▼────────────┐      ┌───────────▼────────────┐
│ Can it be extended with │      │ Are domain boundaries  │
│ optional props/params  │      │ completely distinct?   │
│ without breaking       │      └───────────┬────────────┘
│ existing callers?      │                  │
└───────────┬────────────┘                 YES
            │                               │
     ┌──────┴──────┐            ┌───────────▼────────────┐
    YES            NO           │ Implement new focused  │
     │             │            │ abstraction. Document  │
┌────▼───────┐ ┌───▼──────────┐ │ in .ai/ architecture.  │
│ EXTEND &   │ │ EXTRACT      │ └────────────────────────┘
│ REUSE      │ │ shared base  │
└────────────┘ │ & specialize │
               └──────────────┘
```

### Bad Pattern (Blind Duplication)
Creating `DeleteConfirmModal.tsx` with 150 lines of duplicate backdrop, CSS transitions, and keyboard event handlers when `Dialog.tsx` already exists.

### Good Pattern (Clean Parameterization)
```tsx
import { Dialog } from '@/components/ui/Dialog';

export function DeleteConfirmModal({ isOpen, onClose, onConfirm, itemName }: Props) {
  return (
    <Dialog
      isOpen={isOpen}
      onClose={onClose}
      title={`Delete ${itemName}?`}
      variant="destructive"
      onConfirm={onConfirm}
    >
      <p>This action cannot be undone.</p>
    </Dialog>
  );
}
```

---

## 4. When NOT to Reuse (Engineering Judgment)

Do NOT force reuse if:
1. **Security Risk:** The existing code has known vulnerabilities, insecure deserialization, or lacks authorization checks.
2. **Obsolete / Deprecated Code:** The existing component is marked `@deprecated` or scheduled for retirement in an ADR.
3. **Unwanted Coupling:** Reusing it would couple two independent bounded domains (e.g., coupling Billing internals with Marketing).
4. **Brittle Complexity:** Reusing it requires more than 3 boolean flags, fragile nested conditionals, or CSS `!important` overrides.
