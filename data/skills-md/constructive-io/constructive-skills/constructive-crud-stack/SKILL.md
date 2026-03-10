---
name: constructive-crud-stack
description: Build CRUD actions as Stack cards (iOS-style slide-in panels) for any Constructive CRM. Covers the Stack card trigger pattern, CardComponent structure, the card API (close/push/setTitle), useCardReady for deferred loading, and stacked confirm-delete. For dynamic forms that introspect _meta at runtime, see the constructive-meta-forms skill.
compatibility: Next.js 14+ (App Router), Constructive SDK, @constructive/stack, @tanstack/react-query
metadata:
  author: constructive-io
  version: "2.0.0"
---

# Constructive CRUD Stack Cards

Build any create/edit/delete action as a slide-in Stack card. Cancel/Save/Delete CTAs live in a sticky footer. Cards stack naturally — e.g., pushing a confirm-delete card on top of an edit card.

---

## 1. Stack Card Trigger

Every CRUD action opens a card. Push it from any button, row click, or link:

```tsx
'use client';
import { useCardStack } from '@/components/ui/stack';
import { EditContactCard } from './edit-contact-card';

function EditContactButton({ contactId }: { contactId: string }) {
  const stack = useCardStack();

  return (
    <Button
      onClick={() =>
        stack.push({
          id: `edit-contact-${contactId}`,
          title: 'Edit Contact',
          description: 'Update contact details.',
          Component: EditContactCard,
          props: { contactId },
          width: 480,
        })
      }
    >
      Edit
    </Button>
  );
}
```

---

## 2. Card Component Structure

Every card is a `CardComponent<Props>` — TypeScript enforces the injected `card` prop:

```tsx
'use client';
import type { CardComponent } from '@/components/ui/stack';
import { Button } from '@/components/ui/button';
import { Field } from '@/components/ui/field';
import { Input } from '@/components/ui/input';

export type EditContactCardProps = {
  contactId: string;
  onSuccess?: () => void;
};

export const EditContactCard: CardComponent<EditContactCardProps> = ({
  contactId,
  onSuccess,
  card,       // ← injected: card.close(), card.push(), card.setTitle(), etc.
}) => {
  const [name, setName] = useState('');

  const handleSave = async () => {
    await updateContact({ id: contactId, name });
    showSuccessToast({ message: 'Contact updated' });
    onSuccess?.();
    card.close();
  };

  return (
    <div className='flex h-full flex-col'>
      {/* ── Scrollable Form Body ── */}
      <div className='flex-1 space-y-4 overflow-y-auto p-4'>
        <Field label='Name'>
          <Input value={name} onChange={(e) => setName(e.target.value)} />
        </Field>
        {/* more fields... */}
      </div>

      {/* ── Sticky Footer ── */}
      <div className='flex items-center justify-between border-t px-4 py-3'>
        <Button variant='destructive' onClick={handleDelete}>Delete</Button>
        <div className='flex gap-2'>
          <Button variant='outline' onClick={() => card.close()}>Cancel</Button>
          <Button onClick={handleSave}>Save</Button>
        </div>
      </div>
    </div>
  );
};
```

---

## 3. Card API (`card` prop — injected by CardStackProvider)

| Method | Description |
|---|---|
| `card.close()` | Dismiss this card with animation |
| `card.push({ id, title, Component, props, width? })` | Push a new card on top of the stack |
| `card.setTitle(title)` | Update card header title dynamically |
| `card.setDescription(desc)` | Update subtitle |
| `card.updateProps(patch)` | Patch card props from inside the card |

### `card.push` behavior

By default, `card.push()` replaces all cards above the current card, then pushes the new one. Use `{ append: true }` to push purely on top without replacing:

```tsx
card.push({ id: '...', Component: MyCard, props: {...} });                  // default: replaces above
card.push({ id: '...', Component: MyCard, props: {...} }, { append: true }); // pure append
```

---

## 4. Deferred Data Loading (`useCardReady`)

Use `useCardReady()` to delay data fetching until the card's enter animation completes. This prevents janky mid-animation fetches and dropped frames:

```tsx
import { useCardReady } from '@/components/ui/stack';

export const EditContactCard: CardComponent<Props> = ({ contactId }) => {
  const { isReady } = useCardReady();  // true after ~220ms (animation completes)

  const { data } = useContactQuery({
    variables: { id: contactId },
    enabled: isReady,  // ← only fetches after animation
  });

  if (!isReady || !data) {
    return <ContactFormSkeleton />;
  }
  // ... render form
};
```

---

## 5. Stacked Confirm Delete

Push a confirm card instead of an alert dialog. Stacks visually over the edit card:

```tsx
const handleDeleteClick = () => {
  card.push({
    id: `confirm-delete-${contactId}`,
    title: 'Delete Contact?',
    description: 'This cannot be undone.',
    Component: ConfirmDeleteCard,
    props: {
      message: 'Are you sure you want to delete this contact?',
      onConfirm: async () => {
        await deleteContact({ id: contactId });
        showSuccessToast({ message: 'Contact deleted' });
        card.close();  // closes confirm card (top of stack)
        card.close();  // closes edit card
      },
    },
    width: 400,
  });
};

// ── ConfirmDeleteCard ──
type ConfirmDeleteCardProps = {
  message: string;
  onConfirm: () => Promise<void>;
};

const ConfirmDeleteCard: CardComponent<ConfirmDeleteCardProps> = ({ message, onConfirm, card }) => {
  const [isDeleting, setIsDeleting] = useState(false);
  const handleConfirm = async () => {
    setIsDeleting(true);
    try { await onConfirm(); }
    finally { setIsDeleting(false); }
  };

  return (
    <div className='flex h-full flex-col'>
      <div className='flex-1 p-4'>
        <p className='text-muted-foreground text-sm'>{message}</p>
      </div>
      <div className='flex justify-end gap-2 border-t px-4 py-3'>
        <Button variant='outline' onClick={() => card.close()} disabled={isDeleting}>Cancel</Button>
        <Button variant='destructive' onClick={handleConfirm} disabled={isDeleting}>
          {isDeleting ? 'Deleting…' : 'Delete'}
        </Button>
      </div>
    </div>
  );
};
```

---

## 6. CardStackProvider Setup (Root Layout)

The provider must be high in the tree so all pages can push cards. Include `ClientOnlyStackViewport` to avoid hydration mismatches:

```tsx
// app/layout.tsx
import { CardStackProvider } from '@/components/ui/stack';
import { ClientOnlyStackViewport } from '@/components/client-only-stack-viewport';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        <CardStackProvider layoutMode='side-by-side' defaultPeekOffset={48}>
          {children}
          <ClientOnlyStackViewport />
        </CardStackProvider>
      </body>
    </html>
  );
}
```

---

## 7. CardSpec Options (Full Reference)

```ts
stack.push({
  id: 'unique-card-id',            // required — prevents duplicate cards
  title: 'Edit Contact',           // shown in card header
  description: 'Update details',   // subtitle in header
  headerSize: 'md',                // 'sm' | 'md' | 'lg'
  Component: EditContactCard,      // CardComponent<Props>
  props: { contactId },            // typed props (excluding injected card prop)
  width: 480,                      // default: 480px
  peekOffset: 24,                  // px peeking behind cards above (default: 48)
  allowCover: false,               // allow being fully covered (default: false)
  backdrop: true,                  // show backdrop behind stack (default: true)
  onClose: () => console.log('closed'),  // callback on any close method
});
```

---

## 8. Using DynamicFormCard (from `constructive-meta-forms`)

Combine both skills: the Stack card trigger pattern (this skill) with schema-driven forms (constructive-meta-forms). `DynamicFormCard` introspects `_meta` at runtime and renders the correct inputs for any table — no static field config needed:

```tsx
import { DynamicFormCard } from '@/components/crm/dynamic-form-card';
import { useCardStack } from '@/components/ui/stack';

function ContactDetailPage({ contactId }) {
  const stack = useCardStack();

  const handleEdit = () => {
    stack.push({
      id: `edit-contact-${contactId}`,
      title: 'Edit Contact',
      description: 'Update contact fields.',
      Component: DynamicFormCard,  // from constructive-meta-forms
      props: {
        tableName: 'Contact',
        recordId: contactId,
      },
      width: 480,
    });
  };

  return <Button onClick={handleEdit}>Edit</Button>;
}
```

For static forms with handcrafted fields (more control over layout/validation), use the `CardComponent` pattern from Section 2 above.

---

## Troubleshooting

| Issue | Solution |
|---|---|
| `useCardStack must be used within a CardStackProvider` | Ensure `CardStackProvider` is in root `layout.tsx` |
| Card doesn't slide in | Check `ClientOnlyStackViewport` is mounted (prevents hydration mismatch) |
| Card pushes but nothing appears | Verify `CardStackViewport` (or `ClientOnlyStackViewport`) is rendered in tree |
| Stale card props after update | Use `card.updateProps(patch)` or re-push with new props |
