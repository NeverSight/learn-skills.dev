---
name: dialogs-modals
description: Modal and dialog patterns, confirmations, destructive actions, and focus management. Use when building modals, dialogs, or confirmation dialogs.
version: 1.0.0
---

# Dialogs & Modals

This skill covers modal and dialog design — when to use them, confirmation patterns, destructive actions, and focus management for accessibility.

## Use-When

This skill activates when:
- Agent builds modal or dialog components
- Agent creates confirmation dialogs
- Agent designs destructive action warnings
- Agent needs focus trap implementation
- Agent builds alerts or prompts

## Core Rules

- ALWAYS trap focus inside modal when open
- ALWAYS return focus to trigger when modal closes
- ALWAYS allow closing with Escape key
- ALWAYS include a close button
- NEVER use modals for critical flows that must complete
- NEVER trap users in modals without escape

## Common Agent Mistakes

- No focus trap (tab escapes modal)
- Focus not returned to trigger on close
- No close button or Escape key support
- Using modals for everything (annoying)
- Missing destructive action warnings

## Examples

### ✅ Correct

```tsx
<Dialog open={isOpen} onOpenChange={setIsOpen}>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>Delete Item</DialogTitle>
      <DialogDescription>
        Are you sure you want to delete this item? This action cannot be undone.
      </DialogDescription>
    </DialogHeader>
    <DialogFooter>
      <Button variant="outline" onClick={() => setIsOpen(false)}>
        Cancel
      </Button>
      <Button variant="destructive" onClick={handleDelete}>
        Delete
      </Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### ❌ Wrong

```tsx
// No focus management
<div className={isOpen ? 'block' : 'hidden'}>
  <div>Modal content</div>
  <button onClick={onClose}>Close</button>
</div>

// No way to close
<div className="modal">
  Important content
</div>
```

## References

- [WAI-ARIA Dialog Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialogmodal/)
- [Modal UX Guidelines](https://www.nngroup.com/articles/modal-window/)
