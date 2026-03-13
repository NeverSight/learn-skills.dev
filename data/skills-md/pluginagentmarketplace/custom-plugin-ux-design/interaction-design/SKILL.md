---
name: interaction-design
description: Master interaction design - patterns, micro-interactions, user flows, affordances, feedback
sasmp_version: "1.3.0"
bonded_agent: 03-interaction-design
bond_type: PRIMARY_BOND
---

# Interaction Design Skill

> **Atomic Skill**: Design intuitive interactions that guide users through seamless experiences

## Purpose

This skill provides frameworks for designing responsive, accessible, and delightful user interactions.

## Skill Invocation

```
Skill("custom-plugin-ux-design:interaction-design")
```

## Parameter Schema

### Input Parameters
```typescript
interface InteractionDesignParams {
  // Required
  type: "pattern" | "microinteraction" | "flow" | "feedback" | "gesture";
  context: string;

  // Optional
  platform?: "web" | "mobile" | "desktop";
  interaction_model?: "touch" | "mouse" | "keyboard" | "voice" | "hybrid";
  accessibility?: {
    reduced_motion?: boolean;
    keyboard_only?: boolean;
  };
}
```

### Validation Rules
```yaml
type:
  type: enum
  required: true
  values: [pattern, microinteraction, flow, feedback, gesture]

context:
  type: string
  required: true
  min_length: 10

platform:
  type: enum
  default: "web"
```

## Execution Flow

```
INTERACTION DESIGN EXECUTION
────────────────────────────────────────────

Step 1: UNDERSTAND USER GOALS
├── Identify user intent
├── Map expected outcomes
└── Define success criteria

Step 2: DESIGN TRIGGERS
├── Define interaction triggers
├── Specify input methods
└── Consider accessibility

Step 3: CREATE RESPONSE
├── Design visual feedback
├── Specify timing/easing
└── Add audio/haptic (optional)

Step 4: HANDLE STATES
├── Success state
├── Error state
├── Loading state
└── Empty state

Step 5: DOCUMENT & TEST
├── Create specifications
├── Prototype interactions
└── Validate with users

────────────────────────────────────────────
```

## Retry Logic

```yaml
retry_config:
  max_attempts: 3
  backoff_type: exponential
  initial_delay_ms: 500
  max_delay_ms: 5000
  retryable_errors:
    - ANIMATION_RENDER_FAILED
    - PROTOTYPE_SYNC_ERROR
```

## Logging Hooks

```typescript
interface InteractionLog {
  timestamp: string;
  event: "interaction_start" | "feedback_shown" | "complete" | "error";
  interaction_type: string;
  duration_ms: number;
  success: boolean;
}
```

## Learning Modules

### Module 1: Interaction Patterns
```
COMMON PATTERNS
├── Navigation
│   ├── Tab navigation
│   ├── Sidebar toggle
│   └── Breadcrumbs
├── Data Entry
│   ├── Form validation
│   ├── Autocomplete
│   └── Date pickers
├── Content
│   ├── Infinite scroll
│   ├── Pull to refresh
│   └── Expand/collapse
└── Actions
    ├── Drag and drop
    ├── Swipe actions
    └── Long press
```

### Module 2: Micro-interactions
```
MICRO-INTERACTION ANATOMY
├── Trigger (user action)
├── Rules (what happens)
├── Feedback (visual response)
└── Loops/Modes (ongoing state)

TIMING GUIDELINES
├── Instant: 0-100ms (feedback)
├── Fast: 100-300ms (transitions)
├── Normal: 300-500ms (animations)
└── Slow: 500ms+ (complex sequences)

EASING CURVES
├── ease-out: Deceleration (entering)
├── ease-in: Acceleration (exiting)
├── ease-in-out: Smooth (moving)
└── spring: Natural (bouncy)
```

### Module 3: User Flows
```
FLOW DESIGN PRINCIPLES
├── Minimize steps to goal
├── Provide clear progress
├── Allow easy recovery
├── Confirm destructive actions
└── Remember user state

FLOW COMPONENTS
├── Entry points
├── Decision points
├── Action points
├── Exit points
└── Error paths
```

### Module 4: Affordances
```
AFFORDANCE TYPES
├── Explicit (buttons, links)
├── Pattern-based (icons, gestures)
├── Hidden (shortcuts, gestures)
└── Negative (disabled states)

SIGNIFIERS
├── Visual cues (icons, arrows)
├── Text labels
├── Cursor changes
├── Animation hints
└── Sound cues
```

### Module 5: Feedback Systems
```
FEEDBACK TYPES
├── Visual (color, motion)
├── Auditory (sounds, voice)
├── Haptic (vibration)
└── Systemic (notifications)

FEEDBACK TIMING
├── Immediate: < 100ms
├── Responsive: 100-300ms
├── Perceived: 300-1000ms
└── Delayed: > 1000ms (show progress)
```

## Error Handling

| Error Code | Description | Recovery |
|------------|-------------|----------|
| `IX-001` | Missing feedback | Add visual response |
| `IX-002` | Gesture conflict | Redesign gesture |
| `IX-003` | Animation jank | Optimize performance |
| `IX-004` | Unclear affordance | Add signifiers |
| `IX-005` | Dead-end flow | Add escape routes |

## Troubleshooting

### Problem: Users miss interactions
```
Diagnosis:
├── Check: Affordance visibility
├── Check: Position in hierarchy
├── Check: Size and contrast
└── Solution: Enhance discoverability

Steps:
1. Conduct findability test
2. Increase visual prominence
3. Add onboarding hints
4. Consider progressive disclosure
```

### Problem: Interactions feel slow
```
Diagnosis:
├── Check: Animation duration
├── Check: Easing curves
├── Check: Response delay
└── Solution: Optimize timing

Steps:
1. Measure time to feedback
2. Reduce to 100-300ms range
3. Use appropriate easing
4. Add immediate micro-feedback
```

## Unit Test Templates

```typescript
describe("InteractionDesignSkill", () => {
  describe("pattern validation", () => {
    it("should include trigger and feedback", async () => {
      const result = await invoke({
        type: "pattern",
        context: "form submission"
      });
      expect(result.pattern.trigger).toBeDefined();
      expect(result.pattern.feedback).toBeDefined();
    });
  });

  describe("microinteraction timing", () => {
    it("should stay within timing guidelines", async () => {
      const result = await invoke({
        type: "microinteraction",
        context: "button click"
      });
      expect(result.animation.duration_ms).toBeLessThanOrEqual(300);
    });
  });

  describe("accessibility", () => {
    it("should provide reduced motion alternative", async () => {
      const result = await invoke({
        type: "microinteraction",
        accessibility: { reduced_motion: true }
      });
      expect(result.animation.reduced_motion_fallback).toBeDefined();
    });
  });
});
```

## Quality Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Task completion | > 95% | User success rate |
| Time to feedback | < 100ms | Perceived responsiveness |
| Animation FPS | 60fps | Frame rate |
| Accessibility | 100% | Keyboard navigable |

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-30 | Production-grade upgrade |
