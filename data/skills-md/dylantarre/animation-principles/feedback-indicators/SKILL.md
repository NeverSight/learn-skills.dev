---
name: feedback-indicators
description: Use when confirming user actions - success checkmarks, error alerts, form validation, save confirmations, or any animation acknowledging what the user did.
---

# Feedback Indicator Animations

Apply Disney's 12 principles to action confirmation animations.

## Principle Application

**Squash & Stretch**: Success checkmarks can scale with overshoot. Compress on draw, expand on complete.

**Anticipation**: Brief gather before feedback appears. 50ms of preparation before the confirmation.

**Staging**: Feedback appears at the action location. Button shows checkmark, field shows validation.

**Straight Ahead vs Pose-to-Pose**: Define feedback states: neutral → processing → success/error.

**Follow Through & Overlapping**: Icon animates, then label appears. Stagger confirmation elements.

**Slow In/Slow Out**: Success: ease-out (confident arrival). Error: ease-in-out (shake settles).

**Arcs**: Checkmarks draw in arcs, not straight lines. Error X's cross naturally.

**Secondary Action**: Checkmark draws + color shifts + scale bounces for rich feedback.

**Timing**:
- Instant feedback: 100-200ms (form validation)
- Success confirmation: 300-500ms (checkmark draw)
- Error indication: 400ms (shake + message)
- Auto-dismiss: 2000-4000ms after appearance

**Exaggeration**: Success deserves celebration. Overshoot scale to 1.2, bold colors, confident motion.

**Solid Drawing**: Feedback icons must be clear at a glance. Recognition in 100ms or less.

**Appeal**: Positive feedback should feel rewarding. Negative feedback firm but not punishing.

## Timing Recommendations

| Feedback Type | Duration | Auto-dismiss | Easing |
|--------------|----------|--------------|--------|
| Inline Validation | 150ms | No | ease-out |
| Checkmark Draw | 400ms | 3000ms | ease-out |
| Success Toast | 300ms | 4000ms | ease-out |
| Error Shake | 400ms | No | ease-in-out |
| Error Toast | 300ms | 6000ms | ease-out |
| Save Indicator | 200ms | 2000ms | ease-out |

## Implementation Patterns

```css
/* Checkmark draw */
.checkmark {
  stroke-dasharray: 50;
  stroke-dashoffset: 50;
  animation: draw-check 400ms ease-out forwards;
}

@keyframes draw-check {
  to { stroke-dashoffset: 0; }
}

/* Success with scale */
.success-icon {
  animation: success 500ms cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
}

@keyframes success {
  0% { transform: scale(0); opacity: 0; }
  60% { transform: scale(1.2); opacity: 1; }
  100% { transform: scale(1); opacity: 1; }
}

/* Error shake */
.error-shake {
  animation: shake 400ms ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-6px); }
  40%, 80% { transform: translateX(6px); }
}

/* Inline validation */
.field-valid {
  animation: valid-pop 200ms ease-out;
}

@keyframes valid-pop {
  0% { transform: scale(0.8); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
```

## SVG Checkmark Pattern

```html
<svg class="checkmark" viewBox="0 0 24 24">
  <circle cx="12" cy="12" r="10" fill="#10B981"/>
  <path
    class="check-path"
    d="M7 13l3 3 7-7"
    stroke="white"
    stroke-width="2"
    fill="none"
  />
</svg>
```

## Auto-Dismiss Pattern

```javascript
// Show success, auto-hide
element.classList.add('success-visible');

setTimeout(() => {
  element.classList.remove('success-visible');
  element.classList.add('success-hidden');
}, 3000);
```

## Key Rules

1. Feedback must appear within 100ms of action
2. Success states: celebrate briefly, don't linger
3. Error states: persist until user acknowledges
4. Always provide text alongside icons for accessibility
5. `prefers-reduced-motion`: instant state, no animation
