---
name: ux-best-practices
description: UX patterns for visual hierarchy, error states, loading states, and empty states. Use when designing layouts, handling errors, or building forms.
version: 1.0.0
---

# UX Best Practices

This skill covers UX patterns for creating exceptional user experiences — visual hierarchy, error handling, loading states, and empty states.

## Use-When

This skill activates when:
- Agent designs page layouts
- Agent builds forms with validation
- Agent creates async operations with loading states
- Agent displays lists that might be empty
- Agent handles API errors

## Core Rules

- ALWAYS use consistent spacing from the design system
- ALWAYS show loading states during async operations
- ALWAYS provide clear, specific error messages
- ALWAYS provide empty states for lists/collections
- ALWAYS allow error recovery when possible

## Common Agent Mistakes

- Inconsistent spacing throughout the layout
- Generic error messages like "An error occurred"
- Not disabling buttons during form submission
- Showing empty tables without helpful messaging

## Examples

### ✅ Correct

```tsx
// Consistent spacing
<div className="space-y-4">
  <h1 className="text-2xl font-bold">Title</h1>
  <p>Content</p>
  <Button disabled={isLoading}>
    {isLoading ? "Loading..." : "Submit"}
  </Button>
</div>

// Specific error message
catch {
  toast.error("Failed to save. Please try again.")
}
```

### ❌ Wrong

```tsx
// Random spacing
<div className="p-2">
  <h1 className="mb-3">Title</h1>
  <p className="mb-6">Content</p>
</div>

// Generic error
catch {
  toast.error("An error occurred")
}
```

## References

- [Visual Hierarchy - Nielsen Norman Group](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)
- [Error Message Guidelines - Nielsen Norman Group](https://www.nngroup.com/articles/error-message-guidelines/)
