---
name: onboarding-ux
description: First-time user experience, tooltips, guided tours, and feature discovery. Use when creating onboarding flows, tours, or user education.
version: 1.0.0
---

# Onboarding & UX

This skill covers onboarding patterns — first-time user experience, tooltips, guided tours, and feature discovery.

## Use-When

This skill activates when:
- Agent builds onboarding flows
- Agent creates tooltips or feature highlights
- Agent designs first-time user experiences
- Agent implements feature discovery

## Core Rules

- ALWAYS make onboarding optional and dismissible
- ALWAYS let users skip or complete quickly
- NEVER block access to core features with tours
- PREFER in-context hints over isolated tours
- ALWAYS remember completed onboarding (don't repeat)

## Common Agent Mistakes

- Blocking users until tour completes
- No way to dismiss or skip
- Repeating onboarding on every visit
- Too much information at once
- Annoying users with constant tooltips

## Examples

### ✅ Correct

```tsx
// Dismissible tooltip
<Tooltip content="Click to save" side="top">
  <Button>Save</Button>
</Tooltip>
```

### ❌ Wrong

```tsx
// Blocked access
{!hasSeenTour && <TourBlockingOverlay />}
```

## References

- [Onboarding UX](https://www.nngroup.com/articles/onboarding-ux-101/)
