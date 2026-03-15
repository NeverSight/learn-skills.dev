---
name: posthog-instrumentation
description: Automatically add PostHog analytics instrumentation to code. Triggers when user asks to add tracking, instrument events, add analytics, or implement feature flags in their codebase.
---

# PostHog Instrumentation Skill

Help users add PostHog analytics, event tracking, and feature flags to their code.

## When to Use

- User asks to "add PostHog" or "add analytics"
- User wants to track events or user actions
- User needs to implement feature flags
- User asks about instrumenting their code

## Workflow

1. Identify the framework (React, Next.js, Python, Node.js, etc.)
2. Check for existing PostHog setup
3. Add appropriate instrumentation

## Code Patterns

### JavaScript/TypeScript
```javascript
// Event tracking
posthog.capture('button_clicked', { button_name: 'signup' })

// Feature flags
if (posthog.isFeatureEnabled('new-feature')) {
  // Show new feature
}

// User identification
posthog.identify(userId, { email: user.email })
```

### Python
```python
from posthog import Posthog
posthog = Posthog(api_key='<ph_project_api_key>')

# Event tracking
posthog.capture(distinct_id='user_123', event='purchase_completed')

# Feature flags
if posthog.feature_enabled('new-feature', 'user_123'):
    # Show new feature
```

### React
```jsx
import { usePostHog } from 'posthog-js/react'

function MyComponent() {
  const posthog = usePostHog()

  const handleClick = () => {
    posthog.capture('button_clicked')
  }
}
```

## Best Practices

- Use consistent event naming (snake_case recommended)
- Include relevant properties with events
- Identify users early in their session
- Use feature flags for gradual rollouts
