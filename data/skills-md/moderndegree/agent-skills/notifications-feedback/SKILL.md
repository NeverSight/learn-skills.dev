---
name: notifications-feedback
description: Toast notifications, alerts, feedback messages, and their timing. Use when adding user feedback, success messages, or alerts.
version: 1.0.0
---

# Notifications & Feedback

This skill covers notification patterns — toast types, placement, timing, and dismissible patterns for providing user feedback.

## Use-When

This skill activates when:
- Agent adds success/error/warning toasts
- Agent provides user feedback
- Agent creates notification systems
- Agent builds alert components

## Core Rules

- ALWAYS use appropriate toast type (success, error, warning, info)
- ALWAYS allow dismissing notifications
- ALWAYS position toasts consistently (usually top-right or bottom-center)
- ALWAYS auto-dismiss non-critical toasts (3-5 seconds)
- NEVER stack more than 3 toasts at once
- NEVER use toasts for critical info requiring user action

## Common Agent Mistakes

- Wrong toast type for message (error shown as success)
- Toasts that can't be dismissed
- Toasts that disappear too quickly or stay too long
- Stacking too many toasts
- Using toasts for critical alerts

## Examples

### ✅ Correct

```tsx
// Appropriate toast usage
<Toast variant="success" onDismiss={() => {}}>
  Changes saved successfully
</Toast>

<Toast variant="error" action={{ label: 'Retry', onClick: retry }}>
  Failed to save. Would you like to retry?
</Toast>
```

### ❌ Wrong

```tsx
// Generic message
<Toast>Something happened</Toast>

// Can't dismiss
<div className="toast">
  Message
</div>
```

## References

- [Toast Notification UX](https://www.nngroup.com/articles/toast-notifications/)
