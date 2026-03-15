---
name: material-design-3-motion
description: Applies Material Design 3 Expressive motion and animation principles to create natural, intuitive, and engaging user experiences. Use this when implementing animations, transitions, micro-interactions, or when the user asks to apply Material Design 3 motion guidelines.
license: Apache-2.0
---

# Material Design 3 Motion and Animation

## Overview

This skill guides the implementation of Material Design 3 (M3) Expressive motion principles to create springy, natural-feeling animations that enhance usability and delight users.

**Keywords**: Material Design 3, M3, motion, animation, transitions, micro-interactions, easing, duration, spring physics, expressive motion, haptics, physics-based animation

## Core Principles

### Expressive Motion Philosophy

M3 Expressive motion is designed to feel alive, natural, and responsive:

1. **Physics-Based Springs**: Use spring-based animations governed by stiffness, damping, and velocity — replacing traditional cubic-bezier easing for more natural, lively motion
2. **Purposeful Motion**: Every animation should serve a purpose—guiding attention, providing feedback, or showing relationships
3. **Responsive Feel**: Motion responds to user input with appropriate speed and timing
4. **Spatial Coherence**: Elements move in ways that respect spatial relationships and physics
5. **Haptic Integration**: Pair spring animations with platform-native haptic feedback for tactile reinforcement

### Motion Modes

**Expressive Motion** (Default for M3 Expressive):
- Overshoots, bounces, and adds energy
- Ideal for touch interactions and hero moments
- Creates a playful, emotionally resonant feel
- Uses higher spring energy and pronounced bounce

**Standard Motion** (Utilitarian flows):
- Restrained, minimal bounce
- Better for productivity-focused or system-critical flows
- Natural feel without excess playfulness

**Legacy Motion** (Compatibility):
- Traditional easing for backwards compatibility
- Use only when spring physics cannot be applied

### Spring Physics Parameters

M3 Expressive motion uses three key physics parameters instead of traditional time/easing curves:

1. **Stiffness**: Controls how "hard" the spring is — higher stiffness means the animation finishes more quickly
2. **Damping**: Determines how quickly the bounce fades out — a damping value of 1 eliminates bounce completely
3. **Initial Velocity**: Sets the initial speed, influencing overall timing and feel

| Scheme     | Stiffness | Damping | Bounce Effect |
|------------|-----------|---------|---------------|
| Expressive | High      | Medium  | Pronounced overshoot |
| Standard   | Medium    | High    | Minimal/none |

## Animation Types

### 1. Transitions

**Enter Transitions** (Elements appearing):
- Fade + Scale: Elements fade in while scaling from 80% to 100%
- Fade + Slide: Elements slide in from edge while fading
- Container Transform: Morphing one container into another

**Exit Transitions** (Elements disappearing):
- Fade + Scale: Elements scale down to 80% while fading out
- Fade + Slide: Elements slide away while fading
- Keep exits faster than enters (maintain forward momentum)

**Shared Element Transitions** (Between screens/states):
- Morph containers smoothly between views
- Maintain visual continuity
- Use container transform pattern

### 2. Micro-interactions

**Hover States**:
- Subtle elevation change (add shadow)
- Color shift using state layer
- Scale slightly (1.02x-1.05x)
- Duration: 100-200ms

**Focus States**:
- Outline or ring animation
- Scale or elevation change
- Duration: 200-300ms

**Press/Touch States**:
- Ripple effect from touch point
- Scale down slightly (0.98x)
- State layer with opacity
- Duration: 100-150ms

**Loading States**:
- Shimmer or skeleton screens
- Circular progress indicators
- Linear progress bars
- Continuous, smooth motion

### 3. Complex Animations

**Stagger Animations**:
- Animate list items with incremental delay
- Delay between items: 30-50ms
- Creates cascade effect

**Choreographed Animations**:
- Multiple elements moving in coordination
- Use animation-delay for orchestration
- Maintain spatial relationships

**Morphing Shapes**:
- Smooth path interpolation between shapes
- Variable corner radius transitions
- Use for state changes and transformations

## Duration Guidelines

### Standard Durations

**Extra Small** (50-100ms):
- Icon state changes
- Tooltip appearances
- Simple opacity changes

**Small** (100-200ms):
- Button hover states
- Simple scale animations
- Color transitions

**Medium** (200-300ms):
- Modal dialogs
- Navigation transitions
- Card expansions

**Large** (300-500ms):
- Page transitions
- Complex transformations
- Sheet presentations

**Extra Large** (500ms+):
- Major state changes
- Full screen transitions
- Use sparingly

### Context-Based Adjustments

- **Mobile**: Slightly faster (0.8x-0.9x of base duration)
- **Desktop**: Standard durations
- **Reduced Motion**: Reduce to 10-20% of standard duration or disable
- **Large Elements**: Increase duration proportionally

## Spring Physics Implementation

### Expressive Spring (Default for M3 Expressive)

```css
/* CSS with expressive spring-like bezier approximation */
transition-timing-function: cubic-bezier(0.05, 0.7, 0.1, 1.0);

/* Enhanced linear() for expressive spring with overshoot */
transition-timing-function: linear(
  0, 0.004, 0.016 2.5%, 0.063 5%, 0.141, 0.25, 
  0.391 11.3%, 0.563, 0.765, 1.000 20%, 1.066 23.8%, 
  1.109 27.5%, 1.130 31.3%, 1.138 35%, 1.136 38.8%, 
  1.121 46.3%, 1.093 53.8%, 1.057 61.3%, 1.025 68.8%, 
  1.005 77.5%, 0.997 87.5%, 1
);
```

### Standard Spring

```css
/* CSS with standard spring-like bezier approximation */
transition-timing-function: cubic-bezier(0.2, 0.0, 0, 1.0);

/* CSS linear() for better standard spring approximation */
transition-timing-function: linear(
  0, 0.009, 0.035 2.1%, 0.141 4.4%, 0.723 12.9%, 
  0.938 16.7%, 1.017, 1.077, 1.121, 1.149 24.3%, 
  1.159, 1.163, 1.161, 1.154 29.9%, 1.129 32.8%, 
  1.051 39.6%, 1.017 43.1%, 0.991, 0.977 51%, 
  0.974 53.8%, 0.975 57.1%, 0.997 69.8%, 1.003 76.9%, 1
);
```

### JavaScript (Web Animations API)

```javascript
// Expressive spring animation
element.animate(
  [
    { transform: 'scale(0)', opacity: 0 },
    { transform: 'scale(1)', opacity: 1 }
  ],
  {
    duration: 300,
    easing: 'cubic-bezier(0.05, 0.7, 0.1, 1.0)',
    fill: 'forwards'
  }
);

// Standard spring animation
element.animate(
  [
    { transform: 'translateY(20px)', opacity: 0 },
    { transform: 'translateY(0)', opacity: 1 }
  ],
  {
    duration: 250,
    easing: 'cubic-bezier(0.2, 0.0, 0, 1.0)',
    fill: 'forwards'
  }
);
```

### Choosing Expressive vs Standard Motion

| Scenario | Motion Mode | Why |
|----------|-------------|-----|
| Button press feedback | Expressive | User-triggered, benefits from bounce |
| Page transition | Standard | Functional, should not distract |
| Loading completion | Expressive | Celebratory moment of delight |
| Form validation | Standard | Utilitarian feedback |
| FAB expansion | Expressive | Key interaction with visual emphasis |
| List scroll | Standard | Continuous motion, should be smooth |
| Shape morphing | Expressive | Visual storytelling moment |
| Tooltip appearance | Standard | Informational, should not distract |

## Haptics Integration

M3 Expressive recommends pairing spring-driven animations with platform-native haptic feedback:

### Principles

1. **Coordinate with Motion**: Haptic effects should fire at the key moment of the animation (e.g., at the point of overshoot or completion)
2. **Match Intensity**: Gentle haptics for subtle interactions, stronger for significant state changes
3. **Platform-Native**: Use the platform's haptic engine for the most natural feel
4. **Respect Preferences**: Honor user haptic settings and provide accessibility options

### Web Implementation

```javascript
// Pair haptic feedback with expressive motion
function expressivePress(element) {
  // Trigger haptic feedback
  if (navigator.vibrate) {
    navigator.vibrate(10); // Short, subtle haptic
  }
  
  // Trigger spring animation
  element.animate([
    { transform: 'scale(1)' },
    { transform: 'scale(0.95)' },
    { transform: 'scale(1.02)' },
    { transform: 'scale(1)' }
  ], {
    duration: 300,
    easing: 'cubic-bezier(0.05, 0.7, 0.1, 1.0)'
  });
}
```

## Implementation Patterns

### Container Transform

Smoothly morph from one container to another:

```javascript
// Using View Transitions API (modern browsers)
document.startViewTransition(() => {
  // Update DOM
  container.classList.toggle('expanded');
});

// CSS
::view-transition-old(container),
::view-transition-new(container) {
  animation-duration: 300ms;
  animation-timing-function: cubic-bezier(0.2, 0.0, 0, 1.0);
}
```

### Shared Axis Transition

Elements exit and enter along a shared axis:

```css
/* X-axis shared transition */
.exit-left {
  animation: exit-left 300ms cubic-bezier(0.2, 0.0, 0, 1.0);
}

.enter-right {
  animation: enter-right 300ms cubic-bezier(0.2, 0.0, 0, 1.0);
}

@keyframes exit-left {
  from { transform: translateX(0); opacity: 1; }
  to { transform: translateX(-100px); opacity: 0; }
}

@keyframes enter-right {
  from { transform: translateX(100px); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}
```

### Elevation Change

Animate elevation with shadow and transform:

```css
.elevated-card {
  transition: 
    box-shadow 200ms cubic-bezier(0.2, 0.0, 0, 1.0),
    transform 200ms cubic-bezier(0.2, 0.0, 0, 1.0);
}

.elevated-card:hover {
  box-shadow: 
    0px 4px 8px rgba(0, 0, 0, 0.12),
    0px 8px 16px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}
```

### Ripple Effect

Material ripple for touch feedback:

```css
.ripple {
  position: relative;
  overflow: hidden;
}

.ripple::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.5);
  transform: translate(-50%, -50%);
  transition: width 0.3s, height 0.3s;
}

.ripple:active::after {
  width: 300%;
  height: 300%;
}
```

## Best Practices

### Do's

1. ✅ Use spring physics for natural motion
2. ✅ Match animation duration to element size (larger = longer)
3. ✅ Provide immediate feedback for user interactions
4. ✅ Use motion to show relationships between elements
5. ✅ Test animations on lower-end devices
6. ✅ Respect prefers-reduced-motion setting
7. ✅ Use stagger animations to make large datasets feel lighter
8. ✅ Keep motion purposeful and functional

### Don'ts

1. ❌ Don't use linear easing (feels mechanical)
2. ❌ Don't animate too many properties simultaneously
3. ❌ Don't make animations too slow (feels sluggish)
4. ❌ Don't ignore accessibility preferences
5. ❌ Don't use motion purely for decoration
6. ❌ Don't animate layout properties excessively (causes reflow)
7. ❌ Don't use different easing curves randomly

## Accessibility

### Reduced Motion

Always respect user preferences:

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Focus Indicators

Ensure animated focus states are still visible:
- Maintain adequate contrast
- Don't rely solely on motion for focus indication
- Use both color and shape changes

### Performance

- Prefer `transform` and `opacity` (GPU accelerated)
- Avoid animating `width`, `height`, `top`, `left` (causes layout reflow)
- Use `will-change` sparingly for complex animations
- Test on mobile devices and low-end hardware

## Motion Tokens

Define motion tokens for consistency. M3 Expressive introduces tokenized spring-based motion:

```css
:root {
  /* Durations */
  --md-sys-motion-duration-short1: 50ms;
  --md-sys-motion-duration-short2: 100ms;
  --md-sys-motion-duration-short3: 150ms;
  --md-sys-motion-duration-short4: 200ms;
  --md-sys-motion-duration-medium1: 250ms;
  --md-sys-motion-duration-medium2: 300ms;
  --md-sys-motion-duration-medium3: 350ms;
  --md-sys-motion-duration-medium4: 400ms;
  --md-sys-motion-duration-long1: 450ms;
  --md-sys-motion-duration-long2: 500ms;
  --md-sys-motion-duration-long3: 550ms;
  --md-sys-motion-duration-long4: 600ms;
  
  /* Easing — Standard (utilitarian) */
  --md-sys-motion-easing-standard: cubic-bezier(0.2, 0.0, 0, 1.0);
  --md-sys-motion-easing-standard-decelerate: cubic-bezier(0.0, 0.0, 0, 1.0);
  --md-sys-motion-easing-standard-accelerate: cubic-bezier(0.3, 0.0, 1.0, 1.0);
  
  /* Easing — Expressive (default for M3 Expressive) */
  --md-sys-motion-easing-expressive: cubic-bezier(0.05, 0.7, 0.1, 1.0);
  --md-sys-motion-easing-expressive-decelerate: cubic-bezier(0.05, 0.7, 0.1, 1.0);
  --md-sys-motion-easing-expressive-accelerate: cubic-bezier(0.3, 0.0, 0.8, 0.15);
  
  /* Easing — Emphasized (legacy naming, same as expressive) */
  --md-sys-motion-easing-emphasized: cubic-bezier(0.05, 0.7, 0.1, 1.0);
  --md-sys-motion-easing-emphasized-decelerate: cubic-bezier(0.05, 0.7, 0.1, 1.0);
  --md-sys-motion-easing-emphasized-accelerate: cubic-bezier(0.3, 0.0, 0.8, 0.15);
  
  /* Legacy easing */
  --md-sys-motion-easing-legacy: cubic-bezier(0.4, 0.0, 0.2, 1.0);
  
  /* Expressive tokenized motion (new in M3 Expressive) */
  --md-sys-motion-expressive-fast-spatial: cubic-bezier(0.05, 0.7, 0.1, 1.0);
  --md-sys-motion-expressive-fast-effects: cubic-bezier(0.2, 0.0, 0, 1.0);
  --md-sys-motion-expressive-slow-spatial: cubic-bezier(0.05, 0.7, 0.1, 1.0);
  --md-sys-motion-expressive-slow-effects: cubic-bezier(0.2, 0.0, 0, 1.0);
}
```

## Checklist for Motion Implementation

When implementing M3 motion, ensure:

- [ ] Spring-based physics easing is used (not linear or ease-in-out)
- [ ] Expressive vs standard motion modes are chosen appropriately per context
- [ ] Durations match element size and complexity
- [ ] Reduced motion preferences are respected
- [ ] Only transform and opacity are animated (when possible)
- [ ] Hover, focus, and press states have appropriate feedback
- [ ] Page transitions feel smooth and coherent
- [ ] Motion serves a functional purpose
- [ ] Stagger animations are used for lists
- [ ] All animations are tested on mobile devices
- [ ] Motion tokens are defined and used consistently (including expressive tokens)
- [ ] Container transforms are used for view transitions
- [ ] Ripple effects are implemented for touch targets
- [ ] Haptic feedback is coordinated with spring animations where appropriate
- [ ] Shape morphing animations use expressive easing

## Resources

- `examples/motion-patterns.css` — Ready-to-use CSS animation patterns using M3 motion tokens (fade, scale, slide, shared axis, state layer, elevation, and theme transitions). Copy the relevant @keyframes and classes into your project.
- M3 motion overview: https://m3.material.io/styles/motion/overview
- Material Design Tokens (motion): https://github.com/material-foundation/material-tokens
