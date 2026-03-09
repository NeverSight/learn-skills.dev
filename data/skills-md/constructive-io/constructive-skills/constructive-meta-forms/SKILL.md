---
name: constructive-meta-forms
description: Use the _meta GraphQL endpoint on any Constructive app-public DB to introspect table schema at runtime and render fully dynamic CRUD forms with zero static field configuration. Covers DynamicFormCard (create/edit/delete), locked FK pre-fill from context (defaultValues + defaultValueLabels), and the O2M/M2M related-record pattern. Use when building create/edit/delete UI for any Constructive-provisioned table.
compatibility: Next.js 14+ (App Router), Constructive SDK, @tanstack/react-query, graphql-request
metadata:
  author: constructive-io
  version: "2.0.0"
---

# Constructive `_meta` Dynamic Forms

Build fully dynamic CRUD forms for **any** Constructive-provisioned table — zero static field configuration required. The `_meta` query built into every Constructive `app-public` GraphQL endpoint tells you field names, types, required status, FK relationships, and mutation names — all at runtime.

One component. Any table. No codegen needed for forms.

---

## 1. What `_meta` gives you

```graphql
query GetMeta {
  _meta {
    tables {
      name
      fields { name isNotNull hasDefault type { pgType gqlType isArray } }
      inflection { tableType createInputType patchType filterType orderByType }
      query { all one create update delete }
      primaryKeyConstraints { name fields { name } }
      foreignKeyConstraints { name fields { name } referencedTable referencedFields }
      uniqueConstraints { name fields { name } }
    }
  }
}
```

- `fields` → names, types, nullability, defaults — enough to render any input
- `inflection` → exact GraphQL type names for mutations (`CreateContactInput`, `ContactPatch`)
- `query` → exact mutation/query resolver names (`createContact`, `updateContact`, `deleteContact`)
- `foreignKeyConstraints` → which fields are FKs and what table they reference
- **Fetch once with `staleTime: Infinity`** — schema never changes at runtime

---

## 2. TypeScript types

```ts
// src/types/meta.ts
export type MetaField = {
  name: string;
  isNotNull: boolean;
  hasDefault: boolean;
  type: { pgType: string; gqlType: string; isArray: boolean };
};

export type MetaTable = {
  name: string;
  fields: MetaField[];
  inflection: {
    tableType: string;
    createInputType: string;
    patchType: string | null;
    filterType: string | null;
    orderByType: string;
  };
  query: {
    all: string;         // e.g. "contacts"
    one: string | null;  // ⚠️ may be a non-existent root field — see §3 bug note
    create: string | null;
    update: string | null;
    delete: string | null;
  };
  primaryKeyConstraints: Array<{ name: string; fields: { name: string }[] }>;
  foreignKeyConstraints: Array<{
    name: string;
    fields: { name: string }[];
    referencedTable: string;
    referencedFields: string[];
  }>;
  uniqueConstraints: Array<{ name: string; fields: { name: string }[] }>;
};
```

---

## 3. ⚠️ Platform bug: `query.one` returns a non-existent root field

`_meta.query.one` returns the **singular** name (e.g. `"contact"`) but the Constructive GraphQL root only exposes **plural** queries (e.g. `contacts`). Using `query.one` as the root field will fail.

**Fix — always use `query.all` + `condition: { id: $id }`:**

```ts
function buildFetchQuery(table: MetaTable): string {
  const fieldNames = table.fields.map((f) => f.name).join('\n    ');
  // Use query.all with a condition filter + read nodes[0]
  // DO NOT use query.one — it returns a non-existent root field name
  return `
    query DynamicFetch($id: UUID!) {
      ${table.query.all}(condition: { id: $id }) {
        nodes { ${fieldNames} }
      }
    }
  `;
}

// Read the result:
const result = data[table.query.all].nodes[0] as Record<string, unknown> | undefined;
```

---

## 4. `useMeta` / `useTableMeta` hooks

```ts
// src/lib/meta/use-meta.ts
'use client';
import { useQuery } from '@tanstack/react-query';
import { CRM_ENDPOINT } from '@/components/crm/crm-provider';
import { TokenManager } from '@/lib/auth/token-manager';
import type { MetaTable } from '@/types/meta';

const META_QUERY = `query GetMeta {
  _meta {
    tables {
      name
      fields { name isNotNull hasDefault type { pgType gqlType isArray } }
      inflection { tableType createInputType patchType filterType orderByType }
      query { all one create update delete }
      primaryKeyConstraints { name fields { name } }
      foreignKeyConstraints { name fields { name } referencedTable referencedFields }
      uniqueConstraints { name fields { name } }
    }
  }
}`;

async function fetchMeta(): Promise<{ _meta: { tables: MetaTable[] } }> {
  const { token } = TokenManager.getToken('schema-builder');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  };
  if (token) headers['Authorization'] = `Bearer ${token.accessToken}`;
  const res = await fetch(CRM_ENDPOINT, {
    method: 'POST', headers,
    body: JSON.stringify({ query: META_QUERY }),
  });
  if (!res.ok) throw new Error(`_meta fetch failed: ${res.status}`);
  const json = await res.json();
  if (json.errors?.length) throw new Error(json.errors[0].message ?? '_meta error');
  return json.data;
}

export function useMeta() {
  return useQuery({ queryKey: ['_meta'], queryFn: fetchMeta, staleTime: Infinity });
}

export function useTableMeta(tableName: string): MetaTable | null {
  const { data } = useMeta();
  return data?._meta.tables.find((t) => t.name === tableName) ?? null;
}
```

---

## 5. Field renderer utilities

```ts
// src/lib/meta/field-renderer.ts
import type { MetaField } from '@/types/meta';

/** System fields — always skip in forms (auto-managed by Constructive) */
export const SYSTEM_FIELDS = new Set([
  'id', 'entityId', 'createdAt', 'updatedAt',
  'created_at', 'updated_at', 'entity_id',
]);

export type FieldInputType =
  | 'text' | 'textarea' | 'number' | 'boolean'
  | 'date' | 'datetime' | 'uuid' | 'json' | 'select' | 'hidden';

const TEXTAREA_HINTS = ['bio', 'description', 'notes', 'body', 'content', 'summary', 'details'];

export function getInputType(field: MetaField, isForeignKey: boolean): FieldInputType {
  if (SYSTEM_FIELDS.has(field.name)) return 'hidden';
  if (isForeignKey) return 'select';
  const pg = field.type.pgType.toLowerCase();
  switch (pg) {
    case 'text': case 'varchar': case 'citext':
      return TEXTAREA_HINTS.some((h) => field.name.toLowerCase().includes(h)) ? 'textarea' : 'text';
    case 'int2': case 'int4': case 'int8':
    case 'float4': case 'float8': case 'numeric': return 'number';
    case 'bool': case 'boolean': return 'boolean';
    case 'date': return 'date';
    case 'timestamp': case 'timestamptz': return 'datetime';
    case 'uuid': return 'uuid';
    case 'json': case 'jsonb': return 'json';
    default: return 'text';
  }
}

/**
 * A field is required if it's NOT NULL AND has no server-side default.
 * hasDefault=true = Constructive auto-generates the value (ids, timestamps, etc.) — never require in forms.
 */
export function isRequiredField(field: MetaField): boolean {
  return field.isNotNull && !field.hasDefault;
}

/** camelCase → "Title Case" label */
export function toLabel(fieldName: string): string {
  return fieldName.replace(/([A-Z])/g, ' $1').replace(/^./, (s) => s.toUpperCase()).trim();
}
```

### Required field rule

| `isNotNull` | `hasDefault` | In form |
|---|---|---|
| `true` | `false` | Required input |
| `true` | `true` | Skip in create (id, timestamps), optional in edit |
| `false` | anything | Optional input |

---

## 6. `DynamicField` component

Handles all pgTypes automatically. Add `locked` + `lockedLabel` for pre-filled FK context (see §8).

```tsx
// src/components/crm/dynamic-field.tsx
'use client';
import { Field } from '@/components/ui/field';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Switch } from '@/components/ui/switch';
import { Textarea } from '@/components/ui/textarea';
import { getInputType, SYSTEM_FIELDS, toLabel } from '@/lib/meta/field-renderer';
import type { MetaField } from '@/types/meta';
import { Lock } from 'lucide-react';

type DynamicFieldProps = {
  field: MetaField;
  value: unknown;
  onChange: (value: unknown) => void;
  isForeignKey?: boolean;
  /** Pre-set from context — visible but not editable */
  locked?: boolean;
  /** Human-readable label for locked field (e.g. "Kristopher Floyd" instead of a UUID) */
  lockedLabel?: string;
  error?: string;
};

export function DynamicField({
  field, value, onChange,
  isForeignKey = false, locked = false, lockedLabel, error,
}: DynamicFieldProps) {
  if (SYSTEM_FIELDS.has(field.name)) return null;

  const inputType = getInputType(field, isForeignKey);
  const label = toLabel(field.name);
  const required = field.isNotNull && !field.hasDefault;

  // ── Locked: visible, disabled, not editable ──
  if (locked) {
    const displayValue = lockedLabel ?? (typeof value === 'string' ? value : String(value ?? ''));
    return (
      <Field label={label} required={false}>
        <div className="relative">
          <Input
            value={displayValue}
            readOnly disabled
            className="bg-muted/40 pr-8 text-muted-foreground cursor-default"
          />
          <Lock className="absolute right-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground/60" />
        </div>
        {lockedLabel && (
          <p className="mt-1 text-xs text-muted-foreground font-mono">{String(value)}</p>
        )}
      </Field>
    );
  }

  if (inputType === 'hidden') return null;

  if (inputType === 'boolean') {
    return (
      <div className="flex items-center gap-3 py-1">
        <Switch id={field.name} checked={(value as boolean) ?? false} onCheckedChange={onChange} />
        <Label htmlFor={field.name} className="cursor-pointer">{label}</Label>
        {error && <p className="text-destructive text-sm">{error}</p>}
      </div>
    );
  }

  if (inputType === 'textarea') {
    return (
      <Field label={label} required={required} error={error}>
        <Textarea value={(value as string) ?? ''} onChange={(e) => onChange(e.target.value)} rows={4} />
      </Field>
    );
  }

  if (inputType === 'json') {
    return (
      <Field label={label} required={required} error={error} description="JSON value">
        <Textarea
          value={typeof value === 'string' ? value : JSON.stringify(value ?? null, null, 2)}
          onChange={(e) => { try { onChange(JSON.parse(e.target.value)); } catch { onChange(e.target.value); } }}
          rows={6} className="font-mono text-xs"
        />
      </Field>
    );
  }

  if (inputType === 'number') {
    return (
      <Field label={label} required={required} error={error}>
        <Input type="number" value={(value as number) ?? ''}
          onChange={(e) => onChange(e.target.value === '' ? undefined : Number(e.target.value))} />
      </Field>
    );
  }

  if (inputType === 'date') {
    return (
      <Field label={label} required={required} error={error}>
        <Input type="date" value={(value as string) ?? ''} onChange={(e) => onChange(e.target.value)} />
      </Field>
    );
  }

  if (inputType === 'datetime') {
    return (
      <Field label={label} required={required} error={error}>
        <Input type="datetime-local" value={(value as string) ?? ''} onChange={(e) => onChange(e.target.value)} />
      </Field>
    );
  }

  if (inputType === 'uuid') {
    return (
      <Field label={label} required={required} error={error}>
        <Input value={(value as string) ?? ''} onChange={(e) => onChange(e.target.value)}
          placeholder="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" className="font-mono" />
      </Field>
    );
  }

  if (inputType === 'select') {
    // FK field — raw UUID input until EntitySearch is built
    return (
      <Field label={label} required={required} error={error} description="Foreign key — paste UUID">
        <Input value={(value as string) ?? ''} onChange={(e) => onChange(e.target.value)}
          placeholder={`${label} ID…`} className="font-mono text-sm" />
      </Field>
    );
  }

  return (
    <Field label={label} required={required} error={error}>
      <Input value={(value as string) ?? ''} onChange={(e) => onChange(e.target.value)} />
    </Field>
  );
}
```

---

## 7. `DynamicFormCard` — full implementation

```tsx
// src/components/crm/dynamic-form-card.tsx
'use client';
import { useMemo, useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import type { CardComponent } from '@/components/ui/stack';
import { useCardReady } from '@/components/ui/stack';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { showSuccessToast, showErrorToast } from '@/components/ui/toast';
import { SYSTEM_FIELDS, isRequiredField } from '@/lib/meta/field-renderer';
import { useTableMeta } from '@/lib/meta/use-meta';
import { DynamicField } from './dynamic-field';
import { Loader2 } from 'lucide-react';
import { CRM_ENDPOINT } from '@/components/crm/crm-provider';
import { TokenManager } from '@/lib/auth/token-manager';
import type { MetaTable } from '@/types/meta';

export type DynamicFormCardProps = {
  /** Constructive table type name, e.g. 'Contact', 'Note', 'Deal' */
  tableName: string;
  /** Existing record ID — omit for create mode */
  recordId?: string;
  /**
   * Pre-set field values from context (typically FK fields).
   * e.g. { contactId: "uuid" } when adding a Note from a Contact page.
   * These fields are rendered as visible-but-locked (disabled, 🔒 icon).
   */
  defaultValues?: Record<string, unknown>;
  /**
   * Human-readable display labels for locked fields.
   * e.g. { contactId: "Kristopher Floyd" } → shows name, UUID as helper text.
   */
  defaultValueLabels?: Record<string, string>;
  /** Called after successful save or delete */
  onSuccess?: () => void;
};

async function crmRequest(query: string, variables?: Record<string, unknown>) {
  const { token } = TokenManager.getToken('schema-builder');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json', Accept: 'application/json',
  };
  if (token) headers['Authorization'] = `Bearer ${token.accessToken}`;
  const res = await fetch(CRM_ENDPOINT, {
    method: 'POST', headers, body: JSON.stringify({ query, variables }),
  });
  if (!res.ok) throw new Error(`GraphQL error: ${res.status}`);
  const json = await res.json();
  if (json.errors?.length) throw new Error(json.errors[0].message);
  return json.data;
}

function buildFetchQuery(table: MetaTable): string {
  const fields = table.fields.map((f) => f.name).join('\n      ');
  // Use query.all + condition — NOT query.one (platform bug: query.one is non-existent root field)
  return `
    query DynamicFetch($id: UUID!) {
      ${table.query.all}(condition: { id: $id }) {
        nodes { ${fields} }
      }
    }
  `;
}

export const DynamicFormCard: CardComponent<DynamicFormCardProps> = ({
  tableName, recordId, defaultValues, defaultValueLabels, onSuccess, card,
}) => {
  const isEditMode = !!recordId;
  const { isReady } = useCardReady();
  const tableMeta = useTableMeta(tableName);
  const queryClient = useQueryClient();

  // Seed formValues with defaultValues so locked fields are in place immediately
  const [formValues, setFormValues] = useState<Record<string, unknown>>(defaultValues ?? {});
  const [initialized, setInitialized] = useState(false);
  const [fieldErrors, setFieldErrors] = useState<Record<string, string>>({});
  const [isSaving, setIsSaving] = useState(false);

  const fkFields = useMemo(
    () => new Set(tableMeta?.foreignKeyConstraints.flatMap((fk) => fk.fields.map((f) => f.name)) ?? []),
    [tableMeta],
  );

  const editableFields = useMemo(
    () => tableMeta?.fields.filter((f) => !SYSTEM_FIELDS.has(f.name)) ?? [],
    [tableMeta],
  );

  // Locked = pre-set from defaultValues, cannot be changed by user
  const lockedFields = useMemo(
    () => new Set(Object.keys(defaultValues ?? {})),
    [defaultValues],
  );

  const { data: existingData, isLoading: isLoadingRecord } = useQuery({
    queryKey: ['dynamic-record', tableName, recordId],
    queryFn: async () => {
      const query = buildFetchQuery(tableMeta!);
      const data = await crmRequest(query, { id: recordId });
      return (data[tableMeta!.query.all]?.nodes?.[0] ?? null) as Record<string, unknown> | null;
    },
    enabled: isReady && isEditMode && !!tableMeta,
    staleTime: 0,
  });

  // Initialize form from existing record — locked fields take precedence
  if (existingData && !initialized) {
    const initial: Record<string, unknown> = { ...(defaultValues ?? {}) };
    for (const field of editableFields) {
      if (!lockedFields.has(field.name) && existingData[field.name] !== undefined) {
        initial[field.name] = existingData[field.name];
      }
    }
    setFormValues(initial);
    setInitialized(true);
  }

  const setFieldValue = (name: string, value: unknown) => {
    setFormValues((prev) => ({ ...prev, [name]: value }));
    setFieldErrors((prev) => { const next = { ...prev }; delete next[name]; return next; });
  };

  // Validate — skip locked fields (always satisfied by caller)
  const validate = (): boolean => {
    const errors: Record<string, string> = {};
    for (const field of editableFields) {
      if (lockedFields.has(field.name)) continue;
      if (isRequiredField(field)) {
        const val = formValues[field.name];
        if (val === undefined || val === null || val === '') {
          errors[field.name] = `${field.name} is required`;
        }
      }
    }
    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSave = async () => {
    if (!tableMeta || !validate()) return;
    setIsSaving(true);
    try {
      const input: Record<string, unknown> = {};
      for (const field of editableFields) {
        const val = formValues[field.name];
        if (val !== undefined && val !== '') input[field.name] = val;
      }

      if (isEditMode) {
        const mutation = `
          mutation DynamicUpdate($id: UUID!, $patch: ${tableMeta.inflection.patchType}!) {
            ${tableMeta.query.update}(input: { id: $id, patch: $patch }) { clientMutationId }
          }`;
        await crmRequest(mutation, { id: recordId, patch: input });
      } else {
        const mutation = `
          mutation DynamicCreate($input: ${tableMeta.inflection.createInputType}!) {
            ${tableMeta.query.create}(input: { input: $input }) { clientMutationId }
          }`;
        await crmRequest(mutation, { input });
      }

      await queryClient.invalidateQueries({ queryKey: [tableMeta.query.all] });
      if (isEditMode) await queryClient.invalidateQueries({ queryKey: ['dynamic-record', tableName, recordId] });
      showSuccessToast({ message: isEditMode ? `${tableName} updated` : `${tableName} created` });
      onSuccess?.();
      card.close();
    } catch (err) {
      showErrorToast({
        message: `Failed to ${isEditMode ? 'update' : 'create'} ${tableName}`,
        description: err instanceof Error ? err.message : 'Unknown error',
      });
    } finally {
      setIsSaving(false);
    }
  };

  const handleDelete = () => {
    if (!tableMeta || !recordId) return;
    card.push({
      id: `confirm-delete-${recordId}`,
      title: `Delete ${tableName}?`,
      description: 'This cannot be undone.',
      Component: ConfirmDeleteCard,
      props: {
        tableName, recordId,
        deleteMutation: tableMeta.query.delete!,
        tableType: tableMeta.inflection.tableType,
        listQueryKey: tableMeta.query.all,
        onSuccess: () => { onSuccess?.(); card.close(); },
      },
      width: 400,
    });
  };

  if (!tableMeta || (isEditMode && isLoadingRecord && !initialized)) {
    return (
      <div className="flex h-full flex-col p-4 space-y-4">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="space-y-2">
            <Skeleton className="h-4 w-28" />
            <Skeleton className="h-9 w-full" />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 space-y-4 overflow-y-auto p-4">
        {editableFields.map((field) => (
          <DynamicField
            key={field.name}
            field={field}
            value={formValues[field.name]}
            onChange={(val) => setFieldValue(field.name, val)}
            isForeignKey={fkFields.has(field.name)}
            locked={lockedFields.has(field.name)}
            lockedLabel={defaultValueLabels?.[field.name]}
            error={fieldErrors[field.name]}
          />
        ))}
        {editableFields.length === 0 && (
          <p className="text-muted-foreground py-8 text-center text-sm">No editable fields.</p>
        )}
      </div>
      <div className="flex items-center justify-between border-t px-4 py-3">
        {isEditMode && tableMeta.query.delete ? (
          <Button variant="destructive" size="sm" onClick={handleDelete} disabled={isSaving}>Delete</Button>
        ) : <div />}
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => card.close()} disabled={isSaving}>Cancel</Button>
          <Button onClick={handleSave} disabled={isSaving}>
            {isSaving
              ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" />Saving…</>
              : isEditMode ? 'Save Changes' : `Create ${tableName}`}
          </Button>
        </div>
      </div>
    </div>
  );
};
```

### ConfirmDeleteCard (add in same file)

```tsx
type ConfirmDeleteCardProps = {
  tableName: string; recordId: string; deleteMutation: string;
  tableType: string; listQueryKey: string; onSuccess?: () => void;
};

const ConfirmDeleteCard: CardComponent<ConfirmDeleteCardProps> = ({
  tableName, recordId, deleteMutation, tableType, listQueryKey, onSuccess, card,
}) => {
  const queryClient = useQueryClient();
  const [isDeleting, setIsDeleting] = useState(false);

  const handleConfirm = async () => {
    setIsDeleting(true);
    try {
      const mutation = `mutation DynamicDelete($id: UUID!) {
        ${deleteMutation}(input: { id: $id }) { deleted${tableType}Id }
      }`;
      await crmRequest(mutation, { id: recordId });
      await queryClient.invalidateQueries({ queryKey: [listQueryKey] });
      showSuccessToast({ message: `${tableName} deleted` });
      onSuccess?.(); card.close();
    } catch (err) {
      showErrorToast({
        message: `Failed to delete ${tableName}`,
        description: err instanceof Error ? err.message : 'Unknown error',
      });
      setIsDeleting(false);
    }
  };

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 p-4">
        <p className="text-muted-foreground text-sm">
          Are you sure you want to delete this {tableName.toLowerCase()}? This cannot be undone.
        </p>
      </div>
      <div className="flex justify-end gap-2 border-t px-4 py-3">
        <Button variant="outline" onClick={() => card.close()} disabled={isDeleting}>Cancel</Button>
        <Button variant="destructive" onClick={handleConfirm} disabled={isDeleting}>
          {isDeleting ? <><Loader2 className="mr-2 h-4 w-4 animate-spin" />Deleting…</> : `Delete ${tableName}`}
        </Button>
      </div>
    </div>
  );
};
```

---

## 8. Locked FK pre-fill — related records from context

When opening a form from a parent record page (e.g. adding a Note from a Contact detail page), pass `defaultValues` to pre-set and lock the FK field. The user sees it but cannot change it.

```tsx
// On Kristopher Floyd's contact page:
const contactFullName = `${contact.firstName} ${contact.lastName}`;

// ── Create a new note (+ Add Note button) ──
stack.push({
  id: `add-note-${contactId}`,
  title: 'Add Note',
  description: `New note for ${contactFullName}`,
  Component: DynamicFormCard,
  props: {
    tableName: 'Note',
    defaultValues: { contactId },              // pre-set FK, locked
    defaultValueLabels: { contactId: contactFullName }, // show name, not UUID
    onSuccess: () => queryClient.invalidateQueries({ queryKey: noteKeys.lists() }),
  },
  width: 480,
});

// ── Edit an existing note (click note row) ──
stack.push({
  id: `edit-note-${noteId}`,
  title: 'Edit Note',
  Component: DynamicFormCard,
  props: {
    tableName: 'Note',
    recordId: noteId,
    defaultValues: { contactId },              // locked even in edit — can't reassign owner
    defaultValueLabels: { contactId: contactFullName },
    onSuccess: () => queryClient.invalidateQueries({ queryKey: noteKeys.lists() }),
  },
  width: 480,
});
```

**How it renders:**
- `Contact Id` field → disabled input showing "Kristopher Floyd" + 🔒 icon
- UUID shown as small helper text below
- Field cannot be changed by user
- Value is included in the save mutation automatically
- Validation skips locked fields (they're always satisfied)

**Generic rule:** `defaultValues` works for any FK on any table. The `_meta` FK constraint map tells you which fields are FKs — you don't need to hardcode anything.

---

## 9. Usage patterns

```tsx
import { DynamicFormCard } from '@/components/crm/dynamic-form-card';

// ── Create any record ──
stack.push({ id: 'new-contact', title: 'New Contact',
  Component: DynamicFormCard, props: { tableName: 'Contact' }, width: 480 });

// ── Edit any record ──
stack.push({ id: `edit-${id}`, title: 'Edit Contact',
  Component: DynamicFormCard, props: { tableName: 'Contact', recordId: id }, width: 480 });

// ── Related record (O2M) from parent page ──
stack.push({ id: `add-note-${contactId}`, title: 'Add Note',
  Component: DynamicFormCard,
  props: { tableName: 'Note', defaultValues: { contactId }, defaultValueLabels: { contactId: name } },
  width: 480 });

// ── Any table, same API ──
stack.push({ id: 'new-deal', title: 'New Deal',
  Component: DynamicFormCard, props: { tableName: 'Deal' }, width: 480 });
```

---

## 10. pgType → input type reference

| pgType | Input | Notes |
|---|---|---|
| `text`, `varchar`, `citext` | `<Input>` | `<Textarea>` if name contains bio/description/notes/body |
| `int2/4/8`, `float4/8`, `numeric` | `<Input type="number">` | |
| `bool`, `boolean` | `<Switch>` | |
| `date` | `<Input type="date">` | |
| `timestamp`, `timestamptz` | `<Input type="datetime-local">` | |
| `uuid` (FK) | Locked or UUID input | Use `defaultValues` to lock from context; future: `<EntitySearch>` |
| `uuid` (non-FK) | `<Input>` mono | Rare — raw UUID |
| `json`, `jsonb` | `<Textarea>` mono | JSON.parse / stringify |

---

## 11. Future extensions

| Feature | How |
|---|---|
| **EntitySearch for FK fields** | Replace `select` case in `DynamicField` with an `<EntitySearch tableName={fk.referencedTable}>` component that fetches + autocompletes |
| **Array fields** | Handle `isArray: true` in MetaField — render `<TagInput>` for `text[]` |
| **Enum fields** | Query `__schema` for enum values — render `<Select>` |
| **Package** | Extract `DynamicFormCard`, `DynamicField`, `useMeta`, field-renderer into `@constructive/meta-forms` npm package so any Constructive-backed app gets this for free |

---

## 12. Troubleshooting

| Issue | Fix |
|---|---|
| Single-record fetch fails / field empty | **Use `query.all + condition: { id: $id }` and read `nodes[0]`** — `query.one` returns a non-existent root field (platform bug) |
| `_meta` returns empty tables | Check auth headers — `_meta` requires an authenticated request |
| Mutation fails with GraphQL type error | Verify `inflection.patchType` / `createInputType` match your schema version |
| Form shows no editable fields | All fields in `SYSTEM_FIELDS` — check provisioned columns |
| Required validation on system fields | Bug — verify `SYSTEM_FIELDS` set covers all auto-managed field names |
| Edit form is empty on open | Check `useCardReady()` gate — data fetches only after card animation completes |
| FK shows UUID instead of name | Use `defaultValueLabels` prop, or build `EntitySearch` (future work) |
| `hasDefault=true` field marked required | Bug in `isRequiredField` — must check `!hasDefault` |
